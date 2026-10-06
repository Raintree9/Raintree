import { initNav } from "../modules/nav.js";
import { setCopyrightYear, setOfficeHours } from "../modules/footer.js";
import { renderFooterCountries } from "../modules/footer-countries.js";
import { initContactLinkTracking } from "../modules/pixel.js";

document.addEventListener("DOMContentLoaded", () => {
  initNav();
  setCopyrightYear();
  setOfficeHours();
  renderFooterCountries();
  initContactLinkTracking();
});
