# Trigger-integrity audit — can each watch item's trigger actually fire?

**Run 2026-08-11 ~23:30 ICT, parallel session, branch `claude/vn-research-parallel-thread`.**
Repo-only audit. No lane sweep was run. Two searches spent, both on fixed legal questions
of the kind that settle all future sweeps rather than one more nil.

**Scope:** all 15 rows of the COVERED block and all 33 rows of the date-gate table in
`monitoring-log.md`, plus the numbered items in `research/OPEN-DECISIONS.md`.
**Not re-done:** the seventeen armed kill criteria — item 44 audited those on 07-Aug and
found 5 testable of 17. This is that audit's watch-item analogue.

**This file reports. It repairs nothing.** Every fix below is §4 human-only.

---

## 0 · What was found

**Two phantoms, one of them load-bearing on a dated catalyst four days out.** Plus a new
sub-type the KDH case did not name, four unfalsifiable re-open conditions, two passed-and-
unretired rows, and three places where two control surfaces contradict each other.

A note on the classification that matters most: **PHANTOM and UNOBSERVABLE look identical
in a log and mean opposite things.** UNOBSERVABLE means keep looking, through another
route. PHANTOM means stop — there is nothing to look for. They are kept strictly apart
below, and where I could not tell them apart I have said so rather than guessed.

| Verdict | Count | Meaning |
|---|--:|---|
| **PHANTOM** | **2** | The event or obligation does not exist as described |
| **PREMATURE** | **1** | Real event, but the gate date precedes the earliest date it can legally occur — a guaranteed nil |
| **UNFALSIFIABLE** | **4** | Re-open condition cannot be detected from inside a sweep |
| **PASSED** | **3** | Trigger date gone, row not retired |
| **UNOBSERVABLE** | **2** | Real and reachable in principle, structurally blocked from here |
| **SOUND** | **33** | Checkable condition on a reachable observation |
| **COULD NOT CLASSIFY** | **3** | Stated below with the reason |

---

## 1 · PHANTOM — the obligation does not exist as described

### 1.1 The 14-Aug KDH reviewed-statement gate

**Row:** date-gate table, *H1/2026 REVIEWED statements*.
**Stated trigger:** *"standalone/parent due 2026-08-14 (45 days); consolidated due
2026-08-29 (60 days), per Circular 96/2020."* Carried in `SESSION-HANDOVER.md` as a dated
catalyst — *"Fri 14-Aug … + KDH H1 auditor-reviewed statements"* — and the row calls 14-Aug
*"the document that settles KDH's ₫321bn vs ₫1,097bn basis question."*

**The test that decided it — two independent legs.**

*Leg 1, free, from the file's own record.* The file reads the 45/60 split as a **statement
type** distinction: standalone at 45 days, consolidated at 60. But this same file states the
**quarterly** rule from the same circular as an **entity type** distinction — *"a listed
parent company with subsidiaries must disclose within 30 days; companies without
subsidiaries have 20 days"* (`monitoring-log.md`, "Why 30 July is hard"). Those two readings
are incompatible. The Q2 record decides between them: HPG, KDH and MBB are all parents. Under
the statement-type reading each owed a **standalone at 20 days — 20-Jul**. The file records
all three *"still unfiled at the close on 29 July"* and then filing 29–31 Jul. **No 20-day
standalone was filed by any of the three.** The statement-type reading is falsified by the
file's own three-name sample.

*Leg 2, search 1.* Circular 96/2020's semi-annual provision has the same shape: a general
45-day outer bound for listed organisations and large-scale public companies, and a
**separate special case for a parent company or a higher-level accounting unit**. The
distinction the circular draws is **parent versus non-parent. It is not standalone versus
consolidated.** No source supports the split as the row states it.

**What is established:** the row invents a second deadline. A parent has **one** semi-annual
outer bound, not two, so one of the row's two dates is a date on which KDH is required to
file nothing.

**What is NOT established, stated plainly:** which of the two survives. The retrieved text
truncated before giving the parent clause's number. If the parent bound is 60 days —
the likely reading, since it matches the quarterly 20/30 structure, and it is what the row's
own secondary source said — then **14-Aug is empty and 29-Aug is the real date.** If the
parent bound is 45, then 29-Aug is empty instead. **The row is wrong either way**, and the
direction of the error is worth a human's five minutes because it moves a catalyst by
two weeks in one direction or the other.

**Consequence.** On the 60-day reading the file will look on 14-Aug, find nothing, and the
nil will be uninformative — which is the precise failure the 11-Aug calibration entry named:
*"a watch item that can only ever return one value will, given enough time, be mistaken for
evidence."* KDH is 20.3% of the book and the file has an armed kill criterion on it.

### 1.2 The 29-Aug consolidated deadline is a Saturday

**Test:** `date -d 2026-08-29` → **Saturday**. Verified with `date -d`, not counted by hand.

30-Jun + 60 days = 29-Aug. The arithmetic is right and the date is not a filing day. A
deadline landing on a non-working day rolls forward, so the earliest realistic filing is
**Mon 31-Aug**.

**Why this one stings:** on 09-Aug this file caught an external source putting US retail
sales on **Saturday 15-Aug** and correctly discarded the source's entire date set for it.
It applied that check to somebody else's calendar and not to its own. `SESSION-HANDOVER.md`
currently lists *"29-Aug KDH + VPB consolidated"* as a dated catalyst.

---

## 2 · PREMATURE — a new sub-type, and the closest relative of today's KDH phantom

### 2.1 The KDH insider completion report cannot exist on 21-Aug

**Row:** date-gate table, *KDH insider buy*, leg (b) — the leg that survived this morning's
deletion of the phantom 1%-crossing and is now, in the row's own words, **"the whole
signal."**
**Stated trigger:** *"the completion report following the window's close on 21-Aug"* →
**"RE-OPEN: 21-Aug window close — and NOTHING before it."**

**The test — search 2.** Thông tư 96/2020: an insider (`người nội bộ`) or related person must
disclose the **result** of a registered transaction *within 05 working days from completion
of the transaction, or from the end of the registered transaction period*, with an
explanation if the registered volume was not fully executed. The company then has a further
**03 working days** to publish it on its own site after receiving the report.

**The arithmetic, weekdays verified with `date -d`:** the window closes **Fri 21-Aug**.
Five working days = Mon 24, Tue 25, Wed 26, Thu 27, **Fri 28-Aug** — the report deadline.
Add the company's 3 working days and the public disclosure can legitimately appear as late
as **early September**.

**Verdict: the earliest the signal can exist is 28-Aug. The gate says 21-Aug.** A sweep
re-opening on 21-Aug is guaranteed silence for at least a week, on a signal the row itself
now describes as the entire remaining basis for the KDH insider read.

**Why this is a distinct class from PHANTOM.** The obligation is real and the report will
exist. What is wrong is the **date**, and the failure mode is identical to the phantom's:
a watch that can only return one value. The KDH phantom was *no obligation ever*; this is
*no obligation yet*. Both produce a nil that means nothing and reads like something.

**Not the same defect, and worth saying so:** the VCI Tô Hải row words this correctly —
*"the completion report follows 02-Sep"*. **Follows**, not *on*. One row got it right and
the row next to it did not.

---

## 3 · UNFALSIFIABLE — the re-open condition cannot be seen from inside a sweep

The file already confessed one instance (*"re-open on a TCB announcement"* — unobservable,
so it read as *search every hour*). Four more, same shape.

| Row | Stated re-open | The test that decided it |
|---|---|---|
| **TCB's primary financial statements** (COVERED) | *"network policy changes"* | A sweep can only detect a policy change by attempting the blocked fetch — which is the exact spend the row exists to prevent. The condition is unobservable **except by violating the row** |
| **Single-stock closing prices** (COVERED) | *"only a price feed or an unblocked host reopens it"* | Same structure. Seven attempts, six nil, and attempt seven was made **because** the row's condition gave a sweep no way to know it was still closed |
| **Weekly money market** (COVERED) | *"an overnight print above ~8% re-opens it immediately"* | The **only** channel that has ever delivered an overnight rate to this file is the weekly wrap — first time ever, 11-Aug. The immediate-re-open clause can therefore only be triggered by the report it is meant to preempt. Corroborating: the one spike headline that did surface independently (11%) arrived **undated and ten weeks stale** |
| **SBV ₫220,000bn package guidelines** (gate) | *"in the coming days" from 03-Aug, so **LIVE NOW***  | No date, no issuing obligation, permanently live — 8 days elapsed. **The file already knows this shape is not a trigger:** on 11-Aug 17:54 it correctly refused to call MB's *"August"* Tier 2 tranche a trigger-5 firing because *"trigger 5 requires a DATED catalyst and 'August' is a month."* Same reasoning, not applied here |

**The counter-example, and it is the fix.** The VNDiamond row resolves via
*"(a) FiinQuant MCP authorised by the owner, (b) a widened network policy, (c) incidental
mention in routine lane-3 KDH coverage."* **(a) is genuinely detectable from inside a
session** — MCP authorisation status is visible in the session's own context at startup, at
zero search cost; this session can see FiinQuant is still unauthorised without spending
anything. **(c) is free by construction.** So of four blocked-route rows, exactly one names
a condition a session can actually check, and it was written by the same file. **The template
for repairing the other three already exists in the file.**

---

## 4 · PASSED — trigger date gone, row not retired

| Row | Stated trigger | Status |
|---|---|---|
| **US initial jobless claims** | *"06-AUG, **TOMORROW**"* | Resolved in the log — **199,000 vs ~202,000 consensus** — but the gate row still reads "TOMORROW", five days on |
| **US July employment report** | *"Friday 2026-08-07"* | Resolved in the log — **payrolls −23,000 vs +83,000 consensus**, a large miss against a **pre-registered** direction. The row still carries the pre-registration as live |
| **MBB last cum session / ex-rights** | *"ex TUE 11-Aug"* | Ex-date passed today. Record date tomorrow. Row still reads as forward warning |

**The finding under the first two is not the stale wording.** Both were **pre-registered
forecasts** — *"a weak payroll print is the direction expected, as a TILT not a forecast"* —
and both resolved. `DECISION-FRAMEWORK.md` §6 requires every forecast entering the system to
be **scored** when reality lands, and notes that fewer than ~20 scored forecasts leaves every
confidence number unvalidated. **The payroll tilt was directionally right and there is no
scoring row for it.** Correct calls going unscored costs exactly as much as wrong ones: the
calibration record is the asset, not the call.

---

## 5 · UNOBSERVABLE — real, reachable in principle, blocked from here

| Row | The test |
|---|---|
| **KDH removal-watchlist status** (gate, superseded row) | Asks to *"establish the review date and KDH's current status."* The **only** route is the VNDiamond constituent data, which the row two above it declares **CLOSED — seven attempts, three routes, "NO FURTHER DEDICATED SEARCHES."** An open task whose sole route the same table has closed |
| **Coking-coal index provenance — the load-port amendment effective date** (COVERED, item 46) | Two dedicated attempts, both nil. Re-open names *"a Fastmarkets pricing notice carrying a date, or the methodology PDF"* — both subscriber-gated instruments. **Classified provisionally:** I did not test the host, and per the file's own rule, *a blocked host is evidence about a host, not about a number* |

---

## 6 · Two control surfaces that contradict each other

These are not classification failures. They are two rows that instruct a sweep to do
opposite things, and a sweep reading either one alone will believe it is compliant.

1. **Search weekly vs do not search at all.** The COVERED corporate-action row says re-open
   **"WEEKLY, not hourly"**. The gate row on the four pending share-count increases says
   **"DO NOT SPEND DEDICATED SEARCHES ON EX-DATES"** because `vsd.vn` is gateway-blocked.
   Same subject, opposite instructions, and the weekly one is the one that costs money.

2. **No ex-date established vs MBB's ex-date is established.** The same share-count row
   states *"No ex-date established for any tranche."* The row 6 above it holds MBB's ex-date
   as **11-Aug, record 12-Aug**, confirmed four to five times independently. The row is
   stale on its own most time-critical leg, and **it carries no re-open condition of any
   kind** — no date, no event, nothing that would ever retire it.

3. **Retail sales: established and unestablished in one row.** The US-week row's header
   reads *"✅ THE US WEEK IS NOW FULLY MAPPED, **ALL FROM PRIMARIES** … ADVANCE RETAIL SALES
   FRI 14-AUG."* Its own body reads *"**RETAIL SALES remains unestablished** — it is a Census
   release, not BLS, and no Census date was returned."* Its re-open cell asks for *"a Census
   schedule or a second source."* **`SESSION-HANDOVER.md` carries 14-Aug retail sales as a
   dated catalyst.** A dated catalyst is charter §1 materiality test #3, and this one rests
   on a date the row says it never obtained. The ✅ was applied to the row, not to the item.

---

## 7 · OPEN-DECISIONS — structural findings

- **Duplicate item numbers.** `19` and `20` each appear **twice**: item 19 is both *"re-derive
  MBB's `fy26e_npat`"* (§1) and *"settle λ"* (CFA section); item 20 is both *"KDH land-use fee
  under Decision 45/2026"* (§4) and *"replace the flat ±3pp no-trade band"* (CFA section).
  The file cross-references items by number — the 11-Aug 12:54 entry reasons at length about
  *"open item 20"* — so two of its reference keys are ambiguous. Context resolves them today;
  it will not always.
- **Item 2's trap is now live, not pending.** Item 2 warns *"AFTER 11-AUG IT BECOMES A TRAP"*
  for the MBB price/share-count refresh. 11-Aug has passed. The conditional has become a
  present-tense hazard and still reads as future.
- **Item 35 has no trigger of its own.** It diagnoses that nothing retires an absence claim,
  and proposes that an absence claim must name the field that would resolve it. The proposal
  itself names no field and no date, so nothing will ever retire item 35. Same disease, and
  the diagnosis caught it.
- **Most numbered items correctly have no trigger** — they are decisions awaiting a human,
  not watches. That is not a defect and they are not counted as one.

---

## 8 · Could not classify — and why

| Item | Why not |
|---|---|
| **CAEX licence decision** — *"Q3 window — check weekly, not hourly"* | Nothing in the repo establishes what obligates a decision within Q3, or whether any authority is required to announce one on a timetable. If "Q3" is a company expectation rather than a regulatory deadline, a nil is uninformative and the weekly cost recurs indefinitely. **Deciding this needs a search I was not authorised to spend.** It is the highest-value remaining question of the KDH kind |
| **Coking-coal load-port date** | Provisional UNOBSERVABLE, §5 — host untested |
| **China HRC export price** — *"an assessment dated AUGUST or later"* | The row says no August assessment *is reachable*; the latest is 17 days old. I could not separate a **publication lag** from an **access block** from the repo alone, and those have opposite implications for whether the trigger can fire |

---

## 9 · What a human should do first

Ranked by consequence, not by effort:

1. **Settle the parent's semi-annual outer bound** (§1.1). One reading of one circular clause
   moves a KDH catalyst by two weeks. It is the only item here that changes what the book
   expects to happen this week.
2. **Move the KDH insider gate from 21-Aug to 28-Aug** (§2.1) — or the sweep will read a
   legally-required silence as a bearish insider signal, which is exactly the inference the
   11-Aug calibration entry recorded as **void, not weak**.
3. **Strike 14-Aug and the Saturday 29-Aug** from the handover's dated-catalyst list, or
   re-date them, whichever §1 resolves to.
4. **Drop 14-Aug retail sales** from the dated-catalyst list until a Census date exists (§6.3).
5. **Rewrite the four unfalsifiable re-open conditions on the VNDiamond template** (§3) —
   name a condition a session can check at zero cost.
6. **Score the two resolved US pre-registrations** (§4). The payroll tilt was right.
