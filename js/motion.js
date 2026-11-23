/* ============================================================
   گوشه توت‌فرنگی — motion.js (نسخه ۳)
   همه‌ی انیمیشن‌های GSAP. اگر GSAP نباشد، سایت سالم کار می‌کند.
   ============================================================ */
(function () {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const G = window.gsap;
  const REDUCED = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const FINE = window.matchMedia('(hover:hover) and (pointer:fine)').matches;
  if (!G || REDUCED) { document.documentElement.classList.add('no-motion'); return; }

  const PAGE = document.body.dataset.page;

  /* ---------- 1) ورود صفحه ---------- */
  function pageEnter() {
    const main = $('#main');
    if (!main) return;
    G.fromTo(main, { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: .55, ease: 'power2.out', clearProps: 'transform,opacity' });

    // هدر
    G.fromTo('.header-inner > *', { opacity: 0, y: -12 }, { opacity: 1, y: 0, duration: .5, stagger: .07, ease: 'power2.out', delay: .05, clearProps: 'transform,opacity' });
  }

  /* ---------- 2) خروج نرم صفحه (ترنزیشن واقعی بین صفحه‌ها) ---------- */
  function pageExit() {
    document.addEventListener('click', e => {
      const a = e.target.closest('a[href]');
      if (!a) return;
      const href = a.getAttribute('href');
      if (!href || href.startsWith('#') || href.startsWith('http') || href.startsWith('mailto') ||
          href.startsWith('tel') || a.target === '_blank' || e.metaKey || e.ctrlKey) return;
      e.preventDefault();
      const veil = document.createElement('div');
      veil.style.cssText = 'position:fixed;inset:0;background:var(--cream);z-index:400;opacity:0;pointer-events:none;';
      document.body.appendChild(veil);
      G.timeline({ onComplete: () => { window.location.href = href; } })
        .to('#main', { opacity: 0, y: -14, duration: .25, ease: 'power2.in' }, 0)
        .to(veil, { opacity: 1, duration: .3, ease: 'power2.in' }, 0)
        .set(veil, { pointerEvents: 'auto' });
    });
  }

  /* ---------- 3) ریویل هنگام اسکرول ---------- */
  function scrollReveal() {
    if (!('IntersectionObserver' in window)) return;
    const SEL = '.ph-card, .art-card, .quote-card, .gal-card, .gal-item, .value-card, .contact-card, ' +
                '.strip-item, .mini-item, .good-item, .bag-item, .cal-cell, .timeline li, .featured-article, ' +
                '.events-side > *, .story-media, .story-copy > *, .ph-card, .article-body > *, .ph-badge';
    const io = new IntersectionObserver(entries => {
      entries.forEach(en => {
        if (!en.isIntersecting) return;
        const el = en.target;
        io.unobserve(el);
        if (el.dataset.shown) return;
        el.dataset.shown = '1';
        const parent = el.parentElement;
        const idx = parent ? [...parent.children].indexOf(el) : 0;
        G.fromTo(el, { opacity: 0, y: 30 }, {
          opacity: 1, y: 0, duration: .6, ease: 'power3.out',
          delay: Math.min(idx, 7) * .05, clearProps: 'transform,opacity',
        });
      });
    }, { rootMargin: '0px 0px -6% 0px', threshold: .06 });
    $$(SEL).forEach(el => io.observe(el));
  }

  /* ---------- 4) خانه: تیتر و کارت‌ها ---------- */
  function homeIntro() {
    if (PAGE !== 'home') return;
    const title = $('.hero-title');
    if (title && !title.dataset.split) {
      title.dataset.split = '1';
      title.innerHTML = title.innerHTML.split(/<br\s*\/?>/i)
        .map(line => `<span class="ht-line">${line.trim().split(/\s+/).map(w => `<span class="ht-w">${w}</span>`).join(' ')}</span>`)
        .join('<br>');
    }
    const words = $$('.hero-title .ht-w');
    if (words.length) {
      G.fromTo(words, { yPercent: 115, opacity: 0, rotate: 5 },
        { yPercent: 0, opacity: 1, rotate: 0, duration: .9, stagger: .07, ease: 'power4.out', delay: .15 });
    }
    G.fromTo('.side-menu .side-btn', { x: 40, opacity: 0 },
      { x: 0, opacity: 1, duration: .5, stagger: .06, delay: .35, ease: 'power3.out', clearProps: 'transform,opacity' });
    G.fromTo('.hero-cards > *', { x: -34, opacity: 0 },
      { x: 0, opacity: 1, duration: .65, stagger: .09, delay: .25, ease: 'power3.out', clearProps: 'transform,opacity' });
    G.fromTo('.building-art', { scale: .9, opacity: 0, y: 20 },
      { scale: 1, opacity: 1, y: 0, duration: .9, delay: .1, ease: 'back.out(1.3)', clearProps: 'transform,opacity' });
    $$('.float-art').forEach((f, i) => {
      G.fromTo(f, { scale: 0, opacity: 0, rotate: -40 },
        { scale: 1, opacity: 1, rotate: 0, duration: .7, delay: .6 + i * .12, ease: 'back.out(2)' });
    });
    G.fromTo('.mini-card', { y: 24, opacity: 0, rotate: -3 },
      { y: 0, opacity: 1, rotate: 0, duration: .7, delay: .55, ease: 'back.out(1.5)', clearProps: 'transform,opacity' });

    // شناوری آرام ساختمان
    const b = $('.building-art');
    if (b) G.to(b, { y: -7, duration: 3.6, yoyo: true, repeat: -1, ease: 'sine.inOut' });
  }

  /* ---------- 5) تیتر صفحات داخلی ---------- */
  function innerHead() {
    if (PAGE === 'home') return;
    const h = $('.page-title, .article-head h1, .p-name, .auth-card h1, .thanks-card h1, .notfound h1');
    if (h) G.fromTo(h, { y: 26, opacity: 0 }, { y: 0, opacity: 1, duration: .7, ease: 'power3.out', delay: .1, clearProps: 'transform,opacity' });
    const kick = $('.kicker');
    if (kick) G.fromTo(kick, { opacity: 0, x: 16 }, { opacity: 1, x: 0, duration: .55, delay: .25, clearProps: 'transform,opacity' });
  }

  /* ---------- 6) مغناطیسی ---------- */
  function magnetic() {
    if (!FINE) return;
    $$('.btn, .add-btn, .filter-pill, .side-btn, .size-opt').forEach(el => {
      if (el.dataset.mag) return;
      el.dataset.mag = '1';
      el.addEventListener('mousemove', e => {
        const r = el.getBoundingClientRect();
        G.to(el, {
          x: ((e.clientX - r.left) / r.width - .5) * 10,
          y: ((e.clientY - r.top) / r.height - .5) * 8,
          duration: .35, ease: 'power2.out',
        });
      });
      el.addEventListener('mouseleave', () => G.to(el, { x: 0, y: 0, duration: .55, ease: 'elastic.out(1,.45)' }));
    });
  }

  /* ---------- 7) تیلت کارت‌ها ---------- */
  function tilt() {
    if (!FINE) return;
    $$('.ph-card, .quote-card, .gal-card, .contact-card, .value-card').forEach(el => {
      if (el.dataset.tilt) return;
      el.dataset.tilt = '1';
      el.addEventListener('mousemove', e => {
        const r = el.getBoundingClientRect();
        const px = (e.clientX - r.left) / r.width - .5;
        const py = (e.clientY - r.top) / r.height - .5;
        G.to(el, {
          rotateY: px * 9, rotateX: -py * 9, transformPerspective: 900,
          duration: .4, ease: 'power2.out',
        });
      });
      el.addEventListener('mouseleave', () => G.to(el, { rotateX: 0, rotateY: 0, duration: .6, ease: 'power3.out' }));
    });
  }

  /* ---------- 8) گلبرگ‌ها ---------- */
  function petals() {
    const layer = document.createElement('div');
    layer.style.cssText = 'position:fixed;inset:0;pointer-events:none;z-index:1;overflow:hidden';
    document.body.appendChild(layer);
    const colors = ['#F58CA0', '#FBD3DC', '#E23E4E', '#F7C948'];
    const n = window.innerWidth < 760 ? 6 : 11;
    for (let i = 0; i < n; i++) {
      const s = 10 + Math.random() * 13;
      const p = document.createElement('span');
      p.style.cssText = `position:absolute;top:-40px;left:${Math.random() * 100}%;width:${s}px;height:${s * .84}px;opacity:0`;
      p.innerHTML = `<svg viewBox="0 0 24 20"><path d="M12 1c5 0 11 5 11 9 0 5-5 9-11 9S1 15 1 10C1 6 7 1 12 1z" fill="${colors[i % colors.length]}" opacity=".8"/></svg>`;
      layer.appendChild(p);
      (function drop() {
        G.fromTo(p, { y: -60, rotate: G.utils.random(-40, 40), opacity: 0 },
          {
            y: window.innerHeight + 80, x: G.utils.random(-110, 110),
            rotate: G.utils.random(-240, 240), opacity: .5,
            duration: 12 + Math.random() * 10, ease: 'none', delay: Math.random() * 12,
            onComplete: () => { G.set(p, { y: -60, x: 0 }); drop(); },
          });
      })();
    }
  }

  /* ---------- 9) شمارنده‌ها ---------- */
  function counters() {
    $$('.hero-stats b, .story-stats b').forEach(el => {
      const raw = el.textContent.trim();
      const num = parseInt(raw.replace(/[^\d۰-۹]/g, '').replace(/[۰-۹]/g, d => '۰۱۲۳۴۵۶۷۸۹'.indexOf(d)), 10);
      if (!num || raw.includes('٫')) return;
      const prefix = raw.match(/^[+]|^[۰-۹]*/)[0].includes('+') ? '+' : '';
      const suffix = raw.replace(/[\d۰-۹٬+]/g, '');
      const obj = { v: 0 };
      G.to(obj, {
        v: num, duration: 1.4, ease: 'power2.out', delay: .4,
        onUpdate: () => { el.textContent = prefix + Math.round(obj.v).toLocaleString('fa-IR') + suffix; },
      });
    });
  }

  /* ---------- 10) نشانگر ماوس ---------- */
  function cursor() {
    if (!FINE) return;
    const ring = document.createElement('div');
    ring.id = 'sc-cursor';
    ring.style.cssText = `position:fixed;top:0;left:0;width:28px;height:28px;border-radius:50%;
      border:1.5px solid rgba(226,62,78,.5);pointer-events:none;z-index:390;
      transform:translate(-50%,-50%);opacity:0;transition:width .25s,height .25s,background .25s`;
    document.body.appendChild(ring);
    const xTo = G.quickTo(ring, 'x', { duration: .4, ease: 'power3' });
    const yTo = G.quickTo(ring, 'y', { duration: .4, ease: 'power3' });
    window.addEventListener('mousemove', e => {
      ring.style.opacity = 1; xTo(e.clientX); yTo(e.clientY);
    });
    document.addEventListener('mouseover', e => {
      const hot = e.target.closest('a,button,.ph-card,.gal-card,input,textarea');
      ring.style.width = ring.style.height = hot ? '54px' : '28px';
      ring.style.background = hot ? 'rgba(226,62,78,.08)' : 'transparent';
    });
  }

  /* ---------- 11) دوای تکمه‌های افزودن ---------- */
  function addPulse() {
    document.addEventListener('click', e => {
      const btn = e.target.closest('.add-btn, .btn-red');
      if (!btn) return;
      G.fromTo(btn, { scale: 1 }, { scale: .92, duration: .1, yoyo: true, repeat: 1, ease: 'power2.inOut' });
    }, true);
  }

  /* ---------- راه‌اندازی ---------- */
  function boot() {
    pageEnter();
    pageExit();
    homeIntro();
    innerHead();
    scrollReveal();
    magnetic();
    tilt();
    petals();
    counters();
    cursor();
    addPulse();
    // دوباره بعد از رندر داینامیک
    setTimeout(() => { scrollReveal(); magnetic(); tilt(); }, 900);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
