# Workflow: idea to published

_Last confirmed: 2026-11-02, via interview with Logan. Source for the writing/sourcing/image rules: internal "AI news writing" SOP spreadsheet (shared by Logan)._

## Ideas
- Primary source: the Memeburn Topic Scout morning brief (crawl + candidates), which should surface up to **10 topics/day** — a slight surplus over daily writing capacity so there's room to choose.
- **Logan** has final say on which topics get written. Nothing gets written on spec — see Assignment below.

## Assignment
- Logan reviews and assigns via **Slack**.
- Before any writing starts, the writer sends an **outline** to Logan for approval (title, main keyword, slug, angle, 2 new angles vs. existing coverage, estimated word count). Writing only begins after outline approval.
- Daily capacity: **Huy** and **Duy** each write **5–8 articles/day**, covering all four beats interchangeably.
- Category cap: **AI News** and **Crypto News** are capped at **5 published articles/week** combined (team-wide, not per writer).
- Priority: **phone comparison** pieces currently get the most resourcing — they're the best traffic driver.
- Workday starts **08:00 GMT+7**.

## Writing
Research (required before writing, 9 steps):
1. Check Memeburn itself for duplicate coverage (`site:memeburn.com` + product/company name), last 30 days; link back to any earlier post on the same topic.
2. Check what other outlets are already saying (Google News/Search on the main keyword) — read top 5–10 results, note each one's angle and gaps.
3. Read primary sources first — company blog/newsroom, help center, pricing page — before reading news coverage of them.
4. Fill a product fact sheet: what it is, launch date, who can use it, availability, usage limits, underlying model, data/training, stated limitations — each answer needs a source link.
5. Cross-check every number/date/price against **at least 2 sources**, one of which must be the company itself. Single-sourced claims get highlighted in the draft.
6. Find **at least 2 angles** the top 10 Google results don't already have.
7. If the product was actually hands-on tested (by the writer or team), note duration/device/plan/result with screenshots; if not tested, the article must say so explicitly — never claim "we tested"/"hands-on" without it being true.
8. Pick 3–5 relevant internal Memeburn links (from the NFTP Internal Link Report and author pages); verify each link still works.
9. Submit the outline to the tracking sheet/Logan for approval before writing begins.

Source priority (use higher tiers first; lower tiers only when nothing better exists):
1. **Primary**: company blogs/newsrooms, help centers, pricing pages, model cards, GitHub, arXiv, SEC filings, official X accounts — for specs, pricing, launch dates, eligibility; preferred for outbound links.
2. **Tech press**: The Verge, TechCrunch, Engadget, Wired, Ars Technica, SiliconANGLE — for context, rollout, user reaction.
3. **Business/finance press**: Reuters, Bloomberg, CNBC, WSJ, Yahoo Finance — for funding, IPOs, revenue, stock info.
4. **Independent data/research**: LMArena, Artificial Analysis, Epoch AI, Stanford AI Index, Pew Research — for model comparisons/surveys; always date-stamp the data.
5. **Outside blogs** (vendor/agency/aggregator blogs, Wikipedia): last resort only; attribute as "reports say" and highlight in the draft.

Target length & structure by format (15-part article structure — see full checklist detail below): body is **1,100–1,600 words** (or "no limit" if Logan says so for that piece). Suggested H2 flow by article type:
- **Product/feature/model launch**: What Is X? → What It Can Actually Do → Who Can Get It and What It Costs → How It Compares → What [Company] Didn't Say → Is It Worth It for You?
- **How-to/explainer**: Before You Start → Step by Step → Settings to Change First → Ways to Use It → Common Problems → Is It Worth It?
- **Safety/security/policy**: What Happened → How It Works → What Researchers Found → What It Means for You → What Happens Next
- **AI business news** (funding, IPO, earnings, chips, partnerships): The Deal in Numbers → Why Now → Who Wins and Who Loses → What It Means for You → What to Watch Next
- **Stats/data roundup** ("… statistics 2026"): Key Stats at a Glance → one H2 per data-backed conclusion → comparison table of sources that disagree → How We Collected the Data → FAQ

Images:
- Featured image ≥1200px, 16:9; in-body images max 750px wide, saved as `.jpg`. Title/alt text must accurately describe the image.
- Roughly one image per ~300 words; each image must illustrate the adjacent paragraph, not be decorative filler.
- Screenshots need a "Source: …" caption linking to the original page. Product shots only from the company's own newsroom/press kit — never re-taken from another outlet.
- No faked/mocked-up UI; leaked or experimental features must be labeled as such in the caption.
- Redact emails, account names, private chat content, and API keys before saving any screenshot.

No SA-localisation step currently — see `beats.md` ("Audience note") for the US-audience framing and the conflict this creates with CLAUDE.md's existing SA hard rules.

## Editing & SEO
- **Logan** is the sole editor — approves both the outline (pre-writing) and the final draft (pre-publish).
- Style: write as "we", address the reader as "you"; short sentences, plain words, contractions, American English spelling. Avoid cliché phrases (per the SOP's banned-phrases list). Quotes capped at 15 words. Author's own takes spread through the piece, not dumped at the end. Every acronym/term explained in one sentence on first use.
- Required elements per piece (full 15-part checklist — slug, keyword, SEO title, meta description, excerpt, TL;DR, headline, intro, body, glossary, voice, conclusion, disclaimers when discussing stocks/IPOs/valuations, 5-question FAQ, links):
  - **SEO title**: 50–60 characters, keyword first, no repeated words.
  - **Meta description**: 140–155 characters, includes keyword + company name.
  - **Excerpt**: 40–55 words, keyword in the first sentence, at least one number.
  - **TL;DR**: 5 lines, 70–110 characters each (launch date, who can use it + price, newest detail, one limitation).
  - **Conclusion**: never titled "The Bottom Line"/"The Takeaway", never just a recap — ends on a concrete verdict or recommendation.
  - **FAQ**: 5 questions, each answer under 500 characters, no repeat of body content, each with an internal link.
  - **Links**: 2–3 outbound (prefer primary sources, anchor text embedded naturally, spread across paragraphs, never "we covered"/"as we reported"); at least 3 internal links with descriptive anchor text.
- Pre-submission checklist before sending to Logan (12 checks): no duplicate coverage (or linked if a follow-up); angle has ≥2 new points vs. competitors; plans/pricing/eligibility/age/launch date match the company's own page; benchmark numbers attributed to whoever published them, not inflated; no false "we tested"/"hands-on" claims; every term explained on first use; headline isn't clickbait and the piece delivers on it; character/word counts verified via wordcounter.net; 2–3 outbound + 3+ internal links all checked by hand; no banned clichés, no "The Bottom Line" heading, quotes ≤15 words; images correctly sized/`.jpg`/titled/alt-texted/sourced; numbers in prose match numbers in any table.
- Tools used: Google News/Search, X, Memeburn's own search, the NFTP Internal Link Report, Google Docs (drafting), wordcounter.net (counts), Canva/Infogram (images/charts).

## Publishing
Automated — not a writer/editor concern day-to-day. Memeburn Topic Scout's job stops at suggesting topics for writers to pick from; CMS categorisation, tagging, and social distribution happen automatically after publish.

## Measuring
- Metrics that matter: **pageviews, traffic source, time on page**.
- Tracked in: **GA4** and **Google Search Console**.
