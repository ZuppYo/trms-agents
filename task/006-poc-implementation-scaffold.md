---
title: "006 — POC implementation scaffold"
type: execution
detail: "Python CLI + pipeline skeleton ตาม BRT003 architecture"
tags: [execution, poc, phase1]
created: 2026-06-11
updated: 2026-06-11
---

# 006 — POC implementation scaffold

Related: [003-brt-pipeline-architecture](./003-brt-pipeline-architecture.md) · [004-brt-tech-stack-evaluation](./004-brt-tech-stack-evaluation.md)

## Task Requirement

- Goal: scaffold ที่รัน CLI ได้ + pipeline checkpoint ตาม architecture
- In scope: `src/trns_agents/`, requirements, dub command
- Out of scope: NLLB local translate เต็มรูป, Whisper integration, production polish

## Checklist

- [x] T001 [N] สร้าง `requirements.txt` + `pyproject.toml`
  - ✅ root package
- [x] T002 [N] CLI `trns-agents dub <url> --mode cloud|local [--resume]`
  - ✅ `src/trns_agents/cli.py`
- [x] T003 [N] Transcript: auto + manual VTT/SRT
  - ✅ `transcript/__init__.py`
- [x] T004 [N] Batch + checkpoint work dir
  - ✅ `workdir.py`, `batch.py`, `pipeline.py`
- [x] T005 [N] TTS local (Edge NiwatNeural) + cloud (Gemini) stub
  - ✅ `tts/__init__.py`
- [x] T006 [N] Export SRT + FFmpeg mux skeleton
  - ✅ `render/`, `render/audio.py`
- [x] T007 [N] Smoke test transcript กับ [QbjAQFJJyt0](https://www.youtube.com/watch?v=QbjAQFJJyt0)
  - ✅ 1126 segments, ~34 min, 7 batches @ 5 min
- [x] T007b [N] รัน dub **batch 0** (local, `--max-batches 1 --skip-render`)
  - ✅ 163 TTS wav + partial `output.th.srt` ใน `.trns-agents/QbjAQFJJyt0/`
- [ ] T008 [N] Wire NLLB local translate (replace placeholder)
- [ ] T009 [N] Wire faster-whisper fallback

## Run (after install)

```powershell
cd e:\SRC\ai\my\trns-agents
python -m venv .venv
.venv\Scripts\activate
pip install -e .
# copy .env.example → .env and set GEMINI_API_KEY for cloud

trns-agents dub "https://www.youtube.com/watch?v=QbjAQFJJyt0" --mode local --skip-render
trns-agents dub "https://www.youtube.com/watch?v=QbjAQFJJyt0" --mode local --max-batches 1 --skip-render
trns-agents dub "https://www.youtube.com/watch?v=QbjAQFJJyt0" --mode local --resume --skip-render
```

Prerequisites: **FFmpeg** และ **yt-dlp** ใน PATH (สำหรับ mux/download)
