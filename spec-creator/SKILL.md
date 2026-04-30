---
name: spec-creator
description: Creates publication-grade end-to-end software specifications in BUILT-Spec-Standard format used at BUILT — KI für den Mittelstand. Use whenever the user wants to (a) build a new technical spec from scratch through guided dialogue, or (b) upgrade an existing draft/concept doc to publication-grade. Trigger on phrases like "Spec erstellen", "Spezifikation schreiben", "Konzept aufbereiten", "Spec auf nächstes Level heben", "publikationsreife Spec", "BUILT-Spec-Standard", "Ende-zu-Ende-Spec", or any structured technical doc that will be handed to Claude Code for implementation. Also trigger when the user references DevStage or Telepro as a format reference. Produces specs with TypeScript interfaces, ASCII architecture diagrams, complete data models, ELEMENT-by-ELEMENT functional descriptions, event tables, implementation risks (RISK-N), acceptance criteria, and phased roadmaps — the level a senior engineer writes before a multi-day implementation sprint.
---

# BUILT Spec Creator

A skill for creating publication-grade technical specifications in the BUILT format used at "BUILT — KI für den Mittelstand". This skill captures a proven workflow that turns vague product ideas or rough concept drafts into specifications detailed enough that implementation becomes deterministic.

## When to use this skill

**Use this skill when:**
- The user wants to create a new spec from scratch ("Ich brauche eine Spec für X")
- The user has a rough concept/draft and wants to upgrade it to publication-grade ("Heb diese Spec auf das nächste Level")
- The user wants to hand a specification to Claude Code, an implementer, or publish it externally
- The conversation involves software design that requires structured documentation

**Don't use this skill when:**
- The user just wants a quick brainstorm or list of ideas
- The user is asking architectural questions without intent to document
- The artifact will be a marketing one-pager or pitch deck

## The two operating modes

This skill operates in one of two modes. Detect which mode at the start.

### Mode A: Greenfield (build from scratch via dialogue)

User has an idea, no document yet. Goal: lead them through a structured dialogue that captures all decisions, then produce the final spec.

→ Read `references/greenfield-process.md`

### Mode B: Upgrade (lift existing draft to publication-grade)

User has a draft/concept document. Goal: identify what's missing relative to BUILT-Spec-Standard and add it.

→ Read `references/upgrade-process.md`

## Core principles (apply in both modes)

These principles distinguish a BUILT-Spec from a generic technical writeup.

### 1. Vision-first, then mechanics

Never start with implementation details. Always begin by establishing:
- **What problem does this solve?** (in 1-3 sentences)
- **Who is the user?** (specific persona, not "users")
- **What does success look like?** (concrete deliverable, format, distribution)

If these aren't crystal clear after the user's initial message, ASK before drafting anything. Present options as a numbered or multi-select list where the answer is one of a small set.

### 2. Structured iteration via thematic blocks

Don't ask 30 questions at once. Don't ask one question at a time either. Group related decisions into 4-6 thematic blocks. For each block:

1. List 3-7 candidate features as multi-select options
2. After receiving the selection, give a **fact-based recommendation** with reasoning ("Skip X because it requires Y which is V2-territory")
3. Resolve any **conflicts** that the selection creates (two overlapping features → force differentiation)
4. Identify **architectural escalations** (does this new feature change the system architecture? Stop and clarify)

Example block structure:
- Block 1: Editor & Workflow
- Block 2: Live Performance
- Block 3: Markup & Visual Cues
- Block 4: Data Management
- Block 5: Polish & QoL

### 3. Recommend with reasoning, never just list

When the user picks features, don't just confirm. Push back where appropriate:
- "Auto-Pause on silence: Skip — needs voice sync (V2 territory)"
- "Take Marker: Only useful if YOU do the editing"
- "Notes Marker: Would clutter your script, not recommended"

The user's selection is input. Your job is to ensure the final spec is coherent, not just to transcribe what they said.

### 4. Make abstract features concrete with scenarios

When a user doesn't understand a feature, illustrate with their actual content:
- ❌ "Silence-pause markers insert pauses"
- ✅ "In the script you write `[PAUSE:2]`. Concretely for your CTA: 'If you feel like shadow IT is emerging...' [PAUSE:1] '...talk to me.' That 1 second makes the difference between a normal close and a CTA with punch."

### 5. Detect architectural escalations and stop

Some user responses fundamentally change the system. Examples:
- "I want two windows" → no longer single-page app, now BroadcastChannel + master/slave
- "It should be reachable from outside" → no longer client-only, needs API
- "Multiple users simultaneously" → no longer local, needs server + sync

When you detect this: **stop the feature iteration**, name the escalation, propose architectural options, get user's pick BEFORE continuing.

### 6. Mark implementation risks explicitly

Some parts of the implementation are mathematically tricky, browser-quirky, or full of edge cases. Identify these and document them as named RISK-N items with:
- The problem statement
- Mitigation approach
- Test strategy

The implementer (Claude Code or human) needs to know which parts deserve special care.

### 7. Anchor mitigations IN THE CODE, not just the risks section

A named RISK with a bullet-point mitigation is not enough. The mitigation must show up in the actual code/ELEMENT section, so an implementer reading only that section builds the safe version.

Wrong:
- ELEMENT says "watcher on .next/"
- RISK says "actually watch only on BUILD_ID"
→ Implementer follows ELEMENT, builds buggy code, never reads RISK.

Right:
- ELEMENT code shows `chokidar.watch([join(path, '.next/BUILD_ID'), ...])` directly
- RISK section points to ELEMENT for verification

When upgrading existing drafts: if the draft has code that contradicts your mitigation, **rewrite the code** — don't just add a risk note. Bullet-points cannot override code in the same document.

See `references/upgrade-process.md` Phase 5b for the verification loop to run before declaring an upgrade complete.

## The BUILT Spec Format (target output)

Every spec produced by this skill must contain these sections, in this order. Section depth is described in `references/spec-structure.md`.

```
1. Title block + version
2. ARCHITECTURE OVERVIEW (ASCII diagram + tech decisions table + ports/URLs)
3. FILE STRUCTURE (file tree)
4. DESIGN TOKENS (CSS variables for colors/spacing/typography)
5. APP STATE / SESSION STATE (TypeScript interfaces, complete)
6. EVENTS LIST (BroadcastChannel/WebSocket/REST as applicable)
7. ELEMENT 1..N (per UI element):
   - What the user sees (ASCII mockup)
   - End-to-end function (numbered, with code snippets)
   - Component file (path)
8. MARKUP SYNTAX REFERENCE (if the app has custom syntax)
9. IMPLEMENTATION RISKS (RISK-1 through RISK-N)
10. ACCEPTANCE CRITERIA (checkbox list, grouped)
11. OUT OF SCOPE (V2+ items)
12. IMPLEMENTATION ROADMAP (phased, daily granularity)
13. DECISIONS (decision log table)
14. NAMING & BRANDING
```

For the full template with examples, read `references/spec-structure.md`.

## Style conventions

- **Language:** English for headings and prose, TypeScript/code in English
- **Voice:** Direct, short sentences, no nominalization, no passive
- **Formatting:** Markdown with tables, code blocks, and diagrams. Use Mermaid or ASCII box-drawing characters for architecture and flow diagrams — ASCII is more portable, Mermaid is easier to write. For UI element mockups (showing actual interface layout), always use ASCII — Mermaid cannot represent interfaces.
- **Code snippets:** Real TypeScript, not pseudocode. Functions named with file paths.
- **Diagrams:** Use box-drawing characters (`┌─┐│└┘`) for ASCII art. When using Mermaid, prefer `graph TD` for architecture and `sequenceDiagram` for event flows.
- **Brand colors when relevant:**
  - Midnight `#0A1628`
  - Electric Coral `#FF4E50`
  - Pulse Blue `#3B82F6`
  - Signal Cyan `#06B6D4`

## Workflow checklist

Use this as a TODO list when running the skill end-to-end:

```
GREENFIELD MODE:
[ ] Capture vision (problem, user, success)
[ ] Identify the operating context (file format, platform, distribution)
[ ] Run thematic blocks with multi-selects + recommendations
[ ] Detect & handle architectural escalations
[ ] Resolve conflicts between selected features
[ ] Identify implementation risks
[ ] Produce the spec in BUILT format
[ ] Show user file size + section count for sanity check

UPGRADE MODE:
[ ] Read existing draft completely (Phase 0)
[ ] Compare against BUILT-Spec-Format checklist — what SECTIONS are missing? (Phase 1)
[ ] Run code-level audit using code-audit-catalog.md — what CODE is defective? (Phase 1b)
[ ] Show user gap analysis WITH code-level findings
[ ] Get permission to upgrade (or specific section/finding choices)
[ ] Produce upgraded spec — fix code findings AND add missing sections
[ ] **VERIFY: For each RISK-N, confirm mitigation shows in actual code section, not just risks list**
[ ] Show diff summary (sections added + findings fixed)
```

## Output handling

After producing the spec:

1. Save to the project's working directory as `<project-name>-e2e-spec-v<version>.md` (or ask the user for a preferred path if unclear)
2. Run `wc -l` and `grep -c "^## "` to report metrics (lines, sections)
3. Use `present_files` to make it downloadable if available; otherwise, tell the user the file path so they can open it directly
4. End with a short summary listing:
   - What's in it (sections covered)
   - Implementation Risks (the named RISK items)
   - What's NOT in it (out-of-scope confirmation)
   - Concrete next steps ("Hand to Claude Code with `/plan`", or "Iterate further on X")

## Reference files

- `references/greenfield-process.md` — Step-by-step for Mode A (build from dialogue)
- `references/upgrade-process.md` — Step-by-step for Mode B (lift existing draft)
- `references/code-audit-catalog.md` — **Critical for Mode B:** seven checks for finding defects in existing code, with defect/correct patterns
- `references/spec-structure.md` — Detailed template for each spec section
- `references/example-blocks.md` — Worked examples of thematic blocks (good and bad)
- `references/risk-catalog.md` — Common implementation risks and how to document them
- `assets/spec-template.md` — Empty BUILT-Spec template (skeleton with placeholders)

Read the relevant reference file when you reach that part of the workflow. Don't load all of them upfront — they're long.

**For Mode B specifically:** Always load both `upgrade-process.md` AND `code-audit-catalog.md`. The catalog is what enables Phase 1b (code-level findings) to actually work.

## Failure modes to avoid

These are mistakes that downgrade a spec from publication-grade to "just another doc":

1. **Skipping the vision phase** — leads to features without context
2. **Asking everything in one giant question** — overwhelming, sloppy answers
3. **Just transcribing user picks** — no reasoning, no conflict resolution
4. **Generic ASCII placeholders** — `[Diagram]` or `[Mockup]` instead of actual drawings
5. **Pseudo-code instead of real TypeScript** — implementer can't use it directly
6. **Missing data models** — interfaces left out, "we'll figure it out later"
7. **No implementation risks named** — implementer hits them blind
8. **No acceptance criteria** — no way to verify "done"
9. **Roadmap with vague phases** — "Phase 1: Setup" instead of concrete tasks
10. **Wrong diagram type** — using Mermaid for UI element mockups where ASCII is required (Mermaid cannot represent interface layouts)
11. **Mode B: only checking if SECTIONS exist, not if CODE is correct** — leads to specs that pass structural review but ship broken patterns. Always run Phase 1b code audit.
12. **Mode B: writing mitigations only as bullet points in RISKs section** — the code in the ELEMENT sections still shows the broken version, implementers follow the code. Always anchor mitigations IN the code.

If you catch yourself doing any of these, restart that section.
