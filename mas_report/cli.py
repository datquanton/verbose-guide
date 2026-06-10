"""CLI orchestrator.

Examples:
  # Offline, from a verified fixture (works anywhere):
  python -m mas_report.cli --fixture sample_data/session_2026-06-10.json \
      --drivers "a wave of real estate names (NVL, CII, LDG) surged to their ceiling prices" \
      --drivers "large-cap anchors VIC and VRE contributed the bulk of the index's points" \
      --out out/report_2026-06-10.docx

  # Live, in an environment with vnstock access:
  python -m mas_report.cli --live --date 2026-06-10 --out out/report.docx
"""

from __future__ import annotations

import argparse
import os
import sys

from . import data as data_mod
from .compute import compute_metrics
from .docx_builder import build_fresh, fill_template
from .narrative import build_narrative


def main(argv=None):
    p = argparse.ArgumentParser(description="Generate the MAS daily market report.")
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--fixture", help="path to a verified session JSON")
    src.add_argument("--live", action="store_true", help="fetch live via vnstock")
    p.add_argument("--date", help="session date YYYY-MM-DD (live mode)")
    p.add_argument("--drivers", action="append", default=[],
                   help="market-driver phrase (repeatable; template backend)")
    p.add_argument("--template", help="MAS template .docx with a {{NARRATIVE}} placeholder")
    p.add_argument("--out", default="report.docx", help="output .docx path")
    p.add_argument("--print", dest="print_only", action="store_true",
                   help="print narrative to stdout, skip docx")
    args = p.parse_args(argv)

    if args.fixture:
        session = data_mod.from_fixture(args.fixture)
    else:
        session = data_mod.from_vnstock(args.date)

    metrics = compute_metrics(session)

    news_text = ""
    if os.environ.get("NARRATIVE_BACKEND") == "anthropic":
        try:
            from .news import fetch_headlines, headlines_as_text
            news_text = headlines_as_text(fetch_headlines(session.date))
        except Exception as e:  # news is best-effort
            print(f"[warn] news fetch failed: {e}", file=sys.stderr)

    narrative = build_narrative(metrics, drivers=args.drivers, news_text=news_text)

    print(narrative)
    if args.print_only:
        return 0

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    if args.template:
        fill_template(args.template, narrative, args.out)
    else:
        build_fresh(metrics, narrative, args.out)
    print(f"\n[ok] wrote {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
