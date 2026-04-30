# <PROJECT_NAME> — End-to-End Specification v<VERSION>
## Complete Functional Description of All UI Elements (ELEMENT 1–<N>)
### BUILT — KI für den Mittelstand

---

## ARCHITECTURE OVERVIEW

```
┌──────────────────────────────────────────────────────────────┐
│  <COMPONENT_LAYER_1>                                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                    │
│  │ <COMP_A> │  │ <COMP_B> │  │ <COMP_C> │                    │
│  └──────────┘  └──────────┘  └──────────┘                    │
└──────────────────────────┬───────────────────────────────────┘
                           │ <COMMUNICATION_CHANNEL>
┌──────────────────────────▼───────────────────────────────────┐
│  <COMPONENT_LAYER_2>                                         │
└──────────────────────────────────────────────────────────────┘
```

### Technology Decisions

| Layer | Technology | Rationale |
|---|---|---|
| Distribution | <CHOICE> | <ONE_LINE_REASON> |
| Frontend | <CHOICE> | <ONE_LINE_REASON> |
| Persistence | <CHOICE> | <ONE_LINE_REASON> |
| <ADD_AS_NEEDED> | | |

### Ports / URLs / Distribution

```
<MODE_1>: <URL_OR_PATH>
<MODE_2>: <URL_OR_PATH>
```

---

## FILE STRUCTURE

```
<project-codename>/
├── src/
│   ├── <FILE>                  # <one-line-purpose>
│   └── <FILE>
├── tests/
└── package.json
```

---

## DESIGN TOKENS

```css
:root {
  /* Brand Colors (BUILT v2.6) */
  --color-midnight:        #0A1628;
  --color-electric-coral:  #FF4E50;
  --color-pulse-blue:      #3B82F6;
  --color-signal-cyan:     #06B6D4;
  
  /* Theme */
  /* Typography */
  /* Spacing */
  /* Animation */
}
```

---

## APP STATE / SESSION STATE

```typescript
interface <Subtype1> {
  <field>: <type>;
}

interface <AppState> {
  <field>: <type>;
}

export const initialState: <AppState> = {
  // ...
};
```

---

## EVENTS LIST

### <Direction> → <Direction> Events

| Event | Payload | When |
|-------|---------|------|
| `<event:name>` | `<payload-shape>` | <trigger> |

---

## ELEMENT 1: <NAME>

### What the User Sees

```
┌──────────────────────────────────────────────┐
│  <ASCII MOCKUP HERE>                         │
└──────────────────────────────────────────────┘
```

### End-to-End Function

**1. <Behavior Name>**
- Trigger: <when>
- Effect: <what changes>
- Persistence: <where saved>

```typescript
// <real code, not pseudo>
```

### Component File

`src/<path>`

---

## ELEMENT 2: <NAME>

<repeat structure>

---

## MARKUP SYNTAX REFERENCE (if applicable)

| Marker | Syntax | Render | Behavior |
|--------|--------|--------|----------|
| <name> | `<syntax>` | <visualization> | <behavior> |

---

## IMPLEMENTATION RISKS

### RISK-1: <Name> (HIGH | MEDIUM | LOW)

**Problem:** <concrete description>

**Mitigation:** <specific approach>

**Test Strategy:** <how to verify>

### RISK-2: <Name> (HIGH | MEDIUM | LOW)

<repeat>

---

## ACCEPTANCE CRITERIA

### <Group 1>
- [ ] AC-1: <objectively verifiable criterion>
- [ ] AC-2: <objectively verifiable criterion>

### <Group 2>
- [ ] AC-N: <objectively verifiable criterion>

---

## OUT OF SCOPE (V2+)

- ❌ <Feature> — <reason>
- ❌ <Feature> — <reason>

---

## IMPLEMENTATION ROADMAP

### Phase 1 — <Name> (Day 1)
1. <task>
2. <task>

### Phase 2 — <Name> (Day 2)
N. <task>

<continue numbering across phases>

---

## DECISIONS — ALL RESOLVED

| # | Question | Decision |
|---|----------|----------|
| 1 | <question> | **<decision>** |

---

## NAMING & BRANDING

**App Name:** <name>
**Codename:** `<codename>`
**Tagline:** <tagline>
**Target Output:** <file>

**Brand Colors:**
- Midnight `#0A1628`
- Electric Coral `#FF4E50`
- Pulse Blue `#3B82F6`
- Signal Cyan `#06B6D4`

**Fonts:**
- UI: <font>
- Code/Editor: <font>

---

**End of Specification v<VERSION>**
