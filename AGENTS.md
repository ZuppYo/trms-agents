# trns-agents

## Repository mission

ผู้ช่วยแปลภาษา (`trns-agents`) — Phase 1: ดึง transcript จากวิดีโอ YouTube (EN) แปลเป็นภาษาไทย แล้วสร้างวิดีโอใหม่ที่มีเสียงพากย์ไทย เพื่อให้ผู้ใช้ดูเนื้อหา YouTube เป็นภาษาไทยได้

**In scope (Phase 1)**
- รับ URL วิดีโอ YouTube → ดึง transcript/caption ภาษาอังกฤษ
- แปล transcript เป็นภาษาไทย (รักษา timestamp)
- สังเคราะห์เสียงพากย์ไทย (TTS) และซิงค์กับวิดีโอ
- ส่งออกวิดีโอ MP4 พร้อมเสียงไทย (และ/หรือ subtitle ไทย)

**Out of scope (Phase 1)**
- อัปโหลดกลับ YouTube หรือแจกจ่ายเนื้อหาที่ไม่มีสิทธิ์
- Lip-sync ระดับสูง / voice cloning ตามตัวพูดต้นฉบับ
- แพลตฟอร์มอื่นนอกจาก YouTube
- UI/เว็บแอป production (ยกเว้นถ้า BRT tasks กำหนดใหม่)

## Non-negotiable rules

- ใช้ workflow task ผ่าน `task/index.md` + `task/log.md` — สร้าง/รัน/archive ตาม skill `iom-todo-task`
- Phase 1 เน้น pipeline ที่ทำงาน end-to-end ได้จริงก่อน polish
- ต้องเคารพ YouTube ToS และลิขสิทธิ์ — ใช้สำหรับ personal/educational; ไม่ re-upload โดยไม่มีสิทธิ์
- เก็บ API keys ใน env — ห้าม commit secrets
- เอกสาร requirement อยู่ใน task BRT series; AGENTS เป็น pointer เท่านั้น
- ภาษาเป้าหมาย Phase 1: EN → TH เท่านั้น
- รักษา timestamp ตลอด pipeline (transcript → แปล → TTS → mux)
- เลือก stack ที่ reproducible (Python + FFmpeg เป็นฐาน) จนกว่า BRT004 จะตัดสิน
- ทุก session อ่าน reload pack ก่อนเริ่มงาน

## Reload pack (minimal)

- `@AGENTS.md`
- `@task/index.md`
- `@task/log.md` (ล่าสุด ~10 entries)
- `@task/001-brt-project-vision.md` (active แรก)
- `@task/prompt.md` (origin prompt)

## Continuity — latest activity

### Snapshot (2026-06-11)

- Done: bootstrap — สร้าง AGENTS.md, task index/log, BRT001–BRT005
- Next: `001-brt-project-vision` — brainstorm เป้าหมายและขอบเขตกับผู้ใช้
- Reload: `@task/001-brt-project-vision.md`

## Task state pointers

- Active index: [task/index.md](task/index.md)
- Activity log: [task/log.md](task/log.md)
- Brainstorm/requirements: BRT001–BRT005 ใน `task/`
- Archive: `task/archive/YYYY-MM-DD/`

## Token hygiene policy

- AGENTS < ~250 บรรทัด; continuity แทนที่ snapshot เก่า ไม่ append
- รายละเอียดเทคนิค/ research อยู่ใน task files ไม่ duplicate ใน AGENTS
