# HotStock — MBB (Ngân hàng TMCP Quân đội, HOSE: MBB)

| File | What it is |
|---|---|
| `HotStock_MBB_2026.docx` | Video/voiceover script — hook, three pillars, close |
| `Ngan_hang_MBB_Hotstock.pptx` | 4-slide deck (11.25" × 15" portrait) |

The deck is built on the **FRT HotStock research-note template**, not the TCB one.
The script `.docx` is still built from the TCB script file, which is where that
document's styles live.

## Slide arc

The FRT template's house style is one chart plus one takeaway headline per slide,
under a running report title. Four of its ten slides are kept and repointed at MBB:

| # | FRT source | Content | Takeaway headline |
|---|---|---|---|
| 1 | slide 1 | Tổng tài sản 2022–2026F | Tổng tài sản tăng 43% trong năm 2025 và hướng tới mốc 2,1 triệu tỷ đồng |
| 2 | slide 7 | Lợi nhuận trước thuế 2022–2026F | LNTT gấp gần 1,8 lần chỉ sau 4 năm, dự phóng vượt 40.000 tỷ đồng |
| 3 | slide 8 | Vốn điều lệ 2022–2026F | Vốn điều lệ tăng hơn gấp đôi sau 4 năm, tạo dư địa cho tín dụng tăng 30–35% |
| 4 | slide 9 | Bảng luận điểm & định giá | Định giá dự phóng 2026 lùi về ~1,2 lần P/B trong khi ROE vẫn trên 21% |

Running title on every slide: **Vốn rẻ dẫn đầu, tăng trưởng vượt trội**.

The arc mirrors FRT's own: scale → profit → the structural driver → valuation.
Slides 1–3 carry one number each and let the chart do the arguing; slide 4 closes
with the three numbered pillars, which map 1:1 to the three sections of the
voiceover script.

Charts trimmed to a single series each. The template's originals were stacked
segment breakdowns; MB's equivalent splits (income/cost lines, CASA by bank)
could not be sourced consistently, and a single rising series is the more legible
choice for a scroll feed anyway. The consequence is that slides 1–3 share one
chart form — deliberate here, but if you later source a multi-series breakdown,
slide 1 or 3 is the one to vary.

## Figures used

Verification status: ✅ confirmed by ≥2 independent sources · ⚠️ single source.

| Metric | Value | Period | |
|---|---|---|---|
| P/B trailing | 1,39x (08/07/2026); vs 5-yr avg 1,34x | Q3 2026 | ✅ |
| P/B forward 2026 | ~1,2x | 2026F | ✅ |
| ROE | 21,1% (MB công bố); 21,57% theo nguồn thứ ba | 2025 | ✅ |
| CASA | ~38%, dẫn đầu bảng xếp hạng cả năm | cuối 2025 | ⚠️ |
| LNTT | 22.729 / 26.306 / 28.829 / 34.268 tỷ | 2022–2025 | ✅ |
| LNTT 2026F | 40.726 tỷ (+18,8%, MAS) — kế hoạch ĐHĐCĐ 39.400 tỷ | 2026F | ✅ |
| Tổng tài sản | 728.532 / 944.954 / 1.133.797 / **1.615.764** tỷ | 2022–2025 | ✅ |
| Tổng tài sản 2026F | mục tiêu >2,1 triệu tỷ (kế hoạch +~28%) | 2026F | ✅ |
| Vốn điều lệ | 45.340 / 52.141 / 53.063 / 80.550 → 102.687 tỷ | 2022–2026F | ✅ |
| Cổ tức 2026 | 25% (10% tiền mặt + 15% cổ phiếu) | ĐHĐCĐ 2026 | ✅ |
| Tăng trưởng tín dụng | 2025: +37% · 2026 mục tiêu 30–35% · +10% YTD tới tháng 5 | 2025–26 | ✅ |
| Giá mục tiêu | BSC 32.900 · MAS 33.300 · KBSV 33.900 · VCBS 37.230 | 2026 | ✅ |

Chart values are in **nghìn tỷ đồng**, matching the template's unit caption.

Everything was collected from Vietnamese financial press and broker notes via web
search; direct access to HOSE, Vietstock, and broker PDFs is blocked by the build
environment's egress policy, so nothing was read from a primary filing.

### Caveats worth knowing before this goes out

- **CASA leadership is a narrow, recently-regained lead.** MB tops the full-year 2025
  ranking at ~38%, but at 9M2025 Techcombank was ahead (38,4% vs MB 36,8%). Both were
  above 34% at year-end. "Dẫn đầu hệ thống" is defensible for FY2025; it is not a
  durable multi-year gap.
- **Q1/2026 was soft on the balance sheet** and the deck does not show it. Total assets
  slipped ~0,3% (-4.500 tỷ) versus end-2025 and customer deposits fell ~1,7%
  (-15.500 tỷ), even as loans grew 3,4% and profit hit a record. If the audience is
  likely to raise it, address it rather than let the growth framing carry unchallenged.
- MB's early-January release guided to "gần 1,5 triệu tỷ, tăng 33%" in total assets for
  2025. The final figure was **1.615.764 tỷ, +43%**. Ignore the earlier estimate — it is
  still circulating in secondary coverage.
- **The deck has no speaker notes.** The FRT template carried none on the slides used,
  and the `.docx` script is the narration of record.
- **The charts' embedded workbooks are still FRT's.** Cached values drive what renders,
  so the slides are correct, but "Edit Data" in PowerPoint opens the template's original
  worksheet. Relink or replace those workbooks if anyone needs to edit the charts
  in place.

## Rebuilding

The scripts edit the source files in place rather than regenerating them, so every
shape offset survives. Unpack the two source files next to the scripts first:

```bash
mkdir frt && (cd frt && unzip -q ../Hot_stock_FRT_2026.pptx)
mkdir tcb_docx && (cd tcb_docx && unzip -q ../HotStock_TCB_2026.docx)
python3 scripts/build_pptx.py     # FRT template -> Ngan_hang_MBB_Hotstock.pptx
python3 scripts/build_docx.py     # TCB script   -> HotStock_MBB_2026.docx
```

`build_pptx.py` does structural work first (keep and reorder four slides, then
`clean.py` sweeps the orphaned slides, charts, notes, embeddings and themes), then
text, then charts and the table. Every replacement is asserted to match exactly
once and the build fails loudly otherwise, so a template change cannot silently
leave FRT copy behind. Table cells are addressed positionally — several template
cells share identical text, so a text-keyed lookup would overwrite the wrong ones.

To retarget the package at VPB, edit the replacement tables and the data constants
at the top of each script; the layout logic needs no changes.

### Earlier versions

`git log` has two prior takes, both on the TCB template: a 6-slide edition
(`cdb24d1`, with a second balance-sheet chart) and a 4-slide cut of it (`0e9005e`,
hero-number cards plus one chart).
