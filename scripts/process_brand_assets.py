"""
Processes the official brand assets (logo + hero banner) into optimized,
web-ready files: a transparent logo (full lockup + icon-only mark) in
multiple sizes, a favicon set, an Open Graph preview image, and a
responsive srcset for the homepage hero banner.

Source files (originals only, never linked from HTML directly):
    assets/images/source/logo-original.jpeg      - portrait lockup on solid black
    assets/images/source/hero-banner-original.png - wide banner, no transparency needed

Run from the project root:
    python scripts/process_brand_assets.py
"""

from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = ROOT / "assets" / "images" / "source"
SRC_LOGO = SOURCE_DIR / "logo-original.jpeg"
SRC_HERO = SOURCE_DIR / "hero-banner-original.png"

BRAND_DIR = ROOT / "assets" / "images" / "brand"
HERO_DIR = ROOT / "assets" / "images" / "hero"
OG_DIR = ROOT / "assets" / "images" / "og"

BRAND_GREEN = (11, 61, 46)  # matches --color-primary


def key_out_black(img: Image.Image, low=10, high=45) -> Image.Image:
    """Convert solid-black background to alpha transparency with a soft
    edge ramp (avoids a hard jagged cutout on JPEG-compressed edges)."""
    arr = np.array(img.convert("RGB")).astype(np.float32)
    brightness = arr.max(axis=2)
    alpha = np.clip((brightness - low) / (high - low) * 255, 0, 255).astype(np.uint8)
    rgba = np.dstack([arr.astype(np.uint8), alpha])
    return Image.fromarray(rgba, mode="RGBA")


def tight_crop(img: Image.Image) -> Image.Image:
    bbox = img.getbbox()
    return img.crop(bbox) if bbox else img


def split_mark_from_wordmark(img: Image.Image) -> tuple[Image.Image, Image.Image]:
    """The source lockup is [circular mark] over [wordmark + tagline],
    separated by a transparent gap. Find that gap by locating the row
    with the fewest opaque pixels in the middle band of the image."""
    alpha = np.array(img)[:, :, 3]
    h = alpha.shape[0]
    band_start, band_end = int(h * 0.35), int(h * 0.75)
    row_opacity = (alpha > 20).sum(axis=1)
    split_row = band_start + int(np.argmin(row_opacity[band_start:band_end]))

    mark = tight_crop(img.crop((0, 0, img.width, split_row)))
    wordmark = tight_crop(img.crop((0, split_row, img.width, h)))
    return mark, wordmark


def pad_to_square(img: Image.Image, padding_ratio=0.12) -> Image.Image:
    size = int(max(img.width, img.height) * (1 + padding_ratio))
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    canvas.paste(img, ((size - img.width) // 2, (size - img.height) // 2), img)
    return canvas


def save_sizes(img: Image.Image, out_dir: Path, base_name: str, widths: list[int]):
    out_dir.mkdir(parents=True, exist_ok=True)
    aspect = img.height / img.width
    for w in widths:
        h = round(w * aspect)
        resized = img.resize((w, h), Image.LANCZOS)
        resized.save(out_dir / f"{base_name}-{w}.png", optimize=True)
        resized.save(out_dir / f"{base_name}-{w}.webp", quality=90, method=6)


def main():
    # ---- Logo ----
    keyed = key_out_black(Image.open(SRC_LOGO))
    full_lockup = tight_crop(keyed)
    mark, wordmark = split_mark_from_wordmark(full_lockup)
    mark_square = pad_to_square(mark)

    save_sizes(full_lockup, BRAND_DIR, "logo-full", [240, 480])
    save_sizes(mark_square, BRAND_DIR, "logo-mark", [64, 128, 256])

    # Favicon set (opaque apple-touch-icon per iOS guidance; transparent elsewhere)
    mark_square.resize((32, 32), Image.LANCZOS).save(BRAND_DIR / "favicon-32.png", optimize=True)
    mark_square.resize((180, 180), Image.LANCZOS).save(BRAND_DIR / "favicon-180.png", optimize=True)

    apple_bg = Image.new("RGBA", mark_square.size, (*BRAND_GREEN, 255))
    apple_bg.paste(mark_square, (0, 0), mark_square)
    apple_bg.convert("RGB").resize((180, 180), Image.LANCZOS).save(
        BRAND_DIR / "apple-touch-icon.png", optimize=True
    )

    # ---- Hero banner ----
    hero = Image.open(SRC_HERO).convert("RGB")
    save_sizes(hero, HERO_DIR, "hero-banner", [640, 960, 1280])
    for f in HERO_DIR.glob("hero-banner-*.png"):
        f.unlink()  # hero has no transparency; keep jpg+webp only, drop the png pass

    aspect = hero.height / hero.width
    for w in (640, 960, 1280):
        h = round(w * aspect)
        hero.resize((w, h), Image.LANCZOS).save(HERO_DIR / f"hero-banner-{w}.jpg", quality=82, optimize=True)
        hero.resize((w, h), Image.LANCZOS).save(HERO_DIR / f"hero-banner-{w}.webp", quality=82, method=6)

    # ---- Open Graph image (1200 wide; source aspect ~2.4:1, not the
    # "ideal" 1.91:1, but platforms auto-crop previews reasonably well) ----
    OG_DIR.mkdir(parents=True, exist_ok=True)
    og_w = 1200
    og_h = round(og_w * aspect)
    hero.resize((og_w, og_h), Image.LANCZOS).save(OG_DIR / "og-image.jpg", quality=85, optimize=True)

    print("Logo full lockup:", full_lockup.size)
    print("Logo mark (pre-pad):", mark.size, "-> square:", mark_square.size)
    print("Wordmark crop (unused, saved for reference):", wordmark.size)
    print("Done.")


if __name__ == "__main__":
    main()
