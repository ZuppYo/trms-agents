---
title: "BRT002 — User requirements"
type: planning
detail: "เก็บ functional/non-functional requirements จากผู้ใช้สำหรับ Phase 1"
tags: [brt, requirements, phase1]
created: 2026-06-11
updated: 2026-06-11
---

# BRT002 — User requirements

Related: [001-brt-project-vision](./001-brt-project-vision.md) · [003-brt-pipeline-architecture](./003-brt-pipeline-architecture.md)

## Task Requirement

- Goal: รวบรวม requirement ที่ชัดเจนจากผู้ใช้ก่อนออกแบบ pipeline
- In scope: input/output, UX ที่ต้องการ, คุณภาพที่ยอมรับได้, ข้อจำกัดด้านเวลา/ทรัพยากร
- Out of scope: implementation

## คำตอบจากผู้ใช้

### รอบที่ 1 (2026-06-11)

| หัวข้อ | คำตอบ |
|--------|-------|
| ผู้ใช้ | ตัวเอง — personal use |
| โหมดเสียง | แทนที่ audio track |
| Backend | cloud (Gemini) + local |
| ตัวอย่าง URL | [QbjAQFJJyt0](https://www.youtube.com/watch?v=QbjAQFJJyt0) |

### รอบที่ 2 (2026-06-11)

| # | คำถาม | คำตอบ |
|---|-------|-------|
| 1 | Interface | **CLI** พอสำหรับ Phase 1 |
| 2 | Subtitle ไทย | **ต้องการ** — SRT/VTT แยก (และ/หรือ mux กับ MP4) |
| 3 | ความยาววิดีโอ | ใช้งานจริง **ส่วนใหญ่ >30 นาที** — ต้องรองรับด้วย chunked pipeline + resume (ดู [003](./003-brt-pipeline-architecture.md#long-video-strategy)) |
| 4 | ไม่มี caption | **Whisper fallback** ได้ + **manual import** จาก Obsidian Web Clipper (VTT/SRT/txt) |
| 5 | TTS | **เสียงผู้ชาย** |

## Requirements

| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| R01 | รับ YouTube URL ภาษาอังกฤษ | Must | URL เดียว Phase 1 |
| R02 | แปล transcript EN → TH | Must | natural Thai |
| R03 | สร้างเสียงพากย์ไทย **เสียงผู้ชาย** | Must | |
| R04 | **แทนที่ audio track** ในวิดีโอ | Must | ไม่ overlay |
| R05 | ส่งออก MP4 + **SRT/VTT ไทย** | Must | video track เดิม |
| R06 | โหมด **cloud — Gemini API** | Must | translate + TTS |
| R07 | โหมด **local** | Must | offline / no cloud |
| R08 | Personal use only | Must | ไม่ re-upload |
| R09 | Acceptance video: [QbjAQFJJyt0](https://www.youtube.com/watch?v=QbjAQFJJyt0) | Must | smoke test |
| R10 | **CLI** interface | Must | `trns-agents dub …` |
| R11 | Whisper fallback เมื่อไม่มี caption | Must | |
| R12 | **Manual transcript import** (VTT/SRT/txt) | Must | Obsidian Web Clipper |
| R13 | รองรับวิดีโอ **>30 นาที** | Must | chunked + checkpoint/resume |
| R14 | Resume หลัง interrupt/failure | Must | ไม่เริ่มใหม่ทั้ง pipeline |
| R15 | Batch / playlist | Won't | Phase 2 |

## MoSCoW

| Priority | Items |
|----------|-------|
| **Must** | R01–R14 |
| **Should** | progress log ต่อ chunk, parallel TTS workers |
| **Could** | burn-in subtitle ใน MP4 |
| **Won't** | R15, re-upload, lip-sync, UI |

## TTS voice (locked)

| Backend | Voice | ID |
|---------|-------|-----|
| local | Edge-TTS ผู้ชายไทย | `th-TH-NiwatNeural` |
| cloud | Gemini TTS ผู้ชาย | `Charon` หรือ `Iapetus` (th-TH) — ทดสอบใน POC |

## Checklist

- [x] T001 [N] บันทึกคำตอบ **input/workflow** จากผู้ใช้
  - ✅ CLI; Whisper + manual import (Obsidian Web Clipper)
- [x] T002 [N] บันทึกคำตอบ **output format** จากผู้ใช้
  - ✅ MP4 replace audio + SRT/VTT ไทย
- [x] T003 [N] บันทึกคำตอบ **quality & TTS** จากผู้ใช้
  - ✅ dual backend; **เสียงผู้ชาย**
- [x] T004 [N] บันทึกคำตอบ **constraints** (งบ, local/cloud, ความยาว)
  - ✅ >30 นาที real-world; แก้ด้วย chunked pipeline (BRT003)
- [x] T005 [N] สรุปเป็น **Requirements table**
  - ✅ R01–R15
- [x] T006 [N] ระบุ **MoSCoW**
  - ✅ อัปเดตครบ
