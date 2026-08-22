# Cross-field consistency audit

**2026-07-28 · applying yesterday's lesson to the whole book, not just the name that caused it**

Last night VPB's two credit fields were found to contradict each other — a Q1-consolidated
balance and an H1-parent growth rate sitting side by side as though they described one
quarter of one company. The lesson recorded in `calibration-log.md` was general: **any two
fields in the same block that can be checked against each other arithmetically must be.**

A lesson applied only to the name that produced it is not a lesson. This is that check run
across all eight holdings. Six tests, four failures. None changes a recommendation today;
one is structural and explains something the brief has been quietly asserting for days.

---

## 1 · HPG — core profit plus the one-off does not equal the headline

| Field | Value |
|---|---:|
| `q1_core_npat` | ₫5,046bn |
| `q1_divestment_gain` | ₫4,123bn |
| Sum | **₫9,169bn** |
| `q1_npat` (headline) | **₫9,056bn** |
| Gap | **₫113bn, 1.25%** |

These three numbers describe one quarter and must reconcile. They do not.

**Why the gap is not harmless.** `q1_core_npat` divided by `q1_volume_mt` gives **₫1.68m per
tonne**, and that figure is the *calibration anchor* for the entire spread bridge — the
conversion cost of US$114/t was solved backwards so the bridge would reproduce it. If core
is instead the headline minus the gain, ₫9,056 − ₫4,123 = **₫4,933bn**, the anchor becomes
**₫1.644m/t**, about 2.2% lower, and the solved conversion cost rises with it.

**The likely explanation, and why it is not good enough.** A pre-tax gain of ₫4,123bn against
an after-tax gain of ₫4,010bn implies tax of ₫113bn — an effective rate of **2.7%**, far below
Vietnam's 20% corporate rate. That is possible under some divestment structures but it is not
the obvious reading, and nothing in the file says which basis each number is on.

**Not resolved.** Both readings are within 2.2% of each other, so nothing in the ranking moves
and no branch changes. It is flagged because the anchor of a model should not be ambiguous,
and because it reads directly off the Q1 statement.

## 2 · KDH — the model and its own dossier disagree on selling price

`assumptions.json` records `q1_asp_per_unit_bn` = **₫44bn**. The unit-economics table in
`research/dossiers/KDH.md` §1 uses **₫42bn**, sourced to the same Q1 handovers.

The dossier's whole derivation hangs on that number:

| | Dossier (ASP ₫42bn) | Model (ASP ₫44bn) |
|---|---:|---:|
| Gross profit per unit at 65% margin | ₫27.3bn | **₫28.6bn** (+4.8%) |
| Solved quarterly fixed opex | ₫94bn | **₫102bn** (+8.3%) |

**Direction of the correction, stated without overclaiming.** A higher gross profit per unit
means **fewer** units are needed to hit any profit branch. Scaling the dossier's counts by the
gross-profit ratio takes the bull branch from **186 units to roughly 178**.

**The headline finding survives.** The bull branch was called arithmetically infeasible because
186 units are needed against a **135-unit sold book**. At 178 it is still far above 135, so the
conclusion holds and the pre-registered Q2 read stands. What needs redoing is the precision,
not the argument — and the two files must agree on one price before either is trusted to a
decimal.

## 3 · MBB and VCI have no driver model at all — this is the structural one

`run.py` builds scenario models for **six** names: KDH, TCB, VPB, TCX, VPX, HPG. Those six have
an `actuals` block and a `model.scenarios` block, so their profit branches are *built* from
drivers — credit growth, net interest margin, handover counts, tonnes shipped.

**MBB and VCI have neither.** They appear only in the `valuation` block. Their `fy26e_npat`
bear/base/bull figures are typed in directly. Nothing derives them, nothing recomputes them
when a driver moves, and they never appear in `SNAPSHOT.md`.

That is **9.6% of the book** (MBB 6.5%, VCI 3.1%) priced off asserted numbers.

**Why it matters more than the weight suggests.** MBB's raw expected return is **+16.0%**, the
third-highest in the book, and the optimizer proposes taking it from **6.5% to 12.0%** — the
joint-largest add in the brief. **The engine's biggest bank add rests on the one bank whose
earnings branches nobody derived.** That is not an argument against MBB, whose S1 screen passed
on its own merits. It is an argument that the number driving the add has never been stress-tested
the way the other six have.

**Confidence is not being cut for this**, and the reason matters. Confidence measures how good
the *evidence* is, and MBB's evidence — a passed S1 screen, sector-best trailing ROE of 20.9% —
is unchanged by the discovery that the arithmetic behind it is thin. The right response is to
build the driver model, not to shade a number down and call it handled.

**What is being corrected:** MBB's `evidence` string still says "NO DOSSIER YET (S1/S3 pending)".
That is simply out of date — the S1 screen was completed on 26 July and `dossiers/MBB.md` exists.
The string understated what is known while missing what is actually missing. Rewritten to say
both. The confidence number is unchanged at 0.55, because the two corrections point in opposite
directions and roughly cancel.

## 4 · TCB — the brief's percentage does not match the recorded guidance

The decision brief describes TCB as "1H 48.9% of plan". The recorded numbers give a range:
`h1_pbt` ₫18,500bn against `guidance_pbt` of ₫35,000–37,500bn is **49.3% to 52.9%**. To get
48.9% the plan would have to be ₫37,832bn, which is outside the recorded guidance.

Small, and it changes nothing — TCB is at roughly half its plan at the half-year either way.
Recorded because a number in a decision document should be reproducible from the inputs, and
this one is not.

---

## Checks that passed

- **TCX**: `h1_pbt` ₫3,555bn / `fy_plan_pbt` ₫7,535bn = 47.2%, matching the brief exactly.
- **VPX**: 41.4% of plan at the half-year — behind pace, needing 58.6% in the second half.
  Consistent with the dossier, and a fact rather than an error.
- **VPX earnings quality**: first-half FVTPL gains of ₫3,461bn are **1.29×** total pre-tax
  profit of ₫2,673bn. The trading book is not a side activity, it is more than all of the
  profit. Already documented; the check confirms it rather than finding it.
- **Implied market caps**: `pe_ttm × npat_ttm` reproduces the market capitalisation used
  elsewhere for all eight, including TCB's ₫206,661bn. Internally consistent — though note
  this test cannot catch an error where *both* fields are wrong together, which is precisely
  what happened to VCI and VPX.

## What a human is being asked to decide

Nothing here is a trade. Four items need a person:

1. **Read HPG's Q1 statement** and pin whether the ₫4,123bn divestment gain is pre- or post-tax.
   That fixes the spread bridge's calibration anchor.
2. **Settle KDH's ASP at ₫42bn or ₫44bn** and re-derive the dossier's handover counts from
   whichever wins.
3. **Decide whether MBB and VCI get driver models.** They are 9.6% of the book and one of them
   is the largest proposed add. Building them is queue work an automated run cannot add itself.
4. **Regenerate or correct TCB's "48.9% of plan"** so it reproduces from the recorded guidance.

*Method note: these are all checks that need no external source. Every one could have been run
the day the numbers were entered. That none of them was is the finding behind the finding.*
