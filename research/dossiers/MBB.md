# MBB — Research Dossier

**Status:** S1 quick screen complete (depth-queue item 3) · 2026-07-26
**Why now:** held at 6.5% of the book with **no screen ever written**. The model carried
`confidence 0.55` on a name that had never been underwritten, and the optimizer wants to
add it (+5.0pp this cycle, north star 20%). Sizing a name up on an un-screened thesis is
exactly the failure this process exists to prevent.

---

## S1 · Quick screen

### 1. What does it sell, to whom?

MB Group: a commercial bank plus one of the widest subsidiary sets in Vietnamese
banking — securities (MBS), insurance (MB Ageas, MIC), asset management, consumer
finance (Mcredit), and since Dec-2024 **MBV**, the former OceanBank, taken 100% under a
compulsory transfer. Retail + SME + a large military-linked corporate franchise.
Target: 40m customers, ~60% of contribution through digital channels.

**Segment profit split not yet obtained** — the AR segment note is the gap. Flagged, not
glossed.

### 2. Who controls it?

Effectively the military-industrial state, through a bloc of holders:

| Holder | Stake |
|---|---|
| Viettel (Military Industry–Telecoms Group) | 14.70% |
| SCIC (state capital investment) | 9.83% |
| Vietnam Helicopter Corporation | 7.00% |
| Tan Cang Saigon (Saigon Newport) | 6.16% |
| **Bloc total** | **~37.7%** |

Manulife Vietnam and UBS have recently crossed 1%. No founding family, no ecosystem
developer parent — **a materially different governance profile from TCB or VPB**, and on
balance a favourable one: no related-party developer lending channel of the kind that
dominates the TCB risk case. The offsetting risk is that a state bloc can be directed
toward policy objectives that are not shareholder-value objectives. The MBV transfer is
precisely that mechanism in action.

### 3. Five-year trend

| Year | Profit | ROE |
|---|---|---|
| 2023 | PBT ₫26,306bn (+15.7%) | 25.0% (ROA 2.5%) |
| 2024 | NPAT-parent ₫22,600bn (+9.5%) | 22.09% |
| 2025 | NPAT-parent ₫26,800bn (+18.3%) | 21.57% |
| TTM 2026 | — | 20.9% |
| 2026 plan | PBT ₫39,400–39,500bn (+15%) | target 20–21% |

Growing, not cyclical, not broken. **But ROE is eroding steadily — 25.0 → 22.1 → 21.6 →
20.9.** Still sector-best, and the direction is what matters for a justified-P/B
valuation. The likely causes are capital build (charter capital heading past ₫102tn) and
MBV dilution of returns; both need confirming from the segment note.

*Model cross-check:* FY25 NPAT-parent ₫26,800bn implies TTM ₫28,879bn
(26,800 + 14,755 − 12,676). `assumptions.json` carries ₫28,065bn, derived independently
from the H1 earnings path — a 2.8% gap. **The `_npat_ttm_method` holds up.** No change.

### 4. Valuation vs its own history

Trades at **P/B 1.24×, P/E 7.46×**, against roughly 1.36–1.58× in recent years — a
discount to its own history while still earning the sector's best ROE.

Justified P/B = (ROE − g)/(COE − g), on ROE 20.9%:

| g | COE 15% | COE 17% |
|---|---|---|
| 10% | 2.18× | 1.56× |
| 12% | 2.97× | 1.78× |

Every cell is far above the traded 1.24×. Even punishing assumptions (COE 17%, g 10%)
imply 1.56×, ~26% above spot. **This is the variant-view candidate**, and it independently
supports the optimizer's instinct to add — reached by a different route than the
expected-return model, which matters.

Caveat: justified P/B is hypersensitive to g, and a *declining* ROE means the sustainable
g is probably nearer the bottom of that range. Treat 1.5–1.8× as the defensible band, not
2.9×.

### 5. Red-flag scan (Vietnam-specific)

- [x] **Weak-bank transfer (MBV/OceanBank)** — the defining idiosyncratic risk. MB took
      100% of a failed bank. The upside is regulatory: transferees receive credit-quota
      and reserve privileges, which is a large part of why MB can target 30–35% credit
      growth while peers get 11–13%. The downside is that MBV's losses are absorbed
      somewhere. **Kill criterion already armed:** transferee drag > 5% of PBT in any quarter.
- [ ] Inspectorate / SSC actions — not found, not yet systematically checked
- [ ] Auditor qualifications — not checked
- [x] Related-party lending — no developer-ecosystem channel; structurally lower risk than TCB
- [x] Pledged founder shares — n/a, no founding family
- [ ] Mcredit consumer-finance asset quality — **unchecked, and it is the closest analogue
      to VPB's FE Credit problem.** Should be the first item in any S3.

### 6. Liquidity

Large-cap, VN30 constituent, high turnover. A 6.5% position exits comfortably inside
5 days at ⅕ ADTV. Not a constraint.

### 7. Corporate actions — one requires the holder to act

- 10% cash dividend, **paid 17-Jul-2026**
- **15% stock dividend + 10:1 rights at ₫10,000** — charter capital +27.5%

The rights issue is not cosmetic. At ₫22,050, subscribing 1 new share per 10 at ₫10,000
gives a theoretical ex-rights price of **₫20,955** (≈ −5.0%). A holder who does not
subscribe absorbs that ~5% as a transfer to those who do. **This is a dated, actionable
item, not background.** Record date still to be announced — it is on the watch list.

---

## Gate: the two-sentence test

> **The market believes** MBB is a good but unexciting state-linked bank whose ROE is
> quietly eroding, and prices it at a discount to its own history at 1.24× book.
>
> **I might believe** the erosion is the *price* of the MBV transfer rather than decay of
> the franchise — and that the transfer bought something valuable in exchange: a
> 30–35% credit-growth allowance in a system rationed to 11–13%. If that is right, the
> ROE trough is near and 1.24× book is too cheap for a 21% ROE.

**Passes S1.** There is a genuine variant view and it is falsifiable.

## What would prove me wrong

1. MBV drag exceeds 5% of PBT in a quarter — the transfer is a cost, not a trade
2. ROE breaks below 20% — erosion is franchise decay, not a transfer effect
3. Mcredit NPL formation accelerates — the FE Credit problem in a different wrapper

## Not done — do not treat this as an S3

Segment profit split · Mcredit asset quality · MBV's absorbed losses · inspectorate
history · auditor notes · the by-hand 8-quarter table. **Confidence stays at 0.55 in
`assumptions.json`.** An S1 screen does not earn an evidence-tier upgrade; only primary
documents do (charter §2).

---
*Sources: [Doanh nhân & Pháp luật — shareholder structure](https://doanhnhan.baophapluat.vn/co-cau-co-dong-mb-mbb-manulife-viet-nam-va-ubs-gia-nhap-nhom-so-huu-tren-1-81494.html) · [CafeBiz — Viettel/SCIC/Tan Cang bloc](https://cafebiz.vn/co-cau-co-dong-dac-biet-gom-viettel-scic-tan-cang-sai-gon-dem-lai-ca-tinh-va-loi-the-vuot-troi-gi-cho-ngan-hang-mb-20220708145052329.chn) · [VnEconomy — compulsory transfer of OceanBank to MB](https://vneconomy.vn/vietcombank-mb-so-huu-100-von-cb-va-oceanbank-moi-quyen-loi-nguoi-gui-tien-duoc-dam-bao.htm) · [Topi — multi-year ROE/profit](https://topi.vn/co-phieu-mbb.html) · [VCBS research PDF](http://static1.vietstock.vn/edocs/19031/mbb_tang_toc_don_dau_chu_ky_moi_02_2026.pdf) · [Tạp chí Kinh tế Tài chính — valuation](https://tapchikinhtetaichinh.vn/mbb-tang-toc-chu-ky-moi-dinh-gia-con-hap-dan-147919.html)*
