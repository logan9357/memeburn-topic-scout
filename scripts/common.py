"""Shared helpers: paths, config, dates, HTTP, text tokenisation."""
from __future__ import annotations

import calendar
import datetime as dt
import html
import json
import re
from email.utils import parsedate_to_datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import requests
import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
CONFIG = ROOT / "config"
KNOWLEDGE = ROOT / "knowledge"

USER_AGENT = "MemeburnTopicScout/1.0 (editorial trend research)"


def load_yaml(name: str) -> dict:
    return yaml.safe_load((CONFIG / name).read_text(encoding="utf-8")) or {}


SETTINGS = load_yaml("settings.yaml")
TZ = ZoneInfo(SETTINGS.get("timezone", "Africa/Johannesburg"))


def now_utc() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def today_str() -> str:
    return dt.datetime.now(TZ).date().isoformat()


def session() -> requests.Session:
    s = requests.Session()
    s.headers["User-Agent"] = USER_AGENT
    return s


def read_json(path: Path, default=None):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def write_json(path: Path, obj) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")


def parse_date(value) -> dt.datetime | None:
    """Parse ISO strings, RFC 822 strings, unix timestamps or time.struct_time into aware UTC datetimes."""
    if value is None or value == "":
        return None
    try:
        if isinstance(value, (int, float)):
            return dt.datetime.fromtimestamp(value, dt.timezone.utc)
        if hasattr(value, "tm_year"):
            return dt.datetime.fromtimestamp(calendar.timegm(value), dt.timezone.utc)
        text = str(value).strip()
        try:
            d = dt.datetime.fromisoformat(text.replace("Z", "+00:00"))
        except ValueError:
            d = parsedate_to_datetime(text)
        if d.tzinfo is None:
            d = d.replace(tzinfo=dt.timezone.utc)
        return d.astimezone(dt.timezone.utc)
    except (ValueError, TypeError, OverflowError):
        return None


def clean_text(value: str, limit: int = 400) -> str:
    text = re.sub(r"<[^>]+>", " ", value or "")
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:limit]


STOPWORDS = set(
    """a an the and or but of to in on for with at by from is are was were be been being as it its this that
    these those after before over into onto out up down new how why what who whom which when where will would
    can could may might should you your we our they their he she his her them us says said say report reports
    reportedly here there just now get gets got more most than then also about amid vs via first latest
    week today year years day days one two three all any not no yes off top best""".split()
)


def tokens(text: str) -> set[str]:
    words = re.findall(r"[a-z0-9][a-z0-9+\-.]*[a-z0-9+]|[a-z0-9]", (text or "").lower())
    return {w for w in words if w not in STOPWORDS and (len(w) > 2 or w.isdigit() or w in {"ai", "5g", "ev"})}


def jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def similar(a: set, b: set, threshold: float = 0.3, min_overlap: int = 2) -> bool:
    small, big = (a, b) if len(a) <= len(b) else (b, a)
    # short search queries ("whatsapp down" -> {"whatsapp"}) match any headline that contains them
    if 1 <= len(small) <= 2 and small <= big and max(len(w) for w in small) >= 4:
        return True
    overlap = len(a & b)
    return overlap >= min_overlap and (jaccard(a, b) >= threshold or overlap >= 4)


def keyword_hits(text: str, keywords: list[str]) -> list[str]:
    low = f" {(text or '').lower()} "
    hits = []
    for kw in keywords:
        if re.search(r"(?<![a-z0-9])" + re.escape(kw.lower()) + r"(?![a-z0-9])", low):
            hits.append(kw)
    return hits
