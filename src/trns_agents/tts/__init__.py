from __future__ import annotations

import asyncio
import os
from pathlib import Path

from ..models import Segment

DEFAULT_LOCAL_VOICE = "th-TH-NiwatNeural"
DEFAULT_CLOUD_VOICE = "Charon"


async def _synthesize_edge(text: str, voice: str, out_path: Path) -> None:
    import edge_tts

    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(str(out_path))


def synthesize_segment_local(
    segment: Segment,
    out_path: Path,
    voice: str | None = None,
) -> Path:
    voice = voice or os.environ.get("TRNS_TTS_VOICE_LOCAL", DEFAULT_LOCAL_VOICE)
    text = segment.text_th or segment.text_en
    out_path.parent.mkdir(parents=True, exist_ok=True)
    asyncio.run(_synthesize_edge(text, voice, out_path))
    return out_path


def synthesize_segment_cloud(
    segment: Segment,
    out_path: Path,
    voice: str | None = None,
    api_key: str | None = None,
) -> Path:
    key = api_key or os.environ.get("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY required for cloud TTS")

    from google import genai
    from google.genai import types

    voice = voice or os.environ.get("TRNS_TTS_VOICE_CLOUD", DEFAULT_CLOUD_VOICE)
    text = segment.text_th or segment.text_en
    client = genai.Client(api_key=key)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-tts",
        contents=text,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=voice)
                )
            ),
        ),
    )
    part = response.candidates[0].content.parts[0]
    audio_bytes = part.inline_data.data
    out_path.write_bytes(audio_bytes)
    return out_path
