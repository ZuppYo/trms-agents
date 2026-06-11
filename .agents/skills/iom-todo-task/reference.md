# iom-todo-task — templates and conventions

## Task file frontmatter

Every **numbered** task file (`task/NNN-*.md`, not `prompt.md` or `index.md`) MUST start with:

```yaml
---
title: "<short human title>"
type: <planning|improvement|execution|continuity|handoff>
detail: "<one line for index tables — no markdown>"
tags: [<tag1>, <tag2>]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

| Field | Use |
|-------|-----|
| `title` | Display name |
| `type` | Index grouping (`improvement`, `planning`, …) |
| `detail` | Copied into `task/index.md` active table |
| `tags` | Filter keys for index/search |
| `created` | Archive folder date (`task/archive/YYYY-MM-DD/`) |
| `updated` | Bump on every create, execute, or material edit |

**Slug** = basename without `.md` (e.g. `016-iom-todo-task-skill-improvement`). Use markdown links by default: `[016-iom-todo-task-skill-improvement](../../../task/016-iom-todo-task-skill-improvement.md)`.

## Task body skeleton

```markdown
---
title: "…"
type: planning
detail: "…"
tags: [skill]
created: 2026-05-28
updated: 2026-05-28
---

# <same as title>

Related: [015-session-continuity-compact](../../../task/015-session-continuity-compact.md) · [iom-todo-task](SKILL.md)

## Task Requirement

- Goal: …
- In scope / out of scope: …
- References: …

## Checklist

- [ ] T001 [N] …
```

## Bootstrap task skeleton (project day 0)

```markdown
---
title: "Project bootstrap"
type: planning
detail: "Initialize AGENTS/task baseline for new project"
tags: [bootstrap, task-management]
created: 2026-05-28
updated: 2026-05-28
---

# Project bootstrap

Related: [AGENTS](../../../AGENTS.md)

## Task Requirement

- Goal: Initialize AGENTS + task workflow for a new repo
- In scope: AGENTS compact baseline, task index/log, first execution flow
- Out of scope: implementation features

## Checklist

- [ ] T001 [N] Create/update `AGENTS.md` from ultra-compact template
- [ ] T002 [N] Ensure `task/index.md` and `task/log.md` exist
- [ ] T003 [N] Validate reload pack pointers and active task flow
```

## `task/index.md` skeleton

```markdown
# Task index

Read for **active** vs **archived** tasks. Use recent entries in `task/log.md` only (latest ~10).

## Active (`task/`)

| Slug | Title | Type | Tags | Updated | Status |
|------|-------|------|------|---------|--------|
| [016-example](./016-example.md) | … | improvement | skill | 2026-05-28 | open |

## Archived (`task/archive/`)

### 2026-05-27

| Slug | Title | Type | Tags | Created |
|------|-------|------|------|---------|
| [007-iom-sdd-context-skill-improvement-dod](./archive/2026-05-27/007-iom-sdd-context-skill-improvement-dod.md) | … | improvement | iom-sdd-context | 2026-05-27 |
```

**Status:** `open` = any `- [ ]` in checklist; `done` = all checklist items `- [x]` (or no checklist).

## `task/log.md` entry format

Append one block per event (newest at **end** of file):

```markdown
## [2026-05-28 14:30] created | 016-iom-todo-task-skill-improvement
- author: agent
- note: initial task from prompt.md § iOM Todo Task Improvement

## [2026-05-28 16:00] executed | 016-iom-todo-task-skill-improvement
- completed: T001, T002
- note: skills updated
```

**Read rule:** inspect only recent event headings from `task/log.md` (latest ~10); do not load full log unless debugging history.

## Numbering

- Next id = highest leading numeric prefix among `task/[0-9]{3,}-*.md` and `task/archive/**/[0-9]{3,}-*.md`, plus 1 (zero-padded recommended).
- Skip: `prompt.md`, `index.md`, `log.md`, unnumbered `*.handoff.md` unless tied to `NNN-` prefix.

## Frontmatter validation (minimum)

- `title`: non-empty string
- `type`: `planning|improvement|execution|continuity|handoff`
- `detail`: one-line non-empty string
- `tags`: non-empty array
- `created`, `updated`: `YYYY-MM-DD`

## Special files (never archive)

| File | Role |
|------|------|
| `task/index.md` | Agent index |
| `task/log.md` | Activity log |
| `task/prompt.md` | Scratch / prompts — not a numbered task |

`NNN-session-continuity-compact.md` — archive like other numbered tasks when done + age rule passes.
