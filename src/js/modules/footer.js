/**
 * Keeps the footer copyright year correct without hand-editing it on
 * every page every January. Markup must include an element with
 * data-copyright-year, pre-filled with a static fallback year for
 * no-JS/pre-hydration rendering.
 */
export function setCopyrightYear() {
  const el = document.querySelector("[data-copyright-year]");
  if (el) el.textContent = String(new Date().getFullYear());
}
