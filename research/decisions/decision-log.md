# Decision Log

Every decision, dated, with the reasoning **as it stood at the time** — not as it
looks in hindsight. Newest first.

Entries are never edited after the fact. A wrong entry stays wrong and gets a
follow-up; rewriting history destroys the only evidence of how thinking actually
changed. Each entry carries a **review date**, so decisions cannot quietly become
permanent by neglect.

Format: `DECISION · rationale · what would change my mind · review date`

---

## 2026-07-26 · Decision engine commissioned; first brief produced

**DECISION:** Adopt `decide.py` output as the standing sizing recommendation, with
the two constitutional breaches (TCB 35%, Techcom cluster 40.5%) scheduled for
correction to cap.

**Rationale.** The book's problem was never idea quality — five of six names printed
record 1H results into falling prices. It was that position sizes bore no stated
relationship to conviction. TCB at 35% is the largest position and, on current
multiples, ranks **7th of 8** on expected return (+3.6% shrunk). That is not a view;
it is an accident of not having done the arithmetic. The first brief's headline is
therefore mechanical, not clever: bring the breaches to cap, and let the freed weight
go to names that actually score.

**What the engine is NOT saying.** It is not saying TCB is a bad company — its Q2 was
a record. It is saying that at ₫29,250 a 35% weight prices in more than the model can
justify, and that the same money in MBB or TCX carries a better expected return per
unit of risk. Those are different claims and only the second is being made.

**What would change my mind:**
- TCB's exit multiple is the weak input. If VN banks re-rate toward 10–12× on the
  FTSE upgrade (against 8.0× base here), TCB's expected return roughly doubles and
  the trim is wrong.
- The Q2 filings due Jul 28–30 could move HPG, KDH and MBB materially — all three
  currently price off estimates.

**Review date:** 2026-08-01, after the Q2 statements land.

**Open risk I am carrying knowingly:** the confidence weights driving this brief are
asserted, not measured. Zero forecasts have been scored. See `calibration-log.md`.

---

## 2026-07-24 · Second account integrated; risk map redrawn

**DECISION:** Treat both brokerage accounts as one book for all sizing purposes.

**Rationale.** Managing accounts separately hid the real exposure. Combined, the
concentration problem moved from KDH (which fell to a compliant 20.3%) to TCB (35%)
and the Techcom cluster (40.5%). Banks total 51.5%; effective independent bets ≈4.7
across eight lines. Two accounts is a custody fact, not a portfolio-construction fact.

**Review date:** ongoing — every brief now runs on combined weights.

---

## 2026-07-24 · Beliefs moved to a versioned file

**DECISION:** All forecasts live in `assumptions.json`; nothing load-bearing lives
only in prose.

**Rationale.** `git log assumptions.json` becomes the record of how views changed and
when. Without it, hindsight quietly rewrites what was believed before an outcome —
the failure mode that makes most investment journals worthless.

**Review date:** permanent (process rule).

---

## 2026-07-23 · No averaging down during the July drawdown

**DECISION:** Hold through the drawdown; add nothing.

**Rationale.** The decline was market-wide beta against record 1H prints, not company
failure — but "the market is wrong" is exactly what a person says before averaging
into a genuine problem. With the book already breaching two concentration caps, adding
would have compounded a sizing error with a conviction error.

**Outcome so far:** correct on the diagnosis (results confirmed the businesses),
unresolved on the price.

**Review date:** superseded by the 2026-07-26 brief.
