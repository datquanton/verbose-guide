/* Portfolio intake: turn a pasted list or the text recognised from a broker screenshot into {ticker, weight} rows.
   parse() is pure and runs in Node for testing; readImage() runs text recognition in the browser, on the device. */
(function (root) {
  'use strict';
  /* three-letter words that appear on broker screens and are not tickers */
  var STOP = ('VND USD KLG GIA TKL TKH TSL LAI BAN MUA TAI SAN CCQ TON LOT ALL SUM NAV ETF PNL AVG QTY VOL MAX MIN THE AND FOR TOP DAY NET HNX HSX VNI YTD ROE EPS BUY SEL TAX FEE CASH').split(' ');

  function toNum(tok) {
    var s = tok.replace(/[^\d.,\-]/g, ''); if (!/\d/.test(s)) return null;
    var neg = s.charAt(0) === '-'; s = s.replace(/-/g, '');
    var hasDot = s.indexOf('.') >= 0, hasCom = s.indexOf(',') >= 0, v;
    if (hasDot && hasCom) {                                   // the later separator is the decimal one
      var dec = s.lastIndexOf('.') > s.lastIndexOf(',') ? '.' : ',', th = dec === '.' ? ',' : '.';
      v = parseFloat(s.split(th).join('').replace(dec, '.'));
    } else if (hasDot || hasCom) {
      var sep = hasDot ? '.' : ',', parts = s.split(sep);
      var thousands = parts.length > 2 || (parts[1].length === 3 && parts[0].length <= 3 && parts[0] !== '0');
      v = thousands ? parseFloat(parts.join('')) : parseFloat(parts.join('.'));
    } else v = parseFloat(s);
    return isFinite(v) ? (neg ? -v : v) : null;
  }

  function parse(text, known, prices) {
    known = known || {}; prices = prices || {};
    var rows = [], cur = null, fixed = false, names = Object.keys(known);
    function priced(k, rest) {
      if (!prices[k]) return false;
      return rest.some(function (t) { if (!/\d/.test(t) || /%/.test(t)) return false; var v = toNum(t); return v > 0 && Math.abs((v < 1000 ? v * 1000 : v) / prices[k] - 1) < 0.25; });
    }
    function fuzzy(w, rest) {
      var nums = []; rest.forEach(function (t) { if (/\d/.test(t) && !/%/.test(t)) { var v = toNum(t); if (v > 0) nums.push(v < 1000 ? v * 1000 : v); } });
      if (nums.length < 2) return null;
      var hit = names.filter(function (k) {
        if (k.length !== 3) return false; var d = 0; for (var c = 0; c < 3; c++) if (k.charAt(c) !== w.charAt(c)) d++;
        return d === 1 && prices[k] && nums.some(function (v) { return Math.abs(v / prices[k] - 1) < 0.1; });
      });
      return hit.length === 1 ? hit[0] : null;
    }
    String(text || '').replace(/[,;]\s+(?=[A-Za-z]{3}\b)/g, '\n').split(/\r?\n/).forEach(function (line) {
      var toks = line.replace(/[|\[\]{}()]/g, ' ').split(/\s+/).filter(Boolean), tk = null, ti = -1;
      for (var pass = 0; pass < 2 && !tk; pass++) for (var i = 0; i < toks.length && i < 3; i++) {         // a ticker sits at the start of its row
        var w = toks[i].replace(/[^A-Za-z0-9]/g, '').toUpperCase();
        if (!/^[A-Z0-9]{3}$/.test(w)) continue;
        if (pass === 0) { if (known[w] && (toks[i].replace(/[^A-Za-z0-9]/g, '') === w || priced(w, toks.slice(i + 1)))) { tk = w; ti = i; break; } continue; }   // an exact ticker at the row start wins; a lower-case word must be confirmed by a price
        var fz = fuzzy(w, toks.slice(i + 1));                                    // one misread letter, confirmed by a price on the row
        if (fz) { tk = fz; ti = i; fixed = true; break; }
        if (/^[A-Z]/.test(w) && /[A-Z]{2}/.test(w) && STOP.indexOf(w) < 0 && toks[i] === toks[i].toUpperCase()) { tk = w; ti = i; break; }
      }
      if (tk) { cur = { ticker: tk, nums: [], pcts: [], known: !!known[tk] }; rows.push(cur); toks = toks.slice(ti + 1); }
      if (!cur) return;
      toks.forEach(function (t) {
        if (!/\d/.test(t) || /[A-Za-z]{2}/.test(t.replace(/VND|vnd|đ|tr|k/g, ''))) return;
        var v = toNum(t); if (v == null) return;
        if (/%/.test(t)) cur.pcts.push(v); else cur.nums.push(v);
      });
    });
    /* merge repeated tickers (a screen can list one stock on two lines) */
    var by = {}, list = [];
    rows.forEach(function (r) { if (by[r.ticker]) { by[r.ticker].nums = by[r.ticker].nums.concat(r.nums); by[r.ticker].pcts = by[r.ticker].pcts.concat(r.pcts); } else { by[r.ticker] = r; list.push(r); } });
    list = list.filter(function (r) { return r.known || r.nums.length || r.pcts.length; });
    if (!list.length) return { mode: 'none', rows: [] };

    /* A: the text already gives weights ("VCB 20%", "HPG 15") */
    var simple = list.filter(function (r) { var all = r.nums.concat(r.pcts); return all.length === 1 && all[0] > 0 && all[0] <= 100; });
    var sumA = simple.reduce(function (s, r) { return s + r.nums.concat(r.pcts)[0]; }, 0);
    if (simple.length >= Math.max(1, list.length * 0.6) && sumA <= 100.5) {
      return { mode: 'weights', rows: list.map(function (r) { var a = r.nums.concat(r.pcts); var w = r.pcts.length ? r.pcts[0] : a[0]; return { ticker: r.ticker, weight: w > 0 && w <= 100 ? w : null, known: r.known }; }) };
    }
    /* B: a holdings table. Market value = quantity x price; find the number that is the product of two others. */
    var out = list.map(function (r) {
      var n = r.nums.filter(function (x) { return x > 0; }), val = null, how = null, px = prices[r.ticker], qty = null, price = null, used = [];
      var vnd = function (x) { return x < 1000 ? x * 1000 : x; };                 // broker screens show prices in thousands
      /* every (quantity, price, value) triple on the row: a broker table often has two, cost value and market value */
      var tri = [];
      for (var i = 0; i < n.length; i++) for (var j = 0; j < n.length; j++) {
        if (i === j || n[i] < 1 || n[i] !== Math.round(n[i]) || n[j] === n[i] && n[j] < 1000) continue;   // n[i] = quantity (whole shares)
        for (var k = 0; k < n.length; k++) {
          if (k === i || k === j || n[k] <= n[j] || n[k] <= n[i]) continue;
          var p1 = n[i] * n[j], p2 = p1 * 1000, p3 = p1 / 1000;
          if (Math.abs(n[k] / p1 - 1) < 0.02 || Math.abs(n[k] / p2 - 1) < 0.02 || Math.abs(n[k] / p3 - 1) < 0.02) { if (!tri.some(function (x) { return x.j === j || n[x.j] === n[j]; })) tri.push({ i: i, j: j, k: k, gap: px ? Math.abs(vnd(n[j]) / px - 1) : 0 }); break; }
        }
      }
      var costTri = null;
      if (tri.length) {
        var mkt = px ? tri.slice().sort(function (a, b) { return a.gap - b.gap; })[0] : tri.slice().sort(function (a, b) { return b.k - a.k; })[0];   // nearest the last close; else the right-most
        if (!px || mkt.gap < 0.25) { qty = n[mkt.i]; price = n[mkt.j]; val = qty * vnd(price); how = 'product'; used = [mkt.i, mkt.j, mkt.k];
          costTri = tri.filter(function (x) { return x !== mkt && x.i === mkt.i || x !== mkt && n[x.i] === n[mkt.i]; })[0] || null; }
      }
      if (val == null && px) {                                                   // quantity x known close
        var qi = -1; n.forEach(function (x, ix) { if (qi < 0 && x === Math.round(x) && x >= 10 && Math.abs(x / px - 1) > 0.2 && Math.abs(x * 1000 / px - 1) > 0.2) qi = ix; });
        if (qi >= 0) { qty = n[qi]; val = qty * px; how = 'quantity'; used = [qi];
          n.forEach(function (x, ix) { if (price == null && ix !== qi && Math.abs(vnd(x) / px - 1) < 0.03) { price = x; used.push(ix); } }); if (price == null) price = px; }
      }
      if (val == null && n.length) { val = Math.max.apply(null, n); how = 'largest'; }
      /* cost price: another price-like number on the row, confirmed by the profit/loss % when the screen shows one */
      var cost = null, derived = false;
      if (price != null) {
        var cand = []; n.forEach(function (x, ix) { if (used.indexOf(ix) < 0 && x / price > 0.25 && x / price < 4) cand.push(x); });
        var pl = r.pcts.filter(function (x) { return Math.abs(x) < 95; });
        if (costTri) cost = n[costTri.j];                                         // the row states the cost value outright
        if (cost == null) pl.forEach(function (q) {                               // a printed cost confirmed by a profit/loss % on the row
          var implied = price / (1 + q / 100); cand.forEach(function (x) { if (cost == null && Math.abs(x / implied - 1) < 0.002) cost = x; }); });
        if (cost == null && pl.length === 1) {                                    // price and P/L % pin the cost down; a printed cost that disagrees was misread
          var implied = price / (1 + pl[0] / 100), near = cand.filter(function (x) { return Math.abs(x / implied - 1) < 0.05; })[0];
          if (near != null || !cand.length) { cost = implied; derived = true; }
        }
        if (cost == null && cand.length === 1 && !pl.length) cost = cand[0];
      }
      return { ticker: r.ticker, value: val, how: how, known: r.known, qty: qty, price: price == null ? null : vnd(price), cost: cost == null ? null : derived ? Math.round(vnd(cost) / 10) * 10 : Math.round(vnd(cost)) };
    });
    /* values must share one unit: if some came from quantity x close (VND) and others are in thousands or millions, rescale by median ratio is not safe; flag instead */
    var tot = out.reduce(function (s, r) { return s + (r.value || 0); }, 0);
    out.forEach(function (r) { r.weight = tot > 0 && r.value ? r.value / tot * 100 : null; });
    var mixed = out.some(function (r) { return r.how === 'quantity'; }) && out.some(function (r) { return r.how === 'product' || r.how === 'largest'; });
    var allVnd = out.every(function (r) { return r.how === 'product' || r.how === 'quantity'; });
    return { mode: 'values', rows: out, total: allVnd ? tot : null, unsure: fixed || mixed || out.some(function (r) { return r.how === 'largest'; }) };
  }

  /* ---- browser only: recognise text in an image, on the device ---- */
  var worker = null;
  function loadScript(src) { return new Promise(function (ok, bad) { var s = document.createElement('script'); s.src = src; s.onload = ok; s.onerror = function () { bad(new Error('load')); }; document.head.appendChild(s); }); }
  function prepare(file) {
    return new Promise(function (ok, bad) {
      var img = new Image(), url = URL.createObjectURL(file);
      img.onload = function () {
        var sc = Math.min(3, Math.max(1, 3400 / img.width)), c = document.createElement('canvas');
        c.width = Math.round(img.width * sc); c.height = Math.round(img.height * sc);
        if (c.width * c.height > 16e6) { var k = Math.sqrt(16e6 / (c.width * c.height)); c.width = Math.round(c.width * k); c.height = Math.round(c.height * k); }
        var g = c.getContext('2d'); g.imageSmoothingQuality = 'high'; g.drawImage(img, 0, 0, c.width, c.height); URL.revokeObjectURL(url);
        var d = g.getImageData(0, 0, c.width, c.height), a = d.data, sum = 0, i, y;
        for (i = 0; i < a.length; i += 4) { y = 0.299 * a[i] + 0.587 * a[i + 1] + 0.114 * a[i + 2]; a[i] = a[i + 1] = a[i + 2] = y; sum += y; }
        if (sum / (a.length / 4) < 120) for (i = 0; i < a.length; i += 4) a[i] = a[i + 1] = a[i + 2] = 255 - a[i];   // dark theme: make it dark text on light
        g.putImageData(d, 0, 0); ok(c);
      };
      img.onerror = function () { URL.revokeObjectURL(url); bad(new Error('image')); };
      img.src = url;
    });
  }
  function readImage(file, base, onProgress) {
    var T = base + 'vendor/tesseract/';
    return prepare(file).then(function (canvas) {
      var ready = root.Tesseract ? Promise.resolve() : loadScript(T + 'tesseract.min.js');
      return ready.then(function () {
        if (worker) return worker;
        var abs = new URL(T, document.baseURI).href;
        return root.Tesseract.createWorker('eng', 1, { workerPath: abs + 'worker.min.js', corePath: abs, langPath: abs, gzip: true,
          logger: function (m) { if (onProgress && m.status === 'recognizing text') onProgress(m.progress); } }).then(function (w) { worker = w; return w.setParameters({ preserve_interword_spaces: '1', tessedit_pageseg_mode: '6' }).then(function () { return w; }); });
      }).then(function (w) { return w.recognize(canvas); }).then(function (r) { return r.data.text; });
    });
  }

  var API = { parse: parse, toNum: toNum, readImage: readImage };
  root.PM_INTAKE = API;
  if (typeof module !== 'undefined' && module.exports) module.exports = API;
})(typeof window !== 'undefined' ? window : globalThis);
