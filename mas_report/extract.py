"""
Step 1 of the Daily MAS pipeline.

Read the Bloomberg-updated workbook (Daily_dataYYYY_*.xlsm) and emit a single
JSON file with every number the report needs. Nothing here touches the web or an
LLM -- it is pure, deterministic extraction, so the figures are guaranteed to
match the workbook exactly (zero hallucination risk downstream).

Usage:
    python -m mas_report.extract path/to/data.xlsm -o report_data.json
"""
from __future__ import annotations

import argparse
import json
import sys

import openpyxl


def _cell(ws, addr):
    return ws[addr].value


def _num(v):
    return v if isinstance(v, (int, float)) else None


def extract(xlsm_path: str) -> dict:
    """Return all report-ready data as a plain dict."""
    wb = openpyxl.load_workbook(xlsm_path, data_only=True)
    D = wb["Dashboard"]
    F = wb["Foreign trading"]

    # 1) OHLC + DoD -- 'Foreign trading' J2:M9 (Previous / Today / %DoD)
    ohlc = {}
    for label, row in [
        ("open", 3), ("high", 4), ("low", 5),
        ("close", 6), ("volume", 8), ("value", 9),
    ]:
        ohlc[label] = {
            "prev": _cell(F, f"K{row}"),
            "today": _cell(F, f"L{row}"),
            "dod": _cell(F, f"M{row}"),
        }

    # 2) Headline indices -- Dashboard A3:E12
    indices = []
    for r in range(3, 13):
        name = _cell(D, f"A{r}")
        if name:
            indices.append({
                "name": name,
                "last": _cell(D, f"B{r}"),
                "1d": _cell(D, f"C{r}"),
                "1m": _cell(D, f"D{r}"),
                "1y": _cell(D, f"E{r}"),
            })

    # 3) Full VN30 valuation table -- Dashboard K6:AH35
    vn30 = []
    for r in range(6, 36):
        if _cell(D, f"K{r}"):
            vn30.append({
                "name": _cell(D, f"K{r}"),
                "ticker": _cell(D, f"L{r}"),
                "mcap": _cell(D, f"M{r}"),
                "last": _cell(D, f"O{r}"),
                "52w_high": _cell(D, f"P{r}"),
                "52w_low": _cell(D, f"Q{r}"),
                "1d": _cell(D, f"S{r}"),
                "1w": _cell(D, f"T{r}"),
                "1m": _cell(D, f"U{r}"),
                "1y": _cell(D, f"V{r}"),
                "pe": _cell(D, f"X{r}"),
                "pb": _cell(D, f"Y{r}"),
                "roe": _cell(D, f"Z{r}"),
                "foreign_own": _cell(D, f"AB{r}"),
                "ex_date": _cell(D, f"AE{r}"),
                "dps": _cell(D, f"AF{r}"),
                "dy_12m": _cell(D, f"AG{r}"),
                "dy_fy": _cell(D, f"AH{r}"),
            })

    # 4) Top VN30 contributors, ranked by 1D move
    movers = [v for v in vn30 if _num(v.get("1d")) is not None]
    gainers = sorted(movers, key=lambda x: x["1d"], reverse=True)[:5]
    losers = sorted(movers, key=lambda x: x["1d"])[:5]

    # 5) Foreign flows -- 'Foreign trading' HOSE row + the sheet's own sentence
    flows = {
        "buy": _cell(F, "B2"),
        "sell": _cell(F, "C2"),
        "net": _cell(F, "D2"),
        "sentence": _cell(F, "A17"),
    }

    # 6) Top foreign inflows / outflows -- 'Foreign trading' F24:I35
    inflows = [
        {"ticker": _cell(F, f"F{r}"), "net": _cell(F, f"G{r}"),
         "price": _cell(F, f"H{r}"), "chg": _cell(F, f"I{r}")}
        for r in range(24, 29) if _cell(F, f"F{r}")
    ]
    outflows = [
        {"ticker": _cell(F, f"F{r}"), "net": _cell(F, f"G{r}"),
         "price": _cell(F, f"H{r}"), "chg": _cell(F, f"I{r}")}
        for r in range(29, 36)
        if _cell(F, f"F{r}") and _num(_cell(F, f"G{r}")) is not None and _cell(F, f"G{r}") < 0
    ]

    # 7) Sentences the sheet pre-writes (handy as a grounding cross-check)
    prewritten = {"ohlc": _cell(F, "J11"), "liquidity": _cell(F, "J12")}

    return {
        "ohlc": ohlc,
        "indices": indices,
        "vn30": vn30,
        "gainers": gainers,
        "losers": losers,
        "flows": flows,
        "inflows": inflows,
        "outflows": outflows,
        "prewritten": prewritten,
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description="Extract report data from the MAS .xlsm")
    ap.add_argument("xlsm", help="path to the Bloomberg-updated workbook")
    ap.add_argument("-o", "--out", default="report_data.json", help="output JSON path")
    args = ap.parse_args(argv)

    data = extract(args.xlsm)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2, default=str)

    print(f"[extract] {len(data['vn30'])} VN30 rows -> {args.out}", file=sys.stderr)
    print(f"[extract] close {data['ohlc']['close']['today']} "
          f"({data['ohlc']['close']['dod']*100:+.1f}% DoD)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
