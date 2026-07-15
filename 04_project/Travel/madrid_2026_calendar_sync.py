#!/usr/bin/env python3
"""
Madrid Trip 2026 — Google Calendar Sync (idempotent)

Reads existing events, creates new ones, updates changed ones, deletes stale ones.
Events are tagged with #madrid-2026 in the description for safe identification.

Usage:
  python3 madrid_2026_calendar_sync.py           # sync (create / update / delete)
  python3 madrid_2026_calendar_sync.py --dry-run  # preview changes without modifying
"""

import os, pickle, sys
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Auth files shared with training scheduler
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AUTH_DIR = os.path.join(SCRIPT_DIR, "..", "Training_program", "training-calendar-scheduler")
TOKEN_FILE = os.path.join(AUTH_DIR, ".google_token.pickle")
CREDS_FILE = os.path.join(AUTH_DIR, "google_oauth_credentials.json")

SCOPES = ["https://www.googleapis.com/auth/calendar"]
CALENDAR_ID = "boping.m.zhang@gmail.com"
TIMEZONE = "Europe/Madrid"
TAG = "#madrid-2026"

# Fetch window — slightly wider than trip dates for safety
DATE_MIN = "2026-07-04T00:00:00+02:00"
DATE_MAX = "2026-07-10T00:00:00+02:00"

# ─── Itinerary ────────────────────────────────────────────────────────────────

EVENTS = [
    # ── Jul 4 (Sat) — Arrival + Pride Parade ────────────────────────────────
    {
        "summary": "✈️ Arrive Madrid · Check In",
        "location": "Leonardo Boutique Hotel Madrid, Calle de Fortuny 3, Madrid",
        "start": "2026-07-04T09:40:00",
        "end":   "2026-07-04T11:30:00",
        "description": "Land T1 9:40AM. Bus 200 (tap card €1.50) → Avenida de América → Metro → Chamberí. OR taxi fixed rate €30. ✅ Already checked in — drop bags in room.",
    },
    {
        "summary": "Morning Walk — Architecture + Design (Salesas + Fuencarral)",
        "location": "Frontón Beti Jai, Calle del Marqués de Riscal 7, Madrid",
        "start": "2026-07-04T11:30:00",
        "end":   "2026-07-04T13:30:00",
        "description": "Frontón Beti Jai (Marqués de Riscal 7) — free weekends 10AM–2PM only.\nSalesas: Edmmond Studios, Pompeii (Calle Fernando VI).\nFuencarral: Scalpers, Camper (pedestrianised north section).",
    },
    {
        "summary": "Brunch — Roostiq or La Cocina de San Antón",
        "location": "Roostiq, Calle Augusto Figueroa 47, Madrid",
        "start": "2026-07-04T13:30:00",
        "end":   "2026-07-04T14:30:00",
        "description": "Roostiq (Augusto Figueroa 47) or La Cocina de San Antón rooftop (San Antón Market). 5-min walk from Fuencarral.",
    },
    {
        "summary": "Pre-Parade Dinner — Bazaar",
        "location": "Bazaar Restaurant, Calle Libertad 21, Madrid",
        "start": "2026-07-04T15:00:00",
        "end":   "2026-07-04T16:30:00",
        "description": "Eat properly before the parade. Mediterranean, €15–20 menú.",
    },
    {
        "summary": "🏳️‍🌈 Pride Parade (drop-in)",
        "location": "Paseo de Recoletos, Madrid",
        "start": "2026-07-04T19:30:00",
        "end":   "2026-07-04T21:00:00",
        "description": "No need to position early. Walk up to Paseo de Recoletos at 7:30PM — floats pass continuously.\nWatch ~1 hour. Avoid Plaza Colón + Cibeles (crowded). Big floats peak 7–9PM.\nMetro tip: Line 2 (red) from Canal station — faster than Uber during Pride.",
    },
    {
        "summary": "🏳️‍🌈 Pride Nightlife — Chueca",
        "location": "LL Showbar, Calle Pelayo 11, Madrid",
        "start": "2026-07-04T22:00:00",
        "end":   "2026-07-05T02:00:00",
        "description": "LL Showbar (Pelayo 11) → DLRO Live (Pelayo 59) → Teatro Barceló (Barceló 11).\nGran Vía walk between venues.",
    },

    # ── Jul 5 (Sun) — El Rastro + Prado + Pride Closing ─────────────────────
    {
        "summary": "El Rastro Flea Market",
        "location": "El Rastro, Plaza de Cascorro, La Latina, Madrid",
        "start": "2026-07-05T11:00:00",
        "end":   "2026-07-05T13:00:00",
        "description": "Browse Calle Ribera de Curtidores. ⚠️ Peak crowd — keep valuables front-zip or body-close.\nDepart hotel 10:30AM → Metro to La Latina.",
    },
    {
        "summary": "Lunch — Murillo Café or alternatives",
        "location": "Murillo Café, Calle Ruiz de Alarcón 27, Madrid",
        "start": "2026-07-05T13:00:00",
        "end":   "2026-07-05T14:45:00",
        "description": "Mediterranean, vegetables-forward — recovery meal after big parade day.\n⭐ Murillo Café (Ruiz de Alarcón 27) — behind the Prado, burrata + roasted veg.\nAlt: El Imparcial (Duque de Alba 4) — nearest to El Rastro, historic palace building.\nAlt: La Verónica (Moratín 38) — literary quarter, clean fresh Mediterranean.",
    },
    {
        "summary": "🎨 Prado Museum",
        "location": "Museo del Prado, Calle Ruiz de Alarcón 23, Madrid",
        "start": "2026-07-05T15:00:00",
        "end":   "2026-07-05T19:00:00",
        "description": "✅ Ticket booked. Priority: Bosch — Garden of Earthly Delights, Velázquez — Las Meninas, Goya — Black Paintings (Sala 67).",
    },
    {
        "summary": "🏳️‍🌈 Pride Closing Ceremony",
        "location": "Plaza del Rey, Madrid",
        "start": "2026-07-05T19:00:00",
        "end":   "2026-07-05T20:30:00",
        "description": "Free concerts. Emotional conclusion of MADO. 10-min walk from Prado.",
    },
    {
        "summary": "Dinner — Los Gatos or Celso y Manolo",
        "location": "Los Gatos, Calle Jesús 2, Madrid",
        "start": "2026-07-05T20:30:00",
        "end":   "2026-07-05T22:00:00",
        "description": "Los Gatos (Calle Jesús 2) — classic traditional tapas tavern, great atmosphere.\nOR Celso y Manolo (Calle Libertad 1) — near closing ceremony, modern tapas, tomato dishes exceptional.",
    },

    # ── Jul 6 (Mon) — Ballet + Thyssen (free) + Reina Sofía (free) ──────────
    {
        "summary": "💃 Ballet Class — Danza180",
        "location": "Danza180, Calle de Cea Bermúdez 45, Madrid",
        "start": "2026-07-06T09:30:00",
        "end":   "2026-07-06T11:00:00",
        "description": "Danza Clásica Int/Avanz with Marta López Caballero. danza180.com/180-pro/horarios/",
    },
    {
        "summary": "🎨 Thyssen-Bornemisza (free Monday)",
        "location": "Museo Thyssen-Bornemisza, Paseo del Prado 8, Madrid",
        "start": "2026-07-06T12:00:00",
        "end":   "2026-07-06T14:30:00",
        "description": "Permanent collection FREE on Mondays (12–4PM).\nTemp exhibitions ~€8 at door: Carmen Laffón + Ewa Juszkiewicz.\nPriority: Rembrandt, Vermeer, Art Deco.",
    },
    {
        "summary": "Lunch — La Sanabresa",
        "location": "La Sanabresa, Calle Amor de Dios 12, Madrid",
        "start": "2026-07-06T14:30:00",
        "end":   "2026-07-06T15:30:00",
        "description": "Legendary home-style Castilian cooking. Menú del día ~€15–18 including drink. Roast meats, croquettes, stews. Arrive by 2:30PM — popular with locals.\n(Estado Puro — permanently closed)\nAlt: Taberna Los Chanquetes (Moratín 2), Lamucca de Prado (Calle del Prado 16).",
    },
    {
        "summary": "🎨 Reina Sofía (free 7–9PM)",
        "location": "Museo Reina Sofía, Calle Santa Isabel 52, Madrid",
        "start": "2026-07-06T19:00:00",
        "end":   "2026-07-06T21:00:00",
        "description": "✅ Ticket booked (free slot). Priority: Guernica (Picasso), Dalí, Constructivist + Surrealist.",
    },
    {
        "summary": "Dinner — La Latina Tapas Crawl",
        "location": "El Tempranillo, Calle Cava Baja 38, Madrid",
        "start": "2026-07-06T21:30:00",
        "end":   "2026-07-06T23:30:00",
        "description": "Calle Cava Baja:\n• El Tempranillo (no.38) — best wine selection, creative pintxos\n• Casa Lucas (no.30) — famous tostas, cozy wood interior\n• Casa Lucio (no.35) — huevos estrellados over crispy potatoes",
    },

    # ── Jul 7 (Tue) — Toledo Day Trip + Korean Dinner ───────────────────────
    {
        "summary": "🚄 AVE to Toledo",
        "location": "Madrid Puerta de Atocha, Plaza del Emperador Carlos V, Madrid",
        "start": "2026-07-07T09:00:00",
        "end":   "2026-07-07T09:35:00",
        "description": "AVE from Atocha. 30 min, ~€15 each way. Book via renfe.com.",
    },
    {
        "summary": "Toledo — Cathedral, Alcázar, Old Town",
        "location": "Cathedral of Toledo, Calle Cardenal Cisneros 1, Toledo",
        "start": "2026-07-07T09:45:00",
        "end":   "2026-07-07T14:00:00",
        "description": "• Cathedral — Gothic, Baroque sacristy, El Greco in situ\n• El Tránsito Synagogue — Islamic art + Hebrew inscription synthesis\n• Alcázar — fortress, views over Tagus gorge\n• Medieval streets — three-religion city geometry",
    },
    {
        "summary": "Lunch in Toledo",
        "location": "La Malquerida de la Trinidad, Toledo",
        "start": "2026-07-07T14:00:00",
        "end":   "2026-07-07T15:30:00",
        "description": "La Malquerida de la Trinidad (carcamusas pork stew, arrive early)\nOR El Trébol (bomba potato ball, unbeatable prices).",
    },
    {
        "summary": "Mirador del Valle — Panoramic Views",
        "location": "Mirador del Valle, Toledo",
        "start": "2026-07-07T16:00:00",
        "end":   "2026-07-07T18:00:00",
        "description": "Best panoramic view of Toledo. Late afternoon light. Wander back through old town toward station.",
    },
    {
        "summary": "🚄 AVE back to Madrid",
        "location": "Toledo Train Station, Paseo de la Rosa 2, Toledo",
        "start": "2026-07-07T18:00:00",
        "end":   "2026-07-07T18:35:00",
        "description": "Return AVE to Madrid Atocha. ~30 min.",
    },
    {
        "summary": "🍖 Dinner — PURY JOKBAL (Korean Pork Trotters)",
        "location": "PURY JOKBAL, Madrid",
        "start": "2026-07-07T20:00:00",
        "end":   "2026-07-07T21:30:00",
        "description": "Korean jokbal near Callao. From Atocha: Metro ~10 min to Callao.",
    },

    # ── Jul 8 (Wed) — Ballet + Royal Palace + Parents Dinner ─────────────────
    {
        "summary": "💃 Ballet Class — Danza180",
        "location": "Danza180, Calle de Cea Bermúdez 45, Madrid",
        "start": "2026-07-08T09:30:00",
        "end":   "2026-07-08T11:00:00",
        "description": "Danza Clásica Int/Avanz with Marta López Caballero. danza180.com/180-pro/horarios/",
    },
    {
        "summary": "Lunch — Taberna La Buha + La Latina Tapas",
        "location": "Taberna La Buha, La Latina, Madrid",
        "start": "2026-07-08T13:00:00",
        "end":   "2026-07-08T14:30:00",
        "description": "Taberna La Buha (La Latina) — tortilla con queso fundido (流心土豆饼).\nOptional tapas hop on Calle Cava Baja:\n• El Tempranillo (no.38) — best wine, creative pintxos\n• Casa Lucas (no.30) — famous tostas\n• Casa Lucio (no.35) — huevos estrellados",
    },
    {
        "summary": "Plaza de Oriente — Paseo",
        "location": "Plaza de Oriente, Madrid",
        "start": "2026-07-08T14:30:00",
        "end":   "2026-07-08T16:30:00",
        "description": "Leisurely walk around Plaza de Oriente. Rest before Royal Palace queue.",
    },
    {
        "summary": "🏰 Royal Palace — Free Entry (EU Resident)",
        "location": "Palacio Real de Madrid, Calle de Bailén, Madrid",
        "start": "2026-07-08T16:30:00",
        "end":   "2026-07-08T18:30:00",
        "description": "Queue from 4:30PM. Entry from 5PM. Box office closes 6PM.\nBring: Chinese passport + Dutch residence permit.\nSay: \"Soy residente en la Unión Europea.\"\nNearby: Catedral de la Almudena.",
    },
    {
        "summary": "🛍️ Zara Flagship — Edificio España",
        "location": "Zara Edificio España, Plaza de España, Madrid",
        "start": "2026-07-08T18:30:00",
        "end":   "2026-07-08T19:15:00",
        "description": "World's largest Zara, 4 floors, best men's capsule collection + Zara Home. 5-min walk from Royal Palace.",
    },
    {
        "summary": "🍽️ Dinner with Parents",
        "location": "Exe Convention Plaza Madrid, Avenida de Burgos 8, Madrid",
        "start": "2026-07-08T20:00:00",
        "end":   "2026-07-08T22:00:00",
        "description": "Metro Line 10 (Dark Blue) from Plaza de España → Las Tablas (~30 min, ~€1.60). Depart 7:15PM.\nDinner at parents' hotel or nearby Las Tablas spot.\nReturn: Taxi/Uber to Chamberí (~15 min, ~€15–20).",
    },

    # ── Jul 9 (Thu) — Checkout + Museum + Departure ──────────────────────────
    {
        "summary": "Hotel Checkout + Luggage Storage",
        "location": "Leonardo Boutique Hotel Madrid, Calle de Fortuny 3, Madrid",
        "start": "2026-07-09T09:00:00",
        "end":   "2026-07-09T09:30:00",
        "description": "Check out. Store luggage at front desk until departure.",
    },
    {
        "summary": "🎨 Museo Lázaro Galdiano",
        "location": "Museo Lázaro Galdiano, Calle Serrano 122, Madrid",
        "start": "2026-07-09T09:30:00",
        "end":   "2026-07-09T11:30:00",
        "description": "5-min walk from hotel. Private aristocratic collection in a belle époque mansion: Old Masters, decorative arts, ivory, enamel.\n(Alternative: Matadero Madrid — pick one, not both.)\nNote: Museo Sorolla closed for renovation until late 2026.",
    },
    {
        "summary": "Farewell Lunch — Chamberí",
        "location": "Chamberí, Madrid",
        "start": "2026-07-09T12:00:00",
        "end":   "2026-07-09T13:30:00",
        "description": "Leisurely lunch at a local Chamberí spot.",
    },
    {
        "summary": "🚕 Taxi to Airport T4",
        "location": "Leonardo Boutique Hotel Madrid, Calle de Fortuny 3, Madrid",
        "start": "2026-07-09T14:15:00",
        "end":   "2026-07-09T14:45:00",
        "description": "Retrieve luggage at 2:15PM. Taxi departs 2:30PM. ~€30, ~25 min to T4.",
    },
    {
        "summary": "✈️ Depart Madrid → Amsterdam",
        "location": "Adolfo Suárez Madrid-Barajas Airport, Terminal 4, Madrid",
        "start": "2026-07-09T17:20:00",
        "end":   "2026-07-09T19:30:00",
        "description": "Flight 17:20 (Schengen). Arrive Amsterdam ~19:30.",
    },
]

# ─── Auth ─────────────────────────────────────────────────────────────────────

def authenticate():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as f:
            creds = pickle.load(f)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except RefreshError:
                creds = None
        if not creds:
            if not os.path.exists(CREDS_FILE):
                print(f"Error: credentials not found at {CREDS_FILE}")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "wb") as f:
            pickle.dump(creds, f)
    return build("calendar", "v3", credentials=creds)

# ─── Sync ─────────────────────────────────────────────────────────────────────

def fetch_madrid_events(service):
    """Fetch all events in trip window that carry TAG."""
    items, page_token = [], None
    while True:
        resp = service.events().list(
            calendarId=CALENDAR_ID,
            timeMin=DATE_MIN,
            timeMax=DATE_MAX,
            singleEvents=True,
            orderBy="startTime",
            pageToken=page_token,
        ).execute()
        items.extend(resp.get("items", []))
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    return [ev for ev in items if TAG in (ev.get("description") or "")]


def build_body(ev):
    desc = ev.get("description", "").rstrip()
    if TAG not in desc:
        desc = f"{desc}\n\n{TAG}" if desc else TAG
    return {
        "summary": ev["summary"],
        "location": ev.get("location", ""),
        "description": desc,
        "start": {"dateTime": ev["start"], "timeZone": TIMEZONE},
        "end":   {"dateTime": ev["end"],   "timeZone": TIMEZONE},
    }


def strip_tz(s):
    """Strip timezone suffix for datetime comparison."""
    return s[:19] if s else ""


def needs_update(existing_gcal, desired_ev):
    return (
        strip_tz(existing_gcal.get("start", {}).get("dateTime", "")) != strip_tz(desired_ev["start"])
        or strip_tz(existing_gcal.get("end",   {}).get("dateTime", "")) != strip_tz(desired_ev["end"])
        or existing_gcal.get("location", "") != desired_ev.get("location", "")
    )


def sync(service, dry_run=False):
    print("Fetching existing Madrid events from Google Calendar...")
    existing = fetch_madrid_events(service)
    by_summary = {ev["summary"]: ev for ev in existing}
    desired = {ev["summary"]: ev for ev in EVENTS}

    print(f"Found {len(existing)} tagged events in calendar. Desired: {len(desired)} events.\n")

    created = updated = deleted = skipped = 0

    for summary, ev in desired.items():
        body = build_body(ev)
        if summary in by_summary:
            if needs_update(by_summary[summary], ev):
                if not dry_run:
                    service.events().update(
                        calendarId=CALENDAR_ID,
                        eventId=by_summary[summary]["id"],
                        body=body,
                    ).execute()
                print(f"  ↺ UPDATE  {summary}")
                updated += 1
            else:
                print(f"  · skip    {summary}")
                skipped += 1
        else:
            if not dry_run:
                service.events().insert(calendarId=CALENDAR_ID, body=body).execute()
            print(f"  ✅ CREATE  {summary}")
            created += 1

    # Delete events that were pushed before but are no longer in EVENTS
    for summary, ev in by_summary.items():
        if summary not in desired:
            if not dry_run:
                service.events().delete(calendarId=CALENDAR_ID, eventId=ev["id"]).execute()
            print(f"  🗑  DELETE  {summary}")
            deleted += 1

    prefix = "[DRY RUN] " if dry_run else ""
    print(f"\n{prefix}Done — ✅ created {created}  ↺ updated {updated}  🗑 deleted {deleted}  · skipped {skipped}")


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    if dry_run:
        print("=== DRY RUN — no changes will be made ===\n")
    service = authenticate()
    sync(service, dry_run=dry_run)
