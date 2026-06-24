# Daily MAS report automation

Generates the **"Good Morning Vietnam"** daily report (`Daily_MAS_YYYYMMDD.docx`)
from the Bloomberg-updated workbook, filling your existing Word template. Runs
locally on your PC, where Excel / fireant.vn / dstock all work in your session.

## What it automates

| Piece | Status | Source |
|---|---|---|
| Worded market commentary (3 paras) | ✅ this package | workbook numbers + a one-line news driver |
| VN30 valuation table | ✅ this package | `Dashboard` sheet |
| OHLC + DoD metrics, Close | ✅ this package | `Foreign trading` sheet |
| Short news (3 items) | ⏳ next | web search |
| 6 indicator charts | ⏳ next | `Dashboard` chart data |
| Technical trend views | ⏳ next | rule or manual |

The numbers are read **deterministically** from the workbook — the model never
invents a figure; it only writes the prose around them.

## Why these inputs

Your manual fireant/dstock steps mostly re-key data that already lands in the
`.xlsm` (the `Foreign trading` sheet even pre-writes the OHLC and liquidity
sentences). So the workbook is the single source of truth: keep typing the few
intraday cells Bloomberg is late on, and everything downstream is derived.

## Setup (Windows / PowerShell)

```powershell
py -m pip install -r mas_report\requirements.txt
# optional — for full house-voice commentary instead of the deterministic draft:
setx ANTHROPIC_API_KEY "sk-ant-..."
```

## Run

```powershell
py -m mas_report.run `
   --xlsm "C:\path\Daily_data2025_Aug_updated.xlsm" `
   --template "C:\path\Daily_MAS_template.docx" `
   --news "LPB locked limit-up after Vingroup Chairman Pham Nhat Vuong bought 146.2mn LPB shares (4.8%)."
```

Produces `Daily_MAS_<date>.docx`. The `--news` line is the one judgement call
left to you each morning (the session's driver); omit it and the commentary
still builds from the numbers.

## Individual steps (for debugging)

```powershell
py -m mas_report.extract data.xlsm -o report_data.json
py -m mas_report.commentary report_data.json --news "..." -o commentary.json
py -m mas_report.fill_docx template.docx report_data.json commentary.json -o out.docx
```

## Schedule it

Windows Task Scheduler → daily at e.g. 07:30, action:
`py -m mas_report.run --xlsm ... --template ...` with **Start in** set to this
folder. (Make sure the workbook has refreshed from Bloomberg first.)

## Roadmap

1. **Short news** — web-search + summarize the 3 macro items with sources.
2. **Charts** — rebuild the 6 indicator charts (matplotlib) from the sheet.
3. **Technical view** — carry-forward S/R + a simple trend rule.
4. **Delivery** — auto-create a Gmail draft / drop into Drive.
