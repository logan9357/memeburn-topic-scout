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
Roughly 2 per beat on a normal day, but follow the news — don't force a weak crypto pick on a quiet crypto day.
Put the single best pick at rank 1. Add 2–5 developing stories to `watchlist`.

See `references/examples.md` for worked good/bad picks.
