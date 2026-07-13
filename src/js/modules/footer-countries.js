import { getCountries } from "./data-service.js";

function byFeaturedOrder(a, b) {
  return (a.featuredOrder ?? 0) - (b.featuredOrder ?? 0);
}

function footerCountryLinkMarkup(country) {
  return `<li><a href="country-detail.html?country=${encodeURIComponent(country.id)}">${country.country}</a></li>`;
}

/**
 * Fills the footer's "Popular Countries" list from src/data/countries.json.
 * Every page ships the same footer markup with a [data-footer-countries]
 * <ul>, so this is shared rather than duplicated per page script.
 */
export async function renderFooterCountries() {
  const footerList = document.querySelector("[data-footer-countries]");
  if (!footerList) return;

  try {
    const countries = await getCountries();
    const featured = countries.filter((c) => c.featured).sort(byFeaturedOrder);
    footerList.innerHTML = featured.map(footerCountryLinkMarkup).join("");
  } catch (error) {
    console.error("Failed to load footer countries:", error);
    footerList.innerHTML = `<li class="data-error">Unable to load.</li>`;
  }
}
