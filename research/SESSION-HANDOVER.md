# Session handover — state of the book at 2026-07-31

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
| **KDH** | Filed 30-Jul | Q2 revenue ₫161bn **−85%**; H1 profit ₫321bn −6%, implying **Q2 profit ≈ zero**. Every street estimate too high; VCBS's revenue forecast was **7×** the outcome. |
| **MBB** | **DID NOT APPEAR** | Its Circular 96/2020 deadline was 30-Jul. Nothing surfaced across ~20 sweeps. **Not a verified breach** — press absence, not exchange absence; HOSE and MB IR pages both 403 from this environment. |

## 3 · Calibration: 1 hit, 2 misses

| # | Forecast | Result |
|---|---|---|
| 2 | HPG Q2 core NPAT/tonne below ₫1.60m | ❌ **MISS** — actual ₫1.835m. The forecast contradicted my own timing note written the same day. |
| 1 | KDH Q2 parent NPAT ₫170–348bn | ❌ **MISS** — by ~5× on the falsifiable part. Right in direction, badly wrong in calibration. |
| 10 | US rebar final ≈ headline risk only | ✅ **HIT** — right for the *stated* reason. The rate went the wrong way (finals ~6.6pp above preliminary) and the impact claim still carried it. |

**Forecast #4 (MBB) is open and cannot resolve until MBB files.** A pre-registered read sits
in `calibration-log.md`: *if MBB misses, expect it to miss on credit cost with net interest
income intact.* That read was **strengthened on 30-Jul and then withdrawn the same day**, before
the print, when MBB's Q1 provisioning turned out to be +15.7% against PBT +14.8% — in line with
the business, not the ACB pattern.

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
| **3 Aug** | TCX joins VN30 (ETF demand ~₫60bn = **0.073% of market cap**) **and** July CPI publishes |
| ~21 Aug | KDH insider-buy window closes (Vice Chairman's son, 0.056% → 1.838%) |
| ~mid-Sep | **ITC final injury vote on rebar** — orders issue only on an affirmative vote |
| 21 Sep | FTSE Secondary Emerging effective, **phased in tranches to Sep-2027** |
| — | MBB Q2, overdue |

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
- **"MBB" pulls at least three entities**: MB Bank (ours), MB Securities, and MBB SE (Xetra).
  Poland's mBank too. Five false hits this session.

## 9 · What is blocked, and on what

Three of the highest-value open items sit behind hosts that return **proxy 403** from this
environment: the TCB bond line (`OPEN-DECISIONS` 17b), the Federal Register rate tables, and the
HOSE / MB disclosure pages. **The FiinQuant connector is unauthorised and cannot be authorised
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
