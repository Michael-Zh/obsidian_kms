"""
Turkish Airlines Fare Parser & Coverage Calculator
====================================================
Reads the *_fares.csv files produced by fetch_fares_tk_playwright.py
(one per search) and outputs a coverage-rate analysis.

Usage:
  python parse_tk_html.py          # processes all TK/*_fares.csv files
  python parse_tk_html.py TK/TK_0919_1pax_ow_fra_ist_fares.csv  # one file

Output (printed + saved to TK/):
  TK_flights.csv   — all fare rows combined
  TK_coverage.csv  — coverage rate table
"""

import re
import sys
import pandas as pd
from pathlib import Path


# ─────────────────────────────────────────────────────────────────────────────
# Coverage calculation
# ─────────────────────────────────────────────────────────────────────────────

def get_fare_price_ranking(df):
    df2 = df.copy()
    df2["price_after_promo"] = pd.to_numeric(df2["price_after_promo"], errors="coerce")
    fare_avg = df2.groupby("fare_name")["price_after_promo"].mean()
    ranking  = {f: i for i, f in enumerate(fare_avg.sort_values().index)}
    return ranking, fare_avg.sort_values()


def calculate_coverage(df):
    fare_ranking, fare_avg = get_fare_price_ranking(df)
    fares_sorted = list(fare_avg.index)

    df = df.copy()
    df["route_pair"] = df.apply(
        lambda r: "-".join(sorted([r["departing_airport"], r["arriving_airport"]])),
        axis=1,
    )

    results = []

    def _add_rows(grp, route_pair, trip_type, direction, pax):
        grp = grp.copy()
        grp["fk"] = grp["departing_date"].astype(str) + "_" + grp["flight"]
        total = grp["fk"].nunique()
        for fare in fares_sorted:
            n = grp[grp["fare_name"] == fare]["fk"].nunique()
            results.append({
                "route_pair":        route_pair,
                "trip_type":         trip_type,
                "direction":         direction,
                "pax_count":         pax,
                "fare_name":         fare,
                "flights_with_fare": n,
                "total_flights":     total,
                "coverage_rate":     round(n / total * 100, 1) if total else 0,
                "fare_rank":         fare_ranking[fare],
            })

    for route_pair, rdf in df.groupby("route_pair"):
        for (pax, dep), grp in rdf[rdf["trip_type"] == "OW"].groupby(
                ["pax_count", "departing_airport"]):
            _add_rows(grp, route_pair, "OW", dep, pax)

        for (pax, dep), grp in rdf[rdf["trip_type"] == "RT"].groupby(
                ["pax_count", "departing_airport"]):
            arr = grp["arriving_airport"].iloc[0]
            _add_rows(grp, route_pair, "RT", f"{dep}->{arr}", pax)

    cdf = pd.DataFrame(results)
    if cdf.empty:
        return cdf, fares_sorted
    return cdf.sort_values(
        ["route_pair", "trip_type", "direction", "pax_count", "fare_rank"]
    ), fares_sorted


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main():
    tk_dir = Path.home() / "Documents" / "Audit" / "TK"
    if not tk_dir.exists():
        print(f"Error: {tk_dir} not found.")
        sys.exit(1)

    # Accept explicit file args or auto-discover *_fares.csv in TK/
    if len(sys.argv) > 1:
        files = [Path(f) for f in sys.argv[1:]]
    else:
        files = sorted(tk_dir.glob("*_fares.csv"))

    if not files:
        print("No *_fares.csv files found in TK/.")
        print("Run fetch_fares_tk_playwright.py first to generate them.")
        sys.exit(1)

    print(f"Processing {len(files)} file(s)...\n")

    all_dfs = []
    for f in files:
        try:
            df = pd.read_csv(f)
            print(f"  → {f.name}  ({len(df)} rows)")
            all_dfs.append(df)
        except Exception as e:
            print(f"  ⚠ Could not read {f.name}: {e}")

    if not all_dfs:
        print("No data loaded.")
        sys.exit(1)

    df = pd.concat(all_dfs, ignore_index=True)
    print(f"\nTotal rows: {len(df)}")

    # ── Save combined flights CSV ─────────────────────────────────────────
    flights_csv = tk_dir / "TK_flights.csv"
    df.to_csv(flights_csv, index=False)
    print(f"✓ Saved: {flights_csv}")

    # ── Coverage ──────────────────────────────────────────────────────────
    cdf, fares_sorted = calculate_coverage(df)
    if cdf.empty:
        print("⚠  Coverage calculation returned no results.")
        sys.exit(0)

    coverage_csv = tk_dir / "TK_coverage.csv"
    cdf.drop(columns=["fare_rank"]).to_csv(coverage_csv, index=False)
    print(f"✓ Saved: {coverage_csv}")

    # ── Markdown table ────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("Coverage Rate Analysis — Turkish Airlines (TK)")
    print("=" * 60)

    for route_pair, rdf in cdf.groupby("route_pair"):
        print(f"\n### Route: {route_pair}\n")
        pivot = rdf.pivot_table(
            values="coverage_rate",
            index="fare_name",
            columns=["trip_type", "direction", "pax_count"],
            aggfunc="first",
        )
        pivot.columns = [
            f"{'OW' if tt == 'OW' else 'RT'} {dir_} {p}pax"
            for tt, dir_, p in pivot.columns
        ]
        row_order = [f for f in fares_sorted if f in pivot.index]
        pivot = pivot.reindex(row_order)

        cols = pivot.columns.tolist()
        print("| Fare | " + " | ".join(cols) + " |")
        print("|------|" + "|".join(["------:" for _ in cols]) + "|")
        for fare in row_order:
            vals = [
                f"{pivot.loc[fare, c]:.1f}%" if pd.notna(pivot.loc[fare, c]) else "—"
                for c in cols
            ]
            print(f"| {fare} | " + " | ".join(vals) + " |")

    print(f"\nDone. {len(df)} fare rows from {len(files)} file(s).")


if __name__ == "__main__":
    main()
