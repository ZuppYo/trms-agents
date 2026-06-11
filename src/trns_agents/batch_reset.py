from __future__ import annotations

import shutil

from .models import Segment, SegmentStatus, SegmentsDocument
from .workdir import WorkDir


def reset_batches(work: WorkDir, doc: SegmentsDocument, batch_ids: list[int]) -> SegmentsDocument:
    """Clear checkpoint + TTS for selected batches so they can be reprocessed."""
    for batch_id in batch_ids:
        batch_dir = work.batch_dir(batch_id)
        tts_dir = batch_dir / "tts"
        if tts_dir.exists():
            shutil.rmtree(tts_dir)
        done = work.batch_done(batch_id)
        if done.exists():
            done.unlink()

        for i, seg in enumerate(doc.segments):
            if seg.batch_id != batch_id:
                continue
            doc.segments[i] = seg.model_copy(
                update={
                    "text_th": "",
                    "tts_wav": None,
                    "status": SegmentStatus.PENDING,
                }
            )
    work.save_segments(doc)
    return doc
