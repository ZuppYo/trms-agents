# AGENTS Ultra-Compact Template

Use this template for long-running projects to reduce startup token usage across sessions.

## Project initialization (day 0)

Recommended startup via iOM skills:

1. Use `iom-todo-task` to bootstrap task system (`task/index.md`, `task/log.md`) if missing
2. Create first task: `000-project-bootstrap.md` (or `001-...` if numbering already used)
3. Fill AGENTS using this template with only:
   - Mission (1 line)
   - Hard constraints (5-10 bullets)
   - Reload pack (minimal pointers only)
   - Continuity snapshot (one block only)
4. Run `iom-todo-task` execution on bootstrap task until done
5. Use `iom-todo-task-archive` only when checklist is done and age rule passes

Day-0 deliverables:
- `AGENTS.md` (compact)
- `task/index.md`
- `task/log.md`
- `task/000-project-bootstrap.md` (or next numbered task)

## Repository mission

- One-line scope of this repo
- In-scope vs out-of-scope in 3-6 bullets total

## Non-negotiable rules

- 5-10 bullets only (hard constraints)
- Keep each bullet one line

## Reload pack (minimal)

- `@AGENTS.md`
- `@task/index.md`
- `@task/log.md` (latest 10-20 entries only)
- 1 active task file only (highest priority)
- 1-2 core spec/context paths only

## Continuity — latest activity

Keep this section short and replace old snapshot each time (do not append history).

### Snapshot (YYYY-MM-DD)

- Done: `<task-slug>` — one-line outcome
- Done: `<task-slug>` — one-line outcome
- Next: `<single highest-priority task>`
- Reload: `<single reload task/file>`

## Task state pointers

- Active index: `task/index.md`
- Activity log: `task/log.md` (read tail only)
- Archive: `task/archive/YYYY-MM-DD/`

## Token hygiene policy

- Keep `AGENTS.md` under ~250 lines
- Keep Continuity section under ~50 lines
- Never duplicate old continuity snapshots
- Never paste long task details into AGENTS; link instead
- Prefer pointers over prose

## Optional deep context (link-only)

- `docs/history/` or `task/archive/` for full history
- Long implementation notes stay outside AGENTS
