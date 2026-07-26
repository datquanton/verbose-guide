# Depth Queue — the standing backlog

**Purpose.** Most sweeps find nothing material. This file is what the run does instead
of re-scanning. Per `AGENT-CHARTER.md` §0, a quiet run advances **exactly one** item
here and commits the artifact.

**Rules.**
- Take the **topmost `todo`** item. Do not shop the list for something easier.
- **One item per run.** A half-finished dossier committed as `wip` beats a shallow one
  marked `done` — depth is the point.
- Mark `wip` when started (with the date), `done` when the artifact meets its
  definition of done. Only status marks may be edited by an automated run.
- If an item is blocked (source unreachable, proxy 403), mark `blocked` **with the
  reason** and take the next one. Do not silently skip.
- Items are sized for a single run. If one turns out bigger, split it and say so.
- **⚠ AR-PDF items are systematically blocked.** Three separate hosts (FiinGroup mirror,
  techcombank.com, file.hoaphat.com.vn) all returned proxy 403 on 2026-07-26. This blocks
  a whole *class* of items — #2, #6, and likely #9/#10/#12. **An automated run should skip
  every annual-report item until a human downloads the PDFs into the repo or the FiinQuant
  connector is authorised.** Do not keep re-attempting them; that is the re-scanning
  failure this queue exists to prevent, wearing a different hat.

**Why this order.** Weight-at-risk first, then unverified holdings, then the competitive
picture. TCB leads because it is 35% of the book, ranks 7th of 8 on expected return, and
has no dossier — the largest position is the least documented, which is exactly backwards.

---

## Queue

| # | Status | Item | Output artifact | Definition of done |
|---|---|---|---|---|
| 1 | `wip` | **TCB dossier** — S3 deep dive, from `templates/ticker-dossier.md` | `research/dossiers/TCB.md` | Business/moat, governance (Masterise related-party exposure), 5yr+8q financials, justified P/B valuation, 3 written kill criteria |
| 2 | `blocked` | **TCB AR 2025** — loan book by industry, related-party note, bond holdings on own book, CASA composition, restructured loans | `research/annual-reports/notes/TCB-AR2025.md` | Every "hunt for" item in the AR program Tier 1 #2 answered or explicitly marked not-disclosed |
| 3 | `done` | **MBB S1 screen** — held at 6.5% with **no screen at all**; the model carries confidence 0.55 on a name never underwritten | `research/dossiers/MBB.md` (S1 section) | The S1 checklist in `PROCESS.md`, plus the two-sentence variant-view gate |
| 4 | `done` | **VCI S1 screen** — same gap; held at 3.1%, behind plan, no screen | `research/dossiers/VCI.md` (S1 section) | As above |
| 5 | `done` | **HPG spread model deepening** — build the actual per-tonne bridge: iron ore + coking coal + energy + conversion → cost/t vs realised HRC/rebar price/t | `research/models/assumptions.json` (`hpg.spread_model`) + note | Bear/base/bull spread reconstructed from input prices rather than asserted as NPAT/tonne |
| 6 | `blocked` | **HPG AR 2025** — segment note, capex commitments (DQ2 remainder, rail mill ₫14tn, Phu Yen ₫120tn), FX debt, energy self-sufficiency | `research/annual-reports/notes/HPG-AR2025.md` | Funding math for the announced capex stated explicitly |
| 7 | `done` | **VPB segment sum-of-parts** — parent vs FE Credit vs VPBankS vs GPBank vs OPES | `research/dossiers/VPB.md` | Each segment valued separately; the double-count with VPX made explicit |
| 8 | `done` | **TCX dossier** — margin-book concentration, bond warehouse, offshore funding lines | `research/dossiers/TCX.md` | Priciest name in the book (2.49× P/B) has its multiple defended or challenged with evidence |
| 9 | `blocked` | **VPS Securities** (Tier 3, private, #1 retail share) — AR 2025 + IPO progress | `research/annual-reports/notes/VPS-private.md` | Read across to TCX/VPX/VCI market share and margin economics |
| 10 | `blocked` | **Masterise** (Tier 3, private) — via HNX bond-issuer disclosures of project companies | `research/annual-reports/notes/Masterise-private.md` | The TCB related-party risk lens quantified, not asserted |
| 11 | `done` | **KDH dossier** — consolidate the existing AR notes into a full S3 | `research/dossiers/KDH.md` | Existing §9 primary-document work folded in; RNAV built |
| 12 | `blocked` | **Formosa Ha Tinh** (Tier 3, private) — via Formosa Plastics Group Taiwan filings + monthly output | `research/annual-reports/notes/Formosa-private.md` | HPG's main domestic HRC competitor sized |
| 13 | `todo` | **VPX dossier** — FVTPL book composition, CAEX stake carrying value | `research/dossiers/VPX.md` | The earnings-quality discount in `exit_pe` justified from the book's actual composition |
| 14 | `todo` | **Peer comparison table** — VCB/ACB/CTG vs TCB/VPB/MBB on the 5 bank KPIs | `research/dossiers/_banks-peer-table.md` | Our three banks ranked against the three we don't own |
| 15 | `todo` | **Calibration scoring pass** — once ≥10 forecasts resolve, compute hit rate by confidence bucket, bias, dispersion | `calibration-log.md` aggregate section | The `confidence` column stops being asserted and starts being measured |

## Recurring — not queue items, but standing obligations

These fire on their own triggers and take precedence over the queue when due:

- **Score a forecast the day it resolves.** Never let a resolved forecast sit unscored;
  the calibration record is the only measure of edge and it decays if backfilled from memory.
- **Q2 statements (HPG, KDH, MBB), expected Jul 28–30** — when filed, re-base models,
  raise evidence tier, score open forecasts 1–4.
- **US rebar AD/CVD final, ~Jul 28** — resolves open forecast 10.

## Log

| Date | Run | Item | Result |
|---|---|---|---|
| 2026-07-26 | — | queue created | 15 items; `research/dossiers/` empty at creation, 1 of ~15 AR notes written |
| 2026-07-27 | hourly sweep 01:53 ICT | #9/#10/#12 | `blocked` — skipped per the class-level AR-PDF rule rather than re-attempted |
| 2026-07-27 | hourly sweep 01:53 ICT | #11 KDH dossier | `done` — independent derivation from Q1 unit economics reproduces the model's 80/130/185 handover counts as 81/131/186 (internally consistent). **Bull branch is arithmetically INFEASIBLE**: 186 units needed against a 135-unit sold book. Q1 delivered 6, so even bear needs 25/qtr — a 4.2× step-up. **Pre-registered Q2 read** written before the print: 170bn ⇒ ~19 units, 259 ⇒ ~27, 348 ⇒ ~35. Also: ₫3.45tn of a ₫29.13tn land bank (12%) produces essentially all of 2026's profit. Bull re-weighting recommended, NOT applied |
| 2026-07-27 | hourly sweep 00:53 ICT | #8 TCX dossier | `done` — **ESCALATION: the book is 19.5% Vietnamese brokerage, not 11.4% (+71%).** TCBS is 19.2% of TCB's consolidated PBT, so 6.73pp of the book is TCX *via* TCB; with VPX's 1.42pp look-through, effective brokers = TCX 12.23 + VPX 4.22 + VCI 3.10. The optimizer sees a 3.1% 'Brokers-other' cluster. Banks ex-broker are 43.4%, not 51.5%. Also: margin lending is 52% of TCX net revenue; justified P/B 0.6–1.2× vs 2.49× traded — the most stretched in the book. **Do not add on the current output** — the +5.1pp starts from an effective 12.2% and would take brokers to ~25% |
| 2026-07-26 | hourly sweep 23:53 ICT | #6 HPG AR 2025 | `blocked` — third consecutive proxy 403 on a Vietnamese corporate PDF host. Recorded as a CLASS-level block in the rules above rather than a one-off |
| 2026-07-26 | hourly sweep 23:53 ICT | #7 VPB sum-of-parts | `done` — three findings: (a) the model's "FE Credit is the swing factor" note is MIS-ATTRIBUTED — FE Credit is 0.8% of PBT; the credit risk sits in the parent book (+24.6% YTD, past ₫1 quadrillion) — corrected in run.py; (b) VPX is 14.2% of VPB's PBT, so effective VPX exposure is 4.22% not 2.8% (+51%) — the VPB/VPX overlap is OWNERSHIP, not correlation, and TCB/TCX is the same structure; (c) GPBank earned ₫730bn in 1H, ~1.5× its full-year 2025 — a weak-bank transfer turning positive fast, which strengthens the MBB variant view from a different company |
| 2026-07-26 | hourly sweep 22:53 ICT | #5 HPG spread bridge | `done` — NPAT/t rebuilt from input prices, conversion cost CALIBRATED to the Q1 actual rather than assumed. Two findings: (a) at spot the all-in pre-tax cost is US$522/t vs US$539 HRC — a ~3% margin implying ₫0.36m/t, and **every branch including bear assumes HRC recovers** (bear needs +7.9%); (b) ore/coal are bought 1–2 quarters forward, so **a strong Q2 print on ~Jul 28 does NOT refute the bear thesis** — the squeeze lands in Q3. A 4th `spot_persists` branch is recommended but NOT applied (judgment change, charter §2) |
| 2026-07-26 | hourly sweep 21:53 ICT | #4 VCI S1 screen | `done` — **ESCALATION raised.** Q2 fell 26% QoQ (251 vs 341) behind a +36% YoY headline; revenue flat, OCF negative funded by borrowings, prop book −430bn on FPT/MWG/KDH. ROE 8.9% vs ~15% COE ⇒ justified P/B ~0.39× against 1.38× traded. Found `npat_ttm` fails its own cross-check by 25.2%; correcting flips E[r] +7.0% → −7.5%. Confidence cut 0.65→0.45; number left for a filing. The add fell to +0.8pp (hold) on the confidence cut alone |
| 2026-07-26 | hourly sweep 20:53 ICT | #2 TCB AR 2025 | `blocked` — proxy 403 on both the FiinGroup PDF mirror and techcombank.com IR. The documented Vietnamese-PDF trap. Needs a human to download, or the FiinQuant connector once authorised |
| 2026-07-26 | hourly sweep 20:53 ICT | #3 MBB S1 screen | `done` — passes S1 with a falsifiable variant view: ROE erosion (25.0→20.9%) may be the PRICE of the MBV transfer, which bought a 30–35% credit allowance in a system rationed to 11–13%. Justified P/B 1.56–2.18× vs 1.24× traded. Independently corroborates the optimizer's add. Found an actionable item: the 10:1 rights at ₫10,000 costs a non-subscriber ~5.0%. Confidence held at 0.55 — an S1 earns no tier upgrade |
| 2026-07-26 | hourly sweep 19:53 ICT | #1 TCB dossier | `wip` — §2/3/5/6/7/8 written. Key finding: consensus TP ₫41,828 is on a **pre-60%-bonus** share count; adjusted it is ~10.6% BELOW spot, so the street's target multiple (1.1x P/B) is *below* the traded 1.16x. Corroborates the trim-to-cap call. Open: AR loan-book note, Gia Binh sizing, insider txns, 5yr×8q table |
