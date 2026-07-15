"""
Turkish Airlines Fare Fetcher v2 — Path B → A Fallback
=======================================================
Launch strategy:
  Path B (default): Playwright launches its own Chromium headfully.
                    No manual Chrome setup needed.
  Path A (fallback): If Path B fails (bot block / CAPTCHA immediately),
                     connect to a user-launched Chrome via CDP.

To force Path A manually:
  python fetch_fares_tk_v2.py --cdp

PATH A SETUP (only needed if Path B fails):
  /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome \\
    --remote-debugging-port=9222 --user-data-dir="/tmp/chrome-tk-session"
  Then navigate to https://www.turkishairlines.com/en-tr/
"""

import argparse
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

CDP_URL        = "http://localhost:9222"
TK_HOME        = "https://www.turkishairlines.com/en-tr/"
OUTPUT_DIR     = Path.home() / "Documents" / "Audit" / "TK"
RESULTS_TIMEOUT = 60
MAX_RETRIES    = 3
RETRY_DELAY    = 5
ROUTES_CSV     = Path(__file__).parent / "routes.csv"

_ROUTES = [("IST", "AYT")]   # default for this run

MONTH_NAMES = ["", "January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]

# ─────────────────────────────────────────────────────────────────────────────
# STEALTH HEADERS  (Path B — reduce bot-detection risk)
# ─────────────────────────────────────────────────────────────────────────────

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

# ─────────────────────────────────────────────────────────────────────────────
# AIRPORT → COUNTRY  (used by country modal)
# ─────────────────────────────────────────────────────────────────────────────

AIRPORT_COUNTRY = {
    "IST": "Türkiye", "SAW": "Türkiye", "ADB": "Türkiye", "AYT": "Türkiye",
    "ESB": "Türkiye", "ADA": "Türkiye", "TZX": "Türkiye", "GZT": "Türkiye",
    "VAN": "Türkiye", "NAV": "Türkiye", "ASR": "Türkiye",
    "FRA": "Germany", "MUC": "Germany", "BER": "Germany",
    "LHR": "United Kingdom", "LGW": "United Kingdom", "MAN": "United Kingdom",
    "CDG": "France", "NCE": "France",
    "AMS": "Netherlands",
    "MAD": "Spain", "BCN": "Spain",
    "FCO": "Italy", "MXP": "Italy",
    "ATH": "Greece",
    "JFK": "United States", "LAX": "United States", "ORD": "United States",
    "SFO": "United States", "MIA": "United States", "BOS": "United States",
    "IAD": "United States", "DFW": "United States", "ATL": "United States",
    "DXB": "United Arab Emirates", "AUH": "United Arab Emirates",
    "DOH": "Qatar",
    "SIN": "Singapore",
    "BKK": "Thailand",
    "NRT": "Japan", "KIX": "Japan", "HND": "Japan",
    "PVG": "China", "PEK": "China", "CAN": "China",
    "ICN": "South Korea",
    "KUL": "Malaysia",
    "HKG": "Hong Kong",
    "DEL": "India", "BOM": "India",
    "GRU": "Brazil", "EZE": "Argentina",
    "MEX": "Mexico", "CUN": "Mexico",
    "YYZ": "Canada",
    "SYD": "Australia", "MEL": "Australia",
    "RUH": "Saudi Arabia", "JED": "Saudi Arabia",
    "CAI": "Egypt",
    "JNB": "South Africa",
    "ADD": "Ethiopia",
    "NBO": "Kenya",
}

# ─────────────────────────────────────────────────────────────────────────────
# DATE + SEARCH GENERATION
# ─────────────────────────────────────────────────────────────────────────────

def generate_search_dates(ow_only=False, add_90d=False):
    """
    Default: +45d start, 7 consecutive days, RT only (return = dep + 7d).

    --ow-only   : same 7-day window but OW 2pax instead of RT 1pax
    --add-90d   : additionally scrape +90d start, 7 consecutive days (supplemental)

    Each entry returned: (dep_str, trip_type)
    """
    today = _date.today()
    windows = [45]
    if add_90d:
        windows.append(90)

    results = []
    for offset in windows:
        start = today + _td(days=offset)
        for d in range(7):
            dep = start + _td(days=d)
            trip = "OW" if ow_only else "RT"
            results.append((dep.strftime("%Y-%m-%d"), trip))
    return results


def load_routes(csv_path=ROUTES_CSV, airline_code="TK"):
    if csv_path:
        try:
            routes = []
            with open(csv_path, newline="", encoding="utf-8") as f:
                for row in _csv.DictReader(f):
                    if row.get("airline", "").strip().upper() == airline_code.upper():
                        routes.append((row["departure"].strip().upper(),
                                       row["arrival"].strip().upper()))
            if routes:
                print(f"✓ Loaded {len(routes)} {airline_code} routes from {csv_path}")
                return routes
        except FileNotFoundError:
            pass
    return list(_ROUTES)


def build_searches(routes_csv=ROUTES_CSV, ow_only=False, add_90d=False, all_cabins=False):
    routes  = load_routes(routes_csv)
    dates   = generate_search_dates(ow_only=ow_only, add_90d=add_90d)
    searches = []
    for orig, dest in routes:
        for dep_str, trip_type in dates:
            dep = _date.fromisoformat(dep_str)
            ret = (dep + _td(days=7)).strftime("%Y-%m-%d")
            if trip_type == "OW":
                searches.append({"origin": orig, "destination": dest,
                                 "date": dep_str, "trip_type": "OW", "pax": 2,
                                 "all_cabins": all_cabins})
            else:
                searches.append({"origin": orig, "destination": dest,
                                 "date": dep_str, "return_date": ret,
                                 "trip_type": "RT", "pax": 1,
                                 "all_cabins": all_cabins})
    return searches


def build_filename(search):
    _, month, day = search["date"].split("-")
    return (f"TK_{month}{day}_{search['pax']}pax_{search['trip_type'].lower()}_"
            f"{search['origin'].lower()}_{search['destination'].lower()}.txt")

# ─────────────────────────────────────────────────────────────────────────────
# BROWSER LAUNCH  — Path B → fallback Path A
# ─────────────────────────────────────────────────────────────────────────────

async def dismiss_overlays(page):
    """Dismiss cookie banners and any ad/promo overlays blocking the page."""
    # Ad/promo overlay from Insider (ins-frameless-overlay) — close via Escape or close button
    try:
        overlay = page.locator('[id="ins-frameless-overlay"], [class*="ins-preview-wrapper"]')
        if await overlay.count() > 0:
            # Try clicking a close button inside the overlay first
            close_btn = page.locator(
                '[class*="ins-preview-wrapper"] [class*="close"], '
                '[class*="ins-preview-wrapper"] [aria-label*="close"], '
                '[class*="ins-preview-wrapper"] [aria-label*="Close"]'
            )
            if await close_btn.count() > 0:
                await close_btn.first.click()
            else:
                await page.keyboard.press("Escape")
            await page.wait_for_timeout(500)
            print("     ✓ Ad overlay dismissed")
    except Exception:
        pass

    # Cookie / consent banner
    selectors = [
        '#onetrust-accept-btn-handler',
        'button[id*="accept"]', 'button[class*="accept"]',
        '[aria-label*="Accept"]', 'button:has-text("Accept All")',
        'button:has-text("Accept")', 'button:has-text("Agree")',
        '[class*="CookieBanner"] button', '[class*="consent"] button[class*="primary"]',
    ]
    for sel in selectors:
        try:
            loc = page.locator(sel)
            if await loc.count() > 0 and await loc.first.is_visible():
                await loc.first.click()
                print(f"     ✓ Cookie banner dismissed")
                await page.wait_for_timeout(800)
                return True
        except Exception:
            pass
    return False


# Keep old name as alias so existing call sites work
dismiss_cookie_banner = dismiss_overlays


async def launch_browser(pw, force_cdp=False):
    """
    Try Path B first (own Chromium), fallback to Path A (CDP) on failure.
    Returns (browser, context, page, path_used).
    """
    if not force_cdp:
        print("→ Path B: launching own Chromium...")
        try:
            browser = await pw.chromium.launch(
                headless=False,
                args=STEALTH_ARGS,
            )
            context = await browser.new_context(
                user_agent=STEALTH_UA,
                viewport={"width": 1440, "height": 900},
                locale="en-US",
                timezone_id="Europe/Istanbul",
            )
            # Mask automation flag
            await context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                window.chrome = { runtime: {} };
            """)
            page = await context.new_page()
            await page.goto(TK_HOME, wait_until="domcontentloaded", timeout=30000)
            await page.wait_for_timeout(3000)
            await dismiss_cookie_banner(page)
            await page.wait_for_timeout(1000)
            if "access denied" in (await page.title()).lower():
                raise RuntimeError("Bot detection on load")
            # Wait up to 10s for booking form to appear
            for _attempt in range(5):
                form_visible = await page.evaluate("""() => {
                    const btn = document.querySelector('#buttonSearchflights');
                    if (!btn) return false;
                    const r = btn.getBoundingClientRect();
                    return r.width > 0 && r.height > 0;
                }""")
                if form_visible:
                    break
                await page.wait_for_timeout(2000)
            if not form_visible:
                raise RuntimeError("Booking form not visible after load")
            print("✓ Path B: browser launched, TK home loaded, form visible")
            return browser, context, page, "B"
        except Exception as e:
            print(f"  Path B failed: {e}")
            print("  → Falling back to Path A (CDP)...")

    # Path A
    print(f"→ Path A: connecting to Chrome at {CDP_URL}...")
    print("  Make sure Chrome is running with:")
    print('  /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome \\')
    print('    --remote-debugging-port=9222 --user-data-dir="/tmp/chrome-tk-session"')
    print("  Then navigate to:", TK_HOME)
    input("  Press Enter when ready...")
    try:
        browser = await pw.chromium.connect_over_cdp(CDP_URL)
        context = browser.contexts[0]
        page    = context.pages[0] if context.pages else await context.new_page()
        print(f"✓ Path A: connected. Current page: {page.url}")
        return browser, context, page, "A"
    except Exception as e:
        print(f"✗ Path A also failed: {e}")
        sys.exit(1)

# ─────────────────────────────────────────────────────────────────────────────
# SESSION HEALTH CHECK
# ─────────────────────────────────────────────────────────────────────────────

async def check_session_and_recover(page):
    form_ok = await page.evaluate("""() => {
        const btn = document.querySelector('#buttonSearchflights');
        if (!btn) return false;
        const r = btn.getBoundingClientRect();
        return r.width > 0 && r.height > 0;
    }""")
    if not form_ok:
        print("\n⚠  Booking form not visible — fix in browser then press Enter...")
        sys.stdin.readline()

# ─────────────────────────────────────────────────────────────────────────────
# CAPTCHA
# ─────────────────────────────────────────────────────────────────────────────

async def is_captcha_present(page):
    try:
        return await page.evaluate("""() => {
            const rc = document.querySelector('iframe[src*="recaptcha"], .g-recaptcha, [data-sitekey]');
            if (rc && window.getComputedStyle(rc).display !== 'none') return true;
            const hc = document.querySelector('iframe[src*="hcaptcha"], .h-captcha');
            if (hc && window.getComputedStyle(hc).display !== 'none') return true;
            const body = document.body.innerText;
            return (body.includes('robot') || body.includes('verify you are human')) && body.length < 500;
        }""")
    except Exception:
        return False


async def wait_for_captcha_solved(page):
    print("\n  ⚠  CAPTCHA — solve it in the browser window. Script resumes automatically.\n")
    try:
        await page.wait_for_function(
            """() => {
                const btn = document.querySelector('#buttonSearchflights');
                return btn !== null;
            }""",
            timeout=300_000,
        )
        print("  ✓ CAPTCHA solved\n")
    except PlaywrightTimeout:
        print("  ✗ Timed out waiting for CAPTCHA")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 1 — TRIP TYPE
# ─────────────────────────────────────────────────────────────────────────────

async def select_trip_type(page, trip_type):
    target_lower = "one way" if trip_type == "OW" else "round"
    alternatives = (["One way", "One Way"] if trip_type == "OW"
                    else ["Round trip", "Round Trip", "Return"])
    for text in alternatives:
        for role in ["radio", "button", "tab"]:
            try:
                loc = page.get_by_role(role, name=text)
                if await loc.count() > 0:
                    await loc.first.click()
                    print(f"     ✓ Trip type → {trip_type}")
                    await page.wait_for_timeout(600)
                    return
            except Exception:
                pass
    # JS fallback
    await page.evaluate("""(target) => {
        const all = document.querySelectorAll('button, label, [role="tab"]');
        for (let el of all) {
            if (el.textContent.trim().toLowerCase().includes(target)) { el.click(); return; }
        }
    }""", target_lower)
    await page.wait_for_timeout(400)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 2 — AIRPORT FIELDS
# ─────────────────────────────────────────────────────────────────────────────

async def is_country_modal_open(page):
    return await page.evaluate("""() => {
        const m = document.querySelector('[class*="thy-modal-background"]');
        if (!m) return false;
        const r = m.getBoundingClientRect();
        return r.width > 0 && r.height > 0;
    }""")


async def close_country_modal(page):
    if await is_country_modal_open(page):
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(500)


async def select_via_country_modal(page, airport_code):
    country = AIRPORT_COUNTRY.get(airport_code.upper(), "")
    modal_input = page.locator(
        '[class*="thy-modal-background"] input[type="text"], [class*="CountryModal"] input'
    )
    if country and await modal_input.count() > 0:
        inp = modal_input.first
        await inp.click(click_count=3)
        await inp.fill(country)
        await page.wait_for_timeout(700)
    if country:
        await page.evaluate("""(country) => {
            function vis(el) { const r = el.getBoundingClientRect(); return r.width > 0; }
            const items = document.querySelectorAll('[class*="countryItemLink"], [class*="CountryModal"] [role="button"]');
            for (let item of items) {
                if (vis(item) && item.textContent.trim() === country) { item.click(); return; }
            }
            for (let item of items) {
                if (vis(item) && item.textContent.trim().includes(country)) { item.click(); return; }
            }
        }""", country)
        await page.wait_for_timeout(700)

    airport_clicked = await page.evaluate("""(code) => {
        function vis(el) { const r = el.getBoundingClientRect(); return r.width > 0; }
        const pattern = '(' + code + ')';
        const candidates = [];
        for (let el of document.querySelectorAll('*')) {
            if (!vis(el) || el.children.length > 0) continue;
            const t = el.textContent.trim();
            if (t.includes(pattern) && t.length < 80) candidates.push(el);
        }
        if (candidates.length > 0) {
            candidates.sort((a, b) => a.textContent.length - b.textContent.length);
            candidates[0].click();
            return candidates[0].textContent.trim();
        }
        return null;
    }""", airport_code)

    if airport_clicked:
        await page.wait_for_timeout(500)
        print(f"     ✓ Airport: {airport_clicked}")
        return True
    await page.keyboard.press("Escape")
    return False


async def select_airport(page, field_id, airport_code):
    await close_country_modal(page)
    await page.wait_for_timeout(300)

    field = page.locator(f"#{field_id}")
    # Clear pre-filled value, then type code to trigger autocomplete
    await field.click(click_count=3)
    await field.type(airport_code, delay=80)
    await page.wait_for_timeout(1500)

    # If a country modal opened, use modal flow
    if await is_country_modal_open(page):
        return await select_via_country_modal(page, airport_code)

    # Try standard autocomplete suggestion selectors
    suggestion_selectors = [
        f'[role="option"]:has-text("{airport_code}")',
        f'[class*="portItem"]:has-text("{airport_code}")',
        f'[class*="suggest"]:has-text("{airport_code}")',
        f'[class*="AutoSuggest"] li:has-text("{airport_code}")',
        f'[class*="autosuggest"] li:has-text("{airport_code}")',
        f'[class*="airport"]:has-text("{airport_code}")',
        f'li:has-text("({airport_code})")',
    ]
    for sel in suggestion_selectors:
        try:
            loc = page.locator(sel)
            if await loc.count() > 0:
                await loc.first.click()
                await page.wait_for_timeout(500)
                print(f"     ✓ Airport {airport_code} selected")
                return True
        except Exception:
            pass

    # JS fallback: find visible element containing (CODE) pattern
    clicked = await page.evaluate("""(code) => {
        const pattern = '(' + code + ')';
        const candidates = [];
        const scope = document.querySelectorAll(
            'li, [role="option"], [class*="suggest"] *, [class*="AutoSuggest"] *'
        );
        for (let el of scope) {
            const r = el.getBoundingClientRect();
            if (r.width === 0) continue;
            const t = el.textContent.trim();
            if (t.includes(pattern) && t.length < 100) candidates.push(el);
        }
        if (candidates.length > 0) {
            candidates.sort((a, b) => a.textContent.length - b.textContent.length);
            candidates[0].click();
            return candidates[0].textContent.trim().substring(0, 50);
        }
        return null;
    }""", airport_code)

    if clicked:
        await page.wait_for_timeout(500)
        print(f"     ✓ Airport {airport_code}: {clicked}")
        return True

    print(f"     ✗ Could not select {airport_code}")
    return False

# ─────────────────────────────────────────────────────────────────────────────
# STEP 3 — CALENDAR
# ─────────────────────────────────────────────────────────────────────────────

async def _cal_is_open(page):
    return await page.evaluate("""() => {
        const cal = document.querySelector('.react-calendar');
        if (!cal) return false;
        const r = cal.getBoundingClientRect();
        const s = window.getComputedStyle(cal);
        return r.width > 0 && s.display !== 'none' && s.visibility !== 'hidden';
    }""")


async def _read_cal_label(page):
    return await page.evaluate("""() => {
        const tkBtns = document.querySelectorAll('[class*="monthDropdownButton"]');
        for (let btn of tkBtns) {
            if (btn.getBoundingClientRect().width > 0) {
                const txt = btn.textContent.trim();
                if (txt) return txt;
                if (btn.id && btn.id.startsWith('button')) {
                    const m = btn.id.slice(6).match(/^([A-Za-z]+)(\\d{4})$/);
                    if (m) return m[1] + ' ' + m[2];
                }
            }
        }
        const el = document.querySelector('.react-calendar__navigation__label__labelText--from, .react-calendar__navigation__label');
        if (el && el.getBoundingClientRect().width > 0) return el.textContent.trim();
        return '';
    }""")


async def _nav_to_month(page, year, month_num, target_month):
    for _ in range(24):
        current = await _read_cal_label(page)
        if target_month in current and str(year) in current:
            return True
        m = re.match(r'(\w+)\s+(\d{4})', current.strip())
        if m:
            cur_name = m.group(1)
            cur_year = int(m.group(2))
            cur_idx  = MONTH_NAMES.index(cur_name) if cur_name in MONTH_NAMES else 0
            go_forward = (cur_year * 12 + cur_idx) < (year * 12 + month_num)
        else:
            go_forward = True
        label = "Go to the next month" if go_forward else "Go to the previous month"
        arrow = page.locator(f'button[aria-label="{label}"]')
        if await arrow.count() > 0:
            await arrow.first.click()
            await page.wait_for_timeout(400)
        else:
            break
    return target_month in await _read_cal_label(page)


async def _click_day(page, day_str):
    tiles = page.locator('button.react-calendar__tile.react-calendar__month-view__days__day')
    cnt = await tiles.count()
    for i in range(cnt):
        tile = tiles.nth(i)
        try:
            if await tile.is_disabled():
                continue
            abbr = tile.locator('abbr')
            num_txt = ((await abbr.first.inner_text()).strip()
                       if await abbr.count() > 0
                       else re.match(r'^(\d{1,2})', (await tile.inner_text()).strip()).group(1))
            if num_txt == day_str:
                await tile.click()
                return True
        except Exception:
            pass
    return False


async def _click_calendar_ok(page):
    ok_btn = page.locator('button').filter(has_text=re.compile(r'^(OK|Tamam)$'))
    if await ok_btn.count() > 0:
        await ok_btn.first.click()
        print("     ✓ Calendar OK")
    await page.wait_for_timeout(600)


async def set_calendar_date(page, date_str):
    year, month_num, day = [int(x) for x in date_str.split("-")]
    target_month = MONTH_NAMES[month_num]
    print(f"  → Departure date: {day} {target_month} {year}")
    await close_country_modal(page)

    # TK auto-opens calendar after destination is selected — check first
    opened = await _cal_is_open(page)

    if not opened:
        for sel in ["#bookerDatepicker", "[id*='departing'][id*='date' i]",
                    "[aria-label*='Departure date' i]", "[placeholder*='Departure' i]"]:
            try:
                loc = page.locator(sel)
                if await loc.count() > 0:
                    await loc.first.click()
                    await page.wait_for_timeout(900)
                    if await _cal_is_open(page):
                        opened = True
                        break
            except Exception:
                pass

    if not opened:
        print("     ⚠ Could not open calendar")
        return False

    await _nav_to_month(page, year, month_num, target_month)
    if await _click_day(page, str(day)):
        print(f"     ✓ Day {day} clicked")
        await page.wait_for_timeout(600)
        return True
    print(f"     ✗ Could not click day {day}")
    await page.keyboard.press("Escape")
    return False


async def set_return_date(page, date_str):
    year, month_num, day = [int(x) for x in date_str.split("-")]
    target_month = MONTH_NAMES[month_num]
    print(f"  → Return date: {day} {target_month} {year}")

    if not await _cal_is_open(page):
        for sel in ["#bookerReturnDatepicker", "#returnDate",
                    "[id*='return'][id*='date' i]", "[aria-label*='Return date' i]"]:
            try:
                loc = page.locator(sel)
                if await loc.count() > 0:
                    await loc.first.click()
                    await page.wait_for_timeout(600)
                    if await _cal_is_open(page):
                        break
            except Exception:
                pass

    await _nav_to_month(page, year, month_num, target_month)
    if await _click_day(page, str(day)):
        print(f"     ✓ Return day {day} clicked")
        await page.wait_for_timeout(600)
        return True
    await page.keyboard.press("Escape")
    return False

# ─────────────────────────────────────────────────────────────────────────────
# STEP 3c — PASSENGERS
# ─────────────────────────────────────────────────────────────────────────────

async def set_passengers(page, pax_count):
    if pax_count <= 1:
        return
    print(f"  → Setting passengers to {pax_count}...")
    await page.evaluate("""() => {
        const triggers = document.querySelectorAll('[id*="pax" i], [id*="passenger" i], [class*="passengerCount"]');
        for (let el of triggers) {
            if (el.getBoundingClientRect().width > 0) { el.click(); return; }
        }
    }""")
    await page.wait_for_timeout(400)
    for _ in range(pax_count - 1):
        clicked = await page.evaluate("""() => {
            const btns = document.querySelectorAll(
                'button[aria-label*="Increase"], button[class*="increment"], button[class*="plus"]'
            );
            for (let btn of btns) {
                if (btn.getBoundingClientRect().width > 0) { btn.click(); return true; }
            }
            return false;
        }""")
        if not clicked:
            break
        await page.wait_for_timeout(200)
    print(f"     ✓ {pax_count} passengers")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 4 — WAIT FOR RESULTS
# ─────────────────────────────────────────────────────────────────────────────

async def wait_for_results(page):
    print(f"  → Waiting for results (up to {RESULTS_TIMEOUT}s)...")
    for cycle in range(RESULTS_TIMEOUT // 2):
        await page.wait_for_timeout(2000)
        url = page.url
        if "availability-international" in url or "availability" in url:
            print(f"     ✓ Results URL detected")
            try:
                await page.wait_for_function(
                    """() => document.querySelectorAll('[data-testid^="TK"]').length >= 3""",
                    timeout=45000,
                )
            except PlaywrightTimeout:
                pass
            count = await page.evaluate(
                """() => document.querySelectorAll('[data-testid^="TK"]').length"""
            )
            print(f"     ✓ {count} flight cards")
            await page.wait_for_timeout(1000)
            return True
        if await page.evaluate(
            """() => document.querySelectorAll('[data-testid^="TK"]').length"""
        ) > 0:
            return True
        if await is_captcha_present(page):
            await wait_for_captcha_solved(page)
        if cycle % 3 == 0:
            print(f"     ... {cycle*2}s | {url[:60]}")
    print(f"  ⚠  Results not detected after {RESULTS_TIMEOUT}s")
    return False

# ─────────────────────────────────────────────────────────────────────────────
# STEP 5 — EXPAND FARES & SAVE CSV
# ─────────────────────────────────────────────────────────────────────────────

async def expand_and_save(page, search):
    import csv as csv_mod

    checking_date = datetime.now().strftime("%Y-%m-%d")
    out_dir  = Path(OUTPUT_DIR)
    out_dir.mkdir(exist_ok=True)
    shots_dir = out_dir / "screenshots"
    shots_dir.mkdir(exist_ok=True)

    try:
        await page.wait_for_function(
            """() => document.querySelectorAll('[data-testid^="TK"]').length >= 1""",
            timeout=30000,
        )
    except PlaywrightTimeout:
        pass

    flight_ids = await page.evaluate("""() => {
        const ids = new Set();
        for (let el of document.querySelectorAll('[data-testid]')) {
            const tid = el.getAttribute('data-testid');
            if (tid && /^TK\\d/.test(tid)) ids.add(tid);
        }
        return [...ids];
    }""")
    print(f"  → {len(flight_ids)} TK flights found")

    all_fares = []

    for flight_id in flight_ids:
        info = await page.evaluate("""(tid) => {
            const item = document.querySelector('[data-testid="' + tid + '"]');
            if (!item) return {};
            const tm = (item.querySelector('[role="button"][aria-label*="Itinerary details"]')
                       ?.getAttribute('aria-label') || '').match(/(\\d{2}:\\d{2}) - (\\d{2}:\\d{2})/);
            const raw = item.textContent.replace(/\\s+/g, '');
            const codes = [...raw.matchAll(/(\\d{2}:\\d{2})([A-Z]{3})/g)].map(m => m[2]);
            return {
                dep_time:     tm ? tm[1] : 'N/A',
                arr_time:     tm ? tm[2] : 'N/A',
                from_airport: codes[0] || '',
                to_airport:   codes[1] || '',
            };
        }""", flight_id)

        for cabin in (["Economy", "Business"] if search.get("all_cabins") else ["Economy"]):
            sel = f'[data-testid="{flight_id}"] [aria-label*="{cabin} cabin. Best available fare"]'
            loc = page.locator(sel)
            if await loc.count() == 0:
                continue
            try:
                await dismiss_overlays(page)
                await loc.scroll_into_view_if_needed()
                await loc.click(timeout=5000)
                await page.wait_for_timeout(700)
            except Exception as e:
                print(f"     ⚠ {flight_id} {cabin}: {e}")
                continue

            fares = await page.evaluate("""(tid) => {
                const item = document.querySelector('[data-testid="' + tid + '"]');
                if (!item) return [];
                const result = [];
                for (let btn of item.querySelectorAll('button[aria-label*="Select fare package"]')) {
                    const m = btn.getAttribute('aria-label')
                        .match(/^(.+?) - ([\\d.]+)\\s+([A-Z]{3})\\s+Select fare package/);
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

            print(f"     {flight_id} {cabin}: {[f['fare_name'] for f in fares]}")

            # screenshot
            date_slug = search["date"].replace("-", "")
            shot_path = shots_dir / f"{date_slug}_{flight_id}_{cabin.lower()}.png"
            try:
                await page.screenshot(path=str(shot_path), full_page=False)
            except Exception:
                pass

    if all_fares:
        csv_name = build_filename(search).replace(".txt", "_fares.csv")
        csv_path = out_dir / csv_name
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv_mod.DictWriter(f, fieldnames=all_fares[0].keys())
            writer.writeheader()
            writer.writerows(all_fares)
        print(f"  ✓ Saved: {csv_path} ({len(all_fares)} fare rows)")
    else:
        print("  ⚠  No fares extracted")

    return all_fares

# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

async def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Turkish Airlines fare scraper.\n\n"
                    "Default: +45d start, 7 days, RT only.\n"
                    "--ow-only  : OW 2pax instead of RT (supplemental check)\n"
                    "--add-90d  : also scrape +90d window (supplemental check)\n"
                    "--test     : IST->AYT, first date only (quick smoke test)")
    parser.add_argument("--cdp",        action="store_true", help="Force Path A (CDP mode)")
    parser.add_argument("--test",       action="store_true", help="IST→AYT, first date only")
    parser.add_argument("--ow-only",    action="store_true", dest="ow_only",
                        help="Scrape OW 2pax instead of RT (supplemental)")
    parser.add_argument("--add-90d",    action="store_true", dest="add_90d",
                        help="Also scrape +90d window in addition to +45d (supplemental)")
    parser.add_argument("--all-cabins", action="store_true", dest="all_cabins",
                        help="Scrape Economy + Business (default: Economy only)")
    args = parser.parse_args()

    searches = build_searches(ow_only=args.ow_only, add_90d=args.add_90d,
                               all_cabins=args.all_cabins)
    if args.test:
        ist_ayt = [s for s in searches if s["origin"] == "IST" and s["destination"] == "AYT"]
        first_date = ist_ayt[0]["date"] if ist_ayt else None
        searches = [s for s in ist_ayt if s["date"] == first_date][:1] if first_date else []
        mode_label = f"TEST: IST→AYT, {first_date}, {searches[0]['trip_type'] if searches else '?'}"
    else:
        n_routes = len(set((s["origin"], s["destination"]) for s in searches))
        n_days   = len(set(s["date"] for s in searches))
        trip_str = "OW" if args.ow_only else "RT"
        supp     = " +90d" if args.add_90d else ""
        mode_label = f"{len(searches)} searches — {n_routes} routes × {n_days} dates, {trip_str}{supp}"

async def run_worker(pw, worker_id, searches, force_cdp, results_list, failed_list):
    """Run one browser instance over a subset of searches."""
    prefix = f"[W{worker_id}]"
    try:
        browser, context, page, path_used = await launch_browser(pw, force_cdp=force_cdp)
        print(f"{prefix} ✓ Path {path_used} browser ready")
    except Exception as e:
        print(f"{prefix} ✗ Browser launch failed: {e}")
        for s in searches:
            failed_list.append({**s, "error": f"Browser launch failed: {e}"})
            results_list.append((build_filename(s), False))
        return

    for i, search in enumerate(searches, 1):
        label = (f"{prefix} [{i}/{len(searches)}] {search['origin']} → {search['destination']} "
                 f"| {search['date']} | {search['trip_type']} | {search['pax']} pax")
        print(label)
        last_error = None

        for attempt in range(1, MAX_RETRIES + 1):
            if attempt > 1:
                print(f"{prefix}   ↻ Retry {attempt}/{MAX_RETRIES}...")
                await page.wait_for_timeout(RETRY_DELAY * 1000)
            try:
                await page.goto(TK_HOME, wait_until="domcontentloaded")
                await page.wait_for_timeout(2500)
                if await is_captcha_present(page):
                    await wait_for_captcha_solved(page)
                await check_session_and_recover(page)
                await select_trip_type(page, search["trip_type"])
                await select_airport(page, "fromPort", search["origin"])
                await select_airport(page, "toPort", search["destination"])
                date_ok = await set_calendar_date(page, search["date"])
                if not date_ok:
                    raise RuntimeError("Departure date not set")
                if search["trip_type"] == "RT" and search.get("return_date"):
                    ret_ok = await set_return_date(page, search["return_date"])
                    if not ret_ok:
                        raise RuntimeError("Return date not set")
                await _click_calendar_ok(page)
                await page.keyboard.press("Escape")
                await page.wait_for_timeout(400)
                await set_passengers(page, search["pax"])
                await page.locator("#buttonSearchflights").click()
                found = await wait_for_results(page)
                if not found:
                    raise RuntimeError("Results not detected")
                if await is_captcha_present(page):
                    await wait_for_captcha_solved(page)
                await expand_and_save(page, search)
                results_list.append((build_filename(search), True))
                last_error = None
                break
            except Exception as e:
                last_error = str(e)
                print(f"{prefix}   ✗ Attempt {attempt}: {e}")

        if last_error:
            failed_list.append({**search, "error": last_error})
            results_list.append((build_filename(search), False))

        if i < len(searches):
            await page.wait_for_timeout(3000)

    if path_used == "B":
        await browser.close()
    print(f"{prefix} Worker done.")


async def run_concurrent(pw, searches, force_cdp, n_workers):
    """Fan searches out to n_workers browsers, return (results, failed)."""
    # Split routes (not individual searches) across workers so each browser
    # handles complete route batches — avoids splitting one route's 7 dates
    routes = list(dict.fromkeys((s["origin"], s["destination"]) for s in searches))
    route_batches = [[] for _ in range(n_workers)]
    for i, route in enumerate(routes):
        route_batches[i % n_workers].append(route)

    worker_searches = []
    for batch in route_batches:
        batch_set = set(batch)
        worker_searches.append([s for s in searches
                                 if (s["origin"], s["destination"]) in batch_set])

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
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Turkish Airlines fare scraper.\n\n"
                    "Default: +45d start, 7 days, RT only, 3 concurrent browsers.\n"
                    "--ow-only     : OW 2pax instead of RT (supplemental check)\n"
                    "--add-90d     : also scrape +90d window (supplemental check)\n"
                    "--all-cabins  : Economy + Business (default: Economy only)\n"
                    "--workers N   : override concurrency (1/2/3, default 3)\n"
                    "--test        : IST->AYT, first date only (quick smoke test)")
    parser.add_argument("--cdp",        action="store_true", help="Force Path A (CDP mode)")
    parser.add_argument("--test",       action="store_true", help="IST→AYT, first date only")
    parser.add_argument("--ow-only",    action="store_true", dest="ow_only",
                        help="Scrape OW 2pax instead of RT (supplemental)")
    parser.add_argument("--add-90d",    action="store_true", dest="add_90d",
                        help="Also scrape +90d window in addition to +45d (supplemental)")
    parser.add_argument("--all-cabins", action="store_true", dest="all_cabins",
                        help="Scrape Economy + Business (default: Economy only)")
    parser.add_argument("--workers",    type=int, default=3, choices=[1, 2, 3],
                        help="Number of concurrent browsers (1-3, default 3)")
    args = parser.parse_args()

    searches = build_searches(ow_only=args.ow_only, add_90d=args.add_90d,
                               all_cabins=args.all_cabins)
    if args.test:
        ist_ayt = [s for s in searches if s["origin"] == "IST" and s["destination"] == "AYT"]
        first_date = ist_ayt[0]["date"] if ist_ayt else None
        searches = [s for s in ist_ayt if s["date"] == first_date][:1] if first_date else []
        mode_label = f"TEST: IST→AYT, {first_date}, {searches[0]['trip_type'] if searches else '?'}"
        n_workers = 1
    else:
        n_routes = len(set((s["origin"], s["destination"]) for s in searches))
        n_days   = len(set(s["date"] for s in searches))
        trip_str = "OW" if args.ow_only else "RT"
        supp     = " +90d" if args.add_90d else ""
        n_workers = min(args.workers, n_routes)   # no point in more workers than routes
        mode_label = (f"{len(searches)} searches — {n_routes} routes × {n_days} dates, "
                      f"{trip_str}{supp}, {n_workers} browser(s)")

    print("=" * 65)
    print("Turkish Airlines Fare Fetcher v2")
    print(f"Mode: {'Path A (CDP forced)' if args.cdp else 'Path B → A fallback'}")
    print(f"Searches: {len(searches)} ({mode_label})")
    print("=" * 65 + "\n")

    async with async_playwright() as pw:
        if n_workers == 1:
            # Single-worker path (same as before, no prefix noise)
            results, failed = [], []
            await run_worker(pw, 1, searches, args.cdp, results, failed)
        else:
            print(f"Starting {n_workers} concurrent browsers...")
            results, failed = await run_concurrent(pw, searches, args.cdp, n_workers)

    print(f"\n{'='*65}")
    print("Batch complete:")
    ok_results   = [(f, ok) for f, ok in results if ok]
    fail_results = [(f, ok) for f, ok in results if not ok]
    for fname, _ in sorted(ok_results):
        print(f"  ✓  {fname}")
    for fname, _ in sorted(fail_results):
        print(f"  ✗  {fname}")
    if failed:
        print(f"\n⚠  {len(failed)} failed searches. Details:")
        for s in failed:
            print(f"   {s['origin']}→{s['destination']} {s['date']}: {s.get('error','?')}")
    else:
        print("\n✓ All searches completed.")
    print("\nNext: run  python parse_tk_html.py  to generate coverage table.")


if __name__ == "__main__":
    asyncio.run(main())
