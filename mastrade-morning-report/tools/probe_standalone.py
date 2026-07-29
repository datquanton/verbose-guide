#!/usr/bin/env python3
"""Standalone MAStrade endpoint probe — stdlib only, no repo, no pip install.

Answers one question: does the MAStrade quote endpoint already return open/high/low
and market breadth, or do those have to come from somewhere else?

Save this file anywhere and run it on a machine that can reach mastrade.masvn.com:

    python probe_standalone.py

Needs nothing but Python 3.8+. Writes probe_output/ (raw JSON per endpoint) and
probe_output/SHAPES.txt (every key each endpoint returned).

Read-only GETs, one at a time.
"""

from __future__ import annotations

import json
import os
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = os.environ.get("MASTRADE_BASE_URL", "https://mastrade.masvn.com")
SYMBOL = os.environ.get("MASTRADE_SYMBOL", "VN-INDEX")
OUTDIR = "probe_output"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/125.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": f"{BASE}/market/market-watch",
}

# What we're hunting for, and the names it might hide behind.
LOOKING_FOR = {
    "open":     ("o", "op", "open", "openIndex", "OpenIndex", "openPrice"),
    "high":     ("h", "hi", "high", "highIndex", "HighIndex", "highPrice"),
    "low":      ("l", "lo", "low", "lowIndex", "LowIndex", "lowPrice"),
    "advances": ("ad", "adv", "advances", "up", "totalUp", "UpCount", "gainers"),
    "declines": ("de", "dec", "declines", "down", "totalDown", "DownCount", "losers"),
}


def build_query(name, args, fields):
    """MAStrade's hand-rolled GraphQL-ish query string."""
    inner = ",".join(f"{k}:{json.dumps(v, ensure_ascii=False)}" for k, v in args.items())
    return f"query{{{name}({inner}){{{','.join(fields)}}}}}"


def get(path, params=None, insecure=False):
    url = BASE.rstrip("/") + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=HEADERS)
    ctx = None
    if insecure:  # mirrors the shipped script's SSLError fallback
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
    with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_retry(path, params=None):
    try:
        return get(path, params)
    except urllib.error.URLError as exc:
        if isinstance(getattr(exc, "reason", None), ssl.SSLError):
            return get(path, params, insecure=True)
        raise


def first_row(payload):
    """Pull one representative dict out of whatever shape came back."""
    if isinstance(payload, dict):
        data = payload.get("data")
        if isinstance(data, list) and data and isinstance(data[0], dict):
            return data[0]
        if isinstance(data, dict):
            return data
        return payload
    if isinstance(payload, list) and payload and isinstance(payload[0], dict):
        return payload[0]
    return {}


PROBES = [
    ("quote_index", lambda: get_retry(f"/api/v1/market/{SYMBOL}/quote")),
    ("quote_vn30", lambda: get_retry("/api/v1/market/VN30/quote")),
    ("quote_stock_HPG", lambda: get_retry("/api/v1/market/HPG/quote")),
    ("detail_index", lambda: get_retry("/api/v2/vs/detailIndex", {"query": build_query(
        "vsDetailIndex", {"fetchCount": 1, "symbol": SYMBOL},
        ["symbol", "TradingDate", "PE", "PB", "MarketCapital",
         "TotalForeignBuyVal", "TotalForeignSellVal"])})),
    ("foreign_total", lambda: get_retry("/api/v2/vs/foreignHistory", {"query": build_query(
        "vsForeignTotal", {"range": "1D"}, ["NetBuyVal"])})),
    ("top_foreign_buy", lambda: get_retry("/api/v1/market/top", {
        "top": "TOP_FOREIGN_NET_BUY_VALUE", "fetchCount": 4})),
    # Guesses. 404s here are still useful answers.
    ("top_gainer", lambda: get_retry("/api/v1/market/top", {"top": "TOP_GAINER", "fetchCount": 5})),
    ("top_loser", lambda: get_retry("/api/v1/market/top", {"top": "TOP_LOSER", "fetchCount": 5})),
    ("market_breadth", lambda: get_retry("/api/v1/market/breadth")),
    ("market_overview", lambda: get_retry("/api/v1/market/overview")),
]


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    print(f"probing {BASE}\n")

    shapes, quote_row = [], {}
    for label, fn in PROBES:
        try:
            payload = fn()
        except urllib.error.HTTPError as exc:
            print(f"[--] {label:20s} HTTP {exc.code}")
            shapes.append(f"### {label}\nHTTP {exc.code}\n")
        except Exception as exc:  # noqa: BLE001
            print(f"[--] {label:20s} {type(exc).__name__}: {str(exc)[:90]}")
            shapes.append(f"### {label}\n{type(exc).__name__}: {exc}\n")
        else:
            with open(os.path.join(OUTDIR, f"{label}.json"), "w", encoding="utf-8") as fh:
                json.dump(payload, fh, ensure_ascii=False, indent=2)
            row = first_row(payload)
            keys = sorted(row) if isinstance(row, dict) else []
            print(f"[ok] {label:20s} {len(keys)} keys")
            shapes.append(f"### {label}\nkeys: {keys}\nsample: "
                          f"{json.dumps(row, ensure_ascii=False)[:900]}\n")
            if label == "quote_index":
                quote_row = row
        time.sleep(0.4)

    with open(os.path.join(OUTDIR, "SHAPES.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(shapes))

    print("\n" + "=" * 62)
    print("ANSWER: does the quote endpoint already carry OHLC / breadth?")
    print("=" * 62)
    if not quote_row:
        print("  quote_index failed — nothing to check. See the errors above.")
    else:
        for logical, names in LOOKING_FOR.items():
            hit = next((n for n in names if n in quote_row), None)
            if hit:
                print(f"  {logical:9s} FOUND as '{hit}' = {quote_row[hit]!r}")
            else:
                print(f"  {logical:9s} not found")
        print(f"\n  all keys on the index quote: {sorted(quote_row)}")

    print(f"\nWrote {OUTDIR}/SHAPES.txt — send that over and the collector gets wired "
          "to the real names.")


if __name__ == "__main__":
    sys.exit(main())
