# Example Blocks — Good vs Bad

This file contains worked examples of thematic blocks from real spec dialogues. Use them as patterns when running your own iteration with the user.

## What makes a good block

- **3-7 options** (not 2, not 15)
- **One sentence per option** explaining what it does
- **Concrete examples** in the option text, not abstract descriptions
- **Mutual exclusivity** clear (or explicitly multi-select)
- **Recommendation** delivered after the user picks

## What makes a bad block

- Too many options (decision fatigue)
- Options that overlap heavily (user can't tell them apart)
- Abstract descriptions ("better UX")
- No reasoning after the pick (just "great, moving on")

---

## Example 1: GOOD — Live-Performance Block (from Telepro session)

### The question

```
multi_select: "Which live recording features would be game-changers for you?"
options:
- Take Marker: Press 'T' during recording to set a marker (exportable later with timestamp for DaVinci editing)
- Auto-Pause on long silence: If you hesitate for 3+ seconds, scroll pauses automatically
- Breath Indicator: At '---' marks, an icon briefly flashes (1 sec)
- Pre-Roll Countdown: Before scroll starts, a 3-2-1 countdown runs
- Silence Pause Marker: In the script, use '[PAUSE:3]' to insert a 3-second pause
```

### Why it's good
- Each option explains the user benefit, not just the feature name
- Concrete mechanic in each option ("Hotkey 'T'", "3+ seconds", "[PAUSE:3]")
- Multi-select makes it clear user can pick multiple

### Recommendation after pick

After user said "I don't understand" instead of picking:

```
"Fair point. The features sound abstract — let me show you
for each one **exactly when it helps during your recording**.
With concrete scenarios from your 8-min demo script.

[detailed explanation of each feature with concrete scenarios from the user's actual project]

**Concrete recommendation for your setup:**
- ✅ Pre-Roll Countdown
- ✅ Breath Indicator
- ✅ Silence Pause Marker
- ❓ Take Marker (only if you edit yourself)
- ❌ Auto-Pause"
```

### Why the recommendation is good
- Acknowledges the user's hesitation without dismissing it
- Uses the user's own project as illustration
- Makes a clear recommendation with reasoning per item
- Adapts based on conditional ("only if you edit yourself")

---

## Example 2: BAD — Too Abstract

### The question (don't do this)

```
multi_select: "Which features do you need?"
options:
- Storage features
- UX improvements
- Performance optimizations
- Advanced features
- Future-oriented
```

### Why it's bad
- Options are categories, not features
- No way for the user to make an informed pick
- Recommendations would be impossible

### Better version

```
multi_select: "Which editing features would you actually use?"
options:
- Word counter + estimated speaking duration live in the editor (e.g. '847 words / 5:38 min')
- Section overview in sidebar with click-to-jump (outline view)
- Markdown templates: Predefined script structures (8-min demo, 20-min deep-dive) to load
- Script versions: Auto-snapshot before each prompter run, rollback possible later
- Multi-script library: Save multiple scripts in parallel + switch between them
```

### Why this is better
- Each option describes exact behavior with concrete numbers/examples
- User can imagine using each one
- Recommendations can be specific

---

## Example 3: GOOD — Architectural Escalation Detection

### The trigger

User said: "I'd also like to have kind of two windows — one is the editor view and the other one I want to display as full view in the teleprompter"

### What the assistant did

```
"Understood. Four features selected + one **structurally important
new point** I need to sharpen before I continue.

## The Multi-Window Requirement — this is significant

What you're describing is actually a **dual-window setup**:

[ASCII diagram of dual-window architecture]

**This is a professional standard:** The presenter sees the prompter,
the operator sits at the editor window and can make live corrections.

**Technically, this means:** The mode-switch approach is replaced.
Instead of 'Edit → Prompter' you have **two permanently open windows
that synchronize with each other**.

This isn't trivial — but it's elegantly solvable. I need two
clarifying questions before I can specify it correctly:"
```

Then asked architecture questions before continuing with feature blocks.

### Why this is good
- Recognized the structural impact ("this is significant")
- Stopped the feature flow ("before I continue")
- Explained what the user was actually asking for in technical terms
- Set up the architecture decisions that needed to happen first

### When to escalate

Listen for these signals:
- "It should also be able to X" (X = network, multi-user, persistence layer)
- "On another device / in the browser / mobile"
- "Multiple at the same time"
- "Over the internet"
- "In the background / as a service"

Each of these usually changes the architecture, not just adds a feature.

---

## Example 4: GOOD — Conflict Resolution

### The setup

User picked both `Trigger Words (highlighted in red)` and `Emphasis Marker (**Word**)`. Both visually highlight words.

### What the assistant did

```
"Block 3 noted. Four markers selected. One quick clarification,
because two of them are visually similar and I want to make sure
the spec is clean.

## Conflict Check: Emphasis vs. Trigger Words

Both features highlight words visually. To keep them from
interfering, here's my proposal for a clear differentiation:

| Marker | Syntax | Visual | Purpose |
|--------|--------|--------|---------|
| Emphasis | **Word** | Bold + Pulse Blue #3B82F6 | Spoken emphasis |
| Trigger Word | !!Word!! | Bold + Coral #FF4E50 + Glow | Content-critical |

Example from your script:
[concrete example combining both markers]

In the prompter:
- 'Shadow IT' → blue, bold (spoken emphasis)
- 'three levels' → coral, bold, glow (you **must not skip this**)

Two different colors = two different mental triggers."
```

### Why this is good
- Spotted the conflict before producing the spec
- Proposed a concrete differentiation
- Used the user's actual content to illustrate
- Made the choice obvious (two purposes, two colors)

---

## Example 5: GOOD — Block Closing Recap

### After Block 1 of Telepro

```
"## Block 1 is final — Current state

What's confirmed so far (Block 1 + Architecture):

- ✅ **Word Counter + Speaking Duration** live in the editor
- ✅ **Outline Sidebar** with click-to-jump
- ✅ **Multi-Script Library** (multiple scripts in parallel)
- ✅ **Script Versions** (auto-snapshot before each prompter run)
- ✅ **Dual Window** (Studio + Prompter, BroadcastChannel)
- ✅ **Hotkeys in Prompter only** + Stream Deck-optimized F-keys

---

## Block 2 – Live Performance: your selection is still pending

As a reminder — this was the multi-select from the previous round:
[reminder of options]"
```

### Why this is good
- Builds incremental clarity (user knows where they are)
- Visible progress markers (✅)
- Reminds user of pending blocks
- Forms a natural checkpoint before moving on

---

## Patterns for difficult moments

### When the user says "I don't understand"

→ Don't repeat the same options louder. Switch to **concrete scenarios from their actual project**. Use their content (script text, project name, target audience) to illustrate each feature.

### When the user picks something contradictory

→ Resolve via **conflict-check section** with table differentiating the items.

### When the user picks something inferior

→ Push back **once** with reasoning. If they confirm, accept it.
Example: "Take Marker is only useful if YOU edit. You're recording to SD card — are you sure you want that feature?" If they say yes, include it.

### When the user opens a new architecture concern mid-block

→ **Stop the block**, address the architecture, then resume.

### When the user gets impatient

→ Move to **batch mode**. Group remaining blocks into one big multi-select with recommendations pre-marked, and ship.

```
"Let's combine Block 4 and Block 5 into one selection. My recommendation is marked next to each."
```
