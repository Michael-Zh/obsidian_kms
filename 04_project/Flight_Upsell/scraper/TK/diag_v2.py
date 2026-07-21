"""
Diagnostic script for TK v2 (Path B — own Chromium, en-tr locale)
Runs step-by-step with screenshots so we can see exactly where it fails.
"""
import asyncio, re
from pathlib import Path
from playwright.async_api import async_playwright

TK_HOME = "https://www.turkishairlines.com/en-tr/"
OUT = Path("TK/diag_v2")

STEALTH_ARGS = [
    "--disable-blink-features=AutomationControlled",
    "--no-sandbox", "--disable-dev-shm-usage", "--start-maximized",
]
STEALTH_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)
AIRPORT_COUNTRY = {
    "IST": "Türkiye", "AYT": "Türkiye",
}


async def shot(page, name):
    OUT.mkdir(parents=True, exist_ok=True)
    p = OUT / f"{name}.png"
    await page.screenshot(path=str(p), full_page=False)
    print(f"  📸 {p.name}")


async def main():
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=False, args=STEALTH_ARGS)
        context = await browser.new_context(
            user_agent=STEALTH_UA,
            viewport={"width": 1440, "height": 900},
            locale="en-US",
            timezone_id="Europe/Istanbul",
        )
        await context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            window.chrome = { runtime: {} };
        """)
        page = await context.new_page()

        # ── Step 1: Load TK home ──────────────────────────────────────────────
        print("\n=== Step 1: Load TK home (en-tr) ===")
        await page.goto(TK_HOME, wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)
        await shot(page, "01_home")
        print(f"  Title: {await page.title()}")

        # ── Step 2: Dismiss cookie banner ─────────────────────────────────────
        print("\n=== Step 2: Cookie banner ===")
        cookie_selectors = [
            '#onetrust-accept-btn-handler',
            'button[id*="accept"]', 'button[class*="accept"]',
            'button:has-text("Accept All")', 'button:has-text("Accept")',
        ]
        for sel in cookie_selectors:
            try:
                loc = page.locator(sel)
                if await loc.count() > 0 and await loc.first.is_visible():
                    await loc.first.click()
                    print(f"  ✓ Dismissed: {sel}")
                    await page.wait_for_timeout(800)
                    break
            except Exception:
                pass
        await shot(page, "02_after_cookie")

        # ── Step 3: Check booking form ────────────────────────────────────────
        print("\n=== Step 3: Booking form check ===")
        form_info = await page.evaluate("""() => {
            const fields = ['#fromPort', '#toPort', '#bookerDatepicker', '#buttonSearchflights'];
            const result = {};
            for (let id of fields) {
                const el = document.querySelector(id);
                if (!el) { result[id] = 'NOT FOUND'; continue; }
                const r = el.getBoundingClientRect();
                result[id] = { visible: r.width > 0 && r.height > 0, w: Math.round(r.width), h: Math.round(r.height) };
            }
            return result;
        }""")
        for k, v in form_info.items():
            print(f"  {k}: {v}")

        # ── Step 4: Click FROM field ──────────────────────────────────────────
        print("\n=== Step 4: Click #fromPort ===")
        try:
            await page.locator("#fromPort").click()
            await page.wait_for_timeout(1200)
            print("  Clicked #fromPort")
        except Exception as e:
            print(f"  ✗ {e}")
        await shot(page, "04_from_clicked")

        modal_state = await page.evaluate("""() => {
            const m = document.querySelector('[class*="thy-modal-background"]');
            if (!m) return 'no modal';
            const r = m.getBoundingClientRect();
            return r.width > 0 ? `OPEN (${Math.round(r.width)}x${Math.round(r.height)})` : 'hidden';
        }""")
        print(f"  Modal state: {modal_state}")

        # ── Step 5: Type IST into fromPort, look for autocomplete ────────────
        print("\n=== Step 5: Type IST into #fromPort (new autocomplete approach) ===")
        from_field = page.locator("#fromPort")
        await from_field.click(click_count=3)
        await from_field.type("IST", delay=80)
        await page.wait_for_timeout(1500)
        await shot(page, "05a_after_typing_ist")

        # Log what autocomplete suggestions appeared
        suggestions = await page.evaluate("""() => {
            const selectors = [
                '[role="option"]', 'li[class*="suggest"]', '[class*="portItem"]',
                '[class*="AutoSuggest"] li', '[class*="autosuggest"] li',
                '[class*="airport"]', 'li'
            ];
            const seen = new Set();
            const results = [];
            for (let sel of selectors) {
                for (let el of document.querySelectorAll(sel)) {
                    const r = el.getBoundingClientRect();
                    if (r.width === 0) continue;
                    const t = el.textContent.trim().substring(0, 60);
                    if (t.includes('IST') || t.includes('Istanbul')) {
                        if (!seen.has(t)) { seen.add(t); results.push({sel, text: t}); }
                    }
                }
            }
            return results.slice(0, 10);
        }""")
        print(f"  Suggestions found: {len(suggestions)}")
        for s in suggestions:
            print(f"    [{s['sel']}] {s['text']}")

        # Try clicking first matching suggestion
        airport_clicked = await page.evaluate("""(code) => {
            const pattern = '(' + code + ')';
            const candidates = [];
            const scope = document.querySelectorAll('li, [role="option"], [class*="suggest"] *, [class*="AutoSuggest"] *');
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
        }""", "IST")
        print(f"  Airport click result: {airport_clicked}")
        await page.wait_for_timeout(800)
        await shot(page, "05b_after_ist_click")

        # ── Step 6: Check fromPort value ──────────────────────────────────────
        print("\n=== Step 6: Check fromPort value after IST selection ===")
        from_val = await page.evaluate("""() => {
            const el = document.querySelector('#fromPort');
            if (!el) return 'not found';
            return { value: el.value || '', innerText: el.innerText?.trim().substring(0,40) || '',
                     placeholder: el.placeholder || '' };
        }""")
        print(f"  #fromPort: {from_val}")

        # ── Step 7: Type AYT into toPort ─────────────────────────────────────
        print("\n=== Step 7: Type AYT into #toPort ===")
        to_field = page.locator("#toPort")
        await to_field.click(click_count=3)
        await to_field.type("AYT", delay=80)
        await page.wait_for_timeout(1500)
        await shot(page, "07a_after_typing_ayt")

        ayt_clicked = await page.evaluate("""(code) => {
            const pattern = '(' + code + ')';
            const candidates = [];
            const scope = document.querySelectorAll('li, [role="option"], [class*="suggest"] *, [class*="AutoSuggest"] *');
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
        }""", "AYT")
        print(f"  AYT click result: {ayt_clicked}")
        await page.wait_for_timeout(800)
        await shot(page, "07b_after_ayt_click")

        # Check if calendar auto-opened after AYT selection
        cal_auto = await page.evaluate("""() => {
            const c = document.querySelector('.react-calendar');
            if (!c) return false;
            const r = c.getBoundingClientRect();
            return r.width > 0;
        }""")
        print(f"  Calendar auto-opened after AYT: {cal_auto}")

        # ── Step 8: Try opening calendar ─────────────────────────────────────
        print("\n=== Step 8: Try opening date calendar ===")
        if not cal_auto:
            await page.locator("#bookerDatepicker").click()
            await page.wait_for_timeout(900)
        cal_open = await page.evaluate("""() => {
            const c = document.querySelector('.react-calendar');
            if (!c) return false;
            const r = c.getBoundingClientRect();
            return r.width > 0;
        }""")
        print(f"  Calendar open: {cal_open}")
        if cal_open:
            await shot(page, "08_calendar_open")

        print("\n=== Done. Check TK/diag_v2/ for screenshots. ===")
        input("Press Enter to close browser...")
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
