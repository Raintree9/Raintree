import { initNav } from "../modules/nav.js";
import { setCopyrightYear, setOfficeHours } from "../modules/footer.js";
import { generateEventId, initContactLinkTracking, trackViewContent } from "../modules/pixel.js";

const PENDING_LEAD_KEY = "rt_pending_lead";
const UTM_PARAMS = ["utm_source", "utm_campaign", "utm_content"];

function currentScript() {
  // import.meta isn't needed here — the <script type="module"> tag that
  // loaded this file carries the per-page content_name/content_category
  // as data attributes, found via its own src.
  return document.querySelector('script[src*="landing-page.js"]');
}

function populateUtmFields(form) {
  const params = new URLSearchParams(window.location.search);
  UTM_PARAMS.forEach((key) => {
    const field = form.querySelector(`[data-utm="${key}"]`);
    if (field) field.value = params.get(key) || "";
  });
}

function initContactForm(contentName, contentCategory) {
  const form = document.querySelector("[data-contact-form]");
  if (!form) return;

  populateUtmFields(form);

  const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const INDIAN_MOBILE_PATTERN = /^(?:\+?91|0)?([6-9]\d{9})$/;

  function showFieldError(field, message) {
    field.setAttribute("data-touched", "true");
    field.setCustomValidity(message ?? "");
    const errorEl = document.getElementById(`${field.id}-error`);
    if (errorEl) errorEl.textContent = message ?? "";
  }

  function validateField(field) {
    if (field.validity.valueMissing) {
      showFieldError(field, field.type === "checkbox" ? "Please accept to continue." : "This field is required.");
      return false;
    }
    if (field.type === "email" && field.value && !EMAIL_PATTERN.test(field.value)) {
      showFieldError(field, "Enter a valid email address.");
      return false;
    }
    if (field.id === "phone" && !INDIAN_MOBILE_PATTERN.test(field.value.replace(/[\s-]/g, ""))) {
      showFieldError(field, "Enter a valid 10-digit Indian mobile number.");
      return false;
    }
    showFieldError(field, "");
    return true;
  }

  const fields = [...form.querySelectorAll("input[required], select[required], textarea[required]")];
  const errorNote = document.querySelector("[data-form-error]");
  const submitBtn = form.querySelector("button[type='submit']");

  fields.forEach((field) => {
    field.addEventListener("blur", () => validateField(field));
    if (field.type === "checkbox") {
      field.addEventListener("change", () => validateField(field));
    }
  });

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const allValid = fields.map(validateField).every(Boolean);
    if (!allValid) {
      fields.find((f) => !validateField(f))?.focus();
      return;
    }

    if (errorNote) errorNote.hidden = true;
    submitBtn.disabled = true;

    try {
      const response = await fetch(form.action, {
        method: form.method,
        body: new FormData(form),
        headers: { Accept: "application/json" },
      });

      if (!response.ok) throw new Error(`Formspree responded with ${response.status}`);

      sessionStorage.setItem(
        PENDING_LEAD_KEY,
        JSON.stringify({
          eventId: generateEventId(),
          contentName,
          contentCategory,
        })
      );

      window.location.href = "../../thank-you.html";
    } catch (error) {
      console.error("Landing page form submission failed:", error);
      if (errorNote) errorNote.hidden = false;
      submitBtn.disabled = false;
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  const script = currentScript();
  const contentName = script?.dataset.contentName || "Landing Page";
  const contentCategory = script?.dataset.contentCategory || "visitor";

  initNav();
  setCopyrightYear();
  setOfficeHours();
  initContactLinkTracking();
  initContactForm(contentName, contentCategory);
  trackViewContent({ content_name: contentName, content_category: contentCategory });
});
