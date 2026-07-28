# HotStock — MBB (Ngân hàng TMCP Quân đội, HOSE: MBB)

An MBB edition of the TCB HotStock package, built from the original TCB files so the
layout, typography and colour system carry over unchanged. The deck is cut from six
slides to four — see [Slide arc](#slide-arc).

| File | What it is |
|---|---|
| `HotStock_MBB_2026.docx` | Video/voiceover script — hook, three pillars, close |
| `Ngan_hang_MBB_Hotstock.pptx` | 4-slide deck (11.25" × 15" portrait), speaker notes on every slide |

## Narrative

| | Pillar | Headline |
|---|---|---|
| ① | Định giá | P/B dự phóng 2026 ~1,2x trên ROE 21,1% |
| ② | Vốn rẻ | CASA ~38% cuối 2025 — dẫn đầu hệ thống |
| ③ | Tăng trưởng | Room tín dụng 30–35%, nhóm cao nhất 2026–2028 |

## Slide arc

| # | Slide | Job |
|---|---|---|
| 1 | Cover | Ticker, thesis line, two teaser chips |
| 2 | `01 / THESIS` — Ba lý do | Three hero numbers, one per pillar |
| 3 | `02 / EARNINGS` — chart | One rising series: LNTT 2022–2026F |
| 4 | `03 / CATALYST` | Two cards: 2,1 triệu tỷ tài sản · 102.687 tỷ vốn điều lệ |

Cut from the original six: the balance-sheet chart (three bar series plus a
secondary-axis growth line — too dense to read in a scroll feed) and the
fundamentals card slide, which repeated CASA and ROE from the metrics slide.

Rules the layout follows, so it reads in one pass:

- **One idea per slide.** Each slide answers a single question; the section tag
  (`01 / THESIS`) states which.
- **Every number appears exactly once.** LNTT lives on the chart, CASA on slide 2,
  charter capital on slide 4 — no stat is repeated across slides.
- **The enumeration lives in one place.** Slide 2 owns ①②③ and those three pillars
  map 1:1 to the three sections of the voiceover script. The cover's two chips are
  deliberately unnumbered teasers so nothing is numbered twice.
- **Headlines carry the takeaway, not a description** — "LNTT gấp gần 1,8 lần chỉ
  sau 4 năm" rather than "Biểu đồ lợi nhuận".
- **Hero-number hierarchy**: 78–88pt figure → 24pt pillar label → 18pt evidence line.

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
| Vốn điều lệ | 45.340 / 52.141 / 53.063 / 80.550 → 102.687 tỷ | 2022–2026F | ✅ |
| Cổ tức 2026 | 25% (10% tiền mặt + 15% cổ phiếu) | ĐHĐCĐ 2026 | ✅ |
| Tăng trưởng tín dụng | 2025: +37% · 2026 mục tiêu 30–35% · +10% YTD tới tháng 5 | 2025–26 | ✅ |
| Giá mục tiêu | BSC 32.900 · MAS 33.300 · KBSV 33.900 · VCBS 37.230 | 2026 | ✅ |
| Q1/2026 | LNTT 9.628 tỷ (+14,8%) | Q1 2026 | ✅ |

Everything was collected from Vietnamese financial press and broker notes via web
search; direct access to HOSE, Vietstock, and broker PDFs is blocked by the build
environment's egress policy, so nothing was read from a primary filing.

### Caveats worth knowing before this goes out

- **No figure on the deck is now a projection except the two labelled as such** — LNTT
  2026F (40.726 tỷ) and the 2026 asset/capital targets. Dropping the balance-sheet chart
  also removed the modelled equity series, so the ⚠️ items are down to one.
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

## Chart

**Slide 3** keeps the template's styling, re-based to 2022–2026F. It was a 5-series
stacked P&L breakdown; MB's yearly income/cost split could not be sourced consistently,
so it is now a single clustered series — Lợi nhuận trước thuế — with data labels on.
That also suits the shorter deck: one series, one message, readable at a glance.
Restoring the stacked view needs the five income and cost lines from MB's audited P&L.

The balance-sheet chart from the six-slide version was dropped with its slide. Its
numbers survive in the slide-4 copy and speaker notes; `git show cdb24d1` has the
series if you want it back.

Brand accent `E4002B` (Techcombank red) was swapped for `1B4F9C` (MB blue) on every
slide. Revert with a single find-and-replace if you prefer the original red.

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
