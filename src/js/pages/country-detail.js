import { initNav } from "../modules/nav.js";
import { setCopyrightYear } from "../modules/footer.js";
import { renderFooterCountries } from "../modules/footer-countries.js";
import { getCountryById } from "../modules/data-service.js";
import { PHOTO_COUNTRIES, serviceLabel } from "../modules/destination-card.js";

const INFO_FIELDS = [
  { key: "visaType", label: "Visa Type", icon: "icon-document" },
  { key: "lengthOfStay", label: "Length of Stay", icon: "icon-clock" },
  { key: "visaValidity", label: "Visa Validity", icon: "icon-clock" },
  { key: "entryType", label: "Entry Type", icon: "icon-arrow-right" },
  { key: "method", label: "Application Method", icon: "icon-globe" },
  { key: "purposeText", label: "Purpose", icon: "icon-user" },
  { key: "processingTime", label: "Processing Time", icon: "icon-clock" },
  { key: "note", label: "Important Note", icon: "icon-shield-check" },
];

const IMPORTANT_NOTE =
  "Visa validity and stay duration are subject to the final decision of the destination country's immigration authorities.";

function infoCardMarkup(field, value) {
  return `
    <li class="card info-card">
      <span class="info-card__icon" aria-hidden="true"><svg><use href="assets/icons/sprite.svg#${field.icon}"></use></svg></span>
      <span>
        <span class="info-card__label">${field.label}</span>
        <span class="info-card__value">${value}</span>
      </span>
    </li>
  `;
}

function purposeBadgeMarkup(purpose) {
  return `<li class="badge">${purpose}</li>`;
}

function documentItemMarkup(doc) {
  return `
    <li class="checklist__item">
      <span class="checklist__icon" aria-hidden="true"><svg><use href="assets/icons/sprite.svg#icon-check"></use></svg></span>
      <span>${doc}</span>
    </li>
  `;
}

function updateMeta(id, attr, value) {
  document.getElementById(id)?.setAttribute(attr, value);
}

function heroMediaMarkup(country) {
  if (!PHOTO_COUNTRIES.has(country.id)) {
    return `
      <div class="media-placeholder" aria-hidden="true">
        <span class="media-placeholder__flag">${country.flag ?? ""}</span>
      </div>
    `;
  }

  const base = `assets/images/destinations/${country.id}`;
  return `
    <picture>
      <source
        type="image/webp"
        srcset="${base}-480.webp 480w, ${base}-800.webp 800w, ${base}-1200.webp 1200w"
        sizes="(max-width: 767px) 100vw, 40vw"
      />
      <img
        src="${base}-800.jpg"
        srcset="${base}-480.jpg 480w, ${base}-800.jpg 800w, ${base}-1200.jpg 1200w"
        sizes="(max-width: 767px) 100vw, 40vw"
        width="800"
        height="600"
        alt=""
        loading="lazy"
        decoding="async"
      />
    </picture>
  `;
}

function renderCountry(country) {
  const label = serviceLabel(country);
  const title = `${country.country} ${label} Requirements | RainTree Immigration`;
  const description = `${country.country} ${label.toLowerCase()}: ${country.visaType}, ${country.lengthOfStay}, processing in ${country.processingTime}. Full requirements and document checklist from RainTree Immigration.`;
  const canonicalUrl = `https://www.raintreeimmigration.com/country-detail.html?country=${encodeURIComponent(country.id)}`;

  document.title = title;
  updateMeta("meta-description", "content", description);
  updateMeta("canonical-link", "href", canonicalUrl);
  updateMeta("meta-og-title", "content", title);
  updateMeta("meta-og-description", "content", description);
  updateMeta("meta-og-url", "content", canonicalUrl);
  updateMeta("meta-twitter-title", "content", title);
  updateMeta("meta-twitter-description", "content", description);

  const breadcrumbScript = document.getElementById("breadcrumb-jsonld");
  if (breadcrumbScript) {
    breadcrumbScript.textContent = JSON.stringify({
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      itemListElement: [
        { "@type": "ListItem", position: 1, name: "Home", item: "https://www.raintreeimmigration.com/" },
        { "@type": "ListItem", position: 2, name: "Countries", item: "https://www.raintreeimmigration.com/countries.html" },
        { "@type": "ListItem", position: 3, name: `${country.country} ${label}`, item: canonicalUrl },
      ],
    });
  }

  document.querySelectorAll("[data-breadcrumb-country]").forEach((el) => {
    el.textContent = `${country.country} ${label}`;
  });

  const heroMedia = document.querySelector("[data-hero-media]");
  if (heroMedia) {
    heroMedia.innerHTML = heroMediaMarkup(country);
  }

  document.querySelectorAll("[data-hero-title-flag]").forEach((el) => {
    el.textContent = country.flag ?? "";
  });
  document.querySelectorAll("[data-hero-title]").forEach((el) => {
    el.textContent = `${country.country} ${label}`;
  });

  document.querySelectorAll("[data-hero-status]").forEach((el) => {
    if (country.status === "closed") {
      el.textContent = `Applications for ${country.country} are currently closed`;
      el.hidden = false;
    } else {
      el.hidden = true;
    }
  });

  const purposeText = country.purpose.join(", ");
  document.querySelectorAll("[data-hero-desc]").forEach((el) => {
    el.textContent =
      country.serviceType === "work-permit"
        ? `Planning to work in ${country.country}? Here's everything you need to know about the work permit process, required documents, and processing time.`
        : `Planning to visit ${country.country} for ${purposeText.toLowerCase()}? Here's everything you need to know about the visa process, required documents, and processing time.`;
  });

  const purposeList = document.querySelector("[data-hero-purpose]");
  if (purposeList) {
    purposeList.innerHTML = country.purpose.map(purposeBadgeMarkup).join("");
  }

  const infoGrid = document.querySelector("[data-info-grid]");
  if (infoGrid) {
    const values = { ...country, purposeText, note: IMPORTANT_NOTE };
    infoGrid.innerHTML = INFO_FIELDS.map((field) => infoCardMarkup(field, values[field.key])).join("");
  }

  const docsList = document.querySelector("[data-documents-list]");
  if (docsList) {
    docsList.innerHTML = country.documents.length
      ? country.documents.map(documentItemMarkup).join("")
      : `<li class="checklist__item"><span>Document list coming soon — contact us for the latest requirements.</span></li>`;
  }

  document.querySelectorAll("[data-cta-country-name]").forEach((el) => {
    el.textContent = country.country;
  });
}

function showNotFound() {
  const content = document.querySelector("[data-detail-content]");
  const notFound = document.querySelector("[data-not-found]");
  if (content) content.hidden = true;
  if (notFound) notFound.hidden = false;
}

async function init() {
  const params = new URLSearchParams(window.location.search);
  const countryId = params.get("country");

  if (!countryId) {
    showNotFound();
    return;
  }

  try {
    const country = await getCountryById(countryId);
    if (!country) {
      showNotFound();
      return;
    }
    renderCountry(country);
  } catch (error) {
    console.error("Failed to load country:", error);
    showNotFound();
  }
}

document.addEventListener("DOMContentLoaded", () => {
  initNav();
  setCopyrightYear();
  renderFooterCountries();
  init();
});
