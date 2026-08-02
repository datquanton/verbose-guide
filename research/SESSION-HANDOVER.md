# Session handover — state of the book at 2026-07-31

**Updated 02-Aug 15:53 ICT.** MBB filed (§2, §3). **Two of the four escalations in §4 are now RESOLVED**,
and a new structural one has replaced them — see §4 and §9.

**Written at the owner's request to make this session's context survive the container.**
The session is ephemeral; this file and the git history are not. Everything below is already
recorded in `monitoring-log.md`, `assumptions.json` and `calibration-log.md` — this exists so
a reader arriving cold knows *where things stand* without reading 108 commits.

**Nothing here is new analysis. No trade has been placed or recommended as executed.
The system recommends; a human signs.**

---

## 1 · What the engine currently says

`python3 research/models/decide.py`. Ranked by shrunk expected return:

| | E[r] | Conf | Proposed this cycle |
|---|---:|---:|---|
| TCX | +18.5% | 0.80 | ADD +5.6pp → 11.1% |
| VPX | +15.0% | 0.55 | hold (inside no-trade band) |
| HPG | +10.6% | 0.70 | ADD +3.2pp → 20.0% |
| MBB | +8.8% | 0.55 | ADD +5.6pp → 12.1% |
| KDH | +8.1% | 0.50 | TRIM −4.6pp → 15.7% |
| VCI | +4.3% | 0.40 | hold |
| TCB | +3.4% | 0.80 | **TRIM −15.0pp → 20.0%** (cap breach) |
| VPB | +1.0% | 0.70 | ADD +5.4pp → 15.4% |

**Read these numbers with the three blocking caveats in `OPEN-DECISIONS.md` §1 in hand.**
They are not decorative — each one can move the ranking.

## 2 · The quarter that just landed

| | Status | Result |
|---|---|---|
| **HPG** | Filed 29-Jul | Q2 revenue ₫55,557bn **+53%**, NPAT ₫6,424bn **+51%**; H1 = 70% of FY plan. Confidence 0.60 → 0.70. |
| **KDH** | Filed 30-Jul | **CORRECTED 02-Aug: Q2 NPAT is ₫770bn and H1 ~₫1,097bn — 73% of the ₫1,500bn FY plan.** The ~~"H1 ₫321bn, Q2 profit ≈ zero"~~ on this row was wrong: ₫321bn is on a different basis (core/ex-gain/parent) and was paired with a consolidated Q1. **Core operations did collapse** — Q2 revenue ₫161bn **−85%**, ~3.7 units handed, OCF −₫2,580bn — but profit came from **>₫906bn of financial income** on the Bình Trưng Mới 51% transfer. **The 73% is a one-off, not a run-rate.** Every street estimate too high; VCBS's revenue forecast was **7×** the outcome. |
| **MBB** | **Filed, surfaced 31-Jul** — one day past its Circular 96/2020 deadline | Q2 PBT **₫10,560bn +40%**; Q2 NPAT-to-parent **₫8,229.06bn +40.01%**; H1 NPAT-to-parent ₫15,744.58bn +26.51%. Net interest income +36.55%. NPL 1.45% (from 1.42%) with coverage *rising* to 93.63%. Confidence **held at 0.55** — T5 press, and charter §2 permits a rise only on T1–T2. |

**All three statements are now in. The date gate is closed; the next is Q3, due 30-Oct.**

**Two figures in MBB's Q2 coverage were the Q1 numbers reappearing** — provisioning ₫3,455bn (+15.7%)
and loans ₫1.12 million tỷ (+3.3%), both already on file to the digit. Neither was logged, so **H1
provisioning is still unknown.** The tell was free: *a new figure that exactly equals an old one is
usually the old one.*

## 3 · Calibration: 1 hit, 2 misses

| # | Forecast | Result |
|---|---|---|
| 2 | HPG Q2 core NPAT/tonne below ₫1.60m | ❌ **MISS** — actual ₫1.835m. The forecast contradicted my own timing note written the same day. |
| 1 | KDH Q2 parent NPAT ₫170–348bn | ❌ **MISS** — by ~5× on the falsifiable part. Right in direction, badly wrong in calibration. |
| 10 | US rebar final ≈ headline risk only | ✅ **HIT** — right for the *stated* reason. The rate went the wrong way (finals ~6.6pp above preliminary) and the impact claim still carried it. |
| 4 | MBB Q2 NPAT ≈ ₫7,052bn, band ₫6,347–7,757bn | ❌ **MISS** — actual consolidated NPAT ₫8,448bn, **+19.8%**, on the forecast's own measure. |

**Now 1 hit, 3 misses across four resolved forecasts. All three misses were on the estimate side,
not the direction side** — the base cases keep being wrong about *magnitude*, twice too high
(KDH, HPG) and once too low (MBB).

**The pre-registered read on #4 is scored WRONG, on its own stipulation.** It said *if MBB misses,
expect it to miss on credit cost with net interest income intact* — and pre-committed that *"if MBB
instead misses on the top line, **or beats outright**, this read is wrong."* **MBB beat outright.**
That clause is the only reason this is recorded as a failure rather than quietly retired.

**The read-across is the finding, not the miss.** ACB printed **−12%** and VIB **−8%** on
provisions; I inferred a sector cycle and applied it to MBB. **MBB printed +40%** — a ~52pp spread
between two large banks in one quarter. What did work was the sequencing: MBB's *own* Q1 provisioning
(+15.7% vs PBT +14.8%) contradicted the peer inference, and the read was **withdrawn on 30-Jul,
before the print**, on that bank-specific evidence.

## 4 · Escalations raised this session, all still open

1. **Circular 25/2026/TT-NHNN** — SBV raised the cap on short-term funding usable for
   medium/long-term lending from **30% to 40%**, effective 01-Jul. **T1.** Bears on 71.8% of the
   book. It had been in force four weeks and this repo had no record of it.
2. **Price staleness, measured** — TCB had a dated observation **3.42% below** the file's figure.
   On the file's own sensitivity that moves TCB from 7th of eight to 6th, weakening a stated
   support for the headline trim. The market fell **6.55%** in the week to 24-Jul.
3. **`cash_yield` applied inconsistently** — three of eight names paid cash in H1 (TCB ₫700,
   MBB ₫1,000, VPB ₫500) and the field records exactly one of them, on a premise shown false.
   All three are banks.
4. **KDH Q2** — see §2. `fy26e_npat` branches now contradicted by the run-rate; ~10 units handed
   in H1 against a bear branch needing 80.
5. **MBB Q2 — the same defect, opposite sign.** Escalation trigger #4 fired (estimate → filed
   actual). H1 PBT **₫20,188bn** leaves bear needing H2 **−26.6%**, base **−11.2%**, bull **+4.3%**
   — and bank profit here is second-half weighted, so a *flat* H2 gives FY PBT ₫40,376bn, above
   base. **Two of three branches now require profit to fall outright.** The 28-Jul pre-registered
   table called this exact row in advance and its instruction is *rebuild, do not celebrate*.
   **The sharp part: a +40% quarter moved MBB's expected return by zero** — still +8.8% — because
   the branches are typed in and nothing derives them. The engine is blind to the best print in the
   book while proposing MBB as its joint-largest add. `OPEN-DECISIONS` item 19, new.

### Resolved overnight, 31-Jul → 01-Aug

| Was blocking | Outcome |
|---|---|
| **`OPEN-DECISIONS` item 1** — VPB's two credit fields "cannot both be right" | ✅ **RESOLVED.** They can: **both describe the PARENT** (₫1,060,000bn, +24.6%). Consolidated loans are a *third* series at **₫1,160,000bn, +23%**. The fake +10.19% came from dividing a **parent stock by a consolidated base**. **Resolves in VPB's favour** — H2 needs ≤ +12.0% on the base branch, not the feared +22.5%. |
| **TCB credit-vs-loans**, the reason confidence was cut 0.85→0.80 | ✅ **RESOLVED, and the 28-Jul inference was INVERTED.** **+10.4% is loans; +14.3% is credit** incl. quota-exempt infrastructure/social housing. So the non-loan book **grew**, not shrank. `loans_start_fy`→`loans_mid_fy` is **+14.46% vs a reported +14.3%** — the model's pair was never mismatched. H2 needs **+1.5/+3.2/+5.0%**. |

**Near-miss worth knowing about:** the inverted TCB reading produced a **~₫40,700bn** gap sitting beside
the **₫39–40,000bn** of real-estate exposure TCB cut and the **₫44,500bn** Masterise raised — an
irresistible "exposure moved from loans into bonds" story. **The source names the gap as quota-exempt
lending.** It was false, and *quantitatively closer* to the on-file numbers than the truth.
**The Masterise test still needs the corporate-bond line and is NOT settled.**

### New escalations raised overnight

5. **The 403 wall is suppressing THREE confidence restorations across 51.5% of the book.** MBB (0.55),
   VPB (0.70), TCB (0.80) — in every case the evidential objection has been *answered*, and in every case
   the raise is blocked because the evidence is press, not the document (charter §2, T1–T2 only).
   **Confidence multiplies `fy26e_npat`, so this biases expected returns downward, selectively, on the
   three largest bank positions.** `OPEN-DECISIONS` item 17 is no longer an access inconvenience.
6. **HCMC Decision 45/2026/QĐ-UBND** — the land-price adjustment coefficient (**K = K1×K2×K3, K1=K3=1**),
   **in force since 01-Jul-2026**, and the repo had **zero record of it**. Land-use fee is the largest cost
   input for a developer and **KDH is 20.3% of the book with >₫23,000bn of inventory.** *Third* dated
   regulation missed in four days, and the **second effective 01-Jul**. New `OPEN-DECISIONS` item 20.
   **The direction is not established** — a higher table raises fees, a published K unblocks stalled
   approvals, and the two cannot be netted from here.
7. **`OPEN-DECISIONS` item 13 got WORSE.** A **third** candidate for HPG's divestment gain (~₫3,800bn,
   Phố Nối) joins ₫4,123bn and ₫4,010bn. **The spread bridge's calibration anchor now ranges
   1.644–1.752m/t, a 6.5% spread**, and the new figure moves it *up* — the opposite direction from the only
   alternative previously considered.

### 02-Aug 15:53 — the MoIT back-sweep ran once and explained yesterday's puzzle: the open channel is INDIA

**Decision 1959/QĐ-BCT (04-Jul-2025) did two things in one document.** It imposed the **official Chinese
HRC anti-dumping duty of up to 27.83% for FIVE YEARS** (to ~04-Jul-2030 unless replaced/extended/revoked —
long-dated support not previously on file) **and TERMINATED the investigation into Indian HRC.**

- **⚠ The India termination was NOT a finding of no dumping.** It was terminated because Indian imports were
  **under 3% of total import volume** — the **de minimis negligibility** threshold. A **volume** test over a
  **dated** window (case AD20, initiated July 2024).
- **So the open import channel is India's.** Chinese HRC: 27.83% for five years plus the wide-format route
  closed 17-Apr-2026. **Indian HRC: nothing.** The file logged *"Indian landed at US$535"* on 26-Jul as
  spread bear-evidence and **never knew Indian HRC is duty-free.** **That is the mechanism behind "closed a
  channel, did not hold the price."**
- **Forward item, with its uncertainty stated:** the termination rests on a volume threshold. **IF** Indian
  volumes have risen above 3%, the ground erodes and a fresh petition becomes possible — **HPG is a proven
  petitioner, twice.** **Whether they now exceed 3% is NOT established and NOT assumed.** Cheap check:
  Indian HRC's share of Vietnamese HRC imports in 2026. Added to the gate table.
- **Also found:** **Decision 2310/QĐ-BCT (14-Aug-2025)** — official AD on **galvanised steel from China and
  South Korea**; peers **HSG/NKG** sit in that product. And **612's investigation was initiated 27-Oct-2025**.
- **Trap disarmed by logic, not by vote:** one source says the wide band is 1,800–2,300mm, two say
  1,880–2,300mm. The underlying duty covers **below 1,880mm**, so 1,800 would overlap by 80mm — incoherent.
  **1,880 is right.**

**Nothing modelled, no confidence moved, no numeric driver changed.** The back-sweep justified itself on its
first run, as the SBV/MoF one did.

### 02-Aug 14:53 — HPG: a live trade case, in force since April, absent from this repo

**Decision 612/QĐ-BCT** — MoIT, issued 02-Apr-2026, **effective 17-Apr-2026**: a **temporary 27.83%
anti-circumvention duty** on Chinese HRC of width **1,880–2,300mm**, 24 HS codes, excluding carbon >0.30%
and plate ≥10mm. **HPG and Formosa are the PETITIONERS**, not bystanders.

- Vietnam already taxed Chinese HRC **below** 1,880mm at 23.01–27.83%; exporters shifted to wide format.
  Wide HRC imports ran **~650,000t in H1/2025, ~15× YoY** — **that figure is a year old; the current
  run-rate is not established.**
- **It is TEMPORARY, so a FINAL determination is pending and this file cannot date it.** An unlogged dated
  catalyst on a 16.8% position, and the **second** live trade case on HPG alongside the US rebar ITC vote
  due mid-to-late September.
- **⚠ It has NOT held the price.** Three months after it took effect, domestic HRC was still falling with
  import competition *increasing* (13-Jul), and HPG then cut its August offer ~US$34/t, Formosa ~US$40/t.
  **The measure closed a channel; it did not support the price. Do NOT read it as bear-evidence-cancelled.**
- **Nothing modelled, confidence not moved** — the bridge's HRC input is HPG's own offer, which prices this
  measure in by construction, and HPG's unresolved `cap_now` defect would make any confidence move
  uninterpretable.
- **New gate row: a monthly MoIT / trade-defence back-sweep, which has never been run.** `_regulatory` held
  thirteen instruments and **zero from MoIT** — the 31-Jul lesson named MoIT for HPG and no sweep queried
  it, because the back-sweep that exists runs on a **banking-finance** digest that cannot return a
  trade-defence decision.

Steel *prices* were already current (the ₫900/kg August HRC cut, rebar +₫100/kg from 27-Jul at ₫15,120/kg,
domestic HRC ₫14,000–14,350). **Only the regulation was missing.**

### ⚠⚠⚠ 02-Aug 13:53 — AUDIT COMPLETE, ALL EIGHT. SIX FIRE. THE RANKING REORDERS. START HERE.

| ticker | wt | implied shares | actual | err | mu_raw engine → corrected | delta |
|---|--:|--:|--:|--:|---|--:|
| **TCB** | 35.0% | 7,065.3m | 7,086.2m | −0.3% | +1.9% → +1.6% | −0.3pp |
| **KDH** | 20.3% | 1,000.5m | 1,122.1m | −10.8% | +16.1% → +3.5% | **−12.6pp ⚠** |
| HPG | 16.8% | 7,800.3m | 8,443.0m | −7.6% | +15.1% → +6.4% | −8.8pp |
| **VPB** | 10.0% | 6,739.4m | 7,933.9m | −15.1% | +1.4% → **−13.9%** | **−15.3pp ⚠** |
| **MBB** | 6.5% | 9,495.0m | 8,055.0m | **+17.9%** | +16.0% → **+36.7%** | **+20.7pp ⚠** |
| **TCX** | 5.5% | 2,000.4m | 2,773.9m | −27.9% | +23.1% → **−11.2%** | **−34.3pp ⚠** |
| **VCI** | 3.1% | 922.9m | 1,152.2m | −19.9% | +10.7% → **−11.3%** | **−22.0pp ⚠** |
| **VPX** | 2.8% | 1,473.7m | 1,875.0m | −21.4% | +27.2% → **−0.0%** | **−27.2pp ⚠** |

**Only TCB is right. Only HPG is wrong-but-below-threshold. Six of eight fire, at 48.2% of the book.**

**⚠ THE RANKING REORDERS** — engine VPX / TCX / KDH / MBB / HPG / VCI / TCB / VPB → corrected
**MBB +36.7 / HPG +6.4 / KDH +3.5 / TCB +1.6 / VPX −0.0 / TCX −11.2 / VCI −11.3 / VPB −13.9**.
**The engine's top two become fifth and sixth; MBB goes fourth to first; four names turn negative.**

- **MBB goes the OTHER way.** Its 15% dividend has **NOT executed — record date 12-AUG-2026** (with the
  805.5m rights offer). So `cap_now` is too **HIGH** and correcting it **RAISES** MBB's return. **This
  SUPPORTS the MBB add and destroys the TCX add.** It also settles item 19's puzzle: **16.0% × 0.55 = the
  recorded +8.8% exactly**; corrected **+20.2%**. **The branch re-derivation is still needed.**
- **VCI:** both actions executed (bonus record date 27-Mar-2026; ESOP results Jun-2026) → 1,152.24m.
- **VPX verified to the dong:** 1,875m × ₫25,400 = the stated **₫47,625bn**. It was the engine's #1.
- **Robustness:** share counts firm on all eight; directions robust because every gap but TCB's and HPG's is
  10.8–27.9% against ~5% price uncertainty. **HPG is the one name where price error could matter — and the
  only sub-threshold one.**

**Nothing retuned. No confidence moved on any name.** **⚠ NO WEIGHT SHOULD MOVE ON THE CURRENT RANKING —
nor toward the corrected one**, which rests on prices already known stale.

**Sequence for a human: (1) refresh eight dated prices [item 2] → (2) settle `pe_ttm`/`npat_ttm` per name
[item 25] → (3) THEN re-rank.**

### ⚠⚠ 02-Aug 12:53 — `cap_now` AUDIT COMPLETE (7 of 8). THREE NAMES FIRE. START HERE.

| ticker | wt | `cap_now` err | delta | status |
|---|--:|--:|--:|---|
| **TCB** | 35.0% | −0.3% | −0.3pp | **correct** |
| **KDH** | 20.3% | −10.8% | **−12.6pp** | **⚠ TRIGGER 3** (likely reading) |
| HPG | 16.8% | −7.6% | −8.8pp | material, below threshold |
| **VPB** | 10.0% | −15.1% | **−15.3pp** | **⚠ TRIGGER 3** |
| MBB | 6.5% | +17.9%? | +20.7pp? | direction **not** established |
| **TCX** | 5.5% | −27.9% | **−34.3pp** | **⚠ TRIGGER 3** |
| VCI | 3.1% | −19.9%? | −22.0pp? | direction **not** established |
| **VPX** | 2.8% | — | — | **NOT CHECKED — not claimed clean** |

**Three fire, 35.8% of the book. With HPG, names with a measured error are 52.6%. TCB (35%) is clean.**

- **KDH** (new this hour): confirmed floor **1,011.1m** shares — already above the implied 1,000.5m — and
  likely **1,122.1m** after the 111m 2025 issue (101m dividend + 9.96m ESOP, Q3–Q4 2025 window), which
  matches an independently reported 1.12bn outstanding. **Fires on the likely reading; recorded as NOT
  established beyond doubt — one completion notice settles it.** A source typo was in the way: ₫9,904bn is
  a transposition of **₫9,094bn** (9,094 + 1,017 = 10,111 exactly).
- **VPB**: 26% issuance is ~2.07bn shares to ₫100,000bn, **first tranche in implementation May 2026**. The
  implied 6,739.4m = charter **₫67,394bn, a ~2022 figure** — stale on any reading.
- **MBB / VCI** turn on whether a corporate action executed and whether the price is adjusted. **Neither
  assumed.** MBB's larger reading would explain item 19 exactly (16.0% × 0.55 = the recorded +8.8%;
  corrected +20.2%) — **hypothesis only, not usable to argue the MBB add.**

**The directions do NOT agree** — four understate market cap, MBB probably overstates, TCB is right — so
**correcting them REORDERS the ranking rather than shifting it uniformly.**

**Nothing retuned; no confidence moved on any name.** Confidence multiplies `mu_raw` and would disguise a
denominator fault as a conviction change. **Fix is one read per name: current shares outstanding, or TTM
NPAT off the filed statements. NO WEIGHT SHOULD MOVE ON THE CURRENT RANKING.**

**Also corrected:** the 08:53 KDH foreign-gap figure was **~₫282bn** computed off `cap_now`; on the
corrected cap it is **~₫323bn**. Conclusion unchanged. First demonstrated case of this fault propagating
out of the engine into narrative.

### ⚠⚠ 02-Aug 11:53 — THE `cap_now` DEFECT IS BOOK-WIDE. START HERE.

Ran the cross-check the 10:53 section said had not been run. **`decide.py` line 67 sets
`cap_now = pe_ttm × npat_ttm` for all eight names and divides every scenario by it.** Shares derived from
charter capital at ₫10,000 par.

| ticker | wt | `cap_now` err | mu_raw engine → true | delta | status |
|---|--:|--:|---|--:|---|
| **TCB** | 35.0% | **−0.3%** | +1.9% → +1.6% | −0.3pp | **correct** |
| HPG | 16.8% | −7.6% | +15.1% → +6.4% | −8.8pp | material, no trigger |
| **VPB** | 10.0% | −15.1% | +1.4% → **−13.9%** | **−15.3pp** | **⚠ TRIGGER 3** |
| MBB | 6.5% | +17.9%? | +16.0% → +36.7%? | +20.7pp? | **direction NOT established** |
| **TCX** | 5.5% | −27.9% | +23.1% → **−11.2%** | **−34.3pp** | **⚠ TRIGGER 3** |
| VCI | 3.1% | −19.9%? | +10.7% → −11.3%? | −22.0pp? | **direction NOT established** |

- **TCB is 35% of the book and is correct to 0.3%.** The largest position is unaffected. Say this first.
- **VPB's is the clearest break:** implied 6,739.4m shares = charter **₫67,394bn, its ~2022 figure**, against
  ₫79,339bn today. **Direction robust** — every 2026 action (26% dividend, 624m placement) only raises it.
- **HPG's inputs predate the 767m-share issue that SETTLED in May 2026** (₫76,755bn → ₫84,430bn).
- **MBB unresolved:** +17.9% off on the pre-dividend count, only +2.5% if the 15% executed. **If** the
  larger reading holds it explains item 19 exactly — 16.0% × 0.55 = the recorded **+8.8%**; corrected
  **+20.2%**. **Hypothesis only — do NOT use it to argue the MBB add until the ex-date is settled.**
- **VCI unresolved:** −22.0pp if the ESOP+bonus completed, the other way if not.
- **Not checked: KDH (20.3%), VPX (2.8%).**
- **The errors do NOT share a direction**, so they do not cancel in the ranking.

**Nothing retuned on any name** (§5 unresolved measure, §4 scope-lock). **Confidence deliberately not moved
on any name** — it multiplies `mu_raw`, so moving four scalars would disguise a denominator fault as a
conviction change. **Fix is one read per name: current shares outstanding, or TTM NPAT off the filed
statements.** OPEN-DECISIONS item 25 widened.

**No weight should move on the current ranking until `cap_now` is settled per name.**

**Minor correction to the 10:53 section below:** it says `cap_now` is "38.7% below" TCX's true cap. It is
**27.9% below**; the true cap is **38.7% above**. The mu_raw figures and the sign flip are unaffected.

### ⚠⚠ 02-Aug 10:53 — READ THIS BEFORE THE 09:53 SECTION BELOW, WHICH IS PARTLY WITHDRAWN

**The 09:53 P/B finding was wrong and was pushed before it was caught. It is fully withdrawn here.** I used
TCX's **listing-date** share count. **TCX paid a 20% stock dividend (5:1) in Q2/2026** — 462.3m shares,
charter capital ₫23,115.8bn → ₫27,739bn — so the count is **2,773,896,000**, confirmed three ways to 0.02%.

- **`2.49x` P/B is exactly right and always was**: 41,100 × 2,773,896,000 / ₫45,782bn = **2.4902×**. The
  original `valuation.TCX.evidence` string is **restored**.
- **The kill criterion is not near.** Trigger price **₫33,010, not ₫39,616** — **24.5% away** at the file
  price, **18.8%** at the verified 24-Jul price of ₫39,200. **Nothing was ever 3.8% away.**
- **Unaffected, because it rests on filed equity rather than the share count:** filed equity ₫45,782bn and
  the 1.13× ratio, the withdrawal of the 31-Jul 1.56×, headroom ₫40,064bn, HSC/KBSV/Phú Hưng past 190%,
  the three-values finding, the margin-figure resolution, USD/VND, the VNDiamond waiting list.

**⚠⚠ ESCALATION TRIGGER 3 — expected return moves >10pp. It moves 34.3pp, and this one is real.**

**`decide.py` line 67: `cap_now = pe_ttm × npat_ttm`.** For TCX that is **20.3 × 4,050 = ₫82,215bn** against
a true market cap of **₫114,007bn** at the file price (₫108,737bn at ₫39,200, corroborated by an
independently reported ₫108,758.6bn). **`cap_now` is 38.7% too low, so every branch return is overstated.**

| market cap used | mu_raw |
|---|---:|
| engine, `pe_ttm × npat_ttm` ₫82,215bn | **+23.1%** |
| true, at file price ₫41,100 | **−11.2%** |
| true, at verified 24-Jul ₫39,200 | **−6.9%** |

**TCX is ranked FIRST and is a proposed ADD. On the corrected market cap its expected return is negative.**
**Which input is wrong is not established** — `pe_ttm` should be 28.15, or `npat_ttm` ₫5,616bn, or both are
pre-dividend — **so neither was changed** (§5 forbids retuning an unresolved measure; §4 scope-locks
`decide.py`). **Confidence is the wrong instrument**: it multiplies `mu_raw`. **The fix is one read —
TCBS's TTM NPAT off the filed statements.** New **OPEN-DECISIONS item 25**; item 24 withdrawn and replaced.

**⚠ The same defect may exist on the other seven.** `cap_now` is `pe_ttm × npat_ttm` for every name and
**the file holds no share count for any of them** — **no ticker's market cap has ever been cross-checked
against shares × price.** That check has not been run.

**Two smaller things.** The file's price is **wrong for the date it is presumed to hold** — TCX's verified
24-Jul price is **₫39,200** vs ₫41,100 on file (**4.85% high**), which also kills yesterday's "trough"
reading. And an **adjustment trap**: a 20% stock dividend cuts the quoted price ~16.7% on its ex-date, so
₫46,800 at listing and ₫39,200 in July are **not on the same basis**.

**A corporate action on a held name went unrecorded.** Lane 3 tracks stock dividends (TCB 60%, VPB 26%,
MBB 15% + rights); **TCX's 20% was never on the list**, and it is the one fact that would have prevented
all of this.

### New escalations raised 02-Aug 09:53 — TCX, and it is the largest of the weekend

**Trigger 4 fired on TCX: a derived estimate became a filed actual, and correcting it moved a KILL
CRITERION from an apparent 24.5% away to 3.8% away with no price movement.**

- **TCBS's filed end-Q2 equity is ₫45,782bn** (+3.8% YTD), reported margin/equity **1.13×**. The 31-Jul
  entry derived **₫33,018bn** and **1.56×** — **39% low.** It flagged itself as an estimate and then wrote
  its conclusions flat; **those conclusions are withdrawn.** Headroom is **₫40,064bn, not ~₫14,500bn**;
  **56% of the cap drawn, not 78%.** The three brokers are a tight band — VCI 0.97×, VPX 1.116× *(period
  mismatch: equity end-Q1, book end-Q2)*, TCX 1.125× — **not the 0.97–1.56 spread on file.** The
  constrained brokers are **competitors**: HSC, KBSV, Phú Hưng are all past **190%** of the cap.
- **Three values for one quantity coexisted in this repo:** `margin_equity_pct` **0.98**, the log's
  **1.56×**, the filed **1.125×**. Two files, two days, no check looked for it.
- **The valuation side cuts against TCX.** TCX has **2,311,308,021 shares** — never on file — so
  `price × shares` = **₫94,995bn** vs `pe_ttm × npat_ttm` = **₫82,215bn**, **15.5% apart**. `pe_ttm` 20.3
  or `npat_ttm` 4,050 is wrong. **And `valuation.TCX.evidence` calls the multiple THE risk at 2.49×, which
  cannot be reproduced from any combination of file inputs and filed equity.** Reproducible P/B is
  **2.075×**.
- **⚠ `decide.py`'s TCX kill criterion is "P/B < 2.0x on unchanged earnings" — trigger price ₫39,616
  against a file price of ₫41,100.** **NOT declared fired**: ₫41,100 is stale and already logged as a
  **trough**, so the true distance may be larger. **The finding is that the distance was mismeasured by
  ~6×**, and the input that settles it is **OPEN-DECISIONS item 2**, open since 29-Jul. **Refreshing TCX's
  price is the cheapest high-stakes check in the book right now.**
- **The criterion says "on unchanged earnings" and equity grew 3.8% YTD** — so the denominator rises and
  pulls P/B toward the trigger **at a flat price**. Nothing in the repo tracked that drift.
- Applied: `confidence` 0.80 → **0.75**, `evidence` restated. **`exit_pe`, `probs`, `fy26e_npat`
  untouched — judgment, human-only.** New **OPEN-DECISIONS item 24**.

**KDH / VNDiamond — partial answer, not a resolution.** The cadence is confirmed (cutoff at quarter end →
announced the 20th → effective the first Monday after; Q2 was 31-Mar / 20-Apr / 04-May). **KDH was placed
on the removal WAITING LIST at the Q2 review — watchlisted in May, not removed — and a waiting list
executes at the next review, which takes effect TOMORROW.** **It does not establish that 20-Jul removed
KDH**; four attempts at that announcement have failed. **The stated cause of the FOL fall is twelve months
of foreign selling — the same mechanism as the Dragon Capital / VinaCapital finding, so those are one story
and the file had them as two.**

**Also new: USD/VND is at an all-time high** (central rate ₫25,338 on 1-Aug; commercial 26,060–26,110;
free market 26,429–26,520 — consistent, with the ±5% band near its ceiling). **The HPG spread bridge has
no FX line**, and a currency at its band ceiling constrains SBV easing room. **Nothing modelled.**

**And the four circulating margin figures resolve** — 435 (margin only) → 445 (adds advances) → 446
(80 of 85 firms) → **453.8 (full coverage, +7% QoQ, +49% YoY)**. The 29-Jul preference for the 445/435
split was correct.

## 5 · The engine tried to reward a bad print — read this before touching confidence

When KDH's miss landed, applying the routine's own rule (estimate → actual raises confidence)
pushed KDH's expected return **up** from +8.1% to +9.7% and moved it 5th → 4th.

**Confidence multiplies `fy26e_npat`.** The rule assumes branches are re-derived at the same
time; they cannot be, because that is human-only. So raising confidence alone amplifies branches
the same print just contradicted.

**Root cause: one field carries two meanings.** Confidence in the *trailing* data rose;
confidence in the *forward branches* fell. A single scalar cannot move both ways — and when
forced, it should not move in the direction that flatters. **Confidence was held at 0.50 and the
whole thing escalated instead.** That is a deliberate deviation from the routine's instruction,
recorded so a human can overrule it.

**MBB, a day later, is the same defect pointing the other way — and it is the better test.** KDH's
branches were contradicted from *above*, so holding confidence cost nothing; it was the convenient
answer as well as the right one. MBB's are contradicted from *below*, so holding confidence
**understates a genuinely good quarter** and leaves MBB ranked 4th on a +40% print. It was held
anyway, because charter §2 forbids raising confidence on press *about* a filing, and that is the
same rule that protected KDH. **A rule that only binds when it flatters you does not bind.**
Both names need the same human fix, which is not a confidence number: **re-derive the branches.**

## 6 · What this session got wrong, and what changed as a result

Four self-corrections, three of them on the same day. They share one shape: **building on a
qualitative phrase before getting the figure.**

| What I claimed | What was true |
|---|---|
| KDH's ₫281.4bn is net profit — "three routes agree" | It is **revenue**. All three routes traced to the same ambiguous press phrasing; one of them meant the opposite of my reading. |
| KDH's reported ₫770bn Q2 profit is "internally impossible" | Irreconcilable **on one measure basis** — total NPAT vs parent NPAT would reconcile it. Same failure, opposite sign. |
| MBB was already showing the ACB provisioning pattern in Q1 | Provisions **+15.7%** against PBT **+14.8%** — in line, not disproportionate. Withdrawn *before* the print. |
| The rebar case is resolved | **Commerce's part** is resolved. The **ITC injury vote (~mid-Sept)** decides whether orders issue at all. |

**New standing lessons in `calibration-log.md`:** independence of confirming routes must be
checked, not assumed; a near-match is not a match and a contradiction is not an impossibility;
get the figure before building on the adjective; verify when evidence *contradicts* you, not only
when it confirms you; any ticker-only headline gets an exchange check before a period check.

## 7 · Live dates

| Date | Item |
|---|---|
| **3 Aug** | TCX's VN30 entry is **effective** — but **the ETF rebalance COMPLETED 31-Jul**, the session before. **The flow has already happened**; an effective date is not a flow date. Sizing confirmed at ₫59–60bn = **0.073% of market cap**. **July CPI publishes the same day** |
| ~21 Aug | KDH insider-buy window closes (Vice Chairman's son, 0.056% → 1.838%) |
| **mid-to-late Sep** | **ITC final injury vote on rebar** — within 45 days of the 30-Jul Commerce finals. An "August" date circulating is a **stale pre-determination projection**. **The ITC has already voted affirmative on ALGERIA in the same petition.** Vietnam's margins (128.53–136.57%) are **2.4–4× Bulgaria's and Egypt's** |
| 21 Sep | FTSE Secondary Emerging effective, **phased in tranches to Sep-2027** |
| 30 Oct | Next Circular 96/2020 deadline — Q3 statements |
| — | MBB stock dividend 15% and rights 10:1 at ₫10,000 — **both still pending, no record date announced.** The rights price is ~45% of market and dilutive to anyone not taking it up |

## 8 · Structural facts a reader should not have to rediscover

- **Vietnam CPI is 4.38%** (H1, accelerating), not the **3.5%** `risk.py` uses as its
  real-return threshold. Every safety-first ratio against that line is too flattering.
- **SBV is constrained on two sides**: FX (Fed held 3.50–3.75% with three *hike* dissents) and
  inflation (CPI 4.38% against a band near 4.5%). Funding-cost relief is not coming from policy.
- **Effective brokerage exposure is 19.5%**, not the 11.4% stated — TCB contains TCBS, VPB
  contains VPBankS.
- **Effective breadth is 1.70 of 8 holdings.** At that breadth no achievable forecasting skill
  produces even a 0.25 information ratio. The binding constraint is concentration, not research.
- **Portfolio beta to VN-Index is 1.81**, correlation 0.93. Most deviation from the market is
  leverage, not selection.
- **Four of eight holdings have a negative expected *compounded* return** once volatility drag is
  applied — 68.4% of the book.
- **MBB is one of the three largest lenders to KDH.** Two holdings, one linkage, not previously
  on file.
- **Bank outcomes did not travel across the sector this quarter.** ACB −12%, VIB −8%, MBB +40%
  on PBT — same quarter, same rate environment. Peer read-across was tested prospectively here
  and failed by ~52 percentage points.
- **Foreigners have net sold ₫92,000bn YTD** (>62,000 to May, ~80,000 to June, 92,000 to July) and 2026
  is on track to be the **fourth consecutive year** of net selling — a third independent ground against the
  TCX FTSE event tree, though active outflow and passive inclusion inflow are **different pools and must
  not be netted**.
- **Interbank funding cost rose at every tenor through July** (overnight 2.43%→2.97%, 3-week 5.29%→5.88%)
  **while deposit rates sat still** — and **Circular 25/2026 took effect in the same month**, relaxing a
  ratio while the price moved against it. Loans outgrew deposits **2.2× at TCB** and **13.2% vs a shrinking
  base at MBB**.
- **All three HPG spread inputs are now pinned on the file's own benchmarks:** ore **$98.25**, coal
  **$218.50**, HRC **$535–546.5**. The July move cost **−₫0.437m/t** — coal relief clawed back only 41% of
  the price cut. Spot case **₫0.86–1.10m/t**, still below the ₫1.25m bear branch but the gap has narrowed
  from ₫0.42m to ₫0.15–0.39m.
- **"MBB" pulls at least three entities**: MB Bank (ours), MB Securities, and MBB SE (Xetra).
  Poland's mBank too. Five false hits this session.

## 9 · What is blocked, and on what

**Five** fronts now, not three, all returning **proxy 403**: the TCB bond line (`OPEN-DECISIONS` 17b),
the Federal Register rate tables, the HOSE / MB disclosure pages, **techcombank.com's own Q2
press-release PDF**, and **HPG's statement note on other income** (which is what would settle item 13).
**This is no longer only an access problem — see §4 escalation 5.** **The FiinQuant connector is unauthorised and cannot be authorised
from a non-interactive session.** This is `OPEN-DECISIONS` item 17 and it is now binding on three
fronts at once.

`DEPTH-QUEUE.md` is **exhausted**, and an automated run may only edit status marks — not add or
re-scope items. Every quiet sweep has reported this. It needs a person.

---

## The private dashboard is NOT in this repo, by design

`research-hq-PRIVATE.html` (v7) contains position data and lives only in the session scratchpad.
**This repository is public and it must stay out.** It was delivered to the owner directly. If a
future session needs it, it must be rebuilt from `assumptions.json` plus the owner's position
file — never committed here.

*Maintained by hand at the owner's request. Not auto-generated, not read by any script.*
