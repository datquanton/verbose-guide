# Research Process — Systematic Playbook (v1)

The pipeline every idea passes through. Each stage has a **gate**: the idea either
advances with a written artifact, or it dies and the reason is logged. No position
without a dossier; no dossier without the checklist.

```
Idea → S1 Quick Screen → S2 Industry Dossier → S3 Company Deep Dive
     → S4 Data Verification → S5 Thesis Memo → S6 Sizing & Entry
     → S7 Monitoring → S8 Post-mortem
```

Artifacts live in this repo: `research/dossiers/<TICKER>.md` (from the template),
sector work in root catalogs, monitoring in `monitoring-log.md`, published views in
`banking-updates/`.

---

## S1 · Quick screen (30–60 min) — kill fast

- [ ] What does the company actually sell, to whom, and what % of profit comes from each line?
- [ ] Who controls it? (state %, founding family, foreign strategic, ecosystem parent)
- [ ] 5-yr revenue / profit / ROE trend — one look: growing, cyclical, or broken?
- [ ] Valuation vs own 5-yr history (P/E, P/B band) — cheap for a reason or cheap by mistake?
- [ ] **Red-flag scan (Vietnam-specific):** inspectorate/SSC actions, bond-proceeds
      findings, auditor qualifications, related-party lending, pledged founder shares
- [ ] Liquidity: can the intended position be exited in ≤5 trading days at ⅕ of ADTV?

**Gate:** two sentences — "the market believes X; I might believe Y." No variant view → pass.

## S2 · Industry dossier (per sector, refreshed quarterly)

- [ ] Demand drivers with numbers (credit quota, public capex, presale absorption, steel spread)
- [ ] Supply/competition map, market shares, capacity coming online
- [ ] Regulatory state: SBV circulars, quotas/caps, trade duties (USITC/DOC), FOL rules
- [ ] Cycle position: where are margins vs 10-yr range? What's the consensus assuming?
- [ ] All current sell-side sector reports cataloged with dates (staleness matters — see KDH)
- [ ] Index/flow mechanics: VN30 / VNDiamond / FTSE-EM membership and rebalance dates

**Gate:** the cross-house forecast table (like `vietnam-banking-industry-reports-2026.md` §4).

## S3 · Company deep dive — the dossier

Use `research/templates/ticker-dossier.md`. Non-negotiable sections:

**Business & moat**
- [ ] Unit economics: what one unit of growth costs and earns (1% credit growth, 1 tonne of steel, 1 handed-over unit)
- [ ] Moat test: why does the excess return survive competition? (TCB=CASA, HPG=scale+integration, TCBS=ecosystem distribution)

**Governance (heavily weighted in VN)**
- [ ] Controlling shareholder incentives; parent–subsidiary conflicts (bank vs listed broker arm)
- [ ] Related-party exposure: ecosystem lending (e.g., bank ↔ developer), cross-holdings
- [ ] History of dilution, ESOP size/pricing, treatment of minorities
- [ ] Insider transactions last 12m (registered buys/sells — signal, both ways)
- [ ] Any inspectorate/SSC/tax findings, ever — and how management responded

**Financials (5 years + 8 quarters)**
- [ ] Fill the "figures to internalize" table in the dossier from FiinPro/SSI — by hand, not paste. Internalizing = typing the numbers and computing the ratios yourself
- [ ] Earnings-quality screen (see guide §5): one-offs stripped, cash conversion, accrual ratio
- [ ] Balance sheet stress: debt maturity wall, FX debt, off-BS commitments, pledged assets
- [ ] For each sector, the 5 sector KPIs (guide §1–4) computed and charted vs peers

**Valuation — always two methods**
- [ ] Primary: sector-appropriate (banks/brokers: justified P/B vs sustainable ROE; developer: RNAV with land marked; steel: mid-cycle EV/EBITDA + P/E)
- [ ] Secondary: cross-check (residual income, DCF, or replacement cost)
- [ ] Reverse-engineer the market: what growth/ROE does today's price imply? Is disagreeing with that plausible?
- [ ] All sell-side TPs tabled **with dates** and stock-dividend adjustments verified

**Catalysts & risks**
- [ ] Dated catalyst calendar (earnings, ex-dates, index reviews, regulatory decisions)
- [ ] Pre-mortem: "it's 12 months later and this lost 40% — what happened?" Write 3 paths
- [ ] **Kill criteria: 3 falsifiable conditions that force a sell/resize. Written before entry.**

**Gate:** dossier complete, or the gaps are explicitly listed as "unknowns accepted."

## S4 · Data verification

- [ ] Every load-bearing number confirmed in ≥2 independent sources (filing + data terminal)
- [ ] Quarterly statements pulled from primary source (HOSE disclosure / company IR), not press
- [ ] Share count reconciled post stock-dividends/ESOP (feeds lag — HPG/TCX both burned us)
- [ ] Data pull: FiinPro / FiinQuant connector / SSI iBoard (see `research/guides/data-sources.md`)

## S5 · Thesis memo (1 page, forced brevity)

Format: **Thesis (3 sentences) · Variant perception (what consensus misses) · Valuation
(base/bull/bear with probabilities) · Catalysts (dated) · Top 3 risks · Kill criteria ·
Proposed size.** If it doesn't fit a page, the thesis isn't clear yet.

## S6 · Sizing & entry rules (portfolio constitution)

- [ ] Max single name: 20% at cost. Max risk-cluster (correlated group): 35%
      *(current book violates both — KDH 44%, Techcom cluster 33%)*
- [ ] Classify: **carry** (hold through events) vs **event** (dated catalyst, pre-written exit)
- [ ] No averaging down into governance flags or unexplained drawdowns — only into
      confirmed-thesis + market-beta weakness
- [ ] Entry staged in thirds; full size only after first confirming datapoint

## S7 · Monitoring (automated + manual)

- [ ] Routine sweeps → `monitoring-log.md` (running; SBV/USITC/news every 3h)
- [ ] Per-name KPI watch list from the dossier (e.g., KDH: presales absorption, OCF;
      VPB: FE Credit NPL formation; TCX/VPX: margin book vs system margin debt)
- [ ] Quarterly re-underwrite: does the thesis survive the new quarter's numbers?
- [ ] Kill-criteria check at every material event — mechanically, not "when it feels right"

## S8 · Post-mortem (every exit, win or lose)

- [ ] Entry thesis vs what actually happened; process error vs bad luck separated
- [ ] Decision journal entry: what to repeat, what to ban
- [ ] Update this playbook if the process itself failed

---

## Cadence

| Rhythm | Work |
|---|---|
| Every 3h (automated) | Monitoring sweep → log |
| Weekly | Price/TP table refresh; catalyst calendar check; read new sell-side reports |
| Quarterly | Earnings re-underwrite per name; industry dossier refresh; banking-updates post |
| Per trade | Thesis memo before, post-mortem after |
