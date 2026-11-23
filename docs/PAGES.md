# صفحات و نقشه‌ی سایت / Pages map

## نقشه‌ی لینک‌ها

```
index.html
├── menu.html
│   └── product-<id>.html  ×10
│       └── (سایر محصولات / سبد)
├── shop.html
│   └── product-jam.html · product-mug.html · product-tote.html
├── events.html        (رزرو در همان صفحه)
├── gallery.html       (+ لایت‌باکس)
├── articles.html
│   └── article-<slug>.html  ×6
├── story.html
├── contact.html
├── login.html ⇄ register.html
├── bag.html → checkout.html → thanks.html
└── 404.html
```

## جدول کامل

| صفحه | فایل | `data-page` | اسکریپت اختصاصی |
|---|---|---|---|
| خانه | `index.html` | `home` | `motion.js` (هیرو، شمارنده، شناوری) |
| منو | `menu.html` | `menu` | `initMenuFilters()` |
| محصول | `product-*.html` | `product` | `initProductPage()` |
| فروشگاه | `shop.html` | `shop` | — |
| رویدادها | `events.html` | `events` | `initCalendar()` |
| گالری | `gallery.html` | `gallery` | `initGallery()` |
| مقالات | `articles.html` | `articles` | `initArticleFilters()` |
| مقاله | `article-*.html` | `article` | `initReadbar()` |
| داستان | `story.html` | `story` | ریویل اسکرول |
| تماس | `contact.html` | `contact` | `initForms()` |
| ورود | `login.html` | `login` | `initForms()` |
| ثبت‌نام | `register.html` | `register` | `initForms()` + قدرت رمز |
| سبد | `bag.html` | `bag` | `initBagPage()` |
| تسویه | `checkout.html` | `checkout` | `initCheckout()` |
| تشکر | `thanks.html` | `thanks` | `initThanks()` |
| ۴۰۴ | `404.html` | `404` | — |

## اجزای مشترک (در `build.py`)

| تابع | خروجی |
|---|---|
| `layout()` | کل سند HTML: `<head>`، هدر، `<main>`، فوتر، کشوی سبد، توست، اسکریپت‌ها |
| `header(active)` | هدر چسبان + ناوبری دسکتاپ + منوی موبایل + دکمه‌های تم/حساب/سبد |
| `footer()` | فوتر چهارستونه + خبرنامه + نوار پایین با «طراحی شده توسط SalarWeb» |
| `CART_DRAWER` | کشوی سبد مشترک همه‌ی صفحه‌ها |
| `product_card(p)` | کارت محصول با عکس، امتیاز، قیمت و دکمه‌ی افزودن |
| `article_card(a)` | کارت مقاله |
| `page_head(...)` | سربرگ صفحه‌ها + breadcrumb |
| `svg(icon, cls)` | درج آیکون از sprite با `viewBox` درست |

## کلاس‌های مهم CSS

| خانواده | نمونه |
|---|---|
| چیدمان | `.wrap` `.section` `.section-alt` `.cards-grid` `.hero-grid` `.split-grid` |
| کارت | `.card` `.ph-card` `.art-card` `.quote-card` `.contact-card` |
| دکمه | `.btn` `.btn-red` `.btn-ghost` `.btn-lg` `.btn-block` `.link-arrow` `.add-btn` |
| فرم | `.field` `.field-row` `.field-err` `.check` `.pass-meter` |
| سبد | `.cart-drawer` `.d-item` `.bag-item` `.sum-row` `.sum-total` |
| تقویم | `.calendar-card` `.cal-grid` `.cal-cell` `.event-card` `.stamp` |
| تیتر | `.page-title` `.hero-title` `.section-head` `.kicker` `.p-name` |
