# Upgrade Process — Lifting an Existing Draft to Publication-Grade

This is Mode B: the user has a draft, concept doc, or earlier-version spec. Your job is to identify what's missing relative to BUILT-Spec-Standard and produce an upgraded version.

## Phase 0: Read the existing draft completely

Before anything else, use `view` to read the entire draft. Don't skim.

While reading, build a mental checklist:
- What's the current structure?
- What's missing relative to BUILT-Spec-Format?
- Are there places where the document says "we'll decide later" or hand-waves over details?

## Phase 1: Gap Analysis

Compare the draft against the BUILT-Spec-Format checklist. For each section, classify:

| Section | Status |
|---------|--------|
| Title & version | ✅ present / ⚠️ missing version / ❌ missing |
| Architecture Overview (ASCII/Mermaid) | ✅ / ❌ |
| Tech-Decisions table | ✅ / ❌ |
| File Structure tree | ✅ / ❌ |
| Design Tokens | ✅ / ❌ |
| App State (TypeScript interfaces) | ✅ / ⚠️ pseudo-code / ❌ |
| Events list | ✅ / ❌ |
| ELEMENT-by-ELEMENT descriptions | ✅ / ⚠️ partial / ❌ |
| - ASCII mockups | ✅ / ❌ |
| - Numbered E2E function | ✅ / ❌ |
| - Code snippets | ✅ / ❌ |
| Markup syntax reference (if applicable) | ✅ / ❌ |
| Implementation Risks | ✅ / ❌ |
| Acceptance Criteria | ✅ / ❌ |
| Out of Scope | ✅ / ❌ |
| Roadmap (phased) | ✅ / ❌ |
| Decision log | ✅ / ❌ |
| Naming & Branding | ✅ / ❌ |

## Phase 2: Show the user the gap analysis

Present the table to the user. Don't immediately start writing.

```
"I've compared your draft against the BUILT-Spec standard. Here are the gaps:

[gap table from Phase 1]
[code-level findings from Phase 1b]

Three options for how to proceed:

1. **Full Upgrade** — I'll fill all gaps, you'll get a publication-grade spec
2. **Selective** — you tell me which sections to add
3. **Structure only** — I keep the content, just map it to the standard structure

What works for you?"
```

Present options as a numbered list or multi-select (use `ask_user_input_v0` in Claude.ai, `AskUserQuestion` in Claude Code, or plain Markdown if neither is available).

## Phase 1b: Code-Level Audit (CRITICAL — don't skip)

> **The pitfall this phase prevents:** Phase 1 only checks "is the section present?" not "is the content correct?". A draft can have all sections checked ✅ and still ship code that's broken in production. Phase 1b finds the broken code.

This phase is mandatory whenever the draft contains code snippets, configuration, or implementation details. Skip only if the draft is purely conceptual (no code at all).

### Audit Pattern

Walk the draft a second time, this time looking for **defects**, not gaps. For each piece of code, configuration, or implementation detail, ask:

**"If an implementer copies this verbatim, will it work reliably in production?"**

If the answer is "no, it has a known failure mode", you've found a code-level finding.

### The seven audit checks

Run all seven explicitly. Don't trust your instinct — go through the list.

#### Check 1: Lifecycle race conditions

Look for: any code that starts an async resource (file watcher, database connection, network listener) and immediately uses it.

**Defect pattern:**
```typescript
const watcher = chokidar.watch(path, opts)
watcher.on('add', ...)
session.active = true  // ← Wrong: events between watch() and 'ready' are lost
```

**Correct pattern:**
```typescript
return new Promise((resolve) => {
  const watcher = chokidar.watch(path, opts)
  watcher.on('ready', () => { session.active = true; resolve(watcher) })
  watcher.on('add', ...)
})
```

If you see the defect pattern, flag it.

#### Check 2: File-system watch noise

Look for: chokidar/fs.watch on directories that contain frequently-touched files (`.next/`, `node_modules/`, `dist/`, `.git/`).

**Defect pattern:** `chokidar.watch(projectPath + '/.next/')` — triggers on every Hot-Reload write.

**Correct pattern:** Watch only specific files within the directory: `chokidar.watch([path + '/.next/BUILD_ID', path + '/.next/trace'])`.

#### Check 3: WebSocket / network reconnect strategy

Look for: WebSocket reconnect code with fixed delay (`setTimeout(reconnect, 3000)`) or no max-attempt cap.

**Defect pattern:** Fixed 3-second retry — under network instability creates retry storms. No cap = infinite reconnect attempts.

**Correct pattern:** Exponential backoff (1s → 2s → 4s → 8s, capped at 8s) with max 10 attempts before showing failure UI.

#### Check 4: React rendering performance

Look for: any component receiving frequently-updating props without `React.memo`, especially if it does SVG/Canvas rendering, has 5+ DOM children, or runs every N seconds.

**Defect pattern:**
```typescript
function VelocitySparkline({ velocity, latestDelta }) {
  return velocity.map(v => <line ... />)
}
```

**Correct pattern:**
```typescript
export const VelocitySparkline = memo(VelocitySparklineImpl, (prev, next) => {
  // Custom comparator
})
```

#### Check 5: Stream backpressure

Look for: `fs.WriteStream`, `Response.write`, or similar stream APIs without backpressure handling.

**Defect pattern:** `stream.write(data)` ignoring the boolean return value.

**Correct pattern:** `highWaterMark` set, `drain` event handled, `closeStream` returns Promise that awaits drain.

#### Check 6: Persistence schema versioning

Look for: any persistence layer (IndexedDB, NDJSON logs, JSON files, SQLite) that's read by another tool or future versions of itself.

**Defect pattern:** Records without `schemaVersion` field.

**Correct pattern:** First record (or every record) carries `schemaVersion`; reader validates and refuses on major-version mismatch.

#### Check 7: Hotkey / focus / preventDefault

Look for: `window.addEventListener('keydown', ...)` for system-level shortcuts (Cmd+digit, Cmd+S, etc.).

**Defect pattern:** Handler runs even when user is in input field, doesn't check `document.hasFocus()`, no `preventDefault()` for keys with browser defaults.

**Correct pattern:** Three guards before triggering action:
1. `document.hasFocus()` — app has system focus
2. `target.tagName !== 'INPUT' && !target.isContentEditable` — user not typing
3. `e.preventDefault()` — block browser defaults like Cmd+0 (zoom) or Cmd+1-9 (tabs)

### How to present findings

For each finding, write a small block:

```markdown
**FINDING-N: [Short Name]** (HIGH | MEDIUM | LOW)

📍 Location: ELEMENT X / Section Y, line ~N
🐞 Defect: [what's wrong with the current code]
💡 Fix: [what the correct version is]
🔗 Related: [if this maps to a known RISK pattern]
```

### Bundle findings into the gap analysis

When showing Phase 2 gap analysis to the user, present BOTH:

```markdown
## Structural Gaps (what's missing)
| Section | Status |
[table]

## Code-Level Findings (what's defective in the existing code)
- FINDING-1: ELEMENT 10 watches `.next/` globally → false positives on Hot-Reload
- FINDING-2: ELEMENT 9 uses fixed 3s retry → retry storm under load
- FINDING-3: ELEMENT 14 missing React.memo → re-renders on every state update
- FINDING-4: ELEMENT 15 writes session:start without schemaVersion → CutBot cannot validate
- ...
```

Each finding becomes a RISK-N + a code rewrite in the upgrade. The user can then decide:
- Full upgrade (fix all findings)
- Selective (only critical ones)
- Defer (keep the defect, add only RISK-N as warning)

### When findings overlap with missing RISKs

A finding from Phase 1b often becomes a RISK in Phase 4. The two-step relationship:

1. **Phase 1b finds:** "ELEMENT 10 watches `.next/` globally — buggy"
2. **Phase 4 risk:** RISK-4 Build-Watcher false positives
3. **Phase 5 fix:** Rewrite ELEMENT 10 code with specific file paths + debounce

This way, the upgraded spec is correct by construction (Check 7 in Phase 5b verifies this).

## Phase 3: Identify content gaps vs. format gaps

Two kinds of gaps:

### Format gaps
The information is there, just not in the right structure. Example: User has hotkey list as bullet points, BUILT-Format wants it as a table with both keyboard and Stream Deck columns.

→ You can fix these without asking the user.

### Content gaps
The information is missing. Example: No data model, no acceptance criteria, no implementation risks.

→ You need to either:
  - **Infer from context** — if user mentions "section hotkey 1-9", the spec needs a `currentSectionIndex: number` in state
  - **Ask the user** — for things that can't be inferred, like "what should happen if the user closes Studio while Prompter is recording?"

When you ask, batch related questions together. Don't ping-pong.

## Phase 4: Upgrade Section by Section

Work through the spec in order. For each section:

### If section is ✅ present and good
Keep as-is, maybe minor formatting cleanup.

### If section is ⚠️ partial
Augment what's there. Don't rewrite if the existing prose is fine — add code snippets, add the data model, add the missing edge cases.

### If section is ❌ missing
Write from scratch. Use the rest of the spec as input. If you can't infer it, batch a question to the user.

## Phase 5: Critical sections that almost always need work

These are the sections that drafts almost always under-deliver:

### 1. App State / Session State
Drafts often say "we'll have a state object" without specifying it. Write it as TypeScript with every field typed.

### 2. ELEMENT mockups
Drafts often skip the ASCII mockups. Add them. They take effort but force the writer to think through the actual UI.

### 3. Implementation Risks
Almost always missing. Look at the feature set, identify:
- Mathematically tricky bits (timing, sync, layout calculations)
- Browser-quirky bits (audio latency, IndexedDB quota, focus handling)
- Concurrency bits (race conditions, inter-window sync)
- Performance bits (large data sets, frame budgets)

Document each as RISK-N with problem / mitigation / test strategy.

### 4. Acceptance Criteria
Drafts often have vague success metrics. Convert to checkbox list, group by feature area, make each one objectively verifiable.

Bad: "Performance should be good"
Good: "AC-34: 60 FPS on 5,000-word script (Browser DevTools Performance Profiler)"

### 5. Roadmap
Drafts often have vague phases like "Phase 1: Setup, Phase 2: Core, Phase 3: Polish". Convert to daily granularity with concrete numbered tasks.

## Phase 5b: Anchor mitigations IN THE CODE — not just in RISKs section

> ⚠️ **Critical pitfall — read this before delivering an upgraded spec.**

When you add the IMPLEMENTATION RISKS section, it's tempting to write the mitigation as bullet points in the risk description and stop there. **This is not enough.** A spec is publication-grade only when the mitigations are **anchored in the actual code/ELEMENT sections**, not just described abstractly in the risks list.

### The two-level rule

For every named RISK, both must be true:

**Level 1 (RISKs section):** Risk is named, severity rated, mitigation strategy described, test strategy documented.

**Level 2 (ELEMENT/Code sections):** The actual code snippet, configuration, or implementation detail in the relevant ELEMENT section **shows the mitigation in action**. The implementer should be able to copy the code and have the risk already mitigated, without having to read the RISKs section to know what to do differently.

### Concrete examples

**Bad (RISKs-only):**
```markdown
### RISK-2: WebSocket Reconnect State Consistency

**Mitigation:** useWebSocket.ts with auto-reconnect (exponential backoff 1s → 8s).

### ELEMENT 9: AUTO-RECONNECT
- WebSocket onclose triggers
- Retry after 3 seconds
- ...
```

The ELEMENT 9 code says "3 seconds" — contradicts the mitigation. An implementer reading only ELEMENT 9 builds the buggy version.

**Good (anchored):**
```markdown
### RISK-2: WebSocket Reconnect State Consistency

**Mitigation in the spec:** See ELEMENT 9 — useWebSocket.ts with exponential backoff. Server sends state:full automatically on connection.

### ELEMENT 9: AUTO-RECONNECT
[...]
const delay = Math.min(BASE_DELAY * Math.pow(2, attemptRef.current), MAX_DELAY)
attemptRef.current += 1
[...]
```

The ELEMENT 9 code IS the mitigation. RISKs section only points to it.

### Verification step before delivery

Before declaring the upgrade complete, run this loop:

For each RISK-N:
1. Read the RISKs entry — what's the mitigation strategy?
2. Find the corresponding ELEMENT section (usually called out as "See ELEMENT X")
3. Open the code snippet in that ELEMENT
4. **Verify:** Does the code actually do what the mitigation says?
5. If no → the spec is inconsistent. Fix the code.

### Common patterns where this fails

| Risk Pattern | Mitigation Site (where the code lives) |
|--------------|----------------------------------------|
| Async lifecycle race conditions | The function that initializes the resource (e.g. `startWatcher` returning Promise) |
| Performance / re-render | The component file (React.memo wrapper, comparator) |
| File-system watch noise | The watcher setup (specific paths, debounce) |
| Persistence schema evolution | The persistence module (schema version constants) |
| Backpressure / streams | The stream creation (highWaterMark, drain handlers) |
| Hotkey / focus conflicts | The hook/listener (hasFocus, preventDefault, target checks) |

### When to refactor existing code instead of just adding RISKs

If the existing draft has code that contradicts a mitigation (e.g. "watch on `.next/`" but mitigation says "watch only on BUILD_ID"), you must **rewrite the existing code section**, not just add a risk note. Bullet-point mitigations cannot override code that's right there in the spec — implementers will use the code.

This is the difference between "spec that warns about pitfalls" and "spec that's correct by construction".

## Phase 6: Diff Summary

After producing the upgraded spec, show the user what changed:

```
"Spec v1.0 → v2.0 — What was added:

✅ Architecture diagram in ASCII/Mermaid (was missing)
✅ App State as complete TypeScript interfaces (was prose)
✅ ELEMENT 1-14 with mockups + E2E function descriptions
✅ 6 Implementation Risks documented (RISK-1 through RISK-6)
✅ 37 Acceptance Criteria, grouped
✅ 7-day roadmap with daily tasks
✅ Decision log with 17 decisions
✅ Code snippets in TypeScript (were pseudo-code)

Lines before: 938
Lines now: 2,205
Sections: 14 → 27"
```

## Common pitfalls in Upgrade Mode

- **Rewriting where not needed** — if the draft has good prose, don't replace it with template-prose
- **Inventing risks that don't exist** — only name real risks based on the actual feature set
- **Padding with boilerplate** — every line should add information, not fill space
- **Ignoring the user's voice** — match the tone of the original draft (formal vs. casual)
- **Adding sections the user doesn't need** — small projects don't need 50 acceptance criteria

## When the draft is too thin

If the draft is so vague that you'd basically be doing Greenfield mode, say so:

```
"Your draft is more of a concept stub. To bring it to publication-grade,
we'd need to work through it similarly to a new project — with structured
question blocks about features and architecture.

Should we switch to Greenfield mode and develop the spec from the draft
as a starting point? Or do you already have concrete answers to
[list of gaps] that I can write in directly?"
```
