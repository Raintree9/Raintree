import { initNav } from "../modules/nav.js";
import { setCopyrightYear } from "../modules/footer.js";
import { renderFooterCountries } from "../modules/footer-countries.js";
import { getCountries } from "../modules/data-service.js";
import { destinationCardMarkup } from "../modules/destination-card.js";

const REGIONS = ["All Countries", "Asia", "Europe", "North America", "Oceania", "Middle East"];

let allCountries = [];
let activeRegion = "All Countries";
let searchTerm = "";

function regionPillMarkup(region) {
  const pressed = region === activeRegion;
  return `<button type="button" class="filter-pill" data-region="${region}" aria-pressed="${pressed}">${region}</button>`;
}

function renderPills() {
  const container = document.querySelector("[data-region-pills]");
  if (!container) return;
  container.innerHTML = REGIONS.map(regionPillMarkup).join("");
  container.querySelectorAll(".filter-pill").forEach((btn) => {
    btn.addEventListener("click", () => {
      activeRegion = btn.dataset.region;
      renderPills();
      renderGrid();
    });
  });
}

function applyFilters() {
  return allCountries.filter((country) => {
    const matchesRegion = activeRegion === "All Countries" || country.region === activeRegion;
    const matchesSearch = country.country.toLowerCase().includes(searchTerm.trim().toLowerCase());
    return matchesRegion && matchesSearch;
  });
}

function renderGrid() {
  const grid = document.querySelector("[data-countries-grid]");
  const count = document.querySelector("[data-countries-count]");
  if (!grid) return;

  const filtered = applyFilters();

  if (count) {
    count.textContent = `${filtered.length} destination${filtered.length === 1 ? "" : "s"} found`;
  }

  grid.innerHTML = filtered.length
    ? filtered.map(destinationCardMarkup).join("")
    : `<li class="countries-empty">No destinations match your search. Try a different name or filter.</li>`;
}

function initSearch() {
  const input = document.querySelector("[data-country-search]");
  if (!input) return;
  input.addEventListener("input", () => {
    searchTerm = input.value;
    renderGrid();
  });
}

async function init() {
  const grid = document.querySelector("[data-countries-grid]");
  if (!grid) return;

  try {
    allCountries = (await getCountries()).slice().sort((a, b) => a.country.localeCompare(b.country));
    renderPills();
    initSearch();
    renderGrid();
  } catch (error) {
    console.error("Failed to load countries:", error);
    grid.innerHTML = `<li class="countries-empty">We couldn't load destinations right now. Please refresh or check back shortly.</li>`;
  }
}

document.addEventListener("DOMContentLoaded", () => {
  initNav();
  setCopyrightYear();
  renderFooterCountries();
  init();
});
