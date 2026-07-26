# Decision Brief — generated 2026-07-24

> `python3 research/models/decide.py`. Beliefs in `assumptions.json`; decisions recorded in `research/decisions/decision-log.md`; accuracy scored in `calibration-log.md`. **Recommendations, not orders — a human signs every trade.**

## 1 · Ranked expected return (12m)

`E[r] = Σ p(scenario) × [ exit multiple × FY26E earnings / market cap − 1 ] × confidence`

| Rank | Ticker | Raw E[r] | Conf | **Shrunk E[r]** | Bear branch | σ | E[r]/σ | Evidence |
|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | **VPX** | +27.2% | 0.70 | **+19.0%** | -20.4% | 51% | 0.38 | Q2 official; but 1H leaned on VND3.46tn FVTPL marks -> earnings QUALITY discount in exit_pe |
| 2 | **TCX** | +23.1% | 0.80 | **+18.5%** | -13.3% | 43% | 0.43 | Q2 official; 1H 47.1% of plan; the risk is the MULTIPLE (2.49x P/B, priciest in book), not the earnings |
| 3 | **HPG** | +15.1% | 0.60 | **+9.1%** | +0.2% | 32% | 0.29 | Q2 UNFILED; 26-Jul spread evidence moved mass to bear; FY26E is CORE (ex VND4.12tn Pho Noi gain); cyclical multiple INVERTED (low on peak) |
| 4 | **MBB** | +16.0% | 0.55 | **+8.8%** | -13.1% | 36% | 0.24 | NO DOSSIER YET (S1/S3 pending); Q2 estimate only; ROE TTM 20.9% is sector-best |
| 5 | **KDH** | +16.1% | 0.50 | **+8.1%** | -31.2% | 54% | 0.15 | Q2 UNFILED; estimate dispersion extreme (MBS 170 vs SSI 348); FY26 rests on one variable (Gladia handovers) |
| 6 | **VCI** | +10.7% | 0.65 | **+7.0%** | -27.1% | 44% | 0.16 | Q2 official but BEHIND plan (1H ~29% of a +41% FY target); ROE 8.9% at 17x; no dossier |
| 7 | **TCB** | +4.3% | 0.85 | **+3.6%** | -19.3% | 34% | 0.11 | Q2 official; 1H 48.9% of plan; NIM recovering 3.1->3.4% |
| 8 | **VPB** | +1.4% | 0.85 | **+1.2%** | -25.9% | 36% | 0.03 | Q2 official; 1H PBT +68% vs +22% plan; credit +24.6% YTD |

The **confidence column is the discipline**: three of eight names still price off an unfiled quarter. Shrinking their expected return toward zero is what stops the optimizer from rewarding a name for being poorly understood.

## 2 · Target weights vs the book you own

Two columns on purpose. **North star** is where the math points if the assumptions are right. **This cycle** moves at most 5pp per name — because the assumptions are not all equally right yet, and three of these names report within the week.

| Ticker | Cluster | Current | **This cycle** | Δ | North star | Action |
|---|---|---:|---:|---:|---:|---|
| VPX | VPBank eco | 2.8% | **3.6%** | +0.8pp | 2.8% | hold |
| TCX | Techcom eco | 5.5% | **10.6%** | +5.1pp | 20.0% | **ADD** +5.1pp |
| HPG | Steel | 16.8% | **19.2%** | +2.4pp | 20.0% | hold |
| MBB | Banks-other | 6.5% | **11.5%** | +5.0pp | 20.0% | **ADD** +5.0pp |
| KDH | Residential | 20.3% | **14.9%** | -5.4pp | 2.3% | **TRIM** -5.4pp |
| VCI | Brokers-other | 3.1% | **6.2%** | +3.1pp | 5.7% | **ADD** +3.1pp |
| TCB | Techcom eco | 35.0% | **20.0%** | -15.0pp | 15.0% | **TRIM** -15.0pp |
| VPB | VPBank eco | 10.0% | **14.0%** | +4.0pp | 14.2% | **ADD** +4.0pp |

| | Expected return | Expected vol | Return/vol | Utility |
|---|---:|---:|---:|---:|
| Book as owned | +6.9% | 30.5% | 0.23 | -0.210 |
| After this cycle | +7.9% | 29.9% | 0.27 | -0.189 |
| North star | +9.1% | 29.3% | 0.31 | **-0.166** |
| **This cycle captures** | **+1.0pp** | **-0.6pp** | **+0.04** | **+0.021** |

The optimizer maximizes **utility** (`E[r] − λ/2 × σ²`, λ=6), not raw return — which is why the north star can show a *lower* expected return than an intermediate step and still be the better book. It is buying a large reduction in risk with a small amount of return. That trade is the entire point of running a portfolio instead of a list of favourite stocks.


No-trade band ±3pp — smaller gaps are inside the noise of the assumptions and are not worth the spread.

## 3 · Risk diagnostics

| Cluster | Current | Target | Cap | Status |
|---|---:|---:|---:|---|
| Techcom eco | 40.5% | 30.6% | 35% | ⚠ **BREACH** → resolved |
| Residential | 20.3% | 14.9% | 35% | ok |
| Steel | 16.8% | 19.2% | 35% | ok |
| VPBank eco | 12.8% | 17.6% | 35% | ok |
| Banks-other | 6.5% | 11.5% | 35% | ok |
| Brokers-other | 3.1% | 6.2% | 35% | ok |

- Effective independent bets: **4.7 → 6.7** (HHI 0.211 → 0.148)

**Marginal contribution to risk** — the honest answer to 'what am I actually exposed to':

| Ticker | Weight (target) | MCTR | % of portfolio risk |
|---|---:|---:|---:|
| KDH | 14.9% | 40.3% | 20% |
| TCB | 20.0% | 28.3% | 19% |
| HPG | 19.2% | 22.2% | 14% |
| VPB | 14.0% | 28.2% | 13% |
| TCX | 10.6% | 33.7% | 12% |
| MBB | 11.5% | 27.8% | 11% |
| VCI | 6.2% | 30.8% | 6% |
| VPX | 3.6% | 37.6% | 5% |

## 4 · Trade list

- **SELL TCB** — 35.0% → 20.0% (-15.0pp; north star 15.0%). E[r] +3.6%, bear branch -19.3%. Q2 official; 1H 48.9% of plan; NIM recovering 3.1->3.4%
- **SELL KDH** — 20.3% → 14.9% (-5.4pp; north star 2.3%). E[r] +8.1%, bear branch -31.2%. Q2 UNFILED; estimate dispersion extreme (MBS 170 vs SSI 348); FY26 rests on one variable (Gladia handovers)
- **BUY TCX** — 5.5% → 10.6% (+5.1pp; north star 20.0%). E[r] +18.5%, bear branch -13.3%. Q2 official; 1H 47.1% of plan; the risk is the MULTIPLE (2.49x P/B, priciest in book), not the earnings
- **BUY MBB** — 6.5% → 11.5% (+5.0pp; north star 20.0%). E[r] +8.8%, bear branch -13.1%. NO DOSSIER YET (S1/S3 pending); Q2 estimate only; ROE TTM 20.9% is sector-best
- **BUY VPB** — 10.0% → 14.0% (+4.0pp; north star 14.2%). E[r] +1.2%, bear branch -25.9%. Q2 official; 1H PBT +68% vs +22% plan; credit +24.6% YTD
- **BUY VCI** — 3.1% → 6.2% (+3.1pp; north star 5.7%). E[r] +7.0%, bear branch -27.1%. Q2 official but BEHIND plan (1H ~29% of a +41% FY target); ROE 8.9% at 17x; no dossier

**Sequencing rule:** trims before adds (fund the buys, don't lever), and nothing that fights a dated catalyst inside 5 sessions — see the catalyst calendar.

## 5 · Kill-criteria check (mechanical)

| Ticker | Condition | Test | Status |
|---|---|---|---|
| VPX | Earnings quality confirmed synthetic | FVTPL marks > 50% of PBT for a third consecutive quarter | armed |
| VPX | The free option expires worthless | CAEX licence rejected under the 5-licence cap | armed |
| TCX | The multiple is the thesis, and it goes | P/B < 2.0x on unchanged earnings = the re-rating case is dead | armed |
| TCX | FTSE flows disappoint | no net foreign accumulation in the 4 weeks after Sep 21 | armed |
| HPG | The spread thesis breaks | core NPAT/tonne < VND1.25m for two consecutive quarters | armed — 26-Jul spread evidence moved this closer |
| HPG | DQ2 ramp disappoints | HRC volume run-rate < 85% of nameplate at Q4 | armed |
| MBB | Weak-bank transfer turns from privilege to cost | transferee drag > 5% of PBT in any quarter | armed |
| KDH | Handover pace fails | customer advances < VND1,000bn at 3Q26 with Gladia Heights launched | armed — the decisive test |
| KDH | Leverage outruns delivery | debt > VND18tn without a matching pre-sale step-up | armed |
| KDH | Earnings quality stays synthetic | a second consecutive quarter where bargain-purchase or revaluation gains exceed operating PBT | armed |
| VCI | Behind plan becomes broken plan | 9M PBT < 55% of the FY target | armed — 1H already only ~29% |
| VCI | The single bull case fails | no market-share gain in foreign brokerage through the FTSE event | armed |
| TCB | NIM fails to hold the Q2 recovery | Q3 NIM < 3.25% (vs 3.4% in Q2) | armed |
| TCB | Ecosystem credit concentration turns | developer/related-party NPL formation > 2.0%, or a Masterise bond event | armed |
| VPB | FE Credit re-breaks | consumer-finance NPL formation re-accelerates > 3.0% credit cost annualized | armed |
| VPB | Placement prices badly | foreign placement executed > 15% below market | armed |

Written before the event, checked at every event, not 'when it feels right'. A triggered criterion is not a suggestion — it forces the resize at the next brief.

---

**What this brief cannot do.** It cannot price governance, quota politics, an An Lap-style related-party surprise, or a market that simply stays irrational longer than the horizon. Those are Layer 4 and they live in the dossiers. The optimizer's job is to stop *arithmetic* mistakes — position sizes that don't match stated conviction — not to replace judgment about what is true.

