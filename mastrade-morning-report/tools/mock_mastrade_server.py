"""Offline stand-in for the MAStrade API.

Lets you exercise mastrade_morning_report end-to-end (including the frozen .exe)
without touching the real endpoint:

    python tools/mock_mastrade_server.py 8765 &
    python src/mastrade_morning_report.py --base-url http://127.0.0.1:8765 --output out.docx

The response shapes here were derived from how the script consumes them, so this
doubles as documentation of the API contract the script expects.
"""

from __future__ import annotations

import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

# /api/v1/market/<symbol>/quote  ->  {"data": [ {...} ]}
#   c  = close/current index value      ch = absolute change
#   r  = fractional change (0.0049 = 0.49%; the script multiplies by 100)
#   vo = volume in shares               va = traded value in VND
QUOTE = {"data": [{"c": 1281.45, "ch": 6.32, "r": 0.004956, "vo": 412_300_000, "va": 9_874_000_000_000}]}

# /api/v2/vs/detailIndex  ->  list of rows; the script takes row[0]
DETAIL_INDEX = [
    {
        "symbol": "VN-INDEX",
        "TradingDate": "2026-07-29",
        "PE": 13.42,
        "PB": 1.71,
        "Max52WCloseIndex": 1350.2,
        "Min52WCloseIndex": 1035.8,
        "TotalForeignBuyVal": 1_520_000_000_000,
        "TotalForeignSellVal": 1_180_000_000_000,
        "MarketCapital": 5_120_000_000_000_000,
    }
]

# /api/v2/vs/stockInfluence -> list of rows keyed by StockCode
INFLUENCE_UP = [{"StockCode": s, "InfluenceIndex": 1.0} for s in ("VCB", "FPT", "HPG", "GAS", "VIC")]
INFLUENCE_DOWN = [{"StockCode": s, "InfluenceIndex": -1.0} for s in ("VHM", "MSN", "BID", "CTG", "MWG")]

# /api/v2/vs/foreignHistory -> single object
FOREIGN_TOTAL = {"NetBuyVal": 340_500_000_000}

# /api/v1/market/top -> list of rows;  s = symbol, frBva = foreign buy, frSva = foreign sell
TOP_BUY = [
    {"s": "FPT", "frBva": 300_000_000_000, "frSva": 179_600_000_000},
    {"s": "HPG", "frBva": 210_000_000_000, "frSva": 121_900_000_000},
]
TOP_SELL = [
    {"s": "VHM", "frBva": 40_000_000_000, "frSva": 104_200_000_000},
    {"s": "MSN", "frBva": 22_000_000_000, "frSva": 53_900_000_000},
]


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):  # keep test output readable
        sys.stderr.write("  mock <- %s\n" % (fmt % args))

    def _send(self, payload):
        body = json.dumps(payload).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        path, qs = parsed.path, parse_qs(parsed.query)
        query = (qs.get("query") or [""])[0]

        if path.endswith("/quote"):
            return self._send(QUOTE)
        if path == "/api/v2/vs/detailIndex":
            return self._send(DETAIL_INDEX)
        if path == "/api/v2/vs/stockInfluence":
            return self._send(INFLUENCE_DOWN if '"ASC"' in query else INFLUENCE_UP)
        if path == "/api/v2/vs/foreignHistory":
            return self._send(FOREIGN_TOTAL)
        if path == "/api/v1/market/top":
            top = (qs.get("top") or [""])[0]
            return self._send(TOP_SELL if "SELL" in top else TOP_BUY)

        self.send_error(404, f"no mock for {path}")


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    print(f"mock MAStrade API on http://127.0.0.1:{port}", flush=True)
    HTTPServer(("127.0.0.1", port), Handler).serve_forever()
