"""
Regenerates the Meta Pixel / Meta domain-verification / Google Tag Manager
<head> and <body> blocks in every page from a single source of truth:
config/tracking.json.

This project has no templating layer (each HTML file is a standalone static
page, same as the rest of the site), so the blocks are still physically
duplicated across pages after this runs — but there's exactly one place to
change an ID. Edit config/tracking.json, then run:

    python scripts/build_tracking.py

Each block below is regenerated between its own start/end marker comments,
so re-running this script is idempotent — it never duplicates a block, it
only replaces what's between the markers.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = json.loads((ROOT / "config" / "tracking.json").read_text(encoding="utf-8"))

PAGES = [
    "index.html",
    "about.html",
    "services.html",
    "countries.html",
    "country-detail.html",
    "contact.html",
    "privacy-policy.html",
    "terms-and-conditions.html",
    "thank-you.html",
    "lp/canada-visitor-visa/index.html",
    "lp/uk-visitor-visa/index.html",
    "lp/schengen-visa/index.html",
    "lp/australia-visitor-visa/index.html",
]


def gtm_head_block():
    # No leading indent on the first line: the regex match starts exactly at
    # "<!--", so whatever indentation already precedes it in the file is left
    # untouched — adding our own here would double it up.
    gtm_id = CONFIG["gtmId"]
    return f"""<!-- Google Tag Manager -->
  <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
  new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
  j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
  'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
  }})(window,document,'script','dataLayer','{gtm_id}');</script>
  <!-- End Google Tag Manager -->"""


def gtm_noscript_block():
    gtm_id = CONFIG["gtmId"]
    return f"""<!-- Google Tag Manager (noscript) -->
  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id={gtm_id}"
  height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
  <!-- End Google Tag Manager (noscript) -->"""


def meta_pixel_block():
    pixel_id = CONFIG["metaPixelId"]
    verification = CONFIG.get("metaDomainVerification", "").strip()
    verification_tag = (
        f'\n  <meta name="facebook-domain-verification" content="{verification}" />'
        if verification
        else ""
    )
    return f"""<!-- Meta Pixel Code -->
  <script>
  !function(f,b,e,v,n,t,s)
  {{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
  n.callMethod.apply(n,arguments):n.queue.push(arguments)}};
  if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
  n.queue=[];t=b.createElement(e);t.async=!0;
  t.src=v;s=b.getElementsByTagName(e)[0];
  s.parentNode.insertBefore(t,s)}}(window, document,'script',
  'https://connect.facebook.net/en_US/fbevents.js');
  fbq('init', '{pixel_id}');
  fbq('track', 'PageView');
  </script>
  <noscript><img height="1" width="1" style="display:none"
  src="https://www.facebook.com/tr?id={pixel_id}&ev=PageView&noscript=1"
  /></noscript>
  <!-- End Meta Pixel Code -->{verification_tag}"""


BLOCKS = [
    ("<!-- Google Tag Manager -->", "<!-- End Google Tag Manager -->", gtm_head_block),
    ("<!-- Google Tag Manager \\(noscript\\) -->", "<!-- End Google Tag Manager \\(noscript\\) -->", gtm_noscript_block),
    ("<!-- Meta Pixel Code -->", "<!-- End Meta Pixel Code -->", meta_pixel_block),
]


def replace_block(content, start_marker, end_marker, new_block):
    pattern = re.compile(
        re.escape(start_marker) + r".*?" + re.escape(end_marker)
        if "\\(" not in start_marker
        else start_marker + r".*?" + end_marker,
        re.DOTALL,
    )
    if not pattern.search(content):
        return content, False
    return pattern.sub(lambda _: new_block, content, count=1), True


def main():
    updated = []
    for page in PAGES:
        path = ROOT / page
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8")
        original = content
        for start_marker, end_marker, block_fn in BLOCKS:
            content, _ = replace_block(content, start_marker, end_marker, block_fn())
        if content != original:
            path.write_text(content, encoding="utf-8")
            updated.append(page)

    print(f"Pixel ID: {CONFIG['metaPixelId']}")
    print(f"GTM ID:   {CONFIG['gtmId']}")
    print(f"Domain verification: {CONFIG.get('metaDomainVerification') or '(not set)'}")
    print(f"Updated {len(updated)} page(s): {', '.join(updated) if updated else '(none — nothing to regenerate yet)'}")


if __name__ == "__main__":
    main()
