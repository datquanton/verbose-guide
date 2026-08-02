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
| 1 | 2026-07-24 | KDH | Q2/26 parent NPAT between MBS ₫170bn and SSI ₫348bn; base case FY26 NPAT ₫1,590bn | conf 0.50 | Q2 FS (~Jul 28–30) | ❌ **MISS — scored 30-Jul, see below** |
| 2 | 2026-07-26 | HPG | Q2 core NPAT/tonne **below** ₫1.60m as the Formosa/iron-ore spread squeeze bites | bear p=0.45 | Q2 FS | ❌ **MISS — scored 29-Jul, see below** |
| 3 | 2026-07-24 | HPG | FY26 core NPAT (ex Pho Noi gain) ₫23.3tn base case | conf 0.60 | FY26 audited | ⏳ open |
| 4 | 2026-07-24 | MBB | Q2/26 NPAT ≈ ₫7,052bn (VCBS est.); FY26 base ₫30.5tn | conf 0.55 | Q2 FS (~Jul 28–30) | ❌ **MISS — scored 31-Jul, see below** |
| 5 | 2026-07-24 | TCB | FY26 PBT ₫33.2tn base — **below** company guidance ₫35–37.5tn | conf 0.85 | FY26 audited | ⏳ open |
| 6 | 2026-07-24 | VPB | FY26 PBT ₫30.7tn base vs ₫41.6tn target — plan leans on VPBankS | conf 0.85 | FY26 audited | ⏳ open |
| 7 | 2026-07-24 | TCX | FTSE Sep-21 event EV ≈ +6.2%; base case "in-line, quiet digestion" p=0.45 | conf 0.80 | ~Oct 21 (1m after) | ⏳ open |
| 8 | 2026-07-24 | VPX | CAEX licence granted ~Q3 at p=0.40 | conf 0.70 | Q3/26 end | ⏳ open |
| 9 | 2026-07-24 | VCI | 9M PBT reaches ≥55% of FY target (the kill-criterion threshold) | conf 0.65 | Q3 FS (~Oct) | ⏳ open |
| 10 | 2026-07-23 | HPG | US rebar AD/CVD final ≈ headline risk only, <3% of revenue, no thesis change | conf 0.75 | ~Jul 28 Federal Register | ✅ **HIT — scored 30-Jul, see below** |

### Annotations on open forecasts

**#10 · Rebar — the final ISSUED 29-Jul-2026. Not scored: the rates are not in hand. Read
pre-registered 2026-07-30 03:53.**
Commerce issued the final determinations for Vietnam, Egypt and Bulgaria on 29-Jul. The rates are not
yet obtainable — `federalregister.gov` 403s from here and Vietnamese press still quotes preliminaries.

**The read, registered before the numbers arrive.** Provisional duties near 122% have been collected
since March, under the extension HPG itself requested. **HPG has therefore already traded a full
quarter under them, and that quarter printed revenue +53% and NPAT +51%.** The commercial effect of
losing US rebar is already inside the reported run-rate rather than ahead of it. If the forecast
scores as a HIT, *this* is the reason it should be credited to — not "the rate came in low."

**And the scoring trap is explicit:** four numbers circulate for this one case — petition 117.61%,
HPG preliminary 121.97%, all-others preliminary 130.77%, and the unpublished final. **Only Hoa Phat's
final rate scores this forecast.** Press already headlines "130%" alongside Hoa Phat's name; that is
the all-others rate and must not be used.

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

**~~Strengthened 2026-07-30 09:53~~ — WITHDRAWN 2026-07-30 20:54, still before the print.** I
strengthened this read from "peers suggest" to "MBB was already doing this", on the basis of press
describing MBB's Q1 as having *"a sharp increase in risk provisioning"*. **I now have the number and
it does not support that.** MBB's Q1 provisioning was **₫3,455bn, +15.7%** — against Q1 PBT of
**+14.8%**. Provisioning grew **in line with the business**, not disproportionately.

**That is not the ACB pattern.** ACB's Q2 had net interest income **+16.5%** and profit **−12%** —
provisions overwhelming a growing top line. MBB's Q1 shows nothing of the kind.

**The original read stands on its own footing**; it rests on ACB and VIB actually printing −12% and
−8%, which is unchanged. What does not stand is the claim that MBB itself was already showing the
pattern. **Withdrawn before the print, because withdrawing it afterwards would be indistinguishable
from retrofitting.**

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

### #1 · KDH Q2/2026 — **MISS**, and by a factor of five on the part that was falsifiable

**Resolved 2026-07-30.** Q2 revenue **₫161bn (−85% YoY)**; H1 revenue ₫442bn (−75%); H1 net profit
**₫321bn (−6%)** against Q1 of ~₫327bn, so **Q2 profit was approximately zero**.

**Scored against the pre-registered rule, not the range.** That rule already declared the stated
range (₫170–348bn) close to unfalsifiable and said it must not score as a hit. It does not — but it
is worth recording that **even a range spanning the entire published consensus was missed, on the
low side.** Every house was too high; VCBS's ₫1,123bn revenue forecast was **seven times** the ₫161bn
outcome.

**The falsifiable part was the units read**, which mapped ₫170bn ⇒ ~19 units, ₫259bn ⇒ ~27,
₫348bn ⇒ ~35. **Actual: ₫161bn of revenue at ₫42–44bn ASP is ~3.7–3.8 units.** The mapping was
**five times too high at its most conservative point.**

**Right in direction, badly wrong in calibration — and that is the finding.** The dossier's
bull-infeasibility work was pointing the right way: it said handovers could not reach the bull case,
and handovers indeed collapsed. But *every* branch, including bear at 80 units for the year, is now
far above the run-rate — roughly **10 units handed in H1 against a bear branch needing 80**. Being
directionally right while the entire scenario tree sits above the outcome is not a success. **The
tree was calibrated off Q1's six units and a sold book, and never off the possibility that handovers
would simply stop.**

**What actually happened, per the filing:** financial costs ×3 and selling expenses ×2.9, on payment
discounts and customer-support costs. **The company was discounting hard and still not handing over
units.** H1 operating cash flow ≈ **−₫2,580bn**, borrowings **+₫6,500bn**, inventory **>₫23,000bn**.

**Process note recorded regardless of outcome, as the rule required:** writing down the consensus
span and calling it a forecast was a process failure. It has now also proved an expensive one — the
span was wide enough to feel safe and still missed.

### #10 · US rebar final — **HIT**, and right for the stated reason. First hit of three scored.

**Resolved 2026-07-30.** Federal Register **2026-15438** (AD) and **2026-15437** (CVD), both applicable
30-Jul. **Final dumping margins for Vietnam 128.53%–136.57%**, cash deposit rates **123.49%–131.53%**
after an export-subsidy offset. Preliminary was 121.97%–130.77%.

**The rate went the "wrong" way and the forecast still holds — which is the right outcome for the
right reason.** The forecast did not predict the rate; it predicted the *impact*: "headline risk only,
<3% of revenue, no thesis change." Duties near 122% have been collected since March under the
extension HPG itself requested, so **HPG already traded a full quarter under them — and that quarter
printed revenue +53% and NPAT +51%.** Moving a prohibitive duty from ~122% to ~129% changes nothing
commercially. The trade was already uneconomic; the earnings effect is already in the run-rate.

**Not over-credited.** Two caveats are recorded rather than glossed. First, **the finals came in ~6.6pp
higher at both ends**, so anyone reading the forecast as "the rate will be mild" would have been
wrong — it was the *impact* claim that carried it. Second, **which end applies to Hoa Phat is not
confirmed**: the preliminary structure put the mandatory respondent at the lower rate, so 128.53% is
the likely figure, but that is inference from structure, not a reading of the table.
`federalregister.gov` 403s from this environment, so the rates are T5 trade press on a T1 document.

### #4 · MBB Q2/2026 — **MISS**, on the high side, and the pre-registered read is **wrong**

**Resolved 2026-07-31**, one day past the Circular 96/2020 deadline. Q2 PBT **₫10,560bn, +40%**;
Q2 NPAT-to-parent **₫8,229.06bn, +40.01%**; H1 NPAT-to-parent **₫15,744.58bn, +26.51%**.

**Scored on the forecast's own measure.** The pre-registered band was ₫6,347–7,757bn, and the
₫7,052bn centre was derived as ₫8,812bn PBT × 0.80 — i.e. **consolidated NPAT**, not
parent-attributable. Like for like, actual consolidated NPAT is ₫10,560 × 0.80 = **₫8,448bn**:
**+19.8% above the forecast**, ₫691bn outside the band. On parent-attributable the error is +16.7%.
**Miss on either measure**, and the band was chosen at ±10% precisely so that a 20% error could not
be argued into a hit afterwards.

**The pre-registered read is scored WRONG, on its own terms.** It read: *"if MBB misses, expect it
to miss on credit cost with net interest income intact, not on revenue"* — with the explicit
stipulation *"if MBB instead misses on the top line, or beats outright, this read is wrong and gets
scored as wrong."* **MBB beat outright.** Net interest income rose 36.55% to ₫16,893.65bn and profit
rose faster still. The conditional never triggered, and the clause that pre-committed to calling that
a failure is the reason this is recorded as one rather than quietly retired as "not applicable."

**Where the read came from, and why it failed.** It was built on a peer read-across: ACB printed Q2
PBT **−12%** on sharply higher provisions with net interest income +16.5%, and VIB **−8%**. The
inference was a sector provisioning cycle. **MBB printed +40% in the same quarter.** Same sector,
same quarter, same rate environment, opposite outcome — a spread of roughly **52 percentage points**
between ACB and MBB. NPL did drift up, 1.42% → 1.45%, but coverage *rose* 92.24% → 93.63%, which is
the opposite of a bank being forced to provide.

**So the read-across is the finding, not the miss.** The miss itself is unremarkable — a broker was
20% low. What is worth keeping is that **"peers are showing X, therefore this bank will show X" was
tested prospectively and failed**, on three banks in one quarter, and that the 30-Jul withdrawal was
correct for the right reason: when MBB's *own* Q1 provisioning turned out to be +15.7% against PBT
+14.8%, the bank-specific evidence contradicted the peer inference, and the bank-specific evidence
was right.

**One thing this does not resolve.** H1 provisioning is still unknown — the figure circulating in
Q2-context coverage was the Q1 number reappearing (see `assumptions.json`
`_TWO_FIGURES_IN_THE_SAME_COVERAGE_WERE_STALE_2026_07_31`). So the *mechanism* the read named is
still unmeasured; only its *conclusion* has been falsified.

**And the forecast's second clause is now live against the print.** "FY26 base ₫30.5tn" implies FY
PBT ₫38,125bn. H1 PBT is **₫20,188bn**, so the base branch requires H2 to **fall 11.2%** and the bear
branch to fall 26.6%, against a market whose bank profits are seasonally second-half weighted.
**That is not a miss on a forecast, it is a scenario tree that has stopped discriminating** — which
is exactly what the 28-Jul pre-registered H2 table said the ≥₫20,000bn row would mean. Escalated for
a human rebuild; branch re-derivation is not an automated edit.

**Scored 1 hit, 3 misses across four resolved forecasts.**

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
| 2026-07-30 | **Nearly inverted my own pre-registered test on a ticker collision.** A search returned "MBB raises full-year margin outlook after Q2 earnings jump" — **MBB SE, a German holding company on Xetra**, EBITDA +62% to €75.2m. Logging it as ours would have recorded the exact opposite of the read registered for forecast #4 (*miss on credit cost, net interest income intact*), hours before the real statement resolves it. The string "MBB" pulls at least three entities: MB Bank, MB Securities, and MBB SE — plus Poland's mBank in the same result set. | **Verify when evidence CONTRADICTS you, not only when it confirms you.** The 28-Jul lesson covered convenient claims; this is its mirror. Dismissing inconvenient evidence unexamined is the same failure with the opposite sign — and it is more tempting once a position is registered in writing. Operationally: **any ticker-only headline gets an exchange check before a period check.** |
| 2026-07-30 | **Built on an adjective three times in one day.** "Declining revenue" (KDH, morning), "sharp increase in provisioning" (MBB, midday), and a rejected figure I called "impossible" (KDH, evening) were all qualitative phrases treated as if they carried numbers. When the figures arrived they went the other way twice: KDH's ₫281.4bn was revenue, and MBB's provisioning was **+15.7% against PBT +14.8%** — in line with the business, not the ACB pattern I claimed it was. | **Get the figure before building on the adjective.** A press characterisation — "sharp", "strong", "declining" — is a lead to a number, never a substitute for one, and it must not be used to strengthen a registered position. Where a claim is strengthened on qualitative evidence and the number later fails to support it, **the withdrawal happens before the resolving event**, not after. |
| 2026-07-30 | **Forced two numbers to be incompatible, having forced two others to be identical twelve hours earlier.** In the morning I decided KDH's ₫281.4bn revenue and ₫281.0bn derived profit were the same number; they were not. In the evening I declared a reported Q2 profit of ₫770bn "internally impossible" against H1 of ₫321bn; it is irreconcilable **on one measure basis**, but total NPAT versus parent NPAT would reconcile it, and KDH fully consolidates JVs it part-owns. **Same failure, opposite sign.** | **Hold open the possibility that two figures are different quantities — in both directions.** A near-match is not a match; a contradiction is not an impossibility. Before collapsing two numbers into one *or* declaring them incompatible, name the measure each is on. Where the measure cannot be established, the finding is "these do not reconcile on basis X", never "this one is wrong". |
| 2026-07-30 | **Counted one route three times and called it corroboration.** Across three sweeps I escalated KDH's `q1_revenue` from "suspected mislabel" to "THREE ROUTES NOW AGREE" that ₫281.4bn was net profit. It is revenue — a source gives net revenue ₫281.4bn (−60.4%) and profit ₫327bn (+175.5%) as separate figures. **All three of my routes traced back to the same ambiguous press phrasing**, and one of them inverted its meaning: the clause "despite declining revenue... 281" meant revenue declined *to* 281.4, not that profit was 281. I also treated ₫281.0bn (arithmetic) as matching ₫281.4bn (stated). The file's original counter-argument — 6 units × ₫42–44bn ≈ ₫252–264bn, consistent with a real revenue line — was sound and I overrode it. | **Independence of confirming routes must be checked, not assumed. The count of confirmations is not the strength of the evidence.** Before a claim is escalated on multiple routes, each route is traced to its origin; routes sharing a source are one route. And a near-match is recorded as a near-match — ₫281.0bn ≠ ₫281.4bn was the tell, present from the start. |
| 2026-07-29 | **Built two entries on a date I never checked, and the correct date was already in the repo.** The `cash_yield` note said MBB's cash "went ex on 10-Jun-2026"; the record date was **10-Jul**, payment from **17-Jul**. Two log entries repeated it, and one made "TCB and MBB paid on the same day" the centre of its argument. The private dashboard's MBB card had said "paid 17-Jul" the whole time — **one fact recorded two ways in two places, and the sweep reached for the wrong copy.** The underlying finding survived (three past-paid dividends, one credited) but the framing was false. | **A date inherited from a note is not evidence; it is a claim to verify like any other.** Dates lifted from existing repo prose now get the same period check as dates from a search. And where the same fact lives in two files, the sweep reconciles them rather than picking one — the charter's warning that duplicated *rules* drift applies identically to duplicated *data*. |
| 2026-07-29 | **A "pending" flag with no date on it rots silently.** TCB's corporate action was carried as "7% cash + 60% bonus pending"; the cash half was paid 10-Jun-2026 and the flag looked exactly as valid seven weeks later as the day it was written. Checking the two names recorded the same way found the same defect on VPB, which had **also** paid cash — ₫500/share on 25-May — with no record of it anywhere in the repo. The consequence was not cosmetic: `cash_yield` credits TCB 2.39% *because* the dividend was believed pending, while excluding MBB's identical 10-Jun payment as "already past". **One name credited, two identically-situated names not, all three banks.** | **Every status flag carries the date of the event it describes, not the date it was written.** "Pending" is not a state, it is a claim about a future date, and a claim about a date that omits the date cannot be checked or expired. Applied immediately: when one stale flag is found, every other flag written in the same form gets checked in the same sweep — which is how VPB's was found an hour after TCB's. |
| 2026-07-29 | **A T1 regulatory change sat unrecorded for four weeks while hourly sweeps ran.** Circular 25/2026/TT-NHNN raised the cap on short-term funding usable for medium- and long-term lending from 30% to 40%, issued 22-Jun and effective 01-Jul. It bears on 71.8% of the book — banks 51.5% plus KDH 20.3% — and it directly relaxes the constraint behind the 'H2 looks demanding' framing recorded for both VPB and MBB. It was published in the government gazette, so it was dated, scheduled, primary and findable the whole time. It surfaced only as a side clause in a market recap run for a different lane. **This is the second instance of the same failure in two days**, after HPG's half-year volume disclosure sat unlogged for three weeks. | **Scheduled primary sources are checked on a calendar, not hunted as news.** The lanes are built to find things that *happened*; a circular that is gazetted on a known date never 'happens' in that sense and so is never found. Lane 5 nominally covers SBV/MoF circulars — nominal coverage was worth nothing without a schedule. Regulator gazettes now join recurring operating disclosures as dated catalysts to be checked on their own cadence. |
| 2026-07-29 | **Fifth period mislabel in four days, and the closest to landing.** A search summary opened: 'KDH core profit in **Q2 2026** reached approximately 53bn, declining 57% YoY, due to Gladia handover delays.' Past tense, a specific figure, a stated cause — it read exactly like the print that resolves forecast #1, one day before that print is due. It is **Q1**: the summary's own next paragraph dates the 53bn by the 285bn extraordinary gain and the 6 units handed, both unmistakably Q1 and both already on file, and the underlying article is dated 01-Jul and titled 'brokers diverge in Q2 **forecasts**'. The lede attached the wrong quarter to a number its own body dated correctly. | **Never believe a summary's opening sentence about a period without reading the rest of the summary.** The lede is where the period error lives, because that is the sentence written by whoever compressed the article. Where the body supplies dating evidence — a named one-off, a unit count, an article date — that evidence outranks the lede's label. Applied here it also produced a free cross-check on a number we hold, which is the second reason to read on rather than stop at the headline. |
| 2026-07-29 | **First scored forecast is a miss, and it was self-inconsistent before the print.** HPG forecast #2 predicted Q2 core NPAT/tonne below 1.60m; it came in at 1.835m. But the spread bridge's own TIMING note, written the same day, said Q2 burns cheap Q1 inputs and a strong Q2 does NOT refute the thesis. The forecast and the note contradicted each other and both sat on file for three days. The 28-Jul consistency audit checked fields against fields and would never have caught it. | Before a forecast is logged it gets checked against every standing NOTE on the same variable, not just against the data. Where a note explains why a period is uninformative, no forecast is registered on that period - it is registered on the period that actually tests the thesis |

| 2026-07-31 | **A peer read-across was tested prospectively and failed by 52 percentage points.** ACB printed Q2 PBT −12% and VIB −8%, both on provisioning; I registered a read that MBB would show the same shape. **MBB printed +40%**, with net interest income +36.6% and NPL coverage *rising* 92.24% → 93.63%. Three banks, one sector, one quarter, opposite outcomes. The read survived a week because it was never stated as what it was: an inference about a *sector*, applied to a *bank*, with no channel named through which the sector effect would reach that bank's book. | **A peer read-across is a hypothesis about a shared mechanism, and it must name the mechanism and the exposure before it is registered.** "Peers are showing X" is a reason to go and measure the bank's own credit cost, not a substitute for measuring it. Where bank-specific evidence contradicts the peer inference — as MBB's own Q1 provisioning did, +15.7% against PBT +14.8% — **the bank-specific evidence outranks it**, and the withdrawal happens then, not after the print. That sequencing is the one part of this that worked. |
| 2026-07-31 | **A new figure that exactly equalled an old one was almost logged as new.** Q2-context coverage of MBB's filing carried "provisioning ₫3,455bn (+15.7%)" and "customer loans ₫1.12 million tỷ (+3.3%)" alongside genuine Q2 figures. **Both were the Q1 numbers already in this file, to the digit** — `q1_provisions` 3,455, `q1_provisions_yoy` 0.157, `q1_credit_growth_ytd` 0.033 — while the true Q2 loan figure was ₫1.22 million tỷ at +13.2% YTD. The provisioning one was the more dangerous: provisioning is the exact mechanism the pre-registered read named, so logging it would have manufactured a test the evidence could not support. | **Exact equality with a figure already on file is a period flag, not a corroboration.** Charter §3's period check now runs specifically against the file's own prior-period values, not only against the source's labelling — the tell here was internal, available without any further search, and it is the cheapest check in the list. Note what passed the same test and was kept: NPL 1.45% and coverage 93.63% were both stated *as changes from* the Q1 values, which is what a genuine new-period figure looks like. |
| 2026-07-31 | **Two scenario trees failed in one week in opposite directions, and the confidence field could not express either.** KDH's branches were contradicted from *above* — Q2 profit ≈ zero against a bear branch needing 80 units a year. MBB's are contradicted from *below* — H1 PBT ₫20,188bn leaves the base branch requiring H2 to fall 11.2% and the bull branch needing +4.3%, in a market where bank profit is second-half weighted. In both cases the routine's rule (estimate → actual raises confidence) would have *amplified branches the print had just invalidated*, flattering a bad quarter in one case and understating a good one in the other. | **`confidence` multiplies `fy26e_npat`, so it can only be raised when the branches are still believed.** Where a print invalidates the branches in either direction, the correct action is to escalate for re-derivation, never to move the scalar. For MBB no deviation was needed — charter §2 already forbids raising confidence on T5 press about a filing, and that rule was applied here exactly as it was on 29-Jul. **The rule that stops you being flattered is the same rule that stops you being conservative; it has to bind in both directions or it binds in neither.** |
| 2026-07-31 | **Escalated a date correctly and described it wrongly, three hours before the event.** At 15:53 I fired trigger 5 on TCX's VN30 entry with *"joins VN30 on MONDAY 3 AUGUST. Today is the last session before it."* The index date was right; **the flow date was not.** VN30 ETFs completed their rebalance on **31-Jul**, the session *before* the 3-Aug effective date — the standard mechanic. The buying was that same afternoon, and anyone acting on my wording would have been a session late. The date gate had carried "3-Aug" since 26-Jul and was never wrong about the index, only about when money moves. | **An effective date is not a flow date, and a dated catalyst is not one date but two.** Every dated catalyst on the gate table now gets asked which date it is — the announcement, the money, or the effect — because they routinely differ and only one of them is tradeable. Applied immediately to the two remaining index items: **FTSE Sep-21 is an effective date phased in tranches to Sep-2027**, so it has no single flow date at all, which is the same defect the 28-Jul entry found in the FTSE event tree from the opposite direction. |
| 2026-07-31 | **Wrote a lesson about a fact living in two files, then left the second copy wrong for two days.** The 29-Jul lesson reads *"where the same fact lives in two files, the sweep reconciles them rather than picking one"* — and it was written about the MBB dividend date. The correction ("TCB and MBB paid on the same day" is **withdrawn, never true**; MBB was record 10-Jul, payment 17-Jul) went into `assumptions.json` on 29-Jul 23:53. **`OPEN-DECISIONS` item 3 still carried the withdrawn argument verbatim on 31-Jul** — in §1, "Blocking a live recommendation", on the 35% position proposed for a 15pp cut. | **A withdrawal is not complete until every copy of the claim carries it, and the index file is the copy that matters most.** When a claim is withdrawn, the same sweep now greps the repo for its distinctive phrasing rather than editing only the file it was found in. Note what let it survive: **the same-day coincidence was rhetorical, not load-bearing** — the substantive finding stood without it, so nothing broke and nothing flagged. **Decorative claims are the ones that rot**, because no downstream number depends on them and no check touches them. |
| 2026-07-31 | **A lesson about missing gazetted regulations failed to catch the next gazetted regulation, three days later.** The 29-Jul lesson — written after Circular 25/2026/TT-NHNN sat unrecorded for four weeks — said *"regulator gazettes now join recurring operating disclosures as dated catalysts to be checked on their own cadence."* On 31-Jul, **HCMC Decision 45/2026/QĐ-UBND** was found in force since **01-Jul-2026**, setting the land-price adjustment coefficient that drives land-use fees for **KDH, 20.3% of the book**. Zero hits for it, or for "land-use fee", "bảng giá đất" or "hệ số K", anywhere in the repo. **Both instruments took effect on the same date and both were missed.** | **A lesson scoped to the regulator that produced it does not generalise on its own.** "Check regulator gazettes" was read as *SBV* gazettes, because SBV was what triggered it. The fix is to name the regulators per holding rather than the category: **SBV and MoF for the banks and brokers, HCMC/provincial People's Committees and MoNRE for KDH, MoIT and USITC/Commerce for HPG** — each with its own cadence. And **effective dates cluster**: 01-Jul-2026 carried at least two instruments bearing on 71.8% and 20.3% of the book respectively, so quarter and half-year boundaries get swept as dates, not waited on as news. |
| 2026-08-01 | **Stopped at a reconciliation that worked, and it was the wrong one — caught by one more search.** TCB's model implied credit +14.46% against a recorded "+10.39% credit growth", and the 28-Jul note resolved the 4.1pp gap by concluding the **corporate bond book had shrunk**. The rates were assigned to the wrong measures: **+10.4% is customer loans, +14.3% is credit including quota-exempt infrastructure and social housing.** Credit grew *faster*, so the non-loan part **expanded**. Worse, the inverted version produced a ~₫40,700bn gap sitting beside the ₫39–40,000bn of real-estate exposure TCB cut and the ₫44,500bn Masterise raised — **an arithmetically seductive Masterise story that the source explicitly contradicts by naming the gap as quota-exempt lending.** | **A reconciliation that works is not the same as the right one, and the more satisfying it is the harder it must be checked.** Both the 28-Jul error and the near-miss came from finding *an* explanation for a numeric gap and stopping. Where a gap is closed by inference, the sweep now looks for the issuer's own wording of what the gap *is* before building on it — here one further search returned the exact clause and killed both readings. Note the shape: the false version was **quantitatively closer** to the on-file numbers than the true one, because 40,700 ≈ 39–40,000 ≈ 44,500 is the kind of coincidence a large balance sheet produces constantly. |
| 2026-08-01 | **Fourth dated regulation found in force with no record in the repo, and the lesson written two days ago still did not catch it.** Circular 25/2026 (four weeks late, found 29-Jul) → HCMC Decision 45/2026 (one month, found 31-Jul) → **Circular 08/2026/TT-NHNN, issued MAY 2026 — three months** — plus the SBV credit-quota exemptions for 25 banks and 18 projects. The 31-Jul fix was to *"name the regulators per holding rather than the category"*, and SBV **was** named. It still missed, because the sweep looks for regulations that bear on a *thesis* and Circular 08 bears on a *ratio nobody was tracking* (LDR) — it only became visible once the night's own funding-gap entries created a reason to care. | **Naming the regulator is not enough; the gazette has to be swept on its own cadence regardless of whether a question is currently live.** Every miss so far was findable, dated and primary the whole time, and each was found only when something else made it relevant. That is the definition of a source being hunted as news rather than checked on a calendar. Concretely: **SBV and MoF circulars get a monthly back-sweep of the preceding quarter**, not a search when a thesis needs one. Note the second-order damage this one did — the exemptions mean **credit-growth rates are not comparable across banks**, and this file had been comparing them all week. |
| 2026-08-01 | **Two sources gave one event different technical labels, and the file assumed one of them was wrong.** VPB's 26% was described as both *cổ phiếu thưởng* (bonus shares, from owner's equity) and *cổ tức cổ phiếu* (stock dividend, from retained earnings), and the 29-Jul note recorded the label as "not yet pinned" on the assumption that one description was an error. **Both were correct at different times: the AGM approved a bonus issue on 22-Apr and shareholders amended it into a stock dividend by written poll in July.** The instrument changed. | **When two sources give one event different *technical* labels, check whether the thing itself changed between them before deciding a source is wrong.** A label conflict is a question about *time* as often as about accuracy — and the dates were available in both cases. Note this is the mirror of the 30-Jul lesson about counting one route three times: there, apparent corroboration hid a single source; here, apparent contradiction hid two real events. **Both failures come from comparing statements without first placing them on a timeline.** |
| 2026-08-01 | **Offered an illustrative range for an unknown quantity, and it was 5–12× too high.** Unable to find KDH's VNDiamond weight, I wrote *"at an illustrative 3/5/7% it would be ₫375/624/874bn of forced selling"* and labelled it explicitly as illustration rather than estimate. **The real figure is ~₫72bn.** The caveat was honest and the numbers still misled, because a reader takes magnitude from digits, not from the sentence around them. | **When a quantity is unknown, say it cannot be sized and stop — do not demonstrate the arithmetic with invented inputs.** An illustration anchors at whatever it happens to be, and the anchoring survives the disclaimer. This is the same failure as the 27-Jul iron-ore error in a different costume: there a *forecast* was logged as a *price*; here an *illustration* functioned as an *estimate*. **Both come from letting a number into the record whose provenance is weaker than its precision suggests.** |
| 2026-08-02 | **Mis-dated this file's own entry by a day, at the one hour where that is possible.** The 23:53 ICT sweep on 1-Aug was filed under a `## 2026-08-02` heading, and its lead sentence described a rule effective 01-Aug as taking effect "yesterday". **This is the file that spent the week cataloguing ten period errors in other people's numbers.** | **An hourly routine crossing midnight changes the date, and 23:53 is the single slot per day where that is live.** The date on an entry is now derived from the sweep hour rather than carried over from the previous entry's heading. Note the shape: every period error logged this week was in *incoming* data, and the checks were all built to face outward. **A check that only points at sources does not catch the file's own hand.** |
| 2026-08-02 | **Dismissed a correct number as "internally impossible", then spent ten days building on the wrong one.** On 30-Jul a reported KDH Q2 profit of ₫770bn was called impossible against an H1 of ₫321bn. **₫770bn is the correct consolidated figure**; ₫321bn is on some other basis (core, ex-gain, or parent). From the bad input I derived "Q2 profit ≈ zero", which then scored forecast #1 a MISS, drove a "branches contradicted from above" escalation, and framed KDH as the quarter's disaster. **The withdrawal took three attempts** — partial on 30-Jul, "under-done in force" on 02-Aug 02:53, and complete only here. | **When an outside figure contradicts a derived one, suspect the derivation first — it is the one whose inputs you control and therefore the one you can be wrong about privately.** The 30-Jul entry had the right instinct (*"irreconcilable on one measure basis, not impossible"*) and then kept reasoning from the derived number anyway. **A caveat that does not change what you do next is decoration.** Operationally: a derived figure that conflicts with a reported one is not evidence against the report until its own inputs have been re-verified — and here they never were, for ten days. |
| 2026-08-02 | **Flagged a derivation as an estimate, then built firm conclusions on it and flagged none of those.** The 31-Jul entry derived TCBS's equity at ~₫33,018bn and said so explicitly: *"1.56× is an estimate built on file figures, not a filed number... the precise utilisation needs TCBS's reported equity."* **The caveat was exemplary and it protected nothing.** The same entry then wrote *"more than three-quarters drawn against its regulatory limit"*, *"the margin line cannot grow much faster than equity does"* and *"the name with the least headroom is the one the engine ranks first"* — as findings, unhedged, and they propagated into the next day's CCP entry as settled fact. Filed equity is **₫45,782bn**; the derivation was **39% low**, headroom is **₫40,064bn not ₫14,500bn**, and every one of those sentences is now withdrawn. | **A caveat attaches to a number, not to the sentences downstream of it — so the caveat has to be restated at every conclusion, or the conclusion has to inherit the hedge in its own words.** This is the 02-Aug KDH lesson (*"a caveat that does not change what you do next is decoration"*) meeting the 31-Jul one about decorative claims rotting, and the shape is worse here: the hedge was on the *input* while the *output* was stated flatly, which is precisely the arrangement that lets an estimate launder itself into a fact one entry later. Operationally: **when a note says "escalated, not modelled", the conclusions in that same note get marked provisional too — and when the real figure lands, the sweep greps for those conclusions rather than only correcting the field.** |
| 2026-08-02 | **Three values for one quantity sat in this repo simultaneously and no check looked for that.** `assumptions.json` carried `tcx.actuals.margin_equity_pct` = **0.98**; the 31-Jul log carried **1.56×**; the filed figure is **1.125×**. **The two file values bracket the truth and neither is it**, and they differ from each other by 59% — a disagreement visible without any search, in two files, for two days. The 29-Jul lesson already said *"where the same fact lives in two files, the sweep reconciles them rather than picking one"*; it was written about a **date** and read as being about dates. | **The reconcile-duplicates rule is about quantities, not just dates, and it needs a mechanical trigger rather than good intentions.** Concretely: when a sweep touches any field, it greps the log for the same quantity expressed as prose and checks the two agree — the tell here was a ratio stated three ways, and ratios are the easiest thing in the file to cross-check because they are one division. Note this is the **third** time a lesson failed to generalise past the example that produced it (SBV→all regulators, dates→all facts, and now dates→quantities). **The pattern is that a lesson written from one instance inherits that instance's category, so the lesson now states the category explicitly and names what else falls in it.** |
| 2026-08-02 | **A correction with no news in it moved a live kill criterion from 24.5% away to 3.8% away.** Nothing happened to TCBS, no price moved, and no forecast resolved — a **denominator** was replaced with a filed one. `decide.py`'s TCX criterion is *"P/B < 2.0x on unchanged earnings"*; against the evidence string's unreproducible **2.49×** it read as remote, and against the reproducible **2.075×** it is ~one bad week away. **The distance to an armed kill criterion had been mismeasured by roughly a factor of six**, and the input that settles it — a current dated price — has been open as item 2 since 29-Jul. | **Corrections are not only repairs to the record; they can re-price live risk, so every correction is checked against the kill criteria and caps before it is filed as housekeeping.** Until now corrections were treated as restoring truth and escalations as responding to events — this one was both, and it arrived through the housekeeping door. **Second-order point worth keeping: the criterion says "on unchanged earnings", and equity grew 3.8% YTD, so the book-value denominator rises and drags P/B toward the trigger at a flat price.** A threshold defined on a ratio moves on its own even when the market does nothing, and no item in this repo tracked that drift. |
| 2026-08-02 | **Wrote "suspect the derivation first" at 09:53 and violated it in the same entry.** The KDH lesson filed hours earlier reads: *"when an outside figure contradicts a derived one, suspect the derivation first — it is the one whose inputs you control."* At 09:53 my **derived** P/B of 2.075× contradicted the file's **recorded** 2.49×, and I concluded the file was wrong, restated a live evidence string, cut confidence, opened an OPEN-DECISIONS item, escalated trigger 4 and pushed it. **2.49× was exact.** My share count was TCX's **listing-date** figure; TCX paid a **20% stock dividend in Q2/2026** and the real count is 2,773,896,000. The claim that "2.49× cannot be reproduced from any combination of this file's inputs" was **disproved by the file's own inputs** — 41,100 × shares ÷ 45,782bn = 2.4902×. | **A lesson applied only to incoming data is not applied at all.** Every check I built this week points outward at sources; this one needed to point at my own arithmetic, and the 02-Aug midnight lesson had already said exactly that (*"a check that only points at sources does not catch the file's own hand"*) — **two lessons, both on file, both written by me, neither fired.** The operational fix is narrower than "be careful": **a share count, like a price, is a dated quantity and expires on any corporate action.** Before any per-share or market-cap arithmetic, the sweep now checks the ticker's corporate-action history over the period spanned — and note that **lane 3 already tracks stock dividends** (TCB 60%, VPB 26%, MBB 15% + rights) and **TCX's 20% was simply never on the list.** The data needed to prevent this was in the lane definition, unqueried. |
| 2026-08-02 | **The wrong finding was loud and the right one was underneath it.** The 09:53 entry led with a false kill-criterion alarm; the same corrected arithmetic then exposed that `decide.py` prices TCX off `cap_now = pe_ttm × npat_ttm` = ₫82,215bn against a true market cap of ₫114,007bn — **38.7% low, overstating mu_raw by 34.3pp and flipping it from +23.1% to −11.2% on the engine's top-ranked proposed add.** Trigger 3 fired at 3× its threshold, and it had been sitting in the engine untouched while three sweeps argued about narrative items. | **When a correction is forced, re-run the arithmetic all the way through rather than stopping at the sentence that was wrong.** The instinct after finding an error is to repair the specific claim and move on; here the repair was the cheap part and the discovery was two divisions further down. **Structural point worth keeping: this file has spent a week auditing evidence strings and log prose, and the largest error found so far was in a two-token expression in the engine that no lane covers.** `cap_now` is `pe_ttm × npat_ttm` for all eight names and **no ticker's market cap has ever been checked against shares × price** — a whole class of input that no routine touches, found only because a share count happened to be wrong. |
| 2026-08-02 | **The engine's single most-used expression had never been checked, and it was wrong on at least three of eight names.** `decide.py` computes `cap_now = pe_ttm × npat_ttm` and divides every scenario by it — it is the denominator of every expected return in the book. Checked for the first time today, only because a wrong share count on TCX forced it: **TCB correct to 0.3%, HPG −7.6%, VPB −15.1%, TCX −27.9%, MBB +17.9%**, two more unresolved. VPB's implied share count is its **~2022** charter capital. **A week of sweeps audited evidence strings, log prose, press periods and regulator gazettes, and never once multiplied two fields together and compared the answer to a number anyone could look up.** | **Audit the inputs the model actually divides by, before auditing the prose that describes them.** The lanes are built to find *news*; a stale field generates no news and so is never found — the same structural blindness the 01-Aug gazette lesson identified, now shown to apply to the file's own numbers, not just to outside sources. Concretely: **every field that feeds a denominator gets a provenance date and an independent reconstruction** (`cap_now` against shares × price; ratios against their two components). Note the shape that made this invisible: `pe_ttm × npat_ttm` is *internally* consistent for any pair of numbers — nothing in the file can contradict it, so no consistency audit could ever flag it. **It could only be caught from outside, and nothing was looking.** |
| 2026-08-02 | **The errors did not share a direction, which is the part that would have defeated a sanity check.** Intuition says a stale share count biases everything one way and largely cancels when eight names are ranked against each other. It does not: **TCX and VPB are overstated, MBB is probably understated, TCB is exactly right.** Each name's `pe_ttm`/`npat_ttm` froze a share count at whatever moment it was typed, and the eight have had corporate actions — TCX 20%, HPG 767m shares, VPB 26%, MBB 15%, TCB 60%, VCI ESOP+bonus — at six different times. | **"It probably cancels" is a hypothesis about a correlation, and correlations between independently-stale fields are usually zero.** Where a defect is found in one instance of a repeated pattern, the correct next step is to **measure every instance rather than reason about the aggregate** — the measurement here took one script and would have taken minutes at any point in the past week. And record the clean ones explicitly: **TCB being correct is a finding, not an absence of one**, and stating it stopped a 35% position from being dragged into an escalation it had no part in. |
