"""Validate today's brief and post it to Slack.

  python scripts/post_slack.py --validate     # check data/briefs/<date>.json, print problems, exit 1 if invalid
  python scripts/post_slack.py --dry-run      # print the Slack payload instead of posting
  python scripts/post_slack.py                # post (needs SLACK_WEBHOOK_URL)
"""
from __future__ import annotations

import argparse
import json
import os
import sys

import requests

from common import DATA, SETTINGS, read_json, today_str

CATS = {"phone": "📱", "tech": "💻", "ai": "🤖", "crypto": "🪙"}
URGENCY = {"breaking": "🚨 Breaking", "today": "⏰ Today", "evergreen": "🌲 Evergreen"}
FORMATS = {"news", "explainer", "how-to", "listicle", "comparison", "review-roundup", "opinion"}

LABELS = {
    "en": {"header": "Memeburn topic picks", "why": "Why now", "angle": "Angle", "headlines": "Headlines",
           "kw": "Keywords", "src": "Sources", "writer": "Suggested writer", "watch": "Watchlist", "notes": "Note"},
    "vi": {"header": "Gợi ý topic Memeburn", "why": "Vì sao nên viết ngay", "angle": "Góc viết", "headlines": "Tiêu đề gợi ý",
           "kw": "Từ khoá", "src": "Nguồn", "writer": "Writer gợi ý", "watch": "Theo dõi thêm", "notes": "Lưu ý"},
}


def validate(brief: dict, candidates: dict | None) -> list[str]:
    errs = []
    topics = brief.get("topics")
    if not isinstance(topics, list) or not topics:
        return ["`topics` must be a non-empty list"]
    known_urls = set()
    if candidates:
        known_urls = {i["url"] for c in candidates["candidates"] for i in c["items"]}
    for t in topics:
        p = f"topic #{t.get('rank', '?')}"
        for field in ("rank", "working_title", "category", "urgency", "traffic_potential", "score",
                      "why_now", "angle", "format", "headline_options", "seo_keywords", "sources"):
            if field not in t or t[field] in ("", None, []):
                errs.append(f"{p}: missing `{field}`")
        if t.get("category") not in CATS:
            errs.append(f"{p}: category must be one of {list(CATS)}")
        if t.get("urgency") not in URGENCY:
            errs.append(f"{p}: urgency must be one of {list(URGENCY)}")
        if t.get("traffic_potential") not in ("high", "medium"):
            errs.append(f"{p}: traffic_potential must be high|medium")
        if t.get("format") not in FORMATS:
            errs.append(f"{p}: format must be one of {sorted(FORMATS)}")
        if not isinstance(t.get("score"), int) or not 0 <= t["score"] <= 100:
            errs.append(f"{p}: score must be an int 0-100")
        if not 2 <= len(t.get("headline_options", [])) <= 3:
            errs.append(f"{p}: need 2-3 headline_options")
        if not 1 <= len(t.get("sources", [])) <= 4:
            errs.append(f"{p}: need 1-4 sources")
        for s in t.get("sources", []):
            if known_urls and s.get("url") not in known_urls:
                errs.append(f"{p}: source URL not found in candidates (no invented links): {s.get('url')}")
    return errs


def topic_blocks(t: dict, L: dict) -> list[dict]:
    emoji = CATS[t["category"]]
    heat = "🔥🔥🔥" if t["traffic_potential"] == "high" else "🔥🔥"
    head = f"*{t['rank']}. {emoji} {t['working_title']}*\n{URGENCY[t['urgency']]} · {heat} · score {t['score']} · {t['format']} · ~{t.get('est_words', 600)}w"
    body = [
        head,
        f"*{L['why']}:* {t['why_now']}",
        f"*{L['angle']}:* {t['angle']}",
        f"*{L['headlines']}:*\n" + "\n".join(f"• {h}" for h in t["headline_options"]),
        f"*{L['kw']}:* `" + "` · `".join(t["seo_keywords"]) + "`",
    ]
    if t.get("notes_for_writer"):
        body.append(f"*{L['notes']}:* {t['notes_for_writer']}")
    writers = SETTINGS.get("writers", {}).get(t["category"]) or []
    if writers:
        body.append(f"*{L['writer']}:* " + " ".join(f"<@{w}>" for w in writers))
    text = "\n".join(body)[:2900]
    src = " · ".join(f"<{s['url']}|{s['title'][:60]}>" for s in t["sources"])
    return [
        {"type": "section", "text": {"type": "mrkdwn", "text": text}},
        {"type": "context", "elements": [{"type": "mrkdwn", "text": f"{L['src']}: {src}"[:2900]}]},
        {"type": "divider"},
    ]


def build_payload(brief: dict) -> dict:
    L = LABELS.get(brief.get("language", SETTINGS.get("brief_language", "en")), LABELS["en"])
    topics = sorted(brief["topics"], key=lambda t: t["rank"])
    blocks = [
        {"type": "header", "text": {"type": "plain_text", "text": f"☀️ {L['header']} — {brief['date']}"}},
        {"type": "section", "text": {"type": "mrkdwn", "text": brief.get("summary", "")[:2900] or " "}},
        {"type": "divider"},
    ]
    for t in topics[:14]:  # Slack caps a message at 50 blocks
        blocks += topic_blocks(t, L)
    if brief.get("watchlist"):
        blocks.append({"type": "context", "elements": [{"type": "mrkdwn",
                       "text": f"👀 *{L['watch']}:* " + " · ".join(brief["watchlist"])[:2800]}]})
    fallback = f"{L['header']} {brief['date']}: " + "; ".join(t["working_title"] for t in topics[:5])
    return {"text": fallback, "blocks": blocks, "unfurl_links": False, "unfurl_media": False}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", default=today_str())
    ap.add_argument("--validate", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    brief = read_json(DATA / "briefs" / f"{args.date}.json")
    if not brief:
        sys.exit(f"No brief at data/briefs/{args.date}.json")
    errs = validate(brief, read_json(DATA / "candidates" / f"{args.date}.json"))
    if errs:
        print("Brief is INVALID:\n- " + "\n- ".join(errs))
        sys.exit(1)
    if args.validate:
        print(f"Brief OK: {len(brief['topics'])} topics")
        return

    payload = build_payload(brief)
    if args.dry_run:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return
    url = os.environ.get("SLACK_WEBHOOK_URL")
    if not url:
        sys.exit("SLACK_WEBHOOK_URL is not set (use --dry-run to preview)")
    resp = requests.post(url, json=payload, timeout=20)
    if resp.status_code != 200:
        sys.exit(f"Slack error {resp.status_code}: {resp.text}")
    print(f"[slack] posted {len(brief['topics'])} topics for {args.date}")


if __name__ == "__main__":
    main()
