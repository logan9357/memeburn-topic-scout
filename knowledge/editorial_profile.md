# Memeburn editorial profile

_Built 2026-11-13 via `/learn-process`, from 1,041 posts published in the last 90 days (WP REST API,
`data/memeburn/archive.json`), `knowledge/stats.json`, `data/history/outcomes_summary.json`, and every file
in `knowledge/process/`. This replaces the placeholder that was here before — there is no prior real
profile to diff against, so everything below is new. WebFetch of live memeburn.com article pages returned
HTTP 403 (blocked for automated fetches), so claims below about full article bodies are inferred from
WP API metadata (openings, word/H2/image counts, outbound domains) rather than confirmed by reading a
rendered page — flagged again under Open questions._

## Beats & mix
- WordPress categories don't map 1:1 onto this project's four beats. "News" is a near-universal parent tag
  (813/1,041 posts, 78%), almost always paired with a more specific category.
- **phone** has no dedicated WP category — phone content is split across **Tech** (evergreen comparisons/
  buying guides, 77/141 sampled phone "vs"/deal titles) and **News + Tech News** (reactive phone news,
  46/141) and occasionally **AI News** when the phone story is AI-feature-led (15/141).
- **tech** ≈ Tech News (415 posts) + Tech (164 posts, evergreen/long-form).
- **ai** ≈ AI News (254 posts) + AI (36 posts, evergreen/long-form, much longer pieces — see Article shape).
- **crypto** ≈ Crypto News (138 posts) + Crypto (21 posts, evergreen/long-form).
- Pickup rate by beat over the last 14 days of suggested topics (`data/history/outcomes_summary.json`):
  **phone 33%** (19/58 published), **ai 29%** (8/28), **crypto 14%** (1/7), **tech 9%** (1/11). Phone and AI
  are what actually gets chosen; tech and crypto get suggested plenty but rarely picked up.

## Production workflow (from `knowledge/process/workflow.md`, confirmed 2026-11-02 interview; updated 2026-11-13)
- **Ideas**: the Topic Scout morning brief is the primary idea source, **~10 topics/day** — confirmed
  2026-11-13 as the current number (not the old `topics_per_brief: 16` target); `config/settings.yaml`
  and `beats.md` have been updated to match. Every brief actually produced so far landed at 8–10 topics,
  which is correct, not a shortfall.
- **Assignment**: Logan reviews via Slack. **Confirmed 2026-11-13: the outline-approval step (writer
  sends Logan an outline before writing starts) is no longer happening day-to-day** — the current flow is
  simply posting the ranked brief to Slack and Huy/Duy self-selecting what fits their day.
- **Capacity**: Huy and Duy each write 5–8 articles/day, any beat. AI News + Crypto News combined are
  capped at 5 published articles/week team-wide — consistent with crypto's and (to a lesser extent) ai's
  lower publish counts despite steady suggestion volume.
- **Editing**: Logan is the sole editor, approving both outline and final draft. 15-part per-piece
  checklist (SEO title, meta description, excerpt, TL;DR, glossary, FAQ, etc.) — see workflow.md for the
  full list; not repeated here since that file is the ground truth.
- **Publishing**: automated once approved — not a writer/editor concern day-to-day.
- **Measuring**: GA4 + Google Search Console, watching pageviews/traffic source/time on page — but no
  export has been dropped into `knowledge/performance/` yet (see Open questions).

## Writers & beats
- Two bylines dominate: **Vincee Cole** (450 posts, 43%) and **Marko Nguyen** (417 posts, 40%) — together
  83% of all output, spread across every beat (News, Tech News, AI News, Crypto News, Tech).
- Smaller/secondary bylines write mostly the evergreen, non-"News" categories: **Temaz Tra** and
  **Jennie Pham** concentrate in AI News; **Michael Sacchitello**, **Mabel Kenneth**, **Josephine Abiodun**,
  **Archana Shivkumar** write mostly Tech/AI/Crypto (the longer-form, evergreen track).
  **Staff Reporter**/**Norris** handle "Partnered" (sponsored) content, a separate track.
- **Confirmed 2026-11-13**: Vincee Cole and Marko Nguyen are Huy's and Duy's actual publishing bylines
  (exact pairing — which name is Huy vs. Duy — still unconfirmed). Since both writers cover all four
  beats equally (per beats.md), there's no beat-specific writer to tag, so `config/settings.yaml`'s
  `writers:` map is intentionally left empty rather than guessing a pairing.

## What wins
**Updated 2026-11-20 with a full 14-day outcome review** (140 suggested topics across Nov 6–19, matched
against real GA4 traffic from `knowledge/performance/ga4_28d_2026-10-23_to_2026-11-19.csv`, 405 articles).
This is a much larger sample than the first GA4 pass on 2026-11-13 (which had phone n≈22) — treat these
numbers as solid, not just directional.
- **By beat — suggested / published / pickup rate / avg pageviews**: phone 62/26/**42%**/**1,310**; ai
  37/21/**57%**/286; tech 26/6/23%/325; crypto 15/6/40%/104.
  - Phone still drives far more traffic per published pick than any other beat (**4–12x**), confirming the
    existing ~70% mix target is directionally right.
  - **AI has the highest pickup rate (57%) but near-bottom traffic (286)** — writers reach for AI topics
    readily (they're often fast, newsy explainers) but they don't pull proportionate readers. Don't read
    "writers keep choosing AI" as "AI is working" — on this data it mostly isn't, outside breaking/major
    stories (Anthropic IPO, Jensen Huang, Nvidia earnings). Reserve high `traffic_potential`/high `score`
    AI picks for genuinely major news, not routine AI product-update explainers.
  - **Tech has the lowest pickup rate (23%)** despite being suggested almost as often as AI — writers
    skip most tech suggestions. Suggest fewer, more clearly "shippable" tech picks rather than padding
    the brief with marginal tech news nobody ends up writing.
- **By format — suggested / published / pickup rate / avg pageviews**: comparison 10/6/**60%**/**1,922**;
  news 59/26/44%/1,078; explainer 40/18/45%/413; listicle 7/5/**71%**/263; review-roundup 5/1/20%/970
  (n=1, noisy); **how-to 19/3/16%/305 — worst on both axes**, lowest pickup rate AND unremarkable traffic
  when it does run.
  - Comparison is confirmed as the best format on both traffic (1,922 avg, ~1.8–7x other formats) and
    pickup (60%) — yet it's still only ~7% of suggested topics (10/140). There's room to suggest
    meaningfully more comparison-shaped phone picks (spec battles, "X vs Y", buying-guide comparisons)
    than the brief currently does.
  - Deprioritize `how-to` relative to other formats unless a how-to pick is tied to a very concrete,
    high-search-intent fix (a widely-reported bug/outage), not a routine feature walkthrough.
- **Concrete examples from this window**: top published picks were Samsung Galaxy XCover 7 Pro One UI 9
  rollout (phone/news, 6,385 views), Motorola Signature 27 vs Galaxy S25+ (phone/comparison, 4,324), and
  Google Pixel Tag vs AirTag (phone/comparison, 2,234) — all phone, two of three comparisons.
- **Black Friday deal content remains validated**: deal-roundup picks (iPhone, Apple Watch, tablets,
  Samsung phones, AI gadgets, Ray-Ban Meta) each pulled real views in this window — confirms `beats.md`'s
  "annual calendar hooks" entry for Black Friday.
- **Caveat**: category/format buckets still have uneven sample sizes (crypto and tech on the low end,
  comparison/listicle/review-roundup under 10 suggestions each) — keep refreshing this from
  `knowledge/performance/` (see its README for the live GA4 sheet) rather than treating these as final.

## Angle playbook
- Every sampled headline/opening is USD- and US-carrier-framed with zero rand/ZA framing anywhere in the
  90-day sample (e.g. "$899", "Android Auto", "US carriers", "T-Mobile's Un-Carrier Pledge") — strongly
  confirms `beats.md`'s US-audience override is already how Memeburn actually writes, not just a stated
  intention.
- Headlines lead with the **quantified verdict**, not a neutral description: "Samsung Wins 4 of 7 Rounds,"
  "25% More Battery," "Is the Upgrade Worth It?," "$300 More." The comparison isn't just named — it's
  already scored in the headline.
- Openings are verdict-first, inverted-pyramid: state the conclusion in sentence one, then the date/source
  in sentence two. E.g. "The Chinese Xiaomi 18 Pro is worth its roughly $320 premium over the POCO F8 Pro
  only if cameras are your priority, because..." — the reader gets the answer before the background.
- This is the strongest, most consistent, most evidence-backed pattern in the whole archive — any
  `headline_options` and `angle` text Claude writes for phone-comparison picks should mirror it: name the
  two things being compared, and resolve the comparison with a number or a conditional ("worth it if...")
  rather than leaving it open.

## Headline style
- Median headline length: **71 characters**.
- Pattern frequency (90 days): straight-news (469), colon/split "X: Y" (399), price/launch (191),
  comparison (140), question (133), number/listicle (48), how-to (18), sa-localised (6 — essentially
  extinct, confirming the US-audience shift is real and not just a recent announcement).
- Colon/split is common beyond comparisons too: "ColorOS 17 on OnePlus 15: 3 Changes That Matter Before
  You Update."

## Article shape
- **This varies a lot by track, more than a single blended median suggests.** Overall median is 1,442
  words (p25 1,221, p75 1,735), but:
  - "...News" categories (reactive: News/Tech News/AI News/Crypto News) run **1,268–1,430 words median**
    — matches workflow.md's stated 1,100–1,600 body target closely.
  - "Tech"/"AI"/"Crypto" (no "News" suffix — the evergreen/comparison/listicle track) run far longer:
    **2,166–3,164 words mean**. The written SOP's 1,100–1,600 target undershoots what evergreen pieces
    actually run.
  - "X vs Y" comparison-titled posts: median **1,608 words**. "Best X" listicles: median **2,741 words**.
  - **Confirmed 2026-11-13**: comparison/listicle picks in the daily brief should carry an `est_words` of
    roughly **1,600–2,800**, not the ~450–800 used so far. Reactive news-format picks stay closer to
    workflow.md's 1,100–1,600.
- avg_h2 **7.3**, avg_images **5.1** per post.
- Top outbound domains: **amzn.to (353) + link.amazon (48)** — by far the most-linked destination across
  the whole archive, well ahead of any single news outlet, pointing to heavy affiliate/shopping-link use
  especially in deal/buying-guide content. Next: x.com (123, likely tweet embeds/official statements),
  **gsmarena.com (94)** and notebookcheck.net (41) as the dominant phone-spec primary sources, then
  official company sources (apple.com 37, openai.com 30, anthropic.com 25, samsung.com/news.samsung.com 38
  combined, blog.google 22) — consistent with workflow.md's "primary sources first" sourcing rule.
  Tech press (techcrunch.com 30, androidauthority.com 26, macrumors.com 28) and business/finance press
  (reuters.com 22, cnbc.com 22, finance.yahoo.com 26) both show up meaningfully, as the SOP's source
  hierarchy predicts.

## Publishing rhythm
- **Weekday**: fairly even across all 7 days (Thu 164 down to Tue 140) — this is effectively a 7-day/week
  operation, weekends (Sat 152, Sun 149) nearly as active as weekdays.
- **Hour of day**, converted from the raw SAST data to the writers' actual **GMT+7**: clear peaks around
  **9am** (92 posts), **1pm** (79), **5pm** (68), **8–9pm** (81/71), with a smaller cluster around 1am
  (58) — publishing happens in multiple waves through the day, not one single morning batch. The 9am
  GMT+7 peak lines up neatly with the brief landing at 7am and the 8am workday start.
- **Practical implication**: a `breaking` pick doesn't have to clear in the first hour of the workday to
  still be useful — there's real publishing activity through the afternoon and evening too.

## Resolved 2026-11-13 (confirmed by Logan)
- `topics_per_brief` → ~10/day, matching workflow.md and actual output (not the old 16 target).
- The outline-approval step is gone; posting the ranked brief to Slack for self-selection is the current
  flow.
- Vincee Cole / Marko Nguyen = Huy / Duy's actual bylines (exact pairing still unconfirmed, but doesn't
  block anything since both cover all beats equally).
- Comparison/listicle picks should carry `est_words` ~1,600–2,800, not ~450–800.
- The weekly GA4 sheet is a **live, standing source**, not a one-off snapshot — Logan updates it
  in place and won't re-share a new link each week. See `knowledge/performance/README.md` for the
  URL and the refresh steps (pull "Bài viết – 7 ngày" tab → CSV → rerun `track_outcomes.py`).

## Open questions (still need Logan to confirm)
1. Which byline is Huy and which is Duy, specifically — Vincee Cole or Marko Nguyen? (Low priority: no
   beat-specific tagging depends on it since both cover every beat equally.)
2. `memeburn.com` returns HTTP 403 to automated WebFetch, so this profile couldn't verify inline
   source-crediting phrasing, CTA/related-article box patterns, or exact affiliate-link placement by
   reading a live page — only inferred from WP API metadata. If you want these confirmed, either paste in
   2–3 full article texts, or point to another access route.
3. "News" is applied to 78% of all posts as what looks like a default/parent tag alongside a more specific
   category — does it carry any independent editorial meaning Claude should weight, or is it purely
   structural?
