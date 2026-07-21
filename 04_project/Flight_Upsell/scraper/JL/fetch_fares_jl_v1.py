"""
Japan Airlines Fare Scraper v1
==============================
Scrapes jal.co.jp/jp/en/inter/ for branded fare coverage data.

Launch modes:
  Path B (default): Playwright launches its own Chromium headfully.
  Path A (--cdp):   Connect to user-launched Chrome via CDP.

PATH A SETUP (only if Path B is blocked):
  Launch Chrome manually:
    /Applications/Google Chrome.app/Contents/MacOS/Google Chrome
    --remote-debugging-port=9222 --user-data-dir="/tmp/chrome-jl-session"
  Then navigate to https://www.jal.co.jp/jp/en/inter/

JAL fare tiers (Economy):
  Economy Special  — rebook with charge, no refund
  Economy Semi-Flex — rebook free, refund with charge
  Economy Flex     — rebook free, refund free

Results page structure: fare comparison table is already expanded inline per
flight row — no click-to-expand needed (unlike TK).
"""

import argparse
import asyncio
import csv as _csv
import re
import sys
from datetime import date as _date, datetime, timedelta as _td
from pathlib import Path

from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

CDP_URL         = "http://localhost:9222"
JAL_HOME        = "https://www.jal.co.jp/jp/en/inter/"
OUTPUT_DIR      = Path.home() / "Documents" / "Audit" / "JL"
RESULTS_TIMEOUT = 90        # seconds to wait for results page
MAX_RETRIES     = 3
RETRY_DELAY     = 5
ROUTES_CSV      = Path(__file__).parent / "routes.csv"

STEALTH_ARGS = [
    "--disable-blink-features=AutomationControlled",
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--disable-extensions",
    "--start-maximized",
]

STEALTH_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)

# Canonical airport names as they appear in JAL's autocomplete dropdown.
# Used to verify the scraper selected the correct airport (not a city code like TYO).
# Format:  IATA_CODE -> (expected_city_fragment, expected_airport_fragment)
# The scraper will assert both strings appear in the selected suggestion text.
AIRPORT_VERIFY = {
    # Japan — departure airports
    "HND": ("Tokyo", "Haneda"),
    "NRT": ("Tokyo", "Narita"),
    "KIX": ("Osaka", "Kansai"),
    "ITM": ("Osaka", "Itami"),
    "NGO": ("Nagoya",  "Chubu"),
    "FUK": ("Fukuoka", "Fukuoka"),
    "OKA": ("Okinawa", "Naha"),
    "CTS": ("Sapporo", "New Chitose"),
    # Common international destinations
    "JFK": ("New York",   "Kennedy"),
    "LAX": ("Los Angeles", ""),
    "SFO": ("San Francisco", ""),
    "ORD": ("Chicago",    "O'Hare"),
    "BOS": ("Boston",     ""),
    "DFW": ("Dallas",     ""),
    "LAS": ("Las Vegas",  ""),
    "MCO": ("Orlando",    ""),
    "SAN": ("San Diego",  ""),
    "SEA": ("Seattle",    ""),
    "LHR": ("London",     "Heathrow"),
    "CDG": ("Paris",      "Charles de Gaulle"),
    "FRA": ("Frankfurt",  ""),
    "BER": ("Berlin",     ""),
    "MUC": ("Munich",     ""),
    "NCE": ("Nice",       ""),
    "MAD": ("Madrid",     ""),
    "BCN": ("Barcelona",  ""),
    "FCO": ("Rome",       "Fiumicino"),
    "HEL": ("Helsinki",   ""),
    "CPH": ("Copenhagen", ""),
    "DUB": ("Dublin",     ""),
    "LIS": ("Lisbon",     ""),
    "BKK": ("Bangkok",    "Suvarnabhumi"),
    "SIN": ("Singapore",  ""),
    "KUL": ("Kuala Lumpur", ""),
    "ICN": ("Seoul",      "Incheon"),
    "PEK": ("Beijing",    ""),
    "PVG": ("Shanghai",   "Pudong"),
    "HKG": ("Hong Kong",  ""),
    "SYD": ("Sydney",     ""),
    "MEL": ("Melbourne",  ""),
    "GRU": ("Sao Paulo",  "Guarulhos"),
    "DEL": ("Delhi",      ""),
    "YVR": ("Vancouver",  ""),
    "YYZ": ("Toronto",    ""),
    "NBO": ("Nairobi",    ""),
    "CAI": ("Cairo",      ""),
    "KEF": ("Reykjavik",  "Keflavik"),
}

MONTH_NAMES = ["", "January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]

# ─────────────────────────────────────────────────────────────────────────────
# ROUTE + DATE HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def load_routes():
    routes = []
    try:
        with open(ROUTES_CSV, newline="", encoding="utf-8") as f:
            for row in _csv.DictReader(f):
                if row.get("airline", "").strip().upper() == "JL":
                    routes.append((row["departure"].strip().upper(),
                                   row["arrival"].strip().upper()))
    except FileNotFoundError:
        pass
    if not routes:
        # fallback: a single test route
        routes = [("HND", "LHR")]
    print(f"✓ Loaded {len(routes)} JL routes")
    return routes


def generate_searches(routes, test_mode=False):
    """7 consecutive days starting +45d from today, RT 1pax."""
    today = _date.today()
    start = today + _td(days=45)
    searches = []
    for origin, dest in routes:
        for d in range(7):
            dep = start + _td(days=d)
            ret = dep + _td(days=7)
            searches.append({
                "origin":       origin,
                "destination":  dest,
                "date":         dep.strftime("%Y-%m-%d"),
                "return_date":  ret.strftime("%Y-%m-%d"),
                "trip_type":    "RT",
                "pax":          1,
            })
    if test_mode:
        # keep only first route, first date
        searches = [s for s in searches
                    if s["origin"] == routes[0][0]
                    and s["destination"] == routes[0][1]][:1]
    return searches


def build_filename(s):
    _, mm, dd = s["date"].split("-")
    return (f"JL_{mm}{dd}_{s['pax']}pax_{s['trip_type'].lower()}_"
            f"{s['origin'].lower()}_{s['destination'].lower()}_fares.csv")

# ─────────────────────────────────────────────────────────────────────────────
# BROWSER LAUNCH
# ─────────────────────────────────────────────────────────────────────────────

async def launch_browser(pw, force_cdp=False):
    """Path B (own Chromium) → fallback Path A (CDP)."""
    if not force_cdp:
        try:
            browser = await pw.chromium.launch(
                headless=False,
                args=STEALTH_ARGS,
            )
            context = await browser.new_context(user_agent=STEALTH_UA)
            await context.add_init_script(
                "Object.defineProperty(navigator,'webdriver',{get:()=>undefined})"
            )
            page = await context.new_page()
            return browser, context, page, "B"
        except Exception as e:
            print(f"  Path B failed ({e}), trying Path A (CDP)...")

    # Path A
    browser = await pw.chromium.connect_over_cdp(CDP_URL)
    context = browser.contexts[0] if browser.contexts else await browser.new_context()
    page = context.pages[0] if context.pages else await context.new_page()
    return browser, context, page, "A"

# ─────────────────────────────────────────────────────────────────────────────
# OVERLAY DISMISSAL
# ─────────────────────────────────────────────────────────────────────────────

async def dismiss_overlays(page):
    """
    Dismiss all overlays that can intercept pointer events on jal.co.jp.

    Known overlays:
    - #ensNotifyBanner          — Ensighten cookie/consent banner
    - #JS_domIntl_AirSelOverlay — JAL airport-selector backdrop (the div itself
                                  has aria-label="Close"; click IT, not a child)
    """
    # 1. Ensighten consent banner — JAL uses #ensCloseBanner (not #ensSave)
    for sel in [
        "#ensCloseBanner",                               # JAL confirmed id
        "#ensSave",
        "#ensNotifyBanner button[class*='accept' i]",
        "#ensNotifyBanner button[class*='agree' i]",
        "#ensNotifyBanner button[class*='allow' i]",
        "#ensNotifyBanner button:last-of-type",
        "[id*='cookie'] button[id*='accept' i]",
        "button[class*='cookieAccept' i]",
    ]:
        try:
            loc = page.locator(sel)
            if await loc.count() > 0 and await loc.first.is_visible():
                await loc.first.click(timeout=2000)
                await page.wait_for_timeout(600)
        except Exception:
            pass

    # 2. JAL airport-selector overlay — the div itself is the close target
    #    (aria-label="Close (Press escape to close)" is on the div, not a child)
    try:
        overlay = page.locator("#JS_domIntl_AirSelOverlay")
        if await overlay.count() > 0 and await overlay.first.is_visible():
            # Try clicking it directly (backdrop dismiss)
            await overlay.first.click(timeout=2000, force=True)
            await page.wait_for_timeout(500)
    except Exception:
        pass

    # 3. Escape key as fallback
    try:
        overlay = page.locator("#JS_domIntl_AirSelOverlay")
        if await overlay.count() > 0 and await overlay.first.is_visible():
            await page.keyboard.press("Escape")
            await page.wait_for_timeout(500)
    except Exception:
        pass

    # 4. JS force-hide as last resort — removes display blocker without click
    try:
        await page.evaluate("""() => {
            const el = document.getElementById('JS_domIntl_AirSelOverlay');
            if (el) el.style.display = 'none';
            const banner = document.getElementById('ensNotifyBanner');
            if (banner) banner.style.display = 'none';
        }""")
        await page.wait_for_timeout(300)
    except Exception:
        pass

# ─────────────────────────────────────────────────────────────────────────────
# CAPTCHA
# ─────────────────────────────────────────────────────────────────────────────

async def is_captcha_present(page):
    url = page.url.lower()
    title = (await page.title()).lower()
    return ("captcha" in url or "captcha" in title or
            "access denied" in title or "blocked" in title)


async def wait_for_captcha_solved(page, timeout_s=300):
    print("  ⚠ CAPTCHA detected — please solve it manually in the browser window.")
    for _ in range(timeout_s // 5):
        await page.wait_for_timeout(5000)
        if not await is_captcha_present(page):
            print("  ✓ CAPTCHA resolved")
            return
    print("  ✗ CAPTCHA not resolved in time, continuing anyway")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 1 — TRIP TYPE
# ─────────────────────────────────────────────────────────────────────────────

async def select_trip_type(page, trip_type):
    """Select Round-trip or One-way radio button."""
    label = "Round-trip" if trip_type == "RT" else "One-way"
    print(f"  → Trip type: {label}")
    try:
        # Radio buttons are inside a modal that opens when you click the search widget
        for sel in [
            f"input[type='radio'][value*='{label.lower()}' i]",
            f"label:has-text('{label}')",
            f"[aria-label*='{label}' i]",
        ]:
            loc = page.locator(sel)
            if await loc.count() > 0:
                await loc.first.click(timeout=3000)
                await page.wait_for_timeout(400)
                print(f"     ✓ {label} selected")
                return True
    except Exception as e:
        print(f"     ⚠ Could not select trip type: {e}")
    return False

# ─────────────────────────────────────────────────────────────────────────────
# STEP 2 — AIRPORT SELECTION  (text input + autocomplete)
# ─────────────────────────────────────────────────────────────────────────────

async def select_airport(page, role, iata_code):
    """
    JAL airport selection flow:
    1. Modal may already be open (JAL auto-opens arrival after departure is selected)
       → if so, use the visible input directly WITHOUT dismissing the overlay
    2. If modal not open → dismiss overlay blocking the form, then click field to open it
    3. Type IATA code in the modal's text input
    4. Click matching suggestion (verified against AIRPORT_VERIFY)

    Confirmed selectors from DOM inspection:
      Departure input: #JS_interTk_departureAirport  (class CLS_Input_Airport)
      Arrival input:   #JS_interTk_arrivalAirport

    IMPORTANT: JS_domIntl_AirSelOverlay is the modal backdrop AND its children include
    the airport search inputs. Hiding it with display:none hides the inputs too.
    So we must NOT dismiss the overlay when the modal is already open for us.
    """
    print(f"  → Airport ({role}): {iata_code}")
    verify = AIRPORT_VERIFY.get(iata_code.upper(), ("", ""))

    primary_sel = ("#JS_interTk_departureAirport" if role == "from"
                   else "#JS_interTk_arrivalAirport")

    # ── Step 1: find the modal input ─────────────────────────────────────────
    # Check if JAL already opened the modal for us (auto-opens arrival after departure)
    modal_input = None
    for sel in [
        primary_sel,
        "input.CLS_Input_Airport:visible",
        "[id*='AirSel'] input:visible",
        "[class*='airportSearch' i] input:visible",
    ]:
        try:
            loc = page.locator(sel)
            if await loc.count() > 0 and await loc.first.is_visible():
                modal_input = loc.first
                break
        except Exception:
            pass

    if modal_input is None:
        # Modal not open — dismiss overlay then click the field to open it
        await dismiss_overlays(page)
        await page.wait_for_timeout(500)

        field_clicked = False
        try:
            loc = page.locator(primary_sel)
            if await loc.count() > 0:
                await loc.first.click(timeout=4000)
                await page.wait_for_timeout(800)
                field_clicked = True
        except Exception:
            pass

        if not field_clicked:
            fallback_sels = {
                "from": [
                    ".CLS_Input_Airport:first-of-type",
                    "input[id*='departure' i]",
                    "input[id*='origin' i]",
                ],
                "to": [
                    ".CLS_Input_Airport:last-of-type",
                    "input[id*='arrival' i]",
                    "input[id*='destination' i]",
                ],
            }
            for sel in fallback_sels[role]:
                try:
                    loc = page.locator(sel)
                    if await loc.count() > 0 and await loc.first.is_visible():
                        await loc.first.click(timeout=3000)
                        await page.wait_for_timeout(800)
                        field_clicked = True
                        break
                except Exception:
                    pass

        if not field_clicked:
            print(f"     ✗ Could not click {role} field")
            return False

        # Find the now-visible modal input
        await page.wait_for_timeout(500)
        for sel in [
            primary_sel,
            "input.CLS_Input_Airport:visible",
            "[id*='AirSel'] input:visible",
        ]:
            try:
                loc = page.locator(sel)
                if await loc.count() > 0 and await loc.first.is_visible():
                    modal_input = loc.first
                    break
            except Exception:
                pass

    if modal_input is None:
        print(f"     ✗ Could not find airport text input")
        return False

    # ── Step 2: type IATA code ────────────────────────────────────────────────
    await modal_input.fill("")
    await modal_input.type(iata_code, delay=120)
    await page.wait_for_timeout(2000)   # give autocomplete time to populate

    # If no suggestions visible yet, wait another second
    has_suggestions = False
    for check_sel in [
        f"[role='option']:has-text('{iata_code}')",
        f"li:has-text('{iata_code}')",
        f"[id*='AirSel'] li:has-text('{iata_code}')",
    ]:
        try:
            if await page.locator(check_sel).count() > 0:
                has_suggestions = True
                break
        except Exception:
            pass
    if not has_suggestions:
        await page.wait_for_timeout(1500)

    # Diagnostic screenshot
    try:
        snapshot_path = (Path.home() / "Documents" / "Audit" / "JL" / "screenshots" /
                         f"diag_autocomplete_{role}_{iata_code}.png")
        snapshot_path.parent.mkdir(parents=True, exist_ok=True)
        await page.screenshot(path=str(snapshot_path), full_page=False)
    except Exception:
        pass

    # ── Step 3: click matching suggestion ────────────────────────────────────
    suggestion_clicked = False
    for sel in [
        f"[role='option']:has-text('{iata_code}')",
        f"li:has-text('{iata_code}')",
        f"[class*='suggestion' i]:has-text('{iata_code}')",
        f"[class*='airport-list' i] *:has-text('{iata_code}')",
        f"[class*='select' i] li:has-text('{iata_code}')",
        f"[id*='AirSel'] li:has-text('{iata_code}')",
    ]:
        try:
            opts = page.locator(sel)
            count = await opts.count()
            for i in range(count):
                opt = opts.nth(i)
                text = (await opt.text_content() or "").strip()
                if not re.search(r'\b' + iata_code + r'\b', text, re.IGNORECASE):
                    continue
                city_frag, airport_frag = verify
                city_ok    = (not city_frag)    or (city_frag.lower()    in text.lower())
                airport_ok = (not airport_frag) or (airport_frag.lower() in text.lower())
                if city_ok and airport_ok:
                    print(f"     ✓ Matched: \"{text[:60].strip()}\"")
                    await opt.click(timeout=3000)
                    suggestion_clicked = True
                    break
                else:
                    print(f"     ⚠ Skipping \"{text[:60].strip()}\"")
            if suggestion_clicked:
                break
        except Exception:
            pass

    if not suggestion_clicked:
        for sel in [f"li:has-text('{iata_code}')", f"[role='option']:has-text('{iata_code}')"]:
            try:
                loc = page.locator(sel).first
                if await loc.count() > 0:
                    text = await loc.text_content() or ""
                    print(f"     → Fallback: \"{text[:60].strip()}\"")
                    await loc.click(timeout=3000)
                    suggestion_clicked = True
                    break
            except Exception:
                pass

    if not suggestion_clicked:
        print(f"     ✗ Could not select airport {iata_code}")
        return False

    await page.wait_for_timeout(600)
    return True

# ─────────────────────────────────────────────────────────────────────────────
# STEP 2b — CONFIRM AIRPORT SELECTION
# After both airports are filled, JAL shows a "Confirmed" button that must be
# clicked to close the airport panel and activate the date picker.
# ─────────────────────────────────────────────────────────────────────────────

async def _confirm_airport_selection(page):
    """Click the Confirmed / Confirm button that closes the JAL airport panel.
    DOM confirmed: <button class="button raised grey">Confirmed</button>
    This activates the date picker calendar (triggers a fare data API call).
    """
    # CSS selectors
    for sel in [
        "button:has-text('Confirmed')",
        "button:has-text('Confirm')",
        "button.raised",
        "button[class*='raised']",
    ]:
        try:
            loc = page.locator(sel)
            if await loc.count() > 0 and await loc.first.is_visible():
                await loc.first.click(timeout=3000)
                await page.wait_for_timeout(2000)   # wait for calendar API call
                print("     ✓ Airport Confirmed clicked")
                return True
        except Exception:
            pass

    # JS fallback — find by exact text
    try:
        result = await page.evaluate("""() => {
            const btns = [...document.querySelectorAll('button')];
            const btn = btns.find(b =>
                (b.textContent || '').trim() === 'Confirmed' ||
                (b.textContent || '').trim() === 'Confirm'
            );
            if (btn) { btn.click(); return true; }
            return false;
        }""")
        if result:
            await page.wait_for_timeout(2000)
            print("     ✓ Airport Confirmed (JS click)")
            return True
    except Exception:
        pass

    print("     ⚠ Confirmed button not found — continuing anyway")
    return False

# ─────────────────────────────────────────────────────────────────────────────
# STEP 3 — DATE SELECTION  (modal calendar with NEXT button)
# ─────────────────────────────────────────────────────────────────────────────

async def _cal_is_open(page):
    """Return True only when the JAL calendar has active (non-disabled) day buttons.
    The calendar DOM is always present in the page but all buttons are disabled
    until 'Please select a date' is clicked, which triggers the fare API call.
    """
    try:
        enabled = await page.locator(".calendar-table button:not([disabled])").count()
        if enabled > 0:
            return True
    except Exception:
        pass
    return False


async def _read_calendar_headers(page):
    """Return [(table_id, label), ...] for the two CURRENTLY-VISIBLE calendar
    months. JAL pre-renders all 12 months as <li class="JS_calendarList"> with
    table IDs like JS202606 (June 2026); hidden months carry `dis-hide`.
    """
    return await page.evaluate("""() => {
        const out = [];
        const lis = [...document.querySelectorAll('.calendar-table-wrap .JS_calendarList')];
        for (const li of lis) {
            if (li.classList.contains('dis-hide')) continue;
            const tbl = li.querySelector('table.calendar-table');
            if (!tbl) continue;
            const id = tbl.id || '';
            const label = (tbl.querySelector('th.text-eyebrow')?.textContent || '').trim();
            out.push([id, label]);
        }
        return out;
    }""")


async def _nav_to_month(page, target_year, target_month_num):
    """Navigate calendar so the LEFT visible calendar is the target month.

    JAL renders every month as <li class="...{N}thCalPart JS_calendarList">,
    each containing <table class="calendar-table" id="JS{YYYYMM}">. Hidden
    months have `dis-hide` on the li. NEXT/PREV slide which two are visible.
    Use the table IDs (deterministic) instead of header text (race-prone).
    """
    target_id = f"JS{target_year}{target_month_num:02d}"

    # Wait until at least one visible calendar is present (fare API resolved).
    for _ in range(20):
        headers = await _read_calendar_headers(page)
        if headers:
            break
        await page.wait_for_timeout(500)

    # If still empty after waiting, dump full DOM diagnostic so we can see why.
    headers0 = await _read_calendar_headers(page)
    if not headers0:
        try:
            diag_dir = Path.home() / "Documents" / "Audit" / "JL"
            diag_dir.mkdir(parents=True, exist_ok=True)
            diag_path = diag_dir / "diag_nav_no_headers.txt"
            if not diag_path.exists():
                info = await page.evaluate("""() => {
                    const lis = [...document.querySelectorAll('.calendar-table-wrap .JS_calendarList')];
                    const dialogs = [...document.querySelectorAll('[role=dialog],.modal,[class*=Modal]')].map(d => ({cls: d.className, vis: d.offsetParent !== null}));
                    return {
                        url: location.href,
                        liCount: lis.length,
                        liSnapshot: lis.slice(0, 4).map(li => ({cls: li.className, hidden: li.classList.contains('dis-hide'), offsetParent: li.offsetParent !== null, hasTable: !!li.querySelector('table.calendar-table'), tableId: li.querySelector('table.calendar-table')?.id || ''})),
                        dialogs,
                        bodyLen: document.body.innerHTML.length,
                    };
                }""")
                import json as _json
                diag_path.write_text(_json.dumps({"target": target_id, "info": info}, indent=2), encoding="utf-8")
                print(f"     ⓘ No-headers diagnostic: {diag_path}")
                # Also dump full HTML snapshot
                html = await page.content()
                (diag_dir / "diag_nav_no_headers.html").write_text(html, encoding="utf-8")
                # And screenshot
                await page.screenshot(path=str(diag_dir / "diag_nav_no_headers.png"), full_page=True)
        except Exception as e:
            print(f"     ⚠ no-headers diag error: {e}")
        return False

    iterations = 0
    for _ in range(24):
        iterations += 1
        headers = await _read_calendar_headers(page)
        if headers and headers[0][0] == target_id:
            return True
        if not headers:
            return False
        # Decide direction: target_id may be earlier (PREV) or later (NEXT)
        # than the current visible window. Use lexicographic compare on the
        # JS{YYYYMM} ID since it sorts chronologically.
        left_id = headers[0][0]
        go_prev = target_id < left_id
        all_ids = await page.evaluate("""() => [...document.querySelectorAll('.JS_calendarList table.calendar-table')].map(t => t.id);""")
        if target_id not in all_ids:
            try:
                diag_dir = Path.home() / "Documents" / "Audit" / "JL"
                diag_dir.mkdir(parents=True, exist_ok=True)
                diag_path = diag_dir / "diag_nav_missing.txt"
                if not diag_path.exists():
                    info = {
                        "target": target_id,
                        "rendered_ids": all_ids,
                        "visible_headers": headers,
                    }
                    import json as _json
                    diag_path.write_text(_json.dumps(info, indent=2), encoding="utf-8")
                    print(f"     ⓘ Nav diagnostic: {diag_path}")
            except Exception:
                pass
            return False
        before = headers[0][0]
        clicked = False
        prev_sels = [".JS_prevBtn", "button.calendar-prev"]
        next_sels = [".JS_nextBtn", "button.calendar-next"]
        for sel in (prev_sels if go_prev else next_sels):
            try:
                loc = page.locator(sel)
                if await loc.count() > 0 and await loc.first.is_visible():
                    # Skip if hidden via u-vishid utility class
                    cls = await loc.first.get_attribute("class") or ""
                    if "u-vishid" in cls:
                        continue
                    await loc.first.click()
                    clicked = True
                    break
            except Exception:
                pass
        if not clicked:
            try:
                diag_dir = Path.home() / "Documents" / "Audit" / "JL"
                diag_dir.mkdir(parents=True, exist_ok=True)
                diag_path = diag_dir / "diag_nav_no_next.txt"
                if not diag_path.exists():
                    info = await page.evaluate("""() => {
                        const next = document.querySelector('.JS_nextBtn');
                        const prev = document.querySelector('.JS_prevBtn');
                        return {
                            next: next ? {cls: next.className, visible: next.offsetParent !== null, disabled: next.disabled} : null,
                            prev: prev ? {cls: prev.className, visible: prev.offsetParent !== null, disabled: prev.disabled} : null,
                        };
                    }""")
                    import json as _json
                    diag_path.write_text(_json.dumps({"target": target_id, "go_prev": go_prev, "headers_seen": headers, "btns": info}, indent=2), encoding="utf-8")
                    print(f"     ⓘ No-NEXT/PREV diagnostic: {diag_path}")
            except Exception:
                pass
            return False
        for _ in range(8):
            await page.wait_for_timeout(250)
            new_headers = await _read_calendar_headers(page)
            new_left = new_headers[0][0] if new_headers else ""
            if new_left and new_left != before:
                break

    # Loop exhausted: dump diagnostic on which months stayed visible.
    try:
        diag_dir = Path.home() / "Documents" / "Audit" / "JL"
        diag_dir.mkdir(parents=True, exist_ok=True)
        diag_path = diag_dir / "diag_nav_stuck.txt"
        if not diag_path.exists():
            info = await page.evaluate("""() => {
                const lis = [...document.querySelectorAll('.calendar-table-wrap .JS_calendarList')];
                return lis.map(li => {
                    const tbl = li.querySelector('table.calendar-table');
                    return {
                        cls: li.className,
                        hidden: li.classList.contains('dis-hide'),
                        offsetParent: li.offsetParent !== null,
                        id: tbl ? tbl.id : '',
                        label: (tbl?.querySelector('th.text-eyebrow')?.textContent || '').trim(),
                    };
                });
            }""")
            import json as _json
            diag_path.write_text(_json.dumps({"target": target_id, "iterations": iterations, "lis": info}, indent=2), encoding="utf-8")
            print(f"     ⓘ Nav-stuck diagnostic: {diag_path}")
    except Exception:
        pass
    return False


async def _click_day(page, year, month_num, day_num):
    """
    Click a specific day in the target month's calendar table.
    JAL renders every month with id=JS{YYYYMM} on the <table>; that gives us
    a deterministic scope (no need to guess "first vs second column" or
    chase JS class indices like firstCalPart).
    """
    table_id = f"JS{year}{month_num:02d}"

    # Wait for at least one enabled day button anywhere (fare API resolved).
    for _ in range(10):
        enabled = await page.locator(".calendar-table button:not([disabled])").count()
        if enabled > 0:
            break
        await page.wait_for_timeout(500)

    clicked = await page.evaluate("""({tableId, day}) => {
        const tbl = document.getElementById(tableId);
        if (!tbl) return {ok: false, reason: 'table not found: ' + tableId};
        // Bail if the parent li is hidden (target wasn't actually navigated to)
        let li = tbl.closest('li.JS_calendarList');
        if (li && li.classList.contains('dis-hide')) {
            return {ok: false, reason: 'target month is hidden — nav failed'};
        }
        const buttons = [...tbl.querySelectorAll('tbody button')];
        for (const btn of buttons) {
            if (btn.disabled) continue;
            const txt = (btn.textContent || '').trim();
            const leading = txt.split(/\\s+/)[0];
            if (leading !== String(day)) continue;
            btn.scrollIntoView({block: 'center'});
            btn.click();
            return {ok: true};
        }
        return {ok: false, reason: 'day ' + day + ' not enabled in ' + tableId};
    }""", {"tableId": table_id, "day": day_num})

    if clicked.get("ok"):
        return True

    print(f"     ⓘ _click_day: {clicked.get('reason')}")
    return False


async def open_calendar(page):
    """Click the departure date field to activate the JAL calendar.
    DOM confirmed: div#JS_interTk_domLbDepDate (tabindex=0, contains 'Please select a date')
    Clicking triggers a fare API call; calendar buttons enable after ~2-8s.
    """
    for sel in [
        "#JS_interTk_domLbDepDate",          # JAL confirmed ID
        "[data-calendar='JS_calDatesSelect']",
        ".input-going .mdl-input-area",
        ".mdl-input-parts.input-going",
        "div:has-text('Please select a date')",
    ]:
        try:
            loc = page.locator(sel)
            if await loc.count() > 0 and await loc.first.is_visible():
                await loc.first.click(timeout=3000)
                print(f"     → Clicked date field ({sel[:40]}), waiting for calendar API...")
                # Fare API can take 3-8s to enable calendar buttons
                for _ in range(16):
                    await page.wait_for_timeout(500)
                    if await _cal_is_open(page):
                        return True
                break   # clicked but calendar never activated
        except Exception:
            pass
    return False


async def _read_form_date(page, role):
    """Return (year, month, day) tuple from JAL's hidden inputs, or (None, None, None).
    role = 'departure' or 'arrival' (JAL names — 'arrival' is the return date for RT).
    """
    prefix = "JS_departureYear" if role == "departure" else "JS_arrivalYear"
    pmonth = "JS_departureMonth" if role == "departure" else "JS_arrivalMonth"
    pday   = "JS_departureDay"   if role == "departure" else "JS_arrivalDay"
    vals = await page.evaluate(f"""() => {{
        const y = document.getElementById('{prefix}');
        const m = document.getElementById('{pmonth}');
        const d = document.getElementById('{pday}');
        return [y && y.value, m && m.value, d && d.value];
    }}""")
    return tuple(vals)


async def set_departure_date(page, date_str):
    """Set departure date. JAL calendar requires: pick date → click NEXT."""
    year, month_num, day = [int(x) for x in date_str.split("-")]
    print(f"  → Departure date: {date_str}")

    if not await _cal_is_open(page):
        if not await open_calendar(page):
            print("     ✗ Could not open calendar")
            return False

    if not await _nav_to_month(page, year, month_num):
        print(f"     ✗ Could not navigate to {MONTH_NAMES[month_num]} {year}")
        return False
    if not await _click_day(page, year, month_num, day):
        print(f"     ✗ Could not click day {day}")
        return False
    print(f"     ✓ Departure day {day} clicked")
    await page.wait_for_timeout(800)

    # Verify form actually accepted the date before continuing.
    y, m, d = await _read_form_date(page, "departure")
    if (y, m, d) != (str(year), str(month_num), str(day)):
        print(f"     ✗ Form rejected departure: hidden inputs = ({y!r}, {m!r}, {d!r})")
        return False

    # JAL's calendar lets you pick departure and return in the same view —
    # no form-step NEXT button needed. (Earlier code mis-clicked the calendar
    # slider's NEXT, advancing the visible months a year ahead.)
    return True


async def set_return_date(page, date_str):
    """Set return date (calendar should already be open after NEXT)."""
    year, month_num, day = [int(x) for x in date_str.split("-")]
    print(f"  → Return date: {date_str}")
    if not await _nav_to_month(page, year, month_num):
        print(f"     ✗ Could not navigate to {MONTH_NAMES[month_num]} {year}")
        return False
    if not await _click_day(page, year, month_num, day):
        print(f"     ✗ Could not click return day {day}")
        return False
    print(f"     ✓ Return day {day} clicked")
    await page.wait_for_timeout(600)

    # Verify form accepted the return date.
    y, m, d = await _read_form_date(page, "arrival")
    if (y, m, d) != (str(year), str(month_num), str(day)):
        print(f"     ✗ Form rejected return: hidden inputs = ({y!r}, {m!r}, {d!r})")
        return False
    return True


async def confirm_dates(page):
    """Confirm date selection (close modal / click Done if present)."""
    for sel in ["button:has-text('Done')", "button:has-text('OK')",
                "button:has-text('Confirm')", "button[type='submit']",
                "[class*='calendar'] [class*='confirm' i]"]:
        try:
            loc = page.locator(sel)
            if await loc.count() > 0 and await loc.first.is_visible():
                await loc.first.click(timeout=2000)
                await page.wait_for_timeout(400)
                return
        except Exception:
            pass
    # Try pressing Escape to close
    await page.keyboard.press("Escape")
    await page.wait_for_timeout(400)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 4 — SEARCH BUTTON
# ─────────────────────────────────────────────────────────────────────────────

async def click_search(page):
    print("  → Clicking Search flights...")
    # Dismiss any overlays that could intercept the click
    await dismiss_overlays(page)
    await page.wait_for_timeout(400)

    # Primary: JS click by confirmed ID — bypasses viewport/scroll restrictions
    try:
        result = await page.evaluate("""() => {
            const btn = document.getElementById('JS_interTk_submitBtn');
            if (btn && !btn.disabled) { btn.click(); return true; }
            return false;
        }""")
        if result:
            print("     ✓ Search clicked (JS)")
            return True
    except Exception:
        pass

    # Fallback: Playwright click with scroll
    for sel in [
        "#JS_interTk_submitBtn",
        "button:has-text('Search flights')",
        "button[type='submit']:has-text('Search')",
        "button[class*='btn-rd' i]",
    ]:
        try:
            loc = page.locator(sel)
            if await loc.count() > 0 and await loc.first.is_visible():
                await loc.first.scroll_into_view_if_needed(timeout=3000)
                await loc.first.click(timeout=5000)
                print("     ✓ Search clicked")
                return True
        except Exception:
            pass
    print("     ✗ Search button not found")
    return False

# ─────────────────────────────────────────────────────────────────────────────
# STEP 5 — WAIT FOR RESULTS
# ─────────────────────────────────────────────────────────────────────────────

async def wait_for_results(page):
    print(f"  → Waiting for results (up to {RESULTS_TIMEOUT}s)...")
    # Screenshot immediately to see state after search click
    try:
        shots_dir = OUTPUT_DIR / "screenshots"
        shots_dir.mkdir(parents=True, exist_ok=True)
        await page.screenshot(path=str(shots_dir / "after_search_click.png"), full_page=False)
    except Exception:
        pass
    # Also check for inline error messages JAL might show
    try:
        errors = await page.evaluate("""() => {
            return [...document.querySelectorAll('[class*="error" i], [class*="alert" i], [class*="warning" i]')]
                .filter(el => el.offsetParent !== null)
                .map(el => (el.textContent||'').trim().substring(0, 100));
        }""")
        if errors:
            print(f"     ⚠ Page errors/alerts: {errors}")
    except Exception:
        pass
    for cycle in range(RESULTS_TIMEOUT // 3):
        await page.wait_for_timeout(3000)
        url = page.url
        # JAL international booking lands on booking.jal.co.jp/...
        # Generic check: we've left the homepage and are not still on /inter/.
        if url != JAL_HOME and "/inter/" not in url:
            print(f"     ✓ Results URL: {url[:80]}")
            await page.wait_for_timeout(2000)
            return True
        # Check for fare table rows on page
        row_count = await page.evaluate("""() => {
            return document.querySelectorAll(
                '[class*="flight-row"], [class*="flightRow"], [class*="flight-item"], tr[class*="flight"]'
            ).length;
        }""")
        if row_count > 0:
            print(f"     ✓ {row_count} flight rows found on page")
            return True
        if await is_captcha_present(page):
            await wait_for_captcha_solved(page)
        if cycle % 3 == 0:
            print(f"     ... {cycle*3}s | {url[:70]}")
    print(f"  ⚠ Results not detected after {RESULTS_TIMEOUT}s")
    return False

# ─────────────────────────────────────────────────────────────────────────────
# STEP 6 — EXTRACT FARES & SAVE CSV
# ─────────────────────────────────────────────────────────────────────────────

# JAL fare tier names as they appear on the results page
JAL_FARE_TIERS = ["Economy Special", "Economy Semi-Flex", "Economy Flex"]


async def extract_and_save(page, search):
    """
    Parse the JAL results page. Each flight row already shows all three fare
    tier columns inline — no click-to-expand needed.

    The fare table per flight looks like:
      | Fare rule    | Economy Special | Economy Semi-Flex | Economy Flex |
      | Rebook       | ...             | ...               | ...          |
      | Price        | ¥ 126,050       | ¥ 138,550         | ¥ 247,550    |
      | [Select btn] | [Select]        | [Select]          | [Select]     |
    """
    checking_date = datetime.now().strftime("%Y-%m-%d")
    out_dir   = OUTPUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    shots_dir = out_dir / "screenshots"
    shots_dir.mkdir(exist_ok=True)

    await page.wait_for_timeout(2000)

    all_fares = []

    # ── Extract flight data from page ──────────────────────────────────────
    flights = await page.evaluate("""() => {
        const results = [];

        // Try to find flight rows — JAL uses various class patterns
        const rowSelectors = [
            '[class*="flight-row"]',
            '[class*="flightRow"]',
            '[class*="flight-item"]',
            '[class*="FlightItem"]',
            'tr[class*="flight"]',
        ];
        let rows = [];
        for (const sel of rowSelectors) {
            rows = [...document.querySelectorAll(sel)];
            if (rows.length > 0) break;
        }

        for (const row of rows) {
            const text = row.innerText || row.textContent || '';

            // Extract flight number (e.g. JL047, JL 047)
            const flightMatch = text.match(/JL\\s*0?(\\d{2,4})/i);
            const flightNum = flightMatch ? 'JL' + flightMatch[1].padStart(3,'0') : '';

            // Extract departure/arrival times (HH:MM pattern)
            const times = [...text.matchAll(/(\\d{2}:\\d{2})/g)].map(m => m[1]);
            const depTime = times[0] || '';
            const arrTime = times[1] || '';

            // Extract per-fare prices — look for the price row
            // JAL shows prices in a table row, or as spans near Select buttons
            const farePrices = {};
            const fareNames = ['Economy Special', 'Economy Semi-Flex', 'Economy Flex'];

            // Approach 1: find Select buttons with price context
            const selectBtns = [...row.querySelectorAll('button, [class*="select" i]')]
                .filter(el => (el.textContent || '').trim() === 'Select');

            // Approach 2: price cells in fare comparison table
            const priceCells = [...row.querySelectorAll(
                '[class*="price" i], [class*="fare-amount" i], td[class*="fare" i]'
            )];

            // Try to match prices to fare columns by position
            const cols = [...row.querySelectorAll('td, [class*="col" i]')]
                .filter(el => el.children.length > 0 || (el.textContent || '').trim());

            // Look for yen amounts ¥ X,XXX,XXX
            const yenAmounts = [...text.matchAll(/[¥￥]\\s*([\\d,]+)/g)]
                .map(m => m[1].replace(/,/g, ''));

            // Map amounts to fare tiers (order: Special, Semi-Flex, Flex)
            yenAmounts.forEach((amt, i) => {
                if (i < fareNames.length) {
                    farePrices[fareNames[i]] = amt;
                }
            });

            if (flightNum || depTime) {
                results.push({
                    flight:   flightNum,
                    dep_time: depTime,
                    arr_time: arrTime,
                    fares:    farePrices,
                });
            }
        }
        return results;
    }""")

    if not flights:
        print("  ⚠ No flights extracted — page structure may differ from expected")
        print("    Taking diagnostic screenshot...")
        shot = shots_dir / f"diagnostic_{search['date']}_{search['origin']}_{search['destination']}.png"
        await page.screenshot(path=str(shot), full_page=True)
        print(f"    Saved: {shot}")
        return []

    date_slug = search["date"].replace("-", "")
    print(f"  → {len(flights)} flights extracted")

    for flight in flights:
        flt_id = flight["flight"] or f"UNKNOWN_{search['origin']}_{search['destination']}"

        # Screenshot
        shot_path = shots_dir / f"{date_slug}_{flt_id}_economy.png"
        try:
            await page.screenshot(path=str(shot_path), full_page=False)
        except Exception:
            pass

        fare_names_found = list(flight["fares"].keys())
        print(f"     {flt_id} {flight['dep_time']}–{flight['arr_time']}: "
              f"{fare_names_found if fare_names_found else '(no fares parsed)'}")

        for fare_name, price in flight["fares"].items():
            all_fares.append({
                "checking_date":     checking_date,
                "departing_date":    search["date"],
                "trip_type":         search["trip_type"],
                "pax_count":         search["pax"],
                "departing_airport": search["origin"],
                "arriving_airport":  search["destination"],
                "flight":            flt_id,
                "departing_time":    flight["dep_time"],
                "arrival_time":      flight["arr_time"],
                "fare_name":         fare_name,
                "price_after_promo": price,
                "currency":          "JPY",
            })

        # If no fares found, record the flight with empty fare entries
        # so we can track coverage (flight exists but fare not seen)
        if not flight["fares"]:
            for tier in JAL_FARE_TIERS:
                all_fares.append({
                    "checking_date":     checking_date,
                    "departing_date":    search["date"],
                    "trip_type":         search["trip_type"],
                    "pax_count":         search["pax"],
                    "departing_airport": search["origin"],
                    "arriving_airport":  search["destination"],
                    "flight":            flt_id,
                    "departing_time":    flight["dep_time"],
                    "arrival_time":      flight["arr_time"],
                    "fare_name":         tier,
                    "price_after_promo": "",
                    "currency":          "JPY",
                })

    if all_fares:
        csv_path = out_dir / build_filename(search)
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = _csv.DictWriter(f, fieldnames=list(all_fares[0].keys()))
            writer.writeheader()
            writer.writerows(all_fares)
        print(f"  ✓ Saved: {csv_path} ({len(all_fares)} rows)")

    return all_fares

# ─────────────────────────────────────────────────────────────────────────────
# WORKER
# ─────────────────────────────────────────────────────────────────────────────

async def run_worker(pw, worker_id, searches, force_cdp, results_list, failed_list):
    prefix = f"[W{worker_id}]"
    try:
        browser, context, page, path_used = await launch_browser(pw, force_cdp)
        print(f"{prefix} ✓ Path {path_used} browser ready")
    except Exception as e:
        print(f"{prefix} ✗ Browser launch failed: {e}")
        for s in searches:
            failed_list.append({**s, "error": str(e)})
        return

    for i, search in enumerate(searches, 1):
        label = (f"{prefix} [{i}/{len(searches)}] "
                 f"{search['origin']} → {search['destination']} | "
                 f"{search['date']} | {search['trip_type']}")
        print(label)
        last_error = None

        for attempt in range(1, MAX_RETRIES + 1):
            if attempt > 1:
                print(f"{prefix}   ↻ Retry {attempt}/{MAX_RETRIES}...")
                await page.wait_for_timeout(RETRY_DELAY * 1000)
            try:
                await page.goto(JAL_HOME, wait_until="domcontentloaded")
                await page.wait_for_timeout(4000)   # wait for dynamic overlays to appear
                await dismiss_overlays(page)
                await page.wait_for_timeout(800)    # let DOM settle after dismissal

                if await is_captcha_present(page):
                    await wait_for_captcha_solved(page)

                # Open the booking form (JAL shows a modal when you click the search widget)
                for sel in ["[class*='search-form' i]", "[class*='booking' i]",
                            "text=Select an airport/city"]:
                    try:
                        loc = page.locator(sel)
                        if await loc.count() > 0 and await loc.first.is_visible():
                            await loc.first.click(timeout=3000)
                            await page.wait_for_timeout(800)
                            break
                    except Exception:
                        pass

                await dismiss_overlays(page)        # re-check after any form interaction
                await select_trip_type(page, search["trip_type"])
                await select_airport(page, "from", search["origin"])
                await select_airport(page, "to", search["destination"])

                dep_ok = await set_departure_date(page, search["date"])
                if not dep_ok:
                    raise RuntimeError("Departure date not set")

                if search["trip_type"] == "RT":
                    ret_ok = await set_return_date(page, search["return_date"])
                    if not ret_ok:
                        raise RuntimeError("Return date not set")

                await confirm_dates(page)
                await click_search(page)

                results_ok = await wait_for_results(page)
                if not results_ok:
                    raise RuntimeError("Results page not detected")

                fares = await extract_and_save(page, search)
                results_list.append((build_filename(search), len(fares) > 0))
                last_error = None
                break

            except Exception as e:
                last_error = e
                print(f"{prefix}   ✗ Attempt {attempt}: {e}")

        if last_error is not None:
            failed_list.append({**search, "error": str(last_error)})
            results_list.append((build_filename(search), False))

    try:
        await browser.close()
    except Exception:
        pass


async def run_concurrent(pw, searches, force_cdp, n_workers):
    routes = list(dict.fromkeys((s["origin"], s["destination"]) for s in searches))
    batches = [[] for _ in range(n_workers)]
    for i, route in enumerate(routes):
        batches[i % n_workers].append(route)

    worker_searches = []
    for batch in batches:
        batch_set = set(batch)
        worker_searches.append(
            [s for s in searches if (s["origin"], s["destination"]) in batch_set]
        )

    results, failed = [], []
    tasks = [
        run_worker(pw, wid + 1, wsearches, force_cdp, results, failed)
        for wid, wsearches in enumerate(worker_searches)
        if wsearches
    ]
    await asyncio.gather(*tasks)
    return results, failed

# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

async def main():
    parser = argparse.ArgumentParser(
        description=(
            "Japan Airlines fare scraper.\n\n"
            "Default: +45d start, 7 days RT, 1 pax, 3 concurrent browsers.\n"
            "--test    : first route, first date only (quick smoke test)\n"
            "--workers : 1/2/3 concurrent browsers (default 3)\n"
            "--cdp     : force Path A (connect to user-launched Chrome)"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--cdp",     action="store_true", help="Force Path A (CDP)")
    parser.add_argument("--test",    action="store_true", help="First route, first date only")
    parser.add_argument("--workers", type=int, default=3, choices=[1, 2, 3],
                        help="Concurrent browsers (default 3)")
    args = parser.parse_args()

    routes   = load_routes()
    searches = generate_searches(routes, test_mode=args.test)
    n_workers = min(args.workers, len(routes)) if not args.test else 1

    start_time = datetime.now()
    print(f"\n{'='*60}")
    print(f"  JAL Fare Scraper — {len(searches)} searches | "
          f"{len(routes)} routes × 7 dates | {n_workers} worker(s)")
    print(f"  Output: {OUTPUT_DIR}")
    print(f"{'='*60}\n")

    async with async_playwright() as pw:
        if n_workers == 1:
            results, failed = [], []
            await run_worker(pw, 1, searches, args.cdp, results, failed)
        else:
            print(f"Starting {n_workers} concurrent browsers...")
            results, failed = await run_concurrent(pw, searches, args.cdp, n_workers)

    elapsed = datetime.now() - start_time
    mins, secs = divmod(int(elapsed.total_seconds()), 60)
    ok_count = sum(1 for _, ok in results if ok)

    print(f"\n{'='*60}")
    print(f"  Done: {ok_count}/{len(searches)} searches OK | "
          f"Elapsed: {mins}m {secs}s")
    if failed:
        print(f"  Failed ({len(failed)}):")
        for f in failed:
            print(f"    {f.get('origin')}→{f.get('destination')} "
                  f"{f.get('date')}: {f.get('error','?')}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    asyncio.run(main())
