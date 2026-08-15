/* ============================================================
 * SHER12 i18n — 简 / 繁 / EN 三语切换
 * - 加载 i18n-dict.json（同目录）
 * - 按 [data-i18n-html] 属性从深到浅替换 innerHTML
 * - localStorage 记忆语言，跨页面生效
 * - 切换器 UI 自动注入（优先 #i18n-switcher → nav → 页面顶部）
 * ============================================================ */
(function () {
  'use strict';

  var LS_KEY = 'sher12-lang';
  var LANGS = [
    { id: 'zh-CN', label: '\u7b80' },   // 简
    { id: 'zh-TW', label: '\u7e41' },   // 繁
    { id: 'en',    label: 'EN' }
  ];

  var dict = null;
  var lookup = null;
  var current = localStorage.getItem(LS_KEY);
  if (!current || LANGS.every(function (l) { return l.id !== current; })) {
    current = 'zh-CN';
  }

  /* HTML 实体 → 真实字符。
   * 双重解码：build 注入属性时把 key 里的 & 转成 &amp;（如 &nbsp; → &amp;nbsp;），
   * getAttribute 返回原文，需解码两次才能与字典 key（单次实体）对齐。 */
  function decodeKey(s) {
    var t = document.createElement('textarea');
    t.innerHTML = s;
    t.innerHTML = t.value; // 第二遍：处理 &amp;nbsp; → &nbsp; → \xa0
    return t.value;
  }

  function buildLookup(d) {
    lookup = {};
    Object.keys(d).forEach(function (k) {
      lookup[decodeKey(k)] = d[k];
    });
  }

  function depthOf(el) {
    var n = 0, p = el.parentNode;
    while (p && p !== document.documentElement) { n++; p = p.parentNode; }
    return n;
  }

  function apply(lang) {
    if (!lookup) return;
    current = lang;
    try { localStorage.setItem(LS_KEY, lang); } catch (e) {}

    var docLang = lang === 'zh-TW' ? 'zh-Hant' : (lang === 'en' ? 'en' : 'zh-CN');
    document.documentElement.lang = docLang;
    document.documentElement.setAttribute('data-lang', lang);

    /* head 上的打标属性 = 页面标题，单独翻译 title（head 本身不可整体替换） */
    var headEl = document.querySelector('head[data-i18n-html]');
    if (headEl) {
      var headKey = decodeKey(headEl.getAttribute('data-i18n-html'));
      var headRec = lookup[headKey];
      if (headRec && headRec[lang]) document.title = headRec[lang];
    }

    /* 从深到浅替换，避免父容器覆盖子元素翻译；仅处理 body 内元素 */
    var els = Array.prototype.slice.call(document.querySelectorAll('body [data-i18n-html]'));
    els.sort(function (a, b) { return depthOf(b) - depthOf(a); });

    var missing = 0;
    for (var i = 0; i < els.length; i++) {
      var el = els[i];
      var key = decodeKey(el.getAttribute('data-i18n-html'));
      var rec = lookup[key];
      if (rec && rec[lang]) {
        el.innerHTML = rec[lang];
      } else {
        missing++;
      }
    }

    /* 按钮高亮 */
    var btns = document.querySelectorAll('[data-i18n-btn]');
    for (var j = 0; j < btns.length; j++) {
      btns[j].classList.toggle('active', btns[j].getAttribute('data-i18n-btn') === lang);
    }
    if (missing > 0) {
      // eslint-disable-next-line no-console
      console.warn('[i18n] %d element(s) missing translation for %s', missing, lang);
    }
  }

  /* ---- 切换器 ---- */
  function injectStyle() {
    if (document.getElementById('sher12-i18n-style')) return;
    var css =
      '#sher12-i18n-switcher{display:inline-flex;align-items:center;gap:2px;' +
      'margin-left:14px;padding:3px;border:1px solid currentColor;border-radius:999px;' +
      'font-size:12px;line-height:1;letter-spacing:.02em;user-select:none;' +
      'vertical-align:middle;}' +
      '#sher12-i18n-switcher .i18n-btn{background:transparent;border:0;cursor:pointer;' +
      'padding:5px 9px;border-radius:999px;color:inherit;font:inherit;opacity:.55;' +
      'transition:opacity .15s ease;}' +
      '#sher12-i18n-switcher .i18n-btn:hover{opacity:.9;}' +
      '#sher12-i18n-switcher .i18n-btn.active{opacity:1;background:currentColor;' +
      'color:#111;font-weight:600;}' +
      '@media (max-width:768px){#sher12-i18n-switcher{margin-left:8px;}' +
      '#sher12-i18n-switcher .i18n-btn{padding:4px 7px;}}';
    var st = document.createElement('style');
    st.id = 'sher12-i18n-style';
    st.textContent = css;
    document.head.appendChild(st);
  }

  function renderSwitcher() {
    injectStyle();
    var host = document.getElementById('sher12-i18n-switcher');
    if (!host) {
      var navLinks = document.querySelector('.nav-links');
      if (navLinks) {
        host = document.createElement('div');
        host.id = 'sher12-i18n-switcher';
        navLinks.appendChild(host);
      } else {
        var nav = document.querySelector('nav');
        if (nav) {
          host = document.createElement('div');
          host.id = 'sher12-i18n-switcher';
          nav.appendChild(host);
        } else {
          host = document.createElement('div');
          host.id = 'sher12-i18n-switcher';
          host.style.cssText = 'position:fixed;top:14px;right:14px;z-index:9999;' +
            'background:#111;color:#fff;border-radius:999px;';
          document.body.insertBefore(host, document.body.firstChild);
        }
      }
    }
    host.classList.add('sher12-i18n-host');

    LANGS.forEach(function (l) {
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'i18n-btn' + (l.id === current ? ' active' : '');
      btn.setAttribute('data-i18n-btn', l.id);
      btn.textContent = l.label;
      btn.title = l.id;
      btn.addEventListener('click', function () { apply(l.id); });
      host.appendChild(btn);
    });
  }

  /* ---- 启动 ---- */
  function init() {
    renderSwitcher();
    fetch('i18n-dict.json', { cache: 'no-cache' })
      .then(function (r) {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        return r.json();
      })
      .then(function (d) {
        dict = d;
        buildLookup(d);
        apply(current);
      })
      .catch(function (err) {
        console.warn('[i18n] dict load failed, staying in default language:', err);
      });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
