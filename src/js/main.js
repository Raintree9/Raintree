import { initNav } from "./modules/nav.js";
import { setCopyrightYear } from "./modules/footer.js";

document.addEventListener("DOMContentLoaded", () => {
  initNav();
  setCopyrightYear();
});
