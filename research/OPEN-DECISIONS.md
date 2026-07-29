# Open decisions — things only a human can settle

**Rebuilt 2026-07-28 12:00 ICT. This is an index, not new analysis.** Every item below was
found and written up elsewhere; nothing here is a new finding and nothing here is being
claimed as material. It exists because 28 July produced eighteen separate flags across nine
log entries and several files, and **a decision system whose findings cannot be found has
not finished the job.**

Ordered by what it costs to leave undone.

---

## 1 · Blocking a live recommendation

| # | Decision | Why it blocks | Where it is written up |
|---|---|---|---|
| 1 | **Read VPB's consolidated Q2 credit balance off the statement.** | The model holds `credit_q2` ₫1,060,000bn and `credit_growth_ytd` 24.6%, which imply +10.19% and +24.6% respectively. They cannot both be right. At +24.6% the base branch needs another +8.3% in H2 and is comfortable; at +10.2% it needs **+22.5%**. The engine is meanwhile proposing **ADD +5.3pp to VPB.** | `assumptions.json` → `vpb.actuals._CREDIT_INPUTS_FAIL_VERIFICATION_2026_07_28`; log 01:53 |
| 2 | **Refresh all eight prices and add a `_price_date` per ticker.** **← now the highest-value item on this page, escalated 29-Jul 16:53** | Prices are undated and presumed 24 July. A 1% move is **73% of VPB's entire expected-return signal** and 25% of TCB's. **TCB now has a dated observation ₫3.42% below the file's figure** (₫28,250 on 27-Jul vs ₫29,250 here) — three times the drift previously recorded. On the file's own sensitivity that lifts TCB's E[r] by ~3.1pp and **moves it from 7th of eight to 6th**, weakening a stated support for the headline 15pp trim. The trim survives on the 20% cap, which is constitutional rather than a ranking. **And the market fell 6.55% in the week to 24-Jul** with forced liquidation — an undated price field is a different order of problem in that market than in a quiet one. | `assumptions.json` → `valuation._PRICES_ARE_UNDATED_2026_07_28`, `_MARKET_CONTEXT_2026_07_29`; log 09:53 and 16:53 |
| 3 | **Set the `cash_yield` convention and populate all eight.** **← the convention is not merely missing, it is being applied inconsistently; found 29-Jul 21:53** | Filled in for TCB only — and **TCB's value rests on a premise that is false.** The note justifies including TCB's 7% cash because it is "pending"; it was **paid on 10-Jun-2026**, the *same day* MBB's 10% cash was paid, which the same note **excludes** as "already past". **Two dividends, one payment date, opposite treatments, and the asymmetry favours the largest position.** Removing TCB's 0.024 cuts its shrunk expected return 1.92pp to ~+1.50%, against VPB's +0.99%.  MBB's 2026 dividend includes **10% cash = 4.54%** of price; including it moves MBB from 4th to 3rd, above HPG. Seven blanks are not seven zeros, and the omission only touches dividend payers, so it biases against the banks. | `assumptions.json` → `valuation._CASH_YIELD_POPULATED_FOR_ONE_OF_EIGHT_2026_07_28`; log 10:53 |

## 2 · Judgment calls the charter reserves for a person

| # | Decision | The finding behind it | Where |
|---|---|---|---|
| 4 | **Re-weight KDH's scenario probabilities.** | The bull branch needs ~178–186 units handed against a **135-unit sold book** — arithmetically out of reach — yet carries p=0.20. | `dossiers/KDH.md` §2 |
| 5 | **Re-weight the TCX FTSE event tree, or retire it.** | It prices 21 September as one discrete day (+20%/+5%/−15%, EV +6.25%). Inclusion is actually **phased in tranches to September 2027**, and the announcement effect was largely banked in April. | `assumptions.json` → `tcx._FTSE_IS_PHASED_2026_07_28`; log 04:53 |
| 6 | **Decide whether to add a `spot_persists` branch to HPG.** | No existing branch describes current input prices. At spot the case is **₫0.60–0.68m/t** against a bear branch of ₫1.25m. | `hpg-spread-bridge.md` §6–7 |
| 7 | **Raise `corr_same_cluster` toward ~0.95 for parent/subsidiary pairs.** | TCB contains TCBS; VPB contains VPBankS. The optimizer models these as 0.80-correlated when one *contains* the other. | `assumptions.json` → `vpb.model._VPX_LOOKTHROUGH_2026_07_26` |
| 8 | **Decide what to do about 19.5% effective brokerage exposure.** | Look-through, not the 11.4% stated. The proposed TCX add starts from an effective 12.2%. | `dossiers/TCX.md`; `_LOOKTHROUGH_EXPOSURE_2026_07_27` |

## 3 · Machinery — an automated run may not touch these (charter §4)

| # | Decision | Why it matters |
|---|---|---|
| 9 | **Build driver models for MBB and VCI in `run.py`.** | 9.6% of the book has `fy26e_npat` typed in with nothing deriving it. MBB is the joint-largest proposed add. Inverting the branches showed they are *coherent* — the problem is they cannot be stress-tested. |
| 10 | **Wire `ftse_event_tree` into `decide.py`, or label it narrative.** | It is read only by `run.py` and printed into the snapshot. Its +6.25% never reaches expected returns or weights. VCI's stated bull case is "an EVENT bet" and the event is absent from VCI's numbers. |
| 11 | **Correct the FE Credit attribution printed by `run.py`.** | The line says FE Credit NPL formation is the swing factor. FE Credit is 0.8% of consolidated profit; the risk sits in the parent book. |
| 12 | **Replace the two scheduled-routine prompts.** | The live hourly prompt keeps its own copy of the lanes, the broker estimates and the run rules, and those copies have drifted from the repo. Drafts are written and ready to paste. |

## 4 · Reads that take one line off a filed statement

| # | Question | Consequence if left |
|---|---|---|
| 13 | Is HPG's ₫4,123bn divestment gain pre- or post-tax? | Core + one-off = ₫9,169bn against a ₫9,056bn headline. The ₫1.68m/t figure it implies is the **calibration anchor of the whole spread bridge**. |
| 14 | Is KDH's `q1_revenue` ₫281.4bn actually revenue, or net profit? | ₫355.7bn × (1 − 21%) = ₫281.0bn. If it is profit, the dossier's second verification route for Thursday's units count never existed. |
| 15 | Is KDH's ASP ₫42bn or ₫44bn? | The model and its own dossier disagree. Changes gross profit per unit by 4.8% and solved fixed opex by 8.3%. The bull-infeasibility conclusion survives either way. |
| 16 | **What is MBB's 2026 credit-growth target? REOPENED 29-Jul 14:53** — the "mostly resolved at 30–35%" status is withdrawn. **Chairman Lưu Trung Thái is on the record at 25%** (Jan-2026), against the unattributed 30–35% this file prefers. A named source is stronger evidence, but it may predate an AGM-approved figure. Both survive: 25% as internal plan, 30–35% as SBV quota allowance. **AGM minutes settle it; the H1 statement will not.** | **The period half IS now resolved, by arithmetic.** Q1 credit is pinned at **₫1,140,000bn, +3.3% YTD** (two sources, T5). So the "10%" cannot be a Q2 increment — that would give ~13.3% YTD, contradicting the same source's "10% as of May". **It is cumulative YTD at end-May**, meaning +6.7pp in April–May alone. Credit is accelerating, H1 is likely above 10%, and the recorded "H2 must add +18.2% to +22.7%" **overstates the requirement**. MBB's version of VPB's problem is milder, not identical — and MBB is the joint-largest proposed add. |

## 5 · Access a human must grant

| # | What | Unblocks |
|---|---|---|
| 17 | **Download the annual-report PDFs** (TCB, HPG) into the repo, or authorise the FiinQuant connector. | Depth-queue items 2, 6, 9, 10, 12 — the entire annual-report tier. Three hosts have returned proxy 403. |
| 17b | **Open one specific PDF and read one line.** TCB's Q2 separate VAS statement is at `techcombank.com/content/dam/techcombank/public-site/documents/techcombank-vas-bao-cao-tai-chinh-rieng-le-2q26-searchable.pdf` (proxy 403 from here). Read the **corporate bond / investment securities balance at 30-Jun-2026 vs 31-Dec-2025**. | This is now the highest-value single line in the repo. It tests whether TCB's property de-risking was a removal or a relocation — see the Masterise section below — and it resolves the credit-vs-loans gap in one read. |
| 18 | **Add or re-scope depth-queue items.** An automated run may only edit status marks. | The queue is exhausted. Note that item 10 (Masterise) is **partly reachable via HNX bond disclosures**, which do not need the blocked PDFs. |

---

## Risk, measured against the alternative — added 2026-07-29

`python3 research/models/risk.py`. Not a decision, but it reframes several of the ones above.

Roy's safety-first ratio asks how much expected return you get per unit of volatility
**above a threshold you actually care about**. The threshold that matters here is a
Vietnamese 12-month bank deposit at roughly 6% — what this money earns doing nothing.

**The book expects +6.85% with 30.5% volatility, so the safety-first ratio against that
deposit is 0.028 and the chance of underperforming it is 48.8%.** A coin flip.

Per name at the same threshold, the ranking runs almost exactly opposite to the weights:

| | Weight | SF ratio |
|---|---:|---:|
| TCX | 5.5% | **+0.292** |
| VPX | 2.8% | +0.177 |
| HPG | 16.8% | +0.146 |
| MBB | 6.5% | +0.076 |
| KDH | 20.3% | +0.038 |
| VCI | 3.1% | −0.038 |
| **TCB** | **35.0%** | **−0.077** |
| **VPB** | **10.0%** | **−0.141** |

*Refreshed 2026-07-29 after HPG's Q2 filing raised its confidence 0.60 → 0.70. HPG's ratio
moved +0.098 → +0.146 and the book's moved 0.020 → 0.028. **Nothing else changed, and the
ordering did not change at all.** Recorded because a table of risk numbers that silently
goes stale is the thing this file exists to prevent.*

**TCB, VPB and VCI together are 48.1% of the book on negative ratios** — on these numbers
not expected to beat a term deposit at all. The two best ratios are the two smallest
positions. That is a fourth independent route to the TCB trim, after expected return, the
bonus-adjusted consensus target, and the peer table's ROE ÷ P/B.

The proposed books improve it but not dramatically: this cycle 0.057, north star 0.093.

**Tested 2026-07-29 and partly cleared.** The engine cuts a name's expected return by
confidence but not its risk. Re-run under two alternatives — shrinking dispersion too, and
widening it as confidence falls — **the ranking is identical under all three**, so nothing
above depends on that choice. The *levels* do: KDH's volatility is 54.5%, 36.5% or 97.6%
depending on the convention, and the optimizer penalises volatility **squared**. So position
sizes are convention-dependent even though the ordering is not. Worth a human settling, and
worth recording as a choice rather than a default.

**Two honest caveats.** The simulation's left tail comes out *thinner* than a normal
(5th percentile −34.4% against −43.6%) because scenario branches are bounded by
construction and the real world is not — that is a model limitation, not comfort. And
`cash_yield` being blank for seven of eight names biases the book's expected return **down**,
so these ratios are, if anything, harsher than the truth. Fixing item 3 above would move them.

---

## Five more, from the CFA Level III toolkit — added 2026-07-29

`python3 research/models/cfa.py`; written up in `research/models/CFA-TOOLKIT.md`. Ten standard
institutional tests, run against the actual holdings. All diagnostic — nothing there changes a
weight. Five items land here because the charter reserves them for a person.

| # | Decision | The finding behind it |
|---|---|---|
| 19 | **Settle λ, the risk-aversion parameter.** | Backed out of the book itself, λ is **0.354**. The optimizer config says **6.0** — 17× higher. Both cannot be right, and λ multiplies σ *squared*. Optimizer config is human-only under §4. |
| 20 | **Replace the flat ±3pp no-trade band with volatility-scaled corridors.** | A corridor should *narrow* as volatility rises. A flat band cannot, so today's rule lets **the most volatile position in the book drift the furthest** before anyone looks at it. KDH at 54.5% warrants ±2.0pp. |
| 21 | **Decide whether concentration or forecasting is the thing to fix.** | Effective breadth is **1.70 of 8 holdings** (Buckle). At that breadth the fundamental law says **no achievable forecasting skill** produces even a 0.25 information ratio — required IC is 0.31. The binding constraint is structural. Adding uncorrelated positions beats improving any of the eight dossiers. |
| 22 | **Decide whether the beta is intended.** | Portfolio beta to VN-Index is **1.81**, correlation **0.93**. Most of this book's deviation from the market is *leverage*, not selection. Jensen's alpha is negative at every index assumption and gets worse as the index rises. |
| 23 | **Hold the tax-timing question in view — do not act on it.** | Securities tax today is 0.1% of *proceeds*, so rebalancing is nearly free. A draft MoF decree would tax **20% of gains** instead. Every position is at a loss, so the proposed TCB and KDH trims would crystallise usable losses **under the draft rules and nothing under today's.** The decree is not law and loss-offset treatment is unspecified. |

**Two results worth noting even though they are not decisions.** Reverse optimisation (Π = λΣw)
ranks the names by how far each position exceeds the view behind it, and that ranking is the
**exact inverse of the safety-first ranking above** — trim VPB, TCB, VCI; add TCX, VPX, HPG. Two
unrelated formulas, same answer. And volatility drag (g ≈ μ − σ²/2) puts **four of eight holdings,
68.4% of the book, on a negative expected *compounded* return** — KDH expects +8.1% and compounds
at −6.8% purely on its 54.5% volatility.

---

## The one thing on this page that is close to a thesis

Item 1 aside, the finding most likely to change what the book owns is the **Masterise
hypothesis**, and it is deliberately not in the tables above because it is not yet a
decision — it is a question with three named tests.

Masterise-linked companies raised **₫44,500bn** of bonds in the first half. TCB cut
**₫39,000–40,000bn** of corporate property exposure from its Q3/25 peak over broadly the
same period, a reduction the TCB dossier treats as materially weakening the bear case. The
ratio is **1.11–1.14**.

If the exposure moved rather than disappeared, a bull point becomes a neutral one — and
because TCBS is a major bond arranger, it may have moved *within* the group we own twice
over. **Two numbers being close is not evidence.** The three tests are named in
`assumptions.json` → `tcb._MASTERISE_BOND_RAMP_2026_07_28`, and none has been run.

---

*Maintained by the hourly sweep as an index only. Items are added when found and removed
when a human resolves them. Nothing here is actioned automatically; the system recommends,
a human signs.*
