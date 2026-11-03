---
description: Build today's Memeburn topic brief from trend data and post it to Slack
argument-hint: "[--dry-run] [--no-crawl]"
---
Arguments: $ARGUMENTS

Produce today's Memeburn morning topic brief.

1. **Prepare data** (skip if `--no-crawl` is in the arguments and `data/candidates/<today>.json` exists).
   Today's date is the SAST date: `python -c "import sys; sys.path.insert(0,'scripts'); from common import today_str; print(today_str())"`.
   ```
   python scripts/crawl_trends.py
   python scripts/fetch_memeburn.py --days 7
   python scripts/track_outcomes.py
   python scripts/build_candidates.py
   ```
   If more than half the sources failed, continue but mention it in `summary`.

2. **Load context**: the `memeburn-topic-scout` skill, `knowledge/editorial_profile.md`, any files in
   `knowledge/process/`, `data/history/outcomes_summary.json`, and `config/settings.yaml`
   (`topics_per_brief`, `brief_language`).

3. **Review candidates** in `data/candidates/<today>.json`. The prescore is a hint, not a decision — re-rank
   with the skill's rubric. Merge clusters that are the same story. For the top ~10 contenders you may
   WebFetch one source each to check the facts and find the angle.

4. **Write `data/briefs/<today>.json`** following `config/brief_schema.md` exactly, in the configured
   language. Aim for a mix: at least one pick per beat when the day allows, at least one `breaking` if
   anything qualifies, and 1–2 `evergreen` explainers/how-tos riding a trending search.

5. **Validate**: `python scripts/post_slack.py --validate`. Fix and re-run until it passes.

6. **Publish**:
   - if `--dry-run` is in the arguments: `python scripts/post_slack.py --dry-run` and show a short summary.
   - otherwise: `python scripts/post_slack.py`. If `SLACK_WEBHOOK_URL` isn't set, fall back to dry-run and say so.

7. End with a 3-line recap: number of picks per beat, the #1 pick, and any source failures.
