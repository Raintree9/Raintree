"""
Converts the raw country/visa CSV export into a clean, structured JSON file
consumed by the frontend.

The source CSV (data/raw/country-visa-data.csv) contains two different
sections stacked in one sheet:
  1. A visa summary table (20 rows, one per country).
  2. A series of per-country "Required Documents" checklists, each headed
     by a repeated country label and a run of "✅ ..." lines.

This script merges both sections into one record per country, matched by
the country's flag emoji (the only identifier common to both sections).

Run from the project root:
    python scripts/convert_data.py
"""

import json
import re
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_CSV = PROJECT_ROOT / "data" / "raw" / "country-visa-data.csv"
OUTPUT_JSON = PROJECT_ROOT / "src" / "data" / "countries.json"

FLAG_PATTERN = re.compile(r"^[\U0001F1E6-\U0001F1FF]{2}")

# The source data has no region column, but the Countries page design
# requires region filters. Assumption — confirm/adjust before launch.
REGION_BY_FLAG = {
    "🇪🇺": "Europe",
    "🇬🇧": "Europe",
    "🇷🇺": "Europe",
    "🇯🇵": "Asia",
    "🇰🇷": "Asia",
    "🇹🇼": "Asia",
    "🇸🇬": "Asia",
    "🇰🇭": "Asia",
    "🇨🇳": "Asia",
    "🇮🇩": "Asia",
    "🇲🇻": "Asia",
    "🇹🇭": "Asia",
    "🇲🇾": "Asia",
    "🇱🇰": "Asia",
    "🇻🇳": "Asia",
    "🇭🇰": "Asia",
    "🇦🇺": "Oceania",
    "🇳🇿": "Oceania",
    "🇨🇦": "North America",
    "🇦🇪": "Middle East",
}

# Curated homepage/footer "Popular Destinations" — a product/editorial
# choice, not visa data, so it lives here rather than being hardcoded in
# page markup. Order matches the approved Home mockup.
FEATURED_IDS = ["canada", "australia", "united-kingdom", "schengen", "japan"]


def extract_flag(text):
    if not isinstance(text, str):
        return None
    match = FLAG_PATTERN.match(text.strip())
    return match.group(0) if match else None


def slugify(name):
    slug = name.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug).strip("-")
    return slug


def parse_summary_rows(rows):
    """Rows stay part of the summary table as long as 'Visa Type' is populated."""
    countries = []
    flag_index = {}
    index = 0

    while index < len(rows) and isinstance(rows[index].get("Visa Type"), str):
        row = rows[index]
        raw_country = row["Country"].strip()
        flag = extract_flag(raw_country)
        name = raw_country[len(flag):].strip() if flag else raw_country
        purposes = [p.strip() for p in str(row["Purpose"]).split(",") if p.strip()]

        record = {
            "id": slugify(name),
            "flag": flag,
            "country": name,
            "region": REGION_BY_FLAG.get(flag, "Other"),
            "visaType": row["Visa Type"].strip(),
            "lengthOfStay": row["Length of Stay"].strip(),
            "visaValidity": row["Visa Validity"].strip(),
            "entryType": row["Entry Type"].strip(),
            "method": row["Method"].strip(),
            "purpose": purposes,
            "processingTime": row["Processing Time"].strip(),
            "documents": [],
            "featured": False,
            "featuredOrder": None,
        }
        countries.append(record)
        if flag:
            flag_index[flag] = record
        index += 1

    return countries, flag_index, index


def parse_document_blocks(rows, start_index, flag_index):
    """Everything after the summary table: per-country document checklists."""
    current_record = None
    unmatched_headers = []

    for row in rows[start_index:]:
        cell = row.get("Country")
        if not isinstance(cell, str) or not cell.strip():
            continue

        text = cell.strip()

        if text == "Required Documents":
            continue

        if text.startswith("✅"):
            if current_record is not None:
                current_record["documents"].append(text.lstrip("✅").strip())
            continue

        # Anything else is a new country header for a document block.
        flag = extract_flag(text)
        current_record = flag_index.get(flag) if flag else None
        if current_record is None:
            unmatched_headers.append(text)

    return unmatched_headers


def main():
    df = pd.read_csv(RAW_CSV)
    rows = df.to_dict(orient="records")

    countries, flag_index, summary_end = parse_summary_rows(rows)
    unmatched = parse_document_blocks(rows, summary_end, flag_index)

    by_id = {c["id"]: c for c in countries}
    missing_featured = []
    for order, country_id in enumerate(FEATURED_IDS):
        record = by_id.get(country_id)
        if record is None:
            missing_featured.append(country_id)
            continue
        record["featured"] = True
        record["featuredOrder"] = order

    empty_docs = [c["country"] for c in countries if not c["documents"]]

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(countries, f, ensure_ascii=False, indent=2)

    print(f"Wrote {len(countries)} countries to {OUTPUT_JSON.relative_to(PROJECT_ROOT)}")
    if unmatched:
        print(f"WARNING: {len(unmatched)} document block(s) could not be matched to a country: {unmatched}")
    if empty_docs:
        print(f"WARNING: {len(empty_docs)} countries have no documents: {empty_docs}")
    if missing_featured:
        print(f"WARNING: featured id(s) not found in data: {missing_featured}")


if __name__ == "__main__":
    main()
