import { initNav } from "../modules/nav.js";
import { setCopyrightYear } from "../modules/footer.js";
import { renderFooterCountries } from "../modules/footer-countries.js";
import { getCountries } from "../modules/data-service.js";
import { destinationCardMarkup } from "../modules/destination-card.js";

const REGIONS = ["All Countries", "Asia", "Europe", "North America", "Oceania", "Middle East"];
const SERVICES = [
  { id: "visitor-visa", label: "Visitor Visa" },
  { id: "work-permit", label: "Work Permit" },
];

let allCountries = [];
let activeRegion = "All Countries";
let activeService = "visitor-visa";
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

function servicePillMarkup(service) {
  const pressed = service.id === activeService;
  return `<button type="button" class="filter-pill filter-pill--lg" data-service="${service.id}" aria-pressed="${pressed}">${service.label}</button>`;
}

function renderServicePills() {
  const container = document.querySelector("[data-service-pills]");
  if (!container) return;
  container.innerHTML = SERVICES.map(servicePillMarkup).join("");
  container.querySelectorAll(".filter-pill").forEach((btn) => {
    btn.addEventListener("click", () => {
      activeService = btn.dataset.service;
      renderServicePills();
      renderGrid();
    });
  });
}

function applyFilters() {
  return allCountries.filter((country) => {
    const matchesService = country.serviceType === activeService;
    const matchesRegion = activeRegion === "All Countries" || country.region === activeRegion;
    const matchesSearch = country.country.toLowerCase().includes(searchTerm.trim().toLowerCase());
    return matchesService && matchesRegion && matchesSearch;
  });
}

function emptyStateMarkup() {
  if (activeService === "work-permit") {
    return `<li class="countries-empty">We're currently expanding our work permit destinations. Contact us to check eligibility for your destination.</li>`;
  }
  return `<li class="countries-empty">No destinations match your search. Try a different name or filter.</li>`;
}

function renderGrid() {
  const grid = document.querySelector("[data-countries-grid]");
  const count = document.querySelector("[data-countries-count]");
  if (!grid) return;

  const filtered = applyFilters();

  if (count) {
    count.textContent = filtered.length
      ? `${filtered.length} destination${filtered.length === 1 ? "" : "s"} found`
      : "";
  }

  grid.innerHTML = filtered.length ? filtered.map(destinationCardMarkup).join("") : emptyStateMarkup();
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

  const requestedService = new URLSearchParams(window.location.search).get("service");
  if (SERVICES.some((service) => service.id === requestedService)) {
    activeService = requestedService;
  }

  try {
    allCountries = (await getCountries()).slice().sort((a, b) => a.country.localeCompare(b.country));
    renderServicePills();
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
