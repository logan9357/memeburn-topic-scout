.PHONY: setup learn prepare brief preview post daily

setup:
	pip install -r requirements.txt
	npm install -g @anthropic-ai/claude-code

learn:                 ## learn Memeburn's current process (run monthly)
	claude "/learn-process"

prepare:               ## crawl + build candidates, no AI
	python scripts/crawl_trends.py
	python scripts/fetch_memeburn.py --days 7
	python scripts/track_outcomes.py
	python scripts/build_candidates.py

preview: prepare       ## full run without posting to Slack
	claude -p "/morning-brief --no-crawl --dry-run" --allowedTools "Read,Write,Edit,Glob,Grep,WebFetch,Bash(python:*)"

post:                  ## post the brief that's already written
	python scripts/post_slack.py

daily: preview post
