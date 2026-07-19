import { initNav } from "../modules/nav.js";
import { setCopyrightYear } from "../modules/footer.js";
import { getCountries } from "../modules/data-service.js";
import { renderFooterCountries } from "../modules/footer-countries.js";
import { destinationCardMarkup } from "../modules/destination-card.js";

function byFeaturedOrder(a, b) {
  return (a.featuredOrder ?? 0) - (b.featuredOrder ?? 0);
}

// Client quotes are editorial copy, not visa data, so they live here —
// but each quote's country flag is looked up from countries.json rather
// than re-typed, since that data already exists in one place.
const TESTIMONIALS = [
  {
    quote: "Excellent service! They guided me through the entire process.",
    name: "Rohit Sharma",
    countryId: "canada",
    photoId: "rohit-sharma",
  },
  {
    quote: "Very professional and transparent. Their team is always supportive.",
    name: "Priya Nair",
    countryId: "australia",
    photoId: "priya-nair",
  },
  {
    quote: "Thanks to Raintree, my Japan trip was smooth and memorable.",
    name: "Vikram Raj",
    countryId: "japan",
    photoId: "vikram-raj",
  },
];

function initials(fullName) {
  return fullName
    .split(" ")
    .map((part) => part[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();
}

function avatarMarkup(testimonial) {
  if (!testimonial.photoId) {
    // Fallback for a future testimonial added before a real photo exists —
    // never substitute a stock photo for a named person (see docs/Production-Image-Guide.md).
    return `<span class="testimonial-card__avatar testimonial-card__avatar--initials" aria-hidden="true">${initials(testimonial.name)}</span>`;
  }

  const base = `assets/images/testimonials/${testimonial.photoId}`;
  return `
    <picture>
      <source type="image/webp" srcset="${base}-128.webp 1x, ${base}-256.webp 2x" />
      <img
        class="testimonial-card__avatar"
        src="${base}-128.jpg"
        srcset="${base}-128.jpg 1x, ${base}-256.jpg 2x"
        width="64"
        height="64"
        alt=""
        loading="lazy"
        decoding="async"
      />
    </picture>
  `;
}

function starsMarkup() {
  return Array.from({ length: 5 })
    .map(() => `<svg width="16" height="16"><use href="assets/icons/sprite.svg#icon-star"></use></svg>`)
    .join("");
}

function testimonialCardMarkup(testimonial, country) {
  return `
    <li>
      <article class="card testimonial-card">
        <div class="testimonial-card__stars">
          <span class="visually-hidden">Rated 5 out of 5 stars</span>
          <span aria-hidden="true">${starsMarkup()}</span>
        </div>
        <p class="testimonial-card__quote">&ldquo;${testimonial.quote}&rdquo;</p>
        <div class="testimonial-card__author">
          ${avatarMarkup(testimonial)}
          <div>
            <p class="testimonial-card__name">${testimonial.name}</p>
            <p class="testimonial-card__origin">
              <span aria-hidden="true">${country?.flag ?? ""}</span>
              <span>${country?.country ?? ""}</span>
            </p>
          </div>
        </div>
      </article>
    </li>
  `;
}

async function renderFeaturedDestinations() {
  const grid = document.querySelector("[data-destinations-grid]");
  if (!grid) return;

  try {
    const countries = await getCountries();
    const featured = countries.filter((c) => c.featured).sort(byFeaturedOrder);
    grid.innerHTML = featured.length
      ? featured.map(destinationCardMarkup).join("")
      : `<li class="data-error">No featured destinations are configured yet.</li>`;
  } catch (error) {
    console.error("Failed to load destinations:", error);
    grid.innerHTML = `<li class="data-error">We couldn't load destinations right now. Please refresh or check back shortly.</li>`;
  }
}

async function renderTestimonials() {
  const track = document.querySelector("[data-testimonial-track]");
  if (!track) return;

  try {
    const countries = await getCountries();
    const byId = new Map(countries.map((c) => [c.id, c]));
    track.innerHTML = TESTIMONIALS.map((t) => testimonialCardMarkup(t, byId.get(t.countryId))).join("");
  } catch (error) {
    console.error("Failed to load testimonials:", error);
    track.innerHTML = `<li class="data-error">We couldn't load client stories right now.</li>`;
  }
}

function initTestimonialCarousel() {
  const track = document.querySelector("[data-testimonial-track]");
  const prevBtn = document.querySelector("[data-testimonial-prev]");
  const nextBtn = document.querySelector("[data-testimonial-next]");
  if (!track || !prevBtn || !nextBtn) return;

  const step = () => (track.querySelector("li")?.offsetWidth ?? 320) + 24;

  prevBtn.addEventListener("click", () => {
    track.scrollBy({ left: -step(), behavior: "smooth" });
  });
  nextBtn.addEventListener("click", () => {
    track.scrollBy({ left: step(), behavior: "smooth" });
  });
}

function initHeroSlideshow() {
  const root = document.querySelector("[data-hero-slideshow]");
  if (!root) return;

  const slides = Array.from(root.querySelectorAll("[data-slide]"));
  const dots = Array.from(root.querySelectorAll("[data-slide-dot]"));
  if (slides.length < 2) return;

  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  let index = 0;
  let timer = null;

  function show(nextIndex) {
    slides[index].classList.remove("is-active");
    dots[index]?.classList.remove("is-active");
    dots[index]?.setAttribute("aria-selected", "false");

    index = nextIndex;

    slides[index].classList.add("is-active");
    dots[index]?.classList.add("is-active");
    dots[index]?.setAttribute("aria-selected", "true");
  }

  function stop() {
    if (timer) clearInterval(timer);
    timer = null;
  }

  function start() {
    stop();
    if (reduceMotion || document.hidden) return;
    timer = setInterval(() => show((index + 1) % slides.length), 5000);
  }

  dots.forEach((dot, dotIndex) => {
    dot.addEventListener("click", () => {
      show(dotIndex);
      start();
    });
  });

  root.addEventListener("mouseenter", stop);
  root.addEventListener("mouseleave", start);
  root.addEventListener("focusin", stop);
  root.addEventListener("focusout", start);
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) stop();
    else start();
  });

  start();
}

document.addEventListener("DOMContentLoaded", () => {
  initNav();
  setCopyrightYear();
  initHeroSlideshow();
  initTestimonialCarousel();
  renderFeaturedDestinations();
  renderTestimonials();
  renderFooterCountries();
});
