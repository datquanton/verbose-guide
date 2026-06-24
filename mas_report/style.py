"""
Style corpus loader.

Drop ~10 past 'Good Morning Vietnam' reports (.docx) into a folder (default:
mas_report/style_corpus/). This module pulls the commentary (headline + body)
out of each and returns few-shot examples that commentary.py feeds to Claude so
the generated prose matches the desk's voice.

Only the commentary cell is extracted -- never the numbers -- so old figures
can't leak into a new day's report.
"""
from __future__ import annotations

import glob
import os

from docx import Document

DEFAULT_DIR = os.path.join(os.path.dirname(__file__), "style_corpus")


def _commentary_from_doc(path: str) -> dict | None:
    """Extract {'headline','body'} from one report's market-commentary cell."""
    doc = Document(path)
    for tbl in doc.tables:
        for ri, row in enumerate(tbl.rows):
            if row.cells[0].text.strip().upper().startswith("VIETNAM STOCK MARKET"):
                if ri + 1 >= len(tbl.rows):
                    return None
                paras = [p.text.strip() for p in tbl.rows[ri + 1].cells[0].paragraphs
                         if p.text.strip()]
                if len(paras) >= 2:
                    return {"headline": paras[0], "body": "\n\n".join(paras[1:])}
    return None


def load_examples(corpus_dir: str = DEFAULT_DIR, limit: int = 10) -> list[dict]:
    """Return up to `limit` {'headline','body'} examples, newest file first."""
    if not os.path.isdir(corpus_dir):
        return []
    paths = sorted(glob.glob(os.path.join(corpus_dir, "*.docx")),
                   key=os.path.getmtime, reverse=True)
    out = []
    for p in paths[:limit]:
        try:
            ex = _commentary_from_doc(p)
        except Exception:
            ex = None
        if ex:
            out.append(ex)
    return out


def as_fewshot(examples: list[dict]) -> str:
    """Render examples as a voice reference block for the system prompt."""
    if not examples:
        return ""
    blocks = []
    for i, ex in enumerate(examples, 1):
        blocks.append(f"--- EXAMPLE {i} ---\nHeadline: {ex['headline']}\n{ex['body']}")
    return ("HOUSE-VOICE EXAMPLES (match tone, structure, phrasing; never reuse "
            "their numbers):\n\n" + "\n\n".join(blocks))


if __name__ == "__main__":
    ex = load_examples()
    print(f"Loaded {len(ex)} style example(s) from {DEFAULT_DIR}")
    for e in ex:
        print(" -", e["headline"])
