# Data Sources — Where Every Number Comes From

Ranked by reliability for each job. Rule from PROCESS.md S4: every load-bearing
number gets confirmed in two independent sources, one of them primary.

## 1. Company financials (primary)

| Source | What | Notes |
|---|---|---|
| **HOSE disclosures** (hsx.vn) | Audited/reviewed FS, corporate actions, insider filings | The legal record — ex-dates and record dates live here |
| **Company IR pages** | Press releases, analyst presentations, transcripts | TCB/VPB/HPG/TCBS all publish English decks quarterly |
| **FiinPro-X / FiinGroup** | Full financials history, ownership, ratios, sector data | The professional terminal; FiinRatings research is free on their site |
| **SSI iBoard** (iboard.ssi.com.vn) | Real-time prices, financials tabs, foreign flows | Free, good for daily monitoring and the dossier tables |

**FiinQuant MCP connector:** attached to this session but **not yet authorized** —
authorize it in claude.ai → Settings → Connectors, and these pulls become automated:
live prices, financial statements, ratios and ownership data directly into the
dossiers instead of hand-collected estimates.

## 2. Market data & screens (secondary)

- **Vietstock Finance** (finance.vietstock.vn) — financials, filings archive, analyst-report library (bao-cao-phan-tich section aggregates broker TPs)
- **CafeF** (cafef.vn) — fastest earnings coverage; du-lieu section for data; treat numbers as press-grade until verified
- **Simplize / TradingView / stockanalysis.com** — ratios and charts; **warning: all three lagged the HPG and TCX stock-dividend share-count adjustments** — never take P/E, market cap or "consensus TP" from these without reconciling share count
- **Fireant, Wichart** — VN retail terminals, decent for quick ratio history

## 3. Policy & macro (the monitoring routine's lanes)

- **SBV** (sbv.gov.vn — English portal available): policy rates, credit-growth statistics (monthly), circulars, OMO results. Credit and deposit growth prints are the single most important macro series for this book
- **GSO** (gso.gov.vn): GDP, CPI, IIP — quarterly rhythm
- **USITC** (usitc.gov) + **Federal Register** (federalregister.gov) + **trade.gov**: AD/CVD case calendars and determinations — the July 28 rebar final lives here; search "Vietnam steel" in Federal Register for the official documents, not press paraphrases
- **FTSE Russell** (ftserussell.com): index review calendars, country classification announcements (Sept 21 upgrade)

## 4. Research & news (context)

- Sell-side PDFs: MBS, Vietcap, SSI, KBSV, Mirae Asset, Shinhan, GTJA, Yuanta publish
  English PDFs on their sites (catalogued in our root research notes with URLs)
- FiinRatings / VIS Rating: credit-side view — the best early-warning source on
  banks' asset quality and developers' funding
- News tiering: **Reuters/Bloomberg** (wire-grade) > **The Investor / VIR / Việt Nam
  News** (state-linked but reliable English) > **CafeF / Vietstock / tinnhanhchungkhoan**
  (fast, verify) > blogs/Facebook groups (leads only, never sources)

## 5. Known traps (learned in this repo)

1. **Stock-dividend adjustment lag** — TCX 20%, HPG 10%, TCB 60% pending, VPB ~26%
   pending: after any ex-date, re-verify share count before trusting any per-share metric
2. **Stale consensus** — KDH's "avg TP 38,850" predates the July collapse; always
   date-stamp every TP you record
3. **Proxy 403s** — this environment can't fetch most .vn PDFs directly; numbers come
   via search excerpts, so S4 verification against FiinPro/iBoard is mandatory before acting
4. **Headline NPAT** — VN press reports consolidated headline including one-offs;
   rebuild parent-shareholder, ex-one-off numbers yourself (KDH 1Q26 is the canonical example)
