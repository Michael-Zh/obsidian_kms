"""
BQ Coverage Check — Enhanced with domestic/international analysis logic.

Usage:
  python3 bq_coverage_check.py TK                    # full analysis
  python3 bq_coverage_check.py TK --update-routes    # also write flagged ODs to routes.csv
  python3 bq_coverage_check.py TK --force-refresh    # force table recreate
"""

import argparse
import json
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

AUDIT_DIR  = Path(__file__).parent.parent
SQL_DIR    = Path(__file__).parent
BQ_TABLE   = "trip-ibu-adhoc.ibu_adhoc_temp.MZ_coverage_check_for_claude"
PROJECT    = "trip-ibu-adhoc"
STALE_DAYS = 30

def _routes_csv(airline: str) -> Path:
    """Per-airline routes CSV: audit/{AIRLINE}/routes.csv."""
    return AUDIT_DIR / airline.upper() / "routes.csv"

def _snapshot_csv(airline: str) -> Path:
    """BQ raw snapshot: audit/{AIRLINE}/bq_snapshot_YYYYMMDD.csv."""
    from datetime import date as _d
    stamp = _d.today().strftime("%Y%m%d")
    return AUDIT_DIR / airline.upper() / f"bq_snapshot_{stamp}.csv"

SUPPLY_COVERAGE_FLOOR    = 0.80   # absolute flag threshold
CONSISTENCY_DEVIATION    = 0.20   # pp below group median = consistency flag
DIRECTION_DIFF_THRESHOLD = 0.15   # pp difference between directions = show both
GLOBAL_VOL_PERCENTILE    = 0.75   # flag ODs only above this volume percentile (or coverage=0)

# OD count limits per country pair
OD_LIMIT_TOP  = 20   # top CP_TOP_TIER CPs by volume get this many ODs
OD_LIMIT_REST = 10   # all other CPs
CP_TOP_TIER   = 5    # number of CPs considered "top tier"

# Home country for each airline (used to determine outbound direction)
AIRLINE_HOME_COUNTRY = {
    "TK": "TR", "CA": "CN", "NH": "JP", "JL": "JP",
    "AA": "US", "UA": "US", "DL": "US", "AC": "CA", "WS": "CA",
    "EY": "AE", "EK": "AE", "QR": "QA", "SQ": "SG",
    "BA": "GB", "LH": "DE", "AF": "FR", "KL": "NL",
    "TG": "TH", "MH": "MY", "GA": "ID", "PR": "PH",
    "KE": "KR", "OZ": "KR", "CX": "HK", "BR": "TW",
}


# ─── BQ helpers ──────────────────────────────────────────────────────────────

def run_bq(query, fmt="json"):
    cmd = [
        "bq", "query",
        f"--project_id={PROJECT}",
        "--use_legacy_sql=false",
        f"--format={fmt}",
        "--max_rows=500000",
        "--quiet",
    ]
    result = subprocess.run(cmd, input=query, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"BQ error:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)
    if fmt == "json":
        return json.loads(result.stdout) if result.stdout.strip() else []
    return result.stdout


def table_last_updated():
    query = f"SELECT FORMAT_DATE('%Y-%m-%d', MAX(d)) AS last_d FROM `{BQ_TABLE}`"
    try:
        rows = run_bq(query)
        val = rows[0].get("last_d") if rows else None
        return datetime.strptime(val, "%Y-%m-%d").date() if val else None
    except SystemExit:
        return None


def check_and_refresh_table(force=False):
    print("Checking BQ table freshness...")
    last_d = table_last_updated()
    today  = date.today()
    if last_d is None:
        print("  Table not found — creating.")
        _recreate()
    elif force:
        print(f"  Last updated: {last_d} — force-refreshing.")
        _recreate()
    elif (today - last_d).days > STALE_DAYS:
        print(f"  Last updated: {last_d} ({(today - last_d).days}d ago) — refreshing.")
        _recreate()
    else:
        print(f"  Last updated: {last_d} ({(today - last_d).days}d ago) — table is fresh.")


def _recreate():
    sql = (SQL_DIR / "create_coverage_table.sql").read_text(encoding="utf-8")
    print("  Running CREATE OR REPLACE TABLE... (takes ~1-2 min)")
    cmd = ["bq", "query", f"--project_id={PROJECT}",
           "--use_legacy_sql=false", "--quiet"]
    r = subprocess.run(cmd, input=sql, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"Failed:\n{r.stderr}", file=sys.stderr)
        sys.exit(1)
    print("  OK Table refreshed.")


# ─── Analysis helpers ─────────────────────────────────────────────────────────

def _f(val):
    """Parse float safely from BQ JSON value."""
    try:
        return float(val)
    except (TypeError, ValueError):
        return None


def _primary_direction(undirected, all_directions, home_country):
    """
    Given a set of directional data for one undirected pair, decide which
    direction(s) to highlight.

    Returns: (primary_direction, secondary_direction_or_None, reason)
      primary   — the main direction to show
      secondary — second direction if coverage diff > threshold, else None
      reason    — short string explaining the choice
    """
    parts = undirected.split("-")
    c1, c2 = parts[0], parts[1]

    # volumes per direction
    dir_vols = {d["direction"]: d["direction_total"] for d in all_directions}
    dir1 = f"{c1}-{c2}"
    dir2 = f"{c2}-{c1}"

    # Determine preferred direction
    if c1 == home_country:
        primary, secondary = dir1, dir2
        reason = f"home outbound ({c1}→{c2})"
    elif c2 == home_country:
        primary, secondary = dir2, dir1
        reason = f"home outbound ({c2}→{c1})"
    else:
        # third-country: use higher volume direction
        if dir_vols.get(dir1, 0) >= dir_vols.get(dir2, 0):
            primary, secondary = dir1, dir2
        else:
            primary, secondary = dir2, dir1
        reason = f"higher volume ({primary})"

    # Check if coverage differs significantly between directions
    def avg_cov(direction):
        rows = [d for d in all_directions if d["direction"] == direction]
        if not rows:
            return None
        vals = [_f(r["supply_cov_pct"]) for r in rows if _f(r["supply_cov_pct"]) is not None]
        return sum(vals) / len(vals) if vals else None

    cov_primary   = avg_cov(primary)
    cov_secondary = avg_cov(secondary)

    if (cov_primary is not None and cov_secondary is not None and
            abs(cov_primary - cov_secondary) > DIRECTION_DIFF_THRESHOLD * 100):
        return primary, secondary, reason + " [both: large coverage diff]"

    return primary, None, reason


# ─── Domestic analysis ────────────────────────────────────────────────────────

DOMESTIC_QUERY = """
WITH base AS (
  SELECT
    airport_pair,
    brand_name,
    SUM(total_cnt)              AS total_cnt,
    SUM(has_brand_cnt)          AS has_brand_cnt,
    SUM(output_total_cnt)       AS output_total_cnt,
    SUM(output_has_brand_cnt)   AS output_has_brand_cnt,
    SAFE_DIVIDE(SUM(has_brand_cnt), SUM(total_cnt))                     AS supply_coverage,
    SAFE_DIVIDE(SUM(output_has_brand_cnt), SUM(output_total_cnt))       AS selection_coverage
  FROM `{table}`
  WHERE vc = '{airline}'
    AND d >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
    AND SPLIT(country_pair,'-')[SAFE_OFFSET(0)] = SPLIT(country_pair,'-')[SAFE_OFFSET(1)]
    AND data_level = 'airport/city level'
    AND LENGTH(TRIM(airport_pair)) > 0
  GROUP BY airport_pair, brand_name
),
od_vol AS (
  SELECT airport_pair, SUM(total_cnt) AS od_total
  FROM base GROUP BY airport_pair
),
top_ods AS (
  SELECT airport_pair, od_total,
    ROW_NUMBER() OVER (ORDER BY od_total DESC) AS rnk,
    COUNT(*) OVER () AS n_total
  FROM od_vol
  QUALIFY rnk <= {dom_od_limit}
),
fare_medians AS (
  SELECT b.brand_name,
    APPROX_QUANTILES(b.supply_coverage, 2)[OFFSET(1)] AS median_cov
  FROM base b JOIN top_ods t ON b.airport_pair = t.airport_pair
  GROUP BY b.brand_name
)
SELECT
  t.rnk, t.airport_pair, t.od_total, t.n_total,
  b.brand_name,
  ROUND(b.supply_coverage * 100, 1)                                   AS supply_cov_pct,
  ROUND(b.selection_coverage * 100, 1)                                AS selection_cov_pct,
  ROUND((b.supply_coverage - b.selection_coverage) * 100, 1)         AS filter_drop_pp,
  ROUND(fm.median_cov * 100, 1)                                       AS group_median_pct,
  ROUND((b.supply_coverage - fm.median_cov) * 100, 1)                AS deviation_pp
FROM base b
JOIN top_ods t ON b.airport_pair = t.airport_pair
JOIN fare_medians fm ON b.brand_name = fm.brand_name
ORDER BY t.od_total DESC, b.brand_name
"""


def analyze_domestic(airline):
    print(f"\nAnalyzing domestic routes for {airline}...")
    rows = run_bq(DOMESTIC_QUERY.format(table=BQ_TABLE, airline=airline, dom_od_limit=OD_LIMIT_TOP))
    if not rows:
        print("  No domestic data found.")
        return [], []

    n_total = int(rows[0]["n_total"]) if rows else 0
    top_n   = max(int(r["rnk"]) for r in rows) if rows else 0

    # Compute global domestic volume threshold (P75)
    od_vols_all = list({r["airport_pair"]: int(r["od_total"]) for r in rows}.values())
    od_vols_sorted = sorted(od_vols_all)
    dom_vol_threshold = od_vols_sorted[int(len(od_vols_sorted) * GLOBAL_VOL_PERCENTILE)] if od_vols_sorted else 0
    cutoff = min(od_vols_sorted) if od_vols_sorted else 0
    print(f"  Domestic OD pairs total: {n_total} | Top {top_n} | Min 请求量: {cutoff:,}")
    print(f"  量级门槛 (P{int(GLOBAL_VOL_PERCENTILE*100)}): {dom_vol_threshold:,} 请求量（低于门槛且coverage>0%不标记）")

    # Group by OD pair
    od_data = {}
    for r in rows:
        od = r["airport_pair"]
        if od not in od_data:
            od_data[od] = {"rnk": int(r["rnk"]), "od_total": int(r["od_total"]), "fares": []}
        cov     = _f(r["supply_cov_pct"])
        sel_cov = _f(r["selection_cov_pct"])
        drop    = _f(r["filter_drop_pp"])
        med     = _f(r["group_median_pct"])
        dev     = _f(r["deviation_pp"])
        above_threshold = int(r["od_total"]) >= dom_vol_threshold
        is_zero = (cov is not None and cov == 0)
        flag = None
        if cov is not None and cov < SUPPLY_COVERAGE_FLOOR * 100 and (above_threshold or is_zero):
            flag = "ABS"
        elif (dev is not None and dev < -CONSISTENCY_DEVIATION * 100 and (above_threshold or is_zero)):
            flag = "DEV"
        # selection flag:拿回来了但被比价过滤掉（drop > 5pp）
        sel_flag = None
        if (cov is not None and cov >= SUPPLY_COVERAGE_FLOOR * 100 and
                drop is not None and drop > 5 and (above_threshold or is_zero)):
            sel_flag = "FILTER"
        od_data[od]["fares"].append({
            "fare": r["brand_name"], "cov": cov, "sel_cov": sel_cov, "drop": drop,
            "median": med, "dev": dev, "flag": flag, "sel_flag": sel_flag,
            "above_threshold": above_threshold,
        })

    # Separate flagged vs clean
    flagged_ods = []
    filter_ods  = []   # supply OK but selection filtered
    clean_ods   = []
    for od, d in sorted(od_data.items(), key=lambda x: x[1]["rnk"]):
        supply_flags = [f["flag"] for f in d["fares"] if f["flag"]]
        sel_flags    = [f["sel_flag"] for f in d["fares"] if f["sel_flag"]]
        if supply_flags:
            flagged_ods.append({"od": od, "volume": d["od_total"], "rnk": d["rnk"],
                                 "fares": d["fares"], "flags": supply_flags})
        elif sel_flags:
            filter_ods.append({"od": od, "volume": d["od_total"], "rnk": d["rnk"],
                                "fares": d["fares"], "flags": sel_flags})
        else:
            clean_ods.append(od)

    # Print domestic summary — supply gaps
    print(f"\n  【资源缺口】 {'#':>4}  {'OD Pair':<12}  {'Trace ID':>10}  资源侧覆盖率 → 比价后覆盖率")
    print("  " + "-" * 72)
    for item in flagged_ods:
        fare_summary = "  ".join(
            f"{f['fare']}: {f['cov']:.0f}%→{f['sel_cov']:.0f}% [{f['flag']}]"
            if f["sel_cov"] is not None else
            f"{f['fare']}: {f['cov']:.0f}% [{f['flag']}]"
            for f in item["fares"] if f["flag"]
        )
        vol_note = "" if item["volume"] >= dom_vol_threshold else " (低量)"
        print(f"  #{item['rnk']:>3}  {item['od']:<12}  {item['volume']:>10,}{vol_note}  {fare_summary}")

    # Print selection filter gaps
    if filter_ods:
        print(f"\n  【比价过滤】 资源侧达标但比价后覆盖率明显下降（drop > 5pp）")
        print("  " + "-" * 72)
        for item in filter_ods:
            fare_summary = "  ".join(
                f"{f['fare']}: {f['cov']:.0f}%→{f['sel_cov']:.0f}% (↓{f['drop']:.1f}pp)"
                for f in item["fares"] if f["sel_flag"]
            )
            print(f"  #{item['rnk']:>3}  {item['od']:<12}  {item['volume']:>10,}  {fare_summary}")

    if not flagged_ods:
        print("  无国内线被标记。")
        return flagged_ods, []

    flag_rate = len(flagged_ods) / top_n if top_n else 0
    print(f"\n  被标记: {len(flagged_ods)} / {top_n} 国内 OD Pairs ({flag_rate:.0%})")

    # ── Anomaly mode: when flagged rate is high, narrow to scrape candidates ──
    ANOMALY_THRESHOLD = 0.70
    if flag_rate >= ANOMALY_THRESHOLD:
        print(f"\n  ⚠ ANOMALY: {flag_rate:.0%} 的前 {top_n} 条 OD 被标记 — 疑似系统性问题，而非个别航线问题")
        print(f"  候选精简至两组：")

        # Group A: top 3 by volume (meeting threshold or zero-coverage)
        top3 = sorted(flagged_ods, key=lambda x: -x["volume"])[:3]
        print(f"\n    Group A — 前3名（按请求量）：")
        for item in top3:
            fare_covs = "  ".join(
                f"{f['fare']}:{f['cov']:.0f}%" for f in item["fares"] if f["cov"] is not None
            )
            print(f"      {item['od']:<10}  请求量 {item['volume']:>7,}  [{fare_covs}]")

        # Group B: per-fare bottom 3 ODs (above threshold or zero-coverage)
        all_fares = sorted({f["fare"] for od in flagged_ods for f in od["fares"]})
        print(f"\n    Group B — 各运价最低覆盖率（底部3条，过滤低量）：")
        group_b_ods = set()
        for fare in all_fares:
            fare_rows = []
            for od in flagged_ods:
                fare_entry = next((f for f in od["fares"] if f["fare"] == fare), None)
                # include if above volume threshold OR coverage is 0
                if fare_entry and fare_entry["cov"] is not None:
                    qualifies = (od["volume"] >= dom_vol_threshold or fare_entry["cov"] == 0)
                    if qualifies:
                        fare_rows.append((od, fare_entry["cov"]))
            if not fare_rows:
                continue
            bottom3_fare = sorted(fare_rows, key=lambda x: x[1])[:3]
            labels = "  ".join(
                f"{od['od']}:{cov:.0f}%{'(A)' if od['od'] in {t['od'] for t in top3} else ''}"
                for od, cov in bottom3_fare
            )
            print(f"      {fare:<12}  {labels}")
            group_b_ods.update(od["od"] for od, _ in bottom3_fare)

        # Merge A + B, deduplicated
        seen = set()
        candidates = []
        for c in top3:
            if c["od"] not in seen:
                seen.add(c["od"])
                candidates.append(c)
        for od in flagged_ods:
            if od["od"] in group_b_ods and od["od"] not in seen:
                seen.add(od["od"])
                candidates.append(od)

        routes_to_scrape = [
            {"airline": airline, "dep": c["od"].split("-")[0], "arr": c["od"].split("-")[1]}
            for c in candidates
        ]
        print(f"\n  Scrape 候选（异常模式）: {len(routes_to_scrape)} 条 — "
              f"{[c['od'] for c in candidates]}")
    else:
        routes_to_scrape = [
            {"airline": airline, "dep": od["od"].split("-")[0], "arr": od["od"].split("-")[1]}
            for od in flagged_ods
        ]

    return flagged_ods, routes_to_scrape


# ─── International analysis ───────────────────────────────────────────────────

INTL_QUERY = """
WITH base_od AS (
  SELECT
    airport_pair, country_pair,
    LEAST(SPLIT(country_pair,'-')[SAFE_OFFSET(0)], SPLIT(country_pair,'-')[SAFE_OFFSET(1)]) || '-' ||
    GREATEST(SPLIT(country_pair,'-')[SAFE_OFFSET(0)], SPLIT(country_pair,'-')[SAFE_OFFSET(1)]) AS undirected_pair,
    LEAST(SPLIT(airport_pair,'-')[SAFE_OFFSET(0)], SPLIT(airport_pair,'-')[SAFE_OFFSET(1)]) || '-' ||
    GREATEST(SPLIT(airport_pair,'-')[SAFE_OFFSET(0)], SPLIT(airport_pair,'-')[SAFE_OFFSET(1)]) AS undirected_od,
    brand_name,
    SUM(total_cnt)              AS total_cnt,
    SUM(has_brand_cnt)          AS has_brand_cnt,
    SUM(output_total_cnt)       AS output_total_cnt,
    SUM(output_has_brand_cnt)   AS output_has_brand_cnt
  FROM `{table}`
  WHERE vc = '{airline}'
    AND d >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
    AND SPLIT(country_pair,'-')[SAFE_OFFSET(0)] != SPLIT(country_pair,'-')[SAFE_OFFSET(1)]
    AND data_level = 'airport/city level'
    AND LENGTH(TRIM(airport_pair)) > 0
    AND LENGTH(TRIM(country_pair)) > 0
  GROUP BY airport_pair, country_pair, undirected_pair, undirected_od, brand_name
),
cp_vol AS (
  SELECT undirected_pair, SUM(total_cnt) AS merged_total
  FROM base_od GROUP BY undirected_pair
),
top_cps AS (
  SELECT undirected_pair, merged_total,
    ROW_NUMBER() OVER (ORDER BY merged_total DESC) AS rnk
  FROM cp_vol
  QUALIFY rnk <= 50
),
od_vol AS (
  SELECT o.undirected_pair, o.undirected_od, SUM(o.total_cnt) AS od_merged_total, t.rnk AS cp_rnk
  FROM base_od o
  JOIN top_cps t ON o.undirected_pair = t.undirected_pair
  GROUP BY o.undirected_pair, o.undirected_od, t.rnk
),
top_ods_raw AS (
  SELECT undirected_pair, undirected_od, od_merged_total, cp_rnk,
    ROW_NUMBER() OVER (PARTITION BY undirected_pair ORDER BY od_merged_total DESC) AS od_rnk_in_cp
  FROM od_vol
),
top_ods_per_cp AS (
  SELECT undirected_pair, undirected_od, od_rnk_in_cp
  FROM top_ods_raw
  WHERE od_rnk_in_cp <= IF(cp_rnk <= {cp_top_tier}, {od_limit_top}, {od_limit_rest})
)
SELECT
  t.rnk,
  t.undirected_pair,
  t.merged_total,
  o.country_pair                                    AS direction,
  SUM(o.total_cnt)                                  AS direction_total,
  o.airport_pair,
  SUM(o.total_cnt)                                  AS od_total,
  o.brand_name,
  ROUND(SAFE_DIVIDE(SUM(o.has_brand_cnt), SUM(o.total_cnt)) * 100, 1)                             AS supply_cov_pct,
  ROUND(SAFE_DIVIDE(SUM(o.output_has_brand_cnt), SUM(o.output_total_cnt)) * 100, 1)               AS selection_cov_pct,
  ROUND((SAFE_DIVIDE(SUM(o.has_brand_cnt), SUM(o.total_cnt)) -
         SAFE_DIVIDE(SUM(o.output_has_brand_cnt), SUM(o.output_total_cnt))) * 100, 1)             AS filter_drop_pp,
  top_od.od_rnk_in_cp
FROM base_od o
JOIN top_cps t ON o.undirected_pair = t.undirected_pair
JOIN top_ods_per_cp top_od
  ON o.undirected_pair = top_od.undirected_pair
  AND o.undirected_od  = top_od.undirected_od
GROUP BY t.rnk, t.undirected_pair, t.merged_total, o.country_pair, o.airport_pair, o.brand_name, top_od.od_rnk_in_cp
ORDER BY t.rnk, o.country_pair, SUM(o.total_cnt) DESC, o.brand_name
"""


def analyze_international(airline):
    home = AIRLINE_HOME_COUNTRY.get(airline, "")
    print(f"\nAnalyzing international routes for {airline} (home country: {home or 'unknown'})...")
    rows = run_bq(INTL_QUERY.format(
        table=BQ_TABLE, airline=airline,
        cp_top_tier=CP_TOP_TIER, od_limit_top=OD_LIMIT_TOP, od_limit_rest=OD_LIMIT_REST,
    ))
    if not rows:
        print("  No international data found.")
        return [], []

    # Build nested structure: undirected_pair → direction → airport_pair → fare
    cp_data = {}
    for r in rows:
        up = r["undirected_pair"]
        if up not in cp_data:
            cp_data[up] = {"rnk": int(r["rnk"]), "merged_total": int(r["merged_total"]),
                           "directions": {}}
        dr = r["direction"]
        if dr not in cp_data[up]["directions"]:
            cp_data[up]["directions"][dr] = {
                "direction_total": int(r["direction_total"]),
                "airport_pairs": {}
            }
        od = r["airport_pair"]
        if od not in cp_data[up]["directions"][dr]["airport_pairs"]:
            cp_data[up]["directions"][dr]["airport_pairs"][od] = {
                "od_total": int(r["od_total"]),
                "od_rnk_in_cp": int(r["od_rnk_in_cp"]),
                "fares": []
            }
        cp_data[up]["directions"][dr]["airport_pairs"][od]["fares"].append({
            "fare": r["brand_name"],
            "cov": _f(r["supply_cov_pct"]),
            "sel_cov": _f(r["selection_cov_pct"]),
            "drop": _f(r["filter_drop_pp"]),
        })

    # Compute global volume threshold (P75 of all OD od_merged_total across all CPs)
    all_od_vols = []
    for up, d in cp_data.items():
        seen_ods = set()
        for dr, ddata in d["directions"].items():
            for od, odata in ddata["airport_pairs"].items():
                und_od = "-".join(sorted(od.split("-")))
                if und_od not in seen_ods:
                    seen_ods.add(und_od)
                    all_od_vols.append(odata["od_total"])
    all_od_vols_sorted = sorted(all_od_vols)
    vol_threshold = all_od_vols_sorted[int(len(all_od_vols_sorted) * GLOBAL_VOL_PERCENTILE)] if all_od_vols_sorted else 0
    print(f"  Global OD volume P{int(GLOBAL_VOL_PERCENTILE*100)} threshold: {vol_threshold:,} 请求量")

    # Step 1: Country-pair level flag
    cp_summary = []
    for up, d in sorted(cp_data.items(), key=lambda x: x[1]["rnk"]):
        all_dir_rows = []
        for dr, ddata in d["directions"].items():
            for od, odata in ddata["airport_pairs"].items():
                for f in odata["fares"]:
                    all_dir_rows.append({
                        "direction": dr,
                        "direction_total": ddata["direction_total"],
                        "od": od, "od_total": odata["od_total"],
                        "fare": f["fare"], "cov": f["cov"],
                    })

        primary, secondary, dir_reason = _primary_direction(up, [
            {"direction": dr, "direction_total": ddata["direction_total"],
             "supply_cov_pct": sum(
                 f["cov"] or 0
                 for od_d in ddata["airport_pairs"].values()
                 for f in od_d["fares"]
             ) / max(1, sum(
                 1 for od_d in ddata["airport_pairs"].values()
                 for f in od_d["fares"]
             ))}
            for dr, ddata in d["directions"].items()
        ], home)

        show_directions = [primary] + ([secondary] if secondary else [])

        def weighted_avg_cov(direction):
            od_map = d["directions"].get(direction, {}).get("airport_pairs", {})
            fare_stats = {}
            for od, odata in od_map.items():
                for f in odata["fares"]:
                    if f["fare"] not in fare_stats:
                        fare_stats[f["fare"]] = {"sum_cov_vol": 0, "sum_vol": 0}
                    if f["cov"] is not None:
                        fare_stats[f["fare"]]["sum_cov_vol"] += f["cov"] * odata["od_total"]
                        fare_stats[f["fare"]]["sum_vol"] += odata["od_total"]
            return {fare: (s["sum_cov_vol"] / s["sum_vol"] if s["sum_vol"] else None)
                    for fare, s in fare_stats.items()}

        fare_covs = weighted_avg_cov(primary)
        cp_flagged = any(v is not None and v < SUPPLY_COVERAGE_FLOOR * 100
                         for v in fare_covs.values())

        # Top 3 ODs in primary direction for context display
        od_map_primary = d["directions"].get(primary, {}).get("airport_pairs", {})
        top3_ods = sorted(od_map_primary.items(), key=lambda x: -x[1]["od_total"])[:3]

        cp_summary.append({
            "undirected_pair": up,
            "rnk": d["rnk"],
            "merged_total": d["merged_total"],
            "primary_direction": primary,
            "secondary_direction": secondary,
            "dir_reason": dir_reason,
            "show_directions": show_directions,
            "fare_covs_primary": fare_covs,
            "cp_flagged": cp_flagged,
            "top3_ods": top3_ods,
            "od_data": d,
        })

    flagged_cps = [c for c in cp_summary if c["cp_flagged"]]

    # Print Step 1 summary — show ALL CPs with top 3 ODs for context
    od_limit_info = f"（前{CP_TOP_TIER}名最多{OD_LIMIT_TOP}条OD，其余最多{OD_LIMIT_REST}条）"
    print(f"\n  Step 1 — Top 50 国际 Country Pairs  {od_limit_info}")
    print(f"  量级门槛：全局OD P{int(GLOBAL_VOL_PERCENTILE*100)} = {vol_threshold:,} 请求量（低于门槛且coverage>0%不标记）")
    print()

    for cp in cp_summary[:20]:
        flag_str = ""
        if cp["cp_flagged"]:
            bad = [f"{f}:{v:.0f}%" for f, v in cp["fare_covs_primary"].items()
                   if v is not None and v < SUPPLY_COVERAGE_FLOOR * 100]
            flag_str = "  ← " + ", ".join(bad) + " ⚠"
        print(f"  [{cp['rnk']:>3}] {cp['undirected_pair']:<10}  "
              f"请求量 {cp['merged_total']:>10,}  {cp['primary_direction']:<10}{flag_str}")
        # Top 3 ODs for scale context
        for od, odata in cp["top3_ods"]:
            fare_snaps = "  ".join(
                f"{f['fare'][:6]}:{f['cov']:.0f}%" if f["cov"] is not None else f"{f['fare'][:6]}:—"
                for f in odata["fares"]
            )
            print(f"         #{odata['od_rnk_in_cp']:>2} {od:<10}  请求量 {odata['od_total']:>7,}  {fare_snaps}")
        print()

    if len(cp_summary) > 20:
        n_flag_in_rest = sum(1 for c in cp_summary[20:] if c["cp_flagged"])
        print(f"  ... 另有 {len(cp_summary) - 20} 个 country pair（其中 {n_flag_in_rest} 个有问题，详见JSON输出）")

    print(f"\n  被标记 Country Pairs: {len(flagged_cps)} / {len(cp_summary)}")

    # Step 2: OD-level drill-down for ALL country pairs
    routes_to_scrape = []
    print(f"\n  Step 2 — OD 明细（共 {len(cp_summary)} 个 Country Pairs）")

    for cp in cp_summary:
        od_limit = OD_LIMIT_TOP if cp["rnk"] <= CP_TOP_TIER else OD_LIMIT_REST
        print(f"\n  [{cp['rnk']:>3}] {cp['undirected_pair']}  "
              f"(请求量 {cp['merged_total']:,})  方向: {cp['dir_reason']}  "
              f"[OD上限: {od_limit}]")

        for direction in cp["show_directions"]:
            od_map = cp["od_data"]["directions"].get(direction, {}).get("airport_pairs", {})
            if not od_map:
                continue

            sorted_ods = sorted(od_map.items(), key=lambda x: -x[1]["od_total"])
            all_covs_by_fare = {}
            for od, odata in sorted_ods:
                for f in odata["fares"]:
                    all_covs_by_fare.setdefault(f["fare"], []).append(f["cov"])

            medians_by_fare = {
                fare: sorted(vals)[len(vals) // 2]
                for fare, vals in all_covs_by_fare.items()
                if vals and all(v is not None for v in vals)
            }

            fare_cols = list(medians_by_fare.keys())
            # header: each fare shows supply/selection pair
            header_fares = "  ".join(f"{f[:6]:>13}" for f in fare_cols)
            print(f"\n    方向: {direction}  ({len(sorted_ods)} 条 OD)")
            print(f"    {'#':>3}  {'OD':<10}  {'Trace ID':>8}  {header_fares}")
            print(f"    {'':>3}  {'':10}  {'':>8}  " +
                  "  ".join(f"{'供→比价':>13}" for _ in fare_cols))
            print("    " + "-" * (26 + 15 * len(fare_cols)))

            for od, odata in sorted_ods:
                fare_map_cov = {f["fare"]: f["cov"]     for f in odata["fares"]}
                fare_map_sel = {f["fare"]: f["sel_cov"] for f in odata["fares"]}
                fare_map_drp = {f["fare"]: f["drop"]    for f in odata["fares"]}
                flags_here = []
                vals = []
                above_threshold = odata["od_total"] >= vol_threshold
                for fare, med in medians_by_fare.items():
                    v     = fare_map_cov.get(fare)
                    v_sel = fare_map_sel.get(fare)
                    drp   = fare_map_drp.get(fare)
                    flag = ""
                    is_zero = (v is not None and v == 0)
                    if v is not None and v < SUPPLY_COVERAGE_FLOOR * 100 and (above_threshold or is_zero):
                        flag = "▲"
                        flags_here.append(f"{fare}:{v:.0f}%[ABS]")
                    elif (v is not None and med is not None and
                          v < med - CONSISTENCY_DEVIATION * 100 and (above_threshold or is_zero)):
                        flag = "△"
                        flags_here.append(f"{fare}:{v:.0f}%[DEV]")
                    elif (drp is not None and drp > 5 and above_threshold and
                          v is not None and v >= SUPPLY_COVERAGE_FLOOR * 100):
                        flag = "◇"   # selection filter flag
                        flags_here.append(f"{fare}:↓{drp:.0f}pp[FILTER]")
                    # show as "supply→selection"
                    if v is not None and v_sel is not None:
                        cell = f"{v:.0f}%→{v_sel:.0f}%{flag}"
                    elif v is not None:
                        cell = f"{v:.0f}%{flag}"
                    else:
                        cell = "—"
                    vals.append(cell)

                vol_note = "" if above_threshold else " (低量)"
                flag_note = "  ← " + ", ".join(flags_here) if flags_here else ""
                print(f"    #{odata['od_rnk_in_cp']:>2}  {od:<10}  {odata['od_total']:>7,}{vol_note}  " +
                      "  ".join(f"{v:>13}" for v in vals) + flag_note)

                if flags_here:
                    dep, arr = od.split("-")
                    routes_to_scrape.append({"airline": airline, "dep": dep, "arr": arr})

    return cp_summary, routes_to_scrape


# ─── Routes CSV helpers ───────────────────────────────────────────────────────

def load_existing_routes(airline):
    existing = set()
    routes_csv = _routes_csv(airline)
    if not routes_csv.exists():
        return existing
    with open(routes_csv, newline="", encoding="utf-8") as f:
        for line in f:
            parts = [p.strip() for p in line.split(",")]
            if len(parts) >= 3 and parts[0].upper() == airline.upper():
                existing.add((parts[1].upper(), parts[2].upper()))
    return existing


def update_routes_csv(airline, new_routes):
    routes_csv = _routes_csv(airline)
    existing = load_existing_routes(airline)
    to_add = [(r["dep"], r["arr"]) for r in new_routes
              if (r["dep"], r["arr"]) not in existing]
    seen = set()
    to_add_dedup = []
    for pair in to_add:
        if pair not in seen:
            seen.add(pair)
            to_add_dedup.append(pair)
    if not to_add_dedup:
        print(f"\n  {routes_csv.name}: no new routes to add.")
        return
    need_header = not routes_csv.exists() or routes_csv.stat().st_size == 0
    with open(routes_csv, "a", encoding="utf-8") as f:
        if need_header:
            f.write("airline,departure,arrival\n")
        for dep, arr in to_add_dedup:
            f.write(f"{airline},{dep},{arr}\n")
    print(f"\n  {routes_csv.relative_to(AUDIT_DIR)}: added {len(to_add_dedup)} new route(s).")
    for dep, arr in to_add_dedup:
        print(f"    {airline},{dep},{arr}")


# ─── BQ raw snapshot ──────────────────────────────────────────────────────────

def save_bq_snapshot(airline, rows):
    """
    Persist raw BQ rows for this airline to audit/{AIRLINE}/bq_snapshot_YYYYMMDD.csv.
    Each row contains all coverage metrics so future analysis doesn't need to
    re-query BQ for historical data.
    """
    if not rows:
        return
    snap = _snapshot_csv(airline)
    snap.parent.mkdir(parents=True, exist_ok=True)
    import csv as _csv_mod
    fieldnames = list(rows[0].keys())
    with open(snap, "w", newline="", encoding="utf-8") as f:
        w = _csv_mod.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print(f"\n  BQ snapshot saved: {snap.relative_to(AUDIT_DIR)} ({len(rows)} rows)")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("airline", help="IATA airline code, e.g. TK")
    parser.add_argument("--update-routes", action="store_true",
                        help="Write flagged ODs to routes.csv")
    parser.add_argument("--force-refresh", action="store_true",
                        help="Force table recreate even if fresh")
    parser.add_argument("--no-snapshot", action="store_true",
                        help="Skip saving raw BQ snapshot CSV (default: always save)")
    args = parser.parse_args()
    airline = args.airline.upper()

    check_and_refresh_table(force=args.force_refresh)

    # Save raw BQ snapshot before analysis (unless opted out)
    if not args.no_snapshot:
        snapshot_query = f"""
SELECT
  vc, haultype, country_pair, airport_pair, brand_name,
  SUM(total_cnt)            AS total_cnt,
  SUM(has_brand_cnt)        AS has_brand_cnt,
  SUM(output_total_cnt)     AS output_total_cnt,
  SUM(output_has_brand_cnt) AS output_has_brand_cnt,
  ROUND(SAFE_DIVIDE(SUM(has_brand_cnt), SUM(total_cnt)) * 100, 2)               AS supply_pct,
  ROUND(SAFE_DIVIDE(SUM(output_has_brand_cnt), SUM(output_total_cnt)) * 100, 2) AS selection_pct,
  ROUND((SAFE_DIVIDE(SUM(has_brand_cnt), SUM(total_cnt)) -
         SAFE_DIVIDE(SUM(output_has_brand_cnt), SUM(output_total_cnt))) * 100, 2) AS filter_drop_pp
FROM `{BQ_TABLE}`
WHERE vc = '{airline}'
  AND haultype != ''
GROUP BY vc, haultype, country_pair, airport_pair, brand_name
ORDER BY country_pair, airport_pair, brand_name
"""
        raw_rows = run_bq(snapshot_query)
        save_bq_snapshot(airline, raw_rows)

    dom_flagged, dom_routes   = analyze_domestic(airline)
    int_summary, int_routes   = analyze_international(airline)

    all_routes = dom_routes + int_routes

    if args.update_routes:
        update_routes_csv(airline, all_routes)

    # Machine-readable output for skill integration
    print("\n__ANALYSIS_JSON__")
    print(json.dumps({
        "airline": airline,
        "domestic": {
            "flagged_count": len(dom_flagged),
            "flagged_ods": [
                {"od": d["od"], "volume": d["volume"],
                 "flags": [f"{f['fare']}:{f['cov']:.0f}%[{f['flag']}]"
                           for f in d["fares"] if f["flag"]]}
                for d in dom_flagged
            ],
        },
        "international": {
            "country_pairs_analyzed": len(int_summary),
            "flagged_country_pairs": sum(1 for c in int_summary if c["cp_flagged"]),
        },
        "routes_to_scrape": [
            {"airline": r["airline"], "dep": r["dep"], "arr": r["arr"]}
            for r in all_routes
        ],
    }, indent=2))


if __name__ == "__main__":
    main()
