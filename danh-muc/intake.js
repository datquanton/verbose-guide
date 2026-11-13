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
    var rows = [], cur = null;
    String(text || '').replace(/[,;]\s+(?=[A-Za-z]{3}\b)/g, '\n').split(/\r?\n/).forEach(function (line) {
      var toks = line.replace(/[|\[\]{}()]/g, ' ').split(/\s+/).filter(Boolean), tk = null, ti = -1;
      for (var i = 0; i < toks.length && i < 3; i++) {         // a ticker sits at the start of its row
        var w = toks[i].replace(/[^A-Za-z0-9]/g, '').toUpperCase();
        if (/^[A-Z][A-Z0-9]{2}$/.test(w) && /[A-Z]{2}/.test(w) && (known[w] || (STOP.indexOf(w) < 0 && toks[i] === toks[i].toUpperCase()))) { tk = w; ti = i; break; }
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
      var n = r.nums.filter(function (x) { return x > 0; }), val = null, how = null, px = prices[r.ticker];
      for (var i = 0; i < n.length && val == null; i++) for (var j = 0; j < n.length && val == null; j++) {
        if (i === j || n[i] < 1 || n[i] !== Math.round(n[i])) continue;           // n[i] = quantity (whole shares)
        if (px && !(Math.abs(n[j] / px - 1) < 0.2 || Math.abs(n[j] * 1000 / px - 1) < 0.2)) continue;  // n[j] = a price near the last close
        for (var k = 0; k < n.length; k++) {
          if (k === i || k === j) continue;
          var p1 = n[i] * n[j], p2 = p1 * 1000, p3 = p1 / 1000;
          if (Math.abs(n[k] / p1 - 1) < 0.02 || Math.abs(n[k] / p2 - 1) < 0.02 || Math.abs(n[k] / p3 - 1) < 0.02) { val = n[k]; how = 'product'; break; }
        }
      }
      if (val == null && px) {                                                   // quantity x known close
        var q = n.filter(function (x) { return x === Math.round(x) && x >= 10 && Math.abs(x / px - 1) > 0.2 && Math.abs(x * 1000 / px - 1) > 0.2; })[0];
        if (q) { val = q * px; how = 'quantity'; }
      }
      if (val == null && n.length) { val = Math.max.apply(null, n); how = 'largest'; }
      return { ticker: r.ticker, value: val, how: how, known: r.known };
    });
    /* values must share one unit: if some came from quantity x close (VND) and others are in thousands or millions, rescale by median ratio is not safe; flag instead */
    var tot = out.reduce(function (s, r) { return s + (r.value || 0); }, 0);
    out.forEach(function (r) { r.weight = tot > 0 && r.value ? r.value / tot * 100 : null; });
    var mixed = out.some(function (r) { return r.how === 'quantity'; }) && out.some(function (r) { return r.how === 'product' || r.how === 'largest'; });
    return { mode: 'values', rows: out, unsure: mixed || out.some(function (r) { return r.how === 'largest'; }) };
  }

  /* ---- browser only: recognise text in an image, on the device ---- */
  var worker = null;
  function loadScript(src) { return new Promise(function (ok, bad) { var s = document.createElement('script'); s.src = src; s.onload = ok; s.onerror = function () { bad(new Error('load')); }; document.head.appendChild(s); }); }
  function prepare(file) {
    return new Promise(function (ok, bad) {
      var img = new Image(), url = URL.createObjectURL(file);
      img.onload = function () {
        var sc = Math.min(3, Math.max(1, 1800 / img.width)), c = document.createElement('canvas');
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
