# انتشار / Deployment

قالب کاملاً استاتیک است؛ هر جایی که HTML سرو کند کار می‌کند. نیازی به Node، PHP یا دیتابیس نیست.

## ۱) GitHub Pages (پیشنهادی)

ورک‌فلوی آماده در `.github/workflows/pages.yml` هست.

1. ریپو را روی GitHub بفرست.
2. **Settings → Pages → Source** را روی **GitHub Actions** بگذار.
3. هر push روی `main` سایت را منتشر می‌کند.
4. آدرس نهایی: `https://<username>.github.io/strawberry-corner-cafe/`

> همه‌ی مسیرها نسبی هستند، پس زیرپوشه (`/repo-name/`) هم درست کار می‌کند.

## ۲) Netlify / Vercel / Cloudflare Pages

| تنظیم | مقدار |
|---|---|
| Build command | خالی (یا `python3 build.py` اگر می‌خواهی در سرور بیلد شود) |
| Output / publish directory | `/` (ریشه‌ی ریپو) |
| Framework preset | None |

## ۳) هاست اشتراکی ایرانی (cPanel / DirectAdmin)

1. کل پوشه را داخل `public_html` آپلود کن (ZIP → Extract).
2. مطمئن شو `index.html` در ریشه است.
3. اگر خطای ۴۰۴ می‌خواهی سفارشی باشد، در `.htaccess`:

```apache
ErrorDocument 404 /404.html
```

## ۴) اجرای محلی

```bash
python3 -m http.server 8000
# یا
npx serve .
```

## نکته‌های انتشار

- **دامنه و سئو:** در همه‌ی صفحه‌ها `<title>` و `<meta name="description">` از `build.py` ساخته می‌شوند؛ اگر دامنه‌ی نهایی را داری، می‌توانی تگ `canonical` و `og:` را هم به `layout()` اضافه کنی.
- **کش:** فونت‌ها و تصاویر تغییر نمی‌کنند؛ در هاست اشتراکی `expires` طولانی بده.
- **فشرده‌سازی:** gzip/brotli روی HTML و CSS تفاوت محسوسی می‌دهد (فایل CSS حدود ۳۸ کیلوبایت است).
- **فرم‌ها:** برای فرم‌های واقعی، یا به یک سرویس فرم متصل کن یا به بک‌اند خودت (بخش ۹ در `docs/CUSTOMIZATION.md`).
- **HTTPS:** برای `localStorage` و درگاه پرداخت لازم است.

## چک‌لیست پیش از تحویل

- [ ] نام برند، تلفن و نشانی واقعی مشتری جای‌گذاری شده
- [ ] `SITE['designer']` روی نام تو تنظیم است
- [ ] محصولات و قیمت‌ها به‌روزند (`python3 build.py && python3 make_data_js.py`)
- [ ] تصاویر مشتری در `assets/img/` با نسبت ۱:۱
- [ ] لینک‌های شبکه‌های اجتماعی
- [ ] تست موبایل واقعی (iOS Safari) و دسکتاپ
- [ ] `404.html` کار می‌کند
