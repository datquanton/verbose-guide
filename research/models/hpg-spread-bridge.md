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

---

## 7 · Update 2026-07-28 — the volume denominator is now a known number

HPG's operating release for the first half gives **Q2 sales of 3.5m tonnes** for the basket
this model prices (construction steel + high-quality coil + HRC + billet), with H1 at 6.5m
tonnes. That release is a company disclosure, tier T2 — it is not the audited statement,
which is still to come.

**It cross-checks.** H1 6.5 minus Q2 3.5 leaves Q1 at 3.0m tonnes, which is exactly the
`q1_volume_mt` this model already carried from a separate, earlier source. Two independent
routes to the same number.

### Volume is not the problem, and that is the finding

`remaining_volume_mt` in `assumptions.json` covers the three quarters Q2 through Q4. One of
those three is now an actual, so the branches can be restated as what the **second half**
must still deliver:

| Branch | Full Q2–Q4 | H2 must deliver | Per quarter | Versus the 3.5m Q2 actual |
|---|---:|---:|---:|---|
| bear | 10.5mt | 7.0mt | 3.50mt | **flat** — no growth required at all |
| base | 11.5mt | 8.0mt | 4.00mt | **+14.3%** — roughly one repeat of the Q1→Q2 ramp |
| bull | 12.5mt | 9.0mt | 4.50mt | **+28.6%** — that ramp repeating twice |

Q1 to Q2 was **+16.7%** (3.0 → 3.5). So the base branch does not need a step-change; it
needs the ramp already observed to continue for two more quarters, which is what a plant
commissioning new capacity normally does.

**The consequence.** Every branch's volume assumption is now either comfortable (bear) or
merely a continuation (base). Whatever goes wrong with this position will therefore go
wrong on the **margin** blade, not the volume blade. The `spread_watch` note framed both
blades as moving against HPG; on the evidence, only one is. Monthly volume releases have
stopped being decision-relevant, and NPAT per tonne has become the only number that matters.

### What a known denominator buys: the Q2 print now reads directly

Because tonnes are fixed at 3.5m, any Q2 core profit headline converts to margin per tonne
with no interpretation required. Q1 core was **₫1.68m/t**. Branches are 1.25 / 1.60 / 1.85.

| If Q2 core NPAT is… | Implied NPAT/tonne | Versus Q1 | Read as |
|---|---:|---:|---|
| ₫5,020bn | ₫1.43m | −14.7% | Margin contracting — but still **above** the 1.25 bear branch, so even the low end of the estimate range does not breach bear |
| ₫5,600bn | ₫1.60m | −4.9% | Exactly the base branch, and exactly the threshold of open forecast #2 |
| ₫6,400–6,500bn (street) | ₫1.83–1.86m | +8.7 to +10.4% | Margin **expansion**, at or above the **bull** branch |

### The trap, stated before the number lands

The street's ₫6,400–6,500bn implies per-tonne margin *expanding* about 10% in a quarter when
Formosa cut August/September HRC by roughly US$40/t and Indian HRC landed near US$535/t.
That is not incoherent — it is what §4's inventory lag predicts, because Q2 burns ore bought
in Q1 at about US$101/t.

**So a strong Q2 is not evidence against the spread thesis.** It is the lag behaving as
modelled. The quarter that tests the thesis is **Q3**, which burns today's US$97.70 ore
against an HRC price that has already been cut. Confidence must not be raised on a Q2 beat,
and this paragraph exists so that reading cannot be constructed after the fact.

---

## 8 · Correction 2026-08-03 — the iron-ore input of US$115 has no source, and Fitch's figure is US$100

**The grid, §5's recommendation and §6's provenance line all rest on `ore ≈ US$115/t`. That number
is not supported by anything.**

Fitch Ratings' 2026 assumptions — the single release this model cites for coking coal — are
**iron ore US$100/t** (raised from 95) and **coking coal US$220/t** (raised from 190). Same source,
same year, same revision. **This model carries Fitch's coal number exactly and an iron-ore number
15% above Fitch's.**

An earlier correction (`valuation.HPG._CORRECTED_2026_07_27`) called the 115 "a Fitch forecast
mis-logged as spot." **It is not spot and it is not Fitch.** Its most likely origin is the 26-Jul
summary that carried "coking coal 2026F raised to US$220/t" and "iron ore up to ~US$115/t" in one
sentence — one report of the Fitch release getting one of the two numbers right. *That is an
inference about origin. What is established is that Fitch says 100 and this file says 115.*

**The asymmetry was recorded on 31-Jul and read backwards.** That entry noted "ore is 14.6% below
modelled and coal is 0.7% below it." Two inputs drawn from one source cannot miss the market by
14.6% and 0.7% — **the discrepancy was in the input, not in the market.** Against Fitch: coal
$218.50 is 0.7% below 220, and **ore $98.25 is 1.75% below 100.** Both inputs sit essentially on
Fitch's assumptions.

The file's own ore observations already said so: **97.70** (27-Jul, SGX), **98.02** (08-Jul),
**98.25** (30-Jul), **~101** (the Q1 inventory cost used in §4), **103** (DCE converted) — and one
outlier at 115.

### What it changes — no rebuild required, the answer is in §2's own grid

§2 already carries a row for `ore = 100`. At HRC 539 and coal 220 it reads **₫0.86m/t**.

| | Ore input | Core NPAT/t at HRC 539 |
|---|---:|---:|
| §5's recommended `spot_persists` branch, as written | 115 | ₫0.36m |
| The same branch on **Fitch's actual assumption** | **100** | **₫0.86m** |

**2.4× higher.** A human acting on §5 as written would have embedded a downside branch roughly
₫0.5m/t too severe.

**The convergence that confirms it.** The 31-Jul spot repricing, done independently on live quotes,
put the spot case at **₫0.86m/t at HPG's volume price** and ₫1.10m at its list price. The
Fitch-consistent grid reading is **₫0.86m/t**. These are the same number. The apparent gap between
"the bridge says 0.36" and "spot work says 0.86–1.10" was never a forecast-versus-spot divergence —
**it was the phantom 115, and it was attributed to the market for a week.**

### What survives unchanged

**₫0.86m/t is still below the 1.25m/t bear branch.** *No branch describes the world as it is* holds.
What changes is the **size** of the miss — the gap to bear is **₫0.39m/t, not ₫0.89m/t** — and the
fact that **the cost side is not delivering relief.** "Ore 14.6% below modelled" reads as a windfall
already banked; ore at 1.75% below forecast is no windfall at all, and the compression from the
August HRC cut is not being offset.

**The grid and §5 are left standing rather than edited.** Re-solving the model and repricing a branch
is a judgment change reserved for a human (charter §2); this section records the defect next to the
numbers it affects. **OPEN-DECISIONS item 6 — whether to add `spot_persists` — is now both more
urgent and to be decided on ₫0.86m/t rather than ₫0.36m/t.**

---

## 9 · Structural note 2026-08-05 — no price in this model has a stated delivery basis

§1's table has a **Basis** column, and every entry in it documents a *consumption ratio or a
derivation* — 1.60 t/t of ore, 0.65 t/t of coal, D&A over ~12mt. **Not one of the model's
PRICES carries a delivery term anywhere in this file.**

| Input | Values used | Delivery basis stated? |
|---|---|---|
| Iron ore | 97.70 (SGX), 98.02, 98.25, ~101 (Q1 inventory), 103 (DCE converted), 93.66 | **no** |
| Coking coal | 190 (Q1), 218.50, 220 (Fitch), 228, 238.9 | **no** — "PHCC FOB Australia" appears only in log entries |
| HRC | 539 (spot), 560 (Q1), 546.5/535 (HPG's own offers) | **no** — and separately the file holds "Indian HRC ~US$535/t **landed** Vietnam" and "China HRC **US$485 FOB**" |

**Three prices, three different and undocumented delivery bases, one model.**

### Why this is more than a documentation gap

**The conversion cost of US$114/t is *solved*, not assumed** — calibrated so the bridge reproduces
the known Q1/26 actual of ₫1.68m/t. **So it absorbs whatever basis mismatch existed at Q1 prices.**
The calibration is therefore self-consistent *at Q1* and stays valid **only while the basis spreads
hold constant.**

**If freight moves, the solved conversion cost silently absorbs a freight change as though it were a
conversion change, and the model cannot see the difference.**

### The size, against the gap the model is currently read against

HRC gearing is **₫0.42m per US$20/t**, i.e. **₫0.021m per US$1/t**:

| | ₫m/t |
|---|---:|
| A US$15/t freight **level** embedded in the calibration | **0.315** |
| A US$5/t freight **change** | 0.105 |
| For scale: gap from the 04-Aug spot case (₫1.076m) to the ₫1.25m bear branch | **0.174** |

**A US$8.3/t move in freight alone would close that gap.** The variable is undocumented, unmodelled,
and larger than the distance currently being measured.

**Nothing is changed here.** Naming a basis for each input is a model decision (charter §2/§4), and
the freight figures used above are indicative, not sourced. **What is established is that the model
has no basis column for its prices and that the omission is material at the scale currently in
play.**
