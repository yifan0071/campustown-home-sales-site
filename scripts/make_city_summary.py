"""Build the summary files the site reads.

Reads data/college_town_home_sales.csv (read-only) and writes:
  data/city_summary.json      one entry per city, plus totals
  data/distance_summary.json  sales grouped by distance to campus

Run from the repository root:
  python3 scripts/make_city_summary.py

Uses only the Python standard library. Every number is computed here from the CSV.

Rules (see README "Data notes"):
  - A sale is counted in price statistics only if 10,000 <= sale_price <= 5,000,000.
  - Price per square foot also needs living_area_sqft > 0.
  - Days on market = contract_date - list_date, only when both dates are present
    and the result is not negative.
  - All headline figures are medians. Each city also reports its sample size.
  - zipcode, county_fips and parcel_number are read as text (the script does not use them).
"""

import csv
import json
import statistics
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "college_town_home_sales.csv"
CITY_OUT = ROOT / "data" / "city_summary.json"
DISTANCE_OUT = ROOT / "data" / "distance_summary.json"

PRICE_MIN = 10_000
PRICE_MAX = 5_000_000

# Distance bands in miles to campus. The last band is open-ended.
DISTANCE_BANDS = [(0, 1), (1, 2), (2, 3), (3, 5), (5, 10), (10, None)]


def parse_date(text):
    if not text:
        return None
    return date.fromisoformat(text)


def parse_number(text):
    if text is None or text.strip() == "":
        return None
    return float(text)


def round_or_none(value, digits=0):
    if value is None:
        return None
    return round(value, digits)


def band_label(low, high):
    if high is None:
        return f"{low:g}+ mi"
    return f"{low:g}–{high:g} mi"


def band_index(miles):
    for i, (low, high) in enumerate(DISTANCE_BANDS):
        if miles >= low and (high is None or miles < high):
            return i
    return None


def main():
    with SOURCE.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    total_rows = len(rows)
    sale_dates = [parse_date(r["sale_date"]) for r in rows if r["sale_date"]]

    # Rows whose price passes the rule
    priced = []
    excluded_price = 0
    for r in rows:
        price = parse_number(r["sale_price"])
        if price is None or not (PRICE_MIN <= price <= PRICE_MAX):
            excluded_price += 1
            continue
        priced.append(r)

    negative_dom = 0

    def days_on_market(r):
        nonlocal negative_dom
        listed = parse_date(r["list_date"])
        contracted = parse_date(r["contract_date"])
        if listed is None or contracted is None:
            return None
        days = (contracted - listed).days
        if days < 0:
            negative_dom += 1
            return None
        return days

    # ---- City summary ----
    by_city = {}
    for r in priced:
        by_city.setdefault((r["city"], r["state"]), []).append(r)

    cities = []
    for (city, state), group in by_city.items():
        prices = [parse_number(r["sale_price"]) for r in group]

        psf = []
        for r in group:
            area = parse_number(r["living_area_sqft"])
            if area is not None and area > 0:
                psf.append(parse_number(r["sale_price"]) / area)

        dom = [d for d in (days_on_market(r) for r in group) if d is not None]
        no_list = sum(1 for r in group if not r["list_date"])

        cities.append({
            "city": city,
            "state": state,
            "university": group[0]["university"],
            "sales": len(group),
            "median_price": round_or_none(statistics.median(prices)),
            "median_price_per_sqft": round_or_none(statistics.median(psf)) if psf else None,
            "sales_with_price_per_sqft": len(psf),
            "median_days_on_market": round_or_none(statistics.median(dom)) if dom else None,
            "sales_with_days_on_market": len(dom),
            "share_without_list_date_pct": round_or_none(100 * no_list / len(group), 1),
        })

    cities.sort(key=lambda c: c["sales"], reverse=True)

    all_prices = [parse_number(r["sale_price"]) for r in priced]
    city_output = {
        "source": "data/college_town_home_sales.csv",
        "sale_date_range": [min(sale_dates).isoformat(), max(sale_dates).isoformat()],
        "rules": {
            "price_min": PRICE_MIN,
            "price_max": PRICE_MAX,
            "price_per_sqft_needs_area_above": 0,
            "days_on_market": "contract_date minus list_date, both present, not negative",
        },
        "totals": {
            "rows_in_source": total_rows,
            "rows_excluded_by_price": excluded_price,
            "rows_used": len(priced),
            "median_price": round_or_none(statistics.median(all_prices)),
            "rows_with_negative_days_on_market_excluded": negative_dom,
        },
        "cities": cities,
    }

    # ---- Distance summary ----
    band_groups = [[] for _ in DISTANCE_BANDS]
    for r in priced:
        miles = parse_number(r["miles_to_campus"])
        if miles is None:
            continue
        idx = band_index(miles)
        if idx is not None:
            band_groups[idx].append(parse_number(r["sale_price"]))

    bands = []
    for (low, high), prices in zip(DISTANCE_BANDS, band_groups):
        bands.append({
            "label": band_label(low, high),
            "sales": len(prices),
            "median_price": round_or_none(statistics.median(prices)) if prices else None,
        })

    distance_output = {
        "source": "data/college_town_home_sales.csv",
        "rules": city_output["rules"],
        "bands": bands,
    }

    CITY_OUT.write_text(json.dumps(city_output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    DISTANCE_OUT.write_text(json.dumps(distance_output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"rows in source: {total_rows}")
    print(f"excluded by price rule: {excluded_price}")
    print(f"rows used: {len(priced)}")
    print(f"days-on-market negative (excluded): {negative_dom}")
    print(f"wrote {CITY_OUT.relative_to(ROOT)} and {DISTANCE_OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
