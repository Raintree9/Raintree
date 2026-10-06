/**
 * Thin wrapper around the Meta Pixel global (window.fbq), loaded by the
 * base snippet in every page's <head> — generated from config/tracking.json
 * by scripts/build_tracking.py. Centralizes event calls so page scripts
 * never touch window.fbq directly, and no-ops safely if the pixel didn't
 * load (ad blocker, consent tool, etc.) instead of throwing.
 *
 * Every event gets its own event_id (crypto.randomUUID), passed to fbq as
 * eventID. CAPI_ENDPOINT is null until a server-side Conversions API relay
 * exists (tracked for a later session — this project is static-hosted on
 * GitHub Pages with no server runtime, so CAPI needs a separate serverless
 * function). Once that endpoint exists, set CAPI_ENDPOINT below and every
 * event already has the event_id plumbing in place for Meta to dedupe the
 * browser + server copies of the same event — no other changes needed here.
 */

const CAPI_ENDPOINT = null; // e.g. "https://<worker>.workers.dev/meta-capi"

export function generateEventId() {
  if (typeof crypto !== "undefined" && typeof crypto.randomUUID === "function") {
    return crypto.randomUUID();
  }
  return `${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

function sendToCapi(eventName, params, eventId) {
  if (!CAPI_ENDPOINT) return;
  fetch(CAPI_ENDPOINT, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ eventName, params, eventId, eventSourceUrl: window.location.href }),
    keepalive: true,
  }).catch(() => {});
}

function fire(eventName, params, eventId) {
  if (typeof window.fbq === "function") {
    window.fbq("track", eventName, params, { eventID: eventId });
  }
  sendToCapi(eventName, params, eventId);
}

function fireCustom(eventName, params, eventId) {
  if (typeof window.fbq === "function") {
    window.fbq("trackCustom", eventName, params, { eventID: eventId });
  }
  sendToCapi(eventName, params, eventId);
}

/** Standard Contact event — for actions that directly initiate contact
 *  (phone call, WhatsApp), not general navigation toward a contact page. */
export function trackContact(params) {
  fire("Contact", params, generateEventId());
}

/** Standard ViewContent event — fire on a specific visa/country/service
 *  page, e.g. { content_name: "Canada Visitor Visa", content_category: "visitor" }. */
export function trackViewContent(params) {
  fire("ViewContent", params, generateEventId());
}

/** Standard Schedule event — fire only after a confirmed consultation
 *  booking (not a booking-page visit or button click). */
export function trackSchedule(params) {
  fire("Schedule", params, generateEventId());
}

/**
 * Standard Lead event — fire ONLY after a genuine confirmed enquiry.
 * Accepts an optional pre-generated eventId so a Lead started on one page
 * (e.g. the contact form) can be confirmed and fired on another (e.g.
 * /thank-you.html) using the same event_id throughout — required for Meta
 * to dedupe this browser event against the future CAPI copy of the same
 * event. Returns the event_id used, so callers that generate their own can
 * carry it forward (e.g. into a GA4 dataLayer push).
 */
export function trackLead(params, eventId) {
  const id = eventId || generateEventId();
  fire("Lead", params, id);
  return id;
}

/** Custom event, for site-specific actions with no matching standard event. */
export function trackCustom(eventName, params) {
  fireCustom(eventName, params, generateEventId());
}

/** Pushes an event onto the GTM/GA4 dataLayer. Safe to call before GTM has
 *  finished loading — dataLayer.push queues it either way. */
export function pushDataLayerEvent(eventName, data = {}) {
  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push({ event: eventName, ...data });
}

const CONTACT_LINK_SELECTOR = 'a[href^="tel:"], a[href*="wa.me"], a[href*="api.whatsapp.com"]';

function contactMethodFor(href) {
  if (href.startsWith("tel:")) return "phone";
  return "whatsapp";
}

/**
 * Delegated click tracking for direct-contact links (call/WhatsApp) present
 * in the shared header and footer on every page. Fires the standard
 * Contact event once per click — these links represent someone actually
 * initiating contact, unlike a "Book Consultation" link that just
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
