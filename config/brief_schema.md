# Brief file contract: data/briefs/<YYYY-MM-DD>.json

`scripts/post_slack.py --validate` enforces this. Claude must write exactly this shape.

```json
{
  "date": "2026-11-02",
  "language": "en",
  "summary": "One or two sentences: what dominates today and where the traffic is.",
  "topics": [
    {
      "rank": 1,
      "candidate_ids": ["c03", "c11"],
      "working_title": "Samsung confirms Galaxy S27 launch date, US pre-orders open",
      "category": "phone",
      "urgency": "breaking",
      "traffic_potential": "high",
      "score": 86,
      "why_now": "Trending on Google US (50K+), covered by 6 outlets in 5 hours, Memeburn has nothing yet.",
      "angle": "What it costs, which US carriers carry it, and whether to wait or buy the S26 on sale.",
      "format": "news",
      "est_words": 600,
      "headline_options": ["...", "..."],
      "seo_keywords": ["galaxy s27 price", "galaxy s27 launch date"],
      "sources": [{"title": "...", "url": "https://..."}],
      "notes_for_writer": "Optional: embargo, image rights, things to verify."
    }
  ],
  "watchlist": ["Optional short list of developing stories worth checking at lunch"],
  "upcoming": [
    {"date": "2026-11-27", "event": "Black Friday / Cyber Monday", "prep_idea": "Phone/accessory deal comparison listicle, start drafting now"}
  ]
}
```

Allowed values
- category: phone | tech | ai | crypto
- urgency: breaking (publish within ~2h) | today | evergreen (any day this week)
- traffic_potential: high | medium
- format: news | explainer | how-to | listicle | comparison | review-roundup | opinion
- score: integer 0–100 (Claude's final editorial score, not the prescore)
- sources: 1–4 entries, every URL must appear in that day's candidates file
- headline_options: 2–3 entries; seo_keywords: 2–5 entries
- upcoming: optional, **max 2–4 entries — be selective, not exhaustive** (keep it to genuinely hot,
  high-interest items so it doesn't crowd the writers' view; see skill's "Annual calendar hooks"
  section for the bar). Not a daily requirement — **omit the field entirely on days with nothing
  that clears the bar**, don't include it empty or pad it with a weak entry. Each entry needs
  `date` (real date, not a guess — only from a calendar-known recurring event or a dated signal in
  today's candidates) and `event`; `prep_idea` is optional but recommended (what a writer could
  start drafting ahead of time). This is for recurring-event/launch awareness — distinct from
  `watchlist`, which is for developing stories, not calendar dates.
