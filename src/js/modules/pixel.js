/**
 * Thin wrapper around the Meta Pixel global (window.fbq), which is loaded
 * by the base snippet in every page's <head> — see docs/meta-pixel.md.
 * Centralizes event calls so page scripts never touch window.fbq directly,
 * and no-ops safely (instead of throwing) if the pixel didn't load, e.g.
 * an ad blocker or consent tool stripped it.
 */
function fire(method, ...args) {
  if (typeof window.fbq !== "function") return;
  window.fbq(method, ...args);
}

/** Standard Lead event — fire only after a genuine confirmed enquiry
 *  (e.g. a successful contact form submission), never on a mere click. */
export function trackLead(params) {
  fire("track", "Lead", params);
}

/** Standard Contact event — for actions that directly initiate contact
 *  (phone call, email, WhatsApp), not general navigation toward a
 *  contact page. */
export function trackContact(params) {
  fire("track", "Contact", params);
}

/** Custom event, for site-specific actions with no matching standard event
 *  (e.g. ViewDestination). */
export function trackCustom(eventName, params) {
  fire("trackCustom", eventName, params);
}

const CONTACT_LINK_SELECTOR = 'a[href^="tel:"], a[href^="mailto:"], a[href*="wa.me"]';

function contactMethodFor(href) {
  if (href.startsWith("tel:")) return "phone";
  if (href.startsWith("mailto:")) return "email";
  return "whatsapp";
}

/**
 * Delegated click tracking for direct-contact links (call/email/WhatsApp)
 * present in the shared header and footer on every page. Fires the
 * standard Contact event once per click — these links represent someone
 * actually initiating contact, unlike a "Book Consultation" link that just
 * navigates to the contact page (that page load is already covered by the
 * base snippet's own PageView, so it isn't double-counted here).
 */
export function initContactLinkTracking() {
  document.addEventListener("click", (event) => {
    const link = event.target.closest(CONTACT_LINK_SELECTOR);
    if (!link) return;
    trackContact({ content_name: contactMethodFor(link.getAttribute("href")) });
  });
}
