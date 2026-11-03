"""Turn raw crawl items into pre-scored topic clusters for Claude to review.

Reads : data/raw/<date>.json, data/memeburn/recent.json, data/briefs/*.json (recent)
Writes: data/candidates/<date>.json

The pre-score is a cheap, transparent heuristic so Claude doesn't wade through 500 headlines.
Claude makes the editorial decision; the score breakdown is kept so it can disagree with it.
"""
from __future__ import annotations

import argparse
import datetime as dt
import math

from common import (
    DATA, SETTINGS, keyword_hits, load_yaml, now_utc, parse_date, read_json, similar, today_str, tokens, write_json,
)

TOPICS = load_yaml("topics.yaml")
CATEGORIES: dict[str, list[str]] = TOPICS["categories"]


def classify(text: str, hint: str | None) -> tuple[str, dict]:
    hits = {cat: keyword_hits(text, kws) for cat, kws in CATEGORIES.items()}
    scores = {cat: len(h) for cat, h in hits.items()}
    if hint in scores:
        scores[hint] += 0.5
    best = max(scores, key=scores.get)
    return (best if scores[best] > 0 else "other"), {k: v for k, v in hits.items() if v}


def cluster(items: list[dict]) -> list[list[dict]]:
    # strongest signals first so they become cluster "heads"
    items = sorted(items, key=item_strength, reverse=True)
    clusters: list[dict] = []  # each: {"items": [...]}, first item is the head
    for it in items:
        toks = tokens(f"{it['title']} {it.get('summary', '')[:120]}")
        it["_tokens"] = toks
        for c in clusters:
            if any(similar(toks, m["_tokens"]) for m in c["items"]):
                c["items"].append(it)
                break
        else:
            clusters.append({"items": [it]})
    return [c["items"] for c in clusters]


def item_strength(it: dict) -> float:
    s = it.get("signal", {})
    return (
        math.log10(s.get("trends_traffic", 0) + 1) * 3
        + math.log10(s.get("hn_points", 0) + 1) * 2
        + math.log10(s.get("reddit_score", 0) + 1) * 2
        + (11 - s["coingecko_rank"] if s.get("coingecko_rank") else 0)
        + 1
    )


def score_cluster(items, category, covered, suggested_before, now) -> tuple[float, dict]:
    sources = {i["source"] for i in items}
    sig = {
        "trends_traffic": max((i["signal"].get("trends_traffic", 0) for i in items), default=0),
        "hn_points": max((i["signal"].get("hn_points", 0) for i in items), default=0),
        "reddit_score": max((i["signal"].get("reddit_score", 0) for i in items), default=0),
        "coingecko_rank": min((i["signal"]["coingecko_rank"] for i in items if i["signal"].get("coingecko_rank")), default=None),
    }
    times = [parse_date(i["published"]) for i in items if i.get("published")]
    newest_h = min(((now - t).total_seconds() / 3600 for t in times if t), default=12)

    b = {
        "source_diversity": 10 * min(len(sources), 5),          # same story on many outlets = it's big
        "search_demand": min(25, 12 * math.log10(sig["trends_traffic"] / 1000 + 1)) if sig["trends_traffic"] else 0,
        "community_buzz": min(10, sig["hn_points"] / 60) + min(10, sig["reddit_score"] / 800),
        "crypto_trending": (11 - sig["coingecko_rank"]) if sig["coingecko_rank"] else 0,
        "freshness": max(0.0, 15 - newest_h / 2),
        "beat_fit": 10 if category != "other" else -20,
        "already_covered_by_memeburn": -30 if covered else 0,
        "suggested_recently": -15 if suggested_before else 0,
    }
    total = max(0.0, min(100.0, sum(b.values())))
    return round(total, 1), {k: round(v, 1) for k, v in b.items()} | {"signals": sig, "newest_hours": round(newest_h, 1)}


def recent_brief_topics(days: int, today: str) -> list[dict]:
    out = []
    cutoff = dt.date.fromisoformat(today) - dt.timedelta(days=days)
    for path in sorted((DATA / "briefs").glob("*.json")):
        try:
            d = dt.date.fromisoformat(path.stem)
        except ValueError:
            continue
        if cutoff <= d < dt.date.fromisoformat(today):
            for t in (read_json(path, {}) or {}).get("topics", []):
                text = " ".join([t.get("working_title", "")] + t.get("seo_keywords", []))
                out.append({"date": path.stem, "title": t.get("working_title", ""), "tokens": tokens(text)})
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", default=today_str())
    args = parser.parse_args()

    raw = read_json(DATA / "raw" / f"{args.date}.json")
    if not raw:
        raise SystemExit(f"No crawl for {args.date}. Run scripts/crawl_trends.py first.")
    now = now_utc()
    max_age = dt.timedelta(hours=SETTINGS.get("freshness_hours", 48))

    items = []
    for it in raw["items"]:
        pub = parse_date(it.get("published"))
        if pub and now - pub > max_age:
            continue
        items.append(it)

    mb = read_json(DATA / "memeburn" / "recent.json", {"posts": []})
    cov_cutoff = now - dt.timedelta(days=SETTINGS["memeburn"].get("coverage_lookback_days", 3))
    mb_posts = [
        {**p, "tokens": tokens(p["title"])}
        for p in mb["posts"]
        if (parse_date(p.get("date")) or now) >= cov_cutoff
    ]
    past = recent_brief_topics(SETTINGS.get("dedupe_lookback_days", 3), args.date)

    candidates = []
    for group in cluster(items):
        head = group[0]
        text = " ".join(f"{i['title']} {i.get('summary', '')}" for i in group)
        hint = next((i["category_hint"] for i in group if i.get("category_hint")), None)
        category, cat_hits = classify(text, hint)
        toks = set().union(*(i["_tokens"] for i in group))
        covered = [{"title": p["title"], "url": p["url"], "date": p["date"]} for p in mb_posts if similar(toks, p["tokens"], 0.2)]
        before = [{"date": b["date"], "title": b["title"]} for b in past if similar(toks, b["tokens"], 0.2)]
        score, breakdown = score_cluster(group, category, covered, before, now)
        candidates.append(
            {
                "title": head["title"],
                "category": category,
                "prescore": score,
                "score_breakdown": breakdown,
                "category_keyword_hits": cat_hits,
                "memeburn_recent_similar": covered[:3],
                "suggested_in_recent_briefs": before[:3],
                "source_count": len({i["source"] for i in group}),
                "items": [
                    {k: i[k] for k in ("source", "title", "url", "published", "summary", "signal")}
                    for i in group[:8]
                ],
            }
        )

    candidates.sort(key=lambda c: c["prescore"], reverse=True)
    candidates = candidates[: SETTINGS.get("max_candidates", 60)]
    for n, c in enumerate(candidates, start=1):
        c["id"] = f"c{n:02d}"

    out = DATA / "candidates" / f"{args.date}.json"
    write_json(out, {
        "date": args.date,
        "generated_at": now.isoformat(),
        "crawl_errors": raw.get("errors", []),
        "candidate_count": len(candidates),
        "candidates": candidates,
    })
    by_cat = {}
    for c in candidates:
        by_cat[c["category"]] = by_cat.get(c["category"], 0) + 1
    print(f"[candidates] {len(items)} fresh items -> {len(candidates)} clusters {by_cat} -> {out}")


if __name__ == "__main__":
    main()
