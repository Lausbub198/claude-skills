---
name: spec2opsx
description: Converts a spec document into OpenSpec (opsx) changes. Splits the document into logical units, initializes opsx if needed, and creates all artifacts (proposal, specs, design, tasks) per change. Supports --fast and --tools flags.
version: 1.2.0
requires: openspec CLI (npm install -g openspec)
---

# spec2opsx — Spec Document → OpenSpec Changes

Converts a specification document into a set of OpenSpec changes, each with a full artifact set.

## Invocation

```
/spec2opsx <path-to-spec>
/spec2opsx <path-to-spec> --fast
/spec2opsx <path-to-spec> --tools claude
/spec2opsx <path-to-spec> --tools claude,cursor --fast
```

**Flags:**

| Flag | Description |
|------|-------------|
| `--fast` | Skip confirmation step, use `/opsx:ff` per change instead of `/opsx:continue` |
| `--tools <list>` | AI tools to configure during `openspec init` (comma-separated). Skips the tools prompt. |

**Supported `--tools` values:** `amazon-q`, `antigravity`, `auggie`, `bob`, `claude`, `cline`, `codex`, `cursor`, `factory`, `gemini`, `github-copilot`, `windsurf`, `roocode`, `trae`, and others. Use `all` or `none` as shortcuts.

If no path is provided, ask the user before continuing.

---

## Step 0: Preflights

Run these checks in order before doing anything else.

### 0a. Spec file exists

```bash
test -f "<provided-path>" && echo "FILE_OK" || echo "FILE_NOT_FOUND"
```

If `FILE_NOT_FOUND`: stop immediately and tell the user:
> "Spec file not found at `<path>`. Please provide the correct path."

### 0b. Multi-repo check

Scan the first 200 lines of the spec for signals of multiple distinct services or repositories (e.g., separate backend and frontend repos, monorepo workspaces, microservices with different roots).

If detected: **before continuing**, ask:
> "This spec describes multiple services. Which project root should OpenSpec be initialized in? (Provide the directory path, or type 'ask' to decide per-change.)"

Wait for the user's answer before proceeding to 0c.

### 0c. OpenSpec CLI installed

```bash
which openspec 2>/dev/null && echo "CLI_OK" || echo "CLI_NOT_FOUND"
```

If `CLI_NOT_FOUND`: stop immediately and tell the user:
> "The `openspec` CLI is not installed. Install it first:
> ```
> npm install -g openspec
> ```
> Then re-run `/spec2opsx`."

### 0d. Project init check

```bash
ls openspec/ 2>/dev/null && echo "INITIALIZED" || echo "NOT_INITIALIZED"
```

**If `INITIALIZED`:** confirm `✓ OpenSpec already present` and continue to Step 0e.

**If `NOT_INITIALIZED`:**

1. Inform the user: `OpenSpec is not yet initialized in this project.`
2. Determine the tools value:
   - If `--tools` was passed: use that value directly
   - If `--tools` was not passed: ask — `Which AI tools should be configured? (e.g. claude, cursor, claude,cursor — or "all"/"none")`
   - Default if the user presses Enter without input: `claude`
3. Run init non-interactively:
   ```bash
   openspec init --tools <tools-value>
   ```
4. Confirm: `✓ OpenSpec initialized (tools: <tools-value>)`

> Note: The expanded command set (`/opsx:new`, `/opsx:ff`, `/opsx:continue`, etc.) is a global profile setting. This skill does not touch it — the user manages their own profile via `openspec config profile`.

### 0e. Skill recommendations

Scan the spec for technology signals. For each technology detected, identify Claude Code skills that encode best practices for that tech. Present these to the user so they can decide whether to embed skill references in the generated artifacts.

#### Technology → skill mapping

| If spec mentions... | Relevant skills |
|---------------------|-----------------|
| Node.js, Express, Fastify, Hono | `backend-patterns` |
| React, Next.js, Vite, Remix | `react-best-practices`, `frontend-patterns` |
| TypeScript | `coding-standards` |
| Python, FastAPI, Flask | `python-patterns` |
| Django | `django-patterns` |
| Go / Golang | `golang-patterns` |
| Kotlin, Spring Boot | `kotlin-patterns`, `springboot-patterns` |
| REST API, HTTP endpoints | `api-design` |
| tests, Jest, Vitest, pytest | `tdd-workflow` |
| E2E, Playwright, Cypress | `e2e-testing` |
| auth, JWT, OAuth, sessions | `security-review` |
| WebSocket, SSE, real-time | `backend-patterns` |
| Tailwind, CSS, animations | `frontend-patterns` |
| PostgreSQL, MySQL, Prisma, Drizzle | `backend-patterns` |
| Vanilla JS, no framework, single-file HTML | `coding-standards`, `frontend-patterns` |
| IndexedDB, localStorage, Web Storage | `coding-standards` |
| BroadcastChannel, inter-window sync, multi-window | `backend-patterns` |
| Custom parser, custom syntax, custom markdown | `coding-standards` |
| Web Audio API, AudioContext | *(no skill covers this yet — note in report)* |
| ZIP, JSZip, file export/import | `coding-standards` |

Skill installation source: `https://github.com/anthropics/claude-code-skills` (everything-claude-code collection).

#### Checking which skills are available

Claude Code skills are only visible when loaded into the active session — there is no command to enumerate installed skills. Instead, present **all** recommended skills and ask the user which ones they have installed:

```
Detected tech stack: [list from scan]

Recommended skills:
  backend-patterns
  coding-standards
  frontend-patterns
  tdd-workflow
  [... others detected]

Which of these do you have installed?
(Type the names, "all", or "none". If unsure, type "unknown" and all will be embedded as references.)
```

Use the user's answer to determine availability:
- If the user lists specific names: those are ✓ available, others are ⚠ not installed
- If `all`: all recommended skills are available
- If `none`: treat all as not installed
- If `unknown`: treat all as available (embed all references; user can remove unused ones)

#### Ask the user how to handle skills in artifacts

After presenting the list, ask:

```
Embed skill references in generated artifacts (design.md / tasks.md)?
  [A] Yes, all recommended skills (including not-yet-installed)
  [B] Yes, available skills only
  [C] Skip — no skill references in artifacts
```

**Store the user's choice as `skill-mode` in the conversation context.** This choice is used throughout Step 3 — confirm it before creating the first change's artifacts if there have been many turns between this step and Step 3. Default if the user does not answer or skips: **[C]**.

---

## Step 1: Analyze the Spec Document

Read the spec document in full. Identify logical change boundaries using this principle:

**Primary goal: vertical slices — each change is testable end-to-end immediately after implementation.**

A vertical slice bundles the backend logic, API endpoint(s), and frontend UI for a single feature into one change. After implementing it, the developer runs the app and verifies the feature works — without needing a future change to complete the loop.

**How to slice:**
- Find natural feature boundaries: a data event + the UI that displays it, an action + the endpoint that handles it
- Include both the backend piece AND the frontend piece in the same change when they form a complete testable unit
- One change = one "I can demo this right now" moment

**Exception — foundation change:**
The very first change is always infrastructure: the server, shared state, WebSocket connection, frontend shell, and design tokens. This is the skeleton that makes all subsequent slices runnable. Keep it as thin as possible — only what is needed to get a blank dashboard up and connected.

**Keep together when:**
- Backend and frontend serve the same feature (default: yes, put them together)
- A piece is small and only makes sense alongside a neighboring feature
- Infrastructure wiring that has no standalone testable behavior

**Split into separate changes when:**
- Two features are genuinely independent and can be tested without each other
- A feature is large enough that its backend and frontend each warrant separate review sessions
- One part has a hard dependency that the other doesn't share

**Ordering:** Each change must be immediately runnable after the previous one.
1. Foundation (server + WebSocket + frontend shell + design tokens) — blank connected dashboard
2. Feature slices in dependency order — each adds one testable capability
3. Last: cross-cutting concerns (OBS mode, reconnect logic, polish)

**Example for a real-time dashboard:**
- Change 1: foundation (server, session, blank UI, WebSocket connected)
- Change 2: file-tracking (file watcher backend + file tree widget — test: save a file, see it appear)
- Change 3: git-tracking (git watcher + git activity widget — test: commit, see it on timeline)
- Change 4: code-preview (code stream widget — test: save file, see code update live)
- Change 5: act-management (act:set + progress tracker — test: Cmd+1, stepper updates)
- Change 6: live-stats (stats broadcast + stats bar — test: watch counters update)

---

## Step 2: Propose the Breakdown

> Skip this step in `--fast` mode.

Present the proposed changes as a numbered list:

```
Proposed breakdown: X changes

1. <change-name>
   What: <one sentence describing scope>
   Why separate: <dependency or independence reason>

2. <change-name>
   ...

Order reflects build dependencies.
Proceed? (or describe adjustments)
```

Wait for user confirmation or adjustments before continuing.

In **`--fast` mode**: show a brief summary (`X changes: [name-1], [name-2], ... — proceeding.`) and continue without waiting.

---

## Step 3: Execute — Create Changes and Artifacts

Before creating the first change, confirm the `skill-mode` choice from Step 0e if more than a few turns have passed: `"Proceeding with skill-mode [A/B/C] — correct?"`. If the user doesn't remember or says skip: use **[C]**.

For each change in order:

### 3a. Create the change scaffold

```
/opsx:new <change-name>
```

Change names must be kebab-case and under 40 characters.

Emit a status line before each artifact so the user can follow along:

```
── Change 1/N: <change-name> ──
```

### 3b. Create artifacts

`/opsx:continue` is context-driven — it picks up from the current change scaffold and creates the next artifact in sequence (proposal → specs → design → tasks). Call it once per artifact.

**`--fast` mode:** Use `/opsx:ff` — creates all artifacts in one step. No pauses.

**Normal mode:** Call `/opsx:continue` once per artifact, emit a status line before each call, and pause for user review:

1. `Creating proposal.md...` → `/opsx:continue` → wait for user review
2. `Creating specs/...` → `/opsx:continue` → wait for user review
3. `Creating design.md...` → `/opsx:continue` → **pause and explicitly tell the user:** *"This is the right moment to adjust tech choices, architecture, or integration points before tasks are generated. Any changes now are cheap — once tasks are created you'd need to revise them too."* Then wait.
4. `Creating tasks.md...` → `/opsx:continue`

After all 4 artifacts for a change are done, emit: `✓ <change-name> complete (proposal / specs / design / tasks)` before moving to the next change.

### What belongs in each artifact

**`proposal.md`** — Extract from spec:
- The problem being solved and why it matters
- Scope: what is and is not included in this change
- Success criteria

**`specs/`** — Extract from spec:
- Functional requirements
- Data structures, interfaces, event schemas
- API endpoints and their contracts
- Edge cases and error states

**`design.md`** — Extract from spec:
- Technology choices and rationale
- Architecture decisions (component structure, data flow)
- Integration points with other changes
- Flag any open decisions as `> ⚠ Decision needed:` callouts
- **If skill-mode is A or B:** add a `## Required Skills` section at the bottom listing skills relevant to this specific change:
  ```
  ## Required Skills
  Use these skills when implementing this change with /opsx:apply:
  - /react-best-practices — for all React components
  - /backend-patterns — for Express routes and middleware
  - /tdd-workflow — before writing any implementation code
  ```
  Only include skills from the approved set (all recommended for mode A, available-only for mode B). Only list skills relevant to what this specific change implements — not the full project skill set.
- **If skill-mode is C:** omit the Required Skills section entirely.

**`tasks.md`** — Derive from spec:
- Concrete, checkable implementation tasks
- Each task should be completable in one focused session
- Order: infrastructure → data layer → logic → UI → tests
- Format: `- [ ] Task description`
- **If skill-mode is A or B:** add inline skill hints on tasks where a skill adds clear value:
  ```
  - [ ] Implement FileTree component → /react-best-practices
  - [ ] Set up Express routes → /backend-patterns
  - [ ] Write unit tests → /tdd-workflow
  ```
  Do not add hints on every task — only where the skill makes a meaningful difference. Use only skills from the approved set (all for mode A, available-only for mode B).
- **If skill-mode is C:** write plain tasks with no skill annotations.

---

## Step 4: Summary

After all changes are created, output:

```
✓ spec2opsx complete

Created: X changes
  1. <name> — proposal ✓  specs ✓  design ✓  tasks ✓
  2. <name> — ...

Next step: /opsx:apply <change-name> to start implementation
Recommended order: [list in dependency order]
```

---

## Step 5: Consistency Audit

After all changes are created, spawn a single `architect` subagent (read-only — no edits) to audit all artifacts against the original spec.

The agent checks three dimensions:

1. **Internal consistency per change** — `proposal.md` ↔ `specs/` ↔ `design.md` ↔ `tasks.md` agree on interfaces, filenames, event names, and numeric thresholds
2. **Cross-change consistency** — shared types defined in one change are referenced correctly by all consumers; file paths and module names are stable; inter-module contracts (BroadcastChannel events, function signatures, etc.) match on both sides
3. **Spec conformance** — every acceptance criterion appears in at least one change's `tasks.md`; all RISKs are addressed; no thresholds have drifted (debounce durations, clamp ranges, frame-rate constants, etc.)

Report findings as `CRITICAL` / `WARN` / `MINOR` with: change name, artifact file, line reference, and issue description.

**In `--fast` mode**: run audit unconditionally — correctness always matters.

**Output format:**
```
── Consistency Audit ──
CRITICAL  foundation/specs/broadcast-channel/spec.md  Missing heartbeat:pong in Prompter→Studio catalogue
WARN      take-recording/tasks.md  Version snapshot ownership unclear — Studio or Prompter?
MINOR     image-library/design.md  Resize described as "50%" but spec says 2048px longest side
...
X CRITICAL · Y WARN · Z MINOR
```

If zero findings: `✓ No issues found — all artifacts consistent.`

---

## Step 6: Cascade Fix

Fix all CRITICAL and WARN findings from Step 5, enforcing the spec→design→tasks cascade for every change touched.

**For each CRITICAL or WARN finding:**
1. Fix the **spec file** first (source of truth) — use `/opsx:continue` to apply the edit (or `/opsx:ff` in `--fast` mode)
2. If the fix changes an architecture decision or integration point → use `/opsx:continue` to update **design.md** for that change in the same pass
3. If the fix changes an implementation step or adds/removes work → use `/opsx:continue` to update **tasks.md** for that change in the same pass
4. All three updates are one atomic edit — never fix a spec and leave design/tasks stale

**MINOR findings:** apply via `/opsx:continue` only when trivially safe (terminology, formatting); skip if ambiguous.

After all fixes, re-run the Step 5 audit to verify no CRITICAL/WARN findings remain. If new issues surface, iterate (max 2 additional rounds; if issues persist after 2 rounds, surface to user).

**Append to the Step 4 summary block:**
```
Audit:    6 CRITICAL · 24 WARN · 22 MINOR found
Fixed:    all CRITICAL and WARN; 4 MINOR skipped (ambiguous)
Re-audit: ✓ 0 CRITICAL · 0 WARN · 4 MINOR remaining
```

---

## Rules

- **Spec→design→tasks cascade (CRITICAL):** When a spec file changes, its parent change's `design.md` and `tasks.md` MUST be reviewed and updated in the same edit pass. Fixing a spec without cascading into design/tasks leaves stale artifacts. This applies both in Step 6 automated fixes and in any manual edits during Step 3.
- Never put the entire spec document into a single change — always split
- In fast mode, still read the spec fully before creating anything
- Do not modify the user's global OpenSpec profile
- The multi-repo check (Step 0b) must happen before `openspec init`, not after

### Recovery from mid-flow interruption

If the skill run is interrupted after Step 2 but before all changes are created, the `openspec/` directory will be in a partially initialized state. To resume:

**Option A — continue manually:**
1. Run `/opsx:new <next-change-name>` for each remaining change
2. Follow Step 3b artifact sequence per change

**Option B — restart cleanly:**
1. Delete the `openspec/` directory
2. Re-run `/spec2opsx <spec-path>` from the beginning

If you want to skip already-created changes, note the last completed change name and tell the model: `"Changes 1–N are done, continue from change N+1."` The model will skip Step 0d (init already present) and jump to Step 1 analysis, then propose only the remaining changes.
