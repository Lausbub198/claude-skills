---
name: youtube-strategy
description: >
  YouTube strategy workflow based on "Mastering the YouTube Algorithm with Claude Code and AI Strategy".
  Use this skill whenever the user wants to research video topics, analyze competitors, write retention-optimized
  scripts, generate SEO metadata, or set up A/B tests. Covers the full pre-production strategy pipeline:
  Fundament (Topic Research) -> Phase 1 (Competitive Analysis) -> Phase 2 (SEO & Metadata) ->
  Phase 3 (Retention Script) -> Phase 4 (A/B Testing) -> Phase 5 (Demo Pack, optional).
  Triggers on: YouTube strategy, video topic research, competitive analysis, retention script,
  YouTube SEO, video metadata, A/B testing, thumbnail variants, viral topic scoring, content strategy,
  demo pack, live demo, demo setup.
---

# YouTube Strategy Workflow

Strategy pipeline with 1 fundament + 5 phases based on the notebook "Mastering the YouTube Algorithm
with Claude Code and AI Strategy". The user's niche: **AI, Agentic Coding, Developer Tools** --
German-language YouTube channel.

## How This Skill Works

Each phase is a self-contained workflow. You can run them in sequence (recommended) or jump
to a specific phase. Read the corresponding reference file for detailed instructions before
executing a phase.

## Phase Overview

| Phase | What It Does | Reference |
|-------|-------------|-----------|
| Fundament: Topic Research | Generate video ideas, score them for virality potential | [references/01-fundament-topic-research.md](references/01-fundament-topic-research.md) |
| Phase 1: Competitive Analysis | Multi-platform search for outlier content patterns | [references/02-phase1-competitive-analysis.md](references/02-phase1-competitive-analysis.md) |
| Phase 2: SEO & Metadata | Intent-specific titles, descriptions, tags, chapters | [references/03-phase2-seo-metadata.md](references/03-phase2-seo-metadata.md) |
| Phase 3: Retention Script | Write scripts with rehooks every 60-90s and open loops | [references/04-phase3-retention-script.md](references/04-phase3-retention-script.md) |
| Phase 4: A/B Testing | 3 title+thumbnail variants based on emotional triggers | [references/05-phase4-ab-testing.md](references/05-phase4-ab-testing.md) |
| Phase 5: Demo Pack *(optional)* | Setup guide + production pack for videos with a live demo | [references/06-phase5-demo-pack.md](references/06-phase5-demo-pack.md) |

## Data Sources

The multi-platform analysis uses these APIs (all free tiers, no API keys needed except YouTube):

| Source | API | Key Required |
|--------|-----|-------------|
| YouTube | Data API v3 (reuses OAuth from project) | Yes (already configured) |
| Reddit | PRAW | No (read-only public data suffices) |
| Hacker News | Algolia Search API | No |
| GitHub | Trending page scraper | No |
| Google Trends | Pytrends | No |

## Backend Helper

All data-fetching goes through the standalone helper script bundled with this skill:
```
/opt/homebrew/bin/python3.13 ~/.claude/skills/youtube-strategy/youtube_strategy.py <command> [args]
```

The script has zero project dependencies. It reads YouTube OAuth from `~/.config/yt_post_production/yt_token.json` (shared token) and calls Claude via the local `claude` CLI binary.

Available commands:
- `search-youtube "<query>"` -- Search YouTube for videos in the niche
- `channel-stats <channel_id>` -- Get channel subscriber/avg-view data
- `search-reddit "<query>"` -- Search Reddit for trending topics
- `search-hn "<query>"` -- Search Hacker News Algolia API
- `github-trending` -- Get GitHub trending repos (AI/ML focused)
- `google-trends "<keyword>"` -- Get Google Trends interest over time
- `score-topics "<json_topics>"` -- Score topics using Claude (1-100 virality score)
- `generate-titles "<topic>" "<angle>"` -- Generate SEO title variants

## Workflow Sequence

When the user asks to run the full strategy, execute phases in order:

1. **Ask clarifying questions first:**
   - What's the current content focus? (specific AI topic, tool, or trend?)
   - Target video length? (10min, 20min, 30min+?)
   - Any specific competitors or channels to analyze?
   - Upcoming video or just research?

2. **Run Fundament (Topic Research)** -- read [references/01-fundament-topic-research.md](references/01-fundament-topic-research.md)
   - Use `claude` CLI to generate 10 topic ideas
   - Score each on: search demand, competition, trend direction, emotional hook potential, uniqueness
   - Present top 3 with scores >=80

3. **Let the user pick a topic**, then continue.

4. **Run Phase 1 (Competitive Analysis)** -- read [references/02-phase1-competitive-analysis.md](references/02-phase1-competitive-analysis.md)
   - Search YouTube for the topic -> find outlier videos (5x channel avg views)
   - Search Reddit, HN, GitHub for related trending discussions
   - Extract patterns: length, hook style, thumbnail approach, emotional triggers
   - Present a pattern report

5. **Run Phase 2 (SEO & Metadata)** -- read [references/03-phase2-seo-metadata.md](references/03-phase2-seo-metadata.md)
   - Generate 3 title variants (click-optimized, search-optimized, hybrid)
   - Write full YouTube description with chapter markers
   - Generate 20-30 tags
   - **Note:** The cross-check against spoken content happens later (after the telepro-script exists -- see step 8)

6. **Run Phase 3 (Retention Script)** -- read [references/04-phase3-retention-script.md](references/04-phase3-retention-script.md)
   - Generate a retention-optimized script **directly in TelePro markdown format**
   - Include: PAS hook, rehooks every 60-90s, open loops, pattern interrupts, Key Takeaways, CTA
   - Output saved as `<topic-slug>/telepro-script.md` — ready for TelePro editor, no conversion needed

7. **Re-run Phase 2 cross-check** against `telepro-script.md`
   - Use the spoken lines in `telepro-script.md` as the proxy transcript
   - Run the metadata-vs-spoken-content validation prompt from Phase 2 Step 5
   - Fix any CRITICAL or WARNING mismatches in title, description, tags, or chapters

8. **Run Phase 4 (A/B Testing)** -- read [references/05-phase4-ab-testing.md](references/05-phase4-ab-testing.md)
   - Generate 3 title angles: curiosity, fear/pain, specific result
   - Create thumbnail briefing for each angle
   - Provide A/B test setup instructions for YouTube

9. **Run Phase 5 (Demo Pack) if applicable** -- read [references/06-phase5-demo-pack.md](references/06-phase5-demo-pack.md)
   - **Trigger check:** After finishing Phase 3, scan `telepro-script.md` for demo markers:
     - Any `[IMG:DEMO_...]` placeholder, or
     - Script sections describing a live tool interaction (e.g. „ich zeige live", „ich öffne jetzt", „Demo:", „Claude generiert")
   - If at least one demo marker is found, ask: **„Das Script enthält eine Live-Demo. Soll ich ein Demo-Pack erstellen? (Phase 5)"**
   - On YES: generate `demo-setup.md` + `demo-pack.md` per the reference file instructions
   - On NO: skip Phase 5 entirely

## Integration with youtube-production

The youtube-strategy skill feeds into the youtube-production pipeline:

1. **Phase 3 (Retention Script)** outputs `telepro-script.md` directly in TelePro markdown format.
   No conversion step needed — the file is ready for the TelePro editor immediately.

2. **Phase 2 (SEO & Metadata)** cross-check uses `telepro-script.md` as the proxy transcript.
   Spoken lines in the file validate metadata against actual spoken words **before filming**,
   catching clickbait mismatches early.

3. **Phase 4 (A/B Testing)** thumbnail briefings feed into the production pipeline's
   thumbnail creation process (see `youtube-production` skill references).

### Practical Execution Order

```
Fundament (Topic Research)
  -> Phase 1 (Competitive Analysis)
  -> Phase 2 (SEO & Metadata) -- generate initial titles, description, tags, chapters
  -> Phase 3 (Retention Script) -- outputs telepro-script.md directly (TelePro-ready)
     -> Demo markers found? Ask user → Phase 5 (Demo Pack) if YES
  -> Phase 2 cross-check re-run with telepro-script.md as proxy transcript
  -> Phase 4 (A/B Testing)
  -> Phase 5 (Demo Pack) -- demo-setup.md + demo-pack.md [only if demo video]
```

## Output Format

After running the full workflow, save results to a directory named after the video topic (short slug, kebab-case) in the current project. Derive the slug from the chosen title or topic — e.g. topic "Claude Code als KI-Assistent" → `claude-code-ki-assistent/`. Never use the generic name `youtube-strategy/`.
```
<topic-slug>/
├── topic-research.md          # Fundament output
├── competitive-analysis.md    # Phase 1 output
├── seo-metadata.md            # Phase 2 output
├── telepro-script.md          # Phase 3 output — TelePro-ready, direct to editor
├── ab-testing.md              # Phase 4 output (variants + briefings)
├── demo-setup.md              # Phase 5 output — test data & connector setup guide [demo videos only]
├── demo-pack.md               # Phase 5 output — shooting day prompts, choreography, fallbacks [demo videos only]
└── test-data/                 # Phase 5 output — ready-to-use demo files (copy directly, no typing) [demo videos only]
    ├── <source-files>         #   Python/JS/config files for the demo project
    ├── <import-files>         #   CSVs/Excel for external services (if applicable)
    └── demo-projekt-anleitung.md  #   Step-by-step copy guide with validation checklist
```

## Key Principles

- **The algorithm rewards watch time above all** -- aim for 50-60% average view duration, 70%+ for priority suggested placement
- **33% of viewers leave in the first 30 seconds** if bored -- the hook is everything
- **YouTube 2026 NLP analyzes spoken words** against metadata -- no clickbait mismatches
- **Intent-specific language** > keyword stuffing -- tell the algorithm which audience cluster
- **Start with high-probability topics** -- perfect optimization on a topic nobody searches for is useless
