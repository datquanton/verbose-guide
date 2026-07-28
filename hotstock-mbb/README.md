# HotStock — MBB (Ngân hàng TMCP Quân đội, HOSE: MBB)

An MBB edition of the TCB HotStock package, built from the original TCB files so the
layout, typography, colour system and 6-slide structure are byte-for-byte the same.

| File | What it is |
|---|---|
| `HotStock_MBB_2026.docx` | Video/voiceover script — hook, three pillars, close |
| `Ngan_hang_MBB_Hotstock.pptx` | 6-slide deck (11.25" × 15" portrait), speaker notes on every slide |

## Narrative

| | Pillar | Headline |
|---|---|---|
| ① | Định giá | P/B dự phóng 2026 ~1,2x trên ROE 21,1% |
| ② | Vốn rẻ | CASA ~38% cuối 2025 — dẫn đầu hệ thống |
| ③ | Catalyst | Room tín dụng nhóm cao nhất 2026–2028 + tăng vốn lên 102.687 tỷ |

This differs from the TCB story in one important way. TCB was pitched as *cheap versus
its own history*; MBB is not — it trades at roughly 1,4x trailing P/B, slightly **above**
its 5-year average of ~1,34x. The MBB case is growth-at-a-reasonable-price: forward P/B
compresses to ~1,2x on 2026 book, against sector-leading ROE and a credit-growth quota
nobody else has. The deck and script are written on that basis, not on a discount claim.

## Figures used

Verification status: ✅ confirmed by ≥2 independent sources · ⚠️ single source or
partly modelled.

| Metric | Value | Period | |
|---|---|---|---|
| P/B trailing | 1,39x (08/07/2026); ~1,42x vs 5-yr avg 1,34x | Q3 2026 | ✅ |
| P/B forward 2026 | ~1,2x | 2026F | ✅ |
| ROE | 21,1% (MB công bố); 21,57% theo nguồn thứ ba | 2025 | ✅ |
| CASA | ~38%, dẫn đầu bảng xếp hạng cả năm | cuối 2025 | ⚠️ |
| LNTT | 22.729 / 26.306 / 28.829 / 34.268 tỷ | 2022–2025 | ✅ |
| LNTT 2026F | 40.726 tỷ (+18,8%, MAS) — kế hoạch ĐHĐCĐ 39.400 tỷ (+15–20%) | 2026F | ✅ |
| Tổng tài sản | 728.532 / 944.954 / 1.133.797 / **1.615.764** tỷ | 2022–2025 | ✅ |
| Tổng tài sản 2026F | mục tiêu >2,1 triệu tỷ (kế hoạch +~28%) | 2026F | ✅ |
| Vốn chủ sở hữu | 79.613 / 96.711 / 118.356 tỷ | 2022–2024 | ⚠️ |
| Vốn chủ sở hữu | 144.549 tỷ (2025) / 175.134 tỷ (2026F) — dự phóng | 2025–26F | ⚠️ |
| Vốn điều lệ | 45.340 / 52.141 / 53.063 / 80.550 → 102.687 tỷ | 2022–2026F | ✅ |
| Cổ tức 2026 | 25% (10% tiền mặt + 15% cổ phiếu) | ĐHĐCĐ 2026 | ✅ |
| Tăng trưởng tín dụng | 2025: +37% · 2026 mục tiêu 30–35% · +10% YTD tới tháng 5 | 2025–26 | ✅ |
| Giá mục tiêu | BSC 32.900 · MAS 33.300 · KBSV 33.900 · VCBS 37.230 | 2026 | ✅ |
| Q1/2026 | LNTT 9.628 tỷ (+14,8%) | Q1 2026 | ✅ |

Everything was collected from Vietnamese financial press and broker notes via web
search; direct access to HOSE, Vietstock, and broker PDFs is blocked by the build
environment's egress policy, so nothing was read from a primary filing.

### Caveats worth knowing before this goes out

- **Vốn chủ sở hữu 2025 (144.549 tỷ) and 2026F (175.134 tỷ) are broker projections**, not
  reported figures. They cross-check against reported ROE of 21,1% and 2024 equity of
  118.356 tỷ, but reconcile them with MB's audited statements before publishing. The 2022
  equity-growth bar (27,4%) is derived using a 2021 equity base of ~62.486 tỷ.
- **CASA leadership is a narrow, recently-regained lead.** MB tops the full-year 2025
  ranking at ~38%, but at 9M2025 Techcombank was ahead (38,4% vs MB 36,8%). Both were
  above 34% at year-end. "Cao nhất hệ thống" is defensible for FY2025; it is not a
  durable multi-year gap.
- **Q1/2026 was soft on the balance sheet** and the deck does not show this. Total assets
  slipped ~0,3% (-4.500 tỷ) versus end-2025 and customer deposits fell ~1,7%
  (-15.500 tỷ), even as loans grew 3,4% and profit hit a record. If the audience is
  likely to raise it, address it rather than let the "bứt tốc" framing carry unchallenged.
- MB's early-January release guided to "gần 1,5 triệu tỷ, tăng 33%" in total assets for
  2025. The final figure was **1.615.764 tỷ, +43%**. Ignore the earlier estimate — it is
  still circulating in secondary coverage.

## Charts

Both charts keep the template's styling and were re-based to 2022–2026F:

- **Slide 3** — Tổng tài sản + Vốn chủ sở hữu (cột) with Tăng trưởng VCSH % (đường).
  The hidden Vốn Điều Lệ series carries the charter-capital path.
- **Slide 5** — was a 5-series stacked P&L breakdown; MB's yearly income/cost split could
  not be sourced consistently, so it is now a single clustered series, Lợi nhuận trước
  thuế, with data labels on. Restoring the stacked view needs the five income and cost
  lines from MB's audited P&L.

Brand accent `E4002B` (Techcombank red) was swapped for `1B4F9C` (MB blue) across all six
slides. Revert with a single find-and-replace if you prefer the original red.

## Rebuilding

The scripts edit the original TCB files in place rather than regenerating them, so every
shape offset survives. Unpack the two TCB source files next to the scripts first:

```bash
mkdir tcb_pptx && (cd tcb_pptx && unzip -q ../Ngan_hang_TCB_Hotstock.pptx)
mkdir tcb_docx && (cd tcb_docx && unzip -q ../HotStock_TCB_2026.docx)
python3 scripts/build_pptx.py     # -> Ngan_hang_MBB_Hotstock.pptx
python3 scripts/build_docx.py     # -> HotStock_MBB_2026.docx
```

Each script asserts that every string it expects to replace was found exactly once and
fails loudly otherwise, so a template change cannot silently leave TCB copy behind.
To retarget the package at VPB instead, edit the replacement tables at the top of each
script — the layout logic needs no changes.
