"""
Step 3 of the Daily MAS pipeline -- inject generated content into the EXISTING
.docx template (preserving layout, fonts, headers, disclaimers).

It targets, by content (not fragile indices):
  * the "VIETNAM STOCK MARKET" commentary cell  -> headline + 3 body paragraphs
  * the VN30 valuation table (matched by ticker) -> last price, performance,
    valuation, foreign ownership
  * the Summary box "Close" cell                 -> today's close

Charts and short-news are left for the next pipeline stage.

Usage:
    python -m mas_report.fill_docx template.docx report_data.json commentary.json -o out.docx
"""
from __future__ import annotations

import argparse
import json

from docx import Document


# --- low-level helpers -------------------------------------------------------

def set_paragraph_text(paragraph, text):
    """Replace a paragraph's text, keeping the first run's formatting."""
    if paragraph.runs:
        paragraph.runs[0].text = text
        for r in paragraph.runs[1:]:
            r.text = ""
    else:
        paragraph.add_run(text)


def find_commentary_cell(doc):
    """Return the cell holding the market commentary (headline + body)."""
    for tbl in doc.tables:
        for row in tbl.rows:
            for cell in row.cells:
                if cell.text.strip().upper().startswith("VIETNAM STOCK MARKET"):
                    # commentary body lives in the next row, same column
                    return tbl
    return None


def _fmt(v, dp=1):
    return f"{v:,.{dp}f}" if isinstance(v, (int, float)) else "N/A"


# --- fill steps --------------------------------------------------------------

def fill_commentary(doc, headline, body):
    tbl = find_commentary_cell(doc)
    if tbl is None:
        raise RuntimeError("Could not locate the 'VIETNAM STOCK MARKET' table")
    body_cell = tbl.rows[1].cells[0]
    paras = body_cell.paragraphs
    body_blocks = [b for b in body.split("\n\n") if b.strip()]

    # p0 = headline; p1.. = body paragraphs (template ships with 5 paragraphs)
    set_paragraph_text(paras[0], headline)
    for i, block in enumerate(body_blocks, start=1):
        if i < len(paras):
            set_paragraph_text(paras[i], block)
        else:  # template ran out of paragraphs -> append a new one
            body_cell.add_paragraph(block)
    # blank any leftover template paragraphs
    for j in range(1 + len(body_blocks), len(paras)):
        set_paragraph_text(paras[j], "")


def fill_vn30(doc, vn30):
    """Find the 36x24 valuation table and fill rows matched by ticker."""
    target = None
    for tbl in doc.tables:
        if len(tbl.columns) >= 23 and tbl.rows[0].cells[0].text.strip() == "Name":
            target = tbl
            break
    if target is None:
        return 0
    by_ticker = {v["ticker"]: v for v in vn30}
    filled = 0
    # columns: 4 Last, 5 52wH, 6 52wL, 8 1D, 9 1W, 10 1M, 11 1Y,
    #          13 PE, 14 PB, 15 ROE, 17 ForeignOwn
    colmap = [
        (4, "last", 0), (5, "52w_high", 0), (6, "52w_low", 0),
        (8, "1d", 1), (9, "1w", 1), (10, "1m", 1), (11, "1y", 1),
        (13, "pe", 1), (14, "pb", 1), (15, "roe", 1), (17, "foreign_own", 1),
    ]
    for row in target.rows:
        tk = row.cells[1].text.strip()
        if tk in by_ticker:
            v = by_ticker[tk]
            for col, key, dp in colmap:
                if v.get(key) is not None:
                    for p in row.cells[col].paragraphs:
                        if p.runs:
                            set_paragraph_text(p, _fmt(v[key], dp))
                            break
            filled += 1
    return filled


def fill_summary_close(doc, close_value):
    for tbl in doc.tables:
        for row in tbl.rows:
            if row.cells and row.cells[0].text.strip().startswith("Close") and len(row.cells) > 1:
                # the value sits in the adjacent cell
                set_paragraph_text(row.cells[1].paragraphs[0], f"{close_value:,.0f}")
                return True
    return False


def main(argv=None):
    ap = argparse.ArgumentParser(description="Fill the MAS .docx template")
    ap.add_argument("template", help="the existing Daily_MAS template .docx")
    ap.add_argument("data_json", help="report_data.json")
    ap.add_argument("commentary_json", help="commentary.json (headline/body)")
    ap.add_argument("-o", "--out", default="Daily_MAS_out.docx")
    args = ap.parse_args(argv)

    data = json.load(open(args.data_json, encoding="utf-8"))
    comm = json.load(open(args.commentary_json, encoding="utf-8"))

    doc = Document(args.template)
    fill_commentary(doc, comm["headline"], comm["body"])
    n = fill_vn30(doc, data["vn30"])
    fill_summary_close(doc, data["ohlc"]["close"]["today"])
    doc.save(args.out)
    print(f"[fill] commentary injected; {n} VN30 rows filled -> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
