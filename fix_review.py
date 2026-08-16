# -*- coding: utf-8 -*-
import json, re, glob, os

site = os.path.dirname(os.path.abspath(__file__))
dj = os.path.join(site, 'i18n-dict.json')
d = json.load(open(dj, encoding='utf-8'))

# ---- 1. Dict EN fixes ----
en_fix = {
 "Caps designed in China · A brand of our own": "Caps designed in China",
 "wearing it is the statement": "just wear it",
 "Quality is the attitude": "Quality speaks for itself",
 "The fit, decides everything.": "Fit is everything.",
 "Up, always up.": "Up, just up.",
 "The voice of Hong Kong and Macao, is the voice of China, too.": "From Hong Kong and Macao, same roots.",
}
en_exact = {"态度": "Energy"}
en_fix_hits = 0
for k, v in d.items():
    if not isinstance(v, dict): continue
    en = v.get('en','')
    for old, new in en_fix.items():
        if old in en:
            v['en'] = en.replace(old, new); en_fix_hits += 1
    if k in en_exact and v.get('en') == "Attitude":
        v['en'] = en_exact[k]; en_fix_hits += 1

# ---- 2. Dict key renames (slogans zh) ----
renames = {"版型，定生死。": ("版型，为先。","版型，為先。"),
           "向上，永远向上。": ("向上，只管向上。","向上，只管向上。")}
ren_hits = 0
for old,(nz,nt) in renames.items():
    if old in d:
        v = d.pop(old)
        v['en'] = "Fit is everything." if "版型" in nz else "Up, just up."
        d[nz] = v; ren_hits += 1
        if isinstance(v, dict) and 'zh-Hant' in v: v['zh-Hant'] = nt

json.dump(d, open(dj,'w',encoding='utf-8'), ensure_ascii=False, indent=1)
import shutil; shutil.copy(dj, os.path.join(site,'dist','i18n-dict.json'))

# ---- 3. HTML fixes (root + dist) ----
zh_fix = {
 "中国人自己的帽饰品牌。把中国文化的图腾，戴在头上。":"中国帽子本土设计。把中国文化的纹样，戴在头上。",
 "SHER12 — 中国人自己的帽饰品牌":"SHER12 — 中国帽子本土设计",
 "中国人自己的帽饰品牌":"中国帽子本土设计",
 "版型，定生死。":"版型，为先。","版型定生死":"版型为先",
 "向上，永远向上。":"向上，只管向上。",
 "最直接的文化表达":"文化，不言而喻",
 "SHER logo 醒目印花":"SHER 印花","醒目印花":"印花","刺绣点睛":"刺绣",
 "戴上就是表态":"戴上就好","品质之选":"款","百搭之选":"百搭",
 "打破常规":"不落俗套","出行无忧":"出行常备","帽子焕新":"帽子如新",
 "野性十足":"一抹野性","毛屑灰尘全走":"干净利落",
 "大湾区的心声":"根在南方","比数字编号更懂中国人":"不多不少",
 "一针一线绣在帽子上":"绣在帽子上","中国文化的图腾":"中国文化的纹样",
}
html_files = sorted(glob.glob(os.path.join(site,'*.html'))) + sorted(glob.glob(os.path.join(site,'dist','*.html')))
html_hits = {}
for f in html_files:
    c = open(f, encoding='utf-8').read(); orig = c; n = 0
    for old, new in zh_fix.items():
        if old in c: n += c.count(old); c = c.replace(old, new)
    if c != orig:
        open(f,'w',encoding='utf-8').write(c); html_hits[os.path.relpath(f, site)] = n

# ---- 4. Check data-i18n-html attr keys still match dict ----
miss = 0
for f in glob.glob(os.path.join(site,'*.html')):
    c = open(f, encoding='utf-8').read()
    for key in re.findall(r'data-i18n-html="([^"]+)"', c):
        if key not in d: miss += 1

print(f"EN fixes: {en_fix_hits}, key renames: {ren_hits}, html files changed: {len(html_hits)}, attr-key misses: {miss}")
