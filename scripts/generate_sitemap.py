"""
Generates sitemap.xml from the static page list plus every country in
src/data/countries.json (each is a distinct indexable URL via ?country=id).
Excludes privacy-policy.html and terms-and-conditions.html, which carry a
noindex meta tag and should not appear in the sitemap.

Run from the project root:
    python scripts/generate_sitemap.py
"""

import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COUNTRIES_JSON = ROOT / "src" / "data" / "countries.json"
OUTPUT = ROOT / "sitemap.xml"

SITE_URL = "https://www.raintreeimmigration.com"
TODAY = date.today().isoformat()

STATIC_PAGES = [
    ("/", "1.0", "weekly"),
    ("/services.html", "0.8", "monthly"),
    ("/countries.html", "0.9", "weekly"),
    ("/about.html", "0.6", "monthly"),
    ("/contact.html", "0.7", "monthly"),
]


def main():
    countries = json.loads(COUNTRIES_JSON.read_text(encoding="utf-8"))

    urls = [(f"{SITE_URL}{path}", TODAY, changefreq, priority) for path, priority, changefreq in STATIC_PAGES]
    for country in countries:
        urls.append(
            (f"{SITE_URL}/country-detail.html?country={country['id']}", TODAY, "monthly", "0.6")
        )

    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, lastmod, changefreq, priority in urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{loc}</loc>")
        lines.append(f"    <lastmod>{lastmod}</lastmod>")
        lines.append(f"    <changefreq>{changefreq}</changefreq>")
        lines.append(f"    <priority>{priority}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")

    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {len(urls)} URLs to {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
