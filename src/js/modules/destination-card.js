/**
 * Renders one destination-card <li> for a country record from
 * src/data/countries.json. Shared by the Home page's featured grid and
 * the Countries listing page's full grid so both stay visually identical.
 */

// Countries with a processed production photo in assets/images/destinations/.
// Countries not in this set still render the flag-on-gradient placeholder
// until a photo is sourced and run through scripts/process_content_images.py.
export const PHOTO_COUNTRIES = new Set([
  "australia",
  "cambodia",
  "canada",
  "china",
  "dubai",
  "hong-kong",
  "indonesia",
  "japan",
  "malaysia",
  "maldives",
  "new-zealand",
  "russia",
  "schengen",
  "singapore",
  "slovakia",
  "south-korea",
  "sri-lanka",
  "taiwan",
  "thailand",
  "united-arab-emirates",
  "united-kingdom",
  "vietnam",
]);

export function serviceLabel(country) {
  return country.serviceType === "work-permit" ? "Work Permit" : "Visitor Visa";
}

function destinationMediaMarkup(country) {
  if (!PHOTO_COUNTRIES.has(country.id)) {
    return `
      <div class="destination-card__media media-placeholder" aria-hidden="true">
        <span class="media-placeholder__flag">${country.flag ?? ""}</span>
      </div>
    `;
  }

  const base = `assets/images/destinations/${country.id}`;
  return `
    <div class="destination-card__media">
      <picture>
        <source
          type="image/webp"
          srcset="${base}-480.webp 480w, ${base}-800.webp 800w, ${base}-1200.webp 1200w"
          sizes="(max-width: 599px) 50vw, (max-width: 1023px) 33vw, 240px"
        />
        <img
          src="${base}-480.jpg"
          srcset="${base}-480.jpg 480w, ${base}-800.jpg 800w, ${base}-1200.jpg 1200w"
          sizes="(max-width: 599px) 50vw, (max-width: 1023px) 33vw, 240px"
          width="480"
          height="360"
          alt=""
          loading="lazy"
          decoding="async"
        />
      </picture>
    </div>
  `;
}

export function destinationCardMarkup(country) {
  const isClosed = country.status === "closed";
  return `
    <li>
      <a
        class="destination-card card card--hoverable${isClosed ? " destination-card--closed" : ""}"
        href="country-detail.html?country=${encodeURIComponent(country.id)}"
      >
        ${destinationMediaMarkup(country)}
        ${isClosed ? `<span class="destination-card__status-badge">Closed</span>` : ""}
        <div class="destination-card__body">
          <span>
            <span class="destination-card__name">${country.country}</span>
            <span class="destination-card__label">${serviceLabel(country)}</span>
          </span>
          <span class="destination-card__arrow" aria-hidden="true">
            <svg width="16" height="16"><use href="assets/icons/sprite.svg#icon-arrow-right"></use></svg>
          </span>
        </div>
      </a>
    </li>
  `;
}
