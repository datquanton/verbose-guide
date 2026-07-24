# Model Snapshot — generated from assumptions.json (as of 2026-07-24)

> Regenerate: `python3 research/models/run.py` · Edit beliefs in `assumptions.json` — git history of that file IS the record of how your views changed.

## 1 · Portfolio structure (weights only — sizes live in the private layer)

| Ticker | Cluster | Weight | vs 20% cap |
|---|---|---:|---|
| TCB | Techcom eco | 35.0% | ⚠ BREACH |
| KDH | Residential | 20.3% | ⚠ BREACH |
| HPG | Steel | 16.8% | ok |
| VPB | VPBank eco | 10.0% | ok |
| MBB | Banks-other | 6.5% | ok |
| TCX | Techcom eco | 5.5% | ok |
| VCI | Brokers-other | 3.1% | ok |
| VPX | VPBank eco | 2.8% | ok |

**Clusters** (cap 35%):

- Techcom eco: 40.5% ⚠ BREACH
- Residential: 20.3%
- Steel: 16.8%
- VPBank eco: 12.8%
- Banks-other: 6.5%
- Brokers-other: 3.1%
- Concentration (HHI): 0.211 — effective number of independent bets ≈ 4.7

## 2 · KDH — Gladia handover model (the whole 2026 P&L is one variable)

NPAT_parent ≈ units × ASP × GM − opex, ×(1−tax) ×51% Gladia stake, + one-off bargain gain

| Scenario | Units handed FY26 | Revenue | NPAT to parent (incl ₫285bn one-off) | vs plan 1,500 / stretch 2,500 |
|---|---:|---:|---:|---|
| bear | 80 | 3,360 | 1,033 | misses plan |
| base | 130 | 5,460 | 1,590 | ≈ plan |
| bull | 185 | 7,770 | 2,203 | ≈ stretch |

- Reality check: 135 units sold by end-Q1, 46 handed. Base case needs ~84 more handovers in 9 months — requires selling out the low-rise AND handing it over. Watch `customer advances` (₫688.6bn at Q1) build each quarter.
- Leverage tracker: debt ₫15,348bn; capitalized interest run-rate ≈ ₫900bn/yr = 60% of planned NPAT — deferred into inventory, not avoided.
- Kill-criteria check (Layer 3): advances < ₫1,000bn by 3Q26 with Heights launched ⇒ bear branch confirmed.


## 3 · TCB — quota × NIM × credit-cost grid (H2 modeled, anchored on H1 actual)

H2 PBT ≈ TOI_H2×(1−CIR) − credit_cost/2 × avg H2 loans; TOI = NII/(1−non-interest share). FY = H1 actual + H2.

| Scenario | FY credit growth | NIM | Credit cost | H2 PBT | FY PBT | % of target |
|---|---:|---:|---:|---:|---:|---:|
| bear | 16% | 3.10% | 0.70% | 12,617 | 31,117 | 83% |
| base | 18% | 3.30% | 0.50% | 14,730 | 33,230 | 89% |
| bull | 20% | 3.50% | 0.40% | 16,391 | 34,891 | 93% |

- Company guidance/target: ₫35,000 – 37,500bn. H1 actual ₫18,500bn = 49% of the top target.
- Sensitivity that matters: NIM ±0.1% ≈ ±₫1.3tn PBT; the CASA franchise is the margin defense.

## 4 · VPB — quota × NIM × credit-cost grid (H2 modeled, anchored on H1 actual)

H2 PBT ≈ TOI_H2×(1−CIR) − credit_cost/2 × avg H2 loans; TOI = NII/(1−non-interest share). FY = H1 actual + H2.

| Scenario | FY credit growth | NIM | Credit cost | H2 PBT | FY PBT | % of target |
|---|---:|---:|---:|---:|---:|---:|
| bear | 30% | 4.10% | 2.60% | 8,018 | 26,898 | 65% |
| base | 35% | 4.30% | 2.20% | 11,803 | 30,683 | 74% |
| bull | 40% | 4.50% | 1.90% | 15,106 | 33,986 | 82% |

- Company guidance/target: ₫41,600bn. H1 actual ₫18,880bn = 45% of the top target.
- Sensitivity that matters: each +0.2% of credit cost ≈ −₫2.3tn PBT — FE Credit NPL formation is the swing factor.

## 5 · TCX — margin-engine model + FTSE event tree

| Scenario | H2 avg margin book | Spread | H2 PBT | FY PBT | vs plan 7,535 |
|---|---:|---:|---:|---:|---|
| bear | 46,000 | 4.2% | 2,807 | 6,362 | 84% |
| base | 52,000 | 4.6% | 3,651 | 7,206 | 96% |
| bull | 58,000 | 5.0% | 4,519 | 8,074 | 107% |

**Sep 21 FTSE event tree (Layer 2 — probabilities are the assumption):**
- strong inflows + follow-through: p=35%, price move +20%
- in-line, quiet digestion: p=45%, price move +5%
- sell-the-news / flow disappointment: p=20%, price move -15%
- **Expected value of the event ≈ +6.2%** — positive but modest; the position pays if the *base business* keeps compounding, the event is a kicker not a thesis.

## 6 · VPX — earnings-quality split + CAEX option

H1 PBT ₫2,673bn splits ≈ core ₫1,200bn + FVTPL-driven ₫1,473bn (marks, not fees) — model them separately:

| Scenario | H2 core vs H1 | H2 FVTPL vs H1 | FY PBT | vs plan 6,453 |
|---|---:|---:|---:|---|
| bear | 0.9x | 0.4x | 4,334 | 67% |
| base | 1.1x | 0.8x | 5,156 | 80% |
| bull | 1.3x | 1.2x | 5,977 | 93% |

**CAEX crypto-license option:** license granted ~Q3 p=40% → +15% · delayed / unresolved p=45% → +0% · rejected (5-license cap) p=15% → -8%
- Option EV ≈ +4.8%. Note the asymmetry vs TCX: VPX's risk is earnings QUALITY (FVTPL), TCX's is MULTIPLE.

## 7 · HPG — volume × spread model

FY NPAT = Q1 actual (₫9,056bn incl ₫4,123bn one-off divestment gain) + remaining volume × core NPAT/tonne

| Scenario | Q2–Q4 volume (m t) | Core NPAT/t (₫m) | FY NPAT | vs target 22,000 | vs street 18–28k |
|---|---:|---:|---:|---|---|
| bear | 10.5 | 1.25 | 22,181 | 101% | low end |
| base | 11.5 | 1.6 | 27,456 | 125% | high end |
| bull | 12.5 | 1.85 | 32,181 | 146% | high end |

- Q1 core ≈ ₫1.68m/tonne. The bear case IS the early-July domestic HRC price cuts — watch the spread, not volume.
- Jul 28 US rebar final: headline risk only (~3% of revenue) — a red print that day is a Layer-4 flag, not a model input.

---
*Models beat your inconsistency, not the market. Layer-4 items (governance, quota politics, the An Lap seller question) are NOT in these numbers — see dossiers and monitoring log.*
