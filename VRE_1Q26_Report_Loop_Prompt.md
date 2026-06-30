# VRE 1Q26 — Condensed Report Loop Prompt

A reusable prompt for `/loop` that **continuously regenerates a tight, 1Q26-focused VRE note** —
denser and shorter than the 23-page TCBS/TCX initiation. Each iteration refreshes inputs, rotates a
"spotlight," self-critiques the prior draft, and writes a new versioned file so you build a series, not
one stale document.

---

## How to run

```
/loop 30m  <paste the PROMPT block below>
```

- Default cadence `30m` is sensible for an idle refresh; use `/loop 10m` while actively iterating, or a
  longer interval (e.g. `2h`) for a slow drip. The loop keeps running until you stop it.
- It writes `reports/VRE_1Q26_note_v<N>.md` each cycle (N increments), so prior versions are preserved.
- **Price caveat:** the spot price/upside is the one input that goes stale fastest and that I cannot
  fetch live in every environment. Each iteration the prompt asks you (or a connected data tool) to
  confirm the live VRE price; if none is supplied it carries the last known print and flags it.

---

## THE PROMPT (copy everything between the lines)

---
You are a senior Mirae Asset (Vietnam) equity analyst covering Vincom Retail (VRE VN, HOSE). Each time this
runs, produce ONE fresh, CONDENSED institutional note on VRE with the emphasis on 1Q2026 results — tighter
and shorter than a typical AI-generated initiation (target ~1.5–2 pages; density over length; no filler).

INPUTS (read before writing):
1. `/home/user/verbose-guide/VRE_Investment_Report.md` (the full reference note)
2. `/home/user/verbose-guide/VRE_Competitive_Research_Strategy.md` (the edge framework + self-audit)
3. The most recent `reports/VRE_1Q26_note_v*.md` if any (your prior iteration)
4. If a market-data tool (e.g. FiinQuant) is connected, pull the LATEST VRE price, P/B and consensus;
   otherwise carry forward the last known spot (note the date) and flag it as needing refresh.

EACH ITERATION, DO ALL OF:
- Re-anchor on 1Q2026 actuals: revenue VND2,294bn (+7.6% YoY); leasing rev +9.0% (+11.8% like-for-like);
  NPATMI VND1,606bn (+36.4%; +38.4% like-for-like); occupancy 88.9% (+2.8ppt); footfall +13.2%;
  EBITDA margin 62.6%; leasing NOI margin 70.4%; net debt/equity 4.9%; ~25%/30% of FY revenue/profit guidance.
- Hold the house call unless inputs change it: BUY, TP VND34,972 (FCFF DCF, WACC 11%, g 1%). Recompute the
  expected return from the latest spot and adjust the rating label if the implied return crosses a band
  (Buy ≥+20%, Trading Buy +10–20%, Hold −10/+10%, Sell ≤−10%).
- Keep the differentiator front and centre: the 3-stream earnings bridge (core leasing ~VND3,893bn vs
  recurring financial income on ~VND29.5tn of deposits/intercompany lending vs the ~VND1,900bn one-off),
  and value the leasing annuity, not the headline PAT.
- IMPROVE on the prior version: read your last note, list its 2–3 weakest spots, and fix them this cycle.
- ROTATE the spotlight so successive notes aren't identical — pick the next theme in this cycle:
  (a) earnings quality / related-party deposits, (b) footfall quality vs Aeon (like-for-like),
  (c) Mega-Mall + shophouse pipeline & dated catalysts, (d) valuation cross-checks (DCF vs P/B band vs peers),
  (e) balance sheet / cash conversion / REIT optionality. Note which spotlight this version uses.

STRUCTURE (condensed; ~1.5–2 pages):
1. Header line: Rating · TP · spot · expected return · P/E & P/B (spot) · "our EPS/PBT vs consensus".
2. Call (3–4 sentences): the thesis and what 1Q26 changed.
3. 1Q26 read-through: a 5–6 row metrics table (YoY + like-for-like) and two sentences on quality of the beat.
4. This iteration's SPOTLIGHT (the rotating deep-dive, ~1 paragraph).
5. Forecasts: a compact 4-column table (2024A/2025A/2026F/2027F: revenue, EBITDA, NPATMI, EPS, P/B).
6. Valuation (3–4 sentences): DCF anchor + one cross-check.
7. Risks & "what would change our view": 3 ranked, falsifiable bullets.
Footnote: 2025 reported PAT includes a ~VND1,900bn one-off; normalised NPATMI ~VND4.5–5.0tn. State the
spot-price date and that the model has known hygiene fixes pending (sensitivity grid, share count 2,272 vs
2,328.8m, version drift on 2026F revenue) — never publish false precision.

OUTPUT: write the note to `reports/VRE_1Q26_note_v<N>.md` (increment N from the highest existing version;
start at v1). End with a 3-line changelog: what you changed vs the prior version, which spotlight you used,
and any input that needs a human/data refresh.
---

---

## What makes this a *loop* and not a one-shot

- **Versioned, not overwritten** — you accumulate a dated series you can diff (useful around the next print).
- **Self-improving** — every cycle critiques and fixes the previous note, so quality ratchets up.
- **Non-repeating** — the rotating spotlight means five consecutive runs read as five angles on the same call,
  not five copies.
- **Drift-aware** — it re-pulls price/consensus each cycle and flags what it couldn't verify, so the note
  never silently goes stale.

## Optional: stricter / lighter variants
- **Tighter (1 page):** add to the prompt — *"Hard cap 600 words; drop the forecast table to revenue + NPATMI + TP only."*
- **Event-driven instead of timed:** rather than `/loop`, ask me to *subscribe to VRE filings/price triggers* and
  regenerate only when 2Q26 prints or the price moves >5% — less noise than a fixed interval.
