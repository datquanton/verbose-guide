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
        dates = parse_dates(cells[-2], as_of.year)
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
    print("\nnote: event-conditioned rows carry no date and are not audited here.")


if __name__ == "__main__":
    main()
