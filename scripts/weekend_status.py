#!/usr/bin/env python3
"""
weekend_status.py — Classify upcoming weekends as available / occupied / at-risk.

Feeds the "Weekend Allocation" section of 00_system/_priority.md. Reads three
Google calendars (read-only) and applies the rules agreed 2026-09-03:

  Location calendars (AMS / DH) — a weekend is:
    DH present            -> 🔒 occupied  (away at Jeroen's; no big-block work)
    AMS present only      -> 🟢 available (home)
    nothing present       -> ⚠️ unplanned (treated as at-risk, not as free —
                             an empty location calendar means undecided, and
                             undecided weekends are the ones that get eaten)

  Main calendar — cross-check for shows/performances. A show on a 🟢 weekend
  downgrades it to ⚠️ (a show typically eats the surrounding block).

Only events whose title is exactly "AMS" or "DH" count as location markers —
same rule as the app's /api/location/plan (Session 27).

Usage:
  python3 scripts/weekend_status.py                # next 8 weekends, table
  python3 scripts/weekend_status.py --weeks 12
  python3 scripts/weekend_status.py --json
  python3 scripts/weekend_status.py --from 2026-09-01

Auth: needs a Google OAuth client file + token cached next to this script.
  CREDS: scripts/.google_oauth_credentials.json   (gitignored)
  TOKEN: scripts/.google_token.pickle             (gitignored, auto-created)
First run opens a browser for consent; after that it refreshes silently.
Scope is calendar.readonly — this script never writes to any calendar.
"""

from __future__ import annotations

import argparse
import json
import os
import pickle
import sys
from datetime import datetime, timedelta, date

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(SCRIPT_DIR, ".google_token.pickle")
CREDS_FILE = os.path.join(SCRIPT_DIR, ".google_oauth_credentials.json")

# Read-only: this script must never mutate a calendar.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

MAIN_CALENDAR_ID = "boping.m.zhang@gmail.com"
LOCATION_CALENDARS = {
    "AMS": "ab70e18afc46e8cabc4ce4f0f84ba4bf3ee2d5775428ed68a42454f9cb8de668@group.calendar.google.com",
    "DH":  "d11c4ce62cf20d3ac8edbcbf868ab43c095afc5bf3cadfae5d28337225cf5a9a@group.calendar.google.com",
}

# Main-calendar titles that signal a show / performance eating the weekend.
SHOW_KEYWORDS = [
    "show", "performance", "premiere", "ballet", "opera", "concert",
    "theatre", "theater", "dance", "festival", "gala", "recital",
    "演出", "首演", "音乐会", "芭蕾", "剧场", "音乐节",
]

# Titles that are routine and should NOT downgrade a weekend.
IGNORE_KEYWORDS = [
    "dinner", "lunch", "breakfast", "shower", "bath", "sauna",
    "launch seq", "shutdown seq", "gym", "reformer", "stretch",
]


def authenticate():
    """Return an authorized Calendar service, or exit with setup instructions."""
    try:
        from google.auth.transport.requests import Request
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
    except ModuleNotFoundError as e:
        sys.exit(
            f"Missing dependency: {e.name}\n"
            "Install with:  /usr/bin/python3 -m pip install --user "
            "google-api-python-client google-auth-oauthlib"
        )

    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as f:
            creds = pickle.load(f)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDS_FILE):
                sys.exit(
                    "No Google credentials found.\n\n"
                    f"Expected OAuth client file at:\n  {CREDS_FILE}\n\n"
                    "To create one:\n"
                    "  1. console.cloud.google.com -> APIs & Services -> Credentials\n"
                    "  2. Create OAuth client ID -> Desktop app\n"
                    "  3. Download the JSON and save it to the path above\n"
                    "  4. Re-run this script; a browser opens once for consent\n\n"
                    "Scope requested is calendar.readonly (no write access)."
                )
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "wb") as f:
            pickle.dump(creds, f)

    return build("calendar", "v3", credentials=creds)


def this_or_next_friday(from_date: date) -> date:
    """Snap to Friday — same convention as the app's snapToFriday."""
    return from_date + timedelta(days=(4 - from_date.weekday()) % 7)


def fetch(service, calendar_id: str, start: date, end: date) -> list[dict]:
    try:
        result = service.events().list(
            calendarId=calendar_id,
            timeMin=datetime.combine(start, datetime.min.time()).isoformat() + "Z",
            timeMax=datetime.combine(end, datetime.max.time()).isoformat() + "Z",
            singleEvents=True,
            orderBy="startTime",
        ).execute()
        return result.get("items", [])
    except Exception as e:
        print(f"  warning: could not read {calendar_id[:24]}…: {e}", file=sys.stderr)
        return []


def event_date(event: dict) -> date | None:
    raw = event.get("start", {}).get("dateTime") or event.get("start", {}).get("date")
    if not raw:
        return None
    try:
        return datetime.fromisoformat(raw.replace("Z", "")).date()
    except ValueError:
        return None


def is_show(title: str) -> bool:
    t = title.lower()
    if any(k in t for k in IGNORE_KEYWORDS):
        return False
    return any(k in t for k in SHOW_KEYWORDS)


def classify(weeks: int, start_from: date) -> list[dict]:
    service = authenticate()

    first_friday = this_or_next_friday(start_from)
    fridays = [first_friday + timedelta(weeks=i) for i in range(weeks)]
    window_end = fridays[-1] + timedelta(days=2)

    # Location markers, per calendar
    location_hits: dict[date, set[str]] = {}
    for loc, cal_id in LOCATION_CALENDARS.items():
        for ev in fetch(service, cal_id, first_friday, window_end):
            # Only exact "AMS"/"DH" titles are location markers (app parity)
            if (ev.get("summary") or "").strip() not in ("AMS", "DH"):
                continue
            d = event_date(ev)
            if d:
                location_hits.setdefault(d, set()).add(loc)

    # Shows on the main calendar
    shows: dict[date, list[str]] = {}
    for ev in fetch(service, MAIN_CALENDAR_ID, first_friday, window_end):
        title = (ev.get("summary") or "").strip()
        if not title or not is_show(title):
            continue
        d = event_date(ev)
        if d:
            shows.setdefault(d, []).append(title)

    out = []
    for fri in fridays:
        days = [fri, fri + timedelta(days=1), fri + timedelta(days=2)]
        locs: set[str] = set()
        for d in days:
            locs |= location_hits.get(d, set())
        weekend_shows = [s for d in days for s in shows.get(d, [])]

        if "DH" in locs:
            status, reason = "occupied", "DH — 在海牙"
        elif "AMS" in locs and weekend_shows:
            status, reason = "at_risk", f"AMS，但有演出：{', '.join(weekend_shows)}"
        elif "AMS" in locs:
            status, reason = "available", "AMS — 在家"
        elif weekend_shows:
            status, reason = "occupied", f"演出：{', '.join(weekend_shows)}"
        else:
            status, reason = "unplanned", "location calendar 未填 — 视为待定"

        out.append({
            "weekend_start": fri.isoformat(),
            "label": f"{fri.strftime('%-m/%-d')}–{(fri + timedelta(days=2)).strftime('%-d')}",
            "status": status,
            "locations": sorted(locs),
            "shows": weekend_shows,
            "reason": reason,
        })
    return out


ICON = {
    "available": "🟢 可用",
    "at_risk":   "⚠️ 待定",
    "unplanned": "⚠️ 未填",
    "occupied":  "🔒 已占用",
}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--weeks", type=int, default=8, help="how many weekends ahead (default 8)")
    ap.add_argument("--from", dest="from_date", help="start date YYYY-MM-DD (default today)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args()

    start = date.fromisoformat(args.from_date) if args.from_date else date.today()
    rows = classify(args.weeks, start)

    if args.json:
        print(json.dumps(rows, indent=2, ensure_ascii=False))
        return

    print(f"\n周末状态 — 未来 {args.weeks} 个周末（起 {rows[0]['weekend_start']}）\n")
    print(f"{'周末':<12} {'状态':<12} 依据")
    print("─" * 76)
    for r in rows:
        print(f"{r['label']:<12} {ICON[r['status']]:<12} {r['reason']}")

    free = [r for r in rows if r["status"] == "available"]
    maybe = [r for r in rows if r["status"] in ("at_risk", "unplanned")]
    print(f"\n🟢 可用 {len(free)} 个 · ⚠️ 待定 {len(maybe)} 个 · "
          f"🔒 已占用 {len(rows) - len(free) - len(maybe)} 个")
    print("\n分配规则：每个 🟢 只排一件大块事项；⚠️ 不排，留作缓冲。")
    print("详见 00_system/_priority.md → Weekend Allocation")


if __name__ == "__main__":
    main()
