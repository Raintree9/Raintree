"""
Processes client-supplied content photography (service photos, destination
photos, the About team photo) from the staging folder into optimized,
responsive production assets.

Source folder (read-only input, never linked from HTML):
    assets/images/Place holders/

All source photos arrived portrait-oriented. Destinations, the team photo,
and testimonials crop to landscape/square boxes that suit their content
fine. The two service photos (visitor-visa, work-permit) are different:
they're portrait/square-native subjects (a traveler looking up at a plane
overhead; a person holding a passport), and forcing them into a landscape
box cropped the actual subject out. Those two crop to 4:5 portrait instead
— see cards.css / layout.css for the container layouts built around that.

Every crop below has a hand-picked vertical crop bias (0.0 = crop window
starts at the very top of the source, 1.0 = crop window ends at the very
bottom, 0.5 = centered) chosen by looking at where the subject actually
sits in that specific photo.

Run from the project root:
    python scripts/process_content_images.py
"""

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = ROOT / "assets" / "images" / "Place holders"
DEST_DESTINATIONS = ROOT / "assets" / "images" / "destinations"
DEST_SERVICES = ROOT / "assets" / "images" / "services"
DEST_TEAM = ROOT / "assets" / "images" / "team"
DEST_TESTIMONIALS = ROOT / "assets" / "images" / "testimonials"
HERO_SOURCE_DIR = ROOT / "assets" / "images" / "hero animation"
DEST_HERO = ROOT / "assets" / "images" / "hero"

JPEG_QUALITY = 82
WEBP_QUALITY = 82

# country-id -> vertical crop bias (0=top, 1=bottom, 0.5=center) for a 4:3 crop
DESTINATIONS = {
    "australia": 0.25,      # Opera House + harbour bridge, keep sunset sky
    "canada": 0.08,         # CN Tower is very tall, crop near the top
    "cambodia": 0.50,       # Angkor Wat centered, huge empty sky above
    "japan": 0.30,          # Mt Fuji + pagoda roofs, avoid bottom shrubs
    "new-zealand": 0.80,    # crop below the "NEW ZEALAND" text overlay
    "russia": 0.33,         # St Basil's + crowd, avoid bottom watermark
    "schengen": 0.25,       # Eiffel Tower (Paris stand-in per image guide)
    "singapore": 0.31,      # Marina Bay Sands + reflection, avoid bottom text
    "south-korea": 0.50,    # Gyeongbokgung gate, well-balanced already
    "taiwan": 0.63,         # crop below the "TAIPEI" text overlay
    "united-kingdom": 0.17, # Big Ben is very tall, crop near the top
    "china": 0.68,          # Great Wall watchtower + flags, lots of sky/clouds above
    "hong-kong": 0.60,      # skyline + harbour, avoid top sky and bottom treeline
    "indonesia": 0.66,      # Tanah Lot temple + dancers, keep both in frame
    "malaysia": 0.20,       # Petronas Towers are very tall, crop near the top
    "maldives": 0.63,       # overwater bungalows, avoid top mountain/sky
    "sri-lanka": 0.50,      # Sigiriya rock centered, already well-balanced
    "thailand": 0.04,       # golden Buddha statue's head must stay in frame
    "united-arab-emirates": 0.21,  # Burj Khalifa's tapering silhouette is the recognizable part, not just the tip
    "vietnam": 0.59,        # Hoi An lantern canal, avoid mountains/sky above
    "dubai": 0.30,          # Burj Khalifa + "DUBAI" text label, avoid the fountain plaza at the very bottom
    "slovakia": 0.05,       # "SLOVAKIA" text + castle towers near the top, avoid the river/bridge below
}

# service name -> vertical crop bias for a 4:5 portrait crop. Both service
# photos are portrait/square-native; a landscape crop (the old 16:10/4:3
# treatment) left visitor-visa showing almost nothing but the underside of
# a plane, cropping the traveler out entirely. 4:5 keeps enough vertical
# room for the actual subject to read clearly. One crop now serves both
# the service-card and detail-row placements (see cards.css / layout.css).
SERVICES = {
    "visitor-visa": 0.0,   # top-aligned: keeps the full plane AND the traveler's head/shoulders
    "work-permit": 0.5,    # centered: face + both hands + documents already well-balanced
}

# testimonial author -> vertical crop bias for a 1:1 headshot crop
TESTIMONIALS = {
    "rohit-sharma": 0.30,
    "priya-nair": 0.22,
    "vikram-raj": 0.12,  # face sits lower in a much taller portrait
}

TEAM_BIAS = 0.35  # About page team photo, favor faces over table

# Home hero slideshow. These sources are mostly square/portrait (an
# illustration, a studio photo, a travel collage, an office photo) going
# into a slide panel that's roughly 4:5 (see .hero-slideshow__photo), so a
# gentle 4:5 crop keeps each composition intact instead of the 2:1 full-
# banner crop this file uses elsewhere, which would slice most of these
# apart. Format: slide id -> (source stem, crop bias, optional pre-crop
# box in source pixels applied before the ratio crop).
HERO_SLIDES = {
    # two travelers illustration — already near-square, centered crop
    "slide-visa-experts": ("2df396f8c0e461402dc1e4644407203e", 0.5, None),
    # travel-landmarks collage — centered crop keeps the main globe/figure;
    # only trims the decorative signpost/food icons at the edges
    "slide-destinations": ("9d943e19954282657dd175a80cb49f6f", 0.5, None),
    # woman with suitcase + passport — top-weighted to keep her face and
    # the passport in frame, crop the legs/suitcase at the bottom
    "slide-process": ("5de439359b0833f83f2a20d6959407d1", 0.15, None),
    # support agent — pre-crop excludes a third-party branded mug in the
    # foreground (x:0-480 of the original), then top-weighted for her face
    "slide-support": ("8f957f14100910bdfa276291f9f6b567", 0.25, (480, 0, 1024, 1024)),
}

DESTINATION_WIDTHS = [480, 800, 1200]
SERVICE_WIDTHS = [640, 960, 1280]
TEAM_WIDTHS = [640, 960, 1280]
TESTIMONIAL_WIDTHS = [128, 256]
HERO_WIDTHS = [640, 960, 1280]


def find_source(stem):
    for ext in (".jpg", ".jpeg", ".png"):
        candidate = SOURCE_DIR / f"{stem}{ext}"
        if candidate.exists():
            return candidate
    raise FileNotFoundError(f"No source file found for '{stem}' in {SOURCE_DIR}")


def crop_to_ratio(img, target_ratio, vertical_bias=0.5):
    w, h = img.size
    current_ratio = w / h
    if current_ratio > target_ratio:
        new_w = round(h * target_ratio)
        x0 = round((w - new_w) * vertical_bias)
        return img.crop((x0, 0, x0 + new_w, h))
    new_h = round(w / target_ratio)
    max_y0 = h - new_h
    y0 = round(max_y0 * vertical_bias)
    return img.crop((0, y0, w, y0 + new_h))


def export_sizes(img, out_dir, base_name, widths):
    out_dir.mkdir(parents=True, exist_ok=True)
    rgb = img.convert("RGB")
    aspect = rgb.height / rgb.width
    for w in widths:
        h = round(w * aspect)
        resized = rgb.resize((w, h), Image.LANCZOS)
        resized.save(out_dir / f"{base_name}-{w}.jpg", quality=JPEG_QUALITY, optimize=True)
        resized.save(out_dir / f"{base_name}-{w}.webp", quality=WEBP_QUALITY, method=6)


def process_destinations():
    for country_id, bias in DESTINATIONS.items():
        src = find_source(country_id)
        img = Image.open(src)
        cropped = crop_to_ratio(img, 4 / 3, bias)
        export_sizes(cropped, DEST_DESTINATIONS, country_id, DESTINATION_WIDTHS)
        print(f"  destinations/{country_id}: {cropped.size} -> {DESTINATION_WIDTHS}")


def process_services():
    for name, bias in SERVICES.items():
        src = find_source(name)
        img = Image.open(src)
        cropped = crop_to_ratio(img, 4 / 5, bias)
        export_sizes(cropped, DEST_SERVICES, name, SERVICE_WIDTHS)
        print(f"  services/{name}: {cropped.size} -> {SERVICE_WIDTHS}")


def process_team():
    src = find_source("about-team")
    img = Image.open(src)
    cropped = crop_to_ratio(img, 4 / 3, TEAM_BIAS)
    export_sizes(cropped, DEST_TEAM, "about-team", TEAM_WIDTHS)
    print(f"  team/about-team: {cropped.size} -> {TEAM_WIDTHS}")


def process_testimonials():
    for name, bias in TESTIMONIALS.items():
        src = find_source(name)
        img = Image.open(src)
        cropped = crop_to_ratio(img, 1 / 1, bias)
        export_sizes(cropped, DEST_TESTIMONIALS, name, TESTIMONIAL_WIDTHS)
        print(f"  testimonials/{name}: {cropped.size} -> {TESTIMONIAL_WIDTHS}")


def process_hero_slides():
    for name, (stem, bias, pre_crop) in HERO_SLIDES.items():
        src = HERO_SOURCE_DIR / f"{stem}.jpg"
        img = Image.open(src)
        if pre_crop:
            img = img.crop(pre_crop)
        cropped = crop_to_ratio(img, 4 / 5, bias)
        export_sizes(cropped, DEST_HERO, name, HERO_WIDTHS)
        print(f"  hero/{name}: {cropped.size} -> {HERO_WIDTHS}")


def main():
    print("Destinations:")
    process_destinations()
    print("Services:")
    process_services()
    print("Team:")
    process_team()
    print("Testimonials:")
    process_testimonials()
    print("Hero slideshow:")
    process_hero_slides()
    print("Done.")


if __name__ == "__main__":
    main()
