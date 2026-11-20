# Beats

_Last confirmed: 2026-11-02, via interview with Logan._

## Who covers what
- **Huy** and **Duy** both cover all four beats equally (phone, tech, AI, crypto) — no fixed beat ownership between them.
- **AI News** and **Crypto News**: capped at a **max of 5 published articles/week** (team-wide cap per category, not per writer).
- **Phone comparisons**: currently the priority format — extra effort is being directed here because it's driving the best traffic right now. Treat phone-comparison-shaped topics (spec battles, "X vs Y", buying guides) as high-value picks.
- **Phone allocation (confirmed by Logan, 2026-11-04)**: phone should make up roughly **70% of each day's brief** — a sharp increase from the earlier "~2 per beat" default. Comparison-style phone pieces specifically (X vs Y, buying guides, deal comparisons) are showing very strong traffic signal right now, so actively favor them over other phone formats when candidates allow. AI/crypto/tech fill the remaining ~30%, still respecting AI/crypto's weekly published-article cap. On a day with genuinely thin phone news, don't force weak phone filler just to hit 70% — but actively widen the net (include phone deals, software-update how-tos, spec leaks, buying guides) before conceding the slot to another beat.

## Annual calendar hooks & upcoming launches (confirmed by Logan, 2026-11-11)
Beyond reactive news, proactively favor topics tied to recurring industry events/launches when the daily crawl actually surfaces a real signal for one (a leak, an official date, confirmed production news) — these have long search tails ("what to expect", rumor roundups, buying-guide-ahead-of-launch) and let Memeburn get ahead of the story instead of chasing it. Near-term recurring calendar to keep in mind (verify every specific date/price/spec against today's candidates before publishing — never state one from memory):
- **Black Friday / Cyber Monday** (late Nov) — phone/accessory deal comparisons, Memeburn's highest-value seasonal format.
- **CES** (early Jan, Las Vegas) — AI gadgets, first-look previews; "what to expect at CES" content runs well in late December.
- **Samsung Galaxy Unpacked** (historically Jan/Feb) — flagship launch; rumor-roundup and "S-series vs last gen" comparisons in the run-up.
- **MWC Barcelona** (late Feb/early Mar) — the biggest phone-industry trade show; foldables and mid-range Android flagships cluster here.
- **Apple spring event** (historically Mar) — new iPads, SE/e-line refreshes.
- Further out (track in watchlist, not yet actionable): **Google I/O** (May), **WWDC** (Jun).
- **Crypto tax season** (Jan–Apr) — evergreen explainer content ("crypto taxes 2026/2027"), not tied to a single date.
This list is a lens for spotting good candidates early, not a source of facts — a topic only becomes a ranked pick (not just watchlist) once a real candidate with a credible source backs it.

**Confirmed 2026-11-13**: near-term items from this list also go into the brief's `upcoming` field (date, event, one-line prep idea) so they show as a dedicated "📅 Upcoming events" section in the Slack post — separate from ranked topics and from `watchlist` — giving writers a heads-up to start prepping before there's a ranked pick for it. **Keep this to max 2-4 genuinely hot, high-interest items** (Logan: don't let it get noisy for writers) — not every item on the list above; most of these stay off `upcoming` entirely until they're actually close and hot. See `config/brief_schema.md` and the skill's "Annual calendar hooks" section.

## Capacity
- Each writer can produce **5–8 articles/day**. With 2 writers (Huy, Duy), team daily capacity is **10–16 articles/day**.
- The morning brief should suggest **~10 topics/day** (`topics_per_brief` in `config/settings.yaml`, confirmed by Logan 2026-11-13) — workflow.md's number, not the old 16 target; every brief actually produced so far has landed in the 8–10 range and that's correct, not a shortfall.
- Working hours start at **08:00 GMT+7** (note: this is the writers' local time, not Memeburn's SA/ZA editorial timezone — useful for timing when the Slack brief should land to be seen at the start of the day).
- Bylines: **Vincee Cole** and **Marko Nguyen** are Huy's and Duy's actual publishing names (confirmed by Logan 2026-11-13, exact pairing — which name is Huy vs. Duy — still to confirm) — together they account for 83% of all output in the 90-day archive.

## Audience note (overrides CLAUDE.md's SA framing)
Logan confirmed the editorial target is primarily a **US audience**, not South African readers. No SA-localisation step (Rand pricing, SA carrier comparisons, local examples) is part of the current writing process. This conflicts with CLAUDE.md's "Hard rules" section (Rand pricing for SA audiences, SA angle in `why_now`) and the `memeburn-topic-scout` skill's rubric — flagged for Logan to reconcile; until resolved, this file's statement is the more recent ground truth per the `/learn-process` precedence rule.
