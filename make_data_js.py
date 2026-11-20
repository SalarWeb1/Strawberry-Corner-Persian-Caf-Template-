#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""تولید js/data.js از src/data.py — بعد از هر تغییر در داده‌ها اجرا کن."""
import io, json, os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, 'src'))
os.chdir(ROOT)
from data import PRODUCTS, ARTICLES, GALLERY, EVENTS

prods = [dict(id=p['id'], name=p['name'], cat=p['cat'], img=p['img'], price=p['price'],
              sub=p['sub'], sizes=[[a, b] for a, b in p['sizes']]) for p in PRODUCTS]
arts = [dict(slug=a['slug'], title=a['title'], cat=a['cat'], img=a['img']) for a in ARTICLES]
gal = [[g[0], g[1]] for g in GALLERY]
evs = [dict(icon=e['icon'], title=e['title'], wd=e['wd'], time=e['time'],
            desc=e['desc'], seats=e['seats']) for e in EVENTS]

js = "window.DATA = " + json.dumps(
    dict(products=prods, articles=arts, gallery=gal, events=evs),
    ensure_ascii=False, indent=1) + ";\n"

with io.open('js/data.js', 'w', encoding='utf-8') as f:
    f.write(js)
print('✓ js/data.js ساخته شد')
