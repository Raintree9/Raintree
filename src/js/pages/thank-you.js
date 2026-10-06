import { initNav } from "../modules/nav.js";
import { setCopyrightYear, setOfficeHours } from "../modules/footer.js";
import { renderFooterCountries } from "../modules/footer-countries.js";
import { trackLead, pushDataLayerEvent, initContactLinkTracking } from "../modules/pixel.js";

const PENDING_LEAD_KEY = "rt_pending_lead";

/**
 * Lead only fires here, and only once: contact.js sets this sessionStorage
 * flag right after a genuine successful Formspree submission, carrying the
 * event_id that will later let a Conversions API copy of the same event
 * dedupe against this browser one. The flag is removed immediately (before
 * any parsing/firing), so a refresh of this page, a direct visit, or the
 * back button landing here never fires a duplicate Lead.
 */
function fireLeadIfPending() {
  const raw = sessionStorage.getItem(PENDING_LEAD_KEY);
  if (!raw) return;

  sessionStorage.removeItem(PENDING_LEAD_KEY);

  let pending;
  try {
    pending = JSON.parse(raw);
  } catch {
    return;
  }
  if (!pending?.eventId) return;

  trackLead({ content_name: pending.contentName, content_category: pending.contentCategory }, pending.eventId);
  pushDataLayerEvent("generate_lead", { event_id: pending.eventId });
}

document.addEventListener("DOMContentLoaded", () => {
  initNav();
  setCopyrightYear();
  setOfficeHours();
  renderFooterCountries();
  initContactLinkTracking();
  fireLeadIfPending();
});
