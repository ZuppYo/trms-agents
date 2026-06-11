from __future__ import annotations

import json
import os
from pathlib import Path

from .models import ProjectMeta, SegmentsDocument


class WorkDir:
    """Checkpoint work directory: .trns-agents/{video_id}/"""

    def __init__(self, video_id: str, root: Path | None = None) -> None:
        base = root or Path(os.environ.get("TRNS_WORK_DIR", ".trns-agents"))
        self.root = base / video_id
        self.root.mkdir(parents=True, exist_ok=True)

    def path(self, *parts: str) -> Path:
        p = self.root.joinpath(*parts)
        p.parent.mkdir(parents=True, exist_ok=True)
        return p

    @property
    def meta_path(self) -> Path:
        return self.path("meta.json")

    @property
    def segments_path(self) -> Path:
        return self.path("segments.json")

    @property
    def output_mp4(self) -> Path:
        return self.path("output.th.mp4")

    @property
    def output_srt(self) -> Path:
        return self.path("output.th.srt")

    def batch_dir(self, batch_id: int) -> Path:
        return self.path("batches", f"{batch_id:03d}")

    def batch_done(self, batch_id: int) -> Path:
        return self.batch_dir(batch_id) / ".done"

    def is_batch_done(self, batch_id: int) -> bool:
        return self.batch_done(batch_id).exists()

    def mark_batch_done(self, batch_id: int) -> None:
        self.batch_done(batch_id).write_text("ok", encoding="utf-8")

    def save_meta(self, meta: ProjectMeta) -> None:
        self.meta_path.write_text(meta.model_dump_json(indent=2), encoding="utf-8")

    def load_meta(self) -> ProjectMeta:
        return ProjectMeta.model_validate_json(self.meta_path.read_text(encoding="utf-8"))

    def save_segments(self, doc: SegmentsDocument) -> None:
        self.segments_path.write_text(doc.model_dump_json(indent=2), encoding="utf-8")

    def load_segments(self) -> SegmentsDocument:
        return SegmentsDocument.model_validate_json(
            self.segments_path.read_text(encoding="utf-8")
        )

    def write_json(self, rel: str, data: object) -> Path:
        p = self.path(rel)
        p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return p
