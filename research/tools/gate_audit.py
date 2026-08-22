#!/usr/bin/env python3
"""Audit the gate table at the top of monitoring-log.md.

Three defects this catches. The first two were found the hard way on 20-Aug-2026;
the third (3) was found on 22-Aug-2026 by reading the table by hand and noticing
that a whole ROW SHAPE had never been audited at all -- see ISO_DATE_RE below.
A checker that reports "none passed" against rows it cannot parse is worse than
no checker, because the clean line reads as coverage.


  1. A FENCED ROW WHOSE RE-OPEN DATE HAS PASSED. Rows 36 and 37 both said
     "the next week's report, i.e. Sat 15-Aug or later" and were still
     carrying week 03-07 Aug on 20-Aug -- five days overdue -- even though
     the week 10-14 wrap was already written up in an ordinary entry.

  2. A ROW WHOSE PIPE COUNT IS WRONG, which silently breaks the table.
     Two legacy 3-pipe rows are known and expected.

  3. A DATE-COLUMN ROW WHOSE ISO FENCE HAS PASSED. Rows shaped
     "| topic | 2026-08-15 | lanes |" were invisible to (1) twice over: the
     date is ISO, which DATE_RE cannot match, and it sits in the MIDDLE cell
     while (1) reads cells[-2]. Rows 87 and 88 sat six days past their fence
     while this tool printed "re-open dates: none passed" on every run.

The general defect behind (1): the file does the work in entries and does
not write it back to the table. A gate row caches conclusions AND their
errors, with more authority than an ordinary entry, because sweeps are told
to trust it rather than re-derive. So a stale gate row is worse than a
stale entry, and it is exactly where a wrong claim sits undisturbed.

Usage:  python3 research/tools/gate_audit.py [YYYY-MM-DD]
        (date defaults to today; pass one to audit as of another day)
"""

import datetime
import io
import re
import sys

LOG = "monitoring-log.md"
GATE_SCAN_LINES = 140  # the gate table lives at the top of the file
EXPECTED_PIPES = 4

# --- anchors, not line numbers ---------------------------------------------
#
# This tool used to hard-code row numbers: LEGACY_THREE_PIPE_ROWS = {62, 86}
# and a WATCH list keyed to rows 25, 33 and 53. Found 22-Aug-2026, by declining
# to insert a new gate row: INSERTING OR DELETING ANY ROW SILENTLY REPOINTS ALL
# OF THEM. The pipe check would flag two innocent rows as malformed and stop
# flagging the two real legacy ones; value-drift would read the wrong rows and
# report "no drift" on quantities it was no longer watching. A checker failing
# SILENTLY and reading as coverage -- the defect this tool exists to catch.
#
# So rows are now identified by a distinctive substring of their own text, and
# resolution FAILS LOUDLY: an anchor matching zero rows, or more than one, is
# reported as a broken anchor rather than quietly skipped. The resolved line
# numbers are printed so a reader can see what each check actually bound to.
LEGACY_THREE_PIPE_ANCHORS = (
    "Commerce finals done 28-Jul",      # US rebar row
    "RESOLVED 03-Aug 11:53: 52.9",      # July PMI row
)


def resolve_anchor(lines, anchor):
    """Line numbers of gate rows containing anchor. Caller checks for != 1."""
    return [
        idx
        for idx, line in enumerate(lines[:GATE_SCAN_LINES], start=1)
        if line.startswith("|") and anchor in line
    ]

MONTHS = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}
DATE_RE = re.compile(r"(\d{1,2})-([A-Za-z]{3})(?:-(\d{4}))?")

# The table uses TWO date conventions and this tool only ever read one of them.
# Prose cells write "24-Aug" / "15-Aug-2026"; the DATE-COLUMN rows -- shaped
# "| topic | 2026-08-15 | lanes |" -- write ISO. Found by hand on 22-Aug-2026:
# rows 87 and 88 carried an ISO fence of 2026-08-15 that had passed SEVEN DAYS
# earlier and this tool reported "re-open dates: none passed" every run, for two
# independent reasons: DATE_RE cannot match ISO, and the fence in those rows sits
# in the MIDDLE cell while the check reads cells[-2] (which holds the lane
# numbers). Row 64 had the same shape and was also fixed by hand, not by this.
#
# The table holds only ~10 ISO dates and every one of them is a fence, so taking
# the maximum ISO date anywhere in the row is precise here. It is a convention,
# not a guarantee -- if a prose cell ever writes an ISO date as history, this
# will read it as a fence.
ISO_DATE_RE = re.compile(r"(20\d{2})-([01]\d)-([0-3]\d)")

# A row that announces its own closure is not overdue. This is a heuristic with a
# KNOWN failure mode, stated so a clean run is not over-read: a row that says
# RESOLVED about a SUB-question while its main fence is still live gets skipped.
CLOSED_MARKERS = ("CLOSED", "RESOLVED", "SUPERSEDED")


def parse_iso_dates(text):
    out = []
    for year, month, day in ISO_DATE_RE.findall(text):
        try:
            out.append(datetime.date(int(year), int(month), int(day)))
        except ValueError:
            continue
    return out


def parse_dates(text, default_year):
    """Every DD-Mon[-YYYY] in text, as dates. Unparseable ones are skipped."""
    out = []
    for day, mon, year in DATE_RE.findall(text):
        month = MONTHS.get(mon.lower())
        if month is None:
            continue
        try:
            out.append(datetime.date(int(year) if year else default_year, month, int(day)))
        except ValueError:
            continue
    return out


def audit(as_of):
    lines = io.open(LOG, encoding="utf-8").read().split("\n")
    overdue, broken, iso_overdue = [], [], []

    legacy = set()
    for anchor in LEGACY_THREE_PIPE_ANCHORS:
        found = resolve_anchor(lines, anchor)
        if len(found) == 1:
            legacy.add(found[0])
        else:
            broken.append((0, f"ANCHOR {anchor!r} matched {len(found)} rows, expected 1"))

    for idx, line in enumerate(lines[:GATE_SCAN_LINES], start=1):
        if not line.startswith("|"):
            continue

        pipes = line.count("|")
        if pipes != EXPECTED_PIPES and idx not in legacy:
            broken.append((idx, pipes))

        cells = line.split("|")
        if len(cells) < 4:
            continue

        # last cell is empty (trailing pipe); the re-open condition is the one before it.
        # Take the LATEST date in the cell, not any past one: a condition reads
        # "not before X" / "X or later", so the fence is the maximum. Cells often
        # also carry history ("advanced from Sat 15-Aug"), and treating those as
        # the fence flags rows that were just brought current -- which this tool
        # did on its first run, against the two rows it had itself just fixed.
        dates = parse_dates(ANNOTATION_RE.sub("", strip_struck(cells[-2])), as_of.year)
        if dates and max(dates) < as_of:
            topic = re.sub(r"[*~`]", "", cells[1]).strip()[:70]
            overdue.append((idx, max(dates), topic))
            continue

        # ISO fence, read from the whole row -- see ISO_DATE_RE above.
        row = ANNOTATION_RE.sub("", strip_struck(line))
        if any(marker in row for marker in CLOSED_MARKERS):
            continue
        iso = parse_iso_dates(row)
        if iso and max(iso) < as_of:
            topic = re.sub(r"[*~`]", "", cells[1]).strip()[:70]
            iso_overdue.append((idx, max(iso), topic))

    return overdue, broken, iso_overdue


def main():
    as_of = (
        datetime.date.fromisoformat(sys.argv[1])
        if len(sys.argv) > 1
        else datetime.date.today()
    )
    overdue, broken, iso_overdue = audit(as_of)

    print(f"gate audit as of {as_of.isoformat()}")

    if broken:
        print(f"\nBROKEN PIPE COUNT ({len(broken)}) -- the table is silently malformed:")
        for idx, pipes in broken:
            if idx == 0:
                print(f"  BROKEN ANCHOR: {pipes}")
            else:
                print(f"  line {idx}: {pipes} pipes, expected {EXPECTED_PIPES}")
    else:
        print("\npipe counts: clean (excluding the two known legacy rows)")

    if overdue:
        print(f"\nRE-OPEN DATE HAS PASSED ({len(overdue)}) -- these rows are due:")
        for idx, latest, topic in overdue:
            days = (as_of - latest).days
            print(f"  line {idx}: {latest.isoformat()} ({days}d overdue) -- {topic}")
    else:
        print("\nre-open dates: none passed")

    # A date in the re-open column is a heuristic, not a proof: rows whose
    # condition is an EVENT ("a policy-rate move", "an issuer filing naming a
    # date") carry no date and cannot be audited this way. Absence of a hit is
    # not evidence the row is current.
    if iso_overdue:
        print(f"\nISO-DATED FENCE HAS PASSED ({len(iso_overdue)}) -- date-column rows, invisible to the check above:")
        for idx, latest, topic in iso_overdue:
            days = (as_of - latest).days
            print(f"  line {idx}: {latest.isoformat()} ({days}d overdue) -- {topic}")
    else:
        print("\nISO-dated fences: none passed")

    print("\nnote: event-conditioned rows carry no date and are not audited above.")
    print("note: rows whose text says CLOSED/RESOLVED/SUPERSEDED are skipped by the ISO check,")
    print("      so a row that resolves a SUB-question with a live main fence will be missed.")

    passed = deadlines(as_of)
    if passed:
        print(f"\nPASSED OBLIGATIONS ({len(passed)}) -- curated register, human-only:")
        for when, what, why in passed:
            print(f"  {when.isoformat()} ({(as_of - when).days}d overdue) -- {what}")
            print(f"      {why}")
    else:
        print("\npassed obligations: none")

    stale = value_drift()
    if stale:
        print(f"\nVALUE DRIFT ({len(stale)}) -- the row and the log disagree:")
        for label, line_no, in_row, in_log in stale:
            print(f"  line {line_no}: {label}")
            print(f"      row carries: {in_row}")
            print(f"      log's newest: {in_log}")
    else:
        print("\nvalue drift: none on the watched quantities")
    print(f"note: value drift covers only the {len(WATCH)} curated quantities below, not the whole table.")


# --- value drift -------------------------------------------------------------
#
# The date audit above misses the more common failure: a row whose condition is
# an EVENT, satisfied by an ordinary entry that was never written back. Row 33
# asked for "an assessment dated August or later"; the file got one on 03-Aug
# and the row still carried the 24-Jul figure seventeen days later.
#
# There is no robust general parser for this, so this is a CURATED watchlist:
# (label, gate line, regex). The regex is applied to the gate row and to the
# whole log; the log's first match is its newest, since entries are newest-first.
# A quantity not listed here is not checked. Keep this list SHORT and each
# pattern tightly bound to ONE quantity: an earlier entry here matched any
# share count rather than MBB's specifically, and reported KDH's 1,122.1m as
# MBB drift. A check that silently watches the wrong quantity is worse than
# no check, because it reads as coverage.

# (label, ROW ANCHOR, regex) -- the anchor is a distinctive substring of the
# row's own text. It replaced hard-coded line numbers 33, 53 and 25 on
# 22-Aug-2026; see the note at the top of this file for why.
WATCH = [
    ("China HRC export, SS400 3mm FOB Tianjin",
     "CHINA HRC EXPORT PRICE (Mysteel weekly)", r"US\$(\d{3})/t FOB"),
    ("HPG domestic rebar, CB240 / D10 CB300",
     "HPG DOMESTIC CONSTRUCTION-STEEL PRICE (CB240 / D10 CB300)", r"₫\*?\*?(1[45],\d{3})/kg"),
    ("HPG HRC volume offer, CFR HCMC",
     "HPG's August HRC cut", r"\*\*(\d{3}) CFR HCMC\*\*"),
]


# A deadline stated in a row's BODY is invisible to the re-open check above,
# which reads only the last cell. I first tried a general parser for "due by
# <date>" and it FAILED on the case that motivated it: row 59 says the item-38
# re-derivation is "due by THIS DATE" -- referential, with the date elsewhere in
# the row -- so it parsed nothing, while matching my own annotation prose and
# producing one false positive instead.
#
# Curated beats general in this file; that is now three for three. So this is a
# hand-maintained register of dated obligations, each with the reason it cannot
# be discharged by an automated run.
DEADLINES = [
    (
        datetime.date(2026, 8, 22),
        "HPG coking-coal leg: the pinned US$228 REQUIRES HUMAN RE-DERIVATION",
        "Section 4 human-only -- every ore and coal field is. "
        "`_coking_coal_price_basis` pins 'US$228 FOB Australia index (pinned 2026-08-06)'. "
        "Four independent statements found 22-Aug put the SAME basis on a monotone path "
        "244.1 (30-Jun) -> 238.8 (10-Jul) -> 217 (31-Jul) -> 214.9 (07-Aug), and 228 sits "
        "nowhere on it -- it is one day BEFORE the 214.9 and 6.1% higher. At the file's own "
        "gearing of 0.14m VND per US$10/t, moving 228 -> ~215 is +0.182m/t, i.e. +21.1% on the "
        "standing 0.8632m/t spread, which is ~17% of HPG FY NPAT. FAVOURABLE direction, which "
        "is why it needs a human: this file withdrew a coal conclusion on 06-Aug for getting "
        "the direction wrong. "
        "REVISED 22-Aug 14:53 AFTER A SECOND-PROVIDER CHECK: the '~215 now' half is WITHDRAWN. "
        "Kallanish weeklies (07-Jul 237.08, 14-Jul 232.91) show the derived 10-Jul 238.8 sits above "
        "the weekly containing its own date, and the 214.9 is now TWO WEEKS STALE while two weaker "
        "indicators point up (this file's own 225 at 14-Aug; a 248.50 on 20-Aug that is almost "
        "certainly a different series and could not be verified). WHAT STANDS: 228 is UNLOCATED -- no "
        "dated 06-Aug print supports it -- and the file holds three August numbers spanning 6.1%. The "
        "+16-21% spread effect is a SENSITIVITY, not a current estimate.",
    ),
    (
        datetime.date(2026, 8, 10),
        "MBB item 38: fy26e_npat REQUIRES HUMAN RE-DERIVATION",
        "Section 4 human-only. Stored {bear 28,000, base 30,500, bull 33,000}. "
        "Two broker FY26 PBT estimates found 21-Aug imply NPAT of 31,527bn "
        "(VPBankS) and 34,595bn (VCBS) at a 20% rate -- the base sits BELOW both "
        "and the bull sits BELOW the higher one. Largest E[r] in the book.",
    ),
]


def deadlines(as_of):
    return [(when, what, why) for when, what, why in DEADLINES if when < as_of]


STRUCK_RE = re.compile(r"~~.*?~~", re.S)
# Italic parentheticals are editorial annotations -- "(advanced 20-Aug 21:54: ...)".
# Their dates are provenance, not the fence, and leaving them in makes max() pick
# the annotation date instead of the condition.
ANNOTATION_RE = re.compile(r"\*\(.*?\)\*", re.S)


def strip_struck(text):
    """Drop ~~struck~~ spans -- this file corrects by striking, not deleting."""
    return STRUCK_RE.sub("", text)


def value_drift():
    lines = io.open(LOG, encoding="utf-8").read().split("\n")
    # The gate table sits ABOVE the entries, so scanning the whole file would
    # match the gate row itself first and report "no drift" on a stale row --
    # which is exactly what this did on its first run, against row 33, whose
    # staleness was already known. Entries are newest-first BELOW the table.
    entries = "\n".join(lines[GATE_SCAN_LINES:])
    out = []
    for label, anchor, pattern in WATCH:
        found = resolve_anchor(lines, anchor)
        if len(found) != 1:
            # Loud, not silent: an anchor that stops resolving means the row was
            # renamed or removed, and the quantity is no longer being watched.
            out.append((label, 0, f"ANCHOR {anchor!r} matched {len(found)} rows", "-"))
            continue
        line_no = found[0]
        # This file corrects by striking through rather than deleting, so a
        # ~~struck~~ value is history, not the row's current claim. Leaving it in
        # made this report flag row 33 as stale immediately after it was fixed.
        in_row = re.search(pattern, strip_struck(lines[line_no - 1]))
        in_log = re.search(pattern, entries)
        if not in_row:
            # Silence from a checker must not read as "clean": the pattern not
            # matching the row at all is a different state from the values
            # agreeing, and it hid a stale row 33 for one run.
            out.append((label, line_no, "PATTERN DID NOT MATCH THE ROW", in_log.group(1) if in_log else "-"))
        elif in_log and in_row.group(1) != in_log.group(1):
            out.append((label, line_no, in_row.group(1), in_log.group(1)))
    return out


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        # piping to head is normal use; do not traceback on it
        pass
