# VCI — Research Dossier

**Status:** S1 quick screen complete (depth-queue item 4) · 2026-07-26
**Why now:** last held name with no screen. Held at 3.1%, behind plan, and the optimizer
wants to **add** +3.1pp. This screen concludes the add should be suspended, and found a
defect in the model input that helped generate it.

> ⚠ **ESCALATION (trigger 3): VCI's market-cap input fails its own mandated cross-check
> by 25.2%, and correcting it flips expected return from +7.0% to −7.5% — a 14.5pp
> swing.** Detail in §4. No number was changed on inference; confidence lowered and the
> input flagged for resolution against a primary source.

---

## S1 · Quick screen

### 1. What does it sell?

Four engines, and they are pulling in different directions:

| Engine | Q2/26 state |
|---|---|
| **Institutional brokerage** | **#1 in Vietnam, >28% share** — the franchise |
| Retail brokerage | 4th on HOSE, ~7% share |
| Margin lending | ₫16,644bn book; **0.97× equity vs a 2.0× regulatory cap** |
| Proprietary book | **Losing** — >₫430bn unrealised on FPT, MWG and KDH |

Q2: PBT ₫270.8bn (+28% YoY), NPAT ₫250.6bn (+36%), but **revenue roughly flat**, operating
cash flow **negative and funded by borrowings**, and the prop book underwater.

**The composition matters more than the growth rate.** A +36% headline built on flat
revenue, negative OCF and a losing prop book is not the same +36% as one built on fees.

### 2. Sequential deterioration the YoY number hides

1H NPAT-MI ₫591bn less Q2 ₫251bn implies **Q1 ₫340bn** — which matches the separately
reported ₫341bn, so the split is sound.

**Q2 ₫251bn vs Q1 ₫340bn = −26% quarter-on-quarter.** Every headline reports "+36%".
Both are true; only one is informative about direction. This is the single most useful
thing on this page and it does not appear in any of the coverage.

### 3. Who controls it?

Chairwoman **Nguyễn Thanh Phượng** holds 30.8m shares (2.68% directly). Founded 2007 as
VCSC, listed on HOSE 2017.

**Headline-vs-substance check:** press reported that "the fund chaired by Nguyễn Thanh
Phượng registered to divest its entire VCI stake." The holding was **135,000 shares** —
roughly 0.01% of the company, about ₫2.8bn. That is noise dressed as an ownership
signal. Recorded here so it is not mistaken for one later.

### 4. Valuation — and a defect in our own input

Trades at **P/E 17.2×, P/B 1.38×, ROE TTM 8.9%** — the most expensive earnings and the
lowest returns in the book simultaneously.

**Justified P/B = (ROE − g)/(COE − g).** With ROE 8.9% against a ~15% cost of equity, the
numerator is far below the denominator at any sensible g:

| g | COE 15% |
|---|---|
| 5% | **0.39×** |
| 8% | 0.13× |

Against 1.38× traded. **A business earning 8.9% on equity while its owners require ~15%
destroys value every year it persists**, and no multiple rescues that. Compare MBB in the
same framework: 20.9% ROE, 1.24× book, justified 1.56–2.18×. The two names sit at
opposite ends of the same calculation, and the book currently holds both.

**The honest caveat:** brokers are violently cyclical and 8.9% may be a trough ROE. In a
bull market this franchise has earned far more. But that reframes rather than rescues the
thesis — the bull case *requires* a large ROE recovery, so it is a cyclical timing bet on
the FTSE flow event, not an investment in a compounding business. That is a legitimate
position to hold; it is not the position the model thinks it holds.

**The input defect.** `assumptions.json` carries `npat_ttm 1,100` for VCI, giving a market
cap of ₫18,920bn. Cross-checking off the balance sheet: margin book ₫16,644bn at 0.97×
equity implies equity ≈ **₫17,159bn**; at P/B 1.38× that is a market cap of **₫23,679bn**.

| Route | Market cap | Implied npat_ttm |
|---|---|---|
| `pe_ttm × npat_ttm` (in file) | ₫18,920bn | 1,100 |
| `P/B × implied equity` | ₫23,679bn | 1,377 |
| **Gap** | **+25.2%** | — |

The `_npat_ttm_method` note in `assumptions.json` mandates that these agree within ~5%.
They do not. The 1,100 was an early rough estimate, and the balance-sheet route is better
evidenced. On the corrected cap, VCI's expected return goes **+10.7% → −11.5% raw**, and
**+7.0% → −7.5% shrunk**.

**No number was changed on this.** Two conflicting derivations do not make a third
inferred number true, and `npat_ttm` should be set from a filing, not from arithmetic on
press figures. What *was* changed: **confidence 0.65 → 0.45**, which is permitted on any
evidence tier and is plainly warranted once a load-bearing input is known to be suspect.

### 5. Red flags

- [x] **Prop book losing ₫430bn** on FPT, MWG, KDH — note it is long KDH, which we also own
- [x] **Negative operating cash flow funded by borrowings** — an earnings-quality flag
- [x] **1H at 29–30% of a ₫2,300bn PBT plan** targeting +41%; H2 must deliver ~70%
- [x] Stock at a **3-year low** despite rising reported profit — the market is pricing the composition, not the headline
- [ ] Inspectorate / SSC actions — not checked
- [x] Margin book at 0.97× equity vs the 2.0× cap — **genuine headroom**, the strongest bull point

### 6. Liquidity

Mid-cap, adequately liquid; a 3.1% position is not size-constrained.

---

## Gate: the two-sentence test

> **The market believes** VCI is a value-destroying broker — 8.9% ROE against a ~15%
> cost of equity — whose reported growth is flattered by a weak base, and has marked it
> to a three-year low.
>
> **I might believe** the institutional franchise (>28% share, #1) is a genuinely scarce
> asset ahead of the 21 September FTSE upgrade, and that margin capacity at 0.97× versus
> a 2.0× cap is real optionality if flows arrive.

**Passes S1 — narrowly, and as an event position only.** The variant view exists but it is
a dated, single-catalyst bet, not a franchise investment. It should be sized as such.

## What would prove me wrong

1. 9M PBT below 55% of the FY target (already an armed kill criterion)
2. No institutional/foreign market-share gain through the FTSE event
3. ROE fails to recover above ~12% in a rising market — then it is structural, not cyclical

## Recommendation to the CIO run

1. **Suspend the +3.1pp add** until `npat_ttm` is resolved from a filing. The add was
   partly generated by an input that fails its own cross-check.
2. Resolve `npat_ttm` from the Q2 statements — share count and equity, primary source.
3. If the balance-sheet route is confirmed, VCI's expected return is **negative** and it
   becomes a trim candidate, not an add.

**Not done:** inspectorate history, IB pipeline detail, prop-book full composition,
5-year ROE series, the by-hand 8-quarter table.

---
*Sources: [Doanh nghiệp Hội nhập — 29% of plan](https://doanhnghiephoinhap.vn/vietcap-moi-hoan-thanh-29-ke-hoach-loi-nhuan-sau-nua-nam-143926.html) · [Vietstock — Q2 brokerage & lending](https://vietstock.vn/2026/07/moi-gioi-va-cho-vay-tich-cuc-vci-tang-lai-36-trong-quy-2-737-1471007.htm) · [Kinh doanh Net — margin, negative OCF](https://kinhdoanhnet.vn/margin-keo-loi-nhuan-vietcap-tang-36-dong-tien-am-duoc-bu-dap-bang-vay-no-a80035.html) · [Doanh Nhân VN — prop-book losses](https://baomoi.com/vietcap-tam-lo-tu-doanh-hon-430-ty-dong-tu-fpt-mwg-kdh-du-lai-sau-thue-tang-36-trong-quy-ii-c55667033.epi) · [VietnamBiz — HOSE Q2 market share](https://vietnambiz.vn/thi-phan-moi-gioi-hose-quy-ii2026-ssi-tang-nhe-vpbanks-cao-ky-luc-4-ctck-lon-lien-tiep-cung-sut-giam-202676163432428.htm) · [Stockbiz — 3-year low](https://stockbiz.vn/tin-tuc/loi-nhuan-tang-tu-van-nhieu-thuong-vu-ipo-co-phieu-vietcap-van-lao-doc-ve-day-3-nam/41014732) · [Doanh nhân & Pháp luật — fund divestment](https://doanhnhan.baophapluat.vn/quy-lien-quan-chu-tich-nguyen-thanh-phuong-dang-ky-thoai-toan-bo-von-tai-chung-khoan-vci.html)*
