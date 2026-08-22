# VPB — Research Dossier

**Status:** sum-of-parts complete (depth-queue item 7) · 2026-07-26
**Why now:** VPB is 10% of the book, and the model has been carrying a sensitivity note
that this analysis shows is attributed to the wrong entity.

---

## 1 · The sum of the parts (1H/2026 PBT)

| Segment | 1H PBT (₫bn) | % of consolidated |
|---|---:|---:|
| **Parent bank** | 15,567 | **82.5%** |
| **VPBankS (= VPX)** | 2,673 | **14.2%** |
| GPBank | 730 | 3.9% |
| OPES (insurance) | 613 | 3.2% |
| **FE Credit** | **153** | **0.8%** |
| Sum of parts | 19,736 | 104.5% |
| **Consolidated** | **18,880** | 100% |
| Eliminations / holding costs | −856 | −4.5% |

*Cross-check: the VPBankS line (₫2,673bn) matches `vpx.actuals.h1_pbt` in
`assumptions.json` exactly — two independently sourced routes agreeing, which is the
best evidence available that both are right.*

## 2 · Finding 1 — the model's stated sensitivity is mis-attributed

`run.py` prints, for VPB: *"each +0.2% of credit cost ≈ −₫2.3tn PBT — **FE Credit NPL
formation is the swing factor**."*

The **₫2.3tn is right** (0.2% × ~₫1,150tn of credit). The **attribution is wrong**, and
badly so. FE Credit now contributes **0.8%** of consolidated profit — ₫153bn out of
₫18,880bn. It cannot be the swing factor for anything. The press framing is blunt about
the reversal: from "golden goose" to the smallest link in the ecosystem.

**The credit risk did not go away — it moved.** It now sits in the **parent bank's own
book**, which has grown credit +24.6% year-to-date and passed ₫1 quadrillion. That is a
different risk with different drivers: it is corporate and mortgage underwriting into a
fast expansion, not consumer-finance delinquency.

Watching FE Credit's NPL formation as the VPB risk indicator would have been monitoring a
0.8% segment while the actual exposure grew elsewhere. **This is the most useful thing in
this dossier** — a live monitoring instruction that was pointed at the wrong place.

## 3 · Finding 2 — the VPB/VPX overlap is ownership, not correlation

VPB's consolidated earnings **already contain** VPBankS. The book holds both:

| | |
|---|---|
| VPX held directly | 2.80% |
| VPX inside the 10.0% VPB position (14.2% of its PBT) | +1.42pp |
| **Effective VPX exposure** | **4.22%** |
| vs stated | **+51%** |

The optimizer treats VPB and VPX as two assets with a correlation of 0.80 (same cluster).
That is the wrong model of the relationship. **They are not two correlated things; one
contains the other.** Correlation can fall in a crisis; a consolidation line cannot.

The "VPBank eco" cluster at 12.8% is not itself wrong, but the *reason* it is a cluster is
stronger than the correlation assumption implies. Worth noting the same structure exists
on the other side of the book: TCB consolidates TCBS, and the portfolio holds TCB (35%)
and TCX (5.5%) too. **Both clusters are ownership overlaps, not thematic ones.**

Recommended but **not applied**: raise `corr_same_cluster` for parent/subsidiary pairs
toward ~0.95, or net out the look-through. Changing the optimizer's correlation config is
explicitly forbidden to an automated run (charter §4) — an agent that can widen its own
constraints has none. Flagged for the CIO run.

## 4 · Finding 3 — the weak-bank transfer is contributing, not dragging

**GPBank earned ₫730bn in 1H — already ~1.5× its full-year 2025 result.** The standing
assumption about compulsory transfers is that they are a cost absorbed for regulatory
favour. Here it is positive within eighteen months.

**Read-across to MBB:** the MBB S1 screen written earlier today argued that MBB's ROE
erosion is the *price* of the MBV/OceanBank transfer. VPB's experience is evidence that
the price can be smaller than assumed and can turn positive quickly. That strengthens the
MBB variant view — and it was reached from a different company, which is the kind of
cross-read the dossier programme exists to produce.

## 5 · What this does to the thesis

VPB is **82.5% a conventional bank** plus a genuinely good securities arm. The "complex
conglomerate with a consumer-finance problem" framing is out of date:

- FE Credit is no longer material either way — neither the risk nor the recovery story
- The FY26 plan (₫41.6tn) leaning on VPBankS is confirmed: VPX is 14.2% of profit and grew 3×
- 1H PBT ₫18,880bn against the ₫41.6tn target = 45.4%, needing a stronger H2
- The model's base case (₫30.7tn) sits well below the target, and nothing here changes that

**No change to `exit_pe` or `probs`** — those are judgment inputs and this is T5 evidence
(charter §2). The segment data is a fact about composition, not about value.

## 6 · Open

Segment *balance sheets* (not just P&L), FE Credit's NPL levels now that its P&L is
immaterial, GPBank consolidation terms, the ₫250m foreign placement pricing, SMBC board
representation, and the by-hand 8-quarter series. The AR is the source for most of it and
is currently unreachable — see the queue.

---
*Sources: [Tin nhanh chứng khoán — FE Credit ₫152.6bn](https://m.tinnhanhchungkhoan.vn/vpbank-vpb-fe-credit-dong-gop-1526-ty-dong-loi-nhuan-post394348.amp) · [CafeBiz — FE Credit from golden goose to smallest link](https://cafebiz.vn/cuoc-doi-ngoi-trong-he-sinh-thai-vpbank-fe-credit-tu-ga-de-trung-vang-thanh-mat-xich-nho-nhat-176260721090138062.chn) · [Phụ Nữ VN — segment drivers](https://baomoi.com/mang-kinh-doanh-nao-giup-vpbank-lap-dinh-loi-nhuan-c55638144.epi) · [Chính phủ — credit past ₫1 quadrillion](https://baochinhphu.vn/vpbank-vuot-moc-1-trieu-ty-dong-tin-dung-trong-quy-i-2026-102260417144906691.htm) · [VPBank IR](https://www.vpbank.com.vn/tin-tuc/thong-cao-bao-chi/2026/vpbank-duy-tri-tang-truong-manh-me-trong-quy-i2026-quy-mo-tin-dung-vuot-1-trieu-ty-dong)*
