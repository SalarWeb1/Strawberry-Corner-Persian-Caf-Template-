/* ============================================================
   گوشه توت‌فرنگی — app.js (نسخه ۳)
   سبد خرید، کشوی سبد، پرواز محصول به سبد، تقویم شمسی، فرم‌ها
   ============================================================ */
(function () {
  'use strict';

  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const G = window.gsap;
  const PAGE = document.body.dataset.page || 'page';

  /* ---------------- کمکی‌ها ---------------- */
  const faNum = n => Number(n).toLocaleString('fa-IR');
  const money = n => faNum(n) + ' تومان';
  const store = {
    get(k, d) { try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} },
    del(k) { try { localStorage.removeItem(k); } catch (e) {} },
  };

  const PRODUCTS = window.DATA.products;
  const byId = id => PRODUCTS.find(p => p.id === id);

  let cart = store.get('sc3_cart', []);       // [{id, size, sizeName, qty, price}]
  const SHIP = 35000;

  /* ---------------- توست ---------------- */
  let toastTimer;
  function toast(msg, icon = 'i-check') {
    const t = $('#toast');
    if (!t) return;
    t.innerHTML = `<svg><use href="#${icon}"/></svg><span>${msg}</span>`;
    t.classList.add('show');
    if (G) G.fromTo(t, { y: 20, opacity: .4 }, { y: 0, opacity: 1, duration: .4, ease: 'back.out(2)' });
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => t.classList.remove('show'), 2600);
  }

  /* ---------------- سبد ---------------- */
  const cartCount = () => cart.reduce((s, i) => s + i.qty, 0);
  const cartTotal = () => cart.reduce((s, i) => s + i.price * i.qty, 0);
  function saveCart() {
    store.set('sc3_cart', cart);
    updateCartUI();
  }
  function addToCart(id, opts = {}) {
    const p = byId(id);
    if (!p) return;
    const sizeIdx = opts.sizeIdx || 0;
    const sizeName = (p.sizes[sizeIdx] || p.sizes[0])[0];
    const price = (p.sizes[sizeIdx] || p.sizes[0])[1];
    const qty = opts.qty || 1;
    const key = id + '|' + sizeName;
    const found = cart.find(i => i.id + '|' + i.sizeName === key);
    if (found) found.qty += qty;
    else cart.push({ id, sizeIdx, sizeName, qty, price });
    saveCart();
    toast(`${p.name} به سبد اضافه شد`, 'i-check');
  }

  function updateCartUI() {
    const n = cartCount();
    $$('#cart-count, [data-cart-count]').forEach(el => {
      el.textContent = faNum(n);
      el.hidden = false;
    });
    $$('[data-cart-total]').forEach(el => el.textContent = money(cartTotal()));
    const dc = $('#drawer-count');
    if (dc) dc.textContent = faNum(n) + ' خوراکی';
    const dt = $('#drawer-total');
    if (dt) dt.textContent = money(cartTotal());
    renderDrawer();
  }

  /* ---------------- کشوی سبد ---------------- */
  function renderDrawer() {
    const body = $('#drawer-body');
    if (!body) return;
    if (!cart.length) {
      body.innerHTML = `<div class="drawer-empty">
        <svg><use href="#i-bag"/></svg>
        <p>سبدت خالی است.<br>یک لته توت‌فرنگی بگذار توی‌اش.</p>
        <a class="btn btn-red" href="menu.html" style="margin-top:14px">دیدن منو</a>
      </div>`;
      return;
    }
    body.innerHTML = cart.map((i, idx) => {
      const p = byId(i.id) || { name: 'آیتم', img: 'latte.jpg' };
      return `<div class="d-item">
        <span class="d-art"><img src="assets/img/${p.img}" alt="${p.name}" loading="lazy"></span>
        <div class="d-info">
          <div class="d-name">${p.name}</div>
          <div class="d-sub">${i.sizeName} · ${money(i.price)}</div>
        </div>
        <div class="stepper" style="transform:scale(.86)">
          <button data-ddec="${idx}" aria-label="کم">−</button><b>${faNum(i.qty)}</b><button data-dinc="${idx}" aria-label="زیاد">+</button>
        </div>
        <button class="d-remove" data-ddel="${idx}" aria-label="حذف"><svg><use href="#i-trash"/></svg></button>
      </div>`;
    }).join('');
    $$('[data-dinc]', body).forEach(b => b.onclick = () => { cart[+b.dataset.dinc].qty++; saveCart(); });
    $$('[data-ddec]', body).forEach(b => b.onclick = () => {
      const i = +b.dataset.ddec; cart[i].qty--;
      if (cart[i].qty < 1) cart.splice(i, 1);
      saveCart();
    });
    $$('[data-ddel]', body).forEach(b => b.onclick = () => {
      cart.splice(+b.dataset.ddel, 1); saveCart(); toast('از سبد حذف شد', 'i-trash');
    });
  }

  function openDrawer() {
    const d = $('#cart-drawer'), o = $('#drawer-overlay');
    if (!d) return;
    d.classList.add('open'); d.setAttribute('aria-hidden', 'false');
    if (o) o.hidden = false;
    document.body.style.overflow = 'hidden';
    if (G) G.fromTo(d, { x: -30 }, { x: 0, duration: .4, ease: 'power3.out' });
  }
  function closeDrawer() {
    const d = $('#cart-drawer'), o = $('#drawer-overlay');
    if (!d) return;
    d.classList.remove('open'); d.setAttribute('aria-hidden', 'true');
    if (o) o.hidden = true;
    document.body.style.overflow = '';
  }

  /* ---------------- پرواز محصول به سبد ---------------- */
  function flyToCart(sourceEl, imgSrc) {
    const target = $('#cart-btn');
    if (!target || !sourceEl) return;
    const s = sourceEl.getBoundingClientRect();
    const t = target.getBoundingClientRect();

    const ghost = document.createElement('img');
    ghost.src = imgSrc;
    ghost.style.cssText = `position:fixed;left:${s.left}px;top:${s.top}px;width:${s.width}px;height:${s.height}px;
      border-radius:18px;object-fit:cover;z-index:250;pointer-events:none;box-shadow:0 20px 40px -18px rgba(0,0,0,.5)`;
    document.body.appendChild(ghost);

    const dx = t.left + t.width / 2 - (s.left + s.width / 2);
    const dy = t.top + t.height / 2 - (s.top + s.height / 2);

    if (!G) {
      ghost.remove();
      target.classList.add('pulse');
      setTimeout(() => target.classList.remove('pulse'), 520);
      return;
    }
    G.timeline({ onComplete: () => {
      ghost.remove();
      target.classList.add('pulse');
      setTimeout(() => target.classList.remove('pulse'), 520);
      G.fromTo(target, { scale: 1 }, { scale: 1.18, duration: .18, yoyo: true, repeat: 1, ease: 'power2.inOut' });
    }})
      .to(ghost, { scale: .25, width: 34, height: 34, borderRadius: '50%', duration: .25, ease: 'power2.in' })
      .to(ghost, { x: dx, y: dy, rotate: 380, duration: .8, ease: 'power2.inOut' }, '>-0.05')
      .to(ghost, { opacity: 0, scale: .1, duration: .22 }, '>-0.15');
  }

  /* ---------------- اتصال دکمه‌های افزودن ---------------- */
  document.addEventListener('click', e => {
    const btn = e.target.closest('[data-add]');
    if (btn) {
      e.preventDefault();
      const id = btn.dataset.add;
      addToCart(id, { sizeIdx: +(btn.dataset.size || 0) });
      const card = btn.closest('.ph-card, .product-info, .mini-item');
      const img = card ? card.querySelector('img') : null;
      if (img) flyToCart(img, img.currentSrc || img.src);
      else flyToCart(btn, `assets/img/${(byId(id) || {}).img || 'latte.jpg'}`);
      if (btn.classList.contains('add-btn')) {
        btn.classList.add('added');
        setTimeout(() => btn.classList.remove('added'), 900);
      }
    }
    if (e.target.closest('#cart-btn')) { e.preventDefault(); openDrawer(); }
    if (e.target.closest('#drawer-close, #drawer-overlay, #drawer-continue')) closeDrawer();
  });

  /* ---------------- هدر ---------------- */
  function initHeader() {
    const burger = $('#burger'), mnav = $('#mobile-nav');
    if (burger) burger.onclick = () => {
      const open = mnav.classList.toggle('open');
      burger.setAttribute('aria-expanded', open);
    };

    const themeBtn = $('#theme-btn');
    const saved = store.get('sc3_theme', 'light');
    if (saved === 'dark') document.documentElement.setAttribute('data-theme', 'dark');
    const paint = () => {
      const dark = document.documentElement.getAttribute('data-theme') === 'dark';
      if (themeBtn) themeBtn.innerHTML = `<svg><use href="#${dark ? 'i-sun' : 'i-moon'}"/></svg>`;
    };
    paint();
    if (themeBtn) themeBtn.onclick = () => {
      const dark = document.documentElement.getAttribute('data-theme') === 'dark';
      if (dark) document.documentElement.removeAttribute('data-theme');
      else document.documentElement.setAttribute('data-theme', 'dark');
      store.set('sc3_theme', dark ? 'light' : 'dark');
      paint();
    };

    const toTop = $('#to-top');
    if (toTop) {
      toTop.onclick = () => window.scrollTo({ top: 0, behavior: 'smooth' });
      window.addEventListener('scroll', () => {
        toTop.classList.toggle('show', window.scrollY > 600);
      }, { passive: true });
    }
  }

  /* ---------------- فیلتر منو ---------------- */
  function initMenuFilters() {
    const wrap = $('#menu-filters');
    if (!wrap) return;
    const search = $('#menu-search');
    const blocks = $$('[data-block]');
    const empty = $('#menu-empty');
    let activeCat = 'all';

    function apply() {
      const q = (search && search.value || '').trim();
      let shown = 0;
      blocks.forEach(b => {
        const cat = b.dataset.block;
        const catOk = activeCat === 'all' || cat === activeCat;
        let visibleInBlock = 0;
        $$('.ph-card', b).forEach(card => {
          const name = card.querySelector('.ph-name').textContent;
          const ok = catOk && (!q || name.includes(q));
          card.style.display = ok ? '' : 'none';
          if (ok) { visibleInBlock++; shown++; }
        });
        b.hidden = visibleInBlock === 0;
      });
      if (empty) empty.hidden = shown !== 0;
    }

    $$('.filter-pill', wrap).forEach(pill => {
      pill.onclick = () => {
        $$('.filter-pill', wrap).forEach(x => x.classList.remove('active'));
        pill.classList.add('active');
        activeCat = pill.dataset.filter;
        apply();
      };
    });
    if (search) search.addEventListener('input', apply);
  }

  /* ---------------- فیلتر مقالات ---------------- */
  function initArticleFilters() {
    const wrap = $('#article-filters');
    if (!wrap) return;
    const search = $('#article-search');
    const grid = $('#articles-grid');
    const empty = $('#articles-empty');
    let cat = 'all';
    function apply() {
      const q = (search && search.value || '').trim();
      let shown = 0;
      $$('.art-card', grid).forEach(card => {
        const ok = (cat === 'all' || card.dataset.cat === cat) &&
                   (!q || card.textContent.includes(q));
        card.style.display = ok ? '' : 'none';
        if (ok) shown++;
      });
      if (empty) empty.hidden = shown !== 0;
    }
    $$('.filter-pill', wrap).forEach(p => p.onclick = () => {
      $$('.filter-pill', wrap).forEach(x => x.classList.remove('active'));
      p.classList.add('active'); cat = p.dataset.afilter; apply();
    });
    if (search) search.addEventListener('input', apply);
  }

  /* ---------------- صفحه محصول ---------------- */
  function initProductPage() {
    const info = $('.product-info');
    if (!info) return;
    const basePrice = +($('#p-price') ? info.querySelector('.p-price b').dataset.raw || 0 : 0);
    const priceEl = $('#p-price');
    let sizeIdx = 0, qty = 1;

    $$('.size-opt').forEach(btn => {
      btn.onclick = () => {
        $$('.size-opt').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        sizeIdx = +btn.dataset.size;
        priceEl.textContent = money(+btn.dataset.price);
        if (G) G.fromTo(priceEl, { y: 8, opacity: .3 }, { y: 0, opacity: 1, duration: .35 });
      };
    });

    $$('[data-qty]').forEach(b => {
      b.onclick = () => {
        qty = b.dataset.qty === 'inc' ? Math.min(20, qty + 1) : Math.max(1, qty - 1);
        $('#p-qty').textContent = faNum(qty);
        if (G) G.fromTo('#p-qty', { scale: 1.4 }, { scale: 1, duration: .3, ease: 'back.out(3)' });
      };
    });

    const addBtn = $('#add-to-cart');
    if (addBtn) addBtn.onclick = () => {
      const id = addBtn.dataset.id;
      addToCart(id, { sizeIdx, qty });
      const img = $('#product-img');
      if (img) flyToCart(img, img.src);
      addBtn.querySelector('span').textContent = 'اضافه شد ✓';
      setTimeout(() => addBtn.querySelector('span').textContent = 'افزودن به سبد', 1400);
    };

    // تب‌ها
    $$('#p-tabs button').forEach(t => t.onclick = () => {
      $$('#p-tabs button').forEach(x => x.classList.remove('active'));
      t.classList.add('active');
      $$('.tab-panel').forEach(p => p.classList.toggle('active', p.dataset.panel === t.dataset.tab));
    });

    // چرخش ملایم عکس با حرکت ماوس
    const stage = $('.stage-media'), img = $('#product-img');
    if (stage && img && window.matchMedia('(hover:hover)').matches) {
      stage.addEventListener('mousemove', e => {
        const r = stage.getBoundingClientRect();
        const px = (e.clientX - r.left) / r.width - .5;
        const py = (e.clientY - r.top) / r.height - .5;
        img.style.transform = `perspective(900px) rotateY(${px * 10}deg) rotateX(${-py * 10}deg) scale(1.04)`;
      });
      stage.addEventListener('mouseleave', () => img.style.transform = '');
    }
  }

  /* ---------------- گالری ---------------- */
  function initGallery() {
    const grid = $('#gallery');
    const lb = $('#lightbox');
    if (!grid || !lb) return;
    const items = $$('.gal-card img', grid);
    let idx = 0;
    function show(i) {
      idx = (i + items.length) % items.length;
      const img = items[idx];
      $('#lb-frame').innerHTML = `<img src="${img.src}" alt="${img.alt}">`;
      $('#lb-caption').textContent = img.alt;
      if (G) G.fromTo('#lb-frame', { opacity: 0, scale: .94 }, { opacity: 1, scale: 1, duration: .35, ease: 'power2.out' });
    }
    items.forEach((img, i) => img.closest('.gal-card').onclick = () => {
      lb.hidden = false; show(i);
      if (G) G.fromTo(lb, { opacity: 0 }, { opacity: 1, duration: .25 });
    });
    const close = () => {
      if (G) G.to(lb, { opacity: 0, duration: .2, onComplete: () => { lb.hidden = true; lb.style.opacity = 1; } });
      else lb.hidden = true;
    };
    $('#lb-close').onclick = close;
    $('#lb-prev').onclick = () => show(idx - 1);
    $('#lb-next').onclick = () => show(idx + 1);
    lb.addEventListener('click', e => { if (e.target === lb) close(); });
    document.addEventListener('keydown', e => {
      if (lb.hidden) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft') show(idx + 1);
      if (e.key === 'ArrowRight') show(idx - 1);
    });
  }

  /* ---------------- تقویم شمسی ---------------- */
  const MONTHS = ['فروردین','اردیبهشت','خرداد','تیر','مرداد','شهریور','مهر','آبان','آذر','دی','بهمن','اسفند'];
  const WEEKDAYS = ['شنبه','یکشنبه','دوشنبه','سه‌شنبه','چهارشنبه','پنجشنبه','جمعه'];
  const J_BREAKS = [-61, 9, 38, 199, 426, 686, 756, 818, 1111, 1181, 1210, 1635, 2060, 2097, 2192, 2262, 2324, 2394, 2456, 3178];
  const jdiv = (a, b) => ~~(a / b);
  function jalCal(jy) {
    const bl = J_BREAKS.length, gy = jy + 621;
    let leapJ = -14, jp = J_BREAKS[0], jump = 0;
    for (let i = 1; i < bl; i++) {
      const jm = J_BREAKS[i];
      jump = jm - jp;
      if (jy < jm) break;
      leapJ = leapJ + jdiv(jump, 33) * 8 + jdiv(jump % 33, 4);
      jp = jm;
    }
    let n = jy - jp;
    leapJ = leapJ + jdiv(n, 33) * 8 + jdiv(n % 33 + 3, 4);
    if (jump % 33 === 4 && jump - n === 4) leapJ += 1;
    const leapG = jdiv(gy, 4) - jdiv((jdiv(gy, 100) + 1) * 3, 4) - 150;
    const march = 20 + leapJ - leapG;
    if (jump - n < 6) n = n - jump + jdiv(jump + 4, 33) * 33;
    let leap = (((n + 1) % 33) - 1) % 4;
    if (leap === -1) leap = 4;
    return { leap, gy, march };
  }
  function g2d(gy, gm, gd) {
    let d = jdiv((gy + jdiv(gm - 8, 6) + 100100) * 1461, 4) + jdiv(153 * ((gm + 9) % 12) + 2, 5) + gd - 34840408;
    d = d - jdiv(jdiv(gy + 100100 + jdiv(gm - 8, 6), 100) * 3, 4) + 752;
    return d;
  }
  function d2g(jdn) {
    let j = 4 * jdn + 139361631;
    j = j + jdiv(jdiv(4 * jdn + 183187720, 146097) * 3, 4) * 4 - 3908;
    const i = jdiv((j % 1461), 4) * 5 + 308;
    const gd = jdiv((i % 153), 5) + 1;
    const gm = (jdiv(i, 153) % 12) + 1;
    const gy = jdiv(j, 1461) - 100100 + jdiv(8 - gm, 6);
    return { gy, gm, gd };
  }
  function j2d(jy, jm, jd) {
    const r = jalCal(jy);
    return g2d(r.gy, 3, r.march) + (jm - 1) * 31 - jdiv(jm, 7) * (jm - 7) + jd - 1;
  }
  function d2j(jdn) {
    let gy = d2g(jdn).gy, jy = gy - 621;
    const r = jalCal(jy);
    let jdn1f = g2d(gy, 3, r.march), k, jm, jd;
    k = jdn - jdn1f;
    if (k >= 0) {
      if (k <= 185) { jm = 1 + jdiv(k, 31); jd = (k % 31) + 1; return { jy, jm, jd }; }
      k -= 186;
    } else { jy -= 1; k += 179; if (r.leap === 1) k += 1; }
    jm = 7 + jdiv(k, 30); jd = (k % 30) + 1;
    return { jy, jm, jd };
  }
  const todayJ = d2j(g2d(new Date().getFullYear(), new Date().getMonth() + 1, new Date().getDate()));
  function monthLen(jy, jm) { return jm <= 6 ? 31 : (jm <= 11 ? 30 : (jalCal(jy).leap === 1 ? 30 : 29)); }

  function initCalendar() {
    const grid = $('#cal-grid');
    if (!grid) return;
    let cy = todayJ.jy, cm = todayJ.jm;
    const detail = $('#event-detail');
    const events = window.DATA.events;

    function dayHasEvent(jd) {
      const seed = (cy * 31 + cm * 17 + jd) % 9;
      return seed < 3 ? events[(cy + cm + jd) % events.length] : null;
    }
    function render() {
      $('#cal-month').textContent = MONTHS[cm - 1];
      $('#cal-year').textContent = faNum(cy);
      const first = j2d(cy, cm, 1);
      const firstWd = (first + 1) % 7; // شنبه = 0
      const len = monthLen(cy, cm);
      const prevLen = monthLen(cm === 1 ? cy - 1 : cy, cm === 1 ? 12 : cm - 1);
      let html = '';
      for (let i = 0; i < firstWd; i++) {
        html += `<div class="cal-cell other"><span class="d-num">${faNum(prevLen - firstWd + i + 1)}</span></div>`;
      }
      for (let d = 1; d <= len; d++) {
        const ev = dayHasEvent(d);
        const isToday = cy === todayJ.jy && cm === todayJ.jm && d === todayJ.jd;
        html += `<div class="cal-cell${isToday ? ' today' : ''}" data-day="${d}">
          <span class="d-num">${faNum(d)}</span>
          ${ev ? `<span class="ev"><svg><use href="#${ev.icon}"/></svg><span>${ev.title}</span></span>` : ''}
        </div>`;
      }
      const total = firstWd + len;
      const rest = (7 - total % 7) % 7;
      for (let i = 1; i <= rest; i++) html += `<div class="cal-cell other"><span class="d-num">${faNum(i)}</span></div>`;
      grid.innerHTML = html;

      $$('.cal-cell', grid).forEach(cell => {
        if (!cell.dataset.day) return;
        cell.addEventListener('click', () => {
          $$('.cal-cell').forEach(c => c.classList.remove('selected'));
          cell.classList.add('selected');
          showEvent(+cell.dataset.day);
        });
      });
      // پیش‌فرض: اولین روز دارای رویداد
      const firstEv = $$('.cal-cell .ev').length ? $$('.cal-cell').find(c => c.querySelector('.ev')) : null;
      if (firstEv) firstEv.classList.add('selected');
      showEvent(firstEv ? +firstEv.dataset.day : (cy === todayJ.jy && cm === todayJ.jm ? todayJ.jd : 12));
    }
    function showEvent(day) {
      const ev = dayHasEvent(day) || events[day % events.length];
      const wd = WEEKDAYS[(j2d(cy, cm, day) + 1) % 7];
      if (!detail) return;
      detail.innerHTML = `<article class="event-card">
        <div class="event-date">
          <span class="wd">${wd}</span>
          <span class="dd">${faNum(day)}</span>
          <span class="mm">${MONTHS[cm - 1]}</span>
        </div>
        <div class="event-body">
          <span class="event-icon"><svg><use href="#${ev.icon}"/></svg></span>
          <h3 class="event-title">${ev.title}</h3>
          <div class="event-meta">${ev.wd} · ساعت ${ev.time}</div>
          <p class="event-desc">${ev.desc}</p>
          <div class="event-row">
            <span class="seats-left">${faNum(ev.seats)} صندلی مانده</span>
            <button class="btn btn-red" id="reserve-btn">رزرو صندلی <svg><use href="#i-cal"/></svg></button>
          </div>
        </div>
      </article>`;
      const rb = $('#reserve-btn');
      if (rb) rb.onclick = () => {
        rb.outerHTML = `<span class="btn btn-ghost" style="pointer-events:none">رزرو شد ✓</span>`;
        toast('صندلی‌ات رزرو شد!', 'i-check');
        const card = detail.querySelector('.event-card');
        const stamp = document.createElement('span');
        stamp.className = 'stamp';
        stamp.textContent = 'رزرو شد';
        card.appendChild(stamp);
        if (G) G.fromTo(stamp, { scale: 2.4, rotate: -22, opacity: 0 }, { scale: 1, rotate: -8, opacity: 1, duration: .5, ease: 'back.out(2)' });
      };
    }
    $('#cal-prev').onclick = () => { cm--; if (cm < 1) { cm = 12; cy--; } render(); };
    $('#cal-next').onclick = () => { cm++; if (cm > 12) { cm = 1; cy++; } render(); };
    render();
  }

  /* ---------------- سبد کامل ---------------- */
  function initBagPage() {
    const wrap = $('#bag-items');
    if (!wrap) return;
    const emptyEl = $('#bag-empty');

    function render() {
      const n = cartCount();
      $('#bag-count').textContent = faNum(n) + ' آیتم';
      if (!cart.length) {
        wrap.innerHTML = '';
        emptyEl.hidden = false;
      } else {
        emptyEl.hidden = true;
        wrap.innerHTML = cart.map((i, idx) => {
          const p = byId(i.id) || { name: 'آیتم', img: 'latte.jpg' };
          return `<div class="bag-item">
            <span class="bi-art"><img src="assets/img/${p.img}" alt="${p.name}"></span>
            <div class="bi-info">
              <div class="bi-name">${p.name}</div>
              <div class="bi-sub">${i.sizeName} · ${money(i.price)}</div>
            </div>
            <div class="stepper">
              <button data-inc="${idx}" aria-label="زیاد">+</button><b>${faNum(i.qty)}</b><button data-dec="${idx}" aria-label="کم">−</button>
            </div>
            <div class="bi-price">${money(i.price * i.qty)}</div>
            <button class="bi-remove" data-del="${idx}" aria-label="حذف"><svg><use href="#i-trash"/></svg></button>
          </div>`;
        }).join('');
        $$('[data-inc]', wrap).forEach(b => b.onclick = () => { cart[+b.dataset.inc].qty++; saveCart(); render(); });
        $$('[data-dec]', wrap).forEach(b => b.onclick = () => {
          const i = +b.dataset.dec; cart[i].qty--;
          if (cart[i].qty < 1) cart.splice(i, 1);
          saveCart(); render();
        });
        $$('[data-del]', wrap).forEach(b => b.onclick = () => {
          cart.splice(+b.dataset.del, 1); saveCart(); render(); toast('حذف شد', 'i-trash');
        });
      }
      const items = cartTotal();
      const off = store.get('sc3_coupon', 0) ? Math.round(items * .1) : 0;
      const ship = items >= 300000 || items === 0 ? 0 : SHIP;
      $('#sum-items').textContent = money(items);
      $('#sum-off').textContent = off ? '− ' + money(off) : '۰ تومان';
      $('#sum-ship').textContent = ship ? money(ship) : 'رایگان';
      $('#sum-total').textContent = money(Math.max(0, items - off + ship));
    }
    render();
    window.__scRenderBag = render;

    const cbtn = $('#coupon-btn');
    if (cbtn) cbtn.onclick = () => {
      const code = ($('#coupon').value || '').trim().toUpperCase();
      if (code === 'STRAWBERRY') { store.set('sc3_coupon', 1); toast('کد تخفیف ۱۰٪ اعمال شد', 'i-gift2'); }
      else { store.del('sc3_coupon'); toast('کد معتبر نیست', 'i-x'); }
      render();
    };

    // پیشنهادها
    const sug = $('#bag-suggest');
    if (sug) {
      sug.innerHTML = window.DATA.products.slice(0, 4).map(p => `
        <article class="ph-card">
          <a class="ph-media" href="product-${p.id}.html"><img src="assets/img/${p.img}" alt="${p.name}" loading="lazy"></a>
          <div class="ph-body">
            <div class="ph-top"><h3 class="ph-name"><a href="product-${p.id}.html">${p.name}</a></h3></div>
            <p class="ph-sub">${p.sub}</p>
            <div class="ph-foot">
              <div class="ph-price"><b>${money(p.price)}</b></div>
              <button class="add-btn" data-add="${p.id}" aria-label="افزودن"><svg><use href="#i-plus"/></svg></button>
            </div>
          </div>
        </article>`).join('');
    }
  }

  /* ---------------- تسویه ---------------- */
  function initCheckout() {
    const form = $('#checkout-form');
    if (!form) return;
    const items = $('#co-items');
    function render() {
      if (!cart.length) {
        $('#co-count').textContent = 'سبد خالی';
        items.innerHTML = `<p style="font-size:12.5px;color:var(--muted)">سبدی برای تسویه نیست.</p>`;
        return;
      }
      $('#co-count').textContent = faNum(cartCount()) + ' آیتم';
      items.innerHTML = cart.map(i => {
        const p = byId(i.id) || { name: 'آیتم', img: 'latte.jpg' };
        return `<div class="co-item">
          <img src="assets/img/${p.img}" alt="${p.name}">
          <span class="co-name">${p.name}<br><small class="co-qty">${i.sizeName}</small></span>
          <span class="co-qty">×${faNum(i.qty)}</span>
        </div>`;
      }).join('');
      const t = cartTotal();
      const ship = t >= 300000 ? 0 : SHIP;
      $('#co-items-total').textContent = money(t);
      $('#co-total').textContent = money(t + ship);
    }
    render();

    form.addEventListener('submit', e => {
      e.preventDefault();
      if (!validate(form)) { toast('لطفاً فیلدهای لازم را کامل کن', 'i-x'); return; }
      const data = Object.fromEntries(new FormData(form).entries());
      const order = {
        no: 'SC-' + (1405) + '-' + String(Math.floor(Math.random() * 9000) + 1000),
        items: cart.slice(),
        total: cartTotal() + (cartTotal() >= 300000 ? 0 : SHIP),
        name: data.name, phone: data.phone, address: data.address,
        time: data.time, pay: data.pay, gift: !!data.gift,
        date: `${faNum(todayJ.jd)} ${MONTHS[todayJ.jm - 1]} ${faNum(todayJ.jy)}`,
      };
      store.set('sc3_lastorder', order);
      const btn = $('#pay-btn');
      btn.innerHTML = 'در حال ثبت…';
      setTimeout(() => { window.location.href = 'thanks.html'; }, 700);
    });
  }

  /* ---------------- صفحه تشکر ---------------- */
  function initThanks() {
    const box = $('#receipt');
    if (!box) return;
    const order = store.get('sc3_lastorder', null);
    if (!order) {
      box.innerHTML = `<p style="font-size:13px;color:var(--muted);text-align:center">سفارشی ثبت نشده است.</p>`;
      return;
    }
    $('#order-no').textContent = order.no;
    box.innerHTML = order.items.map(i => {
      const p = byId(i.id) || { name: 'آیتم' };
      return `<div class="receipt-row"><span>${p.name} · ${i.sizeName} ×${faNum(i.qty)}</span><b>${money(i.price * i.qty)}</b></div>`;
    }).join('') + `
      <div class="receipt-row"><span>ارسال</span><b>${order.total - order.items.reduce((s, i) => s + i.price * i.qty, 0) === 0 ? 'رایگان' : money(SHIP)}</b></div>
      <div class="receipt-row"><span>زمان تحویل</span><b>${order.time}</b></div>
      <div class="receipt-row"><span>نشانی</span><b style="font-size:11.5px;max-width:60%;text-align:left">${order.address}</b></div>
      <div class="receipt-total"><span>قابل پرداخت</span><b>${money(order.total)}</b></div>`;

    // کانفتی
    const conf = $('#confetti');
    const colors = ['#E23E4E', '#F58CA0', '#2FA08C', '#F7C948', '#FBD3DC'];
    for (let i = 0; i < 48; i++) {
      const el = document.createElement('i');
      el.style.left = Math.random() * 100 + '%';
      el.style.background = colors[i % colors.length];
      conf.appendChild(el);
    }
    if (G) {
      G.fromTo('#confetti i', { y: -30, opacity: 1, rotate: 0 }, {
        y: window.innerHeight + 80, opacity: 0,
        rotate: () => G.utils.random(360, 720),
        duration: () => G.utils.random(1.8, 3),
        stagger: { each: .03, from: 'random' }, ease: 'power1.in',
      });
      G.fromTo('.thanks-building', { scale: .9, opacity: 0 }, { scale: 1, opacity: 1, duration: .8, ease: 'back.out(1.4)' });
      G.fromTo('.bunting-overlay.show', { opacity: 0, y: -12 }, { opacity: 1, y: 0, duration: .7, delay: .4 });
    }
    // سبد خالی شود
    cart = []; store.set('sc3_cart', []); updateCartUI();
  }

  /* ---------------- فرم‌ها ---------------- */
  function validate(form) {
    let ok = true;
    $$('input[required], textarea[required]', form).forEach(f => {
      const field = f.closest('.field') || f.closest('.check');
      const err = field && field.querySelector('.field-err');
      let bad = !f.value.trim();
      if (f.type === 'email' && f.value && !/^\S+@\S+\.\S+$/.test(f.value)) bad = true;
      if (f.type === 'tel' && f.value && f.value.replace(/\D/g, '').length < 10) bad = true;
      if (f.minLength > 0 && f.value && f.value.length < f.minLength) bad = true;
      if (f.type === 'checkbox' && !f.checked) bad = true;
      if (field && field.classList.contains('field')) field.classList.toggle('has-error', bad);
      if (err) err.textContent = bad ? 'این فیلد را درست پر کن' : '';
      if (bad) ok = false;
    });
    return ok;
  }

  function initForms() {
    // نمایش/مخفی کردن رمز
    $$('.pass-toggle').forEach(b => b.onclick = () => {
      const inp = document.getElementById(b.dataset.pass);
      if (!inp) return;
      inp.type = inp.type === 'password' ? 'text' : 'password';
    });
    // قدرت رمز
    const pass = $('#reg-pass'), bar = $('#pass-bar');
    if (pass && bar) pass.addEventListener('input', () => {
      const v = pass.value;
      let s = 0;
      if (v.length >= 6) s++;
      if (/[A-Z]/.test(v) || /[آ-ی]/.test(v)) s++;
      if (/\d/.test(v)) s++;
      if (/[^A-Za-z0-9آ-ی]/.test(v)) s++;
      bar.style.width = (s * 25) + '%';
      bar.style.background = s <= 1 ? '#E23E4E' : s === 2 ? '#F7C948' : '#2FA08C';
    });

    const loginForm = $('#login-form');
    if (loginForm) loginForm.addEventListener('submit', e => {
      e.preventDefault();
      if (!validate(loginForm)) return;
      toast('خوش برگشتی! (نمونه)', 'i-check');
      setTimeout(() => window.location.href = 'index.html', 900);
    });

    const regForm = $('#register-form');
    if (regForm) regForm.addEventListener('submit', e => {
      e.preventDefault();
      if (!validate(regForm)) { toast('فرم را کامل کن', 'i-x'); return; }
      const d = Object.fromEntries(new FormData(regForm).entries());
      store.set('sc3_user', { name: d.fname, phone: d.phone });
      toast('حسابت ساخته شد، ۵۰ امتیاز هدیه گرفتی!', 'i-gift2');
      setTimeout(() => window.location.href = 'index.html', 1100);
    });

    const cForm = $('#contact-form');
    if (cForm) cForm.addEventListener('submit', e => {
      e.preventDefault();
      if (!validate(cForm)) { toast('فیلدها را کامل کن', 'i-x'); return; }
      cForm.reset();
      toast('پیامت رسید، به‌زودی جواب می‌دهیم');
    });

    $$('[data-newsletter]').forEach(f => f.addEventListener('submit', e => {
      e.preventDefault();
      const inp = f.querySelector('input');
      if (!inp.value || !/^\S+@\S+\.\S+$/.test(inp.value)) { toast('ایمیل درست نیست', 'i-x'); return; }
      inp.value = '';
      toast('عضو خبرنامه شدی!', 'i-mail');
    }));
  }

  /* ---------------- نوار مطالعه ---------------- */
  function initReadbar() {
    const bar = $('#readbar');
    if (!bar) return;
    const upd = () => {
      const h = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.width = h > 0 ? Math.min(100, (window.scrollY / h) * 100) + '%' : '0%';
    };
    window.addEventListener('scroll', upd, { passive: true });
    upd();
  }

  /* ---------------- راه‌اندازی ---------------- */
  function boot() {
    initHeader();
    updateCartUI();
    initMenuFilters();
    initArticleFilters();
    initProductPage();
    initGallery();
    initCalendar();
    initBagPage();
    initCheckout();
    initThanks();
    initForms();
    initReadbar();
    if (pageNeedsBagRender && window.__scRenderBag) window.__scRenderBag();
  }
  const pageNeedsBagRender = PAGE === 'bag';

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();

  // برای دسترسی motion.js
  window.SC = { toast, addToCart, cartCount, openDrawer, closeDrawer, PRODUCTS };
})();
