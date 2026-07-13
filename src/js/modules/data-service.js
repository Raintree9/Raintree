/**
 * Shared accessor for src/data/countries.json. Fetches once per page load
 * and caches the parsed result so every page/component that needs country
 * data (Home destinations, Countries listing, Country Detail) shares one
 * request instead of re-fetching.
 */
// Relative, not absolute — GitHub Pages project sites are served from a
// subpath (username.github.io/repo-name/), and a leading slash would
// resolve to the domain root instead, breaking every fetch.
const DATA_URL = "src/data/countries.json";

// Cache the in-flight promise, not just the resolved value — callers that
// fire concurrently (e.g. destinations + testimonials both requesting data
// on DOMContentLoaded, neither awaiting the other) would otherwise both
// race past a "resolved value" cache check before either fetch finishes,
// each triggering its own network request.
let cachePromise = null;

export function getCountries() {
  if (!cachePromise) {
    cachePromise = fetch(DATA_URL).then((response) => {
      if (!response.ok) {
        throw new Error(`Failed to load country data: ${response.status} ${response.statusText}`);
      }
      return response.json();
    });
  }
  return cachePromise;
}

export async function getCountryById(id) {
  const countries = await getCountries();
  return countries.find((country) => country.id === id) ?? null;
}
