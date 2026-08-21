#!/usr/bin/env python3
"""Audit the gate table at the top of monitoring-log.md.

Two defects this catches, both found the hard way on 20-Aug-2026:

  1. A FENCED ROW WHOSE RE-OPEN DATE HAS PASSED. Rows 36 and 37 both said
     "the next week's report, i.e. Sat 15-Aug or later" and were still
     carrying week 03-07 Aug on 20-Aug -- five days overdue -- even though
     the week 10-14 wrap was already written up in an ordinary entry.

  2. A ROW WHOSE PIPE COUNT IS WRONG, which silently breaks the table.
     Two legacy 3-pipe rows are known and expected.

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
LEGACY_THREE_PIPE_ROWS = {62, 86}
EXPECTED_PIPES = 4

MONTHS = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}
DATE_RE = re.compile(r"(\d{1,2})-([A-Za-z]{3})(?:-(\d{4}))?")


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
    overdue, broken = [], []

    for idx, line in enumerate(lines[:GATE_SCAN_LINES], start=1):
        if not line.startswith("|"):
            continue

        pipes = line.count("|")
        if pipes != EXPECTED_PIPES and idx not in LEGACY_THREE_PIPE_ROWS:
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

    return overdue, broken


def main():
    as_of = (
        datetime.date.fromisoformat(sys.argv[1])
        if len(sys.argv) > 1
        else datetime.date.today()
    )
    overdue, broken = audit(as_of)

    print(f"gate audit as of {as_of.isoformat()}")

    if broken:
        print(f"\nBROKEN PIPE COUNT ({len(broken)}) -- the table is silently malformed:")
        for idx, pipes in broken:
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
    print("\nnote: event-conditioned rows carry no date and are not audited above.")

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

WATCH = [
    ("China HRC export, SS400 3mm FOB Tianjin", 33, r"US\$(\d{3})/t FOB"),
    ("HPG domestic rebar, CB240 / D10 CB300", 53, r"₫\*?\*?(1[45],\d{3})/kg"),
    ("HPG HRC volume offer, CFR HCMC", 25, r"\*\*(\d{3}) CFR HCMC\*\*"),
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
    for label, line_no, pattern in WATCH:
        if line_no > len(lines):
            continue
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
