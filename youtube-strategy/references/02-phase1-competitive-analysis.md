# Phase 1: Competitive Analysis

Multi-platform search for outlier content. Find what's ALREADY working in the AI/DevTools niche
so you can pattern-match success instead of guessing.

## Goal

Identify videos and posts in the niche that significantly outperformed their channel/community average
in the last 30-90 days. Extract the patterns that made them work: hooks, length, structure, emotional
triggers, thumbnail style.

## Data Sources

We search across multiple platforms to capture the full picture:

### YouTube (Data API v3)
Uses the existing OAuth token from the project. Find videos with 5x+ channel average views.

### Reddit (PRAW / public JSON)
Search r/artificial, r/MachineLearning, r/programming, r/de_EDV, r/selbststaendig.
Look for posts with 3x+ subreddit average upvotes. These signal what topics resonate.

### Hacker News (Algolia API)
Search for AI/Claude Code/devtools posts with 100+ points. HN front-page stories
often predict what YouTube audiences will care about 1-2 weeks later.

### GitHub Trending
AI/ML repos that are spiking — these are content goldmines for tutorial/review videos.

### Google Trends (Pytrends)
Compare search interest for the topic vs. related terms. Rising trends = growing audience.

## Process

### Step 1: Search YouTube for Outlier Videos

Run the Python helper to find top-performing videos:

```bash
cd /Users/a7wwiri/Projects/Video_Post_Production
source .venv/bin/activate
python -m backend.modules.youtube_strategy search-youtube "<topic in German>"
```

This returns videos from the last 30 days. From the results, identify the "outliers" —
videos where views are significantly above the channel's typical view count.

For each outlier, extract:
- Title (exact wording)
- Thumbnail style (face close-up? text overlay? before/after?)
- Video length
- First 30 seconds hook pattern (if transcript available)
- Comment sentiment (what are viewers saying?)

### Step 2: Search Reddit for Trending Discussions

```bash
python -m backend.modules.youtube_strategy search-reddit "<topic keywords>"
```

Identifies Reddit threads with high engagement. Note:
- What specific question or pain point triggered the discussion?
- What solutions/answers got the most upvotes?
- What controversies or debates emerged? (Controversy = engagement)

### Step 3: Search Hacker News

```bash
python -m backend.modules.youtube_strategy search-hn "<topic keywords>"
```

HN is a leading indicator — what's hot on HN today is YouTube content next week.

### Step 4: Check GitHub Trending

```bash
python -m backend.modules.youtube_strategy github-trending
```

New AI tools or frameworks spiking on GitHub are perfect for "first to cover" advantage.

### Step 5: Google Trends Comparison

```bash
python -m backend.modules.youtube_strategy google-trends "<keyword1>,<keyword2>,<keyword3>"
```

Compare the topic against related terms. Rising trends = growing search volume.

### Step 6: Synthesize the Pattern Report

After collecting data from all platforms, create a pattern report:

```markdown
## Competitive Analysis: [Topic]

### YouTube Outliers (last 30 days)
| Video Title | Channel | Views vs Avg | Length | Hook Type |
|------------|---------|-------------|--------|-----------|
| ... | ... | 5.2x | 18min | Curiosity gap |

### Cross-Platform Signals
- **Reddit:** [Top threads and what they reveal about audience interest]
- **Hacker News:** [Recent front-page stories in this space]
- **GitHub:** [Trending repos that could be video material]
- **Google Trends:** [Interest trajectory — rising/falling/stable]

### Pattern Extraction
1. **Hook patterns:** [What first-30s approaches do top videos use?]
2. **Ideal length:** [What length correlates with high retention?]
3. **Thumbnail patterns:** [Face? Text? Color palette?]
4. **Title patterns:** [List format? How-to? Challenge? News?]
5. **Emotional triggers:** [Curiosity? Fear? Specific result? Urgency?]

### Strategic Implications
- [What this means for our video]
- [What to copy / what to differentiate on]
- [Content gaps nobody is filling]
```

## Success Criteria

- [ ] YouTube outlier analysis completed (minimum 3 outlier videos identified)
- [ ] Reddit, HN, GitHub data collected
- [ ] Google Trends comparison done
- [ ] Pattern report written with actionable insights
- [ ] Clear recommendation: what patterns to apply, what gaps to fill
- [ ] Results saved to `youtube-strategy/competitive-analysis.md`
