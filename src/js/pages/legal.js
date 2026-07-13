import { initNav } from "../modules/nav.js";
import { setCopyrightYear } from "../modules/footer.js";
import { renderFooterCountries } from "../modules/footer-countries.js";

document.addEventListener("DOMContentLoaded", () => {
  initNav();
  setCopyrightYear();
  renderFooterCountries();
});
