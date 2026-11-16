/* Company facts: turns the numbers in company.js into a fact card and data-derived evidence for one ticker.
   Pure functions (browser: window.PM_FACTS, Node: module.exports). Every sentence states a reported figure; none is a forecast.
   Text is [Vietnamese, English]. */
(function (root) {
  'use strict';
  var C = null, M = null;
  function init(company, market) { C = company; M = market; }

  function last(a, k) { return a && a.length > (k || 0) ? a[a.length - 1 - (k || 0)] : null; }
  function f(x, d, vi) { if (x == null || !isFinite(x)) return '–'; var s = Math.abs(x).toFixed(d); if (vi) s = s.replace('.', ','); return (x < 0 ? '−' : '') + s; }
  function money(x, vi) {            // VND bn -> "8.217 tỷ" / "26,9 nghìn tỷ"
    if (x == null) return '–'; var a = Math.abs(x);
    if (a >= 10000) return f(x / 1000, 1, vi) + (vi ? ' nghìn tỷ' : 'tn');
    var s = Math.round(a).toLocaleString(vi ? 'vi-VN' : 'en-US'); return (x < 0 ? '−' : '') + (vi ? s + ' tỷ' : 'VND' + s + 'bn');
  }
  function pct(x, vi, d) { return x == null ? '–' : (x > 0 ? '+' : '') + f(x * 100, d == null ? 0 : d, vi) + '%'; }
  function p0(x, vi, d) { return x == null ? '–' : f(x * 100, d == null ? 1 : d, vi) + '%'; }
  function both(fn) { return [fn(true), fn(false)]; }
  function yoy(a, k) { var x = last(a, k || 0), y = last(a, (k || 0) + 4); return x != null && y != null && y > 0 ? x / y - 1 : null; }
  function sum4(a, k) { var s = 0; for (var i = 0; i < 4; i++) { var v = last(a, (k || 0) + i); if (v == null) return null; s += v; } return s; }
  function rng(a) { var v = (a || []).filter(function (x) { return x != null && x > 0; }); if (v.length < 6) return null; var s = v.slice().sort(function (x, y) { return x - y; }); return { lo: s[0], hi: s[s.length - 1], med: s[s.length >> 1], n: v.length, now: last(a), pos: s.indexOf(last(a)) / (s.length - 1) }; }

  function rank(t, key, higherBetter) {
    var sec = M.t[t] && M.t[t].sec; if (!sec) return null;
    var rows = []; for (var k in M.t) if (M.t[k].sec === sec && C.t[k]) { var v = key(C.t[k], k); if (v != null) rows.push([k, v]); }
    if (rows.length < 4) return null;
    rows.sort(function (a, b) { return higherBetter ? b[1] - a[1] : a[1] - b[1]; });
    for (var i = 0; i < rows.length; i++) if (rows[i][0] === t) return { r: i + 1, n: rows.length };
    return null;
  }

  /* numbers the card and the signals share */
  function metrics(t) {
    var c = C && C.t[t]; if (!c) return null;
    var m = { c: c, type: c.type, q: last(c.q), stale: !c.last };
    m.np = last(c.np); m.npYoY = yoy(c.np); m.npPrev = last(c.np, 4); m.rev = last(c.rev); m.revYoY = yoy(c.rev);
    m.ttm = sum4(c.np); m.ttm0 = sum4(c.np, 4); m.ttmYoY = m.ttm != null && m.ttm0 != null && m.ttm0 > 0 ? m.ttm / m.ttm0 - 1 : null;
    m.down = 0; for (var k = 0; k < 4; k++) { var g = yoy(c.np, k); if (g != null && g < 0) m.down++; else break; }
    m.roe = last(c.roe); m.roeRank = rank(t, function (x) { return last(x.roe); }, true);
    m.growRank = rank(t, function (x) { return yoy(x.np); }, true);
    m.pb = M.t[t] ? M.t[t].pb : last(c.pb); m.pe = M.t[t] ? M.t[t].pe : last(c.pe);
    m.pbRank = rank(t, function (x, k2) { return M.t[k2].pb; }, false);
    m.pbR = rng(c.pb); m.peR = rng(c.pe);
    if (c.type === 'Bank') {
      m.nim = last(c.nim); m.nim0 = last(c.nim, 4); m.npl = last(c.npl); m.npl0 = last(c.npl, 4); m.g2 = last(c.g2); m.g20 = last(c.g2, 4);
      m.cov = last(c.cov); m.cov0 = last(c.cov, 4); m.casa = last(c.casa); m.cof = last(c.cof); m.credit = last(c.credit); m.cir = last(c.cir);
      m.pbtYoY = yoy(c.pbt); m.prov = c.prov; m.prov0 = c.prov0;
    } else {
      m.gm = last(c.gm); m.gm0 = last(c.gm, 4); m.de = last(c.de); m.de0 = last(c.de, 4); m.cover = last(c.cover);
      m.pbt = last(c.pbt); m.nonCore = c.type === 'Company' && m.pbt > 0 ? ((c.fin || 0) + Math.max(0, c.oth || 0)) / m.pbt : null;
      m.doh = last(c.doh); m.doh0 = last(c.doh, 4); m.fcf = last(c.fcf); m.mle = last(c.mle); m.mlg = last(c.mlg);
    }
    return m;
  }

  /* data-derived evidence: { driver, dir, text: [vi, en] } */
  function signals(t) {
    var m = metrics(t), out = []; if (!m) return out;
    var c = m.c, q = m.q;
    function add(driver, dir, fn) { out.push({ driver: driver, dir: dir, text: both(fn), src: 'data', lvl: 2 }); }
    var name = t;
    if (m.np != null && m.np < 0) add('growth', -1, function (v) { return v ? name + ' lỗ ' + money(-m.np, v) + ' trong ' + q + (m.npPrev > 0 ? ' (cùng kỳ lãi ' + money(m.npPrev, v) + ')' : '') + '.' : name + ' lost ' + money(-m.np, v) + ' in ' + q + (m.npPrev > 0 ? ' (a profit of ' + money(m.npPrev, v) + ' a year earlier)' : '') + '.'; });
    else if (m.npYoY != null) {
      if (m.npYoY >= 0.2 && (m.ttmYoY == null || m.ttmYoY >= 0.1)) add('growth', 1, function (v) { return v ? 'Lợi nhuận ' + q + ' đạt ' + money(m.np, v) + ', ' + pct(m.npYoY, v) + ' so với cùng kỳ' + (m.ttmYoY != null ? '; 12 tháng gần nhất ' + money(m.ttm, v) + ', ' + pct(m.ttmYoY, v) : '') + '.' : q + ' profit was ' + money(m.np, v) + ', ' + pct(m.npYoY, v) + ' year on year' + (m.ttmYoY != null ? '; the last 12 months total ' + money(m.ttm, v) + ', ' + pct(m.ttmYoY, v) : '') + '.'; });
      else if (m.npYoY <= -0.1) add('growth', -1, function (v) { return v ? 'Lợi nhuận ' + q + ' là ' + money(m.np, v) + ', ' + pct(m.npYoY, v) + ' so với cùng kỳ' + (m.down >= 2 ? ', quý thứ ' + m.down + ' liên tiếp giảm' : '') + '.' : q + ' profit was ' + money(m.np, v) + ', ' + pct(m.npYoY, v) + ' year on year' + (m.down >= 2 ? ', the ' + ['', '', 'second', 'third', 'fourth'][m.down] + ' straight quarter of decline' : '') + '.'; });
    }
    if (m.npYoY != null && m.revYoY != null && m.npYoY > 0.15 && m.revYoY < 0.03 && m.type === 'Company') add('earnings', -1, function (v) { return v ? 'Lợi nhuận tăng ' + pct(m.npYoY, v) + ' trong khi doanh thu chỉ ' + pct(m.revYoY, v) + ': mức tăng không đến từ bán hàng.' : 'Profit rose ' + pct(m.npYoY, v) + ' while revenue was only ' + pct(m.revYoY, v) + ': the gain did not come from sales.'; });
    if (m.roe != null && m.type !== 'Bank') {
      var rk = m.roeRank;
      if (m.roe >= 0.18) add('quality', 1, function (v) { return (v ? 'ROE 12 tháng ' + p0(m.roe, v) : 'Trailing ROE of ' + p0(m.roe, v)) + (rk ? (v ? ', xếp ' + rk.r + '/' + rk.n + ' trong ngành' : ', ranked ' + rk.r + ' of ' + rk.n + ' in its sector') : '') + '.'; });
      else if (m.roe < 0.08) add('quality', -1, function (v) { return (v ? 'ROE 12 tháng chỉ ' + p0(m.roe, v) : 'Trailing ROE of only ' + p0(m.roe, v)) + (rk ? (v ? ', xếp ' + rk.r + '/' + rk.n + ' trong ngành' : ', ranked ' + rk.r + ' of ' + rk.n + ' in its sector') : '') + (v ? ': thấp hơn lãi suất tiền gửi dài hạn.' : ': below what a long-term deposit pays.'); });
    }
    if (m.type === 'Company') {
      if (m.gm != null && m.gm0 != null && Math.abs(m.gm - m.gm0) >= 0.02) add(m.gm > m.gm0 ? 'quality' : 'earnings', m.gm > m.gm0 ? 1 : -1, function (v) { return v ? 'Biên lợi nhuận gộp 12 tháng ' + (m.gm > m.gm0 ? 'tăng' : 'giảm') + ' từ ' + p0(m.gm0, v) + (m.gm > m.gm0 ? ' lên ' : ' xuống ') + p0(m.gm, v) + ' trong một năm.' : 'Trailing gross margin ' + (m.gm > m.gm0 ? 'rose' : 'fell') + ' from ' + p0(m.gm0, v) + ' to ' + p0(m.gm, v) + ' in a year.'; });
      if (m.nonCore != null && m.nonCore >= 1) add('earnings', -1, function (v) { var x = money((c.fin || 0) + Math.max(0, c.oth || 0), v); return v ? 'Thu nhập tài chính và thu nhập khác ' + q + ' (' + x + ') lớn hơn cả lợi nhuận trước thuế (' + money(m.pbt, v) + '): hoạt động kinh doanh chính đang lỗ.' : 'Financial and other income in ' + q + ' (' + x + ') exceeded pre-tax profit (' + money(m.pbt, v) + '): the core business lost money.'; });
      else if (m.nonCore != null && m.nonCore >= 0.4) add('earnings', -1, function (v) { return v ? p0(m.nonCore, v, 0) + ' lợi nhuận trước thuế ' + q + ' đến từ thu nhập tài chính và thu nhập khác (' + money((c.fin || 0) + Math.max(0, c.oth || 0), v) + ' trên ' + money(m.pbt, v) + '), không phải hoạt động kinh doanh chính.' : p0(m.nonCore, v, 0) + ' of ' + q + ' pre-tax profit came from financial and other income (' + money((c.fin || 0) + Math.max(0, c.oth || 0), v) + ' of ' + money(m.pbt, v) + '), not from the core business.'; });
      if (m.cover != null && m.cover < 2 && m.de > 0.3) add('quality', -1, function (v) { return v ? 'Lợi nhuận hoạt động chỉ gấp ' + f(m.cover, 1, v) + ' lần chi phí lãi vay; nợ vay bằng ' + f(m.de, 2, v) + ' lần vốn chủ.' : 'Operating profit covers interest only ' + f(m.cover, 1, v) + ' times; debt is ' + f(m.de, 2, v) + 'x equity.'; });
      else if (m.de != null && m.de0 != null && m.de - m.de0 >= 0.25) add('quality', -1, function (v) { return v ? 'Nợ vay trên vốn chủ tăng từ ' + f(m.de0, 2, v) + ' lên ' + f(m.de, 2, v) + ' lần trong một năm.' : 'Debt to equity rose from ' + f(m.de0, 2, v) + 'x to ' + f(m.de, 2, v) + 'x in a year.'; });
      else if (m.de != null && m.de < 0.15 && m.roe >= 0.12) add('quality', 1, function (v) { return v ? 'Gần như không vay nợ (nợ vay bằng ' + f(m.de, 2, v) + ' lần vốn chủ) với ROE ' + p0(m.roe, v) + '.' : 'Almost no debt (' + f(m.de, 2, v) + 'x equity) on an ROE of ' + p0(m.roe, v) + '.'; });
      if (m.doh != null && m.doh0 != null && m.doh0 > 20 && m.doh / m.doh0 >= 1.2) add('earnings', -1, function (v) { return v ? 'Số ngày tồn kho tăng từ ' + f(m.doh0, 0, v) + ' lên ' + f(m.doh, 0, v) + ' trong một năm.' : 'Inventory days rose from ' + f(m.doh0, 0, v) + ' to ' + f(m.doh, 0, v) + ' in a year.'; });
    }
    if (m.type === 'Securities') {
      if (m.mle != null && m.mle >= 1.5) add('margin', -1, function (v) { return v ? 'Dư nợ ký quỹ bằng ' + f(m.mle, 2, v) + ' lần vốn chủ: gần hết dư địa cho vay nếu không tăng vốn.' : 'Margin loans are ' + f(m.mle, 2, v) + 'x equity: little lending headroom without new capital.'; });
      if (m.mlg != null && m.mlg <= -0.1) add('margin', -1, function (v) { return v ? 'Dư nợ ký quỹ ' + pct(m.mlg, v) + ' so với cùng kỳ.' : 'Margin loans are ' + pct(m.mlg, v) + ' year on year.'; });
    }
    if (m.type === 'Bank') {
      if (m.nim != null && m.nim0 != null && Math.abs(m.nim - m.nim0) >= 0.001) add('nim', m.nim > m.nim0 ? 1 : -1, function (v) { return v ? 'NIM 12 tháng ' + (m.nim > m.nim0 ? 'tăng' : 'giảm') + ' từ ' + p0(m.nim0, v, 2) + (m.nim > m.nim0 ? ' lên ' : ' xuống ') + p0(m.nim, v, 2) + ' trong một năm.' : 'Trailing NIM ' + (m.nim > m.nim0 ? 'rose' : 'fell') + ' from ' + p0(m.nim0, v, 2) + ' to ' + p0(m.nim, v, 2) + ' in a year.'; });
      if (m.npl != null && m.npl0 != null && (m.npl - m.npl0 >= 0.0015 || (m.g2 != null && m.g20 != null && m.g2 - m.g20 >= 0.003))) add('asset', -1, function (v) { return v ? 'Nợ xấu ' + p0(m.npl0, v, 2) + ' → ' + p0(m.npl, v, 2) + ' và nợ nhóm 2 ' + p0(m.g20, v, 2) + ' → ' + p0(m.g2, v, 2) + ' trong một năm; tỷ lệ bao phủ ' + p0(m.cov, v, 0) + '.' : 'NPLs ' + p0(m.npl0, v, 2) + ' → ' + p0(m.npl, v, 2) + ' and group-2 loans ' + p0(m.g20, v, 2) + ' → ' + p0(m.g2, v, 2) + ' in a year; coverage ' + p0(m.cov, v, 0) + '.'; });
      else if (m.npl != null && m.npl < 0.012 && m.cov >= 1) add('asset', 1, function (v) { return v ? 'Nợ xấu ' + p0(m.npl, v, 2) + ' với tỷ lệ bao phủ ' + p0(m.cov, v, 0) + '.' : 'NPLs of ' + p0(m.npl, v, 2) + ' with coverage of ' + p0(m.cov, v, 0) + '.'; });
      if (m.cov != null && m.cov < 0.6) add('asset', -1, function (v) { return v ? 'Dự phòng chỉ bao phủ ' + p0(m.cov, v, 0) + ' nợ xấu' + (m.cov0 != null ? ' (một năm trước ' + p0(m.cov0, v, 0) + ')' : '') + '.' : 'Reserves cover only ' + p0(m.cov, v, 0) + ' of bad loans' + (m.cov0 != null ? ' (' + p0(m.cov0, v, 0) + ' a year earlier)' : '') + '.'; });
      if (m.prov != null && m.prov0 != null && m.prov0 > 0 && m.pbtYoY != null) {
        if (m.prov < m.prov0 * 0.85 && m.pbtYoY > 0 && m.cov != null && m.cov0 != null && m.cov < m.cov0) add('asset', -1, function (v) { return v ? 'LNTT ' + q + ' ' + pct(m.pbtYoY, v) + ' một phần nhờ trích lập giảm (' + money(m.prov0, v) + ' → ' + money(m.prov, v) + ') trong khi tỷ lệ bao phủ giảm từ ' + p0(m.cov0, v, 0) + ' xuống ' + p0(m.cov, v, 0) + '.' : q + ' pre-tax profit of ' + pct(m.pbtYoY, v) + ' was helped by lower provisions (' + money(m.prov0, v) + ' → ' + money(m.prov, v) + ') while coverage fell from ' + p0(m.cov0, v, 0) + ' to ' + p0(m.cov, v, 0) + '.'; });
        else if (m.prov > m.prov0 * 1.5) add('asset', -1, function (v) { return v ? 'Chi phí dự phòng ' + q + ' tăng từ ' + money(m.prov0, v) + ' lên ' + money(m.prov, v) + ' so với cùng kỳ.' : q + ' provision expense rose from ' + money(m.prov0, v) + ' to ' + money(m.prov, v) + ' year on year.'; });
      }
      if (m.casa != null && m.cof != null) {
        if (m.casa >= 0.25) add('funding', 1, function (v) { return v ? 'CASA ' + p0(m.casa, v) + ', chi phí vốn ' + p0(m.cof, v, 2) + '.' : 'CASA of ' + p0(m.casa, v) + ', cost of funds ' + p0(m.cof, v, 2) + '.'; });
        else if (m.casa < 0.1) add('funding', -1, function (v) { return v ? 'CASA chỉ ' + p0(m.casa, v) + ', chi phí vốn ' + p0(m.cof, v, 2) + '.' : 'CASA of only ' + p0(m.casa, v) + ', cost of funds ' + p0(m.cof, v, 2) + '.'; });
      }
      if (m.roe != null && m.roe >= 0.2) add('quality', 1, function (v) { return (v ? 'ROE 12 tháng ' : 'Trailing ROE of ') + p0(m.roe, v) + (m.roeRank ? (v ? ', xếp ' + m.roeRank.r + '/' + m.roeRank.n + ' trong các ngân hàng theo dõi' : ', ranked ' + m.roeRank.r + ' of ' + m.roeRank.n + ' among the banks tracked') : '') + '.'; });
    }
    /* valuation against the stock's own recent history (not a call on direction) */
    var R = m.pbR;
    if (R && R.n >= 8 && m.pb > 0) {
      if (R.now <= R.lo * 1.03) add('valuation', 1, function (v) { return v ? 'P/B ' + f(R.now, 2, v) + ' lần, thấp nhất trong ' + R.n + ' quý gần đây (khoảng ' + f(R.lo, 2, v) + '–' + f(R.hi, 2, v) + ', trung vị ' + f(R.med, 2, v) + ').' : 'P/B of ' + f(R.now, 2, v) + 'x, the lowest of the last ' + R.n + ' quarters (range ' + f(R.lo, 2, v) + '–' + f(R.hi, 2, v) + ', median ' + f(R.med, 2, v) + ').'; });
      else if (R.now >= R.hi * 0.97) add('valuation', -1, function (v) { return v ? 'P/B ' + f(R.now, 2, v) + ' lần, cao nhất trong ' + R.n + ' quý gần đây (khoảng ' + f(R.lo, 2, v) + '–' + f(R.hi, 2, v) + ', trung vị ' + f(R.med, 2, v) + ').' : 'P/B of ' + f(R.now, 2, v) + 'x, the highest of the last ' + R.n + ' quarters (range ' + f(R.lo, 2, v) + '–' + f(R.hi, 2, v) + ', median ' + f(R.med, 2, v) + ').'; });
    }
    return out;
  }

  /* fact card: bars of quarterly profit plus a few headline figures */
  function card(t) {
    var m = metrics(t); if (!m) return null;
    var c = m.c, n = Math.min(8, c.q.length), stats = [];
    function S(label, value, note) { stats.push({ label: label, value: value, note: note || ['', ''] }); }
    S(['Lợi nhuận ' + m.q, m.q + ' profit'], both(function (v) { return money(m.np, v); }), both(function (v) { return m.npYoY == null ? '' : pct(m.npYoY, v) + (v ? ' so với cùng kỳ' : ' year on year'); }));
    S(['12 tháng gần nhất', 'Last 12 months'], both(function (v) { return money(m.ttm, v); }), both(function (v) { return m.ttmYoY == null ? '' : pct(m.ttmYoY, v) + (v ? ' so với 12 tháng trước' : ' on the prior 12 months'); }));
    S(['ROE (12 tháng)', 'ROE (trailing)'], both(function (v) { return p0(m.roe, v); }), both(function (v) { return m.roeRank ? (v ? 'xếp ' + m.roeRank.r + '/' + m.roeRank.n + ' trong ngành' : 'ranked ' + m.roeRank.r + ' of ' + m.roeRank.n + ' in sector') : ''; }));
    if (m.type === 'Bank') {
      S(['NIM', 'NIM'], both(function (v) { return p0(m.nim, v, 2); }), both(function (v) { return m.nim0 == null ? '' : (v ? 'một năm trước ' : 'a year ago ') + p0(m.nim0, v, 2); }));
      S(['Nợ xấu · bao phủ', 'NPLs · coverage'], both(function (v) { return p0(m.npl, v, 2) + ' · ' + p0(m.cov, v, 0); }), both(function (v) { return m.npl0 == null ? '' : (v ? 'một năm trước ' : 'a year ago ') + p0(m.npl0, v, 2) + ' · ' + p0(m.cov0, v, 0); }));
      S(['CASA · chi phí vốn', 'CASA · cost of funds'], both(function (v) { return p0(m.casa, v) + ' · ' + p0(m.cof, v, 2); }));
    } else {
      if (m.type === 'Company') S(['Biên gộp (12 tháng)', 'Gross margin (trailing)'], both(function (v) { return p0(m.gm, v); }), both(function (v) { return m.gm0 == null ? '' : (v ? 'một năm trước ' : 'a year ago ') + p0(m.gm0, v); }));
      if (m.type === 'Securities') S(['Ký quỹ / vốn chủ', 'Margin loans / equity'], both(function (v) { return m.mle == null ? '–' : f(m.mle, 2, v) + (v ? ' lần' : 'x'); }), both(function (v) { return m.mlg == null ? '' : (v ? 'dư nợ ' : 'loans ') + pct(m.mlg, v) + (v ? ' so với cùng kỳ' : ' year on year'); }));
      S(['Nợ vay / vốn chủ', 'Debt / equity'], both(function (v) { return m.de == null ? '–' : f(m.de, 2, v) + (v ? ' lần' : 'x'); }), both(function (v) { return m.cover == null || m.type !== 'Company' ? '' : (v ? 'lãi vay được trả ' + f(m.cover, 1, v) + ' lần' : 'interest covered ' + f(m.cover, 1, v) + ' times'); }));
    }
    S(['P/B', 'P/B'], both(function (v) { return m.pb == null ? '–' : f(m.pb, 2, v) + (v ? ' lần' : 'x'); }), both(function (v) { return m.pbR ? (v ? m.pbR.n + ' quý: ' : m.pbR.n + ' quarters: ') + f(m.pbR.lo, 2, v) + '–' + f(m.pbR.hi, 2, v) : (m.pbRank ? (v ? 'rẻ thứ ' + m.pbRank.r + '/' + m.pbRank.n + ' trong ngành' : m.pbRank.r + ' of ' + m.pbRank.n + ' cheapest in sector') : ''); }));
    return { q: c.q.slice(-n), np: c.np.slice(-n), stats: stats, asof: m.q, stale: m.stale };
  }

  var API = { init: init, metrics: metrics, signals: signals, card: card };
  root.PM_FACTS = API;
  if (typeof module !== 'undefined' && module.exports) module.exports = API;
})(typeof window !== 'undefined' ? window : globalThis);
