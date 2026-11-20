# Daily Memeburn Topic Scout run: crawl/build locally, then Claude does the editorial pass and posts to Slack.
# Scheduled via Windows Task Scheduler (task: MemeburnMorningBrief) at 07:00 local time (this machine is GMT+7,
# matching the writers' workday start minus 1h).
$ErrorActionPreference = "Stop"
$repoDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $repoDir

# Load .env (SLACK_WEBHOOK_URL) into the process environment, if present.
$envFile = Join-Path $repoDir ".env"
if (Test-Path $envFile) {
    Get-Content $envFile | ForEach-Object {
        if ($_ -match '^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*?)\s*$') {
            [System.Environment]::SetEnvironmentVariable($matches[1], $matches[2], "Process")
        }
    }
}

$venvPython = Join-Path $repoDir ".venv\Scripts\python.exe"
$logDir = Join-Path $repoDir "logs"
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$logFile = Join-Path $logDir ("morning-brief-{0}.log" -f (Get-Date -Format "yyyy-MM-dd_HHmmss"))

Start-Transcript -Path $logFile

try {
    & $venvPython scripts\crawl_trends.py
    & $venvPython scripts\fetch_memeburn.py --days 7
    & $venvPython scripts\track_outcomes.py
    & $venvPython scripts\build_candidates.py

    if (-not $env:SLACK_WEBHOOK_URL) {
        Write-Warning "SLACK_WEBHOOK_URL not set (.env missing or empty) -- running Claude in --dry-run mode."
        claude -p "/morning-brief --no-crawl --dry-run" --allowedTools "Read,Write,Edit,Glob,Grep,WebFetch,Bash" --max-turns 40
    } else {
        claude -p "/morning-brief --no-crawl" --allowedTools "Read,Write,Edit,Glob,Grep,WebFetch,Bash" --max-turns 40
    }
} finally {
    Stop-Transcript
}
