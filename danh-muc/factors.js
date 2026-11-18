/* Factor scores for the portfolio consultant. Pure functions (browser: window.PM_FACTORS, Node: module.exports).
   Each factor is the average of a few measures, each turned into a percentile rank (0-100) across the stocks tracked.
   50 is the middle of this universe. A score describes the stock today; it is not a forecast. */
(function (root) {
  'use strict';
  var KEYS = ['value', 'growth', 'quality', 'momentum', 'lowrisk', 'flow'];
  var S = null;   // { t: { TICKER: { value: .., ..., raw: {...} } }, sectors: { sec: {...} } }

  function last(a, k) { return a && a.length > (k || 0) ? a[a.length - 1 - (k || 0)] : null; }
  function yoy(a) { var x = last(a), y = last(a, 4); return x != null && y != null && y > 0 ? x / y - 1 : null; }
  function sum4(a, k) { var s = 0; for (var i = 0; i < 4; i++) { var v = last(a, (k || 0) + i); if (v == null) return null; s += v; } return s; }
  function median(v) { var s = v.filter(function (x) { return x != null; }).sort(function (a, b) { return a - b; }); if (!s.length) return null; var m = s.length >> 1; return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2; }

  function init(M, C, F) {
    var T = Object.keys(M.t), raw = {};
    T.forEach(function (t) {
      var m = M.t[t], c = C && C.t[t], f = F && F.t[t], r = {};
      var ttm = c ? sum4(c.np) : null, ttm0 = c ? sum4(c.np, 4) : null;
      /* value: what you pay for trailing earnings and for book. Losses rank last on earnings. */
      r.ey = m.pe > 0 && m.pe < 200 && !(ttm != null && ttm <= 0) && !(c && last(c.np) < 0) ? 1 / m.pe : (m.pe ? 0 : null);
      r.by = m.pb > 0 ? 1 / m.pb : null;
      /* growth: latest quarter and trailing year against a year earlier */
      r.gq = c ? yoy(c.np) : null; if (r.gq == null && c && last(c.np) != null && last(c.np, 4) != null) r.gq = last(c.np) > last(c.np, 4) ? 1 : -1;   // from or into a loss
      r.gt = ttm != null && ttm0 != null && ttm0 > 0 ? ttm / ttm0 - 1 : null;
      r.gr = c ? yoy(c.rev) : null;
      /* quality: return on equity, plus balance-sheet strength suited to the kind of company */
      r.roe = c ? last(c.roe) : null;
      if (c && c.type === 'Bank') { r.cov = last(c.cov); r.npl = last(c.npl) == null ? null : -last(c.npl); r.casa = last(c.casa); }
      else if (c && c.type === 'Company') { r.de = last(c.de) == null ? null : -last(c.de); var pbt = last(c.pbt); r.core = pbt > 0 ? -Math.min(2, ((c.fin || 0) + Math.max(0, c.oth || 0)) / pbt) : (pbt != null ? -2 : null); }
      else if (c && c.type === 'Securities') { r.mle = last(c.mle) == null ? null : -last(c.mle); }
      /* momentum */
      r.rs3 = m.rs3m; r.d200 = m.d200 != null ? m.d200 : m.d50; r.r6 = f ? f.r6m : null; r.r12 = f ? f.r12_1 : null;
      /* low risk */
      r.vol = -m.vol; r.beta = m.beta == null ? null : -m.beta; r.dd = m.dd;
      /* flow: who has been buying */
      r.fnet = f ? f.fnet : null; r.obi = f ? f.obi : null;
      raw[t] = r;
    });
    function rank(key) {
      var v = T.filter(function (t) { return raw[t][key] != null && isFinite(raw[t][key]); }).sort(function (a, b) { return raw[a][key] - raw[b][key]; }), out = {};
      v.forEach(function (t, i) {                              // ties share the average rank
        var j = i; while (j + 1 < v.length && raw[v[j + 1]][key] === raw[t][key]) j++;
        var k = i; while (k > 0 && raw[v[k - 1]][key] === raw[t][key]) k--;
        out[t] = v.length > 1 ? ((j + k) / 2) / (v.length - 1) * 100 : 50;
      });
      return out;
    }
    var parts = { value: ['ey', 'by'], growth: ['gq', 'gt', 'gr'], quality: ['roe', 'cov', 'npl', 'casa', 'de', 'core', 'mle'], momentum: ['rs3', 'd200', 'r6', 'r12'], lowrisk: ['vol', 'beta', 'dd'], flow: ['fnet', 'obi'] };
    var ranks = {}; Object.keys(parts).forEach(function (f) { parts[f].forEach(function (k) { ranks[k] = rank(k); }); });
    var out = {};
    T.forEach(function (t) {
      var o = { sec: M.t[t].sec, raw: raw[t] };
      KEYS.forEach(function (f) { var v = parts[f].map(function (k) { return ranks[k][t]; }).filter(function (x) { return x != null; }); o[f] = v.length ? Math.round(v.reduce(function (a, b) { return a + b; }, 0) / v.length) : null; });
      out[t] = o;
    });
    /* rank inside the sector, and sector medians */
    var secs = {};
    T.forEach(function (t) { (secs[out[t].sec] = secs[out[t].sec] || []).push(t); });
    var sectors = {};
    Object.keys(secs).forEach(function (s) {
      var mem = secs[s], row = { n: mem.length };
      KEYS.forEach(function (f) {
        row[f] = median(mem.map(function (t) { return out[t][f]; })); if (row[f] != null) row[f] = Math.round(row[f]);
        var srt = mem.filter(function (t) { return out[t][f] != null; }).sort(function (a, b) { return out[b][f] - out[a][f]; });
        srt.forEach(function (t, i) { (out[t].inSec = out[t].inSec || {})[f] = { r: i + 1, n: srt.length }; });
      });
      sectors[s] = row;
    });
    S = { t: out, sectors: sectors };
    return S;
  }

  /* one-line reading of a stock's shape; returns a code */
  function shape(t) {
    var s = S && S.t[t]; if (!s) return null;
    var v = s.value, g = s.growth, q = s.quality, m = s.momentum, f = s.flow;
    if (v == null || m == null) return null;
    if (v >= 65 && m <= 35 && (g == null || g <= 40)) return 'valueTrap';
    if (v >= 60 && q != null && q >= 65 && m <= 40) return 'qualityOutOfFavour';
    if (v >= 60 && q != null && q >= 65) return 'qualityCheap';
    if (v <= 30 && m >= 70) return 'expensiveMomentum';
    if (g != null && g >= 70 && v <= 35) return 'growthAtPrice';
    if (g != null && g >= 65 && m <= 35) return 'growthIgnored';
    if (m <= 20 && f != null && f <= 30) return 'soldOff';
    if (m >= 70 && f != null && f >= 60) return 'inFavour';
    if (q != null && q <= 30 && v <= 40) return 'weakAndDear';
    return 'mixed';
  }

  /* weighted exposure of a set of {ticker, weight} */
  function exposure(items) {
    var out = {}, cover = 0, tot = 0;
    items.forEach(function (i) { tot += i.weight; if (S.t[i.ticker]) cover += i.weight; });
    KEYS.forEach(function (f) { var w = 0, a = 0; items.forEach(function (i) { var s = S.t[i.ticker]; if (s && s[f] != null) { w += i.weight; a += i.weight * s[f]; } }); out[f] = w > 0 ? Math.round(a / w) : null; });
    return { scores: out, cover: tot > 0 ? cover / tot : 0 };
  }

  var API = { init: init, shape: shape, exposure: exposure, KEYS: KEYS, get: function (t) { return S && S.t[t] || null; }, sectors: function () { return S ? S.sectors : {}; }, all: function () { return S ? S.t : {}; } };
  root.PM_FACTORS = API;
  if (typeof module !== 'undefined' && module.exports) module.exports = API;
})(typeof window !== 'undefined' ? window : globalThis);
