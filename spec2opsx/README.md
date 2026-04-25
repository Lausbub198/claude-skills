# spec2opsx

A Claude Code skill that converts a specification document into a set of [OpenSpec](https://github.com/Fission-AI/OpenSpec) (opsx) changes — each with a full artifact set and immediately testable end-to-end.

---

## What it does

You write (or already have) a product specification. You run `/spec2opsx your-spec.md`. The skill:

1. **Initializes OpenSpec** in your project if it isn't already set up
2. **Detects the tech stack** mentioned in the spec and recommends relevant Claude Code skills
3. **Slices the spec into vertical changes** — each one bundles backend + frontend so the feature is runnable and testable immediately after implementation
4. **Creates all four OpenSpec artifacts** per change: `proposal.md`, `specs/`, `design.md`, `tasks.md`
5. **Embeds skill references** in the artifacts so `/opsx:apply` automatically uses best-practice skills during implementation (optional, your choice)

---

## Prerequisites

| Requirement | Notes |
|-------------|-------|
| [Claude Code](https://docs.anthropic.com/en/docs/claude-code) | The CLI where this skill runs |
| [OpenSpec CLI](https://github.com/Fission-AI/OpenSpec) | `npm install -g openspec` |
| OpenSpec expanded profile | Enables `/opsx:new`, `/opsx:ff`, `/opsx:continue` — run `openspec config profile` to activate |

---

## Installation

Copy the skill file into your Claude Code skills directory:

```bash
cp spec2opsx.md ~/.claude/skills/spec2opsx.md
```

That's it. Claude Code picks it up automatically on the next session.

---

## Usage

```bash
/spec2opsx path/to/your-spec.md
```

### Flags

| Flag | Description |
|------|-------------|
| `--fast` | Skip the breakdown confirmation step and create all artifacts without pausing between them |
| `--tools <list>` | AI tools to configure during `openspec init` — skips the interactive prompt |

**Examples:**

```bash
# Interactive mode — review and approve each step
/spec2opsx docs/feature-spec.md

# Fast mode — create everything without pausing
/spec2opsx docs/feature-spec.md --fast

# Pre-configure tools for a specific IDE
/spec2opsx docs/feature-spec.md --tools cursor
/spec2opsx docs/feature-spec.md --tools claude,cursor --fast
```

**Supported `--tools` values:** `amazon-q`, `bob`, `claude`, `cline`, `codex`, `cursor`, `factory`, `gemini`, `github-copilot`, `windsurf`, `roocode`, `trae`, and others. Use `all` or `none` as shortcuts.

---

## How it works

### Step 0 — Project init

The skill checks whether OpenSpec is already initialized in your project. If not, it runs `openspec init --tools <value>` non-interactively. Your global OpenSpec profile is never touched.

### Step 0b — Tech stack detection and skill recommendations

The skill scans the spec for technology signals (Node.js, React, TypeScript, PostgreSQL, etc.) and maps them to Claude Code skills that encode best practices for those technologies.

It checks which skills you have installed and presents a list:

```
Detected tech stack: Node.js, React, TypeScript, WebSocket, PostgreSQL

Recommended skills:
  ✓ backend-patterns      — available
  ✓ react-best-practices  — available
  ⚠ frontend-patterns     — not installed  → https://github.com/anthropics/claude-code-skills
  ⚠ coding-standards      — not installed  → https://github.com/anthropics/claude-code-skills
  ✓ tdd-workflow          — available
```

Then it asks how you want skill references handled in the generated artifacts:

```
Embed skill references in generated artifacts (design.md / tasks.md)?
  [A] Yes, all recommended skills (including not-yet-installed)
  [B] Yes, available skills only
  [C] Skip — no skill references in artifacts
```

Choosing **A** or **B** means `design.md` gets a `## Required Skills` section and `tasks.md` gets inline hints like `→ /react-best-practices` on relevant tasks. When you later run `/opsx:apply`, Claude picks up these references automatically. Choosing **C** generates clean artifacts with no skill annotations.

### Step 1 — Vertical slice analysis

The spec is split into **vertical slices** — not layers. Each change bundles the backend logic, API endpoint(s), and frontend UI for one feature so it's runnable end-to-end immediately after implementation.

**The rule:** one change = one "I can demo this right now" moment.

The first change is always a thin **foundation** (server + connection + frontend shell) — just enough to get a blank screen running. Everything else is feature slices in dependency order.

### Step 2 — Breakdown proposal (interactive mode)

Before creating anything, the skill presents its proposed breakdown:

```
Proposed breakdown: 6 changes

1. foundation
   What: Express server, WebSocket setup, blank React shell, design tokens
   Why separate: required skeleton for all subsequent slices

2. file-tracking
   What: File watcher backend + FileTree widget
   Why separate: independent feature, immediately testable (save a file, see it appear)
...

Proceed? (or describe adjustments)
```

You can adjust names, merge changes, or reorder before anything is created. In `--fast` mode this step is skipped.

### Step 3 — Artifact creation

For each change, the skill creates:

| Artifact | Contents |
|----------|----------|
| `proposal.md` | Problem, scope, success criteria |
| `specs/` | Functional requirements, data structures, API contracts, edge cases |
| `design.md` | Tech choices, architecture decisions, open questions flagged with `⚠ Decision needed:` |
| `tasks.md` | Checkable tasks ordered infrastructure → data → logic → UI → tests |

**Interactive mode** pauses after each artifact so you can review it. The pause after `design.md` is intentional — that's the cheapest moment to change tech choices or architecture before tasks are generated.

**Fast mode** (`--fast`) creates all four artifacts per change without pausing.

### Step 4 — Summary

```
✓ spec2opsx complete

Created: 6 changes
  1. foundation         — proposal ✓  specs ✓  design ✓  tasks ✓
  2. file-tracking      — proposal ✓  specs ✓  design ✓  tasks ✓
  ...

Next step: /opsx:apply foundation to start implementation
Recommended order: foundation → file-tracking → git-tracking → ...
```

---

## Workflow overview

```
your-spec.md
     │
     ▼
/spec2opsx ──► openspec init (if needed)
     │
     ▼
 tech stack detection + skill recommendations
     │
     ▼
 breakdown proposal (interactive) or auto-proceed (--fast)
     │
     ▼
 for each change:
   /opsx:new → proposal → specs → design → tasks
     │
     ▼
 /opsx:apply <change-name>   ← implement one change at a time
```

---

## Interactive vs fast mode

| | Interactive | Fast (`--fast`) |
|-|-------------|-----------------|
| Breakdown proposal | shown, waits for approval | shown briefly, auto-proceeds |
| Artifact creation | pauses after each artifact | all 4 created in one step |
| Architecture checkpoint | yes — explicit pause at `design.md` | no |
| Best for | first pass on a new spec, or when you want to influence design | already familiar with the spec, want artifacts quickly |

---

## Skill references in artifacts

When you choose mode **A** or **B**, the generated `design.md` includes a section like:

```markdown
## Required Skills
Use these skills when implementing this change with /opsx:apply:
- /react-best-practices — for all React components
- /backend-patterns — for Express routes and middleware
- /tdd-workflow — before writing any implementation code
```

And `tasks.md` includes inline hints:

```markdown
- [ ] Implement FileTree component → /react-best-practices
- [ ] Set up Express routes → /backend-patterns
- [ ] Write unit tests → /tdd-workflow
```

These hints are added only where a skill makes a meaningful difference — not on every task.

Skills are sourced from the [everything-claude-code](https://github.com/anthropics/claude-code-skills) collection. Installation is typically: copy the skill directory into `~/.claude/skills/`.

---

## Example output structure

After running `/spec2opsx docs/dashboard-spec.md` on a real-time dashboard spec:

```
openspec/
└── changes/
    ├── foundation/
    │   ├── proposal.md
    │   ├── specs/
    │   ├── design.md
    │   └── tasks.md
    ├── file-tracking/
    │   ├── proposal.md
    │   ├── specs/
    │   ├── design.md
    │   └── tasks.md
    ├── git-tracking/
    ├── code-preview/
    ├── act-management/
    └── live-stats/
```

---

## License

MIT
