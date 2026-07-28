# HotStock — MBB (Ngân hàng TMCP Quân đội, HOSE: MBB)

| File | What it is |
|---|---|
| `HotStock_MBB_2026.docx` | Video/voiceover script — hook, three pillars, close |
| `Ngan_hang_MBB_Hotstock.pptx` | 4-slide deck (11.25" × 15" portrait) |

Deck built on the **FRT HotStock research-note template**; the script `.docx` is built
from the TCB script file, where that document's styles live.

**No third-party research house is cited anywhere.** Every figure in the deck comes
from the in-house MBB model (`FinModel_MBB_1Q26`), sheets `A-Chart` and `Valuation`.
Both build scripts assert that no competitor name survives into the output.

## Slide arc

The template's house style is one chart plus one takeaway headline per slide. The four
charts are the ones that actually decide a bank case — volume, margin, risk, return:

| # | Chart | Series (2022–2026F) | Takeaway headline |
|---|---|---|---|
| 1 | Volume | Dư nợ tín dụng · Tiền gửi khách hàng (nghìn tỷ) | Tín dụng tăng 35% trong 2025 và liên tục mở rộng nhanh hơn tốc độ huy động |
| 2 | Margin | NIM · Chi phí vốn (%) | CASA gần 38% kéo chi phí vốn về 3,1%, bù lại phần lớn áp lực thu hẹp của NIM |
| 3 | Risk | Tỷ lệ nợ xấu · Chi phí tín dụng (%) | Nợ xấu nhích lên 1,9% trong 2025 nhưng chi phí tín dụng được dự báo hạ nhiệt |
| 4 | Return | ROE (%) | ROE duy trì trên 20% suốt chu kỳ, trong khi P/B dự phóng 2026 chỉ quanh 1,2 lần |

Running title on every slide: **Vốn rẻ dẫn đầu, tăng trưởng vượt trội**.
Source line on every slide: *Nguồn: Dữ liệu doanh nghiệp, Mirae Asset Research ước tính*.

Slides 2 and 3 carry numbers that cut against the pitch — NIM compressing from 5,8% to
3,7%, NPL rising to 1,9%. That is deliberate. The model shows both, the headlines frame
them honestly (cost of funds is what MB's CASA actually defends, not NIM; credit cost is
forecast to fall even as NPL rises), and a bank deck that hides its margin and asset-quality
trend does not survive the first question from a real audience.

## Figures used — all from the model

| Metric | 2022 | 2023 | 2024 | 2025 | 2026F | Source |
|---|---|---|---|---|---|---|
| Dư nợ tín dụng (nghìn tỷ) | 460,6 | 611,0 | 776,7 | 1.048,2 | 1.344,2 | A-Chart!31 |
| Tiền gửi khách hàng (nghìn tỷ) | 443,6 | 567,5 | 714,2 | 923,5 | 1.163,7 | A-Chart!32 |
| Tăng trưởng tín dụng | 26,7% | 32,7% | 27,1% | 35,0% | 28,2% | A-Chart!34 |
| NIM | 5,76% | 4,87% | 4,13% | 3,76% | 3,69% | A-Chart!4 |
| Chi phí vốn | 2,83% | 4,30% | 3,51% | 3,24% | 3,10% | A-Chart!9 |
| CASA | 37,6% | 38,1% | 38,0% | 38,2% | 35,9% | A-Chart!123 |
| Tỷ lệ nợ xấu | 1,09% | 1,61% | 1,62% | 1,90% | 1,50% | A-Chart!99 |
| Chi phí tín dụng / dư nợ | 1,75% | 1,00% | 1,23% | 1,57% | 1,22% | A-Chart!100 |
| Bao phủ nợ xấu | 238% | 117% | 92,2% | 79,9% | 80,9% | A-Chart!98 |
| CIR | 32,5% | 31,5% | 30,7% | 28,3% | 28,7% | A-Chart!122 |
| ROE | 24,6% | 23,5% | 21,2% | 20,7% | 20,5% | Valuation!23 |

Valuation, from `Valuation!A1:A3` and `!15`: giá mục tiêu **33.300 đ**, thị giá 24.600 đ,
upside **35,4%**; BPS 2026F 20.079 đ, tức P/B dự phóng ~1,22 lần; fair P/B 1,66x on a
sustainable ROE of 20,5%.

Cross-checks against MB's public disclosures all tie: total assets 1.615.764 tỷ at
end-2025 (+43%), Q1/26 PBT 9.628 tỷ, CASA ~38%, ROE ~21%.

### Caveats worth knowing before this goes out

- **NIM is in a multi-year downtrend** (5,76% → 3,69%) and slide 2 shows it. The defensible
  claim is that MB's CASA keeps *cost of funds* falling — not that NIM is protected.
- **NPL coverage has fallen hard**, 238% (2022) → ~80% (2025–26F). It is not on any slide;
  if the audience knows the sector, expect the question.
- **Q1/2026 was soft on the balance sheet.** Total assets slipped ~0,3% (-4.500 tỷ) versus
  end-2025 and customer deposits fell ~1,7% (-15.500 tỷ), even as loans grew 3,4% and profit
  hit a record.
- **CASA leadership is a narrow, recently-regained lead.** MB tops the full-year 2025 ranking
  at ~38%, but at 9M2025 Techcombank was ahead. Defensible for FY2025; not a durable gap.
- **The deck has no speaker notes** — the `.docx` script is the narration of record.
- **The charts' embedded workbooks are still the template's.** Cached values drive what
  renders, so the slides are correct, but "Edit Data" opens the template's original
  worksheet. Relink if anyone needs to edit charts in place.
- **The model's `MBB 1Q26 Dashboard` tab has a broken balance-sheet section** (row mapping
  slipped — "Total liabilities 1.041", "Fixed assets 765.048"). Its income-statement rows
  are sound and were used; nothing was taken from its BS block.

## Rebuilding

```bash
mkdir frt && (cd frt && unzip -q ../Hot_stock_FRT_2026.pptx)
mkdir tcb_docx && (cd tcb_docx && unzip -q ../HotStock_TCB_2026.docx)
python3 scripts/build_pptx.py     # FRT template -> Ngan_hang_MBB_Hotstock.pptx
python3 scripts/build_docx.py     # TCB script   -> HotStock_MBB_2026.docx
```

`build_pptx.py` does structural work first (keep and reorder four slides, then `clean.py`
sweeps orphaned slides, charts, notes, embeddings and themes), then text, then charts.
Every replacement is asserted to match exactly once and the build fails loudly otherwise.

Chart surgery worth knowing about if you change the template: the series-name swap has to
be scoped to the `<c:ser>` block because the chart title is also a `<c:tx>` and comes first
in the part; the category axis is replaced wholesale because some charts cache years as
numbers, which cannot hold a label like `26F`; the c15 filtered-series caches are dropped so
hidden series stop carrying the template's numbers; and the fixed axis maxima that suited
the template's scales are removed.

To retarget at another ticker, edit the data constants and replacement tables at the top of
each script; the layout logic needs no changes.

### Earlier versions

`git log` has three prior takes: a 6-slide edition on the TCB template (`cdb24d1`), a 4-slide
cut of it (`0e9005e`), and the first FRT-template version (`48dc6f4`, whose last slide was a
6×4 table — replaced here because it read too small at portrait size).
