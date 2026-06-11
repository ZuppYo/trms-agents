---
title: "007 — Session handoff"
type: handoff
detail: "Handoff สำหรับ new session — รัน batch 2-6 + mux MP4"
tags: [handoff, continuity, poc]
created: 2026-06-11
updated: 2026-06-11
---

# 007 — Session handoff

Related: [006-poc-implementation-scaffold](./006-poc-implementation-scaffold.md) · [AGENTS](../AGENTS.md)

## Task Requirement

- Goal: ให้ session ใหม่ทำงานต่อได้ทันทีโดยไม่ต้องอ่าน chat history ยาว
- Next work: — (POC closed; ดู archive สำหรับ history)

## สรุปโปรเจกต (1 ย่อหน้า)

`trns-agents` = CLI แปล YouTube EN→TH (personal use). Phase 1 **local-only** (ข้าม cloud):
- Transcript: `youtube-transcript-api`
- Translate: **NLLB-200** (`translate/nllb.py`)
- TTS: **Edge `th-TH-NiwatNeural`** (เสียงผู้ชาย)
- Checkpoint: `.trns-agents/{video_id}/` + `--resume` + `--redo-batches`

## สถานะปัจจุบัน (2026-06-11)

| รายการ | ค่า |
|--------|-----|
| Test URL | `https://www.youtube.com/watch?v=QbjAQFJJyt0` |
| video_id | `QbjAQFJJyt0` |
| Work dir | `.trns-agents/QbjAQFJJyt0/` |
| Total segments | 1126 (~34 min, 7 batches × ~5 min) |
| **tts_done** | **1126/1126** (batches 000–006) |
| Output | `output.th.mp4` (~333 MB) + `output.th.srt` |
| FFmpeg | ✅ 8.1.1 (winget Gyan.FFmpeg) |
| yt-dlp | ✅ 2026.06.09 |
| venv | `e:\SRC\ai\my\trns-agents\.venv` |

## คำสั่งที่ใช้บ่อย

```powershell
cd E:\SRC\ai\my\trns-agents
.venv\Scripts\activate

# remux หลังแก้ TTS / assemble (ข้าม translate+TTS)
trns-agents dub "https://www.youtube.com/watch?v=QbjAQFJJyt0" --mode local --resume

# redo batch ที่แปลผิด
trns-agents dub "https://www.youtube.com/watch?v=QbjAQFJJyt0" --mode local --redo-batches 3 --max-batches 1 --skip-render
```

## Reload pack (อ่านก่อนทำงาน)

1. `@AGENTS.md`
2. `@task/007-session-handoff.md` (ไฟล์นี้)
3. `@task/006-poc-implementation-scaffold.md`
4. `@src/trns_agents/pipeline.py` (ถ้าแก้ pipeline)

## ข้อควรรู้

- **ไม่ใช้ cloud** — ไม่ต้อง `GEMINI_API_KEY`
- NLLB แปลคุณภาพพอใช้ แต่ไม่ natural เท่า LLM
- `--skip-render` ข้าม download/mux; remux ไม่ใส่ flag นี้
- แก้เสียงเงียบ: `amix normalize=0` ใน `render/audio.py`
- T004 (faster-whisper) ยกเลิก — วิดีโอทดสอบมี caption

## Checklist (สำหรับ session ใหม่)

- [x] T001 รัน batch 2–6 (`--resume --skip-render`) จน tts_done = 1126
  - ✅ tts_done 1126/1126, batches 000–006 done (~37 min wall-clock)
- [x] T002 รัน mux (`--resume` ไม่ใส่ skip-render) → `output.th.mp4`
  - ✅ `output.th.mp4` (333 MB) + `output.th.srt`; แก้ chunked ffmpeg + winget ffmpeg discovery
- [x] T003 อัปเดต T012 ใน [006](./006-poc-implementation-scaffold.md) + AGENTS snapshot
  - ✅ T012 done; AGENTS + 007 status table อัปเดต
- [x] T004 (optional) T009 faster-whisper fallback
  - ⚠️ ยกเลิก — ไม่ทำ (user request)
