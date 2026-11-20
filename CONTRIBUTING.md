# Contributing

Thanks for wanting to improve **Strawberry Corner**. This guide keeps the project consistent.

## Ways to help

- 🐛 Report a bug (use the issue template)
- 💡 Suggest a new page or feature
- 🎨 Improve illustrations or copy
- 🌍 Add an English (LTR) locale
- 📝 Fix documentation or typos

## Ground rules

- **No frameworks, no bundlers.** Plain HTML, CSS and vanilla ES6 only.
- **No external runtime requests.** Everything (fonts, scripts, images) must live inside the repo so the template keeps working offline.
- **Keep RTL first.** Persian is the primary locale; LTR support must be additive.
- **Respect motion preferences.** Anything animated must be disabled under `prefers-reduced-motion` and must survive GSAP being absent.

## Editing pages

Generated pages (`index.html`, `menu.html`, `product-*.html`, …) are **output**. Never edit them directly — your change will be overwritten.

1. Edit data → `src/data.py`
2. Edit layout/partials (header, footer, components) → `build.py`
3. Edit styles → `css/site.css` / `css/motion.css`
4. Edit behaviour → `js/app.js` / `js/motion.js`

Then regenerate:

```bash
python3 build.py
python3 make_data_js.py
```

## Before opening a PR

```bash
node --check js/app.js && node --check js/motion.js && node --check js/data.js
python3 build.py            # must regenerate without errors
```

- Test at 1440 px, 768 px and 390 px widths.
- Check both light and dark themes.
- Confirm the console is free of errors on the pages you touched.
- Keep the diff focused; one feature per PR.

## Commit style

Conventional Commits, e.g.:

```
feat(cart): add coupon field to drawer
fix(calendar): correct month length for Esfand
docs(readme): add Persian quick start
style(site): tighten product card spacing
```

## Code style

- 2-space indentation (4 for Python), UTF-8, LF line endings (see `.editorconfig`).
- CSS: one selector per line group, custom properties for tokens, mobile-first media queries at the end of the file.
- JS: `const`/`let`, small pure helpers, no globals other than the `window.DATA` / `window.SC` bridges.
- Comments in Persian or English are both fine.

## Reporting a bug

Include: page URL/file, browser + version, steps to reproduce, expected vs actual, and a screenshot if possible.

By contributing you agree to follow the [Code of Conduct](./CODE_OF_CONDUCT.md).
