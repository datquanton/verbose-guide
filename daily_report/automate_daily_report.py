#!/usr/bin/env python3
"""
Automate the Mirae Asset "Good Morning Vietnam" mobile daily report.

It takes the daily MAS Word report (the text/table source) plus an optional
market-data provider (for the charts) and produces an updated PowerPoint deck
from a template -- with NO Microsoft Office and NO network share required.

What it updates
---------------
TEXT / TABLES  (sourced from the Word .docx):
  - Daily theme (title slide + slide 1)
  - VN-Index OHLC table (Open/High/Low/Close + % DoD)
  - Global-indices VN INDEX row (last trade, 1D, 1M, 1Y)
  - Slide-1 market narrative (2 lines)
  - Liquidity line + VN30 top gainers / decliners (slide 2)
  - Daily trading value, VN-INDEX (US$mn) (slide 2)
  - Foreign net flow (slide 4)
  - Short-news headlines (slide 5)

CHARTS  (sourced from a ChartDataProvider -- see chart_data.py):
  The 6 charts are native PowerPoint charts that are OLE-linked to an external
  workbook (\\\\10.0.16.23\\...\\Daily data-*.xlsm). The deck stores a *cached*
  copy of each series for display. This script rewrites that cache directly, so
  the charts update headlessly. If no provider is given, charts are left as-is.

Usage
-----
  # text/tables only (no chart data needed):
  python automate_daily_report.py \
      --word  Daily_MAS_YYYYMMDD.docx \
      --template DailyReport_Mobile_EN_template.pptx \
      --out   DailyReport_Mobile_EN_YYYYMMDD.pptx

  # also update charts from CSVs in ./data:
  python automate_daily_report.py ... --chart-source csv --data-dir ./data

  # dump shape ids/text of the template (use after a template redesign to
  # re-check the RECIPE below):
  python automate_daily_report.py --template TEMPLATE.pptx --inspect
"""
from __future__ import annotations
import argparse
import re
import sys
import zipfile
from copy import deepcopy
from pathlib import Path

import docx
from pptx import Presentation
from lxml import etree


# ---------------------------------------------------------------------------
# 1. PARSE THE WORD REPORT  -> a flat dict of fields
# ---------------------------------------------------------------------------
def _norm(s: str) -> str:
    return s.replace("−", "-").replace("–", "-").replace("\xa0", " ")


def parse_word(docx_path: str) -> dict:
    doc = docx.Document(docx_path)

    # The VIETNAM STOCK MARKET narrative lives in table[1], row 1, single cell:
    #   line 0 = daily theme, the rest = body paragraph.
    cell = _norm(doc.tables[1].rows[1].cells[0].text)
    theme = cell.split("\n")[0].strip()
    body = " ".join(cell.split("\n")[1:])

    def grp(pat, s=body):
        m = re.search(pat, s)
        if not m:
            raise ValueError(f"pattern not found in Word doc: {pat!r}")
        return m.groups()

    # OHLC -- tolerant of wording that varies day to day: "pts" optional;
    # "intraday/session high", "a low of", "closed at / a close of".
    def ohlc(anchor):
        return grp(anchor + r" ([\d,]+\.\d+)(?:pts)? ?\(([-+][\d.]+)% ?DoD\)")

    op, op_p = ohlc(r"opened at")
    hi, hi_p = ohlc(r"high of")
    lo, lo_p = ohlc(r"low of")
    cl, cl_p = ohlc(r"(?:closed at|close of)")

    # Liquidity: volume (…mn shares, ±% DoD) and value (VND…bn, ±% DoD) grabbed
    # independently so phrasing ("reached"/"rose to"/"eased to") doesn't matter.
    vol, vol_p = grp(r"([\d,.]+)mn(?: shares?)? \(([-+][\d.]+)% ?DoD\)")
    val, val_p = grp(r"VND ?([\d,]+)bn \(([-+][\d.]+)% ?DoD\)")

    # VN30 winners / losers -- handles "top winners are:" + "Top losers are:"
    # as well as the older "Meanwhile, … weighed the index".
    def tickers(pat):
        m = re.search(pat, body, re.IGNORECASE)
        return re.findall(r"[A-Z]{3}", m.group(1)) if m else []

    winners = tickers(r"top winners are:? (.+?)(?:\. Meanwhile|\. Top losers|weighed|$)")
    losers = tickers(r"(?:Meanwhile,|Top losers are:?)\s*(.+?)(?: weighed| Foreign|$)")

    fx_m = re.search(r"net (seller|buyer)s?.*?(?:out|in)flows? of VND([\d,]+)bn", body)
    fx_side = fx_m.group(1) + "s"        # -> "sellers" / "buyers"
    fx_amt = fx_m.group(2)

    # 1M / 1Y for the VN INDEX row come from the valuation table (table[8]); the
    # VN-Index line is the first data row (after 2 header rows). A cell may be
    # "####" (Excel column too narrow in the source) -> treat as unavailable.
    def numeric(x):
        try:
            float(x.replace(",", ""))
            return x
        except ValueError:
            return None

    vn_ne = [_norm(c.text).strip() for c in doc.tables[8].rows[2].cells
             if _norm(c.text).strip()]
    one_m = numeric(vn_ne[7]) if len(vn_ne) > 8 else None   # …,1D,1W,1M,1Y,…
    one_y = numeric(vn_ne[8]) if len(vn_ne) > 8 else None

    # Short-news headlines: the 3 news titles (paragraphs 1, 3, 5).
    news = [doc.paragraphs[i].text.strip() for i in (1, 3, 5)]

    def pct1(x):  # "+0.27" -> "+0.3" ; "-0.69" -> "-0.7"
        v = round(float(x), 1)
        return f"{v:+.1f}"

    def num(x):
        return float(x.replace(",", ""))

    return {
        "theme": theme,
        # OHLC: raw value (float) + % DoD to 1 dp; the applier formats the value
        # to match each deck's own cell style (decimals / comma / spacing).
        "ohlc": {
            "open": (num(op), f"{pct1(op_p)}%"),
            "high": (num(hi), f"{pct1(hi_p)}%"),
            "low": (num(lo), f"{pct1(lo_p)}%"),
            "close": (num(cl), f"{pct1(cl_p)}%"),
        },
        # global-indices VN INDEX row: last=close, 1D=close DoD, 1M/1Y from table
        "vnindex_row": (pct1(cl_p).lstrip("+"), one_m, one_y),
        "close_num": num(cl),
        "close_pts": cl,
        "close_dod": cl_p.lstrip("+"),
        "volume_mn": vol,
        "volume_dod": vol_p.lstrip("+"),
        "value_bn": val,
        "value_dod": val_p.lstrip("+"),
        "value_bn_num": float(val.replace(",", "")),
        "winners": winners,
        "losers": losers,
        "fx_side": fx_side,
        "fx_amount": fx_amt,
        "news": news,
    }


# ---------------------------------------------------------------------------
# 2. APPLY TEXT / TABLES TO THE DECK
#    Addressing is by (slide_index, shape_id). Re-check with --inspect if the
#    template layout ever changes.
# ---------------------------------------------------------------------------
# USD/VND rate used to convert HOSE trading value (VNDbn) -> US$mn for the
# slide-2 table. The deck's own historical cells imply ~26,278; the Word
# report's "$10.3bn = VND270tn" implies ~26,214. Override via --fx-rate.
DEFAULT_FX_RATE = 26.278  # thousand VND per USD


def _shape(slide, shape_id):
    for s in slide.shapes:
        if s.shape_id == shape_id:
            return s
    raise KeyError(f"shape id {shape_id} not on slide")


def _set_para(shape, p, text):
    """Set a whole paragraph's text, preserving the first run's formatting."""
    para = shape.text_frame.paragraphs[p]
    if para.runs:
        para.runs[0].text = text
        for r in para.runs[1:]:
            r.text = ""
    else:
        para.text = text


def _set_cell(table_shape, row, col, text):
    cell = table_shape.table.cell(row, col)
    para = cell.text_frame.paragraphs[0]
    if para.runs:
        para.runs[0].text = text
        for r in para.runs[1:]:
            r.text = ""
    else:
        cell.text = text


def _fmt_like(sample: str, value: float) -> str:
    """Format `value` to mirror an existing cell (decimals, comma, trailing space)."""
    core = sample.rstrip()
    trail = sample[len(core):]
    dec = len(core.split(".")[-1]) if "." in core else 0
    body = f"{value:,.{dec}f}" if "," in core else f"{value:.{dec}f}"
    return body + trail


def apply_text(prs, f: dict, fx_rate: float):
    s = prs.slides

    # -- Slide 0: theme + OHLC table + global indices VN INDEX row
    _set_para(_shape(s[0], 32), 0, f["theme"])
    ohlc = _shape(s[0], 40).table
    for ri, key in [(1, "open"), (2, "high"), (3, "low"), (4, "close")]:
        value, pct = f["ohlc"][key]
        _set_cell(_shape(s[0], 40), ri, 1, _fmt_like(ohlc.cell(ri, 1).text, value))
        _set_cell(_shape(s[0], 40), ri, 2, pct)
    d1, m1, y1 = f["vnindex_row"]
    gidx = _shape(s[0], 2)
    _set_cell(gidx, 1, 1, _fmt_like(gidx.table.cell(1, 1).text, f["close_num"]))
    _set_cell(gidx, 1, 2, d1)
    if m1 is not None:                       # 1M may be unavailable in the source
        _set_cell(gidx, 1, 3, m1)
    if y1 is not None:
        _set_cell(gidx, 1, 4, y1)

    # -- Slide 1: narrative (2 lines) + theme.
    # The narrative is the one editorial spot; we write a concise, fully
    # data-driven baseline (no stale text) that the analyst can embellish.
    verb = "fell" if f["close_dod"].startswith("-") else "rose"
    narr0 = (f'The VN-Index {verb} {f["close_dod"].lstrip("-")}% to close at '
             f'{f["close_pts"]}pts.')
    narr1 = (f'Liquidity reached {f["volume_mn"]}mn shares worth VND{f["value_bn"]}bn; '
             f'foreign investors were net {f["fx_side"]} of VND{f["fx_amount"]}bn.')
    narr = _shape(s[1], 2)
    _set_para(narr, 0, narr0)
    _set_para(narr, 1, narr1)
    _set_para(_shape(s[1], 8), 0, f["theme"])

    # -- Slide 2: liquidity line + VN30 lists + trading-value table
    liq = (f'Liquidity improved, with volume rising {f["volume_dod"]}% DoD to '
           f'{f["volume_mn"]}mn shares, while trading value increased '
           f'{f["value_dod"]}% to VND{f["value_bn"]}bn, respectively.')
    s2 = _shape(s[2], 3)
    _set_para(s2, 0, liq)
    _set_para(s2, 1, "VN30 top gainers: " + ", ".join(f["winners"][:4]))
    _set_para(s2, 2, "VN30 top decliners: " + ", ".join(f["losers"][:4]))
    usd = round(f["value_bn_num"] / fx_rate)
    _set_cell(_shape(s[2], 4), 2, 1, str(usd))

    # -- Slide 4: foreign flow (whole sentence; net side + amount both vary)
    _set_para(_shape(s[4], 3), 0,
              f'Foreign investors were net {f["fx_side"]}, with a net outflow '
              f'of VND{f["fx_amount"]}bn on HOSE')

    # -- Slide 5: short-news headlines
    s5 = _shape(s[5], 3)
    for i, headline in enumerate(f["news"][:3]):
        _set_para(s5, i, headline)


# ---------------------------------------------------------------------------
# 3. CHART CACHE EDITING (headless -- no Office, no external workbook)
# ---------------------------------------------------------------------------
_C = "http://schemas.openxmlformats.org/drawingml/2006/chart"


def _c(tag):
    return f"{{{_C}}}{tag}"


def _cache(parent):
    for kind in ("numCache", "strCache"):
        e = parent.find(_c(kind))
        if e is not None:
            return e
    for ref in ("numRef", "strRef", "multiLvlStrRef"):
        r = parent.find(_c(ref))
        if r is not None:
            for kind in ("numCache", "strCache"):
                e = r.find(_c(kind))
                if e is not None:
                    return e
    raise ValueError("no cache element found")


def _read_cache(cache):
    n = int(cache.find(_c("ptCount")).get("val"))
    arr = [None] * n
    for pt in cache.findall(_c("pt")):
        i = int(pt.get("idx"))
        v = pt.find(_c("v"))
        if i < n:
            arr[i] = v.text if v is not None else None
    return arr


def _write_cache(cache, arr):
    cache.find(_c("ptCount")).set("val", str(len(arr)))
    for pt in cache.findall(_c("pt")):
        cache.remove(pt)
    for i, v in enumerate(arr):
        if v is None or v == "":
            continue
        pt = etree.SubElement(cache, _c("pt"))
        pt.set("idx", str(i))
        etree.SubElement(pt, _c("v")).text = str(v)


def _series(chart):
    return chart._chartSpace.findall(".//" + _c("ser"))


def append_point(chart, new_category, new_values):
    """Append one new data point (e.g. today) to every series of a time-series chart."""
    for si, ser in enumerate(_series(chart)):
        cc = _cache(ser.find(_c("cat")))
        vc = _cache(ser.find(_c("val")))
        cats = _read_cache(cc) + [str(new_category)]
        vals = _read_cache(vc) + [str(new_values[si])]
        _write_cache(cc, cats)
        _write_cache(vc, vals)


def replace_categories(chart, categories, series_values):
    """Fully replace the categories + each series of a per-day chart (contributors / flows)."""
    for si, ser in enumerate(_series(chart)):
        _write_cache(_cache(ser.find(_c("cat"))), [str(c) for c in categories])
        _write_cache(_cache(ser.find(_c("val"))), [str(v) for v in series_values[si]])


# chartN.xml -> slide index (verified for this template)
TS_CHARTS = {6: "pe_band", 7: "vnindex_fx", 8: "bond_yields", 9: "interbank"}
CAT_CHARTS = {3: "contributors", 4: "foreign_flows"}


def _chart_on(slide):
    for shp in slide.shapes:
        if shp.has_chart:
            return shp.chart
    return None


def update_charts(prs, provider):
    """provider: a ChartDataProvider (see chart_data.py). Skipped series are left as-is."""
    for si, key in TS_CHARTS.items():
        point = provider.timeseries_point(key)  # -> (category, [vals]) or None
        if point:
            append_point(_chart_on(prs.slides[si]), point[0], point[1])
    for si, key in CAT_CHARTS.items():
        cat = provider.category_chart(key)       # -> (categories, [series]) or None
        if cat:
            replace_categories(_chart_on(prs.slides[si]), cat[0], cat[1])


# --- Update charts directly from the Word report's EMBEDDED charts ----------
# The MAS Word .docx embeds the deck's charts as native OOXML (word/charts/
# chartN.xml) with full cached data. This copies that data straight into the
# deck's chart caches -- no external workbook, no manual transcription, and
# it is the authoritative daily source. Deck slide index -> Word chart number:
SLIDE_TO_WORDCHART = {3: 2, 4: 1, 6: 3, 7: 6, 8: 8, 9: 9}


def _copy_cache(src, dst):
    """Copy ptCount + every <c:pt> from one cache element to another,
    leaving the destination's <c:formatCode> untouched."""
    if src is None or dst is None:
        return
    sp, dp = src.find(_c("ptCount")), dst.find(_c("ptCount"))
    if sp is not None and dp is not None:
        dp.set("val", sp.get("val"))
    for pt in dst.findall(_c("pt")):
        dst.remove(pt)
    for pt in src.findall(_c("pt")):
        dst.append(deepcopy(pt))


def _word_chart_series(docx_path, n):
    with zipfile.ZipFile(docx_path) as z:
        root = etree.fromstring(z.read(f"word/charts/chart{n}.xml"))
    return root.findall(".//" + _c("ser"))


def update_charts_from_word(prs, docx_path, mapping=None):
    """Refresh the deck's charts from the Word report's embedded charts.
    Series are matched by position (names/order verified to align); if the
    Word chart has more series than the deck (e.g. bond yields duplicated onto
    a second axis), the extra Word series are ignored."""
    mapping = mapping or SLIDE_TO_WORDCHART
    for slide_idx, wc in mapping.items():
        chart = _chart_on(prs.slides[slide_idx])
        if chart is None:
            continue
        wsers = _word_chart_series(docx_path, wc)
        for pi, ps in enumerate(_series(chart)):
            if pi >= len(wsers):
                break
            ws = wsers[pi]
            _copy_cache(_cache(ws.find(_c("cat"))), _cache(ps.find(_c("cat"))))
            _copy_cache(_cache(ws.find(_c("val"))), _cache(ps.find(_c("val"))))


# ---------------------------------------------------------------------------
# 4. CLI
# ---------------------------------------------------------------------------
def inspect(template):
    prs = Presentation(template)
    for si, slide in enumerate(prs.slides):
        print(f"\n### SLIDE {si}")
        for shp in slide.shapes:
            txt = shp.text_frame.text.replace("\n", " | ") if shp.has_text_frame else ""
            tag = "TABLE" if shp.has_table else ("CHART" if shp.has_chart else "")
            print(f"  id={shp.shape_id:<4} {tag:<6} {shp.name:<22} {txt[:70]}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--template", required=True)
    ap.add_argument("--word")
    ap.add_argument("--out")
    ap.add_argument("--chart-source", choices=["none", "word", "csv", "fiinquant"],
                    default="word",
                    help="'word' (default): copy the deck's 6 charts from the Word "
                         "report's embedded charts; 'csv'/'fiinquant': external feed; "
                         "'none': leave charts as-is")
    ap.add_argument("--data-dir", default="./data")
    ap.add_argument("--fx-rate", type=float, default=DEFAULT_FX_RATE)
    ap.add_argument("--inspect", action="store_true")
    args = ap.parse_args(argv)

    if args.inspect:
        inspect(args.template)
        return 0

    if not (args.word and args.out):
        ap.error("--word and --out are required unless --inspect is used")

    fields = parse_word(args.word)
    prs = Presentation(args.template)
    apply_text(prs, fields, args.fx_rate)

    if args.chart_source == "word":
        update_charts_from_word(prs, args.word)
    elif args.chart_source != "none":
        from chart_data import get_provider
        update_charts(prs, get_provider(args.chart_source, Path(args.data_dir), fields))

    prs.save(args.out)
    print(f"Wrote {args.out}  (charts: {args.chart_source})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
