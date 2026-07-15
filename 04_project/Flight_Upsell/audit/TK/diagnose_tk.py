"""
TK Booking Form Diagnostic
===========================
Connects to your debug Chrome, navigates to TK en-tr, and dumps:
  - Screenshots at each key step
  - Exact IDs / class names / aria-labels of every relevant element
  - Whether the calendar opens and what its class tree looks like

Run:  python diagnose_tk.py
Output goes to TK/diag/
"""

import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

CDP_URL  = "http://localhost:9222"
TK_HOME  = "https://www.turkishairlines.com/en-tr/"
OUT      = Path("TK/diag")

async def shot(page, name):
    OUT.mkdir(parents=True, exist_ok=True)
    p = OUT / f"{name}.png"
    await page.screenshot(path=str(p), full_page=False)
    print(f"  📸 {p}")

async def dump(label, data):
    print(f"\n{'─'*60}")
    print(f"  {label}")
    print(f"{'─'*60}")
    if isinstance(data, (dict, list)):
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(data)

async def main():
    OUT.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as pw:
        browser = await pw.chromium.connect_over_cdp(CDP_URL)
        ctx  = browser.contexts[0]
        page = ctx.pages[0] if ctx.pages else await ctx.new_page()
        print(f"Connected. URL: {page.url}")

        # ── 1. Navigate ───────────────────────────────────────────────────
        print("\n[1] Navigating to TK home...")
        await page.goto(TK_HOME, wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)
        await shot(page, "01_home")

        # ── 2. Trip-type buttons ──────────────────────────────────────────
        print("\n[2] Inspecting trip-type buttons...")
        trip_info = await page.evaluate("""() => {
            const results = [];
            // Cast a wide net
            const els = document.querySelectorAll(
                'button, label, input[type="radio"], [role="tab"], [role="radio"]'
            );
            for (let el of els) {
                const t = (el.textContent || el.value || '').trim();
                if (!t) continue;
                if (/(one.?way|round|return|gidiş)/i.test(t)) {
                    const r = el.getBoundingClientRect();
                    results.push({
                        tag:       el.tagName,
                        id:        el.id || null,
                        classes:   el.className,
                        role:      el.getAttribute('role'),
                        type:      el.getAttribute('type'),
                        name:      el.getAttribute('name'),
                        ariaLabel: el.getAttribute('aria-label'),
                        text:      t.substring(0, 60),
                        visible:   r.width > 0 && r.height > 0,
                    });
                }
            }
            return results;
        }""")
        await dump("Trip-type candidates", trip_info)

        # ── 3. Date fields ────────────────────────────────────────────────
        print("\n[3] Inspecting date fields...")
        date_info = await page.evaluate("""() => {
            const results = [];
            const els = document.querySelectorAll('input, button, div, span');
            for (let el of els) {
                const id    = el.id || '';
                const ph    = el.getAttribute('placeholder') || '';
                const lbl   = el.getAttribute('aria-label') || '';
                const cls   = el.className || '';
                const name  = el.getAttribute('name') || '';
                if (/(date|picker|depart|return|calendar)/i.test(id + ph + lbl + cls + name)) {
                    const r = el.getBoundingClientRect();
                    if (r.width > 0 || id) {
                        results.push({
                            tag:       el.tagName,
                            id:        id || null,
                            name:      name || null,
                            placeholder: ph || null,
                            ariaLabel: lbl || null,
                            classes:   cls.substring(0, 120),
                            visible:   r.width > 0 && r.height > 0,
                        });
                    }
                }
            }
            return results.slice(0, 30);
        }""")
        await dump("Date field candidates", date_info)

        # ── 4. Click departure date and inspect calendar ──────────────────
        print("\n[4] Clicking #bookerDatepicker (or fallbacks)...")
        clicked_sel = None
        for sel in [
            "#bookerDatepicker",
            "[id*='departing']", "[id*='depart']",
            "[aria-label*='Departure' i]", "[placeholder*='Departure' i]",
        ]:
            loc = page.locator(sel)
            cnt = await loc.count()
            if cnt > 0:
                try:
                    await loc.first.click()
                    await page.wait_for_timeout(1000)
                    clicked_sel = sel
                    print(f"  Clicked: {sel}  (found {cnt})")
                    break
                except Exception as e:
                    print(f"  Click failed on {sel}: {e}")

        await shot(page, "02_after_date_click")

        # ── 5. What opened after the click? ──────────────────────────────
        print("\n[5] Looking for calendar / datepicker popup...")
        cal_info = await page.evaluate("""() => {
            const results = [];
            // Look for ANY element that appeared and could be a calendar
            const els = document.querySelectorAll('*');
            for (let el of els) {
                const cls = el.className || '';
                if (/(calendar|datepicker|picker|month|day.?grid)/i.test(cls)) {
                    const r = el.getBoundingClientRect();
                    const s = window.getComputedStyle(el);
                    results.push({
                        tag:      el.tagName,
                        id:       el.id || null,
                        classes:  cls.substring(0, 150),
                        position: s.position,
                        display:  s.display,
                        visible:  r.width > 0 && r.height > 0,
                        rect:     { w: Math.round(r.width), h: Math.round(r.height),
                                    top: Math.round(r.top) },
                    });
                }
            }
            // De-dup by class prefix
            const seen = new Set();
            return results.filter(x => {
                const key = x.classes.substring(0, 40);
                if (seen.has(key)) return false;
                seen.add(key); return true;
            }).slice(0, 20);
        }""")
        await dump("Calendar/datepicker elements after click", cal_info)

        # ── 6. Navigation buttons inside whatever opened ──────────────────
        print("\n[6] Month navigation buttons...")
        nav_info = await page.evaluate("""() => {
            const results = [];
            const btns = document.querySelectorAll('button');
            for (let btn of btns) {
                const lbl = btn.getAttribute('aria-label') || '';
                const cls = btn.className || '';
                if (/(next|prev|month|navigate|forward|back)/i.test(lbl + cls)) {
                    const r = btn.getBoundingClientRect();
                    results.push({
                        ariaLabel: lbl,
                        classes:   cls.substring(0, 100),
                        visible:   r.width > 0 && r.height > 0,
                        rect:      { w: Math.round(r.width), h: Math.round(r.height) },
                    });
                }
            }
            return results;
        }""")
        await dump("Month navigation buttons", nav_info)

        # ── 7. Day tiles ──────────────────────────────────────────────────
        print("\n[7] Day tiles (first 5)...")
        tile_info = await page.evaluate("""() => {
            const results = [];
            const btns = document.querySelectorAll('button');
            for (let btn of btns) {
                const cls = btn.className || '';
                const lbl = btn.getAttribute('aria-label') || '';
                const txt = btn.textContent.trim();
                if (/^\d{1,2}$/.test(txt) || /(tile|day|date)/i.test(cls)) {
                    const r = btn.getBoundingClientRect();
                    if (r.width > 0) {
                        results.push({
                            text:      txt.substring(0, 20),
                            ariaLabel: lbl.substring(0, 80),
                            classes:   cls.substring(0, 120),
                            disabled:  btn.disabled,
                        });
                    }
                }
            }
            return results.slice(0, 5);
        }""")
        await dump("Day tiles (first 5 visible)", tile_info)

        # ── 8. Close & check airport modal ───────────────────────────────
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(500)

        print("\n[8] Clicking #fromPort...")
        try:
            await page.locator("#fromPort").click()
            await page.wait_for_timeout(1000)
            await shot(page, "03_after_fromport_click")
        except Exception as e:
            print(f"  Failed: {e}")

        modal_info = await page.evaluate("""() => {
            const results = [];
            const els = document.querySelectorAll('*');
            for (let el of els) {
                const cls = el.className || '';
                if (/(modal|Modal|overlay|Overlay|dropdown|Dropdown)/i.test(cls)) {
                    const r = el.getBoundingClientRect();
                    const s = window.getComputedStyle(el);
                    if (r.width > 0 && r.height > 0) {
                        results.push({
                            tag:      el.tagName,
                            id:       el.id || null,
                            classes:  cls.substring(0, 150),
                            position: s.position,
                            rect:     { w: Math.round(r.width), h: Math.round(r.height) },
                        });
                    }
                }
            }
            const seen = new Set();
            return results.filter(x => {
                const key = x.classes.substring(0, 40);
                if (seen.has(key)) return false;
                seen.add(key); return true;
            }).slice(0, 15);
        }""")
        await dump("Modal/dropdown elements after fromPort click", modal_info)

        print(f"\n{'='*60}")
        print(f"Done. Screenshots + data above — check TK/diag/ for images.")
        print(f"{'='*60}")


if __name__ == "__main__":
    asyncio.run(main())
