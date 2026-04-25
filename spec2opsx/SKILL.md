---
name: spec2opsx
description: Converts a spec document into OpenSpec (opsx) changes. Splits the document into logical units, initializes opsx if needed, and creates all artifacts (proposal, specs, design, tasks) per change. Supports --fast and --tools flags.
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

## Step 0: Project Init Check

Check whether OpenSpec is already initialized in the current project:

```bash
ls openspec/ 2>/dev/null || echo "NOT_INITIALIZED"
```

**If already initialized:** confirm `✓ OpenSpec already present` and skip to Step 1.

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

---

## Step 0b: Detect Tech Stack and Recommend Skills

Before analyzing the breakdown, scan the spec for technologies. For each technology detected, identify Claude Code skills that encode best practices for that tech. Present these to the user so they can install missing ones and decide whether to embed skill references in the generated artifacts.

### 1 — Detect technologies and map to skills

Scan the spec text for technology signals and map them to Claude Code skills. The list below covers common cases — apply judgment for technologies not listed.

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

Skill sources for installation:
- **everything-claude-code** collection: `https://github.com/anthropics/claude-code-skills` — covers most common stacks
- Individual skill READMEs include installation instructions (typically: copy the skill directory into `~/.claude/skills/`)

### 2 — Check availability and present to user

Claude can see which skills are currently available in its runtime context. Cross-reference the recommended skills against what is actually loaded.

Present the result like this:

```
Detected tech stack: Node.js, React, TypeScript, WebSocket, PostgreSQL

Recommended skills:
  ✓ backend-patterns      — available
  ✓ react-best-practices  — available
  ⚠ frontend-patterns     — not installed  → https://github.com/anthropics/claude-code-skills
  ⚠ coding-standards      — not installed  → https://github.com/anthropics/claude-code-skills
  ✓ tdd-workflow          — available

Install missing skills to get best-practice guidance during implementation.
```

### 3 — Ask the user how to handle skills in artifacts

After presenting the list, ask:

```
Embed skill references in generated artifacts (design.md / tasks.md)?
  [A] Yes, all recommended skills (including not-yet-installed)
  [B] Yes, available skills only
  [C] Skip — no skill references in artifacts
```

Store the user's choice as **skill-mode** for use in Step 3:
- **A**: embed all recommended skills (available + not-yet-installed), so references are ready when the user installs them later
- **B**: embed only skills that are currently available
- **C**: omit all skill references from artifacts

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

In **`--fast` mode**: show a brief summary and proceed immediately without waiting.

---

## Step 3: Execute — Create Changes and Artifacts

For each change in order:

### 3a. Create the change scaffold

```
/opsx:new <change-name>
```

Change names must be kebab-case and under 40 characters.

### 3b. Create artifacts

**`--fast` mode:** Use `/opsx:ff` — creates all artifacts (proposal, specs, design, tasks) in one step.

**Normal mode:** Use `/opsx:continue` for each artifact, pausing for review between steps:
1. `/opsx:continue` → `proposal.md` — wait for user review
2. `/opsx:continue` → `specs/` — wait for user review
3. `/opsx:continue` → `design.md` — **pause here and explicitly tell the user:** *"This is the right moment to adjust tech choices, architecture, or integration points before tasks are generated. Any changes now are cheap — once tasks are created you'd need to revise them too."* Then wait.
4. `/opsx:continue` → `tasks.md`

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

## Rules

- Never put the entire spec document into a single change — always split
- In fast mode, still read the spec fully before creating anything
- Do not modify the user's global OpenSpec profile
- If the spec covers multiple distinct services or repositories, ask the user which project root to use before running `openspec init`
