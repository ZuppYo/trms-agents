---
title: "BRT005 — Constraints & risks"
type: planning
detail: "ข้อจำกัดทางกฎหมาย ToS คุณภาพ และความเสี่ยงทางเทคนิค"
tags: [brt, legal, risks, constraints]
created: 2026-06-11
updated: 2026-06-11
---

# BRT005 — Constraints & risks

Related: [004-brt-tech-stack-evaluation](./004-brt-tech-stack-evaluation.md) · [AGENTS](../AGENTS.md)

## Task Requirement

- Goal: ระบุข้อจำกัดและความเสี่ยงก่อน implement — โดยเฉพาะ YouTube ToS และลิขสิทธิ์
- In scope: legal/ToS, technical risks, mitigation
- Out of scope: คำแนะนำทางกฎหมายเชิง professional

## Legal & ToS (จาก web research)

### YouTube Terms of Service
- **ห้ามดาวน์โหลด** เนื้อหาโดยไม่มีปุ่ม download หรือ permission ([YouTube ToS](https://www.youtube.com/static?template=terms))
- **ห้ามใช้ automated means** (scrapers, bots) โดยไม่ได้รับอนุญาตเป็นลายลักษณ์อักษร
- อนุญาต: ดูผ่าน embed player, personal non-commercial viewing

### YouTube API Developer Policies
- ห้าม **download/cache/store** audiovisual content โดยไม่ได้รับ approval จาก YouTube ([Developer Policies](https://developers.google.com/youtube/terms/developer-policies))
- ห้าม facilitate copyright infringement

### ผลกระทบต่อ trns-agents
| การกระทำ | ความเสี่ยง | แนวทางลดความเสี่ยง |
|----------|-----------|-------------------|
| yt-dlp ดาวน์โหลดวิดีโอ | ละเมิด ToS ถ้าใช้เชิงพาณิชย์/แจกจ่าย | **personal use only**; ไม่ re-upload; ไม่แจกไฟล์สาธารณะ |
| youtube-transcript-api scrape | gray area | ใช้เฉพาะ transcript ที่ YouTube เผยแพร่; พิจารณา TranscriptAPI ถ้า production |
| สร้างวิดีโอ dub แล้วแชร์ | ลิขสิทธิ์ของ creator | ได้รับอนุญาตจาก rights holder หรือใช้เฉพาะส่วนตัว |

> **Disclaimer:** ข้อมูลนี้เพื่อการวางแผน ไม่ใช่คำแนะนำทางกฎหมาย

## Technical risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| YouTube เปลี่ยน API/scrape | transcript ดึงไม่ได้ | fallback Whisper; หรือ paid API |
| TTS ไทยอ่านผิดคำ | คุณภาพต่ำ | LLM polish ก่อน TTS; แบ่ง chunk สั้น |
| Lip-sync ไม่ตรง | UX แย่ Phase 1 | ยอมรับใน Phase 1; Phase 2 Wav2Lip |
| วิดีโอยาว TTS drift | เสียงเพี้ยน | chunk < 2 นาที; Gemini แนะนำ |
| ค่า API สูง | เกินงบ | cache layers; Edge-TTS ฟรี |
| Windows FFmpeg setup | blocker dev | document install path |

## Checklist

- [ ] T001 [N] ผู้ใช้ยืนยัน **use case ส่วนตัว / ไม่ re-upload**
- [ ] T002 [N] ระบุ **acceptable legal posture** (personal only / licensed content / other)
- [ ] T003 [N] ยืนยัน **risk mitigations** ที่จะ implement ใน Phase 1
- [ ] T004 [N] เพิ่มข้อจำกัดที่จำเป็นใน [AGENTS.md](../AGENTS.md) non-negotiable rules
- [ ] T005 [N] สรุป **go/no-go** สำหรับเริ่ม implementation

## Decision (กรอกหลัง brainstorm)

- Legal posture: _(รอกรอก)_
- Go for implementation: _(รอกรอก)_
