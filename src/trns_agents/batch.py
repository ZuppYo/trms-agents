from __future__ import annotations

from .models import Segment


def assign_batches(segments: list[Segment], batch_minutes: int = 5) -> list[Segment]:
    if not segments:
        return segments
    batch_ms = batch_minutes * 60 * 1000
    result: list[Segment] = []
    batch_id = 0
    batch_start = segments[0].start_ms
    for seg in segments:
        if seg.start_ms - batch_start >= batch_ms:
            batch_id += 1
            batch_start = seg.start_ms
        updated = seg.model_copy(update={"batch_id": batch_id})
        result.append(updated)
    return result


def group_by_batch(segments: list[Segment]) -> dict[int, list[Segment]]:
    groups: dict[int, list[Segment]] = {}
    for seg in segments:
        groups.setdefault(seg.batch_id, []).append(seg)
    return dict(sorted(groups.items()))
