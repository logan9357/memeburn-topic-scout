"""Crawl hot topics from every source in config/sources.yaml.

Output: data/raw/<date>.json  ->  {date, fetched_at, items: [...], errors: [...]}
Each item: {source, type, region, category_hint, title, url, summary, published, signal{}}
A failing source is logged in `errors` and never stops the run.
"""
from __future__ import annotations

import argparse
import re
from concurrent.futures import ThreadPoolExecutor

import feedparser

from common import DATA, clean_text, load_yaml, now_utc, parse_date, session, today_str, write_json


def make_item(src: dict, **kw) -> dict:
    item = {
        "source": src["name"],
        "type": src["type"],
        "region": src.get("region", "global"),
        "category_hint": src.get("category_hint"),
        "title": "",
        "url": "",
        "summary": "",
        "published": None,
        "signal": {},
    }
    item.update(kw)
    pub = parse_date(item["published"])
    item["published"] = pub.isoformat() if pub else None
    return item


def entry_time(entry):
    return entry.get("published_parsed") or entry.get("updated_parsed")


def fetch_rss(src, http):
    resp = http.get(src["url"], timeout=25)
    resp.raise_for_status()
    feed = feedparser.parse(resp.content)
    return [
        make_item(
            src,
            title=clean_text(e.get("title", ""), 300),
            url=e.get("link", ""),
            summary=clean_text(e.get("summary", "")),
            published=entry_time(e),
        )
        for e in feed.entries[: src.get("limit", 40)]
    ]


def parse_traffic(text: str) -> int:
    m = re.search(r"([\d.,]+)\s*([KkMm]?)", text or "")
    if not m:
        return 0
    num = float(m.group(1).replace(",", ""))
    return int(num * {"k": 1_000, "m": 1_000_000}.get(m.group(2).lower(), 1))


def fetch_google_trends(src, http):
    resp = http.get(src["url"], timeout=25)
    resp.raise_for_status()
    feed = feedparser.parse(resp.content)
    items = []
    for e in feed.entries[: src.get("limit", 30)]:
        news_title = clean_text(e.get("ht_news_item_title", ""), 300)
        items.append(
            make_item(
                src,
                title=clean_text(e.get("title", ""), 200),
                url=e.get("ht_news_item_url") or e.get("link", ""),
                summary=news_title,
                published=entry_time(e),
                signal={"trends_traffic": parse_traffic(e.get("ht_approx_traffic", ""))},
            )
        )
    return items


def fetch_hn(src, http):
    resp = http.get(
        "https://hn.algolia.com/api/v1/search",
        params={"tags": "front_page", "hitsPerPage": src.get("limit", 30)},
        timeout=25,
    )
    resp.raise_for_status()
    items = []
    for h in resp.json().get("hits", []):
        items.append(
            make_item(
                src,
                title=h.get("title") or "",
                url=h.get("url") or f"https://news.ycombinator.com/item?id={h.get('objectID')}",
                published=h.get("created_at"),
                signal={"hn_points": h.get("points") or 0, "hn_comments": h.get("num_comments") or 0},
            )
        )
    return items


def fetch_reddit(src, http):
    items = []
    for sub in src.get("subreddits", []):
        resp = http.get(
            f"https://www.reddit.com/r/{sub}/top.json",
            params={"t": "day", "limit": src.get("limit", 15)},
            timeout=25,
        )
        resp.raise_for_status()
        for child in resp.json().get("data", {}).get("children", []):
            d = child.get("data", {})
            if d.get("stickied") or d.get("over_18"):
                continue
            items.append(
                make_item(
                    {**src, "name": f"r/{sub}", "region": src.get("region", "global")},
                    title=clean_text(d.get("title", ""), 300),
                    url=d.get("url_overridden_by_dest") or f"https://www.reddit.com{d.get('permalink', '')}",
                    summary=clean_text(d.get("selftext", ""), 300),
                    published=d.get("created_utc"),
                    signal={"reddit_score": d.get("score", 0), "reddit_comments": d.get("num_comments", 0)},
                )
            )
    return items


def fetch_coingecko(src, http):
    resp = http.get("https://api.coingecko.com/api/v3/search/trending", timeout=25)
    resp.raise_for_status()
    items = []
    for rank, coin in enumerate(resp.json().get("coins", [])[:10], start=1):
        c = coin.get("item", {})
        change = (c.get("data", {}).get("price_change_percentage_24h") or {}).get("usd")
        change_txt = f" ({change:+.1f}% 24h)" if isinstance(change, (int, float)) else ""
        items.append(
            make_item(
                src,
                title=f"{c.get('name')} ({c.get('symbol')}) trending on CoinGecko{change_txt}",
                url=f"https://www.coingecko.com/en/coins/{c.get('id')}",
                published=now_utc(),
                signal={
                    "coingecko_rank": rank,
                    "price_change_24h": change,
                    "market_cap_rank": c.get("market_cap_rank"),
                },
            )
        )
    return items


FETCHERS = {
    "rss": fetch_rss,
    "google_trends": fetch_google_trends,
    "hn": fetch_hn,
    "reddit": fetch_reddit,
    "coingecko": fetch_coingecko,
}


def run_source(src):
    http = session()
    try:
        items = FETCHERS[src["type"]](src, http)
        return items, None
    except Exception as exc:  # one broken feed must not kill the run
        return [], {"source": src["name"], "error": f"{type(exc).__name__}: {exc}"[:300]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", default=today_str())
    args = parser.parse_args()

    sources = load_yaml("sources.yaml")["sources"]
    items, errors = [], []
    with ThreadPoolExecutor(max_workers=8) as pool:
        for got, err in pool.map(run_source, sources):
            items.extend(i for i in got if i["title"])
            if err:
                errors.append(err)

    out = DATA / "raw" / f"{args.date}.json"
    write_json(out, {"date": args.date, "fetched_at": now_utc().isoformat(), "items": items, "errors": errors})
    print(f"[crawl] {len(items)} items from {len(sources) - len(errors)}/{len(sources)} sources -> {out}")
    for e in errors:
        print(f"[crawl] WARN {e['source']}: {e['error']}")


if __name__ == "__main__":
    main()
