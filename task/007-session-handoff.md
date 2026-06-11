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
- Next work: รัน batch 2–6 → mux `output.th.mp4` → (optional) T009 Whisper

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
| **tts_done** | **329** (batch 0–1) |
| Pending batches | **2, 3, 4, 5, 6** |
| FFmpeg | ✅ 8.1.1 (winget Gyan.FFmpeg) |
| yt-dlp | ✅ 2026.06.09 |
| venv | `e:\SRC\ai\my\trns-agents\.venv` |

## คำสั่งถัดไป (copy-paste)

```powershell
cd E:\SRC\ai\my\trns-agents
.venv\Scripts\activate

# 1) รัน batch 2–6 (~40–50 นาที wall-clock)
trns-agents dub "https://www.youtube.com/watch?v=QbjAQFJJyt0" --mode local --resume --skip-render

# ตรวจ progress
python -c "from pathlib import Path; import json; p=Path('.trns-agents/QbjAQFJJyt0/batches'); print([x.name for x in p.iterdir() if (x/'.done').exists()]); d=json.load(open('.trns-agents/QbjAQFJJyt0/segments.json',encoding='utf-8')); print('tts_done', sum(1 for s in d['segments'] if s['status']=='tts_done'))"

# 2) หลังครบ 1126 — download + mux MP4
trns-agents dub "https://www.youtube.com/watch?v=QbjAQFJJyt0" --mode local --resume
# output: .trns-agents/QbjAQFJJyt0/output.th.mp4 + output.th.srt
```

## New session prompt (แนะนำ)

```
@task/007-session-handoff.md go
รัน batch 2–6 แล้ว mux MP4 สำหรับ QbjAQFJJyt0 (local mode)
```

## Reload pack (อ่านก่อนทำงาน)

1. `@AGENTS.md`
2. `@task/007-session-handoff.md` (ไฟล์นี้)
3. `@task/006-poc-implementation-scaffold.md`
4. `@src/trns_agents/pipeline.py` (ถ้าแก้ pipeline)

## ข้อควรรู้

- **ไม่ใช้ cloud** — ไม่ต้อง `GEMINI_API_KEY`
- NLLB แปลคุณภาพพอใช้ แต่ไม่ natural เท่า LLM
- รัน batch 2–6 ถูก interrupt ครั้งหนึ่งใน session ก่อน — ยังไม่เริ่ม batch 2
- `--skip-render` ข้าม download/mux; รันครั้งสุดท้ายไม่ใส่ flag นี้
- T009 (faster-whisper) ยังไม่ทำ — ไม่ block งานปัจจุบัน (วิดีโอมี caption)

## Checklist (สำหรับ session ใหม่)

- [ ] T001 รัน batch 2–6 (`--resume --skip-render`) จน tts_done = 1126
- [ ] T002 รัน mux (`--resume` ไม่ใส่ skip-render) → `output.th.mp4`
- [ ] T003 อัปเดต T012 ใน [006](./006-poc-implementation-scaffold.md) + AGENTS snapshot
- [ ] T004 (optional) T009 faster-whisper fallback
