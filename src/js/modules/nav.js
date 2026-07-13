/**
 * Site header behavior: mobile nav toggle, scroll shadow, and
 * Escape/outside-click dismissal. Expects the header markup produced by
 * src/css/components/header.css.
 */
export function initNav() {
  const header = document.querySelector(".site-header");
  const toggle = document.querySelector(".nav-toggle");
  const nav = document.querySelector(".main-nav");

  if (!header || !toggle || !nav) return;

  const closeNav = () => {
    toggle.setAttribute("aria-expanded", "false");
    nav.classList.remove("is-open");
    document.body.classList.remove("nav-open");
  };

  const openNav = () => {
    toggle.setAttribute("aria-expanded", "true");
    nav.classList.add("is-open");
    document.body.classList.add("nav-open");
  };

  toggle.addEventListener("click", () => {
    const isOpen = toggle.getAttribute("aria-expanded") === "true";
    isOpen ? closeNav() : openNav();
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
      closeNav();
      toggle.focus();
    }
  });

  nav.querySelectorAll(".main-nav__link").forEach((link) => {
    link.addEventListener("click", () => {
      if (window.matchMedia("(max-width: 1023px)").matches) closeNav();
    });
  });

  document.addEventListener("click", (event) => {
    if (!header.contains(event.target)) closeNav();
  });

  const onScroll = () => {
    header.classList.toggle("is-scrolled", window.scrollY > 8);
  };
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });
}
