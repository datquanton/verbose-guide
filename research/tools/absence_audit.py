#!/usr/bin/env python3
"""Report live prose-versus-field contradictions in research/models/assumptions.json.

WHY THIS EXISTS. On 2026-08-06 an audit extracted every claim of absence in
assumptions.json -- "still unknown", "is not established", "not on file",
"never recorded" -- and asked whether the file holds the thing it says it
lacks. It found 129 such claims, most of them legitimate (they are the file's
refusals to infer, which is its best habit), and several that were false: the
resolving number was already sitting in the file, sometimes eight fields away.

It named three failure modes, in descending order of danger:

  1. A claim in block A about data in block B. Nobody reading A checks B.
  2. A prose claim contradicted by a plain numeric field in the SAME block.
     The append-only convention assumes prose is superseded by prose; it has
     no mechanism at all for a FIELD superseding prose.
  3. A derived ratio outliving its inputs.

It proposed a cheap rule -- an absence claim about another ticker should name
the field that would resolve it -- and then recorded that conventions are
human-only under charter section 4, so nothing was changed.

On 2026-08-21, fifteen days later, all three of its named contradictions were
still live. Nothing retired them, exactly as it predicted.

So this file implements the audit's proposal as DATA rather than as a
convention: each entry pairs an absence claim with the field path that
resolves it. It changes no convention and edits no prose. It only reports.

The append-only convention is not the bug. A file that never overwrites is
why the 06-Aug audit was possible at all. The cost of never overwriting is
that stale claims accumulate, and the answer to that cost is a detector, not
a deletion.

LIMITS, STATED SO A CLEAN RUN IS NOT MISREAD: this list is CURATED. An
absence claim not listed here is not checked, and "no live contradictions"
means only that the listed ones are resolved. Claims that appear inside a
_meta audit note or inside their own withdrawal note are expected hits and
are excluded per-entry by `ignore_paths` -- quoting a claim in order to
correct it is the convention working, not a contradiction.

Usage:  python3 research/tools/absence_audit.py
"""

import io
import json
import sys

ASSUMPTIONS = "research/models/assumptions.json"


# (label, claim substring, resolver path, ignore_paths, note)
#
# A row fires when the claim is still present somewhere OUTSIDE ignore_paths
# AND the resolver path holds a value. Seeded with the three the 06-Aug audit
# named and the 21-Aug re-test confirmed were still live.
CLAIMS = [
    (
        "VPB provisioning",
        "provisioning line is NOT ESTABLISHED",
        "vpb.actuals.h1_provisions_bn",
        ("_meta.",),
        "Resolved 02-Aug 21:53. vpb.actuals holds h1_provisions_bn and ten related "
        "fields. The TCB block still calls VPB 'the one name where this analysis "
        "could not be run'; the same sentence sits eight fields from the answer in "
        "VPB's own block.",
    ),
    (
        "VPB / CAEX same venture",
        "WHETHER THIS IS THE SAME VENTURE IS NOT ESTABLISHED",
        "vpx.actuals",
        ("_meta.",),
        "Resolved cross-block 05-Aug 20:53 in the VPX block: CAEX is 11/39/50 and "
        "sums to 100, leaving no room for a separate VPB stake, and 11% of 10,000bn "
        "is the 1,100bn in question. Nobody reading vpb will find it.",
    ),
    (
        "TCX P/B 2.075x",
        "2.075",
        "valuation.TCX.evidence",
        ("_meta.", "_WITHDRAWN_"),
        "A derived ratio outliving its inputs: 2.075x used the stale listing-date "
        "share count (2,311,308,021), superseded by the 04-Aug verification of "
        "2,773,896,000. The live figure is 2.49x. Two claims about one ratio, 20% "
        "apart, on the name the file calls priciest in the book.",
    ),
]


def load():
    return json.load(io.open(ASSUMPTIONS, encoding="utf-8"))


def find_claim(doc, needle, ignore_paths):
    """Paths whose string value contains needle, excluding ignored path fragments."""
    found = []

    def walk(node, path):
        if isinstance(node, dict):
            for key, value in node.items():
                walk(value, path + [key])
        elif isinstance(node, list):
            for index, value in enumerate(node):
                walk(value, path + [str(index)])
        elif isinstance(node, str) and needle.lower() in node.lower():
            joined = ".".join(path)
            if not any(frag in joined for frag in ignore_paths):
                found.append(joined)

    walk(doc, [])
    return found


def resolve(doc, path):
    node = doc
    for key in path.split("."):
        if isinstance(node, dict) and key in node:
            node = node[key]
        else:
            return None
    return node


# --- deferrals ---------------------------------------------------------------
#
# A third shape of the same disease, found 21-Aug: the log marks a gap and
# explicitly defers it. "A SMALL GAP FOUND AND LOGGED, NOT CHASED" sat in an
# ordinary entry while the thing it deferred -- what Circular 08/2026/TT-BTC
# actually DOES -- stayed missing for days, on the lane the FTSE upgrade runs
# through. Neither gate_audit nor the curated claims above can see these,
# because they live in prose in monitoring-log.md rather than in the table or
# in assumptions.json.
#
# This does not judge whether a deferral was right. It only makes the queue
# visible, so a sweep with nothing better to do can pick one up.

LOG = "monitoring-log.md"
DEFERRAL_MARKERS = (
    "NOT CHASED",
    "not chased",
    "logged, not",
    "found and logged",
    "deferred",
)


def deferrals(limit=12):
    out = []
    for number, line in enumerate(io.open(LOG, encoding="utf-8"), start=1):
        for marker in DEFERRAL_MARKERS:
            if marker in line:
                out.append((number, marker, line.strip()[:150]))
                break
        if len(out) >= limit:
            break
    return out


def main():
    doc = load()
    live = []

    for label, needle, resolver_path, ignore_paths, note in CLAIMS:
        locations = find_claim(doc, needle, ignore_paths)
        resolved = resolve(doc, resolver_path)
        if locations and resolved is not None:
            live.append((label, locations, resolver_path, resolved, note))

    print(f"absence audit — {len(CLAIMS)} curated claims checked")

    if not live:
        print("\nno live contradictions among the curated claims")
    else:
        print(f"\nLIVE CONTRADICTIONS ({len(live)}) — the file holds what the claim says it lacks:")
        for label, locations, resolver_path, resolved, note in live:
            shown = str(resolved)
            if len(shown) > 90:
                shown = shown[:90] + "…"
            print(f"\n  {label}")
            print(f"    claim still live at: {', '.join(locations)}")
            print(f"    resolved by {resolver_path} = {shown}")
            print(f"    {note}")

    print(
        "\nnote: this list is CURATED. An absence claim not listed is not checked, so a\n"
        "clean run means only that the listed claims are resolved. Nothing here edits\n"
        "prose — the append-only convention is why the original audit was possible."
    )

    queue = deferrals()
    if queue:
        print(f"\nEXPLICIT DEFERRALS IN THE LOG ({len(queue)} newest, a work queue not a verdict):")
        for number, marker, text in queue:
            print(f"  monitoring-log.md:{number}  [{marker}]  {text}")
        print("  (newest first; a deferral may have been right, and this does not judge that.)")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        pass
