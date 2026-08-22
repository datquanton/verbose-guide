# Accounting & Financial Modelling Guide — Keyed to Our Book

Not a generic textbook: every concept is illustrated with the actual companies we own
and the actual numbers from our 2026 research. Work through it with FiinPro/SSI open —
recompute each example yourself; that is what "internalizing the figures" means.

Sections: 1 Banks · 2 Brokers · 3 Developers · 4 Steel · 5 Earnings quality ·
6 Valuation toolkit · 7 Vietnam-specific terms · 8 Study path

---

## 1. Bank accounting & modelling (TCB, VPB)

A bank's P&L is five lines. Model them in this order:

```
Credit growth → Net interest income (NII) → + Fees/other → − Opex → − Provisions → PBT
```

**NII = average earning assets × NIM.** NIM = (interest income − interest expense) /
avg earning assets. The two levers: asset yield (loan mix, repricing) and cost of
funds (deposit rates, CASA share).
*Worked example:* TCB quarterly NIM fell to 3.1% in 1Q26 when deposit competition
spiked, then recovered to 3.4% in 2Q26 as loans repriced. Sector NIM 2.9% —
TCB's ~50bp premium IS the CASA moat, in one number.

**CASA (current account & savings account ratio)** = near-zero-cost deposits / total
deposits. TCB 38.3%. Every point of CASA is roughly a point of deposits on which the
bank pays ~0% instead of ~5–9% term rates → direct NIM defense.

**Credit quota**: in Vietnam the SBV caps each bank's loan growth (2026: ~11–13%
typical; VPB ~35% via GPBank rescue; infrastructure/social-housing loans can be
quota-exempt — TCB grew 14.3% YTD using exemptions vs 11.6% without). **In a
quota regime, volume is policy-granted, so model credit growth = quota × utilization,
not demand.**

**Asset quality trio** — always read together:
- NPL ratio (Circular 31 classification, groups 3–5): TCB 1.15%, VPB parent ~2%, consolidated <3%
- Coverage ratio = provisions held / NPLs: TCB 125.5%. <100% means future P&L pain is stored up
- Credit cost = new provisions / avg loans (the P&L flow): TCB guiding ~0.4%
*Trap:* a flat NPL ratio can be manufactured by write-offs (FiinRatings' 2026 sector
warning — buffers at post-2021 lows). Check gross NPL formation, not just the ratio.

**ROE decomposition (bank DuPont):**
`ROE = (NIM + fee margin − opex margin − credit cost margin) × leverage × (1 − tax)`
VPB: high NIM (~4.4% guided) × high credit-risk appetite; TCB: lower risk, fee-rich.
Same ~16–17% forecast ROE, totally different engines — and different failure modes.

**Valuation — justified P/B:** `P/B* = (ROE − g) / (COE − g)`.
Sanity check: ROE 17%, COE ~13%, g 5% → P/B* ≈ 1.5x — exactly Vietcap's target
multiple for TCB and VPB. When a report says "target P/B 1.5x," this is where it
comes from. Your edge: disagree with their ROE or COE inputs, not the formula.

**Bank red flags:** interest receivables growing faster than loans (uncollected
interest booked as income); restructured-loan disclosures; group-2 loan spikes
(pre-NPL); related-party/ecosystem lending concentration (TCB–Masterise).

## 2. Broker accounting & modelling (TCX, VPX)

Four revenue engines — model each separately:

| Engine | Driver | Our data points |
|---|---|---|
| Margin lending | book × (lending rate − funding cost), spread ~4–6% | TCX ₫51.5tn book (largest); VPX ₫38tn → 50tn target |
| Brokerage fees | market ADTV × share × fee rate (fee war → ~0 for some) | TCX 9.36% HOSE share; VPX "0-fee or 0-margin-interest" promos |
| Prop / FVTPL | mark-to-market gains — volatile, low quality, don't capitalize at high multiples | VPX 1H26 FVTPL ₫3,461bn = the bulk of its blowout |
| IB / bond distribution | issuance volumes × fees | TCX ~48% corporate-bond advisory share |

**The capital constraint is the model:** margin lending ≤ 200% of equity (TCX at
~98% = huge headroom; this is why brokers do IPOs/placements — SSI, VPBankS raises).
Growth = f(equity), so dilution is a feature of the sector; always model per-share.

**FVTPL** (fair value through profit & loss): prop-book marks flow straight to P&L.
Separate "earned" income (margin interest, fees) from "marked" income (FVTPL) —
VPX's 4x Q2 looks different when you do.

**Cyclicality:** every engine is long the same variable (market turnover & prices) —
brokers are leveraged beta. P/B expands/contracts with the cycle: TCX ~2.4–2.5x vs
SSI ~1.9x vs sector ~1.75x. Paying peak multiple on peak margin-book is the classic
top-of-cycle error; that's the live TCX question.

## 3. Developer accounting (KDH) — where accounting matters most

**Revenue ≠ sales.** Under VAS, residential revenue is recognized at **handover**,
not at contract signing. The value chain:
`presales (contracts+deposits) → customer advances (balance-sheet liability) → handover → revenue`
Presales are the leading indicator (12–24m ahead); revenue is the lagging one.
*Worked example:* KDH 1Q26 revenue −60% YoY with only 6 Gladia units handed over —
while brokers still forecast FY NPAT doubling, because contracted sales sit in
advances waiting for handover. Both facts can be true; the question is timing risk.

**Inventory** = land + construction-in-progress + **capitalized interest** (borrowing
costs on development projects are added to inventory, NOT expensed — profits look
clean while cash bleeds). KDH: inventory ₫29.1tn = 73% of assets, OCF negative 5
straight years. That pattern is *normal* for a land-banking developer mid-cycle and
*fatal* in a funding squeeze — which one it is depends entirely on absorption.

**One-off alert — "bargain purchase" gain:** buy a company below the fair value of
its net assets and book the difference as instant profit. KDH's 1Q26 "+131% NPAT"
included ₫285bn of exactly this (An Lap acquisition). Core operating profit was a
fraction of the headline. Always rebuild developer P&L ex-one-offs.

**Valuation — RNAV:** value each project = land + costs to complete vs expected
sales (at assumed ASP × absorption), discount, sum, subtract net debt, apply a
discount (20–40% in VN for execution/legal risk). The stock's 0.85–1.0x P/B says the
market currently credits KDH's 600ha land bank at roughly zero premium — that IS the
bull argument; the bond-inspectorate findings and OCF are the counterweight.

**Developer red flags:** receivables/loans to "development partners" (disguised
funding), guarantees to buyers' banks, land-use-fee escalation (KDH's Tan Tao capex
jumped ₫7.7tn → ₫17.9tn), bond-proceeds misuse findings.

## 4. Commodity/steel accounting (HPG)

**The spread model** — steel profit is a spread, not a margin:
`Spread/tonne ≈ ASP − (~1.6t iron ore + ~0.7t coking coal + scrap/energy/other)`
`EBITDA ≈ Σ (volume_product × spread_product) − fixed costs`
Inputs from our research: iron ore ~$98–104/t, coking coal ~$240/t (both benign),
27.83% AD duty holding up domestic HRC prices — but HPG cut list prices in early
July: watch the spread, not the volume headlines.

**Operating leverage & the capex cycle:** Dung Quat 2 doubles HRC capacity →
depreciation steps up immediately, profit depends on utilization climbing (DQ2 BF1
~80%, BF2 ~50% planned 2026). High fixed costs mean small spread moves swing NPAT
violently — that's why HPG guides +42% NPAT on +33% revenue.

**Inventory lag:** steelmakers carry ~2–3 months of raw materials, so falling ore
prices flatter margins with a lag (and vice versa). Quarterly margins are noisy —
judge on spread × normalized volume.

**Valuation:** mid-cycle P/E and EV/EBITDA (never peak-earnings P/E — the classic
cyclical trap: low P/E at the top). HPG at ~8.2x 2026F vs 10.5x 10-yr average and
P/B 1.3–1.5x (historical bottom zone) — cheap *if* 2026F earnings are mid-cycle,
expensive if they're peak. That's the entire debate.

## 5. Earnings-quality screen (run on every name, every quarter)

1. Strip one-offs (KDH bargain purchase; HPG 1Q26 property-transfer gain; broker FVTPL)
2. Cash conversion: cumulative 3-yr OCF / cumulative NPAT — near or above 1 is healthy
   (banks/brokers: use pre-provision profit vs capital formation instead)
3. Accrual check: receivables + inventory growing faster than revenue = future pain
4. Provision adequacy: coverage trend, write-off rate (banks); slow-moving inventory (developer)
5. Auditor notes: qualifications, emphasis-of-matter, related-party volumes — read them

## 6. Valuation toolkit (which method for which name)

| Sector | Primary | Cross-check | Never |
|---|---|---|---|
| Banks (TCB/VPB) | Justified P/B vs sustainable ROE | Residual income | DCF of dividends only |
| Brokers (TCX/VPX) | P/B vs ROE through cycle | SOTP (margin book + fee biz) | Peak-earnings P/E |
| Developer (KDH) | RNAV with discount | P/B floor + presales multiple | This-year P/E |
| Steel (HPG) | Mid-cycle EV/EBITDA | Replacement cost/tonne of capacity | Peak P/E |

Plus, for everything: **reverse-engineer the price** — what ROE/growth/spread does
the market imply? Your edge lives in disagreeing with a specific implied number.

## 7. Vietnam-specific terms (fast glossary)

- **VAS vs IFRS:** VN accounting standards; key gaps: no fair-value-through-OCI granularity, handover revenue recognition, limited impairment modelling (banks use SBV circulars instead of IFRS 9)
- **Circular 31/41/Circular 102:** SBV loan classification / Basel II capital / new securities-firm exposure limits
- **Charter capital:** par value (₫10,000) × shares — the basis of "capital increase" headlines; bonus issues raise it without new cash
- **FOL (foreign ownership limit):** 30% banks, varies elsewhere; drives VNDiamond membership (KDH's removal trigger) and placement premiums
- **Credit room / quota:** SBV-granted loan-growth ceiling per bank; the 2026 "VIP pass"
- **Stock dividend / bonus shares:** free shares, price adjusts mechanically on ex-date (TCB's upcoming 60%, VPB ~26%, TCX's done 20% — always re-base per-share history)
- **Group 1–5 loans:** performing → loss; NPL = groups 3–5; "group 2" = early warning
- **Mandatory transfer bank:** weak bank absorbed by a strong one (VPB–GPBank) in exchange for quota/reserve incentives
- **BT/PPP:** build-transfer / public-private projects (KDH's Ma Lang bid)

## 8. Study path (edge comes from reps, not reading)

1. **Week 1–2:** rebuild TCB's last 8 quarters in a sheet from FiinPro raw data —
   NII, NIM, CASA, credit cost — until your numbers match the press release. Then do VPB and compare engines.
2. **Week 3:** KDH — build the presales → advances → handover bridge from the
   balance sheet; strip one-offs from 3 years of P&L. You will never trust a
   developer headline again.
3. **Week 4:** HPG spread model — monthly HRC/ore/coal prices vs quarterly gross
   margin, 3 years back. Then TCX/VPX: margin book × spread vs reported margin income.
4. **Ongoing:** every earnings release, fill the dossier table by hand within 48h;
   every broker report, recompute their target from their own assumptions once.
5. **Books, in order:** McKinsey *Valuation* (ch. on ROIC/growth), Damodaran on bank
   valuation (free lecture notes), *Financial Shenanigans* (Schilit) for §5 skills,
   Fridson & Alvarez *Financial Statement Analysis*. Skip generic modelling courses —
   your models above are the course.
