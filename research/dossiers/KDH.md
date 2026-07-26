# KDH — Research Dossier

**Status:** S3 core complete (depth-queue item 11) · 2026-07-27
**Why now:** 20.3% of the book, the widest estimate dispersion in it (MBS ₫170bn vs SSI
₫348bn for Q2), and the statement lands in ~48 hours. **The point of writing this now is
to fix the interpretation before the number arrives**, not after.

> **Independent derivation matches the model.** Working from Q1 unit economics, the FY26
> handover counts implied by each branch come out at **81 / 131 / 186** against the
> `scenarios_units_handed_fy26` of **80 / 130 / 185** already in `assumptions.json`. Two
> routes, one answer — the model is internally consistent.

---

## 1 · Unit economics, calibrated to the Q1 actual

| Input | Value | Source |
|---|---|---|
| ASP per low-rise unit | ₫42bn | Q1 handovers |
| Gross margin | 65% | Q1 actual |
| Gross profit per unit | **₫27.3bn** | derived |
| Quarterly fixed opex | **₫94bn** | **solved**, not assumed: 6 units × ₫27.3bn − ₫70bn ex-gain PBT |
| KDH stake in Gladia | 51% | Doan Nguyen 50.85% / New Binh Trung 50.95%, **fully consolidated** |

## 2 · The finding: every branch needs a step-change in handover pace

| Branch | FY26 NPAT | Ex one-off | Units needed FY | Q2–Q4 | Per quarter |
|---|---:|---:|---:|---:|---:|
| bear | ₫1,033bn | ₫748bn | 81 | 75 | **25.0** |
| base | ₫1,590bn | ₫1,305bn | 131 | 125 | **41.6** |
| bull | ₫2,203bn | ₫1,918bn | **186** | 180 | **60.0** |

**Q1/26 delivered 6 units.**

- Even the **bear** branch requires **25 units/quarter — a 4.2× step-up** on the observed run-rate.
- The **bull** branch requires **186 units against a 135-unit sold book**. It is not merely
  ambitious, it is **arithmetically infeasible** from existing contracts: it needs ~51
  further units sold *and* handed over inside the same year.

**Implication for the model:** the bull branch (p=0.20) should carry materially less
probability than that, and the bear branch is closest to the observed pace while still
demanding a 4× acceleration. This is a probability re-weighting — a judgment change,
reserved for a human (charter §2). **Flagged, not applied.**

The offsetting argument, stated fairly: handovers are lumpy by construction. Units complete
in batches as buildings finish and the interest-subsidy payment schedules run to 12/2026.
A 4× step-up from Q1 to Q4 is normal for a developer; what would be abnormal is the
*full-year total*. That is why the bull branch's infeasibility is the harder finding — it
does not depend on any view about lumpiness.

## 3 · Pre-registered reading of the Q2 print (~28–30 July)

Written **before** the number, so it cannot be rationalised afterwards:

| If Q2 parent NPAT is… | It implies consolidated PBT | ≈ units handed in Q2 | Read as |
|---|---:|---:|---|
| **₫170bn** (MBS) | ₫417bn | **~19** | Bear confirmed. 19 vs 25/qtr needed — still short of even the bear pace |
| **₫259bn** (midpoint) | ₫635bn | **~27** | Bear-to-base. Roughly on the bear track |
| **₫348bn** (SSI) | ₫853bn | **~35** | Base in play. Under the 41.6/qtr the base needs, but a genuine step-change |

**Verify against the statements, not the headline:** the units count is checkable from the
Doan Nguyen/Gladia inventory movement (₫3.45tn at Q1; each handover releases ~₫15bn of
cost) and the revenue line. Two independent routes — use both (charter §3).

**And the number that matters more than profit: customer advances.** ₫688.6bn at Q1, up
from ₫648.3bn. The armed kill criterion is *advances < ₫1,000bn at 3Q26 with Heights
launched*. Advances are the forward-looking series; profit is the backward-looking one.

## 4 · Earnings quality — the standing problem

1. **The +131% Q1 headline was a paper gain.** Note 4.1: An Lap bought 99% for ₫2,552.8bn,
   inventory marked up to ₫5,429.5bn, net assets ₫2,869.5bn → **₫285.2bn bargain-purchase
   gain** through other income. **Ex-gain PBT ≈ ₫70bn** against a ₫355.7bn headline.
2. **P&L borrowing cost is zero; the real cost is ₫225bn/quarter.** All interest is
   capitalised into inventory (FY25: ₫801bn). At ₫15.35tn of debt this runs ~₫1.2–1.3tn/yr
   — deferred into COGS at handover, not avoided. That is **~80% of the ₫1.5tn NPAT plan**
   sitting in inventory waiting to be recognised.
3. **Operating cash flow negative for five consecutive years** (Q1/26: −₫634bn). Profit is
   handover accounting; cash goes to land, funded by borrowing.
4. **Debt +51% in one quarter**, ₫10.15tn → ₫15.35tn. Maturities 2027–2033, so no
   near-term wall — the risk is the carry, not a cliff.
5. **₫600bn still sitting in "advances for capital transfer"** — another acquisition pending.

## 5 · RNAV — first pass, deliberately crude

Book inventory ₫29.13tn is at cost plus capitalised interest. Marking to market:

| Project | Book | Window | Note |
|---|---:|---|---|
| Tan Tao | ₫8.92tn | 2028+ | 85% cleared; the largest asset is the furthest out |
| An Lap / BTD | ₫5.45tn | 2028+ | already stepped to fair value in Q1 |
| Binh Trung | ₫4.89tn | 2027–28 | |
| Doan Nguyen / Gladia | ₫3.45tn | **2026** | the only 2026 earner |
| 11A / Solina | ₫2.07tn | 2027+ | **slipped out of 2026** |
| Phong Phu 2 | ₫1.92tn | 2028+ | |

**The structural point: ₫3.45tn of a ₫29.13tn land bank — 12% — produces essentially all
of 2026's profit.** Everything else is 2027 or later, carrying capitalised interest at
~₫1.25tn/yr in the meantime. Against ₫15.35tn of debt and an ₫18tn market cap, KDH is a
land bank with one small operating project attached.

That is not a criticism of the assets; it is a statement about *timing*, and timing is what
the 2026 thesis rests on. A full RNAV with land marked per-hectare is the next step and is
**not** done here.

## 6 · Kill criteria

Three already armed (advances < ₫1tn at 3Q26; debt > ₫18tn without a matching pre-sale
step-up; a second consecutive quarter where paper gains exceed operating PBT). Added:

4. **Handover pace fails to inflect** — if Q2 and Q3 together deliver fewer than ~50
   units, the FY bear branch is out of reach and the whole 2026 thesis resets to 2027.

## 7 · Decision

No change proposed. The position is 20.3% and within the cap. What this dossier changes is
**how Thursday gets read**: a headline that beats ₫170bn is not automatically good news,
and a miss is not automatically fatal — the diagnostic is the *units handed* and the
*advances balance*, both derivable from the statements.

**Not done:** per-hectare land marks, the Ma Lang BT/PPP commitment, Clarita divestment
completion terms, the 2025 contracted-sales actual. Most need the AR, which is unreachable.

---
*Built on `research/annual-reports/notes/KDH-AR2025.md` §9 (Q1/26 consolidated FS, primary
document) and the v2 deep-dive. Unit economics calibrated to the Q1 actual rather than
assumed.*
