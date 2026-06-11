from __future__ import annotations

import re
from pathlib import Path

from youtube_transcript_api import YouTubeTranscriptApi

from ..models import Segment


def fetch_youtube_transcript(video_id: str, languages: list[str] | None = None) -> list[Segment]:
    langs = languages or ["en", "en-US", "en-GB"]
    api = YouTubeTranscriptApi()
    fetched = api.fetch(video_id, languages=langs)
    segments: list[Segment] = []
    for i, item in enumerate(fetched):
        start_ms = int(item.start * 1000)
        end_ms = int((item.start + item.duration) * 1000)
        segments.append(
            Segment(
                id=f"s{i:05d}",
                start_ms=start_ms,
                end_ms=end_ms,
                text_en=item.text.strip(),
            )
        )
    return [s for s in segments if s.text_en]


def _parse_timestamp(ts: str) -> int:
    """Parse SRT/VTT timestamp to milliseconds."""
    ts = ts.strip().replace(",", ".")
    if ts.count(":") == 2:
        h, m, rest = ts.split(":")
        s_parts = rest.split(".")
        sec = int(s_parts[0])
        ms = int(s_parts[1].ljust(3, "0")[:3]) if len(s_parts) > 1 else 0
        return (int(h) * 3600 + int(m) * 60 + sec) * 1000 + ms
    m, rest = ts.split(":")
    s_parts = rest.split(".")
    sec = int(s_parts[0])
    ms = int(s_parts[1].ljust(3, "0")[:3]) if len(s_parts) > 1 else 0
    return (int(m) * 60 + sec) * 1000 + ms


def parse_vtt_or_srt(content: str) -> list[Segment]:
    content = re.sub(r"^\ufeff", "", content)
    content = re.sub(r"WEBVTT[^\n]*\n", "", content, count=1)
    blocks = re.split(r"\n\s*\n", content.strip())
    segments: list[Segment] = []
    idx = 0
    for block in blocks:
        lines = [ln.strip() for ln in block.splitlines() if ln.strip()]
        if len(lines) < 2:
            continue
        time_line = lines[0] if "-->" in lines[0] else lines[1] if len(lines) > 1 and "-->" in lines[1] else None
        if not time_line or "-->" not in time_line:
            continue
        start_s, end_s = time_line.split("-->")
        text_lines = lines[2:] if time_line == lines[1] else lines[1:]
        text = " ".join(text_lines).strip()
        text = re.sub(r"<[^>]+>", "", text)
        if not text:
            continue
        segments.append(
            Segment(
                id=f"s{idx:05d}",
                start_ms=_parse_timestamp(start_s),
                end_ms=_parse_timestamp(end_s),
                text_en=text,
            )
        )
        idx += 1
    return segments


def load_manual_transcript(path: Path) -> list[Segment]:
    content = path.read_text(encoding="utf-8")
    suffix = path.suffix.lower()
    if suffix in {".vtt", ".srt", ".txt"}:
        return parse_vtt_or_srt(content)
    raise ValueError(f"Unsupported transcript file type: {suffix}")
