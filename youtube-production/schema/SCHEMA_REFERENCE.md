# BUILT Video Script — JSON Schema Reference

> **Schema file:** `video_skript_schema.json`
> **Purpose:** Canonical data format for all BUILT YouTube video artifacts (A1–A8).
> Every video script is a single JSON file following this schema.

---

## `meta` — Video Metadata

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Primary video title (used on YouTube) |
| `title_alt` | string | Alternative title variant for A/B testing |
| `format` | enum | `sonne` (pillar, 15–20 min) · `planet-demo` (4–8 min) · `planet-explainer` (5–15 min) |
| `cluster` | string | Cluster ID and name, e.g. `"C1 — Voice Agents"` |
| `length_min` | number | Target video length in minutes |
| `date` | string | Last updated date (DD.MM.YYYY) |
| `editing_pattern` | string | Chosen editing pattern: Progressive Rhythm / Hybrid Tempo / Anchor / Narrative Loop |
| `editing_pattern_rationale` | string | Why this editing pattern was chosen for the video |

---

## `a1_concept` — A1: Concept & Strategy

The foundational artifact. Defines what the video is about, who it's for, and how it's structured.

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Video title |
| `target_audience` | string | Who is this video for? Demographics, pain points, context |
| `core_promise` | string | What the viewer will have/know after watching |
| `magic_moment` | string | The single most impressive moment in the video — described so vividly you can picture it |
| `target_persona` | string | Fictional representative viewer with name, age, job, and specific problem |
| `stack` | string[] | Tech stack / tools used in the video |
| `emotional_target` | string | What should the viewer feel at the end? One clear emotional goal (no "Emotional Spaghetti") |
| `term_brands` | string[] | Proprietary labels/terms coined for this video's concepts (triggers Zeigarnik effect + authority) |

### `a1_concept.hook` — Opening Hook (PAS Model)

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Hook style variant (PAS Type 1–8, see SKILL.md hook-system) |
| `opening_line` | string | The very first sentence of the video — must grab in 7 seconds |
| `rationale` | string | Why this hook type was chosen for this topic/audience |
| `pas.problem` | string | Problem statement (what hurts) |
| `pas.agitation` | string | Agitation (why it's worse than you think) |
| `pas.solution` | string | Solution preview (what we'll build) |
| `demo_teaser` | string | Brief description of the demo preview shown after hook |
| `engagement_question` | string | First community question asked within 30 seconds |

### `a1_concept.brand_bumper`

| Field | Type | Description |
|-------|------|-------------|
| `variant` | string | Bumper variant (A: Cost/Revenue, B: Time, C: Competence, D: Competition) |
| `text` | string | Exact bumper text (1–2 sentences, max 8 sec) |

### `a1_concept.narrative_structure`

| Field | Type | Description |
|-------|------|-------------|
| `chosen` | string | Structure A (Problem-Solving), B (Feature-Tour), or C (Before/After) |
| `rationale` | string | Why this structure fits the topic |

### `a1_concept.video_structure[]`

High-level timeline overview — one row per major section.

| Field | Type | Description |
|-------|------|-------------|
| `timecode` | string | Approximate start time (MM:SS) |
| `content` | string | What happens in this section |
| `block_type` | string | Visual block type (CC, SC, CS, GR for Sonne) |

### `a1_concept.notebook_insights[]`

Research findings from NotebookLM.

| Field | Type | Description |
|-------|------|-------------|
| `category` | string | Type of insight (Hook, Retention, Market, etc.) |
| `insight` | string | The finding itself |
| `source` | string | NotebookLM source reference, format: `📓 NB: [Notebook Name]` |

### `a1_concept.snowball_keywords`

Results of the mandatory Snowball Keyword Research (interactive with creator).

| Field | Type | Description |
|-------|------|-------------|
| `autocomplete_mining` | string[] | Raw YouTube autocomplete suggestions collected by creator |
| `long_tail_filter` | string[] | Filtered keywords (4+ words, clear intent, contains "KI") |
| `competition_check` | string | Summary of YouTube search competition for top keywords |
| `relevance_check` | string | Does the keyword fit BUILT? Boardroom test? |
| `main_keyword` | string | Primary keyword — goes into title position 1–60 chars, first tag |
| `secondary_keywords` | string[] | 3–5 additional keywords for tags and description |

### `a1_concept.differentiation`

| Field | Type | Description |
|-------|------|-------------|
| `differentiation` | string | What makes this video unique vs. existing YouTube content on the same topic — the "why watch THIS" answer |

### `a1_concept.cluster_classification`

| Field | Type | Description |
|-------|------|-------------|
| `cluster` | string | Cluster ID and name |
| `type` | string | Role in the Sonnensystem (Sonne/Planet-Demo/Planet-Explainer) |
| `related_videos` | string[] | Other videos in this cluster (planned or published) |

### `a1_concept.micro_ctas[]`

| Field | Type | Description |
|-------|------|-------------|
| `timecode` | string | Approximate placement (e.g. `"~00:55"`) |
| `question` | string | Community question to drive engagement |

### `a1_concept.source_registry[]`

Every statistic cited in the video must have an entry here.

| Field | Type | Description |
|-------|------|-------------|
| `statistic` | string | What claim is being made |
| `value` | string | The number/percentage cited |
| `source` | string | Who published this data |
| `year` | number | Publication year |
| `url` | string | Direct link to the source (for YouTube description) |
| `retrieved_at` | string | When the source was accessed (DD.MM.YYYY) |
| `used_in_passages` | number[] | Which passage numbers cite this statistic |
| `text_overlay` | string\|null | Text overlay shown in video (e.g. `"Source: BIA/Kelsey, 2019"`) |

### `a1_concept.doc_references[]`

Official documentation sources used for tech verification.

| Field | Type | Description |
|-------|------|-------------|
| `source` | string | Documentation name |
| `url` | string | Direct URL |
| `retrieved_at` | string | Access date |

---

## `a2_roadmap[]` — A2: Viewer Roadmap

The viewer's journey through the video — phase by phase.

| Field | Type | Description |
|-------|------|-------------|
| `phase` | number | Phase number (sequential) |
| `name` | string | Phase name (e.g. "Hook", "Setup", "Demo", "Live-Test") |
| `precondition` | string | What the viewer must understand before this phase |
| `goal` | string | What this phase achieves |
| `outcome` | string | What the viewer has after this phase |
| `wow_moment` | string | The highlight or surprise of this phase |
| `anchor` | string | Obsidian-compatible anchor (e.g. `^phase-1`) |

---

## `a3_script[]` — A3: Full Script

The complete video script — one entry per passage (scene).

| Field | Type | Description |
|-------|------|-------------|
| `passage` | number | Sequential passage number |
| `title` | string | Short passage title |
| `duration_sec` | number | Estimated duration in seconds |
| `phase_anchor` | string\|null | Links to a2_roadmap phase (e.g. `^phase-1`) |
| `block_type` | string | Visual type: CC/SC/CS/GR (Sonne) or HC/DO/PB/DL/RZ/RC/TC (Demo) |
| `energy` | string | Mood/intensity direction for the creator |
| `viewer_sees` | string | What the viewer sees on screen (camera, graphics, overlays) |
| `text_overlay` | string\|null | Mobile-friendly text overlay (for viewers without sound) |
| `mode` | enum | `teleprompter` (read exact text) or `story` (speak freely from context) |
| `story` | string | **Always populated.** Context for the creator — what this passage is about, why it matters, what to focus on. Creator reads this to understand the passage before recording. |
| `teleprompter` | string | Exact spoken text. Populated when `mode: "teleprompter"`. Empty when `mode: "story"`. Uses `**bold**` for emphasis, `[Pause]` for breaks. |
| `talking_points` | string[] | Thought chain for free speaking. Only used when `mode: "story"`. |
| `stage_directions` | string[] | Concrete actions (what to DO, not say). Camera/screen directions, timing cues. |
| `camera_tip` | string\|null | Specific camera or framing advice for this passage |
| `fallback` | string\|null | What to do if something goes wrong |
| `source_overlay` | string\|null | Source attribution overlay for statistics (e.g. `"Source: BIA/Kelsey, 2019"`) |
| `graphic_refs` | string[] | IDs of graphics shown (e.g. `["GR_01"]`) — links to a4_visuals |
| `prompt_refs` | string[] | IDs of prompts used (e.g. `["PR_01"]`) — links to a5_prompts |
| `retention_markers` | string[] | Retention techniques used (loops, PoH, WAS→WARUM→WIE, etc.) |

---

## `a4_visuals[]` — A4: Graphics & B-Roll

Every visual element in the video.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique ID (e.g. `GR_01`, `BR_01`) |
| `type` | enum | `grafik` (generated graphic) or `b-roll` (footage) |
| `passage` | number | Which passage this visual belongs to |
| `filename` | string | Output filename (e.g. `GR_01_kostenvergleich.png`) |
| `description` | string | Brief description of what the visual shows |

### `a4_visuals[].briefing`

Content briefing — NO brand styling (that's added by a separate style agent).

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Chart/diagram type (e.g. "Horizontal bar chart, 3 bars") |
| `title` | string | Graphic title as shown to the viewer |
| `boardroom_test` | boolean | Would a CEO show this in a presentation? |

### `a4_visuals[].graphic_desc_gemini`

Image generation prompt for Gemini/Imagen.

| Field | Type | Description |
|-------|------|-------------|
| `prompt` | string | Complete generation prompt |
| `content` | string | What the graphic shows (elements, data, structure) |
| `style_note` | string | Additional style guidance (content-focused, not brand) |

### `a4_visuals[].graphic_desc_remotion`

Animation description for Remotion-based motion graphics.

| Field | Type | Description |
|-------|------|-------------|
| `composition_type` | string | Always `"custom_graphic"` |
| `duration_seconds` | number | Total animation duration |
| `elements[]` | array | Individual visual elements with timing and animation |
| `elements[].id` | string | Element identifier |
| `elements[].type` | enum | `text`, `icon`, `box`, `arrow`, `image_ref` |
| `elements[].content` | string | Display content |
| `elements[].appear_at_seconds` | number | When the element appears (relative to graphic start) |
| `elements[].animation` | enum | `fade_in`, `slide_left`, `slide_right`, `slide_up`, `scale_up`, `typewriter`, `draw_path` |
| `elements[].duration_seconds` | number | How long the appear animation takes |
| `elements[].position` | object | `{x, y}` position |
| `elements[].style` | object | Color, size, glow, etc. |
| `transitions` | object | `{in, out}` — how the entire graphic enters/exits |
| `audio_sync[]` | array | Sound effects synced to spoken words |
| `audio_sync[].trigger_word` | string | Spoken word that triggers the effect |
| `audio_sync[].element_id` | string | Which element appears |
| `audio_sync[].sound_effect` | enum | `whoosh`, `pop`, `ding`, `swoosh`, `reveal`, `click`, `rise` |
| `text_reference` | string | The spoken text that accompanies this animation |

---

## `a5_prompts[]` — A5: Claude Prompts

All prompts shown/used in the video — copy-paste ready.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique ID (e.g. `PR_01`) |
| `passage` | number | Which passage uses this prompt |
| `title` | string | Descriptive prompt title |
| `prompt` | string | Complete prompt text (newlines as `\n`) |

---

## `a6_rehearsal` — A6: Rehearsal & Setup

Everything the creator needs to prepare and execute the recording.

### `a6_rehearsal.prerequisites[]`

| Field | Type | Description |
|-------|------|-------------|
| `tool` | string | Tool/service name |
| `version` | string | Required version |
| `plan` | string | Required pricing plan |
| `signup_url` | string | Where to sign up |
| `api_key_path` | string | Where to find the API key in the dashboard |

### `a6_rehearsal.setup_blocks[]`

Step-by-step setup instructions grouped into blocks.

| Field | Type | Description |
|-------|------|-------------|
| `block` | string | Block letter (A, B, C, D) |
| `title` | string | Block title |
| `goal` | string | What this block achieves |
| `duration_min` | number | Estimated duration in minutes |
| `steps` | string[] | Ordered list of concrete steps (copy-paste commands included) |

### `a6_rehearsal.demo_sequence[]`

The exact demo flow for dry-run practice.

| Field | Type | Description |
|-------|------|-------------|
| `nr` | number | Step number |
| `action` | string | What the creator does |
| `input` | string | What gets typed/dictated |
| `screen_shows` | string | Expected screen state |
| `duration` | string | Approximate duration |

### `a6_rehearsal.tests[]`

| Field | Type | Description |
|-------|------|-------------|
| `action` | string | Test input/question |
| `expectation` | string | Expected result |

### `a6_rehearsal.troubleshooting[]`

| Field | Type | Description |
|-------|------|-------------|
| `problem` | string | What went wrong |
| `symptom` | string | What the creator sees |
| `cause` | string | Root cause |
| `fix` | string | How to fix it |
| `prevention` | string | How to avoid it |

### Other `a6_rehearsal` fields

| Field | Type | Description |
|-------|------|-------------|
| `checklist_before` | string[] | Pre-shoot checklist (accounts, keys, tools) |
| `checklist_shoot_day` | string[] | Day-of-shoot checklist (audio, lights, screens) |
| `checklist_shooting` | string[] | During-shoot reminders (pacing, pauses, errors) |
| `doc_sources[]` | array | Official docs used — `{source, url, retrieved_at}` |
| `verified_api_details` | object | Free-form object with verified API specifics (endpoints, headers, models) |
| `audio` | object | Audio specs: `{format, target_lufs, export}` |
| `time_estimate` | object | Time planning: `{setup_min, demo_min, total_min}` |

---

## `a7_cheat_sheet[]` — A7: Cheat Sheet

Quick-reference blocks for the creator during recording.

| Field | Type | Description |
|-------|------|-------------|
| `block` | string | Thematic block name (INTRO, CONTEXT, DEMO, LIVE-TEST, NUMBERS, CTA) |
| `passages` | string | Passage range (e.g. `"1-6"`) |
| `duration` | string | Approximate block duration |
| `goal` | string | What this block achieves |
| `bullet_points` | string[] | Key talking points for quick reference |

---

## `a8_upload` — A8: Upload Package

Everything needed for YouTube upload and promotion.

### `a8_upload.title_variants[]`

| Field | Type | Description |
|-------|------|-------------|
| `option` | string | Variant letter (A, B, C) |
| `title` | string | Full title |
| `characters` | number | Character count |
| `hook_type` | string | Hook strategy used in this title |
| `recommended` | boolean | Is this the recommended option? |

### Other `a8_upload` fields

| Field | Type | Description |
|-------|------|-------------|
| `description` | string | Full YouTube description (with chapters, links, sources) |
| `chapters[]` | array | Chapter markers — `{time, label}` |
| `tags` | string[] | YouTube tags (main keyword first) |
| `main_keyword` | string | Primary SEO keyword |
| `pinned_comment` | string | Full pinned comment text |

### `a8_upload.thumbnail_briefing`

Content-only briefing — describes WHAT the thumbnail shows, not HOW it looks. All design decisions (colors, glow, compositing, layer positioning) are handled by the separate `youtube-thumbnail` skill.

| Field | Type | Description |
|-------|------|-------------|
| `scene_description` | string | Detailed, cinematic description of the background scene. Written like a film set direction — specific enough to generate a compelling image. Think "Mr. Robot meets Apple Keynote": professional, atmospheric, aspirational. The viewer should see themselves in this scene. |
| `creator_pose` | string | What the creator does physically: body language, hand position, what they hold, where they look. E.g. "Holds phone to ear with left hand, right hand open in disbelief gesture, looking slightly left past camera" |
| `creator_emotion` | string | Target emotion for the creator's expression. Mapped by the thumbnail skill to LoRA-safe prompts. E.g. "Confident wonder — slightly raised eyebrows, composed but intrigued" |
| `headline` | string | 2–3 words, DEUTSCH, Großbuchstaben. Must be sensational and curiosity-driven ("reißerisch"), never technical. Complements the title, never repeats it. |
| `tool_composition` | string | Which tools/icons are visible and how they relate. Which tool is dominant (largest). E.g. "Claude Code dominant center, Twilio left, ElevenLabs right — connected by data flow" |
| `contrast_element` | string | The single element that pops visually and draws the eye. E.g. "Phone screen glowing with incoming call", "Terminal cursor blinking on a single line of code" |
| `ab_variant` | string | Alternative thumbnail concept for A/B testing — a fundamentally different visual idea, not just a color swap |
| `target_reaction` | string | What the scrolling Entscheider should think/feel in 0.5 seconds. E.g. "Das will ich auch können." / "Moment — das geht für 30€?" |

### `a8_upload.endscreen`

| Field | Type | Description |
|-------|------|-------------|
| `card_at` | string | Timecode where info card appears |
| `card_target` | string | What the card links to |
| `slot_left` | string | Left endscreen slot content |
| `slot_right` | string | Right endscreen slot content |

### `a8_upload.community_strategy`

| Field | Type | Description |
|-------|------|-------------|
| `shorts_teaser` | string | Best 30-sec clip for YouTube Shorts |
| `community_post_before` | string | Community post before upload (e.g. poll) |
| `community_post_after` | string | Community post after upload (e.g. behind-the-scenes) |
| `cross_promo` | string | Cross-promotion strategy |

### `a8_upload.cluster_linking`

| Field | Type | Description |
|-------|------|-------------|
| `pillar_video` | string | The Sonne (pillar) video of this cluster |
| `satellites` | string[] | Planet videos in this cluster |
| `playlist` | string | Playlist name |
| `endscreen_strategy` | string | How endscreen connects to cluster |

### `a8_upload.consulting_anchor`

| Field | Type | Description |
|-------|------|-------------|
| `text` | string | Exact consulting CTA text |
| `placement` | string | Where in the video and why |
