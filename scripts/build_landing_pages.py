"""
Generates the /lp/<slug>/index.html ad landing pages from LANDING_PAGES
below. These are deliberately simple, fast pages for paid traffic: same
header/footer/tracking as the main site, noindex, a short country-specific
pitch, and the same enquiry form -> /thank-you.html Lead flow used
everywhere else.

Run from the project root (after any edit to LANDING_PAGES or the
template):
    python scripts/build_landing_pages.py

Pixel/GTM blocks are filled in by scripts/build_tracking.py afterwards —
run that too (or just run both; build_tracking.py is idempotent).
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LP_DIR = ROOT / "lp"

SITE_URL = "https://raintreeimmigration.com"
OG_IMAGE = f"{SITE_URL}/assets/images/og/og-default.jpg"

LANDING_PAGES = [
    {
        "slug": "canada-visitor-visa",
        "country": "Canada",
        "article": "",  # "Planning a trip to Canada?" — no article needed
        "content_category": "visitor",
        "official_url": "https://www.canada.ca/en/immigration-refugees-citizenship/services/visit-canada.html",
        "official_label": "IRCC — Canada's official visitor visa page",
    },
    {
        "slug": "uk-visitor-visa",
        "country": "United Kingdom",
        "article": "the ",  # "Planning a trip to the United Kingdom?"
        "content_category": "visitor",
        "official_url": "https://www.gov.uk/standard-visitor-visa",
        "official_label": "GOV.UK — Standard Visitor visa",
    },
    {
        "slug": "schengen-visa",
        "country": "Schengen Area",
        "article": "the ",
        "content_category": "visitor",
        "official_url": "https://home-affairs.ec.europa.eu/policies/schengen-borders-and-visa/visa-policy_en",
        "official_label": "European Commission — Schengen visa policy",
    },
    {
        "slug": "australia-visitor-visa",
        "country": "Australia",
        "article": "",
        "content_category": "visitor",
        "official_url": "https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-listing/visitor-600",
        "official_label": "Australian Department of Home Affairs — Visitor visa (600)",
    },
]

TRUST_POINTS = [
    ("icon-map-pin", "Local Office in Coimbatore", "Visit us in person at our Avinashi Road office — not a call centre."),
    ("icon-user", "Experienced Team", "Years of hands-on visa documentation experience across 20+ destinations."),
    ("icon-shield-check", "Transparent Process", "You'll know exactly what's needed and why, at every step."),
    ("icon-headset", "Real Support", "A real person responds to every enquiry — by phone, WhatsApp, or email."),
]

HOW_IT_WORKS = [
    ("01", "Tell Us Your Plan", "Share your travel details and we'll explain exactly what documents you'll need."),
    ("02", "We Review Your Documents", "Our team checks everything for accuracy and completeness before submission."),
    ("03", "Application Submitted", "Your application is submitted to the relevant authority on your behalf."),
    ("04", "You're Kept Updated", "We share updates as your application moves through the process."),
]

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <!-- Google Tag Manager -->
  <!-- End Google Tag Manager -->

  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />

  <!-- Meta Pixel Code -->
  <!-- End Meta Pixel Code -->
  <title>{country} Visitor Visa Documentation Support | RainTree Immigration</title>
  <meta name="description" content="Documentation and application support for your {country} visitor visa. Local Coimbatore office, transparent process, free consultation." />
  <meta name="robots" content="noindex" />
  <meta name="theme-color" content="#0B3D2E" />
  <link rel="canonical" href="{page_url}" />

  <!-- Social Meta -->
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="RainTree Immigration" />
  <meta property="og:title" content="{country} Visitor Visa Documentation Support | RainTree Immigration" />
  <meta property="og:description" content="Documentation and application support for your {country} visitor visa. Local Coimbatore office, transparent process, free consultation." />
  <meta property="og:url" content="{page_url}" />
  <meta property="og:image" content="{og_image}" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:image:alt" content="RainTree Immigration logo" />
  <meta property="og:locale" content="en_IN" />

  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{country} Visitor Visa Documentation Support | RainTree Immigration" />
  <meta name="twitter:description" content="Documentation and application support for your {country} visitor visa. Local Coimbatore office, transparent process, free consultation." />
  <meta name="twitter:image" content="{og_image}" />
  <!-- End Social Meta -->

  <link rel="icon" type="image/png" sizes="32x32" href="../../assets/images/brand/favicon-32.png" />
  <link rel="icon" type="image/png" sizes="180x180" href="../../assets/images/brand/favicon-180.png" />
  <link rel="apple-touch-icon" href="../../assets/images/brand/apple-touch-icon.png" />

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link
    href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Poppins:wght@400;500;600;700&display=swap"
    rel="stylesheet"
  />

  <link rel="stylesheet" href="../../src/css/main.css" />
  <link rel="stylesheet" href="../../src/css/pages/contact.css" />
</head>
<body>
  <!-- Google Tag Manager (noscript) -->
  <!-- End Google Tag Manager (noscript) -->

  <a class="skip-link" href="#main-content">Skip to main content</a>

  <header class="site-header">
    <div class="site-header__inner">
      <a class="site-logo" href="../../index.html">
        <picture>
          <source type="image/webp" srcset="../../assets/images/brand/logo-mark-64.webp 1x, ../../assets/images/brand/logo-mark-128.webp 2x" />
          <img
            class="site-logo__mark"
            src="../../assets/images/brand/logo-mark-64.png"
            srcset="../../assets/images/brand/logo-mark-64.png 1x, ../../assets/images/brand/logo-mark-128.png 2x"
            width="32"
            height="32"
            alt=""
          />
        </picture>
        <span>
          <span class="site-logo__name">RAINTREE</span>
          <span class="site-logo__tagline">IMMIGRATION</span>
        </span>
      </a>
      <div class="site-header__actions">
        <a class="site-header__phone" href="tel:+917448444288">
          <svg aria-hidden="true"><use href="../../assets/icons/sprite.svg#icon-phone"></use></svg>
          <span>+91 74484 44288</span>
        </a>
      </div>
    </div>
  </header>

  <main id="main-content">
    <section class="page-hero">
      <div class="container">
        <div class="page-hero__content">
          <p class="eyebrow">Visitor Visa Documentation Support</p>
          <h1 class="page-hero__title">{country} Visitor Visa — Documentation Done Right</h1>
          <p class="text-lead">
            Planning a trip to {article}{country}? We help you prepare and submit a complete, accurate application —
            clear guidance from a local Coimbatore team, from document checklist to submission.
          </p>
          <div class="contact-hero__actions">
            <a class="btn btn--primary btn--lg" href="tel:+917448444288">
              <svg aria-hidden="true"><use href="../../assets/icons/sprite.svg#icon-phone"></use></svg>
              Call Us
            </a>
            <a class="btn btn--outline btn--lg" href="https://wa.me/917448444288">
              <svg aria-hidden="true"><use href="../../assets/icons/sprite.svg#icon-whatsapp"></use></svg>
              WhatsApp Us
            </a>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--alt" style="padding-block: var(--space-10) var(--space-16);">
      <div class="container">
        <ul class="grid grid--4" role="list">
{trust_points_markup}
        </ul>
      </div>
    </section>

    <section class="section" aria-labelledby="how-it-works-heading">
      <div class="container">
        <div class="section-header section-header--center">
          <p class="eyebrow">How It Works</p>
          <h2 id="how-it-works-heading">Our Simple Process</h2>
        </div>
        <ol class="process-steps" role="list">
{steps_markup}
        </ol>
        <p class="text-lead" style="text-align: center; margin-top: var(--space-8);">
          For official processing times and the latest requirements, see the
          <a href="{official_url}" target="_blank" rel="noopener noreferrer">{official_label}</a>.
        </p>
      </div>
    </section>

    <section class="section section--alt" aria-labelledby="office-heading">
      <div class="container">
        <div class="detail-row">
          <div class="detail-row__media">
            <picture>
              <source type="image/webp" srcset="../../assets/images/team/about-team-640.webp 640w, ../../assets/images/team/about-team-960.webp 960w" sizes="(max-width: 1023px) 100vw, 40vw" />
              <img
                src="../../assets/images/team/about-team-640.jpg"
                srcset="../../assets/images/team/about-team-640.jpg 640w, ../../assets/images/team/about-team-960.jpg 960w"
                sizes="(max-width: 1023px) 100vw, 40vw"
                width="640"
                height="480"
                alt=""
                loading="lazy"
                decoding="async"
              />
            </picture>
          </div>
          <div>
            <h2 id="office-heading" class="detail-row__title">Visit Our Coimbatore Office</h2>
            <p class="detail-row__desc">
              83/3, Avinashi Rd, TNHB Colony, Civil Aerodrome Post, Coimbatore, Tamil Nadu 641014 — easily
              accessible near Avinashi Road. Prefer to start online? Fill in the form below and we'll call you.
            </p>
          </div>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="form-heading">
      <div class="container">
        <div class="card contact-form-panel" style="max-width: 640px; margin-inline: auto;">
          <h2 id="form-heading">Get Your Free Consultation</h2>
          <p class="text-lead" style="margin-bottom: var(--space-6);">
            Tell us about your trip and our team will get back to you as soon as possible.
          </p>

          <form data-contact-form data-lp-slug="{slug}" novalidate action="https://formspree.io/f/meeyqlrn" method="POST">
            <input type="hidden" name="_next" value="https://raintreeimmigration.com/thank-you.html" />
            <input type="hidden" name="landingPage" value="{slug}" />
            <input type="hidden" name="utm_source" data-utm="utm_source" value="" />
            <input type="hidden" name="utm_campaign" data-utm="utm_campaign" value="" />
            <input type="hidden" name="utm_content" data-utm="utm_content" value="" />

            <p class="contact-form-error" data-form-error role="alert" hidden>
              <svg aria-hidden="true"><use href="../../assets/icons/sprite.svg#icon-shield-check"></use></svg>
              <span>Something went wrong sending your message. Please try again, or call us directly.</span>
            </p>

            <div class="form-row">
              <div class="form-field">
                <label class="form-field__label" for="name">Your Name <span class="required">*</span></label>
                <input type="text" id="name" name="name" autocomplete="name" required />
                <span class="form-field__error" id="name-error" role="alert"></span>
              </div>
              <div class="form-field">
                <label class="form-field__label" for="phone">Your Phone Number <span class="required">*</span></label>
                <input type="tel" id="phone" name="phone" autocomplete="tel" placeholder="98765 43210" required />
                <span class="form-field__error" id="phone-error" role="alert"></span>
              </div>
            </div>

            <div class="form-row">
              <div class="form-field">
                <label class="form-field__label" for="email">Your Email</label>
                <input type="email" id="email" name="email" autocomplete="email" />
                <span class="form-field__error" id="email-error" role="alert"></span>
              </div>
              <div class="form-field">
                <label class="form-field__label" for="travel-month">Planned Travel Month</label>
                <input type="month" id="travel-month" name="travelMonth" />
              </div>
            </div>

            <div class="form-field">
              <label class="form-field__label" for="message">Your Message</label>
              <textarea id="message" name="message"></textarea>
              <span class="form-field__error" id="message-error" role="alert"></span>
            </div>

            <div class="form-field form-field--checkbox">
              <label class="form-checkbox">
                <input type="checkbox" id="consent" name="consent" required />
                <span>
                  I agree to be contacted by RainTree Immigration by phone/WhatsApp.
                  See our <a href="../../privacy-policy.html">Privacy Policy</a>. <span class="required">*</span>
                </span>
              </label>
              <span class="form-field__error" id="consent-error" role="alert"></span>
            </div>

            <button type="submit" class="btn btn--primary btn--block btn--lg">
              <svg aria-hidden="true"><use href="../../assets/icons/sprite.svg#icon-arrow-right"></use></svg>
              Send Message
            </button>

            <p class="form-note" style="margin-top: var(--space-4);">
              <svg aria-hidden="true"><use href="../../assets/icons/sprite.svg#icon-shield-check"></use></svg>
              Your information is safe with us. We never share your details.
            </p>
          </form>
        </div>
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <div class="site-footer__main">
      <div>
        <a class="site-logo" href="../../index.html">
          <picture>
            <source type="image/webp" srcset="../../assets/images/brand/logo-mark-64.webp 1x, ../../assets/images/brand/logo-mark-128.webp 2x" />
            <img
              class="site-logo__mark"
              src="../../assets/images/brand/logo-mark-64.png"
              srcset="../../assets/images/brand/logo-mark-64.png 1x, ../../assets/images/brand/logo-mark-128.png 2x"
              width="30"
              height="30"
              alt=""
            />
          </picture>
          <span>
            <span class="site-logo__name">RAINTREE</span>
            <span class="site-logo__tagline">IMMIGRATION</span>
          </span>
        </a>
        <p class="footer-brand__desc">Your trusted partner for visa and immigration services worldwide.</p>
      </div>

      <div>
        <p class="footer-col__title">Contact Us</p>
        <ul class="footer-col__list" role="list">
          <li class="footer-contact-item">
            <svg aria-hidden="true"><use href="../../assets/icons/sprite.svg#icon-map-pin"></use></svg>
            <span>83/3, Avinashi Rd, TNHB Colony, Civil Aerodrome Post, Coimbatore, Tamil Nadu 641014, India</span>
          </li>
          <li class="footer-contact-item">
            <svg aria-hidden="true"><use href="../../assets/icons/sprite.svg#icon-phone"></use></svg>
            <a href="tel:+917448444288">+91 74484 44288</a>
          </li>
          <li class="footer-contact-item">
            <svg aria-hidden="true"><use href="../../assets/icons/sprite.svg#icon-mail"></use></svg>
            <a href="mailto:info@raintreeimmigration.com">info@raintreeimmigration.com</a>
          </li>
          <li class="footer-contact-item">
            <svg aria-hidden="true"><use href="../../assets/icons/sprite.svg#icon-clock"></use></svg>
            <span data-office-hours>Mon - Sat 9:30 AM - 6:30 PM</span>
          </li>
        </ul>
      </div>
    </div>

    <div class="site-footer__disclaimer">
      <div class="site-footer__disclaimer-inner">
        RainTree Immigration provides visa consultation and documentation support. Visa decisions are made solely
        by the respective embassy or immigration authority. We do not guarantee visa approval and do not provide
        overseas employment or recruitment services.
      </div>
    </div>

    <div class="site-footer__bottom">
      <div class="site-footer__bottom-inner">
        <p>&copy; <span data-copyright-year>2026</span> RainTree Immigration. All Rights Reserved.</p>
        <div class="site-footer__legal">
          <a href="../../privacy-policy.html">Privacy Policy</a>
          <a href="../../terms-and-conditions.html">Terms and Conditions</a>
        </div>
      </div>
    </div>
  </footer>

  <script type="module" src="../../src/js/pages/landing-page.js" data-content-name="{country} Visitor Visa" data-content-category="{content_category}"></script>
</body>
</html>
"""


def trust_point_markup(icon, title, desc):
    return f"""          <li class="card feature-card">
            <span class="feature-card__icon" aria-hidden="true"><svg><use href="../../assets/icons/sprite.svg#{icon}"></use></svg></span>
            <p class="feature-card__title">{title}</p>
            <p class="feature-card__desc">{desc}</p>
          </li>"""


def step_markup(number, title, desc):
    return f"""          <li class="process-step">
            <span class="process-step__number" aria-hidden="true">{number}</span>
            <p class="process-step__title">{title}</p>
            <p class="process-step__desc">{desc}</p>
          </li>"""


def main():
    trust_markup = "\n".join(trust_point_markup(*t) for t in TRUST_POINTS)
    steps_markup = "\n".join(step_markup(*s) for s in HOW_IT_WORKS)

    for page in LANDING_PAGES:
        html = PAGE_TEMPLATE.format(
            slug=page["slug"],
            country=page["country"],
            article=page["article"],
            content_category=page["content_category"],
            official_url=page["official_url"],
            official_label=page["official_label"],
            trust_points_markup=trust_markup,
            steps_markup=steps_markup,
            page_url=f"{SITE_URL}/lp/{page['slug']}/",
            og_image=OG_IMAGE,
        )
        out_dir = LP_DIR / page["slug"]
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "index.html").write_text(html, encoding="utf-8")
        print(f"Wrote lp/{page['slug']}/index.html")


if __name__ == "__main__":
    main()
