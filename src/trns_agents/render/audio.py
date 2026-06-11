from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

from ..models import Segment

# Timeline placement (task 009 — anchor start_ms + mild overlap policy):
# 1. play_at = start_ms always (sync with video).
# 2. Budget = min(end_ms, next.start_ms) - play_at; fit TTS with mild atempo then trim.
# 3. Short overlaps are acceptable; avoids sequential cursor drift (task 008 v2).

_CHUNK_SIZE = 40
_MAX_TEMPO = float(os.environ.get("TRNS_TTS_MAX_TEMPO", "1.15"))


def _ffmpeg_bin() -> str:
    found = shutil.which("ffmpeg")
    if found:
        return found
    winget = Path.home() / "AppData/Local/Microsoft/WinGet/Packages"
    for candidate in winget.glob("Gyan.FFmpeg*/ffmpeg-*/bin/ffmpeg.exe"):
        return str(candidate)
    return "ffmpeg"


def _ffprobe_bin() -> str:
    ffmpeg = Path(_ffmpeg_bin())
    probe = ffmpeg.parent / ("ffprobe.exe" if ffmpeg.suffix else "ffprobe")
    return str(probe) if probe.exists() else "ffprobe"


def _probe_duration_ms(path: Path) -> int:
    cmd = [
        _ffprobe_bin(),
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(path),
    ]
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return max(int(float(result.stdout.strip()) * 1000), 1)


@dataclass(frozen=True)
class _Placement:
    seg: Segment
    play_at_ms: int
    tts_ms: int
    source_tts_ms: int
    atempo: float = 1.0
    trimmed: bool = False


def _slot_budget_ms(seg: Segment, next_seg: Segment | None) -> int:
    play_at = seg.start_ms
    limits: list[int] = []
    if seg.end_ms > play_at:
        limits.append(seg.end_ms - play_at)
    if next_seg is not None and next_seg.start_ms > play_at:
        limits.append(next_seg.start_ms - play_at)
    return max(min(limits), 1) if limits else 1


def _fit_duration(source_ms: int, budget_ms: int) -> tuple[int, float, bool]:
    if source_ms <= budget_ms:
        return source_ms, 1.0, False
    needed_tempo = source_ms / budget_ms
    atempo = min(needed_tempo, _MAX_TEMPO)
    natural_ms = source_ms / atempo
    if natural_ms <= budget_ms + 1:
        return max(int(natural_ms), 1), atempo, False
    return budget_ms, atempo, True


def _compute_placements(clips: list[Segment]) -> list[_Placement]:
    ordered = sorted(clips, key=lambda s: (s.start_ms, s.id))
    placements: list[_Placement] = []

    for i, seg in enumerate(ordered):
        wav = Path(seg.tts_wav)  # type: ignore[arg-type]
        source_ms = _probe_duration_ms(wav)
        next_seg = ordered[i + 1] if i + 1 < len(ordered) else None
        budget_ms = _slot_budget_ms(seg, next_seg)
        fitted_ms, atempo, trimmed = _fit_duration(source_ms, budget_ms)
        placements.append(
            _Placement(
                seg,
                seg.start_ms,
                fitted_ms,
                source_ms,
                atempo,
                trimmed,
            )
        )

    return placements


def _fit_clip(src: Path, dst: Path, atempo: float, duration_ms: int, trimmed: bool) -> None:
    af_parts: list[str] = []
    if abs(atempo - 1.0) > 0.001:
        af_parts.append(f"atempo={atempo:.4f}")
    af_parts.append("aresample=44100")
    if trimmed:
        af_parts.append(f"atrim=0:{duration_ms / 1000.0:.3f}")
        af_parts.append("asetpts=PTS-STARTPTS")
    cmd = [
        _ffmpeg_bin(),
        "-y",
        "-i",
        str(src),
        "-af",
        ",".join(af_parts),
        "-ac",
        "1",
        "-ar",
        "44100",
        str(dst),
    ]
    subprocess.run(cmd, check=True, capture_output=True)


def _mix_placed_clips(
    placed: list[tuple[Path, int]],
    total_sec: float,
    out_path: Path,
) -> None:
    if not placed:
        raise RuntimeError("No clips to mix")
    if len(placed) == 1:
        path, delay_ms = placed[0]
        cmd = [
            _ffmpeg_bin(),
            "-y",
            "-i",
            str(path),
            "-af",
            f"adelay={delay_ms}|{delay_ms}",
            "-t",
            str(total_sec),
            "-ac",
            "1",
            "-ar",
            "44100",
            str(out_path),
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        return

    inputs: list[str] = []
    filter_parts: list[str] = []
    for i, (path, delay_ms) in enumerate(placed):
        inputs.extend(["-i", str(path)])
        filter_parts.append(f"[{i}:a]adelay={delay_ms}|{delay_ms}[a{i}]")
    mix_inputs = "".join(f"[a{i}]" for i in range(len(placed)))
    filter_parts.append(
        f"{mix_inputs}amix=inputs={len(placed)}:duration=longest:dropout_transition=0:normalize=0[outa]"
    )
    cmd = [
        _ffmpeg_bin(),
        "-y",
        *inputs,
        "-filter_complex",
        ";".join(filter_parts),
        "-map",
        "[outa]",
        "-t",
        str(total_sec),
        "-ac",
        "1",
        "-ar",
        "44100",
        str(out_path),
    ]
    subprocess.run(cmd, check=True, capture_output=True)


def _merge_chunk_wavs(chunk_paths: list[Path], total_sec: float, out_path: Path) -> None:
    if len(chunk_paths) == 1:
        shutil.copy2(chunk_paths[0], out_path)
        return
    _mix_placed_clips([(p, 0) for p in chunk_paths], total_sec, out_path)


def assemble_dubbed_audio(segments: list[Segment], total_duration_ms: int, out_path: Path) -> Path:
    """Place per-segment TTS anchored at start_ms with mild overlap fitting."""
    clips = [s for s in segments if s.tts_wav and Path(s.tts_wav).exists()]
    if not clips:
        raise RuntimeError("No TTS wav files to assemble")

    placements = _compute_placements(clips)
    last_end = placements[-1].play_at_ms + placements[-1].tts_ms
    total_sec = max(total_duration_ms / 1000.0, last_end / 1000.0 + 0.5)

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        fitted_placed: list[tuple[Path, int]] = []

        for i, pl in enumerate(placements):
            src = Path(pl.seg.tts_wav)  # type: ignore[arg-type]
            fitted = tmp_path / f"norm_{i:05d}.wav"
            _fit_clip(src, fitted, pl.atempo, pl.tts_ms, pl.trimmed)
            fitted_placed.append((fitted, pl.play_at_ms))

        if len(fitted_placed) <= _CHUNK_SIZE:
            _mix_placed_clips(fitted_placed, total_sec, out_path)
        else:
            chunk_wavs: list[Path] = []
            for i in range(0, len(fitted_placed), _CHUNK_SIZE):
                chunk = fitted_placed[i : i + _CHUNK_SIZE]
                chunk_out = tmp_path / f"chunk_{i:04d}.wav"
                _mix_placed_clips(chunk, total_sec, chunk_out)
                chunk_wavs.append(chunk_out)
            _merge_chunk_wavs(chunk_wavs, total_sec, out_path)

    return out_path
