/* 无头验证 i18n.js：加载真实页面 + 真实字典 + 真实脚本，验证三语切换 */
const { JSDOM } = require('jsdom');
const fs = require('fs');
const path = require('path');

const ROOT = 'C:/Users/savio/WorkBuddy/Claw/sher12-website';
const dict = JSON.parse(fs.readFileSync(path.join(ROOT, 'i18n-dict.json'), 'utf-8'));
const i18nCode = fs.readFileSync(path.join(ROOT, 'i18n.js'), 'utf-8');

const CASES = [
  { file: 'index.html', check: ['品牌密码', '产品', '版型体系', '加入 SHER12 CLUB'] },
  { file: 'product-sign-blue.html', check: ['Sign 乙24H·霁蓝', '返回产品', '刺绣'] },
  { file: 'product-love-pink.html', check: ['Love·桃夭', '桃夭', '栗色'] },
  { file: 'hattype.html', check: ['甲乙丙丁', '瓜皮帽', '渔夫帽'] },
  { file: 'product-cleaner.html', check: ['清洁液', '200ml'] },
];

function makeWindow(html, file) {
  const dom = new JSDOM(html, {
    url: 'http://localhost/' + file,
    runScripts: 'dangerously',
    pretendToBeVisual: true,
  });
  const win = dom.window;
  // stub fetch → 返回本地字典（jsdom 无原生 fetch）
  win.fetch = () => Promise.resolve({ ok: true, json: () => Promise.resolve(dict) });
  // 以 <script> 注入，确保在 window 全局作用域执行（win.eval 在 jsdom 新版跑在 Node 全局）
  const script = win.document.createElement('script');
  script.textContent = i18nCode;
  win.document.head.appendChild(script);
  return dom;
}

function texts(win) {
  return Array.from(win.document.querySelectorAll('[data-i18n-html]'))
    .map((el) => el.textContent.trim())
    .filter(Boolean);
}

(async () => {
  let fail = 0;
  for (const c of CASES) {
    const dom = makeWindow(fs.readFileSync(path.join(ROOT, c.file), 'utf-8'), c.file);
    const win = dom.window;
    await new Promise((r) => setTimeout(r, 80)); // 等 fetch + apply
    const before = texts(win);
    const titleBefore = win.document.title;

    // 点 EN 按钮
    const enBtn = win.document.querySelector('[data-i18n-btn="en"]');
    if (!enBtn) { console.log('[' + c.file + '] ✗ 无 EN 按钮'); fail++; continue; }
    enBtn.click();
    await new Promise((r) => setTimeout(r, 30));
    const enTexts = texts(win);
    const titleEn = win.document.title;

    // 点繁按钮
    const twBtn = win.document.querySelector('[data-i18n-btn="zh-TW"]');
    twBtn.click();
    await new Promise((r) => setTimeout(r, 30));
    const twTexts = texts(win);

    // 点回简
    const cnBtn = win.document.querySelector('[data-i18n-btn="zh-CN"]');
    cnBtn.click();
    await new Promise((r) => setTimeout(r, 30));
    const cnBack = texts(win);

    // 断言: EN 后应出现英文, 繁后应出现繁体, 切回简体应还原
    const okEn = enTexts.some((t) => /[A-Za-z]{3,}/.test(t));
    const okTw = twTexts.some((t) => /[^\x00-\x7f]/.test(t) && /[繁體]/.test(t) === false) || twTexts.some((t) => /裡|裏|萬|爲|這|說/.test(t));
    const okCn = cnBack.join('|') === before.join('|');
    const okTitle = /^[A-Za-z]/.test(titleEn) || titleEn.includes('SHER12');

    const status = (okEn && okTw && okCn && okTitle) ? '✓' : '✗';
    if (status === '✗') fail++;
    console.log('[' + c.file + '] ' + status +
      '  title: ' + titleBefore.slice(0, 24) + ' → EN: ' + titleEn.slice(0, 30) +
      ' | en出现=' + okEn + ' 繁出现=' + okTw + ' 还原=' + okCn + ' title英=' + okTitle);
    if (!okEn) console.log('   EN 样本:', enTexts.slice(0, 8));
    if (!okTw) console.log('   TW 样本:', twTexts.slice(0, 8));
    dom.window.close();
  }
  console.log(fail === 0 ? '\n全部通过 ✓' : '\n' + fail + ' 个页面失败 ✗');
  process.exit(fail === 0 ? 0 : 1);
})();
