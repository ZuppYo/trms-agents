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

## คำตอบจากผู้ใช้ (2026-06-11)

### Input & workflow

| คำถาม | คำตอบ | สถานะ |
|-------|-------|--------|
| กลุ่มผู้ใช้ | ตัวเอง — personal use | ✅ |
| Input | URL เดียว (default Phase 1) | ⚠️ ยังไม่ยืนยัน batch |
| Interface | _(ยังไม่ระบุ — แนะนำ CLI ก่อน)_ | ⚠️ |
| ไม่มี caption | _(ยังไม่ระบุ — แนะนำ Whisper fallback)_ | ⚠️ |

### Output

| คำถาม | คำตอบ | สถานะ |
|-------|-------|--------|
| โหมดเสียง | **แทนที่เสียง** (replace audio) | ✅ |
| Subtitle ไทย | _(ยังไม่ระบุ)_ | ⚠️ |
| ไฟล์ส่งออก | MP4, ความละเอียดเดิม (default) | ⚠️ |

### คุณภาพ & backend

| คำถาม | คำตอบ | สถานะ |
|-------|-------|--------|
| Backend | **2 โหมด**: cloud (Gemini) + local | ✅ |
| คุณภาพแปล | _(ยังไม่ระบุ — default natural Thai)_ | ⚠️ |
| TTS เสียง/เพศ | _(ยังไม่ระบุ)_ | ⚠️ |

### ข้อจำกัด

| คำถาม | คำตอบ | สถานะ |
|-------|-------|--------|
| การใช้งาน | Personal only — ไม่ re-upload | ✅ |
| สภาพแวดล้อม | Windows local (จาก env) | ✅ |
| งบ API | _(ยังไม่ระบุ)_ | ⚠️ |
| ความยาววิดีโอสูงสุด | _(ยังไม่ระบุ)_ | ⚠️ |

## Requirements

| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| R01 | รับ YouTube URL ภาษาอังกฤษ | Must | URL เดียว Phase 1 |
| R02 | แปล transcript EN → TH | Must | |
| R03 | สร้างเสียงพากย์ไทย (TTS) | Must | |
| R04 | **แทนที่ audio track** ในวิดีโอ | Must | ไม่ overlay/duck |
| R05 | ส่งออก MP4 | Must | video track เดิม |
| R06 | โหมด **cloud — Gemini API** | Must | translate + TTS |
| R07 | โหมด **local** | Must | offline / no cloud |
| R08 | Personal use only | Must | ไม่ re-upload, ไม่แจกจ่าย |
| R09 | ตัวอย่างทดสอบ: [QbjAQFJJyt0](https://www.youtube.com/watch?v=QbjAQFJJyt0) | Must | acceptance video |
| R10 | CLI interface | Should | ยังไม่ยืนยัน — แนะนำ Phase 1 |
| R11 | Whisper fallback เมื่อไม่มี caption | Should | ยังไม่ยืนยัน |
| R12 | Subtitle ไทย (SRT/VTT หรือ burn-in) | Could | ยังไม่ยืนยัน |
| R13 | Batch / playlist | Won't | Phase 2 |

## MoSCoW

| Priority | Items |
|----------|-------|
| **Must** | R01–R09 |
| **Should** | R10 CLI, R11 Whisper fallback |
| **Could** | R12 subtitle ไทย |
| **Won't** | R13 batch, re-upload, lip-sync, public distribution |

## Checklist

- [x] T001 [N] บันทึกคำตอบ **input/workflow** จากผู้ใช้
  - ✅ personal use, URL เดียว (default); CLI/caption fallback รอยืนยัน
- [x] T002 [N] บันทึกคำตอบ **output format** จากผู้ใช้
  - ✅ replace audio ยืนยัน; MP4 default; subtitle รอยืนยัน
- [x] T003 [N] บันทึกคำตอบ **quality & TTS** จากผู้ใช้
  - ✅ dual backend cloud Gemini + local; รายละเอียดเสียง/คุณภาพแปล รอยืนยัน
- [x] T004 [N] บันทึกคำตอบ **constraints** (งบ, local/cloud, ความยาว)
  - ✅ personal + Windows; งบ/ความยาว รอยืนยัน
- [x] T005 [N] สรุปเป็น **Requirements table** ใน section ด้านล่างไฟล์นี้
  - ✅ R01–R13
- [x] T006 [N] ระบุ **MoSCoW** (Must/Should/Could/Won't) อย่างน้อย 5 ข้อ
  - ✅ ตาราง MoSCoW ด้านบน
