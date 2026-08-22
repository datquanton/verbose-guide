# VPX (VPBankS) — Research Dossier

**Status:** S3 core complete (depth-queue item 13) · 2026-07-27
**Why now:** `exit_pe` carried an earnings-quality discount that was **asserted**, not
derived from the book's composition — the same defect class the HPG spread bridge fixed.

> ⚠ **ESCALATION — VPX's `npat_ttm` fails the mandated cross-check, and VPX is the
> book's top-ranked name on expected return.** The file's own earnings-path method gives
> **₫3,047–3,447bn**; the file carries **₫2,800bn**. Correcting it takes VPX from
> **+19.0% (rank 1) to roughly +2 to +12%**. This is the **second** instance of the same
> error class in two days — VCI was 25.2% off — and both are brokers. Detail in §4.

---

## 1 · What VPX actually is

Not primarily a broker. The balance sheet says otherwise:

| Item | Q2/26 |
|---|---:|
| FVTPL financial assets | **~₫30tn**, of which **>₫18tn is bonds** |
| Margin lending + advances | **₫38,177bn** (+₫4tn YTD) |
| Remaining margin room | **>₫33tn** |
| HOSE market share | 3.57% (HNX 6.71%, UPCoM 5.28%) |

**A ~₫68tn balance sheet of bonds and margin loans with a 3.57% brokerage attached.**
Brokerage is the smallest thing here. That reframing matters for the multiple: VPX should
be valued as a leveraged credit-and-margin book, not as a fee-earning broker.

## 2 · Earnings quality — more nuanced than "marks flatter the P&L"

1H FVTPL gains were **₫3,461bn** against 1H PBT of **₫2,673bn** — gains exceeding total
profit, which is what drove the discount in the model. But the detail changes the reading:

- **Q2 alone carried a ₫923bn FVTPL loss**, and proprietary trading *still* netted
  **>₫700bn (+58%)**. Losses are being absorbed, not hidden.
- **>60% of the FVTPL book is bonds**, not equities. Bond FVTPL returns are substantially
  carry and rate marks — repeatable in a way equity marks are not.

**So the discount is justified but for a different reason than assumed.** The risk is not
that gains are fake; it is that a ₫30tn bond book is a **rates and credit position** whose
returns depend on the Vietnamese corporate-bond market staying orderly. That is a real
exposure, and it sits inside a company whose parent is 82.5% a bank.

The model's `exit_pe` band (9–16×) is unchanged — the discount survives, its rationale is
now documented rather than asserted. No judgment input moved on T5 evidence (charter §2).

## 3 · The margin headroom

₫38.2tn drawn with **>₫33tn of room** to the 2.0× regulatory ceiling. That is the largest
unused lending capacity of the three brokers in the book (TCX is at 98% of equity, VCI at
97%). If the FTSE flows arrive and turnover rises, VPX has the most room to lever into it.

That is the genuine bull case, and it is better than the one currently in the model
(which leans on the CAEX option). It is also the bear case in reverse: deploying ₫33tn
into margin at the top of a record system margin cycle is how brokers get hurt.

## 4 · The escalation: a second broker with an understated market cap

The file's `_npat_ttm_method` mandates deriving TTM from the earnings path and
cross-checking against market cap. Running it:

- H1/26 NPAT ₫2,169bn at +200.5% YoY → H1/25 = **₫722bn**
- TTM = FY25 + H1/26 − H1/25 → **₫3,047–3,447bn** across plausible FY25 outcomes
- Independent route: margin ₫38,177bn + room >₫33tn ⇒ ceiling ≥₫71.2tn ⇒ equity ≥₫35.6tn;
  at P/B 1.40 that implies a market cap of **₫49.8tn** and `npat_ttm` **₫3,559bn**

**The file carries ₫2,800bn.** Every route says that is too low.

| `npat_ttm` | Market cap | Raw E[r] | Shrunk @0.70 |
|---:|---:|---:|---:|
| **2,800 (in file)** | ₫39,200bn | +27.2% | **+19.0%** ← rank 1 |
| 3,047 | ₫42,658bn | +16.9% | +11.8% |
| 3,247 | ₫45,458bn | +9.7% | +6.8% |
| 3,447 | ₫48,258bn | +3.3% | +2.3% |
| 3,559 (P/B route) | ₫49,826bn | +0.1% | +0.0% |

**VPX's rank-1 position is substantially an artifact of an understated denominator.**

**Control check, so this isn't a false alarm:** TCX's `pe_ttm × npat_ttm` = ₫82.2tn, and
~2.0bn shares at ₫41,100 = ₫82.2tn. **TCX agrees and is fine.** The defect is specific to
the two names whose TTM bases were set as rough early estimates — VCI and VPX.

**No number changed** (charter §2: resolve from a filing, not from inference between two
conflicting derivations). **Confidence cut 0.70 → 0.55**, which is permitted on any tier
once an input is known suspect.

## 5 · Risks

- **Bond book** — ₫18tn+ in a market with a 2022 precedent, at a company inside a banking group
- **Margin at the cycle top** — the headroom is an opportunity and a temptation
- **Thin float** — ~80% held by VPB; price discovery is poor and exit liquidity is limited
- **Zero sell-side coverage** — no external check on the numbers
- **Double-counting** — 4.22% effective exposure once the VPB look-through is included

## 6 · Kill criteria

Two armed (FVTPL marks >50% of PBT for a third consecutive quarter; CAEX licence
rejected). Added:

3. **Margin deployed into a falling market** — if the margin book grows while system
   margin debt contracts, VPX is buying the top of the cycle with borrowed money.

## 7 · Decision

**Suspend any VPX add until `npat_ttm` is resolved from the Q2 filing.** On the file's own
mandated method VPX is not the best expected return in the book; it is mid-table at best.
The business is better than the model gives it credit for — the loss absorption and the
bond-heavy composition are both more solid than "marks flattered it" implies — but the
*valuation* input is wrong in the direction that flatters it.

**Not done:** FVTPL book line-by-line, bond issuer concentration, CAEX carrying value,
the offshore funding structure. Most need the filing.

---
*Sources: [Doanh nhân & Pháp luật — Q2 4×, margin >₫38tn](https://doanhnhan.baophapluat.vn/vpbanks-vpx-lai-quy-ii-gap-4-lan-cung-ky-du-no-margin-vuot-38-000-ty-dong.html) · [Mekong Asean — >₫18tn into bonds](https://mekongasean.vn/vpbanks-bao-lai-quy-2-tang-manh-rot-hon-18000-ty-dong-vao-trai-phieu-57489.html) · [Người Quan Sát — >₫33tn margin room](https://nguoiquansat.vn/vpbanks-vpx-bao-lai-quy-ii-gap-4-lan-cung-ky-con-hon-33-000-ty-dong-room-cho-vay-margin-304623.html) · [Tuổi Trẻ — Q2 profit exceeds TCBS](https://tuoitre.vn/vpbanks-bao-lai-quy-2-gap-4-lan-cung-ky-vuot-tcbs-100260717170520303.htm)*
