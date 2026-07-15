"""
ANA (All Nippon Airways) Fare Scraper v1
=========================================
Scrapes ana.co.jp for branded fare coverage data.

Launch modes:
  Path B (default): Playwright launches its own Chromium headfully.
  Path A (--cdp):   Connect to user-launched Chrome via CDP.

PATH A SETUP (only if Path B is blocked):
  Launch Chrome manually:
    /Applications/Google Chrome.app/Contents/MacOS/Google Chrome
    --remote-debugging-port=9222 --user-data-dir="/tmp/chrome-nh-session"

ANA fare tiers (Economy):
  Value     — changes w/ fee, no refund, 1 checked bag
  Standard  — changes w/ fee, refund w/ fee, 2 checked bags
  Flex      — free changes, refund w/ fee, 2 checked bags
  Full Flex — free changes, free refund, 2 checked bags

Premium Economy tiers: Value, Standard (same pattern)

Results page structure: all fare columns are already visible inline per
flight row — no click-to-expand needed.

Airport selection: click field → dedicated modal opens ("Select departure
location") → type IATA into modal's own search field → click result.

Calendar: single modal, select departure day then return day, then
click "Confirm Selection" (no NEXT button — both dates in one modal).
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
ANA_HOME        = "https://www.ana.co.jp/en/us/"
OUTPUT_DIR      = Path.home() / "Documents" / "Audit" / "NH"
RESULTS_TIMEOUT = 90
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

# IATA → (city_fragment, airport_fragment) for verification.
# ANA uses "City (IATA)" notation in their modal — no full airport names shown.
# Leave airport_frag as "" for all; only verify the city fragment is present.
AIRPORT_VERIFY = {
    # Japan
    "HND": ("Haneda",        ""),
    "NRT": ("Narita",        ""),
    "KIX": ("Kansai",        ""),
    "ITM": ("Itami",         ""),
    "NGO": ("Nagoya",        ""),
    "FUK": ("Fukuoka",       ""),
    "OKA": ("Naha",          ""),
    "CTS": ("Chitose",       ""),
    # Southeast Asia
    "BKK": ("Bangkok",       ""),
    "DMK": ("Bangkok",       ""),
    "SIN": ("Singapore",     ""),
    "KUL": ("Kuala Lumpur",  ""),
    "CGK": ("Jakarta",       ""),
    "HAN": ("Hanoi",         ""),
    "SGN": ("Ho Chi Minh",   ""),
    "MNL": ("Manila",        ""),
    "RGN": ("Yangon",        ""),
    # East Asia
    "HKG": ("Hong Kong",     ""),
    "ICN": ("Seoul",         ""),
    "GMP": ("Seoul",         ""),
    "PEK": ("Beijing",       ""),
    "PKX": ("Beijing",       ""),
    "PVG": ("Shanghai",      ""),
    "SHA": ("Shanghai",      ""),
    "CAN": ("Guangzhou",     ""),
    "CTU": ("Chengdu",       ""),
    "XMN": ("Xiamen",        ""),
    "TAO": ("Qingdao",       ""),
    "TPE": ("Taipei",        ""),
    # North America
    "JFK": ("New York",      ""),
    "EWR": ("Newark",        ""),
    "LAX": ("Los Angeles",   ""),
    "SFO": ("San Francisco", ""),
    "ORD": ("Chicago",       ""),
    "IAH": ("Houston",       ""),
    "SEA": ("Seattle",       ""),
    "LAS": ("Las Vegas",     ""),
    "DEN": ("Denver",        ""),
    "YVR": ("Vancouver",     ""),
    "YYZ": ("Toronto",       ""),
    # Europe
    "LHR": ("London",        ""),
    "CDG": ("Paris",         ""),
    "FRA": ("Frankfurt",     ""),
    "MUC": ("Munich",        ""),
    "BRU": ("Brussels",      ""),
    "VIE": ("Vienna",        ""),
    "ZRH": ("Zurich",        ""),
    "DUS": ("Dusseldorf",    ""),
    "MXP": ("Milan",         ""),
    "FCO": ("Rome",          ""),
    "MAD": ("Madrid",        ""),
    "BCN": ("Barcelona",     ""),
    "HEL": ("Helsinki",      ""),
    "CPH": ("Copenhagen",    ""),
    "SVO": ("Moscow",        ""),
    # Oceania
    "SYD": ("Sydney",        ""),
    "MEL": ("Melbourne",     ""),
    # India
    "DEL": ("Delhi",         ""),
    "BOM": ("Mumbai",        ""),
}

MONTH_NAMES = ["", "January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]

ANA_FARE_TIERS = [
    "Economy Value", "Economy Standard", "Economy Flex", "Economy Full Flex",
    "Premium Economy Value", "Premium Economy Standard",
    "Business",
]

# ─────────────────────────────────────────────────────────────────────────────
# ROUTE + DATE HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def load_routes():
    routes = []
    try:
        with open(ROUTES_CSV, newline="", encoding="utf-8") as f:
            for row in _csv.DictReader(f):
                if row.get("airline", "").strip().upper() == "NH":
                    routes.append((row["departure"].strip().upper(),
                                   row["arrival"].strip().upper()))
    except FileNotFoundError:
        pass
    if not routes:
        routes = [("HND", "BKK")]
    print(f"✓ Loaded {len(routes)} NH routes")
    return routes


def generate_searches(routes, test_mode=False):
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
        searches = [s for s in searches
                    if s["origin"] == routes[0][0]
                    and s["destination"] == routes[0][1]][:1]
    return searches


def build_filename(s):
    _, mm, dd = s["date"].split("-")
    return (f"NH_{mm}{dd}_{s['pax']}pax_{s['trip_type'].lower()}_"
            f"{s['origin'].lower()}_{s['destination'].lower()}_fares.csv")

# ─────────────────────────────────────────────────────────────────────────────
# BROWSER LAUNCH
# ─────────────────────────────────────────────────────────────────────────────

async def launch_browser(pw, force_cdp=False):
    if not force_cdp:
        try:
            browser = await pw.chromium.launch(headless=False, args=STEALTH_ARGS)
            context = await browser.new_context(user_agent=STEALTH_UA)
            await context.add_init_script(
                "Object.defineProperty(navigator,'webdriver',{get:()=>undefined})"
            )
            page = await context.new_page()
            return browser, context, page, "B"
        except Exception as e:
            print(f"  Path B failed ({e}), trying Path A (CDP)...")
    browser = await pw.chromium.connect_over_cdp(CDP_URL)
    context = browser.contexts[0] if browser.contexts else await browser.new_context()
    page = context.pages[0] if context.pages else await context.new_page()
    return browser, context, page, "A"

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

async def dismiss_overlays(page):
    """
    Dismiss ANA overlays. Confirmed from DOM inspection:
    - Cookie consent: button id='ensSave' text='Apply selection and agree'
    - Cancel button: id='ensCancel' (use ensSave to accept all, not cancel)
    """
    for sel in [
        "#ensSave",                              # ANA Ensighten: "Apply selection and agree"
        "button:has-text('Apply selection and agree')",
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


async def is_captcha_present(page):
    # Be specific — ANA's cookie banner contains "robot" in its JS but is not a CAPTCHA
    url = page.url.lower()
    title = (await page.title()).lower()
    return ("captcha" in url or "captcha" in title or
            "access denied" in title or "blocked" in title)


async def wait_for_captcha_solved(page, timeout_s=300):
    print("  ⚠ CAPTCHA detected — please solve it in the browser window.")
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
    label = "Round Trip" if trip_type == "RT" else "One Way"
    print(f"  → Trip type: {label}")
    # ANA uses pill-style toggle buttons (not radio inputs)
    for sel in [
        f"button:has-text('{label}')",
        f"[class*='toggle' i]:has-text('{label}')",
        f"label:has-text('{label}')",
        f"[aria-label='{label}']",
    ]:
        try:
            loc = page.locator(sel)
            if await loc.count() > 0 and await loc.first.is_visible():
                await loc.first.click(timeout=3000)
                await page.wait_for_timeout(300)
                print(f"     ✓ {label} selected")
                return True
        except Exception:
            pass
    return False

# ─────────────────────────────────────────────────────────────────────────────
# STEP 2 — AIRPORT SELECTION  (click field → modal → search → click result)
# ─────────────────────────────────────────────────────────────────────────────

async def _modal_is_open(page):
    """Return True only if a visible airport-search dialog is on screen.
    Static text matches like 'Select departure location' can persist outside
    the modal too; require an actually-visible dialog or modal search input.
    """
    for sel in [
        "[role='dialog']:visible",
        "input[placeholder*='city' i]:visible",
        "input[placeholder*='airport' i]:visible",
    ]:
        try:
            loc = page.locator(sel)
            if await loc.count() > 0 and await loc.first.is_visible():
                return True
        except Exception:
            pass
    return False


async def select_airport(page, role, iata_code):
    """
    ANA airport selection flow (confirmed from DOM inspection):
    - From/To fields are BUTTONS (text = current selection like "Seattle[SEA]")
    - Clicking opens a modal with title "Select departure/arrival location"
    - Modal has its own text input ("Enter the city or airport")
    - Results show: city name + country on line 1, IATA code bold on line 2
    - Click the result row (li) to select

    After selecting "from", ANA may auto-open the "to" modal.
    Check if modal is already open before trying to click any button.
    """
    print(f"  → Airport ({role}): {iata_code}")
    verify = AIRPORT_VERIFY.get(iata_code.upper(), ("", ""))

    # ── Step 1: ensure the modal is open ────────────────────────────────────
    if not await _modal_is_open(page):
        # One-shot diagnostic dump: if we're on the 'to' field and the modal
        # didn't auto-open, capture DOM state so we can find the right selector.
        if role == "to":
            try:
                diag_dir = Path.home() / "Documents" / "Audit" / "NH"
                diag_dir.mkdir(parents=True, exist_ok=True)
                if not (diag_dir / "diag_post_from.html").exists():
                    html = await page.content()
                    (diag_dir / "diag_post_from.html").write_text(html, encoding="utf-8")
                    await page.screenshot(path=str(diag_dir / "diag_post_from.png"), full_page=True)
                    btn_dump = await page.evaluate("""() => {
                        const interesting = /\\[[A-Z]{3}\\]|Select|From|To|Departure|Arrival|Origin|Destination/;
                        return [...document.querySelectorAll('button')]
                            .filter(b => b.offsetParent !== null)
                            .map(b => ({
                                text: (b.innerText || b.textContent || '').trim().substring(0, 200),
                                aria: b.getAttribute('aria-label') || '',
                                cls:  b.className || '',
                                id:   b.id || '',
                                outer: (b.outerHTML || '').substring(0, 500),
                            }))
                            .filter(b => interesting.test(b.text + ' ' + b.aria + ' ' + b.cls));
                    }""")
                    import json as _json
                    (diag_dir / "diag_post_from_buttons.txt").write_text(
                        _json.dumps(btn_dump, indent=2, ensure_ascii=False), encoding="utf-8"
                    )
                    print(f"     ⓘ Diagnostic written: {diag_dir}/diag_post_from.{{html,png,_buttons.txt}}")
            except Exception as e:
                print(f"     ⓘ Diagnostic dump failed: {e}")

        clicked_field = False
        btn_index = 0 if role == "from" else 1

        # Strategy 1: buttons with [XXX] IATA pattern (filled fields)
        try:
            iata_btns = page.locator("button").filter(
                has_text=re.compile(r'\[[A-Z]{3}\]')
            )
            count = await iata_btns.count()
            if count > btn_index:
                await iata_btns.nth(btn_index).click(timeout=4000)
                await page.wait_for_timeout(1000)
                clicked_field = await _modal_is_open(page)
        except Exception:
            pass

        # Strategy 2: unfilled "to" placeholder button
        if not clicked_field and role == "to":
            for placeholder in [
                "button:has-text('Select destination')",
                "button:has-text('Arrival')",
                "button[aria-label*='destination' i]",
                "button[aria-label*='arrival' i]",
                "button[aria-label*='to' i]",
            ]:
                try:
                    loc = page.locator(placeholder)
                    if await loc.count() > 0 and await loc.first.is_visible():
                        await loc.first.click(timeout=3000)
                        await page.wait_for_timeout(1000)
                        clicked_field = await _modal_is_open(page)
                        if clicked_field:
                            break
                except Exception:
                    pass

        # Strategy 3: positional container scan
        if not clicked_field:
            for container_sel in [
                "[class*='be-wws' i]",
                "[class*='booking' i]",
                "[class*='search' i]",
                "main",
            ]:
                try:
                    container = page.locator(container_sel).first
                    if await container.count() == 0:
                        continue
                    btns = container.locator("button")
                    count = await btns.count()
                    airport_btns = []
                    for i in range(min(count, 20)):
                        btn = btns.nth(i)
                        txt = (await btn.text_content() or "").strip()
                        if re.search(r'\[[A-Z]{3}\]', txt) or txt in ("From", "To", "Departure", "Arrival"):
                            airport_btns.append(btn)
                    if len(airport_btns) > btn_index:
                        await airport_btns[btn_index].click(timeout=4000)
                        await page.wait_for_timeout(1000)
                        clicked_field = await _modal_is_open(page)
                        if clicked_field:
                            break
                except Exception:
                    pass

        if not clicked_field:
            print(f"     ✗ Could not open airport modal for {role}")
            return False

    # Find the modal's search input
    modal_input = None
    for sel in [
        "input[placeholder*='city' i]",
        "input[placeholder*='airport' i]",
        "[class*='modal' i] input[type='text']",
        "[role='dialog'] input[type='text']",
        "input[class*='search' i]:visible",
    ]:
        try:
            loc = page.locator(sel)
            if await loc.count() > 0 and await loc.first.is_visible():
                modal_input = loc.first
                break
        except Exception:
            pass

    if modal_input is None:
        print(f"     ✗ Could not find modal search input")
        return False

    await modal_input.fill("")
    await modal_input.type(iata_code, delay=100)
    await page.wait_for_timeout(1500)

    # Diagnostic screenshot
    try:
        snap = (Path.home() / "Documents" / "Audit" / "NH" / "screenshots" /
                f"diag_autocomplete_{role}_{iata_code}.png")
        snap.parent.mkdir(parents=True, exist_ok=True)
        await page.screenshot(path=str(snap), full_page=False)
    except Exception:
        pass

    # Click matching result.
    # ANA modal structure: group <li> contains multiple airport <li>s or flat spans.
    # "Bangkok (BKK)BKK" is a specific airport entry; "ThailandBangkok(All)..." is a group.
    # Strategy: collect all li elements containing the IATA code, verify city fragment,
    # then click the SHORTEST matching li (most specific = single airport row).
    suggestion_clicked = False
    city_frag, _ = verify
    best_target = None
    best_len = 9999

    for sel in [
        f"li:has-text('{iata_code}')",
        f"[role='option']:has-text('{iata_code}')",
        f"[class*='result' i]:has-text('{iata_code}')",
    ]:
        try:
            opts = page.locator(sel)
            count = await opts.count()
            for i in range(count):
                opt = opts.nth(i)
                text = (await opt.text_content() or "").strip()
                if not re.search(r'\b' + iata_code + r'\b', text, re.IGNORECASE):
                    continue
                city_ok = (not city_frag) or (city_frag.lower() in text.lower())
                if city_ok and len(text) < best_len:
                    best_len = len(text)
                    best_target = opt
        except Exception:
            pass

    if best_target is not None:
        text = (await best_target.text_content() or "").strip()
        print(f"     ✓ Matched: \"{text[:60].strip()}\"")
        await best_target.click(timeout=3000)
        suggestion_clicked = True

    if not suggestion_clicked:
        # Last resort: any element with IATA text
        for sel in [f"strong:has-text('{iata_code}')", f"b:has-text('{iata_code}')"]:
            try:
                loc = page.locator(sel).first
                if await loc.count() > 0:
                    text = await loc.text_content() or ""
                    print(f"     → Fallback strong: \"{text[:60].strip()}\"")
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
# STEP 3 — DATE SELECTION
# ANA calendar: single modal, click departure → click return → Confirm Selection
# ─────────────────────────────────────────────────────────────────────────────

async def _cal_is_open(page):
    for sel in [
        "text=Select date",
        "[class*='calendar' i]:visible",
        "[role='dialog']:has-text('Confirm Selection')",
    ]:
        try:
            if await page.locator(sel).count() > 0:
                return True
        except Exception:
            pass
    return False


async def _nav_to_month(page, target_year, target_month_num):
    target_name = MONTH_NAMES[target_month_num]
    for _ in range(24):
        content = await page.content()
        if target_name in content and str(target_year) in content:
            return True
        for sel in [
            "button[aria-label*='Next' i]",
            "button[class*='next' i]",
            "[class*='calendar'] [class*='next' i]",
            "button:has-text('>')",
            # ANA uses a ">" icon button on the right of the calendar header
            "[class*='arrow' i]:not([class*='prev' i])",
        ]:
            try:
                loc = page.locator(sel)
                if await loc.count() > 0 and await loc.first.is_visible():
                    await loc.first.click()
                    await page.wait_for_timeout(400)
                    break
            except Exception:
                pass
    return False


async def _click_day(page, day_num, year, month_num):
    """
    Click a specific day in the ANA calendar.
    ANA calendar uses date attributes like data-date="2026-07-01" or
    aria-label="2026/7/1" etc.
    """
    date_str_variants = [
        f"{year}-{month_num:02d}-{day_num:02d}",
        f"{year}/{month_num}/{day_num}",
        f"{year}/{month_num:02d}/{day_num:02d}",
    ]
    for dv in date_str_variants:
        for sel in [
            f"[data-date='{dv}']",
            f"[aria-label='{dv}']",
            f"td[data-date='{dv}']",
        ]:
            try:
                loc = page.locator(sel)
                if await loc.count() > 0 and not await loc.first.is_disabled():
                    await loc.first.click(timeout=3000)
                    return True
            except Exception:
                pass

    # Fallback: match by day number text in a non-greyed cell
    for sel in [
        f"td:has-text('{day_num}'):not([class*='disabled' i]):not([class*='other' i]):not([class*='prev' i]):not([class*='next' i])",
        f"button:has-text('{day_num}'):not([disabled])",
        f"[class*='day' i]:has-text('{day_num}'):not([class*='disabled' i])",
    ]:
        try:
            opts = page.locator(sel)
            count = await opts.count()
            for i in range(count):
                opt = opts.nth(i)
                # Must match exact day number (not e.g. 1 matching 10, 11...)
                text = (await opt.text_content() or "").strip()
                if text == str(day_num):
                    if await opt.is_visible() and not await opt.is_disabled():
                        await opt.click(timeout=3000)
                        return True
        except Exception:
            pass
    return False


async def open_date_modal(page):
    """Click the departure date field to open the ANA calendar modal."""
    for sel in [
        "[class*='departure' i][class*='date' i]",
        "[class*='date' i][class*='departure' i]",
        "button[class*='date' i]:first-of-type",
        "[aria-label*='Departure' i][aria-label*='date' i]",
        # ANA shows a date button with calendar icon
        "[class*='journey' i] [class*='date' i]",
        "input[type='text'][placeholder*='date' i]",
        # Generic: the Departure date text area
        "text=Departure",
    ]:
        try:
            loc = page.locator(sel)
            if await loc.count() > 0 and await loc.first.is_visible():
                await loc.first.click(timeout=3000)
                await page.wait_for_timeout(800)
                if await _cal_is_open(page):
                    return True
        except Exception:
            pass
    return False


async def set_dates(page, dep_date_str, ret_date_str):
    """
    Set both departure and return dates in ANA's unified calendar modal.
    Flow: open modal → nav to departure month → click dep day →
          nav to return month (if different) → click ret day →
          click "Confirm Selection".
    """
    dep_year, dep_month, dep_day = [int(x) for x in dep_date_str.split("-")]
    ret_year, ret_month, ret_day = [int(x) for x in ret_date_str.split("-")]
    print(f"  → Dates: {dep_date_str} → {ret_date_str}")

    if not await _cal_is_open(page):
        if not await open_date_modal(page):
            print("     ✗ Could not open calendar modal")
            return False

    # Navigate to departure month and click
    await _nav_to_month(page, dep_year, dep_month)
    if not await _click_day(page, dep_day, dep_year, dep_month):
        print(f"     ✗ Could not click departure day {dep_day}")
        return False
    print(f"     ✓ Departure {dep_date_str} clicked")
    await page.wait_for_timeout(600)

    # Navigate to return month and click (may already be visible)
    await _nav_to_month(page, ret_year, ret_month)
    if not await _click_day(page, ret_day, ret_year, ret_month):
        print(f"     ✗ Could not click return day {ret_day}")
        return False
    print(f"     ✓ Return {ret_date_str} clicked")
    await page.wait_for_timeout(400)

    # Click "Confirm Selection"
    for sel in [
        "button:has-text('Confirm Selection')",
        "button:has-text('Confirm')",
        "[class*='confirm' i]:visible",
    ]:
        try:
            loc = page.locator(sel)
            if await loc.count() > 0 and await loc.first.is_visible():
                await loc.first.click(timeout=3000)
                print("     ✓ Confirm Selection clicked")
                await page.wait_for_timeout(600)
                return True
        except Exception:
            pass

    print("     ⚠ Confirm Selection button not found")
    return True  # dates may still be set

# ─────────────────────────────────────────────────────────────────────────────
# STEP 4 — SEARCH BUTTON
# ─────────────────────────────────────────────────────────────────────────────

async def click_search(page):
    print("  → Clicking Search...")
    for sel in [
        "button:has-text('Search')",
        "[class*='search' i] button[type='submit']",
        "button[type='submit']",
        "[aria-label*='Search' i]",
    ]:
        try:
            loc = page.locator(sel)
            if await loc.count() > 0 and await loc.first.is_visible():
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
    for cycle in range(RESULTS_TIMEOUT // 3):
        await page.wait_for_timeout(3000)
        url = page.url
        if any(x in url for x in ["search-results", "flight-list", "availability",
                                    "reservation", "booking"]):
            # Check that actual flight content loaded
            row_count = await page.evaluate("""() => {
                return document.querySelectorAll(
                    '[class*="flight-row"], [class*="flightRow"], '
                    '[class*="flight-item"], [class*="FlightItem"]'
                ).length;
            }""")
            if row_count > 0:
                print(f"     ✓ {row_count} flight rows found")
                return True
        # Also check for date header tabs (ANA results have date tabs at top)
        tab_count = await page.evaluate("""() => {
            return document.querySelectorAll(
                '[class*="date-tab"], [class*="dateTab"], [class*="departure-date"]'
            ).length;
        }""")
        if tab_count > 0:
            print(f"     ✓ Date tabs found ({tab_count})")
            await page.wait_for_timeout(2000)
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

async def extract_and_save(page, search):
    """
    Parse ANA results page.

    Layout (from screenshots):
    - Date tabs at top (±3 days navigation, current date selected)
    - Column headers: Economy Class → Value | Standard | Flex | Full Flex
                      Premium Economy → Value | Standard
    - Each flight row: flight number + times on left, prices in each column
    - Empty cells: if a fare/flight combination has no price, cell is blank
    - No-flight dates: the date tab shows "-" (entire day has no flights)

    For RT searches: ANA shows "Destination 2" return flights in the same page,
    after the outbound section. We capture both.
    """
    checking_date = datetime.now().strftime("%Y-%m-%d")
    out_dir   = OUTPUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    shots_dir = out_dir / "screenshots"
    shots_dir.mkdir(exist_ok=True)

    await page.wait_for_timeout(2000)

    all_fares = []
    date_slug = search["date"].replace("-", "")

    flights = await page.evaluate("""() => {
        const results = [];
        const flightRowSelectors = [
            '[class*="flight-row"]',
            '[class*="flightRow"]',
            '[class*="flight-item"]',
            '[class*="FlightItem"]',
        ];
        let rows = [];
        for (const sel of flightRowSelectors) {
            rows = [...document.querySelectorAll(sel)];
            if (rows.length > 0) break;
        }

        for (const row of rows) {
            const text = row.innerText || row.textContent || '';

            // Flight number: NH followed by 2-4 digits (also possibly codeshare XX9999)
            const flightMatch = text.match(/NH\\s*0?(\\d{2,4})/i);
            const flightNum = flightMatch ? 'NH' + flightMatch[1].padStart(3, '0') : '';

            // Also capture codeshare info (e.g. NH5851 / LH2236)
            const allFlights = [...text.matchAll(/[A-Z]{2}\\s*\\d{3,4}/g)].map(m =>
                m[0].replace(/\\s+/, '')
            ).join('_');

            // Times
            const times = [...text.matchAll(/(\\d{1,2}:\\d{2}\\s*(?:a\\.m\\.|p\\.m\\.|AM|PM)?)/gi)]
                .map(m => m[1].trim());
            const depTime = times[0] || '';
            const arrTime = times[1] || '';

            // Extract USD prices: "USD X,XXX.XX" pattern
            const farePrices = {};
            const fareNames = [
                'Economy Value', 'Economy Standard', 'Economy Flex', 'Economy Full Flex',
                'Premium Economy Value', 'Premium Economy Standard'
            ];

            // USD amounts in order of appearance
            const usdAmounts = [...text.matchAll(/USD\\s*([\\d,]+\\.\\d{2})/g)]
                .map(m => m[1].replace(/,/g, ''));

            usdAmounts.forEach((amt, i) => {
                if (i < fareNames.length) {
                    farePrices[fareNames[i]] = amt;
                }
            });

            if (flightNum || depTime) {
                results.push({
                    flight:      allFlights || flightNum || '',
                    dep_time:    depTime,
                    arr_time:    arrTime,
                    fares:       farePrices,
                });
            }
        }
        return results;
    }""")

    if not flights:
        # Check if this is a no-flight day (date tab shows "-")
        no_flight = await page.evaluate("""() => {
            const tabs = document.querySelectorAll('[class*="date-tab"], [class*="dateTab"]');
            for (const tab of tabs) {
                if (tab.classList.contains('active') || tab.classList.contains('selected')) {
                    return (tab.textContent || '').includes('-');
                }
            }
            return false;
        }""")
        if no_flight:
            print(f"  ⚠ No flights on this date (date shows '-') — expected")
            return []
        print("  ⚠ No flights extracted — taking diagnostic screenshot")
        shot = shots_dir / f"diagnostic_{date_slug}_{search['origin']}_{search['destination']}.png"
        await page.screenshot(path=str(shot), full_page=True)
        print(f"    Saved: {shot}")
        return []

    print(f"  → {len(flights)} flights extracted")

    for flight in flights:
        flt_id = flight["flight"] or f"UNKNOWN_{search['origin']}_{search['destination']}"
        shot_path = shots_dir / f"{date_slug}_{flt_id}_economy.png"
        try:
            await page.screenshot(path=str(shot_path), full_page=False)
        except Exception:
            pass

        fare_names_found = list(flight["fares"].keys())
        print(f"     {flt_id} {flight['dep_time']}→{flight['arr_time']}: "
              f"{fare_names_found if fare_names_found else '(no fares)'}")

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
                "currency":          "USD",
            })

        if not flight["fares"]:
            for tier in ANA_FARE_TIERS[:4]:
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
                    "currency":          "USD",
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
                await page.goto(ANA_HOME, wait_until="domcontentloaded")
                await page.wait_for_timeout(2500)
                await dismiss_overlays(page)

                if await is_captcha_present(page):
                    await wait_for_captcha_solved(page)

                await select_trip_type(page, search["trip_type"])
                await select_airport(page, "from", search["origin"])
                await select_airport(page, "to", search["destination"])

                dates_ok = await set_dates(page, search["date"], search["return_date"])
                if not dates_ok:
                    raise RuntimeError("Dates not set")

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
            "ANA (NH) fare scraper.\n\n"
            "Default: +45d start, 7 days RT, 1 pax, 3 concurrent browsers.\n"
            "--test    : first route, first date only (quick smoke test)\n"
            "--workers : 1/2/3 concurrent browsers (default 3)\n"
            "--cdp     : force Path A (connect to user-launched Chrome)"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--cdp",     action="store_true", help="Force Path A (CDP)")
    parser.add_argument("--test",    action="store_true", help="First route, first date only")
    parser.add_argument("--workers", type=int, default=3, choices=[1, 2, 3])
    args = parser.parse_args()

    routes    = load_routes()
    searches  = generate_searches(routes, test_mode=args.test)
    n_workers = min(args.workers, len(routes)) if not args.test else 1

    start_time = datetime.now()
    print(f"\n{'='*60}")
    print(f"  NH Fare Scraper — {len(searches)} searches | "
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
