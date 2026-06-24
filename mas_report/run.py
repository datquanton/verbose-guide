"""
Orchestrator -- one command to build the day's report from the workbook.

    python -m mas_report.run --xlsm data.xlsm --template template.docx --news "..."

Produces Daily_MAS_<YYYYMMDD>.docx next to the template (date taken from --date,
defaulting to the workbook's mtime so the run is reproducible).
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import os

from . import commentary, extract, fill_docx


def build(xlsm, template, news="", date=None, outdir="."):
    data = extract.extract(xlsm)

    comm = commentary.generate(data, news)

    from docx import Document
    doc = Document(template)
    fill_docx.fill_commentary(doc, comm["headline"], comm["body"])
    n = fill_docx.fill_vn30(doc, data["vn30"])
    fill_docx.fill_summary_close(doc, data["ohlc"]["close"]["today"])

    if date is None:
        date = _dt.date.fromtimestamp(os.path.getmtime(xlsm))
    out = os.path.join(outdir, f"Daily_MAS_{date:%Y%m%d}.docx")
    doc.save(out)

    # keep the structured data + commentary alongside, for audit / reuse
    with open(os.path.join(outdir, f"report_data_{date:%Y%m%d}.json"), "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2, default=str)

    print(f"[run] {out}  ({n} VN30 rows, close {data['ohlc']['close']['today']:,})")
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="Build the Daily MAS report")
    ap.add_argument("--xlsm", required=True, help="Bloomberg-updated workbook")
    ap.add_argument("--template", required=True, help="Daily_MAS template .docx")
    ap.add_argument("--news", default="", help="one-line news driver for the commentary")
    ap.add_argument("--date", help="report date YYYY-MM-DD (default: workbook mtime)")
    ap.add_argument("--outdir", default=".", help="output directory")
    args = ap.parse_args(argv)

    date = _dt.date.fromisoformat(args.date) if args.date else None
    build(args.xlsm, args.template, args.news, date, args.outdir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
