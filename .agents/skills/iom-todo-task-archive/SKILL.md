---
name: iom-todo-task-archive
description: >-
  Archives completed IOM task markdown files from task/ into task/archive/{created-date}/,
  using task/index.md and task/log.md. Moves tasks whose checklists are fully done and whose
  created date is at least one calendar day old. Updates index, log, and AGENTS.md continuity.
  Use when the user asks to archive tasks, run iom-todo-task-archive, or tidy the task folder.
disable-model-invocation: true
---

# IOM Todo Task Archive

Move **finished** numbered tasks from `task/` to `task/archive/{created}/`, then refresh index, log, and **`AGENTS.md`** continuity.

**Prerequisites:** [`task/index.md`](../../../task/index.md) and [`task/log.md`](../../../task/log.md) exist (created by **iom-todo-task**). Read [`../iom-todo-task/reference.md`](../iom-todo-task/reference.md) for frontmatter and slug rules.

---

## Quick start

1. Read `task/index.md` and only recent entries from `task/log.md` (latest ~10 event headings)
2. List candidates in `task/[0-9]{3,}-*.md` (exclude `index.md`, `log.md`, `prompt.md`)
3. For each candidate, apply **eligibility** (below)
4. Move eligible files → `task/archive/{created}/`
5. Update `task/index.md`, append `task/log.md`, patch **`AGENTS.md`** § Continuity

**STOP** after presenting the move plan; wait for user **go** before moving files (same guardrail as task execution).

---

## Eligibility

Archive a numbered task file when **all** are true:

| Rule | Check |
|------|--------|
| **Done** | Every checklist `- [ ]` is absent OR all items are `- [x]` (ignore `Task Requirement` prose) |
| **Age** | Frontmatter `created` ≤ **yesterday** (calendar date using current system date in `YYYY-MM-DD`; if date context is unavailable, ask user to confirm today's date before archiving) |
| **Location** | File is directly under `task/`, not already under `task/archive/` |

**Also move** (same archive folder, same `created` date):

- `task/{NNN}-*.handoff.md` if present for the same numeric prefix `NNN`
- Other `task/{NNN}-*` siblings created as part of the same task (e.g. extra plans) when user confirms or task log references them

**Do not archive:** `task/index.md`, `task/log.md`, `task/prompt.md`, or any file with open `- [ ]` items.

---

## Archive path

Destination: `task/archive/{created}/` where `{created}` is the task file’s YAML `created` value (`YYYY-MM-DD`).

Example: `task/007-foo.md` with `created: 2026-05-27` → `task/archive/2026-05-27/007-foo.md`

Create the date folder if missing.

---

## After move

### 1. `task/log.md`

Append:

```markdown
## [YYYY-MM-DD HH:MM] archived | <slug>
- moved: task/<file> → task/archive/<created>/
- related: <handoff or siblings if any>
```

### 2. `task/index.md`

- Remove row from **Active**
- Add row under **Archived → {created}** (create `### YYYY-MM-DD` if needed)
- Set status `done` on archived rows

### 3. `AGENTS.md` — Continuity block (required in this standard)

Update **only** the `## Continuity — latest activity` section:

- Replace with **one** recent snapshot (date = today), never append old snapshots
- **Done:** up to 2-3 bullets max; each one line only
- **Next:** one highest-priority active task only
- **Reload:** one file pointer only (prefer active continuity task or highest-priority active task)
- Keep continuity concise; avoid embedding long implementation details (link to task/archive instead)

Do **not** duplicate full task/014 history — keep the block short (same style as current AGENTS.md).

Use compact structure from: `.agents/skills/iom-todo-task-archive/references/AGENTS_ULTRA_COMPACT_TEMPLATE.md`

---

## Confirmation message

```
📦 Archive plan

Candidates (eligible):
1. 007-… — created 2026-05-27, all [x]
…

Skipped:
- 015-… — open checklist items
- 010-… — created today (age rule)

Destinations:
- task/archive/2026-05-27/007-….md
…

Will update: task/index.md, task/log.md, AGENTS.md § Continuity

Reply "go" to archive, or "1,3" for subset, or "stop".
```

---

## Errors

- Missing frontmatter `created` → ask user to fix or set from file mtime; do not archive until valid
- Archive folder collision (file already exists) → skip and report
- No eligible files → report and suggest running **iom-todo-task** to close checklists first

---

## Minimum test scenarios

- Create a numbered task with valid frontmatter, then verify it appears in `task/index.md` as `open`
- Execute task checklist until all items are `[x]`, then verify `task/log.md` has `executed` entry
- Archive success: done task with `created <= yesterday` moves to `task/archive/{created}/`, and index/log/AGENTS continuity are updated
- Archive skip: task still has `- [ ]` or `created` is today; report as skipped without moving files
