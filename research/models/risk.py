#!/usr/bin/env python3
"""Downside-risk metrics for the book: Roy's safety-first, shortfall probability, Sortino.

Reads the same beliefs as decide.py. Adds nothing new -- it re-reads the scenario tree and
the block correlation model and asks a different question of them: not "what do we expect?"
but "how likely are we to fall short of a threshold we care about?"

Two things worth knowing before reading the output.

1. Shortfall probability is reported TWO ways. The normal approximation is the textbook
   version and it is optimistic, because equity returns have fatter left tails than a
   normal. The scenario version resamples each name's actual bear/base/bull tree through a
   Gaussian copula built from the same block correlations the optimizer uses, so names go
   bear together as often as the correlation model says they should. Where the two disagree,
   the scenario number is the more honest one.

2. Everything here inherits the input problems logged on 2026-07-28. Garbage in, precise
   garbage out. The caveats are printed at the end rather than buried.

Run: python3 research/models/risk.py
"""
from __future__ import annotations

import json
import math
import pathlib
import random

HERE = pathlib.Path(__file__).parent
A = json.loads((HERE / "assumptions.json").read_text(encoding="utf-8"))
V, P, O = A["valuation"], A["portfolio"], A["optimizer"]
SCEN = ("bear", "base", "bull")

# Thresholds a Vietnamese investor might actually care about. The deposit rate is the one
# that matters most: it is what this money would earn doing nothing risky.
THRESHOLDS = [
    (0.00, "nominal capital preservation"),
    (0.035, "Vietnam CPI, approx -- real capital preservation"),
    (0.06, "12-month bank deposit, approx -- the true alternative"),
    (0.10, "a 10% hurdle"),
]

TRIALS = 200_000
SEED = 20260728


def per_name() -> dict:
    """Same computation decide.py does, kept separate so this file cannot drift from it."""
    res = {}
    for tk, v in V.items():
        if tk.startswith("_"):
            continue
        cap_now = v["pe_ttm"] * v["npat_ttm"]
        rets = [v["exit_pe"][s] * v["fy26e_npat"][s] / cap_now - 1 + v["cash_yield"] for s in SCEN]
        ps = [v["probs"][s] for s in SCEN]
        tot = sum(ps)
        ps = [p / tot for p in ps]
        mu_raw = sum(p * r for p, r in zip(ps, rets))
        sd_scen = math.sqrt(sum(p * (r - mu_raw) ** 2 for p, r in zip(ps, rets)))
        res[tk] = {
            "rets": rets, "ps": ps, "mu_raw": mu_raw,
            "conf": v["confidence"], "mu": mu_raw * v["confidence"],
            "sd_scen": sd_scen,
            "sigma": math.sqrt(sd_scen ** 2 + O["base_vol_annual"] ** 2),
        }
    return res


def corr_matrix(tickers: list[str]) -> list[list[float]]:
    cl = {p["ticker"]: p["cluster"] for p in P["positions"]}
    sec = O["sectors"]
    n = len(tickers)
    m = [[0.0] * n for _ in range(n)]
    for i, a in enumerate(tickers):
        for j, b in enumerate(tickers):
            if i == j:
                m[i][j] = 1.0
            elif cl.get(a) == cl.get(b):
                m[i][j] = O["corr_same_cluster"]
            elif sec.get(a) == sec.get(b):
                m[i][j] = O["corr_same_sector"]
            else:
                m[i][j] = O["corr_market_baseline"]
    return m


def cholesky(m: list[list[float]]) -> list[list[float]]:
    n = len(m)
    L = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = sum(L[i][k] * L[j][k] for k in range(j))
            if i == j:
                L[i][j] = math.sqrt(max(m[i][i] - s, 1e-12))
            else:
                L[i][j] = (m[i][j] - s) / L[j][j]
    return L


def port_stats(wts, mu, sig, corr):
    n = len(wts)
    er = sum(w * m for w, m in zip(wts, mu))
    var = sum(wts[i] * wts[j] * sig[i] * sig[j] * corr[i][j] for i in range(n) for j in range(n))
    return er, math.sqrt(var)


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def simulate(wts, names, corr, shrink: bool):
    """Resample the scenario tree with correlated branch selection plus correlated noise.

    A Gaussian copula drives WHICH branch each name lands on, using the same block
    correlations as the optimizer. That is the point: it stops the simulation from
    diversifying away a risk the correlation model says is common.
    """
    L = cholesky(corr)
    n = len(names)
    rng = random.Random(SEED)
    base_vol = O["base_vol_annual"]
    cum = []
    for t in names:
        c, run = [], 0.0
        for p in per_name()[t]["ps"]:
            run += p
            c.append(run)
        cum.append(c)
    pn = per_name()
    rets = [pn[t]["rets"] for t in names]
    conf = [pn[t]["conf"] for t in names]

    out = []
    for _ in range(TRIALS):
        z = [rng.gauss(0, 1) for _ in range(n)]
        zc = [sum(L[i][k] * z[k] for k in range(i + 1)) for i in range(n)]
        z2 = [rng.gauss(0, 1) for _ in range(n)]
        zn = [sum(L[i][k] * z2[k] for k in range(i + 1)) for i in range(n)]
        r = 0.0
        for i in range(n):
            u = norm_cdf(zc[i])
            b = 0 if u <= cum[i][0] else (1 if u <= cum[i][1] else 2)
            ri = rets[i][b]
            if shrink:
                ri *= conf[i]
            ri += zn[i] * base_vol
            r += wts[i] * ri
        out.append(r)
    out.sort()
    return out


def q(sorted_vals, p):
    idx = min(len(sorted_vals) - 1, max(0, int(p * len(sorted_vals))))
    return sorted_vals[idx]


def report(label, wts_map, pn, corr, names):
    wts = [wts_map[t] for t in names]
    mu = [pn[t]["mu"] for t in names]
    sig = [pn[t]["sigma"] for t in names]
    er, sd = port_stats(wts, mu, sig, corr)

    print(f"\n{'='*78}\n{label}   E[r] {er*100:+.2f}%   sigma {sd*100:.1f}%\n{'='*78}")
    print(f"{'threshold':<46}{'SFRatio':>9}{'P(shortfall)':>15}")
    print(f"{'':<46}{'':>9}{'normal':>15}")
    for t, why in THRESHOLDS:
        sf = (er - t) / sd
        print(f"  {t*100:>4.1f}%  {why:<37}{sf:>9.3f}{norm_cdf(-sf)*100:>14.1f}%")

    sims = simulate(wts, names, corr, shrink=True)
    mean_s = sum(sims) / len(sims)
    print(f"\n  Scenario resample ({TRIALS:,} trials, correlated branches + correlated noise)")
    print(f"    mean {mean_s*100:+.2f}%   median {q(sims,0.50)*100:+.2f}%   "
          f"5th pct {q(sims,0.05)*100:+.1f}%   1st pct {q(sims,0.01)*100:+.1f}%")
    print(f"    {'threshold':<30}{'P(shortfall)':>14}{'vs normal':>12}")
    for t, _why in THRESHOLDS:
        p_sim = sum(1 for x in sims if x < t) / len(sims)
        p_norm = norm_cdf(-(er - t) / sd)
        print(f"      {t*100:>4.1f}%{'':<25}{p_sim*100:>13.1f}%{(p_sim-p_norm)*100:>+11.1f}pp")

    # Sortino against the deposit threshold: only downside deviation is penalised.
    mar = 0.06
    dn = [min(0.0, x - mar) for x in sims]
    dd = math.sqrt(sum(d * d for d in dn) / len(dn))
    print(f"\n    Sortino vs the 6% deposit threshold: {(mean_s-mar)/dd:.3f}   "
          f"(downside deviation {dd*100:.1f}%)")
    return er, sd, sims


def main():
    pn = per_name()
    names = [p["ticker"] for p in P["positions"]]
    corr = corr_matrix(names)

    owned = {p["ticker"]: p["weight_pct"] / 100.0 for p in P["positions"]}
    print("Weights as owned:", "  ".join(f"{t} {owned[t]*100:.1f}%" for t in names))

    report("BOOK AS OWNED", owned, pn, corr, names)

    print("\n\nPer-name safety-first contribution, at the 6% deposit threshold")
    print(f"{'':<6}{'weight':>8}{'E[r]':>9}{'sigma':>8}{'SFRatio':>9}{'bear branch':>13}")
    for t in sorted(names, key=lambda x: -((pn[x]['mu']-0.06)/pn[x]['sigma'])):
        s = (pn[t]["mu"] - 0.06) / pn[t]["sigma"]
        print(f"  {t:<4}{owned[t]*100:>7.1f}%{pn[t]['mu']*100:>8.2f}%{pn[t]['sigma']*100:>7.1f}%"
              f"{s:>9.3f}{pn[t]['rets'][0]*100:>12.1f}%")

    print("""
------------------------------------------------------------------------------
WHAT THIS INHERITS -- read before using any number above
------------------------------------------------------------------------------
  Every figure is computed off assumptions.json, which on 2026-07-28 carries
  these known defects. None is fixed here and none is small:

  - VPB's two credit fields contradict each other; the forward driver is
    unverified. VPB is 10% of the book.
  - Prices are undated, presumed 24-Jul, four sessions stale. A 1% price move
    is 73% of VPB's expected-return signal and 25% of TCB's.
  - cash_yield is populated for TCB alone. MBB's 10% cash dividend, worth 4.5%
    of price, is recorded as zero. Seven blanks bias the book's E[r] DOWN.
  - VCI and VPX npat_ttm both fail the market-cap cross-check.
  - MBB and VCI have no driver model; their earnings branches are typed in.
  - sigma blends scenario dispersion with a flat 28% base vol for every name.
    That is an assumption, not a measurement -- no realised covariance exists.

  The engine shrinks the MEAN by confidence but computes DISPERSION from the
  unshrunk branches, so a low-confidence name loses return without gaining risk.
  TESTED 2026-07-29 against two alternatives -- shrinking dispersion too, and
  WIDENING it as confidence falls -- and the RANKING IS IDENTICAL under all
  three. The trim and add conclusions do not depend on this choice.

  The LEVELS do. KDH's sigma is 54.5% as computed, 36.5% if dispersion is
  shrunk, 97.6% if it is widened. Anything reading sigma levels rather than
  order is convention-dependent: the shortfall probabilities above, and the
  optimizer's own utility function, which penalises sigma SQUARED.

  On the merits: shrinking dispersion is backwards -- being less sure about a
  name should not make it look less volatile. Widening is more defensible in
  principle but produces implausible numbers (KDH at 97.6% annualised). The
  current convention sits between them and is a reasonable compromise, but
  nothing in the file records it as a CHOICE rather than a default.
------------------------------------------------------------------------------""")


if __name__ == "__main__":
    main()
