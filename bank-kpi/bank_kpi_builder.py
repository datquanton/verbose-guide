"""Build the bank KPI template (one sheet per bank) from FiinQuant MCP JSON dumps.

Usage:
    python bank_kpi_builder.py RAW_DIR OUT.xlsx

RAW_DIR holds raw (response_format=raw) MCP outputs, any number of files per kind,
multi-ticker allowed:
    is_a_*.json  bs_a_*.json  cf_a_*.json  ratios_a_*.json   annual statements/ratios
    is_q_*.json  (8 quarters ending at the latest quarter, for LTM and prior LTM)
    bs_q_*.json  (latest quarter and the same quarter a year earlier)
    ratios_q_*.json (latest quarter)
    prices_*.json (daily, adjusted=false, fields close + value)

Every metric is computed from statement lines with the formula listed in the
Definitions sheet, except NPL / Group 2 / CASA / credit growth, which come from
FiinPro's ratio feed because loan classification is not in the statements.
"""
import glob
import json
import os
import sys
from collections import defaultdict
from datetime import date

from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, Reference, Series
from openpyxl.chart.data_source import StrRef
from openpyxl.chart.series import SeriesLabel
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.formatting.rule import FormulaRule, Rule
from openpyxl.styles.differential import DifferentialStyle
from openpyxl.styles.numbers import NumberFormat
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

BN = 1e9
SECTION_FILL = PatternFill("solid", fgColor="E6B8B7")
HEADER_FILL = PatternFill("solid", fgColor="1F3864")
WHITE_BOLD = Font(bold=True, color="FFFFFF")
GREY = Font(color="808080", size=9)

BANKS = ["VCB", "BID", "CTG", "TCB", "MBB", "VPB", "ACB", "HDB", "STB", "LPB", "SHB", "VIB", "TPB", "SSB",
         "MSB", "OCB", "EIB", "NAB", "VBB", "BVB", "ABB", "BAB", "KLB", "NVB", "PGB", "SGB", "VAB"]


# ---------- loading ----------

def load(raw_dir, kind):
    out = defaultdict(dict)
    for path in sorted(glob.glob(os.path.join(raw_dir, f"{kind}_*.json"))):
        with open(path, encoding="utf-8") as f:
            for rec in json.load(f)["data"]["records"]:
                out[rec["ticker"]][(rec["year"], rec["quarter"])] = rec
    return out


def dig(node, *path):
    for p in path:
        if isinstance(node, list):
            node = node[0] if node else None
        if not isinstance(node, dict):
            return None
        node = node.get(p)
    return node


def bs_items(rec):
    if rec is None:
        return None
    b = dig(rec, "financial_statement", "balance_sheet")
    a, l = dig(b, "total_assets"), dig(b, "liabilities_and_shareholder_s_equity", "total_liabilities")
    ta, tl = dig(a, "total_assets"), dig(l, "total_liabilities")
    if ta is None or tl is None:
        return None
    nz = lambda v: v or 0
    te = ta - tl
    mi = nz(dig(b, "minority_interest"))
    loans = nz(dig(a, "loans_and_advances_to_customers_net", "loans_and_advances_to_customers"))
    iea = (nz(dig(a, "balances_with_the_sbv"))
           + nz(dig(a, "placements_with_and_loans_to_other_credit_institutions", "balances_with_other_credit_institutions"))
           + nz(dig(a, "placements_with_and_loans_to_other_credit_institutions", "loans_to_other_credit_institutions"))
           + nz(dig(a, "trading_securities_net", "trading_securities"))
           + loans
           + nz(dig(a, "debt_buying", "debt_buying"))
           + nz(dig(a, "investment_securities", "available_for_sales_securities"))
           + nz(dig(a, "investment_securities", "held_to_maturity_securities")))
    dep = nz(dig(l, "deposits_from_customers"))
    papers = nz(dig(l, "convertible_bonds_c_ds_and_other_valuable_papers_issued"))
    ibl = (nz(dig(l, "due_to_gov_and_loans_from_sbv"))
           + nz(dig(l, "deposits_and_loans_from_other_credit_institutions", "total_deposits_and_loans_from_other_credit_institutions"))
           + dep + nz(dig(l, "funds_received_from_gov_international_and_other_institutions")) + papers)
    return {
        "inv": nz(dig(a, "investment_securities", "available_for_sales_securities")) + nz(dig(a, "investment_securities", "held_to_maturity_securities")),
        "ta": ta, "te": te, "pe": te - mi, "loans": loans, "dep": dep, "papers": papers, "iea": iea, "ibl": ibl,
        "prov_loans": -nz(dig(a, "loans_and_advances_to_customers_net", "less_provision_for_losses_on_loans_and_advances_to_customers")),
        "accrued_int": nz(dig(a, "other_assets", "accrued_interest_and_fee_receivables")),
        "charter": nz(dig(b, "liabilities_and_shareholder_s_equity", "owner_s_equity", "capital", "charter_capital")),
    }


IS_FIELDS = {
    "ii": ("net_interest_income", "interest_and_similar_income"),
    "ie": ("net_interest_income", "interest_and_similar_expenses"),
    "nii": ("net_interest_income", "total_net_interest_income"),
    "nsi": ("net_fee_and_commission_income", "total_net_fee_and_commission_income"),
    "toi": ("total_operating_income",),
    "opex": ("general_and_admin_expenses",),
    "ppop": ("net_operating_profit_before_allowance_for_credit_loss",),
    "prov": ("provision_for_credit_losses",),
    "pbt": ("net_accounting_profit_loss_before_tax",),
    "npat": ("net_profit_loss_after_tax",),
    "npat_parent": ("attributable_to_parent_company",),
}


def is_items(rec):
    if rec is None:
        return None
    s = dig(rec, "financial_statement", "income_statement")
    out = {k: dig(s, *p) for k, p in IS_FIELDS.items()}
    if out["toi"] is None:
        return None
    out = {k: (v or 0) for k, v in out.items()}
    out["noi"] = out["toi"] - out["nii"] - out["nsi"]
    return out


def sum_is(recs):
    items = [is_items(r) for r in recs]
    if len(items) != 4 or any(i is None for i in items):
        return None
    return {k: sum(i[k] for i in items) for k in items[0]}


def cf_items(rec):
    if rec is None:
        return None
    c = dig(rec, "financial_statement", "cash_flow")
    wo = dig(c, "increase_decrease_in_operating_assets", "increase_decrease_in_provision_for_loan_losses")
    rec_ = dig(c, "cash_flows_from_operating_activities", "receipts_from_debts_written_off_or_paid_off_by_risk_fund")
    return {"wo": -(wo or 0), "rec": rec_ or 0}


def ratio_items(rec):
    if rec is None:
        return None
    r = rec["ratios"]
    return {
        # Problem-loan ratio matches the NPL banks report (checked vs TCB FY23-25); category field as fallback.
        "npl": dig(r, "2_asset_quality_component", "problem_loans_and_leases_sum_of_doubtful_and_non_performing_loans_calculated_as_a_percentage_of_gross_loans")
        or dig(r, "4_liquidity_and_assets_component", "debt_category_3_5_gross_loan_to_customer"),
        "g25": dig(r, "4_liquidity_and_assets_component", "debt_category_2_5_gross_loan_to_customer"),
        "casa": dig(r, "2_asset_quality_component", "casa_ratio"),
        "credit_g": dig(r, "6_growth_component", "credit_growth_yo_y"),
        "nim_fiin": dig(r, "5_profitability_component", "nim"),
        "car": dig(r, "1_capital_adequacy_component", "car"),
    }


def load_prices(raw_dir):
    px = defaultdict(list)
    for path in sorted(glob.glob(os.path.join(raw_dir, "prices_*.json"))):
        with open(path, encoding="utf-8") as f:
            for r in json.load(f)["data"]["records"]:
                if r.get("close") is not None:
                    px[r["ticker"]].append((r["timestamp"][:10], r["close"], r.get("value") or 0))
    for t in px:
        px[t].sort()
    return px


def close_on_or_before(series, day):
    last = None
    for d, c, _ in series:
        if d > day:
            break
        last = (d, c)
    if last is None or (date.fromisoformat(day) - date.fromisoformat(last[0])).days > 10:
        return None
    return last


def adtv(series, start, end):
    vals = [v for d, _, v in series if start <= d <= end]
    return sum(vals) / len(vals) if vals else None


# ---------- metrics ----------

def div(a, b):
    if a is None or b in (None, 0):
        return None
    return a / b


def avg(a, b):
    if a is None or b is None:
        return None
    return (a + b) / 2


def growth(cur, prev):
    if cur is None or prev in (None, 0):
        return None
    return cur / prev - 1 if prev > 0 else None


ROWS = [
    ("BALANCE SHEET & ASSET QUALITY", None, None, None),
    ("NPL", "npl", "pct", "Group 3-5 / gross customer loans (FiinPro ratio feed)"),
    ("Group 2", "g2", "pct", "(Group 2-5 − Group 3-5) / gross loans (FiinPro ratio feed)"),
    ("LLR", "llr", "pct", "Loan-loss provisions / Group 3-5 loans"),
    ("Credit Cost", "credit_cost", "pct", "Provision expense (P&L, all credit provisions) / avg gross loans"),
    ("PD (1yrs)", "pd", "pct", "(NPL abs. t − NPL abs. t−1 + write-offs t) / performing loans t−1"),
    ("Recovery rates (5yrs)", "recovery", "pct", "Σ5y recoveries of written-off debt / Σ5y write-offs (CF: use of provisions)"),
    ("Accrued interest/IEA", "accrued_iea", "pct", "Accrued interest & fee receivables / avg interest-earning assets"),
    ("LDR (proxy)", "ldr", "pct", "Gross loans / (customer deposits + valuable papers) — consolidated proxy, NOT the TT22 regulatory LDR"),
    ("CAR (disclosed)", "car", "pct", "FiinPro ratio feed (as disclosed); null for some banks and for the latest quarter"),
    ("CASA", "casa", "pct", "Non-term deposits / total customer deposits (FiinPro ratio feed)"),
    ("Leverage", "leverage", "pct", "Total equity / total assets"),
    ("GROWTH", None, None, None),
    ("Assets", "g_ta", "pct", "Total assets YoY"),
    ("Credit", "g_credit", "pct", "Credit growth YoY (FiinPro ratio feed; loans + corporate bonds per FiinPro)"),
    ("Loans", "g_loans", "pct", "Gross customer loans YoY"),
    ("Depo.", "g_dep", "pct", "Customer deposits YoY"),
    ("Valuable Papers", "g_papers", "pct", "Bonds + CDs + other valuable papers issued YoY"),
    ("Equity", "g_te", "pct", "Total equity YoY"),
    ("NII", "g_nii", "pct", "Net interest income YoY"),
    ("NSI", "g_nsi", "pct", "Net fee & commission (service) income YoY"),
    ("NOI", "g_noi", "pct", "Other non-interest income (TOI − NII − NSI) YoY; negative base → blank"),
    ("PPOP", "g_ppop", "pct", "Pre-provision operating profit YoY"),
    ("PBT", "g_pbt", "pct", "Profit before tax YoY"),
    ("EFFICIENCY & VALUATION", None, None, None),
    ("Loans yield", "loan_yield", "pct", "Interest income / avg (gross loans + investment securities)"),
    ("Cost of funds", "cof", "pct", "Interest expense / avg interest-bearing liabilities (deposits + interbank + papers + gov/SBV)"),
    ("Net interest spread (NIS)", "nis", "pct", "Interest income / avg IEA − cost of funds (IEA = SBV + interbank + securities + loans)"),
    ("Net interest margin (NIM)", "nim", "pct", "NII / avg interest-earning assets"),
    ("Non-NII to TOI", "nonnii_toi", "pct", "(NSI + NOI) / TOI"),
    ("CIR", "cir", "pct", "Operating expenses / TOI"),
    ("ROA", "roa", "pct", "NPAT / avg total assets"),
    ("ROE", "roe", "pct", "NPAT to parent / avg parent equity"),
    ("P/B", "pb", "x", "Market cap at period end (unadjusted close × charter capital/10,000) / parent equity"),
    ("P/E", "pe", "x", "Market cap / NPAT to parent (LTM for latest column)"),
    ("Target price/BVPS (F)", None, "x", "Analyst input"),
    ("Target price", None, "num", "Analyst input"),
    ("MARKET", None, None, None),
    ("ADTV (bn VND)", "adtv", "num", "Average daily traded value over the period (matched + put-through as supplied)"),
    ("ADTV to market cap", "adtv_mcap", "pct", "ADTV / period-end market cap (free-float history not available in API)"),
    ("Interbank rate", None, "pct", "Not in FiinPro API — macro input"),
    ("Deposits rates", None, "pct", "Not in FiinPro API — macro input"),
    ("Banks Liquidity", None, "pct", "Not in FiinPro API — macro input"),
]


def compute_period(cur, prev, prev2_ratio, is_cur, is_prev, cf_hist, rat, rat_prev, px, end_day, start_day):
    """cur/prev: balance-sheet dicts at period end and one year earlier."""
    m = {}
    if cur is None or is_cur is None:
        return m
    npl = rat and rat.get("npl")
    npl_abs = npl * cur["loans"] if npl is not None else None
    m["npl"] = npl
    if rat and rat.get("g25") is not None and npl is not None:
        m["g2"] = rat["g25"] - npl
    m["llr"] = div(cur["prov_loans"], npl_abs)
    avg_loans = avg(cur["loans"], prev and prev["loans"])
    m["credit_cost"] = div(-is_cur["prov"], avg_loans)
    if prev and rat_prev and rat_prev.get("npl") is not None and npl_abs is not None and cf_hist and cf_hist[-1]:
        npl_prev_abs = rat_prev["npl"] * prev["loans"]
        m["pd"] = div(npl_abs - npl_prev_abs + cf_hist[-1]["wo"], prev["loans"] - npl_prev_abs)
    if cf_hist and len(cf_hist) == 5 and all(cf_hist):
        m["recovery"] = div(sum(c["rec"] for c in cf_hist), sum(c["wo"] for c in cf_hist))
    avg_iea = avg(cur["iea"], prev and prev["iea"])
    m["accrued_iea"] = div(cur["accrued_int"], avg_iea)
    m["ldr"] = div(cur["loans"], cur["dep"] + cur["papers"])
    m["car"] = (rat and rat.get("car")) or None  # provider reports 0 when missing
    m["casa"] = rat and rat.get("casa")
    m["leverage"] = div(cur["te"], cur["ta"])
    if prev:
        for k, f in [("g_ta", "ta"), ("g_loans", "loans"), ("g_dep", "dep"), ("g_papers", "papers"), ("g_te", "te")]:
            m[k] = growth(cur[f], prev[f])
    m["g_credit"] = rat and rat.get("credit_g")
    if is_prev:
        for k, f in [("g_nii", "nii"), ("g_nsi", "nsi"), ("g_noi", "noi"), ("g_ppop", "ppop"), ("g_pbt", "pbt")]:
            m[k] = growth(is_cur[f], is_prev[f])
    m["yield"] = div(is_cur["ii"], avg_iea)
    m["loan_yield"] = div(is_cur["ii"], avg(cur["loans"] + cur["inv"], prev and prev["loans"] + prev["inv"]))
    m["cof"] = div(-is_cur["ie"], avg(cur["ibl"], prev and prev["ibl"]))
    if m["yield"] is not None and m["cof"] is not None:
        m["nis"] = m["yield"] - m["cof"]
    m["nim"] = div(is_cur["nii"], avg_iea)
    m["nonnii_toi"] = div(is_cur["toi"] - is_cur["nii"], is_cur["toi"])
    m["cir"] = div(-is_cur["opex"], is_cur["toi"])
    m["roa"] = div(is_cur["npat"], avg(cur["ta"], prev and prev["ta"]))
    m["roe"] = div(is_cur["npat_parent"], avg(cur["pe"], prev and prev["pe"]))
    close = close_on_or_before(px, end_day) if px else None
    if close and cur["charter"]:
        mcap = close[1] * cur["charter"] / 10_000
        m["pb"] = div(mcap, cur["pe"]) if cur["pe"] > 0 else None
        pe = div(mcap, is_cur["npat_parent"]) if is_cur["npat_parent"] > 0 else None
        m["pe"] = pe if pe is not None and pe <= 100 else None  # >100x is not meaningful
        a = adtv(px, start_day, end_day)
        m["adtv"] = a / BN if a else None
        m["adtv_mcap"] = div(a, mcap)
        m["_close"] = close
    return m


def drop_stale_copies(series, t, label, flags, signature):
    """Provider sometimes repeats last year's statement under a new year; blank the copy."""
    out = dict(series)
    for (y, q), rec in series.items():
        prior = series.get((y - 1, q))
        sig = signature(rec)
        if prior is not None and sig and any(sig.values()) and sig == signature(prior):
            out.pop((y, q))
            flags.append((t, f"FY{y}" if q == 5 else f"{q}Q{y}", f"{label} identical to prior year (provider copy) — period blanked"))
    return out


def build_bank(t, D, px, years, latest_q, flags):
    cols = {}
    core = lambda r: {k: round(v / BN) for k, v in (bs_items(r) or {}).items() if k in ("ta", "loans", "dep", "te")}
    bs_a = drop_stale_copies(D["bs_a"][t], t, "Balance sheet", flags, core)
    is_a = drop_stale_copies(D["is_a"][t], t, "Income statement", flags, is_items)
    cf_a = drop_stale_copies(D["cf_a"][t], t, "Cash flow", flags, cf_items)
    r_a = D["ratios_a"][t]
    for y in years:
        cur, prev = bs_items(bs_a.get((y, 5))), bs_items(bs_a.get((y - 1, 5)))
        cf_hist = [cf_items(cf_a.get((yy, 5))) for yy in range(y - 4, y + 1)]
        cols[f"FY{y}"] = compute_period(
            cur, prev, None, is_items(is_a.get((y, 5))), is_items(is_a.get((y - 1, 5))),
            cf_hist, ratio_items(r_a.get((y, 5))), ratio_items(r_a.get((y - 1, 5))),
            px, f"{y}-12-31", f"{y}-01-01")
    ly, lq = latest_q
    end = ly * 4 + lq - 1
    qkeys = [(i // 4, i % 4 + 1) for i in range(end - 3, end + 1)]
    pkeys = [(y - 1, q) for y, q in qkeys]
    is_q = D["is_q"][t]
    for k in qkeys:
        i = is_items(is_q.get(k))
        if i and i["toi"] > 0 and i["npat"] > i["toi"]:
            flags.append((t, f"{k[1]}Q{k[0]}", f"NPAT {i['npat'] / BN:,.0f}bn exceeds TOI {i['toi'] / BN:,.0f}bn — one-off or provider error; LTM column affected"))
    ltm, ltm_prev = sum_is([is_q.get(k) for k in qkeys]), sum_is([is_q.get(k) for k in pkeys])
    cur, prev = bs_items(D["bs_q"][t].get((ly, lq))), bs_items(D["bs_q"][t].get((ly - 1, lq)))
    rat = ratio_items(D["ratios_q"][t].get((ly, lq)))
    m = compute_period(cur, prev, None, ltm, ltm_prev, None, rat, None, px,
                       date.today().isoformat(), (date.today().replace(year=date.today().year - 1)).isoformat())
    cols[f"LTM {lq}Q{str(ly)[2:]}"] = m
    return cols


# ---------- writing ----------

def fmt_cell(cell, kind):
    cell.number_format = {"pct": "0.0%", "x": "0.00", "num": "#,##0"}.get(kind, "General")
    cell.alignment = Alignment(horizontal="right")


# ---------- bilingual labels ----------

LANG = "Search!$B$3"  # EN / VI switch, read by every sheet

VI = {
    "BALANCE SHEET & ASSET QUALITY": "BẢNG CÂN ĐỐI & CHẤT LƯỢNG TÀI SẢN",
    "GROWTH": "TĂNG TRƯỞNG",
    "EFFICIENCY & VALUATION": "HIỆU QUẢ & ĐỊNH GIÁ",
    "MARKET": "THỊ TRƯỜNG",
    "NPL": "Tỷ lệ nợ xấu (NPL)",
    "Group 2": "Nợ nhóm 2",
    "LLR": "Bao phủ nợ xấu (LLR)",
    "Credit Cost": "Chi phí tín dụng",
    "PD (1yrs)": "Xác suất vỡ nợ 1 năm (PD)",
    "Recovery rates (5yrs)": "Tỷ lệ thu hồi nợ đã xử lý (5 năm)",
    "Accrued interest/IEA": "Lãi dự thu / TS sinh lãi",
    "LDR (proxy)": "Cho vay / Huy động (LDR, ước tính)",
    "CAR (disclosed)": "Hệ số an toàn vốn (CAR)",
    "CASA": "Tỷ lệ CASA",
    "Leverage": "VCSH / Tổng tài sản",
    "Assets": "TT Tổng tài sản",
    "Credit": "TT Tín dụng",
    "Loans": "TT Cho vay",
    "Depo.": "TT Tiền gửi KH",
    "Valuable Papers": "TT Giấy tờ có giá",
    "Equity": "TT Vốn chủ sở hữu",
    "NII": "TT Thu nhập lãi thuần",
    "NSI": "TT Lãi thuần dịch vụ",
    "NOI": "TT Thu nhập ngoài lãi khác",
    "PPOP": "TT LN trước dự phòng",
    "PBT": "TT LN trước thuế",
    "Loans yield": "Lợi suất cho vay",
    "Cost of funds": "Chi phí vốn",
    "Net interest spread (NIS)": "Chênh lệch lãi suất (NIS)",
    "Net interest margin (NIM)": "Biên lãi ròng (NIM)",
    "Non-NII to TOI": "Thu nhập ngoài lãi / TOI",
    "CIR": "Chi phí / Thu nhập (CIR)",
    "ROA": "ROA",
    "ROE": "ROE",
    "P/B": "P/B",
    "P/E": "P/E",
    "Target price/BVPS (F)": "Giá mục tiêu / BVPS (DB)",
    "Target price": "Giá mục tiêu",
    "ADTV (bn VND)": "GTGD bình quân ngày (tỷ đồng)",
    "ADTV to market cap": "GTGD bình quân / Vốn hóa",
    "Interbank rate": "Lãi suất liên ngân hàng",
    "Deposits rates": "Lãi suất huy động",
    "Banks Liquidity": "Thanh khoản hệ thống",
}

VI_DEF = {
    "NPL": "Nợ nhóm 3-5 / dư nợ cho vay KH (nguồn chỉ số FiinPro)",
    "Group 2": "(Nhóm 2-5 − Nhóm 3-5) / dư nợ cho vay (nguồn chỉ số FiinPro)",
    "LLR": "Dự phòng rủi ro cho vay / nợ nhóm 3-5",
    "Credit Cost": "Chi phí dự phòng (KQKD, toàn bộ dự phòng tín dụng) / dư nợ bình quân",
    "PD (1yrs)": "(Nợ xấu t − Nợ xấu t−1 + Xóa nợ t) / Dư nợ không xấu t−1",
    "Recovery rates (5yrs)": "Tổng thu hồi nợ đã xử lý 5 năm / Tổng xóa nợ 5 năm (LCTT: sử dụng dự phòng)",
    "Accrued interest/IEA": "Lãi và phí phải thu / TS sinh lãi bình quân",
    "LDR (proxy)": "Cho vay / (Tiền gửi KH + Giấy tờ có giá) — ước tính hợp nhất, KHÔNG phải LDR theo TT22",
    "CAR (disclosed)": "Nguồn chỉ số FiinPro (theo công bố); trống với một số NH và quý gần nhất",
    "CASA": "Tiền gửi không kỳ hạn / Tổng tiền gửi KH (nguồn chỉ số FiinPro)",
    "Leverage": "Tổng VCSH / Tổng tài sản",
    "Assets": "Tăng trưởng tổng tài sản so với cùng kỳ",
    "Credit": "Tăng trưởng tín dụng (cho vay + TPDN, nguồn FiinPro)",
    "Loans": "Tăng trưởng dư nợ cho vay KH",
    "Depo.": "Tăng trưởng tiền gửi khách hàng",
    "Valuable Papers": "Tăng trưởng trái phiếu + CD + giấy tờ có giá phát hành",
    "Equity": "Tăng trưởng tổng VCSH",
    "NII": "Tăng trưởng thu nhập lãi thuần",
    "NSI": "Tăng trưởng lãi thuần từ hoạt động dịch vụ",
    "NOI": "Tăng trưởng thu nhập ngoài lãi khác (TOI − NII − NSI); để trống khi kỳ gốc âm",
    "PPOP": "Tăng trưởng lợi nhuận trước dự phòng",
    "PBT": "Tăng trưởng lợi nhuận trước thuế",
    "Loans yield": "Thu nhập lãi / bình quân (cho vay + chứng khoán đầu tư)",
    "Cost of funds": "Chi phí lãi / bình quân nợ chịu lãi (tiền gửi + liên NH + GTCG + NHNN)",
    "Net interest spread (NIS)": "Thu nhập lãi / TS sinh lãi bình quân − chi phí vốn",
    "Net interest margin (NIM)": "Thu nhập lãi thuần / TS sinh lãi bình quân",
    "Non-NII to TOI": "(Lãi thuần dịch vụ + thu nhập khác) / Tổng thu nhập hoạt động",
    "CIR": "Chi phí hoạt động / Tổng thu nhập hoạt động",
    "ROA": "LNST / Tổng tài sản bình quân",
    "ROE": "LNST cổ đông công ty mẹ / VCSH công ty mẹ bình quân",
    "P/B": "Vốn hóa cuối kỳ (giá chưa điều chỉnh × vốn điều lệ/10.000) / VCSH công ty mẹ",
    "P/E": "Vốn hóa / LNST cổ đông công ty mẹ (cột mới nhất: 4 quý gần nhất)",
    "Target price/BVPS (F)": "Nhập tay (chuyên viên phân tích)",
    "Target price": "Nhập tay (chuyên viên phân tích)",
    "ADTV (bn VND)": "Giá trị giao dịch bình quân ngày trong kỳ",
    "ADTV to market cap": "GTGD bình quân / vốn hóa cuối kỳ (không có lịch sử free-float)",
    "Interbank rate": "Không có trong API FiinPro — nhập dữ liệu vĩ mô",
    "Deposits rates": "Không có trong API FiinPro — nhập dữ liệu vĩ mô",
    "Banks Liquidity": "Không có trong API FiinPro — nhập dữ liệu vĩ mô",
}

LOWER_IS_BETTER = {"NPL", "Group 2", "Credit Cost", "PD (1yrs)", "Cost of funds", "CIR"}


def tr(en, vi, lang=LANG):
    """Formula that shows English or Vietnamese text depending on the language switch."""
    q = lambda s: s.replace('"', '""')
    return f'=IF({lang}="VI","{q(vi)}","{q(en)}")'


def write_bank_sheet(wb, t, name, cols):
    ws = wb.create_sheet(t)
    ws["A1"] = f"{t} — {name}"
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = tr(f"Source: FiinQuantX (FiinPro API) consolidated statements; built {date.today().isoformat()}. Latest column = last 4 reported quarters / latest balance sheet.",
                  f"Nguồn: FiinQuantX (API FiinPro), BCTC hợp nhất; cập nhật {date.today().isoformat()}. Cột mới nhất = 4 quý gần nhất / BCĐKT gần nhất.")
    ws["A2"].font = GREY
    periods = list(cols)
    hdr = 4
    ws.cell(hdr, 1, tr("Definition", "Định nghĩa"))
    ws.cell(hdr, 2, t)
    for j, p in enumerate(periods):
        ws.cell(hdr, 3 + j, p)
    for c in range(1, len(periods) + 3):
        ws.cell(hdr, c).fill, ws.cell(hdr, c).font = HEADER_FILL, WHITE_BOLD
    r = hdr + 1
    for label, key, kind, definition in ROWS:
        if key is None and kind is None:
            for c in range(1, len(periods) + 3):
                ws.cell(r, c).fill = SECTION_FILL
            ws.cell(r, 2, tr(label, VI[label])).font = Font(bold=True)
        else:
            ws.cell(r, 1, tr(definition, VI_DEF[label])).font = GREY
            ws.cell(r, 2, tr(label, VI[label])).font = Font(bold=True)
            for j, p in enumerate(periods):
                v = cols[p].get(key) if key else None
                if v is not None:
                    fmt_cell(ws.cell(r, 3 + j, v), kind)
        r += 1
    ws.column_dimensions["A"].width = 34
    ws.column_dimensions["B"].width = 30
    for c in range(3, len(periods) + 3):
        ws.column_dimensions[get_column_letter(c)].width = 10
    ws.freeze_panes = ws.cell(hdr + 1, 3)


UNIT = {"pct": "%", "x": "x", "num": "bn VND"}
LOOKUP_ROWS = 20
DEFAULT_LOOKUPS = [("TCB", "NPL"), ("TCB", "ROE"), ("TCB", "Net interest margin (NIM)"), ("TCB", "P/B"),
                   ("MBB", "NPL"), ("MBB", "ROE"), ("VCB", "NPL"), ("VCB", "ROE")]
INPUT = PatternFill("solid", fgColor="FFF2CC")
SEL_FILL = PatternFill("solid", fgColor="FCE4D6")
SERIES_COLORS = ["1F3864", "2E75B6", "70AD47", "ED7D31", "7F7F7F"]


def _median(vals):
    vals = sorted(v for v in vals if v is not None)
    if not vals:
        return None
    n = len(vals)
    return vals[n // 2] if n % 2 else (vals[n // 2 - 1] + vals[n // 2]) / 2


def _header(ws, row, heads, start_col=1):
    for j, h in enumerate(heads, start_col):
        c = ws.cell(row, j, h)
        c.fill, c.font = HEADER_FILL, WHITE_BOLD
        c.alignment = Alignment(horizontal="center")


def _section(ws, row, formula, ncols):
    for c in range(1, ncols + 1):
        ws.cell(row, c).fill = SECTION_FILL
    ws.cell(row, 1, formula).font = Font(bold=True, size=12)


def write_search(wb, results, names):
    """Search sheet driven by Bank / Metric / Period / Peers inputs; everything below is formulas."""
    metrics = [(label, kind) for label, key, kind, _ in ROWS if key]
    key_of = {label: key for label, key, kind, _ in ROWS if key}
    banks = list(results)
    periods = list(next(iter(results.values())))
    P = len(periods)

    # Data: one row per bank × metric (+ sector median), periods across from column E.
    data = wb.create_sheet("Data")
    data.append(["Key", "Bank", "Metric", "Unit"] + periods)
    for t in banks:
        for label, kind in metrics:
            data.append([f"{t}|{label}", t, label, UNIT[kind]] + [results[t][p].get(key_of[label]) for p in periods])
    for label, kind in metrics:
        data.append([f"MEDIAN|{label}", "MEDIAN", label, UNIT[kind]]
                    + [_median(results[t][p].get(key_of[label]) for t in banks) for p in periods])
    n = data.max_row
    data.sheet_state = "hidden"
    dcol = lambda j: get_column_letter(5 + j)  # Data column of period j
    keys = f"Data!$A$2:$A${n}"

    # Lists: A ticker, B name, C metric EN, D unit, E period, F EN def, G metric VI, H active label, I lower-is-better, J VI def
    lists = wb.create_sheet("Lists")
    tickers = banks + ["MEDIAN"]
    for i, t in enumerate(tickers, 2):
        lists.cell(i, 1, t)
        lists.cell(i, 2, names.get(t, "Sector median / Trung vị ngành"))
    defs = {label: d for label, key, kind, d in ROWS if key}
    for i, (label, kind) in enumerate(metrics, 2):
        lists.cell(i, 3, label)
        lists.cell(i, 4, UNIT[kind])
        lists.cell(i, 6, defs[label])
        lists.cell(i, 7, VI[label])
        lists.cell(i, 8, f'=IF({LANG}="VI",G{i},C{i})')
        lists.cell(i, 9, label in LOWER_IS_BETTER)
        lists.cell(i, 10, VI_DEF[label])
    for i, p in enumerate(periods, 2):
        lists.cell(i, 5, p)
    lists.cell(2, 11, "EN")
    lists.cell(3, 11, "VI")
    lists.sheet_state = "hidden"
    m_last = len(metrics) + 1

    ws = wb.create_sheet("Search", 1)
    wb.active = wb.index(ws)
    calc = wb.create_sheet("Calc")
    calc.sheet_state = "hidden"

    # --- inputs ---
    ws["A1"] = tr("Bank KPI search", "Tra cứu chỉ tiêu ngân hàng")
    ws["A1"].font = Font(bold=True, size=14)
    ws["A2"] = tr("Yellow cells are inputs — type to filter each dropdown. Everything below updates automatically.",
                  "Ô vàng là ô nhập — gõ để lọc danh sách. Toàn bộ bảng và biểu đồ bên dưới tự cập nhật.")
    ws["A2"].font = GREY
    labels = [("Language / Ngôn ngữ", "Language / Ngôn ngữ"), ("Bank", "Ngân hàng"), ("Metric", "Chỉ tiêu"),
              ("Period (ranking)", "Kỳ (xếp hạng)"), ("Peers", "So sánh với")]
    for i, (en, vi) in enumerate(labels, 3):
        ws.cell(i, 1, tr(en, vi)).font = Font(bold=True)
    ws["B3"], ws["B4"], ws["B5"], ws["B6"] = "EN", "TCB", "ROE", periods[-2]
    ws["B7"], ws["C7"], ws["D7"] = "MBB", "VCB", "ACB"
    for ref in ("B3", "B4", "B5", "B6", "B7", "C7", "D7"):
        ws[ref].fill = INPUT
        ws[ref].font = Font(bold=True)

    # canonical metric / unit / direction / scale live in Calc
    calc["A1"], calc["B1"] = "metric", f'=IFERROR(INDEX(Lists!$C$2:$C${m_last},MATCH(Search!$B$5,Lists!$C$2:$C${m_last},0)),IFERROR(INDEX(Lists!$C$2:$C${m_last},MATCH(Search!$B$5,Lists!$G$2:$G${m_last},0)),""))'
    calc["A2"], calc["B2"] = "unit", f'=IFERROR(INDEX(Lists!$D$2:$D${m_last},MATCH($B$1,Lists!$C$2:$C${m_last},0)),"")'
    calc["A3"], calc["B3"] = "lower", f'=IFERROR(INDEX(Lists!$I$2:$I${m_last},MATCH($B$1,Lists!$C$2:$C${m_last},0)),FALSE)'
    calc["A4"], calc["B4"] = "scale", '=IF($B$2="%",100,1)'
    calc["A5"], calc["B5"] = "label", f'=IFERROR(INDEX(Lists!$H$2:$H${m_last},MATCH($B$1,Lists!$C$2:$C${m_last},0)),Search!$B$5)'
    MET, LOWER, SCALE, MLABEL = "Calc!$B$1", "Calc!$B$3", "Calc!$B$4", "Calc!$B$5"

    ws["C4"] = f'=IFERROR(INDEX(Lists!$B:$B,MATCH($B$4,Lists!$A:$A,0)),IF({LANG}="VI","⚠ không tìm thấy mã","⚠ ticker not found"))'
    ws["C5"] = "=Calc!$B$2"
    ws["D5"] = (f'=IF({MET}="",IF({LANG}="VI","⚠ không tìm thấy chỉ tiêu","⚠ metric not found"),'
                f'IFERROR(INDEX(IF({LANG}="VI",Lists!$J$2:$J${m_last},Lists!$F$2:$F${m_last}),MATCH({MET},Lists!$C$2:$C${m_last},0)),""))')
    ws["C6"] = f'=IF({LOWER},IF({LANG}="VI","hạng 1 = thấp nhất","rank 1 = lowest"),IF({LANG}="VI","hạng 1 = cao nhất","rank 1 = highest"))'
    for ref in ("C4", "D5", "C6"):
        ws[ref].font = GREY
    ws["C5"].font = Font(bold=True)

    dv = lambda f: DataValidation(type="list", formula1=f, allow_blank=True)
    dv_lang, dv_bank, dv_metric, dv_period = dv(f"=Lists!$K$2:$K$3"), dv(f"=Lists!$A$2:$A${len(tickers) + 1}"), \
        dv(f"=Lists!$H$2:$H${m_last}"), dv(f"=Lists!$E$2:$E${P + 1}")
    for d in (dv_lang, dv_bank, dv_metric, dv_period):
        d.showErrorMessage = False  # allow free typing; lookups report "not found"
        ws.add_data_validation(d)
    dv_lang.add("B3")
    dv_bank.add("B4")
    dv_bank.add("B7:D7")
    dv_metric.add("B5")
    dv_period.add("B6")

    ncols = 3 + P
    UNIT_REF = "$C$5"

    # --- history table ---
    h0 = 9
    _section(ws, h0, f'=IF({LANG}="VI","Lịch sử: ","History: ")&{MLABEL}', ncols)
    _header(ws, h0 + 1, [tr("Bank", "Ngân hàng"), tr("Name", "Tên"), tr("Unit", "Đơn vị")] + periods)
    rows_src = ["=$B$4", '=IF($B$7="","",$B$7)', '=IF($C$7="","",$C$7)', '=IF($D$7="","",$D$7)', "MEDIAN"]
    hist = list(range(h0 + 2, h0 + 2 + len(rows_src)))
    for r, src in zip(hist, rows_src):
        ws.cell(r, 1, src).font = Font(bold=(r == hist[0]))
        ws.cell(r, 2, f'=IF(A{r}="","",IFERROR(INDEX(Lists!$B:$B,MATCH(A{r},Lists!$A:$A,0)),"?"))')
        ws.cell(r, 3, f'=IF(A{r}="","",{UNIT_REF})')
        for j in range(P):
            src_v = f"INDEX(Data!{dcol(j)}$2:{dcol(j)}${n},MATCH(A{r}&\"|\"&{MET},{keys},0))"
            c = ws.cell(r, 4 + j, f'=IF(A{r}="","",IFERROR(IF({src_v}="","",{src_v}),""))')
            c.number_format = "0.0%"
            c.font = Font(bold=(r == hist[0]))
    rng = f"D{hist[0]}:{get_column_letter(3 + P)}{hist[-1]}"
    _unit_formats(ws, rng, UNIT_REF)
    for c in range(1, ncols + 1):
        ws.cell(hist[0], c).fill = SEL_FILL

    # chart data: time series
    calc.cell(7, 1, "series")
    for j, p in enumerate(periods):
        calc.cell(7, 2 + j, p)
    for i, r in enumerate(hist):
        cr = 8 + i
        calc.cell(cr, 1, f'=IF(Search!A{r}="","",IF(Search!A{r}="MEDIAN",IF({LANG}="VI","Trung vị ngành","Sector median"),Search!A{r}))')
        for j in range(P):
            col = get_column_letter(4 + j)
            calc.cell(cr, 2 + j, f'=IF(ISNUMBER(Search!{col}{r}),Search!{col}{r}*{SCALE},NA())')

    cap = h0 + 2 + len(rows_src) + 1
    unit_txt = f'IF($C$5="%",IF({LANG}="VI","% (×100)","% (×100)"),$C$5)'
    ws.cell(cap, 1, f'=IF({LANG}="VI","Biểu đồ lịch sử: ","Time series: ")&{MLABEL}&" — "&$B$4&" vs peers · "&{unit_txt}').font = Font(bold=True)
    ws.cell(cap, 10, f'=IF({LANG}="VI","Toàn ngành: ","All banks: ")&{MLABEL}&" · "&$B$6&" · "&{unit_txt}&IF({LANG}="VI"," · "&$B$4&" tô cam"," · "&$B$4&" in orange")').font = Font(bold=True)

    line = LineChart()
    line.title = None
    line.height, line.width = 9, 17
    line.y_axis.number_format = "0.0"
    line.y_axis.majorGridlines = None
    line.x_axis.delete = False
    line.y_axis.delete = False
    line.legend.position = "b"
    line.display_blanks = "gap"
    line.visible_cells_only = False
    for i in range(len(rows_src)):
        cr = 8 + i
        s = Series(Reference(calc, min_col=2, max_col=1 + P, min_row=cr), title=None)
        s.tx = SeriesLabel(strRef=StrRef(f"'Calc'!$A${cr}"))
        s.graphicalProperties.line.solidFill = SERIES_COLORS[i]
        s.graphicalProperties.line.width = 38000 if i == 0 else 19000
        if i == len(rows_src) - 1:
            s.graphicalProperties.line.dashStyle = "dash"
        s.marker.symbol = "circle" if i == 0 else "none"
        s.marker.size = 5
        s.smooth = False
        line.series.append(s)
    line.set_categories(Reference(calc, min_col=2, max_col=1 + P, min_row=7))
    ws.add_chart(line, f"A{cap + 1}")

    # --- rank table + sorted bar chart data ---
    k0 = cap + 20
    _section(ws, k0, f'=IF({LANG}="VI","Xếp hạng toàn ngành: ","Rank all banks: ")&{MLABEL}&" · "&$B$6', ncols)
    _header(ws, k0 + 1, [tr("Bank", "Ngân hàng"), tr("Name", "Tên"), tr("Value", "Giá trị"), tr("Rank", "Hạng")])
    rf, rl = k0 + 2, k0 + 1 + len(banks)
    period_col = f"MATCH($B$6,Data!$1:$1,0)"
    for i, t in enumerate(banks):
        r = rf + i
        ws.cell(r, 1, t)
        ws.cell(r, 2, names.get(t, ""))
        src = f"INDEX(Data!$A$1:${dcol(P - 1)}${n},MATCH($A{r}&\"|\"&{MET},Data!$A$1:$A${n},0),{period_col})"
        c = ws.cell(r, 3, f'=IFERROR(IF({src}="","",{src}),"")')
        c.number_format = "0.0%"
        ws.cell(r, 4, f'=IF(C{r}="","",IF({LOWER},RANK(C{r},$C${rf}:$C${rl},1),RANK(C{r},$C${rf}:$C${rl},0)))')
        # Calc rows 20.. : sort key, sorted ticker, value (others), value (selected)
        cr = 20 + i
        calc.cell(cr, 1, i + 1)
        calc.cell(cr, 2, f'=IF(ISNUMBER(Search!C{r}),Search!C{r}+ROW()*1E-12,"")')
        order = f"IF({LOWER},SMALL($B$20:$B${19 + len(banks)},A{cr}),LARGE($B$20:$B${19 + len(banks)},A{cr}))"
        calc.cell(cr, 3, f'=IF(A{cr}>COUNT($B$20:$B${19 + len(banks)}),"",IFERROR(INDEX(Search!$A${rf}:$A${rl},MATCH({order},$B$20:$B${19 + len(banks)},0)),""))')
        val = f"INDEX(Search!$C${rf}:$C${rl},MATCH(C{cr},Search!$A${rf}:$A${rl},0))*{SCALE}"
        calc.cell(cr, 4, f'=IF(C{cr}="",NA(),IF(C{cr}=Search!$B$4,NA(),{val}))')
        calc.cell(cr, 5, f'=IF(C{cr}="",NA(),IF(C{cr}=Search!$B$4,{val},NA()))')
    _unit_formats(ws, f"C{rf}:C{rl}", UNIT_REF)
    ws.conditional_formatting.add(f"A{rf}:D{rl}", FormulaRule(formula=[f"$A{rf}=$B$4"], fill=SEL_FILL, font=Font(bold=True), stopIfTrue=True))
    ws.conditional_formatting.add(f"A{rf}:D{rl}", FormulaRule(formula=[f"AND($D{rf}<>\"\",$D{rf}<=5)"],
                                                              fill=PatternFill("solid", fgColor="E2EFDA")))

    bar = BarChart()
    bar.type = "col"
    bar.grouping = "clustered"
    bar.overlap = 100
    bar.gapWidth = 40
    bar.legend = None
    bar.height, bar.width = 9, 20
    bar.y_axis.number_format = "0.0"
    bar.y_axis.majorGridlines = None
    bar.x_axis.delete = False
    bar.y_axis.delete = False
    bar.visible_cells_only = False
    last = 19 + len(banks)
    for col, color in ((4, "8EA9DB"), (5, "ED7D31")):
        s = Series(Reference(calc, min_col=col, min_row=20, max_row=last), title=None)
        s.graphicalProperties.solidFill = color
        s.graphicalProperties.line.solidFill = color
        bar.series.append(s)
    bar.set_categories(Reference(calc, min_col=3, min_row=20, max_row=last))
    ws.add_chart(bar, f"J{cap + 1}")

    # --- full profile of the selected bank ---
    p0 = rl + 3
    _section(ws, p0, f'=IF({LANG}="VI","Hồ sơ ngân hàng: ","Bank profile: ")&$B$4&" — "&$C$4', ncols)
    _header(ws, p0 + 1, [tr("Metric", "Chỉ tiêu"), "", tr("Unit", "Đơn vị")] + periods)
    r = p0 + 2
    for label, key, kind, _ in ROWS:
        if key is None and kind is None:
            for c in range(1, ncols + 1):
                ws.cell(r, c).fill = SECTION_FILL
            ws.cell(r, 1, tr(label, VI[label])).font = Font(bold=True)
        else:
            ws.cell(r, 1, tr(label, VI[label])).font = Font(bold=True)
            ws.cell(r, 3, UNIT[kind] if kind else "")
            if key:
                for j in range(P):
                    src_v = f"INDEX(Data!{dcol(j)}$2:{dcol(j)}${n},MATCH($B$4&\"|{label}\",{keys},0))"
                    c = ws.cell(r, 4 + j, f'=IFERROR(IF({src_v}="","",{src_v}),"")')
                    fmt_cell(c, kind)
        r += 1
    ws.conditional_formatting.add(f"A{p0 + 2}:{get_column_letter(ncols)}{r - 1}",
                                  FormulaRule(formula=[f'$A{p0 + 2}={MLABEL}'], fill=SEL_FILL))

    ws.column_dimensions["A"].width = 30
    ws.column_dimensions["B"].width = 18
    ws.column_dimensions["C"].width = 9
    for j in range(P):
        ws.column_dimensions[get_column_letter(4 + j)].width = 9
    ws.freeze_panes = "A8"

    write_lookup(wb, banks, metrics, n, keys, dcol, P, periods, m_last, len(tickers))


def write_lookup(wb, banks, metrics, n, keys, dcol, P, periods, m_last, n_tickers):
    """Free-form grid: any bank × metric pair per row."""
    ws = wb.create_sheet("Lookup", 2)
    ws["A1"] = tr("Free lookup — any bank × metric per row", "Tra cứu tự do — mỗi dòng một cặp ngân hàng × chỉ tiêu")
    ws["A1"].font = Font(bold=True, size=13)
    hdr = 3
    _header(ws, hdr, [tr("Bank", "Ngân hàng"), tr("Name", "Tên"), tr("Metric", "Chỉ tiêu"), tr("Unit", "Đơn vị")] + periods)
    dv_b = DataValidation(type="list", formula1=f"=Lists!$A$2:$A${n_tickers + 1}", allow_blank=True)
    dv_m = DataValidation(type="list", formula1=f"=Lists!$H$2:$H${m_last}", allow_blank=True)
    for d in (dv_b, dv_m):
        d.showErrorMessage = False
        ws.add_data_validation(d)
    first, last = hdr + 1, hdr + LOOKUP_ROWS
    for i, r in enumerate(range(first, last + 1)):
        if i < len(DEFAULT_LOOKUPS):
            ws.cell(r, 1, DEFAULT_LOOKUPS[i][0])
            ws.cell(r, 3, DEFAULT_LOOKUPS[i][1])
        ws.cell(r, 1).fill = ws.cell(r, 3).fill = INPUT
        canon = (f'IFERROR(INDEX(Lists!$C$2:$C${m_last},MATCH($C{r},Lists!$C$2:$C${m_last},0)),'
                 f'IFERROR(INDEX(Lists!$C$2:$C${m_last},MATCH($C{r},Lists!$G$2:$G${m_last},0)),""))')
        ws.cell(r, 2, f'=IF($A{r}="","",IFERROR(INDEX(Lists!$B:$B,MATCH($A{r},Lists!$A:$A,0)),"?"))')
        ws.cell(r, 4, f'=IF($C{r}="","",IFERROR(INDEX(Lists!$D$2:$D${m_last},MATCH({canon},Lists!$C$2:$C${m_last},0)),"?"))')
        for j in range(P):
            src = f"INDEX(Data!{dcol(j)}$2:{dcol(j)}${n},MATCH($A{r}&\"|\"&{canon},{keys},0))"
            c = ws.cell(r, 5 + j, f'=IF(OR($A{r}="",$C{r}=""),"",IFERROR(IF({src}="","",{src}),""))')
            c.number_format = "0.0%"
    dv_b.add(f"A{first}:A{last}")
    dv_m.add(f"C{first}:C{last}")
    _unit_formats(ws, f"E{first}:{get_column_letter(4 + P)}{last}", f"$D{first}")
    ws.column_dimensions["A"].width = 10
    ws.column_dimensions["B"].width = 16
    ws.column_dimensions["C"].width = 30
    ws.freeze_panes = "E4"


def _unit_formats(ws, rng, unit_ref):
    """Show multiples and bn-VND values in their own format; % is the cell default."""
    for i, (unit, fmt) in enumerate((("x", "0.00"), ("bn VND", "#,##0"))):
        style = DifferentialStyle(numFmt=NumberFormat(numFmtId=200 + i, formatCode=fmt))
        ws.conditional_formatting.add(rng, Rule(type="expression", formula=[f'{unit_ref}="{unit}"'], dxf=style, stopIfTrue=True))


def main(raw_dir, out_path):
    D = {k: load(raw_dir, k) for k in ["is_a", "bs_a", "cf_a", "ratios_a", "is_q", "bs_q", "ratios_q"]}
    px = load_prices(raw_dir)
    years = sorted({y for t in D["is_a"] for (y, q) in D["is_a"][t] if q == 5})
    latest_q = max(k for t in D["bs_q"] for k in D["bs_q"][t])
    names = {}
    info = os.path.join(raw_dir, "basic_info.json")
    if os.path.exists(info):
        with open(info, encoding="utf-8") as f:
            names = {r["ticker"]: r["organizationShortName"] for r in json.load(f)["data"]["records"]}

    wb = Workbook()
    readme = wb.active
    readme.title = "README"
    results, flags = {}, []
    for t in BANKS:
        if t not in D["is_a"]:
            continue
        results[t] = build_bank(t, D, px.get(t, []), years, latest_q, flags)
        for p, m in results[t].items():
            r = m.get("recovery")
            if r is not None and r > 3:
                flags.append((t, p, f"Recovery rate {r:.0%}: write-offs too small for a meaningful ratio"))

    # Panel (long format) + per-metric comparison
    panel = wb.create_sheet("Panel")
    panel.append(["Bank", "Metric", "Period", "Value"])
    for t, cols in results.items():
        for label, key, kind, _ in ROWS:
            if not key:
                continue
            for p, m in cols.items():
                if m.get(key) is not None:
                    panel.append([t, label, p, m[key]])
    compare = wb.create_sheet("Compare")
    periods = list(next(iter(results.values())))
    last_two = periods[-2:]
    compare.append(["Metric", "Period"] + list(results))
    for label, key, kind, _ in ROWS:
        if not key:
            continue
        for p in last_two:
            compare.append([label, p] + [results[t][p].get(key) for t in results])
            for c in range(3, len(results) + 3):
                fmt_cell(compare.cell(compare.max_row, c), kind)
    for c in range(1, len(results) + 3):
        compare.cell(1, c).fill, compare.cell(1, c).font = HEADER_FILL, WHITE_BOLD
    compare.column_dimensions["A"].width = 26
    compare.freeze_panes = "C2"

    for t, cols in results.items():
        write_bank_sheet(wb, t, names.get(t, ""), cols)

    qa = wb.create_sheet("QA flags", 1)
    qa.append(["Bank", "Period", "Issue"])
    for row in flags:
        qa.append(list(row))
    for c in range(1, 4):
        qa.cell(1, c).fill, qa.cell(1, c).font = HEADER_FILL, WHITE_BOLD
    qa.column_dimensions["C"].width = 110

    defs = wb.create_sheet("Definitions", 1)
    defs.append(["Metric", "Formula / source", "Chỉ tiêu", "Công thức / nguồn"])
    for label, key, kind, definition in ROWS:
        if kind is not None:
            defs.append([label, definition, VI[label], VI_DEF[label]])
    for c in range(1, 5):
        defs.cell(1, c).fill, defs.cell(1, c).font = HEADER_FILL, WHITE_BOLD
    defs.column_dimensions["A"].width = 26
    defs.column_dimensions["B"].width = 80
    defs.column_dimensions["C"].width = 30
    defs.column_dimensions["D"].width = 80

    lines = [
        "Vietnam listed banks — KPI template (FiinPro API)",
        f"Built {date.today().isoformat()} · {len(results)} banks · periods {periods[0]} → {periods[-1]} · consolidated.",
        "Sheets: Search (bank / metric / period / peers → history + chart, ranking + chart, full bank profile) · Lookup (free bank × metric grid) · one per bank (template layout) · Compare (all banks, last FY + LTM, filterable) · Panel (long format, filterable) · Definitions.",
        "",
        "Read before using:",
        "1. NPL, Group 2, CASA and Credit growth come from FiinPro's ratio feed (loan classification is in the notes, which the API does not expose). All other rows are computed here from statement lines.",
        "2. CAR comes from FiinPro's ratio feed and is missing for some banks and for the latest quarter. LDR is a consolidated proxy, not the TT22 regulatory ratio. FiinPro CASA can run 2-3pp below bank-reported CASA (TCB FY25: 34.5% vs 35.9% reported).",
        "3. P/B and P/E use the unadjusted close on the last trading day ≤ period end × charter capital/10,000 (treasury shares ignored) against period-end equity. FiinPro's own year-end P/B is 2-7% higher because it uses the last equity published at that date (Q3).",
        "4. PD and Recovery need write-offs = 'use of provisions' from the cash-flow statement; banks that report it as zero/blank show blank or 0.",
        "5. Credit cost uses total P&L provision expense (includes non-loan provisions such as VAMC/bonds).",
        "6. The LTM column: flows = last 4 reported quarters; balance-sheet averages = latest quarter and the same quarter a year earlier; P/B uses today's close vs latest equity. PD/Recovery are annual-only.",
        "7. Macro rows (interbank, deposit rates, system liquidity) and target-price rows are inputs — not in the API.",
        "8. 2026F column from the template is not produced: forecasts are analyst inputs.",
        "9. P/E above 100x (near-zero earnings) is left blank. See the QA flags sheet for provider anomalies found while building.",
        "",
        "Tiếng Việt: chọn VI tại ô Search!B3 để chuyển toàn bộ nhãn sang tiếng Việt.",
        "Sheet Search: chọn Ngân hàng / Chỉ tiêu / Kỳ / NH so sánh → bảng lịch sử, biểu đồ theo thời gian, xếp hạng + biểu đồ toàn ngành, hồ sơ đầy đủ của ngân hàng.",
        "Lưu ý: NPL, Nhóm 2, CASA, Tăng trưởng tín dụng, CAR lấy từ bộ chỉ số FiinPro; các chỉ tiêu khác tính từ BCTC. LDR là ước tính hợp nhất, không phải TT22. Xem sheet QA flags về lỗi dữ liệu nguồn.",
    ]
    for i, line in enumerate(lines, 1):
        readme.cell(i, 1, line).font = Font(bold=(i in (1, 5)), size=13 if i == 1 else 11)
    readme.column_dimensions["A"].width = 160

    for ws in (panel, compare):
        ws.auto_filter.ref = ws.dimensions
    panel.freeze_panes = "A2"
    write_search(wb, results, names)
    wb.save(out_path)
    return results


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    res = main(sys.argv[1], sys.argv[2])
    print(f"Saved {sys.argv[2]} with {len(res)} banks")
