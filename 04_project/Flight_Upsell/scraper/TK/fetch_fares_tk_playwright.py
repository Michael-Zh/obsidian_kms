"""
Turkish Airlines Fare Fetcher — Fully Automated
================================================
Connects to your existing Chrome session, fills the entire booking form
(trip type, origin, destination, date via calendar widget), waits for
results, expands all fare tier dropdowns, and saves the HTML.

SETUP:
  1. Launch Chrome with remote debugging:
     Mac:
       /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
         --remote-debugging-port=9222 \
         --user-data-dir="/tmp/chrome-tk-session"

  2. In that Chrome, navigate to: https://www.turkishairlines.com/en-de/

  3. Edit SEARCHES below, then run: python fetch_fares_tk_playwright.py

  4. If a CAPTCHA appears, solve it manually — the script waits.
"""

import asyncio
import calendar as _calendar
import csv as _csv
import re
import sys
from pathlib import Path
from datetime import date as _date, datetime, timedelta as _td
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

CDP_URL    = "http://localhost:9222"
TK_HOME    = "https://www.turkishairlines.com/en-de/"
OUTPUT_DIR = "TK"
RESULTS_TIMEOUT = 60   # seconds to wait for the results page to load
MAX_RETRIES  = 3       # how many times to retry a failed search
RETRY_DELAY  = 5       # seconds to wait between retries

# Routes CSV — set to a file path to load routes dynamically, or None to use
# the hardcoded _ROUTES fallback below.
ROUTES_CSV = "routes.csv"

# Hardcoded fallback routes (used when ROUTES_CSV is None or file not found)
_ROUTES = [("IST", "NAV"), ("IST", "AYT"), ("IST", "ASR"), ("IST", "VAN")]


# ─────────────────────────────────────────────────────────────────────────────
# Dynamic date + search generation
# ─────────────────────────────────────────────────────────────────────────────

def generate_search_dates():
    """
    Returns 3 departure dates:
      today + 2 months → nearest upcoming Monday
      today + 3 months → nearest upcoming Wednesday
      today + 4 months → nearest upcoming Saturday
    If the anchor date already falls on the target weekday, it is used as-is.
    Returns a sorted list of YYYY-MM-DD strings.
    """
    today = _date.today()
    anchors = [
        (2, 0),   # +2 months → Monday
        (3, 2),   # +3 months → Wednesday
        (4, 5),   # +4 months → Saturday
    ]
    results = []
    for months_ahead, target_wd in anchors:
        year  = today.year + (today.month + months_ahead - 1) // 12
        month = (today.month + months_ahead - 1) % 12 + 1
        max_day = _calendar.monthrange(year, month)[1]
        anchor = _date(year, month, min(today.day, max_day))
        days_ahead = (target_wd - anchor.weekday()) % 7
        results.append((anchor + _td(days=days_ahead)).strftime("%Y-%m-%d"))
    return sorted(results)


def load_routes(csv_path=None, airline_code="TK"):
    """
    Load routes from a CSV with columns: airline, departure, arrival.
    Filters to rows matching airline_code.
    Falls back to _ROUTES if csv_path is None or the file is missing.
    """
    if csv_path:
        try:
            routes = []
            with open(csv_path, newline="", encoding="utf-8") as f:
                reader = _csv.DictReader(f)
                for row in reader:
                    if row.get("airline", "").strip().upper() == airline_code.upper():
                        dep = row["departure"].strip().upper()
                        arr = row["arrival"].strip().upper()
                        routes.append((dep, arr))
            if routes:
                print(f"✓ Loaded {len(routes)} {airline_code} routes from {csv_path}")
                return routes
            print(f"⚠ No {airline_code} routes found in {csv_path} — using defaults")
        except FileNotFoundError:
            print(f"⚠ Routes file not found: {csv_path} — using defaults")
        except Exception as e:
            print(f"⚠ Could not read {csv_path}: {e} — using defaults")
    return list(_ROUTES)


def build_searches(routes_csv=ROUTES_CSV):
    """
    Build the full search list from routes + dynamically generated dates.

    Date rule  : today+2m → nearest Mon, today+3m → nearest Wed, today+4m → nearest Sat
    OW rule    : 2 pax, all 3 dates
    RT rule    : 1 pax, all 3 dates as departure, return = departure + 6 days
                 (Mon → Sun, Wed → Tue, Sat → Fri)
    """
    routes  = load_routes(routes_csv)
    dates   = generate_search_dates()
    searches = []

    for orig, dest in routes:
        for d in dates:
            dep = _date.fromisoformat(d)
            ret = (dep + _td(days=6)).strftime("%Y-%m-%d")

            # One-way — 2 pax
            searches.append({
                "origin": orig, "destination": dest,
                "date": d, "trip_type": "OW", "pax": 2,
            })
            # Round-trip — 1 pax, return 6 days later
            searches.append({
                "origin": orig, "destination": dest,
                "date": d, "return_date": ret, "trip_type": "RT", "pax": 1,
            })

    return searches


SEARCHES = build_searches()

# ─────────────────────────────────────────────────────────────────────────────
# Airport → Country mapping for the TK country/region modal
# ─────────────────────────────────────────────────────────────────────────────

AIRPORT_COUNTRY = {
    # Germany
    "FRA": "Germany", "MUC": "Germany", "BER": "Germany", "HAM": "Germany",
    "DUS": "Germany", "STR": "Germany", "NUE": "Germany", "CGN": "Germany",
    "LEJ": "Germany", "HHN": "Germany",
    # Turkey
    "IST": "Türkiye", "SAW": "Türkiye", "ADB": "Türkiye", "AYT": "Türkiye",
    "ESB": "Türkiye", "ADA": "Türkiye", "TZX": "Türkiye", "GZT": "Türkiye",
    "KYA": "Türkiye", "VAN": "Türkiye", "ERZ": "Türkiye", "SZF": "Türkiye",
    "NAV": "Türkiye", "ASR": "Türkiye", "MLX": "Türkiye", "DIY": "Türkiye",
    # France
    "CDG": "France", "ORY": "France", "NCE": "France", "LYS": "France",
    "MRS": "France", "BOD": "France",
    # UK
    "LHR": "United Kingdom", "LGW": "United Kingdom", "MAN": "United Kingdom",
    "STN": "United Kingdom", "LTN": "United Kingdom", "EDI": "United Kingdom",
    "BHX": "United Kingdom", "GLA": "United Kingdom",
    # Netherlands
    "AMS": "Netherlands",
    # Switzerland
    "ZRH": "Switzerland", "GVA": "Switzerland", "BSL": "Switzerland",
    # Austria
    "VIE": "Austria", "SZG": "Austria", "INN": "Austria",
    # Belgium
    "BRU": "Belgium", "CRL": "Belgium",
    # Spain
    "MAD": "Spain", "BCN": "Spain", "AGP": "Spain", "VLC": "Spain",
    "SVQ": "Spain", "PMI": "Spain", "TFS": "Spain",
    # Italy
    "FCO": "Italy", "MXP": "Italy", "VCE": "Italy", "NAP": "Italy",
    "BLQ": "Italy", "CTA": "Italy", "PMO": "Italy",
    # Greece
    "ATH": "Greece", "SKG": "Greece", "HER": "Greece", "RHO": "Greece",
    # USA
    "JFK": "United States", "LAX": "United States", "ORD": "United States",
    "SFO": "United States", "MIA": "United States", "BOS": "United States",
    "IAD": "United States", "DFW": "United States", "ATL": "United States",
    "SEA": "United States", "DEN": "United States", "LAS": "United States",
    # UAE
    "DXB": "United Arab Emirates", "AUH": "United Arab Emirates", "SHJ": "United Arab Emirates",
    # Qatar
    "DOH": "Qatar",
    # Singapore
    "SIN": "Singapore",
    # Thailand
    "BKK": "Thailand", "HKT": "Thailand", "CNX": "Thailand",
    # Japan
    "NRT": "Japan", "KIX": "Japan", "HND": "Japan", "NGO": "Japan",
    # China
    "PVG": "China", "PEK": "China", "CAN": "China", "PKX": "China",
    # South Korea
    "ICN": "South Korea", "GMP": "South Korea",
    # Malaysia
    "KUL": "Malaysia",
    # Hong Kong
    "HKG": "Hong Kong",
    # India
    "DEL": "India", "BOM": "India", "BLR": "India", "MAA": "India",
    # Egypt
    "CAI": "Egypt", "HRG": "Egypt", "SSH": "Egypt",
    # Africa
    "DKR": "Senegal", "ADD": "Ethiopia", "NBO": "Kenya",
    "JNB": "South Africa", "CPT": "South Africa", "LOS": "Nigeria",
    "ACC": "Ghana", "CMN": "Morocco",
    # Americas
    "GRU": "Brazil", "GIG": "Brazil", "BSB": "Brazil",
    "EZE": "Argentina", "BOG": "Colombia", "LIM": "Peru",
    "MEX": "Mexico", "CUN": "Mexico",
    "YYZ": "Canada", "YVR": "Canada", "YUL": "Canada",
    "SYD": "Australia", "MEL": "Australia", "BNE": "Australia",
    # Russia
    "SVO": "Russia", "DME": "Russia", "LED": "Russia",
    # Middle East
    "RUH": "Saudi Arabia", "JED": "Saudi Arabia", "MED": "Saudi Arabia",
    "TLV": "Israel", "AMM": "Jordan", "BEY": "Lebanon",
    "BAH": "Bahrain", "KWI": "Kuwait", "MCT": "Oman",
    # Other Europe
    "BUD": "Hungary", "PRG": "Czech Republic", "WAW": "Poland",
    "KRK": "Poland", "CPH": "Denmark", "OSL": "Norway",
    "ARN": "Sweden", "HEL": "Finland",
    "LIS": "Portugal", "OPO": "Portugal",
    "SOF": "Bulgaria", "OTP": "Romania", "BEG": "Serbia",
    "ZAG": "Croatia", "LJU": "Slovenia",
    "TBS": "Georgia", "EVN": "Armenia", "GYD": "Azerbaijan",
    "TAS": "Uzbekistan", "ALA": "Kazakhstan",
    # South Asia
    "KHI": "Pakistan", "LHE": "Pakistan", "ISB": "Pakistan",
    "DAC": "Bangladesh", "CMB": "Sri Lanka", "KTM": "Nepal",
    # Southeast Asia
    "CGK": "Indonesia", "MNL": "Philippines",
}

# ─────────────────────────────────────────────────────────────────────────────

MONTH_NAMES = ["", "January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]


def build_filename(search):
    year, month, day = search["date"].split("-")
    trip = search["trip_type"].lower()
    orig = search["origin"].lower()
    dest = search["destination"].lower()
    return f"TK_{month}{day}_{search['pax']}pax_{trip}_{orig}_{dest}.txt"


# ─────────────────────────────────────────────────────────────────────────────
# Custom exception — raised when a search step fails (triggers retry)
# ─────────────────────────────────────────────────────────────────────────────

class SearchFailed(Exception):
    pass


# ─────────────────────────────────────────────────────────────────────────────
# Session health check — detects expired sessions / cookie banners
# ─────────────────────────────────────────────────────────────────────────────

async def check_session_and_recover(page):
    """
    Verify the TK booking form is visible after navigation.
    If not, the session may have expired or a consent overlay is blocking it.
    Prints recovery instructions and waits for the user to fix it.
    """
    form_ok = await page.evaluate("""() => {
        const btn = document.querySelector('#buttonSearchflights');
        if (!btn) return false;
        const r = btn.getBoundingClientRect();
        return r.width > 0 && r.height > 0;
    }""")

    if not form_ok:
        print("\n" + "=" * 65)
        print("⚠  SESSION ISSUE DETECTED")
        print("=" * 65)
        print("The TK booking form is not visible. Common causes:")
        print("  1. A cookie consent banner is covering the page")
        print("     → Click 'Accept' or 'Agree' in the Chrome window")
        print("  2. Your session has expired")
        print("     → Refresh the TK page and wait for the form to load")
        print("  3. A login wall appeared")
        print("     → Close it (Esc) or sign in if required")
        print("\nFix it in the Chrome window, then press Enter here to continue...")
        import sys
        sys.stdin.readline()
        print("Resuming...\n")


# ─────────────────────────────────────────────────────────────────────────────
# STEP 1 — Trip type
# ─────────────────────────────────────────────────────────────────────────────

async def select_trip_type(page, trip_type):
    """Click One Way or Round Trip tab using multiple strategies."""
    target_lower = "one way" if trip_type == "OW" else "round"
    alternatives = (
        ["One way", "One Way", "Oneway", "One-way"]
        if trip_type == "OW"
        else ["Round trip", "Round Trip", "Roundtrip", "Round-trip", "Return"]
    )

    # Strategy 1: Playwright native click — fires real browser/React events
    for text in alternatives:
        for role in ["radio", "button", "tab"]:
            try:
                loc = page.get_by_role(role, name=text)
                if await loc.count() > 0:
                    await loc.first.click()
                    print(f"     ✓ Trip type → {trip_type} (role={role}, text='{text}')")
                    await page.wait_for_timeout(600)
                    return
            except Exception:
                pass

    # Strategy 2: JS evaluate fallback
    result = await page.evaluate("""(target) => {
        function vis(el) { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0; }
        const specific = document.querySelectorAll(
            '[class*="RoundAndOneWay"] button, [class*="RoundAndOneWay"] label, ' +
            '[class*="tripType"] button, [class*="trip-type"] button'
        );
        for (let el of specific) {
            if (el.textContent.trim().toLowerCase().includes(target)) {
                el.click();
                return 'found-specific';
            }
        }
        const candidates = ['One way', 'One Way', 'Oneway', 'Round-trip',
                            'Round trip', 'Roundtrip', 'Return'];
        const all = document.querySelectorAll('button, label, [role="tab"], span[class*="tab"]');
        for (let el of all) {
            const t = el.textContent.trim();
            for (let c of candidates) {
                if (t === c && c.toLowerCase().includes(target)) {
                    el.click();
                    return 'found-wide:' + c;
                }
            }
        }
        return false;
    }""", target_lower)

    if result:
        print(f"     ✓ Trip type set to {trip_type} ({result})")
        await page.wait_for_timeout(400)
    else:
        print(f"     ⚠ Could not set trip type to {trip_type} — default may be correct")


# ─────────────────────────────────────────────────────────────────────────────
# STEP 2 — Airport fields via country modal
# ─────────────────────────────────────────────────────────────────────────────

async def is_country_modal_open(page):
    """Return True if the TK country/region modal is visible."""
    return await page.evaluate("""() => {
        const m = document.querySelector('[class*="thy-modal-background"]');
        if (!m) return false;
        const r = m.getBoundingClientRect();
        return r.width > 0 && r.height > 0;
    }""")


async def close_country_modal(page):
    """Dismiss the country modal if it is open."""
    if await is_country_modal_open(page):
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(500)
        if await is_country_modal_open(page):
            await page.evaluate("""() => {
                const btns = document.querySelectorAll(
                    '[class*="thy-modal"] button[class*="close"], ' +
                    '[class*="CountryModal"] button[class*="close"], ' +
                    'button[aria-label*="lose"]'
                );
                for (let b of btns) {
                    if (b.offsetParent !== null) { b.click(); return; }
                }
            }""")
            await page.wait_for_timeout(400)


async def select_via_country_modal(page, airport_code):
    """
    Handle the TK country/region modal:
      Left panel  — country list with search input at top
      Right panel — airports for the selected country
    """
    country = AIRPORT_COUNTRY.get(airport_code.upper(), "")
    print(f"     Modal open — country='{country}' → airport='{airport_code}'")

    # Type country name into modal's search input to filter the list
    modal_input = page.locator(
        '[class*="thy-modal-background"] input[type="text"], '
        '[class*="CountryModal"] input'
    )

    if country and await modal_input.count() > 0:
        inp = modal_input.first
        await inp.click(click_count=3)
        await page.wait_for_timeout(100)
        await inp.fill(country)
        await page.wait_for_timeout(700)

    # Click the country row
    if country:
        country_clicked = await page.evaluate("""(country) => {
            function vis(el) { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0; }
            const items = document.querySelectorAll(
                '[class*="countryItemLink"], [class*="CountryModal"] [role="button"]'
            );
            for (let item of items) {
                if (vis(item) && item.textContent.trim() === country) {
                    item.click();
                    return true;
                }
            }
            for (let item of items) {
                if (vis(item) && item.textContent.trim().includes(country)) {
                    item.click();
                    return true;
                }
            }
            return false;
        }""", country)

        if country_clicked:
            await page.wait_for_timeout(700)
        else:
            print(f"     ⚠ Country '{country}' not found — trying airport code directly")
            if await modal_input.count() > 0:
                await modal_input.first.click(click_count=3)
                await modal_input.first.fill(airport_code)
                await page.wait_for_timeout(700)

    # Click the airport in the right panel — rows look like "Frankfurt (FRA)"
    airport_clicked = await page.evaluate("""(code) => {
        function vis(el) { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0; }
        const pattern = '(' + code + ')';
        const candidates = [];
        const all = document.querySelectorAll('*');
        for (let el of all) {
            if (!vis(el)) continue;
            if (el.children.length > 0) continue;
            const t = el.textContent.trim();
            if (t.includes(pattern) && t.length < 80) {
                candidates.push(el);
            }
        }
        if (candidates.length > 0) {
            candidates.sort((a, b) => a.textContent.length - b.textContent.length);
            candidates[0].click();
            return candidates[0].textContent.trim();
        }
        const btns = document.querySelectorAll('[class*="airport"], [class*="Airport"]');
        for (let btn of btns) {
            if (vis(btn) && btn.textContent.includes(code)) {
                btn.click();
                return btn.textContent.trim().substring(0, 40);
            }
        }
        return null;
    }""", airport_code)

    if airport_clicked:
        await page.wait_for_timeout(500)
        print(f"     ✓ Airport selected: '{airport_clicked}'")
        return True
    else:
        print(f"     ✗ Airport '({airport_code})' not found in right panel")
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(400)
        return False


async def select_airport(page, field_id, airport_code):
    """
    Select an airport in the TK booking form.
    Handles both the country/region modal (TK's current UI) and legacy autocomplete.
    """
    # Always close any lingering modal before touching a field
    await close_country_modal(page)
    await page.wait_for_timeout(300)

    # Click the field
    field = page.locator(f"#{field_id}")
    await field.click()
    await page.wait_for_timeout(900)

    # Detect what opened: country modal or autocomplete?
    if await is_country_modal_open(page):
        return await select_via_country_modal(page, airport_code)

    # No modal — use autocomplete approach
    print(f"     No modal detected, trying autocomplete for {airport_code}")
    await field.click(click_count=3)
    await field.type(airport_code, delay=70)
    await page.wait_for_timeout(1200)

    # Check again — modal may appear after typing
    if await is_country_modal_open(page):
        return await select_via_country_modal(page, airport_code)

    # Try autocomplete dropdown suggestions
    for sel in [
        f'[role="option"]:has-text("{airport_code}")',
        f'li[class*="suggest"]:has-text("{airport_code}")',
        f'li[class*="airport"]:has-text("{airport_code}")',
        f'[class*="portItem"]:has-text("{airport_code}")',
    ]:
        try:
            loc = page.locator(sel)
            if await loc.count() > 0:
                await loc.first.click()
                await page.wait_for_timeout(400)
                print(f"     ✓ Airport {airport_code} selected via autocomplete")
                return True
        except Exception:
            pass

    print(f"     ⚠ Used Enter fallback for {airport_code}")
    await page.keyboard.press("Enter")
    await page.wait_for_timeout(300)
    return False


# ─────────────────────────────────────────────────────────────────────────────
# STEP 3 — Calendar date picker  (react-calendar library)
# ─────────────────────────────────────────────────────────────────────────────

async def _cal_is_open(page):
    """Return True if a react-calendar is visible on the page."""
    return await page.evaluate("""() => {
        const cal = document.querySelector('.react-calendar');
        if (!cal) return false;
        const r = cal.getBoundingClientRect();
        const s = window.getComputedStyle(cal);
        return r.width > 0 && r.height > 0
            && s.display !== 'none'
            && s.visibility !== 'hidden'
            && s.opacity !== '0';
    }""")


async def _read_cal_label(page):
    """Read the left-most visible month/year label from TK's calendar."""
    return await page.evaluate("""() => {
        // TK uses custom month dropdown buttons, e.g. id="buttonMay2026", text "May 2026"
        const tkBtns = document.querySelectorAll('[class*="monthDropdownButton"]');
        for (let btn of tkBtns) {
            const r = btn.getBoundingClientRect();
            if (r.width > 0 && r.height > 0) {
                const txt = btn.textContent.trim();
                if (txt) return txt;
                // Fallback: parse from id like "buttonMay2026"
                if (btn.id && btn.id.startsWith('button')) {
                    const raw = btn.id.slice(6);
                    const m = raw.match(/^([A-Za-z]+)(\d{4})$/);
                    if (m) return m[1] + ' ' + m[2];
                }
            }
        }
        // Standard react-calendar fallback
        const sels = [
            '.react-calendar__navigation__label__labelText--from',
            '.react-calendar__navigation__label__labelText',
            '.react-calendar__navigation__label',
        ];
        for (let s of sels) {
            const el = document.querySelector(s);
            if (el) {
                const r = el.getBoundingClientRect();
                if (r.width > 0 && r.height > 0) {
                    const txt = (el.querySelector('span') || el).textContent.trim();
                    if (txt) return txt;
                }
            }
        }
        return '';
    }""")


async def _nav_to_month(page, year, month_num, target_month):
    """Advance/retreat the react-calendar until the target month is visible."""
    for _ in range(24):
        current = await _read_cal_label(page)
        print(f"     Calendar showing: '{current}'")

        if target_month in current and str(year) in current:
            return True

        m = re.match(r'(\w+)\s+(\d{4})', current.strip())
        if m:
            cur_name = m.group(1)
            cur_year = int(m.group(2))
            cur_idx  = MONTH_NAMES.index(cur_name) if cur_name in MONTH_NAMES else 0
            go_forward = (cur_year * 12 + cur_idx) < (year * 12 + month_num)
        else:
            go_forward = True   # unknown state — keep advancing

        arrow_label = "Go to the next month" if go_forward else "Go to the previous month"
        arrow = page.locator(f'button[aria-label="{arrow_label}"]')
        cnt = await arrow.count()
        if cnt > 0:
            await arrow.first.click()
            await page.wait_for_timeout(400)
        else:
            print(f"     ⚠ Arrow '{arrow_label}' not found")
            break

    return target_month in await _read_cal_label(page)


async def _click_day(page, target_month, year, day, day_str):
    """
    Click the calendar tile for the given day using Playwright's native locator,
    which correctly fires React synthetic events (unlike JS evaluate .click()).

    When airports are selected, TK loads prices into each tile so inner_text()
    returns e.g. "15\n1,234 TRY" — we extract just the leading day number.
    """
    tiles = page.locator(
        'button.react-calendar__tile.react-calendar__month-view__days__day'
    )
    cnt = await tiles.count()
    for i in range(cnt):
        tile = tiles.nth(i)
        try:
            disabled = await tile.is_disabled()
            if disabled:
                continue

            # Try abbr child first (day number only, even when prices are present)
            abbr_loc = tile.locator('abbr')
            if await abbr_loc.count() > 0:
                num_txt = (await abbr_loc.first.inner_text()).strip()
            else:
                # Fallback: grab just the first line / leading digits
                raw = (await tile.inner_text()).strip()
                m = re.match(r'^(\d{1,2})', raw)
                num_txt = m.group(1) if m else raw.split('\n')[0].strip()

            if num_txt == day_str:
                await tile.click()
                return f"tile-{i}:day={num_txt}"
        except Exception:
            pass
    return None


async def _click_calendar_ok(page):
    """
    Click TK's 'OK' confirmation button at the bottom of the date picker.
    Without this click the selected dates are not applied to the search form.
    Uses Playwright native locator (proven working in test_date_picker.py).
    """
    ok_btn = page.locator('button').filter(has_text=re.compile(r'^(OK|Tamam)$'))
    ok_cnt = await ok_btn.count()
    if ok_cnt > 0:
        await ok_btn.first.click()
        print(f"     ✓ Calendar confirmed (OK clicked)")
    else:
        print(f"     ⚠ No OK button found")
    await page.wait_for_timeout(600)


async def set_calendar_date(page, date_str):
    """
    Open the departure date calendar and navigate to the target date.
    Handles both OW (single-date) and RT (range) calendar modes.
    """
    year, month_num, day = [int(x) for x in date_str.split("-")]
    target_month = MONTH_NAMES[month_num]
    day_str      = str(day)

    print(f"  → Opening calendar for {day} {target_month} {year}...")
    await close_country_modal(page)

    # --- Open the departure date field ---
    opened = False
    for sel in [
        "#bookerDatepicker",
        "[id*='departing'][id*='date' i]",
        "[id*='depart'][id*='picker' i]",
        "[aria-label*='Departure date' i]",
        "[aria-label*='departing date' i]",
        "[placeholder*='Departure' i]",
        "input[name*='departure' i]",
    ]:
        try:
            loc = page.locator(sel)
            if await loc.count() > 0:
                await loc.first.click()
                await page.wait_for_timeout(900)
                if await _cal_is_open(page):
                    print(f"     Calendar opened via '{sel}'")
                    opened = True
                    break
        except Exception:
            pass

    if not opened:
        print("     ⚠ Could not open departure date calendar")
        return False

    # --- Try direct aria-label first (if the right tile is already visible) ---
    for pattern in [
        f'abbr[aria-label="{target_month} {day}, {year}"]',
        f'button.react-calendar__tile[aria-label="{target_month} {day}, {year}"]',
        f'abbr[aria-label="{day} {target_month} {year}"]',
    ]:
        try:
            if await page.locator(pattern).count() > 0:
                await page.locator(pattern).first.click()
                print(f"     ✓ Date set via direct aria-label")
                await page.wait_for_timeout(500)
                return True
        except Exception:
            pass

    # --- Navigate to the right month, then click ---
    await _nav_to_month(page, year, month_num, target_month)

    clicked = await _click_day(page, target_month, year, day, day_str)
    if clicked:
        print(f"     ✓ Day {day} clicked ({clicked})")
        await page.wait_for_timeout(600)
        return True
    else:
        print(f"     ✗ Could not click day {day} — calendar may be on wrong month")
        await page.keyboard.press("Escape")
        return False


# ─────────────────────────────────────────────────────────────────────────────
# STEP 3b — Return date (RT only)
# ─────────────────────────────────────────────────────────────────────────────

async def set_return_date(page, date_str):
    """
    Set the return date for a Round Trip search.
    After picking the departure date the calendar often stays open in range
    mode — if so we just navigate and click.  If it closed, we open the
    return-date picker and navigate normally.
    """
    year, month_num, day = [int(x) for x in date_str.split("-")]
    target_month = MONTH_NAMES[month_num]
    day_str      = str(day)

    print(f"  → Setting return date: {day} {target_month} {year}...")

    # If calendar closed after departure click, re-open via return field
    if not await _cal_is_open(page):
        opened = False
        for sel in ["#bookerReturnDatepicker", "#returnDate",
                    "[id*='return'][id*='date' i]", "[aria-label*='Return date' i]",
                    "[placeholder*='Return' i]"]:
            try:
                loc = page.locator(sel)
                if await loc.count() > 0:
                    await loc.first.click()
                    await page.wait_for_timeout(600)
                    if await _cal_is_open(page):
                        opened = True
                        break
            except Exception:
                pass
        if not opened:
            print("     ⚠ Could not open return date calendar")
            return False

    # In RT range mode TK shows two panels.
    # The return date is always in the same month as departure (6 days later),
    # so the left panel already shows the right month after navigating for departure.
    # Use _nav_to_month which reads the left (first) monthDropdownButton label.
    await _nav_to_month(page, year, month_num, target_month)

    clicked = await _click_day(page, target_month, year, day, day_str)
    if clicked:
        print(f"     ✓ Return day {day} clicked ({clicked})")
        await page.wait_for_timeout(600)
        return True
    else:
        print(f"     ✗ Could not click return day {day}")
        await page.keyboard.press("Escape")
        return False


# ─────────────────────────────────────────────────────────────────────────────
# STEP 3c — Passenger count
# ─────────────────────────────────────────────────────────────────────────────

async def set_passengers(page, pax_count):
    """Increase adult passenger count to pax_count (default on TK is 1)."""
    if pax_count <= 1:
        return

    print(f"  → Setting passengers to {pax_count}...")

    # Open the passenger selector (click the field showing "1 Passenger" etc.)
    opened = await page.evaluate("""() => {
        function vis(el) { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0; }
        const triggers = document.querySelectorAll(
            '[id*="pax" i], [id*="passenger" i], [class*="pax-count"], ' +
            '[class*="passengerCount"], [aria-label*="Passenger" i]'
        );
        for (let el of triggers) {
            if (vis(el)) { el.click(); return true; }
        }
        return false;
    }""")
    if opened:
        await page.wait_for_timeout(400)

    # Click the "+" / increase button for Adults (pax_count - 1) times
    for _ in range(pax_count - 1):
        clicked = await page.evaluate("""() => {
            function vis(el) { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0; }
            // Look for an increment/plus button near "Adult" label
            const btns = document.querySelectorAll(
                'button[aria-label*="Increase"], button[aria-label*="increase"], ' +
                'button[aria-label*="Add adult"], button[class*="increment"], ' +
                'button[class*="plus"], [class*="pax"] button:last-child'
            );
            for (let btn of btns) {
                if (vis(btn)) { btn.click(); return true; }
            }
            return false;
        }""")
        if clicked:
            await page.wait_for_timeout(200)
        else:
            print(f"     ⚠ Could not find passenger increment button")
            break

    # Confirm / close the passenger selector if there's a "Done" button
    await page.evaluate("""() => {
        function vis(el) { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0; }
        const done = document.querySelector(
            'button[aria-label*="Done"], button[class*="done"], button[class*="confirm"]'
        );
        if (done && vis(done)) done.click();
    }""")
    await page.wait_for_timeout(300)
    print(f"     ✓ Passengers set to {pax_count}")



# ─────────────────────────────────────────────────────────────────────────────

async def is_captcha_present(page):
    try:
        return await page.evaluate("""() => {
            const rc = document.querySelector('iframe[src*="recaptcha"], .g-recaptcha, [data-sitekey]');
            if (rc) {
                const s = window.getComputedStyle(rc);
                if (s.display !== 'none' && s.visibility !== 'hidden') return true;
            }
            const hc = document.querySelector('iframe[src*="hcaptcha"], .h-captcha');
            if (hc) {
                const s = window.getComputedStyle(hc);
                if (s.display !== 'none' && s.visibility !== 'hidden') return true;
            }
            const body = document.body.innerText;
            if ((body.includes('robot') || body.includes('verify you are human')) && body.length < 500)
                return true;
            return false;
        }""")
    except Exception:
        return False


async def wait_for_captcha_solved(page):
    print("\n  ⚠  CAPTCHA detected! Please solve it in the browser window.")
    print("  The script will resume automatically once the form reappears.\n")
    try:
        await page.wait_for_function(
            """() => {
                const from = document.querySelector('#fromPort');
                const to   = document.querySelector('#toPort');
                const btn  = document.querySelector('#buttonSearchflights');
                return from !== null && to !== null && btn !== null;
            }""",
            timeout=300_000,
        )
        print("  ✓ CAPTCHA solved, resuming...\n")
    except PlaywrightTimeout:
        print("  ✗ Timed out waiting for CAPTCHA solve.")


# ─────────────────────────────────────────────────────────────────────────────
# STEP 4 — Wait for results
# ─────────────────────────────────────────────────────────────────────────────

async def wait_for_results(page):
    """Poll until the availability-international URL appears."""
    print(f"  → Waiting for results page (up to {RESULTS_TIMEOUT}s)...")
    cycles = 0
    max_cycles = RESULTS_TIMEOUT // 2

    while cycles < max_cycles:
        await page.wait_for_timeout(2000)
        cycles += 1
        url = page.url

        if "availability-international" in url:
            print(f"     ✓ Results URL detected — waiting for flight cards to render...")
            # URL changes fast; wait until React actually renders flight cards
            try:
                await page.wait_for_function(
                    """() => document.querySelectorAll('[data-testid^="TK"]').length >= 3""",
                    timeout=45000,
                )
            except PlaywrightTimeout:
                pass
            flight_count = await page.evaluate(
                """() => document.querySelectorAll('[data-testid^="TK"]').length"""
            )
            print(f"     ✓ {flight_count} flight cards in DOM")
            await page.wait_for_timeout(1000)
            return True

        flight_count = await page.evaluate("""() =>
            document.querySelectorAll('[data-testid^="TK"]').length
        """)
        if flight_count > 0:
            print(f"     ✓ {flight_count} flight items detected on page")
            await page.wait_for_timeout(2000)
            return True

        if await is_captcha_present(page):
            await wait_for_captcha_solved(page)

        if cycles % 3 == 0:
            print(f"     ... still waiting ({cycles*2}s) | URL: {url[:60]}")

    print(f"  ⚠  Results not detected after {RESULTS_TIMEOUT}s")
    return False


# ─────────────────────────────────────────────────────────────────────────────
# STEP 5 — Expand TK fare tiers inline & save CSV
# ─────────────────────────────────────────────────────────────────────────────

async def expand_and_save(page, search):
    """
    For each TK flight (skipping VF/AJet), click Economy then Business cabin
    cards one at a time, extract the individual fare tier names + prices from
    the expanded panel, take a screenshot, and save results directly to a CSV.

    The TK UI is an accordion — only one panel can be open at a time, so we
    must extract data immediately after each click rather than saving a single
    HTML snapshot with all panels open simultaneously.
    """
    import csv as csv_mod

    checking_date = datetime.now().strftime("%Y-%m-%d")
    filename_base = build_filename(search)
    out_dir = Path(OUTPUT_DIR)
    out_dir.mkdir(exist_ok=True)
    shots_dir = out_dir / "screenshots"
    shots_dir.mkdir(exist_ok=True)

    # ── Wait for flight cards to actually render ──────────────────────────
    print("  → Confirming flight cards are rendered...")
    try:
        await page.wait_for_function(
            """() => document.querySelectorAll('[data-testid^="TK"]').length >= 1""",
            timeout=30000,
        )
    except PlaywrightTimeout:
        pass

    # ── Collect TK flight IDs — skip VF (AJet) and anything else ─────────
    flight_ids = await page.evaluate("""() => {
        const items = document.querySelectorAll('[data-testid]');
        const ids = [];
        for (let el of items) {
            const tid = el.getAttribute('data-testid');
            if (tid && /^TK\\d/.test(tid)) ids.push(tid);
        }
        return [...new Set(ids)];
    }""")
    print(f"  → {len(flight_ids)} TK flights found (VF/AJet skipped)")

    all_fares = []

    for flight_id in flight_ids:
        # Get basic flight info (times + airport codes)
        info = await page.evaluate("""(tid) => {
            const item = document.querySelector('[data-testid="' + tid + '"]');
            if (!item) return {};
            const timeBtn = item.querySelector('[role="button"][aria-label*="Itinerary details"]');
            const timeLabel = timeBtn ? timeBtn.getAttribute('aria-label') : '';
            const tm = timeLabel.match(/(\\d{2}:\\d{2}) - (\\d{2}:\\d{2})/);
            const raw = item.textContent.replace(/\\s+/g, '');
            const codes = [...raw.matchAll(/(\\d{2}:\\d{2})([A-Z]{3})/g)].map(m => m[2]);
            return {
                dep_time:     tm ? tm[1] : 'N/A',
                arr_time:     tm ? tm[2] : 'N/A',
                from_airport: codes[0] || '',
                to_airport:   codes[1] || '',
            };
        }""", flight_id)

        for cabin in ["Economy", "Business"]:
            # Find this cabin's card within this specific flight
            sel = f'[data-testid="{flight_id}"] [aria-label*="{cabin} cabin. Best available fare"]'
            loc = page.locator(sel)
            if await loc.count() == 0:
                continue

            # Scroll into view then click (short timeout — skip if blocked)
            try:
                await loc.scroll_into_view_if_needed()
                await loc.click(timeout=5000)
                await page.wait_for_timeout(700)
            except Exception as e:
                print(f"     ⚠ {flight_id} {cabin}: could not expand ({e})")
                continue

            # Extract fare tier buttons from the now-open panel
            # Button aria-label format: "EcoFly - 149.13 EUR Select fare package"
            fares = await page.evaluate("""(tid) => {
                const item = document.querySelector('[data-testid="' + tid + '"]');
                if (!item) return [];
                const btns = item.querySelectorAll('button[aria-label*="Select fare package"]');
                const result = [];
                for (let btn of btns) {
                    const lbl = btn.getAttribute('aria-label') || '';
                    const m = lbl.match(/^(.+?) - ([\\d.]+)\\s+([A-Z]{3})\\s+Select fare package/);
                    if (m) result.push({ fare_name: m[1], price: m[2], currency: m[3] });
                }
                return result;
            }""", flight_id)

            for fare in fares:
                all_fares.append({
                    "checking_date":     checking_date,
                    "departing_date":    search["date"],
                    "trip_type":         search["trip_type"],
                    "pax_count":         search["pax"],
                    "departing_airport": info.get("from_airport") or search["origin"],
                    "arriving_airport":  info.get("to_airport")   or search["destination"],
                    "flight":            flight_id,
                    "departing_time":    info.get("dep_time", "N/A"),
                    "arrival_time":      info.get("arr_time", "N/A"),
                    "fare_name":         fare["fare_name"],
                    "price_after_promo": fare["price"],
                    "currency":          fare["currency"],
                })

            names = [f["fare_name"] for f in fares]
            print(f"     {flight_id} {cabin}: {names}")

            # Screenshot the expanded panel (saved regardless of fare count)
            date_slug = search["date"].replace("-", "")
            shot_name = f"{date_slug}_{flight_id}_{cabin.lower()}.png"
            shot_path = shots_dir / shot_name
            try:
                await page.screenshot(path=str(shot_path), full_page=False)
                print(f"     📸 {shot_path.name}")
            except Exception as e:
                print(f"     ⚠ Screenshot failed: {e}")

    # ── Save fare CSV ─────────────────────────────────────────────────────
    if all_fares:
        csv_name = filename_base.replace(".txt", "_fares.csv")
        csv_path = out_dir / csv_name
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv_mod.DictWriter(f, fieldnames=all_fares[0].keys())
            writer.writeheader()
            writer.writerows(all_fares)
        print(f"  ✓ Saved: {csv_path} ({len(all_fares)} fare rows)")
    else:
        print("  ⚠  No fare data extracted")

    return all_fares


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

async def main():
    print("=" * 65)
    print("Turkish Airlines Fare Fetcher — Fully Automated")
    print("=" * 65)
    print(f"Searches: {len(SEARCHES)}\n")

    async with async_playwright() as pw:
        print(f"Connecting to Chrome at {CDP_URL}...")
        try:
            browser = await pw.chromium.connect_over_cdp(CDP_URL)
        except Exception as e:
            print(f"✗ Could not connect: {e}")
            print("\nStart Chrome with:")
            print('  /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome '
                  '--remote-debugging-port=9222 --user-data-dir="/tmp/chrome-tk-session"')
            sys.exit(1)

        context = browser.contexts[0]
        page    = context.pages[0] if context.pages else await context.new_page()
        print(f"✓ Connected. Current page: {page.url}\n")

        results      = []   # (filename, success_bool)
        failed_log   = []   # searches that exhausted all retries

        for i, search in enumerate(SEARCHES, 1):
            label = (f"[{i}/{len(SEARCHES)}] {search['origin']} → {search['destination']} | "
                     f"{search['date']} | {search['trip_type']} | {search['pax']} pax")
            print(label)

            last_error = None

            for attempt in range(1, MAX_RETRIES + 1):
                if attempt > 1:
                    print(f"  ↻ Retry {attempt}/{MAX_RETRIES} — waiting {RETRY_DELAY}s...")
                    await page.wait_for_timeout(RETRY_DELAY * 1000)

                try:
                    # Navigate to TK home
                    await page.goto(TK_HOME, wait_until="domcontentloaded")
                    await page.wait_for_timeout(2500)

                    if await is_captcha_present(page):
                        await wait_for_captcha_solved(page)

                    # Session / cookie health check
                    await check_session_and_recover(page)

                    # 1. Trip type
                    await select_trip_type(page, search["trip_type"])

                    # 2. Origin
                    print(f"  → Origin: {search['origin']}")
                    await select_airport(page, "fromPort", search["origin"])

                    # 3. Destination
                    print(f"  → Destination: {search['destination']}")
                    await select_airport(page, "toPort", search["destination"])

                    # 4. Departure date
                    date_ok = await set_calendar_date(page, search["date"])
                    if not date_ok:
                        raise SearchFailed("Departure date not set")

                    # 4b. Return date (RT only)
                    if search["trip_type"] == "RT" and search.get("return_date"):
                        ret_ok = await set_return_date(page, search["return_date"])
                        if not ret_ok:
                            raise SearchFailed("Return date not set")

                    # Confirm dates with OK button
                    await _click_calendar_ok(page)
                    await page.keyboard.press("Escape")
                    await page.wait_for_timeout(400)

                    # 5. Passengers
                    await set_passengers(page, search["pax"])

                    # 6. Submit
                    print("  → Clicking Search...")
                    try:
                        await page.locator("#buttonSearchflights").click()
                        print("     ✓ Search clicked")
                    except Exception as e:
                        raise SearchFailed(f"Search button click failed: {e}")

                    # 7. Wait for results
                    found = await wait_for_results(page)
                    if not found:
                        raise SearchFailed("Results page not detected within timeout")

                    if await is_captcha_present(page):
                        await wait_for_captcha_solved(page)

                    # 8. Expand fares & save
                    await expand_and_save(page, search)
                    results.append((build_filename(search), True))
                    last_error = None
                    break   # success — exit retry loop

                except SearchFailed as e:
                    last_error = str(e)
                    print(f"  ✗ Attempt {attempt}/{MAX_RETRIES} failed: {e}")
                except Exception as e:
                    last_error = str(e)
                    print(f"  ✗ Attempt {attempt}/{MAX_RETRIES} unexpected error: {e}")

            if last_error:
                failed_log.append({**search, "error": last_error})
                results.append((build_filename(search), False))

            if i < len(SEARCHES):
                print("  → Pausing 3s before next search...\n")
                await page.wait_for_timeout(3000)

    # ── Summary ───────────────────────────────────────────────────────────
    print(f"\n{'='*65}")
    print("Batch complete:")
    for fname, ok in results:
        print(f"  {'✓' if ok else '✗'}  {fname}")

    # ── Write failed searches log ─────────────────────────────────────────
    if failed_log:
        log_path = Path(OUTPUT_DIR) / "failed_searches.log"
        with open(log_path, "w", encoding="utf-8") as f:
            for s in failed_log:
                f.write(f"{s}\n")
        print(f"\n⚠  {len(failed_log)} search(es) failed after {MAX_RETRIES} retries.")
        print(f"   Details saved to: {log_path}")
        print(f"   Re-run with only those searches to retry them.")
    else:
        print(f"\n✓ All searches completed successfully.")

    print(f"\nNext: run  python parse_tk_html.py  to generate the coverage table.")


if __name__ == "__main__":
    asyncio.run(main())
