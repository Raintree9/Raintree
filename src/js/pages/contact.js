import { initNav } from "../modules/nav.js";
import { setCopyrightYear, setOfficeHours } from "../modules/footer.js";
import { renderFooterCountries } from "../modules/footer-countries.js";
import { getCountries } from "../modules/data-service.js";
import { generateEventId, initContactLinkTracking } from "../modules/pixel.js";

const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
// Indian mobile numbers: 10 digits starting 6-9, with an optional +91/91/0
// prefix and optional spaces/hyphens, which are stripped before testing.
const INDIAN_MOBILE_PATTERN = /^(?:\+?91|0)?([6-9]\d{9})$/;

// Maps the form's "Visa Type" options onto the same content_category
// vocabulary used by ViewContent elsewhere (services.js, country-detail.js)
// so Meta's reporting groups them consistently.
const VISA_TYPE_TO_CATEGORY = {
  tourist: "visitor",
  "family-visit": "visitor",
  business: "business",
  student: "student",
  "work-permit-docs": "work-permit-docs",
};

const PENDING_LEAD_KEY = "rt_pending_lead";

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

async function populateCountryDropdown() {
  const select = document.getElementById("country");
  if (!select) return;

  try {
    const countries = (await getCountries()).slice().sort((a, b) => a.country.localeCompare(b.country));
    const options = countries.map((c) => `<option value="${c.id}">${c.country}</option>`).join("");
    select.insertAdjacentHTML("beforeend", options + `<option value="other">Other / Not sure yet</option>`);
  } catch (error) {
    console.error("Failed to load countries for the enquiry form:", error);
    select.insertAdjacentHTML("beforeend", `<option value="other">Other / Not sure yet</option>`);
  }
}

function initContactForm() {
  const form = document.querySelector("[data-contact-form]");
  if (!form) return;

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

      // Lead must only fire after this point is reached (a real, accepted
      // submission) — never on a button click. The event_id travels to
      // /thank-you.html via sessionStorage so that page can fire the
      // actual Lead event (and clear this flag so refreshing or revisiting
      // /thank-you.html directly never fires a duplicate).
      const visaType = form.elements.visaType?.value || "";
      const countrySelect = form.elements.country;
      const countryName = countrySelect?.selectedOptions?.[0]?.textContent || "";
      sessionStorage.setItem(
        PENDING_LEAD_KEY,
        JSON.stringify({
          eventId: generateEventId(),
          contentName: countryName ? `${countryName} enquiry` : "Contact Form",
          contentCategory: VISA_TYPE_TO_CATEGORY[visaType] || "visitor",
        })
      );

      window.location.href = "thank-you.html";
    } catch (error) {
      console.error("Contact form submission failed:", error);
      if (errorNote) errorNote.hidden = false;
      submitBtn.disabled = false;
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  initNav();
  setCopyrightYear();
  setOfficeHours();
  renderFooterCountries();
  populateCountryDropdown();
  initContactForm();
  initContactLinkTracking();
});
