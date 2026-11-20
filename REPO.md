# مشخصات ریپازیتوری / Repository setup

این فایل برای توست (نه برای مشتری). هرچه لازم داری تا ریپو را روی GitHub بسازی و حرفه‌ای دیده شود، همین‌جاست.

---

## نام‌ها

| مورد | مقدار پیشنهادی |
|---|---|
| **نام کامل (اسم محصول)** | **Strawberry Corner — Persian Café Template** / **گوشه توت‌فرنگی — قالب کافه‌ی فارسی** |
| **نام ریپازیتوری (slug)** | `strawberry-corner-cafe` |
| نام جایگزین | `strawberry-corner-persian-cafe` · `goushe-totfarangi` · `cafe-template-fa` |
| **توضیح کوتاه (Description)** | `A complete 30-page Persian (RTL) café template — HTML/CSS/JS, GSAP animations, Jalali calendar, offline-ready. قالب کافه‌ی فارسی` |
| **Website** | آدرس دموی زنده (مثلاً `https://salarweb.ir/demo/strawberry-corner`) |
| **Topics** | `html5` `css3` `javascript` `vanilla-js` `gsap` `rtl` `persian` `farsi` `cafe` `coffee-shop` `restaurant-template` `ecommerce` `static-site` `offline-first` `jalali-calendar` `multipage` `frontend-template` `design-system` `template` |
| **Default branch** | `main` |
| **Social preview** | `docs/screenshots/social-preview.jpg` (1280×640) |

> در GitHub: **Settings → General → Description / Topics**، و در **Settings → Social preview** تصویر بالا را آپلود کن.

---

## ساخت ریپو از همین پوشه

```bash
cd strawberry-corner-cafe

git init -b main
git add .
git commit -m "feat: Strawberry Corner v3 — 30-page Persian café template"

# ریپوی خالی روی GitHub بساز (بدون README/بونس) و بعد:
git remote add origin https://github.com/<username>/strawberry-corner-cafe.git
git push -u origin main
```

### کامیت‌های پیشنهادی برای تاریخچه‌ی تمیز

اگر می‌خواهی تاریخچه‌ی مرحله‌به‌مرحله داشته باشی (به‌جای یک کامیت بزرگ):

```bash
git commit -m "chore: project scaffold, fonts and GSAP vendored"
git commit -m "feat(design): design system, tokens and base layout"
git commit -m "feat(data): products, articles, gallery and events data + build script"
git commit -m "feat(pages): home, menu, product, shop"
git commit -m "feat(pages): events, gallery, articles, story, contact"
git commit -m "feat(pages): auth, cart, checkout, thank-you, 404"
git commit -m "feat(cart): localStorage cart, drawer, flying add-to-cart, coupon"
git commit -m "feat(motion): GSAP transitions, reveals, tilt, confetti"
git commit -m "docs: readme (fa/en), customization and deploy guides, screenshots"
```

---

## ریلیز

در GitHub → **Releases → Draft a new release**:

- Tag: `v3.0.0`
- Title: `v3.0.0 — Strawberry Corner`
- فایل ضمیمه: `strawberry-corner-cafe-v3.0.0.zip` (همین پوشه، زیپ‌شده)
- توضیحات: بخش «۳.۰.۰» را از [`CHANGELOG.md`](./CHANGELOG.md) کپی کن.

---

## چک‌لیست قبل از انتشار ریپو

- [ ] لینک دمو در بخش Website و در بالای README اضافه شده
- [ ] `SITE['designer']` و `designer_url` روی نام خودت تنظیم است
- [ ] شماره تلفن، نشانی و ایمیل واقعی (یا نمونه‌ی واضح) در `src/data.py`
- [ ] `LICENSE` را خوانده و تایید کرده‌ای (پایین را ببین)
- [ ] اسکرین‌شات‌های `docs/screenshots/` مال نسخه‌ی نهایی‌اند
- [ ] `python3 build.py && python3 make_data_js.py` بعد از آخرین تغییر داده اجرا شده
- [ ] ریپو Public است و Topics پر شده
- [ ] GitHub Pages روشن است (Settings → Pages → Source: GitHub Actions)

---

## License note

فایل `LICENSE` روی **MIT** است: استفاده‌ی شخصی و تجاری آزاد، با حفظ نام نویسنده.

اگر می‌خواهی این قالب را **به‌عنوان محصول بفروشی**، دو گزینه داری:

1. **همان MIT بماند** (محبوب‌ترین حالت برای قالب‌های متن‌باز؛ خریدارها بیشتر اعتماد می‌کنند).
2. **مجوز تجاری اختصاصی** بگذاری. در این حالت `LICENSE` را با متن زیر عوض کن:

```
Copyright (c) 2025 SalarWeb

This template is sold as a commercial product.
- You MAY use it in unlimited personal and client projects after purchase.
- You MAY modify it freely for those projects.
- You MAY NOT redistribute, resell or publish the source code,
  modified or unmodified, as a template, theme or starter kit.
```

> بگو کدام را می‌خواهی، همان را جایگزین می‌کنم.

---

## متن پیشنهادی برای معرفی (کپی/پیست)

**فارسی (توییتر/لینکدین/اینستاگرام):**

> 🍓 «گوشه توت‌فرنگی» — قالب کافه‌ی فارسی، ۳۰ صفحه‌ی کامل
> HTML/CSS/JS خالص · بدون فریم‌ورک · کاملاً آفلاین (مناسب شرایط نت)
> تقویم شمسی، سبد خرید، پرواز محصول به سبد، انیمیشن‌های GSAP، حالت شب
> مناسب کافه، قنادی، رستوران و فروشگاه کوچک
> طراحی و توسعه: SalarWeb

**English (Dev.to / X / Dribbble):**

> 🍓 **Strawberry Corner** — a 30-page Persian (RTL) café template built with plain HTML, CSS and vanilla JS. Local GSAP, self-hosted fonts, real Jalali calendar, working cart flow with a flying add-to-cart animation. No CDN, no build step, works fully offline.
