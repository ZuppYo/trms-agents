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

## คำถามสำหรับผู้ใช้ (brainstorm)

### Input & workflow
- รับ input แบบไหน? (URL เดียว / batch / playlist)
- ต้องการ CLI, script, หรือ UI?
- วิดีโอที่ไม่มี caption — ต้อง transcribe ด้วย Whisper หรือข้าม?

### Output
- ต้องการ **dub เต็ม** (แทนที่เสียงพูด) หรือ **overlay** (เสียงไทยทับเสียงเดิม duck ลง)?
- ต้องการ subtitle ไทย burn-in หรือไฟล์ SRT/VTT แยก?
- รูปแบบไฟล์ส่งออก? (MP4, ความละเอียดเดิม)

### คุณภาพ & ภาษา
- ระดับคุณภาพแปลที่ยอมรับ? (literal vs natural Thai)
- เสียง TTS: เพศ/โทนเสียง? หลาย speaker?
- ยอมใช้ cloud API (Gemini/OpenAI) หรือ local-only?

### ข้อจำกัด
- งบ API ต่อวิดีโอ / ต่อเดือน?
- รัน local (Windows) หรือ cloud?
- ความยาววิดีโอสูงสุด Phase 1?

## Checklist

- [ ] T001 [N] บันทึกคำตอบ **input/workflow** จากผู้ใช้
- [ ] T002 [N] บันทึกคำตอบ **output format** จากผู้ใช้
- [ ] T003 [N] บันทึกคำตอบ **quality & TTS** จากผู้ใช้
- [ ] T004 [N] บันทึกคำตอบ **constraints** (งบ, local/cloud, ความยาว)
- [ ] T005 [N] สรุปเป็น **Requirements table** ใน section ด้านล่างไฟล์นี้
- [ ] T006 [N] ระบุ **MoSCoW** (Must/Should/Could/Won't) อย่างน้อย 5 ข้อ

## Requirements (กรอกหลัง brainstorm)

| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| R01 | _(รอกรอก)_ | Must | |
