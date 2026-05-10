# OPSX: Apply with BDD Gate

> **Portability note:** This file lives in two places:
> - `~/.claude/commands/opsx/apply-bdd.md` — global fallback, used in any project
> - `.claude/commands/opsx/apply-bdd.md` — project-local copy (takes precedence), should be committed to the repo
>
> When setting up a new project, copy this file into `.claude/commands/opsx/` alongside the other opsx commands. Update the copy whenever the OpenSpec framework changes its conventions.
>
> Written against **openspec 1.3.0**. If `openspec --version` returns a higher major version, check the changelog before using.

Implement tasks from an OpenSpec change — with BDD test gates enforced after each task.

**Difference from `/opsx:apply`**: After each completed task, BDD scenarios for this change must be GREEN or PENDING before marking `[x]`. A task is not done until the tests agree.

**Input**: Optionally specify a change name (e.g., `/opsx:apply-bdd foundation`). If omitted, infer from context or prompt.

---

## Steps

### 1. Select the change and verify framework version

```bash
openspec --version 2>/dev/null || echo "NOT_FOUND"
```

- If `NOT_FOUND`: abort — "openspec CLI not found. Install it or run from a project where it is available."
- If the returned major version is higher than **1**: warn the user —
  "This skill was written for openspec 1.x. The installed version is X.Y.Z — directory conventions may have changed. Check `.claude/commands/opsx/apply-bdd.md` in the project for an updated copy."
  Then continue anyway (do not abort) unless the user stops you.

If a name is provided, use it. Otherwise:
- Infer from conversation context
- Auto-select if only one active change exists
- If ambiguous, run `openspec list --json` and use **AskUserQuestion** to let the user select

Always announce: "Using change: `<name>`"

### 2. Check schema and status

```bash
openspec status --change "<name>" --json
```

Parse: `schemaName`, which artifact holds tasks, overall progress.

### 3. Get apply instructions

```bash
openspec instructions apply --change "<name>" --json
```

Handle states:
- `blocked` → show message, suggest `/opsx:continue`
- `all_done` → congratulate, suggest `/opsx:archive`
- Otherwise → proceed

### 4. Read context files

Read all files listed in `contextFiles` (proposal, specs, design, tasks for spec-driven).

### 5. Check BDD gate status

```bash
ls e2e/features/<name>/ 2>/dev/null | head -20
```

- Files found → **BDD gate ACTIVE** — tests gate every task completion
- No files found → **BDD gate INACTIVE** — suggest running `/opsx:bdd <name>` first, then proceed without gate

### 6. Show current progress

```
## Implementing: <name> (schema: <schema>)
BDD gate: ACTIVE — N feature files  |  INACTIVE
Progress: N/M tasks complete
```

### 7. Implement tasks (loop until done or blocked)

For each pending task:

a. Announce which task is being worked on  
b. Make the code changes (minimal, focused)  

**After each task — BDD gate check (ACTIVE only):**

```bash
npx bddgen 2>&1 && npx playwright test --project=bdd-web e2e/features/<name>/ --reporter=line 2>&1 | tail -30
```

Interpret results:
- All GREEN or PENDING → mark task complete: `- [ ]` → `- [x]`
- Any FAILED (real assertion failure, not pending) → do NOT mark `[x]`:
  - Show which scenarios failed
  - Continue implementing until they pass
- `bddgen` error → fix the `.feature` file or step stub, retry

If BDD gate INACTIVE → mark task complete immediately.

**Pause if:**
- Task is unclear → ask for clarification
- Implementation reveals a design issue → suggest updating artifacts
- Error or blocker → report and wait
- User interrupts

### 8. Final BDD gate — before declaring completion

If BDD gate ACTIVE:

```bash
npx bddgen 2>&1 && npx playwright test --project=bdd-web e2e/features/<name>/ --reporter=list 2>&1 | tail -40
```

- All GREEN or PENDING → change complete
- Still RED → show which scenarios remain, pause

### 9. Show completion status

```
## Implementation Complete

**Change:** <name>
**Schema:** <schema>
**Progress:** 7/7 tasks ✓
**BDD:** N GREEN, N PENDING

All tasks complete! Run /opsx:archive <name> to archive.
```

---

## Guardrails

- NEVER mark a task `[x]` if related BDD scenarios are FAILED
- Always read context files before starting
- Keep code changes minimal and scoped to each task
- Pause on blockers or unclear requirements — don't guess
- If implementation reveals design issues → suggest updating artifacts first
- BDD gate is per-platform: `--project=bdd-web` for `@web` scenarios; adjust for `@cli` / `@api` if those platforms are in scope
