#!/usr/bin/env python3
"""CIO decision engine — turns the scenario models into a sized, ranked decision brief.

    python3 research/models/decide.py            # writes research/decisions/DECISION-BRIEF.md
    python3 research/models/decide.py --json     # machine-readable, for the agent loop

Where this sits in the stack:

    assumptions.json   beliefs      (what I think is true)
    run.py             earnings     (Layer 1-2: what the company earns)
    decide.py          DECISIONS    (Layer 3: what to own, how much, what kills it)
    decision-log.md    the record   (what I actually did, and why)
    calibration-log.md the score    (was I right — the only real measure of edge)

The chain: scenario earnings -> exit multiple -> probability-weighted expected return
-> confidence shrink -> constrained mean-variance optimization -> trade list.

Every step is arithmetic on stated assumptions. Nothing here knows anything the
assumptions file doesn't say. That is the point: when the output is wrong, the
wrong belief is findable, and `git log assumptions.json` shows when it changed.

Stdlib only.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
A = json.loads((HERE / "assumptions.json").read_text(encoding="utf-8"))

V = A["valuation"]
O = A["optimizer"]
P = A["portfolio"]
SCEN = ("bear", "base", "bull")

OUT: list[str] = []


def w(line: str = "") -> None:
    OUT.append(line)


def pct(x: float, dp: int = 1) -> str:
    return f"{x * 100:+.{dp}f}%"


# ---------------------------------------------------------------- expected return
def expected_returns() -> dict:
    """Probability-weighted 12m total return per name, then shrunk by evidence quality.

    return_s = (exit_pe_s * fy26e_npat_s) / market_cap_now - 1 + cash_yield

    The confidence shrink is deliberate and it is the most important line in this
    file. A 40% expected return computed off an UNFILED quarter is not a 40%
    expected return -- it is a 40% guess. Shrinking toward zero by evidence
    quality stops thin-evidence names from winning the optimizer on the strength
    of their own uncertainty.
    """
    res = {}
    for tk, v in V.items():
        if tk.startswith("_"):
            continue
        cap_now = v["pe_ttm"] * v["npat_ttm"]
        rets, ps = [], []
        for s in SCEN:
            cap_target = v["exit_pe"][s] * v["fy26e_npat"][s]
            rets.append(cap_target / cap_now - 1 + v["cash_yield"])
            ps.append(v["probs"][s])
        tot = sum(ps)
        ps = [p / tot for p in ps]

        mu_raw = sum(p * r for p, r in zip(ps, rets))
        var_scen = sum(p * (r - mu_raw) ** 2 for p, r in zip(ps, rets))
        sd_scen = math.sqrt(var_scen)

        conf = v["confidence"]
        mu = mu_raw * conf

        # Total risk = scenario dispersion + the market noise scenarios don't capture.
        sigma = math.sqrt(sd_scen ** 2 + O["base_vol_annual"] ** 2)

        res[tk] = {
            "ticker": tk, "price": v["price"], "cap_now": cap_now,
            "scen_returns": dict(zip(SCEN, rets)), "probs": dict(zip(SCEN, ps)),
            "mu_raw": mu_raw, "confidence": conf, "mu": mu,
            "sd_scen": sd_scen, "sigma": sigma,
            "downside": rets[0],                       # the bear branch, undiluted
            "ir": mu / sigma if sigma else 0.0,
            "evidence": v["evidence"],
        }
    return res


# ---------------------------------------------------------------- risk model
def covariance(tickers: list[str], er: dict) -> list[list[float]]:
    """Block correlation: same cluster > same sector > market baseline.

    No estimated covariance matrix exists for an 8-name book with this little
    history, and pretending otherwise would be the worst kind of false precision.
    A block model states the correlation assumption out loud where it can be
    argued with. It also earns its keep: it is what makes the optimizer refuse to
    treat TCB and TCX as two independent bets.
    """
    cl = {p["ticker"]: p["cluster"] for p in P["positions"]}
    sec = O["sectors"]
    n = len(tickers)
    cov = [[0.0] * n for _ in range(n)]
    for i, a in enumerate(tickers):
        for j, b in enumerate(tickers):
            if i == j:
                rho = 1.0
            elif cl.get(a) == cl.get(b):
                rho = O["corr_same_cluster"]
            elif sec.get(a) == sec.get(b):
                rho = O["corr_same_sector"]
            else:
                rho = O["corr_market_baseline"]
            cov[i][j] = rho * er[a]["sigma"] * er[b]["sigma"]
    return cov


def port_stats(weights: list[float], mu: list[float], cov: list[list[float]]):
    r = sum(w_ * m for w_, m in zip(weights, mu))
    var = sum(weights[i] * weights[j] * cov[i][j]
              for i in range(len(weights)) for j in range(len(weights)))
    return r, math.sqrt(max(var, 0.0))


# ---------------------------------------------------------------- optimizer
def project_capped_simplex(v: list[float], ub: list[float], total: float) -> list[float]:
    """Euclidean projection onto {w: 0 <= w <= ub, sum(w) = total} by bisection on tau."""
    lo, hi = min(v) - total, max(v)
    for _ in range(200):
        tau = (lo + hi) / 2
        s = sum(min(max(vi - tau, 0.0), ui) for vi, ui in zip(v, ub))
        if s > total:
            lo = tau
        else:
            hi = tau
    tau = (lo + hi) / 2
    return [min(max(vi - tau, 0.0), ui) for vi, ui in zip(v, ub)]


def project_cluster_caps(v: list[float], tickers: list[str], cap: float) -> list[float]:
    """Project onto {sum of each cluster <= cap}, one cluster at a time."""
    cl = {p["ticker"]: p["cluster"] for p in P["positions"]}
    out = list(v)
    groups: dict[str, list[int]] = {}
    for i, tk in enumerate(tickers):
        groups.setdefault(cl.get(tk, tk), []).append(i)
    for idx in groups.values():
        for _ in range(30):
            s = sum(out[i] for i in idx)
            if s <= cap + 1e-9:
                break
            live = [i for i in idx if out[i] > 1e-9]
            if not live:
                break
            cut = (s - cap) / len(live)
            for i in live:
                out[i] = max(out[i] - cut, 0.0)
    return out


def optimize(tickers, mu, cov, w0, total=1.0):
    """Maximize  w'mu - (lambda/2) w'Sigma w - kappa*|w - w0|  subject to the caps.

    Projected gradient ascent with alternating projection onto the two convex
    constraint sets (capped simplex, cluster caps). Eight assets -- this converges
    in a few hundred cheap iterations and avoids a solver dependency.
    """
    n = len(tickers)
    lam = O["risk_aversion_lambda"]
    kappa = O["turnover_cost"]
    ub = [O["max_single_name_pct"] / 100.0] * n
    w_ = [total / n] * n
    step = 0.03

    for it in range(4000):
        grad = []
        for i in range(n):
            g = mu[i] - lam * sum(cov[i][j] * w_[j] for j in range(n))
            d = w_[i] - w0[i]
            g -= kappa * (1.0 if d > 1e-9 else (-1.0 if d < -1e-9 else 0.0))
            grad.append(g)
        w_ = [w_[i] + step * grad[i] for i in range(n)]
        for _ in range(12):                       # alternating projection
            w_ = project_capped_simplex(w_, ub, total)
            w_ = project_cluster_caps(w_, tickers, O["max_cluster_pct"] / 100.0)
        if it > 2500:
            step = 0.008

    # Drop sub-scale positions: a 0.4% weight is noise, not a position.
    floor = O["min_position_pct"] / 100.0
    w_ = [0.0 if x < floor else x for x in w_]
    s = sum(w_)
    w_ = [x / s * total for x in w_] if s else w_
    # Renormalizing can push a name back through its cap, so re-project AFTER it
    # and keep the dropped names pinned at zero.
    keep = [i for i, x in enumerate(w_) if x > 0]
    for _ in range(200):
        w_ = project_capped_simplex(w_, ub, total)
        w_ = project_cluster_caps(w_, tickers, O["max_cluster_pct"] / 100.0)
        for i in range(n):
            if i not in keep:
                w_[i] = 0.0
    return w_


def step_toward(w0, star, tickers, total=1.0):
    """One cycle's move: cap each name's change at max_move_pp_per_cycle.

    A brief that says 'exit the entire 20% KDH position' on the eve of an unfiled
    quarter is an optimizer overreacting to soft inputs, not a recommendation.
    Funds move toward a target in steps, re-underwriting at each one. The step
    limit also bounds the damage when an assumption turns out to be wrong -- which
    is the whole reason the confidence column exists.
    """
    cap_move = O.get("max_move_pp_per_cycle", 100.0) / 100.0
    ub = [O["max_single_name_pct"] / 100.0] * len(tickers)
    stepped = [w0[i] + max(-cap_move, min(cap_move, star[i] - w0[i]))
               for i in range(len(tickers))]
    s = sum(stepped)
    stepped = [x / s * total for x in stepped] if s else stepped
    for _ in range(200):
        stepped = project_capped_simplex(stepped, ub, total)
        stepped = project_cluster_caps(stepped, tickers, O["max_cluster_pct"] / 100.0)
    return stepped


# ---------------------------------------------------------------- brief
def build():
    cur = {p["ticker"]: p["weight_pct"] / 100.0 for p in P["positions"]}
    cl = {p["ticker"]: p["cluster"] for p in P["positions"]}
    er = expected_returns()
    tickers = sorted(cur, key=lambda t: -er[t]["mu"])
    mu = [er[t]["mu"] for t in tickers]
    w0 = [cur[t] for t in tickers]
    cov = covariance(tickers, er)
    star = optimize(tickers, mu, cov, w0)
    tgt = step_toward(w0, star, tickers)

    r0, v0 = port_stats(w0, mu, cov)
    r1, v1 = port_stats(tgt, mu, cov)
    rs, vs = port_stats(star, mu, cov)

    w(f"# Decision Brief — generated {A['_meta']['as_of']}\n")
    w("> `python3 research/models/decide.py`. Beliefs in `assumptions.json`; decisions "
      "recorded in `research/decisions/decision-log.md`; accuracy scored in "
      "`calibration-log.md`. **Recommendations, not orders — a human signs every trade.**\n")

    # ---- 1 · ranked expected returns
    w("## 1 · Ranked expected return (12m)\n")
    w("`E[r] = Σ p(scenario) × [ exit multiple × FY26E earnings / market cap − 1 ] × confidence`\n")
    w("| Rank | Ticker | Raw E[r] | Conf | **Shrunk E[r]** | Bear branch | σ | E[r]/σ | Evidence |")
    w("|---|---|---:|---:|---:|---:|---:|---:|---|")
    for i, t in enumerate(tickers, 1):
        e = er[t]
        w(f"| {i} | **{t}** | {pct(e['mu_raw'])} | {e['confidence']:.2f} | "
          f"**{pct(e['mu'])}** | {pct(e['downside'])} | {e['sigma']*100:.0f}% | "
          f"{e['ir']:.2f} | {e['evidence']} |")
    w("\nThe **confidence column is the discipline**: three of eight names still price off an "
      "unfiled quarter. Shrinking their expected return toward zero is what stops the optimizer "
      "from rewarding a name for being poorly understood.\n")

    # ---- 2 · the optimizer
    w("## 2 · Target weights vs the book you own\n")
    band = O["no_trade_band_pct"] / 100.0
    w(f"Two columns on purpose. **North star** is where the math points if the assumptions "
      f"are right. **This cycle** moves at most {O['max_move_pp_per_cycle']:.0f}pp per name — "
      "because the assumptions are not all equally right yet, and three of these names report "
      "within the week.\n")
    w("| Ticker | Cluster | Current | **This cycle** | Δ | North star | Action |")
    w("|---|---|---:|---:|---:|---:|---|")
    trades = []
    for i, t in enumerate(tickers):
        d = tgt[i] - w0[i]
        if abs(d) < band:
            act = "hold"
        elif d > 0:
            act = f"**ADD** +{d*100:.1f}pp"
        else:
            act = f"**TRIM** {d*100:.1f}pp"
        if abs(d) >= band:
            trades.append((t, w0[i], tgt[i], d, star[i]))
        w(f"| {t} | {cl[t]} | {w0[i]*100:.1f}% | **{tgt[i]*100:.1f}%** | "
          f"{d*100:+.1f}pp | {star[i]*100:.1f}% | {act} |")

    lam = O["risk_aversion_lambda"]
    u = lambda r, v: r - lam / 2 * v * v
    w(f"\n| | Expected return | Expected vol | Return/vol | Utility |")
    w("|---|---:|---:|---:|---:|")
    w(f"| Book as owned | {pct(r0)} | {v0*100:.1f}% | {r0/v0:.2f} | {u(r0,v0):.3f} |")
    w(f"| After this cycle | {pct(r1)} | {v1*100:.1f}% | {r1/v1:.2f} | {u(r1,v1):.3f} |")
    w(f"| North star | {pct(rs)} | {vs*100:.1f}% | {rs/vs:.2f} | **{u(rs,vs):.3f}** |")
    w(f"| **This cycle captures** | **{(r1-r0)*100:+.1f}pp** | **{(v1-v0)*100:+.1f}pp** | "
      f"**{(r1/v1)-(r0/v0):+.2f}** | **{u(r1,v1)-u(r0,v0):+.3f}** |")
    w(f"\nThe optimizer maximizes **utility** (`E[r] − λ/2 × σ²`, λ={lam:.0f}), not raw return — "
      "which is why the north star can show a *lower* expected return than an intermediate "
      "step and still be the better book. It is buying a large reduction in risk with a small "
      "amount of return. That trade is the entire point of running a portfolio instead of a "
      "list of favourite stocks.\n")
    w(f"No-trade band ±{O['no_trade_band_pct']:.0f}pp — smaller gaps are inside the noise of "
      "the assumptions and are not worth the spread.\n")
    over = [t for i, t in enumerate(tickers)
            if w0[i] * 100 > O["max_single_name_pct"] + 1e-6]
    if over:
        w(f"⚠ **{', '.join(over)} moves further than the {O['max_move_pp_per_cycle']:.0f}pp "
          "step limit.** That is deliberate, not a bug: a position already through the "
          f"{O['max_single_name_pct']:.0f}% constitutional cap gets brought back to the cap now. "
          "The step limit governs *discretionary* moves; a breach of the constitution is not "
          "discretionary.\n")

    # ---- 3 · risk diagnostics
    w("## 3 · Risk diagnostics\n")
    w("| Cluster | Current | Target | Cap | Status |")
    w("|---|---:|---:|---:|---|")
    cc: dict[str, list[float]] = {}
    for i, t in enumerate(tickers):
        c = cl[t]
        cc.setdefault(c, [0.0, 0.0])
        cc[c][0] += w0[i]
        cc[c][1] += tgt[i]
    for c, (a, b) in sorted(cc.items(), key=lambda kv: -kv[1][0]):
        cap = O["max_cluster_pct"]
        st = "⚠ **BREACH**" if a * 100 > cap + 1e-6 else "ok"
        st += " → resolved" if a * 100 > cap and b * 100 <= cap + 1e-6 else ""
        w(f"| {c} | {a*100:.1f}% | {b*100:.1f}% | {cap:.0f}% | {st} |")

    hhi0 = sum(x ** 2 for x in w0)
    hhi1 = sum(x ** 2 for x in tgt)
    w(f"\n- Effective independent bets: **{1/hhi0:.1f} → {1/hhi1:.1f}** (HHI {hhi0:.3f} → {hhi1:.3f})")

    # marginal contribution to risk — where the risk actually comes from
    w("\n**Marginal contribution to risk** — the honest answer to 'what am I actually exposed to':\n")
    w("| Ticker | Weight (target) | MCTR | % of portfolio risk |")
    w("|---|---:|---:|---:|")
    mctr = [sum(cov[i][j] * tgt[j] for j in range(len(tickers))) / v1 if v1 else 0
            for i in range(len(tickers))]
    contrib = [tgt[i] * mctr[i] for i in range(len(tickers))]
    tot_c = sum(contrib) or 1.0
    for i, t in sorted(enumerate(tickers), key=lambda kv: -contrib[kv[0]]):
        if tgt[i] < 1e-6:
            continue
        w(f"| {t} | {tgt[i]*100:.1f}% | {mctr[i]*100:.1f}% | {contrib[i]/tot_c*100:.0f}% |")

    # ---- 4 · the trade list
    w("\n## 4 · Trade list\n")
    if not trades:
        w("No trades outside the no-trade band. Hold.\n")
    else:
        for t, a, b, d, st in sorted(trades, key=lambda x: -abs(x[3])):
            verb = "BUY" if d > 0 else "SELL"
            w(f"- **{verb} {t}** — {a*100:.1f}% → {b*100:.1f}% ({d*100:+.1f}pp; north star "
              f"{st*100:.1f}%). E[r] {pct(er[t]['mu'])}, bear branch {pct(er[t]['downside'])}. "
              f"{er[t]['evidence']}")
        w("\n**Sequencing rule:** trims before adds (fund the buys, don't lever), and nothing "
          "that fights a dated catalyst inside 5 sessions — see the catalyst calendar.\n")

    # ---- 5 · kill criteria
    w("## 5 · Kill-criteria check (mechanical)\n")
    kc = A.get("kill_criteria", {})
    if kc:
        w("| Ticker | Condition | Test | Status |")
        w("|---|---|---|---|")
        for t in tickers:
            for k in kc.get(t, []):
                w(f"| {t} | {k['condition']} | {k['test']} | {k['status']} |")
        w("\nWritten before the event, checked at every event, not 'when it feels right'. "
          "A triggered criterion is not a suggestion — it forces the resize at the next brief.\n")
    else:
        w("_No kill criteria defined._\n")

    w("---\n")
    w("**What this brief cannot do.** It cannot price governance, quota politics, an "
      "An Lap-style related-party surprise, or a market that simply stays irrational longer "
      "than the horizon. Those are Layer 4 and they live in the dossiers. The optimizer's job "
      "is to stop *arithmetic* mistakes — position sizes that don't match stated conviction — "
      "not to replace judgment about what is true.\n")

    (ROOT / "research" / "decisions").mkdir(parents=True, exist_ok=True)
    (ROOT / "research" / "decisions" / "DECISION-BRIEF.md").write_text(
        "\n".join(OUT) + "\n", encoding="utf-8")

    return {
        "as_of": A["_meta"]["as_of"],
        "expected_returns": {t: {k: er[t][k] for k in ("mu_raw", "mu", "confidence",
                                                       "sigma", "downside", "ir")}
                             for t in tickers},
        "current_weights": {t: w0[i] for i, t in enumerate(tickers)},
        "target_weights": {t: tgt[i] for i, t in enumerate(tickers)},
        "north_star_weights": {t: star[i] for i, t in enumerate(tickers)},
        "trades": [{"ticker": t, "from": a, "to": b, "delta": d, "north_star": st}
                   for t, a, b, d, st in trades],
        "portfolio": {"current": {"er": r0, "vol": v0},
                      "this_cycle": {"er": r1, "vol": v1},
                      "north_star": {"er": rs, "vol": vs}},
    }


if __name__ == "__main__":
    result = build()
    if "--json" in sys.argv:
        print(json.dumps(result, indent=2))
    else:
        print("\n".join(OUT))
