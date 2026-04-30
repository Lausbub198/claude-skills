# spec-creator

A Claude Code skill that turns a vague product idea or rough concept draft into a publication-grade end-to-end software specification — detailed enough that implementation becomes deterministic.

---

## What it does

Invoke `/spec-creator` and the skill runs in one of two modes:

**Mode A — Greenfield:** You have an idea, no document yet. The skill leads you through a structured dialogue (4–6 thematic blocks, multi-select options, recommendation after each pick) and produces a complete spec at the end.

**Mode B — Upgrade:** You have a draft or concept doc. The skill does a gap analysis against the spec standard (structural sections + code-level defect audit), shows you what's missing, and upgrades it to publication-grade.

Either way, the output is a spec a senior engineer would hand to a dev team before a multi-day sprint:

- ASCII / Mermaid architecture diagram + tech decisions table
- Complete TypeScript interfaces for all app state
- ELEMENT-by-ELEMENT functional descriptions with ASCII UI mockups
- Event tables (BroadcastChannel / WebSocket / REST)
- Named implementation risks (RISK-N) with problem / mitigation / test strategy
- Acceptance criteria (objectively verifiable, grouped)
- Phased roadmap with daily granularity
- Decision log

---

## Installation

Copy the skill directory into your Claude Code skills folder:

```bash
cp -r spec-creator ~/.claude/skills/
```

Or symlink so repo edits are reflected immediately:

```bash
ln -s /path/to/claude-skills/spec-creator ~/.claude/skills/spec-creator
```

Claude Code picks it up automatically on the next session.

---

## Usage

```
/spec-creator
```

The skill detects which mode applies from context. If you already have a draft open or referenced, it goes into Upgrade mode. Otherwise it starts Greenfield mode with the vision questions.

You can also be explicit:

```
/spec-creator upgrade path/to/draft.md
/spec-creator new  →  force Greenfield mode
```

---

## How it works

### Mode A — Greenfield

1. **Vision phase** — Three foundation questions: what problem, who's the user, what does success look like. Nothing gets written until this is clear.
2. **Thematic blocks** — 4–6 blocks of 5–7 feature options each (multi-select). After each pick: reasoned recommendation, conflict resolution if needed, architectural escalation detection.
3. **Cross-block cleanup** — Hotkey collisions, naming consistency, data model gaps, implementation risks (4–7 RISK-N items).
4. **Spec generation** — Full spec in standard format, saved to the project working directory.

### Mode B — Upgrade

1. **Read the draft completely** — no skimming.
2. **Gap analysis** — structural (missing sections) + code-level audit (7 defect checks: async lifecycle races, file-system watch noise, WebSocket reconnect strategy, React rendering, stream backpressure, schema versioning, hotkey/focus handling).
3. **User confirmation** — full upgrade / selective / structure-only.
4. **Upgrade + verification** — for every named RISK, the mitigation is anchored in the actual code/ELEMENT section, not just described in the risks list.

### Key principle: risk mitigations live in the code

The spec is publication-grade only when mitigations appear in the ELEMENT code snippets — not just as bullet points in the risks section. An implementer reading only the ELEMENT section should build the safe version by default.

---

## Reference files

The skill loads reference files on demand (not all upfront):

| File | Used when |
|------|-----------|
| `references/greenfield-process.md` | Mode A — step-by-step dialogue process |
| `references/upgrade-process.md` | Mode B — gap analysis + upgrade workflow |
| `references/code-audit-catalog.md` | Mode B — 7 code-level defect checks with defect/correct patterns |
| `references/spec-structure.md` | Both — detailed template for each spec section |
| `references/example-blocks.md` | Both — worked examples of good/bad thematic blocks |
| `references/risk-catalog.md` | Both — common implementation risk patterns |
| `assets/spec-template.md` | Both — empty spec skeleton with placeholders |

---

## Spec format overview

```
1.  Title block + version
2.  ARCHITECTURE OVERVIEW (diagram + tech decisions + ports/URLs)
3.  FILE STRUCTURE (file tree)
4.  DESIGN TOKENS (CSS variables)
5.  APP STATE / SESSION STATE (TypeScript interfaces)
6.  EVENTS LIST (BroadcastChannel / WebSocket / REST)
7.  ELEMENT 1..N (per UI element):
      - What the user sees (ASCII mockup)
      - End-to-end function (numbered, with code snippets)
      - Component file (path)
8.  MARKUP SYNTAX REFERENCE (if custom syntax)
9.  IMPLEMENTATION RISKS (RISK-1 through RISK-N)
10. ACCEPTANCE CRITERIA (checkbox list, grouped)
11. OUT OF SCOPE (V2+ items)
12. IMPLEMENTATION ROADMAP (phased, daily granularity)
13. DECISIONS (decision log table)
14. NAMING & BRANDING
```

Architecture diagrams: ASCII box-drawing characters or Mermaid (`graph TD`, `sequenceDiagram`).
UI element mockups: ASCII only — Mermaid cannot represent interface layouts.

---

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI

No external tools or packages required.

---

## License

MIT
