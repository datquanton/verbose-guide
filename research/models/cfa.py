#!/usr/bin/env python3
"""CFA Level III portfolio analytics applied to this book.

WHY THIS FILE EXISTS, separately from decide.py and risk.py.

decide.py asks "what should the weights be?". risk.py asks "will this beat a deposit?".
This file asks the questions the Level III curriculum asks, which are different again and
mostly diagnostic rather than prescriptive:

  - Where does the RISK actually sit, as opposed to where the money sits?
  - What returns must you ALREADY believe, for today's weights to be rational?
  - How many genuinely independent bets is this, once correlation is accounted for?
  - How good would your stock-picking have to be to justify the active risk you run?
  - What does volatility cost you in compounded terms, as opposed to average terms?
  - What survives tax?

Every number here is DIAGNOSTIC. Nothing in this file changes a weight, a branch or a
probability, and nothing here is read by decide.py or run.py. The system recommends; a
human signs.

INHERITED DEFECTS. Everything is computed off assumptions.json and inherits every input
problem listed at the end of risk.py -- undated prices, VPB's contradictory credit pair,
cash_yield populated for one name of eight, no driver model for MBB or VCI, and a sigma
that blends scenario dispersion with a flat assumed base vol because no realised
covariance matrix exists. Precise arithmetic on uncertain inputs is still uncertain.

Run: python3 research/models/cfa.py
"""
from __future__ import annotations

import json
import math
import pathlib

import risk  # reuses per_name(), corr_matrix(), cholesky(), port_stats(), simulate()

HERE = pathlib.Path(__file__).parent
A = json.loads((HERE / "assumptions.json").read_text(encoding="utf-8"))
O = A["optimizer"]
P = A["portfolio"]

# ---------------------------------------------------------------------------
# MARKET INPUTS -- sourced 2026-07-29, NOT invented. Each carries its provenance
# because a Level III formula fed a made-up benchmark produces a made-up answer.
# ---------------------------------------------------------------------------
RF_SHORT = 0.0356       # Vietnam 2Y government bond yield. T5 press, Jul-2026.
RF_LONG = 0.0452        # Vietnam 10Y government bond yield, a 33-month high. T5, 09-Jul-2026.
DEPOSIT = 0.06          # 12-month bank deposit, approx. The threshold risk.py uses.
BENCH_DAILY_VOL = 0.0099  # VN-Index realised daily vol, 29-Apr to 28-Jul 2026. T5.
TRADING_DAYS = 252
BENCH_VOL = BENCH_DAILY_VOL * math.sqrt(TRADING_DAYS)   # ~15.7% annualised

TAX_PROCEEDS = 0.001    # PIT on listed-securities disposal: 0.1% of PROCEEDS, not gains.
TAX_DIVIDEND = 0.05     # PIT on dividends.
TAX_GAINS_DRAFT = 0.20  # Draft MoF decree: 20% on actual annual gains. NOT law.

LAMBDA = O["risk_aversion_lambda"]
TURNOVER_COST = O["turnover_cost"]

# Weights from decide.py's two proposed books, for the transfer-coefficient calculation.
THIS_CYCLE = {"TCX": 11.0, "VPX": 1.2, "HPG": 20.0, "MBB": 12.0,
              "KDH": 15.6, "VCI": 5.0, "TCB": 20.0, "VPB": 15.3}
NORTH_STAR = {"TCX": 20.0, "VPX": 0.0, "HPG": 20.0, "MBB": 20.0,
              "KDH": 3.1, "VCI": 4.1, "TCB": 15.0, "VPB": 17.8}


def hr(title: str) -> None:
    print(f"\n{'=' * 78}\n{title}\n{'=' * 78}")


def cov_matrix(sig, corr):
    n = len(sig)
    return [[sig[i] * sig[j] * corr[i][j] for j in range(n)] for i in range(n)]


def matvec(m, v):
    return [sum(m[i][j] * v[j] for j in range(len(v))) for i in range(len(m))]


def pearson(x, y):
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sxx = sum((a - mx) ** 2 for a in x)
    syy = sum((b - my) ** 2 for b in y)
    return sxy / math.sqrt(sxx * syy) if sxx > 0 and syy > 0 else float("nan")


# ---------------------------------------------------------------------------


def main():
    pn = risk.per_name()
    names = [p["ticker"] for p in P["positions"]]
    corr = risk.corr_matrix(names)
    w = [next(p["weight_pct"] for p in P["positions"] if p["ticker"] == t) / 100.0
         for t in names]
    mu = [pn[t]["mu"] for t in names]
    sig = [pn[t]["sigma"] for t in names]
    cov = cov_matrix(sig, corr)
    n = len(names)

    er, sd = risk.port_stats(w, mu, sig, corr)

    print(__doc__.split("Run:")[0].strip().split("\n")[0])
    print(f"\nBook: {n} names.  E[r] {er * 100:+.2f}%   sigma {sd * 100:.1f}%   "
          f"rf(2Y govt) {RF_SHORT * 100:.2f}%   VN-Index sigma {BENCH_VOL * 100:.1f}%")

    # =====================================================================
    hr("1 · RISK BUDGETING — where the risk actually sits")
    print("""
  A weight tells you where the MONEY is. It does not tell you where the RISK is,
  because a volatile name correlated with everything else contributes far more risk
  than its weight suggests, and a small uncorrelated name contributes less.

    Marginal contribution to risk   MCTR_i = (Sigma w)_i / sigma_p
      -- how much portfolio risk rises if you add 1 unit more of name i.
    Contribution to total risk      CCTR_i = w_i x MCTR_i
      -- name i's actual share of portfolio volatility. These SUM to sigma_p exactly.
    Beta to own portfolio           beta_i,p = (Sigma w)_i / sigma_p^2

  The test: is the risk share bigger than the money share? If yes, the position is
  doing more damage than its size implies.""")
    sw = matvec(cov, w)
    mctr = [x / sd for x in sw]
    cctr = [w[i] * mctr[i] for i in range(n)]
    beta_p = [x / (sd ** 2) for x in sw]

    print(f"\n  {'':<6}{'weight':>8}{'MCTR':>9}{'CCTR':>9}{'% of risk':>11}"
          f"{'% of money':>12}{'risk/money':>12}{'beta to pf':>12}")
    order = sorted(range(n), key=lambda i: -cctr[i])
    for i in order:
        share_r = cctr[i] / sd
        ratio = share_r / w[i]
        flag = "  <-- risk hog" if ratio > 1.05 else ("  <-- risk-light" if ratio < 0.95 else "")
        print(f"  {names[i]:<6}{w[i] * 100:>7.1f}%{mctr[i]:>9.3f}{cctr[i]:>9.4f}"
              f"{share_r * 100:>10.1f}%{w[i] * 100:>11.1f}%{ratio:>12.2f}{beta_p[i]:>12.2f}{flag}")
    print(f"  {'':<6}{'':>8}{'':>9}{sum(cctr):>9.4f}{'100.0%':>11}"
          f"     <- sums to sigma_p = {sd:.4f}, as it must")

    # =====================================================================
    hr("2 · DIVERSIFICATION — how many bets is this really?")
    print("""
  Diversification ratio  DR = (sum of w_i x sigma_i) / sigma_p
    The weighted-average volatility of the pieces, divided by the volatility of the
    whole. DR = 1 means no diversification benefit at all. Higher is better.

  Effective number of bets  ENB = 1 / sum(risk-share_i^2)
    A Herfindahl index applied to RISK shares rather than money shares. Answers
    "how many equally-sized independent positions would feel like this?"

  Effective breadth  BR_eff = N / (1 + (N-1) x rho_bar)      [Buckle, 2004]
    THIS IS THE IMPORTANT ONE. The Fundamental Law counts BREADTH as the number of
    INDEPENDENT decisions. Eight correlated Vietnamese financials are not eight
    independent decisions. This formula discounts N by the average correlation.""")
    wavg_vol = sum(w[i] * sig[i] for i in range(n))
    dr = wavg_vol / sd
    shares = [cctr[i] / sd for i in range(n)]
    enb_risk = 1.0 / sum(s * s for s in shares)
    enb_money = 1.0 / sum(x * x for x in w)
    offdiag = [corr[i][j] for i in range(n) for j in range(n) if i != j]
    rho_bar = sum(offdiag) / len(offdiag)
    br_eff = n / (1 + (n - 1) * rho_bar)

    print(f"\n  Weighted-average name volatility      {wavg_vol * 100:.1f}%")
    print(f"  Portfolio volatility                  {sd * 100:.1f}%")
    print(f"  Diversification ratio                 {dr:.3f}   "
          f"(only {(dr - 1) * 100:.1f}% of vol diversified away)")
    print(f"  Effective bets, by MONEY (HHI)        {enb_money:.2f} of {n}")
    print(f"  Effective bets, by RISK               {enb_risk:.2f} of {n}")
    print(f"  Average pairwise correlation          {rho_bar:.3f}")
    print(f"  EFFECTIVE BREADTH BR_eff              {br_eff:.2f} of {n}")

    # =====================================================================
    hr("3 · THE FUNDAMENTAL LAW OF ACTIVE MANAGEMENT")
    print("""
  Grinold's law, with Clarke's transfer coefficient:

        IR  =  TC  x  IC  x  sqrt(BR)

    IR  information ratio -- active return per unit of active risk. The scoreboard.
    IC  information coefficient -- the correlation between your forecasts and what
        actually happens. A skilled equity manager runs IC ~ 0.05. IC = 0.10 is
        exceptional. IC = 0 is a coin flip.
    BR  breadth -- independent decisions per year.
    TC  transfer coefficient -- how much of your view actually reaches the portfolio,
        after caps, step limits and the no-trade band. TC = 1 means the book expresses
        the view perfectly. Constraints push TC down.

  TC here is computed properly: the correlation between the ACTIVE WEIGHTS you are
  permitted this cycle and the UNCONSTRAINED active weights the model wants.""")
    eq = 1.0 / n
    aw_cycle = [THIS_CYCLE[t] / 100.0 - eq for t in names]
    aw_star = [NORTH_STAR[t] / 100.0 - eq for t in names]
    aw_now = [w[i] - eq for i in range(n)]
    tc_cycle = pearson(aw_cycle, aw_star)
    tc_now = pearson(aw_now, aw_star)

    print(f"\n  TC, book as owned vs north star       {tc_now:+.3f}")
    print(f"  TC, this cycle vs north star          {tc_cycle:+.3f}")
    print("\n  Required IC to hit a given information ratio, at BR_eff "
          f"= {br_eff:.2f} and TC = {tc_cycle:.2f}:")
    print(f"    {'target IR':<14}{'required IC':>13}{'verdict':>34}")
    for target in (0.25, 0.50, 0.75, 1.00):
        ic_req = target / (tc_cycle * math.sqrt(br_eff)) if tc_cycle > 0 else float("nan")
        if ic_req < 0.06:
            v = "plausible for a skilled manager"
        elif ic_req < 0.12:
            v = "exceptional, sustained"
        elif ic_req < 0.25:
            v = "top-decile, implausible to sustain"
        else:
            v = "not achievable"
        print(f"    {target:<14.2f}{ic_req:>13.3f}{v:>34}")
    print(f"\n  For contrast, at the NOMINAL breadth of {n} (ignoring correlation) and TC = 1,")
    print(f"  an IR of 0.50 would need IC = {0.50 / math.sqrt(n):.3f} -- which is why "
          f"ignoring\n  correlation makes active management look far easier than it is.")

    # =====================================================================
    hr("4 · SHARPE, AND THE COST OF THE ACTIVE BET")
    print("""
  Sharpe ratio   SR = (E[r] - rf) / sigma        -- return per unit of TOTAL risk.
  Treynor ratio  T  = (E[r] - rf) / beta         -- return per unit of MARKET risk.
  Jensen's alpha alpha = E[r] - [rf + beta(E[r_b] - rf)]
                                                -- return above what the beta alone earns.
  M-squared      M2 = rf + SR_p x sigma_b        -- the book's return restated at the
                                                   INDEX's risk level, so the two are
                                                   directly comparable in return units.
  Active risk    sigma_A = sqrt(sigma_p^2 + sigma_b^2 - 2 rho_pb sigma_p sigma_b)
                                                -- tracking error vs the index.

  A NOTE ON THE IDENTITY SR_p^2 = SR_b^2 + IR^2, which the curriculum gives and which is
  NOT used here. It holds when the active bets are benchmark-NEUTRAL -- portfolio beta of
  1, with the active return uncorrelated to the index. This book's beta is nowhere near
  1, so the identity does not apply and quoting it would be wrong. That failure is itself
  the finding, and it is why Jensen's alpha is the right measure below: most of this
  book's deviation from the index is not stock selection, it is simply MORE MARKET.

  Correlation to the index is DERIVED, not assumed: an average pairwise correlation of
  rho_bar between holdings implies a common market factor with loading sqrt(rho_bar) on
  each name. That is the internally consistent choice given no measured betas exist.""")
    rho_mkt = math.sqrt(rho_bar)
    beta_names = [rho_mkt * sig[i] / BENCH_VOL for i in range(n)]
    beta_p_mkt = sum(w[i] * beta_names[i] for i in range(n))
    cov_pb = beta_p_mkt * BENCH_VOL ** 2
    rho_pb = cov_pb / (sd * BENCH_VOL)
    te = math.sqrt(max(sd ** 2 + BENCH_VOL ** 2 - 2 * cov_pb, 0.0))

    sr_p = (er - RF_SHORT) / sd
    print(f"\n  Implied correlation of each name to the index   {rho_mkt:.3f}")
    print(f"  Portfolio beta to VN-Index                      {beta_p_mkt:.2f}")
    print(f"  Portfolio / index correlation                   {rho_pb:.3f}")
    print(f"  ACTIVE RISK (tracking error)                    {te * 100:.1f}%")
    print(f"  Sharpe ratio of the book, rf = {RF_SHORT * 100:.2f}%           {sr_p:.3f}")

    treynor = (er - RF_SHORT) / beta_p_mkt
    m2 = RF_SHORT + sr_p * BENCH_VOL
    print(f"  Treynor ratio                                   {treynor:.3f}")
    print(f"  M-squared (book restated at index risk)         {m2 * 100:.2f}%")
    print("\n  The index expected return is not something this repo forecasts, so everything")
    print("  that depends on it is run across a range rather than one guess.")
    print(f"\n    {'index':>7}{'index':>9}{'Jensen':>9}{'active':>9}{'IR':>8}"
          f"{'M2 vs':>9}{'book needs':>12}")
    print(f"    {'E[r]':>7}{'Sharpe':>9}{'alpha':>9}{'return':>9}{'':>8}"
          f"{'index':>9}{'E[r] >':>12}")
    for bench_er in (0.08, 0.10, 0.12, 0.14):
        sr_b = (bench_er - RF_SHORT) / BENCH_VOL
        alpha = er - (RF_SHORT + beta_p_mkt * (bench_er - RF_SHORT))
        active_ret = er - bench_er
        ir = active_ret / te
        need = RF_SHORT + sr_b * sd   # return required to MATCH the index's Sharpe
        print(f"    {bench_er * 100:>6.0f}%{sr_b:>9.3f}{alpha * 100:>+8.1f}%"
              f"{active_ret * 100:>+8.1f}%{ir:>8.2f}{(m2 - bench_er) * 100:>+8.1f}pp"
              f"{need * 100:>11.1f}%")
    print(f"""
  Every column is negative at every assumption, and they are four different ways of
  saying the same thing.

  JENSEN'S ALPHA is the cleanest read. It strips out what the book earns simply for
  carrying a beta of {beta_p_mkt:.2f}, and asks what is left over for the stock selection. The
  answer is negative and it gets MORE negative as the index does better -- which is the
  signature of a portfolio that is levered to the market rather than differentiated
  from it. At a 12% index, holding beta {beta_p_mkt:.2f} alone would earn {RF_SHORT * 100 + beta_p_mkt * (12 - RF_SHORT * 100):.1f}%, against the
  book's forecast {er * 100:.1f}%.

  M-SQUARED restates the book at the index's {BENCH_VOL * 100:.1f}% volatility so the two are
  comparable in plain return units: {m2 * 100:.2f}%. That is what this book would have returned
  if it were dialled down to index risk -- below every index assumption in the table.

  THE INFORMATION RATIO is negative throughout, carrying {te * 100:.0f}% of tracking error to get
  there.

  Stated plainly: on these inputs the active bets are not paying for the risk they add,
  and most of the deviation from the index is leverage to the same market rather than
  independent judgment. That conclusion is only as good as the inputs, and the inputs
  have known defects listed at the foot of this file -- but the gap is far too wide to
  be an input artifact.""")

    # =====================================================================
    hr("5 · VOLATILITY DRAG — arithmetic vs geometric return")
    print("""
  You do not eat the arithmetic mean. You eat the COMPOUNDED return, and volatility
  eats into it:

        g  ~=  mu - sigma^2 / 2            (approximation)
        g  =   exp(ln(1+mu) - sigma_ln^2/2) - 1     (lognormal, exact-ish)

  A portfolio that gains 50% then loses 50% has an arithmetic mean of 0% and has lost
  25% of your money. That gap is the drag, and it grows with the SQUARE of volatility.
  This is why the risk numbers above are not an abstraction.""")
    drag = sd ** 2 / 2
    g_approx = er - drag
    var_ln = math.log(1 + sd ** 2 / (1 + er) ** 2)
    g_exact = math.exp(math.log(1 + er) - var_ln / 2) - 1
    print(f"\n  Arithmetic E[r]                       {er * 100:+.2f}%")
    print(f"  Volatility drag  sigma^2/2            {drag * 100:>6.2f}pp")
    print(f"  Geometric return, approximation       {g_approx * 100:+.2f}%")
    print(f"  Geometric return, lognormal           {g_exact * 100:+.2f}%")
    print(f"  Against a {DEPOSIT * 100:.0f}% deposit                 "
          f"{(g_exact - DEPOSIT) * 100:+.2f}pp")
    print(f"\n  {'':<6}{'E[r]':>9}{'sigma':>8}{'drag':>9}{'geometric':>12}")
    for i in sorted(range(n), key=lambda k: -(mu[k] - sig[k] ** 2 / 2)):
        d = sig[i] ** 2 / 2
        print(f"  {names[i]:<6}{mu[i] * 100:>8.2f}%{sig[i] * 100:>7.1f}%"
              f"{d * 100:>8.2f}pp{(mu[i] - d) * 100:>11.2f}%")

    # =====================================================================
    hr("6 · REVERSE OPTIMIZATION — what you must already believe")
    print("""
  Black-Litterman's first step, run on its own. Instead of turning returns into weights,
  turn WEIGHTS into returns:

        Pi  =  lambda x Sigma x w

  This is the set of expected returns that would make today's weights optimal. It is the
  most direct question you can ask a portfolio: NOT "what do I think?" but "what am I
  ALREADY betting, whether I meant to or not?"

  Then compare Pi to the model's own forecast mu. Where Pi exceeds mu, the position is
  larger than your own stated view supports.

  CALIBRATING lambda MATTERS, and getting it wrong makes this section meaningless. The
  scale of Pi is entirely set by lambda, so lambda must be calibrated against the SAME
  portfolio whose covariance Sigma describes. Use an index-derived lambda against a book
  twice as volatile as the index and Pi comes out at implausible levels.

  So lambda is backed out of the book itself:

        lambda_implied = (E[r_p] - rf) / sigma_p^2

  This is the risk aversion that a person ACTUALLY holding this book is revealing,
  given the book's own forecast return. With it, the weighted average of Pi reproduces
  the book's expected excess return exactly -- which is the internal check that the
  calibration is right.
""")
    lam_implied = (er - RF_SHORT) / sd ** 2
    pi_i = [lam_implied * sw[i] for i in range(n)]
    check = sum(w[i] * pi_i[i] for i in range(n))
    print(f"  lambda implied by holding this book       {lam_implied:.3f}")
    print(f"  lambda in the optimizer config            {LAMBDA:.3f}   "
          f"-- {LAMBDA / lam_implied:.0f}x higher")
    print(f"  check: weighted avg Pi                    {check * 100:.2f}%   "
          f"vs book excess return {(er - RF_SHORT) * 100:.2f}%")
    print(f"""
  THAT GAP IS ITSELF A FINDING. The optimizer is configured to be about {LAMBDA / lam_implied:.0f} times more
  risk-averse than the behaviour of actually holding this book implies. Both cannot be
  right. Either the weights are far too aggressive for the stated risk appetite, or
  lambda = {LAMBDA:.0f} is not the risk appetite. A human should settle which.
""")
    print(f"  {'':<6}{'weight':>8}{'implied Pi':>12}{'+ rf':>9}{'forecast':>10}"
          f"{'gap':>10}   {'read':<32}")
    print(f"  {'':<6}{'':>8}{'excess':>12}{'':>9}{'mu':>10}{'':>10}")
    for i in sorted(range(n), key=lambda k: -(pi_i[k] + RF_SHORT - mu[k])):
        implied_total = pi_i[i] + RF_SHORT
        gap = implied_total - mu[i]
        if gap > 0.05:
            rd = "position exceeds the view"
        elif gap > 0.01:
            rd = "position slightly ahead of view"
        elif gap > -0.03:
            rd = "position matches the view"
        else:
            rd = "view exceeds the position"
        print(f"  {names[i]:<6}{w[i] * 100:>7.1f}%{pi_i[i] * 100:>11.1f}%"
              f"{implied_total * 100:>8.1f}%{mu[i] * 100:>9.2f}%{gap * 100:>+8.1f}pp   {rd:<32}")
    print("""
  The ordering is the point, and it is the same ordering the safety-first ratios found
  by a different route: the names where the position most exceeds the view are the ones
  the engine wants trimmed, and the names where the view exceeds the position are the
  ones it wants added. Two unrelated pieces of Level III machinery, same answer.""")

    # =====================================================================
    hr("7 · DOWNSIDE MEASURES — VaR and expected shortfall")
    print("""
  Value at Risk  VaR(alpha)   the loss you exceed alpha% of the time.
  Expected shortfall / CVaR    the AVERAGE loss GIVEN you are in that tail.

  VaR tells you where the door is. Expected shortfall tells you what is behind it, and
  it is the measure Level III prefers precisely because VaR is silent about tail depth.
  Both are taken from the 200,000-trial scenario resample in risk.py, which correlates
  which branch each name lands on -- so names go bear together as often as the
  correlation model says they should.""")
    sims = risk.simulate(w, names, corr, shrink=True)
    print(f"\n  {'confidence':<14}{'VaR':>10}{'expected shortfall':>22}{'gap':>10}")
    for a_ in (0.10, 0.05, 0.01):
        var = risk.q(sims, a_)
        tail = [x for x in sims if x <= var]
        es = sum(tail) / len(tail)
        print(f"  {(1 - a_) * 100:>4.0f}%{'':<9}{var * 100:>9.1f}%{es * 100:>21.1f}%"
              f"{(var - es) * 100:>9.1f}pp")
    print("\n  Level III also asks for the UPSIDE symmetry check:")
    print(f"    median outcome        {risk.q(sims, 0.50) * 100:+.1f}%")
    print(f"    90th percentile       {risk.q(sims, 0.90) * 100:+.1f}%")
    print(f"    10th percentile       {risk.q(sims, 0.10) * 100:+.1f}%")

    # =====================================================================
    hr("8 · TAX-AWARE RETURN — and a live regime risk")
    print("""
  Level III insists returns be measured after tax, because tax is the largest
  controllable drag most investors face.

  Vietnam today, for a resident individual:
    disposal of listed securities   0.1% of PROCEEDS -- not of gains
    dividends                       5%

  A proceeds-based tax is unusual and it has a specific consequence: rebalancing is
  almost free, and it is EQUALLY cheap whether you are selling a winner or a loser.
  There is no tax reason to hold a losing position, and no lock-in on a winning one.

  DRAFT REGIME CHANGE, NOT YET LAW. The Ministry of Finance has proposed taxing 20% of
  actual annual GAINS instead. The PIT Law 2025 took effect 01-Jul-2026 and the decree
  is still being finalised. This matters to this book in an unusual direction -- see
  below.""")
    proposed_turnover = sum(abs(THIS_CYCLE[t] / 100.0 - w[names.index(t)])
                            for t in names) / 2
    print(f"\n  Proposed one-way turnover this cycle           {proposed_turnover * 100:.1f}% of the book")
    print(f"  Transaction cost at {TURNOVER_COST * 100:.1f}% round trip           "
          f"{proposed_turnover * 2 * TURNOVER_COST * 100:.2f}% of the book")
    print(f"  Securities PIT at {TAX_PROCEEDS * 100:.1f}% of proceeds          "
          f"{proposed_turnover * TAX_PROCEEDS * 100:.3f}% of the book")
    print(f"  Combined drag on the rebalance                {(proposed_turnover * 2 * TURNOVER_COST + proposed_turnover * TAX_PROCEEDS) * 100:.2f}%")
    print(f"  Expected utility gain from the rebalance      +2.3% (decide.py)")
    print("""
  So the trade clears its own costs by a wide margin under today's rules.

  UNDER THE DRAFT 20%-ON-GAINS REGIME, the arithmetic inverts in this book's favour, for
  an uncomfortable reason: EVERY position is currently at a loss. A gains-based tax makes
  realised losses valuable if they can offset gains. The proposed TCB and KDH trims would
  crystallise the two largest losses in the book. That is a genuine tax asset under the
  draft rules and worth exactly nothing under today's rules.

  DO NOT ACT ON THIS. The decree is not law, loss-offset treatment is not specified in
  what has been published, and 'sell because of a tax rule that does not exist yet' is
  how people lock in losses for nothing. It is recorded because the timing question --
  rebalance before or after the decree -- is a real one a human should hold in view.""")

    # =====================================================================
    hr("9 · REBALANCING POLICY — how wide should the corridors be?")
    print("""
  Level III gives the drivers of optimal corridor width around a target weight, from
  Masters' framework. Wider corridor means you tolerate more drift before trading.

    HIGHER transaction cost      -> WIDER corridor  (trading hurts, so trade less)
    HIGHER risk tolerance        -> WIDER corridor  (drift matters less to you)
    HIGHER asset volatility      -> NARROWER        (it runs away from target faster)
    HIGHER correlation with the
      rest of the book           -> WIDER           (drift does less to total risk)

  Applied here, using each name's own volatility and its beta to the portfolio:""")
    print(f"\n  {'':<6}{'target':>9}{'sigma':>8}{'beta to pf':>12}{'suggested band':>17}{'current':>10}{'status':>12}")
    for i in sorted(range(n), key=lambda k: -sig[k]):
        tgt = THIS_CYCLE[names[i]]
        # Base band scaled by the ratio of portfolio vol to name vol, and widened by
        # correlation with the book. Anchored on the configured 3pp no-trade band.
        band = O["no_trade_band_pct"] * (sd / sig[i]) * (0.5 + 0.5 * beta_p[i])
        band = max(1.5, min(6.0, band))
        drift = w[i] * 100 - tgt
        status = "TRADE" if abs(drift) > band else "inside band"
        print(f"  {names[i]:<6}{tgt:>8.1f}%{sig[i] * 100:>7.1f}%{beta_p[i]:>12.2f}"
              f"{'+/- %.1fpp' % band:>17}{w[i] * 100:>9.1f}%{status:>12}")
    print(f"""
  Compare that to the flat +/- {O["no_trade_band_pct"]:.0f}pp no-trade band the optimizer uses today. The band
  should NARROW as volatility rises, because a volatile position runs away from its
  target faster and needs catching sooner. A flat band cannot do that. It is uniformly
  too wide here, and it is MOST too wide exactly where it matters most -- on KDH at
  {sig[names.index('KDH')] * 100:.0f}% volatility, which on these drivers warrants about +/- 2.0pp.

  In plain terms: today's rule lets the most volatile position in the book drift the
  furthest before anyone has to look at it. That is backwards.""")

    # =====================================================================
    hr("10 · CERTAINTY EQUIVALENT — what this book is worth to you")
    print("""
  U = E[r] - 0.5 x lambda x sigma^2

  The certain return you would accept INSTEAD of this portfolio. It is the quantity
  decide.py maximises, and it is worth seeing in units you can feel.""")
    for lam, lbl in ((LAMBDA, "optimizer config"), (2.0, "typical textbook"),
                     (lam_implied, "implied by holding it")):
        u = er - 0.5 * lam * sd ** 2
        print(f"  lambda = {lam:>5.2f}  ({lbl:<22})  certainty equivalent "
              f"{u * 100:>+7.2f}%   vs deposit {(u - DEPOSIT) * 100:>+7.2f}pp")
    print(f"""
  At the configured lambda of {LAMBDA:.1f} the certainty equivalent is {er * 100 - 0.5 * LAMBDA * sd ** 2 * 100:.1f}% -- meaning a
  person that risk-averse would rather hold cash and would pay a lot to swap out of this
  book. That is not a verdict on the holdings. It is a statement that lambda = {LAMBDA:.0f} and 30%
  volatility are an incoherent pair, and they were chosen separately.

  The three rows bracket the problem. Only at the lambda implied by ACTUALLY holding the
  book ({lam_implied:.2f}) does the certainty equivalent come out near the expected return, and that
  lambda is barely risk-averse at all. Somewhere between {lam_implied:.2f} and {LAMBDA:.1f} is the real answer,
  and which one it is changes the optimizer's output materially -- because lambda
  multiplies sigma SQUARED, and sigma is 30%.""")

    print("""
==============================================================================
WHAT THIS INHERITS -- read before using any number above
==============================================================================
  Every figure is computed off assumptions.json and carries the same defects
  listed at the end of risk.py: undated prices presumed 24-Jul, VPB's two
  contradictory credit fields, cash_yield populated for one name of eight,
  no driver model for MBB or VCI, and a sigma that blends scenario dispersion
  with a flat assumed 28%% base vol because no realised covariance exists.

  Three things are specific to THIS file and should be read as assumptions,
  not measurements:

  - VN-Index volatility of %.1f%% is annualised from a 90-day realised daily
    vol of %.2f%% (29-Apr to 28-Jul 2026). A calm 90-day window understates
    long-run index volatility, which makes the book look WORSE against the
    index than a full-cycle comparison would. The direction of that bias is
    known; its size is not.
  - No measured betas exist. Each name's correlation to the index is DERIVED
    as sqrt(average pairwise correlation) = %.2f. That is internally
    consistent with the block model but it is not an observation.
  - Breadth is discounted by the Buckle formula using the block model's own
    correlations. If the true correlations are higher -- and for a book that
    is 51%% banks and 19.5%% brokers on a look-through basis, they plausibly
    are -- effective breadth is LOWER than %.2f and every skill requirement
    in section 3 is HARDER than shown.

  Nothing here changes a weight, a branch, a probability or a confidence.
  The system recommends; a human signs.
==============================================================================""" % (
        BENCH_VOL * 100, BENCH_DAILY_VOL * 100, rho_mkt, br_eff))


if __name__ == "__main__":
    main()
