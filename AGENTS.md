# trns-agents

## Repository mission

YouTube EN → TH dubbing assistant — **personal use**; Phase 1 local audio **done** → Phase 2 **cloud (Gemini)**

## Non-negotiable rules

- Personal use only | work dir `.trns-agents/{video_id}/`
- `--resume` for long video | `--max-batches 1` for smoke

## Reload pack (new session)

- `@task/010-session-handoff-cloud-gemini.md` ← **start here**
- `@src/trns_agents/translate/__init__.py` · `@src/trns_agents/tts/__init__.py`
- `@src/trns_agents/render/audio.py`

## Continuity — latest activity

### Snapshot (2026-06-11)

- Done: [008](./task/archive/2026-06-11/008-dub-audio-continuity.md) audio continuity · [009](./task/archive/2026-06-12/009-session-handoff-av-sync.md) A/V sync (anchor `start_ms`, drift 0)
- Next: [010 cloud Gemini](./task/010-session-handoff-cloud-gemini.md) — `--mode cloud` แทน local
- Reload: `@task/010-session-handoff-cloud-gemini.md`
