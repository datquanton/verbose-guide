# Quantitative Models — Roadmap & Usage

Turns the research process into runnable arithmetic. Philosophy (from the four-layer
framework): **models beat your inconsistency, not the market.** Layer 1 (arithmetic)
and Layer 2 (scenarios) live here; Layer 3 (updating/kill criteria) lives in the
monitoring log; Layer 4 (judgment: governance, politics) lives in the dossiers and
is deliberately NOT in these numbers.

## Usage

```bash
python3 research/models/run.py     # regenerates SNAPSHOT.md
```

- **`assumptions.json` is the belief file.** Every number is either a sourced actual
  or a named assumption. To change a view, edit it and rerun — the git history of
  that file becomes your calibration record (what you believed, when, and why).
- `SNAPSHOT.md` is generated output — never edit by hand.
- Rule: after every earnings release or thesis event, update actuals within 48h,
  rerun, and note in the commit message which assumption moved and which direction.

## Current models (v0)

| Module | What it computes | The one variable it exposes |
|---|---|---|
| Portfolio | weights, P&L, cluster caps, HHI/effective bets | KDH breach; ~3.5 effective bets |
| KDH | Gladia handover model → NPAT vs plan/stretch | units handed (advances = the tell) |
| TCB / VPB | H2 grid: quota × NIM × credit cost, anchored on H1 | TCB: NIM; VPB: credit cost (FE) |
| TCX | margin-book engine + FTSE event tree (EV) | book growth vs multiple paid |
| VPX | core vs FVTPL earnings split + CAEX option EV | mark-to-market dependence |
| HPG | Q1 actual + volume × core NPAT/tonne | the spread (not volume) |

## Roadmap

**Phase 1 — v0 scenario models (DONE, this commit).**
Structure over precision: every position has named assumptions, three scenarios, and
a "% of company target" reality check.

**Phase 2 — Q2 re-base + data feed (next ~2 weeks).**
- Re-base all actuals on Q2/26 statements the week they drop (HPG/KDH imminent;
  banks/brokers already partially in).
- Authorize the FiinQuant connector → replace hand-keyed actuals with pulled data;
  add a `sources` field per actual so every number is traceable.
- Add per-model **calibration log**: assumption vs printed actual each quarter,
  error recorded. (This is how your estimates get better — scored, not vibes.)

**Phase 3 — event discipline (by end-Aug).**
- Encode kill criteria as executable checks in run.py (e.g. `KDH: advances < 1,000
  by 3Q26 → print BEAR CONFIRMED`), so the snapshot itself shouts when a threshold
  trips.
- Pre-write the Sep-21 FTSE playbook: for each event-tree branch, the pre-committed
  action (trim/hold/add) — decided while calm, executed mechanically.
- VN30 (Aug 3) and rebar-final (Jul 28) outcomes folded into assumptions.

**Phase 4 — valuation layer (Sep–Oct).**
- KDH RNAV module (per-project: ha × price/ha − costs − debt, with the 520.4ha
  table from SSI as the scaffold).
- Banks: justified-P/B fair-value bands (ROE paths → multiple) replacing reliance
  on street TPs.
- Output a "price vs model band" line per ticker in the snapshot.

**Phase 5 — portfolio engineering (Q4).**
- Sizing from EV and correlation instead of history: target weights from
  scenario-weighted returns, cluster correlation matrix, fractional-Kelly cap.
- Decision journal metrics: hit rate, slugging, average error by assumption type —
  the quarterly self-review the process doc (S8) promises.

## Standing cautions

1. A model with a wrong ASP is precisely wrong; the SNAPSHOT prints assumptions
   beside outputs so they get challenged together.
2. Never add a Layer-4 item (governance, regulatory intent) as a number — keep it
   a flag. The An Lap seller question has no spreadsheet cell.
3. Quarterly statements are unaudited; semi-annual reviewed; annual audited —
   weight the actuals accordingly.
