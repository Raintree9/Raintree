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

// Single source of truth for the office hours shown in the header/footer
// contact info on every page. Placeholder pending the client's confirmed
// hours — update this one value, no page edits needed.
export const OFFICE_HOURS = "Mon - Sat 9:30 AM - 6:30 PM";

/**
 * Fills every element with data-office-hours from the OFFICE_HOURS
 * constant above. Markup must pre-fill the same static text for
 * no-JS/pre-hydration rendering, same pattern as setCopyrightYear.
 */
export function setOfficeHours() {
  document.querySelectorAll("[data-office-hours]").forEach((el) => {
    el.textContent = OFFICE_HOURS;
  });
}
