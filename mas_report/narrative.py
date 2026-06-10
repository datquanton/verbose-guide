"""Turn computed metrics into the MAS 'Good Morning Vietnam' prose.

Two backends:
  * template  -- deterministic, offline. Assembles the structured paragraph;
                 weaves in 'driver' bullets (sector/ticker highlights) if given.
  * anthropic -- Claude drafts the prose in house style, using the metrics +
                 news + a one-shot example. Needs ANTHROPIC_API_KEY.
"""

from __future__ import annotations

from typing import List, Optional

from .compute import ReportMetrics, fmt_mover_list
from .config import ANTHROPIC_MODEL, NARRATIVE_BACKEND


def _breadth_sentence(m: ReportMetrics) -> str:
    return (f"Market breadth ended with {m.advancers} advancers "
            f"(incl. {m.ceilings} ceiling) against {m.decliners} decliners "
            f"({m.floors} floor).")


def _foreign_sentence(m: ReportMetrics) -> str:
    if not m.foreign_net_str:
        return ""
    s = f"Foreign investors were net sellers, with net outflows of approximately {m.foreign_net_str}."
    if m.foreign_top_sell:
        s += f" {', '.join(m.foreign_top_sell)} saw the heaviest net selling"
        if m.foreign_top_buy:
            s += f", whereas {m.foreign_top_buy[0]} drew the strongest net buying"
            if len(m.foreign_top_buy) > 1:
                s += f", followed by {', '.join(m.foreign_top_buy[1:])}"
        s += "."
    return s


def build_template_narrative(m: ReportMetrics, drivers: Optional[List[str]] = None) -> str:
    """Deterministic paragraph. `drivers` are short phrases describing the
    notable sector/ticker moves (from news); inserted if provided."""
    direction = "higher" if m.close_change_pts >= 0 else "lower"
    driver_clause = ""
    if drivers:
        driver_clause = " Notably, " + "; ".join(drivers) + "."

    para1 = (
        f"The VN-Index closed {direction} at {m.close_pts} pts ({m.close_dod}). "
        f"Matched volume came in at {m.volume_str} ({m.volume_dod}), "
        f"equivalent to {m.value_str} ({m.value_dod}). "
        f"The index opened at {m.open_pts} pts ({m.open_dod}), "
        f"touched an intraday low of {m.low_pts} pts ({m.low_dod}) "
        f"and a high of {m.high_pts} pts ({m.high_dod}). "
        f"{_breadth_sentence(m)}{driver_clause}"
    )

    para2 = (
        f"Within the VN30, the outperformers were led by {fmt_mover_list(m.gainers)}. "
        f"The downside was led by {fmt_mover_list(m.losers)}."
    )

    para3 = _foreign_sentence(m)
    return "\n\n".join(p for p in [para1, para2, para3] if p)


SAMPLE_STYLE = """\
The VN-Index managed to end marginally higher at 1,793.1 pts (+0.1% DoD), as renewed strength \
in banking stocks helped offset persistent weakness in the Vingroup ecosystem and oil & gas \
names. Despite the positive close, investor caution remained evident throughout the session, \
reflected in subdued trading activity, with matched volume declining to 527mn shares (-26% DoD), \
equivalent to VND13,740bn (-28% DoD). [...] Within the VN30, there were only a few outperformers, \
including ACB (+5.0% DoD), STB (+3.1%) [...]. Foreign investors were net sellers with VND579bn of \
net outflows [...]."""


def build_anthropic_narrative(m: ReportMetrics, news_text: str = "") -> str:
    import os

    import anthropic

    facts = build_template_narrative(m)  # structured facts as grounding
    prompt = (
        "You write the daily Vietnam market paragraph for Mirae Asset's "
        "'Good Morning Vietnam' report. Match the house style of this example "
        "(en-dash for negatives, '(+X.X% DoD)' tags, concise institutional tone):\n\n"
        f"EXAMPLE STYLE:\n{SAMPLE_STYLE}\n\n"
        "Write 3 paragraphs for TODAY using ONLY these verified facts (do not "
        "invent numbers). Keep all figures and DoD tags exactly as given. "
        "Use the news to describe sector/ticker drivers and sentiment in the "
        "first paragraph.\n\n"
        f"VERIFIED FACTS:\n{facts}\n\n"
        f"NEWS HEADLINES (for color only):\n{news_text or '(none)'}\n"
    )
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    resp = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=1200,
        messages=[{"role": "user", "content": prompt}],
    )
    return "".join(block.text for block in resp.content if block.type == "text").strip()


def build_narrative(m: ReportMetrics, drivers=None, news_text: str = "") -> str:
    if NARRATIVE_BACKEND == "anthropic":
        return build_anthropic_narrative(m, news_text=news_text)
    return build_template_narrative(m, drivers=drivers)
