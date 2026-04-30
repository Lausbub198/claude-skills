# BUILT Spec Structure — Detailed Template

This document specifies what each section of a BUILT-Spec needs to contain. Use it as a checklist and reference when writing the final spec.

## Section 1: Title Block

```markdown
# <ProjectName> — End-to-End Specification v<X.Y>
## Complete Functional Description of All UI Elements (ELEMENT 1–<N>)
### BUILT — KI für den Mittelstand

---
```

- Project name: short, code-friendly (e.g. "Teleprompter Pro", "DevStage")
- Version: semantic (1.0, 1.1, 2.0). Increment major on breaking changes.
- Subtitle states what's covered (number of ELEMENTs)
- Branding line: always "BUILT — KI für den Mittelstand" for Andy's projects

## Section 2: ARCHITECTURE OVERVIEW

Three subsections required:

### 2a: ASCII Architecture Diagram

Use box-drawing characters. Show major components, data flows, and persistence layers. Example structure:

```
┌─────────────────────────────────────────────────────────────────┐
│  STUDIO WINDOW  (MacBook — telepro.html?mode=studio)            │
│  ┌──────────┐ ┌──────────────┐ ┌────────────┐ ┌──────────────┐  │
│  │ Editor   │ │ SettingsPanel│ │ Outline    │ │ ImageLibrary │  │
│  └──────────┘ └──────────────┘ └────────────┘ └──────────────┘  │
│                  STATE MASTER (in-memory + IndexedDB)           │
└──────────────────────────┬──────────────────────────────────────┘
                           │ BroadcastChannel("telepro-sync")
┌──────────────────────────▼──────────────────────────────────────┐
│  PROMPTER WINDOW (Elgato — telepro.html?mode=prompter)          │
│  STATELESS RENDERER                                             │
└─────────────────────────────────────────────────────────────────┘
```

The diagram should answer: "What are the major components, what runs where, and how do they talk to each other?"

Alternatively, Mermaid (`graph TD` or `sequenceDiagram`) is acceptable for architecture and flow diagrams. For UI element mockups (Section 7a), ASCII is required.

### 2b: Technology Decisions Table

Markdown table with columns: Layer | Technology | Rationale. Every choice gets a one-line justification.

```markdown
| Layer | Technology | Rationale |
|---|---|---|
| Distribution | Single-File HTML | Double-click opens browser, runs offline |
| Frontend Framework | Vanilla JS (no React) | Minimal footprint, no build pipeline |
| Persistence | IndexedDB | Quota-aware, transactional, async |
```

**Anti-pattern:** "We'll use React because it's modern" → not a justification.

### 2c: Ports/URLs/Distribution

If there are network ports, URL routes, or distribution targets, list them concretely:

```
Studio Mode:   telepro.html?mode=studio
Prompter Mode: telepro.html?mode=prompter
Hotkey-Test:   telepro.html?mode=hotkey-test
```

## Section 3: FILE STRUCTURE

A complete file tree of the project. Even if it's a single-file artifact, show how the source is organized during development.

```
projectname/
├── src/
│   ├── index.html
│   ├── styles/
│   ├── shared/
│   ├── studio/         # one folder per major component group
│   ├── prompter/
│   └── exporters/
├── tests/
├── build.js
└── package.json
```

Every file/folder gets a 1-line comment if its purpose isn't obvious.

## Section 4: DESIGN TOKENS

CSS custom properties for the entire app. Group by purpose:

```css
:root {
  /* Brand Colors */
  --color-midnight:        #0A1628;
  --color-electric-coral:  #FF4E50;
  
  /* Theme */
  --bg-studio-dark:        #0F0F11;
  --text-studio:           #E5E5E7;
  
  /* Typography */
  --font-ui:               'Inter', system-ui, sans-serif;
  --font-mono:             'JetBrains Mono', Consolas, monospace;
  
  /* Spacing */
  --spacing-xs:            4px;
  --spacing-sm:            8px;
  
  /* Animation */
  --duration-fast:         150ms;
}
```

## Section 5: APP STATE / SESSION STATE

The single most important section. This defines the shape of all data the app holds.

Requirements:
- Use TypeScript syntax (interfaces, not just JSDoc)
- Every field typed (no `any`)
- Comments where types alone don't explain ("// Unix timestamp", "// 0-100 %, default 50")
- An `initialState` constant with concrete defaults

Example:

```typescript
interface Settings {
  display: {
    font: 'Arial' | 'Helvetica' | 'Georgia' | 'Inter';
    fontSize: number;            // 12-80 pt, default 28
    horizontalMargin: number;    // 0-90 %, default 20
  };
  scrolling: {
    speed: number;               // 10-200 %, default 50
    autoLoop: boolean;
  };
}

interface AppState {
  settings: Settings;
  scripts: Record<string, Script>;
  isPlaying: boolean;
  // ... live state (not persisted)
}

export const initialState: AppState = {
  settings: defaultSettings,
  scripts: {},
  isPlaying: false,
};
```

## Section 6: EVENTS LIST

If the system uses any kind of messaging (BroadcastChannel, WebSocket, REST), list all events with payload schema and timing.

Format: tables grouped by direction (Server→Client, Client→Server) or by type.

```markdown
### Studio → Prompter Events

| Event | Payload | When |
|-------|---------|------|
| `state:full` | complete `AppState` | On Prompter start |
| `command:start-take` | `{ scriptId, version }` | User clicks Start |
```

If race conditions are possible, document the resolution strategy (versioning, timestamps, etc.) with code snippets.

## Section 7: ELEMENT N — Functional Descriptions

This is the longest section. One subsection per major UI element. Number them `ELEMENT 1`, `ELEMENT 2`, etc.

Per element, three required parts:

### 7a: What the User Sees

ASCII mockup showing the actual UI. Use box characters. Annotate where helpful with arrows and labels.

```
┌──────────────────────────┐
│ ▼ Display                │
│ Font   [Arial         ▾] │
│ Size   [════●════] 28pt  │  ← slider with live value
│ HMargin [══●═════] 20%   │
└──────────────────────────┘
```

### 7b: End-to-End Function

Numbered list of behaviors. For each behavior, describe:
- What triggers it
- What state changes
- What UI updates
- What persists
- What broadcasts

Include real code snippets where the logic is non-obvious. Don't write pseudo-code.

```markdown
**1. Auto-Save (every 3s)**
- Debounced setInterval
- Writes scripts[activeScriptId] to IndexedDB
- Updates metadata
- Broadcast state:script-changed

```typescript
async function autoSave(): Promise<void> {
  const script = state.scripts[state.activeScriptId];
  script.content = editorElement.value;
  script.updatedAt = Date.now();
  script.metadata = parseMetadata(script.content);
  await idb.put('scripts', script);
  broadcast.send('state:script-changed', { id: script.id });
}
```
```

### 7c: Component File

The file path(s) where this element is implemented:

```
src/studio/Editor.ts
src/studio/LivePreview.ts
```

This forces you to think about code organization while writing the spec.

## Section 8: MARKUP SYNTAX REFERENCE (if applicable)

Only if the app has its own custom markup or syntax. Provide:
- Complete table of all markers with syntax, render, behavior
- Parser logic with real code (not pseudo)
- Example input → output

## Section 9: IMPLEMENTATION RISKS

Named RISK-N items. Each has:

```markdown
### RISK-N: <Name> (HIGH | MEDIUM | LOW)

**Problem:** Concrete description of what could go wrong.

**Mitigation:** Specific approach to avoid the problem.

**Test Strategy:** How to verify it actually works (with real data, not just unit tests).
```

Common categories:
- Timing/Sync (audio latency, frame budget, race conditions)
- Concurrency (multi-window, multi-user, multi-tab)
- Browser quirks (IndexedDB quota, autoplay restrictions, focus handling)
- Mathematical (layout calculations, easing curves, edge cases)
- Performance (large data sets, frame drops)

For each RISK that's HIGH or MEDIUM, add a forward-reference from the relevant ELEMENT section: "⚠️ Implementation Risk RISK-1 — see Implementation Risks section".

See `risk-catalog.md` for common risk patterns.

## Section 10: ACCEPTANCE CRITERIA

Checkbox list, grouped by feature area. Each criterion is:
- Numbered (AC-1, AC-2, ...)
- Objectively verifiable (no "should be good" or "feels right")
- Specific about how to verify ("with Browser DevTools Performance Profiler", "in DaVinci Marker-Import")

```markdown
### Core
- [ ] AC-1: Sample script parses correctly, all markers render right
- [ ] AC-2: Scroll runs at constant speed
- [ ] AC-3: Image-pause mechanic (RISK-1) works smoothly, no jump

### Performance
- [ ] AC-34: 60 FPS with a 5,000-word script (Browser DevTools Performance Profiler)
- [ ] AC-35: 10+ images, no frame drop
```

## Section 11: OUT OF SCOPE

What's deliberately not in this version. Use ❌ markers. State each as "X — was not included because Y" so it's clear:

```markdown
- ❌ Voice-Sync (requires Whisper integration, V2 territory)
- ❌ Cloud-Sync (ZIP-Export covers backup use case for V1)
- ❌ Mobile App (different platform, separate project)
```

## Section 12: IMPLEMENTATION ROADMAP

Phased plan with daily granularity. Each phase has:
- Phase name & day allocation
- Numbered tasks (continuous numbering across phases)
- Risk markers where applicable

```markdown
### Phase 4 — Prompter Core (Day 4) ⚠️ CRITICAL
17. ScrollEngine with `requestAnimationFrame`
18. Reading Position Marker
19. Mirror modes
20. Hotkey Listener
21. **Image-Pause Mechanic** (RISK-1) — with thorough testing
22. Slow/Fast-Mode with 500ms Fade
```

Total task count typically 30-50 for a 5-7 day project. Tasks should be checkable (one developer-day or less each).

## Section 13: DECISIONS

Decision log as table. Every architectural choice that wasn't obvious gets a row:

```markdown
| # | Question | Decision |
|---|----------|---------|
| 1 | Single-window or dual-window? | **Dual-Window** via BroadcastChannel |
| 2 | Studio = Master or Symmetric? | **Studio = Master** |
| 3 | Where are hotkeys processed? | **In the Prompter** (keyboard + Stream Deck) |
```

This is the audit trail. When implementer asks "why did you do X?", point to the decision log.

## Section 14: NAMING & BRANDING

Final section. Short. App name, codename, tagline, brand colors, fonts.

```markdown
**App Name:** Teleprompter Pro
**Codename:** `telepro`
**Tagline:** "Andy's Teleprompter. Built for BUILT."
**Target Output:** Single-File `telepro.html`

**Brand Colors:**
- Midnight `#0A1628`
- Electric Coral `#FF4E50`

**Fonts:**
- UI: Inter
- Editor: JetBrains Mono
```

## Anti-Patterns (do not do)

These lower the quality below publication-grade:

1. **Pseudocode where real code is possible** — `// do something with images` is not acceptable
2. **`[Diagram TBD]` placeholders** — if a diagram is needed, draw it in ASCII
3. **`any` types in TypeScript** — every field must be properly typed
4. **Vague acceptance criteria** — "AC: app should be fast" → no
5. **Missing edge cases** — what happens when user does X with empty state, conflicting state, edge values?
6. **One giant ELEMENT instead of 10 small ones** — break it up
7. **No code paths shown** — readers can't trace what happens when

## Quality Bar Check

Before delivering, the spec passes if:
- [ ] Implementer can start coding without asking architecture questions
- [ ] Every TypeScript interface is complete
- [ ] Every UI element has an ASCII mockup
- [ ] Every feature has a code path or numbered E2E description
- [ ] Risks are named with mitigation + test strategy
- [ ] Acceptance criteria are objectively verifiable
- [ ] Roadmap has daily-level tasks
- [ ] Decision log captures every non-obvious choice
