/* Portfolio desk engine: pure functions, no DOM, no text. Returns numbers and codes; app.js turns them into words.
   Runs in the browser (window.PM_ENGINE) and in Node (module.exports) so the rules can be tested. */
(function (root) {
  'use strict';

  /* House rules. Each is a convention of this tool, shown on the page under "Method". */
  var RULES = {
    pByConv: [45, 50, 55, 60, 65],          // default probability of being right, by conviction 1..5
    riskShare: [0.04, 0.06, 0.08, 0.11, 0.14], // share of the drawdown budget one position may lose, by conviction
    nameCap: [4, 7, 10, 15, 20],            // ceiling on one name, % of portfolio, by conviction
    kellyFrac: 0.25,                        // fraction of the Kelly stake used as a ceiling
    sectorCap: 30, clusterCap: 50,          // % of portfolio
    bands: { easing: [80, 100], neutral: [65, 90], tight: [50, 75] }, // invested %, by liquidity regime
    adtvShare: 0.15, exitDays: 5,           // can sell 15% of daily turnover; flag if exit takes > 5 sessions
    staleDays: 90, priceStaleDays: 14,
    pairCorr: 0.7
  };

  var M = null, R = null, IDX = {};
  function init(market, research) {
    M = market; R = research; IDX = {};
    M.order.forEach(function (t, i) { IDX[t] = i; });
  }

  function num(x) { var n = typeof x === 'number' ? x : parseFloat(x); return isFinite(n) ? n : null; }
  function median(a) { if (!a.length) return null; var s = a.slice().sort(function (x, y) { return x - y; }); var m = s.length >> 1; return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2; }
  function round(x, step) { return Math.round(x / step) * step; }
  function daysBetween(a, b) { return Math.round((new Date(b) - new Date(a)) / 864e5); }

  function sectorOf(p) { var m = M.t[p.ticker]; return m ? m.sec : (p.sector && R.sectors[p.sector] ? p.sector : 'other'); }
  function sectorVol(sec) {
    var v = []; for (var t in M.t) if (M.t[t].sec === sec) v.push(M.t[t].vol);
    if (!v.length) for (var u in M.t) v.push(M.t[u].vol);
    return median(v);
  }
  function corr(a, b) {
    if (a.ticker === b.ticker) return 1;
    var i = IDX[a.ticker], j = IDX[b.ticker];
    if (i != null && j != null) { var hi = Math.max(i, j), lo = Math.min(i, j); var c = M.tri[hi * (hi - 1) / 2 + lo]; if (c != null) return c / 100; }
    var k = [a.sector, b.sector].sort().join('|');
    return M.seccorr[k] != null ? M.seccorr[k] : M.avgcorr;
  }

  function regime(settings, today) {
    var liq = R.regime.liquidity.reduce(function (s, x) { return s + x.dir; }, 0);
    var trend = M.index.d200 == null ? 0 : (M.index.d200 < 0 ? -1 : 1);
    var score = liq + trend;
    var auto = score <= -3 ? 'tight' : score >= 3 ? 'easing' : 'neutral';
    var growth = R.regime.growth.reduce(function (s, x) { return s + x.dir; }, 0);
    var use = settings.regime && settings.regime !== 'auto' ? settings.regime : auto;
    return { auto: auto, use: use, overridden: use !== auto, score: score, n: R.regime.liquidity.length + 1, growth: growth > 0 ? 'strong' : growth < 0 ? 'weak' : 'mixed',
      band: RULES.bands[use], indexD200: M.index.d200, priceAge: daysBetween(M.asof, today), researchAge: daysBetween(R.asof, today) };
  }

  /* One position: the arithmetic of the investor's own numbers, plus what prices say. */
  function metrics(p, settings, reg) {
    var mk = M.t[p.ticker] || null, sec = sectorOf(p);
    var conv = Math.min(5, Math.max(1, num(p.conviction) || 3));
    var prob = num(p.p); var probDefault = prob == null; if (probDefault) prob = RULES.pByConv[conv - 1];
    var U = num(p.up), D = num(p.down), w = Math.max(0, num(p.weight) || 0);
    var maxDD = num(settings.maxDD) || 15;
    var o = { id: p.id, ticker: p.ticker, sector: sec, covered: !!mk, conv: conv, prob: prob, probDefault: probDefault, up: U, down: D, weight: w, status: p.status === 'idea' ? 'idea' : 'hold',
      vol: mk ? mk.vol : sectorVol(sec), volEst: !mk, beta: mk && mk.beta != null ? mk.beta : 1, mk: mk, cap: RULES.nameCap[conv - 1] };
    o.monthSigma = o.vol / Math.sqrt(12);
    o.complete = U != null && D != null && U > 0 && D > 0;
    if (o.complete) {
      var u = U / 100, d = D / 100, q = 1 - prob / 100;
      o.breakeven = D / (U + D) * 100;
      o.ev = prob / 100 * U - q * D;
      o.payoff = U / D;
      o.kelly = (prob / 100 * u - q * d) / (u * d) * 100;
      o.kellyCap = Math.max(0, o.kelly * RULES.kellyFrac);
      o.riskPct = maxDD * RULES.riskShare[conv - 1];
      o.noise = D < o.monthSigma;
      /* a stop tighter than one month of normal movement is not a real limit on the loss: size on the wider of the two */
      o.downEff = Math.max(D, o.monthSigma);
      o.riskW = o.riskPct / o.downEff * 100;
      var cands = [['kelly', o.kellyCap], ['risk', o.riskW], ['cap', o.cap]];
      cands.sort(function (a, b) { return a[1] - b[1]; });
      o.raw = o.ev <= 0 ? 0 : cands[0][1];
      o.binding = o.ev <= 0 ? 'negEV' : cands[0][0];
      o.tilt = reg.use === 'tight' ? R.sectors[sec].tilt : 1;
      o.raw *= o.tilt;
      o.ddSmall = !!mk && D < Math.abs(mk.dd) / 2;
      /* probability at which the suggested size halves: shows how fragile the number is */
      o.probMinus10 = Math.max(0, ((prob - 10) / 100 * U - (1 - (prob - 10) / 100) * D));
    }
    var d200 = mk ? (mk.d200 != null ? mk.d200 : mk.d50) : null, rs = mk ? mk.rs3m : null;
    o.trend = mk == null || d200 == null ? 'unknown' : (d200 > 0 && (rs == null || rs > 0)) ? 'confirm' : (d200 < -5 && (rs == null || rs < 0)) ? 'against' : 'mixed';
    o.hasThesis = !!(p.thesis && p.thesis.trim()); o.hasKill = !!(p.kill && p.kill.trim()); o.hasCatalyst = !!(p.catalyst && p.catalyst.trim());
    o.edge = p.edge || 'none'; o.horizon = num(p.horizon);
    return o;
  }

  /* Book-level risk for a set of {ticker, sector, vol, weight, down, beta}. Weights in % of portfolio. */
  function book(items) {
    var xs = items.filter(function (i) { return i.weight > 0; });
    var out = { n: xs.length, invested: 0, stress: 0, beta: 0, sectors: {}, clusters: {}, top: null, share: {}, pairs: [] };
    if (!xs.length) { out.vol = 0; out.neff = 0; out.badMonth = 0; out.avgCorr = null; return out; }
    var v = 0, sx = 0, cw = 0, cs = 0, rc = [];
    xs.forEach(function (a, i) {
      out.invested += a.weight; out.beta += a.weight / 100 * a.beta;
      if (a.down) out.stress += a.weight * (a.downEff || a.down) / 100;
      out.sectors[a.sector] = (out.sectors[a.sector] || 0) + a.weight;
      var cl = R.sectors[a.sector].cluster; out.clusters[cl] = (out.clusters[cl] || 0) + a.weight;
      if (!out.top || a.weight > out.top.weight) out.top = a;
      var xa = a.weight / 100 * a.vol, acc = 0; sx += xa;
      xs.forEach(function (b, j) {
        var c = corr(a, b), xb = b.weight / 100 * b.vol; acc += xa * xb * c;
        if (j < i) { cw += a.weight * b.weight; cs += a.weight * b.weight * c; if (c >= RULES.pairCorr) out.pairs.push({ a: a.ticker, b: b.ticker, c: c }); }
      });
      rc.push(acc); v += acc;
    });
    out.vol = Math.sqrt(v);
    out.neff = v > 0 ? sx * sx / v : xs.length;
    out.badMonth = 1.65 * out.vol / Math.sqrt(12);
    out.avgCorr = cw > 0 ? cs / cw : null;
    xs.forEach(function (a, i) { out.share[a.id] = v > 0 ? rc[i] / v * 100 : 0; });
    return out;
  }

  /* Suggested weights: each position's own ceiling, then the sector, cluster and total ceilings. */
  function allocate(ms, reg) {
    var s = {}, why = {};
    ms.forEach(function (m) { s[m.id] = m.complete ? m.raw : null; why[m.id] = m.complete ? [m.binding] : ['incomplete']; if (m.complete && m.tilt < 1 && m.raw > 0) why[m.id].push('regime'); });
    function scale(group, cap, tag, keyOf) {
      var tot = {};
      ms.forEach(function (m) { if (s[m.id]) { var k = keyOf(m); tot[k] = (tot[k] || 0) + s[m.id]; } });
      ms.forEach(function (m) { var k = keyOf(m); if (s[m.id] && tot[k] > cap) { s[m.id] *= cap / tot[k]; if (why[m.id].indexOf(tag) < 0) why[m.id].push(tag); } });
    }
    scale(null, RULES.sectorCap, 'sector', function (m) { return m.sector; });
    scale(null, RULES.clusterCap, 'cluster', function (m) { return 'c:' + R.sectors[m.sector].cluster; });
    scale(null, reg.band[1], 'total', function () { return 'all'; });
    ms.forEach(function (m) {
      if (s[m.id] == null) { m.suggest = null; m.action = 'needNumbers'; m.why = why[m.id]; return; }
      var x = round(s[m.id], 0.5); m.suggest = x; m.why = why[m.id];
      var w = m.weight;
      if (m.status === 'idea') m.action = x <= 0 ? 'pass' : 'start';
      else if (x <= 0) m.action = w > 0 ? 'exit' : 'pass';
      else if (w - x >= 1 && w > x * 1.25) m.action = 'trim';
      else if (x - w >= 1 && w < x * 0.75) m.action = 'add';
      else m.action = 'hold';
      /* tranches for buying: price confirmation and liquidity decide how fast */
      if (m.action === 'start' || m.action === 'add') m.tranches = (m.trend === 'confirm' && reg.use !== 'tight') ? 2 : 3;
      m.delta = x - w;
    });
    return ms;
  }

  /* Match the investor's stated likes and dislikes against the research. */
  function evidence(p, sec) {
    var likes = p.likes || [], dislikes = p.dislikes || [];
    var out = { agree: [], challenge: [], blindRisk: [], blindSupport: [], forN: 0, againstN: 0, tickerLevel: false, sectorLevel: false, srcs: {} };
    R.claims.forEach(function (c) {
      var lvl = -1;
      if (c.scope.charAt(0) === 't') { if (c.scope.slice(2).split(',').indexOf(p.ticker) >= 0) lvl = 2; }
      else if (c.scope === 's:' + sec) lvl = 1;
      else if (c.scope === 's:*') lvl = 0;
      if (lvl < 0) return;
      var e = { text: c.text, src: c.src, driver: c.driver, dir: c.dir, lvl: lvl };
      if (lvl === 2) out.tickerLevel = true; if (lvl === 1) out.sectorLevel = true;
      if (lvl > 0) { if (c.dir > 0) out.forN++; else out.againstN++; }
      out.srcs[c.src] = 1;
      var liked = likes.indexOf(c.driver) >= 0, disliked = dislikes.indexOf(c.driver) >= 0;
      if (liked) (c.dir > 0 ? out.agree : out.challenge).push(e);
      else if (disliked) (c.dir < 0 ? out.agree : out.challenge).push(e);
      else (c.dir < 0 ? out.blindRisk : out.blindSupport).push(e);
    });
    ['agree', 'challenge', 'blindRisk', 'blindSupport'].forEach(function (k) { out[k].sort(function (a, b) { return b.lvl - a.lvl; }); });
    return out;
  }

  function questions(m, ev, reg) {
    var q = [];
    if (!m.hasThesis) q.push('noThesis');
    if (m.edge === 'none') q.push('noEdge');
    if (!m.complete) q.push('noNumbers');
    else {
      if (m.ev <= 0) q.push('negEV');
      else if (m.prob - m.breakeven < 7) q.push('thinEdge');
      if (m.noise) q.push('noise');
      if (m.ddSmall) q.push('ddSmall');
      if (!m.probDefault && m.prob >= 65 && ev.againstN > ev.forN) q.push('probVsResearch');
    }
    if (!m.hasKill) q.push('noKill');
    if (!m.hasCatalyst) q.push('noCatalyst');
    if (R.consensus && R.consensus[m.ticker] >= 2) q.push('consensus');
    if (m.trend === 'against') q.push('priceDisagrees');
    if (ev.challenge.length) q.push('challenge');
    if (m.conv >= 4) q.push('hold5');
    q.push('preMortem');
    return q;
  }

  function analyse(state, today) {
    today = today || new Date().toISOString().slice(0, 10);
    var settings = state.settings || {}, reg = regime(settings, today);
    var maxDD = num(settings.maxDD) || 15, capital = num(settings.capital);
    var ms = (state.positions || []).filter(function (p) { return p.ticker; }).map(function (p) { return metrics(p, settings, reg); });
    allocate(ms, reg);
    var src = {}; (state.positions || []).forEach(function (p) { src[p.id] = p; });
    ms.forEach(function (m) {
      m.ev_ = evidence(src[m.id], m.sector);
      m.questions = questions(m, m.ev_, reg);
      var rep = R.sectors[m.sector].src; m.reportAge = rep ? daysBetween(R.reports[rep].date, today) : null; m.report = rep || null;
      m.stale = m.reportAge != null && m.reportAge > RULES.staleDays;
      if (capital && m.mk) {
        var tgt = Math.max(m.weight, m.suggest || 0) / 100 * capital;      // bn VND
        m.exitDays = tgt / (m.mk.adtv * RULES.adtvShare);
      }
    });
    var now = book(ms.filter(function (m) { return m.status === 'hold'; }));
    var after = book(ms.map(function (m) { var c = {}; for (var k in m) c[k] = m[k]; c.weight = m.suggest == null ? (m.status === 'hold' ? m.weight : 0) : m.suggest; return c; }));
    ms.forEach(function (m) {
      var sw = 0, sc = 0;
      ms.forEach(function (o) { if (o.id !== m.id && o.status === 'hold' && o.weight > 0) { sw += o.weight; sc += o.weight * corr(m, o); } });
      m.corrOthers = sw > 0 ? sc / sw : null;
    });
    ms.forEach(function (m) { m.riskShare = now.share[m.id] != null ? now.share[m.id] : null; m.capShare = now.invested > 0 && m.status === 'hold' ? m.weight / now.invested * 100 : null; });

    var f = [];
    function add(code, sev, lens, data) { f.push({ code: code, sev: sev, lens: lens, data: data || {} }); }
    var held = ms.filter(function (m) { return m.status === 'hold' && m.weight > 0; });
    if (now.invested > 100.5) add('leverage', 3, 'dalio', { v: now.invested });
    if (held.length) {
      if (now.invested > reg.band[1] + 0.5 && now.invested <= 100.5) add('overInvested', reg.use === 'tight' ? 3 : 2, 'druck', { v: now.invested, hi: reg.band[1], regime: reg.use });
      else if (now.invested < reg.band[0] - 0.5) add('underInvested', 1, 'druck', { v: now.invested, lo: reg.band[0], regime: reg.use });
      if (now.stress > maxDD + 0.05) add('stress', 3, 'dalio', { v: now.stress, max: maxDD });
      if (held.length >= 3 && now.neff < Math.max(2, held.length * 0.5)) add('fewBets', 2, 'dalio', { n: held.length, neff: now.neff, corr: now.avgCorr });
      for (var s in now.sectors) if (now.sectors[s] > RULES.sectorCap + 0.5) add('sector', 2, 'dalio', { sector: s, v: now.sectors[s], cap: RULES.sectorCap });
      for (var cl in now.clusters) if (cl !== 'other' && now.clusters[cl] > RULES.clusterCap + 0.5) add('cluster', reg.use === 'tight' && cl === 'rates' ? 3 : 2, 'dalio', { cluster: cl, v: now.clusters[cl], cap: RULES.clusterCap });
      held.forEach(function (m) {
        if (m.weight > m.cap + 0.5) add('overCap', m.weight > 25 ? 3 : 2, 'buffett', { t: m.ticker, v: m.weight, cap: m.cap, conv: m.conv });
        if (m.complete && m.ev <= 0) add('negEV', 3, 'druck', { t: m.ticker, ev: m.ev, prob: m.prob, be: m.breakeven });
        if (m.riskShare != null && m.riskShare - m.capShare > 8) add('riskSkew', 1, 'dalio', { t: m.ticker, risk: m.riskShare, cap: m.capShare });
        if (m.exitDays != null && m.exitDays > RULES.exitDays) add('illiquid', 2, 'druck', { t: m.ticker, days: m.exitDays });
      });
      var byW = held.slice().sort(function (a, b) { return b.weight - a.weight; }), big = byW[0];
      var better = held.filter(function (m) { return m.conv - big.conv >= 2 && m.weight < big.weight * 0.6; }).sort(function (a, b) { return b.conv - a.conv; })[0];
      if (better) add('convMismatch', 2, 'druck', { big: big.ticker, bigConv: big.conv, bigW: big.weight, small: better.ticker, smallConv: better.conv, smallW: better.weight });
      now.pairs.forEach(function (pr) { add('pair', 1, 'dalio', pr); });
      var against = held.filter(function (m) { return m.trend === 'against'; });
      if (against.length && reg.use === 'tight') add('againstTrend', 2, 'druck', { list: against.map(function (m) { return m.ticker; }) });
      var noKill = held.filter(function (m) { return !m.hasKill; });
      if (noKill.length) add('noKill', 2, 'buffett', { list: noKill.map(function (m) { return m.ticker; }) });
      var noNum = held.filter(function (m) { return !m.complete; });
      if (noNum.length) add('noNumbers', 2, 'druck', { list: noNum.map(function (m) { return m.ticker; }) });
      var noEdge = held.filter(function (m) { return m.edge === 'none'; });
      if (noEdge.length) add('noEdge', 1, 'dalio', { list: noEdge.map(function (m) { return m.ticker; }) });
    }
    var stale = ms.filter(function (m) { return m.stale; });
    if (stale.length) add('stale', 1, 'method', { list: stale.map(function (m) { return m.ticker; }), days: Math.max.apply(null, stale.map(function (m) { return m.reportAge; })) });
    var unc = ms.filter(function (m) { return !m.ev_.tickerLevel && !m.ev_.sectorLevel; });
    if (unc.length) add('uncovered', 1, 'method', { list: unc.map(function (m) { return m.ticker; }) });
    if (reg.priceAge > RULES.priceStaleDays) add('priceStale', 2, 'method', { days: reg.priceAge });
    f.sort(function (a, b) { return b.sev - a.sev; });

    return { regime: reg, positions: ms, now: now, after: after, findings: f, maxDD: maxDD, capital: capital, rules: RULES };
  }

  var API = { init: init, analyse: analyse, RULES: RULES, sectorOf: sectorOf };
  root.PM_ENGINE = API;
  if (typeof module !== 'undefined' && module.exports) module.exports = API;
})(typeof window !== 'undefined' ? window : globalThis);
