---
topic: equity-research/sector
date: 2026-10-14
type: prompt-chain
tags: [banks, fiinpro, kpi, template, workflow]
---

# Banks KPI workbook — build prompt chain

A staged chain for building the bank KPI workbook end to end. Run one prompt per turn and check its output against the acceptance checks before moving on. Each stage leaves files behind that the next stage reads, so the chain can stop and restart at any stage.

Current state (2026-10-14): stages 1–3, 5–6 and 9 are done at basic depth in `Banks_KPI_FiinPro_2026-10-14.xlsx`. ★ marks what a full run would add.

---

## Stage 0 — Scope lock

> Before building anything, restate the scope and ask me to confirm: (1) bank universe — all 27 listed banks, or a named subset; (2) peer groups — e.g. SOCBs (VCB, BID, CTG), large private (TCB, MBB, VPB, ACB, HDB, STB, LPB), mid, small; (3) periods — annual FY2014→latest, quarterly ★ 1Q2016→latest, LTM; (4) units — VND bn for amounts, % for ratios; (5) language — EN/VI labels; (6) where files go in the vault (topic `equity-research/sector`). Don't start until I confirm.

**Accept:** one confirmed scope block saved to the top of the build note.

## Stage 1 — Data inventory & pull

> Using the FiinQuant MCP tools in raw format, pull for every bank in scope: income statement, balance sheet, cash flow and ratios — annual FY2014→latest **and ★ quarterly 1Q2016→latest** — plus daily unadjusted close + traded value since 2014. Batch 4–5 tickers per call (60 s timeout). Save every response unchanged to `RAW_DIR` with the naming `{is|bs|cf|ratios}_{a|q}_N.json`, `prices_N.json`. Then print a coverage matrix: bank × dataset × first/last period × count, and list every gap.

**Accept:** coverage matrix shows no unexplained gaps; gaps are listed by name.

## Stage 2 — Source-data validation

> Run QA on the raw data before computing anything: (a) a period identical to the prior one (provider copy), compared at VND-bn precision; (b) assets ≠ liabilities + equity; (c) annual P&L ≠ sum of 4 quarters by more than 1%; (d) NPAT > TOI or other impossible combinations; (e) unit breaks (a series jumping ×1000); (f) NPL/CASA/CAR outside plausible ranges. Write every finding to a QA table with bank, period, check, values, and the action taken (blank / keep + flag). Do not silently fix data.

**Accept:** QA table produced; every flagged period has an explicit action.

## Stage 3 — Metric definitions, reconciled to my template

> Lock one definition per metric (EN + VI label, formula, source line items, unit, better-direction). Reconcile against my hand-built TCB reference figures: for every metric show my number vs computed, and where they differ by more than 0.2pp, test alternative formulas and propose the one that matches, or explain why it can't (e.g. needs notes data). ★ Ask me to rule on: credit cost denominator, PD formula, cost of deposits vs cost of funds, CASA source, LDR (TT22 needs parent-only data).

**Accept:** a definitions table I've signed off; reconciliation table attached.

## Stage 4 — Compute layer ★

> Compute every metric for each bank and period: annual, ★ quarterly (annualised where it's a rate), and LTM. Add ★ peer-group medians and averages, sector median, ★ 5-year averages (for P/B as in my template), and ★ percentile rank within the sector for each bank × metric × period. Keep raw → metrics in a script (`bank_kpi_builder.py`), never hand-entered numbers.

**Accept:** spot-check 5 random bank × metric × period cells by hand from the raw statements.

## Stage 5 — Workbook structure

> Build the workbook with these sheets: README (EN/VI), Search, ★ Dashboard (one-page sector view), Lookup, Definitions (EN/VI), QA flags, Compare, Panel (long format), one sheet per bank in my template layout, ★ Quarterly (bank × metric × quarter), ★ Peers (group medians), ★ Inputs (forecasts, target price, macro), hidden Data/Lists/Calc. Every displayed number traces to Data via formulas.

**Accept:** sheet list matches; no hard-coded numbers outside Data and Inputs.

## Stage 6 — Search & charts UX

> On Search: one control panel (bank, metric, period, peers, ★ peer group, ★ annual/quarterly toggle, language). Show: history table + line chart (bank vs peers vs sector median), all-bank ranking + bar chart with the selected bank highlighted, full bank profile with the selected metric highlighted, ★ a scatter chart (e.g. ROE vs P/B) across banks for the chosen period. Dropdowns accept typing; wrong inputs show "not found" instead of errors.

**Accept:** recalculated in LibreOffice/Excel with 3 different input sets; screenshots attached; no #N/A or #REF visible.

## Stage 7 — Valuation & forecast inputs ★

> Add the 2026F/2027F columns from my template as input cells on the Inputs sheet (loan growth, NIM, credit cost, CIR, payout) and derive forecast P&L, BVPS, ROE, target P/B (Gordon: (ROE−g)/(COE−g)) and target price, so the bank profile shows FY history + forecast. Inputs are yellow; derived values are formulas.

**Accept:** changing one input moves target price; a worked example for one bank matches a hand calculation.

## Stage 8 — Macro & market inputs ★

> Add a Macro sheet for interbank O/N rate, 12M deposit rates (Big-4 vs private), system liquidity, with source and date columns. If FiinQuant has no series, leave dated input rows and say which source to use. Link these into the MARKET rows of the bank sheets. Add historical free float if available; otherwise keep ADTV/market cap and say so.

**Accept:** every macro value has a source and as-of date.

## Stage 9 — Verification & delivery

> Recalculate the workbook headless, then: compare every Search/Lookup output against Panel (0 mismatches), check EN and VI modes, render Search to PNG for both, list QA flags and open questions. Commit the workbook, builder and note to the vault, and give me a short summary of what changed and which numbers need my judgement.

**Accept:** verification counts reported; screenshots sent; committed and pushed.

## Stage 10 — Refresh routine ★

> Turn stages 1, 2, 4, 5 and 9 into a one-command refresh (pull → QA → build → verify) that runs after each quarterly reporting season, writes a changelog of what moved (new quarter, restated periods, new QA flags), and keeps the previous workbook version.

**Accept:** a refresh run on unchanged data reproduces the workbook exactly.
