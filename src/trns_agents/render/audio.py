from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

from ..models import Segment


def assemble_dubbed_audio(segments: list[Segment], total_duration_ms: int, out_path: Path) -> Path:
    """Place per-segment TTS clips on a silent timeline via FFmpeg."""
    clips = [s for s in segments if s.tts_wav and Path(s.tts_wav).exists()]
    if not clips:
        raise RuntimeError("No TTS wav files to assemble")

    total_sec = max(total_duration_ms / 1000.0, clips[-1].end_ms / 1000.0 + 1.0)

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        inputs: list[str] = []
        filter_parts: list[str] = []
        for i, seg in enumerate(clips):
            wav = Path(seg.tts_wav)
            inputs.extend(["-i", str(wav)])
            delay_ms = max(seg.start_ms, 0)
            filter_parts.append(f"[{i}:a]adelay={delay_ms}|{delay_ms}[a{i}]")

        mix_inputs = "".join(f"[a{i}]" for i in range(len(clips)))
        filter_parts.append(
            f"{mix_inputs}amix=inputs={len(clips)}:duration=longest:dropout_transition=0[outa]"
        )
        filter_complex = ";".join(filter_parts)

        cmd = [
            "ffmpeg",
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

    return out_path
