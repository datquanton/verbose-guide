# Session handover — state of the book at 2026-07-31

**Updated 01-Aug 05:53 ICT.** MBB filed (§2, §3). **Two of the four escalations in §4 are now RESOLVED**,
and a new structural one has replaced them — see §4 and §9.

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
| **MBB** | **Filed, surfaced 31-Jul** — one day past its Circular 96/2020 deadline | Q2 PBT **₫10,560bn +40%**; Q2 NPAT-to-parent **₫8,229.06bn +40.01%**; H1 NPAT-to-parent ₫15,744.58bn +26.51%. Net interest income +36.55%. NPL 1.45% (from 1.42%) with coverage *rising* to 93.63%. Confidence **held at 0.55** — T5 press, and charter §2 permits a rise only on T1–T2. |

**All three statements are now in. The date gate is closed; the next is Q3, due 30-Oct.**

**Two figures in MBB's Q2 coverage were the Q1 numbers reappearing** — provisioning ₫3,455bn (+15.7%)
and loans ₫1.12 million tỷ (+3.3%), both already on file to the digit. Neither was logged, so **H1
provisioning is still unknown.** The tell was free: *a new figure that exactly equals an old one is
usually the old one.*

## 3 · Calibration: 1 hit, 2 misses

| # | Forecast | Result |
|---|---|---|
| 2 | HPG Q2 core NPAT/tonne below ₫1.60m | ❌ **MISS** — actual ₫1.835m. The forecast contradicted my own timing note written the same day. |
| 1 | KDH Q2 parent NPAT ₫170–348bn | ❌ **MISS** — by ~5× on the falsifiable part. Right in direction, badly wrong in calibration. |
| 10 | US rebar final ≈ headline risk only | ✅ **HIT** — right for the *stated* reason. The rate went the wrong way (finals ~6.6pp above preliminary) and the impact claim still carried it. |
| 4 | MBB Q2 NPAT ≈ ₫7,052bn, band ₫6,347–7,757bn | ❌ **MISS** — actual consolidated NPAT ₫8,448bn, **+19.8%**, on the forecast's own measure. |

**Now 1 hit, 3 misses across four resolved forecasts. All three misses were on the estimate side,
not the direction side** — the base cases keep being wrong about *magnitude*, twice too high
(KDH, HPG) and once too low (MBB).

**The pre-registered read on #4 is scored WRONG, on its own stipulation.** It said *if MBB misses,
expect it to miss on credit cost with net interest income intact* — and pre-committed that *"if MBB
instead misses on the top line, **or beats outright**, this read is wrong."* **MBB beat outright.**
That clause is the only reason this is recorded as a failure rather than quietly retired.

**The read-across is the finding, not the miss.** ACB printed **−12%** and VIB **−8%** on
provisions; I inferred a sector cycle and applied it to MBB. **MBB printed +40%** — a ~52pp spread
between two large banks in one quarter. What did work was the sequencing: MBB's *own* Q1 provisioning
(+15.7% vs PBT +14.8%) contradicted the peer inference, and the read was **withdrawn on 30-Jul,
before the print**, on that bank-specific evidence.

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
5. **MBB Q2 — the same defect, opposite sign.** Escalation trigger #4 fired (estimate → filed
   actual). H1 PBT **₫20,188bn** leaves bear needing H2 **−26.6%**, base **−11.2%**, bull **+4.3%**
   — and bank profit here is second-half weighted, so a *flat* H2 gives FY PBT ₫40,376bn, above
   base. **Two of three branches now require profit to fall outright.** The 28-Jul pre-registered
   table called this exact row in advance and its instruction is *rebuild, do not celebrate*.
   **The sharp part: a +40% quarter moved MBB's expected return by zero** — still +8.8% — because
   the branches are typed in and nothing derives them. The engine is blind to the best print in the
   book while proposing MBB as its joint-largest add. `OPEN-DECISIONS` item 19, new.

### Resolved overnight, 31-Jul → 01-Aug

| Was blocking | Outcome |
|---|---|
| **`OPEN-DECISIONS` item 1** — VPB's two credit fields "cannot both be right" | ✅ **RESOLVED.** They can: **both describe the PARENT** (₫1,060,000bn, +24.6%). Consolidated loans are a *third* series at **₫1,160,000bn, +23%**. The fake +10.19% came from dividing a **parent stock by a consolidated base**. **Resolves in VPB's favour** — H2 needs ≤ +12.0% on the base branch, not the feared +22.5%. |
| **TCB credit-vs-loans**, the reason confidence was cut 0.85→0.80 | ✅ **RESOLVED, and the 28-Jul inference was INVERTED.** **+10.4% is loans; +14.3% is credit** incl. quota-exempt infrastructure/social housing. So the non-loan book **grew**, not shrank. `loans_start_fy`→`loans_mid_fy` is **+14.46% vs a reported +14.3%** — the model's pair was never mismatched. H2 needs **+1.5/+3.2/+5.0%**. |

**Near-miss worth knowing about:** the inverted TCB reading produced a **~₫40,700bn** gap sitting beside
the **₫39–40,000bn** of real-estate exposure TCB cut and the **₫44,500bn** Masterise raised — an
irresistible "exposure moved from loans into bonds" story. **The source names the gap as quota-exempt
lending.** It was false, and *quantitatively closer* to the on-file numbers than the truth.
**The Masterise test still needs the corporate-bond line and is NOT settled.**

### New escalations raised overnight

5. **The 403 wall is suppressing THREE confidence restorations across 51.5% of the book.** MBB (0.55),
   VPB (0.70), TCB (0.80) — in every case the evidential objection has been *answered*, and in every case
   the raise is blocked because the evidence is press, not the document (charter §2, T1–T2 only).
   **Confidence multiplies `fy26e_npat`, so this biases expected returns downward, selectively, on the
   three largest bank positions.** `OPEN-DECISIONS` item 17 is no longer an access inconvenience.
6. **HCMC Decision 45/2026/QĐ-UBND** — the land-price adjustment coefficient (**K = K1×K2×K3, K1=K3=1**),
   **in force since 01-Jul-2026**, and the repo had **zero record of it**. Land-use fee is the largest cost
   input for a developer and **KDH is 20.3% of the book with >₫23,000bn of inventory.** *Third* dated
   regulation missed in four days, and the **second effective 01-Jul**. New `OPEN-DECISIONS` item 20.
   **The direction is not established** — a higher table raises fees, a published K unblocks stalled
   approvals, and the two cannot be netted from here.
7. **`OPEN-DECISIONS` item 13 got WORSE.** A **third** candidate for HPG's divestment gain (~₫3,800bn,
   Phố Nối) joins ₫4,123bn and ₫4,010bn. **The spread bridge's calibration anchor now ranges
   1.644–1.752m/t, a 6.5% spread**, and the new figure moves it *up* — the opposite direction from the only
   alternative previously considered.

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

**MBB, a day later, is the same defect pointing the other way — and it is the better test.** KDH's
branches were contradicted from *above*, so holding confidence cost nothing; it was the convenient
answer as well as the right one. MBB's are contradicted from *below*, so holding confidence
**understates a genuinely good quarter** and leaves MBB ranked 4th on a +40% print. It was held
anyway, because charter §2 forbids raising confidence on press *about* a filing, and that is the
same rule that protected KDH. **A rule that only binds when it flatters you does not bind.**
Both names need the same human fix, which is not a confidence number: **re-derive the branches.**

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
| **3 Aug** | TCX's VN30 entry is **effective** — but **the ETF rebalance COMPLETED 31-Jul**, the session before. **The flow has already happened**; an effective date is not a flow date. Sizing confirmed at ₫59–60bn = **0.073% of market cap**. **July CPI publishes the same day** |
| ~21 Aug | KDH insider-buy window closes (Vice Chairman's son, 0.056% → 1.838%) |
| **mid-to-late Sep** | **ITC final injury vote on rebar** — within 45 days of the 30-Jul Commerce finals. An "August" date circulating is a **stale pre-determination projection**. **The ITC has already voted affirmative on ALGERIA in the same petition.** Vietnam's margins (128.53–136.57%) are **2.4–4× Bulgaria's and Egypt's** |
| 21 Sep | FTSE Secondary Emerging effective, **phased in tranches to Sep-2027** |
| 30 Oct | Next Circular 96/2020 deadline — Q3 statements |
| — | MBB stock dividend 15% and rights 10:1 at ₫10,000 — **both still pending, no record date announced.** The rights price is ~45% of market and dilutive to anyone not taking it up |

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
- **Bank outcomes did not travel across the sector this quarter.** ACB −12%, VIB −8%, MBB +40%
  on PBT — same quarter, same rate environment. Peer read-across was tested prospectively here
  and failed by ~52 percentage points.
- **Foreigners have net sold ₫92,000bn YTD** (>62,000 to May, ~80,000 to June, 92,000 to July) and 2026
  is on track to be the **fourth consecutive year** of net selling — a third independent ground against the
  TCX FTSE event tree, though active outflow and passive inclusion inflow are **different pools and must
  not be netted**.
- **Interbank funding cost rose at every tenor through July** (overnight 2.43%→2.97%, 3-week 5.29%→5.88%)
  **while deposit rates sat still** — and **Circular 25/2026 took effect in the same month**, relaxing a
  ratio while the price moved against it. Loans outgrew deposits **2.2× at TCB** and **13.2% vs a shrinking
  base at MBB**.
- **All three HPG spread inputs are now pinned on the file's own benchmarks:** ore **$98.25**, coal
  **$218.50**, HRC **$535–546.5**. The July move cost **−₫0.437m/t** — coal relief clawed back only 41% of
  the price cut. Spot case **₫0.86–1.10m/t**, still below the ₫1.25m bear branch but the gap has narrowed
  from ₫0.42m to ₫0.15–0.39m.
- **"MBB" pulls at least three entities**: MB Bank (ours), MB Securities, and MBB SE (Xetra).
  Poland's mBank too. Five false hits this session.

## 9 · What is blocked, and on what

**Five** fronts now, not three, all returning **proxy 403**: the TCB bond line (`OPEN-DECISIONS` 17b),
the Federal Register rate tables, the HOSE / MB disclosure pages, **techcombank.com's own Q2
press-release PDF**, and **HPG's statement note on other income** (which is what would settle item 13).
**This is no longer only an access problem — see §4 escalation 5.** **The FiinQuant connector is unauthorised and cannot be authorised
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
