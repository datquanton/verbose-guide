#!/usr/bin/env python3
"""Ask BEFORE searching: has this file already concluded on these terms?

WHY THIS EXISTS. On 2026-08-22 a sweep went looking for an NLG-vs-KDH
comparison and found the file already had it in full. That was not the first
time. An earlier sweep had written, in the file itself:

    "Second time today I nearly re-reported a comparison the file had already
     made ... Neither topic has a gate row -- the gate table covers what has
     been SEARCHED, not what has been CONCLUDED."

The diagnosis was written and no mechanism followed. By 22-Aug the same thing
had happened at least five times in one day (system margin debt, MBB's H1 and
plan, the Fed/Jackson Hole row, VPX's H1, NLG) -- every one caught by grepping
AFTER spending the search rather than before.

So the defect is ORDERING, not knowledge. `gate_audit.py` tracks what is
FENCED; `absence_audit.py` tracks what is CONTRADICTED or DEFERRED. Nothing
tracks what is CONCLUDED. This does, badly but cheaply, and cheap is the point:
the rule "grep before you search" only gets followed if it is one command.

LIMIT, STATED SO A CLEAN RUN IS NOT MISREAD: this can only find terms you
thought to pass it. A miss here is NOT evidence the topic is uncovered -- it is
evidence that these particular strings are absent. The same curation limit the
other two tools carry.

Usage:
    python3 research/tools/coverage_check.py 415.14 "Nam Long" NLG
    python3 research/tools/coverage_check.py --context 7630 23460
"""

import io
import re
import sys

LOG = "monitoring-log.md"
GATE_SCAN_LINES = 140  # above this is the gate table, below it the entries
MAX_SHOWN = 4


def load():
    return io.open(LOG, encoding="utf-8").read().split("\n")


def hits(lines, term):
    """(line_no, text) for every line containing term, case-insensitively."""
    needle = term.lower()
    return [(n, ln) for n, ln in enumerate(lines, start=1) if needle in ln.lower()]


def classify(line_no):
    return "GATE" if line_no <= GATE_SCAN_LINES else "entry"


def report(terms, show_context):
    lines = load()
    verdicts = []

    for term in terms:
        found = hits(lines, term)
        verdicts.append((term, found))

    covered = [t for t, f in verdicts if f]
    absent = [t for t, f in verdicts if not f]

    print(f"coverage check over {LOG} ({len(lines)} lines) -- {len(terms)} term(s)\n")

    for term, found in verdicts:
        if not found:
            print(f"  ABSENT   {term!r} -- 0 hits")
            continue
        where = ", ".join(sorted({classify(n) for n, _ in found}))
        print(f"  COVERED  {term!r} -- {len(found)} hit(s) [{where}]")
        if show_context:
            for line_no, text in found[:MAX_SHOWN]:
                trimmed = re.sub(r"\s+", " ", text).strip()[:150]
                print(f"             {LOG}:{line_no}  {trimmed}")
            if len(found) > MAX_SHOWN:
                print(f"             ... and {len(found) - MAX_SHOWN} more")

    print()
    if covered and not absent:
        print("VERDICT: every term is already in the file. A search here is likely to")
        print("         re-derive what is written. Read the hits first.")
    elif absent and not covered:
        print("VERDICT: none of these terms appear. Searching is justified.")
    else:
        print("VERDICT: MIXED -- the absent terms are where a search can add something;")
        print("         the covered ones are probably already answered.")

    print()
    print("note: a term-level miss is NOT proof the topic is uncovered. This finds")
    print("      strings, not subjects, and only the strings you passed it.")
    return 0


def main():
    args = [a for a in sys.argv[1:]]
    show_context = "--context" in args
    terms = [a for a in args if not a.startswith("--")]
    if not terms:
        print(__doc__)
        return 2
    return report(terms, show_context)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        pass
