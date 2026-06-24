"""
Step 2 of the Daily MAS pipeline -- the worded market commentary (the longest
manual part).

Design:
  * All NUMBERS come straight from report_data.json (deterministic -- no model
    ever invents a figure). build_facts() formats them the way the house writes.
  * Only the NARRATIVE -- ordering, the day's driver, the prose voice -- is
    written by Claude, tightly constrained to the facts + a news driver string.
  * If no ANTHROPIC_API_KEY is set, a deterministic template still produces a
    usable draft, so the pipeline never hard-fails.

Usage:
    python -m mas_report.commentary report_data.json --news "LPB locked limit-up
        after Vingroup Chairman Pham Nhat Vuong bought 146.2mn LPB shares (4.8%)."
"""
from __future__ import annotations

import argparse
import json
import os
import textwrap

MODEL = "claude-opus-4-8"

# One real published session, used as a style anchor (few-shot). Keep this in
# sync with whatever the desk considers "house voice".
STYLE_EXAMPLE = textwrap.dedent("""\
    Headline: High-volume volatility shakes trading session
    Body: Driven by persistent momentum from the Vingroup cohort, the VN-Index
    climbed higher on Tuesday, opening up at 1,871.9pts (+0.8% DoD). Early buying
    interest in VIC and VHM quickly propelled the index to an intraday high of
    1,886.6pts (+1.5% DoD), though this initial peak faded as the morning session
    progressed. ... A late-session rebound lifted the VN-Index to close at
    1,869.0pts (+0.6% DoD) with nearly 15pts contribution from VIC. This
    volatility triggered a massive surge in market liquidity, with trading volume
    soaring to 945mn shares (+82.0% DoD) and trading value spiking to VND30,989bn
    (+112.0% DoD).""")

SYSTEM_PROMPT = textwrap.dedent("""\
    You are a sell-side equity strategist at Mirae Asset Securities (Vietnam)
    writing the "Good Morning Vietnam" daily market commentary. Write in the
    desk's established voice: concise, factual, lightly narrative, present-to-past
    tense for the session just closed. British/US business-press register.

    Output EXACTLY three paragraphs, no headers inside the body:
      P1: the index's intraday path (open -> high/low -> close) with DoD figures,
          the session's main driver, and the liquidity surge/contraction.
      P2: "Within VN30, <gainers> were the largest gain contributors to the index.
          Meanwhile, <losers> capped the market's upside."
      P3: the foreign-flow line.

    Also produce a 4-8 word headline capturing the session.

    HARD RULES:
      * Use ONLY the numbers in the FACTS block. Never invent or round differently.
      * Quote every percentage/level exactly as given.
      * The only non-FACTS content allowed is the NEWS DRIVER, woven into P1.
      * Return strict JSON: {"headline": "...", "body": "...paragraphs joined by \\n\\n..."}
    """)


def _pct(v, dp=1):
    return f"{v*100:+.{dp}f}%" if isinstance(v, (int, float)) else "n/a"


def _fmt_movers(rows):
    return ", ".join(f"{r['ticker'].replace(' VN','')} ({_pct(r['1d']/100)})" for r in rows)


def build_facts(data: dict) -> str:
    """Render the deterministic facts block the model must stay inside."""
    o = data["ohlc"]
    def line(lbl, k):
        c = o[k]
        return f"  {lbl}: {c['today']:,} (prev {c['prev']:,}, {_pct(c['dod'])} DoD)"
    f = data["flows"]
    return textwrap.dedent(f"""\
        VN-INDEX OHLC (points):
        {line('Open', 'open')}
        {line('High', 'high')}
        {line('Low', 'low')}
        {line('Close', 'close')}
        LIQUIDITY:
          Volume: {o['volume']['today']:,}mn shares ({_pct(o['volume']['dod'])} DoD)
          Value:  VND{o['value']['today']:,}bn ({_pct(o['value']['dod'])} DoD)
        VN30 TOP GAINERS (by 1D): {_fmt_movers(data['gainers'])}
        VN30 TOP LOSERS  (by 1D): {_fmt_movers(data['losers'])}
        FOREIGN FLOWS (HOSE): net VND{f['net']:,}bn | buy VND{f['buy']:,}bn | sell VND{f['sell']:,}bn
        FOREIGN FLOW SENTENCE (verbatim ok): {f['sentence']}
        """)


def _fallback(data: dict, news: str) -> dict:
    """Deterministic draft used when no API key is available."""
    o = data["ohlc"]
    g, l = data["gainers"], data["losers"]
    f = data["flows"]
    p1 = (f"The VN-Index opened at {o['open']['today']:,}pts ({_pct(o['open']['dod'])} DoD), "
          f"reached an intraday high of {o['high']['today']:,}pts ({_pct(o['high']['dod'])} DoD) "
          f"and a low of {o['low']['today']:,}pts ({_pct(o['low']['dod'])} DoD), "
          f"before closing at {o['close']['today']:,}pts ({_pct(o['close']['dod'])} DoD). "
          + (news.strip() + " " if news else "")
          + f"Liquidity reached {o['volume']['today']:,}mn shares ({_pct(o['volume']['dod'])} DoD) "
          f"and VND{o['value']['today']:,}bn in value ({_pct(o['value']['dod'])} DoD).")
    p2 = (f"Within VN30, {_fmt_movers(g)} were the largest gain contributors to the index. "
          f"Meanwhile, {_fmt_movers(l)} capped the market's upside.")
    p3 = f["sentence"] + "." if f.get("sentence") else (
        f"Foreign investors recorded net flows of VND{f['net']:,}bn on HOSE.")
    return {"headline": "Market commentary (auto-draft)", "body": "\n\n".join([p1, p2, p3])}


def generate(data: dict, news: str = "") -> dict:
    """Return {'headline','body'} for the day's commentary."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return _fallback(data, news)

    import anthropic  # imported lazily so the fallback path needs no dependency
    client = anthropic.Anthropic(api_key=api_key)
    facts = build_facts(data)
    user = (f"FACTS:\n{facts}\n\nNEWS DRIVER (for P1; may be empty):\n{news or '(none provided)'}\n\n"
            f"STYLE EXAMPLE (voice only, do not reuse its numbers):\n{STYLE_EXAMPLE}\n\n"
            "Write today's commentary as strict JSON.")
    msg = client.messages.create(
        model=MODEL, max_tokens=1200, system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user}],
    )
    text = msg.content[0].text.strip()
    if text.startswith("```"):
        text = text.split("```")[1].lstrip("json").strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"headline": "Market commentary", "body": text}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Generate the daily worded commentary")
    ap.add_argument("data_json", help="report_data.json from extract.py")
    ap.add_argument("--news", default="", help="one-line news driver for paragraph 1")
    ap.add_argument("-o", "--out", help="write JSON result here (default: stdout)")
    args = ap.parse_args(argv)

    data = json.load(open(args.data_json, encoding="utf-8"))
    result = generate(data, args.news)
    rendered = f"{result['headline']}\n\n{result['body']}"
    if args.out:
        json.dump(result, open(args.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(rendered)
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
