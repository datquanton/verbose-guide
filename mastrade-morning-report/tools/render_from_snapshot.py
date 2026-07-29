"""Re-render a .docx from a saved snapshot JSON, without calling the API.

Every run of mastrade_morning_report writes its full ReportData to
data/snapshots/*.json. That file contains everything build_docx needs, so a
report can be regenerated offline — handy for reissuing a report, for checking
formatting changes against real data, or for testing when the market is closed.

    python tools/render_from_snapshot.py data/snapshots/2026-07-29_114150.json
    python tools/render_from_snapshot.py snap.json -o out/report.docx
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent.parent / "src" / "mastrade_morning_report.py"


def _load_report_module():
    """Import the script by path, registering it so @dataclass can resolve it."""
    spec = importlib.util.spec_from_file_location("mastrade_morning_report", _SRC)
    module = importlib.util.module_from_spec(spec)
    sys.modules["mastrade_morning_report"] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("snapshot", type=Path, help="path to a snapshot .json")
    parser.add_argument("-o", "--output", type=Path, default=None)
    args = parser.parse_args()

    m = _load_report_module()

    raw = json.loads(args.snapshot.read_text(encoding="utf-8"))
    try:
        # Nested StockValue rows come back as plain dicts; build_docx needs attributes.
        for key in ("foreign_net_buy", "foreign_net_sell"):
            raw[key] = [m.StockValue(**row) for row in raw[key]]
        data = m.ReportData(**raw)
    except (KeyError, TypeError) as exc:
        raise SystemExit(f"{args.snapshot} is not a valid snapshot: {exc}") from exc

    output = args.output or args.snapshot.with_suffix(".docx")
    m.build_docx(data, output)
    print(f"Created: {output.resolve()}")


if __name__ == "__main__":
    main()
