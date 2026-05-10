"""YouTube Strategy Helper — standalone, zero project dependencies.

Callable from any directory:
    python ~/.claude/skills/youtube-strategy/youtube_strategy.py <command> [args]

Commands:
    search-youtube "<query>"           Search YouTube via Data API v3
    channel-stats <channel_id>         Get channel avg-view baseline
    search-reddit "<query>"            Search Reddit via public JSON
    search-hn "<query>"                Search Hacker News via Algolia
    github-trending                    GitHub trending repos (AI/ML filtered)
    google-trends "<kw1>,<kw2>"        Google Trends interest over time
    score-topics "<json>"              Score topics via Claude (1-100)
    generate-titles "<topic>" "<angle>" Generate SEO title variants

YouTube auth: reads ~/.config/yt_post_production/yt_token.json (shared with Video_Post_Production).
Claude calls: uses the `claude` CLI binary (Claude Max, zero API cost).
"""

from __future__ import annotations

import json
import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# ── YouTube OAuth (reads shared token, no project dependency) ────────────────

_YT_CONFIG_DIR = Path.home() / ".config" / "yt_post_production"
_YT_TOKEN_PATH = _YT_CONFIG_DIR / "yt_token.json"
_YT_CLIENT_SECRET_PATH = _YT_CONFIG_DIR / "client_secret.json"

_YT_SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl",
]


def _load_yt_credentials():
    """Load stored OAuth token, refresh if expired."""
    if not _YT_TOKEN_PATH.exists():
        raise RuntimeError(
            f"YouTube-Token nicht gefunden: {_YT_TOKEN_PATH}\n"
            "Bitte zuerst in Video_Post_Production authentifizieren."
        )
    try:
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
        creds = Credentials.from_authorized_user_file(str(_YT_TOKEN_PATH), _YT_SCOPES)
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            _YT_TOKEN_PATH.write_text(creds.to_json(), encoding="utf-8")
        return creds
    except ImportError:
        raise RuntimeError(
            "google-auth nicht installiert. "
            "pip install google-auth google-auth-oauthlib google-api-python-client"
        )


def _get_youtube_client():
    from googleapiclient.discovery import build
    creds = _load_yt_credentials()
    return build("youtube", "v3", credentials=creds)


# ── Claude CLI call (zero API cost via Claude Max) ───────────────────────────

def _call_claude(system: str, prompt: str) -> str:
    """Call Claude via the `claude` CLI. Falls back to ANTHROPIC_API_KEY if CLI not found."""
    claude_bin = _find_claude_bin()
    if claude_bin:
        result = subprocess.run(
            [claude_bin, "--print", "--system", system, prompt],
            capture_output=True, text=True, timeout=60,
        )
        if result.returncode == 0:
            return result.stdout.strip()
        raise RuntimeError(f"claude CLI error: {result.stderr[:300]}")

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if api_key:
        return _call_claude_api(system, prompt, api_key)

    raise RuntimeError(
        "Claude CLI not found and ANTHROPIC_API_KEY not set. "
        "Install Claude Code or set ANTHROPIC_API_KEY."
    )


def _find_claude_bin() -> str | None:
    """Locate the claude CLI binary."""
    candidates = [
        os.path.expanduser("~/.local/bin/claude"),
        "/usr/local/bin/claude",
        "/opt/homebrew/bin/claude",
    ]
    for path in candidates:
        if os.path.isfile(path):
            return path
    # Try PATH
    result = subprocess.run(["which", "claude"], capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip()
    return None


def _call_claude_api(system: str, prompt: str, api_key: str) -> str:
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        msg = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2048,
            system=system,
            messages=[{"role": "user", "content": prompt}],
        )
        return msg.content[0].text
    except ImportError:
        raise RuntimeError("anthropic SDK not installed. pip install anthropic")


# ── YouTube search ───────────────────────────────────────────────────────────

def search_youtube(query: str, max_results: int = 20, days_back: int = 30) -> list[dict]:
    from datetime import datetime, timedelta, timezone
    youtube = _get_youtube_client()
    published_after = (datetime.now(timezone.utc) - timedelta(days=days_back)).isoformat()

    results: list[dict] = []
    page_token = None

    while len(results) < max_results:
        resp = youtube.search().list(
            part="snippet",
            q=query,
            type="video",
            maxResults=min(50, max_results - len(results)),
            order="viewCount",
            publishedAfter=published_after,
            relevanceLanguage="de",
            pageToken=page_token,
        ).execute()

        video_ids = [item["id"]["videoId"] for item in resp.get("items", [])]
        if not video_ids:
            break

        stats_resp = youtube.videos().list(
            part="statistics",
            id=",".join(video_ids),
        ).execute()

        stats_map: dict[str, dict] = {
            v["id"]: {
                "views": int(v["statistics"].get("viewCount", 0)),
                "likes": int(v["statistics"].get("likeCount", 0)),
                "comments": int(v["statistics"].get("commentCount", 0)),
            }
            for v in stats_resp.get("items", [])
        }

        for item in resp.get("items", []):
            vid = item["id"]["videoId"]
            snippet = item["snippet"]
            results.append({
                "video_id": vid,
                "title": snippet["title"],
                "channel_id": snippet["channelId"],
                "channel_title": snippet["channelTitle"],
                "published_at": snippet["publishedAt"],
                "description": snippet["description"][:300],
                "thumbnail": snippet["thumbnails"]["high"]["url"],
                **stats_map.get(vid, {"views": 0, "likes": 0, "comments": 0}),
                "url": f"https://youtube.com/watch?v={vid}",
            })

        page_token = resp.get("nextPageToken")
        if not page_token:
            break

    return results


def channel_stats(channel_id: str) -> dict:
    youtube = _get_youtube_client()
    resp = youtube.channels().list(part="statistics,snippet", id=channel_id).execute()
    if not resp.get("items"):
        return {"error": f"Channel {channel_id} nicht gefunden"}
    item = resp["items"][0]
    stats = item["statistics"]
    sub_count = int(stats.get("subscriberCount", 0))
    view_count = int(stats.get("viewCount", 0))
    video_count = int(stats.get("videoCount", 0))
    return {
        "channel_id": channel_id,
        "title": item["snippet"]["title"],
        "subscribers": sub_count,
        "total_views": view_count,
        "video_count": video_count,
        "avg_views_per_video": round(view_count / video_count) if video_count else 0,
    }


# ── Reddit (public JSON, no auth) ────────────────────────────────────────────

REDDIT_SUBREDDITS = [
    "artificial", "MachineLearning", "programming",
    "de_EDV", "selbststaendig", "ChatGPT", "ClaudeAI", "LocalLLaMA",
]


def search_reddit(query: str, limit: int = 30) -> list[dict]:
    import urllib.request
    import urllib.parse

    all_posts: list[dict] = []
    per_sub = max(1, limit // len(REDDIT_SUBREDDITS) + 1)

    for subreddit in REDDIT_SUBREDDITS:
        try:
            url = (
                f"https://www.reddit.com/r/{subreddit}/search.json"
                f"?q={urllib.parse.quote(query)}&sort=relevance&limit={per_sub}&restrict_sr=on"
            )
            req = urllib.request.Request(url, headers={"User-Agent": "youtube-strategy-skill/1.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read())
            for post in data.get("data", {}).get("children", []):
                p = post["data"]
                all_posts.append({
                    "subreddit": p["subreddit"],
                    "title": p["title"],
                    "score": p["score"],
                    "num_comments": p["num_comments"],
                    "url": f"https://reddit.com{p['permalink']}",
                    "created_utc": p["created_utc"],
                })
        except Exception as e:
            logger.debug("Reddit r/%s failed: %s", subreddit, e)

    all_posts.sort(key=lambda x: x["score"], reverse=True)
    return all_posts[:limit]


# ── Hacker News (Algolia API, no auth) ──────────────────────────────────────

def search_hn(query: str, limit: int = 30) -> list[dict]:
    import urllib.request
    import urllib.parse

    url = (
        f"https://hn.algolia.com/api/v1/search"
        f"?query={urllib.parse.quote(query)}&tags=story&hitsPerPage={limit}"
    )
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "youtube-strategy-skill/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
    except Exception as e:
        logger.error("HN search failed: %s", e)
        return []

    return [
        {
            "title": hit.get("title", ""),
            "url": hit.get("url") or f"https://news.ycombinator.com/item?id={hit['objectID']}",
            "points": hit.get("points", 0),
            "num_comments": hit.get("num_comments", 0),
            "created_at": hit.get("created_at", ""),
            "author": hit.get("author", ""),
        }
        for hit in data.get("hits", [])
    ]


# ── GitHub Trending ──────────────────────────────────────────────────────────

_AI_KEYWORDS = [
    "ai", "llm", "gpt", "claude", "agent", "ml", "machine-learning",
    "nlp", "transformer", "diffusion", "rag", "embedding", "vector",
    "langchain", "llama", "mistral", "anthropic", "openai", "copilot",
    "mcp", "tool-use", "function-call", "autogen", "crewai",
]


def github_trending(lang: str = "") -> list[dict]:
    import urllib.request
    import re

    results: list[dict] = []
    languages = [lang] if lang else ["python", "typescript", "jupyter-notebook", "rust"]

    for language in languages:
        try:
            url = f"https://github.com/trending/{urllib.request.quote(language)}?since=weekly"
            req = urllib.request.Request(url, headers={"User-Agent": "youtube-strategy-skill/1.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                html = resp.read().decode()
        except Exception as e:
            logger.debug("GitHub trending failed for %s: %s", language, e)
            continue

        repo_blocks = re.findall(
            r'<h2[^>]*class="[^"]*h3[^"]*lh-condensed[^"]*"[^>]*>.*?<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>.*?</h2>.*?<p[^>]*class="[^"]*col-9[^"]*"[^>]*>(.*?)</p>',
            html, re.DOTALL,
        )
        for path, _name_html, desc in repo_blocks:
            repo_name = path.strip().strip("/")
            desc_clean = re.sub(r"<[^>]+>", "", desc).strip()
            combined = f"{repo_name} {desc_clean}".lower()
            if lang or any(kw in combined for kw in _AI_KEYWORDS):
                results.append({
                    "repo": repo_name,
                    "url": f"https://github.com/{repo_name}",
                    "description": desc_clean[:200],
                    "language": language,
                })

    return results[:30]


# ── Google Trends ────────────────────────────────────────────────────────────

def google_trends(keywords: str, timeframe: str = "today 3-m") -> dict:
    try:
        from pytrends.request import TrendReq
    except ImportError:
        return {"error": "pytrends nicht installiert. pip install pytrends"}

    kw_list = [k.strip() for k in keywords.split(",") if k.strip()]
    if not kw_list:
        return {"error": "Keine Keywords angegeben"}

    try:
        pytrends = TrendReq(hl="de-DE", tz=120)
        pytrends.build_payload(kw_list, timeframe=timeframe)
        interest = pytrends.interest_over_time()
        if interest.empty:
            return {"error": "Keine Daten von Google Trends", "keywords": kw_list}
        return {
            "keywords": kw_list,
            "latest": {kw: int(interest[kw].iloc[-1]) for kw in kw_list if kw in interest.columns},
            "average": {kw: round(float(interest[kw].mean()), 1) for kw in kw_list if kw in interest.columns},
        }
    except Exception as e:
        return {"error": str(e), "keywords": kw_list}


# ── Claude-powered helpers ───────────────────────────────────────────────────

def score_topics(topics_json: str) -> list[dict]:
    try:
        topics = json.loads(topics_json)
    except json.JSONDecodeError:
        return [{"error": 'Ungültiges JSON. Format: [{"title": "...", "description": "..."}]'}]

    system = (
        "Du bist ein YouTube-Content-Stratege für einen deutschsprachigen Kanal "
        "über KI, agentisches Coding und Developer Tools. Zielgruppe: deutschsprachige "
        "Entwickler und Tech-Enthusiasten. Bewerte jedes Topic auf einer Skala von 1-100 "
        "nach diesen Kriterien:\n"
        "- Search Demand (25%): Wie aktiv suchen Leute danach?\n"
        "- Emotional Hook Potential (25%): Neugier, FOMO, konkretes Ergebnis\n"
        "- Uniqueness (20%): Anderer Winkel als was es schon gibt\n"
        "- Competition Gap (15%): Schwache Konkurrenz oder nur englisch?\n"
        "- Trend Direction (15%): Steigendes oder fallendes Interesse?\n\n"
        'Antworte NUR mit JSON: [{"title": "...", "score": 85, '
        '"breakdown": {"search": 90, "hook": 80, "unique": 85, '
        '"competition": 75, "trend": 90}, "why": "1 Satz"}]'
    )
    response = _call_claude(system, f"Bewerte diese Video-Topics:\n{json.dumps(topics, ensure_ascii=False, indent=2)}")
    return _parse_json_response(response)


def generate_titles(topic: str, angle: str = "all") -> dict:
    system = (
        "Du bist ein YouTube-SEO-Experte für einen deutschsprachigen Kanal "
        "über KI, agentisches Coding und Developer Tools.\n"
        "Generiere Titel-Varianten. Jeder Titel max. 60 Zeichen.\n"
        "Antworte NUR mit JSON."
    )
    prompts = {
        "click": (
            f"Generiere 3 Click-optimierte Titel für: {topic}\n"
            'Format: {"click_titles": [{"title": "...", "trigger": "curiosity/fear/result"}]}'
        ),
        "search": (
            f"Generiere 3 Search-optimierte Titel für: {topic}\n"
            'Format: {"search_titles": [{"title": "...", "target_keyword": "..."}]}'
        ),
        "hybrid": (
            f"Generiere 3 Hybrid-Titel für: {topic}\n"
            'Format: {"hybrid_titles": [{"title": "..."}]}'
        ),
    }
    if angle == "all":
        result = {}
        for a, prompt in prompts.items():
            result.update(_parse_json_response(_call_claude(system, prompt)))
        return result
    if angle not in prompts:
        return {"error": f"Unbekannter Angle: {angle}. Erwartet: click, search, hybrid, all"}
    return _parse_json_response(_call_claude(system, prompts[angle]))


def _parse_json_response(response: str) -> Any:
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        import re
        m = re.search(r"```(?:json)?\s*([\s\S]*?)```", response)
        if m:
            return json.loads(m.group(1))
        return {"error": "Antwort konnte nicht geparst werden", "raw": response[:500]}


# ── CLI entry point ──────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]
    args = sys.argv[2:]

    def out(data):
        print(json.dumps(data, ensure_ascii=False, indent=2))

    try:
        match cmd:
            case "search-youtube":  out(search_youtube(args[0] if args else ""))
            case "channel-stats":   out(channel_stats(args[0] if args else ""))
            case "search-reddit":   out(search_reddit(args[0] if args else ""))
            case "search-hn":       out(search_hn(args[0] if args else ""))
            case "github-trending": out(github_trending(args[0] if args else ""))
            case "google-trends":   out(google_trends(args[0] if args else ""))
            case "score-topics":    out(score_topics(args[0] if args else "[]"))
            case "generate-titles":
                topic = args[0] if args else ""
                angle = args[1] if len(args) > 1 else "all"
                out(generate_titles(topic, angle))
            case _:
                print(f"Unbekanntes Kommando: {cmd}")
                print(__doc__)
                sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
