# Session handover — state of the book at 2026-07-31

**Updated 04-Aug 02:53 ICT.** *(02:53: tried to score last night's ISM inference against rates pricing and **could not — no post-print futures move is available, so it stays an unscored inference.** The number that did surface is a trap: a piece **published 03-Aug** reports the US 10-year *"finished the week near 4.74%"* — **the week ended 31-Jul, one session BEFORE the ISM print**, so it must not be cited as a reaction to it. **What it is genuinely worth: US 10-year 4.74%, highest since Jan-2025, against a 3.50–3.75% policy rate — "high US long yields keep the dollar firm" is ONE step, not four, and it is the first MEASURED evidence for the FX side of the SBV constraint** rather than for the Fed's likely behaviour. Small correction: the ISM consensus is quoted as both **54.0 and 53.0**; not settled, beat holds either way.)*  *(00:53 — **self-correction of a qualifier I propagated to four documents yesterday.** The four dated drifts imply an **index level at the file's price date of ~1,750–1,770** (beta=1 assumed), and **Monday 03-Aug closed at 1,762.84** — so **the file's prices are approximately right RIGHT NOW; the market recovered ~4.6% from the 24-Jul trough back to them. The staleness has transited through zero.** Two consequences: **(a)** *"E[r] is currently understated"* (17:53) **does not survive** against today's market — it was true relative to late July and the market closed it, not a fix; **(b)** the −4.6% sensitivity I used at 19:53 to call the volatility-drag finding "not robust" **points at the wrong date, so the AS-FILED row — 7 of 8, 93.5% of the book compounding negatively — is the one to read, and I UNDER-CLAIMED that finding.** Weakness stated: the estimate rests almost entirely on **TCX**, the only name with an exact index anchor. **Item 2's urgency is unchanged** — the current error is small and will grow again.)*  *(23:53: **the last unverified `npat_ttm` is resolved and the file's number was 28% too low.** VPBankS FY2025 PBT **₫4,476bn** (revenue ₫7,910bn, >3× 2024, 110% of plan) ×0.8 — the TCX convention — gives **npat_ttm 3,580.8** against 2,800 on file. **`pe_ttm` re-derives 17.81 → 13.93, so VPX's printed trailing P/E was 27.9% too high on the one name whose thesis is earnings quality.** E[r] moved **0.03bp**, demonstrating the 22:53 circularity finding rather than arguing it. **The July margin-room reconstruction was right to 0.61% (3,559 vs 3,580.8) — and that method is now what REPLACES the dead cross-check, so scoring it mattered.** Confidence held at 0.55: a trailing figure does not touch the forward branches confidence multiplies. **All eight `npat_ttm` are now on a filed basis.**)*  *(22:53, model audit: **the `cap_now` repair destroyed the detector that found the errors it fixed.** `pe_ttm` is now derived as `market_cap / npat_ttm`, so `cap_now = market_cap` for ANY `npat_ttm` — **the "mandated market-cap cross-check" that found the VCI and VPX flags is now circular and cannot fail**, and `risk.py` still advertises it as live. **⚠ VCI's flag says "suspend the optimizer add" and ALL THREE of its grounds have lapsed** — share count confirmed to 0.07% by two routes (one today's insider filing), `npat_ttm` now FY2025 FILED 1,342, and `npat_ttm` can no longer move E[r] — **while the brief proposes VCI ADD +6.7pp. Lifting it is a human call and was NOT taken.** VPX's flag is unresolved but re-scoped: it no longer touches E[r], it overstates the **printed P/E by up to 21%** on the one name whose thesis is earnings quality.)*  *(21:53: **US ISM Manufacturing July printed 55.6** — from 53.3, vs 54.0 consensus, **highest since May 2022**, with employment back in expansion for the first time in ~3 years. A dated catalyst named on 02-Aug, resolved on its day. **It partially RESTORES the support downgraded at 12:53**: a strong US print makes a Fed cut less likely, which firms the FX side of the "SBV is boxed in" conclusion that this morning's CPI had loosened — and restores it with measured data rather than inference about Vietnam. **Stated as a four-step inference chain, none of it measured; nothing moved.** Two chains refused outright: **US steel prices are a different benchmark from the Asian one HPG realises**, and **ISM is not the domestic steel industry an ITC injury vote examines**. Next: **US July employment report, Friday 07-Aug**.)*  *(20:53: **item 26 — the most valuable human task on the page — answered as far as arithmetic can answer it, and the answer runs AGAINST the alarm.** Stripping every basis point of provisioning relief (reverting each bank to its own prior-year intensity, −4.7 / −7.2 / −13.8% of H1 PBT): on a flat H2 **TCB clears bull by 3.5%, VPB by 6.5%, MBB clears base.** **The branches are too LOW, not too high** — normalisation closes only 42–55% of the overshoot. **The inverse is the decision number: H2 provisioning intensity needed to justify BASE is TCB 26.7% (2.17× prior), MBB 35.7% (1.08× prior), VPB 65.8% (1.25× prior) — so MBB's branches are defensible under credible credit stress and TCB's and VPB's need a credit EVENT.** Not tested: deterioration beyond last year, with every pipeline deteriorating. Nothing modelled.)*  *(19:53, third audit of the day and the largest: **the 02-Aug `cap_now` repair invalidated every hand-written document quoting an engine number, and three were still wrong.** §1 here (fixed 18:53); **`OPEN-DECISIONS` item 19**, which said *"the engine is BLIND to the best print in the book"* about MBB at +8.8% — MBB is now **rank 1 at +18.3% shrunk, leading by 14pp, with a +6.7pp ADD off branches derived from nothing**; and **`CFA-TOOLKIT.md` §5**, whose volatility-drag table understates its own conclusion — **7 of 8 holdings, 93.5% of the book, compound negatively**, not 4 of 8 / 68.4%, and **only MBB compounds positively.** **Qualified rather than banked: a −4.6% price correction (item 2's measured drift) takes 93.5% → 41.7%, because TCB is 35% of the book at −2.85%.** Direction robust, magnitude hostage to item 2. Nothing modelled.)*  *(18:53: **§1 below was STALE and is regenerated** — it carried the pre-`cap_now`-fix rankings from 02-Aug through seven header updates today, showing **TCX as the top-ranked ADD when the engine now ranks it 7th with a TRIM**, and reversing VCI, VPX and VPB's actions. `DECISION-BRIEF.md` was correct throughout; this summary of it was not. **A fresh timestamp on a stale body is worse than an obviously old file.** Also: street target prices found this sweep are **unusable until dated and adjusted** — TCB's ₫39,000 is quoted pre-60%-bonus and adjusts to ~₫24,375, *below* the model's ₫29,711, so two of three apparent gaps are smaller than their own corporate-action adjustment.)*  *(17:53, two findings. **(a) A US CORE circumvention inquiry on Vietnam has been live since 25-Mar-2026 and this file recorded on 31-Jul that no 2026 case existed — a false negative written WITH an instruction not to re-check it.** Allegation: **CORE finished in Indonesia from VIETNAMESE cold-rolled steel** — a *substrate* channel, not the direct-rebar exposure on file. **Preliminary determination intended 24-AUG**, underlying rates AD 87.07–162.96% / CVD 0.30–257.83%, so near-binary. Root cause is the 15:53 diagnosis: **federalregister.gov is gateway-blocked, so lane 2 runs on press and "nothing in the press" became "nothing filed."** HPG confidence HELD at 0.75 — the exposure is unquantified and cutting on alarm is not evidence; flagged for the human CIO run. **(b) An audit of suppressing negatives turned up a FOURTH dated price and it DATES THE PRICE FILE: KDH 20-Jul −0.28%, TCX 24-Jul −4.6%, TCB 27-Jul −3.4%, VCI 28-Jul −3.9% — the signature of a ~20-JULY file, not the presumed 24-July. That SUPERSEDES the 02-Aug trough argument: E[r] is UNDERSTATED, not overstated.**)*  *(16:53, post-close: **HOSE's VN30 review discloses TCX's average market cap to 30-Jun as ₫116,532bn** — compared cap-to-cap, the corrected share count gives ₫114,007bn (−2.2%) and the stale one ₫95,005bn (−18.5%), so **the exchange settles the count that caused this session's largest error**, from a higher-tier source than the fix. **Second external confirmation of the `cap_now` repair today**, after VCI — two of eight now verified by unrelated documents. **VN-Index closed 1,762.84, clearing the 1,750 level the file explicitly refused to forecast on 02-Aug — the restraint scored.** **Foreign net BUY ₫1,061bn on HOSE** (vs −₫307bn on 31-Jul) with **HPG 2nd (₫283bn) and MBB 4th (₫89bn)** — one session, not a trend, against ₫92,000bn of 7-month net selling. **KDH +3.24% but the whole property sector rose, so it says nothing about VNDiamond.** TCX fell on its effective date, corroborating the flow-date/effective-date distinction.)*  *(15:53: **the KDH/VNDiamond question is BLOCKED BY NETWORK POLICY, not unresearched.** The primary document was found — vietcat.com's official 31-Jul rebalance disclosure for the VNDiamond ETF — and the gateway returned **403** (`connect_rejected`). **ssi.com.vn and ftp2.ssi.com.vn are blocked too**, closing the standing route for every future VNDiamond/VN30 review; ~13 hosts now blocked. **No further dedicated searches** — it resolves only via FiinQuant MCP authorised by the owner, a widened network policy, or incidental mention in routine KDH coverage. **KDH's status stays UNKNOWN.** One substantive gain: **DCVFMVN is ~96% of the ~₫12,300bn six-ETF pool — one fund IS the flow**, so a removal would be a single concentrated programme trade, not six funds spreading it.)* 

**⚠ OWNER ACTION REQUIRED, and it is the binding constraint on this workstream.** The **FiinQuant MCP connector is unauthorised** and **cannot be authorised from a non-interactive session** — it needs the owner in claude.ai connector settings. It would answer index-membership, price and share-count questions directly: the three inputs that have produced this session's largest error (TCX share count), its last broken model input (OPEN-DECISIONS item 2, prices) and its longest-running unresolved question (KDH/VNDiamond, seven failed attempts on 20.3% of the book). Widening the environment's network policy to vietcat.com and ssi.com.vn would substitute for part of it.
 *(14:53: a VCI insider filing — **Tô Hải registering 31.05m shares, 15.13%→17.83%, ~₫612bn, window 04-Aug to 02-Sep** — does three things. It **externally confirms the `cap_now` share count** (1,151.4–1,151.9m from two ratios vs 1,152.24m on file, ±0.07%); it **contradicts the VCI price** (₫19,700 *limit-up* on 28-Jul vs ₫20,500 on file); and it **argues against VCI's own near-certain October kill criterion**, a tension left unresolved. **Qualified: his wife fully divested shortly before — size unknown, so household reallocation is not excluded.** Confidence held at 0.40 (registration ≠ execution). **Biggest read-across: item 2 is now THREE FOR THREE — every dated price sits below the file's, in a 3.4–4.6% band, which points at a systematic DATE OFFSET and REVERSES the 02-Aug "E[r] biased high" conclusion for the whole panel.** No price applied — a partial refresh breaks cross-name comparability in `decide.py`.)*  *(13:53: **the HPG spread bridge's iron-ore input of US$115 has no source.** Fitch's 2026 assumption is **US$100** — set in the same revision that gave the coal 220 this file uses exactly. The 27-Jul note calling 115 "a Fitch forecast" is falsified. Read the bridge's own grid at `ore = 100`: **₫0.86m/t**, identical to the 31-Jul spot repricing — **the "forecast vs spot" gap was the phantom input, not the market.** The recommended `spot_persists` branch is **2.4× too severe as written**. Still below the ₫1.25m bear branch, so the central finding holds; the miss is ₫0.39m/t, not ₫0.89m/t, and **the cost side is delivering no relief.** Nothing modelled; bridge §8 correction appended, item 6 updated.)*  *(12:53: July CPI +4.45% — second consecutive fall, **May 5.60% confirmed as the 2026 peak**. The pre-registered test from 02-Aug 19:53 resolved; the 7-month cumulative average rose 4.38%→4.39% in the same month, exactly as warned. **Core 4.63% now sits ABOVE headline** — the fall is petrol and food, so this is not yet a demand turn. **Level unchanged: still ~0.95pp above `risk.py`'s 3.5%.** The 31-Jul "SBV boxed in on two sides" conclusion now leans mainly on the **inferred** FX support — a downgrade, recorded as such. 3 of the 4 quadruple-date items are resolved; **VNDiamond is the only one left, check after 15:00 ICT**.)*  *(Timestamps on the three sections below dated 20:57 / 21:57 / 22:57 were corrected from 21:53 / 22:53 / 23:53 — they had drifted 56 minutes ahead; see the 23:53 log entry.)* MBB filed (§2, §3). **Two of the four escalations in §4 are now RESOLVED**,
and a new structural one has replaced them — see §4 and §9.

**Written at the owner's request to make this session's context survive the container.**
The session is ephemeral; this file and the git history are not. Everything below is already
recorded in `monitoring-log.md`, `assumptions.json` and `calibration-log.md` — this exists so
a reader arriving cold knows *where things stand* without reading 108 commits.

**Nothing here is new analysis. No trade has been placed or recommended as executed.
The system recommends; a human signs.**

---

## 1 · What the engine currently says

**⚠ REGENERATED 03-Aug 18:53 from `research/decisions/DECISION-BRIEF.md`. The table that stood here
until now was PRE-`cap_now`-FIX and had been stale since 02-Aug — through seven header updates on
03-Aug alone. It ranked TCX first with an ADD; the engine now ranks it seventh with a TRIM.**

`python3 research/models/decide.py`. Ranked by **shrunk** expected return:

| Rank | | Raw E[r] | Conf | **Shrunk E[r]** | Proposed this cycle |
|---|---|---:|---:|---:|---|
| 1 | **MBB** | +36.6% | 0.50 | **+18.3%** | ADD +6.7pp → 13.2% |
| 2 | **HPG** | +6.3% | 0.75 | **+4.7%** | ADD +3.2pp → 20.0% |
| 3 | **TCB** | +4.0% | 0.70 | **+2.8%** | **TRIM −15.0pp → 20.0%** (cap breach) |
| 4 | **KDH** | +3.5% | 0.55 | **+1.9%** | TRIM −3.2pp → 17.1% |
| 5 | **VPX** | −0.0% | 0.55 | **−0.0%** | ADD +5.6pp → 8.4% |
| 6 | **VCI** | −11.3% | 0.40 | **−4.5%** | ADD +6.7pp → 9.8% |
| 7 | **TCX** | −11.2% | 0.75 | **−8.4%** | **TRIM −3.3pp → 2.2%** |
| 8 | **VPB** | −13.9% | 0.70 | **−9.7%** | hold (−0.8pp → 9.2%) |

Book as owned +1.8% E[r] / 29.2% vol; after this cycle +2.7% / 28.9%; north star +3.8% / 28.4%.

**⚠ THE ENGINE'S LARGEST CONVICTION RESTS ON ITS LEAST-DERIVED NUMBERS.** MBB leads by 14pp of
shrunk return, and MBB **has no driver model** — `run.py` builds scenarios for KDH, TCB, VPB, TCX,
VPX and HPG only, so MBB's branches are typed in, derived from nothing and recomputed by nothing.
The brief's own evidence cell says they **require human re-derivation** against a filed H1 that
already implies bear needs H2 −26.6%. **Read the ranking with that in hand.**

**Read these numbers with the blocking caveats in `OPEN-DECISIONS.md` §1 — item 2 above all**
(prices are undated and, as of 17:53, probably ~20-July rather than the presumed 24-July, which
means expected returns are more likely **understated** than overstated). They are not decorative;
each one can move the ranking.

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

### 02-Aug 22:57 — earnings-quality sweep COMPLETE across the book; TCX is the counter-example

**TCX Q2/2026: revenue +41%, costs +78.6%, PBT +21%, margin 65.2% → 56.0%.** Profit grew at **half** the
rate of revenue. Where the banks' reported profit outran their operating line, **TCX's lags its own top
line — nothing is flattered here.**

- **⚠ But: TCBS arranged ~₫61,000bn of bonds in Q2, +138%** (~₫59,000bn non-bank corporate, **48% share,
  #1 in Vietnam**) **while that segment's net income rose just 7% to ₫964bn.** Volume +138% → income +7%.
  Fee compression, low-margin volume, or undisclosed offsets — **not established, not guessed.** A
  growth-quality problem, not an accounting one.
- **It joins the 18:53 Masterise finding:** TCBS is registrar for Masterise-linked paper, H1 issuance
  ₫44,500bn. **The Masterise exposure sits inside the ₫964bn segment growing at 7%** — the part of TCX most
  connected to the property-bond complex is its weakest-growing line. **Share of arranged volume that is
  Masterise-linked: not established.**

**BOOK-WIDE PICTURE NOW COMPLETE:**

| name | earnings-quality read |
|---|---|
| TCB / MBB / VPB | flattered by falling provisioning intensity — **5.8 / 9.2 / 23.4pp** of growth |
| VPX | FVTPL test **unevaluable** (gross vs net give opposite answers) |
| VCI | profit **−26% QoQ** behind a +36% YoY headline; OCF negative, prop book −₫430bn |
| **TCX** | **profit lags revenue — understated, not flattered** |
| KDH / HPG | one-off gains already documented (deconsolidation; Q1 divestment) |

**Confidence not moved (0.75).** Favourable on accounting, unfavourable on operating leverage — they
offset. TCX's live issue remains the multiple and the undated price.

### 02-Aug 21:57 — the same lens on the brokers: VPX's kill criterion is UNEVALUABLE

**For a bank the discretionary line is the credit charge; for a broker it is FVTPL.** VPX's armed criterion:
*"FVTPL marks > 50% of PBT for a third consecutive quarter."*

| quarter | FVTPL gross | PBT | ratio |
|---|--:|--:|--:|
| Q1/2026 | ₫1,822bn | ₫514bn | **354%** |
| Q2/2026 | ₫1,639bn | ₫2,159bn | **76%** |

- **Two consecutive quarters above the test on a GROSS reading** — the criterion needs three, so **it has
  not fired**; Q4/2025 (not on file) decides whether Q3 could be the third.
- **⚠ But gross and net give OPPOSITE answers.** The file's existing *"Q2 absorbed a ₫923bn FVTPL loss, prop
  netted >₫700bn"* reconciles exactly: **₫1,639bn gross − ₫923bn = ₫716bn net.** On gross Q2 is **76%** and
  the chain continues; **on net it is 33% and the chain breaks.** **The criterion does not say which.**
- **Second undefined armed criterion today**, after TCB's *"a Masterise bond event"*. **New OPEN-DECISIONS
  item 27.** A criterion that cannot be evaluated is not a safeguard.
- **Franchise point, sharper than the file had it: Q2 brokerage revenue was ₫126bn of ₫4,098bn — 3.1%.**
  Margin lending and FVTPL are the business. Bond book now >₫18,000bn.
- **Period trap disarmed by division:** the source put ₫1,904bn "27% of revenue" in a Q2 list; ₫1,904bn is
  46.5% of Q2 revenue — it is an **H1** figure. Not used.

**Confidence not moved (0.55): the finding is a test that cannot be evaluated, not a resolved fact.**

### 02-Aug 20:57 — VPB's provisioning gap is CLOSED, and it breaks the peer pattern both ways

**The 20:53 standing check is answered. Refusing to infer it from TCB/MBB was correct.**

| | prov/PPOP prior → now | change | **PPOP growth** | provisioning share of PBT growth |
|---|--:|--:|--:|--:|
| TCB | 12.2% → 7.9% | −4.3pp | +16.7% | 5.8pp of 22.5 |
| MBB | 32.9% → 27.6% | −5.3pp | +17.9% | 9.2pp of 27.1 |
| **VPB** | **52.8% → 45.2%** | **−7.6pp** | **+44.6%** | **23.4pp of 68** |

- **Provisions ROSE 23.7%** to ₫15,579bn — the opposite of both peers. On the crude question VPB looks the
  most conservative.
- **Yet intensity fell the MOST (−7.6pp)** — so **23.4pp of the 68% growth** is lower provisioning
  intensity, the largest contribution of the three. Derived 45.2% matched reported 45.2% **exactly**
  (second method validation today).
- **And the underlying business is by far the strongest: PPOP +44.6%** vs ~17% at both peers. **VPB's
  growth is not manufactured the way the peers' partly is.** All three are true; each alone misleads.
- **⚠ Group 4 "doubtful" debt +44.5%** (₫10,880bn → ₫15,718bn) **while the NPL ratio FELL 3.33% → 3.28%.**
  Third instance today of a ratio diluted by loan growth — **and VPB's NPL ratio is already double the
  peers'.**
- **FE Credit: ₫6,158bn of provisions — ~40% of the group charge — for ₫152.6bn of profit.** Sharpens the
  existing note: not merely immaterial to profit, it consumes 40% of the credit charge to produce it.
  Bears on item 11.
- **Confidence HELD at 0.70, deliberately.** Evidence completeness argues up, 23.4pp flattering plus
  group-4 argues down; **deciding which dominates is item 26's branch rebuild, not a scalar move.**
- **Noted, not pursued:** VPB put **₫1,100bn into a tokenised-asset exchange** — touches VPX's CAEX option.
  **Same venture? Not established.**

**The three-bank provisioning picture is now complete at 51.5% of the book.**

### 03-Aug 11:53 — July PMI 52.9, and it corroborates two independent threads

**Date-gated item resolved on schedule. PMI 52.9** (Jun 51.8, May 52.8) — **highest of 2026**, **13th
consecutive month** above 50, improvement the most marked since February, **new orders near a record**, and
**output growth fastest since March 2011**.

*(Source discrepancy flagged, not resolved: one headline says the PMI rose fastest in 13 years, another
dates OUTPUT growth to Mar-2011 — different measures, neither adopted as the other. The 52.9 level is
consistent.)*

- **⚠ Corroborates the FDI finding from one hour earlier:** manufacturing took **82.6% of realised FDI** in
  the best half in five years; now manufacturing **output** prints at a multi-year high. **Same story, two
  angles, found independently.**
- **⚠ Corroborates the CPI withdrawal from 19:53 yesterday:** the PMI release reports **easing inflationary
  pressure**, pointing the same way as the monthly CPI series peaking in **May (5.60%)** and falling to
  **4.69%** in June. **Does not settle it** — a survey is not the CPI — **and July CPI is still due today.**
- **Per-name, with the limit stated: HPG (16.8%)** — supportive of **volume**, but **the binding variable is
  the SPREAD** (bear branch ₫1.25m/tonne), which this does not touch. **Must not be read as relieving the
  spread case. KDH (20.3%)** — bears on the **Lê Minh Xuân industrial park**, its one non-residential
  segment.
- **Nothing modelled** (no PMI input in `run.py`); **no confidence moved.** PMI gate **CLOSED**.
- **Held the no-KDH/VNDiamond rule until 15:00.**

### ⚠ 03-Aug 10:53 — foreign capital runs TWO ways; the file only had one

**Zero repo hits for FDI** — while it carries extensive foreign **portfolio**-flow data and a thesis ground
built on it.

| flow | H1/2026 | per month |
|---|--:|--:|
| foreign **portfolio** (7M) | −₫92,000bn ≈ −US$3.52bn | **−US$0.50bn OUT** |
| foreign **direct**, realised (6M) | **US$13.03bn, +11.2%** | **+US$2.17bn IN** |

**FDI inflow is ~4.3× the portfolio outflow per month.** Best H1 in five years; **registered FDI US$34.65bn,
+61%, a record.**

- **⚠ Item 5's third ground is NARROWED but SURVIVES.** *"The marginal foreign dollar has been negative for
  four years"* is **true of portfolio flows, false of foreign capital overall.** The ground holds — the FTSE
  event is an equity event — but the phrase now reads **"the marginal foreign PORTFOLIO dollar."**
- **The file made this distinction once and stopped a level short:** the 31-Jul note separated *active* from
  *passive* equity money. **Portfolio vs direct is the same discipline one level up, unapplied.**
- **Per-name:** manufacturing took **82.6%** of realised FDI (US$10.76bn) — bears on **HPG volumes** and
  directly on **KDH's Lê Minh Xuân industrial park**, the one non-residential segment. **Real estate took
  just 7.4% (US$965m)** — foreign direct money is *not* going into property, consistent with KDH's
  residential collapse.
- **Currency:** US$13.03bn of disbursement is a dong support the 02-Aug USD/VND note lacked, with the
  central rate at a record ₫25,338.
- **July PMI and CPI still not published** at 10:53; both due today. **Held the no-KDH rule until 15:00.**

### 03-Aug 09:53 — stopping rule expired, data NOT reachable: check after 15:00, not 09:00

**My route was right and my clock was wrong.** At 05:53 the VNDiamond search route was abandoned with
*"resolves TODAY by observation… market opens 09:00 ICT"*. The session has run 54 minutes and **web search
does not index intraday Vietnamese equity prints** — two attempts returned nothing from today.

- **⚠ REVISED: the HOSE close is ~15:00 ICT and coverage publishes after it. Check after 15:00.** Without
  this the next five hourly sweeps each re-check and find nothing — the exact waste the stopping rule
  existed to prevent. **A route with a wrong time still burns budget.**
- **Nothing adopted from the results:** a bundle contradicting itself across dates (index slightly down with
  56% of codes off >1% / up ~40 points with foreigners net buying / ~3% recovery). **Third mixed-date market
  summary in three days.**
- **Undated lead, NOT adopted:** ~**₫2,554bn foreign net selling "in the week"**, down >30% on the prior
  week, **TCB, VPB**, VHM, VIX, ACB most sold; VIC, VNM, **HPG**, FPT, VCB most bought. Fits the ₫12,000bn
  July run-rate (~₫2,800bn/wk) **but is not dated.** **TCB + VPB are 45% of the book and the file carries
  foreign selling only in aggregate and for KDH.** **For a post-close sweep to date.**
- **Trigger 5 remains live on KDH. Nothing modelled; no confidence moved.**

### ⚠ 03-Aug 08:53 — KDH's Q2 one-offs EXCEED the quarter's profit; inventory is far larger than the file had

**No holding has filed its H1 reviewed statement early — the 14-Aug gate stands.** But the check returned
the Q2 profit composition.

**~₫875bn of capital-transfer gains + ~₫22bn of transfer-price-vs-book-value = ₫897bn of one-offs, against
Q2 NPAT of ₫770bn — 116% of the quarter's entire profit.**

| reading | one-offs post-tax | residual from everything else |
|---|--:|--:|
| ₫897bn is **pre-tax** (20%) | ~₫718bn | **+₫52bn** |
| ₫897bn is **post-tax** | ₫897bn | **−₫127bn** |

**Basis not established. The range IS the finding — do not quote the −₫127bn alone.** The **14-Aug reviewed
statement will state the tax treatment**, so this collapses on a known date.

- **Corroboration both ways:** `q2_financial_income` on file is **₫906bn** vs **₫897bn** itemised — a **1%**
  match, so they are the same money seen two ways.
- **⚠ Balance sheet moves opposite to the income statement:** **inventory ₫29,488bn, +27% YTD** (file had
  *"above ₫23,000bn"*) and **total assets ₫39,471bn, +16%** — **inventory +27% while H1 revenue fell 75%**
  (₫442bn vs ₫1,759bn), funded by the ₫6,500bn of extra borrowing already on file. **That is what the
  one-off gains are masking.**
- **New bases:** H1/2025 revenue **₫1,759bn**; Q2/2025 NPAT **~₫196bn**.
- **Confidence held at 0.55** — sharpens a known picture rather than changing an input; **branches need
  re-derivation (item 4)**, which a scalar cannot substitute for.

### ⚠ 03-Aug 08:02 — WEEKLY REFRESH run 1: nothing filed, but a filing gate is 11 DAYS AWAY and uncalendered

**STEP 1: nothing new filed.** All eight Q2/2026 statements are in; last refresh 11.5h ago. **On the letter
of STEP 1 this run should not have committed — the departure is stated in the log entry, with reasons.**

**⚠ The file believed its next filing gate was Q3 on 30-Oct (88 days). It is 11 days.** Circular 96/2020
also requires **semi-annual AUDITOR-REVIEWED statements**:

| filing | due | days |
|---|---|--:|
| **standalone / parent — REVIEWED** | **2026-08-14** | **11** |
| consolidated — REVIEWED | 2026-08-29 | 26 |

**Zero repo hits for "soát xét" / "bán niên" — the concept was absent.**

- **These are auditor-reviewed; the quarterlies on file are self-reported. A review can RESTATE them.**
  Every Q2 figure treated as a filed actual since 29-Jul is a management number not yet audited.
- **⚠ The 14-Aug standalone filing settles KDH's ₫321bn vs ₫1,097bn basis question** — the confusion that
  caused the "Q2 profit ≈ zero" cascade, a wrongly scored forecast and a false escalation. Also bears on
  **item 17b** (TCB bonds), **HPG's debt currency mix**, **VPB's provisioning detail**.
- **Mid-August is dense: 14-Aug is one day before the 15-Aug two-circular cluster** — three dated events in
  two days on 71.8% of the book. **Added to the gate table.**
- **STEP 2:** no new bank data; PPOP analysis unchanged (TCB 5.8pp / MBB 9.2pp / **VPB 23.4pp, resolved
  20:57**). **⚠ The routine's own prompt is already stale** — it still calls VPB's provisioning "the
  standing open check". **Flagged, not edited**; rewriting a scheduled prompt unasked is not appropriate.
- **STEP 3:** no model input changed — `npat_ttm`, `pe_ttm`, `shares_outstanding`, `market_cap_bn`,
  `confidence` all untouched. **STEP 4: no trigger fires.**
- **⚠ Process:** the routine's prompt says *"Q3 is due 30-Oct"* — **I wrote it yesterday from this file, so
  it inherited the blind spot** and would have repeated it weekly. Item 12's problem, except **this copy
  didn't drift — it was born wrong.**

### 03-Aug 07:53 — the cross-check ran once and found two index defects

**Applied the 06:53 lesson** (*grep OPEN-DECISIONS for a holding whenever a sweep records a figure about
it*), retroactively over 24 hours.

- **⚠ Item 11 was materially mis-stated.** It says `run.py` is wrong to call FE Credit NPL formation the
  swing factor, since FE Credit is 0.8% of profit. **Both halves are true of different lines:** FE Credit's
  H1 provisions were **₫6,158bn of ₫15,579bn group — 39.5% of the credit charge** — for **₫152.6bn = 0.81%
  of PBT.** **It consumes ~49× more of the charge than it contributes of the profit.** `run.py` is wrong
  about profit and **defensible about provisioning**; the fix is to **name the line**, not delete the claim.
  **Second-order, for item 26:** a subsidiary taking 39.5% of the charge for 0.8% of profit is exactly where
  provisioning flattery can originate.
- **⚠ Items 19 and 20 each exist twice** (§1/§4 = MBB branches, KDH land-use fee; CFA section = λ,
  volatility corridors). **Log entries and commits cite them ambiguously.** **Fixed by disambiguation, not
  renumbering** — the log and git history are append-only and already cite those numbers. Read the CFA ones
  as **CFA-19 … CFA-23**; every pre-03-Aug reference means the §1/§4 item. **New items number from 24 up.**
- **Fifth instance of a quantity/link recoverable from what the file already held — and the FIRST caught
  prospectively by a check** rather than by accident.

**Lane clean: July PMI still not out** (June 51.8, May 52.8 on file and correct; release ~11:00 ICT).
**Stopping rule held — no VNDiamond searches. Market opens in one hour.**

### ⚠ 03-Aug 06:53 — item 17b, "the highest-value single line in the repo", is PARTLY ANSWERED

**The answer entered the file yesterday, from a different article.** Item 17b asks for TCB's corporate bond
balance at 30-Jun-2026, marked blocked behind a proxy 403. The 02-Aug provisioning sweep logged **"corporate
bond book +80%"** alongside Group 2 loans +46%. **That is the change 17b asks for**, and nothing connected
them for a day.

- **It reverses the 28-Jul inference in sign AND magnitude.** That note said the bond book *"must have
  shrunk… every plausible starting point implies a large decline"* (57%/32%/18%). It **grew 80%.** The
  01-Aug withdrawal is now emphatically confirmed.
- **On removal-vs-relocation:** TCB cut real-estate exposure ₫39–40,000bn while the bond book grew 80% —
  **consistent with RELOCATION, but it does not establish it.** **"Corporate bonds" ≠ "property bonds" and
  the composition is NOT established. No Masterise link drawn** — that is the 01-Aug near-miss exactly.
- **Still missing:** (a) the **base period** (+80% vs 31-Dec-2025 or vs H1/2025 — 17b wants the year-end);
  (b) the **absolute balance**.
- **⚠ Reconstruction refused, deliberately.** The balance solves in principle from credit growth, loan
  growth and the +80% — but **14.3% credit is STANDALONE (incl. quota-exempt infra/social housing) while
  ₫835,813bn loans is CONSOLIDATED.** Solving across them yields a number with **no defined meaning**, so
  **none was produced** (01-Aug lesson). **Revised ask: both rates on the same basis, or the balance itself.**
- **Fourth instance** of a quantity recoverable from what the file already held — after `cap_now`, KDH's
  percentage pair, MBB's provisions.

**Held to the 05:53 stopping rule: no VNDiamond searches. Market opens 09:00.**

### 03-Aug 05:53 — VNDiamond: two corrections, and the search route is ABANDONED

- **The tracking pool is SIX ETFs, not four.** The file names four (FUEVFVND ₫12,070bn, MAFM ₫345bn, KIM
  ₫71bn, VFCVN unknown) and says *"the four"* five times. **BVFVN Diamond and ABF VNDiamond were never on
  file.** `found_total` ₫12,486bn is a **floor, not a total**. **Proportion: FUEVFVND is 96.7% of it, so the
  ~₫72bn KDH forced-flow estimate barely moves — the defect is the completeness claim, not the magnitude.**
- **Constituent count unresolved.** File says **19**; a Q2/2026 source says **18** (9 banks + 9 non-banks,
  no additions) — **but that document is a PREDICTION report and the language is forward-looking, so 18 may
  be a forecast.** Both recorded, neither adopted.
- **⚠ STOPPING RULE: the fifth failed attempt on whether the August review removed KDH.** All five returned
  Q2/2026 material. The 01-Aug entry recorded this as a negative result *"so the next sweep does not re-run
  it"* — **and it was re-run three times since.** **The search route is abandoned.**
- **It resolves TODAY by observation:** changes are effective today, market opens **09:00 ICT**, and **KDH's
  own volume and price action plus the ETFs' published holdings will answer it.** **No further searches
  before 09:00.** **Trigger 5 remains live on 20.3% of the book** — this is a budget discipline, not a
  judgment that the question stopped mattering.

### ⚠ 03-Aug 04:53 — HPG's interest step is STRUCTURAL and geared against the bear branch

**The cause is now known: after Dung Quất 2 reached full capacity, HPG no longer capitalises borrowing
costs into construction-in-progress — it expenses them.** While DQ2 was building, that interest never
touched the P&L. **A permanent, one-direction change**, still working through (Q1 interest **2× Q1-2024**
and **+14% on Q4-2025**).

**Debt was flat in Q1 and jumped in Q2:** ~₫90,394bn end-2025 → **₫90,600bn** end-Mar (+₫206bn, **69%
short-term**) → **₫98,530bn** end-Jun (**+₫7,930bn, +8.8%**). Recent and short-dated.

| branch | FY volume | interest/tonne | % of core NPAT/tonne |
|---|--:|--:|--:|
| **bear** | 13.5m t | **₫0.421m** | **33.7%** of ₫1.25m |
| base | 14.5m t | ₫0.392m | 24.5% of ₫1.60m |
| bull | 15.5m t | ₫0.367m | 19.8% of ₫1.85m |

- **⚠ Interest per tonne is inversely geared to volume, so the bear branch is hit twice** — low volume, and
  the high per-tonne burden that low volume creates. 02:53 showed no branch *responds* to interest; this
  shows the direction it would respond in is **adverse to the downside**.
- **Stated fairly:** the burden **falls** as DQ2 ramps (₫0.421m → ₫0.367m) — **that is the point of the
  investment.** Operating leverage in both directions, **and the model shows neither.**
- **Currency mix STILL not established** after two searches. Bounded only: Q1 financial costs ₫1,868bn less
  interest ₫1,333bn = **₫535bn of non-interest financial cost — an upper bound on any FX loss, not a
  measurement.** Remains the next cheap check.
- **Item 28 sharpened. Nothing modelled; confidence not moved.**

### 03-Aug 03:53 — KDH: a documented Layer-4 governance finding, but time-barred

**Government Inspectorate Conclusion 46/KL-TTCP, 06-Feb-2026** — absent from the repo. Found at KDH:
**bond proceeds used to repay debt** rather than for working capital as disclosed (reported **>₫100bn**);
**offering documents not accurate, truthful or verifiable**; **late disclosure**.

- **⚠ NO penalty was imposed — time-barred** under art. 6.1(d), so UBCKNN issued no decision. KDH must
  implement the conclusion and comply going forward.
- **The statute point cuts both ways.** Time-barred means the conduct is **old** (almost certainly the
  2021–22 placement wave), so **this is not evidence about current conduct**, and KDH's AGM calls it
  bond-debt free today. It also means it was never tested in a proceeding.
- **Proportion: ₫100bn is small** against >₫23,000bn inventory and +₫6,500bn H1 borrowings. **The
  significance is the conduct, not the amount.**
- **Why it is on file:** `run.py`'s footer says Layer-4 governance items are **not** in the numbers, and the
  KDH dossier carried the An Lap concern only as a **hypothetical**. This is the same family, **documented
  by a state inspection**, on the **second-largest position (20.3%)**.
- **Confidence held at 0.55**, with the case for cutting stated: KDH's inputs come from KDH's disclosures
  and a regulator found those wanting. **Against (prevailing):** time-barred, pre-dates every model figure,
  no penalty — and the scalar cannot encode a governance opinion. **Escalated, not applied.**
- **No link drawn** to the TCB/TCBS Masterise-registrar finding. Thematically adjacent, mechanically
  unrelated.

### ⚠ 03-Aug 02:53 — HPG's missing interest line is now SIZED: 24–36% of the model's central metric

**Record debt ₫98,530bn at 30-Jun-2026, +9% in six months**, mostly short-term working-capital borrowing.
**Q1/2026 financial costs roughly doubled to ~₫1,868bn; interest expense >₫1,333bn — ~₫15bn/day.**

| branch | core NPAT/tonne | interest (₫0.444m/t) as % |
|---|--:|--:|
| bear | ₫1.25m | **35.5%** |
| base | ₫1.60m | **27.8%** |
| bull | ₫1.85m | **24.0%** |

Annualised: **₫5,332bn = 24.2% of the ₫22,000bn FY target.**

- **This is NOT an arithmetic omission.** NPAT is struck after interest, so it sits inside the observed core
  NPAT/tonne. **The defect is that no branch RESPONDS to it** — volume and spread vary, interest per tonne
  is constant by construction, while debt rose 9% and financial costs doubled. **Worst in the bear branch.**
- **Compounds with USD/VND at a record ₫25,338** *if* material USD debt — **currency mix not established**,
  and it is one line off the balance sheet. **Next cheap check.**
- **New OPEN-DECISIONS item 28.** Branch construction is human-only.

**⚠ Figure rejected from the same source:** it also claimed H1 profit *"₫10,539bn, 67% of plan"*. **The
file's ₫15,480bn is corroborated three ways** — 70.4% of the ₫22,000bn target, 9,056 + 6,424 = 15,480
exactly, and +104% on H1/2025's ₫7,600bn matching the filed +103%. **₫10,539bn at 67% implies a ~₫15,730bn
plan — 2025 vintage.** The revenue figure in the same summary (₫108,870bn, +47%) **is** correct for H1/2026.
**Second bundled true-plus-stale summary in two hours.**

**Undated lead, NOT a finding:** a report that **KDH was cited for violations in bond issuance and use of
proceeds** — zero hits in the repo, no date established, and KDH's AGM described it as bond-debt free.
**For the next sweep to date.**

### 03-Aug 01:53 — Moody's separated our three banks in MAY and the file never knew

**04-May-2026:** Vietnam's sovereign outlook **Stable → Positive**, Ba2 affirmed. **05-May-2026:** six banks
raised to positive outlook — **Vietcombank, BIDV, Agribank, VietinBank, ACB and VPBank.**

- **⚠ VPB is on the list. TCB and MBB are not.** The file has treated the three as a bloc on funding and
  rating questions; a rating agency has separated them.
- **Absence is NOT a verdict.** Whether TCB/MBB were assessed and left unchanged, rated by Moody's at all,
  or outside the action's scope is **not established and not assumed** — the same discipline that held on
  VPB's provisioning, where a strong three-name pattern would have predicted the wrong sign.
- **Specific connection:** the upgrade is framed as an advantage in accessing **international capital
  markets**, and **VPB has a live 624m-share foreign placement** (lane 3's "$250m placement"). **VPB carries
  an armed criterion: *"placement prices badly — executed >15% below market."*** This is evidence bearing on
  an armed criterion.
- **Tension to keep visible:** VPB is **last on corrected E[r] (−13.9% raw)** *and* the only one of our
  banks with a positive outlook *and* has the strongest operating line (**PPOP +44.6%**). All three at once.

**⚠ Large trap disarmed:** an article had the VN-Index at *"a record high of 1,929 in early Friday trade"*.
**Friday's close was 1,735.78, and the file's own `vnindex_q2_peak` is 1,927** — the "record" is the Q2 peak,
the article is from early May. The index is **~10% below it, down four straight weeks.** Caught by a stored
value, not a search. Also stale in the same piece: a UOB FX forecast treating Q1/2026 as future. The Fed
line matched `fed_funds_target` exactly.

**Confidence not moved — context, not a model input. July PMI and CPI still not out.**

### 03-Aug 00:53 — KDH's share count is CORROBORATED; the proof was already in the file

**KDH's insider disclosure — 0.056% → 1.838% on a 20,000,000-share purchase — implies 1,122,334,456 shares
outstanding**, agreeing to **0.024%** with the 1,122,060,000 derived from charter capital on 2-Aug. It also
**rejects** both rivals: 1,011.1m would give 1.978pp and 1,000.5m would give 1.999pp against a filed
1.782pp. **The 2025 111m-share issue executed.**

- **Discharges the 12:53 caveat** that the issue was *"a plan with a closed window, not a completion
  notice."* **KDH's trigger-3 firing (+16.1% → +3.5%, 12.6pp) on 20.3% of the book now rests on a
  corroborated count**, confirmed two independent ways.
- **No search was needed** — the pair had sat in the date-gate table for days, read only as a signal about
  insider conviction. **Third instance of a quantity recoverable from figures already held** (`pe_ttm ×
  npat_ttm`, MBB's provisions, this).
- **Nothing modelled**; the number it confirms is already the number in use.

**Rest of the sweep empty and expected:** July PMI and CPI publish today, not yet out; June PMI 51.8 / May
52.8 already on file and correct.

### ⚠⚠ 02-Aug 20:53 — USER-DIRECTED: provisioning is flattering bank PBT. And the data refresh closes item 25.

**PPOP = PBT + credit provisions. PPOP is the operating line; PBT is the headline.**

| | PBT H1/26 | growth | provisions | change | **PPOP growth** | **provisioning share of growth** |
|---|--:|--:|--:|--:|--:|--:|
| **TCB** (35.0%) | ₫18,540bn | +22.5% | ₫1,587bn | **−24.6%** | **+16.7%** | **5.8pp of 22.5pp** |
| **MBB** (6.5%) | ₫20,188bn | +27.1% | ₫7,701.9bn | **−0.9%** | **+17.9%** | **9.2pp of 27.1pp** |

- **Both pipelines move the other way.** TCB: **Group 2 loans +46%, corporate bonds +80%.** MBB: **NPL
  balance +27% vs loans +13.2%** — bad debt grew at twice the pace of the book while provisions stayed flat.
- **Why the ratios hide it:** MBB's NPL *ratio* is 1.45% and coverage *rose* to 93.63%. **Loans are the
  ratio's denominator**, so a 27% rise in bad debt is a 3bp move. Coverage rising while the balance rises
  means **the reserve was topped up without a matching P&L charge** — recoveries/write-backs, not
  repeatable revenue.
- **Method validated:** MBB provisions derived as TOI − opex − PBT = **7,703** vs reported **7,701.9**
  (0.01%). **Runs on any bank whose income statement is on file.**
- **Sector, not held:** Vietcombank Q2 PBT **+57.9%** with provisions **−38%**.
- **⚠ THE GAP: VPB (10.0%) grew PBT 68% and its provisioning line is NOT established.** Largest unexplained
  jump in the book. **Not inferred from peers** — that is the 31-Jul lesson. One search settles it.

**DATA REFRESH — `cap_now` now correct on all eight; OPEN-DECISIONS item 25 CLOSED.** `shares_outstanding`
and `market_cap_bn` are explicit fields; `npat_ttm` from filed statements with the basis recorded per name;
`pe_ttm` = market cap ÷ `npat_ttm`, so `cap_now` = shares × price exactly. TTM computable for **HPG, TCB,
VPB, MBB (68.3%)**; FY2025 used for KDH/TCX/VCI; **VPX `npat_ttm` unchanged**, `pe_ttm` corrected.
**`pe_ttm` is no longer cross-name comparable.**

**⚠ Ranking reordered:** raw E[r] **MBB +36.6 · HPG +6.3 · TCB +4.0 · KDH +3.5 · VPX −0.0 · VCI −11.3 ·
TCX −11.2 · VPB −13.9.** The former top two (VPX, TCX) are now fifth and seventh.

**Confidence:** TCB 0.80→**0.70**, MBB 0.55→**0.50** (reported PBT is lower-quality by a quantified amount),
HPG 0.70→**0.75**, KDH 0.50→**0.55** (filed actuals). **`fy26e_npat`, `exit_pe`, `probs` untouched** —
**re-deriving the bank branches onto a PPOP basis is now the most valuable human task in the repo.**

**⚠ Prices are the last weak link: still undated, presumed 24-Jul, demonstrated wrong for TCX by 4.85%.
Item 2 is the only input left between this file and a trustworthy ranking.**

**Recurring job created:** `trig_013ufGFB2857Btru5wJjZyHL` — weekly Mondays 08:00 ICT (01:00 UTC), fires
into this session. Checks new filings, runs the PPOP/LLR analysis as a standing step, refreshes
`npat_ttm`/shares/`pe_ttm`, runs the engine, checks triggers, commits.

### 02-Aug 19:53 — "inflation accelerating" is WITHDRAWN; CPI peaked in MAY

**The LEVEL finding stands. The DIRECTION claim is withdrawn.** The 31-Jul note argued acceleration from
*"2M +2.94%, 4M +3.99%, 5M +4.31%, 6M +4.38%"* — **cumulative averages, not monthly rates.** An average
rises whenever the newest month exceeds it, so **it cannot turn until the monthly rate is already below it.**

| Jan | Feb | Mar | Apr | **May** | **Jun** |
|--:|--:|--:|--:|--:|--:|
| 2.53% | 3.35% | 4.65% | 5.46% | **5.60% peak** | **4.69% (−91bp)** |

- **The file already held the disconfirming figure** — *"June alone was −0.39% m/m but +4.69% YoY"* sat one
  sentence after the word "accelerating" and was never compared to it.
- **Survives untouched:** June CPI at 4.69% is still **1.19pp above the 3.5%** in `risk.py`'s threshold, so
  the "repo understates inflation" finding and that open item are unchanged.
- **Weakens:** the chain *inflation accelerating → SBV room closing → tension with 1.7–3.2× system credit
  growth and the 40% funding ratio*. **Not reversed — one month is not a trend.** The honest state is that
  **the direction is unknown and the file was asserting one**, on 51.5% of the book in banks.
- **Tomorrow's print is now a real test.** **Do not judge it by the cumulative average** — that will keep
  rising for months either way.
- **Trap disarmed:** a *"CPI tháng 7 +0.48%"* article is **not** July 2026. Four searches confirm the latest
  GSO data covers six months; the fetch 403'd, so **the repo's own 03-Aug date gate was the sole line of
  defence** — the first time that has been true.

**Nothing modelled; no confidence moved.**

### 02-Aug 18:53 — the TCB/TCX Masterise link is CURRENT, established from TCBS's own website

**`tcbs.com.vn` publishes a bondholder record-date notice for bond IHP32602.** The 17:53 entry recorded
TCBS-as-registrar as an inference *"explicitly NOT established"*; it is now **primary-source established
for that lot** — ₫5,000bn, issued 30-Jun-2026.

- **Scoped:** this covers **IHP32602 specifically**, **not** all ₫44,500bn of H1/2026 issuance. What it
  changes is that **the structure is live, not a 2022–23 relic** — the gap the 17:53 period flag named.
- **The issuer, Hưng Phát Invest Hà Nội**, has three lots totalling **₫16,950bn** with **accumulated losses
  of ₫208bn** and coupons of **10.0–10.6%** against system deposit rates near 5–6%.
- **⚠ Refinement to my own 17:53 statement.** I said 12–60 month terms mature "H1/2027 to H1/2031, so the
  ₫44,500bn does not contribute to any 2026 maturity wall". **The 2026 part stands**, but it implied an even
  spread: **₫12,650bn of ₫16,950bn — 75% — falls in H1/2027** (an 18-month lot from Oct-2025 maturing
  ~Apr-2027, and a 12-month lot maturing Jun-2027). **A range is not a distribution.**
- **⚠ Entity boundary problem in an armed criterion.** Hưng Phát Invest bets on **Grand Marina Saigon**
  (Masterise) **and Cần Giờ** (Vingroup/Phạm Nhật Vượng) — the ₫9,300bn was raised to take transfer of part
  of the latter. **"Masterise-related" is a loose label**, and TCB's kill criterion names *"a Masterise bond
  event"* on a **35%** position. **Definitional, not data — criterion wording is human-only.**

**Evidence status changed; no model input did.** No trigger claimed mechanically, no confidence moved.
Layer 4.

### 02-Aug 17:53 — the Masterise exposure runs through the BROKER too, not just the bank

**⚠ Period flag first: this is STRUCTURE, not news.** The supporting article cites **2022** reports — a
2022–23 era story. **Nothing has happened recently.**

**Seven enterprises on the Sài Gòn Bình An project raised ₫32,905bn of bonds, and TCBS — which is TCX —
was the DEPOSITARY for all of them.**

- TCB's kill criterion is *"developer/related-party NPL formation > 2.0%, **or a Masterise bond event**"*.
  The file has treated that as **TCB-only, a bank lending question**. On this structure **a Masterise bond
  event plausibly reaches TCX too** — fee income, reputation, distribution liability, possibly inventory.
  **TCB 35% + TCX 5.5% = 40.5% of the book in one cluster.** Added as a **second independent ground** to
  OPEN-DECISIONS item 7 (`corr_same_cluster` at 0.80).
- **Disclosure gap, same period caveat:** of the seven, only SDI Corp had published payment and financial
  reports; the rest published nothing, and Osaka Garden had settled lot OSGCB2122001 with the information
  still absent from HNX. **Whether they report now is NOT established — that is the check.**
- **Current and separate:** H1/2026 Masterise-linked issuance was **₫44,500bn across 6 enterprises / 8
  lots**, 9–10%, 12–60 months, mostly collateralised, with **"a securities company"** as registrar —
  **the source does NOT name it.** That it is TCBS is a **natural inference and explicitly NOT
  established**; identifying it is **the highest-value cheap check now open on TCB**.
- **Term arithmetic cuts against alarm:** 12–60 months from H1/2026 matures **H1/2027–H1/2031**, so the
  ₫44,500bn contributes **nothing** to a 2026 maturity wall.
- **New context:** VIS Rating puts **~₫60,000bn of RE bonds maturing in H2/2026 — nearly half of all
  corporate maturities.** That is the environment a "Masterise bond event" would occur in.

**Layer 4, nothing modelled, no confidence moved, no numeric driver changed.**

### 02-Aug 16:53 — the causal chain behind HPG's August cut, and it is a DOUBLE hit

**The EU's new steel mechanism, effective 01-JUL-2026, cut India's HRC quota to the EU by ~34%.** Indian
material was redirected and **Vietnam is the LARGEST destination for Indian HRC in H1/2026.** Indian and
Indonesian prices into Vietnam fell continuously; domestic producers cut to compete. **That is HPG's August
cut, from the supply side.**

- **⚠ The same EU measure hits HPG twice.** The file had HPG's own stated reasons — weak rainy-season
  demand, **a reduced EU export quota for Vietnamese steel**, slower Brazilian buying. **The second edge is
  that the same regime diverts Indian supply INTO Vietnam.** Coverage calls it a *"double storm"*: the EU
  shrinks HPG's export outlet **and** enlarges its domestic competition.
- **Price correspondence:** Indonesian HRC ~US$543/t vs ~US$576/t in early June — **−US$33/t in two
  months; HPG cut US$34/t.** HPG's US$535 volume price is **below** the Indonesian quote.
- **⚠ Measure trap flagged, question still OPEN:** "Vietnam is India's largest destination" is *Vietnam's
  share of India's exports*; the de minimis test is *India's share of Vietnam's imports*. **Different
  denominators — the 3% question is NOT answered.**
- **Two "contradictory" stories are both true:** duties displaced Chinese **volume** (imports possibly
  6m t 2025 → under 2m t 2026, consumption +25%); India and Indonesia replaced it at a lower **price**.
  Origin mix improved, price level did not.
- **Also logged: Decision 460/QĐ-BCT (21-Feb-2025)**, the provisional Chinese HRC duty 19.38–27.83%.

**⚠ This materially strengthens OPEN-DECISIONS item 6** (`spot_persists` branch for HPG). The standing
objection is that spot is a moment; **now there is a dated structural third-country cause with no expiry on
file.** Branch creation and weighting are human-only — nothing added.

**Nothing modelled, no confidence moved, no numeric driver changed.**

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
