# trns-agents

## Repository mission

ผู้ช่วยแปลภาษา (`trns-agents`) — Phase 1: YouTube EN → TH dubbing (personal use)

**In scope (Phase 1)**
- CLI: `trns-agents dub <url> --mode cloud|local [--resume] [--transcript file.vtt]`
- Transcript: auto │ Whisper (planned) │ manual VTT/SRT
- แปล + TTS เสียงผู้ชาย + **แทนที่ audio** + export **SRT**
- วิดีโอยาว: chunked batches + checkpoint ใน `.trns-agents/{video_id}/`
- Code: `src/trns_agents/`

**Out of scope (Phase 1)**
- Re-upload, public distribution, UI, batch playlist

## Non-negotiable rules

- Personal use only — ไม่ re-upload / ไม่แจกจ่าย
- Task workflow: `task/index.md` + `task/log.md`
- API keys ใน `.env` — ห้าม commit
- EN → TH; TTS male (`th-TH-NiwatNeural` / Gemini `Charon`)
- Timestamp รักษาตลอด pipeline
- Work dir checkpoint + `--resume` สำหรับวิดีโอยาว

## Reload pack (minimal)

- `@AGENTS.md`
- `@task/index.md`
- `@task/log.md` (tail ~10)
- `@task/006-poc-implementation-scaffold.md`
- `@src/trns_agents/pipeline.py`

## Continuity — latest activity

### Snapshot (2026-06-11)

- Done: BRT004–BRT005 — stack lock, cost estimate, legal GO
- Done: `006-poc-implementation-scaffold` — CLI + pipeline skeleton
- Next: T007 smoke test + NLLB/Whisper wiring
- Reload: `@task/006-poc-implementation-scaffold.md`

## Task state pointers

- Index: [task/index.md](task/index.md)
- Log: [task/log.md](task/log.md)
- Architecture: [003-brt-pipeline-architecture.md](task/003-brt-pipeline-architecture.md)
