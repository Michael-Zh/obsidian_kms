"""
ANA (NH) OW Fare Scraper — v2 CDP mode
========================================
Requires Chrome started with:
  /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
    --remote-debugging-port=9222 --user-data-dir="/tmp/chrome-nh-session"
Open ana.co.jp/en/us in that window, accept cookies once.

Scraping plan (per route):
  OW, 1 pax, Mon+1mo out (non-GMP), Mon+3mo out (non-GMP only).
  GMP routes: Mon+1mo only.
  Each search opens a results page with 7-day date tabs → click each "From USD..." tab, extract fares.
Output: per-search CSV.
"""

import argparse, asyncio, csv, re, time, calendar
from datetime import date as _d, datetime, timedelta as _td
from pathlib import Path
from playwright.async_api import async_playwright

CDP_URL = "http://localhost:9222"
HOME    = "https://www.ana.co.jp/en/us/"
OUT     = Path(__file__).parent
ROUTES  = OUT / "routes.csv"
MAX_RETRIES = 2; RETRY_DELAY = 10

# ── Route / Date ──────────────────────────────────────────────────────────────

def load_routes():
    routes = []
    with open(ROUTES, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r.get("airline","").strip().upper() == "NH":
                routes.append((r["departure"].strip().upper(), r["arrival"].strip().upper()))
    if not routes: routes = [("HND","BKK")]
    print(f"✓ {len(routes)} routes")
    return routes

def next_wkday(iso, after=None):
    d = (after or _d.today()) + _td(days=1)
    while d.weekday() != iso: d += _td(days=1)
    return d

def add_months(d, n):
    m = d.month + n; y = d.year + (m-1)//12; m = (m-1)%12+1
    ld = [31,29 if y%4==0 and (y%100!=0 or y%400==0) else 28,31,30,31,30,31,31,30,31,30,31][m-1]
    return d.replace(year=y, month=m, day=min(d.day, ld))

def gen_searches(routes, test=False):
    """OW, 1pax.
    +1mo: find first Monday after +1mo mark → covers Mon-Thu.
    +3mo: find first Thursday after +3mo mark → covers Thu-Sun.
    GMP: +1mo Monday only."""
    today = _d.today()
    # First Monday in the +1mo window
    d1 = next_wkday(0, after=add_months(today, 1) - _td(days=7))
    # First Thursday in the +3mo window
    d3 = next_wkday(3, after=add_months(today, 3) - _td(days=7))
    searches = []
    for orig, dest in routes:
        gmp = "GMP" in (orig, dest)
        searches.append({"origin":orig,"dest":dest,"date":d1,"trip":"OW","pax":1})
        if not gmp:
            searches.append({"origin":orig,"dest":dest,"date":d3,"trip":"OW","pax":1})
    if test: searches = [searches[0]]
    return searches

def fname(s):
    return f"NH_{s['date'].strftime('%Y%m%d')}_{s['origin']}_{s['dest']}_ow_1pax.csv"

# ── Browser ──────────────────────────────────────────────────────────────────

async def connect(pw):
    b = await pw.chromium.connect_over_cdp(CDP_URL)
    ctx = b.contexts[0] if b.contexts else await b.new_context()
    pg = ctx.pages[0] if ctx.pages else await ctx.new_page()
    return b, ctx, pg

# ── Navigation helpers ───────────────────────────────────────────────────────

async def go_home(page):
    """Navigate to home page and accept cookies."""
    await page.goto(HOME, wait_until="domcontentloaded")
    await page.wait_for_timeout(4000)
    try:
        c = page.locator("#ensSave")
        if await c.is_visible(timeout=3000):
            await c.click(); await page.wait_for_timeout(500)
            print("    ✓ cookie accepted")
    except: pass

async def click_one_way(page):
    """Click the One Way tab (li[role=button])."""
    ow = page.locator('li[data-value="onewayOrMulticity"]').first
    for _ in range(3):
        try:
            if await ow.is_visible(timeout=3000):
                pressed = await ow.get_attribute("aria-pressed")
                if pressed != "true":
                    await ow.click(); await page.wait_for_timeout(1500)
                return True
        except: pass
        await page.wait_for_timeout(1000)
    print("    ✗ OW tab not found")
    return False

# ── Airport selection ────────────────────────────────────────────────────────

async def select_airport(page, role, iata):
    """Click departure/arrival button, type IATA in search, JS-click the option.
    ANA modal uses li[data-value] elements that need direct JS click.
    role: 'from' or 'to'."""
    if role == "from":
        btn_sel = "button.be-wws-reserve-ticket-departure-airport__button"
    else:
        btn_sel = "button.be-wws-reserve-ticket-arrival-airport__button"

    try:
        btn = page.locator(btn_sel).first
        # Click the <span> inside the button to open modal
        await btn.locator("span").first.click(timeout=5000)
        await page.wait_for_timeout(2000)
    except:
        print(f"    ✗ {role} button not found")
        return False

    # Type IATA into search input
    inp = page.locator('input[placeholder*="airport"], input[class*="searchbox"]').first
    try:
        await inp.wait_for(state="visible", timeout=5000)
        await inp.fill(iata)
        await page.wait_for_timeout(1500)
    except Exception as e:
        print(f"    ✗ {role} search input: {e}")
        return False

    # JS-click the matching data-value option
    # ANA uses data-value="HND" for Haneda, data-value="BKK+" for main Bangkok
    data_values = [iata + "+", iata]  # try "+" variant first (specific airport vs All)
    clicked = await page.evaluate(f"""(dvs) => {{
        for (const dv of dvs) {{
            const items = document.querySelectorAll('[data-value="' + dv + '"]');
            for (const el of items) {{
                if (el.offsetParent !== null) {{
                    el.scrollIntoView({{block: 'center'}});
                    el.click();
                    return 'clicked ' + dv;
                }}
            }}
        }}
        return 'not found';
    }}""", data_values)
    await page.wait_for_timeout(1000)

    # Verify
    txt = (await btn.text_content() or "").strip()
    print(f"    ✓ {role}: {txt}")
    return True

# ── Date selection ───────────────────────────────────────────────────────────

async def select_date(page, target_date):
    """Click date button, use JS to navigate calendar and click target date.

    ANA calendar has two panels (current month + next month).
    Uses JS to find panels by header text, navigate with Next button,
    click target day, and confirm selection.

    target_date: datetime.date object."""
    date_btn = page.locator("button.be-wws-reserve-ticket-departure-date__button").first

    # Open calendar
    await date_btn.click(force=True, timeout=5000)
    await page.wait_for_timeout(1500)

    # Wait for calendar panels to appear
    panels_found = await page.evaluate("""() => {
        return new Promise(resolve => {
            let tries = 0;
            const check = () => {
                const panels = document.querySelectorAll('[class*="be-calendar"]');
                const vis = Array.from(panels).filter(p => p.offsetParent !== null);
                if (vis.length > 0) resolve(vis.length);
                else if (++tries > 50) resolve(0);
                else setTimeout(check, 200);
            };
            check();
        });
    }""")
    if not panels_found:
        print("    ⚠ calendar panels not found")
        return False

    target_month = target_date.month
    target_day = target_date.day

    # Navigate to target month and click day using JS
    month_names = ["January","February","March","April","May","June",
                   "July","August","September","October","November","December"]

    for step in range(24):
        result = await page.evaluate(f"""(data) => {{
            const t_month = {target_month};
            const t_day = {target_day};
            const monthNames = {month_names};

            const panels = document.querySelectorAll('[class*="be-calendar"]');
            const visible = Array.from(panels).filter(p => p.offsetParent !== null);
            if (visible.length === 0) return {{status: 'no_panels'}};

            // Check if any visible panel shows target month
            for (const p of visible) {{
                const h = p.querySelector('[class*="header"]');
                if (!h) continue;
                const headerText = h.textContent || '';
                for (let mi = 0; mi < monthNames.length; mi++) {{
                    if (headerText.includes(monthNames[mi]) && headerText.includes('2026')) {{
                        if (mi + 1 === t_month) {{
                            // Found target month! Click the day
                            const btns = p.querySelectorAll('button');
                            for (const b of btns) {{
                                if (b.offsetParent === null) continue;
                                if (b.textContent.trim() === String(t_day)) {{
                                    b.click();
                                    return {{status: 'ok', month: monthNames[mi], day: t_day}};
                                }}
                            }}
                            return {{status: 'day_not_found', month: monthNames[mi]}};
                        }}
                    }}
                }}
            }}

            // Click Next button in visible calendar
            const nextBtns = document.querySelectorAll('button.be-calendar__button--next');
            for (const b of nextBtns) {{
                if (b.offsetParent !== null) {{
                    b.click();
                    return {{status: 'next'}};
                }}
            }}
            return {{status: 'no_next'}};
        }}""")
        if result["status"] == "ok":
            break
        elif result["status"] == "next":
            await page.wait_for_timeout(600)
            continue
        else:
            print(f"    ⚠ calendar nav: {result}")
            break

    # Confirm selection
    await page.wait_for_timeout(500)
    confirm_btn = page.locator("button:has-text('Confirm Selection')").first
    try:
        if await confirm_btn.is_visible(timeout=3000):
            await confirm_btn.click(force=True)
            await page.wait_for_timeout(500)
    except: pass

    # Verify
    final_text = (await date_btn.text_content() or "").strip()
    expected = target_date.strftime("%Y/%-m/%-d") if target_date.month < 10 else target_date.strftime("%Y/%m/%d")
    # ANA shows YYYY/M/D format
    print(f"    ✓ date: {final_text}")
    return True

# ── Search ───────────────────────────────────────────────────────────────────

async def click_search(page):
    await page.evaluate("""() => {
        const btn = document.querySelector('button.be-wws-reserve-ticket-submit__button');
        if (btn) btn.click();
    }""")
    print("    Search clicked")

async def wait_results(page, timeout=90):
    t0 = time.time()
    while time.time()-t0 < timeout:
        await page.wait_for_timeout(3000)
        body = await page.evaluate("()=>document.body.innerText")
        u = page.url
        if "server maintenance" in body.lower() or "heavy traffic" in body.lower():
            print("    ⚠ anti-bot"); await asyncio.sleep(30); continue
        if "Search Results" in body and "USD" in body:
            print("    ✓ results loaded (USD)")
            return True
        if "Search Results" in body and ("From USD" in body or "No results" in body):
            print("    ✓ results page (may have fares)")
            return True
        elapsed = int(time.time()-t0)
        if elapsed%15<3: print(f"    ... {elapsed}s")
    print("    ⚠ timeout")
    return False

# ── Extract fares from results page ──────────────────────────────────────────

async def extract_all_tabs(page, search):
    """On results page, click each date tab (by Angular button id), extract NH fares."""
    checking = datetime.now().strftime("%Y-%m-%d")
    shot_dir = OUT / "screenshots"; shot_dir.mkdir(exist_ok=True)

    await page.wait_for_timeout(3000)
    slug = search["date"].strftime("%Y%m%d")

    # Screenshot (viewport only, skip if takes too long)
    try:
        await page.evaluate("() => window.scrollTo({top: 500, behavior: 'instant'})")
        await page.wait_for_timeout(1000)
        await page.screenshot(path=str(shot_dir/f"{slug}_{search['origin']}_{search['dest']}_results.png"), timeout=5000)
        await page.evaluate("() => window.scrollTo({top: 0, behavior: 'instant'})")
        await page.wait_for_timeout(500)
    except:
        pass  # screenshot is optional, don't block on it

    # ANA results page has Angular date-nav buttons: id="c-result-date-navi-btn-0" through btn-6
    # Each button's inner spans contain: "Destination 1", "Jul 28 (Tue)", "From USD1,299.50"
    # Buttons with images (prev/next week) have different ids: "previous-week-btn-0", "next-week-btn-0"
    # Only extract from c-result-date-navi-btn-N that have "From USD" in their spans

    all_rows = []
    origin = search["origin"]
    dest = search["dest"]

    tab_btns = page.locator("button[id^='c-result-date-navi-btn-']")
    tab_count = await tab_btns.count()
    if tab_count == 0:
        print("    ⚠ no date tabs found")
        return all_rows

    # First, find global tier names from the page
    body = await page.evaluate("()=>document.body.innerText")

    for idx in range(tab_count):
        btn = tab_btns.nth(idx)

        # Get span texts to determine date and if it's a valid fare tab
        spans = await btn.locator("span").all_text_contents()
        date_label = ""
        has_fare = False
        is_selected = "selected" in (await btn.get_attribute("class") or "")

        for s in spans:
            s = s.strip()
            if re.search(r'[A-Z][a-z]{2}\s+\d{1,2}\s+\(', s):
                date_label = s  # e.g. "Jul 28 (Tue)"
            if "From USD" in s:
                has_fare = True

        if not date_label or not has_fare:
            continue

        if not is_selected:
            # JS click to bypass Angular loading spinner
            await page.evaluate(f"""() => {{
                const btn = document.querySelector('#c-result-date-navi-btn-{idx}');
                if (btn) btn.click();
            }}""")
            await page.wait_for_timeout(3000)

        # Parse current page body
        body = await page.evaluate("()=>document.body.innerText")
        tab_rows = _parse_flights(body, checking, origin, dest, date_label)
        if tab_rows:
            nf = len(set(r['flight'] for r in tab_rows))
            print(f"    [{date_label}] {len(tab_rows)} rows, {nf} flights")
            all_rows.extend(tab_rows)
        else:
            print(f"    [{date_label}] no flights")

    # Write CSV
    if all_rows:
        csv_p = OUT / fname(search)
        fields = ["checking_date","departing_date","trip_type","pax_count",
                   "departing_airport","arriving_airport","flight",
                   "departing_time","arrival_time","fare_name","price","currency"]
        with open(csv_p,"w",newline="",encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(all_rows)
        nf = len(set(r["flight"] for r in all_rows))
        print(f"    ✓ {csv_p.name} ({len(all_rows)} rows, {nf} flights)")
    else:
        print(f"    ⚠ no fares from any tab")

    return all_rows

def _parse_flights(text, checking, origin, dest, date_label):
    """Parse flight fare info from ANA results page body text.

    ANA results page structure:
    - NH flights listed as: duration | time | NH#### | Flight details
    - After each flight: "A fare selection screen will be displayed for each flight."
      followed by USD prices
    - Tier headers (Value/Standard/Flex/Full Flex) appear in page header area
    """
    rows = []

    # Find global tier names from the page header
    global_tiers = []
    for t in ["Value", "Standard", "Flex", "Full Flex"]:
        if t in text[:3000]:
            global_tiers.append(f"Economy {t}")

    if not global_tiers:
        # Some pages only show a subset
        for t in ["Value", "Standard", "Flex", "Full Flex"]:
            if t in text:
                global_tiers.append(f"Economy {t}")

    # Find all NH flight numbers
    for m in re.finditer(r'(NH\s*(\d{1,4}))', text):
        flight_num = f"NH{m.group(2).zfill(3)}"

        # Get context: ~100 chars before, up to 400 after this NH number
        start = max(0, m.start() - 150)
        ctx = text[start:m.start()]

        # Duration and times appear before NH flight number
        times = re.findall(r'(\d{1,2}:\d{2})\s*(a\.m\.|p\.m\.)?', ctx)
        dep_time = ""
        arr_time = ""
        if times:
            dep_time = times[0][0] + (times[0][1] or "")
            arr_time = times[-1][0] + (times[-1][1] or "") if len(times) > 1 else ""

        # Look for prices in the area after this flight, up to next flight
        section_start = m.end()
        # Find next NH flight or end of text
        next_nh = re.search(r'NH\s*\d{1,4}', text[section_start:])
        section_end = section_start + next_nh.start() if next_nh else len(text)
        section = text[section_start:section_end]

        # Split by fare selection screen markers
        screens = section.split("A fare selection screen will be displayed for each flight.")
        if len(screens) < 2:
            continue

        # Each screen after the first contains: "Not available" or tier-priced
        for screen in screens[1:]:
            if "Not available" in screen:
                continue
            prices = re.findall(r'USD\s*([\d,]+\.\d{2})', screen)
            for j, price in enumerate(prices):
                tier_name = global_tiers[j] if j < len(global_tiers) else f"Tier{j+1}"
                rows.append({
                    "checking_date": checking,
                    "departing_date": date_label,
                    "trip_type": "OW",
                    "pax_count": 1,
                    "departing_airport": origin,
                    "arriving_airport": dest,
                    "flight": flight_num,
                    "departing_time": dep_time,
                    "arrival_time": arr_time,
                    "fare_name": tier_name,
                    "price": price.replace(",", ""),
                    "currency": "USD",
                })

    return rows

# ── Per-search runner ────────────────────────────────────────────────────────

async def run_one(page, search, is_first):
    label = f"{search['origin']}→{search['dest']} {search['date'].strftime('%Y-%m-%d')}"
    for attempt in range(1, MAX_RETRIES+1):
        try:
            # Always start from home page for clean state
            if is_first or attempt > 1:
                await go_home(page)
            else:
                # Navigate to home
                await go_home(page)

            await click_one_way(page)
            await select_airport(page, "from", search["origin"])
            await select_airport(page, "to", search["dest"])
            await select_date(page, search["date"])
            await click_search(page)

            if not await wait_results(page):
                raise RuntimeError("no results")

            return await extract_all_tabs(page, search)

        except Exception as e:
            print(f"    ✗ {attempt}: {e}")
            if attempt < MAX_RETRIES:
                print(f"    ↻ retry {RETRY_DELAY}s...")
                await asyncio.sleep(RETRY_DELAY)
            else:
                import traceback; traceback.print_exc()
                return None

# ── Main ─────────────────────────────────────────────────────────────────────

async def main():
    p = argparse.ArgumentParser()
    p.add_argument("--test", action="store_true")
    a = p.parse_args()

    routes = load_routes()
    searches = gen_searches(routes, test=a.test)
    print(f"\n{'='*60}")
    print(f"  NH OW Scraper v2 — {len(searches)} searches | {len(routes)} routes")
    print(f"  Output: {OUT}")
    print(f"{'='*60}\n")

    async with async_playwright() as pw:
        _, _, page = await connect(pw)
        print("✓ CDP connected\n")

        t_start = time.time()
        t_prev = t_start
        ok = 0
        total = len(searches)
        for i, s in enumerate(searches, 1):
            remaining = total - i
            label = f"{s['origin']}→{s['dest']} | {s['date'].strftime('%Y-%m-%d')}"
            print(f"── [{i}/{total}] {label}  (done {i-1}/{total}, {remaining} left)")

            fares = await run_one(page, s, is_first=(i==1))
            if fares is not None:
                ok += 1

            # Timing
            now = time.time()
            dt = now - t_prev
            elapsed = now - t_start
            t_prev = now
            avg = elapsed / i
            eta = avg * remaining
            print(f"    ⏱ this: {dt:.0f}s | elapsed: {elapsed:.0f}s | avg: {avg:.0f}s/search | ETA: {eta:.0f}s\n")

        total_time = time.time() - t_start
    print(f"{'='*60}")
    print(f"  ✅ Done: {ok}/{total} OK | {total_time:.0f}s total ({total_time/total:.0f}s avg)")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    asyncio.run(main())
