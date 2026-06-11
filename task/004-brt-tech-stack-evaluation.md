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
- Out of scope: implement POC (task execution ถัดไป)

## Web research summary (2026)

### Transcript extraction

| Option | ข้อดี | ข้อเสีย | เหมาะกับ |
|--------|-------|---------|----------|
| [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) | ฟรี, ไม่ต้อง API key, maintained (v1.2.3 Jan 2026) | scrape — อาจพังเมื่อ YouTube เปลี่ยน | prototype / low volume |
| [TranscriptAPI](https://transcriptapi.com) | REST, MCP, ~49ms median, scale | มีค่าใช้จ่าย | production scale |
| [Supadata](https://supadata.ai) | multi-platform, AI fallback ไม่มี caption | มีค่าใช้จ่าย | ต้องการ fallback |
| Whisper + yt-dlp | ทำงานได้แม้ไม่มี caption | ช้า, ต้อง GPU สำหรับความเร็ว | วิดีโอไม่มี subtitle |

### Translation EN → TH

| Option | ข้อดี | ข้อเสีย |
|--------|-------|---------|
| Gemini API | ภาษาไทยดี, รวมกับ TTS ได้ | ค่าใช้จ่าย, ต้อง network |
| OpenAI GPT | คุณภาพสูง | ค่าใช้จ่าย |
| Meta NLLB (local) | ฟรี, offline | คุณภาพต่ำกว่า LLM, ต้อง refine |
| Google Translate (RPC) | ฟรีใน youtube-auto-dub | unofficial, อาจถูกบล็อก |

### Thai TTS

| Option | ข้อดี | ข้อเสีย |
|--------|-------|---------|
| Edge-TTS (`th-TH-KanyaNeural`, `th-TH-NiwatNeural`) | ฟรี, stable, ใช้ใน dub pipelines หลายโปรเจกต์ | โทนเสียงจำกัด |
| [Gemini TTS](https://ai.google.dev/gemini-api/docs/speech-generation) (`th-TH` GA) | 30+ voices, style control, multispeaker | artifacts บางคำไทย, chunk ยาว drift |
| Google Cloud Neural2 | benchmark คุณภาพ | billing |

### Video / audio

- **yt-dlp** — ดาวน์โหลดวิดีโอ/เสียง
- **FFmpeg** — mux, burn subtitle, duck audio
- **Demucs** (optional) — แยก vocal/BGM ก่อน dub

## Recommended default (Phase 1 draft)

```
Python 3.11+
├── youtube-transcript-api  (caption path)
├── yt-dlp + openai-whisper (fallback path)
├── google-genai            (translate + optional Gemini TTS)
├── edge-tts                (free TTS fallback)
└── ffmpeg                  (render)
```

> ต้องยืนยันกับผู้ใช้ใน BRT002 ก่อน lock

## Checklist

- [ ] T001 [N] ยืนยัน **transcript** strategy กับผู้ใช้
- [ ] T002 [N] ยืนยัน **translation** provider
- [ ] T003 [N] ยืนยัน **TTS** provider (และเสียงไทยที่ต้องการ)
- [ ] T004 [N] ประเมิน **cost estimate** ต่อวิดีโอ 10 นาที (rough)
- [ ] T005 [N] บันทึก **final stack table** ใน section ด้านล่าง
- [ ] T006 [N] สร้าง `requirements.txt` draft (หรือระบุใน task execution ถัดไป)

## Final stack (กรอกหลังยืนยัน)

| Stage | Choice | Rationale |
|-------|--------|-----------|
| Transcript | _(รอกรอก)_ | |
| Translate | _(รอกรอก)_ | |
| TTS | _(รอกรอก)_ | |
| Render | FFmpeg + yt-dlp | industry standard |
