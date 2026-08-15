# -*- coding: utf-8 -*-
"""SHER12 网站 i18n 构建脚本 v2
方案: 每个含中文「直接文本」的元素打 data-i18n-html="纯文本"（整体替换 innerHTML）
- key = 元素内部纯文本（去标签、trim）
- 翻译值里保留 <b>/<br>/<span> 结构
- JS 从最深元素向浅替换，避免覆盖
用法: python build_i18n.py scan | verify
"""
import os, re, json, sys
from zhconv import convert

ROOT = os.path.dirname(os.path.abspath(__file__))
DICT_PATH = os.path.join(ROOT, 'i18n-dict.json')
CN = 'zh-CN'; TW = 'zh-TW'; EN = 'en'

VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
SKIP_TAGS = {'script','style','noscript','textarea','title','svg'}

def mask_blocks(html):
    """等长掩码 script/style 块，保持偏移一致"""
    def _m(m):
        s = m.group(0)
        name = 'script' if s.lstrip().lower().startswith('<script') else 'style'
        ol = len('<%s>' % name); cl = len('</%s>' % name)
        return '<%s>%s</%s>' % (name, ' ' * max(0, len(s) - ol - cl), name)
    html = re.sub(r'<script[\s\S]*?</script>', _m, html, flags=re.I)
    html = re.sub(r'<style[\s\S]*?</style>', _m, html, flags=re.I)
    return html

def scan_elements(html):
    """返回 [{tag_start, start_tag_end, key, is_container}] 含中文的元素
    - 叶子（无子标签）: key = 纯文本
    - 容器（子标签内含中文）: key = 压缩空白后的完整 innerHTML
    """
    # token 流: 切出标签与文本
    tokens = []  # (type, start, end)  type: 'tag'|'text'
    pos = 0
    tag_re = re.compile(r'<[^<>]*>')
    for m in tag_re.finditer(html):
        if m.start() > pos:
            tokens.append(('text', pos, m.start()))
        tokens.append(('tag', m.start(), m.end()))
        pos = m.end()
    if pos < len(html):
        tokens.append(('text', pos, len(html)))

    # 解析标签
    tag_parse = re.compile(r'<(/)?([a-zA-Z][a-zA-Z0-9]*)((?:\s[^<>]*?)?)(/?)>')
    stack = []  # {name, tag_start, start_tag_end, texts:[], child_has_zh:False}
    elements = []
    for typ, s, e in tokens:
        if typ == 'tag':
            m = tag_parse.match(html, s, e)
            if not m: continue
            closing, name, attrs, selfclose = m.group(1), m.group(2).lower(), m.group(3) or '', m.group(4)
            if name in SKIP_TAGS:
                continue
            if closing:
                for i in range(len(stack)-1, -1, -1):
                    if stack[i]['name'] == name:
                        el = stack.pop(i)
                        el['close_start'] = m.start()
                        elements.append(el)
                        # 向上标记祖先有中文子标签
                        zh = el['zh']
                        for anc in stack:
                            if zh:
                                anc['child_zh'] = True
                        break
            elif selfclose or name in VOID:
                pass
            else:
                stack.append({'name': name, 'tag_start': s, 'start_tag_end': m.end(),
                              'texts': [], 'zh': False, 'child_zh': False})
        else:
            txt = html[s:e]
            if not stack: continue
            top = stack[-1]
            top['texts'].append(txt)
            if re.search(r'[\u4e00-\u9fff]', txt):
                top['zh'] = True

    zh_re = re.compile(r'[\u4e00-\u9fff]')
    INLINE = {'b','span','i','em','strong','br','u','sup','sub','mark'}
    out = []
    for el in elements:
        if not el['zh'] and not el['child_zh']:
            continue
        if el['child_zh']:
            # 容器: 仅当内部子标签全为内联格式标签（复合句整段翻译）
            inner = html[el['start_tag_end']:el['close_start']]
            inner = re.sub(r'>\s+<', '><', inner).strip()
            # 检查内部出现的标签是否都是内联
            inner_tags = set(re.findall(r'<(/)?([a-zA-Z][a-zA-Z0-9]*)', inner))
            tags = {t for _, t in inner_tags if t.lower() != 'br'}
            if tags and tags <= INLINE and zh_re.search(inner):
                out.append({'start_tag_end': el['start_tag_end'], 'key': inner})
        elif el['zh']:
            # 纯叶子: key = 直接文本
            joined = ''.join(el['texts'])
            text = ' '.join(joined.split())
            if text:
                out.append({'start_tag_end': el['start_tag_end'], 'key': text})
    # 去重（同一元素只注入一次；若有重复取最长 key）
    seen = {}
    for e in out:
        pos = e['start_tag_end']
        if pos not in seen or len(e['key']) > len(seen[pos]['key']):
            seen[pos] = e
    out = list(seen.values())
    out.sort(key=lambda x: -x['start_tag_end'])
    return out

def inject(html, els):
    """从后往前注入 data-i18n-html（在开始标签的 > 前插入）"""
    edits = []
    for el in els:
        key = el['key']
        attr = f' data-i18n-html="{key.replace("&","&amp;").replace(chr(34),"&quot;").replace("<","&lt;").replace(">","&gt;")}"'
        edits.append((el['start_tag_end'] - 1, attr))
    for pos, attr in sorted(edits, key=lambda x: -x[0]):
        html = html[:pos] + attr + html[pos:]
    return html

def load_dict():
    if os.path.exists(DICT_PATH):
        return json.load(open(DICT_PATH, encoding='utf-8'))
    return {}

def save_dict(d):
    json.dump(d, open(DICT_PATH, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'scan'
    files = sorted(f for f in os.listdir(ROOT) if f.endswith('.html'))
    d = load_dict()
    for fn in files:
        path = os.path.join(ROOT, fn)
        html = open(path, encoding='utf-8').read()
        masked = mask_blocks(html)
        els = scan_elements(masked)
        for el in els:
            key = el['key']
            if key not in d:
                d[key] = {CN: key, TW: convert(key, 'zh-hant'), EN: ''}
        html = inject(html, els)
        open(path, 'w', encoding='utf-8').write(html)
        print(f'{fn}: {len(els)} 个元素打标')
    save_dict(d)
    print(f'\n字典共 {len(d)} 条 → i18n-dict.json')
    print(f'待填英文: {sum(1 for v in d.values() if not v.get(EN))} 条')
    # 输出打标汇总供检查
    if cmd == 'scan':
        print('\n=== 复合句（含标签）抽查 ===')

if __name__ == '__main__':
    main()
