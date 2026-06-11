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
- In scope: `src/trns_agents/`, requirements, dub command, local NLLB
- Out of scope: cloud mode (ข้าม Phase 1 ชั่วคราว), Whisper integration

## Checklist

- [x] T001–T007b — scaffold + batch 0 EN placeholder
- [x] T008 [N] Wire NLLB local translate
  - ✅ `translate/nllb.py` (facebook/nllb-200-distilled-600M)
- [x] T008b [N] `--redo-batches` สำหรับ re-process
  - ✅ `batch_reset.py`
- [x] T010 [N] Redo batch 0 ด้วย NLLB + TTS ไทย
  - ✅ ~163 segments, SRT ไทย (เช่น "ดีมากเลย มันแค่เพิ่มทุกอย่าง")
- [x] T011 [N] รัน batch 1 (local)
  - ✅ batch 0–1 done (329 segments)
- [x] T011b [N] ติดตั้ง FFmpeg + yt-dlp
  - ✅ winget; ffmpeg 8.1.1, yt-dlp 2026.06.09
- [x] T012 [N] รัน batch 2–6 + FFmpeg mux → **handoff [007](./007-session-handoff.md)**
  - ✅ 1126/1126 segments; `output.th.mp4` + `output.th.srt`; แก้ chunked ffmpeg + `amix normalize=0`

## Run (local-only workflow)

```powershell
cd E:\SRC\ai\my\trns-agents
.venv\Scripts\activate
pip install -e ".[local]"

# batch ถัดไป (เพิ่ม max-batches ทีละ 1)
trns-agents dub "https://www.youtube.com/watch?v=QbjAQFJJyt0" --mode local --resume --max-batches 3 --skip-render

# รันทั้งหมดที่เหลือ
trns-agents dub "https://www.youtube.com/watch?v=QbjAQFJJyt0" --mode local --resume --skip-render

# redo batch ที่แปลผิด
trns-agents dub "…" --mode local --redo-batches 0 --max-batches 1 --skip-render
```

Prerequisites สำหรับ MP4 สุดท้าย: **FFmpeg** + **yt-dlp** (โค้ด auto-discover winget ffmpeg ถ้าไม่อยู่ใน PATH)
