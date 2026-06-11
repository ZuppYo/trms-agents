---
title: "BRT004 — Tech stack evaluation"
type: planning
detail: "ประเมินและเลือก library/API สำหรับแต่ละ stage ของ pipeline"
tags: [brt, tech-stack, research]
created: 2026-06-11
updated: 2026-06-11
---

# BRT004 — Tech stack evaluation

Related: [003-brt-pipeline-architecture](./003-brt-pipeline-architecture.md) · [005-brt-constraints-risks](./005-brt-constraints-risks.md)

## Task Requirement

- Goal: เลือก stack ที่เหมาะกับ Windows local dev + requirement จาก BRT002
- In scope: เปรียบเทียบตัวเลือกต่อ stage, แนะนำ default Phase 1
- Out of scope: full production hardening

## Final stack (locked 2026-06-11)

| Stage | cloud | local | Rationale |
|-------|-------|-------|-----------|
| Transcript auto | youtube-transcript-api | same | ฟรี, มี timestamp |
| Transcript fallback | faster-whisper | same | วิดีโอยาว, VAD |
| Transcript manual | VTT/SRT parser | same | Obsidian Web Clipper |
| Translate | Gemini 2.5 Flash | NLLB-200-distilled-600M | คุณภาพ vs offline |
| TTS (male) | Gemini TTS `Charon` | Edge `th-TH-NiwatNeural` | ผู้ใช้ขอเสียงชาย |
| Long video | batch checkpoint + `--resume` | same | >30 min |
| Render | FFmpeg replace audio | same | R04 |
| Subtitle | export `.srt` / `.vtt` | same | R05 |

## Cost estimate — วิดีโอ 60 นาที (cloud mode, rough)

สมมติฐาน: ~130 คำ/นาที (EN speech) → ~7,800 คำ/ชม.; ~12  batches × 5 นาที

| Stage | ปริมาณโดยประมาณ | ราคา (USD) | หมายเหตุ |
|-------|-----------------|------------|----------|
| Transcript auto | ฟรี | $0 | youtube-transcript-api |
| Translate (Gemini 2.5 Flash) | ~10k in + ~10k out tokens | **$0.03–0.15** | [$0.30/1M in, $2.50/1M out](https://ai.google.dev/pricing) |
| TTS (Gemini 2.5 Flash TTS) | ~60 นาทีเสียง | **$1.50–4.00** | [$0.50/1M in, $10/1M audio out](https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash-preview-tts) — ช่วงกว้างตาม tokenization |
| yt-dlp + FFmpeg | local compute | $0 | bandwidth/electricity only |
| **รวม cloud (typical)** | | **~$2–5 / ชม.วิดีโอ** | ใช้ `--mode local` = $0 API |

### วิธีลดค่าใช้จ่าย

1. **`--mode local`** — NLLB + Edge-TTS ฟรี (ช้ากว่า, คุณภาพต่ำกว่า LLM)
2. **Hybrid** — แปลด้วย Gemini, TTS ด้วย Edge (ลด TTS cost ~90%)
3. **`--resume`** — ไม่จ่ายซ้ำเมื่อ retry
4. **Free tier Gemini** — ใช้ quota ฟรีสำหรับ POC / วิดีโอสั้น

## Dependencies

See [requirements.txt](../requirements.txt) and [pyproject.toml](../pyproject.toml).

## Checklist

- [x] T001 [N] ยืนยัน **transcript** strategy
  - ✅ auto + Whisper + manual import
- [x] T002 [N] ยืนยัน **translation** provider
  - ✅ Gemini / NLLB
- [x] T003 [N] ยืนยัน **TTS** (เสียงผู้ชาย)
  - ✅ Gemini Charon / Edge NiwatNeural
- [x] T004 [N] ประเมิน **cost estimate** ต่อวิดีโอ 60 นาที
  - ✅ ~$2–5 cloud; $0 local API
- [x] T005 [N] บันทึก **final stack table**
  - ✅ ด้านบน
- [x] T006 [N] สร้าง `requirements.txt` draft
  - ✅ requirements.txt + pyproject.toml
