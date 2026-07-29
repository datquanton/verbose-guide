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

# ---------------------------------------------------------------------------
# Fixture for the commentary collector, using the real 28 Jul 2026 session as
# published in Daily_MAS_20260729.docx (prev close 1,669.01 from its Table 1).
# `o`/`h`/`l` and the breadth keys are our best guess at the real names — if
# tools/probe_mastrade.py shows otherwise, fix them here and in CANDIDATES.
# ---------------------------------------------------------------------------
COMMENTARY_QUOTE = {
    "data": [{
        "o": 1654.0, "h": 1685.0, "l": 1651.0, "c": 1681.0,
        "ch": 11.99, "r": 0.00718,
        "vo": 805_000_000, "va": 19_197_000_000_000,
        "ad": 195, "de": 128, "nc": 42,
    }]
}

COMMENTARY_DETAIL = [{
    "symbol": "VN-INDEX", "PE": 13.7, "PB": 1.9,
    "MarketCapital": 7_968_147_000_000_000,
    "TotalForeignBuyVal": 2_937_000_000_000,
    "TotalForeignSellVal": 4_907_000_000_000,
}]

COMMENTARY_FOREIGN_TOTAL = {"NetBuyVal": -1_970_000_000_000}

# VN30 constituents with the percent moves quoted in the published commentary.
VN30_PCT = {
    "SSI": 4.5, "HPG": 3.1, "MWG": 3.0, "VNM": 2.9, "MSN": 2.8,
    "VJC": -2.0, "SAB": -1.0, "LPB": -0.9, "HDB": -0.7, "SHB": -0.4,
    "ACB": 1.2, "BID": 0.8, "BSR": 0.5, "CTG": 1.1, "FPT": 2.2,
    "GAS": 0.3, "GVR": -0.2, "MBB": 1.5, "PLX": 0.1, "SSB": 0.6,
    "STB": 1.9, "TCB": 0.9, "TPB": -0.1, "VCB": 0.7, "VHM": 2.1,
    "VIB": 0.4, "VIC": 1.7, "VPB": 1.3, "VPL": -0.3, "VRE": 2.6,
}

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
            symbol = path.split("/")[-2]
            if symbol in VN30_PCT and self.server.commentary:
                pct = VN30_PCT[symbol]
                close = 20_000 * (1 + pct / 100)
                return self._send({"data": [{
                    "c": round(close, 2), "ch": round(close - 20_000, 2), "r": pct / 100,
                    "vo": 1_000_000, "va": 20_000_000_000,
                }]})
            return self._send(COMMENTARY_QUOTE if self.server.commentary else QUOTE)
        if path == "/api/v2/vs/detailIndex":
            return self._send(COMMENTARY_DETAIL if self.server.commentary else DETAIL_INDEX)
        if path == "/api/v2/vs/stockInfluence":
            return self._send(INFLUENCE_DOWN if '"ASC"' in query else INFLUENCE_UP)
        if path == "/api/v2/vs/foreignHistory":
            return self._send(COMMENTARY_FOREIGN_TOTAL if self.server.commentary else FOREIGN_TOTAL)
        if path == "/api/v1/market/top":
            top = (qs.get("top") or [""])[0]
            return self._send(TOP_SELL if "SELL" in top else TOP_BUY)

        self.send_error(404, f"no mock for {path}")


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    # --commentary serves the richer 28 Jul 2026 fixture used by mastrade_commentary.py
    commentary = "--commentary" in sys.argv
    server = HTTPServer(("127.0.0.1", port), Handler)
    server.commentary = commentary
    print(f"mock MAStrade API on http://127.0.0.1:{port}"
          f"{' [commentary fixture]' if commentary else ''}", flush=True)
    server.serve_forever()
