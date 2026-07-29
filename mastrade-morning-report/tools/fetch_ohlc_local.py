"""Fetch session OHLC from public Vietnamese market-data APIs.

Run this on YOUR machine — it needs internet access to vndirect.com.vn, which the
sandbox where it was written does not have.

    python tools/fetch_ohlc_local.py                       # VNINDEX, last 5 sessions
    python tools/fetch_ohlc_local.py --symbol VN30 --days 10
    python tools/fetch_ohlc_local.py --json ohlc.json      # feed the commentary tool

Why an API instead of screenshotting DStock: OHLC is structured data. Scraping pixels
off a chart is slower, breaks whenever the page changes, and gives you numbers you then
have to re-key by hand. Use the browser only for things genuinely locked behind a login
(see "Driving your own Chrome" in the README).

ENDPOINT CAVEAT
---------------
api-finfo.vndirect.com.vn is the backend DStock and VNDirect's iBoard use, and its
response shape is stable in practice — but it is undocumented and was NOT reachable
from where this was written, so none of it is verified. Every field goes through
pick() with candidates, and --raw dumps the untouched response so you can see what
actually came back. If the shape has moved, --raw shows you exactly how.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from datetime import date, timedelta
from typing import Any

import requests

FINFO = "https://api-finfo.vndirect.com.vn/v4/stock_prices"

# Same defensive pattern as mastrade_commentary.CANDIDATES.
CANDIDATES: dict[str, tuple[str, ...]] = {
    "date":   ("date", "tradingDate", "TradingDate"),
    "open":   ("open", "openPrice", "adOpen", "o"),
    "high":   ("high", "highPrice", "adHigh", "h"),
    "low":    ("low", "lowPrice", "adLow", "l"),
    "close":  ("close", "closePrice", "adClose", "c"),
    "prev":   ("basicPrice", "refPrice", "priorClosePrice", "prevClose"),
    "volume": ("nmVolume", "totalVolume", "volume", "accumulatedVol"),
    "value":  ("nmValue", "totalValue", "value", "accumulatedVal"),
}


def pick(row: dict[str, Any], key: str, default: Any = None) -> Any:
    for name in CANDIDATES.get(key, (key,)):
        if name in row and row[name] not in (None, ""):
            return row[name]
    return default


@dataclass
class Session:
    date: str
    open: float | None
    high: float | None
    low: float | None
    close: float | None
    prev_close: float | None
    volume: float | None
    value: float | None

    @property
    def change_pct(self) -> float | None:
        if self.close is None or not self.prev_close:
            return None
        return (self.close - self.prev_close) / self.prev_close * 100


def _f(v: Any) -> float | None:
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def fetch(symbol: str, days: int, timeout: int = 30) -> tuple[list[Session], Any]:
    """Return (sessions newest-first, raw payload)."""
    start = date.today() - timedelta(days=days * 3)  # pad for weekends/holidays
    params = {
        "sort": "date",
        "q": f"code:{symbol}~date:gte:{start.isoformat()}~date:lte:{date.today().isoformat()}",
        "size": str(max(days * 2, 20)),
        "page": "1",
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/125.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://dstock.vndirect.com.vn",
        "Referer": "https://dstock.vndirect.com.vn/",
    }
    response = requests.get(FINFO, params=params, headers=headers, timeout=timeout)
    response.raise_for_status()
    payload = response.json()

    rows = payload.get("data") if isinstance(payload, dict) else payload
    if not rows:
        return [], payload

    sessions = [
        Session(
            date=str(pick(r, "date", "")),
            open=_f(pick(r, "open")),
            high=_f(pick(r, "high")),
            low=_f(pick(r, "low")),
            close=_f(pick(r, "close")),
            prev_close=_f(pick(r, "prev")),
            volume=_f(pick(r, "volume")),
            value=_f(pick(r, "value")),
        )
        for r in rows
    ]
    sessions.sort(key=lambda s: s.date, reverse=True)
    return sessions[:days], payload


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--symbol", default="VNINDEX", help="VNINDEX, VN30, or a ticker like HPG")
    p.add_argument("--days", type=int, default=5)
    p.add_argument("--json", dest="json_out", help="write parsed sessions here")
    p.add_argument("--raw", help="write the untouched API response here")
    args = p.parse_args()

    try:
        sessions, payload = fetch(args.symbol, args.days)
    except requests.RequestException as exc:
        raise SystemExit(f"request failed: {exc}") from exc
    except ValueError as exc:
        raise SystemExit(f"response was not JSON: {exc}") from exc

    if args.raw:
        with open(args.raw, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2)
        print(f"raw response -> {args.raw}", file=sys.stderr)

    if not sessions:
        raise SystemExit(
            f"no rows for {args.symbol}. Re-run with --raw out.json to see what came back; "
            "the field names may have moved (update CANDIDATES)."
        )

    unresolved = [k for k in ("open", "high", "low", "close") if getattr(sessions[0], k) is None]
    if unresolved:
        print(f"warning: could not resolve {', '.join(unresolved)} — check --raw output "
              "and update CANDIDATES", file=sys.stderr)

    print(f"{'date':12s} {'open':>10s} {'high':>10s} {'low':>10s} {'close':>10s} {'chg%':>8s}")
    for s in sessions:
        chg = "" if s.change_pct is None else f"{s.change_pct:+.2f}"
        cells = [f"{v:>10.2f}" if v is not None else f"{'-':>10s}"
                 for v in (s.open, s.high, s.low, s.close)]
        print(f"{s.date:12s} {' '.join(cells)} {chg:>8s}")

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump([asdict(s) for s in sessions], fh, ensure_ascii=False, indent=2)
        print(f"\nparsed -> {args.json_out}", file=sys.stderr)


if __name__ == "__main__":
    main()
