from __future__ import annotations

import re
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class BackendMode(str, Enum):
    CLOUD = "cloud"
    LOCAL = "local"


class SegmentStatus(str, Enum):
    PENDING = "pending"
    TRANSLATED = "translated"
    TTS_DONE = "tts_done"
    DONE = "done"


class Segment(BaseModel):
    id: str
    start_ms: int
    end_ms: int
    text_en: str
    text_th: str = ""
    batch_id: int = 0
    tts_wav: str | None = None
    status: SegmentStatus = SegmentStatus.PENDING


class ProjectMeta(BaseModel):
    video_id: str
    url: str
    mode: BackendMode = BackendMode.LOCAL
    voice: str = "th-TH-NiwatNeural"
    batch_minutes: int = 5
    transcript_source: Literal["auto", "whisper", "manual"] = "auto"


class SegmentsDocument(BaseModel):
    video_id: str
    segments: list[Segment] = Field(default_factory=list)


YOUTUBE_ID_RE = re.compile(
    r"(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([A-Za-z0-9_-]{11})"
)


def extract_video_id(url_or_id: str) -> str:
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", url_or_id):
        return url_or_id
    match = YOUTUBE_ID_RE.search(url_or_id)
    if not match:
        raise ValueError(f"Cannot parse YouTube video id from: {url_or_id!r}")
    return match.group(1)
