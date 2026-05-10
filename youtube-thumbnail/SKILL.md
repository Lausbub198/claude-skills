---
name: youtube-thumbnail
description: >
  Generate YouTube thumbnails via Gemini Flash (Nano Banana 2) based on video scripts and the BUILT Brandbook (v4.0).
  Use this skill whenever the user mentions thumbnails, YouTube thumbnails, video covers, Vorschaubilder,
  or asks to create visuals for a YouTube video. Also trigger when the user uploads a video script and asks
  for visual assets. This skill REQUIRES a video script as input — it cannot run without one. The skill
  generates 4 background variations for the user to choose from. The creator (person cutout) is
  always set manually in the editor from real video footage. Every step requires user verification
  before proceeding.

  AUFRUF-MODI:
  A) STANDALONE — Wenn nur der /youtube-thumbnail Skill aufgerufen wird. Der User übergibt
     das fertige Video-Skript (Sprechtext / Teleprompter-Text). Startet bei Schritt 0
     (Emotional Concept Proposals) → User wählt Konzept → Schritt 1 bestätigt → Schritt 2+.
  B) ALS POST-PIPELINE-SCHRITT von /youtube-production — Thumbnail-Pipeline läuft automatisch
     nach dem Firebase-Upload des Skripts. Daten kommen aus a8_upload.thumbnail_briefing.
     In diesem Modus: Schritt 0 ZUSÄTZLICH ausführen (Sprechtext aus a3_script) und das
     bestehende Briefing als "Konzept D" präsentieren. User wählt aus allen 4 → Schritt 1 bestätigt.
---

# YouTube Thumbnail Generator — BUILT

Generate brand-consistent YouTube thumbnails for the BUILT channel ("BUILT — KI für den Mittelstand") using a **multi-layer compositing pipeline**.

### Entscheider-Design-Prinzip (BUILT v4.0)

Jedes Thumbnail muss den **Boardroom-Test** bestehen: Würde ein Geschäftsführer, Abteilungsleiter oder Selbstständiger dieses Bild in einer Präsentation zeigen können, ohne dass es unseriös wirkt? Die Zielgruppe sind Entscheider im Mittelstand — C-Level, Geschäftsführer, Kleinunternehmer. Hintergründe und Icon-Kompositionen müssen **Deloitte/McKinsey/Apple Keynote-Qualität** ausstrahlen, nicht Gaming-Ästhetik oder Clip-Art.

## Architecture: Multi-Layer Pipeline

Thumbnails are NOT generated as a single image. They are composed from **separate layers** generated independently:

```
Layer 1:  Background Scene    (Nano Banana 2 — thematic, no person, style-matched from background_styles)
Layer 2:  Headline Text       (rendered live in editor — sits BEHIND person)
Layer 3:  Person Cutout       (Video frame extraction → rembg → cutout, scaled 2x)
Layer 4a: Tool-Komposition    (Nano Banana 2 — premium 3D tool logos, 4 variations)
Layer 4b: 3D Charakter        (Nano Banana 2 — thematic mascot on gray bg → rembg, OPTIONAL)
Layer 4c: UI-Mockup           (Nano Banana 2 — laptop/phone with product UI on gray bg → rembg, OPTIONAL)
Layer 4d: Pfeil/Directional   (Nano Banana 2 — bold Beacon Yellow arrow on gray bg → rembg, OPTIONAL)
Layer 5:  Glow Effect         (dynamic radial gradient behind person's head)
```

**Why multi-layer?** Because it matches professional YouTube thumbnail quality (reference: @Mike-Mildenberger, @everlastai) where text goes behind the person's head, icons float with glow, and each element can be positioned independently.

## System Architecture

**Two systems work together:**

1. **Thumbnail Studio SPA (UI)** — Vite-based, served as static assets by the FastAPI review server.
   - Source: `/Users/a7wwiri/Projects/Video_Post_Production/thumbnail_studio/src/`
   - Build output: `/Users/a7wwiri/Projects/Video_Post_Production/backend/static/thumbnail_studio/`
   - Start: `python -m backend review` (from `Video_Post_Production/`), Port **8899**
   - Browser URL: **`http://localhost:8899/thumbnail-studio/`**
   - After changes to `thumbnail_studio/src/*`: `cd thumbnail_studio && npm run build:nocheck`

2. **Thumbnail Generator API-Backend** — Next.js, API routes only (`/api/generate-bg`, `/api/remove-bg`, `/api/project/files`, `/api/project/init`, `/api/video-frames`, `/api/image`, `/api/composite`, `/api/analyze`, `/api/share`, `/api/youtube/*`).
   - Source: `/Users/a7wwiri/Projects/Thumbnail_generator/`
   - Auto-started by review server as subprocess on port 3001 — no manual `npm run dev` needed.
   - FastAPI proxies `/api/*` → Next.js :3001 and `/output/*` → Next.js :3001.

**Editor components** (`thumbnail_studio/src/components/editor/`): AssetTabs, GlowControls, TextControls, PresetSelector, ProjectManager, ProjectMenuButton, VideoFramePicker, LayersPanel, BrandKitPanel, PreviewSizes, VariantSwitcher, YouTubeUpload, CTRScorePanel.

## Prerequisites

**MANDATORY**: A video script must be provided. If no script is present, ask for it immediately.

Before starting, read:
→ `references/brandbook-thumbnail-rules.md`
→ `references/gemini-thumbnail-config.json`

**API Keys** (in `/Users/a7wwiri/Projects/Thumbnail_generator/.env.local`):
- `GOOGLE_API_KEY` — Gemini Flash / Nano Banana 2 (backgrounds, tool compositions)

**Tools required**:
- `rembg` (system PATH — uses `birefnet-general` + alpha matting, runs server-side in Next.js API)
- Node.js with `sharp` and `@napi-rs/canvas` (in `Thumbnail_generator/`)
- Vite + React 19 (in `Video_Post_Production/thumbnail_studio/` — for SPA build only)

## Workflow (7 Steps)

### Step 0: Emotional Concept Proposals

**Input:** The finished video script — the actual spoken text (teleprompter, transcript, or
what was said on camera). Plain text only. No JSON required for this step.

**In AUFRUF-MODUS B (post youtube-production):** Extract spoken text from `a3_script[].teleprompter_text`
concatenated in order. Treat it as the video script.

#### Extract from the spoken text

Read the full script and derive:

| Field | How to find it |
|---|---|
| Video topic | What is the video primarily about? (first 2-3 sentences usually reveal this) |
| Core promise | What does the viewer gain from watching? (stated in hook/intro) |
| Key result / stat | Any specific number, timeframe, or measurable outcome ("100 Anfragen", "in 20 Minuten", "0 Euro") |
| Target audience | Who is addressed? (implied by language, problems discussed) |
| Tools mentioned | Any tool, software, or technology named |
| Video tone | Educational, story-driven, provocative, inspiring? |

#### Generate 3 Emotional Concept Proposals

For each trigger, derive all fields from the spoken script content:

| Trigger | Headline formula | Background style | Creator expression | Accent color |
|---|---|---|---|---|
| **Neugier** | Information gap / incomplete truth ("DAS VERSCHWEIGEN SIE DIR", "NIEMAND REDET DARÜBER") | `abstract_tech` — mysterious data streams, holographic panels | `curious_skeptical` — one raised eyebrow | Pulse Blue #4A9EFF |
| **Angst/FOMO** | Loss/threat statement ("DU VERLIERST GELD", "DEIN KONKURRENT WEISS DAS") | `dark_cinematic` — heavy shadows, tension | `focused_gaze` — serious, direct, sovereign (NOT panicked) | Electric Coral #FF6B4A |
| **Spezifisches Ergebnis** | Number + timeframe from script ("100K IN 28 TAGEN", "IN 20 MIN FERTIG") | `clean_minimal` or `dark_cinematic` | `slight_smile` — confident success | Beacon Yellow #FFD23F |

**Headline rules (always):**
- 2–4 words max, DEUTSCH, GROSSBUCHSTABEN
- **Emotional reaction or direct statement** — never a description of the video
- Short and punchy beats complete sentences: "WAHNSINN!" beats "DAS IST WIRKLICH WAHNSINN"
- **Good archetypes** (match these patterns):
  - Emotional reaction: "EINFACH WAHNSINN", "UNFASSBAR!", "NICHT ZU GLAUBEN"
  - Direct loss: "DU BLEIBST ZURÜCK", "NIE WIEDER MANUELL", "GERADE ABGEHÄNGT"
  - Information gap: "NIEMAND SAGT DIR DAS", "DAS VERSTECKEN ALLE", "KEINER ZEIGT DAS"
  - Outcome: "KI NIMMT AB", "0€ GEHALT", "NIE WIEDER", "IN 2 MIN FERTIG"
- **Bad (reject immediately):** descriptive phrases, tool names, event descriptions
  - Bad: "DAS BAUEN DIE ANDEREN", "JEDEN MONTAG VERLOREN", "LIVE ARTIFACTS ERKLÄRT"
- Scan the script for lines the creator says with genuine emotion — those are candidates
  (e.g. if creator says "Das ist doch einfach Wahnsinn" → headline = "EINFACH WAHNSINN")
- Never use technical tool names. The headline is an emotional trigger, not a description.

**Derivation rule for "Spezifisches Ergebnis":** Use the most concrete number or outcome
from the script. If no number exists, invent none — use the strongest emotional reaction
the outcome provokes instead (e.g. "EINFACH WAHNSINN" over "SEHR SCHNELL FERTIG").

#### Proposal output format

Present all 3 (or 4 in MODUS B) as a structured block:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KONZEPT A — NEUGIER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Headline:      "DAS VERSCHWEIGEN SIE DIR"
Click-Hook:    Viewer fragt sich: wer verschweigt was? Muss ich das wissen?
Komplementarität: Titel sagt WAS → Thumbnail sagt WER es versteckt
Background:    abstract_tech — fließende Datenströme, holographische Panels
Scene:         abstract holographic environment, flowing blue data streams, translucent
               floating panels with code particles, deep midnight atmosphere
Creator:       curious-skeptical — leicht hochgezogene Augenbraue, analytischer Blick
Optional:      —
Accent:        Pulse Blue #4A9EFF

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KONZEPT B — ANGST / FOMO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Headline:      "DU VERLIERST GELD"
Click-Hook:    Viewer hat Angst, etwas zu verpassen oder bereits zu verlieren
Komplementarität: Titel sagt WIE → Thumbnail sagt WAS du verlierst wenn du es nicht tust
Background:    dark_cinematic — dunkles Studio, schwere Schatten, dramatisches Licht
Scene:         dark premium tech studio interior, dramatic side-lighting, deep foreground
               shadows, tense cinematic atmosphere, matte surfaces
Creator:       focused-gaze — direkter intensiver Blick in die Kamera, ruhige Stärke
Optional:      —
Accent:        Electric Coral #FF6B4A

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KONZEPT C — SPEZIFISCHES ERGEBNIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Headline:      "IN 20 MIN FERTIG"
Click-Hook:    Konkretes Versprechen — Viewer glaubt, das auch schaffen zu können
Komplementarität: Titel sagt WAS gebaut wird → Thumbnail sagt WIE SCHNELL
Background:    clean_minimal — minimalistisches dunkles Studio, Apple-Ästhetik
Scene:         minimalist premium dark studio, single MacBook Pro on matte surface,
               single spotlight, architectural shadows, zero clutter
Creator:       slight-smile — leichtes natürliches Lächeln, zugewandt, Erfolg ausstrahlend
Optional:      UI-Mockup (Layer 4c) wenn Tool-Demo im Video
Accent:        Beacon Yellow #FFD23F
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**In AUFRUF-MODUS B:** Zeige zusätzlich "KONZEPT D" mit den Feldern aus
`a8_upload.thumbnail_briefing` (so wie es das youtube-production Script vorbereitet hat).

#### 🔄 CHECKPOINT 0: Concept Selection

> "Welches Konzept nehmen wir? A (Neugier), B (Angst/FOMO), C (Spezifisches Ergebnis)[, D (Script-Briefing)]?
> Oder soll ich Elemente kombinieren?"

The selected concept's fields feed directly into Step 1:
- `headline` → Layer 2 text in editor
- `scene` → `scene_description` for Layer 1 background prompt
- `creator expression` → frame selection guidance in Layer 3
- `background style` → Gemini generation style
- `optional layers` → which of Layer 4b/4c/4d to generate
- `accent color` → glow color and optional text color

---

### Step 1: Briefing Confirmation

The selected concept from Step 0 provides the full briefing. Confirm the active fields:

| Field | Value (from selected concept) |
|---|---|
| Headline | From concept proposal (2–4 words, GROSSBUCHSTABEN) |
| Scene description | From concept `Scene` field |
| Background style | From concept `Background` field |
| Creator expression | From concept `Creator` field |
| Optional layers | From concept `Optional` field |
| Accent color | From concept `Accent` field |

**`creator_emotion` → Frame Selection Guide:**

Use the creator expression field to identify the best frame in the footage:

| Expression | Suche nach diesem Ausdruck im Video |
|---|---|
| curious-skeptical | eine hochgezogene Augenbraue, leicht fragender Ausdruck |
| focused-gaze | konzentrierter direkter Blick in die Kamera, ruhige Stärke |
| slight-smile | leichtes natürliches Lächeln, Mundwinkel leicht oben, zugewandt |
| sovereign-wonder | leicht hochgezogene Augenbrauen, offener Blick, stille Faszination |

**Headline rules (always apply):**
- NEVER too specific — general and sensational ("reißerisch")
- Good: "UNFASSBAR!", "WAHNSINN!", "NIE WIEDER", "KI NIMMT AB"
- Bad: "TWILIO API SETUP", "N8N WORKFLOW"
- Thumbnail text ≠ video title (complementarity rule)

**🔄 CHECKPOINT 1**: "Konzept **[X]** ist aktiv. Headline: **[HEADLINE]**, Style: **[Stil]**. Passt das so — weiter mit Layer-Generierung?"

### Step 2: Generate Layers

#### Layer 1: Background Scene (without person)

Generate a thematic background via **Nano Banana 2**. NO person in the prompt. Generate **4 variations** for user to choose from.

**Prompt assembly (4 parts combined — order matters):**
1. `TEMPLATE.background_prompt_template` with filled variables (`{{scene_description}}` from the selected concept's `Scene` field, `{{lighting_style}}` + `{{person_side}}` from style)
2. `background_styles.<selected_style>.prompt_suffix` (selected in Step 1)
3. `brand.global_style.prompt_block` — **MANDATORY append to every background prompt** (cinematic concept art style, bokeh, lighting, color grade)
4. `brand.negative_keywords`

**Selected style determines** `{{lighting_style}}` and the visual feel — read `background_styles.<style>` from `gemini-thumbnail-config.json`.

**4 variation strategy:**
- Variation 1: Main variant — selected style + concept scene description
- Variation 2: Same style, different angle or lighting intensity
- Variation 3: Alternative scene concept (different environment, same style)
- Variation 4: Alternative emotional angle — e.g. if Neugier is selected, try a darker more tension-heavy version

Key rules (always enforced):
- `no people, no person, no text, no letters` always in prompt
- `{{person_side}}` = opposite of where person will stand (leave compositional space)
- 16:9 aspect ratio, 1344×768 or higher

**Background prompt examples by style:**
- `dark_cinematic`: `"wide angle dark premium tech studio interior, matte desk surfaces, premium equipment silhouettes, warm bokeh depth, cinematic Rembrandt lighting"`
- `illustrated_workshop`: `"illustrated 3D workshop with robots working on circuit boards, glowing code streams, warm amber light, floating holographic elements, layered depth"`
- `abstract_tech`: `"holographic displays with data visualizations, flowing teal light streams, translucent floating UI panels, volumetric blue beams"`
- `clean_minimal`: `"minimalist dark studio, single MacBook Pro on matte surface, single spotlight, architectural shadows, Apple keynote aesthetic"`

#### Layer 3: Person Cutout (Video Frame — always)

The person layer **always** comes from real video footage. Frame candidates are surfaced by the **Precision Editor's video analysis** — no manual probe script needed.

In the Thumbnail Studio editor, Person-Tab → "Frame aus Video verwenden" (via `VideoFramePicker.tsx`): select a candidate or scrub the video freely, draw a crop rectangle, click "Frame verwenden" → rembg (`birefnet-general` + alpha matting) runs automatically server-side → cutout saved and ready in the editor.

**Frame selection guidance:**
- Use the emotion table from Step 1 to identify which expression to look for
- The script's `creator_pose` is the ideal — if it doesn't exist in the footage, pick the closest alternative and note the substitution
- Best frames: direct camera gaze, clear expression, sharp focus on face

#### Layer 4: Tool-Komposition (ONE composed image, not individual icons)

Generate a **single composed image** showing all tools and their relationships.

**Process:**
1. **JSON v3:** Read `a1_concept.stack[]` for the exact tool list. Read `thumbnail_briefing.tool_composition` for the visual layout description.
   **Markdown:** Extract from script body manually.
2. Identify the "master" tool (first in stack or most visually dominant per `tool_composition`)
3. Generate **4 variations** via Nano Banana 2 for user to choose from
4. Use `rembg` for cutout → single layer in editor

**Resolution:** 512×512 or 768×768 (sufficient for ~300×200px in the final thumbnail)

**Quality standard (STRICT — no cheap-looking results):**
- 3D isometric/perspective rendering, NOT flat design
- Each icon as glassmorphism/glossy floating tile with shadow and reflection
- Glowing connection lines (volumetric glow, not simple strokes)
- Depth of field between foreground and background icons
- Light effects: rim-light, ambient occlusion, volumetric glows
- Master tool visually dominant (larger, more glow, centered)
- Style reference: Premium App Store feature graphic, Apple Keynote slides
- NEVER: clip-art, flat design, stock look, cheap/generic appearance

**Background:** Plain solid light gray (`#E0E0E0`) for clean rembg cutout

**Example prompt (Voice Agent with Claude Code + Twilio + ElevenLabs):**
```
"premium 3D isometric tech composition on plain light gray background,
central large glossy Claude Code icon (orange asterisk on warm gradient tile)
connected via glowing blue energy lines to smaller Twilio icon (red phone on white tile)
on the left and ElevenLabs icon (audio waveform on dark blue tile) on the right,
floating glass tiles with soft shadows and reflections, volumetric light rays between icons,
depth of field, premium product render style, no text, no labels, high detail"
```

**Self-iteration rule:** Generate at minimum 2-3 prompt variations. Only show user the best 4 results.

#### Layer 4b: 3D Charakter (OPTIONAL)

**Trigger — generate when video theme has a clear "character":**
- KI-Assistent / Chatbot → `helpful_robot`
- Voice-Agent / Telefon-Sekretariat → `business_assistant`
- Analyse / Reporting / Dashboard → `data_analyst`
- Build-Video / App erstellt → `tech_wizard`

**Process:**
1. Read `a1_concept.stack[]` + `meta.title` → select `character_type` from `floating_elements.character_mascot.character_types`
2. Assemble prompt: `floating_elements.character_mascot.prompt_template` with `{{character_type}}` + `{{character_style}}`
3. Generate **4 variations** (768×768, plain `#E0E0E0` background)
4. User selects one → **rembg cutout** (`birefnet-general`)
5. Import cutout into editor as new layer

**rembg rule:** Plain solid gray background (`#E0E0E0`) is MANDATORY for clean cutout. If generated image has gradient or textured background → regenerate.

**Positioning in editor:** Opposite side from person, upper half, scale ~35-45% of person height.

#### Layer 4c: UI-Mockup (OPTIONAL)

**Trigger — generate when:** The video demonstrates a software tool or workflow that benefits from showing the UI (e.g., building with Claude Code, n8n workflow, Twilio dashboard).

**Process:**
1. Derive `{{ui_description}}` from `a1_concept.stack[0]` using `floating_elements.ui_mockup.ui_description_guide`
2. Choose `{{mockup_type}}`: `laptop_perspective` (more dynamic) or `monitor_straight` (more screen area)
3. Assemble prompt: `floating_elements.ui_mockup.prompt_template` with variables
4. Generate **2 variations** (1024×768, plain `#E0E0E0` background)
5. User selects one → **rembg cutout** (`birefnet-general`)
6. Import into editor as layer

**rembg rule:** Plain solid gray background (`#E0E0E0`) is MANDATORY. Device must have clean edges. If device blends into background → regenerate with more explicit "plain solid light gray (#E0E0E0) background" in prompt.

**Positioning in editor:** Can be same side as person (person "interacts" with it) or opposite side. Never overlap the headline text.

#### Layer 4d: Pfeil / Directional Arrow (OPTIONAL)

**Trigger — generate when:** A specific element (person holding mockup, key icon, mascot) should be pointed out for emphasis.

**Process:**
1. Determine direction from intended composition (arrow FROM headline TO emphasized element)
2. Select `{{direction_description}}` from `floating_elements.directional_arrow.directions`
3. Assemble prompt: `floating_elements.directional_arrow.prompt_template` with direction
4. Generate **1 variation** (512×512, plain `#E0E0E0` background)
5. **rembg cutout** (`birefnet-general`) — yellow arrow on gray provides strong contrast for clean cutout
6. Import into editor, position pointing at the target element

**Rule:** Max 1 arrow per thumbnail. Always Beacon Yellow (#FFD23F). Never combine with more than 1 other optional element.

#### Layer 2: Headline Text

Text is rendered **live in the editor** — no pre-generation needed. The editor renders text with:
- Inter Display Black font
- Multi-layer stroke (3 layers: deep, mid, crisp)
- Multi-layer shadow (deep 8/10px + mid 4/5px)
- Vertical gradient (light → dark, top → bottom)
- Text goes BEHIND the person (depth layering)

### Step 3: 🛡️ Validate All Prompts

Before running any generation, validate background and icon prompts:

| # | Rule | Check | Auto-Fix |
|---|------|-------|----------|
| V1 | **No text in images** | All prompts contain `no text` | Append |
| V2 | **Background has no person** | BG prompt contains `no people, no person` | Add |
| V3 | **Boardroom-Test (BG)** | Background prompt includes `premium`, `cinematic`, `professional` — NOT: neon, gaming, cartoon, clip-art, meme | Add `premium tech aesthetic, executive quality` |
| V4 | **Boardroom-Test (Icons)** | Tool-Komposition prompt includes `premium 3D`, `glossy`, `professional` — NOT: flat design, clip-art, cartoon | Add `premium product render style, executive quality` |
| V5 | **Entscheider-Qualität** | Would a Geschäftsführer/C-Level show this in a board presentation? If any element looks cheap, unserious, or gaming-aesthetic → regenerate | Flag for review |
| V6 | **Charakter ist thematisch** | Character type matches video content — no generic robot for finance topics, no business_assistant for code tutorials | Reassign character_type |
| V7 | **UI-Mockup zeigt reale UI** | Laptop screen description references actual tool from `a1_concept.stack[]` | Rewrite ui_description |
| V8 | **Max 2 optionale Elemente** | Not all three optional layers simultaneously — pick Charakter+Mockup OR Charakter+Pfeil OR Mockup+Pfeil | Remove least impactful |
| V9 | **Plain gray bg für rembg** | All floating elements (4b/4c/4d) generated on plain `#E0E0E0` — no gradients, no textured bg | Regenerate if bg is not flat gray |

Show validation output to user before generating.

### Step 4: Composite in Editor

After all layers are ready, open the editor for positioning:

1. **Start review server** (if not running): `cd /Users/a7wwiri/Projects/Video_Post_Production && python -m backend review` (port 8899; auto-starts Next.js API backend as subprocess)
2. **Open editor**: `http://localhost:8899/thumbnail-studio/?projectName=<project_name>` (or click the **Studio** button in the review UI topbar)
3. Click **"Letzte Generierung laden"** or drag individual layers onto the canvas

**Layer positioning guidelines:**
- **Person**: Scale ~2x frame height (94-100% scale in editor), head in upper portion, body extends below frame
- **Text**: Position on opposite side of face, fills 40-50% of frame area
- **Glow**: Center on person's head, golden/amber color, 40-60% intensity, radius 300-400px
- **Icons**: Arrange in circle formation, lower-left area, 25-35% scale

**Editor controls:**
- Drag & Drop layers on canvas
- Per-layer: position (X/Y), scale, horizontal stretch (scaleX), opacity, visibility, z-order
- Live headline text editing
- Text color (White, Yellow, Warm White, Blue, Cyan), gradient toggle, size slider (60-220px)
- Glow color, intensity, radius, position, "Center glow on head" button
- PNG Export button

**Optional layer positioning:**
- **3D Charakter (4b)**: Opposite side from person, upper half of frame, 35-45% of person's height, slight overlap with background elements ok — never overlaps headline text
- **UI-Mockup (4c)**: Same side as person (person "holds" or "looks at" it) OR opposite if person is centered; never covers face; scale so screen is readable
- **Pfeil (4d)**: Points FROM headline text TOWARD the emphasized element; tip touches or slightly overlaps the target; scale large enough to read at 160×90px mobile preview

**🔄 CHECKPOINT 2**: "Alle Layer sind generiert und die Komposition ist validiert. Öffne http://localhost:8899/thumbnail-studio/ für den Feinschliff. Sag Bescheid wenn du fertig bist."

### Step 5: Refinement

**Common adjustments:**
| Issue | Fix |
|---|---|
| Face too narrow | Use scaleX slider (stretch to 110-120%) |
| Wrong emotion/expression | Go back to VideoFramePicker — select a different frame |
| Different gaze direction | Go back to VideoFramePicker — scrub to a frame looking the other way |
| Text too small/big | Text size slider |
| Text overlaps face | Move text X/Y or person position |
| Background doesn't fit | Regenerate background with different prompt |
| Icons look flat | Regenerate with more detailed 3D prompt |
| Glow wrong color | Switch in Glow panel |

### Step 6: Export

1. Click **"PNG Export"** in the editor toolbar
2. File downloads as `thumbnail-[timestamp].png` (1280×720)
3. Verify: readable at mobile size (160×90px)?
4. Verify: grayscale test — enough contrast?

**🔄 CHECKPOINT 3**: "Thumbnail exportiert. Zufrieden oder soll ich Variationen erstellen?"

## Positioning Rules (CRITICAL)

The person's gaze direction determines the ENTIRE layout:

### Position RIGHT (Person schaut nach links)
```
┌──────────────────────────────────────┐
│ HEADLINE     │                       │
│ TEXT         │    👤 Person           │
│ (1-2 Zeilen)│    (rechte Hälfte)     │
│              │                       │
│ [Icons]      │                       │
└──────────────────────────────────────┘
```
- Person: right side, max 45% frame width, head in upper third
- Text: LEFT at head height (Y: 30-120px), 1-2 lines, NO overlap with person
- Icons: LEFT below text
- Glow: behind person's head

### Position LEFT (Person schaut nach rechts)
```
┌──────────────────────────────────────┐
│                │         HEADLINE    │
│ 👤 Person      │         TEXT        │
│ (linke Hälfte) │         (1-2 Zeilen)│
│                │                     │
│                │         [Icons]     │
└──────────────────────────────────────┘
```
- Person: left side, max 45% frame width, head in upper third
- Text: RIGHT at head height, 1-2 lines, NO overlap with person
- Icons: RIGHT below text
- Glow: behind person's head

### Position CENTER (Person schaut frontal)
```
┌──────────────────────────────────────┐
│      HEADLINE TEXT (volle Breite)    │
│         ┌─────────────┐             │
│ [Icon]  │  👤 Person   │  [Icon]    │
│ (links) │  (zentriert) │  (rechts)  │
│         │              │            │
└──────────────────────────────────────┘
```
- Person: centered, max 40% frame width
- Text: TOP across full width, max 30% head overlap allowed
- Icons: split LEFT and RIGHT of person (ideal for tool comparisons)
- Glow: behind person's head, centered

### Person Scale Rules
- Person max 45% frame width (LEFT/RIGHT) or 40% (CENTER)
- Head occupies 30-35% of frame HEIGHT (NOT 50%+!)
- Body extends below frame (cropped at ~waist level)
- Head always in upper third of frame

### Text Rules
- Font size: 100-160px depending on word count
- 1-2 lines maximum
- At head height when LEFT/RIGHT positioned
- Across full width when CENTER positioned
- ALWAYS behind person (depth layering)

## Compositing Design Rules (Reference-Matched)

Based on analysis of @Mike-Mildenberger and @everlastai thumbnails:

| Rule | Value |
|------|-------|
| **Text size** | 100-160px, fills 40-50% of frame |
| **Text stroke** | 3-layer: deep (fontSize×0.09), mid (×0.07), tight (×0.06) |
| **Text shadows** | Deep: 8/10px offset, 24px blur. Mid: 4/5px, 12px blur |
| **Text gradient** | Vertical: full color top → 45% darker bottom |
| **Line height** | 1.05 (very tight, broadcast style) |
| **Text color** | White default, Yellow alternate |
| **Text position** | Determined by Positioning Rules above |
| **Depth layering** | Text renders BEHIND person (key professional look!) |
| **Person scale** | Max 45% frame width, head 30-35% frame height |
| **Face glow** | Radial gradient behind head, color matches text, 40-60% intensity |
| **Background** | Thematic to video, saturated (+18%), dark, **Entscheider-tauglich** — must pass Boardroom-Test |
| **Icons** | Premium 3D glossy, **Entscheider-Qualität** — Deloitte/McKinsey/Apple Keynote level |
| **Icon quality** | Deloitte/McKinsey/Apple Keynote aesthetic, NOT clip-art |
| **Icon resolution** | 512×512 or 768×768 (sufficient for thumbnail size) |
| **Saturation** | +18% on background |
| **Sharpening** | sigma 0.8-1.0 post-composite |

## Brand Rules (Always Enforced)

**Colors — max 3 per thumbnail:**
- Midnight: #0A0E1A (background, 60-70%)
- Beacon Yellow: #FFD23F (headlines)
- One accent: Pulse Blue #4A9EFF, Electric Coral #FF6B4A, or Signal Cyan #00E5CC

**Headline rules:**
- Max 3-5 words, DEUTSCH, Großbuchstaben
- Sensational/emotional, not technical
- Thumbnail text ≠ video title (complementarity rule)

**Forbidden:**
- Bright white backgrounds, neon, stock photo aesthetic
- Emojis, clip-art, gaming aesthetic
- Fake shock faces / übertriebene YouTube-Grimassen
- More than 3 colors per thumbnail

## File Locations

| What | Path |
|------|------|
| API-Backend (Next.js) | `/Users/a7wwiri/Projects/Thumbnail_generator/` — auto-started by review server on port 3001 |
| API Keys | `/Users/a7wwiri/Projects/Thumbnail_generator/.env.local` |
| rembg | system PATH (`rembg`) |
| Output dir | `output/<project>/thumbnail/` |
| Fonts | `public/fonts/InterDisplay-Black.ttf` |
| Logo PNGs | `public/logos/` |
| Composite script (CLI fallback) | `scripts/composite-multilayer.mjs` |
| Design spec | `docs/THUMBNAIL_DESIGN_SPEC.md` |
| Editor (Vite SPA) | `http://localhost:8899/thumbnail-studio/` (requires `python -m backend review` in `Video_Post_Production/`) |
| SPA source | `/Users/a7wwiri/Projects/Video_Post_Production/thumbnail_studio/src/` |
| SPA build output | `/Users/a7wwiri/Projects/Video_Post_Production/backend/static/thumbnail_studio/` |
| SPA build command | `cd /Users/a7wwiri/Projects/Video_Post_Production/thumbnail_studio && npm run build:nocheck` |
| Video candidates | `output/<project>/thumbnail/candidates/` — `candidate_NN.jpg` (1280px preview) + `candidate_NN_4k.jpg` (3840×2160 master) |
| Probe script | `python /Users/a7wwiri/Projects/Video_Post_Production/test_thumbnail_probe.py --minutes <N>` |
