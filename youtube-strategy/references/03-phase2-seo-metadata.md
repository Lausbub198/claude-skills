# Phase 2: Intent-Specific SEO & Metadata

Generate YouTube metadata optimized for the 2026 NLP algorithm. YouTube now semantically
analyzes your title, description, tags, AND spoken content to determine which audience
cluster receives your video. Keyword stuffing is dead -- intent-specific language wins.

## The 2026 YouTube SEO Reality

- **YouTube NLP listens to your auto-captions** -- if your spoken words don't match your metadata, YouTube buries the video as clickbait
- **Intent-specific language** > keyword density -- you're telling the algorithm WHICH audience, not WHAT keywords
- **Title, description, and tags must form a coherent signal** -- they should all point to the same audience cluster
- **Chapters are indexed** -- they appear in search results and help discovery
- **Transcript-metadata mismatch is the #1 penalty** -- always cross-check before publishing

## Process

### Step 1: Generate Title Variants

Use Claude to generate 3 title variants, each optimized for a different goal:

1. **Click-Optimized:** Curiosity-driven, emotionally compelling. This is what gets the click from browse features and suggested sidebar.
2. **Search-Optimized:** Clear, specific, answers exactly what someone would search for. This wins in YouTube search and Google.
3. **Hybrid:** Balances click appeal with search clarity. Often the safest choice.

Prompt for Claude:

```
Generate 3 title variants for a German YouTube video about [TOPIC].
The target audience is German-speaking developers and tech enthusiasts.

Title 1 (Click-Optimized): Create a curiosity-driven title. Use pattern interrupts,
bold claims, or emotional triggers. Max 60 characters.
Examples: "Dieser Claude Code Trick ist illegal (fast)" / "Warum 90% der KI-Tools Geld verbrennen"

Title 2 (Search-Optimized): Clear, specific, answers search intent directly.
Include key terms someone would actually search for. Max 60 characters.
Example: "Claude Code Tutorial: So automatisierst du deinen Workflow 2026"

Title 3 (Hybrid): Best of both worlds. Searchable but still click-worthy.
Max 60 characters.

For each title, explain:
- Which emotional trigger it uses (curiosity/fear/specific result/urgency/social proof)
- Why it would work for this specific audience
- CTR estimate: low/medium/high
```

### Step 2: Write the Description

YouTube indexes the first 2-3 lines of your description heavily. Structure:

```
[LINE 1-2: Value promise -- what they'll learn, why watch]
[LINE 3-4: Key topics covered -- keyword-rich but natural]

[CHAPTER OVERVIEW with timestamps]

[DETAILED DESCRIPTION -- 2-3 paragraphs, natural language]

[LINKS & RESOURCES]
- Related video: [URL]
- Tool mentioned: [URL]
- Free resource: [URL]

[HASHTAGS -- 3 max, at the very end]
```

The first 200 characters are the most important -- they appear in search results.

### Step 3: Generate Tags

20-30 tags, organized by priority:

- **Primary (5-7):** Exact topic keywords in German (e.g., "Claude Code Tutorial", "KI Entwicklung")
- **Secondary (8-12):** Related concepts, broader terms ("KI Agenten", "Developer Tools", "Automatisierung")
- **Long-tail (5-10):** Specific phrases someone might search ("Claude Code fur Anfanger Deutsch", "KI Coding Workflow 2026")

Rules:
- Start with the most specific tags, end with broader category tags
- Always include "Deutsch" / "German" variants
- No competitor names (YouTube may flag this)
- No misleading tags (this IS checked against content)

### Step 4: Generate Chapter Markers

Chapters should be timestamped and keyword-optimized:

```
00:00 - [Hook title -- intriguing, not descriptive]
01:30 - [Topic 1 -- clear, searchable]
05:00 - [Topic 2 -- clear, searchable]
...
```

Each chapter title should be a mini-search-term. Viewers skim chapters to decide if the video is worth their time.

### Step 5: Metadata-Spoken-Content Cross-Check (CRITICAL)

This is the most important step. Before you ever upload, validate that your metadata
(title, description, tags, chapters) matches what will actually be spoken in the video.

**Instead of waiting for a post-filming transcript**, use the **telepro-script markdown**
as a proxy for the spoken content. This validates metadata BEFORE filming, catching
clickbait mismatches at the script-writing stage.

#### Why telepro-script instead of a post-filming transcript

- Validates metadata **before filming** -- catch broken promises early
- The `##` lines contain every word that will be spoken -- identical to what YouTube's NLP hears
- The structured format makes extraction deterministic: `##` = spoken, `#` = headers, `[NOTE:]` = internal notes
- No need to wait for post-production pipeline transcription

#### How the telepro-script is produced

The telepro-script markdown comes from this pipeline:

1. **Phase 3 (Retention Script)** produces the script with hooks, rehooks, open loops
2. **youtube-production A3 (Skript phase)** converts it to JSON passages with `teleprompter` fields
3. **telepro-script skill** (`~/.claude/skills/telepro-script/`) converts A3 passages to TelePro markdown

The resulting markdown file uses the TelePro format where `##`-prefixed lines are spoken text.

#### Extracting spoken content from the telepro-script

To extract the spoken text from a telepro-script markdown document:

1. Read the telepro-script file
2. Collect all lines beginning with `##` (no space after the markers)
3. Strip the `##` prefix to get the spoken text
4. Ignore all other content: `#` headers, `[NOTE:]` markers, `[PAUSE:N]`, `[SLOW]`/`[/SLOW]` blocks,
   `---` breath markers, `[IMG:...]` image references, empty lines, `**bold**`/`!!trigger!!` formatting

The extracted `##` lines form the exact spoken content that YouTube's NLP will analyze.

#### Running the cross-check

Claude can perform this validation:

```
You are a YouTube content validator. Compare the following metadata against the
actual spoken words extracted from the telepro-script markdown:

- VIDEO TITLE: [title]
- VIDEO DESCRIPTION: [description]
- VIDEO TAGS: [tags]
- CHAPTER MARKERS: [chapters]
- TELEPRO SCRIPT SPOKEN CONTENT (extracted ## lines):
  [the extracted spoken text]

Find ALL mismatches where the metadata promises something the spoken content
doesn't deliver. Flag severity:
  CRITICAL: clickbait (title promises something never said)
  WARNING: exaggeration (tag/keyword barely mentioned)
  INFO: minor mismatch (chapter timing slightly off)

Also check:
- Does the title's core promise appear in the first 30 seconds of spoken content?
- Are all tags represented in the spoken content at least once?
- Do chapter markers reflect the actual flow of spoken sections?
- Does the description over-promise compared to what's actually said?
```

#### If no telepro-script exists yet

If you're running SEO Phase 2 before Phase 3 (Retention Script) and the `telepro-script`
skill hasn't produced output yet:

1. **Generate initial SEO metadata now** (title variants, description, tags, chapters)
   based on the topic and competitive analysis
2. **Run the cross-check later** after Phase 3 completes and the telepro-script exists
3. **Revisit and adjust** any metadata that fails the cross-check

This is the recommended practical order since SEO metadata generation doesn't strictly
depend on having the script first -- but validation does.

### Step 6: Assemble the Final Metadata Package

Output everything in a single document:

```markdown
# SEO Metadata: [Topic]

## Title Variants
### Click-Optimized
**[Title]** -- CTR: [estimate]
**Trigger:** [emotional trigger]

### Search-Optimized
**[Title]** -- CTR: [estimate]
**Trigger:** [emotional trigger]

### Hybrid
**[Title]** -- CTR: [estimate]
**Trigger:** [emotional trigger]

## Final Description
[Full description with chapters]

## Tags (30)
primary, secondary, long-tail, ...

## Chapter Markers
[TIMESTAMP] - [Chapter title]
...

## Metadata-Spoken-Content Validation
### Input: Telepro-script markdown
[Path to telepro-script file or extracted ## lines]

### Issues Found: [X]
- [ ] [Issue 1] -- Severity: CRITICAL
- [ ] [Issue 2] -- Severity: WARNING

### Resolution
[How each issue was fixed]

## Final Checklist
- [ ] Title under 60 characters
- [ ] Description first 200 chars optimized
- [ ] 20-30 tags, specific to broad
- [ ] Chapters created and accurate
- [ ] Telepro-script cross-check completed (0 critical issues)
- [ ] No clickbait promises unmatched by spoken content
```

## Success Criteria

- [ ] 3 title variants generated (click, search, hybrid)
- [ ] Full description with chapters written
- [ ] 20-30 tags organized by priority
- [ ] Chapter markers created
- [ ] Telepro-script markdown used as proxy for spoken content (not post-filming transcript)
- [ ] Metadata-spoken-content cross-check completed
- [ ] 0 critical mismatches remaining
- [ ] Results saved to `youtube-strategy/seo-metadata.md`
