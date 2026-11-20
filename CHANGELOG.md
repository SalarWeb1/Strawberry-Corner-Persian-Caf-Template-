# Changelog

All notable changes to **Strawberry Corner — Persian Café Template**.
Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versioning follows [SemVer](https://semver.org/).

---

## [3.0.0] — 2025-11-20

The biggest release: from a single-page demo to a complete, sellable multi-page product.

### Added
- **30 standalone pages** — home, menu, 10 product pages, shop, events, gallery, articles, 6 article pages, story, contact, login, register, cart, checkout, thank-you, 404.
- **Real multi-page architecture** — every page is its own HTML file with real links (no AJAX view switching).
- **Python build system** — `build.py` renders all pages from shared header/footer partials + `src/data.py`.
- **Custom illustration set** — 10 generated cartoon images (760×760 JPEG + 320×320 thumbs) for drinks, sweets and goods.
- **Flying add-to-cart animation** — the product photo detaches, arcs into the cart icon, and the counter pops.
- **Cart drawer** on every page with quantity steppers, totals and a link to the full cart page.
- **Persistent cart count** — badge on the cart icon everywhere, visible counts in the drawer, cart and checkout pages.
- **Login & register pages** with inline validation, password visibility toggle and a password strength meter.
- **Contact page** with contact cards, validated form and an illustrated map.
- **6 full Persian articles** + reading pages with cover, drop cap, pull quote, author box and reading progress bar.
- **Coupon code** support (`STRAWBERRY` = 10% off).
- **Dark mode** with `localStorage` persistence.
- **Repo tooling** — docs (`docs/`), screenshots, GitHub Actions Pages workflow, issue/PR templates, license, changelog, contributing guide.

### Changed
- New design system (`css/site.css`) — fresh tokens, header, footer, drawers, auth, checkout, responsive scale to 320 px.
- Home hero rebuilt: floating product bubbles, animated stats, feature strip.
- Prices switched from the display font to the body font for legibility.
- Local fonts now include all four Vazirmatn weights plus Gulzar.
- Motion layer rewritten for multi-page: soft page enter/exit, scroll reveals, tilt, magnetic buttons, petals, custom cursor, animated counters.

### Fixed
- SVG sprite definitions (`paperTex`, awning patterns, glow gradient) now ship with every page, so the café building renders correctly everywhere.
- Bunting overlay no longer stretches across the page on the thank-you screen.
- Toast is fully hidden when idle.
- Confetti sits behind the header instead of over it.
- Calendar meta line no longer prints a broken template literal.
- Mobile: home hero no longer pushes the building three screens down; product grid is two columns; no horizontal overflow on any page.

### Removed
- `css/base.css` (v2 leftovers) and unused SVG product symbols superseded by photographs.

---

## [2.0.0] — 2025-11-19

### Added
- GSAP 3.12.5 vendored locally (`js/libs/gsap.min.js`) — works offline and on Iran's national network.
- Intro curtain, page transitions, hero word-by-word animation, falling petals, custom cursor, magnetic buttons, 3D card tilt.
- Gallery and articles views, plus an article reading view.
- Confetti on checkout, reservation stamp, reading progress bar.
- Single-file build (`strawberry-cafe-single.html`) with CSS/JS/fonts inlined.
- Persian README and a portable zip.

### Changed
- Detailed café building illustration, paper texture filter and bunting symbol.
- Mobile header rebuilt; horizontal overflow fixed.

### Fixed
- Jalali calendar replaced `Intl` with the standard algorithm (no more «ناعدد»).
- SVG symbols given explicit `viewBox` so the building no longer renders tiny.
- Empty cart badge hidden; quick-add no longer navigates away.

---

## [1.0.0] — 2025-11-19

### Added
- First version: Persian RTL café front end inspired by the reference video.
- Home, menu, product detail, shop, events, cart, thank-you and story views.
- Local Vazirmatn + Gulzar fonts, SVG illustration sprite, drag-to-rotate product art.
- Jalali calendar, cart with `localStorage`, theme toggle, points and favourites.
