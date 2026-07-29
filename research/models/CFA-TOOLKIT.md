# CFA Level III analytics, applied to this book

**Built 2026-07-29. `python3 research/models/cfa.py`.**

Ten pieces of Level III machinery, run against the actual holdings. Each section below
gives the formula, what it means in plain words, and what it says here.

**Nothing in this file changes a weight, a branch, a probability or a confidence.** It is
diagnostic. `decide.py` and `run.py` do not read it. The system recommends; a human signs.

**What it is measured against.** Sourced 2026-07-29, not invented:

| Input | Value | Source |
|---|---:|---|
| Vietnam 2Y government bond | 3.56% | press, Jul-2026 (T5) |
| Vietnam 10Y government bond | 4.52% | press, 09-Jul-2026, a 33-month high (T5) |
| 12-month bank deposit | ~6.0% | the threshold `risk.py` already uses |
| VN-Index volatility | 15.7% | annualised from 0.99% realised daily vol, 29-Apr to 28-Jul (T5) |
| Securities disposal tax | 0.1% of **proceeds** | current law |
| Dividend tax | 5% | current law |

Note the oddity in the first three rows: **a bank deposit pays more than a 10-year
government bond.** So the 6% hurdle in `risk.py` is harsher than the true risk-free rate,
and deliberately so.

---

## Where each of these sits in the CFA curriculum

**A note on the structure.** From 2025 the Level III exam is a **common core** plus one of three
**pathways** — Portfolio Management, Private Markets, Private Wealth. The core is Asset Allocation,
Portfolio Construction, Performance Measurement, Derivatives & Risk Management, and Ethics. Most of
what follows is core; two items sit in a pathway, and those are marked.

Reading titles are given in the classic form as well, because those are what search engines and
older study material use, and the underlying content has largely carried over.

| § | What was computed | Level III module | Reading / topic |
|---|---|---|---|
| 1 | MCTR, CCTR, risk contribution | **Portfolio Construction** *(core)* | *Active Equity Investing: Portfolio Construction* — risk budgeting; absolute vs relative risk attribution |
| 2 | Diversification ratio, effective number of bets | **Portfolio Construction** *(core)* · **Asset Allocation** | *Principles of Asset Allocation* — risk budgeting |
| 2 | **Effective breadth**, BR_eff = N ÷ [1+(N−1)ρ̄] | **Portfolio Construction** *(core)* | *Active Equity Investing: Portfolio Construction* — the breadth discussion inside the Fundamental Law |
| 3 | **Fundamental Law**, IR = TC × IC × √BR | **Portfolio Construction** *(core)* | *Active Equity Investing: Portfolio Construction* — Grinold's law, Clarke's transfer coefficient |
| 4 | Sharpe, Treynor, Jensen's α, M², IR, tracking error | **Performance Measurement** *(core)* | *Portfolio Performance Evaluation* and *Investment Manager Selection* — the appraisal ratios |
| 4 | SR_p² = SR_b² + IR², optimal active risk | **Portfolio Construction** *(core)* | *Active Equity Investing: Portfolio Construction* — relationship of IR to the Sharpe ratio |
| 5 | Volatility drag, arithmetic vs geometric | **Asset Allocation** *(core)* | *Capital Market Expectations* / *Overview of Asset Allocation* — compounding over multiple periods. Origin is Level I Quantitative Methods |
| 6 | **Reverse optimization, Π = λΣw** | **Asset Allocation** *(core)* | **Principles of Asset Allocation** — reverse optimization and Black–Litterman |
| 7 | VaR, expected shortfall / CVaR | **Derivatives & Risk Management** *(core)* | *Measuring and Managing Market Risk* — parametric, historical and Monte Carlo VaR; CVaR |
| 8 | After-tax return; the 20%-on-gains regime | **Private Wealth pathway** · also **Asset Allocation** | *Taxes and Private Wealth Management in a Global Context*; *Asset Allocation with Real-World Constraints* |
| 9 | Rebalancing corridor width | **Asset Allocation** *(core)* | *Asset Allocation with Real-World Constraints* — rebalancing policy, Masters' corridor drivers |
| 10 | Certainty equivalent, U = E[r] − ½λσ² | **Asset Allocation** *(core)* | *Principles of Asset Allocation* — mean–variance optimization and the utility function |

### Already in the repo before this file, and where they sit

| What | Where it lives here | Level III module | Reading / topic |
|---|---|---|---|
| **Roy's safety-first ratio**, shortfall probability | `risk.py` | **Asset Allocation** *(core)* | *Principles of Asset Allocation* — shortfall risk and goals-based allocation. Origin is Level I Quant (*Common Probability Distributions*) |
| Sortino ratio, downside deviation | `risk.py` | **Performance Measurement** *(core)* | *Portfolio Performance Evaluation* — downside risk-adjusted measures |
| Monte Carlo simulation, Gaussian copula | `risk.py` | **Asset Allocation** · **Derivatives & Risk Management** | *Principles of Asset Allocation* — Monte Carlo in allocation; *Measuring and Managing Market Risk* — simulation VaR |
| Mean–variance optimizer, λ, the utility objective | `decide.py` | **Asset Allocation** *(core)* | *Principles of Asset Allocation* — MVO |
| 20% single-name and 35% cluster caps | `assumptions.json` | **Asset Allocation** *(core)* | *Asset Allocation with Real-World Constraints* — constraints and their cost |
| Scenario probabilities, confidence weights | `assumptions.json` | **Asset Allocation** *(core)* | *Capital Market Expectations* — forecasting and its biases |
| Correlation block model | `assumptions.json` | **Asset Allocation** *(core)* | *Capital Market Expectations* — estimating the covariance structure |
| Calibration log, scored forecasts | `calibration-log.md` | **Behavioral Finance** · **Performance Measurement** | *The Behavioral Biases of Individuals* — overconfidence and hindsight bias; *Investment Manager Selection* |
| Kill criteria, the charter, no-trade band | `AGENT-CHARTER.md` | **Asset Allocation** *(core)* | *Overview of Asset Allocation* — the investment policy statement and governance |

**The three densest modules for this book**, if the point is to know where to read:

1. **Principles of Asset Allocation** — reverse optimization, Black–Litterman, mean–variance,
   the utility function, Monte Carlo, shortfall risk. Sections 2, 5, 6, 7 and 10 above.
2. **Active Equity Investing: Portfolio Construction** — the Fundamental Law, transfer
   coefficient, breadth, risk budgeting. Sections 1, 2, 3 and part of 4. **This is the module that
   produced the most uncomfortable result here.**
3. **Asset Allocation with Real-World Constraints** — rebalancing corridors, taxes, constraints.
   Sections 8 and 9.

**One caveat on precision.** CFA restructured Level III in 2025 and module boundaries moved; the
mapping above reflects that structure, but if you are working from a specific year's curriculum,
confirm the module a reading now sits under. The *readings* and the *formulas* have been stable —
it is the packaging that changed.

---

## 1 · Risk budgeting — where the risk actually sits

> MCTR_i = (Σw)_i ÷ σ_p   ·   CCTR_i = w_i × MCTR_i   ·   Σ CCTR = σ_p

**What it means.** A weight tells you where the money is, not where the risk is. A
volatile name correlated with everything else contributes more risk than its size
suggests. The contributions sum exactly to portfolio volatility, so "share of risk" is a
real decomposition rather than an analogy.

| | Weight | Share of risk | Risk ÷ money | Beta to own book |
|---|---:|---:|---:|---:|
| TCB | 35.0% | 33.3% | 0.95 | 0.95 |
| **KDH** | **20.3%** | **28.2%** | **1.39** | **1.39** |
| HPG | 16.8% | 11.7% | 0.70 | 0.70 |
| VPB | 10.0% | 9.0% | 0.90 | 0.90 |
| TCX | 5.5% | 6.0% | 1.09 | 1.09 |
| MBB | 6.5% | 5.8% | 0.89 | 0.89 |
| VPX | 2.8% | 3.1% | 1.12 | 1.12 |
| VCI | 3.1% | 2.9% | 0.92 | 0.92 |

**KDH is the finding.** It is the third-largest position by money and the second-largest
by risk — it carries **39% more risk than its weight implies**. HPG is the mirror image at
0.70: a 16.8% position doing 11.7% of the damage.

This is a new argument for the KDH trim, and it is independent of KDH's expected return.
Even if the earnings case were fine, the position is oversized *in risk terms*.

## 2 · Diversification — how many bets is this really?

> DR = Σ(w_i σ_i) ÷ σ_p   ·   ENB = 1 ÷ Σ(risk share)²   ·   **BR_eff = N ÷ [1 + (N−1)ρ̄]**

**What it means.** The diversification ratio compares the average volatility of the pieces
to the volatility of the whole. Effective number of bets applies a concentration index to
*risk* shares. **Effective breadth** is the important one: it discounts the number of
holdings by how correlated they are, because correlated positions are not separate
decisions.

| | |
|---|---:|
| Weighted-average name volatility | 39.2% |
| Portfolio volatility | 30.5% |
| Diversification ratio | 1.284 — only 28% of volatility diversified away |
| Effective bets, by money | 4.74 of 8 |
| Effective bets, by risk | 4.52 of 8 |
| Average pairwise correlation | 0.529 |
| **Effective breadth** | **1.70 of 8** |

**Eight holdings are functionally about 1.7 independent bets.** That is the single most
consequential number in this file, and section 3 is what it costs.

## 3 · The Fundamental Law of Active Management

> **IR = TC × IC × √BR**

**What it means.**
- **IR**, information ratio — active return per unit of active risk. The scoreboard.
- **IC**, information coefficient — the correlation between your forecasts and reality. A
  skilled equity manager runs about 0.05. 0.10 is exceptional. 0 is a coin flip.
- **BR**, breadth — independent decisions per year.
- **TC**, transfer coefficient — how much of your view survives caps, step limits and the
  no-trade band before reaching the portfolio. 1.0 is perfect expression.

**TC is computed, not assumed:** the correlation between the active weights permitted this
cycle and the unconstrained active weights the model wants.

| | |
|---|---:|
| TC, book as owned vs north star | **+0.157** |
| TC, this cycle vs north star | +0.617 |

The first number is the interesting one. **The book as currently held expresses almost none
of the model's view** — a transfer coefficient of 0.16 means the weights and the forecasts
are nearly unrelated. That is what a portfolio looks like when positions accumulated before
the analysis existed.

**Required IC**, at BR_eff = 1.70 and TC = 0.62:

| Target IR | Required IC | Verdict |
|---:|---:|---|
| 0.25 | 0.310 | not achievable |
| 0.50 | 0.621 | not achievable |
| 0.75 | 0.931 | not achievable |
| 1.00 | 1.242 | not achievable (IC is a correlation; it cannot exceed 1) |

**Read this correctly.** It is not "you have no skill". It says the *structure* forbids the
payoff: with 1.7 effective bets, no achievable level of forecasting skill produces even a
modest information ratio. **The binding constraint is concentration, not skill** — and the
fix is more independent positions, not better research on these eight.

For contrast, at the naive breadth of 8 with perfect transfer, an IR of 0.50 would need
IC = 0.177. Ignoring correlation makes active management look roughly twice as easy as it is.

## 4 · Sharpe, Treynor, Jensen, M² — is the active bet paying?

> SR = (E[r] − rf) ÷ σ · T = (E[r] − rf) ÷ β · α = E[r] − [rf + β(E[r_b] − rf)] · M² = rf + SR_p × σ_b

**What they mean.** Sharpe is return per unit of *total* risk; Treynor per unit of *market*
risk; **Jensen's alpha** is what is left after subtracting what the beta alone would have
earned; **M²** restates the book at the index's risk level so the two are comparable in
plain return units.

| | |
|---|---:|
| Portfolio beta to VN-Index | **1.81** |
| Portfolio / index correlation | 0.934 |
| Active risk (tracking error) | 16.8% |
| Sharpe ratio | 0.108 |
| Treynor ratio | 0.018 |
| **M² — the book at index risk** | **5.26%** |

| Index E[r] | Index Sharpe | Jensen's α | Active return | IR | M² vs index |
|---:|---:|---:|---:|---:|---:|
| 8% | 0.283 | −4.8% | −1.1% | −0.07 | −2.7pp |
| 10% | 0.410 | −8.4% | −3.1% | −0.19 | −4.7pp |
| 12% | 0.537 | −12.0% | −5.1% | −0.31 | −6.7pp |
| 14% | 0.664 | −15.6% | −7.1% | −0.43 | −8.7pp |

**A beta of 1.81 is the finding.** The correlation to the index is 0.93 — so this is not
really a stock-picking portfolio that happens to be volatile. **It is a levered bet on the
same market**, and Jensen's alpha gets *more* negative as the index does better, which is
the signature of exactly that.

**On the identity SR_p² = SR_b² + IR², which the curriculum gives and which is deliberately
NOT used here.** It holds only when active bets are benchmark-neutral — beta of 1, active
return uncorrelated with the index. This book's beta is 1.81, so the identity does not
apply, and quoting it would be wrong. Its failure *is* the finding.

## 5 · Volatility drag — arithmetic vs geometric return

> g ≈ μ − σ²/2

**What it means.** You do not eat the average return, you eat the compounded one. Gain 50%
then lose 50% and the arithmetic mean is 0% while a quarter of your money is gone. The gap
grows with the **square** of volatility.

| | |
|---|---:|
| Arithmetic E[r] | +6.85% |
| Volatility drag σ²/2 | −4.65pp |
| **Geometric return (lognormal)** | **+2.75%** |
| Against a 6% deposit | **−3.25pp** |

| | E[r] | σ | Drag | Geometric |
|---|---:|---:|---:|---:|
| TCX | 18.48% | 42.7% | 9.11pp | +9.37% |
| HPG | 10.60% | 31.6% | 4.99pp | +5.61% |
| MBB | 8.78% | 36.4% | 6.61pp | +2.17% |
| VPX | 14.95% | 50.7% | 12.86pp | +2.09% |
| TCB | 3.42% | 33.6% | 5.63pp | **−2.21%** |
| VPB | 0.99% | 35.5% | 6.30pp | **−5.32%** |
| VCI | 4.30% | 44.4% | 9.87pp | **−5.57%** |
| KDH | 8.06% | 54.5% | 14.84pp | **−6.78%** |

**This is the harshest table in the repo.** Four of eight holdings — 68.4% of the book —
have a **negative expected compounded return**. KDH has a positive expected return of +8.1%
and a geometric return of −6.8%, entirely because of its 54.5% volatility. Volatility is
not a discomfort to be tolerated here; it is eating the return.

## 6 · Reverse optimization — what you must already believe

> **Π = λ Σ w**

**What it means.** Black–Litterman's first step, run alone. Instead of turning returns into
weights, turn weights into returns. Π is the set of expected returns that would make
today's weights optimal — so the question is not "what do I think?" but **"what am I
already betting, whether I meant to or not?"**

**Calibrating λ is what makes this section meaningful or meaningless.** Π scales entirely
with λ, so λ must be calibrated on the *same* portfolio the covariance describes. Here it
is backed out of the book itself: λ_implied = (E[r_p] − rf) ÷ σ_p².

| | |
|---|---:|
| λ implied by holding this book | **0.354** |
| λ in the optimizer config | **6.000** — 17× higher |
| Check: weighted-average Π | 3.29% vs book excess return 3.29% ✓ |

**That 17× gap is itself a finding.** The optimizer is configured to be seventeen times more
risk-averse than the act of holding this book implies. Both cannot be right.

| | Weight | Implied Π (+rf) | Forecast μ | Gap |
|---|---:|---:|---:|---:|
| **VPB** | 10.0% | 6.5% | 0.99% | **+5.5pp** — position exceeds the view |
| **TCB** | 35.0% | 6.7% | 3.42% | +3.3pp |
| VCI | 3.1% | 6.6% | 4.30% | +2.3pp |
| KDH | 20.3% | 8.1% | 8.06% | +0.1pp |
| MBB | 6.5% | 6.5% | 8.78% | −2.3pp |
| HPG | 16.8% | 5.9% | 10.60% | −4.7pp |
| VPX | 2.8% | 7.3% | 14.95% | −7.7pp |
| **TCX** | 5.5% | 7.1% | 18.48% | **−11.3pp** — view exceeds the position |

**This ordering is the exact inverse of the safety-first ranking in `risk.py`.** Two
unrelated pieces of machinery, run off different formulas, produce the same answer: trim
VPB, TCB and VCI; add TCX, VPX, HPG.

## 7 · Value at Risk and expected shortfall

> VaR(α) = the loss exceeded α% of the time · ES/CVaR = the *average* loss given you are there

**What it means.** VaR tells you where the door is. Expected shortfall tells you what is
behind it. Level III prefers ES precisely because VaR is silent about tail depth. Both come
from the 200,000-trial correlated resample in `risk.py`.

| Confidence | VaR | Expected shortfall | Gap |
|---:|---:|---:|---:|
| 90% | −25.4% | −36.9% | 11.5pp |
| 95% | −34.2% | −44.3% | 10.1pp |
| 99% | −50.6% | −59.0% | 8.3pp |

Symmetry check: median +6.7%, 90th percentile +39.4%, 10th percentile −25.4%.

## 8 · Tax-aware return, and a live regime risk

**Today.** Disposal of listed securities is taxed at **0.1% of proceeds — not of gains**.
Dividends at 5%. A proceeds-based tax has a specific consequence: **rebalancing is nearly
free, and equally cheap whether you sell a winner or a loser.** There is no tax lock-in and
no tax reason to hold a loser.

| | |
|---|---:|
| Proposed one-way turnover this cycle | 21.3% of the book |
| Transaction cost at 0.5% round trip | 0.21% |
| Securities PIT at 0.1% of proceeds | 0.021% |
| **Combined drag** | **0.23%** |
| Utility gain from the rebalance (`decide.py`) | +2.3% |

The trade clears its own costs roughly tenfold under today's rules.

**The draft change.** The Ministry of Finance has proposed taxing **20% of actual annual
gains** instead. The PIT Law 2025 took effect 01-Jul-2026; the decree is still being
finalised and drew strong negative reaction.

Under a gains-based regime the arithmetic inverts in this book's favour, for an
uncomfortable reason: **every position is currently at a loss.** Realised losses become
valuable if they offset gains, and the proposed TCB and KDH trims would crystallise the two
largest losses in the book.

**Do not act on this.** The decree is not law, loss-offset treatment is not specified in
what has been published, and selling because of a tax rule that does not yet exist is how
people realise losses for nothing. It is recorded because the *timing* question —
rebalance before or after the decree — is real and belongs to a human.

## 9 · Rebalancing corridors

**What it means.** Level III gives the drivers of optimal corridor width around a target:
higher transaction cost → wider; higher risk tolerance → wider; **higher volatility →
narrower** (it drifts away faster); higher correlation with the rest of the book → wider.

| | Target | σ | Beta to book | Suggested band |
|---|---:|---:|---:|---:|
| KDH | 15.6% | 54.5% | 1.39 | ±2.0pp |
| VPX | 1.2% | 50.7% | 1.12 | ±1.9pp |
| VCI | 5.0% | 44.4% | 0.92 | ±2.0pp |
| TCX | 11.0% | 42.7% | 1.09 | ±2.2pp |
| MBB | 12.0% | 36.4% | 0.89 | ±2.4pp |
| VPB | 15.3% | 35.5% | 0.90 | ±2.4pp |
| HPG | 20.0% | 31.6% | 0.70 | ±2.5pp |
| TCB | 20.0% | 33.6% | 0.95 | ±2.7pp |

**Against the flat ±3pp band the optimizer uses today:** a single band cannot narrow as
volatility rises. It is uniformly too wide here, and most too wide exactly where it matters
— **today's rule lets the most volatile position in the book drift the furthest before
anyone has to look at it.**

## 10 · Certainty equivalent

> U = E[r] − ½ λ σ²

**What it means.** The guaranteed return you would swap this portfolio for. It is the
quantity `decide.py` maximises.

| λ | | Certainty equivalent | vs deposit |
|---:|---|---:|---:|
| 6.00 | optimizer config | **−21.06%** | −27.06pp |
| 2.00 | typical textbook | −2.45% | −8.45pp |
| 0.35 | implied by holding it | +5.21% | −0.79pp |

At λ = 6 the certainty equivalent is −21%, meaning someone that risk-averse would pay
heavily to swap into cash. **That is not a verdict on the holdings — it says λ = 6 and 30%
volatility are an incoherent pair, chosen separately.** Because λ multiplies σ *squared*,
which value is right changes the optimizer's output materially.

---

## What a human is being asked to decide

Nothing here is a trade. Five items, none of which an automated run may touch:

1. **Settle λ.** It sits somewhere between 0.35 and 6.0 and the optimizer's weights depend
   on the choice. (Charter §4: optimizer config is human-only.)
2. **Replace the flat ±3pp no-trade band** with volatility-scaled corridors.
3. **Decide whether concentration or forecasting is the thing to fix.** Section 3 says the
   structure, not the research, is what caps the achievable information ratio. Adding
   genuinely uncorrelated positions would do more than improving any of the eight dossiers.
4. **Note the beta.** At 1.81 with 0.93 correlation to the index, most of this book's
   deviation from the market is leverage, not selection. If that is intended, it should be
   written down as intended.
5. **Hold the tax-timing question in view** without acting on it.

---

## What this inherits

Every figure is computed off `assumptions.json` and carries the defects listed at the foot
of `risk.py`: undated prices presumed 24-Jul, VPB's contradictory credit pair, `cash_yield`
populated for one name of eight, no driver model for MBB or VCI, and a σ that blends
scenario dispersion with a flat assumed 28% base vol because no realised covariance exists.

Three limitations are specific to this file:

- **VN-Index volatility of 15.7%** is annualised from a 90-day window. A calm window
  understates long-run index volatility, which makes the book look **worse** against the
  index than a full-cycle comparison would. The direction of that bias is known; its size
  is not.
- **No measured betas exist.** Each name's correlation to the index is *derived* as
  √(average pairwise correlation) = 0.73 — internally consistent with the block model, but
  not an observation.
- **Effective breadth uses return correlations** as a proxy for signal correlations. For a
  book that is 51% banks and 19.5% brokers on a look-through basis, true correlations are
  plausibly higher — in which case breadth is **lower** than 1.70 and every skill
  requirement in section 3 is **harder** than shown.
