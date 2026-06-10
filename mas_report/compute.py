"""Deterministic computation + formatting. Fully offline / unit-tested.

This module holds all the number-crunching so it can be tested without any
network access. Nothing here calls an API.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import ROUND_HALF_UP, Decimal
from typing import List, Optional

from .config import NEG_SIGN, TOP_N_MOVERS


def round_half_up(value: float, decimals: int = 1) -> float:
    """Round-half-up (finance convention), avoiding float/banker's-rounding
    surprises: 1.65 -> 1.7, 1.45 -> 1.5, 0.649 -> 0.6."""
    q = Decimal(1).scaleb(-decimals)
    return float(Decimal(str(value)).quantize(q, rounding=ROUND_HALF_UP))


# --------------------------------------------------------------------------
# Input / output data structures
# --------------------------------------------------------------------------
@dataclass
class Mover:
    ticker: str
    pct: float  # daily % change, e.g. 1.89 or -1.94


@dataclass
class SessionData:
    """Raw numbers for one trading session (today) + the prior close."""

    date: str                 # ISO date of the session, e.g. "2026-06-10"
    prev_close: float         # previous trading day's index close (DoD reference)

    open: float
    high: float
    low: float
    close: float

    matched_volume: float     # matched shares traded (today), e.g. 625_012_446
    matched_value_bn: float   # matched value in VND bn (today), e.g. 19_786.58
    prev_matched_volume: float
    prev_matched_value_bn: float

    advancers: int = 0
    ceilings: int = 0
    unchanged: int = 0
    decliners: int = 0
    floors: int = 0

    vn30_movers: List[Mover] = field(default_factory=list)

    foreign_net_bn: Optional[float] = None    # +buy / -sell, VND bn
    foreign_buy_bn: Optional[float] = None
    foreign_sell_bn: Optional[float] = None
    foreign_top_buy: List[str] = field(default_factory=list)
    foreign_top_sell: List[str] = field(default_factory=list)


# --------------------------------------------------------------------------
# Math helpers
# --------------------------------------------------------------------------
def pct_change(today: float, reference: float) -> float:
    """Percentage change of `today` vs `reference`."""
    if reference == 0:
        raise ValueError("reference value is zero")
    return (today - reference) / reference * 100.0


# --------------------------------------------------------------------------
# Formatting helpers (match the MAS house style)
# --------------------------------------------------------------------------
def fmt_signed_pct(value: float, decimals: int = 1) -> str:
    """Format a percentage with explicit sign and the report's en-dash for
    negatives, e.g. 0.59 -> '+0.6%', -0.199 -> '–0.2%'."""
    rounded = round_half_up(value, decimals)
    if rounded == 0:  # avoid '-0.0' / '+-' edge cases
        rounded = 0.0
    sign = NEG_SIGN if rounded < 0 else "+"
    return f"{sign}{abs(rounded):.{decimals}f}%"


def fmt_dod(value: float, decimals: int = 1) -> str:
    return f"{fmt_signed_pct(value, decimals)} DoD"


def fmt_pts(value: float) -> str:
    """Index points with one decimal and thousands separators, e.g. 1803.71 -> '1,803.7'."""
    return f"{value:,.1f}"


def fmt_mn_shares(shares: float) -> str:
    """Shares -> 'NNNmn shares', e.g. 625_012_446 -> '625mn shares'."""
    return f"{round(shares / 1e6):,.0f}mn shares"


def fmt_vnd_bn(value_bn: float) -> str:
    """VND bn -> 'VNDx,xxxbn', e.g. 19786.58 -> 'VND19,787bn'."""
    return f"VND{round(value_bn):,.0f}bn"


# --------------------------------------------------------------------------
# Derived metrics
# --------------------------------------------------------------------------
@dataclass
class ReportMetrics:
    date: str
    # raw + formatted OHLC
    close: float
    close_change_pts: float
    open_dod: str
    high_dod: str
    low_dod: str
    close_dod: str
    open_pts: str
    high_pts: str
    low_pts: str
    close_pts: str
    # liquidity
    volume_str: str
    volume_dod: str
    value_str: str
    value_dod: str
    # breadth
    advancers: int
    ceilings: int
    decliners: int
    floors: int
    # movers
    gainers: List[Mover]
    losers: List[Mover]
    # foreign
    foreign_net_str: Optional[str]
    foreign_top_buy: List[str]
    foreign_top_sell: List[str]


def top_movers(movers: List[Mover], n: int = TOP_N_MOVERS):
    """Return (gainers, losers): top-n by % gain (desc) and % loss (asc)."""
    gainers = sorted((m for m in movers if m.pct > 0), key=lambda m: m.pct, reverse=True)[:n]
    losers = sorted((m for m in movers if m.pct < 0), key=lambda m: m.pct)[:n]
    return gainers, losers


def compute_metrics(s: SessionData) -> ReportMetrics:
    ref = s.prev_close
    gainers, losers = top_movers(s.vn30_movers)

    foreign_net_str = None
    if s.foreign_net_bn is not None:
        foreign_net_str = fmt_vnd_bn(abs(s.foreign_net_bn))

    return ReportMetrics(
        date=s.date,
        close=s.close,
        close_change_pts=s.close - ref,
        open_dod=fmt_dod(pct_change(s.open, ref)),
        high_dod=fmt_dod(pct_change(s.high, ref)),
        low_dod=fmt_dod(pct_change(s.low, ref)),
        close_dod=fmt_dod(pct_change(s.close, ref)),
        open_pts=fmt_pts(s.open),
        high_pts=fmt_pts(s.high),
        low_pts=fmt_pts(s.low),
        close_pts=fmt_pts(s.close),
        volume_str=fmt_mn_shares(s.matched_volume),
        volume_dod=fmt_dod(pct_change(s.matched_volume, s.prev_matched_volume)),
        value_str=fmt_vnd_bn(s.matched_value_bn),
        value_dod=fmt_dod(pct_change(s.matched_value_bn, s.prev_matched_value_bn)),
        advancers=s.advancers,
        ceilings=s.ceilings,
        decliners=s.decliners,
        floors=s.floors,
        gainers=gainers,
        losers=losers,
        foreign_net_str=foreign_net_str,
        foreign_top_buy=s.foreign_top_buy,
        foreign_top_sell=s.foreign_top_sell,
    )


def fmt_mover_list(movers: List[Mover], first_suffix: str = " DoD") -> str:
    """Render movers as 'VRE (+1.9% DoD), VJC (+1.7%), ...' — only the first
    item carries the 'DoD' suffix, matching the report style."""
    parts = []
    for i, m in enumerate(movers):
        suffix = first_suffix if i == 0 else ""
        parts.append(f"{m.ticker} ({fmt_signed_pct(m.pct)}{suffix})")
    return ", ".join(parts)
