/* Portfolio desk: state, form and rendering. Logic lives in engine.js, words in i18n.js, evidence in research.js. */
(function () {
  'use strict';
  var doc = document, html = doc.documentElement;
  var LI = html.lang === 'en' ? 1 : 0, ROOT = html.getAttribute('data-root') || '../';
  var T = window.PM_TEXT, R = window.PM_RESEARCH, M = window.PM_MARKET, E = window.PM_ENGINE;
  var KEY = 'pm-desk-v1';
  E.init(M, R);

  /* ---------- helpers ---------- */
  function L(pair) { return pair[LI]; }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function t(pair, vars) { var s = L(pair); if (vars) for (var k in vars) s = s.split('{' + k + '}').join(esc(vars[k])); return s; }
  function n(x, d) { if (x == null || !isFinite(x)) return '–'; var s = Math.abs(x).toFixed(d == null ? 1 : d); if (LI === 0) s = s.replace('.', ','); return (x < 0 ? '−' : '') + s; }
  function n0(x) { return n(x, 0); }
  function g(x) { return n(x, Math.abs(x - Math.round(x)) < 0.05 ? 0 : 1); }           // drop ".0"
  function sg(x, d) { return x == null ? '–' : (x > 0 ? '+' : '') + n(x, d); }
  function px(x) { return x == null ? '–' : Math.round(x).toLocaleString(LI ? 'en-US' : 'vi-VN'); }
  function date(iso) { var p = iso.split('-'); return LI ? Number(p[2]) + ' ' + ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][p[1] - 1] + ' ' + p[0] : p[2] + '/' + p[1] + '/' + p[0]; }
  function $(id) { return doc.getElementById(id); }
  function secName(s) { return L(R.sectors[s].name); }
  function srcLink(key) { var r = R.reports[key]; return '<a class="src" href="' + ROOT + r.url[LI] + '">' + esc(L(r.title)) + ', ' + date(r.date) + '</a>'; }
  function uid() { return 'p' + Date.now().toString(36) + Math.floor(Math.random() * 1e4).toString(36); }

  /* ---------- state ---------- */
  var state = { v: 1, settings: { capital: '', maxDD: 15, regime: 'auto' }, positions: [] };
  var editing = null;   // position being edited (a copy), or null
  function clean(s) {
    var out = { v: 1, settings: { capital: '', maxDD: 15, regime: 'auto' }, positions: [] };
    if (!s || typeof s !== 'object' || !Array.isArray(s.positions)) return null;
    var st = s.settings || {};
    out.settings.capital = st.capital == null ? '' : String(st.capital).slice(0, 12);
    out.settings.maxDD = Math.min(60, Math.max(3, parseFloat(st.maxDD) || 15));
    out.settings.regime = ['auto', 'easing', 'neutral', 'tight'].indexOf(st.regime) >= 0 ? st.regime : 'auto';
    out.settings.asked = !!st.asked;
    s.positions.slice(0, 60).forEach(function (p) {
      if (!p || !p.ticker) return;
      var str = function (x, m) { return x == null ? '' : String(x).slice(0, m); };
      var arr = function (a) { return Array.isArray(a) ? a.filter(function (d) { return R.drivers[d]; }) : []; };
      out.positions.push({ id: str(p.id, 24) || uid(), ticker: str(p.ticker, 8).toUpperCase().replace(/[^A-Z0-9]/g, ''), sector: R.sectors[p.sector] ? p.sector : 'other', status: p.status === 'idea' ? 'idea' : 'hold',
        weight: str(p.weight, 8), conviction: Math.min(5, Math.max(1, parseInt(p.conviction, 10) || 3)), up: str(p.up, 8), down: str(p.down, 8), p: str(p.p, 8), horizon: str(p.horizon, 6),
        edge: ['none', 'info', 'analysis', 'time', 'behaviour'].indexOf(p.edge) >= 0 ? p.edge : 'none', likes: arr(p.likes), dislikes: arr(p.dislikes), thesis: str(p.thesis, 2000), catalyst: str(p.catalyst, 600), kill: str(p.kill, 600) });
    });
    return out;
  }
  function load() { try { var s = clean(JSON.parse(localStorage.getItem(KEY))); if (s) state = s; } catch (e) {} }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) {} }

  var EXAMPLE = { settings: { capital: '2', maxDD: 15, regime: 'auto' }, positions: [
    { ticker: 'VHM', status: 'hold', weight: 22, conviction: 3, up: 30, down: 20, horizon: 12, edge: 'none', likes: ['earnings'], dislikes: [], thesis: ['Lợi nhuận kỷ lục, P/E thấp.', 'Record earnings on a low P/E.'] },
    { ticker: 'KDH', status: 'hold', weight: 12, conviction: 2, up: 40, down: 25, horizon: 18, edge: 'time', likes: ['valuation'], dislikes: ['rates'], thesis: ['Giá đã giảm sâu, quỹ đất tốt.', 'The price has fallen a long way and the land bank is good.'] },
    { ticker: 'SSI', status: 'hold', weight: 18, conviction: 3, up: 25, down: 15, horizon: 9, edge: 'none', likes: ['brokerage', 'flows'], dislikes: [] },
    { ticker: 'TCB', status: 'hold', weight: 20, conviction: 5, up: 35, down: 15, p: 65, horizon: 12, edge: 'analysis', likes: ['funding', 'nim'], dislikes: ['asset'], thesis: ['CASA cao giúp NIM hồi phục sớm hơn ngành.', 'High CASA lets NIM recover ahead of the sector.'], catalyst: ['Kết quả 4Q26', '4Q26 results'], kill: ['NIM quay lại dưới 3,1%', 'NIM back below 3.1%'] },
    { ticker: 'HPG', status: 'hold', weight: 10, conviction: 5, up: 40, down: 15, horizon: 18, edge: 'info', likes: ['volume', 'protection'], dislikes: [], thesis: ['Dung Quất 2 thay thế HRC nhập khẩu.', 'Dung Quat 2 replaces imported HRC.'] },
    { ticker: 'FPT', status: 'hold', weight: 8, conviction: 2, up: 10, down: 20, horizon: 6, edge: 'none', likes: [], dislikes: ['momentum'] },
    { ticker: 'MWG', status: 'idea', weight: 0, conviction: 4, up: 30, down: 12, horizon: 12, edge: 'analysis', likes: ['growth'], dislikes: ['inventory'], thesis: ['Chuỗi niêm yết đang giành thị phần.', 'Listed chains are taking share.'] }
  ] };
  function loadExample() {
    var s = JSON.parse(JSON.stringify(EXAMPLE));
    s.positions.forEach(function (p) { ['thesis', 'catalyst', 'kill'].forEach(function (k) { if (Array.isArray(p[k])) p[k] = p[k][LI]; }); p.id = uid() + p.ticker; });
    state = clean(s); editing = null; iv = null; save(); render();
  }

  /* ---------- section 1: input ---------- */
  function driversFor(sec) { var out = []; for (var k in R.drivers) { var d = R.drivers[k]; if (!d.sec || d.sec.indexOf(sec) >= 0) out.push(k); } return out; }
  function field(label, inner, hint) { return '<label class="fld"><span class="lab">' + label + '</span>' + inner + (hint ? '<span class="hint">' + hint + '</span>' : '') + '</label>'; }
  function opt(v, label, cur) { return '<option value="' + v + '"' + (String(cur) === String(v) ? ' selected' : '') + '>' + esc(label) + '</option>'; }

  function renderInput() {
    var s = state.settings, h = '';
    if (!state.positions.length) {   // first visit: the question comes first
      $('pm-input').innerHTML = '<div id="editor"></div><p class="btns"><button type="button" class="btn" id="b-example">' + L(T.example) + '</button><button type="button" class="btn" id="b-import">' + L(T.importBtn) + '</button><input type="file" id="f-import" accept="application/json,.json" hidden></p>';
      renderEditor(); return;
    }
    h += '<div class="grid3">' +
      field(L(T.maxDD), '<input type="number" id="set-maxDD" min="3" max="60" step="1" inputmode="decimal" value="' + esc(s.maxDD) + '">', L(T.maxDDHint)) +
      field(L(T.regime), '<select id="set-regime">' + opt('auto', L(T.regimeAuto), s.regime) + opt('easing', L(T.rgEasing), s.regime) + opt('neutral', L(T.rgNeutral), s.regime) + opt('tight', L(T.rgTight), s.regime) + '</select>') +
      field(L(T.capital), '<input type="number" id="set-capital" min="0" step="0.1" inputmode="decimal" value="' + esc(s.capital) + '">', L(T.capitalHint)) + '</div>';
    if (!state.positions.length) h += '<p class="empty">' + L(T.empty) + '</p>';
    else {
      h += '<div class="tablewrap"><table><thead><tr><th>' + L(T.thTicker) + '</th><th>' + L(T.thStatus) + '</th><th class="num">' + L(T.thWeight) + '</th><th class="num">' + L(T.thConv) + '</th><th class="num">' + L(T.thUD) + '</th><th></th></tr></thead><tbody>';
      state.positions.forEach(function (p) {
        var mk = M.t[p.ticker];
        h += '<tr><td>' + esc(p.ticker) + ' <span class="sub">' + esc(mk ? mk.name : secName(p.sector)) + '</span></td><td>' + L(p.status === 'idea' ? T.stIdea : T.stHold) + '</td><td class="num">' + (p.weight === '' ? '–' : g(parseFloat(p.weight) || 0) + '%') + '</td><td class="num">' + p.conviction + '/5</td><td class="num">' +
          (p.up !== '' && p.down !== '' ? '+' + esc(p.up) + '% / −' + esc(p.down) + '%' : '–') + '</td><td class="num"><button type="button" class="lnk" data-edit="' + esc(p.id) + '">' + L(T.edit) + '</button> <button type="button" class="lnk" data-del="' + esc(p.id) + '">' + L(T.remove) + '</button></td></tr>';
      });
      h += '</tbody></table></div>';
    }
    h += '<p class="btns"><button type="button" class="btn primary" id="b-add">' + L(T.add) + '</button><button type="button" class="btn" id="b-example">' + L(T.example) + '</button>' +
      '<button type="button" class="btn" id="b-export">' + L(T.exportBtn) + '</button><button type="button" class="btn" id="b-import">' + L(T.importBtn) + '</button>' +
      (state.positions.length ? '<button type="button" class="btn" id="b-print">' + L(T.print) + '</button><button type="button" class="btn danger" id="b-clear">' + L(T.clear) + '</button>' : '') +
      '<input type="file" id="f-import" accept="application/json,.json" hidden></p>';
    h += '<div id="editor"></div>';
    $('pm-input').innerHTML = h;
    renderEditor();
  }

  function chips(kind, list, sec) {
    return '<div class="chips" data-kind="' + kind + '">' + driversFor(sec).map(function (k) {
      return '<button type="button" class="chip' + (list.indexOf(k) >= 0 ? ' on ' + kind : '') + '" aria-pressed="' + (list.indexOf(k) >= 0) + '" data-chip="' + k + '">' + esc(L(R.drivers[k].label)) + '</button>';
    }).join('') + '</div>';
  }

  /* ---------- guided interview: one question at a time ---------- */
  var iv = null;   // { steps, i, draft, first, auto }
  function ivSteps(d, askDD) {
    var st = []; if (askDD) st.push('dd');
    st.push('ticker'); if (d.ticker && !M.t[d.ticker]) st.push('sector');
    st.push('status'); if (d.status !== 'idea') st.push('weight');
    return st.concat(['thesis', 'likes', 'dislikes', 'up', 'down', 'conviction', 'edge', 'catalyst', 'kill', 'done']);
  }
  function startInterview(auto) {
    editing = null;
    var d = blank(), askDD = !state.positions.length && !state.settings.asked;
    iv = { draft: d, askDD: askDD, i: 0, first: !state.positions.length, auto: !!auto };
    iv.steps = ivSteps(d, askDD);
  }
  function ivProbe() { var s = { settings: state.settings, positions: [iv.draft] }; return E.analyse(s).positions[0] || null; }
  function choice(attr, val, label, on) { return '<button type="button" class="choice' + (on ? ' on' : '') + '" ' + attr + '="' + esc(val) + '">' + label + '</button>'; }
  function renderInterview() {
    var box = $('editor'), d = iv.draft, id = iv.steps[iv.i], I = T.iv, tk = { t: d.ticker }, mk = M.t[d.ticker], sec = mk ? mk.sec : d.sector;
    var real = iv.steps.filter(function (x) { return x !== 'done'; }), k = Math.min(iv.i + 1, real.length);
    var q = '', hint = '', body = '', note = '', nav = true, skippable = true, m;
    function numq(field, picks, unit, max) {
      return '<div class="choices">' + picks.map(function (v) { return choice('data-ivnum', field + ':' + v, (unit === '+' ? '+' : unit === '-' ? '−' : '') + v + '%', String(d[field]) === String(v)); }).join('') + '</div>' +
        '<label class="fld inline"><span class="lab">' + L(I.other) + '</span><input type="number" id="iv-in" data-field="' + field + '" min="0" max="' + max + '" step="0.5" inputmode="decimal" value="' + esc(d[field]) + '"></label>';
    }
    if (id === 'dd') { q = L(I.qDD); hint = L(I.hDD); skippable = false; body = '<div class="choices">' + [10, 15, 20, 30].map(function (v) { return choice('data-ivdd', v, '−' + v + '%', false); }).join('') + '</div>'; nav = false; }
    else if (id === 'ticker') { q = L(iv.first ? I.qTicker0 : I.qTicker); hint = L(I.hTicker); skippable = false; body = '<label class="fld inline"><input type="text" id="iv-in" data-field="ticker" list="ticker-list" maxlength="8" autocapitalize="characters" value="' + esc(d.ticker) + '"></label>'; }
    else if (id === 'sector') { q = t(I.qSector, tk); skippable = false; nav = false; body = '<div class="choices">' + Object.keys(R.sectors).map(function (s) { return choice('data-ivset', 'sector:' + s, esc(secName(s)), false); }).join('') + '</div>'; }
    else if (id === 'status') {
      q = t(I.qStatus, tk); skippable = false; nav = false;
      body = '<div class="choices">' + choice('data-ivset', 'status:hold', L(I.own), false) + choice('data-ivset', 'status:idea', L(I.consider), false) + '</div>';
      m = ivProbe(); var nm = mk ? mk.name : d.ticker;
      note = (m && (m.ev_.tickerLevel || m.ev_.sectorLevel)) ? t(I.nCovered, { name: nm, sector: secName(sec), f: m.ev_.forN, a: m.ev_.againstN }) : t(I.nUncovered, { name: nm, sector: secName(sec) });
      if (mk && m && m.trend !== 'unknown') note += ' ' + t(T.pTrend[m.trend], { a: sg(mk.d200 != null ? mk.d200 : mk.d50), b: sg(mk.rs3m) });
    }
    else if (id === 'weight') { q = t(I.qWeight, tk); hint = L(I.hWeight); body = numq('weight', [3, 5, 10, 15, 20], '', 200); }
    else if (id === 'thesis') { q = t(I.qThesis, tk); hint = L(I.hThesis); body = '<label class="fld"><textarea id="iv-in" data-field="thesis" rows="3" maxlength="2000">' + esc(d.thesis) + '</textarea></label>'; }
    else if (id === 'likes' || id === 'dislikes') {
      var like = id === 'likes'; q = t(like ? I.qLikes : I.qDislikes, tk); hint = L(I.hTags);
      body = '<div class="chips">' + driversFor(sec).filter(function (x) { return like || d.likes.indexOf(x) < 0; }).map(function (x) { var on = d[id].indexOf(x) >= 0; return '<button type="button" class="chip' + (on ? ' on ' + (like ? 'like' : 'dislike') : '') + '" aria-pressed="' + on + '" data-ivchip="' + id + ':' + x + '">' + esc(L(R.drivers[x].label)) + '</button>'; }).join('') + '</div>';
    }
    else if (id === 'up') { q = t(I.qUp, tk); body = numq('up', [15, 25, 40, 60], '+', 1000); }
    else if (id === 'down') { q = t(I.qDown, tk); hint = L(T.fDownHint); body = numq('down', [8, 12, 20, 30], '-', 100); m = ivProbe(); if (mk && m) note = t(I.nVol, { t: d.ticker, m: n(m.monthSigma), dd: n0(Math.abs(mk.dd)) }); }
    else if (id === 'conviction') {
      q = L(I.qConv); skippable = false; nav = false; body = '<div class="choices col">' + [1, 2, 3, 4, 5].map(function (i) { return choice('data-ivset', 'conviction:' + i, L(T['conv' + i]), false); }).join('') + '</div>';
      m = ivProbe(); if (m && m.complete) note = t(m.breakeven > 50 ? I.nBEbad : I.nBE, { u: g(m.up), d: g(m.down), be: n0(m.breakeven) });
    }
    else if (id === 'edge') { q = L(I.qEdge); skippable = false; nav = false; body = '<div class="choices col">' + ['info', 'analysis', 'time', 'behaviour', 'none'].map(function (e) { return choice('data-ivset', 'edge:' + e, L(T['edge' + e.charAt(0).toUpperCase() + e.slice(1)]), false); }).join('') + '</div>'; }
    else if (id === 'catalyst') {
      q = L(I.qCatalyst); body = '<label class="fld"><input type="text" id="iv-in" data-field="catalyst" maxlength="600" placeholder="' + esc(L(T.fCatalystPh)) + '" value="' + esc(d.catalyst) + '"></label>' +
        '<div class="choices">' + [3, 6, 12, 24].map(function (v) { return choice('data-ivhz', v, t(I.months, { n: v }), String(d.horizon) === String(v)); }).join('') + '</div>';
    }
    else if (id === 'kill') {
      q = t(I.qKill, tk); body = '<label class="fld"><input type="text" id="iv-in" data-field="kill" maxlength="600" placeholder="' + esc(L(T.fKillPh)) + '" value="' + esc(d.kill) + '"></label><p class="sub">' + L(I.hKill) + '</p><div class="choices col">' +
        (R.watch[sec] || R.watch['*']).map(function (w) { return choice('data-ivfill', L(w), esc(L(w)), d.kill === L(w)); }).join('') + '</div>';
    }
    else if (id === 'done') {
      var res = E.analyse(state).positions.filter(function (x) { return x.id === d.id; })[0];
      var h = '<div class="iv done"><p class="ivq">' + t(I.doneT, tk) + '</p>';
      if (res) {
        h += '<p>' + (res.suggest == null ? L(I.doneNoSize) : t(I.doneSize, { w: g(res.weight), s: g(res.suggest), act: L(T.act[res.action]).toLowerCase() })) + '</p>';
        var top = res.ev_.challenge[0] || res.ev_.blindRisk[0];
        if (top) h += '<p class="lab">' + L(I.doneAgainst) + '</p><div class="ev against"><ul><li>' + esc(L(top.text)) + ' ' + srcLink(top.src) + '</li></ul></div>';
      }
      box.innerHTML = h + '<p class="btns"><button type="button" class="btn primary" id="iv-another">' + L(I.another) + '</button><button type="button" class="btn" id="iv-see">' + L(I.see) + '</button></p></div>';
      return;
    }
    box.innerHTML = '<form class="iv" id="iv-form" autocomplete="off"><div class="ivbar"><i style="width:' + (k / real.length * 100).toFixed(0) + '%"></i></div><p class="ivstep">' + t(I.progress, { k: k, n: real.length }) + (d.ticker && id !== 'ticker' ? ' · ' + esc(d.ticker) : '') + '</p>' +
      '<p class="ivq" id="iv-q">' + q + '</p>' + (hint ? '<p class="sub">' + hint + '</p>' : '') + (note ? '<p class="ivnote">' + note + '</p>' : '') + body +
      '<p class="btns">' + (nav ? '<button type="submit" class="btn primary">' + L(I.next) + '</button>' : '') + (iv.i > 0 ? '<button type="button" class="btn" id="iv-back">' + L(I.back) + '</button>' : '') +
      (skippable ? '<button type="button" class="lnk" id="iv-skip">' + L(I.skip) + '</button>' : '') + '<span class="spacer"></span>' +
      (id !== 'dd' ? '<button type="button" class="lnk" id="iv-form-switch">' + L(I.form) + '</button>' : '') + (state.positions.length || iv.i > 0 ? '<button type="button" class="lnk" id="iv-stop">' + L(I.stop) + '</button>' : '') +
      '<span class="err" id="iv-err" role="alert"></span></p></form>';
    var inp = $('iv-in'); if (inp && !iv.auto) inp.focus({ preventScroll: true });
  }
  function ivRead() { var el = $('iv-in'); if (!el) return; var f = el.getAttribute('data-field'), v = el.value; if (f === 'ticker') v = v.toUpperCase().replace(/[^A-Z0-9]/g, '').slice(0, 8); iv.draft[f] = v; }
  function ivGo(delta) {
    var d = iv.draft, id = iv.steps[iv.i];
    if (delta > 0 && id === 'ticker') {
      if (!d.ticker) { $('iv-err').textContent = L(T.needTicker); return; }
      var mk = M.t[d.ticker]; if (mk) d.sector = mk.sec;
    }
    iv.auto = false;
    iv.steps = ivSteps(d, iv.askDD);
    iv.i = Math.max(0, Math.min(iv.steps.length - 1, iv.steps.indexOf(id) + delta));
    if (iv.steps[iv.i] === 'done') ivFinish(); else renderInterview();
  }
  function ivFinish() {
    var d = iv.draft, ok = driversFor(M.t[d.ticker] ? M.t[d.ticker].sec : d.sector);
    d.likes = d.likes.filter(function (x) { return ok.indexOf(x) >= 0; }); d.dislikes = d.dislikes.filter(function (x) { return ok.indexOf(x) >= 0 && d.likes.indexOf(x) < 0; });
    if (d.status === 'idea') d.weight = '0';
    state.positions.push(d); state = clean(state); save();
    var keep = iv; renderInput(); iv = keep; renderInterview(); renderResults();
  }
  function renderEditor() {
    var box = $('editor'); if (!box) return;
    if (!editing && !iv && !state.positions.length) startInterview(true);
    if (!editing && iv) { renderInterview(); return; }
    if (!editing) { box.innerHTML = ''; return; }
    var p = editing, mk = M.t[p.ticker], sec = mk ? mk.sec : p.sector, isNew = !state.positions.some(function (x) { return x.id === p.id; });
    var defP = E.RULES.pByConv[p.conviction - 1];
    var h = '<form class="editor" id="ed-form" autocomplete="off"><h3>' + L(isNew ? T.edNew : T.edEdit) + (p.ticker ? ' · ' + esc(p.ticker) + (mk ? ' <span class="sub">' + esc(mk.name) + ' · ' + secName(sec) + '</span>' : '') : '') + '</h3><div class="grid3">' +
      field(L(T.fTicker), '<input type="text" id="ed-ticker" list="ticker-list" maxlength="8" value="' + esc(p.ticker) + '" required>') +
      (mk ? '' : field(L(T.fSector), '<select id="ed-sector">' + Object.keys(R.sectors).map(function (k) { return opt(k, secName(k), p.sector); }).join('') + '</select>', p.ticker ? L(T.fSectorHint) : '')) +
      field(L(T.fStatus), '<select id="ed-status">' + opt('hold', L(T.stHold), p.status) + opt('idea', L(T.stIdea), p.status) + '</select>') +
      field(L(T.fWeight), '<input type="number" id="ed-weight" min="0" max="200" step="0.5" inputmode="decimal" value="' + esc(p.weight) + '">') +
      field(L(T.fConv), '<select id="ed-conviction">' + [1, 2, 3, 4, 5].map(function (i) { return opt(i, L(T['conv' + i]), p.conviction); }).join('') + '</select>') +
      field(L(T.fUp), '<input type="number" id="ed-up" min="0" max="1000" step="1" inputmode="decimal" value="' + esc(p.up) + '">') +
      field(L(T.fDown), '<input type="number" id="ed-down" min="0" max="100" step="1" inputmode="decimal" value="' + esc(p.down) + '">', L(T.fDownHint)) +
      field(L(T.fProb), '<input type="number" id="ed-p" min="1" max="99" step="1" inputmode="decimal" placeholder="' + defP + '" value="' + esc(p.p) + '">', t(T.fProbHint, { p: defP })) +
      field(L(T.fHorizon), '<input type="number" id="ed-horizon" min="1" max="120" step="1" inputmode="numeric" value="' + esc(p.horizon) + '">') +
      field(L(T.fEdge), '<select id="ed-edge">' + ['none', 'info', 'analysis', 'time', 'behaviour'].map(function (k) { return opt(k, L(T['edge' + k.charAt(0).toUpperCase() + k.slice(1)]), p.edge); }).join('') + '</select>') + '</div>' +
      '<div class="fld"><span class="lab">' + L(T.fLikes) + '</span>' + chips('like', p.likes, sec) + '</div>' +
      '<div class="fld"><span class="lab">' + L(T.fDislikes) + '</span>' + chips('dislike', p.dislikes, sec) + '</div>' +
      field(L(T.fThesis), '<textarea id="ed-thesis" rows="3" maxlength="2000" placeholder="' + esc(L(T.fThesisPh)) + '">' + esc(p.thesis) + '</textarea>') +
      '<div class="grid2">' + field(L(T.fCatalyst), '<input type="text" id="ed-catalyst" maxlength="600" placeholder="' + esc(L(T.fCatalystPh)) + '" value="' + esc(p.catalyst) + '">') +
      field(L(T.fKill), '<input type="text" id="ed-kill" maxlength="600" placeholder="' + esc(L(T.fKillPh)) + '" value="' + esc(p.kill) + '">') + '</div>' +
      '<p class="btns"><button type="submit" class="btn primary">' + L(T.save) + '</button><button type="button" class="btn" id="ed-cancel">' + L(T.cancel) + '</button><span class="err" id="ed-err" role="alert"></span></p></form>';
    box.innerHTML = h;
  }
  function readEditor() {
    if (!editing) return;
    ['ticker', 'sector', 'status', 'weight', 'conviction', 'up', 'down', 'p', 'horizon', 'edge', 'thesis', 'catalyst', 'kill'].forEach(function (k) { var el = $('ed-' + k); if (el) editing[k] = el.value; });
    editing.ticker = editing.ticker.toUpperCase().replace(/[^A-Z0-9]/g, '').slice(0, 8);
    editing.conviction = parseInt(editing.conviction, 10) || 3;
  }
  function blank() { return { id: uid(), ticker: '', sector: 'other', status: 'hold', weight: '', conviction: 3, up: '', down: '', p: '', horizon: '', edge: 'none', likes: [], dislikes: [], thesis: '', catalyst: '', kill: '' }; }

  /* ---------- section 2: consult ---------- */
  function tile(label, value, note, cls) { return '<div class="tile"><div class="label">' + label + '</div><div class="value' + (cls ? ' ' + cls : '') + '">' + value + '</div><div class="note">' + note + '</div></div>'; }
  function listT(a) { return a.map(esc).join(', '); }

  function findingText(f) {
    var d = f.data, tp = T.f[f.code], v = {};
    switch (f.code) {
      case 'leverage': v = { v: n0(d.v) }; break;
      case 'overInvested': v = { v: n0(d.v), hi: d.hi, r: L(T['rg' + d.regime.charAt(0).toUpperCase() + d.regime.slice(1)]).toLowerCase() }; break;
      case 'underInvested': v = { v: n0(d.v), lo: d.lo }; break;
      case 'stress': v = { v: n(d.v), max: g(d.max) }; break;
      case 'fewBets': v = { n: d.n, neff: n(d.neff), c: n(d.corr, 2) }; break;
      case 'sector': v = { s: secName(d.sector), v: n0(d.v), cap: d.cap }; break;
      case 'cluster': v = { s: L(R.clusters[d.cluster]), v: n0(d.v), cap: d.cap }; break;
      case 'overCap': v = { t: d.t, v: g(d.v), cap: d.cap, conv: d.conv }; break;
      case 'negEV': v = { t: d.t, be: n0(d.be), p: n0(d.prob) }; break;
      case 'riskSkew': v = { t: d.t, c: n0(d.cap), r: n0(d.risk) }; break;
      case 'illiquid': v = { t: d.t, d: n0(Math.ceil(d.days)) }; break;
      case 'convMismatch': v = { big: d.big, bw: g(d.bigW), bc: d.bigConv, small: d.small, sw: g(d.smallW), sc: d.smallConv }; break;
      case 'pair': v = { a: d.a, b: d.b, c: n(d.c, 2) }; break;
      case 'stale': v = { list: d.list.join(', '), d: d.days }; break;
      case 'priceStale': v = { d: d.days }; break;
      default: v = { list: (d.list || []).join(', ') };
    }
    return { title: t(tp[0], v), body: t(tp[1], v) };
  }

  function whyText(m) { return m.why.map(function (w) { return L(T.why[w]); }).join(' · '); }

  function renderConsult(a) {
    var box = $('pm-consult');
    if (!a.positions.length) { box.innerHTML = ''; box.hidden = true; return; }
    box.hidden = false;
    var reg = a.regime, now = a.now, aft = a.after, h = '<h2 id="nhan-dinh">' + L(T.s2) + '</h2>';
    var held = now.n > 0;

    /* tiles */
    if (held) {
      var over = now.invested > reg.band[1] + 0.5;
      h += '<div class="tiles">' +
        tile(L(T.tInvested), n0(now.invested) + '%', t(T.tInvestedNote, { cash: n0(Math.max(0, 100 - now.invested)), lo: reg.band[0], hi: reg.band[1] }), over ? 'down' : '') +
        tile(L(T.tBets), n(now.neff), t(T.tBetsNote, { n: now.n, c: now.avgCorr == null ? '–' : n(now.avgCorr, 2) })) +
        tile(L(T.tVol), '−' + n(now.badMonth) + '%', t(T.tVolNote, { v: n(now.vol), b: n(now.beta, 2) })) +
        tile(L(T.tStress), '−' + n(now.stress) + '%', t(T.tStressNote, { m: g(a.maxDD) }), now.stress > a.maxDD ? 'down' : '') + '</div>';
      if (aft.n) h += '<p class="after">' + t(T.afterLine, { inv: n0(aft.invested), neff: n(aft.neff), bad: n(aft.badMonth), stress: n(aft.stress) }) + '</p>';
    }

    /* regime */
    var gw = L(T['g' + reg.growth.charAt(0).toUpperCase() + reg.growth.slice(1)]);
    var k = R.regime.liquidity.filter(function (x) { return x.dir < 0; }).length + (reg.indexD200 < 0 ? 1 : 0);
    h += '<figure class="viz"><p class="viz-title">' + L(T.hRegime) + '</p><p class="viz-sub">' + t(T.regimeLine[reg.use], { g: gw }) + (reg.overridden ? ' ' + t(T.regimeOver, { a: L(T['rg' + reg.auto.charAt(0).toUpperCase() + reg.auto.slice(1)]).toLowerCase() }) : '') + '</p>' +
      '<p class="body">' + t(T.regimeWhy, { k: k, n: reg.n, lo: reg.band[0], hi: reg.band[1] }) + '</p><div class="grid2 sig">';
    function sigs(title, arr, extra) { return '<div><p class="lab">' + title + '</p><ul class="signals">' + arr.map(function (x) { return '<li class="' + (x.dir < 0 ? 'neg' : 'pos') + '"><span class="mark" aria-hidden="true">' + (x.dir < 0 ? '▼' : '▲') + '</span>' + esc(L(x.text)) + '</li>'; }).join('') + (extra || '') + '</ul></div>'; }
    var idx = '<li class="' + (reg.indexD200 < 0 ? 'neg' : 'pos') + '"><span class="mark" aria-hidden="true">' + (reg.indexD200 < 0 ? '▼' : '▲') + '</span>' + t(T.idxLine, { d: sg(reg.indexD200), date: date(M.asof) }) + '</li>';
    h += sigs(L(T.liq), R.regime.liquidity, idx) + sigs(L(T.gro), R.regime.growth) + '</div><figcaption>' + L(T.src) + ': ' + srcLink('macro') + ' · ' + srcLink('druck') + ' · ' + srcLink('market') + '</figcaption></figure>';

    /* findings */
    h += '<h3>' + L(T.hFind) + '</h3>';
    if (!a.findings.length) h += '<p class="empty">' + L(T.noFind) + '</p>';
    else h += '<ul class="findings">' + a.findings.map(function (f) { var x = findingText(f); return '<li class="sev' + f.sev + '"><p class="ft"><span class="pill sev' + f.sev + '">' + L(T['sev' + f.sev]) + '</span> ' + x.title + ' <span class="lens">' + L(T.lens[f.lens]) + '</span></p><p class="fb">' + x.body + '</p></li>'; }).join('') + '</ul>';

    /* allocation */
    var maxW = 5; a.positions.forEach(function (m) { maxW = Math.max(maxW, m.weight, m.suggest || 0); });
    h += '<figure class="viz"><p class="viz-title">' + L(T.hAlloc) + '</p><p class="viz-sub">' + L(T.allocSub) + '</p><div class="legend"><span><i class="sw now"></i>' + L(T.legNow) + '</span><span><i class="sw sug"></i>' + L(T.legSug) + '</span></div>';
    a.positions.forEach(function (m) {
      h += '<div class="alloc"><div class="name">' + esc(m.ticker) + '</div><div class="track"><div class="bar now" style="width:' + (m.weight / maxW * 100).toFixed(1) + '%"></div><div class="bar sug" style="width:' + ((m.suggest || 0) / maxW * 100).toFixed(1) + '%"></div></div><div class="val">' + g(m.weight) + ' → ' + (m.suggest == null ? '–' : g(m.suggest)) + '%</div></div>';
    });
    h += '<details class="tbl"><summary>' + L(T.thWhy) + '</summary><div class="tablewrap"><table><thead><tr><th>' + L(T.thTicker) + '</th><th class="num">' + L(T.thNow) + '</th><th class="num">' + L(T.thSug) + '</th><th>' + L(T.thAct) + '</th><th>' + L(T.thWhy) + '</th></tr></thead><tbody>' +
      a.positions.map(function (m) { return '<tr><td>' + esc(m.ticker) + '</td><td class="num">' + g(m.weight) + '%</td><td class="num">' + (m.suggest == null ? '–' : g(m.suggest) + '%') + '</td><td><span class="pill act-' + m.action + '">' + L(T.act[m.action]) + '</span></td><td>' + whyText(m) + '</td></tr>'; }).join('') +
      '<tr><td>' + L(T.cash) + '</td><td class="num">' + n0(Math.max(0, 100 - now.invested)) + '%</td><td class="num">' + n0(Math.max(0, 100 - aft.invested)) + '%</td><td></td><td></td></tr></tbody></table></div></details></figure>';

    /* positions */
    h += '<h3>' + L(T.hPos) + '</h3>';
    a.positions.forEach(function (m, i) { h += positionCard(m, a, i === 0); });
    box.innerHTML = h;
  }

  function evList(title, arr, cls) {
    if (!arr.length) return '';
    return '<div class="ev ' + cls + '"><p class="lab">' + title + ' (' + arr.length + ')</p><ul>' + arr.map(function (e) { return '<li>' + esc(L(e.text)) + ' ' + srcLink(e.src) + '</li>'; }).join('') + '</ul></div>';
  }

  function positionCard(m, a, open) {
    var p = state.positions.filter(function (x) { return x.id === m.id; })[0] || {}, mk = m.mk, ev = m.ev_, reg = a.regime;
    var h = '<details class="pos"' + (open ? ' open' : '') + '><summary><span class="tk">' + esc(m.ticker) + '</span><span class="nm">' + esc(mk ? mk.name : '') + ' · ' + secName(m.sector) + '</span><span class="wt">' + g(m.weight) + '% → ' + (m.suggest == null ? '–' : g(m.suggest) + '%') + '</span><span class="pill act-' + m.action + '">' + L(T.act[m.action]) + '</span></summary><div class="posbody">';
    if (p.thesis) h += '<blockquote>' + esc(p.thesis) + '</blockquote>';

    /* numbers */
    h += '<h4>' + L(T.pNumbers) + '</h4>';
    if (!m.complete) h += '<p>' + L(T.pNoNum) + '</p>';
    else {
      h += '<p>' + t(T.pBE, { be: n0(m.breakeven), p: n0(m.prob), d: m.probDefault ? L(T.pDef) : '' }) + ' ' + t(T.pEV, { ev: sg(m.ev), r: n(m.payoff) }) + '</p>';
      if (m.ev <= 0) h += '<p class="warn">' + L(T.pNeg) + '</p>';
      else {
        h += '<p>' + t(T.pSize, { a: n(m.riskW), r: n(m.riskPct, 2), k: n(m.kellyCap), c: m.cap }) + (m.noise ? ' ' + t(T.pNoiseSize, { d: g(m.down), m: n(m.monthSigma) }) : '') + (m.tilt < 1 ? ' ' + t(T.pTilt, { t: n(m.tilt, 2) }) : '');
        var sc = m.why.filter(function (w) { return w === 'sector' || w === 'cluster' || w === 'total'; });
        if (sc.length) h += ' ' + t(T.pScaled, { w: sc.map(function (w) { return L(T.why[w]); }).join(', ') });
        h += '</p><p class="sub">' + t(T.pFragile, { p: n0(m.prob - 10), ev: sg(((m.prob - 10) / 100 * m.up - (1 - (m.prob - 10) / 100) * m.down)) }) + '</p>';
      }
    }

    /* price */
    h += '<h4>' + L(T.pPrices) + '</h4>';
    if (mk) {
      var d200 = mk.d200 != null ? mk.d200 : mk.d50;
      h += '<p>' + (m.trend === 'unknown' ? L(T.pTrend.unknown) : t(T.pTrend[m.trend], { a: sg(d200), b: sg(mk.rs3m) })) + ' ' + t(T.pVol, { v: n(mk.vol), m: n(m.monthSigma), dd: n(mk.dd), b: n(mk.beta, 2) }) + '</p>' +
        '<p class="sub">' + t(T.pVal, { pe: mk.pe > 60 ? '>60' : n(mk.pe), pb: n(mk.pb, 2), adtv: n0(mk.adtv), px: px(mk.px), date: date(mk.asof) }) + (m.exitDays != null && m.exitDays >= 1 ? ' ' + t(T.pExit, { d: n0(Math.ceil(m.exitDays)) }) : '') + '</p>';
    } else h += '<p>' + t(T.pNoMk, { v: n(m.vol) }) + '</p>';

    /* research */
    h += '<h4>' + L(T.pResearch) + '</h4>';
    if (!ev.tickerLevel && !ev.sectorLevel) h += '<p class="warn">' + L(T.rNone) + '</p>';
    else {
      if (!ev.tickerLevel) h += '<p class="sub">' + L(T.rSectorOnly) + '</p>';
      if (m.stale) h += '<p class="warn">' + t(T.rStale, { d: m.reportAge }) + '</p>';
      if (!(p.likes || []).length && !(p.dislikes || []).length) h += '<p class="sub">' + L(T.rTagHint) + '</p>';
    }
    h += evList(L(T.rChallenge), ev.challenge, 'against') + evList(L(T.rAgree), ev.agree, 'for') + evList(L(T.rBlindRisk), ev.blindRisk, 'against') + evList(L(T.rBlindSupport), ev.blindSupport, 'for');
    if (ev.forN + ev.againstN) h += '<p class="sub">' + t(T.rBalance, { f: ev.forN, a: ev.againstN }) + '</p>';

    /* lenses */
    var miss = []; if (!m.hasThesis) miss.push(L(T.bfMissThesis)); if (m.edge === 'none') miss.push(L(T.bfMissEdge));
    var bf = [miss.length ? t(T.bfUnderstand.part, { x: miss.join(LI ? ' and ' : ' và ') }) : L(T.bfUnderstand.yes),
      !m.complete ? L(T.bfSafety.none) : t(T.bfSafety[m.payoff >= 2 ? 'good' : 'thin'], { r: n(m.payoff) })];
    if (mk) bf.push(t(T.bfHold, { dd: n0(Math.abs(mk.dd)) }));
    var liqKey = reg.use === 'tight' ? (m.tilt < 1 || R.sectors[m.sector].tilt < 1 ? 'tight' : 'tight1') : reg.use;
    var sizeKey = m.suggest == null ? 'na' : (m.action === 'trim' || m.action === 'exit') ? 'big' : m.action === 'add' ? 'small' : 'ok';
    var dr = [t(T.drLiq[liqKey], { t: n(R.sectors[m.sector].tilt, 2) }), L(T.drPrice[m.trend]), t(T.drSize[sizeKey], { w: g(m.weight), s: g(m.suggest || 0) })];
    var da = [];
    if (m.riskShare != null && m.capShare != null) da.push(t(T.daRisk, { c: n0(m.capShare), r: n0(m.riskShare) }));
    da.push(m.corrOthers == null ? L(T.daCorr.na) : t(T.daCorr[m.corrOthers >= 0.55 ? 'high' : m.corrOthers >= 0.3 ? 'mid' : 'low'], { c: n(m.corrOthers, 2) }));
    var cons = R.consensus[m.ticker];
    da.push(cons >= 2 ? t(T.daPriced.consensus, { n: cons }) : (ev.forN + ev.againstN) ? t(T.daPriced.balance, { f: ev.forN, a: ev.againstN }) : L(T.daPriced.none));
    function lens(name, items) { return '<div class="lensbox"><p class="lab">' + name + '</p><ul>' + items.map(function (x) { return '<li>' + x + '</li>'; }).join('') + '</ul></div>'; }
    h += '<h4>' + L(T.pLens) + '</h4><div class="grid3 lenses">' + lens('Buffett', bf) + lens('Druckenmiller', dr) + lens('Dalio', da) + '</div>';

    /* plan */
    var key = m.action;
    if (key === 'start' || key === 'add') key += (m.tranches === 2 ? '2' : m.trend === 'against' ? '3a' : '3');
    h += '<h4>' + L(T.pPlan) + '</h4><p><strong>' + t(T.plan[key], { w: g(m.weight), s: g(m.suggest || 0) }) + '</strong></p><ul class="plan">';
    h += '<li>' + (m.hasKill ? t(T.xThesis, { k: p.kill }) : L(T.xThesisNone)) + '</li>';
    if (m.complete) {
      h += '<li>' + (mk ? t(T.xPrice, { px: px(mk.px * (1 - m.down / 100)), d: g(m.down), date: date(mk.asof) }) : t(T.xPriceNo, { d: g(m.down) })) + (m.noise ? ' <span class="warn">' + t(T.xNoise, { m: n(m.monthSigma) }) + '</span>' : '') + '</li>';
      h += '<li>' + (mk ? t(T.xTarget, { px: px(mk.px * (1 + m.up / 100)), u: g(m.up) }) : t(T.xTargetNo, { u: g(m.up) })) + '</li>';
    }
    h += '<li>' + (m.horizon ? t(T.xTime, { h: g(m.horizon) }) : L(T.xTimeNo)) + '</li><li>' + t(T.xSize, { c: m.cap }) + '</li></ul>';
    var watch = (R.watch[m.sector] || []).concat(R.watch['*']);
    h += '<p class="lab">' + L(T.xWatch) + '</p><ul class="watch">' + watch.map(function (w) { return '<li>' + esc(L(w)) + '</li>'; }).join('') + '</ul>';

    /* questions */
    h += '<h4>' + L(T.pQuestions) + '</h4><ol class="qs">' + m.questions.map(function (q) {
      return '<li>' + t(T.q[q], { be: n0(m.breakeven), p: n0(m.prob), d: g(m.down), m: n(m.monthSigma), dd: mk ? n0(Math.abs(mk.dd)) : '', n: ev.challenge.length }) + '</li>';
    }).join('') + '</ol>';
    h += '<p class="btns"><button type="button" class="btn" data-edit="' + esc(m.id) + '">' + L(T.edit) + ' ' + esc(m.ticker) + '</button></p></div></details>';
    return h;
  }

  /* ---------- static sections ---------- */
  function renderStatic() {
    doc.querySelectorAll('[data-t]').forEach(function (el) { el.textContent = L(T[el.getAttribute('data-t')]); });
    var h = '<h2 id="khung-tu-duy">' + L(T.s3) + '</h2><p>' + L(T.s3note) + '</p><div class="cards fw">' + T.fw.map(function (f) { return '<div class="card"><h3>' + L(f[0]) + '</h3><p class="sum">' + L(f[1]) + '</p><p class="meta">' + L(f[2]) + '</p></div>'; }).join('') + '</div>';
    h += '<h2 id="phuong-phap">' + L(T.s4) + '</h2><ul>' + T.method.map(function (x) { return '<li>' + t(x, { n: M.order.length, s: M.sessions, d: date(M.asof), r: date(R.asof) }) + '</li>'; }).join('') + '</ul>';
    h += '<ul class="srcs">' + Object.keys(R.reports).map(function (k) { return '<li>' + srcLink(k) + '</li>'; }).join('') + '</ul><p class="disclaimer">' + L(T.disclaimer) + '</p>';
    $('pm-static').innerHTML = h;
    $('ticker-list').innerHTML = M.order.map(function (k) { return '<option value="' + k + '">' + esc(M.t[k].name) + '</option>'; }).join('');
  }

  function renderResults() { renderConsult(E.analyse(state)); }
  function render() { renderInput(); renderResults(); }

  /* ---------- events ---------- */
  doc.addEventListener('click', function (e) {
    var el = e.target.closest('button'); if (!el) return;
    var id = el.id, ed = el.getAttribute('data-edit'), del = el.getAttribute('data-del'), chip = el.getAttribute('data-chip');
    var a;
    if (iv && !editing) {
      if ((a = el.getAttribute('data-ivdd'))) { state.settings.maxDD = parseFloat(a); state.settings.asked = true; save(); iv.askDD = false; iv.steps = ivSteps(iv.draft, false); iv.i = 0; iv.auto = false; renderInput(); renderResults(); return; }
      if ((a = el.getAttribute('data-ivset'))) { ivRead(); var kv = a.split(':'); iv.draft[kv[0]] = kv[0] === 'conviction' ? parseInt(kv[1], 10) : kv[1]; ivGo(1); return; }
      if ((a = el.getAttribute('data-ivnum'))) { var nv = a.split(':'); iv.draft[nv[0]] = nv[1]; ivGo(1); return; }
      if ((a = el.getAttribute('data-ivhz'))) { ivRead(); iv.draft.horizon = iv.draft.horizon === a ? '' : a; renderInterview(); return; }
      if ((a = el.getAttribute('data-ivfill'))) { iv.draft.kill = a; renderInterview(); return; }
      if ((a = el.getAttribute('data-ivchip'))) { var lc = a.split(':'), arr = iv.draft[lc[0]], ix = arr.indexOf(lc[1]); if (ix >= 0) arr.splice(ix, 1); else arr.push(lc[1]); renderInterview(); return; }
      if (id === 'iv-back') { ivRead(); ivGo(-1); return; }
      if (id === 'iv-skip') { var fld = $('iv-in'); if (fld) iv.draft[fld.getAttribute('data-field')] = ''; ivGo(1); return; }
      if (id === 'iv-stop') { iv = null; renderEditor(); if (!state.positions.length) renderInput(); return; }
      if (id === 'iv-form-switch') { ivRead(); editing = iv.draft; iv = null; renderEditor(); return; }
      if (id === 'iv-another') { startInterview(false); renderInterview(); $('editor').scrollIntoView({ block: 'center' }); return; }
      if (id === 'iv-see') { iv = null; renderEditor(); var c0 = $('nhan-dinh'); if (c0) c0.scrollIntoView({ block: 'start' }); return; }
    }
    if (chip && editing) {
      readEditor();
      var kind = el.parentNode.getAttribute('data-kind'), mine = kind === 'like' ? 'likes' : 'dislikes', other = kind === 'like' ? 'dislikes' : 'likes';
      var i = editing[mine].indexOf(chip);
      if (i >= 0) editing[mine].splice(i, 1); else { editing[mine].push(chip); editing[other] = editing[other].filter(function (x) { return x !== chip; }); }
      renderEditor(); return;
    }
    if (ed) { var p = state.positions.filter(function (x) { return x.id === ed; })[0]; if (p) { iv = null; editing = JSON.parse(JSON.stringify(p)); renderInput(); $('editor').scrollIntoView({ block: 'start' }); var f = $('ed-weight'); if (f) f.focus({ preventScroll: true }); } return; }
    if (del) { state.positions = state.positions.filter(function (x) { return x.id !== del; }); if (editing && editing.id === del) editing = null; save(); render(); return; }
    if (id === 'b-add') { startInterview(false); renderInterview(); $('editor').scrollIntoView({ block: 'center' }); }
    else if (id === 'ed-cancel') { editing = null; iv = null; renderEditor(); }
    else if (id === 'b-example') { if (!state.positions.length || confirm(L(T.confirmExample))) loadExample(); }
    else if (id === 'b-clear') { if (confirm(L(T.confirmClear))) { state.positions = []; editing = null; iv = null; save(); render(); } }
    else if (id === 'b-print') { doc.querySelectorAll('details.pos').forEach(function (d) { d.open = true; }); window.print(); }
    else if (id === 'b-export') {
      var blob = new Blob([JSON.stringify(state, null, 1)], { type: 'application/json' }), a = doc.createElement('a');
      a.href = URL.createObjectURL(blob); a.download = 'danh-muc-' + new Date().toISOString().slice(0, 10) + '.json'; doc.body.appendChild(a); a.click(); a.remove(); setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
    }
    else if (id === 'b-import') $('f-import').click();
  });
  doc.addEventListener('submit', function (e) {
    if (e.target.id === 'iv-form') { e.preventDefault(); ivRead(); ivGo(1); return; }
    if (e.target.id !== 'ed-form') return;
    e.preventDefault(); readEditor();
    if (!editing.ticker) { $('ed-err').textContent = L(T.needTicker); return; }
    var mk = M.t[editing.ticker]; if (mk) editing.sector = mk.sec;
    var ok = driversFor(editing.sector); editing.likes = editing.likes.filter(function (d) { return ok.indexOf(d) >= 0; }); editing.dislikes = editing.dislikes.filter(function (d) { return ok.indexOf(d) >= 0; });
    var i = -1; state.positions.forEach(function (x, j) { if (x.id === editing.id) i = j; });
    if (i >= 0) state.positions[i] = editing; else state.positions.push(editing);
    state = clean(state); editing = null; save(); render();
    var c = $('nhan-dinh'); if (c) c.scrollIntoView({ block: 'start' });
  });
  doc.addEventListener('change', function (e) {
    var id = e.target.id;
    if (id === 'set-maxDD' || id === 'set-regime' || id === 'set-capital') {
      if (!$('set-maxDD')) return;
      state.settings.maxDD = Math.min(60, Math.max(3, parseFloat($('set-maxDD').value) || 15)); state.settings.regime = $('set-regime').value; state.settings.capital = $('set-capital').value;
      save(); renderResults();
    } else if (editing && (id === 'ed-ticker' || id === 'ed-sector' || id === 'ed-conviction')) { readEditor(); var mk = M.t[editing.ticker]; if (mk) editing.sector = mk.sec; renderEditor(); }
    else if (id === 'f-import') {
      var file = e.target.files[0]; if (!file) return;
      var rd = new FileReader();
      rd.onload = function () { var s = null; try { s = clean(JSON.parse(rd.result)); } catch (err) {} if (!s) { alert(L(T.importBad)); return; } state = s; editing = null; iv = null; save(); render(); };
      rd.readAsText(file);
    }
  });

  load(); renderStatic(); render();
})();
