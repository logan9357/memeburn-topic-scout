---
description: Learn (or refresh) how Memeburn currently produces news content and save it as the editorial profile
---
Learn Memeburn's current news production process and write `knowledge/editorial_profile.md`.

1. Pull the archive and compute stats:
   ```
   python scripts/fetch_memeburn.py --days 90 --with-content --out data/memeburn/archive.json
   python scripts/learn_stats.py
   ```
2. Read `knowledge/stats.json`, every file in `knowledge/process/` (team SOPs, style guide, briefs — these
   are the ground truth), `data/history/outcomes_summary.json` if present, and any CSVs in
   `knowledge/performance/`. WebFetch 6–8 recent Memeburn articles across the four beats to see the
   writing itself (intro style, how sources are credited, any regional localisation, CTAs, image use).
3. Write `knowledge/editorial_profile.md` with these sections, each backed by evidence (numbers from
   stats, quotes from SOPs, or article examples):
   - **Beats & mix** – share of output per beat, which categories/tags map to phone/tech/AI/crypto
   - **Production workflow** – pitch → assignment → writing → editing → publishing, who does what, turnaround
     (from SOPs; if absent, infer cadence from timestamps and list the gaps as questions)
   - **Writers & beats** – which author covers what (for writer suggestions)
   - **What wins** – formats, angles and topics with the best pickup/pageviews; what Memeburn consistently skips
   - **Angle playbook** – how global stories get a US-relevant hook (USD pricing, US carriers/retailers,
     availability, regulators); note current confirmed audience is US, not South African (`knowledge/process/beats.md`)
   - **Headline style** – length, patterns, examples of good ones
   - **Article shape** – typical word count per format, structure, sourcing habits (top outbound sources)
   - **Publishing rhythm** – busiest hours/days, so `urgency` matches when writers can actually ship
   - **Open questions** – things the data can't tell you; ask the user to confirm them
4. Show the user a short summary of what changed versus the previous profile (if any) and the open questions.
   In an interactive session, update the profile with their answers.
