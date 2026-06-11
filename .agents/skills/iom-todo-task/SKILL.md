---
name: iom-todo-task
description: >-
  Creates or executes IOM task markdown under task/: YAML frontmatter, markdown links,
  task/index.md, and task/log.md. On create, allocates NNN-slug, updates index and log. On execute,
  reads Task Requirement then - [ ] items ([N]/[U]), writes - [x] and bumps updated/log/index.
  Use for iom-todo-task, new task checklists, or running task/*.md sequentially.
disable-model-invocation: false
---

# IOM Todo Task

**Create** planning/execution tasks under `task/`, or **execute** an existing task file. Templates: [reference.md](reference.md).

**Related skill:** [iom-todo-task-archive](../iom-todo-task-archive/SKILL.md) — move finished tasks to `task/archive/{created}/`.

## Standards (portable v1)

- Canonical task paths: `task/`, `task/index.md`, `task/log.md`, `task/archive/{YYYY-MM-DD}/`
- Numbered task filename: `{NNN}-{kebab-summary}.md` where `NNN` is the leading numeric id (zero-padded recommended; sort by numeric prefix)
- Required frontmatter fields: `title`, `type`, `detail`, `tags`, `created`, `updated`
- Link default: Markdown links (`[label](path-or-file.md)`); Obsidian wikilinks are optional only when user explicitly requests

**Agent context (before any work):**

1. Read [`task/index.md`](../../../task/index.md) for active vs archived tasks
2. Read recent entries from `task/log.md` only (latest ~10 event headings); avoid shell-specific commands when possible

---

## Mode 0 — Bootstrap project task system

Use when starting a new project or when `AGENTS.md` / `task/` baseline is missing.

### 0.1 Detect baseline

1. Check whether `AGENTS.md` exists at repo root
2. Check whether `task/index.md` and `task/log.md` exist
3. If missing, create them from templates (see [reference.md](reference.md))

### 0.2 Initialize AGENTS.md (compact)

1. Create or update `AGENTS.md` using compact template:
   - `.agents/skills/iom-todo-task-archive/references/AGENTS_ULTRA_COMPACT_TEMPLATE.md`
2. Keep only one latest continuity snapshot (do not append history)
3. Keep AGENTS focused on pointers; move deep history to `task/archive/` or dedicated docs

### 0.3 Create bootstrap task

1. Create first numbered task for project bootstrap (e.g. `000-project-bootstrap.md` or next available id)
2. Include checklist for:
   - mission + hard constraints finalized in `AGENTS.md`
   - reload pack paths validated
   - task workflow verified (`create`, `execute`, `archive`)
3. Append `created` event to `task/log.md` and add active row in `task/index.md`

### 0.4 Confirmation

Report created/updated files and ask user to continue execution:

`go` | `1,3` | `go + <detail>` | `stop`

---

## Mode A — Create task

Use when the user asks to **create**, **plan**, or **add** a new task under `task/`.

### A1. Allocate slug

1. Scan `task/` and `task/archive/**/` for files matching `^[0-9]{3,}-.*\.md$`
2. Extract leading numeric prefix (`NNN`) from basename and compute next id = max + 1
3. Slug = `{NNN}-{kebab-summary}.md` (e.g. `016-iom-todo-task-skill-improvement.md`)

### A2. Write task file

1. Create `task/{slug}.md` with YAML frontmatter (`title`, `type`, `detail`, `tags`, `created`, `updated`) — see [reference.md](reference.md)
2. Validate minimum frontmatter:
   - `title` non-empty string
   - `type` one of `planning|improvement|execution|continuity|handoff`
   - `detail` non-empty one line
   - `tags` non-empty array
   - `created`, `updated` in `YYYY-MM-DD`
3. Body: `# title`, related markdown links, `## Task Requirement`, `## Checklist` with `- [ ]` items
4. Set `created` and `updated` to today (`YYYY-MM-DD`)

### A3. Ensure `task/index.md` and `task/log.md`

If missing, create from [reference.md](reference.md) skeletons.

### A4. Update index and log

1. **index.md** — add row under **Active** (`Status: open`)
2. **log.md** — append:

```markdown
## [YYYY-MM-DD HH:MM] created | <slug-without-.md>
- type: <type>
- note: <one line from user request>
```

3. Present path and markdown link to the new task; **do not** execute checklist unless user says **go**

---

## Mode B — Execute task

Use when the user provides a task file path or asks to **run** / **execute** a checklist.

### B0. Context

1. Read task frontmatter; if `updated` stale after edits, bump at end of session
2. Optional: skim `task/index.md` row for this slug

### B1. Read Task File

1. Read the specified markdown file
2. **Task Requirement** — Find heading **Task Requirement** (or Thai equivalents / `Requirements` when clearly document-level). Read from heading through next same-or-higher-level heading **before** any `- [ ]` work.
   - Missing section → note `No "Task Requirement" section found — proceeding from checklist only`
   - Empty section → ask user to fill or confirm
3. Parse unchecked `- [ ]`; skip `- [x]`
4. Confirm with user (**STOP** until **go**, **1,3**, **go + …**, **stop**, or clarification):

```
📋 Task File: <filename>
Found <N> pending tasks:
…
---
🔲 Your turn: go | 1,3 | go + <detail> | stop | <clarification>
```

### B2. Execute Tasks

For each pending item:

0. **Task Requirement wins** over conflicting checkbox text
1. **`[N]`** — new work; **`[U]`** — read prior result/output first, patch only; no flag = `[N]`
2. Follow links/paths in the task line for context
3. Mark `- [x]` with `  - ✅ <result>` (or `  - ⚠️ <reason>` if failed; leave unchecked on hard failure)

After each completed item (or end of batch): bump frontmatter `updated`; append **log.md** `executed | <slug>` with completed ids; set index **Status** to `done` only when **all** checklist items are `[x]`.

### B3. Report

```
📋 Task Execution Complete
✅ Completed: <N>
…
Updated: <filename>, task/log.md, task/index.md (if status changed)
```

---

## Task Requirement section (document-level)

```markdown
## Task Requirement

- Goal: …
- In scope / out of scope: …
- References: [other-task](../task/other-task.md), paths …
```

Mandatory read when present — see Mode B1.

---

## Checklist format

| Flag | Meaning |
|------|---------|
| `[N]` | New — create/overwrite as needed |
| `[U]` | Update — preserve existing output; patch only |
| (none) | Treat as `[N]` |

```markdown
- [ ] T001 [N] Create [task/index.md](../../../task/index.md)
- [ ] T002 [U] Update [015-session-continuity-compact](../../../task/015-session-continuity-compact.md) per review
```

Completed:

```markdown
- [x] T001 [N] …
  - ✅ <result>
```

---

## Behavioral rules

- **Index + log:** On create and on material execute progress, update `task/index.md` and append `task/log.md`
- **Frontmatter:** Never remove YAML; keep `title`/`detail` in sync with index row when title changes
- **Links:** Use markdown links by default; allow wikilinks only when user explicitly requests
- **Language:** Match task file (Thai/English)
- **Order:** Execute checklist top to bottom
- **Safety:** No destructive ops without explicit confirmation; `go +` user text overrides task text where applicable
- **Scope:** Do not edit files outside checklist intent except index/log/frontmatter updates above
- **Archive:** Do not move files to `task/archive/` — use **iom-todo-task-archive**

---

## Error handling

| Case | Action |
|------|--------|
| Task file missing | Stop; report |
| Referenced file missing | Note in result; continue if possible |
| `[U]` with no prior result | Treat as `[N]`; note in result |

---

## Examples

**Create:** User: "สร้าง task ปรับ skill iom-todo-task" → `016-….md`, index row, log `created`, show task path/link.

**Execute:** User: `@task/016-….md go` → Task Requirement → checkboxes → log `executed`.

**Context reload:** `@task/index.md` + recent `task/log.md` entries + active task file.
