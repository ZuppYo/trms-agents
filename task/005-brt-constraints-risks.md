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

- Goal: ระบุข้อจำกัดและความเสี่ยงก่อน implement
- In scope: legal/ToS, technical risks, mitigation, go/no-go
- Out of scope: คำแนะนำทางกฎหมายเชิง professional

## Legal posture (confirmed)

| ข้อ | คำตอบผู้ใช้ |
|-----|-------------|
| Use case | **Personal only** — ใช้เอง Phase 1 |
| Re-upload / แจกจ่าย | **ไม่ทำ** |
| Acceptable risk | ยอมรับ gray area ของ yt-dlp / transcript scrape ภายใต้ personal use |

> Disclaimer: ไม่ใช่คำแนะนำทางกฎหมาย — ดู [YouTube ToS](https://www.youtube.com/static?template=terms)

## Mitigations implemented Phase 1

| Risk | Mitigation ใน code/docs |
|------|-------------------------|
| ToS / copyright | CLI docstring + AGENTS: personal use only |
| API keys leaked | `.env` + `.gitignore` |
| วิดีโอยาวล้มกลางทาง | batch checkpoint + `--resume` |
| Transcript scrape fail | manual `--transcript` + Whisper (optional extra) |
| ค่า API สูง | `--mode local`; cost doc ใน BRT004 |
| FFmpeg missing | clear error จาก subprocess |

## Decision

- **Legal posture:** personal use, no redistribution
- **Go for implementation:** **GO** — POC scaffold เริ่มแล้ว (`src/trns_agents/`)

## Checklist

- [x] T001 [N] ผู้ใช้ยืนยัน **use case ส่วนตัว / ไม่ re-upload**
  - ✅ ยืนยันใน BRT001/BRT002
- [x] T002 [N] ระบุ **acceptable legal posture**
  - ✅ personal only
- [x] T003 [N] ยืนยัน **risk mitigations** Phase 1
  - ✅ ตารางด้านบน
- [x] T004 [N] เพิ่มข้อจำกัดใน [AGENTS.md](../AGENTS.md)
  - ✅ มีอยู่แล้ว + POC go
- [x] T005 [N] สรุป **go/no-go**
  - ✅ GO
