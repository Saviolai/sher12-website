#!/usr/bin/env python3
"""把 i18n-dict.json 的 en 字段从美式英语改为英式/国际英语"""
import json, io, html, re

def norm(s):
    s = html.unescape(s)
    return re.sub(r'\s+', ' ', s).strip()

# 英式英语替换：key = 当前 en 值（归一化后），value = 新的英式版本
BRITISH = {
    # 颜色拼写 -or → -our
    "Color": "Colour",
    "Three colors: Peach Bloom, Chestnut, Bamboo Green.": "Three colours: Peach Bloom, Chestnut, Bamboo Green.",
    "Every city has its own color and temper. Wear it on your head.": "Every city has its own colour and temper. Wear it on your head.",

    # 口语风格 → 英式表达
    "Wanna talk?": "Fancy a chat?",

    # 美式俚语 → 国际正式
    "Custom, wholesale, collabs \u2014 or you just want to say hi. All welcome.": "Bespoke, wholesale, collaborations \u2014 or you simply fancy a chat. All welcome.",

    # crew → community（美式街头俚语 → 国际正式）
    "SHER12 is more than a cap. We're a crew who believe Chinese design deserves a place on your head. Join us \u2014 be first to know about every drop.": "SHER12 is more than a cap. We're a community who believe Chinese design deserves a place on your head. Join us \u2014 be the first to know about every release.",

    # collabs → collaborations
    "42 caps. From culture to collabs, flat-brim to curved \u2014 one of them is yours.": "42 caps. From culture to collaborations, flat-brim to curved \u2014 one of them is yours.",

    # "on hand" → "handy"（英式偏好）
    "Wrinkles gone in 30 seconds. Spray \u2014 creases smooth out on their own. Keep one on hand wherever you go.": "Wrinkles gone in 30 seconds. Spray \u2014 creases smooth out naturally. Keep one handy, wherever you go.",
    "Wrinkles gone in 30 seconds. Spray \u2014 creases smooth out on their own.": "Wrinkles gone in 30 seconds. Spray \u2014 creases smooth out naturally.",

    # Store → Shop（与 门店=Shop 保持一致）
    "Store": "Shop",

    # "gets ... better" → "understands ... better"（更国际正式）
    "We define caps in our own language. Four silhouettes, four clasps \u2014 a system that gets Chinese wearers better than any number code.": "We define caps in our own language. Four silhouettes, four clasps \u2014 a system that understands Chinese wearers better than any number code.",

    # "always on point" → "always spot on"（英式表达）
    "Curved-brim with Velcro \u2014 all Xuan Black, goes with everything. Adjustable, always on point.": "Curved-brim with Velcro \u2014 all Xuan Black, goes with everything. Adjustable, always spot on.",

    # "pure wild" → "purely wild"（语法更正确）
    "Snake-skin print with red-blue contrast \u2014 pure wild.": "Snake-skin print with red-blue contrast \u2014 purely wild.",

    # "say hi" → "say hello"
    # already handled in the "Custom, wholesale..." line above

    # "won't get up, won't work, always buffering" → fine, keep as is (international)

    # "sweet and dreamy" → fine
    # "Art-toy IP \u00d7 cap culture." → fine

    # "A dog forever loading laziness" → fine, poetic

    # "Caps on, we carve our own world" → fine
    # "Caps on, we carve our own world." → fine (with period)

    # "Home Turf" → fine, used in British English

    # "Wear it \u2014 that's the statement." → fine

    # "Water-free cap cleaner" → fine
    # "Water-Free / Foam Pump" → fine

    # "A clean cap, a sharper you." → fine

    # "Less is more \u2014 simplicity is power." → fine

    # "Fit decides everything." → fine

    # "love needs no translation" → fine

    # "Up, always up." → fine

    # "Peace, turned upside down." → fine

    # "The peace you can't see \u2014 that's real peace." → fine
    # "The peace you can't see is the real peace." → fine

    # "Twelve is everything." → fine

    # "Not a random number \u2014 a code carved into Chinese culture." → fine

    # "Once you're here, you're a Shenzhener." → fine

    # "Stitching Chinese cultural totems onto caps, thread by thread." → fine

    # "A Chinese cap brand of our own" → fine

    # "Chinese caps, designed at home \u00b7 A cap brand of our own" → fine

    # "Buy In-Store" → "Buy In-Shop" (British)
    'Buy In-Store \u00b7 OCT "Sandian"': 'Buy In-Shop \u00b7 OCT "Sandian"',

    # "Try On In-Store" → "Try On In-Shop"
    'Try On In-Store \u00b7 101E, F1, OCT-LOFT South, Nanshan, Shenzhen \u2014 "Sandian"': 'Try On In-Shop \u00b7 101E, F1, OCT-LOFT South, Nanshan, Shenzhen \u2014 "Sandian"',

    # "LIVE" → fine (universal)
    # "More +" → fine
    # "All" → fine
    # "More Styles" → fine
    # "Learn More" → fine
    # "More Accessories" → fine

    # "View Series" → fine
    # "View All Type Ding" → fine etc.

    # "About the Brand" → fine

    # "Join SHER12 CLUB" → fine

    # "Our Caps" → fine
    # "Our Caps" → fine

    # "Every cap, made for you" → fine

    # "Good caps need care." → fine

    # "Pump, wipe, fresh again." → fine

    # "One light sweep \u2014 lint and dust gone." → fine

    # "Replaceable Sponge Head" → fine
    # "Wave-Grip Handle" → fine
    # "Brush Head" → fine
    # "Lint Removal / Dusting" → fine

    # "Water-based, gentle cleaning" → fine
    # "Water-Free / Foam Pump" → fine

    # "Brown SHER Webbing" → fine
    # "Green SHER Webbing" → fine
    # "Pink SHER Webbing" → fine
    # "SHER Webbing" → fine

    # "Silver metal bar buckle with 12 at the clasp." → fine
    # "Brown SHER cross-webbing lining." → fine

    # "Heart SHER embroidery up front" → fine

    # "closed, non-adjustable" → fine
    # "Closed, Non-Adjustable" → fine
    # "0 Closed" → fine

    # "Plastic Back Clasp" → fine
    # "Metal Bar Buckle" → fine
    # "Metal Snap Clasp" → fine
    # "Metal Snap" → fine
    # "Plastic Clasp" → fine

    # "Reversible bucket" → fine
    # "Reversible \u00b7 Bucket Hat" → fine
    # "Bucket Hat \u00b7 Reversible" → fine

    # "5-panel cap" → fine
    # "5-Panel Flat-Brim" → fine

    # "Flat-Brim Cap" → fine
    # "Curved-Brim Cap" → fine
    # "Bucket Hat" → fine
    # "Melon Cap" → fine

    # "Sky Azure" → fine
    # "Pale Azure" → fine
    # "Pale Cyan" → fine
    # "Xuan Black" → fine
    # "Ink" → fine
    # "Ochre" → fine (already British spelling!)
    # "Chestnut" → fine
    # "Peach Bloom" → fine
    # "Bamboo Green" → fine
    # "Cinnabar" → fine
    # "Crabapple" → fine
    # "Wisteria" → fine
    # "Moon White" → fine
    # "Jade Dark" → fine

    # "Grey" → already British! Good.
    # "White / Grey Blue" → fine

    # "Light Khaki" → fine
    # "Khaki / Gold Embroidery" → fine
    # "Wine / Gold Embroidery" → fine
    # "Wine" → fine (colour name)
    # "Gold / Full Print" → fine
    # "Cream / Brown" → fine
    # "Cream / Green" → fine
    # "Cream / Pink" → fine
    # "Pink / White" → fine
    # "Red / Blue" → fine
    # "Black / White Print" → fine
    # "Black / White Embroidery" → fine
    # "Xuan Black / White Embroidery" → fine
    # "White / Blue" → fine

    # "Candy Green & Purple" → fine
    # "Wisteria Purple" → fine
    # "Antique Green" → fine
    # "Tan" → fine

    # "Unbowed" → fine
    # "Instinct" → fine
    # "Power" → fine
    # "Spirit" → fine
    # "Freedom" → fine
    # "Romance" → fine
    # "Belonging" → fine
    # "Attitude" → fine
    # "Wild Side" → fine
    # "Voice" → fine
    # "Everything" → fine
    # "Translation" → fine
    # "Business" → fine
    # "Real Peace" → fine
    # "Your Head" → fine
    # "Name" → fine
    # "Mood" → fine
    # "Yourself" → fine
    # "Life or Death" → fine
    # "Up" → fine
    # "Shenzhener" → fine
    # "Hometown" → fine
    # "Home Turf" → fine

    # "Street Dance" → fine
    # "Street dance and caps \u2014 the same attitude." → fine
    # "Street-dance collab, Jia24 fit \u2014 the flat brim stays true to the streets." →
    # "collab" → "collaboration"
    "Street-dance collab, Jia24 fit \u2014 the flat brim stays true to the streets.": "Street-dance collaboration, Jia24 fit \u2014 the flat brim stays true to the streets.",

    # "Pixelated mosaic SHER print \u2014 cap expression for the digital age." → fine
    # "Pixels, the romance of the digital age." → fine

    # "Peace \u2014 the blue edition. Peace, re-expressed." → fine
    # "Peace \u2014 all Ink, composed." → fine

    # "Green crown, white \"\u767c\" across the cap; under the brim: \"\u751f\u8d22\u6709\u9053\". This cap hides a swear word \u2014 but only you know it." → fine

    # "Up, always up. 8848.86m \u2014 the height of a mountain, the height of an attitude." → fine

    # "Two moods, one cap." → fine

    # "Quality is the attitude." → fine

    # "Fit decides everything." → fine

    # "love needs no translation; wearing it is the statement." → fine

    # "The fit, decides everything." → fine (poetic)

    # "Adjustable, is freedom." → fine

    # "Dreaming, is serious business." → fine

    # "Roar it out, don't hold it in." → fine

    # "Sign it, with your name." → fine

    # "Unleash, your wild side." → fine

    # "Wear \"China\" on your head." → fine

    # "Culture, stated directly." → fine

    # "breaking convention." → fine

    # "romantic and mysterious." → fine

    # "calm and composed." → fine

    # "retro and warm." → fine

    # "understated." → fine

    # "clean street style." → fine

    # "function meets style." → fine

    # "goes with everything." → fine (already in "Adjustable, always spot on." line)

    # "the metal buckle, for those who care about quality." → fine (×2)

    # "a closed silhouette." → fine

    # "Peace in another form." → fine

    # "Two sides, two moods." → fine (poetic)

    # "Take care of your cap, and you take care of yourself." → fine

    # "A clean cap, a sharper you." → fine

    # "Less is more \u2014 simplicity is power." → fine

    # "The fit, decides everything." → fine

    # "Not a random number \u2014 a code carved into Chinese culture." → fine

    # "\"Twelve\" embroidery \u2014 twelve is everything." → fine
    # "\"Cap\" has 12 strokes; \"China\" has 12." → fine
    # "12 hours make a day cycle, 12 months make a year." → fine

    # "Stitching Chinese cultural totems onto caps, thread by thread." → fine

    # "A Chinese cap brand of our own" → fine

    # "Chinese caps, designed at home \u00b7 A cap brand of our own" → fine
    # Note: "designed at home" could mean "designed domestically" — let me check the Chinese
    # 中国帽子本土设计 → "Chinese caps, designed at home" — "at home" here means "domestically/in China"
    # Better: "Chinese caps, designed locally" or "Chinese caps, domestically designed"
    # Actually "designed at home" is fine and warm in British English
    # But let me change it to be clearer:
    "Chinese caps, designed at home \u00b7 A cap brand of our own": "Chinese caps, designed at home \u00b7 A cap brand of our own",
    # This one is fine, keep as is

    # "WeChat: CapTure_by_SHER12" → fine
    # "Xiaohongshu @Sher12" → fine
    # "WeChat: sher12cap" → fine

    # "Bespoke, wholesale, collaborations \u2014 or you simply fancy a chat. All welcome." → already updated above

    # Address lines → fine

    # "Want to try them on? We stock at a shop called \"Sandian\" in Shenzhen OCT." → fine

    # "Every cap, made for you" → fine

    # "42 caps. From culture to collaborations, flat-brim to curved \u2014 one of them is yours." → already updated

    # "Our Caps" → fine

    # Product descriptions with "colors" → already handled
}

path = 'i18n-dict.json'
with io.open(path, encoding='utf-8') as f:
    d = json.load(f)

# Build normalized lookup for BRITISH keys
british_norm = {norm(k): v for k, v in BRITISH.items()}

updated = 0
not_found = []
for k, v in d.items():
    en = v.get('en', '')
    nk = norm(en)
    if nk in british_norm:
        v['en'] = british_norm[nk]
        updated += 1
    elif en in BRITISH:
        v['en'] = BRITISH[en]
        updated += 1

with io.open(path, 'w', encoding='utf-8', newline='') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
    f.write('\n')

print('英式英语更新: %d 条' % updated)

# 验证
verify = ['Color', 'Wanna talk?', 'collabs', 'on hand', 'crew who believe']
with io.open(path, encoding='utf-8') as f:
    d2 = json.load(f)
remaining = []
for k, v in d2.items():
    en = v.get('en', '')
    for term in verify:
        if term in en:
            remaining.append((term, en[:80]))
if remaining:
    print('仍有美式残留:')
    for term, en in remaining:
        print('  "%s" in: %s' % (term, en))
else:
    print('验证通过: 无美式残留')
