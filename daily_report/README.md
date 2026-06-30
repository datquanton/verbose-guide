# Daily Report automation — Good Morning Vietnam (Mobile EN)

Automates turning the daily **MAS Word report** + market data into the updated
**`DailyReport_Mobile_EN` PowerPoint** deck — text, tables **and** charts —
with no Microsoft Office and no network-share access required.

## How the deck is wired (why this is the approach)

| Part of the deck | Source | How it's updated |
|---|---|---|
| Theme, OHLC table, VN-Index row, narrative, liquidity line, VN30 lists, trading value, foreign flow, short news | the **Word `.docx`** (text + tables) | `python-pptx`, run-level text edits (formatting preserved) |
| 6 charts (contributors, foreign flows, P/E band, VN vs US$/VND, bond yields, interbank) | a **market-data feed** | chart **cache XML** rewritten directly (`lxml`) |

The charts are **native PowerPoint charts**, but their data is **OLE-linked to an
external workbook**:

```
\\10.0.16.23\mas\Department\Reseach\6.Daily Report\Daily data-2025_Aug_updated.xlsm
```

The deck stores a *cached* copy of each chart's series for display. Because the
link is external, `python-pptx`'s `chart.replace_data()` fails — so this tool
edits the cached `<c:cat>`/`<c:val>` values in the chart XML instead. That makes
chart updates work **headlessly** (server/cron/cloud), independent of the share.

## The one real dependency: where do the chart numbers come from?

The Word report only contains the **text/table** data. The **chart series**
(time-series of P/E, yields, interbank, FX, index; per-ticker contribution and
foreign flows) need a data feed. Three options, swappable via `--chart-source`:

- **`fiinquant`** — pull from the **FiinQuant** connector (VN market data: index,
  foreign flows, valuations/P-E, bond yields, interbank, FX). *Most hands-off.*
  ⚠️ Authorize the FiinQuant connector first (claude.ai connector settings, or
  `/mcp` in an interactive Claude Code session), then wire `FiinQuantProvider`
  in `chart_data.py` (it's a clearly-marked stub today).
- **`csv`** — drop daily CSVs in a folder (formats below). No connector needed.
- **`none`** (default) — text/tables only; charts left untouched.

## Usage

```bash
pip install python-pptx python-docx lxml

# text/tables only:
python automate_daily_report.py \
    --word     Daily_MAS_YYYYMMDD.docx \
    --template DailyReport_Mobile_EN_template.pptx \
    --out      DailyReport_Mobile_EN_YYYYMMDD.pptx

# text/tables + charts from CSVs:
python automate_daily_report.py ... --chart-source csv --data-dir ./data

# after a template redesign, re-check shape addressing:
python automate_daily_report.py --template TEMPLATE.pptx --inspect
```

Use the previous day's deck as the `--template` (it carries the chart history
the time-series charts append onto).

## CSV formats (see `data_sample/`)

`timeseries.csv` — one row per chart key; appends today's point:
```
pe_band,2026-06-30,15.2,11.48,13.59,15.69,17.80,19.90   # P/E,-2SD,-1SD,Avg,+1SD,+2SD
vnindex_fx,2026-06-30,1860.01,26120                       # VN-INDEX, US$/VND
bond_yields,2026-06-30,2.25,2.70,3.02,3.24               # 2Y,5Y,7Y,10Y
interbank,2026-06-30,4.90,5.20                            # O/N, 1-week
```
`contributors.csv` — 10 rows: `ticker,index_impact,one_d_change`
`foreign_flows.csv` — 10 rows: `ticker,flow,net_flow`

## Two deployment shapes

- **A — Windows + PowerPoint (closest to current process):** keep the linked
  `.xlsm`; update it (openpyxl/xlwings or its existing macros), then refresh the
  deck's links via PowerPoint COM (`pywin32`: open → `UpdateLinks()` → save).
  This script still does the text/tables. No chart-cache editing needed.
- **B — Headless (this tool):** no Office, no share. Pull data → `python-pptx`
  for text/tables + chart-cache rewrite. Runs on a schedule anywhere.

## Maintenance notes

- **Addressing** is by `(slide_index, shape_id)` in `apply_text()` and chart
  index in `TS_CHARTS`/`CAT_CHARTS`. If the template layout changes, re-run
  `--inspect` and update those maps.
- **FX rate** for the US$ trading-value cell defaults to `26.278` (the deck's own
  implied rate); override with `--fx-rate`.
- **Narrative** (slide 1, 2 lines) is auto-written from the data as a factual
  baseline — this is the natural spot to add an editorial sentence by hand.
- Charts not fed by the provider are **left unchanged** (no stale-but-wrong data
  silently written).
