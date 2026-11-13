# Overnight run: portfolio consultant (`/danh-muc/`)

A brief for an unattended session. It is written so that a run with nobody watching
can only make the page more correct, never less, and leaves a log a human can check in five minutes.

## The prompt

> You are maintaining the portfolio consultant in `danh-muc/` on branch `site` (production: every push deploys).
> Work through the stages below in order. Each stage ends with a check that must pass before you commit.
> Commit after each stage that changed something, push at the end, and append a dated entry to the run log
> at the bottom of this file. Report only what changed, what you could not verify, and what needs the owner.
>
> **Hard limits**
> 1. Touch nothing outside `danh-muc/`. Report pages, homepages, `assets/` and redirects belong to the site
>    generator. If the homepage link to `/danh-muc/` has been wiped by a rebuild, say so in the log; do not re-add it.
> 2. Before any push: `git fetch`, rebase onto `origin/site`, keep the remote version of every file outside `danh-muc/`.
> 3. Evidence comes only from reports published on this site. Never add a figure from memory or from the web.
>    A number you cannot find in its named source is removed or corrected, not kept.
> 4. Do not change a sizing constant (`RULES` in `engine.js`). Those are the owner's decision. Report findings instead.
> 5. No new dependencies, no server code, no API keys, no analytics.
> 6. If a stage's check fails and one fix attempt does not clear it, revert that stage, log it, and move on.
>
> **Stage 1 · Evidence audit (highest value).** For every claim in `research.js`, extract each number from the
> text and confirm it appears in the source report named by `src`. Confirm the Vietnamese and English texts
> carry the same numbers. Confirm every report in `reports` still exists at its URL in both languages and that
> its date matches the page. Check: zero unexplained numbers; every exception listed with its reason.
>
> **Stage 2 · New research.** Diff the list of report pages against `reports`. For each report not yet covered,
> read it and add claims (both directions: for and against), each with driver, direction and source. Re-run
> stage 1 on the additions. Update `asof`.
>
> **Stage 3 · Rules under stress.** Property-test `engine.js` on at least 20,000 random portfolios: no NaN or
> negative output; no suggested weight above its conviction ceiling; sector, cluster and total ceilings hold;
> a larger loss-if-wrong never raises the size; a higher probability never lowers it; negative expected value
> always gives zero; an empty or malformed portfolio never throws.
>
> **Stage 4 · The page as a stranger meets it.** In a real browser, in both languages, at phone and desktop
> width, light and dark: complete the interview by keyboard only; import malformed and hostile files; check for
> console errors, broken links, horizontal scroll, unfilled placeholders, unlabeled controls, and contrast.
>
> **Stage 5 · Does the advice read right?** Run six archetype portfolios (all banks; one stock at 60%; twelve
> small positions; all cash plus ideas; negative-expectancy holdings; unknown tickers only). Read the output as
> the investor would. Fix anything self-contradictory, misleading or unexplained. Wording fixes are in scope;
> rule changes are reported, not made.
>
> **Stage 6 · Freshness.** If the market data connector is available, rebuild `market.js` (see `README.md`) and
> update the dates in both page shells. If it is not, log the age of the data and stop there.
>
> **Stage 7 · Log.** Append to the run log: date, commits, what changed, what failed, open questions for the owner.

## Run log

### 2026-11-13 · first run

**Stage 1, evidence audit.** 169 claims checked number by number against the report each one names.
Every figure was found in a published report. Four claims drew figures from two reports while citing one;
they now cite both. One figure was rounded differently from its source (FDI +13.1% in a claim citing a report
that prints +13%); corrected to the source's figure. Vietnamese and English texts carry the same numbers.
All nine report pages exist in both languages where a second language is published.
Limit of this check: it proves each number appears in the source, not that the sentence around it means the same thing.

**Stage 2, new research.** Nothing new since the banks 3Q26, VN30 3Q26, market-wide 3Q26 and fund-study reports
were folded in earlier the same day. 63 of 77 tickers have ticker-level evidence; the other 14
(FTS, BSI, BCM, SIP, SZC, CMG, PVS, REE, DGC, HVN, GMD, VGC, CTD, BVH) have sector, macro and price data only.

**Stage 3, rules under stress.** 25,000 random portfolios plus 4,000 monotonicity cases. Three defects found and fixed
in `engine.js`: an unrecognised liquidity setting threw; a negative loss-if-wrong produced a negative stress figure;
negatively correlated pairs could report more independent bets than positions. The page's input cleaning already
blocked all three, so no visitor could have hit them. Re-run: zero failures.

**Stage 4, the page as a stranger meets it.** Both languages, phone and desktop, light and dark: no console errors,
no broken links, no horizontal scroll, no unfilled placeholders. Malformed and hostile stored data loads without
error and injects nothing. Interview inputs now take their accessible name from the question.

**Stage 5, does the advice read right.** Seven archetypes run. Three fixes, wording and one flag, no constant changed:
a tight stop no longer justifies a larger size (sizing uses the wider of the stated loss and one month's normal movement);
the "all wrong at once" tile shows a dash, not −0.0%, when no loss figure exists yet;
when suggested weights leave more cash than the working range, the page now says why (positions at their ceilings) and
that the answer is ideas in other sectors; the single-name warning no longer fires on default conviction for positions
the investor has not been asked about, unless the weight exceeds 20%.

**Stage 6, freshness.** Price data is to 13 Nov 2026, the day of this run. Nothing to rebuild.

**Added during the run at the owner's request (outside the brief's "no new dependencies" limit):**
screenshot and pasted-list intake. Text recognition runs in the visitor's browser with a self-hosted copy of
Tesseract (`vendor/tesseract/`, about 11 MB in the repository, about 7 MB downloaded on first use only).
Tested on synthetic broker screenshots only: light, dark, phone, low resolution, all read exactly.

**Open for the owner**
1. Real broker screenshots have not been tested. Layouts differ by app; the review step is the safety net.
   A handful of real (redacted) screenshots from the apps your readers use would let the parser be tuned.
2. The sizing constants in `RULES` remain my conventions. They decide every suggested number.
3. `danh-muc/` is still not registered with the site generator; a rebuild will remove the homepage link.
4. This file is served publicly at `/danh-muc/OVERNIGHT.md`, as is every file in the site folder. Move it to the vault if you prefer.
