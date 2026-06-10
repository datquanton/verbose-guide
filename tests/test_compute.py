"""Offline unit tests for the deterministic compute layer (today's session)."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mas_report.compute import (  # noqa: E402
    Mover, SessionData, compute_metrics, fmt_dod, fmt_mover_list,
    fmt_signed_pct, fmt_vnd_bn, pct_change, top_movers,
)


def _session():
    return SessionData(
        date="2026-06-10", prev_close=1793.05,
        open=1793.39, high=1804.68, low=1789.48, close=1803.71,
        matched_volume=625_012_446, matched_value_bn=19_786.58,
        prev_matched_volume=527_000_000, prev_matched_value_bn=13_740,
        advancers=197, ceilings=10, decliners=103, floors=2,
        vn30_movers=[Mover("VRE", 1.89), Mover("STB", -1.94), Mover("BID", 1.22),
                     Mover("VJC", 1.68), Mover("PLX", -1.11)],
        foreign_net_bn=-550, foreign_top_sell=["MBB"], foreign_top_buy=["VJC", "VNM"],
    )


def test_pct_change():
    assert round(pct_change(1803.71, 1793.05), 2) == 0.59


def test_signed_pct_formatting():
    assert fmt_signed_pct(0.59) == "+0.6%"
    assert fmt_signed_pct(-0.199) == "–0.2%"   # en-dash
    assert fmt_signed_pct(0.019) == "+0.0%"    # rounds to flat, no '-0.0'


def test_dod_tags_match_hand_analysis():
    m = compute_metrics(_session())
    assert m.close_dod == "+0.6% DoD"
    assert m.high_dod == "+0.6% DoD"   # 11.63/1793.05 = 0.649% -> rounds to 0.6%
    assert m.low_dod == "–0.2% DoD"
    assert m.open_dod == "+0.0% DoD"
    assert m.volume_dod == "+18.6% DoD"
    assert m.value_dod == "+44.0% DoD"


def test_liquidity_strings():
    m = compute_metrics(_session())
    assert m.volume_str == "625mn shares"
    assert m.value_str == "VND19,787bn"
    assert fmt_vnd_bn(13_740) == "VND13,740bn"


def test_round_half_up_finance_convention():
    # values that bite default round(): 1.65 and 1.45 must round UP
    assert fmt_signed_pct(1.65) == "+1.7%"
    assert fmt_signed_pct(1.45) == "+1.5%"


def test_top_movers_split_and_order():
    gainers, losers = top_movers(_session().vn30_movers, n=5)
    assert [g.ticker for g in gainers] == ["VRE", "VJC", "BID"]
    assert [l.ticker for l in losers] == ["STB", "PLX"]


def test_mover_list_only_first_has_dod():
    m = compute_metrics(_session())
    s = fmt_mover_list(m.gainers)
    assert s.startswith("VRE (+1.9% DoD)")
    assert "VJC (+1.7%)" in s and "VJC (+1.7% DoD)" not in s


if __name__ == "__main__":
    import pytest
    raise SystemExit(pytest.main([__file__, "-v"]))
