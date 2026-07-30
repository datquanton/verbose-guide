# Decision Brief — generated 2026-07-24

> `python3 research/models/decide.py`. Beliefs in `assumptions.json`; decisions recorded in `research/decisions/decision-log.md`; accuracy scored in `calibration-log.md`. **Recommendations, not orders — a human signs every trade.**

## 1 · Ranked expected return (12m)

`E[r] = Σ p(scenario) × [ exit multiple × FY26E earnings / market cap − 1 ] × confidence`

| Rank | Ticker | Raw E[r] | Conf | **Shrunk E[r]** | Bear branch | σ | E[r]/σ | Evidence |
|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | **TCX** | +23.1% | 0.80 | **+18.5%** | -13.3% | 43% | 0.43 | Q2 official; 1H 47.1% of plan; the risk is the MULTIPLE (2.49x P/B, priciest in book), not the earnings |
| 2 | **VPX** | +27.2% | 0.55 | **+15.0%** | -20.4% | 51% | 0.29 | S3 done 27-Jul. NOT primarily a broker: ~30tn FVTPL book (>18tn BONDS) + 38.2tn margin vs only 3.57% HOSE share — a leveraged credit/margin book. Discount JUSTIFIED but for a different reason: Q2 absorbed a 923bn FVTPL loss and prop still netted >700bn, so gains are not fake; the risk is a 18tn+ bond position in the VN corporate-bond market. >33tn of unused margin room is the real bull case, better than the CAEX option. npat_ttm suspect — see flag. |
| 3 | **HPG** | +15.1% | 0.70 | **+10.6%** | +0.2% | 32% | 0.34 | Q2/26 FILED 29-Jul: revenue 55,557bn +53%, NPAT 6,424bn +51%; H1 15,480bn +103%, 70% of the FY plan. Q1+Q2 reconciles to H1 exactly. Confidence 0.60 -> 0.70: the quarter is now T1 actual rather than estimate, but FY26 remains a forecast and the H2 spread question is unresolved. STEEL IS 68% OF H1 PROFIT and 93% of revenue - non-steel is overwhelmingly the Pho Noi one-off. fy26e_npat is CORE (ex the 4,123bn gain); H1 core is 11,357bn, so the bear branch now requires a 41% collapse in the H2 run-rate and the base branch requires roughly flat. Cyclical multiple still INVERTED (low on peak). |
| 4 | **MBB** | +16.0% | 0.55 | **+8.8%** | -13.1% | 36% | 0.24 | S1 screen DONE 26-Jul (research/dossiers/MBB.md) - the previous 'NO DOSSIER YET' string was out of date. Passes S1 with a falsifiable variant view: ROE erosion 25.0->20.9% may be the PRICE of the MBV transfer, which bought a 30-35% credit allowance. Trailing ROE 20.9% is sector-best and ROE/(P/B) 16.9% is the best of five banks screened. Q2 is still an ESTIMATE, not filed. THE REAL GAP, found 28-Jul: MBB has NO DRIVER MODEL. run.py builds scenarios for KDH, TCB, VPB, TCX, VPX and HPG only; MBB's fy26e_npat branches are typed in directly, derived from nothing and recomputed by nothing. The optimizer's largest bank add (+5.5pp, 6.5%->12.0%) therefore rests on the one bank whose earnings branches were never built from drivers. Confidence HELD at 0.55: the stale string understated what is known while missing what is missing, and the two corrections roughly cancel. The fix is to build the model, not to shade the number. See CONSISTENCY-AUDIT.md section 3. |
| 5 | **KDH** | +16.1% | 0.50 | **+8.1%** | -31.2% | 54% | 0.15 | Q2/2026 FILED 30-Jul and it is a large miss: Q2 revenue 161bn (-85%), H1 revenue 442bn (-75%), H1 net profit 321bn (-6%), implying Q2 profit of roughly ZERO. Every street estimate (NHSV 102 / MBS 170 / SSI 330 / VCBS 348) was too high; VCBS's revenue forecast was 7x the outcome. Financial costs x3, selling expenses x2.9 on discounting. H1 operating cash flow -2,580bn, borrowings +6,500bn to ~16,500bn bank debt, inventory >23,000bn, D/E >71%. CONFIDENCE DELIBERATELY HELD AT 0.50, NOT RAISED - see _CONFIDENCE_NOT_RAISED_2026_07_30. fy26e_npat branches are now contradicted by the run-rate and REQUIRE HUMAN RE-DERIVATION. |
| 6 | **VCI** | +10.7% | 0.40 | **+4.3%** | -27.1% | 44% | 0.10 | S1 done 26-Jul. Q2 -26% QoQ (251 vs 341) behind the +36% YoY headline; revenue flat, OCF negative funded by borrowings, prop book -430bn on FPT/MWG/KDH. ROE 8.9% vs ~15% COE => justified P/B ~0.39x against 1.38x traded. Bull case is the #1 institutional franchise (>28% share) into FTSE Sep-21 — an EVENT bet, not a franchise investment. npat_ttm suspect, see flag. | 28-Jul: VCI also has NO DRIVER MODEL - not built by run.py, fy26e_npat branches asserted directly. With MBB that is 9.6% of the book priced off numbers nothing derives. See CONSISTENCY-AUDIT.md section 3. |
| 7 | **TCB** | +4.3% | 0.80 | **+3.4%** | -19.3% | 34% | 0.10 | Q2 official - PBT 9,670bn, +22%, a record quarter; H1 18,500bn, which matches h1_pbt exactly. That earnings evidence is T1 and unaffected. BUT the forward credit driver is now unverified: TCB reports credit +10.39% YTD while this file's loan pair implies +14.46% (see tcb.model._CREDIT_VS_LOANS_2026_07_28). Confidence cut 0.85 -> 0.80 on 2026-07-28. The cut is SMALLER than VPB's 0.85 -> 0.70 on purpose: VPB's two fields had no coherent reconciliation, whereas TCB's do - credit and loans are different measures, and the gap between them is itself informative about the bond book. Resolves from the Q2 balance sheet. Also on file: consensus TP is quoted pre-60%-bonus and adjusts to ~10.6% below spot; NIM recovering 3.1->3.4%. |
| 8 | **VPB** | +1.4% | 0.70 | **+1.0%** | -25.9% | 36% | 0.03 | Q2 official; 1H PBT 18,880bn +68% vs +22% plan - that part is T1 and unaffected. BUT the '+24.6% credit YTD' previously cited here as support FAILS the period and entity checks (see vpb.actuals._CREDIT_INPUTS_FAIL_VERIFICATION_2026_07_28). Confidence cut 0.85 -> 0.70 on 2026-07-28: the trailing earnings base is solidly evidenced, the forward credit driver is not. Resolves from the Q2 consolidated statement. |

The **confidence column is the discipline**: three of eight names still price off an unfiled quarter. Shrinking their expected return toward zero is what stops the optimizer from rewarding a name for being poorly understood.

## 2 · Target weights vs the book you own

Two columns on purpose. **North star** is where the math points if the assumptions are right. **This cycle** moves at most 5pp per name — because the assumptions are not all equally right yet, and three of these names report within the week.

| Ticker | Cluster | Current | **This cycle** | Δ | North star | Action |
|---|---|---:|---:|---:|---:|---|
| TCX | Techcom eco | 5.5% | **11.0%** | +5.5pp | 20.0% | **ADD** +5.5pp |
| VPX | VPBank eco | 2.8% | **1.2%** | -1.6pp | 0.0% | hold |
| HPG | Steel | 16.8% | **20.0%** | +3.2pp | 20.0% | **ADD** +3.2pp |
| MBB | Banks-other | 6.5% | **12.0%** | +5.5pp | 20.0% | **ADD** +5.5pp |
| KDH | Residential | 20.3% | **15.6%** | -4.7pp | 3.1% | **TRIM** -4.7pp |
| VCI | Brokers-other | 3.1% | **5.0%** | +1.9pp | 4.1% | hold |
| TCB | Techcom eco | 35.0% | **20.0%** | -15.0pp | 15.0% | **TRIM** -15.0pp |
| VPB | VPBank eco | 10.0% | **15.3%** | +5.3pp | 17.8% | **ADD** +5.3pp |

| | Expected return | Expected vol | Return/vol | Utility |
|---|---:|---:|---:|---:|
| Book as owned | +6.9% | 30.5% | 0.22 | -0.211 |
| After this cycle | +7.7% | 29.7% | 0.26 | -0.188 |
| North star | +8.7% | 29.0% | 0.30 | **-0.165** |
| **This cycle captures** | **+0.8pp** | **-0.8pp** | **+0.03** | **+0.023** |

The optimizer maximizes **utility** (`E[r] − λ/2 × σ²`, λ=6), not raw return — which is why the north star can show a *lower* expected return than an intermediate step and still be the better book. It is buying a large reduction in risk with a small amount of return. That trade is the entire point of running a portfolio instead of a list of favourite stocks.

No-trade band ±3pp — smaller gaps are inside the noise of the assumptions and are not worth the spread.

⚠ **KDH, TCB moves further than the 5pp step limit.** That is deliberate, not a bug: a position already through the 20% constitutional cap gets brought back to the cap now. The step limit governs *discretionary* moves; a breach of the constitution is not discretionary.

## 3 · Risk diagnostics

| Cluster | Current | Target | Cap | Status |
|---|---:|---:|---:|---|
| Techcom eco | 40.5% | 31.0% | 35% | ⚠ **BREACH** → resolved |
| Residential | 20.3% | 15.6% | 35% | ok |
| Steel | 16.8% | 20.0% | 35% | ok |
| VPBank eco | 12.8% | 16.4% | 35% | ok |
| Banks-other | 6.5% | 12.0% | 35% | ok |
| Brokers-other | 3.1% | 5.0% | 35% | ok |

- Effective independent bets: **4.7 → 6.4** (HHI 0.211 → 0.157)

**Marginal contribution to risk** — the honest answer to 'what am I actually exposed to':

| Ticker | Weight (target) | MCTR | % of portfolio risk |
|---|---:|---:|---:|
| KDH | 15.6% | 40.6% | 21% |
| TCB | 20.0% | 28.5% | 19% |
| HPG | 20.0% | 22.3% | 15% |
| VPB | 15.3% | 28.0% | 14% |
| TCX | 11.0% | 33.2% | 12% |
| MBB | 12.0% | 28.0% | 11% |
| VCI | 5.0% | 29.9% | 5% |
| VPX | 1.2% | 36.6% | 1% |

## 4 · Trade list

- **SELL TCB** — 35.0% → 20.0% (-15.0pp; north star 15.0%). E[r] +3.4%, bear branch -19.3%. Q2 official - PBT 9,670bn, +22%, a record quarter; H1 18,500bn, which matches h1_pbt exactly. That earnings evidence is T1 and unaffected. BUT the forward credit driver is now unverified: TCB reports credit +10.39% YTD while this file's loan pair implies +14.46% (see tcb.model._CREDIT_VS_LOANS_2026_07_28). Confidence cut 0.85 -> 0.80 on 2026-07-28. The cut is SMALLER than VPB's 0.85 -> 0.70 on purpose: VPB's two fields had no coherent reconciliation, whereas TCB's do - credit and loans are different measures, and the gap between them is itself informative about the bond book. Resolves from the Q2 balance sheet. Also on file: consensus TP is quoted pre-60%-bonus and adjusts to ~10.6% below spot; NIM recovering 3.1->3.4%.
- **BUY TCX** — 5.5% → 11.0% (+5.5pp; north star 20.0%). E[r] +18.5%, bear branch -13.3%. Q2 official; 1H 47.1% of plan; the risk is the MULTIPLE (2.49x P/B, priciest in book), not the earnings
- **BUY MBB** — 6.5% → 12.0% (+5.5pp; north star 20.0%). E[r] +8.8%, bear branch -13.1%. S1 screen DONE 26-Jul (research/dossiers/MBB.md) - the previous 'NO DOSSIER YET' string was out of date. Passes S1 with a falsifiable variant view: ROE erosion 25.0->20.9% may be the PRICE of the MBV transfer, which bought a 30-35% credit allowance. Trailing ROE 20.9% is sector-best and ROE/(P/B) 16.9% is the best of five banks screened. Q2 is still an ESTIMATE, not filed. THE REAL GAP, found 28-Jul: MBB has NO DRIVER MODEL. run.py builds scenarios for KDH, TCB, VPB, TCX, VPX and HPG only; MBB's fy26e_npat branches are typed in directly, derived from nothing and recomputed by nothing. The optimizer's largest bank add (+5.5pp, 6.5%->12.0%) therefore rests on the one bank whose earnings branches were never built from drivers. Confidence HELD at 0.55: the stale string understated what is known while missing what is missing, and the two corrections roughly cancel. The fix is to build the model, not to shade the number. See CONSISTENCY-AUDIT.md section 3.
- **BUY VPB** — 10.0% → 15.3% (+5.3pp; north star 17.8%). E[r] +1.0%, bear branch -25.9%. Q2 official; 1H PBT 18,880bn +68% vs +22% plan - that part is T1 and unaffected. BUT the '+24.6% credit YTD' previously cited here as support FAILS the period and entity checks (see vpb.actuals._CREDIT_INPUTS_FAIL_VERIFICATION_2026_07_28). Confidence cut 0.85 -> 0.70 on 2026-07-28: the trailing earnings base is solidly evidenced, the forward credit driver is not. Resolves from the Q2 consolidated statement.
- **SELL KDH** — 20.3% → 15.6% (-4.7pp; north star 3.1%). E[r] +8.1%, bear branch -31.2%. Q2/2026 FILED 30-Jul and it is a large miss: Q2 revenue 161bn (-85%), H1 revenue 442bn (-75%), H1 net profit 321bn (-6%), implying Q2 profit of roughly ZERO. Every street estimate (NHSV 102 / MBS 170 / SSI 330 / VCBS 348) was too high; VCBS's revenue forecast was 7x the outcome. Financial costs x3, selling expenses x2.9 on discounting. H1 operating cash flow -2,580bn, borrowings +6,500bn to ~16,500bn bank debt, inventory >23,000bn, D/E >71%. CONFIDENCE DELIBERATELY HELD AT 0.50, NOT RAISED - see _CONFIDENCE_NOT_RAISED_2026_07_30. fy26e_npat branches are now contradicted by the run-rate and REQUIRE HUMAN RE-DERIVATION.
- **BUY HPG** — 16.8% → 20.0% (+3.2pp; north star 20.0%). E[r] +10.6%, bear branch +0.2%. Q2/26 FILED 29-Jul: revenue 55,557bn +53%, NPAT 6,424bn +51%; H1 15,480bn +103%, 70% of the FY plan. Q1+Q2 reconciles to H1 exactly. Confidence 0.60 -> 0.70: the quarter is now T1 actual rather than estimate, but FY26 remains a forecast and the H2 spread question is unresolved. STEEL IS 68% OF H1 PROFIT and 93% of revenue - non-steel is overwhelmingly the Pho Noi one-off. fy26e_npat is CORE (ex the 4,123bn gain); H1 core is 11,357bn, so the bear branch now requires a 41% collapse in the H2 run-rate and the base branch requires roughly flat. Cyclical multiple still INVERTED (low on peak).

**Sequencing rule:** trims before adds (fund the buys, don't lever), and nothing that fights a dated catalyst inside 5 sessions — see the catalyst calendar.

## 5 · Kill-criteria check (mechanical)

| Ticker | Condition | Test | Status |
|---|---|---|---|
| TCX | The multiple is the thesis, and it goes | P/B < 2.0x on unchanged earnings = the re-rating case is dead | armed |
| TCX | FTSE flows disappoint | no net foreign accumulation in the 4 weeks after Sep 21 | armed |
| VPX | Earnings quality confirmed synthetic | FVTPL marks > 50% of PBT for a third consecutive quarter | armed |
| VPX | The free option expires worthless | CAEX licence rejected under the 5-licence cap | armed |
| HPG | The spread thesis breaks | core NPAT/tonne < VND1.25m for two consecutive quarters | armed — 26-Jul spread evidence moved this closer |
| HPG | DQ2 ramp disappoints | HRC volume run-rate < 85% of nameplate at Q4 | armed |
| MBB | Weak-bank transfer turns from privilege to cost | transferee drag > 5% of PBT in any quarter | armed |
| KDH | Handover pace fails | customer advances < VND1,000bn at 3Q26 with Gladia Heights launched | armed — the decisive test |
| KDH | Leverage outruns delivery | debt > VND18tn without a matching pre-sale step-up | armed |
| KDH | Earnings quality stays synthetic | a second consecutive quarter where bargain-purchase or revaluation gains exceed operating PBT | armed |
| VCI | Behind plan becomes broken plan | 9M PBT < 55% of the FY target | armed — 1H only ~29%; as of 2026-07-27 clearing it needs Q3 PBT of 598bn, i.e. 2.21x the Q2 actual and 1.51x the better Q1. Near-certain to fire in October unless the signed IB/IPO pipeline lands inside Q3. See valuation.VCI._KILL_CRITERION_ARITHMETIC_2026_07_27 |
| VCI | The single bull case fails | no market-share gain in foreign brokerage through the FTSE event | armed |
| TCB | NIM fails to hold the Q2 recovery | Q3 NIM < 3.25% (vs 3.4% in Q2) | armed |
| TCB | Ecosystem credit concentration turns | developer/related-party NPL formation > 2.0%, or a Masterise bond event | armed |
| TCB | The real-estate de-risking reverses | RE share of loans back above 32% (was 33.2% in 2024 -> 28.9% at Q1/26) | armed — added from TCB dossier 2026-07-26 |
| VPB | FE Credit re-breaks | consumer-finance NPL formation re-accelerates > 3.0% credit cost annualized | armed |
| VPB | Placement prices badly | foreign placement executed > 15% below market | armed |

Written before the event, checked at every event, not 'when it feels right'. A triggered criterion is not a suggestion — it forces the resize at the next brief.

---

**What this brief cannot do.** It cannot price governance, quota politics, an An Lap-style related-party surprise, or a market that simply stays irrational longer than the horizon. Those are Layer 4 and they live in the dossiers. The optimizer's job is to stop *arithmetic* mistakes — position sizes that don't match stated conviction — not to replace judgment about what is true.

