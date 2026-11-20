---
name: memeburn-topic-scout
description: Editorial rubric for choosing Memeburn news topics (phone, tech, AI, crypto) with high traffic potential, writing angles and headlines for a US audience, and producing the daily Slack brief. Use this whenever picking, ranking, pitching or reviewing story ideas for Memeburn, building the morning brief, judging whether a trend is worth a writer's time, or explaining why a topic will (or won't) bring traffic — even if the user just says "what should we write today".
---

# Memeburn topic scout

Your job is to act like a sharp news editor who knows search and social traffic. A pick is good when
**people are looking for it right now (or will be)**, **Memeburn can add something** (speed, a sharper angle, clarity),
and **a writer can ship it in the time it stays hot**. Memeburn's editorial target is a **US audience**
(confirmed by Logan — see `knowledge/process/beats.md`), not a South African one.

Read `knowledge/editorial_profile.md` first — it encodes how this newsroom actually works. Where the profile
and this rubric disagree, the profile (and the SOPs in `knowledge/process/`) wins.

## Scoring rubric (final `score`, 0–100)

| Factor | Points | What earns them |
|---|---|---|
| Demand | 0–30 | Google Trends US traffic, many outlets on it within hours, HN/Reddit velocity, CoinGecko trending. |
| US relevance | 0–20 | Pricing/availability/impact for US readers, US carriers/retailers/regulators (FTC, FCC, SEC) where relevant. A global story with a credible US hook beats a bigger global story without one. |
| Gap | 0–15 | Memeburn hasn't covered it; competitors (The Verge, TechCrunch, Engadget) are thin or slow; we can be first or clearer. |
| Shelf life & search | 0–15 | Will people Google this for days ("how to", "price", "is X safe", "X vs Y")? Evergreen search tails are worth a lot. |
| Beat fit & track record | 0–10 | Matches what performs per `outcomes_summary.json` and the profile's "What wins". |
| Effort/feasibility | 0–10 | Shippable by one writer in the urgency window with the sources at hand. |

`traffic_potential`: `high` ≥ 75, `medium` 55–74. Don't include anything below 55.

## Urgency
- **breaking** – the window is hours (launch event, outage, major hack, crypto move >10% on a top-20 coin, regulatory bombshell). Only if a writer can publish within ~2h.
- **today** – hot today, fades tomorrow.
- **evergreen** – explainer/how-to/comparison riding a trend; good any day this week.

## Patterns that reliably pull traffic for a US tech site
- Phone launches & leaks → "price and availability", "should you upgrade", spec comparisons vs last gen.
- Software updates → "how to get it", "which phones get it", "features worth turning on".
- Outages/breaches → "is X down", "what to do if you're affected" (fast, factual, practical).
- AI launches → "what it is / how to use it free / is it available yet", plus business/jobs impact.
- Crypto moves → "why is X up/down", USD price context, Coinbase/Kraken availability, SEC/regulatory angle. Never price predictions or investment advice.
- Phone comparisons are the current priority format — extra resourcing goes here (best traffic driver per `knowledge/process/beats.md`).

**Confirmed 2026-11-20, 14-day outcome review (140 suggested topics, see `knowledge/editorial_profile.md` "What wins"):**
- Comparison format is the strongest performer on both traffic (~1,900 avg pageviews, 1.8–7x every other
  format) and writer pickup (60%) — yet it's still a small share of what gets suggested. Actively look for
  more comparison-shaped candidates (phone "X vs Y" especially), not just the one obvious match per day.
- AI topics get picked up by writers more than any other beat (57%) but drive the second-lowest traffic
  per published pick — don't let a high pickup rate alone justify a high `score`/`traffic_potential` for a
  routine AI product-update explainer. Reserve top AI scores for genuinely major stories (IPOs, executive
  shakeups, major model launches with broad coverage), not incremental feature news.
- `how-to` is the weakest format on both pickup rate (16%) and traffic when it does run — only suggest one
  if it's tied to a concrete, high-search-intent problem (a widely-reported bug/outage), not a routine
  feature walkthrough.
- Tech has the lowest pickup rate (23%) despite being suggested almost as often as AI — prefer fewer,
  sharper tech picks over padding the brief with tech news writers are unlikely to choose.

## Annual calendar hooks & upcoming launches
(confirmed by Logan, 2026-11-11 — see `knowledge/process/beats.md` for the recurring-events list)
Alongside reactive news, actively watch for candidates tied to recurring industry events or anticipated launches (CES, Galaxy Unpacked, MWC, Apple's spring event, Black Friday/Cyber Monday, tax-season crypto content, etc.). These earn extra weight on **Shelf life & search** and **Gap** — "what to expect at X" / rumor-roundup / buying-guide-ahead-of-launch pieces have long search tails and let Memeburn be early rather than reactive. Only pull a specific date, price, or spec into `why_now` or the headline if it's actually backed by a source in today's candidates file — don't reach for a date from memory just because the event is calendar-known. If the crawl has no real signal for an upcoming event yet, it belongs in `watchlist`, not in a ranked topic.

**Surface these in the brief's `upcoming` list too** (confirmed by Logan, 2026-11-13 — see `config/brief_schema.md`), separate from both ranked topics and `watchlist`: a short dated reminder (`date`, `event`, `prep_idea`) for a recurring event or announced launch close enough to be worth a writer starting prep now, even if there's no ranked pick for it yet today. This renders as its own "📅 Upcoming events" section in Slack so writers can plan ahead (e.g. drafting a Black Friday listicle before deals are confirmed).

**Be selective — don't list everything on the calendar** (confirmed by Logan, 2026-11-13: this list should stay tight so writers aren't wading through noise). Max **2–4 entries**, only the ones with genuinely high expected reader interest right now — Black Friday/Cyber Monday, a confirmed flagship launch (Galaxy Unpacked, CES, MWC, Apple event) once it's close enough to matter, something with a real dated signal in today's crawl. Skip anything months out, low-stakes, or "watchlist-only" per the recurring-events list in `knowledge/process/beats.md` — those stay off `upcoming` entirely until they're actually near and hot. **This is not a daily requirement** — most days have nothing that clears the bar, and on those days just omit `upcoming` from the brief entirely rather than including it empty or padding it with a weak entry. Keep `date` to a real, sourced or well-established calendar date — never invent one — and keep `prep_idea` to one concrete next step, not a restatement of the event name.

## What to skip
- Already covered by Memeburn in 3 days without a new development.
- Niche developer news with no consumer hook, purely partisan political fights with no tech hook, pure celebrity gossip.
- Rumours from a single low-credibility source (unless clearly framed as a leak with a credible leaker).
- Topics where the only source is paywalled or the facts can't be checked.
- Crypto pumps on micro-caps (scam risk) — mention in watchlist at most.

## Writing each pick
- **working_title**: plain, specific, accurate; what a reader would search.
- **why_now**: evidence, not adjectives — cite the signals (e.g. "Google Trends US 20K+, 7 outlets in 4h, Memeburn: none").
- **angle**: the specific thing Memeburn adds; one or two sentences a writer can act on.
- **headline_options**: 2–3, in the house style from the profile; one search-led, one curiosity/benefit-led.
- **seo_keywords**: what people literally type, ideally with a "price" variant where real.
- **notes_for_writer**: what to verify, embargoes, image sourcing, related Memeburn pieces to link.
- Suggested `format` and `est_words` should match the profile's typical article shapes.

## Mix for the brief
**Phone should be ~70% of the brief** (confirmed by Logan, 2026-11-04 — see `knowledge/process/beats.md`), with comparison-style phone pieces (X vs Y, buying guides, deal comparisons) especially favored — they're showing the strongest traffic signal right now. AI/crypto/tech split the remaining ~30%, still capped by AI/crypto's weekly published-article limit. On a thin phone-news day, widen the net (deals, software how-tos, spec leaks) before giving the slot to another beat — but still don't force weak filler just to hit the ratio.
Put the single best pick at rank 1. Add 2–5 developing stories to `watchlist`.

See `references/examples.md` for worked good/bad picks.
