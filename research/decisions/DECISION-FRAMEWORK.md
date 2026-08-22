# Decision Framework — the CIO layer

The research process (`research/PROCESS.md`) answers *what is true*. This answers
*what to do about it*, and — the part almost every private investor skips — *whether
the last answer was any good*.

```
    monitoring sweep  ──►  assumptions.json  ──►  decide.py  ──►  DECISION BRIEF
      (what changed)        (what I believe)      (the math)      (recommendation)
                                  ▲                                     │
                                  │                                     ▼
                          calibration-log  ◄────────────────────  decision-log
                          (was I right?)                          (what I did)
```

The loop closes. That closure is the whole design: an investor who never scores their
own forecasts is not compounding skill, only opinions.

---

## 1 · The four decision types

Only four things can ever be decided. Naming them stops "I feel nervous about TCB"
from masquerading as analysis.

| Type | Trigger | Decided by |
|---|---|---|
| **Sizing** | Weight drifts from target, or a cap breaches | `decide.py` — arithmetic, low judgment |
| **Entry / exit** | Thesis confirmed, or a kill criterion fires | Human, on a written memo |
| **Belief update** | New evidence lands (a filing, a price, a policy) | Edit `assumptions.json`, note why |
| **Process change** | A post-mortem finds the *method* failed | Edit `PROCESS.md`, dated |

Anything that isn't one of these four is not a decision — it's a feeling, and it
belongs in the log as such or nowhere.

## 2 · What the machine decides vs what a human decides

The dividing line is **falsifiability**, and it is drawn deliberately.

**The engine owns** (mechanical, no discretion):
- Probability-weighted expected returns from stated scenarios
- Confidence shrink by evidence quality
- Constrained optimization → target weights → trade list
- Cap-breach detection, kill-criteria evaluation, risk attribution

**A human owns** (Layer 4 — things no model should be trusted with):
- Governance and related-party judgment. *An An Lap-style bargain-purchase gain is
  arithmetic to the model and a red flag to a person.*
- Whether the exit multiple is defensible at all — the single highest-leverage
  input in `assumptions.json`, and pure judgment
- Politics: credit-quota allocation, the weak-bank transfer regime, trade policy
- Whether to act at all. **The engine recommends. A human signs.**

The engine is not there to be smarter than the analyst. It is there to stop position
sizes from drifting away from stated conviction, which is a failure of arithmetic
rather than insight — and the one an unaided human makes constantly.

## 3 · The decision cadence

| Rhythm | What runs | Output |
|---|---|---|
| Hourly | Monitoring sweep (7 lanes) | `monitoring-log.md` — only if material |
| Daily 08:00 ICT | `decide.py` on current beliefs | `DECISION-BRIEF.md` refreshed |
| On any material event | Belief update → re-run → check kill criteria | Log entry; escalate if a cap or criterion trips |
| Weekly (Mon) | Re-underwrite: does any thesis still hold? | Decision-log entry |
| Quarterly | Re-base on filed statements; **score every forecast** | Calibration-log entry |
| Every exit | Post-mortem: process error vs bad luck | Both logs |

## 4 · Escalation rules — when the agent interrupts a human

Silence is the default. The system only speaks when one of these fires:

1. **A kill criterion triggers.** Not advisory — forces a resize at the next brief.
2. **A cap breaches**, or an existing breach worsens.
3. **Expected return moves >10pp** on any name from one brief to the next.
4. **A held name's evidence status changes** — an estimate becomes a filed actual.
5. **A dated catalyst lands within 5 sessions** of a proposed trade in that name.

Everything else accumulates quietly and shows up in the next scheduled brief.

## 5 · Position-sizing constitution

Rules written when calm, to be obeyed when not. The book currently breaches two.

- Max single name **20%** · max correlated cluster **35%** *(TCB 35% and Techcom 40.5%
  are live breaches — the brief brings both to cap)*
- Minimum position **2%** — below that it cannot move the book and only costs attention
- Max discretionary move **5pp per name per cycle**; a constitutional breach overrides
  this and returns to cap immediately
- No averaging down into governance flags or unexplained drawdowns. Only into a
  confirmed thesis plus market-wide weakness
- Entry staged in thirds; full size only after the first confirming datapoint

## 6 · Scoring — the only measure of edge that matters

Every forecast that enters `assumptions.json` is scored when reality lands, in
`calibration-log.md`. Three things get tracked:

- **Direction** — was the base case on the right side?
- **Magnitude** — Brier-style error on the probability-weighted estimate
- **Attribution** — right for the right reason, or right by luck? *(These score
  differently. Being right by luck is a process failure that happens to pay.)*

The question calibration answers is not "am I up?" — a rising market answers that.
It is: **when I say 45% likely, does it happen about 45% of the time?** If the base
case lands 80% of the time, the scenarios are too timid and the book is under-risked.
If it lands 20% of the time, the models are decoration.

Until roughly 20 scored forecasts accumulate, treat every confidence number in this
system as **unvalidated**. The engine's output is only as good as the calibration
behind it, and that calibration does not exist yet. Building the scoring record is
the highest-value work available right now — higher than any individual stock call.
