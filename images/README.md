# images/ — production photo staging area

This folder is a drop zone for the production photos sourced using
[`docs/Production-Image-Guide.md`](../docs/Production-Image-Guide.md). It is
**not** where the site's live images live — the project's real, served
images are under `assets/images/`. Files placed here still need to be
processed (resized, converted to WebP, matched to a filename the HTML
expects) before they replace anything on the site.

Drop your downloaded originals into the matching subfolder below, named the
way each section describes, then move/process them into `assets/images/`
per the "Final destination" column.

## Folder structure

```
images/
├── services/
│   ├── visitor-visa.jpg
│   └── work-permit.jpg
├── team/
│   └── about-team.jpg
├── destinations/
│   ├── schengen.jpg
│   ├── united-kingdom.jpg
│   ├── japan.jpg
│   ├── south-korea.jpg
│   ├── australia.jpg
│   ├── new-zealand.jpg
│   ├── taiwan.jpg
│   ├── canada.jpg
│   ├── singapore.jpg
│   ├── cambodia.jpg
│   ├── russia.jpg
│   ├── china.jpg
│   ├── indonesia.jpg
│   ├── maldives.jpg
│   ├── united-arab-emirates.jpg
│   ├── thailand.jpg
│   ├── malaysia.jpg
│   ├── sri-lanka.jpg
│   ├── vietnam.jpg
│   └── hong-kong.jpg
└── testimonials/
    ├── rohit-sharma.jpg
    ├── priya-nair.jpg
    └── vikram-raj.jpg
```

The 20 filenames under `destinations/` match the `id` field for each
country in `src/data/countries.json` exactly — this isn't cosmetic, it's
what lets a future processing step (or a person doing it by hand) pair each
photo to the right country without guessing.

## Where each category ends up in the project

| Staged in `images/…` | Final destination | Used by |
|---|---|---|
| `services/visitor-visa.jpg` | `assets/images/services/visitor-visa-{640,960,1280}.{jpg,webp}` | `index.html`, `about.html`, `services.html` |
| `services/work-permit.jpg` | `assets/images/services/work-permit-{640,960,1280}.{jpg,webp}` | `index.html`, `about.html`, `services.html` |
| `team/about-team.jpg` | `assets/images/team/about-team-{640,960,1280}.{jpg,webp}` | `about.html` |
| `destinations/{country-id}.jpg` | `assets/images/destinations/{country-id}-{400,800}.{jpg,webp}` | `index.html`, `countries.html`, `country-detail.html` |
| `testimonials/{name}.jpg` | `assets/images/testimonials/{name}.{jpg,webp}` | `index.html` |

This mirrors the pattern already used for the logo and hero banner: a raw
original goes in first, a processing step produces multiple sized
JPEG + WebP pairs, and only the processed output is what the HTML actually
references. See `scripts/process_brand_assets.py` for the existing example
of that pattern — the same approach (resize to the widths a `srcset` needs,
export both formats) applies to every row above.

## Before you place a file here

Check `docs/Production-Image-Guide.md` for that image's required aspect
ratio and minimum resolution — downloading the wrong crop or too small a
source is easier to catch now than after it's wired into a page.

## Note on testimonials

`priya-nair.jpg`, `rohit-sharma.jpg`, and `vikram-raj.jpg` are attributed to
named, specific people on the site. Per the caution in the image guide,
these three should only be filled with real client photos (with
permission) — not stock images standing in for a real name. If you don't
have real photos yet, leave this subfolder empty rather than filling it
with stock.
