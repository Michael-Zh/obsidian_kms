#!/usr/bin/env python3
"""
Danseur Noble Training Program — Google Calendar Scheduler (Interactive)

Class durations:
- Gym: 120 min
- Dance classes (Ballet/Jazz/Contemporary): 90 min
- Mysore/Ashtanga Led: 90 min
- Reformer: 50 min
- Iyengar: 75 min (Wed/Thu), 90 min (Mon/Sat)
- Yin: 75 min
"""

import os, pickle, json
from datetime import datetime, timedelta
from typing import Dict, List
import sys

from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(SCRIPT_DIR, ".google_token.pickle")
MAIN_CALENDAR_ID = "boping.m.zhang@gmail.com"
TRAINING_CALENDAR_ID = "ea1cec57657387a2fef264ce336796fd22b6b6696591106f58742db91335ef0c@group.calendar.google.com"
CREDS_FILE = os.path.join(SCRIPT_DIR, "google_oauth_credentials.json")
SCOPES = ["https://www.googleapis.com/auth/calendar"]
TIMEZONE = "Europe/Amsterdam"


class TrainingScheduler:
    def __init__(self):
        self.service = None
        self.creds = None
        self._authenticate()
        self.week_plan = []
        self.dropped_plan = []
        self.conflicts = {}
        self.week_start = None
        self.week_end = None

    def _authenticate(self):
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, "rb") as f:
                self.creds = pickle.load(f)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                try:
                    self.creds.refresh(Request())
                except RefreshError:
                    self.creds = None
            if not self.creds:
                if not os.path.exists(CREDS_FILE):
                    print(f"Error: OAuth credentials file not found at {CREDS_FILE}")
                    sys.exit(1)
                flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
                self.creds = flow.run_local_server(port=0)
            with open(TOKEN_FILE, "wb") as f:
                pickle.dump(self.creds, f)
        self.service = build("calendar", "v3", credentials=self.creds)

    def fetch_events(self, calendar_id: str, start_date: datetime, end_date: datetime) -> List[Dict]:
        start_iso = start_date.isoformat() + "Z"
        end_iso = end_date.isoformat() + "Z"
        events_result = self.service.events().list(
            calendarId=calendar_id, timeMin=start_iso, timeMax=end_iso, singleEvents=True, orderBy="startTime"
        ).execute()
        return events_result.get("items", [])

    def find_unmovable_events(self, main_events: List[Dict], start_date: datetime, end_date: datetime) -> Dict:
        conflicts = {}
        for event in main_events:
            raw_start = event.get("start", {}).get("dateTime") or event.get("start", {}).get("date")
            raw_end = event.get("end", {}).get("dateTime") or event.get("end", {}).get("date")
            if not raw_start:
                continue
            try:
                event_dt = datetime.fromisoformat(raw_start.replace("Z", "")).date()
            except:
                continue
            if not (start_date.date() <= event_dt <= end_date.date()):
                continue
            day_key = event_dt.isoformat()
            if day_key not in conflicts:
                conflicts[day_key] = []
            entry = {"title": event.get("summary", "Event")}
            try:
                entry["start"] = datetime.fromisoformat(raw_start.replace("Z", "")).replace(tzinfo=None)
                entry["end"] = datetime.fromisoformat(raw_end.replace("Z", "")).replace(tzinfo=None)
            except:
                entry["start"] = None
                entry["end"] = None
            conflicts[day_key].append(entry)
        return conflicts

    SOFT_KEYWORDS = ["dinner", "lunch", "shower", "bath", "breakfast", "sauna",
                     "launch seq", "shutdown seq"]

    def _is_soft(self, title: str) -> bool:
        t = title.lower()
        return any(kw in t for kw in self.SOFT_KEYWORDS)

    def _classify_conflicts(self, day_key: str, start: datetime, end: datetime):
        hard, soft = [], []
        for ev in self.conflicts.get(day_key, []):
            if ev["start"] is None:
                continue
            if start < ev["end"] and end > ev["start"]:
                (soft if self._is_soft(ev["title"]) else hard).append(ev)
        return hard, soft

    def _find_alt_slot(self, day: datetime, duration_mins: int, earliest_hour: int = 7, latest_hour: int = 23):
        duration = timedelta(minutes=duration_mins)
        dk = day.date().isoformat()

        def next_30(dt):
            if dt.minute % 30 == 0:
                return dt.replace(second=0, microsecond=0)
            return (dt + timedelta(minutes=30 - dt.minute % 30)).replace(second=0, microsecond=0)

        slot = next_30(day.replace(hour=earliest_hour, minute=0, second=0, microsecond=0))
        limit = day.replace(hour=latest_hour, minute=0, second=0, microsecond=0)
        while slot + duration <= limit:
            hard, soft = self._classify_conflicts(dk, slot, slot + duration)
            if not hard:
                return slot, slot + duration, soft
            slot = next_30(max(ev["end"] for ev in hard))
        return None, None, []

    def get_next_week(self):
        today = datetime.now()
        days_until_sunday = (6 - today.weekday()) % 7
        if days_until_sunday == 0:
            days_until_sunday = 7
        week_start = today + timedelta(days=days_until_sunday)
        week_end = week_start + timedelta(days=6)
        return week_start, week_end

    def propose_week(self, start_date: datetime, end_date: datetime, conflicts: Dict) -> List[Dict]:
        week_plan = []

        def dk(d): return d.date().isoformat()

        def schedule(day_name, d, title, h, m, duration_mins, location, fixed=True):
            s = d.replace(hour=h, minute=m, second=0, microsecond=0)
            e = s + timedelta(minutes=duration_mins)
            hard, soft = self._classify_conflicts(dk(d), s, e)
            # Also check against already-planned sessions this week
            for planned in week_plan:
                if planned.get("date", "")[:10] == dk(d):
                    p_s = datetime.fromisoformat(planned["start"])
                    p_e = datetime.fromisoformat(planned["end"])
                    if s < p_e and e > p_s:
                        hard.append({"title": planned["title"], "start": p_s, "end": p_e})
            if not hard:
                entry = {"day": day_name, "date": d.isoformat(), "title": title,
                         "start": s.isoformat(), "end": e.isoformat(), "location": location}
                if soft:
                    entry["move_suggestions"] = [
                        f"Move '{ev['title']}' ({ev['start'].strftime('%H:%M')}) to after {e.strftime('%H:%M')}"
                        for ev in soft
                    ]
                week_plan.append(entry)
                return True
            if not fixed:
                alt_s, alt_e, alt_soft = self._find_alt_slot(d, duration_mins)
                if alt_s:
                    entry = {"day": day_name, "date": d.isoformat(), "title": title,
                             "start": alt_s.isoformat(), "end": alt_e.isoformat(),
                             "location": location, "rescheduled": True,
                             "original_time": f"{h:02d}:{m:02d}"}
                    if alt_soft:
                        entry["move_suggestions"] = [
                            f"Move '{ev['title']}' ({ev['start'].strftime('%H:%M')}) to after {alt_e.strftime('%H:%M')}"
                            for ev in alt_soft
                        ]
                    week_plan.append(entry)
                    return True
            # Record drop with reason
            conflict_names = ", ".join(dict.fromkeys(ev["title"] for ev in hard))
            self.dropped_plan.append({
                "title": title, "day": day_name,
                "preferred_time": f"{h:02d}:{m:02d}",
                "reason": f"conflict: {conflict_names}",
            })
            return False

        sun = start_date
        mon = start_date + timedelta(days=1)
        tue = start_date + timedelta(days=2)
        wed = start_date + timedelta(days=3)
        thu = start_date + timedelta(days=4)
        fri = start_date + timedelta(days=5)

        schedule("Sunday",    sun, "ADC Ballet",                   16,  0,  90, "ADC")
        schedule("Monday",    mon, "Gym - Back/Leg/Arm",           15,  0, 120, "Gym",  fixed=False)
        schedule("Monday",    mon, "Iyengar Yoga",                 20, 15,  75, "Yoga")
        # Mon 19:00 ADC Ballet is a BACKUP only (has pianist) — only schedule if Sun ballet is blocked
        schedule("Tuesday",   tue, "Gym - Chest/Shoulder",         15,  0, 120, "Gym",  fixed=False)
        schedule("Tuesday",   tue, "ADC Improv Contemporary",      18, 45,  90, "ADC",  fixed=False)  # temporary arrangement
        schedule("Thursday",  thu, "Mysore Ashtanga",              7,  0,  90, "Bluebird West")
        # Ballet: Thu 17:30 primary, Fri fallback
        if not schedule("Thursday", thu, "ADC Ballet",            17, 30,  90, "ADC"):
            schedule("Friday",  fri, "ADC Ballet",                17, 30,  90, "ADC")

        # Swimming: backup on office days (Mon, Wed) that have no sessions yet
        for office_day, office_name in [(mon, "Monday"), (wed, "Wednesday")]:
            if not any(e["date"][:10] == dk(office_day) for e in week_plan):
                schedule(office_name, office_day, "Swimming", 7, 30, 60, "Pool")

        week_plan.sort(key=lambda x: x["start"])

        return week_plan

    def display_plan(self, week_plan: List[Dict], conflicts: Dict):
        print("\n" + "=" * 70)
        print("WEEKLY PLAN")
        print("=" * 70)
        current_day = None
        for item in week_plan:
            if item["day"] != current_day:
                current_day = item["day"]
                day_date = datetime.fromisoformat(item["date"]).strftime("%a, %b %d")
                print(f"\n{current_day.upper()} ({day_date})")
                print("-" * 70)
            start_time = datetime.fromisoformat(item["start"]).strftime("%H:%M")
            end_time = datetime.fromisoformat(item["end"]).strftime("%H:%M")
            flag = " [RESCHEDULED]" if item.get("rescheduled") else ""
            print(f"  {start_time}-{end_time}  {item['title']:30s}  [{item['location']}]{flag}")
            for suggestion in item.get("move_suggestions", []):
                print(f"    ⚠ {suggestion}")
        print("\n" + "=" * 70)

    def to_json(self) -> str:
        def serialize(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            raise TypeError(f"Type {type(obj)} not serializable")
        conflicts_out = {
            day: [{"title": e["title"], "start": e["start"], "end": e["end"]} for e in evts]
            for day, evts in self.conflicts.items()
        }
        return json.dumps({"conflicts": conflicts_out, "plan": self.week_plan}, indent=2, default=serialize)

    def push_to_calendar(self):
        print(f"\nPushing {len(self.week_plan)} events to training calendar...")
        for item in self.week_plan:
            event = {
                "summary": item["title"],
                "location": item.get("location", ""),
                "start": {"dateTime": item["start"], "timeZone": TIMEZONE},
                "end":   {"dateTime": item["end"],   "timeZone": TIMEZONE},
            }
            if item.get("move_suggestions"):
                event["description"] = "\n".join(item["move_suggestions"])
            self.service.events().insert(
                calendarId=TRAINING_CALENDAR_ID, body=event
            ).execute()
            start = datetime.fromisoformat(item["start"]).strftime("%a %b %d %H:%M")
            print(f"  ✓ {item['title']} — {start}")
        print("Done.")

    def fetch_past_weeks(self, n: int = 4) -> List[Dict]:
        today = datetime.now()
        days_to_sat = (today.weekday() - 5) % 7
        last_sat = today - timedelta(days=days_to_sat)
        weeks = []
        for i in range(n):
            week_end = (last_sat - timedelta(weeks=i)).replace(hour=23, minute=59, second=59)
            week_start = (week_end - timedelta(days=6)).replace(hour=0, minute=0, second=0)
            raw = self.fetch_events(TRAINING_CALENDAR_ID, week_start, week_end)
            events = []
            for ev in raw:
                rs = ev.get("start", {}).get("dateTime") or ev.get("start", {}).get("date", "")
                re = ev.get("end",   {}).get("dateTime") or ev.get("end",   {}).get("date", "")
                events.append({
                    "title": ev.get("summary", ""),
                    "date":  rs[:10],
                    "start": rs[11:16] if "T" in rs else "",
                    "end":   re[11:16] if re and "T" in re else "",
                })
            weeks.append({
                "week": f"{week_start.strftime('%Y-%m-%d')} → {week_end.strftime('%Y-%m-%d')}",
                "training_events": events,
            })
        return weeks

    def review_past_weeks(self, n: int = 4):
        print(json.dumps({"past_training_weeks": self.fetch_past_weeks(n)}, indent=2))

    def run(self, output_json: bool = False, push: bool = False, review: bool = False):
        if review:
            self.review_past_weeks()
            return

        print("Loading calendars...\n")
        self.week_start, self.week_end = self.get_next_week()
        print(f"Planning: {self.week_start.strftime('%a %b %d')} - {self.week_end.strftime('%a %b %d')}")

        fetch_start = self.week_start - timedelta(days=1)
        fetch_end = self.week_end + timedelta(days=1)
        main_events = self.fetch_events(MAIN_CALENDAR_ID, fetch_start, fetch_end)
        self.conflicts = self.find_unmovable_events(main_events, self.week_start, self.week_end)

        if not output_json and self.conflicts:
            print("\nUNMOVABLE EVENTS:")
            for day, events in sorted(self.conflicts.items()):
                day_obj = datetime.fromisoformat(day)
                print(f"  {day_obj.strftime('%A')}: {', '.join(e['title'] for e in events)}")

        self.week_plan = self.propose_week(self.week_start, self.week_end, self.conflicts)

        if output_json:
            print(self.to_json())
            return

        self.display_plan(self.week_plan, self.conflicts)

        if push:
            self.push_to_calendar()


if __name__ == "__main__":
    output_json = "--json" in sys.argv
    push = "--push" in sys.argv
    review = "--review" in sys.argv
    today = "--today" in sys.argv

    if today:
        from datetime import date, time as dtime
        import pytz
        tz = pytz.timezone(TIMEZONE)
        now = datetime.now(tz)
        start = datetime.combine(now.date(), dtime.min)
        end = datetime.combine(now.date(), dtime.max)
        scheduler = TrainingScheduler()
        training_events = scheduler.fetch_events(TRAINING_CALENDAR_ID, start, end)
        main_events = scheduler.fetch_events(MAIN_CALENDAR_ID, start, end)
        def simplify(events):
            result = []
            for e in events:
                result.append({
                    "title": e.get("summary", ""),
                    "start": e.get("start", {}).get("dateTime") or e.get("start", {}).get("date", ""),
                    "end": e.get("end", {}).get("dateTime") or e.get("end", {}).get("date", ""),
                })
            return result
        print(json.dumps({
            "date": now.strftime("%Y-%m-%d"),
            "training_events": simplify(training_events),
            "main_events": simplify(main_events)
        }, ensure_ascii=False, indent=2))
    else:
        scheduler = TrainingScheduler()
        scheduler.run(output_json=output_json, push=push, review=review)
