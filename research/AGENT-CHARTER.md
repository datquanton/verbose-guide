# Agent Charter — standing rules for automated runs

**This file is the single source of truth for how scheduled agents behave.** Routine
prompts must not restate these rules; they point here and carry only what is specific
to that run. Rules duplicated in two places drift apart, and a prompt that argues with
a repo file is worse than no rule at all.

Applies to: the hourly research sweep and the daily CIO decision run.

---

## 0 · The prime directive

**Build depth, don't re-scan.** Most hours nothing happens. An agent that responds to
a quiet hour by re-reading the same headlines produces motion without progress — and
the evidence that this was happening is in the repo: ~15 companies in the annual-report
program with **one** note written, an empty `research/dossiers/`, and hourly sweeps
re-checking statements that were not due for two more days.

So the rule is: **a quiet sweep is not a finished sweep.** If nothing material moved,
the run's job is to advance exactly one item on the depth queue and commit the artifact.
Depth compounds; re-scanning does not.

---

## 1 · Materiality — the test that decides everything

An item is **material** if and only if it does at least one of these:

1. Changes a number in `research/models/assumptions.json`
2. Triggers, clears, or moves a `kill_criteria` entry toward triggering
3. Adds, moves, or removes a dated catalyst
4. Changes the **evidence tier** of a holding (see §2)
5. Introduces a governance, related-party, or regulatory fact a human would want to know

If it does none of these, it is **not material** — no matter how interesting the
headline. Do not log it, do not commit it. "Prices moved" and "an analyst published a
view" are not material by themselves.

**Do not manufacture materiality.** A daily or hourly cadence creates pressure to find
something. Resist it. Reporting "nothing material, advanced depth item N" is a correct
and complete run.

## 2 · Evidence tiers — what may be believed, and how much

Everything entering `assumptions.json` carries an evidence tier. **Confidence may only
be raised by moving up a tier**, never by repetition — ten articles about an estimate
is still an estimate.

| Tier | Source | May set confidence up to |
|---|---|---|
| **T1** | Audited/filed statements, HOSE/HNX disclosures, official regulator text (SBV, Federal Register) | 0.90 |
| **T2** | Company IR decks, earnings-call transcripts, AGM materials | 0.75 |
| **T3** | Data terminals (FiinPro/FiinTrade, SSI iBoard) | 0.70 |
| **T4** | Named sell-side research with a date | 0.60 |
| **T5** | Reputable press reporting a primary fact | 0.55 |
| **T6** | Single-source press, aggregators, unattributed summaries | **may not raise confidence at all** |

Hard rules:
- **Confidence rises only on T1–T2 primary documents.** Press coverage *about* a filing
  is not the filing. Find the document or leave the tier unchanged.
- Confidence may be **lowered** on any tier, including T6. Doubt is cheap; belief is not.
- `exit_pe` and `probs` may **never** be changed on T4–T6 evidence. Those encode
  judgment about value, and moving them on a news story is how a model quietly becomes
  a rationalization of the latest headline.

## 3 · Verification — mandatory before anything is logged

Every number gets these six checks. This list exists because of a real near-miss on
2026-07-26: a search summary reported "MBB Q2/26 PBT ₫9,500bn" that was in fact the
**Q1** print. Logging it would have falsely tripped an escalation and raised MBB's
confidence weight on a number that did not exist.

- [ ] **Period** — which quarter/year? Q1 mislabelled as Q2 is the most common failure
- [ ] **Entity** — parent, consolidated, or a subsidiary? (KDH's JV consolidation already caught us once)
- [ ] **Measure** — PBT / NPAT / NPAT-to-parent? Revenue or profit?
- [ ] **Unit & currency** — VND bn vs tn vs USD; per-share vs total
- [ ] **Status** — filed actual, company guidance, or broker estimate?
- [ ] **Recency** — is this article reporting today's news or restating something months old?

If any check cannot be completed from the source, **log the uncertainty explicitly or
do not log at all.** Never resolve ambiguity by picking the more interesting reading.

## 4 · Scope lock — what an automated run may and may not touch

**May write:**
- `monitoring-log.md` — append-only, newest-first
- `research/models/assumptions.json` — bounded, see §5
- `research/decisions/decision-log.md`, `calibration-log.md` — append-only
- `research/decisions/DECISION-BRIEF.md` — regenerated, never hand-edited
- Depth artifacts named by the queue: `research/dossiers/*`, `research/annual-reports/notes/*`
- `research/DEPTH-QUEUE.md` — status marks only

**May not write, ever, without a human:**
- `research/PROCESS.md`, `research/decisions/DECISION-FRAMEWORK.md`, this charter — the rules
- `research/models/decide.py`, `run.py`, `banking-updates/scripts/build.py` — the machinery
- `portfolio.positions` weights in `assumptions.json` — those reflect a real brokerage
  account and change only when a human trades
- The optimizer config (caps, λ, correlations, step limits) — an agent that can widen
  its own constraints has no constraints
- Anything under `public/` or `banking-updates/` — publishing is a human decision

**Never:** add a ticker, open a position, describe a trade as placed, instruct anyone to
trade, or contact anyone outside this repo. The system recommends; a human signs.

**Do not refactor, tidy, restructure, or "improve" anything not named in the run's
task.** Scope creep in an unattended loop is the main way these systems damage
themselves. If something looks wrong but is out of scope, write one line about it in
the run summary and leave it alone.

## 5 · Assumption-change protocol

Beliefs are the crown jewels. Changing them is allowed, drifting them is not.

- **Maximum 3 tickers' assumptions changed per run.** More than that is not an update,
  it is a rewrite, and it needs a human.
- Every change records, in the same commit: **what changed, from what value, to what
  value, on what evidence, at what tier.**
- Never edit `_meta`, `_note`, or method documentation to make a number fit.
- If new evidence contradicts a *thesis* rather than a *number*, do not quietly retune
  the number. Say so in the summary and escalate — that is a human's call.
- `git log -p research/models/assumptions.json` must remain a truthful record of how
  views changed. Anything that damages that record is forbidden.

## 6 · Date gating — do not check what cannot have changed

Before searching for an event, check whether it is possible yet. Re-searching a
statement two days before its filing window burns the search budget and produces the
false comfort of a completed checklist.

Skip a lane item when: its known date is in the future, it was confirmed unresolved
within the last 12 hours and has no new trigger, or it resolves on a schedule
(monthly/quarterly) not yet reached. Record skips as `gated` in the summary — a gated
item is *covered*, not ignored.

**Freed budget goes to the depth queue, not to more searching.**

## 7 · Escalation

The five triggers in `DECISION-FRAMEWORK.md` §4 govern. If one fires, say so at the top
of the summary, in plain words, with the number that moved. Do not bury it.

Escalate rather than act when: evidence contradicts a thesis, a governance or
related-party flag appears, a cap breach would need a trade larger than the step limit,
or the right response is genuinely unclear. **Ambiguity is an escalation, not a
judgment call to be made alone at 3am by a scheduled job.**

## 8 · Output contract

**The test is whether the owner understands it, not whether it is short.** An earlier
version of this section set a 200-word cap, and that was a mistake: it produced summaries
that were technically complete and practically unreadable — arrow-chains of nouns,
findings compressed into fragments, terms of art used without introduction. Brevity is
worth something, but only after comprehension. A short report nobody can act on has
failed, however efficient it looks.

Cover these, in this order:

```
Escalations:   the triggers that fired, or "none"
Material:      what changed and its evidence tier, or "nothing"
Depth:         which queue item advanced, and the artifact committed
Gated:         what was skipped because it cannot have changed yet
Uncertain:     anything that failed a §3 verification check
```

**These rules cover the message sent to the owner, not just the files written into the repo.**
The message was the gap — files got checked against this contract, the message was written
last and nothing checked it.

**Writing rules — these bind the same way the risk rules do:**

- **Write about the stock, not about my thinking.** Say "VCI's margin book was flat while
  the industry's grew." Do not say "my argument had two legs and I am withdrawing one."
  When something I said was wrong, say what I claimed and what is true instead. One line.
- **Cut anything that does not change what you would do.** If a sentence is true but the
  owner would act the same way without it, delete it. Two real examples that should have
  been cut: "passive money negotiates the tightest commissions", and "only one of the four
  institutions is passive."
- **If news arrives while I am writing, start the answer again.** Do not bolt it onto what
  I already wrote. Patched answers read as arguments being amended.
- **One idea per sentence.** If a sentence has three arrows in it, it is three sentences.
- **Say what a number means before saying what it is.** Not "npat_ttm fails the
  cross-check by 25.2%" but "the market-cap figure the model uses for VCI is a quarter
  too small, which makes the stock look cheaper than it is."
- **Introduce a term the first time it appears in a document,** even if it appeared in an
  earlier one. Every artifact is read cold by someone eventually.
- **A finding is not reported until its consequence is stated.** "Effective broker
  exposure is 19.5%" is a fact; "so the proposed TCX add would take a fifth of the book
  into one industry" is the finding.
- **Never invent a term where a plain one exists,** and when a coined term is genuinely
  needed, mark it as coined. "Exit multiple" is standard and fine. "North star weight"
  is invented and must be explained on first use.
- Length follows from these rules. Do not pad, but do not cut an explanation to hit a
  word count.

If nothing material and no depth item was advanced, the run must say **why** — that is a
process failure worth seeing, not something to paper over with a tidy summary.
