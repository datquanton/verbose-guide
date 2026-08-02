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
| 1 | ~~**Read VPB's consolidated Q2 credit balance off the statement.**~~ **RESOLVED 2026-08-01 02:53 — and it resolves in VPB's favour.** **The missing figure: consolidated customer loans ₫1,160,000bn at end-Q2, +23% on end-2025.** The 28-Jul logical cross-check is confirmed — consolidated exceeds parent by ~₫100,000bn (FE Credit, VPBankS, the rest of the ring). **There are three series, not two:** parent credit ₫1,060,000bn +24.6% (which is what `credit_q2` **and** `credit_growth_ytd` *both* describe — those two fields are consistent after all); consolidated loans ₫1,160,000bn +23%; and consolidated **credit** incl. bonds, whose end-2025 value is the ₫962,000bn in `credit_start_fy`, 2.0% above the consolidated-loans base — the same credit-vs-loans gap already found at TCB. **The fake +10.19% came from dividing a PARENT stock by a CONSOLIDATED base.** The 28-Jul note was right that an entity error was present and right about which figures existed; it attributed the error to the wrong field. **Stakes as the note framed them:** +24.6% ⇒ base branch comfortable at +8.3% more; +10.2% ⇒ +22.5% and a KDH-style step-change. **Actual consolidated H1 growth ≥ +20.6%**, so against `credit_growth_fy` 30/35/40% H2 needs **at most +7.8% / +12.0% / +16.1%** — upper bounds, since credit ≥ loans. **The feared step-change is not there.** `credit_start_fy` is correct and untouched (962,000 × 1.34 = 1,289,080 = the company's ₫1.29 quadrillion plan). **No engine output changes** — `run.py` reads neither `credit_q2` nor `credit_growth_ytd`. **One thing left for a human:** confidence was cut **0.85 → 0.70** on 28-Jul *because* this driver was unevidenced. It now is — but this is **T5 press**, and charter §2 permits a rise only on T1–T2, the same rule that held MBB at 0.55 yesterday. **Restoring it is a human's call on a name the engine wants to ADD +5.3pp.** | `assumptions.json` → `vpb.actuals._CREDIT_INPUTS_RESOLVED_2026_08_01`; log 01-Aug 02:53 |
| 2 | **Refresh all eight prices and add a `_price_date` per ticker.** **← now the highest-value item on this page, escalated 29-Jul 16:53. SHARPENED 02-Aug 10:53: TCX's verified 24-Jul price is ₫39,200 against ₫41,100 on file — 4.85% too high for the date the whole set is presumed to hold, and a dated 15-Jul price of ₫41,800 sits just above it, so ₫41,100 looks like a mid-July price carried as a late-July one. Not overwritten here: fixing one of eight would make the set MORE inconsistent, and the date convention is the human-owned half of this item. Note the ADJUSTMENT TRAP too — TCX's 20% stock dividend cuts the quoted price ~16.7% on its ex-date, so any series straddling Q2/2026 needs checking for adjustment before a move is read off it.** | Prices are undated and presumed 24 July. A 1% move is **73% of VPB's entire expected-return signal** and 25% of TCB's. **TCB now has a dated observation ₫3.42% below the file's figure** (₫28,250 on 27-Jul vs ₫29,250 here) — three times the drift previously recorded. On the file's own sensitivity that lifts TCB's E[r] by ~3.1pp and **moves it from 7th of eight to 6th**, weakening a stated support for the headline 15pp trim. The trim survives on the 20% cap, which is constitutional rather than a ranking. **And the market fell 6.55% in the week to 24-Jul** with forced liquidation — an undated price field is a different order of problem in that market than in a quiet one. | `assumptions.json` → `valuation._PRICES_ARE_UNDATED_2026_07_28`, `_MARKET_CONTEXT_2026_07_29`; log 09:53 and 16:53 |
| 3 | **Set the `cash_yield` convention and populate all eight.** **← the convention is not merely missing, it is being applied inconsistently; found 29-Jul 21:53. THE SAME-DAY ARGUMENT THIS ENTRY USED TO MAKE IS WITHDRAWN — see below, corrected 31-Jul 19:53.** | Filled in for TCB only — and **TCB's inclusion rests on a premise that is false.** The note justifies including TCB's 7% cash because it is "pending"; it was **paid 10-Jun-2026** (record 20-May, ex 19-May) and has been past for seven weeks. ~~*the same day MBB's 10% cash was paid — two dividends, one payment date, opposite treatments*~~ — **that claim is WITHDRAWN and was never true. MBB's record date was 10-JUL and payment ran from 17-JUL**, five weeks after TCB's, and the correction has been in `assumptions.json` since 29-Jul 23:53. **The inconsistency survives without it and is in fact broader:** three of the eight are known H1-2026 cash payers — **TCB ₫700 paid 10-Jun (2.39%), MBB ₫1,000 paid 17-Jul (4.54%), VPB ₫500 paid 25-May (2.00%)** — and the field records **exactly one**, on a "pending" premise that was false for that one. It is not a coverage gap with a neutral direction: one name credited, two identically-situated names not, **all three banks**, the cluster the engine proposes to trade most. Removing TCB's 0.024 cuts its shrunk expected return 1.92pp to ~+1.50%, against VPB's +0.99%; adding MBB's 4.54% moves MBB from 4th to 3rd, above HPG. **Seven blanks are not seven zeros.** **AND THE CONVENTION NEEDS THREE CELLS, NOT ONE — established 01-Aug 11:53.** The three bank stock issues are **three different instruments**: **TCB 60% is BONUS SHARES from owner's equity (not a dividend, not taxed at issuance)**, while **VPB 26.04% and MBB 15% are STOCK DIVIDENDS from retained earnings (taxed)**. **The largest issue is the untaxed one** — the opposite of what "TCB is paying 67%" implies. On the file's own 5% rate and par basis: TCB 0.12% of price, VPB 0.62%, MBB 0.57%, **totalling 0.141pp of the whole book**. Caveats: the tax is generally **collected on disposal**, so it is deferred not current; the 5% is the file's own assumption, unverified; prices are the undated ones in item 2. | `assumptions.json` → `valuation._CASH_YIELD_POPULATED_FOR_ONE_OF_EIGHT_2026_07_28`, `_regulatory._THE_THREE_BANK_STOCK_ISSUES_ARE_NOT_THE_SAME_INSTRUMENT_2026_08_01`; log 10:53, 21:53, 31-Jul 19:53, 01-Aug 11:53 |

| 19 | **Re-derive MBB's `fy26e_npat` branches. ← NEW, escalated 31-Jul 14:53. Escalation trigger #4 fired: an estimate became a filed actual.** | **The branches are contradicted from BELOW, and the engine cannot see it.** Filed H1 PBT is **₫20,188bn** (Q1 9,628 + Q2 10,560). Against branch-implied FY PBT of 35,000 / 38,125 / 41,250, that leaves **bear needing H2 −26.6%, base −11.2%, bull +4.3%** — and Vietnamese bank profit is *second-half weighted*, so a flat H2 is the conservative case. **A flat H2 gives FY26 PBT ₫40,376bn: above base, just below bull, inside company guidance and near MAS's 40,726.** Two of three branches now require profit to fall outright. **The 28-Jul pre-registered H2 table called this exact row in advance** and its instruction is to rebuild, not to celebrate. **What makes this urgent rather than tidy: MBB's shrunk E[r] did not move at all on a +40% quarter** — it is still +8.8%, because the branches are typed in (item 9) and confidence is correctly held at 0.55 on T5 evidence. **The engine is blind to the best print in the book, while proposing MBB as its joint-largest add (+5.5pp).** Branch re-derivation is human-only under charter §4. | `assumptions.json` → `mbb.actuals._PRE_REGISTERED_H2_TABLE_FIRES_AND_SAYS_REBUILD_2026_07_31`; log 31-Jul 14:53 |
| 24 | ~~**Locate the price and book date behind TCX's `2.49x P/B`.**~~ **WITHDRAWN AND REPLACED 02-Aug 10:53 — the 09:53 finding was wrong.** | **`2.49x` is exactly right and always was.** The 09:53 entry used TCX's **listing-date** share count (2,311,308,021); **TCX paid a 20% stock dividend (5:1) in Q2/2026** — 462.3m shares, charter capital ₫23,115.8bn → ₫27,739bn — so the count is **2,773,896,000**, confirmed three ways to 0.02%. **41,100 × 2,773,896,000 / ₫45,782bn = 2.4902×.** The kill trigger price is **₫33,010, not ₫39,616**; the criterion is **24.5% away** at the file price and **18.8%** at the verified 24-Jul price of ₫39,200. **Nothing was ever 3.8% away.** The 09:53 restatement of `valuation.TCX.evidence` was the error and the original string is restored. **What survives from 09:53 unaffected** (it rests on filed equity, not the share count): filed equity ₫45,782bn, ratio 1.13×, withdrawal of the 31-Jul 1.56×, headroom ₫40,064bn, HSC/KBSV/Phú Hưng past 190%. | `assumptions.json` → `tcx.actuals._WITHDRAWN_THE_09_53_SHARE_COUNT_WAS_PRE_DIVIDEND_AND_EVERY_CONCLUSION_ON_IT_IS_WRONG_2026_08_02`; log 02-Aug 10:53 |
| 25 | ~~**Settle `pe_ttm` / `npat_ttm` — `cap_now` wrong on seven of eight.**~~ **CLOSED 02-Aug 20:53 by the user-directed data refresh.** | **`cap_now` is now exactly right on all eight.** `shares_outstanding` and `market_cap_bn` are explicit fields; `npat_ttm` is set from filed statements with the basis recorded per name in `_npat_ttm_basis_2026_08_02`; `pe_ttm` = market cap ÷ `npat_ttm`. TTM (Jul-25→Jun-26) computable for **HPG, TCB, VPB, MBB (68.3% of the book)**; **FY2025 filed** used for KDH/TCX/VCI; **VPX `npat_ttm` unchanged**, `pe_ttm` corrected. **`pe_ttm` is NO LONGER comparable across names.** **The ranking reordered:** MBB +36.6 / HPG +6.3 / TCB +4.0 / KDH +3.5 / VPX −0.0 / VCI −11.3 / TCX −11.2 / VPB −13.9. **Residual: prices are still undated (item 2) — every market cap here rests on them.** | log 02-Aug 20:53 |
| 26 | **⚠ Re-derive the bank `fy26e_npat` branches onto a PPOP basis, and establish VPB's provisioning line. ← NEW, 02-Aug 20:53, user-directed. Now the most valuable human task in the repo.** | **Reported bank PBT is materially provisioning-driven and the branches are anchored to it.** TCB: PBT +22.5% on PPOP +16.7%, provisions **−24.6%** while **Group 2 loans +46%** and corporate bonds +80% — **5.8pp of the growth is provisioning**. MBB: PBT +27.1% on PPOP +17.9%, provisions **flat** while the **NPL balance rose 27% against loans +13.2%** — **9.2pp is provisioning**. **The headline ratios conceal it**: MBB's NPL ratio moved 3bp because loans are its denominator, and coverage rose because the reserve was topped up without a matching P&L charge. **VPB RESOLVED 02-Aug 21:53:** provisions **ROSE 23.7%** to ₫15,579bn (opposite of both peers) yet **intensity fell 7.6pp — the most of the three — so 23.4pp of its 68% growth is provisioning**; but **PPOP grew 44.6%** against peers' ~17%, so its business is genuinely the strongest. **Group 4 doubtful debt +44.5% while the NPL ratio FELL 3.33%→3.28%.** All three banks now measured; **51.5% of the book has PBT growth that is 5.8 / 9.2 / 23.4pp provisioning-driven with every credit pipeline deteriorating.** **Method is cheap and validated**: PPOP = PBT + provisions, and provisions derive as TOI − opex − PBT (MBB: derived 7,703 vs reported 7,701.9). **Confidence was cut (TCB 0.70, MBB 0.50) but that is a scalar on branches anchored to a flattered base — the branches themselves need rebuilding, which is human-only under §4.** | `assumptions.json` → `tcb.model._PROVISIONING_IS_FLATTERING_REPORTED_PBT_AND_THE_PIPELINE_IS_GROWING_2026_08_02_2053`; log 02-Aug 20:53 |

## 2 · Judgment calls the charter reserves for a person

| # | Decision | The finding behind it | Where |
|---|---|---|---|
| 4 | **Re-weight KDH's scenario probabilities.** | The bull branch needs ~178–186 units handed against a **135-unit sold book** — arithmetically out of reach — yet carries p=0.20. | `dossiers/KDH.md` §2 |
| 5 | **Re-weight the TCX FTSE event tree, or retire it.** **← a third independent ground added 31-Jul 21:53** | It prices 21 September as one discrete day (+20%/+5%/−15%, EV +6.25%). Inclusion is actually **phased in tranches to September 2027**, and the announcement effect was largely banked in April. **Third ground: foreigners have net sold ₫92,000bn YTD** (>₫62,000bn to end-May, ~₫80,000bn to end-June, ₫92,000bn to end-July — **July alone ~₫12,000bn**), and **2026 is on track to be the fourth consecutive year of foreign net selling.** One headline puts it directly: *ahead of the upgrade, foreigners have net sold >₫72,000bn in three stocks.* **Stated proportionately:** aggregate outflow is **active** money and inclusion brings **passive** money — different pools, and they must not be netted. What it does say is that **the marginal foreign dollar has been negative for four years**, which is the assumption the tree's +20% bull branch quietly reverses. **Fourth ground, and the most concrete — 01-Aug 13:53: the exact tranche weights.** Inclusion runs **10% on 21-Sep-2026**, then 20% (Mar-27), 35% (Jun-27), 35% (Sep-27). **The day the tree prices delivers one tenth of the inclusion**, and 90% arrives after forecast #7 resolves. At full weight Vietnam is **0.22% of the FTSE Emerging Index**; **at tranche one that is 0.022%, across 28 stocks.** **And the two sides are asymmetric:** deletion from FTSE Frontier is a **single tranche** in Sep-2026 — **100% of the exit against 10% of the entry, on one date.** Not netted here: that needs Frontier vs Emerging tracking AUM, which the file does not have, and stating a direction without it would be inventing one. | `assumptions.json` → `tcx._FTSE_IS_PHASED_2026_07_28`; log 04:53 |
| 6 | **Decide whether to add a `spot_persists` branch to HPG. ← MATERIALLY STRENGTHENED 02-Aug 16:53: there is now a DATED STRUCTURAL CAUSE for spot to persist.** The standing objection to this branch is that spot is a moment. **The EU's new steel mechanism, effective 01-Jul-2026, cut India's HRC quota to the EU by ~34%, and Vietnam is now the LARGEST destination for Indian HRC.** Indian HRC carries **no Vietnamese anti-dumping duty** (terminated on a <3% negligibility test), Indonesian HRC is quoted ~US$543/t against ~US$576/t in early June, and **HPG's US$535 volume price sits BELOW the Indonesian quote.** **The same EU regime shrinks HPG's export outlet AND enlarges its domestic competition — a double hit, and the file previously had only the export side.** This is a reason for spot to persist rather than mean-revert, and it has **no expiry on file**. | No existing branch describes current input prices. At spot the case is **₫0.60–0.68m/t** against a bear branch of ₫1.25m. **Better evidenced 31-Jul, and correctly dated:** HPG's own August HRC offer is US$546–547/t list and **US$535/t volume**, bracketing the model's US$539 spot almost exactly — so the spot input is sound and the August cut is already inside it. **But Q3 straddles the step** (July ≈580 → August ≈546), so a Q3 average sits *above* spot. **This branch describes Q4, not Q3** — a soft Q3 print is not its vindication. **Repriced 31-Jul 20:53 with all three inputs pinned** (ore US$98.25, coal US$218.50, HRC US$546.5 list / US$535 volume): the branch is now **₫0.86–1.10m/t**, not the ₫0.36m/t the mis-logged ore implied nor the ₫0.83m/t of 27-Jul. **Still below the ₫1.25m bear branch on both readings**, so the finding stands — but the gap is ₫0.15–0.39m/t, and closing. | `hpg-spread-bridge.md` §6–7 |
| 7 | **Raise `corr_same_cluster` toward ~0.95 for parent/subsidiary pairs. ← SECOND INDEPENDENT GROUND ADDED 02-Aug 17:53.** | TCB contains TCBS; VPB contains VPBankS. The optimizer models these as 0.80-correlated when one *contains* the other. **New ground: the link is not only ownership.** Seven issuers on the Sài Gòn Bình An project raised **₫32,905bn** of bonds with **TCBS as depositary** — so **TCB's "Masterise bond event" kill criterion plausibly reaches TCX as well**, through fee income, reputation and distribution liability. **40.5% of the book sits in that cluster.** *(Period-flagged: the ₫32,905bn evidence is a 2022–23 era story, logged as structure not news; and whether TCBS is also the unnamed registrar on the H1/2026 ₫44,500bn is an INFERENCE, not established.)* | `assumptions.json` → `vpb.model._VPX_LOOKTHROUGH_2026_07_26` |
| 8 | **Decide what to do about 19.5% effective brokerage exposure.** | Look-through, not the 11.4% stated. The proposed TCX add starts from an effective 12.2%. | `dossiers/TCX.md`; `_LOOKTHROUGH_EXPOSURE_2026_07_27` |

## 3 · Machinery — an automated run may not touch these (charter §4)

| # | Decision | Why it matters |
|---|---|---|
| 9 | **Build driver models for MBB and VCI in `run.py`. ← the case strengthened 31-Jul.** | 9.6% of the book has `fy26e_npat` typed in with nothing deriving it. MBB is the joint-largest proposed add. Inverting the branches showed they are *coherent* — the problem is they cannot be stress-tested. **Two things changed with MBB's Q2 filing.** (a) The blocker is gone: there is now a filed half-year supplying loans (+13.2% YTD), NIM (4.03% 12m rolling), NPL (1.45%) and coverage (93.63%) as actuals — the reason 28-Jul gave for *deliberately not building it yet* has expired. (b) The cost is now visible rather than theoretical: **a +40% quarter moved MBB's expected return by zero**, because no driver connects the print to the branches. See item 19. |
| 10 | **Wire `ftse_event_tree` into `decide.py`, or label it narrative.** | It is read only by `run.py` and printed into the snapshot. Its +6.25% never reaches expected returns or weights. VCI's stated bull case is "an EVENT bet" and the event is absent from VCI's numbers. |
| 11 | **Correct the FE Credit attribution printed by `run.py`.** | The line says FE Credit NPL formation is the swing factor. FE Credit is 0.8% of consolidated profit; the risk sits in the parent book. |
| 12 | **Replace the two scheduled-routine prompts.** | The live hourly prompt keeps its own copy of the lanes, the broker estimates and the run rules, and those copies have drifted from the repo. Drafts are written and ready to paste. |

## 4 · Reads that take one line off a filed statement

| # | Question | Consequence if left |
|---|---|---|
| 13 | Is HPG's ₫4,123bn divestment gain pre- or post-tax? **← WORSE, not better, 01-Aug 04:53: there is now a THIRD candidate figure.** | Core + one-off = ₫9,169bn against a ₫9,056bn headline. The ₫1.68m/t figure it implies is the **calibration anchor of the whole spread bridge**. **Three numbers now describe one line:** ₫4,123bn (on file), ₫4,010bn (implied by 9,056 − 5,046), and **~₫3,800bn** (press, 01-Aug, *Phố Nối specifically*, explicitly approximate). ₫3,800bn is 7.8% below the file's figure — too far to be a rounding. **It weakens the preferred explanation.** The pre/post-tax story required a 2.7% effective rate. A competing reading now has support: **~₫3,800bn is Phố Nối alone and ₫4,123bn is total other income**, making the ₫113bn gap *composition, not tax*. Neither is established; neither adopted. **Quantified cost: the anchor ranges 1.644 → 1.752m/t across the three, a 6.5% spread** — and the new figure pushes it **higher**, the opposite direction from the only alternative previously considered. **Check that does pass:** ₫4,123bn is Q1, not H1 (9,056 + 6,424 = 15,480 exactly). |
| 14 | ~~Is KDH's `q1_revenue` ₫281.4bn actually revenue, or net profit?~~ **ANSWERED 30-Jul 10:53 — it is REVENUE. The field was right; my three-sweep case against it was wrong.** | A source gives net revenue (*doanh thu thuần*) of ₫281.4bn, **−60.4% YoY**, with after-tax profit separately at **₫327bn, +175.5%**. Two different numbers. The arithmetic route gave ₫281.0bn, not ₫281.4bn — a near-match I treated as a match. **The dossier's second verification route for the units count exists and is live for today's print.** |
| 15 | Is KDH's ASP ₫42bn or ₫44bn? **← one route tried and DISARMED, 01-Aug 05:53** | The model and its own dossier disagree. Changes gross profit per unit by 4.8% and solved fixed opex by 8.3%. The bull-infeasibility conclusion survives either way. **Do not use project price pages.** They return "₫15bn/căn" for Gladia and "from ₫230m/m²" — agency marketing material (below T6), a *starting* price rather than a realised ASP, and **self-contradictory by 4×** (230m/m² on a 250–300m² villa is ₫57–69bn). **The file's own arithmetic already refutes ₫15bn:** Q1 revenue ~₫252–264bn on **6 units** gives ₫42–44bn directly; at ₫15bn six handovers would have produced ~₫90bn. **Settled only by the segment note in the financial statements** — revenue by project ÷ units delivered. |
| 16 | **What is MBB's 2026 credit-growth target? REOPENED 29-Jul 14:53** — the "mostly resolved at 30–35%" status is withdrawn. **Chairman Lưu Trung Thái is on the record at 25%** (Jan-2026), against the unattributed 30–35% this file prefers. A named source is stronger evidence, but it may predate an AGM-approved figure. Both survive: 25% as internal plan, 30–35% as SBV quota allowance. **AGM minutes settle it; the H1 statement will not.** **Narrowed 30-Jul 21:53:** the AGM-referenced set is corroborated again and in fuller form — total assets +28%, credit +30–35%, PBT +15–20%, ROE ~20–21% — and the Chairman's 25% is dated **January, before the April AGM**. That *supports* the sequencing reading (early figure later superseded) over the quota-allowance reading, without proving it. Still open. | **The period half IS now resolved, by arithmetic.** Q1 credit is pinned at **₫1,140,000bn, +3.3% YTD** (two sources, T5). So the "10%" cannot be a Q2 increment — that would give ~13.3% YTD, contradicting the same source's "10% as of May". **It is cumulative YTD at end-May**, meaning +6.7pp in April–May alone. Credit is accelerating, H1 is likely above 10%, and the recorded "H2 must add +18.2% to +22.7%" **overstates the requirement**. MBB's version of VPB's problem is milder, not identical — and MBB is the joint-largest proposed add.  **CONFIRMED BY THE FILING, 31-Jul: actual H1 customer-loan growth is +13.2% YTD**, so the profile is +3.3% (Mar) → ~10% (May) → +13.2% (Jun). The end-May reading was right and the Q2-increment reading is dead. H2 growth needed for 30–35% is **+14.8% to +19.3%**, confirming the requirement was overstated. **The target question itself is still open** — a half-year outturn does not say which target was approved, and +13.2% is consistent with both. |

| 20 | **Establish KDH's land-use fee exposure under HCMC Decision 45/2026/QĐ-UBND. ← NEW, 31-Jul 23:53.** | **A dated, gazetted regulation has been in force since 01-Jul-2026 and this repo had zero record of it** — no hit for "land-use fee", "bảng giá đất", "hệ số K", "Land Law" or "254/2025" in either `assumptions.json` or `monitoring-log.md`. Land-use fee is the largest cost input for a residential developer and equals **land price table × K**. HCMC's new table took effect **01-Jan-2026** on "market principles" (largest increases reported at **8×**); Decision 45 sets **K = K1×K2×K3, with K1=K3=1 for 2026**, so K reduces to a **project-type K2**. **KDH is 20.3% of the book with >₫23,000bn of inventory**, and Gladia/Clarita are exactly the unlaunched projects on which the obligation crystallises. **Two things must be established before any number enters the model: KDH's project-specific K2, and which projects have already settled their fee** (assessed at assignment/conversion — projects already paid are unaffected). **The direction is not established and the obvious reading is not taken:** a higher table raises fees, but a published K removes a procedural blockage that was itself stalling approvals, and the two cannot be netted from here. | `assumptions.json` → `_regulatory.decision_45_2026_qd_ubnd`; log 31-Jul 23:53 |

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
