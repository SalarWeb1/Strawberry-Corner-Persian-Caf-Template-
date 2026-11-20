# -*- coding: utf-8 -*-
"""
سازنده‌ی قالب «گوشه توت‌فرنگی» — نسخه ۳
همه‌ی صفحه‌ها را از قالب مشترک (هدر/فوتر/کشوی سبد) می‌سازد تا لینک‌ها و ساختار یکدست بمانند.
اجرا:  python3 build.py
"""
import io, os, re, html, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))
from data import SITE, PRODUCTS, ARTICLES, GALLERY, EVENTS, CATS

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)

# ---------------------------------------------------------------- sprite
with io.open('src/_keep_sprite.txt', encoding='utf-8') as f:
    SPRITE_KEPT = f.read()
with io.open('src/_defs.txt', encoding='utf-8') as f:
    SPRITE_DEFS = f.read()

EXTRA_ICONS = {
 'i-menu': '<path d="M4 7h16M4 12h16M4 17h16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
 'i-close': '<path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
 'i-search': '<circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" stroke-width="2"/><path d="M16.5 16.5L21 21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
 'i-mail': '<rect x="3" y="5" width="18" height="14" rx="3" fill="none" stroke="currentColor" stroke-width="2"/><path d="M4 7l8 6 8-6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
 'i-phone': '<path d="M7 3h3l2 5-2.5 1.5a12 12 0 0 0 5 5L16 12l5 2v3a2 2 0 0 1-2.2 2A17 17 0 0 1 5 5.2 2 2 0 0 1 7 3z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>',
 'i-pin': '<path d="M12 21s7-6.3 7-11a7 7 0 1 0-14 0c0 4.7 7 11 7 11z" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="10" r="2.5" fill="none" stroke="currentColor" stroke-width="2"/>',
 'i-clock': '<circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 7v5.5l3.5 2" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
 'i-star': '<path d="M12 3.5l2.6 5.3 5.9.9-4.3 4.1 1 5.8-5.2-2.8-5.2 2.8 1-5.8L3.5 9.7l5.9-.9z" fill="currentColor"/>',
 'i-eye': '<path d="M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12z" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="3" fill="none" stroke="currentColor" stroke-width="2"/>',
 'i-lock': '<rect x="4.5" y="10" width="15" height="10" rx="3" fill="none" stroke="currentColor" stroke-width="2"/><path d="M8 10V7.5a4 4 0 0 1 8 0V10" fill="none" stroke="currentColor" stroke-width="2"/>',
 'i-instagram': '<rect x="3.5" y="3.5" width="17" height="17" rx="5" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="17" cy="7" r="1.3" fill="currentColor"/>',
 'i-telegram': '<path d="M21 4L2.5 11.2l5 1.7L19 6.4 9.6 14.5l-.3 5 2.6-2.6 4.2 2.8L21 4z" fill="currentColor"/>',
 'i-whatsapp': '<path d="M12 3a9 9 0 0 0-7.7 13.6L3 21l4.5-1.2A9 9 0 1 0 12 3zm4.4 12.2c-.2.6-1.2 1.1-1.7 1.1-.5 0-1.9-.4-3.6-2s-2-2.9-2-3.4c0-.5.4-1.5 1-1.7.3-.1.6 0 .8.3l.7 1.3c.1.2 0 .4-.1.6l-.5.6c.4.8 1.3 1.7 2.1 2l.6-.5c.2-.2.4-.2.6-.1l1.3.7c.2.1.3.5.3.9z" fill="currentColor"/>',
 'i-arrow-l': '<path d="M14 6l-6 6 6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
 'i-plus-c': '<circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 8v8M8 12h8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
 'i-truck': '<path d="M2 7h10v9H2zM12 10h4l3 3v3h-7z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><circle cx="6" cy="18" r="1.8" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="16.5" cy="18" r="1.8" fill="none" stroke="currentColor" stroke-width="2"/>',
 'i-shield': '<path d="M12 3l7 3v5.5c0 4.3-3 7.7-7 9.5-4-1.8-7-5.2-7-9.5V6z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M8.8 12l2.2 2.2 4.2-4.4" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
 'i-leaf': '<path d="M20 4C10 4 4 9 4 16c0 2 1 4 1 4s2-9 15-9c0 0-3 6-9 8" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
 'i-gift2': '<rect x="3" y="9" width="18" height="11" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><path d="M3 13h18M12 9v11M12 9c-3 0-4.5-1-4.5-2.5S9 4.5 12 9zm0 0c3 0 4.5-1 4.5-2.5S15 4.5 12 9z" fill="none" stroke="currentColor" stroke-width="2"/>',
}
EXTRA_SPRITE = '\n'.join(
    f'<symbol id="{k}" viewBox="0 0 24 24">{v}</symbol>' for k, v in EXTRA_ICONS.items()
)
SPRITE = '<svg xmlns="http://www.w3.org/2000/svg" style="display:none" aria-hidden="true">\n' + SPRITE_DEFS + '\n' + SPRITE_KEPT + '\n' + EXTRA_SPRITE + '\n</svg>'

BOXES = {'building':'0 0 440 500','bunting':'0 0 440 500','strawberry':'0 0 64 64','sprig':'0 0 48 24'}
def svg(icon, cls=''):
    box = BOXES.get(icon, '0 0 24 24')
    return f'<svg class="{cls}" viewBox="{box}" aria-hidden="true"><use href="#{icon}"/></svg>'

# ---------------------------------------------------------------- helpers
def money(n):
    return fa(n) + ' تومان'

def fa(n):
    s = str(n)
    trans = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')
    out = ''
    for i, ch in enumerate(reversed(s)):
        if i and i % 3 == 0 and ch.isdigit():
            out += '٬'
        out += ch.translate(trans)
    return out[::-1]

NAV = [
    ('index.html', 'خانه', 'خانه'),
    ('menu.html', 'منو', 'منو'),
    ('shop.html', 'فروشگاه', 'فروشگاه'),
    ('events.html', 'رویدادها', 'رویدادها'),
    ('gallery.html', 'گالری', 'گالری'),
    ('articles.html', 'مقالات', 'مقالات'),
    ('story.html', 'داستان ما', 'داستان ما'),
    ('contact.html', 'تماس', 'تماس'),
]

# ---------------------------------------------------------------- layout
def header(active):
    links = ''.join(
        f'<a href="{href}"{" class=\"active\"" if key == active else ""}>{label}</a>'
        for href, label, key in NAV
    )
    mob = ''.join(
        f'<a href="{href}"{" class=\"active\"" if key == active else ""}><span>{label}</span>{svg("i-arrow-l")}</a>'
        for href, label, key in NAV
    )
    return f'''
<header class="site-header" id="site-header">
  <div class="header-inner">
    <a class="brand" href="index.html" aria-label="{SITE['name']}">
      {svg('strawberry', 'brand-art')}
      <span class="brand-text">
        <span class="brand-name">{SITE['name']}</span>
        <span class="brand-sub">{SITE['tagline']}</span>
      </span>
    </a>

    <nav class="main-nav" id="main-nav" aria-label="منوی اصلی">{links}</nav>

    <div class="header-actions">
      <button class="icon-btn" id="theme-btn" aria-label="حالت شب / روز" title="حالت شب کافه">{svg('i-moon')}</button>
      <a class="icon-btn" href="login.html" aria-label="ورود و ثبت‌نام" title="حساب من">{svg('i-user')}</a>
      <button class="icon-btn cart-btn" id="cart-btn" aria-label="سبد خرید" title="سبد خرید">
        {svg('i-bag')}
        <em class="count-badge" id="cart-count">۰</em>
      </button>
      <button class="icon-btn burger" id="burger" aria-label="منو" aria-expanded="false">{svg('i-menu')}</button>
    </div>
  </div>
  <div class="mobile-nav" id="mobile-nav">{mob}</div>
</header>'''

def footer():
    nav_links = ''.join(f'<li><a href="{href}">{label}</a></li>' for href, label, _ in NAV)
    cats = ''.join(
        f'<li><a href="menu.html#{cid}">{name}</a></li>' for cid, name in CATS.items()
    )
    return f'''
<footer class="site-footer">
  <div class="footer-inner">
    <div class="footer-brand">
      <a class="brand" href="index.html">
        {svg('strawberry', 'brand-art')}
        <span class="brand-text">
          <span class="brand-name">{SITE['name']}</span>
          <span class="brand-sub">{SITE['tagline']}</span>
        </span>
      </a>
      <p>{SITE['desc']}</p>
      <div class="socials">
        <a href="{SITE['instagram']}" aria-label="اینستاگرام" target="_blank" rel="noopener">{svg('i-instagram')}</a>
        <a href="{SITE['telegram']}" aria-label="تلگرام" target="_blank" rel="noopener">{svg('i-telegram')}</a>
        <a href="{SITE['whatsapp']}" aria-label="واتساپ" target="_blank" rel="noopener">{svg('i-whatsapp')}</a>
      </div>
    </div>

    <div class="footer-col">
      <h4>دسترسی سریع</h4>
      <ul>{nav_links}</ul>
    </div>

    <div class="footer-col">
      <h4>دسته‌بندی‌ها</h4>
      <ul>{cats}
        <li><a href="articles.html">مقالات قهوه</a></li>
        <li><a href="events.html">رویدادها</a></li>
      </ul>
    </div>

    <div class="footer-col footer-contact">
      <h4>تماس با ما</h4>
      <ul class="contact-list">
        <li>{svg('i-pin')}<span>{SITE['address']}</span></li>
        <li>{svg('i-phone')}<a href="tel:{SITE['phone_link']}" dir="ltr">{SITE['phone']}</a></li>
        <li>{svg('i-mail')}<a href="mailto:{SITE['email']}" dir="ltr">{SITE['email']}</a></li>
        <li>{svg('i-clock')}<span>{SITE['hours']}</span></li>
      </ul>
      <form class="newsletter" data-newsletter>
        <input type="email" name="email" placeholder="ایمیل برای خبرنامه" required aria-label="ایمیل خبرنامه">
        <button type="submit" class="btn btn-red">{svg('i-arrow')}<span>عضویت</span></button>
      </form>
    </div>
  </div>

  <div class="footer-bottom">
    <p>© ۱۴۰۴ {SITE['name']} · تمامی حقوق محفوظ است.</p>
    <p class="designer">طراحی شده توسط <a href="{SITE['designer_url']}" target="_blank" rel="noopener"><b>{SITE['designer']}</b></a></p>
  </div>
</footer>'''

CART_DRAWER = f'''
<div class="drawer-overlay" id="drawer-overlay" hidden></div>
<aside class="cart-drawer" id="cart-drawer" aria-hidden="true" aria-label="سبد خرید">
  <header class="drawer-head">
    <h3>سبد کوچولوی تو <span class="drawer-count" id="drawer-count">۰ خوراکی</span></h3>
    <button class="icon-btn" id="drawer-close" aria-label="بستن">{svg('i-close')}</button>
  </header>
  <div class="drawer-body" id="drawer-body"></div>
  <footer class="drawer-foot">
    <div class="drawer-total"><span>مجموع</span><b id="drawer-total">۰ تومان</b></div>
    <a class="btn btn-red btn-block" href="bag.html">مشاهده سبد و تسویه {svg('i-arrow')}</a>
    <button class="btn btn-ghost btn-block" id="drawer-continue">ادامه‌ی خرید</button>
  </footer>
</aside>'''

def layout(title, body, active='', desc=None, page='page', body_class=''):
    desc = desc or SITE['desc']
    return f'''<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | {SITE['name']}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#FBF3E4">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'><path d='M32 12C20 12 12 21 12 32c0 14 12 24 20 26 8-2 20-12 20-26 0-11-8-20-20-20z' fill='%23E23E4E'/><path d='M32 12c-3-4-8-5-12-3 2 3 5 4 8 4-4 0-8 2-10 5 4 1 8 0 11-2-1 3 0 6 3 8 3-2 4-5 3-8 3 2 7 3 11 2-2-3-6-5-10-5 3 0 6-1 8-4-4-2-9-1-12 3z' fill='%233E9B4F'/></svg>">
<link rel="stylesheet" href="css/site.css">
<link rel="stylesheet" href="css/motion.css">
</head>
<body data-page="{page}" class="{body_class}">
{SPRITE}
{header(active)}
<main id="main">
{body}
</main>
{footer()}
{CART_DRAWER}
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<button class="to-top" id="to-top" aria-label="بالا">{svg('i-arrow')}</button>
<script src="js/libs/gsap.min.js"></script>
<script src="js/data.js"></script>
<script src="js/app.js"></script>
<script src="js/motion.js"></script>
</body>
</html>'''

# ---------------------------------------------------------------- components
def product_card(p, cls=''):
    old = f'<s>{money(p["old"])}</s>' if p['old'] else ''
    badge = f'<span class="p-badge">{p["badge"]}</span>' if p['badge'] else ''
    return f'''
<article class="ph-card {cls}" data-cat="{p['cat']}">
  {badge}
  <a class="ph-media" href="product-{p['id']}.html" aria-label="{p['name']}">
    <img src="assets/img/{p['img']}" alt="{p['name']}" width="760" height="760" loading="lazy">
    <span class="ph-view">مشاهده {svg('i-arrow')}</span>
  </a>
  <div class="ph-body">
    <div class="ph-top">
      <h3 class="ph-name"><a href="product-{p['id']}.html">{p['name']}</a></h3>
      <span class="ph-rate">{svg('i-star')}{fa(p['rating']).replace('٫','٫')}</span>
    </div>
    <p class="ph-sub">{p['sub']}</p>
    <div class="ph-foot">
      <div class="ph-price"><b>{money(p['price'])}</b>{old}</div>
      <button class="add-btn" data-add="{p['id']}" aria-label="افزودن {p['name']} به سبد">{svg('i-plus')}</button>
    </div>
  </div>
</article>'''

def article_card(a, cls=''):
    return f'''
<article class="art-card {cls}" data-cat="{a['cat']}">
  <a class="art-media" href="article-{a['slug']}.html">
    <img src="assets/img/{a['img']}" alt="{a['title']}" loading="lazy" width="760" height="760">
    <span class="art-cat">{a['cat']}</span>
  </a>
  <div class="art-body">
    <div class="art-meta"><span>{a['date']}</span><i></i><span>{fa(a['read'])} دقیقه مطالعه</span></div>
    <h3><a href="article-{a['slug']}.html">{a['title']}</a></h3>
    <p>{a['excerpt']}</p>
    <a class="link-arrow" href="article-{a['slug']}.html">ادامه‌ی مطلب {svg('i-arrow')}</a>
  </div>
</article>'''

def page_head(kicker, title, sub, crumb=None):
    crumbs = ''
    if crumb:
        crumbs = ' <span>/</span> '.join(
            f'<a href="{h}">{t}</a>' if h else f'<b>{t}</b>' for h, t in crumb
        )
        crumbs = f'<nav class="crumbs">{svg("i-home")}<span class="sep">/</span>{crumbs}</nav>'
    return f'''
<section class="page-head">
  <div class="wrap">
    {crumbs}
    <span class="kicker">{svg('sprig')}{kicker}</span>
    <h1 class="page-title">{title}</h1>
    <p class="page-sub">{sub}</p>
  </div>
</section>'''

# ---------------------------------------------------------------- pages
def build_index():
    drinks = [p for p in PRODUCTS if p['cat'] == 'drinks'][:4]
    sweets = [p for p in PRODUCTS if p['cat'] == 'sweets'][:2]
    goods = [p for p in PRODUCTS if p['cat'] == 'goods']
    best = sorted(PRODUCTS, key=lambda p: -p['orders'])[:4]
    arts = ARTICLES[:3]
    gal = GALLERY[:6]

    side = ''.join(
        f'<a class="side-btn" href="{href}">{svg(ic)}<span>{label}</span><i>‹</i></a>'
        for href, ic, label in [
            ('index.html', 'i-home', 'خانه'), ('menu.html', 'i-cup', 'منو'),
            ('shop.html', 'i-shop', 'فروشگاه'), ('events.html', 'i-cal', 'رویدادها'),
            ('bag.html', 'i-bag', 'سبد من')]
    )
    side_btns = side.replace('class="side-btn" href="index.html"', 'class="side-btn active" href="index.html"')

    body = f'''
{SPRITE}
<section class="home-hero">
  <div class="wrap hero-grid">
    <aside class="hero-rail">
      <span class="rail-sprig">{svg('sprig')}</span>
      <h1 class="hero-title">اینجا اتفاق‌های<br>خوب می‌افته</h1>
      <p class="hero-sub">قهوه · توت‌فرنگی · یک روز روشن‌تر</p>
      <nav class="side-menu">{side_btns}</nav>
      <div class="mini-card">
        {svg('strawberry', 'mini-art')}
        <p>توت‌های کوچولو<br>روزهای روشن‌تر {svg('heart', 'inline-heart')}</p>
      </div>
    </aside>

    <div class="hero-center">
      <div class="building-wrap">
        {svg('building', 'building-art')}
        {svg('bunting', 'bunting-overlay') if False else ''}
        <img class="float-art float-1" src="assets/img/latte.jpg" alt="لته توت‌فرنگی" width="760" height="760">
        <img class="float-art float-2" src="assets/img/macaron.jpg" alt="ماکارون بری" width="760" height="760">
        <img class="float-art float-3" src="assets/img/jam.jpg" alt="مربای توت‌فرنگی" width="760" height="760">
      </div>
      <div class="hero-cta">
        <a class="btn btn-red btn-lg" href="menu.html">دیدن منو {svg('i-arrow')}</a>
        <a class="btn btn-ghost btn-lg" href="events.html">رزرو میز {svg('i-cal')}</a>
      </div>
      <div class="hero-stats">
        <div><b>+{fa(12)}</b><span>سال تجربه</span></div>
        <div><b>{fa(38)}</b><span>نوع قهوه و شیرینی</span></div>
        <div><b>۴٫۹</b><span>امتیاز مشتری‌ها</span></div>
      </div>
    </div>

    <div class="hero-cards">
      <article class="card season-card">
        <div class="season-art">
          <img src="assets/img/latte.jpg" alt="پیشنهاد فصل" width="760" height="760">
        </div>
        <div class="season-text">
          <span class="card-kicker">{svg('sprig')} پیشنهاد فصل</span>
          <h3 class="season-title">لته‌های<br>توت‌فرنگی</h3>
          <p class="season-sub">دستورهای شیرین<br>برای یک روز روشن‌تر</p>
          <a class="btn btn-red" href="menu.html#drinks">دیدن منو {svg('i-arrow')}</a>
        </div>
        <span class="season-note">روزهای شیرین<br>در پیش است</span>
      </article>

      <article class="card list-card">
        <header class="list-head">
          <span class="list-title">{svg('sprig', 'leaf-ic')} پرفروش‌ترین‌ها</span>
          <a class="link-arrow" href="menu.html">همه {svg('i-arrow')}</a>
        </header>
        <div class="mini-grid">
          {''.join(f"""<a class="mini-item" href="product-{p['id']}.html">
            <span class="mini-art-box"><img src="assets/img/{p['img']}" alt="{p['name']}" loading="lazy" width="760" height="760"></span>
            <span class="mini-name">{p['name']}</span>
            <span class="mini-price">{money(p['price'])}</span>
          </a>""" for p in best)}
        </div>
      </article>

      <article class="card list-card">
        <header class="list-head">
          <span class="list-title">{svg('i-shop', 'leaf-ic')} کالاهای توت‌فرنگی</span>
          <a class="link-arrow" href="shop.html">خرید {svg('i-arrow')}</a>
        </header>
        <div class="goods-strip">
          {''.join(f"""<a class="good-item" href="product-{p['id']}.html">
            <span class="good-box"><img src="assets/img/{p['img']}" alt="{p['name']}" loading="lazy" width="760" height="760"></span>
            <span class="good-name">{p['name']}</span>
          </a>""" for p in goods)}
        </div>
      </article>

      <a class="card promo-card" href="register.html">
        <span class="promo-icon">{svg('i-gift2')}</span>
        <div>
          <b>کارت وفاداری گوشه</b>
          <span>با هر سفارش توت‌فرنگی جمع کن، هفتمین قهوه مهمان ما.</span>
        </div>
        {svg('i-arrow', 'promo-arrow')}
      </a>
    </div>
  </div>
</section>

<section class="strip">
  <div class="wrap strip-inner">
    <div class="strip-item">{svg('i-truck')}<div><b>ارسال ۳۰ دقیقه‌ای</b><span>در محدوده‌ی مرکز شهر</span></div></div>
    <div class="strip-item">{svg('i-leaf')}<div><b>رست تازه‌ی هفتگی</b><span>هر دوشنبه، دانه‌ی تازه</span></div></div>
    <div class="strip-item">{svg('i-shield')}<div><b>پرداخت امن</b><span>درگاه مستقیم بانکی</span></div></div>
    <div class="strip-item">{svg('i-gift2')}<div><b>هدیه‌ی تولد</b><span>یک برش کیک مهمان ما</span></div></div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <header class="section-head">
      <span class="kicker">{svg('sprig')} منوی امروز</span>
      <h2>تازه از دستگاه و فر</h2>
      <p>هر روز صبح، دانه‌ها رست می‌شوند و کیک‌ها از فر بیرون می‌آیند. این چهارتا امروز بیشتر از همه سفارش داده شده‌اند.</p>
      <a class="link-arrow" href="menu.html">همه‌ی منو {svg('i-arrow')}</a>
    </header>
    <div class="cards-grid">
      {''.join(product_card(p) for p in drinks)}
    </div>
    <div class="cards-grid two">
      {''.join(product_card(p) for p in sweets)}
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap story-strip">
    <div class="story-media">
      <img src="assets/img/cappuccino.jpg" alt="کافه گوشه توت‌فرنگی" loading="lazy" width="760" height="760">
      <span class="story-tape"></span>
    </div>
    <div class="story-copy">
      <span class="kicker">{svg('sprig')} داستان گوشه</span>
      <h2>یک گوشه‌ی کوچک،<br>با یک قلب بزرگ</h2>
      <p>سال ۱۳۹۲ یک دستگاه کوچک اسپرسو و دو صندلی چوبی داشتیم. امروز همان دو صندلی سر جایشان هستند — فقط دور و برشان پر شده از آدم‌هایی که اسمشان را یاد گرفته‌ایم و سفارششان را از حفظ می‌دانیم.</p>
      <ul class="ticks">
        <li>{svg('i-check')} توت‌فرنگی از مزرعه‌ی کردان، هر هفته</li>
        <li>{svg('i-check')} رست اختصاصی، هر دوشنبه صبح</li>
        <li>{svg('i-check')} نان و شیرینی، پخت روز</li>
      </ul>
      <a class="btn btn-ghost" href="story.html">بیشتر بخوانید {svg('i-arrow')}</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <header class="section-head">
      <span class="kicker">{svg('sprig')} از دفترچه‌ی گوشه</span>
      <h2>مقاله‌های قهوه</h2>
      <p>هر هفته یک نوشته‌ی تازه درباره‌ی قهوه، شیرینی و چیزهایی که پشت پیشخوان می‌گذرد.</p>
      <a class="link-arrow" href="articles.html">همه‌ی مقالات {svg('i-arrow')}</a>
    </header>
    <div class="arts-grid">
      {''.join(article_card(a) for a in arts)}
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <header class="section-head">
      <span class="kicker">{svg('sprig')} لحظه‌های گوشه</span>
      <h2>گالری</h2>
      <a class="link-arrow" href="gallery.html">همه‌ی عکس‌ها {svg('i-arrow')}</a>
    </header>
    <div class="gal-strip">
      {''.join(f'<a class="gal-item" href="gallery.html"><img src="assets/img/{g[0]}" alt="{g[1]}" loading="lazy" width="760" height="760"><span>{g[1]}</span></a>' for g in gal)}
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <header class="section-head center">
      <span class="kicker">{svg('sprig')} حرف مشتری‌ها</span>
      <h2>آدم‌هایی که برمی‌گردند</h2>
    </header>
    <div class="quotes">
      <figure class="quote-card">
        <div class="stars">{svg('i-star')*5}</div>
        <blockquote>«هر جمعه صبح، لته‌ی توت‌فرنگی و یک برش کیک. هفته‌ام از همین‌جا شروع می‌شود.»</blockquote>
        <figcaption><span class="ava">ن</span><span><b>نگار م.</b><small>مشتری ثابت، ۳ سال</small></span></figcaption>
      </figure>
      <figure class="quote-card">
        <div class="stars">{svg('i-star')*5}</div>
        <blockquote>«کارگاه کیک را رفتم، هم آشپزی یاد گرفتم هم دو تا دوست تازه. فضای خیلی صمیمی‌ای دارد.»</blockquote>
        <figcaption><span class="ava">ا</span><span><b>امیر ر.</b><small>شرکت‌کننده‌ی کارگاه</small></span></figcaption>
      </figure>
      <figure class="quote-card">
        <div class="stars">{svg('i-star')*5}</div>
        <blockquote>«مربای خانگی‌شان را خانه می‌بریم؛ صبح‌ها روی نان تست، بوی کافه را می‌دهد.»</blockquote>
        <figcaption><span class="ava">س</span><span><b>سارا ک.</b><small>خریدار فروشگاه</small></span></figcaption>
      </figure>
    </div>
  </div>
</section>

<section class="cta-band">
  <div class="wrap cta-inner">
    <div>
      <h2>اولین قهوه‌ات مهمان ما</h2>
      <p>عضو کارت وفاداری گوشه شو؛ با ثبت‌نام، یک لته‌ی کوچک هدیه می‌گیری.</p>
    </div>
    <div class="cta-actions">
      <a class="btn btn-red btn-lg" href="register.html">ثبت‌نام سریع {svg('i-arrow')}</a>
      <a class="btn btn-ghost btn-lg" href="login.html">قبلاً عضو شدم</a>
    </div>
  </div>
</section>
'''
    return layout('خانه', body, active='خانه', page='home')

def build_menu():
    cats = [('all', 'همه')] + [(cid, name) for cid, name in CATS.items()]
    pills = ''.join(
        f'<button class="filter-pill{" active" if cid == "all" else ""}" data-filter="{cid}">{name}'
        f'<span class="pill-count">{fa(len([p for p in PRODUCTS if cid == "all" or p["cat"] == cid]))}</span></button>'
        for cid, name in cats
    )
    sections = ''
    for cid, name in CATS.items():
        items = [p for p in PRODUCTS if p['cat'] == cid]
        if not items:
            continue
        sections += f'''
<section class="menu-block" id="{cid}" data-block="{cid}">
  <header class="block-head">
    <h2>{name}</h2>
    <span>{fa(len(items))} آیتم</span>
  </header>
  <div class="cards-grid">
    {''.join(product_card(p) for p in items)}
  </div>
</section>'''

    body = page_head('منو', 'منوی گوشه', 'همه‌چیز تازه، همه‌چیز همان روز — از اسپرسوی ساده تا کیک توت‌فرنگی.',
                     [('index.html', 'خانه'), (None, 'منو')]) + f'''
<section class="section tight">
  <div class="wrap">
    <div class="menu-toolbar">
      <div class="filters" id="menu-filters">{pills}</div>
      <div class="search-box">
        {svg('i-search')}<input type="search" id="menu-search" placeholder="جست‌وجو در منو…" aria-label="جست‌وجو در منو">
      </div>
    </div>
    <div id="menu-blocks">{sections}</div>
    <p class="menu-empty" id="menu-empty" hidden>چیزی با این اسم پیدا نشد. یک کلمه‌ی دیگر امتحان کن.</p>

    <div class="info-band">
      <div>{svg('i-leaf')}<b>دانه‌ی تازه</b><span>رست هفتگی، آسیاب لحظه‌ای</span></div>
      <div>{svg('i-clock')}<b>آماده در ۱۵ دقیقه</b><span>سفارش آنلاین یا حضوری</span></div>
      <div>{svg('i-shield')}<b>حساسیت غذایی؟</b><span>بگو، نسخه‌ی بدون گلوتن هم داریم</span></div>
    </div>
  </div>
</section>
'''
    return layout('منو', body, active='منو', page='menu', desc='منوی کافه گوشه توت‌فرنگی: قهوه، شیرینی و کالاهای خانگی.')

def build_shop():
    goods = [p for p in PRODUCTS if p['cat'] == 'goods']
    body = page_head('فروشگاه', 'کالاهای گوشه', 'چیزهایی که می‌توانی با خودت به خانه ببری؛ از مربای خانگی تا ماگ دست‌ساز.',
                     [('index.html', 'خانه'), (None, 'فروشگاه')]) + f'''
<section class="section tight">
  <div class="wrap">
    <div class="cards-grid">
      {''.join(product_card(p) for p in goods)}
    </div>
    <div class="shop-note">
      {svg('i-gift2')}
      <div><b>بسته‌بندی هدیه، رایگان</b><span>برای سفارش‌های بالای ۳۰۰٬۰۰۰ تومان، جعبه‌ی هدیه و کارت دست‌نویس مهمان ما.</span></div>
      <a class="link-arrow" href="contact.html">سؤال داری؟ {svg('i-arrow')}</a>
    </div>
  </div>
</section>
'''
    return layout('فروشگاه', body, active='فروشگاه', page='shop')

def build_product(p):
    others = [x for x in PRODUCTS if x['id'] != p['id']][:4]
    sizes = ''.join(
        f'<button class="size-opt{" active" if i == 0 else ""}" data-size="{i}" data-price="{price}">'
        f'<b>{name}</b><span>{money(price)}</span></button>'
        for i, (name, price) in enumerate(p['sizes'])
    )
    tags = ''.join(f'<span class="p-tag">{t}</span>' for t in p['tags'])
    old = f'<s>{money(p["old"])}</s>' if p['old'] else ''
    badge = f'<span class="p-badge">{p["badge"]}</span>' if p['badge'] else ''
    body = page_head('محصول', '', '',
                     [('index.html', 'خانه'), ('menu.html', 'منو'), (None, p['name'])]) + f'''
<section class="section tight">
  <div class="wrap product-grid">
    <div class="product-stage">
      <div class="stage-media">
        {badge}
        <img id="product-img" src="assets/img/{p['img']}" alt="{p['name']}" width="760" height="760">
      </div>
      <p class="stage-hint">{svg('i-arrow-l')} گوشه‌ی عکس را بکش تا بچرخد</p>
    </div>

    <div class="product-info" data-product="{p['id']}" data-name="{p['name']}" data-img="assets/img/{p['img']}">
      <span class="p-cat">{CATS[p['cat']]}</span>
      <h1 class="p-name">{p['name']}</h1>
      <div class="p-rate">{svg('i-star')}<b>{fa(p['rating'])}</b><span>· {fa(p['orders'])} سفارش تا امروز</span></div>
      <div class="p-price"><b id="p-price">{money(p['price'])}</b>{old}</div>
      <p class="p-desc">{p['desc']}</p>
      <div class="p-tags">{tags}</div>

      <div class="p-sizes" id="p-sizes">{sizes}</div>

      <div class="p-actions">
        <div class="stepper">
          <button data-qty="dec" aria-label="کم کردن">−</button>
          <b id="p-qty">۱</b>
          <button data-qty="inc" aria-label="زیاد کردن">+</button>
        </div>
        <button class="btn btn-red btn-lg" id="add-to-cart" data-id="{p['id']}">
          {svg('i-bag')}<span>افزودن به سبد</span>
        </button>
      </div>

      <ul class="p-meta">
        <li>{svg('i-truck')} ارسال ۳۰ دقیقه‌ای در مرکز شهر</li>
        <li>{svg('i-clock')} آماده‌سازی ۱۵ دقیقه</li>
        <li>{svg('i-shield')} پرداخت امن درگاه بانکی</li>
      </ul>
    </div>
  </div>

  <div class="wrap">
    <div class="tabs" id="p-tabs">
      <button class="active" data-tab="desc">توضیحات</button>
      <button data-tab="ing">مواد تشکیل‌دهنده</button>
      <button data-tab="delivery">ارسال و نگهداری</button>
    </div>
    <div class="tab-panel active" data-panel="desc">
      <p>{p['desc']}</p>
      <p>همه‌ی مواد اولیه‌ی این آیتم در آشپزخانه‌ی گوشه آماده می‌شوند و همان روز سرو می‌شوند. اگر حساسیت غذایی داری، قبل از سفارش به ما بگو تا نسخه‌ی مناسب برایت بسازیم.</p>
    </div>
    <div class="tab-panel" data-panel="ing">
      <ul class="plain-list">
        <li>مواد اصلی: {p['sub']}</li>
        <li>بدون رنگ و طعم مصنوعی</li>
        <li>نگهداری: در یخچال، مصرف تا ۴۸ ساعت</li>
      </ul>
    </div>
    <div class="tab-panel" data-panel="delivery">
      <p>ارسال در محدوده‌ی مرکز تهران تا ۳۰ دقیقه. برای سفارش‌های بالای ۳۰۰٬۰۰۰ تومان ارسال رایگان است. بسته‌بندی گرم و سرد جداگانه انجام می‌شود.</p>
    </div>
  </div>

  <div class="wrap">
    <header class="section-head">
      <span class="kicker">{svg('sprig')} شاید این‌ها را هم بخواهی</span>
      <h2>پیشنهاد ما</h2>
    </header>
    <div class="cards-grid">
      {''.join(product_card(o) for o in others)}
    </div>
  </div>
</section>
'''
    return layout(p['name'], body, active='منو', page='product', desc=p['desc'])

def build_events():
    ev = EVENTS
    body = page_head('رویدادها', 'تقویم گوشه', 'کارگاه، موسیقی، کتاب و صبح‌های مزرعه — یک صندلی برایت نگه می‌داریم.',
                     [('index.html', 'خانه'), (None, 'رویدادها')]) + f'''
<section class="section tight">
  <div class="wrap events-layout">
    <div class="card calendar-card">
      <header class="cal-head">
        <button class="cal-nav" id="cal-prev" aria-label="ماه قبل">{svg('i-arrow')}</button>
        <h2 class="cal-title"><span id="cal-month">آبان</span> <small id="cal-year">۱۴۰۵</small></h2>
        <button class="cal-nav" id="cal-next" aria-label="ماه بعد"><span style="display:inline-block;transform:scaleX(-1)">{svg('i-arrow')}</span></button>
        <span class="cal-kicker">دورهمی‌های کوچولو در گوشه {svg('sprig')}</span>
      </header>
      <div class="cal-week"><span>شنبه</span><span>یکشنبه</span><span>دوشنبه</span><span>سه‌شنبه</span><span>چهارشنبه</span><span>پنجشنبه</span><span>جمعه</span></div>
      <div class="cal-grid" id="cal-grid"></div>
      <p class="cal-foot"><i class="dot"></i> کارگاه‌ها با ثبت‌نام قبلی؛ ظرفیت محدود</p>
    </div>

    <aside class="events-side">
      <span class="card-kicker">{svg('sprig')} در همین روز</span>
      <div id="event-detail"></div>
      <div class="event-legend">
        {''.join(f'<div class="legend-row">{svg(e["icon"])}<b>{e["title"]}</b><span>{e["wd"]} {e["time"]}</span></div>' for e in ev)}
      </div>
      <div class="help-card">
        {svg('i-phone')}
        <div><b>رزرو تلفنی</b><span dir="ltr">{SITE['phone']}</span></div>
      </div>
    </aside>
  </div>
</section>
'''
    return layout('رویدادها', body, active='رویدادها', page='events')

def build_gallery():
    items = ''.join(
        f'''<figure class="gal-card tilt-{i % 3}">
              <img src="assets/img/{img}" alt="{cap}" loading="lazy" width="760" height="760">
              <figcaption>{cap}</figcaption>
            </figure>''' for i, (img, cap) in enumerate(GALLERY)
    )
    body = page_head('گالری', 'لحظه‌های گوشه', 'عکس‌هایی از صبح‌های تازه، کیک‌های داغ و آدم‌هایی که برمی‌گردند.',
                     [('index.html', 'خانه'), (None, 'گالری')]) + f'''
<section class="section tight">
  <div class="wrap">
    <div class="gallery-grid" id="gallery">{items}</div>
    <div class="insta-band">
      {svg('i-instagram')}
      <div><b>هر روز یک عکس در اینستاگرام گوشه</b><span>پشت صحنه‌ی آشپزخانه، رست دانه و گاهی گربه‌ی کافه.</span></div>
      <a class="btn btn-red" href="{SITE['instagram']}" target="_blank" rel="noopener">دنبال کردن {svg('i-arrow')}</a>
    </div>
  </div>
</section>
<div class="lightbox" id="lightbox" hidden>
  <button class="lb-close" id="lb-close" aria-label="بستن">{svg('i-close')}</button>
  <button class="lb-nav" id="lb-prev" aria-label="قبلی">{svg('i-arrow')}</button>
  <figure class="lb-figure">
    <div class="lb-frame" id="lb-frame"></div>
    <figcaption id="lb-caption"></figcaption>
  </figure>
  <button class="lb-nav" id="lb-next" aria-label="بعدی"><span style="display:inline-block;transform:scaleX(-1)">{svg('i-arrow')}</span></button>
</div>
'''
    return layout('گالری', body, active='گالری', page='gallery')

def build_articles():
    feat = ARTICLES[0]
    rest = ARTICLES[1:]
    cats = sorted(set(a['cat'] for a in ARTICLES))
    pills = '<button class="filter-pill active" data-afilter="all">همه</button>' + ''.join(
        f'<button class="filter-pill" data-afilter="{c}">{c}</button>' for c in cats
    )
    body = page_head('مقالات', 'دفترچه‌ی گوشه', 'درباره‌ی قهوه، شیرینی و چیزهایی که پشت پیشخوان می‌گذرد.',
                     [('index.html', 'خانه'), (None, 'مقالات')]) + f'''
<section class="section tight">
  <div class="wrap">
    <article class="featured-article">
      <a class="fa-media" href="article-{feat['slug']}.html">
        <img src="assets/img/{feat['img']}" alt="{feat['title']}" width="760" height="760">
        <span class="art-cat">{feat['cat']}</span>
      </a>
      <div class="fa-body">
        <div class="art-meta"><span>{feat['date']}</span><i></i><span>{fa(feat['read'])} دقیقه مطالعه</span><i></i><span>{feat['author']}</span></div>
        <h2><a href="article-{feat['slug']}.html">{feat['title']}</a></h2>
        <p>{feat['excerpt']}</p>
        <a class="btn btn-ghost" href="article-{feat['slug']}.html">خواندن مقاله {svg('i-arrow')}</a>
      </div>
    </article>

    <div class="menu-toolbar">
      <div class="filters" id="article-filters">{pills}</div>
      <div class="search-box">{svg('i-search')}<input type="search" id="article-search" placeholder="جست‌وجو در مقالات…" aria-label="جست‌وجو در مقالات"></div>
    </div>

    <div class="arts-grid" id="articles-grid">
      {''.join(article_card(a) for a in rest)}
    </div>
    <p class="menu-empty" id="articles-empty" hidden>مقاله‌ای با این عنوان پیدا نشد.</p>
  </div>
</section>
'''
    return layout('مقالات', body, active='مقالات', page='articles')

def build_article(a):
    related = [x for x in ARTICLES if x['slug'] != a['slug']][:3]
    paras = ''.join(f'<p>{p}</p>' for p in a['body'])
    body = f'''
<article class="article-wrap">
  <div class="wrap">
    <nav class="crumbs">{svg('i-home')}<span class="sep">/</span><a href="index.html">خانه</a><span class="sep">/</span><a href="articles.html">مقالات</a><span class="sep">/</span><b>{a['cat']}</b></nav>
    <header class="article-head">
      <span class="kicker">{svg('sprig')} {a['cat']}</span>
      <h1>{a['title']}</h1>
      <div class="art-meta big">
        <span>{a['date']}</span><i></i><span>{fa(a['read'])} دقیقه مطالعه</span><i></i><span>نویسنده: {a['author']}</span>
      </div>
    </header>
    <figure class="article-cover">
      <img src="assets/img/{a['img']}" alt="{a['title']}" width="760" height="760">
    </figure>
    <div class="article-body">
      <p class="lead">{a['excerpt']}</p>
      {paras}
      <blockquote class="pull-quote">«قهوه‌ی خوب، صبر می‌خواهد؛ درست مثل هر چیز خوبِ دیگر.»</blockquote>
      <div class="article-share">
        <span>این مقاله را برای یک دوست بفرست</span>
        <div class="socials">
          <a href="{SITE['telegram']}" target="_blank" rel="noopener" aria-label="تلگرام">{svg('i-telegram')}</a>
          <a href="{SITE['whatsapp']}" target="_blank" rel="noopener" aria-label="واتساپ">{svg('i-whatsapp')}</a>
          <a href="{SITE['instagram']}" target="_blank" rel="noopener" aria-label="اینستاگرام">{svg('i-instagram')}</a>
        </div>
      </div>
      <div class="author-box">
        <span class="ava">{a['author'][0]}</span>
        <div><b>{a['author']}</b><span>نویسنده و باریستای گوشه توت‌فرنگی</span></div>
        <a class="link-arrow" href="articles.html">مقالات بیشتر {svg('i-arrow')}</a>
      </div>
    </div>

    <header class="section-head">
      <span class="kicker">{svg('sprig')} ادامه‌ی خواندن</span>
      <h2>مقاله‌های دیگر</h2>
    </header>
    <div class="arts-grid">
      {''.join(article_card(r) for r in related)}
    </div>
  </div>
</article>
<div class="readbar" id="readbar"></div>
'''
    return layout(a['title'], body, active='مقالات', page='article', desc=a['excerpt'])

def build_story():
    body = page_head('داستان ما', 'از یک گوشه‌ی کوچک', 'دوازده سال، دو صندلی چوبی و یک دستگاه اسپرسوی کوچک که هنوز کار می‌کند.',
                     [('index.html', 'خانه'), (None, 'داستان ما')]) + f'''
<section class="section tight">
  <div class="wrap story-strip">
    <div class="story-media">
      <img src="assets/img/cake.jpg" alt="آشپزخانه‌ی گوشه" width="760" height="760">
    </div>
    <div class="story-copy">
      <span class="kicker">{svg('sprig')} ۱۳۹۲ تا امروز</span>
      <h2>اولش فقط دو صندلی بود</h2>
      <p>مادر بزرگم می‌گفت هر محله یک گوشه‌ی خوب لازم دارد؛ جایی که بشود بی‌حساب بنشینی. ما همان گوشه را ساختیم: با یک دستگاه کوچک، دو صندلی چوبی و یک شیشه مربای توت‌فرنگی که خودمان پخته بودیم.</p>
      <p>امروز دوازده نفر با ما کار می‌کنند، هر هفته دانه رست می‌کنیم و هر دوشنبه صبح آشپزخانه بوی کیک تازه می‌دهد. اما همان دو صندلی، دقیقاً سر جای خودشان هستند.</p>
      <div class="story-stats">
        <div><b>۱۲</b><span>سال</span></div>
        <div><b>۳۸</b><span>آیتم منو</span></div>
        <div><b>۱۴</b><span>همکار</span></div>
        <div><b>۴٫۹</b><span>امتیاز</span></div>
      </div>
    </div>
  </div>

  <div class="wrap values">
    <div class="value-card">{svg('i-leaf')}<b>مواد اولیه‌ی محلی</b><span>توت از کردان، شیر از دامداری‌های اطراف تهران، آرد از آسیاب سنتی.</span></div>
    <div class="value-card">{svg('i-cup')}<b>قهوه‌ی رست خودمان</b><span>هر دوشنبه ۲۰ کیلو دانه تازه رست می‌کنیم؛ بیشتر از این، کهنه می‌شود.</span></div>
    <div class="value-card">{svg('i-heart') if False else svg('i-gift2')}<b>آدم‌ها قبل از قهوه</b><span>اسم مشتری‌های ثابت را یاد گرفته‌ایم؛ این سخت‌ترین و بهترین بخش کار است.</span></div>
  </div>

  <div class="wrap timeline">
    <h2>مسیر ما</h2>
    <ol>
      <li><b>۱۳۹۲</b><span>افتتاح با دو صندلی و یک دستگاه اسپرسو</span></li>
      <li><b>۱۳۹۵</b><span>شروع پخت کیک توت‌فرنگی؛ اولین صف صبحگاهی</span></li>
      <li><b>۱۳۹۸</b><span>راه‌اندازی رست اختصاصی و کارگاه‌های آخر هفته</span></li>
      <li><b>۱۴۰۲</b><span>شعبه‌ی دوم در کریمخان و شروع فروشگاه آنلاین</span></li>
      <li><b>۱۴۰۵</b><span>۲۰ هزار فنجان در سال؛ همان دو صندلی، همان گوشه</span></li>
    </ol>
  </div>
</section>
'''

    return layout('داستان ما', body, active='داستان ما', page='story')

def build_contact():
    body = page_head('تماس', 'بیا یک قهوه بخوریم', 'سؤال، پیشنهاد، رزرو گروهی یا فقط یک سلام — همه‌اش خوشحال‌مان می‌کند.',
                     [('index.html', 'خانه'), (None, 'تماس')]) + f'''
<section class="section tight">
  <div class="wrap contact-grid">
    <div class="contact-cards">
      <a class="contact-card" href="tel:{SITE['phone_link']}">
        {svg('i-phone')}<b>تلفن کافه</b><span dir="ltr">{SITE['phone']}</span><small>هر روز ۸ تا ۲۳</small>
      </a>
      <a class="contact-card" href="mailto:{SITE['email']}">
        {svg('i-mail')}<b>ایمیل</b><span dir="ltr">{SITE['email']}</span><small>پاسخ تا ۲۴ ساعت</small>
      </a>
      <div class="contact-card">
        {svg('i-pin')}<b>نشانی</b><span>{SITE['address']}</span><small>پارکینگ عمومی در کوچه</small>
      </div>
      <div class="contact-card">
        {svg('i-clock')}<b>ساعت کاری</b><span>{SITE['hours']}</span><small>جمعه‌ها از ۱۰ صبح</small>
      </div>
    </div>

    <form class="contact-form card" id="contact-form" novalidate>
      <h3>برایمان بنویس</h3>
      <div class="field-row">
        <label class="field"><span>نام و نام خانوادگی</span><input type="text" name="name" required placeholder="مثلاً نگار محمدی"></label>
        <label class="field"><span>شماره تماس</span><input type="tel" name="phone" required placeholder="۰۹۱۲…" dir="ltr"></label>
      </div>
      <label class="field"><span>موضوع</span>
        <select name="subject">
          <option>سؤال درباره‌ی منو</option>
          <option>رزرو گروهی</option>
          <option>همکاری و کارگاه</option>
          <option>انتقاد و پیشنهاد</option>
        </select>
      </label>
      <label class="field"><span>پیام</span><textarea name="message" rows="5" required placeholder="سلام! می‌خواستم بپرسم…"></textarea></label>
      <button class="btn btn-red btn-lg" type="submit">ارسال پیام {svg('i-arrow')}</button>
      <p class="form-note">این فرم نمونه است و پیام به سرور ارسال نمی‌شود.</p>
    </form>
  </div>

  <div class="wrap">
    <div class="map-card">
      <div class="map-pin">{svg('i-pin')}</div>
      <div class="map-grid"></div>
      <div class="map-note"><b>اینجاییم</b><span>{SITE['address']}</span></div>
    </div>
  </div>
</section>
'''
    return layout('تماس', body, active='تماس', page='contact')

def build_login():
    body = f'''
<section class="auth-wrap">
  <div class="auth-visual">
    <img src="assets/img/latte.jpg" alt="لته توت‌فرنگی" width="760" height="760">
    <div class="auth-visual-copy">
      <span class="kicker">{svg('sprig')} گوشه توت‌فرنگی</span>
      <h2>خوش برگشتی</h2>
      <p>با حسابت سفارش‌های قبلی، امتیاز توت‌فرنگی و آدرس‌هایت را یک‌جا داری.</p>
      <div class="auth-badge">{svg('i-gift2')} با ورود امروز، ۵۰ امتیاز هدیه بگیر</div>
    </div>
  </div>

  <div class="auth-card">
    <h1>ورود به حساب</h1>
    <p class="auth-sub">شماره موبایل یا ایمیلت را وارد کن.</p>
    <form id="login-form" novalidate>
      <label class="field"><span>موبایل یا ایمیل</span>
        <input type="text" name="ident" id="login-ident" required placeholder="۰۹۱۲۳۴۵۶۷۸۹" dir="ltr">
        <small class="field-err" data-err="ident"></small>
      </label>
      <label class="field"><span>رمز عبور</span>
        <span class="pass-wrap">
          <input type="password" name="password" id="login-pass" required minlength="6" placeholder="••••••">
          <button type="button" class="pass-toggle" data-pass="login-pass" aria-label="نمایش رمز">{svg('i-eye')}</button>
        </span>
        <small class="field-err" data-err="password"></small>
      </label>
      <div class="auth-row">
        <label class="check"><input type="checkbox" name="remember" checked><span>من را به یاد بسپار</span></label>
        <a class="link-arrow" href="login.html">رمز را فراموش کردم؟</a>
      </div>
      <button class="btn btn-red btn-lg btn-block" type="submit">ورود {svg('i-arrow')}</button>
    </form>
    <p class="auth-alt">حساب نداری؟ <a href="register.html">ثبت‌نام کن</a></p>
    <p class="form-note">این صفحه نمونه است؛ احراز هویت واقعی نیاز به بک‌اند دارد.</p>
  </div>
</section>
'''
    return layout('ورود', body, page='login')

def build_register():
    body = f'''
<section class="auth-wrap">
  <div class="auth-visual register">
    <img src="assets/img/cake.jpg" alt="کیک توت‌فرنگی" width="760" height="760">
    <div class="auth-visual-copy">
      <span class="kicker">{svg('sprig')} کارت وفاداری</span>
      <h2>اولین قهوه مهمان ما</h2>
      <p>با ثبت‌نام، یک لته‌ی کوچک توت‌فرنگی هدیه می‌گیری و از تخفیف تولد هم باخبر می‌شوی.</p>
      <ul class="ticks light">
        <li>{svg('i-check')} هفتمین قهوه رایگان</li>
        <li>{svg('i-check')} هدیه‌ی تولد و سالگرد</li>
        <li>{svg('i-check')} دسترسی زودتر به کارگاه‌ها</li>
      </ul>
    </div>
  </div>

  <div class="auth-card">
    <h1>ساخت حساب</h1>
    <p class="auth-sub">۳۰ ثانیه وقت می‌گیرد.</p>
    <form id="register-form" novalidate>
      <div class="field-row">
        <label class="field"><span>نام</span><input type="text" name="fname" required placeholder="نگار"><small class="field-err" data-err="fname"></small></label>
        <label class="field"><span>نام خانوادگی</span><input type="text" name="lname" required placeholder="محمدی"><small class="field-err" data-err="lname"></small></label>
      </div>
      <label class="field"><span>شماره موبایل</span>
        <input type="tel" name="phone" id="reg-phone" required placeholder="۰۹۱۲۳۴۵۶۷۸۹" dir="ltr">
        <small class="field-err" data-err="phone"></small>
      </label>
      <label class="field"><span>ایمیل (اختیاری)</span><input type="email" name="email" placeholder="you@example.com" dir="ltr"></label>
      <label class="field"><span>رمز عبور</span>
        <span class="pass-wrap">
          <input type="password" name="password" id="reg-pass" required minlength="6" placeholder="حداقل ۶ کاراکتر">
          <button type="button" class="pass-toggle" data-pass="reg-pass" aria-label="نمایش رمز">{svg('i-eye')}</button>
        </span>
        <span class="pass-meter"><i id="pass-bar"></i></span>
        <small class="field-err" data-err="password"></small>
      </label>
      <label class="check"><input type="checkbox" name="terms" required><span>قوانین کافه و حریم خصوصی را می‌پذیرم</span></label>
      <button class="btn btn-red btn-lg btn-block" type="submit">ثبت‌نام {svg('i-arrow')}</button>
    </form>
    <p class="auth-alt">حساب داری؟ <a href="login.html">وارد شو</a></p>
  </div>
</section>
'''
    return layout('ثبت‌نام', body, page='register')

def build_bag():
    body = page_head('سبد خرید', 'سبد کوچولوی تو', 'هر چیزی که انتخاب کردی اینجاست؛ می‌توانی تعداد را عوض کنی یا حذف کنی.',
                     [('index.html', 'خانه'), (None, 'سبد خرید')]) + f'''
<section class="section tight">
  <div class="wrap bag-layout">
    <div class="card bag-main">
      <header class="bag-head">
        <h2>سفارش تو</h2>
        <span class="bag-count" id="bag-count">۰ آیتم</span>
      </header>
      <div class="bag-items" id="bag-items"></div>
      <div class="bag-empty" id="bag-empty" hidden>
        {svg('i-bag')}
        <p>سبدت هنوز خالی است.<br>یک لته بگذار توی‌اش، روزت روشن‌تر می‌شود.</p>
        <a class="btn btn-red" href="menu.html">رفتن به منو {svg('i-arrow')}</a>
      </div>
    </div>

    <aside class="card bag-summary-card">
      <h3>جمع سفارش</h3>
      <div class="sum-row"><span>جمع آیتم‌ها</span><b id="sum-items">۰ تومان</b></div>
      <div class="sum-row"><span>تخفیف کارت وفاداری</span><b class="free" id="sum-off">۰ تومان</b></div>
      <div class="sum-row"><span>هزینه‌ی ارسال</span><b id="sum-ship">۳۵٬۰۰۰ تومان</b></div>
      <div class="sum-total"><span>قابل پرداخت</span><b id="sum-total">۰ تومان</b></div>
      <label class="field coupon">
        <span>کد تخفیف</span>
        <span class="coupon-row">
          <input type="text" id="coupon" placeholder="STRAWBERRY">
          <button class="btn btn-ghost" type="button" id="coupon-btn">اعمال</button>
        </span>
      </label>
      <a class="btn btn-red btn-lg btn-block" href="checkout.html">ادامه‌ی تسویه {svg('i-arrow')}</a>
      <a class="link-arrow block" href="menu.html">افزودن آیتم بیشتر {svg('i-plus')}</a>
      <div class="gift-note">{svg('i-gift2')}<span>بالای ۳۰۰٬۰۰۰ تومان، بسته‌بندی هدیه رایگان است.</span></div>
    </aside>
  </div>

  <div class="wrap">
    <header class="section-head">
      <span class="kicker">{svg('sprig')} قبل از رفتن</span>
      <h2>این‌ها را هم اضافه کن</h2>
    </header>
    <div class="cards-grid" id="bag-suggest"></div>
  </div>
</section>
'''
    return layout('سبد خرید', body, page='bag')

def build_checkout():
    body = page_head('تسویه', 'تسویه‌ی سفارش', 'یک قدم تا قهوه‌ات مانده.',
                     [('index.html', 'خانه'), ('bag.html', 'سبد خرید'), (None, 'تسویه')]) + f'''
<section class="section tight">
  <div class="wrap checkout-grid">
    <form class="card checkout-form" id="checkout-form" novalidate>
      <h2>اطلاعات تحویل</h2>
      <div class="field-row">
        <label class="field"><span>نام و نام خانوادگی</span><input type="text" name="name" required placeholder="نگار محمدی"><small class="field-err" data-err="name"></small></label>
        <label class="field"><span>شماره موبایل</span><input type="tel" name="phone" required placeholder="۰۹۱۲۳۴۵۶۷۸۹" dir="ltr"><small class="field-err" data-err="phone"></small></label>
      </div>
      <label class="field"><span>نشانی</span><textarea name="address" rows="3" required placeholder="خیابان، کوچه، پلاک، واحد"></textarea><small class="field-err" data-err="address"></small></label>
      <div class="field-row">
        <label class="field"><span>زمان تحویل</span>
          <select name="time">
            <option>در اسرع وقت (۳۰ دقیقه)</option>
            <option>امروز، ساعت ۱۶:۰۰</option>
            <option>امروز، ساعت ۱۹:۰۰</option>
            <option>فردا صبح، ساعت ۹:۰۰</option>
          </select>
        </label>
        <label class="field"><span>روش پرداخت</span>
          <select name="pay">
            <option>پرداخت آنلاین</option>
            <option>پرداخت در محل</option>
            <option>کیف پول گوشه</option>
          </select>
        </label>
      </div>
      <label class="field"><span>یادداشت (اختیاری)</span><input type="text" name="note" placeholder="مثلاً زنگ نزن، تحویل به نگهبان"></label>
      <label class="check"><input type="checkbox" name="gift" id="gift-check"><span>بسته‌بندی هدیه با کارت دست‌نویس</span></label>
      <button class="btn btn-red btn-lg btn-block" type="submit" id="pay-btn">پرداخت و ثبت سفارش {svg('i-arrow')}</button>
      <p class="form-note">این یک قالب نمایشی است؛ درگاه پرداخت واقعی متصل نیست.</p>
    </form>

    <aside class="card order-summary">
      <h3>خلاصه‌ی سفارش <span id="co-count" class="bag-count">۰ آیتم</span></h3>
      <div class="co-items" id="co-items"></div>
      <div class="sum-row"><span>جمع آیتم‌ها</span><b id="co-items-total">۰ تومان</b></div>
      <div class="sum-row"><span>ارسال</span><b>۳۵٬۰۰۰ تومان</b></div>
      <div class="sum-total"><span>قابل پرداخت</span><b id="co-total">۰ تومان</b></div>
    </aside>
  </div>
</section>
'''
    return layout('تسویه', body, page='checkout')

def build_thanks():
    body = f'''
<section class="thanks-wrap">
  <div class="thanks-card card">
    <span class="thanks-kicker">{svg('i-check')} سفارش ثبت شد</span>
    <h1>ممنون از تو!</h1>
    <p class="thanks-sub">سفارشت به آشپزخانه رسید؛ تا ۱۵ دقیقه‌ی دیگر دم در است.</p>
    <div class="order-no">شماره سفارش: <b id="order-no">—</b></div>
    <div class="receipt" id="receipt"></div>
    <div class="thanks-actions">
      <a class="btn btn-red" href="index.html">برگشت به کافه {svg('i-arrow')}</a>
      <a class="btn btn-ghost" href="menu.html">سفارش دوباره</a>
    </div>
  </div>
  <div class="thanks-art">
    {svg('building', 'thanks-building')}
    {svg('bunting', 'bunting-overlay show')}
  </div>
</section>
<div class="confetti" id="confetti"></div>
'''
    return layout('سفارش ثبت شد', body, page='thanks')

def build_404():
    body = f'''
<section class="notfound">
  <div class="wrap">
    <span class="nf-art">{svg('strawberry')}</span>
    <h1>۴۰۴</h1>
    <p>این صفحه یا فنجان را ما نداریم… شاید لینک قدیمی است.</p>
    <div class="nf-actions">
      <a class="btn btn-red btn-lg" href="index.html">برگشت به خانه {svg('i-arrow')}</a>
      <a class="btn btn-ghost btn-lg" href="menu.html">دیدن منو</a>
    </div>
  </div>
</section>
'''
    return layout('صفحه پیدا نشد', body, page='404')

# ---------------------------------------------------------------- write
def write(name, content):
    with io.open(name, 'w', encoding='utf-8') as f:
        f.write(content)
    print('  ✓', name)

print('ساخت صفحه‌ها…')
write('index.html', build_index())
write('menu.html', build_menu())
write('shop.html', build_shop())
write('events.html', build_events())
write('gallery.html', build_gallery())
write('articles.html', build_articles())
write('story.html', build_story())
write('contact.html', build_contact())
write('login.html', build_login())
write('register.html', build_register())
write('bag.html', build_bag())
write('checkout.html', build_checkout())
write('thanks.html', build_thanks())
write('404.html', build_404())
for p in PRODUCTS:
    write(f'product-{p["id"]}.html', build_product(p))
for a in ARTICLES:
    write(f'article-{a["slug"]}.html', build_article(a))
print('تمام شد.')
