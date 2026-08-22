# TCX (TCBS) — Research Dossier

**Status:** S3 core complete (depth-queue item 8) · 2026-07-27
**Why now:** priciest name in the book (2.49× P/B) and the optimizer wants to add 5.1pp
toward a 20% north star. It also turned out to be the key to a book-level risk the
optimizer cannot see.

> 🔴 **ESCALATION — the book is 19.5% Vietnamese brokerage, not 11.4%.**
> The optimizer sees a "Brokers-other" cluster of 3.1% (VCI alone). On a look-through
> basis the real figure is **19.5%** — a 71% understatement, and ~₫263m of a ₫1,347m
> book concentrated in one industry, one margin-lending cycle and one dated event.
> Detail in §4. This is a risk-measurement failure, not a news item.

---

## 1 · Snapshot

| | |
|---|---|
| Q1/26 PBT · Q2/26 PBT | ₫1,458bn · **₫2,097bn (record)** |
| 1H/26 PBT | ₫3,555bn = **47.1%** of the ₫7,535bn plan |
| P/E TTM · P/B · ROE TTM | 20.3× · **2.49×** · 13.7% |
| Margin book | ₫44.7tn (Q1, +47% YoY) → **₫51.5tn** (Q2) |
| Margin / equity | **98%** vs the 200% regulatory ceiling |
| Corporate bond issuance share | **86%** ex-bank bonds — #1 |
| Portfolio weight | 5.5% stated · **12.2% effective** (§4) |

*Cross-check: Q1 ₫1,458bn + Q2 ₫2,097bn = ₫3,555bn, matching `tcx.actuals.h1_pbt`
exactly. Independent confirmation of a load-bearing input.*

## 2 · The business — and what it actually depends on

**Margin lending is 52% of net revenue** (₫1,211bn in Q1, +69% YoY). This is not a
diversified broker; it is a **leveraged lender to retail equity speculation** with a
brokerage attached. Revenue scales with the margin book, which scales with market
turnover and investor risk appetite.

The bond franchise is the other pillar: **86% share of corporate bond issuance**
ex-bank bonds, ₫18.6tn distributed in Q1. That is close to a monopoly on a market with a
difficult recent history (the 2022 corporate-bond crisis) and structural links to the
Masterise/Techcom development complex. Dominant share of a market that periodically
seizes is a franchise and a tail risk in the same sentence.

Funding: US$488m raised internationally — genuine, but it is wholesale funding supporting
a margin book, which is a procyclical structure.

## 3 · Valuation — the most stretched in the book

Justified P/B = (ROE − g)/(COE − g), on ROE 13.7%:

| g | COE 15% | COE 13% |
|---|---|---|
| 10% | 0.74× | 1.23× |
| 12% | 0.57× | — |

Against **2.49× traded**. Ranking the book on the identical framework:

| | ROE | Traded P/B | Justified band |
|---|---|---|---|
| MBB | 20.9% | 1.24× | 1.56–2.18× — **cheap** |
| VCI | 8.9% | 1.38× | ~0.39× — expensive |
| **TCX** | **13.7%** | **2.49×** | **0.6–1.2× — the most stretched** |

The bull case is that this framework is wrong for a fast compounder: Q2 was a record,
margin book +47%, and 98% loan-to-equity against a 200% cap is genuine capacity to nearly
double the lending book within regulation. A business growing that fast can outrun a
static justified-P/B calculation for years.

**But that is exactly the model's stated risk — "the risk is the MULTIPLE, not the
earnings" — and this dossier confirms it rather than resolving it.** At 2.49× the price
already contains the growth. The `exit_pe` band (14–22×) is unchanged; no judgment input
was moved on T5 evidence.

## 4 · The escalation: look-through broker exposure

TCB consolidates TCBS. TCBS is **19.2%** of TCB's consolidated 1H PBT (₫3,555bn of
₫18,500bn). The book holds TCB at 35%, so **6.73pp of the book is TCBS via TCB**, on top
of the 5.5% held directly.

Applying the same logic to VPB/VPBankS (14.2%, established in the VPB dossier):

| Broker | Stated | **Effective** |
|---|---:|---:|
| TCX | 5.5% | **12.23%** |
| VPX | 2.8% | **4.22%** |
| VCI | 3.1% | 3.10% |
| **Total** | **11.4%** | **19.54%** |

**The optimizer's cluster map cannot see this.** TCX is assigned to "Techcom eco" and VPX
to "VPBank eco", so brokerage appears as a 3.1% cluster. Economically, **one fifth of the
book is Vietnamese brokerage** — three companies in one industry, all levered to the same
margin cycle, all converging on the same 21 September FTSE event, at a moment when system
margin debt is at a record ₫435–454tn.

Banks ex-broker are 43.4% (TCB 28.3 + VPB 8.6 + MBB 6.5), not the 51.5% previously stated.
The book is less a bank book and more a **bank-plus-broker book** than anyone had counted.

**Recommended, NOT applied** (charter §4 — optimizer config is human-only):
1. Add a look-through **industry** exposure layer alongside the cluster map, so a
   consolidated subsidiary is counted where it economically sits.
2. Until then, treat any proposed TCX add as starting from **12.2%**, not 5.5%. The
   optimizer's +5.1pp toward a 20% north star would take effective broker exposure to
   roughly 25% of the book on a single-industry, single-event thesis.

## 5 · Risks

- **Margin cycle** — 52% of revenue from lending into a record system margin book. A
  deleveraging event compresses volume and the multiple together.
- **Bond concentration** — 86% share of a market that has seized before, with ecosystem
  counterparties.
- **The multiple itself** — at 2.49× there is no valuation support beneath the growth.
- **Correlated exit** — the same shock hits TCX, VPX, VCI *and* the parent banks. This is
  the concentration the optimizer's 0.80 same-cluster correlation understates, because
  for TCB/TCX and VPB/VPX it is consolidation, not correlation.

## 6 · Kill criteria

Existing two stand (P/B < 2.0× on unchanged earnings; no net foreign accumulation in the
4 weeks after 21 Sep). Added here:

3. **Margin-book growth stalls** — if the margin book stops growing while loan/equity
   stays near 98%, the engine driving 52% of revenue has stopped, and the multiple has no
   remaining justification.

## 7 · Decision

**Do not add on the current optimizer output.** The recommendation was generated on a
5.5% stated weight; the true starting point is 12.2%. The quality of the business is not
in question — the record quarter is real and the franchise is genuine. The question is
whether to hold a fifth of the book in one industry at the most stretched multiple in it,
ahead of a single dated event.

**Not done:** margin-book client/collateral concentration, bond warehouse composition,
the offshore facility's covenants, related-party flows with TCB and Masterise. Most sit in
the AR, which is currently unreachable.

---
*Sources: [TCBS — Q2/26 record PBT ₫2,097bn](https://www.tcbs.com.vn/tin-tuc/thong-cao-bao-chi/tcbc-tcbs-lap-ky-luc-loi-nhuan-quy-2-2026-voi-2-097-ty-dong-truoc-thue/) · [TCBS — Q1/26 PBT ₫1,458bn](https://www.tcbs.com.vn/tin-tuc/thong-cao-bao-chi/tcbc-tcbs-loi-nhuan-truoc-thue-quy-1-2026-dat-1-458-ty-dong/) · [Vietstock — margin book, US$488m raise](https://vietstock.vn/2026/04/loi-nhuan-truoc-thue-quy-12026-cua-tcbs-dat-1458-ty-dong-huy-dong-488-trieu-usd-von-quoc-te-737-1428001.htm) · [24hMoney — cycle-peak question](https://24hmoney.vn/news/tcbs-2026-loi-nhuan-7500-ty-co-may-in-tien-cua-nganh-chung-khoan-hay-da-tiem-can-dinh-chu-ky-c30a2768159.html) · [Techcombank Q1/26 press release](https://techcombank.com/content/dam/techcombank/public-site/documents/1q26-press-release-vie-vf.pdf)*
