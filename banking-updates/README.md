# Banking Updates — publishing system

A zero-dependency system for compiling research-report metrics **plus your own
written commentary** into polished, share-ready HTML investor updates.

```
banking-updates/
├── README.md                  ← this file
├── data/
│   └── metrics.json           ← THE cumulative dataset: houses, forecasts, charts,
│                                 ticker cases, sources. Add new report data here.
├── templates/
│   ├── style.css              ← shared design (light/dark, charts, tables)
│   └── update-template.md     ← starting point for a new update
├── scripts/
│   └── build.py               ← compiles everything (Python 3, stdlib only)
├── updates/
│   └── 2026-07-22-vietnam-banks-2026/
│       ├── update.md          ← SOURCE: front matter + your writing + placeholders
│       └── index.html         ← OUTPUT: the finished, self-contained blog post
└── index.html                 ← OUTPUT: archive page listing every update
```

## Workflow: publishing a new update

1. **Add new report data** to `data/metrics.json` as you collect it — a new row
   in `dashboard`, a new bar in `charts.forecasts.items`, updated `tickers`
   cases, a new entry in `sources`. Bump `as_of`. This file is the cumulative
   scoreboard; it carries forward between updates automatically.

2. **Start the update** — copy the template into a dated folder:

   ```bash
   mkdir -p banking-updates/updates/2026-10-15-q3-earnings
   cp banking-updates/templates/update-template.md \
      banking-updates/updates/2026-10-15-q3-earnings/update.md
   ```

3. **Write your thoughts** in `update.md`. It's plain markdown
   (`##`/`###` headings, `**bold**`, `*italic*`, `[links](url)`, `-` and `1.`
   lists, `> ` callout boxes, `---` rules). Drop in generated blocks wherever
   you want them:

   | Placeholder | Renders |
   |---|---|
   | `{{tiles}}` | hero stat tiles (from `hero_tiles`) |
   | `{{chart:forecasts}}` | profit-growth-by-house bar chart |
   | `{{chart:nim}}` | NIM trend chart |
   | `{{chart:roe}}` | ROE-by-ticker chart |
   | `{{chart:backing}}` | buy-list consensus chart |
   | `{{table:tickers}}` | ticker-by-ticker investment cases |
   | `{{table:dashboard}}` | cumulative house-by-house dashboard |
   | `{{sources}}` | linked source list |
   | `{{disclaimer}}` | standard disclosure box |

4. **Build:**

   ```bash
   python3 banking-updates/scripts/build.py
   ```

   This regenerates every `updates/*/index.html` **and** the archive
   `index.html` — so older updates automatically pick up styling fixes, and the
   archive stays sorted newest-first.

5. **Commit and share.** Each `index.html` is fully self-contained (inline CSS,
   no external assets, light + dark mode) — sharing options:
   - **GitHub Pages** (best for a permanent link): repo Settings → Pages →
     deploy from branch, then updates live at
     `https://<user>.github.io/<repo>/banking-updates/`.
   - **Email / chat attachment**: send the single `index.html` file as-is.
   - **PDF**: open in a browser → Print → Save as PDF.

## Conventions

- Folder names: `YYYY-MM-DD-short-slug` — the date prefix drives archive sorting.
- Never edit `index.html` by hand — it is overwritten on every build. Your
  writing lives in `update.md`; shared numbers live in `metrics.json`.
- Chart guardrails (already encoded in the CSS/build): single-hue bars from a
  zero baseline, direct value labels, forecast bars in a lighter step, no
  dual axes. Add data, not decoration.
- The disclaimer text lives in `metrics.json → brand.disclaimer`; edit once,
  it applies everywhere.

## Related files

- `../vietnam-banking-industry-reports-2026.md` — the raw report catalog
  (the research inbox); distilled numbers graduate from there into
  `data/metrics.json`.
