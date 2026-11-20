Optional: export article performance from GA4 or Search Console as CSV and drop it here.
Needed columns: `url` (or `page` / `Page path`) and `pageviews` (or `views`).
`scripts/track_outcomes.py` attaches pageviews to suggested topics that got published,
so the brief learns which kinds of picks actually bring traffic.

## Live source (confirmed by Logan, 2026-11-13)
Memeburn's weekly GA4 traffic lives in this Google Sheet and is kept updated in place —
Logan will not re-share a new link each week, so re-open the same one for fresh data:
`https://docs.google.com/spreadsheets/d/1X0q62YmW1xKJWPLHRvRh5Pa9r4Glj7lQFPkSEu4hXIY/edit`
- Sheet tab **"Bài viết – 7 ngày"** (gid `635773172`) has the rolling 7-day article list:
  columns `B` (Bài viết / path) and `F` (Lượt xem / views) are what's needed here.
- Periodically (e.g. before a `/learn-process` refresh, or whenever "What wins" feels stale):
  pull that tab via the Google Sheets tool, convert `url,pageviews` into a dated CSV in this
  folder (e.g. `ga4_weekly_<start>_to_<end>.csv`), then rerun `python scripts/track_outcomes.py`
  so `data/history/outcomes_summary.json` picks up the new numbers.
- This requires the Google Sheets MCP connector to be authorized in the session; if it isn't,
  say so rather than guessing numbers.
