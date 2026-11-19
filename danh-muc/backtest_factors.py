#!/usr/bin/env python3
"""Backtest of the consultant's factors on Vietnamese data. Standard library only.

    python3 backtest_factors.py prices.json fund.json market.js > backtest.js

prices.json  {ticker: {date: adjusted close}}, daily, including VNINDEX
fund.json    {ticker: [{y, q, rev, np, roe}]}   single-quarter revenue-equivalent and profit to parent (VND), trailing ROE
market.js    the page's market file: sector of each ticker and today's market value, used to scale value back in time

Design, and why
  Point in time   a quarter's figures are used only from 45 days after the quarter ends.
  Formation       last trading day of each month; scores rank the stocks that have a full set of inputs that day.
  Portfolios      top third and bottom third by score, equal weight, held one month, no costs unless stated.
  Value           trailing-year profit over market value. Market value in the past = today's market value scaled by the
                  adjusted price, which ignores new share issues; this is an approximation and is stated on the page.
  Growth          profit and revenue against a year earlier (latest quarter and trailing year).
  Quality         trailing ROE only (the live score adds balance-sheet measures that lack clean history).
  Momentum        12 months skipping the last, 6 months, 3 months, distance from the 200-session average.
  Low risk        volatility, beta and deepest fall over 252 sessions.
  Flow            not tested: the flow feed has one year of history with gaps.
Known bias: the universe is the stocks tracked today, so companies that failed or shrank are absent (survivorship).
"""
import json, math, sys, re, datetime

LAG_DAYS, MIN_NAMES, COST_ROUND_TRIP = 45, 30, 0.005
FACTORS = ['value', 'growth', 'quality', 'momentum', 'lowrisk', 'combo']

def qend(y, q): return datetime.date(y, [3, 6, 9, 12][q - 1], [31, 30, 30, 31][q - 1])
def mean(a): return sum(a) / len(a) if a else None
def sd(a): m = mean(a); return math.sqrt(sum((x - m) ** 2 for x in a) / (len(a) - 1)) if len(a) > 1 else None
def tstat(a): s = sd(a); return mean(a) / (s / math.sqrt(len(a))) if s else None
def pct_rank(d):
    """dict key->value  =>  dict key->percentile 0..100 (ties share the average rank)"""
    ks = sorted(d, key=lambda k: d[k]); n = len(ks); out = {}
    i = 0
    while i < n:
        j = i
        while j + 1 < n and d[ks[j + 1]] == d[ks[i]]: j += 1
        for k in ks[i:j + 1]: out[k] = ((i + j) / 2) / (n - 1) * 100 if n > 1 else 50
        i = j + 1
    return out
def spearman(a, b):
    ks = [k for k in a if k in b]
    if len(ks) < 10: return None
    ra = pct_rank({k: a[k] for k in ks}); rb = pct_rank({k: b[k] for k in ks})
    ma = mean(list(ra.values())); mb = mean(list(rb.values()))
    num = sum((ra[k] - ma) * (rb[k] - mb) for k in ks); den = math.sqrt(sum((ra[k] - ma) ** 2 for k in ks) * sum((rb[k] - mb) ** 2 for k in ks))
    return num / den if den else None

def main(pp, fp, mp):
    px = json.load(open(pp)); fund = json.load(open(fp))
    ms = open(mp, encoding='utf-8').read(); M = json.loads(ms[ms.index('{'):ms.rindex('}') + 1])
    cal = sorted(d for d in px['VNINDEX'] if d <= max(px['VNINDEX']))
    pos = {d: i for i, d in enumerate(cal)}
    tick = [t for t in M['t'] if t in px and t in fund]
    # forward-filled close on the index calendar, None before listing
    P = {}
    for t in tick + ['VNINDEX']:
        s = px[t]; first = min(s); row = []; lastv = None
        for d in cal:
            if d in s: lastv = s[d]
            row.append(lastv if d >= first else None)
        P[t] = row
    snap_i = pos[M['asof']] if M['asof'] in pos else len(cal) - 1
    capnow = {t: M['t'][t]['cap'] * 1e12 for t in tick}            # VND at the snapshot date
    # month-end formation dates
    ends = [cal[i] for i in range(len(cal) - 1) if cal[i][:7] != cal[i + 1][:7]]
    F = {}
    for t in tick:
        rows = {(r['y'], r['q']): r for r in fund[t]}
        F[t] = rows
    def avail(t, d):
        """quarters known on date d, newest first"""
        dd = datetime.date.fromisoformat(d)
        ks = [k for k in F[t] if qend(*k) + datetime.timedelta(days=LAG_DAYS) <= dd and F[t][k].get('np') is not None]
        return sorted(ks, reverse=True)
    def prevq(k, n=1):
        y, q = k
        for _ in range(n):
            q -= 1
            if q == 0: y, q = y - 1, 4
        return (y, q)
    def scores(d):
        i = pos[d]; raw = {f: {} for f in ['ey', 'gq', 'gt', 'gr', 'roe', 'r12', 'r6', 'r3', 'd200', 'vol', 'beta', 'dd']}
        idx = P['VNINDEX']; ir = [math.log(idx[j] / idx[j - 1]) for j in range(i - 251, i + 1)]
        im = mean(ir); iv = sum((x - im) ** 2 for x in ir)
        elig = []
        for t in tick:
            p = P[t]
            if i < 252 or p[i - 252] is None or p[i] is None: continue
            ks = avail(t, d)
            if not ks: continue
            k0 = ks[0]; q4 = [k0] + [prevq(k0, n) for n in (1, 2, 3)]; q8 = [prevq(k0, n) for n in (4, 5, 6, 7)]
            g = lambda k, f: (F[t].get(k) or {}).get(f)
            ttm = None if any(g(k, 'np') is None for k in q4) else sum(g(k, 'np') for k in q4)
            ttm0 = None if any(g(k, 'np') is None for k in q8) else sum(g(k, 'np') for k in q8)
            if ttm is None: continue
            elig.append(t)
            cap = capnow[t] * p[i] / P[t][snap_i]
            raw['ey'][t] = ttm / cap
            a, b = g(k0, 'np'), g(prevq(k0, 4), 'np')
            if a is not None and b is not None: raw['gq'][t] = (a / b - 1) if b > 0 else (1 if a > b else -1)
            if ttm0 is not None: raw['gt'][t] = (ttm / ttm0 - 1) if ttm0 > 0 else (1 if ttm > ttm0 else -1)
            a, b = g(k0, 'rev'), g(prevq(k0, 4), 'rev')
            if a is not None and b: raw['gr'][t] = a / b - 1 if b > 0 else 0
            if g(k0, 'roe') is not None: raw['roe'][t] = g(k0, 'roe')
            raw['r12'][t] = p[i - 21] / p[i - 252] - 1; raw['r6'][t] = p[i] / p[i - 126] - 1; raw['r3'][t] = p[i] / p[i - 63] - 1
            raw['d200'][t] = p[i] / mean(p[i - 199:i + 1]) - 1
            r = [math.log(p[j] / p[j - 1]) for j in range(i - 251, i + 1)]; m = mean(r)
            raw['vol'][t] = -math.sqrt(sum((x - m) ** 2 for x in r) / 251)
            raw['beta'][t] = -(sum((x - m) * (y - im) for x, y in zip(r, ir)) / iv)
            pk = p[i - 252]; ddm = 0
            for j in range(i - 252, i + 1): pk = max(pk, p[j]); ddm = min(ddm, p[j] / pk - 1)
            raw['dd'][t] = ddm
        rk = {k: pct_rank(v) for k, v in raw.items()}
        parts = {'value': ['ey'], 'growth': ['gq', 'gt', 'gr'], 'quality': ['roe'], 'momentum': ['r12', 'r6', 'r3', 'd200'], 'lowrisk': ['vol', 'beta', 'dd']}
        out = {f: {} for f in FACTORS}
        for t in elig:
            vals = {}
            for f, ks in parts.items():
                v = [rk[k][t] for k in ks if t in rk[k]]
                if v: vals[f] = mean(v); out[f][t] = vals[f]
            if len(vals) == 5: out['combo'][t] = mean(list(vals.values()))
        return out, elig
    def neutral(sc):
        """rank inside the sector where it has at least 4 names, else across all"""
        bysec = {}
        for t in sc: bysec.setdefault(M['t'][t]['sec'], {})[t] = sc[t]
        out = {}; rest = {}
        for s, d in bysec.items():
            if len(d) >= 4: out.update(pct_rank(d))
            else: rest.update(d)
        allr = pct_rank(sc)
        for t in rest: out[t] = allr[t]
        return out

    res = {f: {'tb': [], 'tu': [], 'top': [], 'bot': [], 'ic': [], 'turn': [], 'ntb': [], 'ntu': []} for f in FACTORS}
    uni, idxr, dates, counts = [], [], [], []
    prev_top = {f: None for f in FACTORS}
    for a, b in zip(ends[:-1], ends[1:]):
        if pos[a] < 252: continue
        sc, elig = scores(a)
        if len(elig) < MIN_NAMES: continue
        ret = {t: P[t][pos[b]] / P[t][pos[a]] - 1 for t in elig}
        u = mean(list(ret.values())); uni.append(u); idxr.append(P['VNINDEX'][pos[b]] / P['VNINDEX'][pos[a]] - 1); dates.append(b); counts.append(len(elig))
        for f in FACTORS:
            s = sc[f]
            if len(s) < MIN_NAMES:
                for k in res[f]: res[f][k].append(None)
                continue
            for key, sx in (('', s), ('n', neutral(s))):
                order = sorted(sx, key=lambda t: sx[t]); n3 = len(order) // 3
                top, bot = order[-n3:], order[:n3]
                rt, rb = mean([ret[t] for t in top]), mean([ret[t] for t in bot]); um = mean([ret[t] for t in sx])
                res[f][key + 'tb'].append(rt - rb); res[f][key + 'tu'].append(rt - um)
                if key == '':
                    res[f]['top'].append(rt); res[f]['bot'].append(rb); res[f]['ic'].append(spearman(s, ret))
                    pt = prev_top[f]; res[f]['turn'].append(None if pt is None else 1 - len(set(top) & pt) / len(top)); prev_top[f] = set(top)
    def clean(a): return [x for x in a if x is not None]
    def summ(a):
        a = clean(a)
        if len(a) < 12: return None
        return {'n': len(a), 'ann': round(mean(a) * 12 * 100, 1), 't': round(tstat(a), 2), 'hit': round(sum(1 for x in a if x > 0) / len(a) * 100)}
    def cum(a):
        c = 1.0; out = []
        for x in a: c *= 1 + (x or 0); out.append(round((c - 1) * 100, 1))
        return out
    def maxdd(a):
        c = 1.0; pk = 1.0; m = 0
        for x in clean(a): c *= 1 + x; pk = max(pk, c); m = min(m, c / pk - 1)
        return round(m * 100, 1)
    periods = [('2019-07', '2021-12'), ('2022-01', '2022-12'), ('2023-01', '2026-12')]
    out = {'from': dates[0], 'to': dates[-1], 'months': len(dates), 'names': [min(counts), max(counts)], 'lag': LAG_DAYS, 'cost': COST_ROUND_TRIP * 100,
           'dates': dates, 'universe': {'ann': round(mean(uni) * 12 * 100, 1), 'index': round(mean(idxr) * 12 * 100, 1), 'cum': cum(uni), 'cumIndex': cum(idxr)}, 'f': {}}
    for f in FACTORS:
        r = res[f]; turn = clean(r['turn']); mt = mean(turn) if turn else None
        net = [None if x is None else x - (tn or 0) * COST_ROUND_TRIP for x, tn in zip(r['tu'], r['turn'])]
        o = {'tb': summ(r['tb']), 'tu': summ(r['tu']), 'ntb': summ(r['ntb']), 'ntu': summ(r['ntu']), 'tuNet': summ(net),
             'ic': None, 'turn': None if mt is None else round(mt * 100), 'dd': maxdd(r['tu']), 'cumTU': cum(r['tu']), 'cumTB': cum(r['tb']), 'sub': []}
        ic = clean(r['ic'])
        if ic: o['ic'] = {'mean': round(mean(ic), 3), 't': round(tstat(ic), 2)}
        for lo, hi in periods:
            seg = [x for x, d in zip(r['tu'], dates) if x is not None and lo <= d[:7] <= hi]
            o['sub'].append({'p': lo[:4] + ('–' + hi[:4] if hi[:4] != lo[:4] else ''), 'ann': round(mean(seg) * 12 * 100, 1) if seg else None, 'n': len(seg)})
        out['f'][f] = o
    sys.stdout.write('/* Generated by backtest_factors.py; do not edit by hand. */\n')
    sys.stdout.write('window.PM_BACKTEST = ' + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + ';\n')

if __name__ == '__main__':
    main(*sys.argv[1:4])
