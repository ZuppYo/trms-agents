from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

from ..models import Segment


def _ffmpeg_bin() -> str:
    found = shutil.which("ffmpeg")
    if found:
        return found
    winget = Path.home() / "AppData/Local/Microsoft/WinGet/Packages"
    for candidate in winget.glob("Gyan.FFmpeg*/ffmpeg-*/bin/ffmpeg.exe"):
        return str(candidate)
    return "ffmpeg"

# Windows CreateProcess limit (~32k); keep per-invocation argv small.
_CHUNK_SIZE = 40


def _ffmpeg_mix_segments(clips: list[Segment], total_sec: float, out_path: Path) -> None:
    inputs: list[str] = []
    filter_parts: list[str] = []
    for i, seg in enumerate(clips):
        inputs.extend(["-i", str(Path(seg.tts_wav))])
        delay_ms = max(seg.start_ms, 0)
        filter_parts.append(f"[{i}:a]adelay={delay_ms}|{delay_ms}[a{i}]")
    mix_inputs = "".join(f"[a{i}]" for i in range(len(clips)))
    filter_parts.append(
        f"{mix_inputs}amix=inputs={len(clips)}:duration=longest:dropout_transition=0[outa]"
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


def _ffmpeg_mix_wavs(wav_paths: list[Path], total_sec: float, out_path: Path) -> None:
    inputs: list[str] = []
    for p in wav_paths:
        inputs.extend(["-i", str(p)])
    n = len(wav_paths)
    mix_inputs = "".join(f"[{i}:a]" for i in range(n))
    filter_complex = f"{mix_inputs}amix=inputs={n}:duration=longest:dropout_transition=0[outa]"
    cmd = [
        _ffmpeg_bin(),
        "-y",
        *inputs,
        "-filter_complex",
        filter_complex,
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


def assemble_dubbed_audio(segments: list[Segment], total_duration_ms: int, out_path: Path) -> Path:
    """Place per-segment TTS clips on a silent timeline via FFmpeg."""
    clips = [s for s in segments if s.tts_wav and Path(s.tts_wav).exists()]
    if not clips:
        raise RuntimeError("No TTS wav files to assemble")

    total_sec = max(total_duration_ms / 1000.0, clips[-1].end_ms / 1000.0 + 1.0)

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        if len(clips) <= _CHUNK_SIZE:
            _ffmpeg_mix_segments(clips, total_sec, out_path)
        else:
            chunk_wavs: list[Path] = []
            for i in range(0, len(clips), _CHUNK_SIZE):
                chunk_out = tmp_path / f"chunk_{i:04d}.wav"
                _ffmpeg_mix_segments(clips[i : i + _CHUNK_SIZE], total_sec, chunk_out)
                chunk_wavs.append(chunk_out)
            _ffmpeg_mix_wavs(chunk_wavs, total_sec, out_path)

    return out_path
