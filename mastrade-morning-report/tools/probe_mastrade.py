"""Discover what the MAStrade endpoints actually return.

The recovered script only reads five fields off the quote endpoint (c, ch, r, vo, va),
but the response almost certainly carries more — open/high/low, market breadth, and so on.
This dumps the raw JSON for every endpoint we know about, plus a few candidate ones,
so the commentary collector can be wired to real field names instead of guesses.

Run it from a machine that can reach mastrade.masvn.com:

    python tools/probe_mastrade.py                    # writes probe_output/*.json
    python tools/probe_mastrade.py --symbol VN30

Read-only GETs, one at a time, with a small delay between them.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from mastrade_morning_report import BASE_URL, MastradeClient  # noqa: E402


def _describe(value, depth: int = 0) -> str:
    """One-line shape summary: keys for dicts, element shape for lists."""
    pad = "  " * depth
    if isinstance(value, dict):
        lines = [f"{pad}dict with {len(value)} keys:"]
        for k, v in value.items():
            kind = type(v).__name__
            preview = "" if isinstance(v, (dict, list)) else f" = {v!r}"
            lines.append(f"{pad}  {k:28s} {kind}{preview}")
        return "\n".join(lines)
    if isinstance(value, list):
        if not value:
            return f"{pad}empty list"
        return f"{pad}list[{len(value)}] of:\n" + _describe(value[0], depth + 1)
    return f"{pad}{type(value).__name__} = {value!r}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--base-url", default=BASE_URL)
    parser.add_argument("--symbol", default="VN-INDEX")
    parser.add_argument("--outdir", type=Path, default=Path("probe_output"))
    parser.add_argument("--delay", type=float, default=0.5, help="seconds between requests")
    args = parser.parse_args()

    client = MastradeClient(args.base_url)
    args.outdir.mkdir(parents=True, exist_ok=True)

    # (label, callable) — each returns parsed JSON.
    probes = [
        # Known-good, from the recovered script. We want the FULL response, not
        # just the five fields the script reads.
        ("quote_index", lambda: client.get_json(f"/api/v1/market/{args.symbol}/quote")),
        ("quote_vn30", lambda: client.get_json("/api/v1/market/VN30/quote")),
        ("quote_single_stock", lambda: client.get_json("/api/v1/market/HPG/quote")),
        ("detail_index", lambda: client.detail_index(args.symbol)),
        ("foreign_total", lambda: client.graphql_query(
            "/api/v2/vs/foreignHistory", "vsForeignTotal", {"range": "1D"},
            ["NetBuyVal", "BuyVal", "SellVal", "TotalBuyVal", "TotalSellVal"])),
        ("influence_desc", lambda: client.stock_influence(args.symbol, "DESC", 5)),
        ("top_foreign_buy", lambda: client.foreign_top("TOP_FOREIGN_NET_BUY_VALUE", 4)),

        # Candidates — we do not know these exist. 404s are expected and are
        # themselves useful information.
        ("top_gainer", lambda: client.foreign_top("TOP_GAINER", 5)),
        ("top_loser", lambda: client.foreign_top("TOP_LOSER", 5)),
        ("top_price_increase", lambda: client.foreign_top("TOP_PRICE_INCREASE", 5)),
        ("top_price_decrease", lambda: client.foreign_top("TOP_PRICE_DECREASE", 5)),
        ("market_breadth", lambda: client.get_json("/api/v1/market/breadth")),
        ("market_overview", lambda: client.get_json("/api/v1/market/overview")),
        ("index_list", lambda: client.get_json("/api/v1/market/index")),
        ("group_vn30", lambda: client.get_json("/api/v1/market/group", {"group": "VN30"})),
    ]

    report = []
    for label, fn in probes:
        try:
            payload = fn()
        except Exception as exc:  # noqa: BLE001 - we want every failure recorded
            status = getattr(getattr(exc, "response", None), "status_code", None)
            note = f"{type(exc).__name__}: {status or str(exc)[:120]}"
            print(f"[--] {label:22s} {note}")
            report.append(f"### {label}\nFAILED: {note}\n")
        else:
            path = args.outdir / f"{label}.json"
            path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            shape = _describe(payload)
            first = shape.splitlines()[0]
            print(f"[ok] {label:22s} -> {path}  ({first})")
            report.append(f"### {label}\n{shape}\n")
        time.sleep(args.delay)

    summary = args.outdir / "SHAPES.txt"
    summary.write_text("\n".join(report), encoding="utf-8")
    print(f"\nField inventory: {summary}")
    print("Send that file over and the collector can be wired to the real field names.")


if __name__ == "__main__":
    main()
