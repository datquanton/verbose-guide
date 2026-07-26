# HPG — the spread bridge

**Depth-queue item 5 · 2026-07-26**

The model has been *asserting* HPG's core NPAT per tonne (bear ₫1.25m / base ₫1.60m /
bull ₫1.85m) rather than deriving it. On a 16.8% position whose only real variable is
spread, an asserted number is a guess wearing a scenario label. This reconstructs it from
input prices.

---

## 1 · Method

Blast-furnace/BOF route, per tonne of crude steel:

| Item | Assumption | Basis |
|---|---|---|
| Iron ore | 1.60 t/t | standard integrated consumption |
| Coking coal | 0.65 t/t | via ~0.45t coke at ~1.35t coal/t coke |
| Conversion | **US$114/t** | **calibrated, not assumed** — see below |
| D&A | US$49/t | ~₫15tn/yr over ~12mt |
| SG&A | US$15/t | estimate |
| Interest | US$17/t | ₫1,359bn/quarter → ₫5.4tn/yr over ~12mt |
| Tax | 20% | statutory |
| FX | 26,300 | VND/USD market rate |

**Conversion cost is solved, not guessed.** Rather than assert a number, it is calibrated
so the bridge reproduces the *known* Q1/26 actual of ₫1.68m/t at Q1 input prices (ore
US$101, coking coal US$190, HRC ~US$560). That yields US$114/t and anchors everything
downstream to a real observation.

## 2 · The sensitivity grid

NPAT per tonne, ₫m. Rows = iron ore US$/t, columns = realised HRC US$/t, coking coal held
at US$220/t (the raised 2026 forecast).

| ore \ HRC | 500 | 520 | **539** | 560 | 580 |
|---|---|---|---|---|---|
| 100 | 0.04 | 0.46 | 0.86 | 1.30 | 1.72 |
| 105 | −0.13 | 0.29 | 0.69 | 1.14 | 1.56 |
| 110 | −0.30 | 0.13 | 0.52 | 0.97 | 1.39 |
| **115** | −0.46 | −0.04 | **0.36** | 0.80 | 1.22 |
| 120 | −0.63 | −0.21 | 0.19 | 0.63 | 1.05 |

**Gearing** — this is the point of the whole exercise:

- Each **US$20/t of HRC** = **₫0.42m/t** of NPAT
- Each **US$10/t of iron ore** = **₫0.34m/t**
- Each **US$10/t of coking coal** = **₫0.14m/t**

At current inputs the all-in pre-tax cost is **US$522/t** against an HRC price of ~US$539.
A **US$17/t pre-tax margin** on a US$539 product — roughly 3%. Steel is a spread business
and the spread is currently paper-thin.

## 3 · The finding: the bear case is not bearish

Solving for the HRC price each scenario *requires*, at current input costs:

| Scenario | NPAT/t | HRC required | vs US$539 spot |
|---|---|---|---|
| bear | ₫1.25m | US$581/t | **+7.9%** |
| base | ₫1.60m | US$598/t | +11.0% |
| bull | ₫1.85m | US$610/t | +13.2% |

**Every scenario in the model — including the bear case — implicitly assumes HRC prices
recover from where they are now.** The bear case needs an 8% price rise. There is no
branch in the model that describes the world as it currently is.

That is a real gap, and it is the opposite of the error I would have expected to find.

## 4 · The timing point that changes how to read Thursday's print

**HPG buys ore and coking coal one to two quarters forward and carries inventory.** Q2's
P&L therefore reflects Q1/early-Q2 input prices — the cheap ones — and the late-July
squeeze (Formosa's US$40/t HRC cut, ore at US$115, coal forecast to US$220) lands in
**Q3, not Q2**.

**So a strong Q2 print on ~28 July does not refute the bear thesis, and must not be read
as doing so.** The Q2 number is a report on a spread environment that no longer exists.
The Q3 print is the one that tests this.

This is the single most useful conclusion here, and it is a warning about a
misinterpretation that was about to become very easy to make.

## 5 · Honest limits

The output is a **gearing map, not a forecast**. Do not read ₫0.36m/t as a prediction:

- Product mix is ignored — HPG sells rebar as well as HRC, with different economics
- Single-point calibration to one quarter absorbs every unmodelled error into `conv`
- D&A, SG&A and interest per tonne are approximations from group-level figures
- US$220/t coking coal is a **2026 forecast**, not current spot
- The inventory lag in §4 means spot prices never map to the current quarter's P&L

What survives all of those caveats is the **gearing** and the **§3 finding**, because both
are ratios and differences rather than levels.

## 6 · Recommended model change — for a human, not an automated run

Add a fourth branch, `spot_persists`: HRC US$539, ore US$115, coal US$220 → **₫0.36m/t**,
describing the current environment rather than a recovery from it. On ~11.5mt of
remaining volume that is roughly **₫4.1tn** of second-half core profit, against ₫14.4tn
implied by the current bear branch.

**Not implemented.** Adding a scenario branch and reweighting probabilities is a judgment
change to beliefs, which charter §2 reserves for a human on primary evidence. It is
recorded here as a recommendation for the CIO run.

---
*Inputs from the 2026-07-26 monitoring entries: Formosa Ha Tinh HRC cut ~₫1,050/kg
(≈US$40/t); Indian HRC ~US$535/t landed Vietnam; domestic HRC ₫14,000–14,350/kg; iron ore
~US$115/t; coking coal 2026F US$220/t. Q1 actual core NPAT/t ₫1.68m from the Q1/26 IR
summary.*
