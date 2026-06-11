# trns-agents

## Repository mission

YouTube EN → TH dubbing assistant — **local-first** Phase 1 (personal use)

**In scope**
- CLI: `trns-agents dub <url> --mode local [--resume] [--redo-batches 0] [--max-batches N]`
- Translate: **NLLB-200** local | TTS: **Edge `th-TH-NiwatNeural`**
- Checkpoint: `.trns-agents/{video_id}/` — 7 batches (~5 min each)
- Code: `src/trns_agents/`

**Progress (QbjAQFJJyt0)**
- Batch 0–1 done (~326/1126 segments) + `output.th.srt`
- Batch 2–6 pending | MP4 pending (needs FFmpeg + yt-dlp)

## Non-negotiable rules

- Personal use only
- Task workflow: `task/index.md` + `task/log.md`
- Local mode default — cloud optional later
- `--resume` / `--redo-batches` for long video workflow

## Reload pack

- `@task/006-poc-implementation-scaffold.md`
- `@src/trns_agents/pipeline.py`
- `@.trns-agents/QbjAQFJJyt0/segments.json`

## Continuity — latest activity

### Snapshot (2026-06-11)

- Done: NLLB local translate + `--redo-batches`
- Done: batch 0–1 dubbed (local) for QbjAQFJJyt0
- Next: batch 2–6 (`--resume --max-batches 3…`) then FFmpeg mux
- Reload: `@task/006-poc-implementation-scaffold.md`
