# VN30 — 2Q/2026 Consolidated Results Review

**As of:** 31 July 2026 (the statutory deadline for consolidated quarterly reports, 30 days after quarter-end)
**Universe:** VN30 basket announced by HOSE in the July 2026 review, effective 03/08/2026
**Currency:** VND bn ("tỷ đồng") throughout. Bank profit = pre-tax (LNTT) unless stated; corporates = after-tax (LNST).

---

## 0. Method and data-quality note

Direct page scraping was not possible from this environment: outbound HTTPS is restricted by the session's egress policy to GitHub/Anthropic hosts, and every Vietnamese financial site (cafef.vn, vietstock.vn, tinnhanhchungkhoan.vn, hsx.vn, …) returns a proxy-level 403 on both `WebFetch` and `curl`. Everything below was therefore assembled from web-search retrieval of Vietnamese financial media reporting on the filed consolidated statements, not from the filings themselves.

Practical consequences, and they matter for how you use this:

- **Every figure is media-reported, not read off a filed BCTC.** Where two outlets disagree I flag it.
- **Actual vs. estimate is tracked explicitly.** Some VN30 names (BID, MBB, GVR, BVH) were still only covered by broker estimates at the time of writing; those rows are marked and should not be treated as reported results.
- Machine-readable companion: [`data/vn30-2q26-results.csv`](../data/vn30-2q26-results.csv), with a `data_status` column (`actual` / `estimate` / `derived` / `partial`).

---

## 1. The basket

HOSE's July 2026 review **added MCH (Masan Consumer) and TCX (Techcom Securities), and dropped TPB (TPBank) and PLX (Petrolimex)**, effective 03/08/2026. Reserve list: VCK, BCM, GEE, VPX, PLX. This follows the January 2026 review, which added VPL (Vinpearl) and removed BCM.

The resulting 30 constituents, by sector:

| Sector | Count | Tickers |
|---|---|---|
| Banks | 13 | ACB, BID, CTG, HDB, LPB, MBB, SHB, SSB, STB, TCB, VCB, VIB, VPB |
| Property & hospitality | 4 | VIC, VHM, VRE, VPL |
| Consumer & retail | 5 | MSN, MCH, VNM, SAB, MWG |
| Securities | 2 | SSI, TCX |
| Industrials & resources | 3 | HPG, GAS, GVR |
| Technology | 1 | FPT |
| Aviation | 1 | VJC |
| Insurance | 1 | BVH |

Two structural reads on the rebalance itself:

1. **The index is being re-weighted toward the domestic consumption and capital-markets story.** TPB and PLX out, MCH and TCX in, swaps a mid-tier bank and a state fuel distributor for a branded-FMCG compounder and the most profitable brokerage in the country. That reduces the banks' headcount to 13 and lifts non-bank earnings beta.
2. **The passive flow attached to it is small.** Four VN30 ETFs hold roughly VND 10,000bn combined; estimated rebalance buying was ~VND 486bn net, with MCH (~VND 384bn) and TCX (~VND 59bn) the buys and VJC, TPB and VNM the largest sells. This is an index event, not a flow event — do not confuse the two when explaining August price action.

---

## 2. Executive summary

**The quarter was strong in aggregate and unusually narrow in composition.**

- Market-wide, 574 of 1,638 listed companies (≈31.8% of market cap) had reported by 28/07 with aggregate after-tax profit **+23.5% YoY — the weakest growth in four quarters.** Non-financials grew faster (+35.2%) than the market average; the deceleration is at the index level, not in any single sector.
- **Within VN30, growth is dramatically more concentrated than the headline suggests.** Vinhomes alone booked VND 52,091bn of H1 after-tax profit (+379%), which is larger than the H1 pre-tax profit of any bank in the country including Vietcombank. Strip the Vin property complex out and the VN30 aggregate looks like a solid mid-teens grower, not a boom.
- **Banks delivered ~mid-to-high-teens sector growth with the widest internal dispersion in years.** Nine VN30 banks with confirmed H1 numbers produced ~VND 127,800bn of pre-tax profit. But the range runs from VPBank +68% and VietinBank +36.7% to Sacombank −44% (Q2) and ACB roughly flat. Credit-cost divergence, not revenue divergence, is doing most of the work.
- **The quality of earnings is mixed and needs to be underwritten name by name.** Several of the biggest YoY moves are base effects or one-offs: GAS is down 24% only because Q2/25 contained a provision reversal; GVR's estimated +31% leans on ~VND 1,500bn of land compensation; FPT's revenue "decline" is a deconsolidation artefact. Conversely, Vinamilk, MWG, Techcombank and TCBS grew on operating drivers with margin expansion behind them.
- **Sector leadership per market-wide data:** transport/ports (+65%), industrial-park property (+58%), retail (+34%), oil & gas (+28%). Within VN30 the same ordering roughly holds, with property (Vin complex) sitting above all of them.
- **Market context:** VN-Index closed 30/07 at 1,744.66 after a ~40-point session. Foreign investors remained heavy net sellers — roughly VND 15,300bn in June, ~VND 80,300bn YTD — with only tentative net buying returning at month-end. FTSE Vietnam 30 was moved into the FTSE Vietnam Index Series and out of the Frontier series effective the September 2026 review.

---

## 3. Company-by-company

### 3.1 Banks (13 of 30)

| Ticker | Q2/26 PBT | YoY | H1/26 PBT | YoY | Status |
|---|---|---|---|---|---|
| VCB | 17,420 | +57.9% | 29,222 | +33.5% | actual |
| CTG | ~15,400 | +27% | 25,868 | +36.7% | H1 actual, Q2 est. |
| VPB | 11,000 | +77% | ~18,900 | +68% | actual |
| TCB | 9,670 | +22.4% | 18,540 | +22.5% | actual |
| BID | 9,921–10,034 | +15–16% | n/c | — | **estimate** |
| MBB | ~8,812 | +18% | n/c | ~+19% | **estimate** |
| HDB | ~6,800 | +44% | n/c | ~+22% | approx. |
| SHB | n/c | +59% | ~10,770 (61% of FY plan) | — | derived |
| ACB | n/c | −12% | 10,700 | −0.4% | actual |
| LPB | n/c | — | 5,973 | −3% | actual |
| VIB | 1,905 (PAT) | −8.2% | 5,180 | +3% | actual |
| SSB | n/c | — | 2,625 | — | actual |
| STB | 2,030 (PAT) | −44% | n/c | — | actual |

**Vietcombank (VCB)** is the quarter's genuine surprise. Q2 pre-tax profit of 17,420bn (+57.9%) on net interest income of 19,142bn (+35.2%) restores it as the system's profit leader with H1 of 29,222bn (+33.5%), ahead of a VietinBank that most brokers had modelled to overtake it. NII growth of that magnitude at VCB's size implies both volume and a NIM that held up better than the sector; sub-1% NPL means it is not paying for growth with provisions. This is the highest-quality earnings print in the basket.

**VietinBank (CTG)** delivered H1 pre-tax profit of 25,868bn (+36.7%), roughly 49% of the annual plan. The brokers' pre-season narrative — CTG overtakes VCB — did not survive contact with VCB's actual print, but on growth rate CTG is the stronger of the two.

**VPBank (VPB)** posted the sharpest growth of any large bank: Q2 pre-tax 11,000bn, +77% YoY and +38.6% QoQ, H1 ~18,900bn (+68%). Two things to underwrite here. First, this is increasingly a *group* result rather than a bank result — VPBankS contributed 2,158bn of pre-tax profit (+293%) and OPES insurance grew 164%. Second, parent-bank credit growth of +24.8% against a system average of ~8.4%, concentrated in real estate (+44%) and wholesale/retail trade (+28%), is a very large relative-growth bet. The earnings are real; the risk build is real too, and it will not show up in NPLs for several quarters.

**Techcombank (TCB)** set a record quarter at 9,670bn (+22.4%), H1 18,540bn (+22.5%), on total operating income of 28,600bn (+17.5%) and fee income of 7,600bn (+37.6%). Fee growth outrunning TOI growth is the cleanest signal in the bank tape this quarter — it is the one large private bank compounding on non-credit revenue rather than balance-sheet expansion. Assets reached VND 1.27 quadrillion.

**SHB** reported Q2 pre-tax profit +59% and H1 at 61% of its VND 17,655bn full-year plan (~10,770bn implied), a strong acceleration off Q1's 4,656bn (+7%).

**HDBank (HDB)** at ~6,800bn (+44%) in Q2 — seasonally flattered by upfront credit-line fee recognition, and running against a very ambitious FY target of 30,100bn (+41%).

**The losers are where the analysis actually is.** **Sacombank (STB)** cut after-tax profit 44% to 2,030bn, with provisions above 5,000bn — 5.5× the prior year — against a bad-debt book that grew by 6,500bn, including Bamboo Airways exposure, and without last year's asset-liquidation gains. **ACB** fell ~12% in Q2 (H1 −0.4%) on heavier provisioning against a Q2/25 base inflated by securities gains — a base effect, not deterioration, but also not growth. **LPBank** H1 pre-tax fell 3% as provisions rose 2.3× to 1,552bn. **VIB** Q2 after-tax fell 8.2% with H1 pre-tax up only 3%.

**Sector read.** The industry entered 2026 in a more selective credit phase — credit/GDP is high, funding costs are up, and sector NIM is expected to stay below 3%. Revenue growth is therefore no longer the differentiator; **credit cost is.** The banks that grew (VCB, CTG, TCB, VPB, SHB, HDB) either have provisioning headroom or non-credit revenue engines. The banks that shrank (STB, ACB, LPB, VIB) are absorbing legacy asset-quality costs. Expect that gap to widen, not converge, in H2.

### 3.2 Property, hospitality and the Vin complex (4 of 30)

**Do not sum these four.** VHM, VRE and VPL are all within Vingroup's consolidation perimeter; adding their profits to VIC's double-counts. Read VIC as the group and the others as segment detail.

**Vingroup (VIC)** — H1 revenue 222,300bn (+72.5%), H1 after-tax profit 20,375bn, **4.5× the prior year**, at 58% of the VND 35,000bn full-year target. VinFast delivered 128,662 vehicles globally in H1 (+78%) and ~429,175 e-motorbikes (3.7×), with six of the ten best-selling domestic models. The industrial-manufacturing and property segments are both contributing; the group is running ahead of plan at the half.

**Vinhomes (VHM)** — the single largest earnings event in the basket. Q2 revenue 52,722bn (~2.9×), Q2 gross profit 34,732bn (**8×**, ~66% gross margin), H1 revenue 116,565bn (3.43×) and H1 after-tax profit 52,091bn (4.79×) — 86.8% of the full-year profit plan in two quarters. Total assets passed VND 1 quadrillion. Presales of 148,104bn (+119%) mean the handover pipeline behind this is already contracted. Handovers at Ocean Park 2/3 and Green Paradise are the driver. The caveat is structural, not doubtful: property revenue recognition is lumpy and this is a handover-cycle peak, so the 2027 comparison base is now extremely high.

**Vincom Retail (VRE)** — Q2 revenue 2,374bn (+10.8%), after-tax profit 1,609bn (+30.4%). Profit growing 3× revenue on a retail-leasing book indicates occupancy/rent-mix improvement plus operating leverage. Quietly one of the cleanest results in the basket.

**Vinpearl (VPL)** — Q2 revenue 3,309bn (+12%) and after-tax profit 631bn (~4×); H1 revenue 6,795bn with core hospitality +33%, H1 profit 2,140bn (8×), 71% of the annual plan. This is a real tourism-recovery result at the operating line, though the H1 multiple flatters against a depressed 2025 base.

### 3.3 Consumer and retail (5 of 30)

**Mobile World (MWG)** — record quarter: Q2 revenue 48,751bn (+29.6%), after-tax profit 3,355bn (~2×); H1 pre-tax 7,361bn (+86%) on revenue above 95,000bn (+30%). Gross margin expanded from 20.1% to ~22.2%. Bach Hoa Xanh did 28,300bn in H1 (+25%), Q2 +31%, opening 632 stores to reach 3,191, with H1 cohorts already at positive store-level operating profit after full logistics cost. One flag: the group is holding a record 66,600bn in cash and has placed 22,127bn into lending and bonds — a meaningful and growing share of profit is now financial income rather than retail. Note media disagreement on the Q2 profit figure (3,355bn after-tax vs. "over 4,000bn" in some coverage); the pre-tax/after-tax distinction most likely explains it.

**Masan Group (MSN)** — record profit: Q2 after-tax 3,800bn (2.3×), H1 5,773bn (2.2×), prompting management to raise FY guidance to 98,000–105,000bn revenue and 10,000–11,500bn pre-minority profit. The doubling is group-level (deleveraging and associate contributions), and is running well ahead of the underlying consumer business.

**Masan Consumer (MCH)** — the new VN30 entrant: Q2 revenue 7,165bn with after-tax profit 1,384bn (+10%); H1 revenue 15,637bn (+14%), profit 3,284bn (+11%), free cash flow ~2,000bn, dividend outlay above 2,600bn. Critically, growth was **volume-led (~+10%)** rather than price-led — the highest-quality growth mix of any consumer name in the basket, and a better read on real Vietnamese household demand than MSN's group number.

**Vinamilk (VNM)** — the recovery is confirmed. Q2 revenue 18,856bn (+12.5%) and after-tax profit 3,184bn (+28%), its best quarter in over five years; H1 revenue 35,034bn (+~18%) and profit 5,643bn (+38.4%), with net cash above 18,000bn. Domestic demand recovery plus export strength plus subsidiary contribution — three independent drivers, which is what makes this durable rather than a bounce.

**Sabeco (SAB)** — the weak link in staples. Q2 revenue ~6,890bn (+1%) with gross profit 2,660bn (+9%) as input costs fell, but advertising spend consumed the gross-margin gain at the operating line. H1 revenue 13,345bn (+6%) and after-tax profit 2,489bn (+21%). Cash and equivalents are roughly 65% of total assets (>20,000bn) — the balance sheet is doing a lot of the earnings work, and the beer volume story remains unresolved.

### 3.4 Industrials and resources (3 of 30)

**Hoa Phat (HPG)** — the standout industrial. Q2 revenue 55,557bn (+53%) and after-tax profit 6,424bn (+51%); H1 revenue 108,870bn (+47%) and profit 15,480bn (+103%), already 70% of the full-year profit plan on 52% of revenue — i.e. margins are running ahead of plan, not just volumes. Nearly 7m tonnes of crude steel in H1; HRC output +50% in the first five months as Dung Quat 2 ramped. The Dung Quat rail-and-special-steel project (700k t/yr) is past 50% construction with product targeted from Q2/2027 for national infrastructure. This is a capacity-cycle earnings story with a visible second leg.

**PV GAS (GAS)** — Q2 after-tax profit 3,604bn, **−24% YoY but +22% QoQ**. The decline is a base effect: Q2/25 contained a bad-debt provision reversal. Sequential improvement is the honest read. Downstream, subsidiary PV GAS D was squeezed hard as US–Iran tensions lifted crude while suppliers lagged on selling-price adjustment, collapsing its gross margin from ~6.9% to under 1%.

**Vietnam Rubber Group (GVR)** — *estimate only.* Q2 profit projected at 1,990bn (+30.7%) on an ~18% rubber price increase plus ~1,500bn of land-conversion compensation; 5M/26 pre-tax was ~3,900bn (+30%). Note the mix: a material part of the growth is compensation income, not rubber or industrial-park operations. Treat the growth rate as lower quality than the headline.

### 3.5 Financial services ex-banks (3 of 30)

**Techcom Securities (TCX)** — the other new entrant, and it arrives on a record: Q2 pre-tax profit 2,097bn (+21%), H1 3,555bn (47% of the annual plan), total assets above 100,000bn. The most profitable brokerage in the market by some distance.

**SSI** — Q2 revenue 3,312bn (+13%) with pre-tax profit 1,511bn (+32%); H1 revenue 6,652bn (+27%) and pre-tax 3,122bn (+39%). Margin lending of ~40,500bn. Third in the industry by quarterly profit, behind TCX.

Read together: brokerage profits are growing on **margin books and investment banking**, not brokerage fees, in a market where retail turnover has not been the driver. That makes securities earnings a leveraged bet on the upgrade/liquidity narrative rather than a cash-flow business — and note VPBankS (+293%) sitting inside VPB, meaning bank investors now carry brokerage beta whether they wanted it or not.

**Bao Viet (BVH)** — *incomplete.* Q1/26 consolidated pre-tax profit was 1,006bn (+18.7%), with non-life revenue 3,917bn (+23.5%) and life revenue 11,284bn (+3.7%). H1 after-tax profit growth was reported at +9.3%; quarterly detail was not confirmed at the time of writing. Directionally: non-life is growing, life is stagnant, and group profit growth is decelerating into single digits.

### 3.6 Technology and aviation (2 of 30)

**FPT** — the most misread number in the basket. Headline Q2 revenue of 13,789bn looks like a sharp decline, and H1 revenue of 26,269bn is far below the prior-year run-rate. **This is an accounting change, not a business contraction:** from 01/01/2026 FPT deconsolidated FPT Telecom to equity-method accounting after the Ministry of Public Security acquired 50.2% (FPT retains 45.66%). Revenue and assets drop out; the profit share stays. On that basis Q2 after-tax profit attributable to the parent was 2,568bn (+14%), H1 pre-tax 5,714bn (+18.1%), H1 attributable profit 5,055bn (+14.1%), EPS 2,967 (+13.4%). The operating engine is intact: foreign IT services H1 revenue 18,902bn (+13.4%), 14 contracts above USD 10m, new bookings +32.3%. Note that media outlets have published the "Q2 revenue −17%" and "H1 revenue +12.6%" figures side by side — they cannot both be right on the same basis, and the deconsolidation is why. Separately, FPT has lost over 114,000bn of market capitalisation from its peak and dropped out of the top-10 most valuable listed companies — the de-rating is far larger than the earnings news, which is itself the investment question.

**Vietjet (VJC)** — Q2 revenue 30,499bn (+71%) with after-tax profit of only **349bn**; H1 revenue 51,536bn (+44%), 59.4% of the annual plan. Over 6.2m passengers in Q2 and 13.4m in H1 across ~72,000 flights, plus ~41,000 tonnes of cargo. The revenue/profit gap is the story: 71% top-line growth converting to a sub-1.2% net margin means fuel and capacity costs are absorbing essentially all of the volume gain. Against a fleet plan of 600+ aircraft by 2030, this is a growth story that is not yet a margin story.

---

## 4. Cross-cutting themes

**1. Growth is decelerating at the index level even as absolute profits set records.** Market-wide +23.5% is the weakest in four quarters. The VN30 number is flattered by one property cycle. Both statements are true simultaneously, and any H2 model should assume the property contribution normalises.

**2. Credit cost has replaced NIM as the swing factor in bank earnings.** With sector NIM stuck below 3%, the difference between a +68% bank and a −44% bank this quarter was provisioning, not lending margin. Bamboo Airways-related exposure and legacy NPLs are still working through the system.

**3. One-off and base effects are pervasive — audit each name.** GAS (−24% purely on a prior-year reversal), ACB (−12% on a prior-year securities-gain base), GVR (+31% including ~1,500bn compensation), FPT (revenue optics from deconsolidation), MSN (group-level rather than operating doubling). Conversely VNM, MWG, MCH, TCB, VRE and HPG grew with margin expansion behind them — those are the results that should survive into H2.

**4. Volume-led beats price-led.** MCH grew ~10% on volume, VNM on domestic recovery plus exports, MWG on traffic with 210bp of gross-margin expansion. That trio is the cleanest available evidence that Vietnamese household demand genuinely recovered in 2Q26, as opposed to nominal growth from pricing.

**5. Financialisation of non-financial balance sheets.** MWG holds 66,600bn in cash with 22,127bn deployed into lending and bonds; SAB's cash is ~65% of assets; VNM carries 18,000bn net cash. A rising share of "operating" profit at consumer names is interest income. That is a rate bet embedded in a consumer multiple.

**6. Foreign flows still contradict fundamentals.** ~VND 80,300bn of net foreign selling YTD against record VN30 profits. The FTSE Vietnam 30 reclassification (into the Vietnam Index Series, out of Frontier, effective the September 2026 review) is the structural offset to watch.

---

## 5. Scorecard

**Highest-quality results** (operating-driven, margin-supported, repeatable): VCB, TCB, HPG, VNM, MWG, VRE, MCH, TCX.

**Strong but requiring a caveat**: VHM and VIC (cycle peak, extreme 2027 base), VPB (growth is real; credit risk build is large and lagging), MSN (group-level mechanics), SHB and HDB (strong but partly seasonal/plan-dependent), VPL (depressed base).

**Weak or deteriorating**: STB (provisioning cliff), LPB and VIB (provisions rising, growth stalled), ACB (flat), SAB (cost-absorbed), VJC (volume without margin), GAS (sequential recovery but negative YoY).

**Insufficient data at the time of writing**: BID, MBB, GVR, BVH.

---

## 6. What to watch into H2/2026

1. **Sacombank's provisioning path.** 5,000bn in one quarter with NPLs still building is the single largest unresolved risk in the VN30 banking block.
2. **Whether VPBank's credit growth (+24.8% vs. ~8.4% system) shows up as asset quality cost in 4Q26/1H27.** It is the cleanest asymmetric risk in the basket.
3. **Vinhomes' 2027 comparison base.** 86.8% of the annual plan in two quarters is a strength now and a headwind later; the presale book (148,104bn, +119%) determines how far the handover cycle extends.
4. **FPT's de-rating vs. its bookings.** New foreign IT bookings +32.3% against a 114,000bn market-cap loss. Either the market is pricing an AI-era disruption to the offshore IT model, or this is a mispricing; the H2 bookings trend arbitrates it.
5. **Vietjet's unit economics.** 71% revenue growth at a sub-1.2% net margin has to converge one way or the other.
6. **MCH and TCX index inclusion from 03/08.** Flow impact is small (~486bn); the meaningful change is that the index now carries more consumer-volume and capital-markets beta.
7. **FTSE upgrade mechanics from the September 2026 review**, against a persistent ~80,300bn YTD foreign outflow.

---

## 7. Sources

Basket and index:
[Tin nhanh Chứng khoán — HOSE chốt rổ VN30](https://www.tinnhanhchungkhoan.vn/hose-chot-ro-vn30-mch-tcx-se-thay-the-cho-tpb-va-plx-post394082.html) ·
[Vietstock — MCH, TCX vào rổ VN30](https://vietstock.vn/2026/07/mch-tcx-vao-ro-vn30-3358-1466674.htm) ·
[Tạp chí Kinh tế Tài chính — danh mục VN30 kỳ 7/2026](https://tapchikinhtetaichinh.vn/hose-cong-bo-danh-muc-vn30-ky-thang-7-2026-bo-sung-mch-va-tcx-161885.html) ·
[Vietstock — đảo danh mục VN30 kỳ 1/2026 (VPL vào, BCM ra)](https://vietstock.vn/2026/01/dao-danh-muc-vn30-ky-thang-12026-vpl-gia-nhap-bcm-bi-loai-ra-3358-1393781.htm) ·
[CafeF — ETF mua bán quanh kỳ cơ cấu](https://cafef.vn/mch-va-tcx-chinh-thuc-lot-ro-vn30-trong-ky-co-cau-thang-7-cac-ca-map-nghin-ty-se-mua-ban-co-phieu-ra-sao-188260715161415394.chn)

Market aggregate:
[CafeF — hơn 570 doanh nghiệp công bố KQKD Q2/2026](https://cafef.vn/hon-570-doanh-nghiep-cong-bo-ket-qua-quy-2-2026-loi-nhuan-tang-truong-thap-nhat-4-quy-188260728172600698.chn) ·
[MBS — Dự báo lợi nhuận Q2/2026](https://www.mbs.com.vn/du-bao-loi-nhuan-q2-2026-tang-truong-trong-moi-truong-day-thach-thuc/) ·
[KIS — Top 5 nhóm ngành tăng trưởng Q2/2026](https://www.kisvn.vn/hoc-dau-tu/nhom-nganh-tang-truong-loi-nhuan-q2-2026) ·
[Vietstock — Nhịp đập thị trường 30/07](https://vietstock.vn/2026/07/nhip-dap-thi-truong-3007-ket-phien-thang-hoa-khoi-ngoai-mua-rong-tro-lai-1636-1473291.htm) ·
[VietnamFinance — FTSE Vietnam 30](https://vietnamfinance.vn/ftse-vietnam-30-duoc-dua-vao-he-thong-ftse-vietnam-index-series-d147184.html)

Banks:
[CafeF — Toàn cảnh lợi nhuận 27 ngân hàng 6T/2026](https://cafef.vn/toan-canh-loi-nhuan-cua-27-ngan-hang-trong-6-thang-dau-nam-2026-188260730152540587.chn) ·
[VnBusiness — Cuộc đua lợi nhuận ngân hàng Q2](https://vnbusiness.vn/cuoc-dua-loi-nhuan-ngan-hang-quy-ii-ke-but-toc-nguoi-hut-hoi.html) ·
[DNSE — NIM thu hẹp, nợ xấu tăng](https://www.dnse.com.vn/senses/tin-tuc/ngan-hang-quy-ii2026-nim-thu-hep-va-no-xau-tang-loi-nhuan-den-tu-dau-35238917) ·
[Thanh Niên — Techcombank Q2 kỷ lục](https://thanhnien.vn/loi-nhuan-quy-2-techcombank-cham-dinh-moi-tu-dong-luc-tang-truong-da-chieu-185260721152115767.htm) ·
[Dân Việt — VPBank lợi nhuận cốt lõi Q2 cao nhất lịch sử](https://etime.danviet.vn/vpbank-loi-nhuan-tu-hoat-dong-cot-loi-quy-ii-cao-nhat-lich-su-d1444223.html) ·
[Thanh Niên — ACB 6T/2026](https://thanhnien.vn/acb-kqkd-6-thang-2026-loi-nhuan-hon-10700-ti-dong-ban-le-va-sme-hoi-phuc-185260722153644093.htm) ·
[Mekong Asean — ACB tăng dự phòng, lãi Q2 giảm ~12%](https://mekongasean.vn/acb-tang-manh-du-phong-loi-nhuan-quy-2-giam-gan-12-so-voi-nam-truoc-57704.html) ·
[Báo Đầu tư — Ngân hàng báo lỗ, giảm lợi nhuận Q2/2026](https://baodautu.vn/nhung-ngan-hang-dau-tien-bao-lo-giam-loi-nhuan-trong-quy-ii2026-d653649.html) ·
[SHB — lãi trước thuế Q2 tăng 59%](https://www.shb.com.vn/44978-2/) ·
[Tin nhanh Chứng khoán — SeABank 6T/2026](https://www.tinnhanhchungkhoan.vn/seabank-ssb-loi-nhuan-truoc-thue-hop-nhat-6-thang-dau-nam-2026-dat-2625-ty-dong-post395001.html) ·
[DNSE — BCTC Q2/2026 VIB](https://www.dnse.com.vn/senses/tin-tuc/bctc-quy-22026-vib-loi-nhuan-q2-dat-190542-ty-dong-giam-824-so-voi-cung-ky-35251647)

Property / Vin complex:
[VietnamFinance — Vingroup lãi 6 tháng gần 20.400 tỷ](https://vietnamfinance.vn/vingroup-bao-lai-6-thang-gan-20400-ty-tang-gap-45-lan-d148388.html) ·
[Vietstock — Vinhomes 6 tháng](https://vietstock.vn/2026/07/vinhomes-dat-gan-87-ke-hoach-loi-nhuan-sau-6-thang-doanh-so-ban-hang-vuot-148000-ty-737-1473680.htm) ·
[VnExpress — Vinhomes lãi kỷ lục hơn 52.000 tỷ](https://vnexpress.net/vinhomes-lai-ky-luc-hon-52-000-ty-dong-nua-dau-nam-5103356.html) ·
[Thời báo Tài chính — VRE Q2/2026](https://thoibaotaichinhvietnam.vn/vre-bao-lai-sau-thue-quy-ii-2026-dat-1-609-ty-dong-tang-hon-30-so-voi-cung-ky-201432.html) ·
[Vietstock — Vinpearl 6 tháng gấp 8 lần](https://vietstock.vn/2026/07/huong-loi-tu-da-phuc-hoi-manh-cua-du-lich-vinpearl-lai-6-thang-gap-8-lan-cung-ky-737-1473782.htm)

Consumer / retail / industrials / other:
[Vietstock — Hòa Phát lãi hơn 6.400 tỷ Q2](https://vietstock.vn/2026/07/hoa-phat-lai-hon-6400-ty-trong-quy-2-tang-51-so-voi-cung-ky-737-1472700.htm) ·
[Vietstock — MWG lãi kỷ lục Q2](https://vietstock.vn/2026/07/tap-doan-the-gioi-di-dong-lai-ky-luc-33-ngan-ty-trong-quy-2-gap-doi-cung-ky-737-1473484.htm) ·
[Tin nhanh Chứng khoán — MWG 6 tháng](https://www.tinnhanhchungkhoan.vn/6-thang-mwg-lai-hon-6100-ty-dong-rot-22127-ty-dong-vao-cho-vay-va-trai-phieu-post394978.html) ·
[Vietstock — Masan lãi kỷ lục 3.800 tỷ Q2](https://vietstock.vn/2026/07/masan-lai-ky-luc-3800-ty-trong-quy-2-gap-23-lan-cung-ky-737-1471321.htm) ·
[Vietstock — MCH 6 tháng](https://vietstock.vn/2026/07/doanh-thu-mch-nua-dau-nam-dat-15637-ty-dong-tien-tu-do-can-moc-2000-ty-737-1471363.htm) ·
[Vietstock — Vinamilk lợi nhuận ròng Q2](https://vietstock.vn/2026/07/loi-nhuan-rong-quy-2-gan-32-ngan-ty-vinamilk-giu-vung-vi-the-tien-mat-rong-hon-18-ngan-ty-737-1474072.htm) ·
[Vietstock — Sabeco Q2/2026](https://vietstock.vn/2026/07/chi-phi-quang-cao-bao-mon-lai-quy-2-cua-sabeco-du-tang-gia-ban-nui-tien-hon-20-ngan-ty-giup-lai-ban-nien-an-tuong-737-1471765.htm) ·
[CafeF — Hé lộ lợi nhuận FPT quý 2](https://cafef.vn/he-lo-loi-nhuan-fpt-quy-2-188260716135124803.chn) ·
[VnExpress — FPT khi không còn hợp nhất FPT Telecom](https://vnexpress.net/so-lieu-tai-chinh-cua-fpt-thay-doi-the-nao-khi-khong-con-hop-nhat-fpt-telecom-5068057.html) ·
[CafeBiz — FPT bốc hơi 114.000 tỷ vốn hóa](https://cafebiz.vn/fpt-boc-hoi-114000-ty-von-hoa-tu-dinh-bang-3-ngan-hang-cong-lai-176260727054747689.chn) ·
[Stockbiz — Vietjet 6 tháng 2026](https://stockbiz.vn/tin-tuc/vjc-vietjet-tang-truong-manh-me-nua-dau-nam-2026-dau-tu-doi-tau-hon-600-may-bay-den-2030-va-hoan-thien-he-sinh-thai-hang-khong/41226104) ·
[Tin nhanh Chứng khoán — SSI 6 tháng](https://www.tinnhanhchungkhoan.vn/ssi-loi-nhuan-truoc-thue-6-thang-dat-3122-ty-dong-tang-39-so-voi-cung-ky-du-no-margin-gan-40500-ty-dong-post394397.html) ·
[Tin nhanh Chứng khoán — TCBS (TCX) Q2 kỷ lục](https://www.tinnhanhchungkhoan.vn/tcbs-tcx-bao-lai-quy-ii2026-cao-nhat-lich-su-vuot-2000-ty-dong-post394023.html) ·
[Dân Việt — Ước tính lợi nhuận Q2/2026 (GVR, ngân hàng)](https://etime.danviet.vn/uoc-tinh-loi-nhuan-quy-ii-2026-ngan-hang-chia-lai-thu-hang-mot-doanh-nghiep-cao-su-co-the-bao-lai-tang-hon-1200-d1439923.html) ·
[Thời báo Tài chính — BVH Q1/2026](https://thoibaotaichinhvietnam.vn/tap-doan-bao-viet-bvh-loi-nhuan-truoc-thue-hop-nhat-quy-i2026-dat-1006-ty-dong-tang-187-196633.html) ·
[Nông nghiệp & Môi trường — PV GAS](https://nongnghiepmoitruong.vn/pv-gas-uoc-lai-hon-8000-ty-vuot-70-ke-hoach-nam-d823567.html)
