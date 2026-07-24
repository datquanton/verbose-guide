#!/usr/bin/env python3
"""Portfolio scenario models v0 — edit assumptions.json, run this, read SNAPSHOT.md.

Layer map (see chat/roadmap): this file covers Layer 1 (deterministic arithmetic)
and Layer 2 (scenario estimation). Layers 3-4 (updating, judgment) live in the
monitoring log and dossiers. Stdlib only: python3 run.py
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
A = json.loads((HERE / "assumptions.json").read_text(encoding="utf-8"))
OUT = []


def w(line=""):
    OUT.append(line)
    print(line)


def vnd(x):
    return f"{x:,.0f}"


# ---------------------------------------------------------------- portfolio
def portfolio():
    p = A["portfolio"]
    rows, clusters = [], {}
    total_mv = total_cost = 0.0
    for pos in p["positions"]:
        mv = pos["shares"] * pos["price"] / 1e6      # VND m
        cost = pos["shares"] * pos["avg_cost"] / 1e6
        total_mv += mv
        total_cost += cost
        clusters[pos["cluster"]] = clusters.get(pos["cluster"], 0) + mv
        rows.append((pos["ticker"], pos["cluster"], mv, cost))
    w("## 1 · Portfolio (Layer 1 — arithmetic, zero judgment)\n")
    w("| Ticker | Cluster | Value ₫m | P&L ₫m | P&L % | Weight | vs 20% cap |")
    w("|---|---|---:|---:|---:|---:|---|")
    for t, c, mv, cost in sorted(rows, key=lambda r: -r[2]):
        wt = mv / total_mv * 100
        flag = "⚠ BREACH" if wt > p["max_single_name_pct"] else "ok"
        w(f"| {t} | {c} | {mv:,.1f} | {mv-cost:+,.1f} | {(mv/cost-1)*100:+.1f}% | {wt:.1f}% | {flag} |")
    w(f"| **Total** | | **{total_mv:,.1f}** | **{total_mv-total_cost:+,.1f}** | **{(total_mv/total_cost-1)*100:+.1f}%** | 100% | |")
    w("\n**Clusters** (cap {}%):\n".format(p["max_cluster_pct"]))
    for c, mv in sorted(clusters.items(), key=lambda kv: -kv[1]):
        wt = mv / total_mv * 100
        flag = " ⚠ BREACH" if wt > p["max_cluster_pct"] else ""
        w(f"- {c}: {wt:.1f}%{flag}")
    hhi = sum((mv / total_mv) ** 2 for _, _, mv, _ in rows)
    w(f"- Concentration (HHI): {hhi:.3f} — effective number of independent bets ≈ {1/hhi:.1f}")
    w("")


# ---------------------------------------------------------------- KDH
def kdh():
    m, act = A["kdh"]["model"], A["kdh"]["actuals"]
    w("## 2 · KDH — Gladia handover model (the whole 2026 P&L is one variable)\n")
    w("NPAT_parent ≈ units × ASP × GM − opex, ×(1−tax) ×51% Gladia stake, + one-off bargain gain\n")
    w("| Scenario | Units handed FY26 | Revenue | NPAT to parent (incl ₫285bn one-off) | vs plan 1,500 / stretch 2,500 |")
    w("|---|---:|---:|---:|---|")
    for name, units in m["scenarios_units_handed_fy26"].items():
        rev = units * m["asp_per_unit_bn"]
        pbt = rev * m["gross_margin"] - m["annual_opex_other"]
        npat_parent = pbt * (1 - m["tax_rate"]) * m["kdh_stake_gladia"] + m["one_off_bargain_gain"]
        vs = "≈ plan" if abs(npat_parent - act["company_plan_npat"]) < 250 else (
            "≈ stretch" if npat_parent > 2000 else "misses plan")
        w(f"| {name} | {units} | {vnd(rev)} | {vnd(npat_parent)} | {vs} |")
    sold = int(act["units_sold_pct_of_226"] * m["gladia_lowrise_units_total"])
    w(f"\n- Reality check: {sold} units sold by end-Q1, {act['units_handed_cumulative']} handed. "
      f"Base case needs ~{m['scenarios_units_handed_fy26']['base'] - act['units_handed_cumulative']} more handovers in 9 months — "
      "requires selling out the low-rise AND handing it over. Watch `customer advances` (₫688.6bn at Q1) build each quarter.")
    ann_int = act["capitalized_interest_q1"] * 4
    w(f"- Leverage tracker: debt ₫{vnd(act['debt'])}bn; capitalized interest run-rate ≈ ₫{vnd(ann_int)}bn/yr "
      f"= {ann_int/act['company_plan_npat']*100:.0f}% of planned NPAT — deferred into inventory, not avoided.")
    w("- Kill-criteria check (Layer 3): advances < ₫1,000bn by 3Q26 with Heights launched ⇒ bear branch confirmed.\n")


# ---------------------------------------------------------------- banks
def bank(key, name):
    m, act = A[key]["model"], A[key]["actuals"]
    start = m.get("loans_start_fy") or m.get("credit_start_fy")
    mid = m["loans_mid_fy"]
    w(f"## {name} — quota × NIM × credit-cost grid (H2 modeled, anchored on H1 actual)\n")
    w("H2 PBT ≈ TOI_H2×(1−CIR) − credit_cost/2 × avg H2 loans; TOI = NII/(1−non-interest share). FY = H1 actual + H2.\n")
    w("| Scenario | FY credit growth | NIM | Credit cost | H2 PBT | FY PBT | % of target |")
    w("|---|---:|---:|---:|---:|---:|---:|")
    tgt = act.get("guidance_pbt") or [act.get("target_pbt")]
    top = tgt[-1] or tgt[0]
    for s in ("bear", "base", "bull"):
        g = m["scenarios"]["credit_growth_fy"][s]
        nim = m["scenarios"]["nim_fy"][s]
        cc = m["scenarios"]["credit_cost"][s]
        end = start * (1 + g)
        avg_h2 = (mid + end) / 2
        nii_h2 = avg_h2 * nim / 2
        toi_h2 = nii_h2 / (1 - m["noninterest_share_of_toi"])
        h2 = toi_h2 * (1 - m["cir"]) - cc / 2 * avg_h2
        fy = act["h1_pbt"] + h2
        w(f"| {s} | {g*100:.0f}% | {nim*100:.2f}% | {cc*100:.2f}% | {vnd(h2)} | {vnd(fy)} | {fy/top*100:.0f}% |")
    w(f"\n- Company guidance/target: ₫{' – '.join(vnd(t) for t in tgt if t)}bn. "
      f"H1 actual ₫{vnd(act['h1_pbt'])}bn = {act['h1_pbt']/top*100:.0f}% of the top target.")
    if key == "vpb":
        w("- Sensitivity that matters: each +0.2% of credit cost ≈ −₫2.3tn PBT — FE Credit NPL formation is the swing factor.")
    else:
        w("- Sensitivity that matters: NIM ±0.1% ≈ ±₫1.3tn PBT; the CASA franchise is the margin defense.")
    w("")


# ---------------------------------------------------------------- brokers
def tcx():
    m, act = A["tcx"]["model"], A["tcx"]["actuals"]
    w("## 5 · TCX — margin-engine model + FTSE event tree\n")
    w("| Scenario | H2 avg margin book | Spread | H2 PBT | FY PBT | vs plan 7,535 |")
    w("|---|---:|---:|---:|---:|---|")
    for s, sc in m["h2_scenarios"].items():
        margin_nii = sc["avg_margin_book"] * sc["margin_spread"] / 2
        other = (act["h1_pbt"] - m["h1_margin_interest_est"]) * sc["other_income_vs_h1"]
        h2_pbt = margin_nii + other * 1.0
        fy = act["h1_pbt"] + h2_pbt
        w(f"| {s} | {vnd(sc['avg_margin_book'])} | {sc['margin_spread']*100:.1f}% | {vnd(h2_pbt)} | {vnd(fy)} | {fy/act['fy_plan_pbt']*100:.0f}% |")
    ev = sum(b["p"] * b["price_move"] for b in A["tcx"]["ftse_event_tree"])
    w("\n**Sep 21 FTSE event tree (Layer 2 — probabilities are the assumption):**")
    for b in A["tcx"]["ftse_event_tree"]:
        w(f"- {b['name']}: p={b['p']:.0%}, price move {b['price_move']:+.0%}")
    w(f"- **Expected value of the event ≈ {ev:+.1%}** — positive but modest; the position pays if the *base business* keeps compounding, the event is a kicker not a thesis.\n")


def vpx():
    m, act = A["vpx"]["model"], A["vpx"]["actuals"]
    w("## 6 · VPX — earnings-quality split + CAEX option\n")
    w("H1 PBT ₫2,673bn splits ≈ core ₫1,200bn + FVTPL-driven ₫1,473bn (marks, not fees) — model them separately:\n")
    w("| Scenario | H2 core vs H1 | H2 FVTPL vs H1 | FY PBT | vs plan 6,453 |")
    w("|---|---:|---:|---:|---|")
    for s, sc in m["h2_scenarios"].items():
        h2 = m["h1_core_pbt_est"] * sc["core_pbt_vs_h1"] + \
             act["h1_fvtpl_gains"] * sc["fvtpl_vs_h1"] * m["fvtpl_flowthrough_to_pbt"]
        fy = act["h1_pbt"] + h2
        w(f"| {s} | {sc['core_pbt_vs_h1']:.1f}x | {sc['fvtpl_vs_h1']:.1f}x | {vnd(fy)} | {fy/act['fy_plan_pbt']*100:.0f}% |")
    ev = sum(b["p"] * b["price_move"] for b in A["vpx"]["caex_option"])
    w("\n**CAEX crypto-license option:** " + " · ".join(
        f"{b['name']} p={b['p']:.0%} → {b['price_move']:+.0%}" for b in A["vpx"]["caex_option"]))
    w(f"- Option EV ≈ {ev:+.1%}. Note the asymmetry vs TCX: VPX's risk is earnings QUALITY (FVTPL), TCX's is MULTIPLE.\n")


# ---------------------------------------------------------------- HPG
def hpg():
    m, act = A["hpg"]["model"], A["hpg"]["actuals"]
    w("## 7 · HPG — volume × spread model\n")
    w("FY NPAT = Q1 actual (₫9,056bn incl ₫4,123bn one-off divestment gain) + remaining volume × core NPAT/tonne\n")
    w("| Scenario | Q2–Q4 volume (m t) | Core NPAT/t (₫m) | FY NPAT | vs target 22,000 | vs street 18–28k |")
    w("|---|---:|---:|---:|---|---|")
    for s in ("bear", "base", "bull"):
        vol = m["remaining_volume_mt"][s]
        per_t = m["core_npat_per_tonne_m"][s]
        fy = act["q1_npat"] + vol * per_t * 1000
        pos = "low end" if fy < 23000 else ("mid" if fy < 27000 else "high end")
        w(f"| {s} | {vol} | {per_t} | {vnd(fy)} | {fy/act['fy_target_npat']*100:.0f}% | {pos} |")
    w("\n- Q1 core ≈ ₫1.68m/tonne. The bear case IS the early-July domestic HRC price cuts — watch the spread, not volume.")
    w("- Jul 28 US rebar final: headline risk only (~3% of revenue) — a red print that day is a Layer-4 flag, not a model input.\n")


def main():
    w(f"# Model Snapshot — generated from assumptions.json (as of {A['_meta']['as_of']})\n")
    w("> Regenerate: `python3 research/models/run.py` · Edit beliefs in `assumptions.json` — "
      "git history of that file IS the record of how your views changed.\n")
    portfolio()
    kdh()
    w("## 3 · TCB" + "" if False else "")
    bank("tcb", "3 · TCB")
    bank("vpb", "4 · VPB")
    tcx()
    vpx()
    hpg()
    w("---")
    w("*Models beat your inconsistency, not the market. Layer-4 items (governance, quota politics, "
      "the An Lap seller question) are NOT in these numbers — see dossiers and monitoring log.*")
    (HERE / "SNAPSHOT.md").write_text("\n".join(OUT) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
