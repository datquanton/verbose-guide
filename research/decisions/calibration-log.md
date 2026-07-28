# Calibration Log — scoring the forecasts

The scoreboard. Every forecast that enters `assumptions.json` gets scored here when
reality lands. Newest first.

**Why this file is the most important one in the repo:** portfolio return measures
the market as much as the manager. Calibration measures only the manager. A book can
be up 30% in a year where every thesis was wrong, and down 10% in a year where every
call was right. Only this file can tell the difference — and only this file can turn
"I have a process" into "I have an edge," because an edge is a claim about accuracy
and accuracy is a measurable thing.

---

## How to score

When an actual lands, add a row. Score three separate things — they come apart more
often than people expect:

| Field | Meaning |
|---|---|
| **Forecast** | What was written, with its date and probability |
| **Actual** | What happened, with the source |
| **Direction** | ✅ / ❌ — was the base case on the right side? |
| **Error** | Actual vs the probability-weighted estimate, in % |
| **Reason** | ✅ right for the stated reason · ⚠️ right for a *different* reason · ❌ wrong |
| **Lesson** | One line. What changes in the model, or nothing |

The **Reason** column is the one that compounds. Right-for-the-wrong-reason is a
process failure that happens to pay, and it must be recorded as a failure or the
process learns the wrong lesson and repeats it with more confidence.

### Aggregate scoring (recompute quarterly, once n ≥ 10)

- **Hit rate by confidence bucket** — of forecasts marked 0.8 confidence, how many landed?
  Well-calibrated means ~80%. Systematically lower means overconfidence, and the
  `confidence` field in `assumptions.json` should be cut across the board.
- **Bias** — mean signed error. Persistently positive means the base cases are
  optimistic, which is the single most common flaw in a private book.
- **Dispersion check** — how often does the actual land *outside* the bear–bull range?
  Should be rare (<15%). More than that and the scenarios are too narrow, which
  understates risk everywhere downstream, including in the optimizer's vol estimates.

---

## Open forecasts — awaiting reality

Recorded now, scored when the statements file. **Written before the outcome is known;
that is what makes them worth scoring.**

| # | Date | Ticker | Forecast | Prob / confidence | Resolves | Status |
|---|---|---|---|---|---|---|
| 1 | 2026-07-24 | KDH | Q2/26 parent NPAT between MBS ₫170bn and SSI ₫348bn; base case FY26 NPAT ₫1,590bn | conf 0.50 | Q2 FS (~Jul 28–30) | ⏳ open |
| 2 | 2026-07-26 | HPG | Q2 core NPAT/tonne **below** ₫1.60m as the Formosa/iron-ore spread squeeze bites | bear p=0.45 | Q2 FS (~Jul 28–30) | ⏳ open |
| 3 | 2026-07-24 | HPG | FY26 core NPAT (ex Pho Noi gain) ₫23.3tn base case | conf 0.60 | FY26 audited | ⏳ open |
| 4 | 2026-07-24 | MBB | Q2/26 NPAT ≈ ₫7,052bn (VCBS est.); FY26 base ₫30.5tn | conf 0.55 | Q2 FS (~Jul 28–30) | ⏳ open |
| 5 | 2026-07-24 | TCB | FY26 PBT ₫33.2tn base — **below** company guidance ₫35–37.5tn | conf 0.85 | FY26 audited | ⏳ open |
| 6 | 2026-07-24 | VPB | FY26 PBT ₫30.7tn base vs ₫41.6tn target — plan leans on VPBankS | conf 0.85 | FY26 audited | ⏳ open |
| 7 | 2026-07-24 | TCX | FTSE Sep-21 event EV ≈ +6.2%; base case "in-line, quiet digestion" p=0.45 | conf 0.80 | ~Oct 21 (1m after) | ⏳ open |
| 8 | 2026-07-24 | VPX | CAEX licence granted ~Q3 at p=0.40 | conf 0.70 | Q3/26 end | ⏳ open |
| 9 | 2026-07-24 | VCI | 9M PBT reaches ≥55% of FY target (the kill-criterion threshold) | conf 0.65 | Q3 FS (~Oct) | ⏳ open |
| 10 | 2026-07-23 | HPG | US rebar AD/CVD final ≈ headline risk only, <3% of revenue, no thesis change | conf 0.75 | ~Jul 28 Federal Register | ⏳ open |

### Annotations on open forecasts

Original rows are **never edited** — a forecast that gets quietly revised as evidence
arrives cannot be scored, and a calibration log that permits revision measures nothing.
Where the evidence moves before resolution, it is recorded here instead, and both the
original and the annotation are visible when the row is finally scored.

- **2026-07-27 · #9 (VCI, 9M PBT ≥ 55% of the FY target, conf 0.65).** The 0.65 now looks
  clearly too high, and it looked too high on the day it was written. Clearing the
  threshold requires **₫1,265bn** of 9M pre-tax profit; the half delivered **₫667bn**; so
  **Q3 alone must produce ₫598bn — 2.21× the ₫270.8bn Q2 actual and 1.51× the ₫396bn
  Q1**. Only the signed IB/IPO pipeline landing inside Q3 gets there. Two facts arrived
  today that make the miss more likely rather than less: peers are not short (SSI finished
  the half at **53%** of its full-year target against VCI's 29%), and VCI's margin book was
  **flat quarter-on-quarter** while the system's grew 7% to a record.
  **The lesson is already visible and does not need the outcome to land:** a confidence of
  0.65 was attached to a forecast whose required arithmetic was never computed. Computing
  it took two minutes. **Confidence should not be set on a plan-completion forecast until
  the implied per-quarter run-rate has been worked out** — that check now belongs in the
  screen, not in the post-mortem.

**Forecast #2 now has an exact resolution test (added 2026-07-28).** It predicts HPG's Q2
core NPAT per tonne comes in **below ₫1.60m**. Until now the denominator was an estimate,
so the print could have been argued either way. HPG has since disclosed Q2 sales of **3.5m
tonnes**, which fixes it. The forecast therefore resolves cleanly at a headline core NPAT
of **₫5,600bn**: below that and the forecast is right, above it and it is wrong. Street
sits at ₫6,400–6,500bn, implying ₫1.83–1.86m/t. **Scoring this one must also apply the
Reason column strictly** — the pre-registered note in `hpg-spread-bridge.md` §7 says a Q2
beat is what the inventory lag predicts and is not evidence against the thesis. If the
forecast misses, it misses; that argument explains the timing, it does not rescue the call.

## Scored forecasts

_None yet — the first batch resolves with the Q2 filings this week (Jul 28–30)._

**Read that as a warning, not a placeholder.** Ten open forecasts and zero scored
means every confidence weight now driving the optimizer is an assertion, not a
measurement. The engine's arithmetic is sound; its inputs are so far unaudited by
reality. Treat the first scoring round as the moment this system starts being worth
something.

---

## Resolution rules, pre-registered 2026-07-29 03:53 — before the numbers land

Four forecasts resolve within days. Three of them **cannot be scored as written**, and
fixing that after the print would let the scoring be shaped by the answer. Rules below are
fixed now.

### #1 · KDH — the forecast as written is close to unfalsifiable

It predicts Q2 parent NPAT "between MBS ₫170bn and SSI ₫348bn." **That range spans 105% —
it is the entire width of published estimates.** Predicting that the answer falls somewhere
between the published estimates is not a forecast, and it must not score as a hit.

**Scored instead on two things that are genuinely falsifiable:**
- the **FY26 base case of ₫1,590bn**, which is a point estimate, when the year resolves;
- the **pre-registered units read** in `dossiers/KDH.md` §3, which maps a Q2 print to units
  handed (₫170bn ⇒ ~19 units, ₫259bn ⇒ ~27, ₫348bn ⇒ ~35) and is checkable against the
  Gladia inventory movement.

**The range itself is recorded as a process failure regardless of where the print lands.**
Writing down the consensus span and calling it a forecast is the habit this log exists to
catch.

**Attribution corrected 2026-07-29 04:53.** The range is right but one label was wrong: **MBS is
at ₫170bn**, **SSI is at ₫330bn** (not 348), and the **₫348bn** figure belongs to a third house,
possibly VCBS, unconfirmed. Score against the range as stated, but do not attribute the top end
to SSI. See `assumptions.json` → `kdh.actuals._FORECAST_ATTRIBUTION_CORRECTED_2026_07_29`, which
also records that the ₫348bn forecast's own revenue implies ~26 units against the ~35 our
pre-registered read maps to that profit — a disagreement to resolve from the statement, not from
our mapping.

### #2 · HPG — already exact, no change

Core NPAT below **₫5,600bn** on the disclosed 3.5m-tonne basket, which is below ₫1.60m per
tonne. Threshold fixed 28 July. Scoreable as it stands.

### #4 · MBB — needs a band

Written as "Q2/26 NPAT ≈ ₫7,052bn." "Approximately" is not scoreable. The figure cross-checks
correctly against the other estimate on file: ₫8,812bn pre-tax × 0.80 = ₫7,050bn.

**Rule: hit if the actual lands within ±10%, i.e. ₫6,347–7,757bn.** Outside that is a miss,
and the signed error gets recorded either way. Ten percent is chosen because it is roughly
the dispersion between broker estimates on this name — a tighter band would score noise, a
wider one would score nothing.

### #10 · Rebar — "no thesis change" needs a test

Written as "headline risk only, <3% of revenue, no thesis change." The first two clauses are
checkable; the third is not, as written.

**Rule: the forecast holds if all three are true.** The final antidumping rate on Hoa Phat is
within ±20pp of the 121.97% preliminary; the scope is not widened beyond rebar; and US rebar
remains under 3% of HPG revenue. **If the rate rises materially or the scope expands, it is a
miss** — and note that Commerce has preliminarily treated Dung Quat, Hai Duong, Hung Yen and
Prestressed Concrete as a **single entity**, so the rate applies group-wide rather than to one
subsidiary.

**One thing this cannot resolve.** `federalregister.gov` returns proxy 403 for both the site
and its API, so the determination will be read from press rather than the register. Score the
direction when it lands; treat the exact rate as T5 until a human confirms it from the source.


## Standing lessons

_Populated as patterns emerge across scored forecasts. Seeded with errors already
made and caught — they were real and they are worth not repeating._

| Date | Lesson | Where it changed the process |
|---|---|---|
| 2026-07-24 | Aggregating percentage P&L across positions instead of value-weighting understated the drawdown by ~5pp (−13.9% reported vs −18.8% actual). | Portfolio math now computed from cost and value, never from averaging percentages |
| 2026-07-24 | Assumed KDH's Gladia JV was equity-accounted; the Q1 statements showed full consolidation. A structural assumption was made without reading the note. | Ownership/consolidation basis is now read from the filing before any model is built |
| 2026-07-26 | Derived TTM earnings from estimated share counts; MBB's base came out ~35% low and produced a fictitious +85% expected return. | `npat_ttm` is now derived from the earnings path (H1 actual + prior H2), with a market-cap cross-check |
| 2026-07-26 | A load-bearing input (`npat_ttm`) can be wrong for a year without anything catching it, because nothing recomputes it. VCI's was 25.2% off and it flipped the sign of expected return. | The cross-check the method already mandates is now run whenever a name is screened, not only when prices refresh |
| 2026-07-26 | "+36% YoY" and "−26% QoQ" described the same VCI quarter. Every source reported the first. | Sequential change is computed alongside year-on-year for every earnings datapoint; a base effect is not a trend |
| 2026-07-27 | **Same error twice in two days.** VCI's `npat_ttm` was 25.2% low; VPX's is ~9-27% low, and VPX was ranked #1 on expected return because of it. Both are the two names whose TTM bases were set as rough early estimates rather than derived. A one-off is a mistake; twice in the same field is a method failure. | Every `npat_ttm` gets the mandated cross-check before it can drive a recommendation — not only when a name happens to be screened. TCX was control-checked and is fine, so the defect is bounded to VCI and VPX |
| 2026-07-27 | Logged a Fitch **forecast** for iron ore (US$115/t) as though it were the **spot price**, then built a cost bridge on it. Spot was US$98–104 and is US$97.70 today — ore never rose. The error made HPG's economics look near-breakeven when they were not. | Charter §3 already requires checking "filed actual / guidance / broker estimate" — that check now applies to **commodity prices too**, not just company earnings. A forecast and a price are different objects |
| 2026-07-26 | Applied a *peak* exit multiple to *peak* cyclical earnings on HPG, and to a non-repeating divestment gain. | Cyclical multiples are now inverted (low on peak, high on trough) and one-offs stripped before any multiple is applied |
| 2026-07-28 | A scheduled **operating disclosure** — HPG's half-year sales volumes — sat unlogged for about three weeks while hourly sweeps ran. The lanes hunt for *news*; nobody was watching the *calendar* of routine company releases, which are tier-T2 primary data and often more useful than the press coverage that follows them. | Recurring operating releases (monthly and quarterly volume/output disclosures) are now treated as dated catalysts to be checked on their schedule, not as news to be stumbled upon |
| 2026-07-28 | **Third input in three days to fail the period/entity checks.** VCI and VPX were both `npat_ttm`; VPB's is a credit balance. Because the third one is a different field, the pattern is not about `npat_ttm` at all — it is about numbers transcribed out of press summaries without pinning down which period and which entity they describe. VPB's block held a Q1-consolidated balance and an H1-parent growth rate side by side as if they were one quarter of one company, and the error was invisible until the two were divided into each other. | Any two fields in the same block that can be arithmetically checked against each other must be, at the time of entry. `credit_q2 / credit_start_fy - 1` had to equal `credit_growth_ytd` and never did |
| 2026-07-28 | **A single sentence contradicted itself and stood for a day.** The 27-Jul coking-coal note said 'SPOT 228, -24% MoM from 238.9 on 10-Jul' - but 238.9 to 228 is -4.6%. The consistency audit run that same morning checked FIELDS against each other and would never have caught this, because both numbers and the false percentage linking them sat inside one prose string. The error mattered: it produced a 'coal is collapsing, this is upside risk' reading when coal was in fact flat, and the corrected spread at spot is 0.60-0.68m/t rather than 0.83m/t - further below the bear branch, not closer. | Percentages stated inside prose notes get recomputed from the figures in the same sentence. A number written as narrative is still a number and gets the same arithmetic check as one written as a field |
| 2026-07-28 | **A near-miss of a different kind: nearly logged an unverified claim because it agreed with me.** A search summary said KDH's Gladia handover pace was 'slower than originally expected'. That would have corroborated the dossier's central finding - that every branch needs a 4x step-up on Q1's six units - and it sits beside an armed kill criterion on handover pace. The verification search did not confirm it and pointed the other way: the low-rise is complete and ready, title certificates were delivered as promised, and construction is described as on schedule. Every other error caught this week was a period, entity or measure mistake - mechanical, catchable by arithmetic. This one would have passed every mechanical check and failed only because the claim was CONVENIENT. | Charter section 3's rule 'never resolve ambiguity by picking the more interesting reading' now carries a second edge: when an unverified claim CONFIRMS an existing finding, that is a reason to verify harder, not a reason to relax. Flagged explicitly in the sweep summary rather than logged |

