# Fundament: Topic Research

Generate and score video topic ideas for the user's niche: **AI, Agentic Coding, Developer Tools** (German-language YouTube).

## Goal

Find 10 high-probability video topics. A topic is "high-probability" when it has:
- Clear search demand (people are actively looking for this)
- Manageable competition (not dominated by huge English channels)
- Strong emotional hook potential (curiosity, fear of missing out, specific result)
- Uniqueness angle (why YOU specifically should make this)

## Process

### Step 1: Understand the Current Context

Ask the user (if not already known):
- Any specific sub-topic focus? (e.g., Claude Code, n8n, AI agents, voice agents, Firecrawl, OpenSpec?)
- Recent videos they've published? (to avoid repeats and build clusters)
- Upcoming product launches or events to align with?

### Step 2: Brainstorm with Claude

Use the `claude` CLI to generate 10 topic ideas. Craft a prompt that asks Claude to:

```
You are a YouTube content strategist for a German-language channel about AI,
Agentic Coding, and Developer Tools. The audience is German-speaking developers,
tech leads, and AI enthusiasts.

Generate 10 video topic ideas that:
1. Address a specific pain point or question German developers actually have
2. Have search demand (people Google/YouTube-search this)
3. Are NOT generic AI news — they teach something actionable
4. Can be 15-25 minutes long
5. Have a strong emotional hook (curiosity gap, fear of missing out, or specific result promise)

For each idea, provide:
- Working title (in German)
- One-sentence description
- The core emotional hook
- Why it would outperform generic AI content
- Estimated search demand: high/medium/low
- Competition level: high/medium/low
```

### Step 3: Score Each Topic

Rate each of the 10 topics on a 1-100 "virality score" using these criteria:

| Criterion | Weight | What to evaluate |
|-----------|--------|-----------------|
| Search Demand | 25% | Are people actively searching for this? Check Google Trends if available. |
| Emotional Hook | 25% | Does it trigger curiosity, FOMO, or promise a specific result? |
| Uniqueness | 20% | Is this angle different from what's already on YouTube? |
| Competition Gap | 15% | Is the competition weak or in English only? (German advantage) |
| Trend Direction | 15% | Is interest in this topic rising or falling? |

Score each 1-100, then compute the weighted total.

### Step 4: Present Top Candidates

Present the top 3-5 topics that scored ≥80. Format:

```markdown
## Top Topic Candidates

### 🥇 [Score: 92] "Exakter Titel auf Deutsch"
**Hook:** [Emotional trigger description]
**Search:** [Demand estimate] | **Competition:** [Level] | **Trend:** [Direction]
**Why this wins:** [1-2 sentences]
**Suggested format:** Tutorial / Deep Dive / Tool Review / News Analysis
```

Ask the user to pick one, or refine. The chosen topic becomes the input for Phase 1 (Competitive Analysis).

## Success Criteria

- [ ] 10 topics generated with working German titles
- [ ] All topics scored on the 5-factor model
- [ ] Top 3 presented with scores ≥80
- [ ] User has selected a topic for Phase 1 (Competitive Analysis)
- [ ] Results saved to `youtube-strategy/topic-research.md`
