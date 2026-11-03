"""Fetch Memeburn's own recent articles (what's already been published, by whom, in which category).

Uses the WordPress REST API, falls back to the RSS feed if the API is blocked.
  python scripts/fetch_memeburn.py --days 7                      -> data/memeburn/recent.json
  python scripts/fetch_memeburn.py --days 90 --with-content \
         --out data/memeburn/archive.json                         -> used by /learn-process
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
from urllib.parse import urlparse

import feedparser

from common import DATA, SETTINGS, clean_text, now_utc, parse_date, session, write_json

BASE = SETTINGS["memeburn"]["base_url"].rstrip("/")
SELF_DOMAINS = {urlparse(BASE).netloc, "memeburn.com", "www.memeburn.com"}


def content_stats(html_body: str) -> dict:
    text = clean_text(html_body, limit=10**7)
    links = re.findall(r'href="(https?://[^"]+)"', html_body or "")
    domains = sorted({urlparse(u).netloc.removeprefix("www.") for u in links} - SELF_DOMAINS)
    return {
        "word_count": len(text.split()),
        "h2_count": len(re.findall(r"<h2", html_body or "", re.I)),
        "image_count": len(re.findall(r"<img", html_body or "", re.I)),
        "embed_count": len(re.findall(r"<(iframe|blockquote class=\"(twitter|instagram|tiktok))", html_body or "", re.I)),
        "outbound_domains": domains,
        "opening": text[:300],
    }


def from_wp_api(since: dt.datetime, with_content: bool) -> list[dict]:
    http = session()
    posts, page = [], 1
    while True:
        resp = http.get(
            f"{BASE}/wp-json/wp/v2/posts",
            params={"per_page": 100, "page": page, "after": since.strftime("%Y-%m-%dT%H:%M:%S"), "_embed": "author,wp:term"},
            timeout=40,
        )
        if resp.status_code == 400 and page > 1:  # past the last page
            break
        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            break
        for p in batch:
            emb = p.get("_embedded", {})
            terms = [t for group in emb.get("wp:term", []) for t in group if isinstance(t, dict)]
            post = {
                "id": p["id"],
                "date": p.get("date_gmt", p.get("date")) + "+00:00" if p.get("date_gmt") else p.get("date"),
                "title": clean_text(p.get("title", {}).get("rendered", ""), 300),
                "url": p.get("link"),
                "author": (emb.get("author") or [{}])[0].get("name"),
                "categories": [t["name"] for t in terms if t.get("taxonomy") == "category"],
                "tags": [t["name"] for t in terms if t.get("taxonomy") == "post_tag"],
                "excerpt": clean_text(p.get("excerpt", {}).get("rendered", ""), 300),
            }
            if with_content:
                post.update(content_stats(p.get("content", {}).get("rendered", "")))
            posts.append(post)
        if page >= int(resp.headers.get("X-WP-TotalPages", page)):
            break
        page += 1
    return posts


def from_rss(since: dt.datetime) -> list[dict]:
    resp = session().get(f"{BASE}/feed/", timeout=30)
    resp.raise_for_status()
    feed = feedparser.parse(resp.content)
    posts = []
    for e in feed.entries:
        pub = parse_date(e.get("published_parsed"))
        if pub and pub < since:
            continue
        posts.append(
            {
                "id": e.get("id"),
                "date": pub.isoformat() if pub else None,
                "title": clean_text(e.get("title", ""), 300),
                "url": e.get("link"),
                "author": e.get("author"),
                "categories": [t.get("term") for t in e.get("tags", [])],
                "tags": [],
                "excerpt": clean_text(e.get("summary", ""), 300),
            }
        )
    return posts


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--with-content", action="store_true", help="add word count, structure and outbound sources")
    parser.add_argument("--out", default=str(DATA / "memeburn" / "recent.json"))
    args = parser.parse_args()

    since = now_utc() - dt.timedelta(days=args.days)
    method = "wp-api"
    try:
        posts = from_wp_api(since, args.with_content)
    except Exception as exc:
        print(f"[memeburn] WP API failed ({exc}); falling back to RSS (only ~10-20 latest posts)")
        posts, method = from_rss(since), "rss"

    posts.sort(key=lambda p: p.get("date") or "", reverse=True)
    write_json(args.out, {"fetched_at": now_utc().isoformat(), "method": method, "days": args.days, "posts": posts})
    print(f"[memeburn] {len(posts)} posts from last {args.days} days via {method} -> {args.out}")


if __name__ == "__main__":
    main()
