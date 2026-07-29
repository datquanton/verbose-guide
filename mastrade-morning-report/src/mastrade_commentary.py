"""Collect the numbers behind the Daily_MAS "VIETNAM STOCK MARKET" commentary.

The morning report covers close / volume / value / foreign flows. The daily
commentary needs more:

    * OHLC for the session, each with a DoD comparison
    * market breadth (gainers, gainers up >1%, losers)
    * top 5 VN30 gainers and losers by % change
    * foreign buy and sell legs, not just the net

This module gathers those and drafts the commentary paragraph.

    python src/mastrade_commentary.py
    python src/mastrade_commentary.py --base-url http://127.0.0.1:8765

IMPORTANT — field names
-----------------------
The quote endpoint is known to use short keys (c, ch, r, vo, va) because the
shipped binary reads them. The keys for open/high/low and for breadth were NOT
verifiable when this was written, so every lookup goes through `pick()` with a
list of candidates and degrades to None rather than crashing. Run
`tools/probe_mastrade.py` from a machine that can reach the API, then add the
real names to the CANDIDATES table below — that is the only edit needed.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mastrade_morning_report import (  # noqa: E402
    BASE_URL,
    MastradeClient,
    fmt_number,
    load_previous_snapshot,
    pct_change,
    vnd_to_billion,
)

# The VN30 basket, taken from Table 1 of Daily_MAS_20260729.docx. The index is
# rebalanced twice a year, so re-check this against a current report each January
# and July. --vn30 overrides it without editing code.
VN30 = [
    "ACB", "BID", "BSR", "CTG", "FPT", "GAS", "GVR", "HDB", "HPG", "LPB",
    "MBB", "MSN", "MWG", "PLX", "SAB", "SHB", "SSB", "SSI", "STB", "TCB",
    "TPB", "VCB", "VHM", "VIB", "VIC", "VJC", "VNM", "VPB", "VPL", "VRE",
]

# Candidate key names, most likely first. Extend from probe output.
CANDIDATES: dict[str, tuple[str, ...]] = {
    "open":     ("o", "op", "open", "openIndex", "OpenIndex", "openPrice"),
    "high":     ("h", "hi", "high", "highIndex", "HighIndex", "highPrice"),
    "low":      ("l", "lo", "low", "lowIndex", "LowIndex", "lowPrice"),
    "close":    ("c", "close", "closeIndex", "ClosePrice"),
    "change":   ("ch", "change", "Change"),
    "rate":     ("r", "changePct", "PerChange", "perChange"),
    "volume":   ("vo", "volume", "totalVolume", "TotalVolume"),
    "value":    ("va", "value", "totalValue", "TotalValue"),
    "advances": ("ad", "adv", "advances", "up", "totalUp", "UpCount", "gainers"),
    "declines": ("de", "dec", "declines", "down", "totalDown", "DownCount", "losers"),
    "nochange": ("nc", "unchanged", "ref", "totalRef", "RefCount"),
    # TotalForeignBuyVal/TotalForeignSellVal are confirmed — detail_index() in the
    # shipped binary requests them by name. The rest are fallbacks.
    "fbuy":     ("TotalForeignBuyVal", "BuyVal", "TotalBuyVal", "ForeignBuyVal", "frBva"),
    "fsell":    ("TotalForeignSellVal", "SellVal", "TotalSellVal", "ForeignSellVal", "frSva"),
    "fnet":     ("NetBuyVal", "netVal", "NetVal"),
}


def pick(row: dict[str, Any] | None, key: str, default: Any = None) -> Any:
    """Read a logical field from a row, trying each known alias in turn."""
    if not row:
        return default
    for name in CANDIDATES.get(key, (key,)):
        if name in row and row[name] not in (None, ""):
            return row[name]
    return default


def _f(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _as_int(value: Any) -> int | None:
    """int() that keeps 0 as 0 and turns anything unparseable into None."""
    parsed = _f(value)
    return None if parsed is None else int(parsed)


def quote_pct(row: dict[str, Any]) -> float | None:
    """Percent change for a quote row.

    The index quote stores `r` as a fraction (0.0021 -> 0.21%); the recovered
    script multiplies by 100, so we follow that. If `r` is absent, derive it from
    the close and the absolute change instead.
    """
    rate = _f(pick(row, "rate"))
    if rate is not None:
        return rate * 100
    close, change = _f(pick(row, "close")), _f(pick(row, "change"))
    if close is not None and change is not None and close != change:
        return change / (close - change) * 100
    return None


@dataclass
class Mover:
    symbol: str
    pct: float


@dataclass
class CommentaryData:
    generated_at: str
    index_symbol: str

    # OHLC — open/high/low are None if the endpoint does not expose them.
    open: float | None
    high: float | None
    low: float | None
    close: float
    change: float
    change_pct: float | None

    # Each OHLC leg measured against the previous session's close.
    open_vs_prev_close_pct: float | None
    high_vs_prev_close_pct: float | None
    low_vs_prev_close_pct: float | None
    prev_close: float | None

    # Breadth — None when unavailable.
    advances: int | None
    declines: int | None
    unchanged: int | None

    volume_shares: int
    value_vnd: int
    volume_change_pct: float | None
    value_change_pct: float | None

    foreign_buy_billion: float | None
    foreign_sell_billion: float | None
    foreign_net_billion: float
    foreign_buy_change_pct: float | None
    foreign_sell_change_pct: float | None

    vn30_gainers: list[Mover] = field(default_factory=list)
    vn30_losers: list[Mover] = field(default_factory=list)


def vn30_movers(client: MastradeClient, symbols: list[str], top: int, verbose: bool = False):
    """Top/bottom movers in the VN30 basket, by percent change.

    Fetches each constituent's quote individually. That is 30 requests, but it
    relies only on the one endpoint the shipped binary proves exists, so it works
    without any endpoint discovery. If probing turns up a batch endpoint that
    returns the whole basket, swap it in here.
    """
    movers: list[Mover] = []
    for sym in symbols:
        try:
            row = client.quote(sym)
        except Exception as exc:  # noqa: BLE001 - one bad ticker must not kill the run
            if verbose:
                print(f"  ! {sym}: {type(exc).__name__}", file=sys.stderr)
            continue
        pct = quote_pct(row)
        if pct is not None:
            movers.append(Mover(symbol=sym, pct=pct))

    movers.sort(key=lambda m: m.pct, reverse=True)
    gainers = [m for m in movers if m.pct > 0][:top]
    losers = [m for m in movers if m.pct < 0]
    losers.sort(key=lambda m: m.pct)
    return gainers, losers[:top]


def collect(args: argparse.Namespace) -> CommentaryData:
    client = MastradeClient(args.base_url)
    quote = client.quote(args.index)
    now = datetime.now()

    prev = load_previous_snapshot(Path(args.snapshot_dir), now.strftime("%Y-%m-%d")) or {}

    close = _f(pick(quote, "close")) or 0.0
    change = _f(pick(quote, "change")) or 0.0
    prev_close = _f(prev.get("close"))
    if prev_close is None and close and change:
        prev_close = close - change  # same session's reference price

    def vs_prev(v: float | None) -> float | None:
        if v is None or not prev_close:
            return None
        return (v - prev_close) / prev_close * 100

    open_, high, low = (_f(pick(quote, k)) for k in ("open", "high", "low"))
    volume = int(_f(pick(quote, "volume")) or 0)
    value = int(_f(pick(quote, "value")) or 0)

    # Foreign flows: the buy/sell legs live on detailIndex, the net on foreignHistory.
    # They are sourced differently and do not always reconcile — see README.
    try:
        detail = client.detail_index(args.index)
    except Exception:  # noqa: BLE001
        detail = {}
    fbuy = _f(pick(detail, "fbuy"))
    fsell = _f(pick(detail, "fsell"))

    try:
        net = vnd_to_billion(client.foreign_total())
    except Exception:  # noqa: BLE001
        net = (vnd_to_billion(fbuy) - vnd_to_billion(fsell)) if (fbuy and fsell) else 0.0

    if args.verbose:
        print(f"  fetching {len(args.vn30)} VN30 quotes...", file=sys.stderr)
    gainers, losers = vn30_movers(client, args.vn30, args.top, args.verbose)

    return CommentaryData(
        generated_at=now.isoformat(timespec="seconds"),
        index_symbol=args.index,
        open=open_,
        high=high,
        low=low,
        close=close,
        change=change,
        change_pct=quote_pct(quote),
        open_vs_prev_close_pct=vs_prev(open_),
        high_vs_prev_close_pct=vs_prev(high),
        low_vs_prev_close_pct=vs_prev(low),
        prev_close=prev_close,
        advances=_as_int(pick(quote, "advances")),
        declines=_as_int(pick(quote, "declines")),
        unchanged=_as_int(pick(quote, "nochange")),
        volume_shares=volume,
        value_vnd=value,
        volume_change_pct=pct_change(volume, prev.get("volume_shares")),
        value_change_pct=pct_change(value, prev.get("value_vnd")),
        foreign_buy_billion=vnd_to_billion(fbuy) if fbuy is not None else None,
        foreign_sell_billion=vnd_to_billion(fsell) if fsell is not None else None,
        foreign_net_billion=net,
        foreign_buy_change_pct=pct_change(vnd_to_billion(fbuy), prev.get("foreign_buy_billion"))
        if fbuy is not None else None,
        foreign_sell_change_pct=pct_change(vnd_to_billion(fsell), prev.get("foreign_sell_billion"))
        if fsell is not None else None,
        vn30_gainers=gainers,
        vn30_losers=losers,
    )


# --------------------------------------------------------------------------- #
# Rendering
# --------------------------------------------------------------------------- #

def _pct1(v: float) -> str:
    """Always one decimal, always signed — the house style is '+3.0%', not '+3%'."""
    return f"{v:+.1f}%"


def _dod(pct: float | None) -> str:
    return "n/a" if pct is None else f"{_pct1(pct)} DoD"


def _paren_dod(pct: float | None) -> str:
    """' (+3.0% DoD)', or nothing at all when there is no comparison to make."""
    return "" if pct is None else f" ({_dod(pct)})"


def _pts(v: float | None) -> str:
    return "n/a" if v is None else f"{fmt_number(v, 0)}pts"


def _movers(items: list[Mover]) -> str:
    return ", ".join(f"{m.symbol} ({_pct1(m.pct)})" for m in items)


def render_commentary(d: CommentaryData) -> str:
    """Draft the commentary paragraph in the house style of Daily_MAS.

    Deliberately plain: it states what happened and leaves the narrative framing
    ("the green of hope", sector attribution, one-off block trades) to the analyst.
    """
    direction = "gained" if d.change > 0 else "fell" if d.change < 0 else "was flat"
    out = []

    session = [f"The {d.index_symbol} {direction}, closing at {_pts(d.close)} ({_dod(d.change_pct)})."]
    if d.open is not None:
        session.append(
            f"It opened at {_pts(d.open)} ({_dod(d.open_vs_prev_close_pct)}), "
            f"traded between an intraday low of {_pts(d.low)} ({_dod(d.low_vs_prev_close_pct)}) "
            f"and a high of {_pts(d.high)} ({_dod(d.high_vs_prev_close_pct)})."
        )
    out.append(" ".join(session))

    if d.advances is not None and d.declines is not None:
        out.append(f"Market breadth: {d.advances} gainers against {d.declines} losers.")

    out.append(
        f"Trading volume was {fmt_number(d.volume_shares / 1_000_000, 0)}mn shares"
        f"{_paren_dod(d.volume_change_pct)} and trading value "
        f"VND{fmt_number(d.value_vnd / 1e9, 0)}bn{_paren_dod(d.value_change_pct)}."
    )

    # Either side can be empty on a strongly one-directional day, so build the
    # clauses separately rather than assuming both exist.
    clauses = []
    if d.vn30_gainers:
        clauses.append(f"the top gainers were {_movers(d.vn30_gainers)}")
    if d.vn30_losers:
        lead = "while " if clauses else ""
        clauses.append(f"{lead}{_movers(d.vn30_losers)} were the biggest drag on the index")
    if clauses:
        out.append(f"Within the VN30 basket {', '.join(clauses)}.")

    side = "net buyers" if d.foreign_net_billion >= 0 else "net sellers"
    flow = f"Foreign investors were {side} of VND{fmt_number(abs(d.foreign_net_billion), 0)}bn"
    if d.foreign_buy_billion is not None and d.foreign_sell_billion is not None:
        flow += (
            f", including VND{fmt_number(d.foreign_buy_billion, 0)}bn in buying"
            f"{_paren_dod(d.foreign_buy_change_pct)} and "
            f"VND{fmt_number(d.foreign_sell_billion, 0)}bn in selling"
            f"{_paren_dod(d.foreign_sell_change_pct)}"
        )
    out.append(flow + ".")

    return "\n\n".join(out)


def parse_args(argv=None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Collect Daily_MAS commentary inputs from MAStrade.")
    p.add_argument("--base-url", default=BASE_URL)
    p.add_argument("--index", default="VN-INDEX")
    p.add_argument("--top", type=int, default=5, help="how many VN30 movers per side")
    p.add_argument("--vn30", nargs="*", default=VN30, help="override the VN30 basket")
    p.add_argument("--snapshot-dir", default="data/commentary_snapshots")
    p.add_argument("--output", type=Path, default=None, help="write the draft text here")
    p.add_argument("--json", type=Path, default=None, help="write the collected data here")
    p.add_argument("--no-save-snapshot", action="store_true")
    p.add_argument("--verbose", action="store_true")
    return p.parse_args(argv)


def main() -> None:
    args = parse_args()
    data = collect(args)
    text = render_commentary(data)

    print(text)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
        print(f"\nDraft: {args.output.resolve()}", file=sys.stderr)
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(asdict(data), ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Data:  {args.json.resolve()}", file=sys.stderr)

    if not args.no_save_snapshot:
        snap = Path(args.snapshot_dir)
        snap.mkdir(parents=True, exist_ok=True)
        path = snap / datetime.now().strftime("%Y-%m-%d_%H%M%S.json")
        path.write_text(json.dumps(asdict(data), ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
