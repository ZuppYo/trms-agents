---
title: "BRT001 — Project vision & scope"
type: planning
detail: "Brainstorm เป้าหมาย ขอบเขต และ success criteria ของ trns-agents Phase 1"
tags: [brt, vision, phase1]
created: 2026-06-11
updated: 2026-06-11
---

# BRT001 — Project vision & scope

Related: [AGENTS](../AGENTS.md) · [prompt.md](./prompt.md) · [002-brt-user-requirements](./002-brt-user-requirements.md)

## Task Requirement

- Goal: กำหนด vision, scope, และ success criteria ของ `trns-agents` Phase 1 ร่วมกับผู้ใช้
- In scope: เป้าหมายผลลัพธ์, กลุ่มผู้ใช้, use cases หลัก, ขอบเขต in/out
- Out of scope: เลือก library รายตัว (ทำใน BRT004), implementation code

## Vision (ยืนยันแล้ว)

**Vision statement:** `trns-agents` คือผู้ช่วยส่วนตัวที่รับ URL วิดีโอ YouTube ภาษาอังกฤษ แปลเนื้อหาเป็นภาษาไทย แล้วสร้างวิดีโอใหม่ที่มีเสียงพากย์ไทยแทนที่เสียงเดิม — เพื่อให้ผู้ใช้ดูและเข้าใจเนื้อหาเป็นภาษาไทยได้

| หัวข้อ | คำตอบ |
|--------|-------|
| กลุ่มผู้ใช้ | ผู้ใช้หลัก = ตัวเอง; **personal use** ใน Phase 1 |
| ตัวอย่างวิดีโอ | [QbjAQFJJyt0](https://www.youtube.com/watch?v=QbjAQFJJyt0) |
| โหมดเสียง | **แทนที่เสียง** (replace audio track) — ไม่ overlay |
| Backend | **2 โหมด**: cloud (Gemini API) และ local |

### Use cases หลัก

1. **UC01** — วาง URL วิดีโอ EN แล้วได้ MP4 เสียงไทย (personal viewing)
2. **UC02** — เลือกโหมด cloud (Gemini) เมื่อต้องการคุณภาพแปล/TTS สูงและมี API key
3. **UC03** — เลือกโหมด local เมื่อไม่ต้องการส่งข้อมูลออก cloud หรือไม่มี API

### Success criteria (Phase 1)

| # | เกณฑ์ | สถานะ |
|---|--------|--------|
| SC1 | Pipeline ทำงาน end-to-end กับ [QbjAQFJJyt0](https://www.youtube.com/watch?v=QbjAQFJJyt0) | Must |
| SC2 | โหมด **cloud (Gemini)** และ **local** ใช้งานได้ทั้งคู่ | Must |
| SC3 | ส่งออก MP4 — **เสียงไทยแทนที่เสียงเดิม** (video track เดิม) | Must |
| SC4 | แปลและพากย์ฟังเข้าใจได้ (natural Thai ยอมรับได้) | Must |
| SC5 | ความยาววิดีโอสูงสุด Phase 1 | **รอยืนยัน** (แนะนำ ≤30 นาที) |

### Out of scope Phase 1 → Phase 2

| Phase 1 (Won't) | Phase 2 (Could) |
|-----------------|-----------------|
| อัปโหลด/re-upload YouTube | Batch / playlist |
| แจกจ่ายวิดีโอ dub สาธารณะ | UI / web app |
| Lip-sync / voice cloning | Multi-speaker diarization |
| แพลตฟอร์มอื่น (TikTok ฯลฯ) | BGM preservation แยก vocal |

## Checklist

- [x] T001 [N] ยืนยัน **vision statement** 1–2 ประโยคกับผู้ใช้
  - ✅ Vision statement บันทึกใน section ด้านบน
- [x] T002 [N] ระบุ **กลุ่มผู้ใช้เป้าหมาย** (เช่น ตัวเอง / นักเรียน / creator)
  - ✅ ตัวเอง — personal use Phase 1
- [x] T003 [N] ระบุ **use cases หลัก** อย่างน้อย 3 ข้อ (พร้อมตัวอย่าง URL ถ้ามี)
  - ✅ UC01–UC03 + example URL QbjAQFJJyt0
- [x] T004 [N] กำหนด **success criteria** Phase 1 (เช่น ความยาววิดีโอสูงสุด, คุณภาพเสียงขั้นต่ำ)
  - ✅ SC1–SC4 ยืนยัน; SC5 รอยืนยันความยาวสูงสุด
- [x] T005 [N] ยืนยัน **out of scope** Phase 1 และสิ่งที่เลื่อนไป Phase 2
  - ✅ ตาราง out of scope ด้านบน
- [x] T006 [N] อัปเดต [AGENTS.md](../AGENTS.md) continuity snapshot หลังผู้ใช้ยืนยัน
  - ✅ อัปเดต AGENTS.md 2026-06-11
