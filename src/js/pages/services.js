import { initNav } from "../modules/nav.js";
import { setCopyrightYear, setOfficeHours } from "../modules/footer.js";
import { renderFooterCountries } from "../modules/footer-countries.js";
import { initContactLinkTracking, trackViewContent } from "../modules/pixel.js";

document.addEventListener("DOMContentLoaded", () => {
  initNav();
  setCopyrightYear();
  setOfficeHours();
  renderFooterCountries();
  initContactLinkTracking();

  // This page covers both visa types at once (not one destination like
  // country-detail.html), so each section fires its own ViewContent rather
  // than picking one.
  if (document.getElementById("visitor-visa-heading")) {
    trackViewContent({ content_name: "Visitor Visa", content_category: "visitor" });
  }
  if (document.getElementById("work-permit-heading")) {
    trackViewContent({ content_name: "Work Permit", content_category: "work-permit-docs" });
  }
});
