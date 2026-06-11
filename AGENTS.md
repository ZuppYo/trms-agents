# trns-agents

## Repository mission

YouTube EN → TH dubbing assistant — **local-first** Phase 1 (personal use)

**Progress (QbjAQFJJyt0)**
- TTS ครบ 1126 segments
- A/V sync: anchor `start_ms` + mild atempo (009 T001–T004 ✅)
- FFmpeg ✅ | yt-dlp ✅

## Reload pack (new session)

- `@task/009-session-handoff-av-sync.md` ← T005 full remux + subjective listen
- `@src/trns_agents/render/audio.py`
- `@scripts/analyze_dub_timing.py`

## Continuity — latest activity

### Snapshot (2026-06-11)

- Done: 009 T001–T004 — policy A; drift median **0**; full timeline **~34 min** (was ~54 min)
- Smoke `--max-batches 1` remux OK
- Next: T005 full remux + listen 0/10/20 min; T006 docs (partial)

## Non-negotiable rules

- Personal use only | local mode default
- `--resume` for long video | work dir `.trns-agents/{video_id}/`
