from __future__ import annotations

import subprocess
from pathlib import Path

from ..models import Segment
from .audio import _ffmpeg_bin


def ms_to_srt_time(ms: int) -> str:
    h = ms // 3_600_000
    ms %= 3_600_000
    m = ms // 60_000
    ms %= 60_000
    s = ms // 1000
    ms %= 1000
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def write_srt(segments: list[Segment], path: Path) -> None:
    lines: list[str] = []
    for i, seg in enumerate(segments, 1):
        text = seg.text_th or seg.text_en
        lines.append(str(i))
        lines.append(f"{ms_to_srt_time(seg.start_ms)} --> {ms_to_srt_time(seg.end_ms)}")
        lines.append(text)
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def download_video(url: str, out_path: Path) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "yt-dlp",
        "-f",
        "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "--merge-output-format",
        "mp4",
        "--ffmpeg-location",
        _ffmpeg_bin(),
        "-o",
        str(out_path),
        url,
    ]
    subprocess.run(cmd, check=True)
    return out_path


def replace_audio(video_path: Path, audio_path: Path, out_path: Path) -> Path:
    cmd = [
        _ffmpeg_bin(),
        "-y",
        "-i",
        str(video_path),
        "-i",
        str(audio_path),
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-map",
        "0:v:0",
        "-map",
        "1:a:0",
        "-shortest",
        str(out_path),
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return out_path
