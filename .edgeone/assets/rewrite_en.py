#!/usr/bin/env python3
"""Rewrite i18n EN translations — from literal to international streetwear brand voice."""
import json, os

DICT_PATH = os.path.join(os.path.dirname(__file__), 'i18n-dict.json')

with open(DICT_PATH, 'r', encoding='utf-8') as f:
    d = json.load(f)

# {chinese_key: new_english_value}
# Only entries that need rework are listed. Everything else stays.
changes = {
    # === Brand philosophy ===
    "中国帽子本土设计 · 做中国人自己的帽饰品牌":
        "Caps designed in China · A brand of our own",

    "我们用一套自己的语言定义帽子。四种帽型，四种扣法，比数字编号更懂中国人。":
        "We name our fits our own way. Four silhouettes, four clasps — a system, not a size chart.",

    "中国人自己的帽饰品牌":
        "China's own cap brand",

    "把中国文化的图腾，一针一线绣在帽子上。":
        "Stitching Chinese motifs onto every cap, thread by thread.",

    "SHER12 不只是一顶帽子。是一群相信「中国设计能上头」的人。加进来，第一时间收到每一次发售。":
        "SHER12 is more than a cap. We're a community who believe Chinese design belongs on your head. Join us — first access to every release.",

    # === 江湖 concept ===
    "戴帽的人，自成江湖":
        "Caps on, we make our own world",
    "戴帽的人，自成江湖。":
        "Caps on, we make our own world.",

    # === 十二 concept ===
    "「帽」字<b>十二</b>笔，「中国」也是<b>十二</b>笔。<br>\n      一天<b>十二</b>个时辰，一年<b>十二</b>个月。<br>\n      不是随便挑的数字——是刻在中国文化里的密码。":
        "The word for 'cap' has <b>12</b> strokes in Chinese. So does 'China'.<br>\n      <b>12</b> hours in a day cycle, <b>12</b> months in a year.<br>\n      Not a random number — a code woven into the culture.",

    "「拾贰」刺绣，十二即一切。帽字十二笔，中国十二笔。":
        "\"Twelve\" embroidery — twelve is everything. 'Cap' has 12 strokes, so does 'China'.",

    # === 深圳人 slogan ===
    "来了就是深圳人。":
        "Arrive, and you belong.",
    "来了，<br>就是<span>深圳人</span>。":
        "Arrive,<br>and you <span>belong</span>.",
    "Sher = Shen（深圳）+ er（人）&nbsp;&nbsp;·&nbsp;&nbsp;<b>来了就是深圳人。</b>":
        "Sher = Shen (Shenzhen) + er (one who belongs) &nbsp;&nbsp;·&nbsp;&nbsp;<b>Arrive, and you belong.</b>",

    # === 不服 → Defy ===
    "不服":
        "Defy",
    "不服 — SHER12":
        "Defy — SHER12",
    "不服，<br>是一种<span>本能</span>。":
        "Defy,<br>is an <span>instinct</span>.",
    "两个字，一种态度。戴上就是表态。":
        "One word, one attitude. Wear it — that's the statement.",
    "「中国」二字，金黄刺绣，酒红底；不服两个字，一种态度。把中国文化，戴在头上。":
        "\"China\" in gold on wine red. Defy — one word, one attitude. Wear the culture on your head.",

    # === 生死 → everything (already good in sentence, fix standalone) ===
    "生死":
        "Everything",
    "五片帽玄色款，可调节。版型定生死。":
        "5-panel in Xuan Black. Adjustable. Fit is everything.",

    # === 珠峰 ===
    "向上，永远向上。8848.86m，一座山的高度，一种态度的高度。":
        "Up, always up. 8,848.86m — the height of a mountain, the height of a mindset.",

    # === 城市 ===
    "每一座城市，都有属于自己的颜色与脾气。把城市戴在头上。":
        "Every city has its own colour and character. Wear yours.",

    # === 广东 ===
    "「广东」刺绣，深圳人的广东认同。大湾区的心声。":
        "\"Guangdong\" embroidery — Shenzhen's roots, the pride of the south.",
    "广东，<br>是一种<span>归属</span>。":
        "Guangdong,<br>is <span>belonging</span>.",

    # === 港澳 ===
    "港澳人的心声，<br>也是中国人的<span>心声</span>。":
        "The voice of Hong Kong and Macao,<br>is the <span>voice</span> of China, too.",

    # === 發财 (Cantonese pun untranslatable) ===
    "绿色帽身+白色大字「發」覆盖全帽，帽檐下印「生财有道」。这顶帽子藏了一句脏话，但只有你自己知道。":
        "Green crown, white \"Fortune\" across the cap. Hidden under the brim: a secret only you know.",

    # === 配件 ===
    "好帽要养。帽刷 + 清洁液 + 除皱喷雾，让你的帽子一直像新的一样。":
        "Good caps deserve care. Brush + cleaner + wrinkle spray — keep every cap fresh.",

    # === 产品描述优化 ===
    "马赛克像素风 SHER 印花，数字时代的帽饰表达。":
        "Pixelated SHER print — cap design for the digital age.",
    "蛇皮纹理印花，红蓝撞色，野性十足。":
        "Snake-skin print, red-blue clash — pure wild.",
    "独角兽，糖果绿紫，甜美梦幻。潮玩 IP × 帽饰文化。":
        "Unicorn in candy green & purple — sweet, dreamy. Art-toy meets cap culture.",
    "一只永远在加载懒惰的狗。不想起床、不想上班、永远在缓冲。":
        "A dog stuck on loading. Won't get up, won't work, always buffering.",

    # === 扣型编码 (use standard cap terminology) ===
    "扣型编码：12 塑胶背扣 · 24 金属日字扣 · 0 封闭不可调 · 10 金属塑扣":
        "Closure Code: 12 plastic snap · 24 metal buckle · 0 fitted (fixed) · 10 metal snap",
    "12 塑胶背扣":
        "12 Plastic Snap",
    "24 金属日字扣":
        "24 Metal Buckle",
    "<span>24 金属日字扣</span><span>12 塑胶背扣</span>":
        "<span>24 Metal Buckle</span><span>12 Plastic Snap</span>",
    "<span>24 金属日字扣</span><span>0 封闭不可调</span>":
        "<span>24 Metal Buckle</span><span>0 Fitted</span>",
    "<span>10 金属塑扣</span>":
        "<span>10 Metal Snap</span>",
    "<span>10 金属塑扣</span><span>0 封闭不可调</span>":
        "<span>10 Metal Snap</span><span>0 Fitted</span>",
    "10 金属塑扣":
        "10 Metal Snap",

    # === 瓜皮帽 ===
    "瓜皮帽":
        "Dome Cap",
    "瓜皮帽 · 丁10":
        "Dome Cap · Ding10",
    "丁10 · 瓜皮帽":
        "Ding10 · Dome Cap",
    "丁 · 瓜皮帽":
        "Ding · Dome Cap",

    # === 小优化 ===
    "好帽要养":
        "Good caps deserve care",
    "版型定生死":
        "Fit is everything",
}

applied = 0
not_found = []

for key, new_en in changes.items():
    if key in d:
        old_en = d[key].get('en', '')
        if old_en != new_en:
            d[key]['en'] = new_en
            applied += 1
            print(f"  [OK] {key[:40]}...")
            print(f"       OLD: {old_en[:80]}")
            print(f"       NEW: {new_en[:80]}")
            print()
    else:
        not_found.append(key)

with open(DICT_PATH, 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

print(f"\n{'='*60}")
print(f"Applied: {applied} changes")
print(f"Not found: {len(not_found)}")
for nf in not_found:
    print(f"  [MISS] {nf[:60]}")
print(f"Total dict entries: {len(d)}")
