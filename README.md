# MAS daily market report automation

Automates the "Vietnam Stock Market" paragraph of the Mirae Asset *Good Morning
Vietnam* daily report: pulls the session data, computes all the `(+X.X% DoD)`
figures, drafts the prose in house style, and writes a `.docx`.

## Pipeline

```
data (vnstock) ──► compute (DoD math) ──► narrative (template | Claude) ──► docx
        ▲                                        ▲
   news RSS ─────────────────────────────────────┘ (sector/ticker drivers)
```

| Report field | Source call |
|---|---|
| OHLC + prior close | `Quote(VNINDEX).history()` |
| Matched volume / value (+prior) | same call, last two rows |
| Breadth (up/ceiling/down/floor) | `Trading.price_board` (aggregate) |
| VN30 top-5 gainers/losers | `Listing.symbols_by_group('VN30')` + `price_board` |
| Foreign net / top buy & sell | `Trading.foreign_trade` |
| Market-driver sentences | RSS (CafeF / VnEconomy) → condensed |

## Install

```bash
pip install -r requirements.txt
```

## Run

Offline, from a verified snapshot (works anywhere, no network):

```bash
python -m mas_report.cli --fixture sample_data/session_2026-06-10.json \
  --drivers "real estate names (NVL, CII, LDG) surged to their ceiling prices" \
  --out out/report.docx
```

Live (in an environment with vnstock access):

```bash
python -m mas_report.cli --live --date 2026-06-10 --out out/report.docx
```

Fill your existing MAS template instead of a fresh doc — put a `{{NARRATIVE}}`
placeholder in the template body where the paragraph should go:

```bash
python -m mas_report.cli --live --template MAS_template.docx --out out/report.docx
```

### Claude-drafted prose (optional)

```bash
export NARRATIVE_BACKEND=anthropic
export ANTHROPIC_API_KEY=sk-...
# ANTHROPIC_MODEL defaults to claude-opus-4-8
python -m mas_report.cli --live --out out/report.docx
```

The template backend is deterministic and needs no API key; the anthropic
backend grounds Claude on the *verified numbers* (it is told not to invent
figures) and uses the news headlines only for color.

## Tests

```bash
python -m pytest tests/ -v
```

The compute layer is fully offline-testable; tests assert the DoD tags,
finance round-half-up (1.65 → 1.7), liquidity strings, and mover ordering
against the 2026-06-10 session.

## Scheduling

`.github/workflows/daily-report.yml` runs weekdays at 15:15 ICT (change the
cron to `15 8 * * 3` for Wednesdays only) and uploads the `.docx` as an
artifact. Wire delivery (Gmail draft / Google Drive upload) into the final
step when you've decided which you want.

## Caveats baked into the workflow (verify on first runs)

1. **Matched vs. total** — ensure the volume/value source is matched-only
   (khớp lệnh), consistent with the report wording. Don't mix in put-through.
2. **Reference close** — DoD uses the exact prior trading-day close from the
   history call (holiday-safe), not a rounded value.
3. **VN30 reconstitution / ex-dividend** — `VN30_FALLBACK` in `config.py` is a
   safety net; the live `symbols_by_group('VN30')` is authoritative. Watch
   ex-dividend days where the reference price is adjusted.
