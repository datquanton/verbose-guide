# Lunch Notice Workflow

Automates the daily Vietnamese-language morning-session market summary
("Phòng Research gửi Anh/Chị tóm tắt phiên giao dịch buổi sáng…") by
scraping public market data and rendering it into a fixed template.

## Trigger

- Scheduled run on every HOSE trading day at **11:35 ICT**, five
  minutes after the morning session closes (11:30).
- Manual re-run command for ad-hoc use.
- Skips weekends and HOSE holidays (table maintained alongside the job).

## Data sources

| Field                              | Primary source                                              | Notes                                                                                         |
| ---------------------------------- | ----------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| VN-Index close, Δ points, Δ %      | `https://mastrade.masvn.com/board/10` (HOSE board)          | Read the index header at 11:30 snapshot.                                                      |
| P/E VN-Index                       | `https://dstock.vndirect.com.vn/` (market overview widget)  | Template attributes "Bloomberg"; either drop the attribution or wire a Bloomberg feed later.  |
| Volume (mn shares), value (bn VND) | `mastrade.masvn.com/board/10` market summary panel          | Capture morning total; compare against the previous trading day's stored morning snapshot.    |
| Top ± index contributors (5 each)  | `dstock.vndirect.com.vn` "Top ảnh hưởng VN-Index"           | Take the five names on each side, in the order shown.                                         |
| Foreign net buy/sell total         | `mastrade.masvn.com/board/10` foreign-flow panel            | HOSE morning value in tỷ VND.                                                                 |
| Foreign top buys / sells (4 each)  | `dstock.vndirect.com.vn` foreign-flow ranking               | Format `TICKER (X tỷ)`, rounded to nearest tỷ.                                                |

## Storage

A small JSON state file keeps prior-morning snapshots so the
"% so với sáng trước đó" deltas can be computed. Schema:

```json
{
  "YYYY-MM-DD": {
    "volume_million_shares": 366.0,
    "value_billion_vnd": 9687.0
  }
}
```

The job reads the previous trading day's entry, then writes today's
entry after rendering.

## Pipeline steps

1. **Resolve date.** Determine today's trading date in ICT; abort on
   non-trading days.
2. **Fetch snapshots.** Call each source. Retry up to 3× with
   exponential backoff. Treat any field that fails to parse as missing
   rather than silently zeroing it.
3. **Load prior snapshot** from the JSON state file (previous trading
   day, not calendar day).
4. **Compute deltas.**
   - `vol_delta_pct = (today.volume / prior.volume - 1) * 100`
   - `val_delta_pct = (today.value / prior.value - 1) * 100`
   - Sign and round to one decimal place; format as `+X.X%` / `-X.X%`.
5. **Render template** (see below).
6. **Persist** the rendered Markdown to
   `lunch-notices/YYYY-MM-DD.md` and update the state file.
7. **Deliver** (out of scope here — Slack/email hook can read the
   rendered file).

## Template

Plain-text Markdown, leading bullet glyphs preserved. Placeholders use
`{{snake_case}}`.

```
Phòng Research gửi Anh/ Chị tóm tắt phiên giao dịch buổi sáng:
• Kết thúc phiên giao dịch buổi sáng, chỉ số VN-Index đóng cửa ở mức {{vnindex_close}} điểm, {{vnindex_change_word}} {{vnindex_change_abs}} điểm ({{vnindex_change_pct}})
• P/E VN-Index ở mức {{pe}} (Bloomberg)
• Khối lượng giao dịch: {{volume_mn}} triệu CP ({{volume_delta_pct}} so với sáng trước đó).
• Giá trị GD: {{value_bn}} tỷ ({{value_delta_pct}} so với sáng trước đó)
• Top các cổ phiếu ảnh hưởng đến thị trường:
+ Chiều tăng điểm: {{top_up_5}}
+ Chiều giảm điểm: {{top_down_5}}
• Khối ngoại {{foreign_side}} {{foreign_net_bn}} tỷ, trong đó:
+ Mua ròng: {{foreign_top_buys}}
+ Bán ròng: {{foreign_top_sells}}
```

Formatting rules:

- `vnindex_change_word` is `tăng` or `giảm` based on sign; `vnindex_change_abs` is unsigned.
- `vnindex_change_pct` is the signed percent in parentheses-friendly form, e.g. `-0.14%`.
- `volume_delta_pct` / `value_delta_pct` always carry a sign: `+7.0%`, `-3%`.
- Top-impact lists are comma-separated tickers, no parens.
- Foreign top buys/sells are comma-separated `TICKER (X tỷ)` items.
- `foreign_side` is `mua ròng` or `bán ròng`; `foreign_net_bn` is unsigned.

## Failure modes

- **Source down / layout change.** Render the template with `??` for
  the missing field and flag the run as degraded so a human can patch
  before delivery.
- **Missing prior-morning snapshot** (e.g. first run, or holiday gap).
  Emit `n/a` for the affected delta and log a warning; do not block
  delivery.
- **Mismatch between sources** on overlapping fields (e.g. VN-Index
  close on both boards). Prefer mastrade for index/volume/value and
  VNDirect for impact and foreign-flow rankings; record both raw
  values in the run log for audit.

## Open questions

- Confirm whether "Bloomberg" attribution on P/E is contractual; if
  not, switch to VNDirect and update the template.
- Decide delivery channel (email, Slack, internal CMS) before wiring
  step 7.
- Decide where the JSON state file lives — repo-tracked, S3, or a
  small KV store.
