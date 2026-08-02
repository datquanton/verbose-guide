# Decision Brief — generated 2026-07-24

> `python3 research/models/decide.py`. Beliefs in `assumptions.json`; decisions recorded in `research/decisions/decision-log.md`; accuracy scored in `calibration-log.md`. **Recommendations, not orders — a human signs every trade.**

## 1 · Ranked expected return (12m)

`E[r] = Σ p(scenario) × [ exit multiple × FY26E earnings / market cap − 1 ] × confidence`

| Rank | Ticker | Raw E[r] | Conf | **Shrunk E[r]** | Bear branch | σ | E[r]/σ | Evidence |
|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | **TCX** | +23.1% | 0.75 | **+17.3%** | -13.3% | 43% | 0.41 | Q2 official; 1H 47.1% of plan; the risk is the MULTIPLE (2.49x P/B, priciest in book), not the earnings. [This is the ORIGINAL string, RESTORED 2026-08-02 10:53. The 09:53 restatement claimed 2.49x was unreproducible and put P/B at 2.075x; that was computed on the LISTING-DATE share count and is withdrawn. With the post-stock-dividend count of 2,773,896,000, 41,100 x shares / filed equity 45,782bn = 2.4902x - the original figure is exact.] SEPARATELY AND UNRESOLVED, ESCALATED NOT APPLIED: decide.py prices this name off cap_now = pe_ttm x npat_ttm = 82,215bn against a true market cap of 114,007bn at this price, 38.7% low, which overstates mu_raw by 34.3pp and flips it from +23.1% to -11.2%. Either pe_ttm (20.3) or npat_ttm (4,050) is wrong; which is not established, so neither is changed. confidence held at 0.75 - the 09:53 grounds for the cut are void, but the input quality on this name is genuinely worse than 0.80 implied: the share count was stale, the price is wrong for its presumed date, and the market cap is 38.7% off. Not lowered further, because confidence is the wrong instrument for a broken denominator. |
| 2 | **VPX** | +27.2% | 0.55 | **+15.0%** | -20.4% | 51% | 0.29 | S3 done 27-Jul. NOT primarily a broker: ~30tn FVTPL book (>18tn BONDS) + 38.2tn margin vs only 3.57% HOSE share — a leveraged credit/margin book. Discount JUSTIFIED but for a different reason: Q2 absorbed a 923bn FVTPL loss and prop still netted >700bn, so gains are not fake; the risk is a 18tn+ bond position in the VN corporate-bond market. >33tn of unused margin room is the real bull case, better than the CAEX option. npat_ttm suspect — see flag. |
| 3 | **HPG** | +15.1% | 0.70 | **+10.6%** | +0.2% | 32% | 0.34 | Q2/26 FILED 29-Jul: revenue 55,557bn +53%, NPAT 6,424bn +51%; H1 15,480bn +103%, 70% of the FY plan. Q1+Q2 reconciles to H1 exactly. Confidence 0.60 -> 0.70: the quarter is now T1 actual rather than estimate, but FY26 remains a forecast and the H2 spread question is unresolved. STEEL IS 68% OF H1 PROFIT and 93% of revenue - non-steel is overwhelmingly the Pho Noi one-off. fy26e_npat is CORE (ex the 4,123bn gain); H1 core is 11,357bn, so the bear branch now requires a 41% collapse in the H2 run-rate and the base branch requires roughly flat. Cyclical multiple still INVERTED (low on peak). |
| 4 | **MBB** | +16.0% | 0.55 | **+8.8%** | -13.1% | 36% | 0.24 | Q2/2026 FILED, surfaced 31-Jul, one day past the Circular 96/2020 deadline. Q2 PBT 10,560bn (+40%); Q2 NPAT-to-parent 8,229.06bn (+40.01%); H1 NPAT-to-parent 15,744.58bn (+26.51%); Q2 net interest income 16,893.65bn (+36.55%). NPL 1.45% (from 1.42%), coverage 93.63% (from 92.24%), customer loans +13.2% YTD. Q1+Q2 parent NPAT reconciles to H1 exactly and the parent share (97.4%) matches Q1's 97.6%. See actuals._Q2_FILED_2026_07_31. THE BRANCHES ARE NOW THE PROBLEM, AND FROM BELOW. H1 PBT of 20,188bn leaves bear needing H2 -26.6%, base -11.2%, bull +4.3%, in a market where bank profit is second-half weighted; a FLAT H2 gives FY26 PBT 40,376bn, above base and just below bull. fy26e_npat 28,000/30,500/33,000 REQUIRES HUMAN RE-DERIVATION - the 28-Jul pre-registered H2 table called exactly this outcome and its instruction is to rebuild, not to celebrate. CONFIDENCE HELD AT 0.55, per charter s2: this is T5 press about a filing, not the filing, and confidence rises only on T1-T2. Note the contrast with KDH, whose branches are contradicted from ABOVE - the same held-confidence decision guards against flattery in one case and against understatement in the other. STILL NO DRIVER MODEL: run.py builds scenarios for KDH, TCB, VPB, TCX, VPX and HPG only; MBB's branches are typed in, derived from nothing and recomputed by nothing. That gap matters MORE than it did on 28-Jul, because there is finally a filed half-year to build from and the engine still wants MBB as its joint-largest add. Trailing ROE 20.9% is sector-best and ROE/(P/B) 16.9% the best of five banks screened; the S1 variant view (ROE erosion 25.0->20.9% as the PRICE of the MBV transfer, which bought a 30-35% credit allowance) is unaffected by this print and arguably supported by it. See dossiers/MBB.md, CONSISTENCY-AUDIT.md section 3. |
| 5 | **KDH** | +16.1% | 0.50 | **+8.1%** | -31.2% | 54% | 0.15 | CORRECTED 2026-08-02 05:53 - THE PREVIOUS EVIDENCE STRING WAS BUILT ON A WRONG H1 FIGURE AND IS RESTATED HERE IN FULL. WHAT IT SAID: 'Q2/2026 FILED 30-Jul and it is a large miss... H1 net profit 321bn (-6%), implying Q2 profit of roughly ZERO.' THAT IS WRONG. WHAT IS TRUE: Q2/2026 CONSOLIDATED NPAT IS 770bn AND H1 IS ~1,097bn, WHICH IS 73% OF THE 1,500bn FY PLAN. The file's own q1_npat of 327 reconciles it (327 + 770 = 1,097). The 321bn carried as h1_npat is on a DIFFERENT BASIS - core, ex-gain or parent - which is not yet established, and pairing it with a CONSOLIDATED Q1 produced a fictitious 'Q2 is roughly zero'. Both figures are retained in kdh.actuals with their bases labelled; neither is deleted. WHAT REMAINS TRUE AND MATTERS: THE CORE BUSINESS DID COLLAPSE. Q2 revenue 161bn is -85%, H1 revenue 442bn is -75%, roughly 3.7-3.8 units were handed in Q2 against a bear branch needing 80 for the year, H1 operating cash flow was -2,580bn, borrowings rose 6,500bn and inventory exceeds 23,000bn. Every street estimate on REVENUE was far too high; VCBS's was 7x the outcome. WHAT DROVE THE PROFIT: FINANCIAL INCOME OF MORE THAN 906bn, largely the deconsolidation gain on transferring 51% OF BINH TRUNG MOI for over 1,743bn. SO THE 73% OF PLAN IS A ONE-OFF, NOT A RUN-RATE - and the correct description of KDH's half is BOTH 'core operations collapsed' AND 'plan is 73% delivered', which are not in tension once the gain is identified. CONFIDENCE HELD AT 0.50, UNCHANGED. It was held on 30-Jul as a deliberate deviation to stop the engine rewarding a bad print; it is held now because the branches need HUMAN RE-DERIVATION against an H1 that is 73% one-off, and moving a scalar is not a substitute for that. fy26e_npat 1,033/1,590/2,203 is unchanged and REQUIRES RE-DERIVATION - charter s4, human-only. ALSO ON FILE: KDH is on the VNDIAMOND REMOVAL WATCHLIST on a foreign-ownership ratio of 61.8% against a 65% minimum, with index changes effective 03-AUG; and its AGM ruled out new equity issuance, which removes one lever for raising that ratio. See kdh.actuals for all of it. |
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
| Book as owned | +6.8% | 30.5% | 0.22 | -0.211 |
| After this cycle | +7.6% | 29.7% | 0.25 | -0.189 |
| North star | +8.5% | 29.0% | 0.29 | **-0.168** |
| **This cycle captures** | **+0.8pp** | **-0.8pp** | **+0.03** | **+0.022** |

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
- **BUY TCX** — 5.5% → 11.0% (+5.5pp; north star 20.0%). E[r] +17.3%, bear branch -13.3%. Q2 official; 1H 47.1% of plan; the risk is the MULTIPLE (2.49x P/B, priciest in book), not the earnings. [This is the ORIGINAL string, RESTORED 2026-08-02 10:53. The 09:53 restatement claimed 2.49x was unreproducible and put P/B at 2.075x; that was computed on the LISTING-DATE share count and is withdrawn. With the post-stock-dividend count of 2,773,896,000, 41,100 x shares / filed equity 45,782bn = 2.4902x - the original figure is exact.] SEPARATELY AND UNRESOLVED, ESCALATED NOT APPLIED: decide.py prices this name off cap_now = pe_ttm x npat_ttm = 82,215bn against a true market cap of 114,007bn at this price, 38.7% low, which overstates mu_raw by 34.3pp and flips it from +23.1% to -11.2%. Either pe_ttm (20.3) or npat_ttm (4,050) is wrong; which is not established, so neither is changed. confidence held at 0.75 - the 09:53 grounds for the cut are void, but the input quality on this name is genuinely worse than 0.80 implied: the share count was stale, the price is wrong for its presumed date, and the market cap is 38.7% off. Not lowered further, because confidence is the wrong instrument for a broken denominator.
- **BUY MBB** — 6.5% → 12.0% (+5.5pp; north star 20.0%). E[r] +8.8%, bear branch -13.1%. Q2/2026 FILED, surfaced 31-Jul, one day past the Circular 96/2020 deadline. Q2 PBT 10,560bn (+40%); Q2 NPAT-to-parent 8,229.06bn (+40.01%); H1 NPAT-to-parent 15,744.58bn (+26.51%); Q2 net interest income 16,893.65bn (+36.55%). NPL 1.45% (from 1.42%), coverage 93.63% (from 92.24%), customer loans +13.2% YTD. Q1+Q2 parent NPAT reconciles to H1 exactly and the parent share (97.4%) matches Q1's 97.6%. See actuals._Q2_FILED_2026_07_31. THE BRANCHES ARE NOW THE PROBLEM, AND FROM BELOW. H1 PBT of 20,188bn leaves bear needing H2 -26.6%, base -11.2%, bull +4.3%, in a market where bank profit is second-half weighted; a FLAT H2 gives FY26 PBT 40,376bn, above base and just below bull. fy26e_npat 28,000/30,500/33,000 REQUIRES HUMAN RE-DERIVATION - the 28-Jul pre-registered H2 table called exactly this outcome and its instruction is to rebuild, not to celebrate. CONFIDENCE HELD AT 0.55, per charter s2: this is T5 press about a filing, not the filing, and confidence rises only on T1-T2. Note the contrast with KDH, whose branches are contradicted from ABOVE - the same held-confidence decision guards against flattery in one case and against understatement in the other. STILL NO DRIVER MODEL: run.py builds scenarios for KDH, TCB, VPB, TCX, VPX and HPG only; MBB's branches are typed in, derived from nothing and recomputed by nothing. That gap matters MORE than it did on 28-Jul, because there is finally a filed half-year to build from and the engine still wants MBB as its joint-largest add. Trailing ROE 20.9% is sector-best and ROE/(P/B) 16.9% the best of five banks screened; the S1 variant view (ROE erosion 25.0->20.9% as the PRICE of the MBV transfer, which bought a 30-35% credit allowance) is unaffected by this print and arguably supported by it. See dossiers/MBB.md, CONSISTENCY-AUDIT.md section 3.
- **BUY VPB** — 10.0% → 15.3% (+5.3pp; north star 17.8%). E[r] +1.0%, bear branch -25.9%. Q2 official; 1H PBT 18,880bn +68% vs +22% plan - that part is T1 and unaffected. BUT the '+24.6% credit YTD' previously cited here as support FAILS the period and entity checks (see vpb.actuals._CREDIT_INPUTS_FAIL_VERIFICATION_2026_07_28). Confidence cut 0.85 -> 0.70 on 2026-07-28: the trailing earnings base is solidly evidenced, the forward credit driver is not. Resolves from the Q2 consolidated statement.
- **SELL KDH** — 20.3% → 15.6% (-4.7pp; north star 3.1%). E[r] +8.1%, bear branch -31.2%. CORRECTED 2026-08-02 05:53 - THE PREVIOUS EVIDENCE STRING WAS BUILT ON A WRONG H1 FIGURE AND IS RESTATED HERE IN FULL. WHAT IT SAID: 'Q2/2026 FILED 30-Jul and it is a large miss... H1 net profit 321bn (-6%), implying Q2 profit of roughly ZERO.' THAT IS WRONG. WHAT IS TRUE: Q2/2026 CONSOLIDATED NPAT IS 770bn AND H1 IS ~1,097bn, WHICH IS 73% OF THE 1,500bn FY PLAN. The file's own q1_npat of 327 reconciles it (327 + 770 = 1,097). The 321bn carried as h1_npat is on a DIFFERENT BASIS - core, ex-gain or parent - which is not yet established, and pairing it with a CONSOLIDATED Q1 produced a fictitious 'Q2 is roughly zero'. Both figures are retained in kdh.actuals with their bases labelled; neither is deleted. WHAT REMAINS TRUE AND MATTERS: THE CORE BUSINESS DID COLLAPSE. Q2 revenue 161bn is -85%, H1 revenue 442bn is -75%, roughly 3.7-3.8 units were handed in Q2 against a bear branch needing 80 for the year, H1 operating cash flow was -2,580bn, borrowings rose 6,500bn and inventory exceeds 23,000bn. Every street estimate on REVENUE was far too high; VCBS's was 7x the outcome. WHAT DROVE THE PROFIT: FINANCIAL INCOME OF MORE THAN 906bn, largely the deconsolidation gain on transferring 51% OF BINH TRUNG MOI for over 1,743bn. SO THE 73% OF PLAN IS A ONE-OFF, NOT A RUN-RATE - and the correct description of KDH's half is BOTH 'core operations collapsed' AND 'plan is 73% delivered', which are not in tension once the gain is identified. CONFIDENCE HELD AT 0.50, UNCHANGED. It was held on 30-Jul as a deliberate deviation to stop the engine rewarding a bad print; it is held now because the branches need HUMAN RE-DERIVATION against an H1 that is 73% one-off, and moving a scalar is not a substitute for that. fy26e_npat 1,033/1,590/2,203 is unchanged and REQUIRES RE-DERIVATION - charter s4, human-only. ALSO ON FILE: KDH is on the VNDIAMOND REMOVAL WATCHLIST on a foreign-ownership ratio of 61.8% against a 65% minimum, with index changes effective 03-AUG; and its AGM ruled out new equity issuance, which removes one lever for raising that ratio. See kdh.actuals for all of it.
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

