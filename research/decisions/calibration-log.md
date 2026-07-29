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
| 2 | 2026-07-26 | HPG | Q2 core NPAT/tonne **below** ₫1.60m as the Formosa/iron-ore spread squeeze bites | bear p=0.45 | Q2 FS | ❌ **MISS — scored 29-Jul, see below** |
| 3 | 2026-07-24 | HPG | FY26 core NPAT (ex Pho Noi gain) ₫23.3tn base case | conf 0.60 | FY26 audited | ⏳ open |
| 4 | 2026-07-24 | MBB | Q2/26 NPAT ≈ ₫7,052bn (VCBS est.); FY26 base ₫30.5tn | conf 0.55 | Q2 FS (~Jul 28–30) | ⏳ open |
| 5 | 2026-07-24 | TCB | FY26 PBT ₫33.2tn base — **below** company guidance ₫35–37.5tn | conf 0.85 | FY26 audited | ⏳ open |
| 6 | 2026-07-24 | VPB | FY26 PBT ₫30.7tn base vs ₫41.6tn target — plan leans on VPBankS | conf 0.85 | FY26 audited | ⏳ open |
| 7 | 2026-07-24 | TCX | FTSE Sep-21 event EV ≈ +6.2%; base case "in-line, quiet digestion" p=0.45 | conf 0.80 | ~Oct 21 (1m after) | ⏳ open |
| 8 | 2026-07-24 | VPX | CAEX licence granted ~Q3 at p=0.40 | conf 0.70 | Q3/26 end | ⏳ open |
| 9 | 2026-07-24 | VCI | 9M PBT reaches ≥55% of FY target (the kill-criterion threshold) | conf 0.65 | Q3 FS (~Oct) | ⏳ open |
| 10 | 2026-07-23 | HPG | US rebar AD/CVD final ≈ headline risk only, <3% of revenue, no thesis change | conf 0.75 | ~Jul 28 Federal Register | ⏳ open |

### Annotations on open forecasts

**#10 · Rebar — the forecast measures two duties, not one. Clarified 2026-07-29 20:54.**
The forecast reads "US rebar AD/CVD final ≈ headline risk only, <3% of revenue, no thesis change".
Scoring it requires reading **both** rates, and they are very different animals: the **antidumping**
preliminary is **121.97%**, the **countervailing** preliminary is **1.08%** ad valorem. The two
finals are aligned to issue on the same date. So the CVD side is already effectively resolved in the
forecast's favour, and essentially the whole test rests on the AD final.

The date itself also came from Hoa Phat: it requested the postponement on 03-Mar-2026, moving the
final from "no later than 26-May" into late July. **The 28-Jul date elapsed with nothing published**,
so this forecast is not late in resolving — it has no published resolution to score against yet.

**#4 · MBB — a pre-print read registered 2026-07-29 19:53, before the statement.**
Forecast #4 resolves tomorrow. The on-file Q2 PBT estimate is ₫8,812bn, **+18% YoY**. Peers that
have now actually printed are running the other way: **ACB −12.06%** and **VIB −8.24%**, with
Saigonbank at a loss. The mechanism in ACB's numbers is specific and testable — **net interest
income +16.5%, profit −12%, the whole gap being provisions.** Sector provisioning is forecast +19%.

**So the registered read is: if MBB misses, expect it to miss on credit cost with net interest
income intact, not on revenue.** Recording it now rather than after the print is the whole point —
a mechanism identified afterwards is a story, identified beforehand it is a test. If MBB instead
misses on the top line, or beats outright, this read is wrong and gets scored as wrong.



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

### #2 · HPG Q2 core NPAT per tonne — **MISS**, resolved 2026-07-29

| Field | |
|---|---|
| **Forecast** | 26-Jul: Q2 core NPAT/tonne **below ₫1.60m**, as the Formosa/iron-ore spread squeeze bites. Bear branch p=0.45. Threshold fixed 28-Jul at ₫5,600bn core on the disclosed 3.5m-tonne basket. |
| **Actual** | Q2 NPAT **₫6,424bn** (+51% YoY), on 3.5m tonnes = **₫1.835m/t**. T1, filed 29-Jul. |
| **Direction** | ❌ Wrong side. Predicted below ₫1.60m; landed just under the **bull** branch of ₫1.85m. |
| **Error** | **+14.7%** above the ₫5,600bn threshold. Against the probability-weighted branch mean the miss is larger still, since bear carried p=0.45. |
| **Reason** | ❌ **Wrong, and wrong in a way that was visible before the print.** |

**The forecast contradicted my own analysis, and both were on file.** The `TIMING` note in
`hpg-spread-bridge.md` says plainly: ore and coal are bought one to two quarters forward, so Q2
burns cheap Q1 inputs and *"a strong Q2 print does NOT refute the bear thesis"* — the squeeze
lands in Q3. That note was written the same day as the forecast. **One said Q2 would be weak; the
other said Q2 could not yet be weak.** I never reconciled them.

The 28 July consistency audit checked *fields against fields* and found four errors. It never
checked a **forecast against a note**, which is where this one was hiding in plain sight.

**Lesson.** A forecast must be checked against every standing note on the same variable before it
is logged, not only against the data. Where a note explains why a period is uninformative, no
forecast should be registered on that period at all — the honest version of #2 would have been a
**Q3** forecast.

**What survives the miss.** The spread bridge's spot-persists arithmetic is untouched: at current
input prices it computes ₫0.60–0.68m/t, and the newly filed H1 makes the bear branch require
**exactly** that (H2 of ₫6,704bn over 7–9m tonnes = ₫0.745–0.958m/t). The thesis was mistimed, not
disproved. It now resolves in Q3, and that is where the next forecast belongs.


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
| 2026-07-29 | **A T1 regulatory change sat unrecorded for four weeks while hourly sweeps ran.** Circular 25/2026/TT-NHNN raised the cap on short-term funding usable for medium- and long-term lending from 30% to 40%, issued 22-Jun and effective 01-Jul. It bears on 71.8% of the book — banks 51.5% plus KDH 20.3% — and it directly relaxes the constraint behind the 'H2 looks demanding' framing recorded for both VPB and MBB. It was published in the government gazette, so it was dated, scheduled, primary and findable the whole time. It surfaced only as a side clause in a market recap run for a different lane. **This is the second instance of the same failure in two days**, after HPG's half-year volume disclosure sat unlogged for three weeks. | **Scheduled primary sources are checked on a calendar, not hunted as news.** The lanes are built to find things that *happened*; a circular that is gazetted on a known date never 'happens' in that sense and so is never found. Lane 5 nominally covers SBV/MoF circulars — nominal coverage was worth nothing without a schedule. Regulator gazettes now join recurring operating disclosures as dated catalysts to be checked on their own cadence. |
| 2026-07-29 | **Fifth period mislabel in four days, and the closest to landing.** A search summary opened: 'KDH core profit in **Q2 2026** reached approximately 53bn, declining 57% YoY, due to Gladia handover delays.' Past tense, a specific figure, a stated cause — it read exactly like the print that resolves forecast #1, one day before that print is due. It is **Q1**: the summary's own next paragraph dates the 53bn by the 285bn extraordinary gain and the 6 units handed, both unmistakably Q1 and both already on file, and the underlying article is dated 01-Jul and titled 'brokers diverge in Q2 **forecasts**'. The lede attached the wrong quarter to a number its own body dated correctly. | **Never believe a summary's opening sentence about a period without reading the rest of the summary.** The lede is where the period error lives, because that is the sentence written by whoever compressed the article. Where the body supplies dating evidence — a named one-off, a unit count, an article date — that evidence outranks the lede's label. Applied here it also produced a free cross-check on a number we hold, which is the second reason to read on rather than stop at the headline. |
| 2026-07-29 | **First scored forecast is a miss, and it was self-inconsistent before the print.** HPG forecast #2 predicted Q2 core NPAT/tonne below 1.60m; it came in at 1.835m. But the spread bridge's own TIMING note, written the same day, said Q2 burns cheap Q1 inputs and a strong Q2 does NOT refute the thesis. The forecast and the note contradicted each other and both sat on file for three days. The 28-Jul consistency audit checked fields against fields and would never have caught it. | Before a forecast is logged it gets checked against every standing NOTE on the same variable, not just against the data. Where a note explains why a period is uninformative, no forecast is registered on that period - it is registered on the period that actually tests the thesis |

