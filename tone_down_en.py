#!/usr/bin/env python3
"""Tone down EN translations — less assertive, more understated (international streetwear aesthetic)."""

import json

DICT_PATH = r"C:\Users\savio\WorkBuddy\Claw\sher12-website\i18n-dict.json"

with open(DICT_PATH, encoding='utf-8') as f:
    d = json.load(f)

# {original_key: new_en_value}
changes = {
    # 1. "Roar it out" too aggressive
    "吼出来，<br>别<span>憋着</span>。":
        "Let it out,<br>don't hold it <span>in</span>.",

    # 2. "Unleash" too dramatic
    "释放，<br>你的<span>野性</span>。":
        "Let loose,<br>your <span>wilder side</span>.",

    # 3. "pure wild" too strong
    "蛇皮纹理印花，红蓝撞色，野性十足。":
        "Snake-skin print, red-blue clash — a bold edge.",

    # 4. "breaking convention" too assertive
    "Sign 系列海棠款，打破常规。":
        "Sign in Crabapple — off the grid.",

    # 5. "that's the statement" too preachy
    "两个字，一种态度。戴上就是表态。":
        "One word. Put it on.",

    # 6. "for those who care about quality" too preachy (two instances)
    "Sign 乙24H版，苍色低调。金属扣品质之选。":
        "Sign Yi24H in Pale Cyan — understated. Metal buckle finish.",
    "Sign 乙24H版，霁蓝清爽。金属扣品质之选。":
        "Sign Yi24H in Clear Sky — crisp. Metal buckle finish.",

    # 7. "we make our own world" too grand
    "戴帽的人，自成江湖。":
        "Caps on, we go our own way.",
    "戴帽的人，自成江湖":
        "Caps on, we go our own way",

    # 8. "Culture, stated directly" too assertive
    "「中国」二字，金黄刺绣，酒红底。最直接的文化表达。":
        "\"China\" in gold embroidery on wine red. Culture, worn simply.",

    # 9. "one word, one attitude. Wear the culture on your head." too pushy
    "「中国」二字，金黄刺绣，酒红底；不服两个字，一种态度。把中国文化，戴在头上。":
        "\"China\" in gold on wine red. Defy — one word. Culture, worn quietly.",

    # 10. "the pride of the south" too nationalistic
    "「广东」刺绣，深圳人的广东认同。大湾区的心声。":
        "\"Guangdong\" embroidery — Shenzhen's roots, rooted in the south.",

    # 11. "always spot on" too casual/cheesy
    "弯沿帽配魔术贴，全玄百搭。可调节，随时到位。":
        "Curved-brim with Velcro — all Xuan Black, goes with everything. Adjustable.",

    # 12. "belongs on your head" too assertive
    "SHER12 不只是一顶帽子。是一群相信「中国设计能上头」的人。加进来，第一时间收到每一次发售。":
        "SHER12 is more than a cap. We're a community who believe Chinese design has a place up there. Join us — first access to every release.",

    # 13. "bold SHER print" — "bold" is fine but "醒目" can be subtler
    "双面玄月白印花渔夫帽，SHER logo 醒目印花。":
        "Reversible bucket in Xuan Black & Moon White with a SHER print.",

    # 14. "the same attitude" — keep but simplify
    "街舞与帽，<br>同一种<span>态度</span>。":
        "Street dance and caps —<br>same <span>energy</span>.",

    # 15. "stays true to the streets" too cliché
    "街舞联名甲24版，平沿更贴街头。":
        "Street-dance collaboration, Jia24 fit — flat brim, street-ready.",
}

count = 0
for key, new_en in changes.items():
    if key in d:
        old_en = d[key].get('en', '')
        if old_en != new_en:
            d[key]['en'] = new_en
            count += 1
            print(f"  [OK] {key[:40]}...")
            print(f"       OLD: {old_en}")
            print(f"       NEW: {new_en}")
    else:
        print(f"  [MISS] {key[:40]}...")

print(f"\nTotal changed: {count}/{len(changes)}")

with open(DICT_PATH, 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
print("Dictionary saved.")
