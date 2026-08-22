# Routine prompts — proposed replacements

**Status: DRAFT, not applied.** These are the texts I propose replacing the two stored
scheduled-task prompts with. **An automated run has not changed and will not change the
live triggers.** A prompt is the instruction an agent runs under; an agent that edits its
own instructions unattended has no instructions. Changing the live triggers is a human
action — copy the blocks below into the scheduler by hand.

---

## Why the current prompts need replacing

The live hourly prompt is roughly 700 words and it carries **its own copy** of three
things that already exist in the repo:

| What the prompt restates | Where it already lives | What goes wrong |
|---|---|---|
| The seven monitoring lanes, with tickers and dates | `monitoring-log.md` header | The header was updated with date gates on 26-Jul. The prompt was not. The two now disagree, and the agent obeys the prompt |
| Estimates to compare against (HPG ~5,020–6,500bn, KDH ~170 vs ~330–348bn, MBB ~8,812bn) | `research/models/assumptions.json` | Numbers frozen into a prompt cannot be revised by a run that learns better ones. They become stale beliefs that the agent treats as current |
| What to do when something is found, and what to commit | `AGENT-CHARTER.md` §1–§8 | Two statements of the same rule drift apart. When they conflict, nothing decides which wins |

That duplication has a measurable cost. The prompt names specific things to search for —
"official Q2/26 statements for HPG, KDH, MBB" — with no gate on whether the filing window
has opened. Charter §6 says do not search for what cannot have changed yet. The prompt
says search for it every hour. **Sweeps have been re-running searches for statements that
were not due for another two days**, which is the exact behaviour the charter was written
to stop.

The fix is not to make the prompt better. It is to make the prompt **thin**: say what this
run is for, point at the files that hold the rules and the lanes, and stop. Then a rule is
changed by editing one file, and every future run picks the change up automatically.

---

## Prompt 1 — hourly research sweep

Replace the stored hourly prompt with this:

```
Hourly research sweep (automated Routine, continuing thread). This is the GATHER stage;
the daily CIO run decides.

Read these three files first, every run. They are the instructions — this prompt is not:
  research/AGENT-CHARTER.md   rules: materiality, evidence tiers, verification, scope
  monitoring-log.md (header)  the lanes to cover and the date gates on each
  research/DEPTH-QUEUE.md     what to do when nothing material happened

Look ONLY for developments newer than the top entry in monitoring-log.md. Cover the core
lanes named in that header; rotate through the others so all are covered daily. Skip any
lane item whose date gate has not opened and report it as `gated` — a gated item is
covered, not ignored.

Budget 4–8 searches. Freed budget goes to the depth queue, never to more searching.

If material (charter §1): log it, update assumptions.json within the charter §5 limits,
run `python3 research/models/run.py && python3 research/models/decide.py`, check the
DECISION-BRIEF against the five escalation triggers in DECISION-FRAMEWORK.md §4, score
any forecast that resolved in calibration-log.md, then commit and push to
claude/banking-vietnam-reports-scrape-5p6rtu.

If nothing material: do NOT commit a log entry. Advance the topmost `todo` depth item and
commit that artifact instead. If the queue has no available item, say so plainly as the
process failure it is — do not invent work and do not re-scan.

Write the summary to the charter §8 contract and its writing rules.
```

**What changed and why.**

- The lane list is gone from the prompt and read from `monitoring-log.md` instead. Editing
  the lanes now takes one edit in one place.
- The hard-coded broker estimates are gone. The run compares against
  `assumptions.json`, which is the file that is actually maintained.
- Date gating is now stated as a rule the run must apply, rather than a list of things to
  search unconditionally.
- The "never place a trade" line is dropped from the prompt **because it is in charter §4**,
  which the run is now required to read. This is the point of the whole exercise: the rule
  is not weaker for being in one place, it is stronger, because there is no second copy to
  drift from it.
- The output contract is a pointer, not a restatement.

## Prompt 2 — daily CIO decision run

```
Daily CIO run (automated Routine, continuing thread). This is the DECIDE stage. The hourly
sweeps gather; this run converts what they gathered into a sized recommendation.

Read research/AGENT-CHARTER.md and research/decisions/DECISION-FRAMEWORK.md first.

1. Run `python3 research/models/run.py && python3 research/models/decide.py`.
2. Read research/decisions/DECISION-BRIEF.md. For every name whose recommended weight
   differs from its held weight by more than 1pp, state in plain words WHY the engine
   wants the change — which input moved, and when it moved. A recommendation whose cause
   you cannot name is a bug, not a decision.
3. Test it against the five escalation triggers in DECISION-FRAMEWORK.md §4. If any
   fires, lead the summary with it.
4. Append the day's recommendation to research/decisions/decision-log.md, including the
   ones you are NOT proposing to act on and why.
5. Score every forecast in calibration-log.md that resolved today. Direction, error
   against the probability-weighted estimate, and whether it was right for the reason
   given or for a different one. Right-for-the-wrong-reason is recorded as a failure.

Recommend only. A human signs every trade — never describe one as placed.

Do not change portfolio weights, optimizer settings, or any file listed in charter §4 as
human-only. If the right answer requires changing one of those, that is an escalation,
not an action.
```

---

## What a human needs to do

1. Open the scheduler and replace the two stored prompts with the blocks above.
2. Keep `monitoring-log.md`'s header as the lane definition. It already says so.
3. When lanes or gates change, edit that header — not the prompt.

Until step 1 happens, sweeps keep firing on the old text, and the charter's date gating is
advisory rather than binding.
