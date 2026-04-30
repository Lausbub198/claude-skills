# Greenfield Process — Building a Spec from Dialogue

This is Mode A: the user has an idea, no document yet. Your job is to lead them through structured dialogue and produce the final spec at the end.

## Phase 0: Capture Vision (before any features)

Before listing any features or asking about implementation, establish the foundation. If the user's initial message doesn't contain answers to all three questions below, ask them with a single-select question (use `ask_user_input_v0` in Claude.ai, `AskUserQuestion` in Claude Code, or plain Markdown if neither is available).

### The three foundation questions

1. **Problem & User** — "What use case should be at the center?" with 3-4 options scoped to the project
2. **Format** — "What format / distribution?" (single HTML file, npm package, web app with backend, mobile app, etc.)
3. **Persona / Decision-Maker** — Who is the primary user the spec is being designed for?

Example for a YouTube video planning project:
- Q1: "Which use case is at the center?" → Internal Tooling / Customer Prototyping / AI Apps / All three
- Q2: "What video format?" → 8-Min Demo / 20-Min Deep-Dive / Strategic Explainer
- Q3: "Which C-level persona?" → Managing Director / CTO / Department Head

### What you do with the answers

Use the answers to constrain everything that follows:
- Vision section in the final spec
- Choice of architecture (e.g. Single-File HTML if user picks "runs offline on MacBook")
- Tone of the spec (CTO-targeted = more architecture; Managing Director-targeted = more business value)

**Don't proceed to features until you can write a 2-sentence summary of vision that the user would agree with.**

## Phase 1: Identify the Operating Context

Before features, lock down the technical context. These are constraints, not features.

Examples of operating context:
- **Platform:** macOS / Linux / Windows / Cross-platform / Mobile
- **Runtime:** Browser / Node.js / Python / Native
- **Distribution:** Single-file / npm / Docker / App Store
- **Hardware:** Specific display sizes (e.g. 1024×600 Elgato), specific input devices (e.g. Stream Deck)
- **Integration points:** Camera, audio, third-party APIs, file system

Ask only the ones that aren't already implied by the vision. If user said "runs on my MacBook offline as an HTML file" you don't need to ask about distribution.

## Phase 2: Thematic Block Iteration

This is the core of the skill. Group features into 4-6 thematic blocks. For each block:

### Step 1: Multi-select with 5-7 options

Present a numbered multi-select list to the user (use `ask_user_input_v0` in Claude.ai, `AskUserQuestion` in Claude Code, or plain Markdown if neither is available):

```
question: "Which [block-theme] features would you actually use?"
options:
  - Feature A: short explanation (e.g. 'XYZ does ABC')
  - Feature B: short explanation
  ...
```

### Step 2: Read the answer, give a reasoned recommendation

Don't just confirm. Pattern:
- If they picked something you'd skip: "I didn't include X in your list — you only need that if Y. Are you sure?"
- If they didn't pick something obvious: "Did you intentionally leave out Z? In your context (8-min solo shoot) that's usually essential."
- If two features overlap: trigger conflict resolution (Step 3)

### Step 3: Resolve conflicts when features overlap

Example conflict: User picked both "Trigger Words" and "Emphasis Markers" — both visually highlight words. Force differentiation:

```
"Both features highlight words visually. So they don't get in each other's way,
here is my proposed clear differentiation:

| Marker | Syntax | Visual | Purpose |
|--------|--------|--------|---------|
| Emphasis | **Word** | Bold + Pulse Blue | Spoken emphasis |
| Trigger | !!Word!! | Bold + Coral + Glow | Content-critical |

Are you OK with that?"
```

### Step 4: Detect architectural escalations

Some answers fundamentally change the architecture. When you spot one, STOP the block iteration and resolve the architecture question first.

Examples of escalation triggers:
- "I want two windows" → BroadcastChannel sync, master/slave model
- "It should be reachable from outside" → Server component, API
- "Multiple people simultaneously" → Multi-user state, conflict resolution
- "Should also run offline" → Service Worker, local-first architecture
- "I need a database" → Persistence layer decision

Pattern:
```
"You chose [Feature X]. That's significant — it structurally changes the architecture.

[Architecture diagram in ASCII]

Three options for how this can be implemented technically:
[options]

What do you think?"
```

Don't continue with feature blocks until the architecture is resolved.

### Step 5: Block-Closing recap

End each block with:
- ✅ Confirmed features
- ❌ Rejected features (with reasoning)
- ⚠️ Open architectural questions if any

This builds incremental clarity.

## Phase 3: Cross-Block Cleanup

After all blocks done, before writing the spec:

1. **Hotkey collisions** — review all hotkeys mentioned across blocks. Check for collisions with macOS/Windows defaults. Propose `Option+F[N]` for Stream Deck users.
2. **Naming consistency** — does every component have a name? Are names consistent (e.g. all `*Service` or all `*Manager`)?
3. **Data model gaps** — for every feature with state, is there a TypeScript interface implied?
4. **Implementation risks** — review the feature set, name 4-7 RISK-N items.

## Phase 4: Generate the Spec

Open `assets/spec-template.md`, fill in based on the conversation. Read `references/spec-structure.md` for what each section needs.

**Critical:** Don't be lazy in code snippets. If the spec mentions a `parseScript()` function, write it out in TypeScript. If it mentions an `<input type="range">` slider, give the actual HTML/CSS.

The spec is the deliverable. The implementer will read it once and start building. Every fuzzy spot in the spec becomes a question they have to come back to ask.

## Phase 5: Deliver

1. Save to the project's working directory as `<project-name>-e2e-spec-v<version>.md` (ask the user if the target path is unclear)
2. `wc -l` and section count
3. `present_files`
4. Closing summary:
   - "X lines, N sections"
   - "ELEMENT 1 through ELEMENT N covered"
   - "Implementation Risks: RISK-1 [Name], RISK-2 [Name], ..."
   - "Out of Scope: [list]"
   - "Recommended next steps: [concrete]"

## Common pitfalls in Greenfield Mode

- **Asking too many questions before starting** — ship after vision + 4-5 blocks, not 20
- **Letting the user dictate everything** — your job is to push back on bad picks
- **Not naming risks** — the spec feels rosy, implementer hits walls
- **Stopping at "concept level"** — generic ASCII, no real code, no real interfaces
