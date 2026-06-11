---
title: "010 — Session handoff: Cloud mode (Gemini)"
type: handoff
detail: "Phase ถัดไป — ใช้ --mode cloud (Gemini แปล + TTS) แทน local NLLB + Edge"
tags: [handoff, continuity, cloud, gemini]
created: 2026-06-11
updated: 2026-06-11
---

# 010 — Session handoff: Cloud mode (Gemini)

Related: [009 A/V sync archive](./archive/2026-06-12/009-session-handoff-av-sync.md) · [008 audio archive](./archive/2026-06-11/008-dub-audio-continuity.md) · [README](../README.md)

## Task Requirement

- Goal: วางแผนและทดสอบ **`--mode cloud`** เป็น workflow หลักแทน local (NLLB + Edge TTS)
- ผลที่ต้องการ: คุณภาพแปล/TTS ดีขึ้น, venv เล็กลง (ไม่ต้อง `[local]` / PyTorch), pipeline เดิมยังใช้ได้
- Out of scope (session นี้): speaker diarization, commercial deploy, เปลี่ยน logic assemble/sync (ทำแล้วใน 008–009)

## งานเก่าปิดแล้ว (สรุป)

| Task | ผลลัพธ์ |
|------|---------|
| [008](./archive/2026-06-11/008-dub-audio-continuity.md) | แก้ทับซ้อน / เสียงไม่ต่อเนื่อง — sequential → ต่อด้วย 009 |
| [009](./archive/2026-06-12/009-session-handoff-av-sync.md) | **Anchor `start_ms`** + atempo ≤1.15 + trim; drift **0**; timeline ตรงความยาววิดีโอ |

**Local mode ใช้ได้แล้ว** — `render/audio.py`, `scripts/analyze_dub_timing.py`, `--resume`, `--max-batches`

วิดีโอที่ทดสอบแล้ว: `QbjAQFJJyt0` (full local), `7f8e5IiUkeo` (smoke batch 0)

## ทำไม cloud ต่อไป

- **แปล:** Gemini มัก natural กว่า NLLB-200 local
- **TTS:** Gemini TTS (`gemini-2.5-flash-preview-tts`) แทน Edge — ไม่พึ่ง `speech.platform.bing.com`
- **venv:** ติดตั้งแค่ `pip install -e .` (~ไม่มี torch/transformers ~1 GB)
- โค้ดมีอยู่แล้วแต่ **ยังไม่ได้ validate เป็น workflow หลัก**

## โค้ดที่มีอยู่ (จุดเริ่ม)

| ส่วน | ไฟล์ | หมายเหตุ |
|------|------|----------|
| CLI `--mode cloud` | [`cli.py`](../src/trns_agents/cli.py) | ต้อง `GEMINI_API_KEY` |
| แปล | [`translate/__init__.py`](../src/trns_agents/translate/__init__.py) | `gemini-2.5-flash` batch ใน prompt |
| TTS | [`tts/__init__.py`](../src/trns_agents/tts/__init__.py) | `synthesize_segment_cloud` — บันทึก raw bytes |
| Pipeline | [`pipeline.py`](../src/trns_agents/pipeline.py) | สลับ local/cloud ตาม `BackendMode` |

## คำถาม / งานที่น่าคุยใน session ถัดไป

1. **Cloud TTS format** — output จาก Gemini เป็น format อะไร? ต้องแปลงก่อน assemble หรือไม่ (WAV/PCM)?
2. **คุณภาพเทียบ local** — แปล + เสียง + sync บนวิดีโอสั้น
3. **ต้นทุน / rate limit** — 783–1126 segments ต่อวิดีโอ; batching API
4. **Default mode** — เปลี่ยน default เป็น `cloud` หรือเก็บ `local`?
5. **Optional deps** — แยก `[local]` ชัดขึ้น / ถอด `faster-whisper` ที่ไม่ได้ใช้
6. **yt-dlp PATH** — ใช้ `python -m yt_dlp` ใน `download_video` (เจอบน Windows)

## Checklist (session ถัดไป)

- [ ] T001 [N] ตั้ง `.env` + smoke `trns-agents dub URL --mode cloud --max-batches 1`
- [ ] T002 [N] ตรวจ cloud TTS output → แก้ decode/convert ถ้า assemble ล้ม
- [ ] T003 [N] เปรียบเทียบคุณภาพแปล cloud vs local (ตัวอย่าง 10–20 segments)
- [ ] T004 [N] วัด drift/overlap หลัง cloud TTS (`analyze_dub_timing.py`)
- [ ] T005 [U] อัปเดต README — cloud เป็นแนะนำ, local เป็น optional/offline

## คำสั่ง (copy-paste)

```powershell
cd E:\SRC\ai\my\trns-agents
.venv\Scripts\activate
copy .env.example .env   # ใส่ GEMINI_API_KEY

# smoke cloud
trns-agents dub "https://www.youtube.com/watch?v=7f8e5IiUkeo" --mode cloud --max-batches 1

# วิเคราะห์ timing (หลังมี TTS wav)
python scripts/analyze_dub_timing.py .trns-agents/VIDEO_ID --batch 0
```

## Reload pack

1. `@task/010-session-handoff-cloud-gemini.md` (ไฟล์นี้)
2. `@src/trns_agents/translate/__init__.py` · `@src/trns_agents/tts/__init__.py`
3. `@src/trns_agents/render/audio.py` (assemble ใช้ร่วมกับ cloud/local)
4. `@task/archive/2026-06-12/009-session-handoff-av-sync.md` (บริบท sync)

## New session prompt

```
@task/010-session-handoff-cloud-gemini.md go
ทดสอบ --mode cloud (Gemini) smoke --max-batches 1
```
