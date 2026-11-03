"""Close the feedback loop: which suggested topics did writers actually publish, and how did they do?

Matches topics in data/briefs/*.json (last 14 days) against Memeburn posts published on/after the brief date.
If you drop GA4 / Search Console exports into knowledge/performance/*.csv (columns: url,pageviews[,sessions]),
pageviews get attached to matched articles so Claude can learn which kinds of picks actually pull traffic.

Writes data/history/outcomes.json (per topic) and data/history/outcomes_summary.json (hit rates).
"""
from __future__ import annotations

import csv
import datetime as dt

from common import DATA, KNOWLEDGE, now_utc, parse_date, read_json, similar, today_str, tokens, write_json


def load_performance() -> dict[str, float]:
    perf: dict[str, float] = {}
    for path in (KNOWLEDGE / "performance").glob("*.csv"):
        with path.open(encoding="utf-8-sig") as fh:
            for row in csv.DictReader(fh):
                url = (row.get("url") or row.get("page") or row.get("Page path") or "").strip().rstrip("/")
                views = row.get("pageviews") or row.get("views") or row.get("Views") or "0"
                key = url.split("memeburn.com")[-1].rstrip("/")
                try:
                    perf[key] = perf.get(key, 0) + float(str(views).replace(",", ""))
                except ValueError:
                    pass
    return perf


def main():
    today = dt.date.fromisoformat(today_str())
    posts = read_json(DATA / "memeburn" / "recent.json", {"posts": []})["posts"]
    archive = read_json(DATA / "memeburn" / "archive.json", {"posts": []})["posts"]
    by_url = {p["url"]: p for p in archive + posts}
    all_posts = [{**p, "tokens": tokens(p["title"] + " " + " ".join(p.get("tags", []))), "dt": parse_date(p.get("date"))}
                 for p in by_url.values()]
    perf = load_performance()

    outcomes = []
    for path in sorted((DATA / "briefs").glob("*.json")):
        try:
            bdate = dt.date.fromisoformat(path.stem)
        except ValueError:
            continue
        if (today - bdate).days > 14 or bdate >= today:
            continue
        for t in read_json(path, {}).get("topics", []):
            ttoks = tokens(" ".join([t.get("working_title", "")] + t.get("headline_options", []) + t.get("seo_keywords", [])))
            match = next((p for p in all_posts
                          if p["dt"] and p["dt"].date() >= bdate and similar(ttoks, p["tokens"], 0.15)), None)
            rec = {
                "brief_date": path.stem, "rank": t.get("rank"), "working_title": t.get("working_title"),
                "category": t.get("category"), "urgency": t.get("urgency"), "format": t.get("format"),
                "score": t.get("score"), "published": bool(match),
            }
            if match:
                path_key = match["url"].split("memeburn.com")[-1].rstrip("/")
                rec.update({
                    "article_url": match["url"], "article_title": match["title"], "author": match.get("author"),
                    "hours_to_publish": round((match["dt"] - parse_date(path.stem + "T06:00:00+02:00")).total_seconds() / 3600, 1),
                    "pageviews": perf.get(path_key),
                })
            outcomes.append(rec)

    summary: dict = {"generated_at": now_utc().isoformat(), "topics_suggested": len(outcomes),
                     "topics_published": sum(o["published"] for o in outcomes), "by_category": {}, "by_format": {}}
    for key, bucket in (("category", "by_category"), ("format", "by_format")):
        for o in outcomes:
            b = summary[bucket].setdefault(o.get(key) or "?", {"suggested": 0, "published": 0, "pageviews": []})
            b["suggested"] += 1
            b["published"] += o["published"]
            if o.get("pageviews"):
                b["pageviews"].append(o["pageviews"])
        for b in summary[bucket].values():
            pv = b.pop("pageviews")
            b["pickup_rate"] = round(b["published"] / b["suggested"], 2) if b["suggested"] else 0
            b["avg_pageviews"] = round(sum(pv) / len(pv)) if pv else None

    write_json(DATA / "history" / "outcomes.json", outcomes)
    write_json(DATA / "history" / "outcomes_summary.json", summary)
    print(f"[outcomes] {summary['topics_published']}/{summary['topics_suggested']} suggested topics published (last 14 days)")


if __name__ == "__main__":
    main()
