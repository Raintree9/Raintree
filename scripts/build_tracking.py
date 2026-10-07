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

SITE_URL = "https://raintreeimmigration.com"
OG_IMAGE = f"{SITE_URL}/assets/images/og/og-default.jpg"

# Open Graph / Twitter metadata for every hand-authored page. Landing pages
# (lp/*) generate their own block directly in scripts/build_landing_pages.py,
# since that script already has each page's title/description at generation
# time — no need to duplicate that config here.
#
# country-detail.html is dynamic: country-detail.js overwrites og:title,
# og:description, og:url (and the plain <title>/meta-description/canonical)
# per country via the element ids below, so this entry is only the
# pre-JS/crawler-fallback default.
PAGE_META = {
    "index.html": {
        "title": "RainTree Immigration | Visa & Immigration Documentation Experts in Coimbatore",
        "description": "Professional travel guidance for visitor visas and work permits with personalized support. Explore visa requirements for 20+ destinations.",
        "path": "/",
    },
    "about.html": {
        "title": "About Us | RainTree Immigration",
        "description": "RainTree Immigration is a trusted name in visa and immigration services, helping individuals, families, and businesses explore the world with ease.",
        "path": "/about.html",
    },
    "services.html": {
        "title": "Our Services | RainTree Immigration",
        "description": "Visitor visas and work permits — explore RainTree Immigration's visa services, requirements, and application support.",
        "path": "/services.html",
    },
    "countries.html": {
        "title": "Explore Destinations | RainTree Immigration",
        "description": "Browse visa requirements, processing times, and required documents for 20+ destinations worldwide with RainTree Immigration.",
        "path": "/countries.html",
    },
    "country-detail.html": {
        "title": "Visa Requirements | RainTree Immigration",
        "description": "Visa type, validity, entry conditions, processing time, and required documents — visa requirements from RainTree Immigration.",
        "path": "/country-detail.html",
        "dynamic": True,
    },
    "contact.html": {
        "title": "Contact Us | RainTree Immigration",
        "description": "Have questions about visas or travel? Contact RainTree Immigration for expert guidance — call, WhatsApp, email, or send us a message.",
        "path": "/contact.html",
    },
    "privacy-policy.html": {
        "title": "Privacy Policy | RainTree Immigration",
        "description": "How RainTree Immigration collects, uses, and protects your personal information.",
        "path": "/privacy-policy.html",
    },
    "terms-and-conditions.html": {
        "title": "Terms and Conditions | RainTree Immigration",
        "description": "Terms and conditions for using RainTree Immigration's website and visa consultancy services.",
        "path": "/terms-and-conditions.html",
    },
    "thank-you.html": {
        "title": "Thank You | RainTree Immigration",
        "description": "Thank you for contacting RainTree Immigration. Our team will reach out to you shortly.",
        "path": "/thank-you.html",
    },
}


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


def social_meta_block(meta):
    url = SITE_URL + meta["path"]
    title = meta["title"]
    description = meta["description"]
    dynamic = meta.get("dynamic", False)

    # Dynamic pages carry ids so country-detail.js can overwrite these three
    # per country; static pages don't need the ids at all.
    og_title_id = ' id="meta-og-title"' if dynamic else ""
    og_desc_id = ' id="meta-og-description"' if dynamic else ""
    og_url_id = ' id="meta-og-url"' if dynamic else ""
    tw_title_id = ' id="meta-twitter-title"' if dynamic else ""
    tw_desc_id = ' id="meta-twitter-description"' if dynamic else ""

    return f"""<!-- Social Meta -->
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="RainTree Immigration" />
  <meta{og_title_id} property="og:title" content="{title}" />
  <meta{og_desc_id} property="og:description" content="{description}" />
  <meta{og_url_id} property="og:url" content="{url}" />
  <meta property="og:image" content="{OG_IMAGE}" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:image:alt" content="RainTree Immigration logo" />
  <meta property="og:locale" content="en_IN" />

  <meta name="twitter:card" content="summary_large_image" />
  <meta{tw_title_id} name="twitter:title" content="{title}" />
  <meta{tw_desc_id} name="twitter:description" content="{description}" />
  <meta name="twitter:image" content="{OG_IMAGE}" />
  <!-- End Social Meta -->"""


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


UNMARKED_SOCIAL_PATTERN = re.compile(
    r'<meta[^>]*\bproperty="og:title".*?<meta[^>]*\bname="twitter:image"[^>]*/>', re.DOTALL
)
CANONICAL_LINK_PATTERN = re.compile(r'<link[^>]*rel="canonical"[^>]*/>')


def apply_social_meta(content, meta):
    new_block = social_meta_block(meta)

    # Already regenerated before — replace between the markers only.
    content, changed = replace_block(content, "<!-- Social Meta -->", "<!-- End Social Meta -->", new_block)
    if changed:
        return content, True

    # Old unmarked og:title..twitter:image block from before this script
    # existed — replace it wholesale and it'll carry markers from now on.
    if UNMARKED_SOCIAL_PATTERN.search(content):
        return UNMARKED_SOCIAL_PATTERN.sub(lambda _: new_block, content, count=1), True

    # No social tags at all yet (e.g. thank-you.html) — insert right after
    # the canonical link.
    match = CANONICAL_LINK_PATTERN.search(content)
    if match:
        insert_at = match.end()
        return content[:insert_at] + "\n\n  " + new_block + content[insert_at:], True

    return content, False


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
        if page in PAGE_META:
            content, _ = apply_social_meta(content, PAGE_META[page])
        if content != original:
            path.write_text(content, encoding="utf-8")
            updated.append(page)

    print(f"Pixel ID: {CONFIG['metaPixelId']}")
    print(f"GTM ID:   {CONFIG['gtmId']}")
    print(f"Domain verification: {CONFIG.get('metaDomainVerification') or '(not set)'}")
    print(f"Updated {len(updated)} page(s): {', '.join(updated) if updated else '(none — nothing to regenerate yet)'}")


if __name__ == "__main__":
    main()
