"""Quantitative profile of how Memeburn currently produces news, from data/memeburn/archive.json.

Output: knowledge/stats.json. Claude reads this (plus SOPs in knowledge/process/) during /learn-process
and writes the human-readable knowledge/editorial_profile.md.
"""
from __future__ import annotations

import re
import statistics
from collections import Counter

from common import DATA, KNOWLEDGE, TZ, now_utc, parse_date, read_json, write_json


def headline_patterns(title: str) -> list[str]:
    t = title.lower()
    pats = []
    if re.match(r"^\d", t) or re.search(r"\b\d+ (ways|things|best|reasons|tips|apps|phones)\b", t):
        pats.append("number/listicle")
    if t.endswith("?") or re.match(r"^(is|are|can|should|will|does|do|why|what|how)\b", t):
        pats.append("question")
    if "how to" in t:
        pats.append("how-to")
    if re.search(r"\bvs\.?\b|versus", t):
        pats.append("comparison")
    if re.search(r"south africa|\bsa\b|mzansi|rand\b|\br\d", t):
        pats.append("sa-localised")
    if re.search(r"price|cost|cheap|deal|specials?|launch", t):
        pats.append("price/launch")
    if ":" in t or " – " in title or " - " in title:
        pats.append("colon/split")
    if re.search(r"\b(here'?s|this is|everything you need)", t):
        pats.append("explainer-hook")
    return pats or ["straight-news"]


def main():
    data = read_json(DATA / "memeburn" / "archive.json")
    if not data or not data.get("posts"):
        raise SystemExit("Run: python scripts/fetch_memeburn.py --days 90 --with-content --out data/memeburn/archive.json")
    posts = data["posts"]
    n = len(posts)
    local = [parse_date(p["date"]).astimezone(TZ) for p in posts if parse_date(p.get("date"))]
    words = [p["word_count"] for p in posts if p.get("word_count")]
    titles = [p["title"] for p in posts]
    days = max(1, data.get("days", 90))

    stats = {
        "generated_at": now_utc().isoformat(),
        "source_method": data.get("method"),
        "window_days": days,
        "post_count": n,
        "posts_per_day": round(n / days, 1),
        "categories": Counter(c for p in posts for c in p.get("categories", [])).most_common(25),
        "top_tags": Counter(t for p in posts for t in p.get("tags", [])).most_common(50),
        "authors": Counter(p.get("author") or "?" for p in posts).most_common(20),
        "author_categories": {
            a: Counter(c for p in posts if p.get("author") == a for c in p.get("categories", [])).most_common(5)
            for a, _ in Counter(p.get("author") for p in posts).most_common(10) if a
        },
        "publish_hour_local": sorted(Counter(d.hour for d in local).items()),
        "publish_weekday": Counter(d.strftime("%a") for d in local).most_common(),
        "word_count": {
            "median": statistics.median(words) if words else None,
            "p25": statistics.quantiles(words, n=4)[0] if len(words) > 4 else None,
            "p75": statistics.quantiles(words, n=4)[2] if len(words) > 4 else None,
        },
        "avg_h2": round(statistics.mean(p.get("h2_count", 0) for p in posts), 1) if words else None,
        "avg_images": round(statistics.mean(p.get("image_count", 0) for p in posts), 1) if words else None,
        "headline": {
            "median_chars": statistics.median(len(t) for t in titles) if titles else None,
            "patterns": Counter(pt for t in titles for pt in headline_patterns(t)).most_common(),
        },
        "top_outbound_sources": Counter(d for p in posts for d in p.get("outbound_domains", [])).most_common(40),
        "sample_headlines": titles[:60],
        "sample_openings": [{"title": p["title"], "opening": p.get("opening", "")} for p in posts[:15]],
    }
    write_json(KNOWLEDGE / "stats.json", stats)
    print(f"[learn] profiled {n} posts ({stats['posts_per_day']}/day) -> knowledge/stats.json")


if __name__ == "__main__":
    main()
