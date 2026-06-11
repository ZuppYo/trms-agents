from __future__ import annotations

import os

from ..models import Segment, SegmentStatus
from .nllb import translate_texts


def translate_segments_gemini(segments: list[Segment], api_key: str | None = None) -> list[Segment]:
    key = api_key or os.environ.get("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY required for cloud translate")

    from google import genai

    client = genai.Client(api_key=key)
    lines = "\n".join(f"{s.id}|{s.text_en}" for s in segments)
    prompt = (
        "Translate each line from English to natural Thai. "
        "Keep the same id prefix before |. Output one line per input.\n\n"
        f"{lines}"
    )
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    text = response.text or ""
    mapping: dict[str, str] = {}
    for line in text.splitlines():
        if "|" not in line:
            continue
        sid, th = line.split("|", 1)
        mapping[sid.strip()] = th.strip()

    out: list[Segment] = []
    for seg in segments:
        th = mapping.get(seg.id, seg.text_en)
        out.append(seg.model_copy(update={"text_th": th, "status": SegmentStatus.TRANSLATED}))
    return out


def translate_segments_local(segments: list[Segment]) -> list[Segment]:
    texts = [s.text_en for s in segments]
    translated = translate_texts(texts)
    out: list[Segment] = []
    for seg, th in zip(segments, translated, strict=True):
        out.append(seg.model_copy(update={"text_th": th, "status": SegmentStatus.TRANSLATED}))
    return out
