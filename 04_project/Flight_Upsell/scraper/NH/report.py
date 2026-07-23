#!/usr/bin/env python3
"""NH Brand Fare Coverage Report Generator.

Reads all NH_*.csv files, computes per-route × per-tier coverage,
generates standalone HTML report."""
import csv, json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

OUT = Path(__file__).parent
CSV_DIR = OUT

# ── Load all CSVs ──────────────────────────────────────────────────────────

def load_all():
    records = []
    for fp in sorted(CSV_DIR.glob("NH_*.csv")):
        with open(fp, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append(row)
    return records

# ── Build coverage matrix ──────────────────────────────────────────────────

def build_coverage(records):
    """route_key -> tier -> {flights_with, total_flights}"""
    # Group by (route_pair, checking_month)
    pairs = defaultdict(lambda: defaultdict(set))  # tier -> set(flight_numbers)
    all_flights = defaultdict(set)  # tier -> all unique flights

    for r in records:
        route = f"{r['departing_airport']}-{r['arriving_airport']}"
        tier = r['fare_name']
        flight = r['flight']
        pairs[route][tier].add(flight)
        all_flights[tier].add(flight)

    # Also compute total unique flights per route
    route_flights = defaultdict(set)
    for r in records:
        route = f"{r['departing_airport']}-{r['arriving_airport']}"
        route_flights[route].add(r['flight'])

    # Coverage rows
    coverage_rows = []
    all_tiers = sorted(set(r['fare_name'] for r in records))
    for route, tiers in sorted(pairs.items()):
        total = len(route_flights[route])
        for tier in all_tiers:
            flights_with = len(tiers.get(tier, set()))
            coverage_rows.append({
                "route_pair": route,
                "tier": tier,
                "flights_with": flights_with,
                "total_flights": total,
                "coverage_pct": round(flights_with / total * 100, 1) if total else 0,
            })
    return coverage_rows, all_tiers, records

# ── Price summary per route × tier ────────────────────────────────────────

def build_price_summary(records):
    summary = defaultdict(lambda: defaultdict(list))
    for r in records:
        route = f"{r['departing_airport']}-{r['arriving_airport']}"
        tier = r['fare_name']
        try:
            summary[route][tier].append(float(r['price']))
        except (ValueError, KeyError):
            pass

    result = {}
    for route, tiers in sorted(summary.items()):
        result[route] = {}
        for tier, prices in sorted(tiers.items()):
            result[route][tier] = {
                "min": min(prices),
                "max": max(prices),
                "avg": round(sum(prices) / len(prices), 2),
                "count": len(prices),
            }
    return result

# ── Flight detail ──────────────────────────────────────────────────────────

def build_flight_detail(records):
    """Per-route per-flight detail: departure times, tier prices."""
    detail = defaultdict(lambda: defaultdict(list))
    for r in records:
        route = f"{r['departing_airport']}-{r['arriving_airport']}"
        flight = r['flight']
        detail[route][flight].append(r)
    return detail

# ── HTML Report ────────────────────────────────────────────────────────────

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>NH Brand Fare Coverage Report</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#f5f5f5;color:#333;line-height:1.6}
header{background:#1a237e;color:#fff;padding:24px 32px}
header h1{font-size:1.5rem;font-weight:600}
header p{opacity:.8;margin-top:4px;font-size:.9rem}
.container{max-width:1200px;margin:0 auto;padding:24px}
.summary-cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:16px;margin-bottom:24px}
.card{background:#fff;border-radius:8px;padding:20px;box-shadow:0 1px 3px rgba(0,0,0,.1)}
.card .label{font-size:.75rem;text-transform:uppercase;color:#666;letter-spacing:.5px}
.card .value{font-size:1.8rem;font-weight:700;color:#1a237e;margin-top:4px}
h2{font-size:1.2rem;margin:32px 0 16px;color:#1a237e}
table{width:100%;border-collapse:collapse;background:#fff;border-radius:8px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,.1);margin-bottom:24px}
th,td{padding:10px 14px;text-align:left;font-size:.85rem}
th{background:#1a237e;color:#fff;font-weight:500;position:sticky;top:0}
tr:nth-child(even){background:#f8f9fa}
tr:hover{background:#e8eaf6}
.coverage-high{color:#2e7d32;font-weight:600}
.coverage-mid{color:#f57f17;font-weight:600}
.coverage-low{color:#c62828;font-weight:600}
.route-section{margin-bottom:32px}
.route-title{font-size:1rem;font-weight:600;color:#1a237e;margin-bottom:8px;padding:8px 12px;background:#e8eaf6;border-radius:4px}
.bar-container{width:100%;height:8px;background:#e0e0e0;border-radius:4px}
.bar{height:100%;border-radius:4px;transition:width .3s}
.bar-high{background:#2e7d32}
.bar-mid{background:#f57f17}
.bar-low{background:#c62828}
.price-table td{font-family:'SF Mono',Monaco,monospace;font-size:.8rem}
.footer{text-align:center;padding:32px;color:#999;font-size:.8rem}
.badge{padding:2px 8px;border-radius:10px;font-size:.75rem;font-weight:500}
.badge-green{background:#e8f5e9;color:#2e7d32}
.badge-yellow{background:#fff8e1;color:#f57f17}
.badge-red{background:#ffebee;color:#c62828}
</style>
</head>
<body>
<header>
<h1>%AIRLINE% Brand Fare Coverage</h1>
<p>Generated %DATE% · %SEARCHES% searches · %ROUTES% routes · %TOTAL_ROWS% rows</p>
</header>
<div class="container">

<div class="summary-cards">
<div class="card"><div class="label">Total Rows</div><div class="value">%TOTAL_ROWS%</div></div>
<div class="card"><div class="label">Routes</div><div class="value">%ROUTES%</div></div>
<div class="card"><div class="label">Unique Flights</div><div class="value">%FLIGHTS%</div></div>
<div class="card"><div class="label">Tiers Found</div><div class="value">%TIERS%</div></div>
</div>

<h2>1. Route × Tier Coverage Matrix</h2>
<p style="color:#666;margin-bottom:16px;font-size:.85rem">
Each cell shows: flights with this tier / total flights on this route.
Coverage % = percentage of flights on this route that offer this tier brand fare.
Green ≥80%, Yellow 50-79%, Red &lt;50%.
</p>
%COVERAGE_TABLE%

<h2>2. Per-Route Detail</h2>
%ROUTE_DETAILS%

</div>
<div class="footer">NH Brand Fare Coverage · %DATE%</div>
</body>
</html>"""

def coverage_class(pct):
    if pct >= 80: return "coverage-high", "badge-green"
    if pct >= 50: return "coverage-mid", "badge-yellow"
    return "coverage-low", "badge-red"

def bar_class(pct):
    if pct >= 80: return "bar-high"
    if pct >= 50: return "bar-mid"
    return "bar-low"

def build_coverage_table(coverage_rows, all_tiers):
    # Pivot: route × tier
    routes = sorted(set(r['route_pair'] for r in coverage_rows))
    cells = {}
    for r in coverage_rows:
        cells[(r['route_pair'], r['tier'])] = r

    html = ['<div style="overflow-x:auto"><table>']
    html.append('<thead><tr><th>Route</th>')
    for t in all_tiers:
        html.append(f'<th>{t}</th>')
    html.append('<th>Flights</th></tr></thead><tbody>')

    for route in routes:
        html.append(f'<tr><td style="font-weight:500">{route}</td>')
        for t in all_tiers:
            c = cells.get((route, t), {})
            flights_with = c.get('flights_with', 0)
            total = c.get('total_flights', 0)
            pct = c.get('coverage_pct', 0)
            cls, badge_cls = coverage_class(pct)
            bar_cls = bar_class(pct)
            html.append(
                f'<td><span class="{cls}">{flights_with}/{total}</span> '
                f'<span class="badge {badge_cls}">{pct}%</span>'
                f'<div class="bar-container"><div class="bar {bar_cls}" style="width:{pct}%"></div></div></td>'
            )
        total_flights = cells.get((route, all_tiers[0]), {}).get('total_flights', 0)
        html.append(f'<td style="font-weight:500">{total_flights}</td></tr>')
    html.append('</tbody></table></div>')
    return '\n'.join(html)

def build_route_details(coverage_rows, all_tiers, price_summary, flight_detail, records):
    routes = sorted(set(r['route_pair'] for r in coverage_rows))

    parts = []
    for route in routes:
        # Get flights on this route with tier prices
        flights = sorted(flight_detail.get(route, {}).items())

        # Build price table
        price_rows = []
        for flight_num, data in flights:
            # Get tiers for this flight
            flight_tiers = defaultdict(list)
            for r in data:
                flight_tiers[r['fare_name']].append(r['price'])
            # Get time
            times = set()
            for r in data:
                if r.get('departing_time'):
                    times.add(r['departing_time'])
            time_str = ', '.join(sorted(times)) if times else '-'

            price_row = f'<tr><td style="font-weight:500">{flight_num}</td><td>{time_str}</td>'
            for t in all_tiers:
                prices = flight_tiers.get(t, [])
                if prices:
                    p_min = min(float(p) for p in prices)
                    p_max = max(float(p) for p in prices)
                    if p_min == p_max:
                        price_row += f'<td class="price-cell">${p_min:,.2f}</td>'
                    else:
                        price_row += f'<td class="price-cell">${p_min:,.2f}–${p_max:,.2f}</td>'
                else:
                    price_row += '<td style="color:#ccc">—</td>'
            price_row += '</tr>'
            price_rows.append(price_row)

        # Coverage summary for this route
        route_cells = [c for c in coverage_rows if c['route_pair'] == route]
        tier_summary = []
        for c in route_cells:
            cls, badge_cls = coverage_class(c['coverage_pct'])
            tier_summary.append(
                f'<span class="badge {badge_cls}">{c["tier"]}: {c["flights_with"]}/{c["total_flights"]} ({c["coverage_pct"]}%)</span>'
            )

        # Price summary for route
        ps = price_summary.get(route, {})
        price_summary_html = []
        for t in all_tiers:
            if t in ps:
                p = ps[t]
                price_summary_html.append(
                    f'<tr><td>{t}</td><td class="price-cell">${p["min"]:,.2f}</td>'
                    f'<td class="price-cell">${p["max"]:,.2f}</td>'
                    f'<td class="price-cell">${p["avg"]:,.2f}</td>'
                    f'<td>{p["count"]}</td></tr>'
                )

        parts.append(f"""
<div class="route-section">
<div class="route-title">{route} · {len(flights)} flights · Tier coverage: {' '.join(tier_summary)}</div>

<h3 style="font-size:.95rem;margin:16px 0 8px">Flight × Tier Price Matrix</h3>
<div style="overflow-x:auto">
<table class="price-table">
<thead><tr><th>Flight</th><th>Time</th>{''.join(f'<th>{t}</th>' for t in all_tiers)}</tr></thead>
<tbody>{''.join(price_rows)}</tbody>
</table>
</div>
</div>""")

    return '\n'.join(parts)

# ── Main ──────────────────────────────────────────────────────────────────

def main():
    records = load_all()
    coverage_rows, all_tiers, _ = build_coverage(records)
    price_summary = build_price_summary(records)
    flight_detail = build_flight_detail(records)

    # Stats
    routes_set = set(f"{r['departing_airport']}-{r['arriving_airport']}" for r in records)
    flights_set = set(r['flight'] for r in records)

    html = HTML
    html = html.replace('%AIRLINE%', 'ANA (NH)')
    html = html.replace('%DATE%', datetime.now().strftime('%Y-%m-%d %H:%M'))
    html = html.replace('%SEARCHES%', '23')
    html = html.replace('%ROUTES%', str(len(routes_set)))
    html = html.replace('%TOTAL_ROWS%', str(len(records)))
    html = html.replace('%FLIGHTS%', str(len(flights_set)))
    html = html.replace('%TIERS%', str(len(all_tiers)))
    html = html.replace('%COVERAGE_TABLE%', build_coverage_table(coverage_rows, all_tiers))
    html = html.replace('%ROUTE_DETAILS%', build_route_details(coverage_rows, all_tiers, price_summary, flight_detail, records))

    out_path = OUT / "NH_coverage_report.html"
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'✓ {out_path} ({len(records)} rows)')

if __name__ == '__main__':
    main()
