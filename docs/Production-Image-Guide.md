# Production Image Guide — RainTree Immigration

RainTree Immigration — Production Assets

Every placeholder currently on the site, in one reference. For each: what it needs to communicate, the ideal shot, search terms for Unsplash or Pexels, and the exact technical spec to match its slot in the layout.

## At a glance

Six image types, 25 files total (2 services × 2 crops, 1 team photo, 20 destination photos, 3 testimonial portraits).

| Image | Appears on | Aspect ratio | Min. resolution | Format | Count |
|---|---|---|---|---|---|
| Visitor Visa | Home, About (card) · Services (detail) | 16:10 + 4:3 | 1600×1000 / 1600×1200 | JPEG → WebP | 1 photo, 2 crops |
| Work Permit | Home, About (card) · Services (detail) | 16:10 + 4:3 | 1600×1000 / 1600×1200 | JPEG → WebP | 1 photo, 2 crops |
| Team / office | About page only | 4:3 | 1600×1200 | JPEG → WebP | 1 |
| Destination photos | Home (5), Countries (20), Country Detail (per country) | 4:3 | 1600×1200 | JPEG → WebP | 20 |
| Testimonial portraits | Home page only | 1:1 | 400×400 | JPEG → WebP | 3 |

---

## A. Visitor Visa photo

Currently a plane icon on a dark green gradient. Appears on the Home and About service cards, and again in the Visitor Visa detail section on the Services page.

**1 — What it should communicate**

Ease and confidence, not paperwork. This is the feeling of *getting there* — leisure and family travel, not a bureaucratic process. It should read as aspirational tourism, the emotional payoff of the visa rather than the visa itself.

**2 — Ideal composition**

A traveler in motion through an airport — walking the terminal with a rolling suitcase, or a close, warm-lit crop of hands holding a passport and boarding pass with a soft-focus departure board behind. Candid, natural light, real body language. Avoid stock clichés: no globes with pins, no oversized paper airplanes, no posed "thumbs up at the airport" shots.

**3 — Search keywords**

- `airport traveler suitcase`
- `passport boarding pass hand`
- `family travel airport`
- `tourist walking terminal`

**4 — Aspect ratio**

16:10 for the card thumbnail, 4:3 for the detail-page image. Pick one wide, loosely-composed photo and crop it both ways rather than sourcing two separate images — keep the subject centered enough to survive both crops.

**5 — Resolution**

```
1600×1000 min (card)
1600×1200 min (detail)
```

Download Unsplash "Large" or a Pexels original — both comfortably clear this on a retina display.

**6 — Format**

Source as JPEG — that's the native format both libraries serve. The project already has a conversion step that outputs paired WebP + JPEG files for production, so a high-res JPEG is the correct thing to download regardless of what ships.

---

## B. Work Permit photo

Currently a briefcase icon on a gold-tinted gradient. Same placement pattern as Visitor Visa: Home and About cards, plus the Work Permit detail section on Services.

**1 — What it should communicate**

Professional purpose — building a career abroad, not a stock-photo boardroom. It should feel more purposeful and forward-looking than the Visitor Visa image, while staying in the same candid, real-life register rather than tipping into generic corporate stock.

**2 — Ideal composition**

A professional in transit or arrival — laptop bag over the shoulder, walking a city street with a skyline behind, or reviewing documents at a desk with a window view of a foreign city. Avoid the handshake-across-a-desk cliché and avoid anyone facing directly into a laptop screen (too generic-office).

**3 — Search keywords**

- `professional city commute`
- `expat working abroad`
- `business traveler laptop bag`
- `young professional skyline`

**4 — Aspect ratio**

16:10 for the card, 4:3 for the detail section — same one-photo-two-crops approach as Visitor Visa.

**5 — Resolution**

```
1600×1000 min (card)
1600×1200 min (detail)
```

**6 — Format**

JPEG source, converted to WebP for production, same as above.

---

## C. About — "Who We Are" team photo

Currently a generic person icon on a dark green gradient. Appears once, on the About page, next to the "Trusted by Travelers, Driven by Excellence" copy.

**1 — What it should communicate**

Trust and warmth through specificity. This is the one image on the whole site whose entire job is "here is who you're actually working with" — it's the least interchangeable placeholder here.

**2 — Ideal composition**

Real colleagues at work in the actual office — a small group reviewing a case together at a table, natural light, genuine mid-conversation moment rather than a stiff lineup facing the camera. If a real office photo isn't available yet, use a placeholder that's obviously generic-professional (small diverse team, bright modern office, collaborative posture) rather than one that reads as a specific fake "team."

**3 — Search keywords**

- `diverse team meeting bright office`
- `consultants working together`
- `small business team collaboration`

**4 — Aspect ratio**

4:3

**5 — Resolution**

```
1600×1200 minimum
```

**6 — Format**

JPEG source, converted to WebP for production.

> **Recommendation:** prioritize a real photo of the RainTree team or office for this one over any stock substitute. Every other placeholder on this page is generic-by-design; this is the exception where authenticity is the actual point of the section.

---

## D. Destination photos

Currently a large flag emoji on a brand-green gradient. One photo per country, reused at two sizes: the small grid card (Home's 5 featured destinations, and all 20 on the Countries page) and the larger hero image on that country's own detail page.

**1 — What it should communicate**

Instant recognition. A user should be able to identify the country from the photo alone, before reading the label — this is a visual index, not scenery for its own sake.

**2 — Ideal composition**

One unmistakable landmark or vista per country, shot in good light (golden hour where possible). Keep people out of the frame, or minimal and small in scene — it keeps the image timeless and doesn't compete with the flag/name overlay. Avoid any photo with visible text, watermarks, or logos baked in.

**4 — Aspect ratio**

4:3 — the same crop serves both the grid card and the detail-page hero, so one photo per country covers both placements.

**5 — Resolution**

```
1600×1200 minimum
```

The detail-page hero is the largest placement (roughly half the page width) — size for that and the small grid thumbnails take care of themselves.

**6 — Format**

JPEG source, converted to WebP for production — same pipeline as every other image on this page.

### Search keywords, all 20 destinations

One recognizable landmark per country. Schengen is a special case — it's a visa zone, not a place — see note below.

| Country | Region | Search keywords |
|---|---|---|
| Schengen | Europe | Eiffel Tower Paris *or* generic "Europe travel skyline" — see note |
| United Kingdom | Europe | Big Ben London, London skyline |
| Japan | Asia | Mount Fuji, Kyoto temple, Tokyo Shibuya crossing |
| South Korea | Asia | Seoul skyline, Gyeongbokgung Palace |
| Australia | Oceania | Sydney Opera House, Sydney Harbour Bridge |
| New Zealand | Oceania | Milford Sound, Auckland skyline |
| Taiwan | Asia | Taipei 101, Taipei skyline |
| Canada | North America | Toronto CN Tower, Banff, Niagara Falls |
| Singapore | Asia | Marina Bay Sands, Gardens by the Bay |
| Cambodia | Asia | Angkor Wat sunrise |
| Russia | Europe | Saint Basil's Cathedral, Red Square Moscow |
| China | Asia | Great Wall of China, Shanghai skyline |
| Indonesia | Asia | Bali rice terraces, Borobudur temple |
| Maldives | Asia | overwater bungalow, turquoise lagoon |
| United Arab Emirates | Middle East | Burj Khalifa, Dubai skyline |
| Thailand | Asia | Bangkok temple, Phuket beach |
| Malaysia | Asia | Petronas Towers Kuala Lumpur |
| Sri Lanka | Asia | Sigiriya rock fortress, tea plantations |
| Vietnam | Asia | Ha Long Bay, Hoi An lanterns |
| Hong Kong | Asia | Hong Kong skyline, Victoria Harbour |

> **Schengen note:** the visa covers 27 countries, so there's no single "correct" landmark. Two reasonable options: (1) use Paris/Eiffel Tower as the most globally recognizable stand-in, since most searchers associate it with "Europe trip," or (2) use a composed shot of a European old-town square or café street that reads as "Europe" without pinning one specific country. Either is defensible — just be consistent with how confidently the other 19 photos name a specific place.

---

## E. Testimonial portraits

Currently initials on a gold gradient circle (RS, PN, VR). Three client quotes on the Home page, attributed to named individuals — Rohit Sharma, Priya Nair, Vikram Raj.

**1 — What it should communicate**

A real person behind a real quote — the entire value of a testimonial is that it's specific and true.

**2 — Ideal composition**

A friendly, direct-to-camera headshot with a warm expression, evenly lit face, and a plain or gently blurred background. At 44px display size, anything busy in the background or an extreme angle will just turn to mush — keep it simple and centered.

**3 — Search keywords**

Only relevant if you proceed despite the caveat below.

- `Indian professional headshot`
- `friendly portrait plain background`

**4 — Aspect ratio**

1:1 — square, cropped to a circle in the layout.

**5 — Resolution**

```
400×400 minimum
```

The live display is only 44px, but keep it sharp in case it's ever reused larger.

**6 — Format**

JPEG source, converted to WebP for production.

> **Think twice before using stock here.** These quotes are attributed to specific named people. A stock photo standing in for "Rohit Sharma" isn't a neutral placeholder the way an airport photo is — it's presenting a stock model as if they were a real, identifiable customer, which is a genuine trust and reputational risk (and in some places a legal one) if a visitor ever recognizes the model from elsewhere. If real client photos with permission aren't available, the current initials-avatar treatment is the safer choice to keep, not replace.

---

Every image on this list currently renders as a CSS gradient with an icon or initials — nothing is broken, this is a planning document for the swap. The project's build pipeline already expects a plain high-resolution JPEG as input and produces the optimized web output automatically, so downloading at "Large" / "Original" size from Unsplash or Pexels is the correct move regardless of format nuances above.
