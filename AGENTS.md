# trns-agents

## Repository mission

YouTube EN → TH dubbing assistant — **local-first** Phase 1 (personal use)

**Progress (QbjAQFJJyt0)**
- Batch 0–1 done: **329/1126** segments + partial `output.th.srt`
- Next: batch 2–6 → mux `output.th.mp4`
- FFmpeg ✅ | yt-dlp ✅

## Reload pack (new session)

- `@task/007-session-handoff.md` ← **start here**
- `@task/006-poc-implementation-scaffold.md`
- `@src/trns_agents/pipeline.py`

## Continuity — latest activity

### Snapshot (2026-06-11)

- Done: NLLB local, batch 0–1, FFmpeg/yt-dlp installed
- Interrupted: batch 2–6 run (not started)
- Next: [007-session-handoff](./task/007-session-handoff.md) T001–T002
- **Recommend: new session** with handoff prompt

## Non-negotiable rules

- Personal use only | local mode default
- `--resume` for long video | work dir `.trns-agents/{video_id}/`
