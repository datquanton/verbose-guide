"""Build a FiinPro-style Excel workbook from FiinQuant MCP JSON dumps.

Usage:
    python fiinpro_export.py TICKER RAW_DIR OUT.xlsx

RAW_DIR holds the raw (response_format=raw) MCP outputs, named:
    is_annual.json  is_quarterly*.json  bs_annual.json  bs_quarterly.json
    cf_annual.json  cf_quarterly.json   ratios_annual.json  ratios_quarterly.json
    prices_daily.json  snapshot.json (optional)  basic_info.json (optional)

Multi-ticker dumps are fine; rows are filtered to TICKER. Statement values are
converted from VND to VND billion (Tỷ VND) to match FiinProX desktop exports.
"""
import glob
import json
import os
import sys
from datetime import date

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

BN = 1e9
HEADER_FILL = PatternFill("solid", fgColor="1F3864")
HEADER_FONT = Font(bold=True, color="FFFFFF")
SECTION_FONT = Font(bold=True)
FLAG_FILL = PatternFill("solid", fgColor="FCE4D6")

# Ratio blocks whose values are VND amounts despite the "_billion_vnd" suffix.
VND_AMOUNT_SUFFIX = "_billion_vnd"


def load_records(raw_dir, pattern, ticker):
    rows, warnings = {}, []
    for path in sorted(glob.glob(os.path.join(raw_dir, pattern))):
        with open(path, encoding="utf-8") as f:
            payload = json.load(f)
        for rec in payload["data"]["records"]:
            if rec.get("ticker") != ticker:
                continue
            key = (rec["year"], rec["quarter"])
            if key in rows and rows[key] != rec:
                warnings.append(f"{os.path.basename(path)}: differing duplicate rows for {key}; kept last")
            rows[key] = rec
    return [rows[k] for k in sorted(rows)], warnings


def label(key):
    text = key.replace("_", " ").strip()
    return text[:1].upper() + text[1:]


def flatten(node, depth=0, out=None, prefix=""):
    """Walk nested provider dicts into (path, label, depth, value) rows.

    A dict holding a 'total_*' child is shown as one header row carrying that
    total, with its other children indented beneath it.
    """
    if out is None:
        out = []
    for key, val in node.items():
        path = f"{prefix}.{key}" if prefix else key
        if isinstance(val, dict):
            total_key = next((k for k in val if k.startswith("total_") and not isinstance(val[k], dict)), None)
            out.append((path, label(key), depth, val.get(total_key) if total_key else None, True))
            children = {k: v for k, v in val.items() if k != total_key}
            flatten(children, depth + 1, out, path)
        elif isinstance(val, list) and val and isinstance(val[0], dict):
            flatten(val[0], depth, out, path)
        else:
            out.append((path, label(key), depth, val, False))
    return out


def period_label(rec):
    return f"FY{rec['year']}" if rec["quarter"] == 5 else f"{rec['quarter']}Q{str(rec['year'])[2:]}"


def write_header(ws, title, ticker, unit, note=None):
    ws["A1"] = title
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = f"Mã CK: {ticker}   |   Đơn vị: {unit}   |   Nguồn: FiinQuantX (FiinPro API) via MCP   |   Trích xuất: {date.today().isoformat()}"
    if note:
        ws["A3"] = note
        ws["A3"].font = Font(italic=True, color="C00000")


def statement_sheet(wb, name, title, records, ticker, block, scale=BN, unit="Tỷ VND", drop=()):
    ws = wb.create_sheet(name)
    write_header(ws, title, ticker, unit)
    periods = [period_label(r) for r in records]
    flats = []
    for rec in records:
        body = rec["financial_statement"] if block == "financial_statement" else rec[block]
        flats.append({p: (lab, d, v, hdr) for p, lab, d, v, hdr in flatten(body)})
    # Row order follows the most recent period (most complete template).
    order = [p for p, *_ in flatten(records[-1]["financial_statement"] if block == "financial_statement" else records[-1][block])]
    for f in flats:
        for p in f:
            if p not in order:
                order.append(p)
    hdr_row = 5
    ws.cell(hdr_row, 1, "Chỉ tiêu")
    ws.cell(hdr_row, 2, "Field path")
    for j, p in enumerate(periods):
        ws.cell(hdr_row, 3 + j, p)
    ws.cell(hdr_row + 1, 1, "Trạng thái kiểm toán")
    for j, rec in enumerate(records):
        ws.cell(hdr_row + 1, 3 + j, rec.get("audit_status") or "n/a")
    r = hdr_row + 2
    for path in order:
        if any(path.startswith(d) for d in drop):
            continue
        meta = next((f[path] for f in reversed(flats) if path in f), None)
        lab, depth, _, is_hdr = meta
        vals = [f.get(path, (None, None, None, None))[2] for f in flats]
        if is_hdr and all(v is None for v in vals):
            ws.cell(r, 1, "   " * depth + lab).font = SECTION_FONT
            ws.cell(r, 2, path)
            r += 1
            continue
        ws.cell(r, 1, "   " * depth + lab)
        if is_hdr:
            ws.cell(r, 1).font = SECTION_FONT
        ws.cell(r, 2, path)
        for j, v in enumerate(vals):
            if isinstance(v, (int, float)):
                s = scale
                if block == "ratios" and not path.endswith(VND_AMOUNT_SUFFIX):
                    s = 1
                if path.split(".")[-1].startswith("eps"):  # per-share VND, not an amount
                    s = 1
                ws.cell(r, 3 + j, v / s).number_format = "#,##0.0" if s != 1 else "0.00%" if abs(v) < 5 else "#,##0.00"
            elif v is not None:
                ws.cell(r, 3 + j, v)
        r += 1
    style_table(ws, hdr_row, len(periods) + 2)
    return ws


def style_table(ws, hdr_row, ncols):
    for c in range(1, ncols + 1):
        cell = ws.cell(hdr_row, c)
        cell.fill, cell.font = HEADER_FILL, HEADER_FONT
        cell.alignment = Alignment(horizontal="center")
    ws.column_dimensions["A"].width = 62
    ws.column_dimensions["B"].width = 18
    for c in range(3, ncols + 1):
        ws.column_dimensions[get_column_letter(c)].width = 12
    ws.freeze_panes = ws.cell(hdr_row + 1, 3)


def get_path(rec, path):
    node = rec["financial_statement"]
    for part in path.split("."):
        if isinstance(node, list):
            node = node[0]
        node = node.get(part) if isinstance(node, dict) else None
        if node is None:
            return None
    return node


def qa_checks(is_a, is_q, bs_a, bs_q):
    rows = []
    npat = "income_statement.net_profit_loss_after_tax"
    q_by_year = {}
    for rec in is_q:
        q_by_year.setdefault(rec["year"], []).append(get_path(rec, npat))
    for rec in is_a:
        qs = q_by_year.get(rec["year"], [])
        annual = get_path(rec, npat)
        if len(qs) == 4 and None not in qs and annual:
            diff = sum(qs) - annual
            rows.append(("NPAT: sum of 4Q vs FY", f"FY{rec['year']}", annual / BN, sum(qs) / BN, diff / BN,
                         "OK" if abs(diff) / abs(annual) < 0.01 else "CHECK"))
    ta = "balance_sheet.total_assets.total_assets"
    tle = "balance_sheet.liabilities_and_shareholder_s_equity.total_liabilities_and_shareholder_s_equity"
    for rec in bs_a + bs_q:
        a, le = get_path(rec, ta), get_path(rec, tle)
        if a and le:
            rows.append(("BS: assets = liabilities + equity", period_label(rec), a / BN, le / BN, (a - le) / BN,
                         "OK" if abs(a - le) < BN else "CHECK"))
    return rows


def main(ticker, raw_dir, out_path):
    warnings = []
    data = {}
    for key, pattern in {
        "is_a": "is_annual*.json", "is_q": "is_quarterly*.json",
        "bs_a": "bs_annual*.json", "bs_q": "bs_quarterly*.json",
        "cf_a": "cf_annual*.json", "cf_q": "cf_quarterly*.json",
        "r_a": "ratios_annual*.json", "r_q": "ratios_quarterly*.json",
    }.items():
        data[key], w = load_records(raw_dir, pattern, ticker)
        warnings += w

    wb = Workbook()
    wb.remove(wb.active)
    readme = wb.create_sheet("README")

    statement_sheet(wb, "KQKD_Nam", f"Kết quả kinh doanh (Hằng năm) - {ticker}", data["is_a"], ticker, "financial_statement")
    statement_sheet(wb, "KQKD_Quy", f"Kết quả kinh doanh (Hằng quý) - {ticker}", data["is_q"], ticker, "financial_statement")
    statement_sheet(wb, "CDKT_Nam", f"Bảng cân đối kế toán (Hằng năm) - {ticker}", data["bs_a"], ticker, "financial_statement")
    statement_sheet(wb, "CDKT_Quy", f"Bảng cân đối kế toán (Hằng quý) - {ticker}", data["bs_q"], ticker, "financial_statement")
    statement_sheet(wb, "LCTT_Nam", f"Lưu chuyển tiền tệ (Hằng năm) - {ticker}", data["cf_a"], ticker, "financial_statement")
    statement_sheet(wb, "LCTT_Quy", f"Lưu chuyển tiền tệ (Hằng quý) - {ticker}", data["cf_q"], ticker, "financial_statement")
    # Valuation block is empty in the provider rows; P/E-P/B there would be today's snapshot, not history.
    statement_sheet(wb, "ChiSo_Nam", f"Chỉ số tài chính (Hằng năm) - {ticker}", data["r_a"], ticker, "ratios",
                    unit="% / lần; dòng '_billion_vnd' = Tỷ VND", drop=("7_valuation_ratios",))
    statement_sheet(wb, "ChiSo_Quy", f"Chỉ số tài chính (Hằng quý) - {ticker}", data["r_q"], ticker, "ratios",
                    unit="% / lần; dòng '_billion_vnd' = Tỷ VND", drop=("7_valuation_ratios",))

    price_path = os.path.join(raw_dir, "prices_daily.json")
    price_rows = []
    if os.path.exists(price_path):
        with open(price_path, encoding="utf-8") as f:
            pdata = json.load(f)
        price_rows = [r for r in pdata["data"]["records"] if r["ticker"] == ticker]
        ws = wb.create_sheet("Gia_Ngay")
        write_header(ws, f"Giá giao dịch ngày (điều chỉnh) - {ticker}", ticker, "VND / cổ phiếu; giá trị VND",
                     "Giá đã điều chỉnh cổ tức/thưởng. Dòng cuối có thể là phiên đang giao dịch (chưa đóng cửa).")
        cols = [("timestamp", "Ngày"), ("open", "Mở cửa"), ("high", "Cao nhất"), ("low", "Thấp nhất"),
                ("close", "Đóng cửa"), ("volume", "KL khớp"), ("value", "GT giao dịch (VND)"),
                ("bu", "KL mua chủ động"), ("sd", "KL bán chủ động"), ("fb", "NN mua (VND)"),
                ("fs", "NN bán (VND)"), ("fn", "NN ròng (VND)")]
        for j, (_, name) in enumerate(cols):
            ws.cell(5, 1 + j, name)
        for i, rec in enumerate(price_rows):
            for j, (k, _) in enumerate(cols):
                v = rec.get(k)
                cell = ws.cell(6 + i, 1 + j, v)
                if k in ("open", "high", "low", "close") and v is not None:
                    cell.number_format = "#,##0"
                elif isinstance(v, (int, float)):
                    cell.number_format = "#,##0"
        if price_rows and not price_rows[-1]["timestamp"].endswith("00:00"):
            for j in range(len(cols)):
                ws.cell(5 + len(price_rows), 1 + j).fill = FLAG_FILL
        style_table(ws, 5, len(cols))
        ws.column_dimensions["A"].width = 18

    snap_path = os.path.join(raw_dir, "snapshot.json")
    if os.path.exists(snap_path):
        with open(snap_path, encoding="utf-8") as f:
            snap = json.load(f)
        ws = wb.create_sheet("Snapshot")
        write_header(ws, f"Snapshot thị trường - {ticker}", ticker, "như provider")
        ws.cell(5, 1, "Chỉ tiêu")
        ws.cell(5, 2, "Giá trị")
        r = 6
        for blk in (snap.get("basic_info", {}), snap.get("snapshot", {})):
            for k, v in blk.items():
                ws.cell(r, 1, k)
                ws.cell(r, 2, v)
                r += 1
        style_table(ws, 5, 2)
        ws.column_dimensions["B"].width = 50

    qa = qa_checks(data["is_a"], data["is_q"], data["bs_a"], data["bs_q"])
    ws = wb.create_sheet("QA")
    write_header(ws, "Kiểm tra dữ liệu", ticker, "Tỷ VND")
    for j, h in enumerate(["Check", "Kỳ", "Giá trị A", "Giá trị B", "Chênh lệch", "Kết quả"]):
        ws.cell(5, 1 + j, h)
    for i, row in enumerate(qa):
        for j, v in enumerate(row):
            c = ws.cell(6 + i, 1 + j, v)
            if isinstance(v, float):
                c.number_format = "#,##0.0"
            if row[-1] == "CHECK":
                c.fill = FLAG_FILL
    style_table(ws, 5, 6)
    ws.column_dimensions["A"].width = 36

    def span(recs):
        return f"{period_label(recs[0])} → {period_label(recs[-1])} ({len(recs)} kỳ)" if recs else "không có dữ liệu"

    lines = [
        (f"{ticker} — FiinPro data pack", True),
        (f"Trích xuất {date.today().isoformat()} qua FiinQuantX MCP. Báo cáo hợp nhất. Giá trị báo cáo đổi sang Tỷ VND.", False),
        ("", False),
        ("Coverage", True),
        (f"KQKD năm: {span(data['is_a'])}", False),
        (f"KQKD quý: {span(data['is_q'])}", False),
        (f"CĐKT năm: {span(data['bs_a'])}", False),
        (f"CĐKT quý: {span(data['bs_q'])}", False),
        (f"LCTT năm: {span(data['cf_a'])}", False),
        (f"LCTT quý: {span(data['cf_q'])}", False),
        (f"Chỉ số năm: {span(data['r_a'])}", False),
        (f"Chỉ số quý: {span(data['r_q'])}", False),
        (f"Giá ngày: {price_rows[0]['timestamp'][:10]} → {price_rows[-1]['timestamp']} ({len(price_rows)} phiên)" if price_rows else "Giá ngày: không có", False),
        ("", False),
        ("Data flags (đọc trước khi dùng số)", True),
        ("1. Ratio rows labelled '_billion_vnd' are delivered in VND by the API; converted to Tỷ VND here.", False),
        ("2. API valuation block (P/E, P/B, EV…) is empty for every period → dropped. The P/E/P/B the MCP attaches to history is TODAY's snapshot, not historical — never use it as a time series.", False),
        ("3. CAR field is null in the API for every period checked; use bank disclosures for CAR.", False),
        ("4. Prices are adjusted (dividends/bonus shares). Last row may be an unclosed intraday bar (highlighted).", False),
        ("5. Not in the API vs FiinProX desktop export: Thuyết minh (notes), liquidity/interest-rate risk, CAR report, pre-2014 history.", False),
        ("6. Cash-flow audit status is not reported by the API (n/a).", False),
        ("7. See QA sheet: NPAT 4Q-sum vs FY, and balance-sheet identity per period.", False),
        ("8. EPS is as-reported per period (not restated for later bonus issues/splits) — not comparable across years without adjustment.", False),
    ] + [(f"Warning: {w}", False) for w in warnings]
    for i, (text, bold) in enumerate(lines, start=1):
        c = readme.cell(i, 1, text)
        if bold:
            c.font = Font(bold=True, size=12 if i == 1 else 11)
    readme.column_dimensions["A"].width = 140

    wb.save(out_path)
    print(f"Saved {out_path}")
    for w in warnings:
        print("WARN", w)
    print(f"QA: {sum(r[-1] == 'OK' for r in qa)} OK, {sum(r[-1] == 'CHECK' for r in qa)} CHECK")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(sys.argv[1].upper(), sys.argv[2], sys.argv[3])
