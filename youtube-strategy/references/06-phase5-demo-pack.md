# Phase 5: Demo Pack

> Optional phase. Only run when the video contains a live demo (tool walkthrough, Claude Artifact, MCP demo, etc.).
> Produces two files: `demo-setup.md` (test data & connector setup) and `demo-pack.md` (shooting day production guide).

---

## Trigger Detection

After Phase 3, scan `telepro-script.md` for demo markers:
- `[IMG:DEMO_...]` placeholders
- Script lines containing: „ich zeige live", „ich öffne jetzt", „Demo:", „Claude generiert", „Live Artifact", „siehst du hier", „ich tippe jetzt"

If at least one marker is present, ask the user:

> **„Das Script enthält eine Live-Demo. Soll ich ein Demo-Pack erstellen? (Phase 5)"**

On YES: generate both files below. On NO: skip Phase 5.

---

## Output 1: `demo-setup.md`

**Purpose:** Step-by-step guide for preparing test data, accounts, and connectors BEFORE the shooting day.

**Format reference:** See `01-hubspot-test-setup.md` in the live-artifacts-video-package for tone and structure.

### Sections to generate

#### Header
```
# [Tool/Platform] Test-Setup für [Demo-Thema]
## [Beschreibung] · BUILT — KI für den Mittelstand

> **Zeitaufwand:** ~XX Min für vollständiges Setup
> **Wann machen:** 1 Tag vor dem Drehtag, damit du Pre-Take entspannt validieren kannst.
```

#### VORAUSSETZUNGEN
Table with columns: Item | Status (☐) | Wo besorgen

Include everything that must be in place BEFORE starting the setup:
- Accounts (free tiers preferred)
- App versions
- Connectors / OAuth tokens
- Existing assets the user already has

#### SCHRITT-FÜR-SCHRITT SETUP (numbered steps)

For each system the demo touches:
- Concrete click paths (Settings → X → Y)
- Exact test data to create (names, amounts, dates, statuses)
- Screenshots or UI hints where helpful
- „Wichtig:"-callouts for non-obvious steps

Use realistic, domain-appropriate test data. Match the channel's niche (Mittelstand, German manufacturing, developer tools, etc.). Numbers should be plausible — not round, not huge.

#### CONNECTOREN AKTIVIEREN
Which connectors to enable in which app, with which permission scopes. Prefer read-only scopes for demo safety.

#### PRE-TAKE VALIDIERUNG
Checklist table: Check | Erwartetes Ergebnis | Status (☐)

Cover every visible element of the demo output. Include:
- Data shows correct values (expected total, count, etc.)
- All connectors stay authenticated
- Generation time target (< X Sek. ideal, < Y Sek. akzeptabel)
- Refresh / live-update behavior

#### TROUBLESHOOTING
Table: Problem | Ursache | Fix

Cover the 4-6 most likely failures:
- Auth / reauth issues
- Missing data / indexing delay
- Wrong language in output
- Performance issues

#### GO/NO-GO-ENTSCHEIDUNG
- ✅ GO: Minimum green checks required (e.g., 6 of 8) + key behaviors working
- ⚠️ NO-GO: What triggers Plan B + what Plan B looks like (simplified demo, pre-recorded backup, fewer sources)

#### ESTIMATED TOTAL EFFORT
Table of each setup step with time estimate. Running total at the bottom.

---

## Output 2: `demo-pack.md`

**Purpose:** Shooting day production guide — exact prompts, click choreography, B-roll cues, fallbacks, timing.

**Format reference:** See `03-demo-pack.md` in the live-artifacts-video-package.

### Sections to generate

#### Header
```
# Demo-Pack — [Demo-Thema]
## BUILT — KI für den Mittelstand · Video Slot: X:XX – X:XX · Modus: Hybrid

> **Hybrid-Definition:** Pre-Take ohne Aufnahme, validiert. Aufnahme-Take mit identischem Prompt.
```

#### VORAB-CHECK
Brief reference to `demo-setup.md` + minimum pass threshold before starting the shooting day.

#### DREHTAG-REIHENFOLGE
Numbered checklist:
1. Setup-Check (X Min) — connector status, test data, fresh chat
2. Pre-Take Phase 1 (X Min) — run through demo, validate output
3. Pre-Take Phase 2 if multi-phase (X Min)
4. Pause + mental Setup (10 Min)
5. AUFNAHME Phase 1
6. AUFNAHME Phase 2 (if applicable)

Explain WHY the order matters (e.g., Phase 2 depends on Phase 1 output, re-take impact).

#### DEMO-PHASE N: [Name] — one section per demo phase in the video

For each phase, include all of the following:

**Script slot:** Reference the time code from `telepro-script.md` (e.g., Skript-Slot 3:30 – 4:30)

**EXAKTER PROMPT (Wort für Wort)**
The exact prompt the presenter will type or paste. Must be:
- Derived from the script section describing the demo
- Complete and copy-paste ready
- Annotated with WHY each element is in the prompt

**ERWARTETE OUTPUT-STRUKTUR**
ASCII diagram of what the output should look like. Use box-drawing characters. Include realistic placeholder values matching the test data.

**KLICK-CHOREOGRAFIE**
Timestamped second-by-second guide:
```
Sek 0–10:  [Action] + [What to say from script]
Sek 10–15: [Action]
...
```

**B-ROLL-CUES** (während Claude generiert)
Table: Cue | Visuell | Sprechtext aus Skript

**FALLBACK-PLÄNE**
Table: Was schiefgeht | Was du machst

Cover the 5-8 most likely failures. Every fallback should have a recoverable path — either continue on camera or explain how to edit around it in post.

**TIMING-BUDGET**
```
Pre-Take Validierung:  X Min
Aufnahme-Take:        ~XX Sek
Re-Take falls nötig:  X× geplant
Total für Phase X:    ~XX Min im Drehplan
```

#### ARCHITEKTUR-VISUALS (for any `[IMG:...]` placeholders in the script that show system diagrams)

For each visual placeholder found in `telepro-script.md`:
- ASCII sketch of the diagram
- Brand colors table (hex codes, which element uses which color)

Use BUILT brand palette:
- Midnight: `#0A1628` (background)
- Electric Coral: `#FF4E50` (highlight border)
- Pulse Blue: `#3B82F6` (data connections)
- Signal Cyan: `#06B6D4` (connectors, arrows)
- Text: `#E5E5E7`

#### ZUSAMMENFASSUNG — Demo-Stats
Table: Phase | Was | Zeit (Skript) | Zeit (Aufnahme) | Risiko

---

## Output 3: `test-data/` Directory (ALWAYS)

**Purpose:** Ready-to-use files the presenter can copy directly into their demo environment — no manual typing, no guessing file formats.

**Model:** See `/Users/a7wwiri/Projects/vs/live-artifacts-video-package/test-data/` for reference structure and tone.

### What to generate

Create a `<topic-slug>/test-data/` directory containing:

#### Source/config files (copy directly into demo project)
All files the demo project needs — Python scripts, config templates, YAML skeletons — ready to paste. Use `DEMO_PLATZHALTER` style values for anything sensitive (never realistic-looking credential strings).

#### Import/data files (where applicable)
For demos that connect to external services (HubSpot, Google Sheets, databases): provide ready-to-import CSVs or Excel templates with realistic test data matching the script's domain. Use the HubSpot CSV format (`hubspot-companies-import.csv`, `hubspot-deals-import.csv`) as a reference for structure and tone.

#### `demo-projekt-anleitung.md`
Step-by-step guide (modeled after `hubspot-import-anleitung.md`) that walks through:
1. Creating the demo environment
2. Copying each file from test-data into the right location
3. What to fill in for placeholder values (format reference, not real values)
4. Validation checklist (table: Check | Erwartung | Status ☐)
5. Cleanup instructions (what to delete/restore after recording)

#### Format rules
- German prose throughout
- Validation checkboxes in every section (`☐`)
- "Wichtig:"-callouts for non-obvious steps
- "Nach der Aufnahme — Aufräumen" section always present
- BUILT footer line on every file

---

## Execution Instructions

1. Parse `telepro-script.md` to extract:
   - All `[IMG:DEMO_...]` and `[IMG:...]` markers → used for visuals and prompt extraction
   - All demo sections (based on heading + content)
   - Exact timing codes `[TIME:x:xx]` → used for script slot references
   - All system/tool names mentioned → used to define what test data is needed

2. Derive test data from the script's context:
   - What systems does the demo connect to?
   - What data must be visible in the demo output (names, amounts, stages, dates)?
   - What is the expected output structure?

3. Generate `demo-setup.md` first (data setup must exist before the pack makes sense)

4. Generate `demo-pack.md` using the exact prompt from the script and the expected output from the test data

5. Save both files to `<topic-slug>/demo-setup.md` and `<topic-slug>/demo-pack.md`

6. Generate `test-data/` directory with all demo files:
   - Source/config files for the demo project
   - Import/data files for external services (if applicable)
   - `demo-projekt-anleitung.md` (step-by-step copy guide)

---

## Quality Checklist

Before delivering Phase 5 output:
- [ ] Exact prompts are copy-paste ready (no ellipsis, no placeholders)
- [ ] Test data in `demo-setup.md` matches the expected output in `demo-pack.md`
- [ ] Every `[IMG:DEMO_...]` in the script has a corresponding ASCII diagram
- [ ] All timing slots align with `[TIME:x:xx]` markers in the script
- [ ] At least one fallback plan for each failure mode
- [ ] GO/NO-GO threshold is concrete (e.g., "6 of 8 checks green"), not vague
- [ ] `test-data/` directory exists with all demo files
- [ ] `test-data/demo-projekt-anleitung.md` includes validation checklist and cleanup section
- [ ] No realistic-looking credential strings in any test-data file (use `DEMO_PLATZHALTER` format)
