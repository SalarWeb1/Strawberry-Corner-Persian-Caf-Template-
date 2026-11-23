# راهنمای شخصی‌سازی / Customization guide

همه‌ی محتوای سایت از یک فایل می‌آید: `src/data.py`.
بعد از هر تغییر، دو دستور را اجرا کن:

```bash
python3 build.py          # بازسازی ۳۰ صفحه
python3 make_data_js.py   # بازسازی js/data.js
```

---

## ۱) اطلاعات برند و تماس

```python
SITE = {
    'name': 'گوشه توت‌فرنگی',           # نام برند در هدر، فوتر و عنوان صفحه‌ها
    'tagline': 'کافه و چیزهای کوچولو',
    'desc': 'کافه‌ای کوچک در گوشه‌ی شهر…',
    'phone': '۰۲۱ ۸۸۷۷ ۶۶۵۵',
    'phone_link': '+982188776655',      # برای لینک tel:
    'mobile': '۰۹۱۲ ۳۴۵ ۶۷۸۹',
    'address': 'تهران، خیابان کریمخان…',
    'hours': 'هر روز ۸ صبح تا ۱۱ شب',
    'email': 'hello@strawberry-corner.ir',
    'instagram': 'https://instagram.com/…',
    'telegram': 'https://t.me/…',
    'whatsapp': 'https://wa.me/…',
    'designer': 'SalarWeb',             # 👈 نام طراح در نوار پایین فوتر
    'designer_url': 'https://salarweb.ir',
}
```

> این اطلاعات در هدر، فوتر، صفحه‌ی تماس و صفحه‌ی ۴۰۴ استفاده می‌شوند.

---

## ۲) محصولات

```python
PRODUCTS = [
    dict(
        id='latte',                 # یکتا؛ نام فایل می‌شود product-latte.html
        name='لته توت‌فرنگی',
        en='Strawberry Latte',      # نام لاتین (اختیاری، برای سئو)
        cat='drinks',               # drinks | sweets | goods
        img='latte.jpg',            # باید در assets/img/ باشد
        price=45000,                # قیمت پیش‌فرض (اولین سایز)
        old=0,                      # قیمت قبل از تخفیف (۰ = بدون تخفیف)
        badge='پرفروش',             # برچسب گوشه‌ی کارت (خالی = بدون برچسب)
        rating=4.9,
        orders=1240,                # «۱۲۴۰ سفارش تا امروز» در صفحه‌ی محصول
        sub='اسپرسو · سریوپ خانگی · شیر تازه',
        desc='توضیح بلند محصول…',
        tags=['سریوپ خانگی', 'شیر تازه'],
        sizes=[('کوچیک', 39000), ('معمولی', 45000), ('بزرگ', 53000)],
    ),
]
```

نکته‌ها:

- `sizes` همیشه لیست زوج‌های «نام، قیمت» است. اگر یک آیتم فقط یک سایز دارد، همان یک‌تایی را بنویس.
- ترتیب `PRODUCTS` روی صفحه‌ی منو و صفحه‌ی خانه اثر دارد.
- با اضافه کردن یک آیتم، یک صفحه‌ی `product-<id>.html` هم خودکار ساخته می‌شود و در لینک‌ها ظاهر می‌شود.

### تصویر محصول

۱. عکس را با نام دلخواه در `assets/img/` بگذار.
۲. نسخه‌ی کوچک هم بساز (برای کارت‌های ریز):

```python
from PIL import Image
im = Image.open('assets/img/my-drink.png').convert('RGB').resize((760, 760), Image.LANCZOS)
im.save('assets/img/my-drink.jpg', 'JPEG', quality=86, optimize=True)
im.resize((320, 320), Image.LANCZOS).save('assets/img/my-drink-sm.jpg', 'JPEG', quality=80, optimize=True)
```

۳. در `data.py` مقدار `img='my-drink.jpg'` را بگذار.

---

## ۳) مقالات

```python
ARTICLES = [
    dict(slug='latte',                  # product-article: article-latte.html
         title='راز یک لته‌ی خوب: از دانه تا فنجان',
         cat='قهوه',                     # برای فیلتر صفحه‌ی مقالات
         img='cappuccino.jpg',
         date='۱۸ آبان ۱۴۰۵',
         read=4,                         # دقیقه مطالعه
         author='سارا ک.',
         excerpt='خلاصه‌ی مقاله در کارت و بالای صفحه…',
         body=[                          # هر آیتم یک پاراگراف
            'پاراگراف اول…',
            'پاراگراف دوم…',
         ]),
]
```

- مقاله‌ی اول (`ARTICLES[0]`) به‌عنوان مقاله‌ی ویژه‌ی صفحه‌ی مقالات نمایش داده می‌شود.
- `cat` جدید بنویسی، فیلتر خودکار در صفحه‌ی مقالات اضافه می‌شود.

---

## ۴) گالری

```python
GALLERY = [
    ('latte.jpg', 'لته‌ی توت‌فرنگی، همین حالا'),   # (نام فایل، کپشن)
]
```

تعداد قاب‌ها آزاد است؛ گرید خودش جور می‌شود. لایت‌باکس از همین داده ساخته می‌شود.

---

## ۵) رویدادها

```python
EVENTS = [
    dict(icon='e-music',       # یکی از آیکون‌های e-* در src/_keep_sprite.txt
         title='عصر موسیقی زنده',
         wd='پنجشنبه',
         time='۱۹:۳۰',
         desc='توضیح رویداد…',
         seats=12),
]
```

آیکون‌های موجود: `e-music` `e-book` `e-cake` `e-basket` `e-lantern` `e-cup` `e-brush` `e-jar`.

رویدادها روی تقویم به‌صورت چرخشی روی روزها پخش می‌شوند. اگر می‌خواهی رویدادها تاریخ دقیق داشته باشند، تابع `dayHasEvent` در `js/app.js` را ساده کن:

```js
function dayHasEvent(jd) {
  return FIXED_EVENTS[`${cy}-${cm}-${jd}`] || null;   // تاریخ دقیق -> رویداد
}
```

---

## ۶) رنگ‌ها و توکن‌های طراحی

در `css/site.css`، بلوک `:root`:

```css
:root{
  --cream:#FBF3E4;      /* پس‌زمینه */
  --paper:#FFFDF8;      /* کارت‌ها */
  --ink:#3A2A26;        /* متن اصلی */
  --ink-soft:#6B534C;   /* متن دوم */
  --red:#E23E4E;        /* رنگ برند */
  --pink:#F58CA0;
  --green:#2FA08C;
  --yellow:#F7C948;
  --radius:22px;
  --display:'Gulzar';   /* فونت تیترها */
  --body:'Vazirmatn';   /* فونت متن */
}
```

و برای حالت شب، بلوک `[data-theme="dark"]` پایین‌تر از همان فایل.

> اگر فونت تیتر را عوض کردی، `line-height` تیترها را هم چک کن؛ گل‌زار فاصله‌ی بیشتری لازم دارد.

---

## ۷) فونت‌ها

۱. فایل WOFF2 را در `fonts/` بگذار.
۲. در بالای `css/site.css` یک `@font-face` اضافه کن.
۳. در `:root` مقدار `--display` یا `--body` را عوض کن.

---

## ۸) شماره سفارش، هزینه ارسال و تخفیف

در `js/app.js`:

```js
const SHIP = 35000;                       // هزینه ارسال
const code === 'STRAWBERRY'               // کد تخفیف (۱۰٪)
```

و فرمت شماره سفارش:

```js
no: 'SC-1405-' + String(Math.floor(Math.random() * 9000) + 1000)
```

---

## ۹) فرم‌ها و اتصال به بک‌اند

فرم‌های ورود، ثبت‌نام، تماس، خبرنامه و تسویه فقط اعتبارسنجی سمت کلاینت دارند و پیام موفقیت نمایش می‌دهند. برای اتصال واقعی:

- در `build.py` تابع `build_login()`، `build_register()`، `build_contact()` و `build_checkout()` را ببین و به فرم‌ها `action` و `method` بده.
- یا در `js/app.js` در شنونده‌ی `submit`، به‌جای `toast(...)` یک `fetch('/api/…')` بگذار.

---

## ۱۰) افزودن یک صفحه‌ی کاملاً جدید

۱. در `build.py` یک تابع `build_mypage()` بساز که `layout(...)` را برمی‌گرداند:

```python
def build_mypage():
    body = page_head('عنوان', 'تیتر صفحه', 'توضیح کوتاه',
                     [('index.html', 'خانه'), (None, 'صفحه‌ی من')]) + '''
<section class="section tight">
  <div class="wrap">…</div>
</section>
'''
    return layout('صفحه‌ی من', body, active='منو', page='mypage')

write('mypage.html', build_mypage())
```

۲. اگر می‌خواهی در منو بیاید، به لیست `NAV` در بالای `build.py` اضافه کن.
۳. `python3 build.py` بزن. لینک‌ها در هدر، فوتر و منوی موبایل خودکار اضافه می‌شوند.
