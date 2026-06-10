"""Data acquisition layer.

Two ways to obtain a `SessionData`:
  * `from_fixture(path)`  -- load a hand-checked JSON snapshot (offline / demo).
  * `from_vnstock(date)`  -- pull live from vnstock (HOSE) in your environment.

The vnstock column names occasionally shift between source providers, so the
adapter resolves columns defensively and raises a clear error if a required
field is missing.
"""

from __future__ import annotations

import datetime as dt
import json
from typing import Optional

from .compute import Mover, SessionData
from .config import INDEX_SYMBOL, VN30_FALLBACK, VNSTOCK_SOURCE


# --------------------------------------------------------------------------
# Offline fixture
# --------------------------------------------------------------------------
def from_fixture(path: str) -> SessionData:
    with open(path, "r", encoding="utf-8") as f:
        d = json.load(f)
    movers = [Mover(m["ticker"], float(m["pct"])) for m in d.get("vn30_movers", [])]
    d = {k: v for k, v in d.items() if k != "vn30_movers"}
    return SessionData(vn30_movers=movers, **d)


# --------------------------------------------------------------------------
# Live vnstock adapter
# --------------------------------------------------------------------------
def _first_col(df, *candidates):
    """Return the first candidate column present in df (case-insensitive)."""
    lower = {c.lower(): c for c in df.columns}
    for cand in candidates:
        if cand.lower() in lower:
            return lower[cand.lower()]
    raise KeyError(f"none of {candidates} in columns {list(df.columns)}")


def _index_ohlc(session_date: str):
    """Return (prev_close, open, high, low, close, volume, value_bn) for the index.

    Uses Quote.history with a small look-back window so we also capture the
    prior trading day's close (the DoD reference).
    """
    from vnstock.api.quote import Quote

    end = dt.date.fromisoformat(session_date)
    start = end - dt.timedelta(days=10)
    q = Quote(symbol=INDEX_SYMBOL, source=VNSTOCK_SOURCE)
    hist = q.history(start=start.isoformat(), end=end.isoformat(), interval="1D")
    hist = hist.sort_values(_first_col(hist, "time", "date")).reset_index(drop=True)

    today = hist.iloc[-1]
    prev = hist.iloc[-2]
    o = _first_col(hist, "open")
    h = _first_col(hist, "high")
    lo = _first_col(hist, "low")
    c = _first_col(hist, "close")
    vol = _first_col(hist, "volume")
    # value column name varies; may be absent for indices.
    try:
        val = _first_col(hist, "value", "amount")
        value_bn_today = float(today[val]) / 1e9
        value_bn_prev = float(prev[val]) / 1e9
    except KeyError:
        value_bn_today = value_bn_prev = float("nan")

    return {
        "prev_close": float(prev[c]),
        "open": float(today[o]),
        "high": float(today[h]),
        "low": float(today[lo]),
        "close": float(today[c]),
        "matched_volume": float(today[vol]),
        "prev_matched_volume": float(prev[vol]),
        "matched_value_bn": value_bn_today,
        "prev_matched_value_bn": value_bn_prev,
    }


def _vn30_symbols():
    try:
        from vnstock.api.listing import Listing

        syms = Listing(source=VNSTOCK_SOURCE).symbols_by_group("VN30")
        out = list(syms) if not hasattr(syms, "tolist") else syms.tolist()
        return out or VN30_FALLBACK
    except Exception:
        return VN30_FALLBACK


def _vn30_movers(symbols):
    """Daily % change per VN30 ticker via Trading.price_board."""
    from vnstock.api.trading import Trading

    board = Trading(source=VNSTOCK_SOURCE).price_board(symbols)
    # Flatten potential MultiIndex columns.
    if hasattr(board.columns, "nlevels") and board.columns.nlevels > 1:
        board.columns = ["_".join(str(p) for p in tup if p) for tup in board.columns]
    tick_col = _first_col(board, "symbol", "listing_symbol", "ticker", "cw_symbol")
    pct_col = _first_col(board, "change_pct", "pct_change", "match_change_pct",
                         "ratio_change", "%_change")
    movers = []
    for _, row in board.iterrows():
        try:
            pct = float(row[pct_col])
        except (TypeError, ValueError):
            continue
        # Some sources report fraction (0.0189) instead of percent (1.89).
        if abs(pct) < 0.5 and pct != 0:
            pct *= 100.0
        movers.append(Mover(str(row[tick_col]), round(pct, 2)))
    return movers


def from_vnstock(session_date: Optional[str] = None) -> SessionData:
    """Build a SessionData live. Breadth + foreign flows are best-effort and
    left at defaults if the provider does not expose them; fill them from the
    fixture or priceboard if needed."""
    if session_date is None:
        session_date = dt.date.today().isoformat()

    ohlc = _index_ohlc(session_date)
    movers = _vn30_movers(_vn30_symbols())

    return SessionData(
        date=session_date,
        vn30_movers=movers,
        **ohlc,
    )
