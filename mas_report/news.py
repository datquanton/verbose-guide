"""Pull a short market recap from financial RSS feeds.

Returns a few recent headline+summary items for the session date. These are
fed to the narrative step as raw material for the 'market drivers' sentences;
they are NOT pasted verbatim into the report.
"""

from __future__ import annotations

import datetime as dt
from typing import List

from .config import NEWS_FEEDS


def fetch_headlines(session_date: str, max_items: int = 8) -> List[dict]:
    import feedparser

    target = dt.date.fromisoformat(session_date)
    items: List[dict] = []
    for url in NEWS_FEEDS:
        feed = feedparser.parse(url)
        for e in feed.entries:
            published = None
            if getattr(e, "published_parsed", None):
                published = dt.date(*e.published_parsed[:3])
            # keep same-day (or undated) market items
            if published is None or published == target:
                items.append({
                    "title": e.get("title", "").strip(),
                    "summary": e.get("summary", "").strip(),
                    "published": published.isoformat() if published else None,
                })
    return items[:max_items]


def headlines_as_text(items: List[dict]) -> str:
    return "\n".join(f"- {it['title']}" for it in items if it.get("title"))
