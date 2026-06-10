"""Static configuration: index symbol, VN30 universe, data source, formatting."""

from __future__ import annotations

import os

# --- Data source -----------------------------------------------------------
# vnstock data source for board/quote calls. VCI and TCBS are the common ones.
VNSTOCK_SOURCE = os.environ.get("VNSTOCK_SOURCE", "VCI")

# VN-Index symbol as used by vnstock Quote.history.
INDEX_SYMBOL = os.environ.get("INDEX_SYMBOL", "VNINDEX")

# How many top movers to list on each side (the report uses 5).
TOP_N_MOVERS = 5

# --- VN30 constituents -----------------------------------------------------
# Fallback list used only if the live Listing.symbols_by_group('VN30') call
# is unavailable. Keep in sync after each quarterly VN30 review.
VN30_FALLBACK = [
    "ACB", "BID", "BSR", "CTG", "FPT", "GAS", "GVR", "HDB", "HPG", "LPB",
    "MBB", "MSN", "MWG", "PLX", "SAB", "SHB", "SSB", "SSI", "STB", "TCB",
    "TPB", "VCB", "VHM", "VIB", "VIC", "VJC", "VNM", "VPB", "VPL", "VRE",
]

# --- Narrative backend -----------------------------------------------------
# "template"  -> deterministic, offline, no API key needed.
# "anthropic" -> Claude drafts the prose in MAS house style (needs API key).
NARRATIVE_BACKEND = os.environ.get("NARRATIVE_BACKEND", "template")
ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-opus-4-8")

# --- News RSS feeds (financial market recap) -------------------------------
NEWS_FEEDS = [
    "https://cafef.vn/thi-truong-chung-khoan.rss",
    "https://vneconomy.vn/chung-khoan.rss",
]

# --- Formatting ------------------------------------------------------------
# The report uses an en-dash (–) for negative changes, not a hyphen.
NEG_SIGN = "–"  # –
