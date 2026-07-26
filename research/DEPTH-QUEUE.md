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

**Why this order.** Weight-at-risk first, then unverified holdings, then the competitive
picture. TCB leads because it is 35% of the book, ranks 7th of 8 on expected return, and
has no dossier — the largest position is the least documented, which is exactly backwards.

---

## Queue

| # | Status | Item | Output artifact | Definition of done |
|---|---|---|---|---|
| 1 | `wip` | **TCB dossier** — S3 deep dive, from `templates/ticker-dossier.md` | `research/dossiers/TCB.md` | Business/moat, governance (Masterise related-party exposure), 5yr+8q financials, justified P/B valuation, 3 written kill criteria |
| 2 | `todo` | **TCB AR 2025** — loan book by industry, related-party note, bond holdings on own book, CASA composition, restructured loans | `research/annual-reports/notes/TCB-AR2025.md` | Every "hunt for" item in the AR program Tier 1 #2 answered or explicitly marked not-disclosed |
| 3 | `todo` | **MBB S1 screen** — held at 6.5% with **no screen at all**; the model carries confidence 0.55 on a name never underwritten | `research/dossiers/MBB.md` (S1 section) | The S1 checklist in `PROCESS.md`, plus the two-sentence variant-view gate |
| 4 | `todo` | **VCI S1 screen** — same gap; held at 3.1%, behind plan, no screen | `research/dossiers/VCI.md` (S1 section) | As above |
| 5 | `todo` | **HPG spread model deepening** — build the actual per-tonne bridge: iron ore + coking coal + energy + conversion → cost/t vs realised HRC/rebar price/t | `research/models/assumptions.json` (`hpg.spread_model`) + note | Bear/base/bull spread reconstructed from input prices rather than asserted as NPAT/tonne |
| 6 | `todo` | **HPG AR 2025** — segment note, capex commitments (DQ2 remainder, rail mill ₫14tn, Phu Yen ₫120tn), FX debt, energy self-sufficiency | `research/annual-reports/notes/HPG-AR2025.md` | Funding math for the announced capex stated explicitly |
| 7 | `todo` | **VPB segment sum-of-parts** — parent vs FE Credit vs VPBankS vs GPBank vs OPES | `research/dossiers/VPB.md` | Each segment valued separately; the double-count with VPX made explicit |
| 8 | `todo` | **TCX dossier** — margin-book concentration, bond warehouse, offshore funding lines | `research/dossiers/TCX.md` | Priciest name in the book (2.49× P/B) has its multiple defended or challenged with evidence |
| 9 | `todo` | **VPS Securities** (Tier 3, private, #1 retail share) — AR 2025 + IPO progress | `research/annual-reports/notes/VPS-private.md` | Read across to TCX/VPX/VCI market share and margin economics |
| 10 | `todo` | **Masterise** (Tier 3, private) — via HNX bond-issuer disclosures of project companies | `research/annual-reports/notes/Masterise-private.md` | The TCB related-party risk lens quantified, not asserted |
| 11 | `todo` | **KDH dossier** — consolidate the existing AR notes into a full S3 | `research/dossiers/KDH.md` | Existing §9 primary-document work folded in; RNAV built |
| 12 | `todo` | **Formosa Ha Tinh** (Tier 3, private) — via Formosa Plastics Group Taiwan filings + monthly output | `research/annual-reports/notes/Formosa-private.md` | HPG's main domestic HRC competitor sized |
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
| 2026-07-26 | hourly sweep 19:53 ICT | #1 TCB dossier | `wip` — §2/3/5/6/7/8 written. Key finding: consensus TP ₫41,828 is on a **pre-60%-bonus** share count; adjusted it is ~10.6% BELOW spot, so the street's target multiple (1.1x P/B) is *below* the traded 1.16x. Corroborates the trim-to-cap call. Open: AR loan-book note, Gia Binh sizing, insider txns, 5yr×8q table |
