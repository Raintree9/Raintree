import { initNav } from "../modules/nav.js";
import { setCopyrightYear } from "../modules/footer.js";
import { renderFooterCountries } from "../modules/footer-countries.js";

const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const PHONE_PATTERN = /^[0-9+\-\s()]{7,}$/;

function showFieldError(field, message) {
  field.setAttribute("data-touched", "true");
  field.setCustomValidity(message ?? "");
  const errorEl = document.getElementById(`${field.id}-error`);
  if (errorEl) errorEl.textContent = message ?? "";
}

function validateField(field) {
  if (field.validity.valueMissing) {
    showFieldError(field, "This field is required.");
    return false;
  }
  if (field.type === "email" && !EMAIL_PATTERN.test(field.value)) {
    showFieldError(field, "Enter a valid email address.");
    return false;
  }
  if (field.id === "phone" && !PHONE_PATTERN.test(field.value)) {
    showFieldError(field, "Enter a valid phone number.");
    return false;
  }
  showFieldError(field, "");
  return true;
}

/**
 * This is a client-side-only form: it validates input and shows a success
 * state, but nothing is actually transmitted anywhere yet. Wire the fetch
 * call below up to a real endpoint (form backend, serverless function, or
 * email API) before relying on this to deliver messages.
 */
function initContactForm() {
  const form = document.querySelector("[data-contact-form]");
  if (!form) return;

  const fields = [...form.querySelectorAll("input[required], select[required], textarea[required]")];

  fields.forEach((field) => {
    field.addEventListener("blur", () => validateField(field));
  });

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const allValid = fields.map(validateField).every(Boolean);
    if (!allValid) {
      fields.find((f) => !validateField(f))?.focus();
      return;
    }

    form.hidden = true;
    const success = document.querySelector("[data-form-success]");
    if (success) {
      success.hidden = false;
      success.focus();
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  initNav();
  setCopyrightYear();
  renderFooterCountries();
  initContactForm();
});
