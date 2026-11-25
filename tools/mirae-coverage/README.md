# Mirae Asset coverage pages

Builds seven pages under `/nganh/` (Vietnamese, with `en/`): six industry reports and an overview, reading Mirae Asset Securities (Vietnam) research into three frames for each of 44 stocks: underlying drivers, milestones, cushion.

```
python3 tools/mirae-coverage/build.py          # from the repository root
python3 tools/mirae-coverage/build.py --whens  # also list every milestone date label and its calendar group
```

| File | What |
|---|---|
| `data.json` | Per-ticker reading of the reports: rating, target, price in the report, target history and notes, thesis, drivers, milestones, cushion, what breaks the thesis, Mirae forecasts, sources (report links). Industry blocks under `segments`. |
| `market.json` | Prices (`price_date`) and trailing P/E and P/B at market price (`val_date`) from FiinQuantX. |
| `meta.json` | Hand-written page text: titles, summaries, tiles, key points, cushion paragraphs. Every number in it was checked against `data.json` and `market.json`; if either changes, recheck the text. |
| `whens.json` | Milestone date label → Vietnamese label and calendar group. A new label not listed here falls back to pattern rules; add it. |
| `build.py` | Generator. Derived columns: gap to target = target ÷ price − 1; margin of safety = 1 − price ÷ target; a target older than 100 days is marked `*`; a target restated in a note where Mirae said it will likely cut forecasts or valuation (`review_down` in `data.json`) is marked `†`. |

How `data.json` was made (25 Nov 2026): the report list comes from `https://masvn.com/api/categories/fe/56/article?page=N&limit=300` with header `locale: en` (815 English reports in Sector & Firm); each PDF is `https://masvn.com/api<file_path>`. The 2026 reports, plus the latest full 2025 report for thinly covered tickers, were converted to text and read; every number used was checked word for word against the report text before it went into the file, and each target and report-date price was cross-checked against the report of that date.

Watch-outs when refreshing:
- Mirae's printed forward P/E and P/B are usually computed at the target price, not the market price. Use market multiples from FiinQuantX for anything called valuation.
- Short results notes often restate an older target. Record when the target was set (`tp_note`), not only the note date.
- Stock dividends and bonus shares cut per-share targets without a change in value; Mirae's rating-history table shows the adjusted figures.
- Fetching needs network access to `masvn.com` and `www.masvn.com` (added to the cloud environment allowlist on 25 Nov 2026).
