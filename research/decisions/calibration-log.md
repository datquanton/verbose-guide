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
| 1 | 2026-07-24 | KDH | Q2/26 parent NPAT between MBS ₫170bn and SSI ₫348bn; base case FY26 NPAT ₫1,590bn | conf 0.50 | Q2 FS (~Jul 28–30) | ⏳ open |
| 2 | 2026-07-26 | HPG | Q2 core NPAT/tonne **below** ₫1.60m as the Formosa/iron-ore spread squeeze bites | bear p=0.45 | Q2 FS (~Jul 28–30) | ⏳ open |
| 3 | 2026-07-24 | HPG | FY26 core NPAT (ex Pho Noi gain) ₫23.3tn base case | conf 0.60 | FY26 audited | ⏳ open |
| 4 | 2026-07-24 | MBB | Q2/26 NPAT ≈ ₫7,052bn (VCBS est.); FY26 base ₫30.5tn | conf 0.55 | Q2 FS (~Jul 28–30) | ⏳ open |
| 5 | 2026-07-24 | TCB | FY26 PBT ₫33.2tn base — **below** company guidance ₫35–37.5tn | conf 0.85 | FY26 audited | ⏳ open |
| 6 | 2026-07-24 | VPB | FY26 PBT ₫30.7tn base vs ₫41.6tn target — plan leans on VPBankS | conf 0.85 | FY26 audited | ⏳ open |
| 7 | 2026-07-24 | TCX | FTSE Sep-21 event EV ≈ +6.2%; base case "in-line, quiet digestion" p=0.45 | conf 0.80 | ~Oct 21 (1m after) | ⏳ open |
| 8 | 2026-07-24 | VPX | CAEX licence granted ~Q3 at p=0.40 | conf 0.70 | Q3/26 end | ⏳ open |
| 9 | 2026-07-24 | VCI | 9M PBT reaches ≥55% of FY target (the kill-criterion threshold) | conf 0.65 | Q3 FS (~Oct) | ⏳ open |
| 10 | 2026-07-23 | HPG | US rebar AD/CVD final ≈ headline risk only, <3% of revenue, no thesis change | conf 0.75 | ~Jul 28 Federal Register | ⏳ open |

## Scored forecasts

_None yet — the first batch resolves with the Q2 filings this week (Jul 28–30)._

**Read that as a warning, not a placeholder.** Ten open forecasts and zero scored
means every confidence weight now driving the optimizer is an assertion, not a
measurement. The engine's arithmetic is sound; its inputs are so far unaudited by
reality. Treat the first scoring round as the moment this system starts being worth
something.

---

## Standing lessons

_Populated as patterns emerge across scored forecasts. Seeded with errors already
made and caught — they were real and they are worth not repeating._

| Date | Lesson | Where it changed the process |
|---|---|---|
| 2026-07-24 | Aggregating percentage P&L across positions instead of value-weighting understated the drawdown by ~5pp (−13.9% reported vs −18.8% actual). | Portfolio math now computed from cost and value, never from averaging percentages |
| 2026-07-24 | Assumed KDH's Gladia JV was equity-accounted; the Q1 statements showed full consolidation. A structural assumption was made without reading the note. | Ownership/consolidation basis is now read from the filing before any model is built |
| 2026-07-26 | Derived TTM earnings from estimated share counts; MBB's base came out ~35% low and produced a fictitious +85% expected return. | `npat_ttm` is now derived from the earnings path (H1 actual + prior H2), with a market-cap cross-check |
| 2026-07-26 | Applied a *peak* exit multiple to *peak* cyclical earnings on HPG, and to a non-repeating divestment gain. | Cyclical multiples are now inverted (low on peak, high on trough) and one-offs stripped before any multiple is applied |
