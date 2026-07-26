#!/usr/bin/env python3
"""Build the banking-updates site.

Compiles every updates/<slug>/update.md (your writing, in markdown, with
{{placeholder}} blocks) together with data/metrics.json (the cumulative
report metrics) into updates/<slug>/index.html, and regenerates the
archive page at banking-updates/index.html.

Usage:  python3 banking-updates/scripts/build.py
No dependencies beyond the Python 3 standard library.
"""
import html
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "data" / "metrics.json").read_text(encoding="utf-8"))
CSS = (ROOT / "templates" / "style.css").read_text(encoding="utf-8")


# ---------------------------------------------------------------- helpers
def esc(s: str) -> str:
    return html.escape(str(s), quote=True)


def md_inline(s: str) -> str:
    """Escape, then convert the inline-markdown subset: links, bold, italic."""
    s = html.escape(s, quote=False)
    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
    return s


# ---------------------------------------------------------------- renderers
def render_tiles() -> str:
    tiles = "".join(
        f'<div class="tile"><div class="label">{esc(t["label"])}</div>'
        f'<div class="value">{esc(t["value"])}</div>'
        f'<div class="note">{esc(t["note"])}</div></div>'
        for t in DATA["hero_tiles"]
    )
    return f'<div class="tiles">{tiles}</div>'


def render_chart(key: str) -> str:
    c = DATA["charts"][key]
    scale = c["scale_max"]
    rows, alt = [], []
    for it in c["items"]:
        width = round(it["value"] / scale * 100, 1)
        soft = " soft" if it.get("soft") else ""
        rows.append(
            f'<div class="barrow" title="{esc(it.get("hint", it["name"]))}">'
            f'<span class="name">{esc(it["name"])}</span>'
            f'<span class="track"><span class="bar{soft}" style="width:{width}%"></span></span>'
            f'<span class="val">{esc(it["display"])}</span></div>'
        )
        alt.append(f'{it["name"]} {it["display"]}')
    return (
        '<figure class="viz">'
        f'<p class="viz-title">{esc(c["title"])}</p>'
        f'<p class="viz-sub">{esc(c["subtitle"])}</p>'
        f'<div role="img" aria-label="Bar chart: {esc(", ".join(alt))}">{"".join(rows)}</div>'
        f'<div class="axis-note">{esc(c["axis_note"])}</div>'
        f'<figcaption>{md_inline(c["caption"])}</figcaption>'
        "</figure>"
    )


def render_ticker_table() -> str:
    rows = []
    for t in DATA["tickers"]:
        rows.append(
            f'<tr><td>{esc(t["ticker"])} <span class="pick {esc(t["badge_class"])}">{esc(t["badge"])}</span></td>'
            f'<td>{esc(t["bank"])}</td><td>{esc(t["backers"])}</td>'
            f'<td class="num">{esc(t["numbers"])}</td><td>{esc(t["case"])}</td></tr>'
        )
    return (
        '<div class="tablewrap"><table><thead><tr>'
        "<th>Ticker</th><th>Bank</th><th>Who backs it</th>"
        "<th>2026 numbers to know</th><th>The case</th>"
        f'</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
    )


def render_dashboard() -> str:
    rows = []
    for h in DATA["dashboard"]:
        if "wide" in h:  # e.g. rating-agency action spanning the metric columns
            rows.append(
                f'<tr><td>{esc(h["house"])}</td><td>{md_inline(h["report"])}</td>'
                f'<td colspan="3">{h["wide"]}</td><td>{esc(h["picks"])}</td></tr>'
            )
            continue
        pc = f' class="num {h.get("profit_class", "")}"'.replace(' ""', '"num"')
        nc = h.get("nim_class", "")
        rows.append(
            f'<tr><td>{esc(h["house"])}</td><td>{md_inline(h["report"])}</td>'
            f'<td class="num {h.get("profit_class", "")}">{esc(h["profit"])}</td>'
            f'<td>{esc(h["credit"])}</td>'
            f'<td class="num {nc}">{esc(h["nim"])}</td>'
            f'<td>{esc(h["picks"])}</td></tr>'
        )
    return (
        '<div class="tablewrap"><table><thead><tr>'
        "<th>House / agency</th><th>Report</th><th>2026 profit growth</th>"
        "<th>Credit growth view</th><th>NIM view</th><th>Named picks</th>"
        f'</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
    )


def render_sources() -> str:
    items = []
    for s in DATA["sources"]:
        links = " · ".join(f'<a href="{esc(l["url"])}">{esc(l["label"])}</a>' for l in s["links"])
        items.append(f"<li>{esc(s['name'])} — {links}</li>")
    return f'<ul class="srcs">{"".join(items)}</ul>'


def render_disclaimer() -> str:
    return (
        '<div class="disclaimer"><strong>Disclosure &amp; disclaimer.</strong> '
        f'{esc(DATA["brand"]["disclaimer"])} Data as of {esc(DATA["as_of"])}.</div>'
    )


PLACEHOLDERS = {
    "tiles": render_tiles,
    "table:tickers": render_ticker_table,
    "table:dashboard": render_dashboard,
    "sources": render_sources,
    "disclaimer": render_disclaimer,
}

# Every chart in metrics.json is a placeholder automatically. Adding a chart to a
# post is then a data edit, not a code edit — which is the difference between a
# publishing system and a one-off page.
for _key in DATA.get("charts", {}):
    PLACEHOLDERS[f"chart:{_key}"] = (lambda k: lambda: render_chart(k))(_key)


# ---------------------------------------------------------------- markdown
def parse_front_matter(text: str):
    meta, body = {}, text
    if text.startswith("---"):
        _, fm, body = text.split("---", 2)
        for line in fm.strip().splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
    return meta, body.strip()


def md_to_html(body: str) -> str:
    """Convert the markdown subset used in update.md files to HTML."""
    out, para, listbuf, listtag, quote = [], [], [], None, []

    def flush_para():
        if para:
            out.append(f"<p>{md_inline(' '.join(para))}</p>")
            para.clear()

    def flush_list():
        nonlocal listtag
        if listbuf:
            items = "".join(f"<li>{md_inline(i)}</li>" for i in listbuf)
            cls = ' class="themes"' if listtag == "ol" else ""
            out.append(f"<{listtag}{cls}>{items}</{listtag}>")
            listbuf.clear()
            listtag = None

    def flush_quote():
        if quote:
            # Consecutive `>` lines are ONE paragraph — join before applying inline
            # formatting, or a **bold span** wrapped across source lines renders as
            # literal asterisks. A blank `>` line starts a new paragraph.
            paras, cur = [], []
            for q in quote:
                if q.strip():
                    cur.append(q.strip())
                elif cur:
                    paras.append(" ".join(cur)); cur = []
            if cur:
                paras.append(" ".join(cur))
            inner = "".join(f'<p style="margin:0 0 10px;">{md_inline(p)}</p>' for p in paras)
            inner = inner.replace('margin:0 0 10px;"', 'margin:0;"', 1) if len(paras) == 1 else inner
            out.append(f'<div class="callout">{inner}</div>')
            quote.clear()

    def flush_all():
        flush_para(); flush_list(); flush_quote()

    for raw in body.splitlines():
        line = raw.rstrip()
        stripped = line.strip()
        ph = re.fullmatch(r"\{\{([\w:]+)\}\}", stripped)
        if ph:
            flush_all()
            key = ph.group(1)
            if key not in PLACEHOLDERS:
                sys.exit(f"ERROR: unknown placeholder {{{{{key}}}}} — valid: {', '.join(PLACEHOLDERS)}")
            out.append(PLACEHOLDERS[key]())
        elif stripped.startswith("### "):
            flush_all(); out.append(f"<h3>{md_inline(stripped[4:])}</h3>")
        elif stripped.startswith("## "):
            flush_all(); out.append(f"<h2>{md_inline(stripped[3:])}</h2>")
        elif stripped in ("---", "***"):
            flush_all(); out.append('<hr class="rule">')
        elif stripped.startswith(">"):
            flush_para(); flush_list(); quote.append(stripped[1:].lstrip())
        elif re.match(r"^\d+\.\s+", stripped):
            flush_para(); flush_quote()
            if listtag not in (None, "ol"):
                flush_list()
            listtag = "ol"; listbuf.append(re.sub(r"^\d+\.\s+", "", stripped))
        elif stripped.startswith("- "):
            flush_para(); flush_quote()
            if listtag not in (None, "ul"):
                flush_list()
            listtag = "ul"; listbuf.append(stripped[2:])
        elif stripped == "":
            flush_all()
        else:
            flush_list(); flush_quote(); para.append(stripped)
    flush_all()
    return "\n".join(out)


# ---------------------------------------------------------------- pages
def page_shell(title: str, body: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<style>
{CSS}
</style>
</head>
<body>
<div class="wrap">
{body}
</div>
</body>
</html>
"""


def build_update(update_dir: Path) -> dict:
    md_file = update_dir / "update.md"
    meta, body = parse_front_matter(md_file.read_text(encoding="utf-8"))
    for req in ("title", "date"):
        if req not in meta:
            sys.exit(f"ERROR: {md_file} front matter is missing '{req}:'")
    kicker = meta.get("kicker", DATA["brand"]["kicker"])
    header = (
        '<p class="byline"><a href="../../index.html">← All updates</a></p>'
        f'<p class="kicker">{esc(kicker)}</p>'
        f"<h1>{esc(meta['title'])}</h1>"
    )
    if meta.get("dek"):
        header += f'<p class="dek">{esc(meta["dek"])}</p>'
    header += f'<p class="byline">Published {esc(meta["date"])} · {esc(meta.get("byline", "Compiled from primary research reports and rating-agency publications (all sources linked below)"))}</p>'
    footer = f'<p class="gen-note">Generated by banking-updates/scripts/build.py · data as of {esc(DATA["as_of"])} · built {date.today().isoformat()}</p>'
    html_out = page_shell(meta["title"], header + md_to_html(body) + footer)
    (update_dir / "index.html").write_text(html_out, encoding="utf-8")
    print(f"  built {update_dir.name}/index.html")
    return {"slug": update_dir.name, "meta": meta}


def build_index(entries: list) -> None:
    entries.sort(key=lambda e: e["meta"]["date"], reverse=True)
    cards = "".join(
        f'<a class="update-card" href="updates/{esc(e["slug"])}/index.html">'
        f'<span class="date">{esc(e["meta"]["date"])}</span>'
        f'<h3>{esc(e["meta"]["title"])}</h3>'
        f'<p>{esc(e["meta"].get("dek", ""))}</p></a>'
        for e in entries
    )
    body = (
        f'<p class="kicker">{esc(DATA["brand"]["kicker"])}</p>'
        f'<h1>{esc(DATA["brand"]["site_title"])}</h1>'
        '<p class="dek">Periodic investor updates on Vietnamese bank equities — '
        "compiled research metrics plus our own view, in one place.</p>"
        f"{cards}"
        f'<p class="gen-note">{len(entries)} update(s) · data as of {esc(DATA["as_of"])}</p>'
    )
    (ROOT / "index.html").write_text(page_shell(DATA["brand"]["site_title"], body), encoding="utf-8")
    print("  built index.html")


def main() -> None:
    updates_dir = ROOT / "updates"
    dirs = sorted(d for d in updates_dir.iterdir() if (d / "update.md").exists())
    if not dirs:
        sys.exit("No updates/<slug>/update.md files found.")
    print(f"Building {len(dirs)} update(s)…")
    entries = [build_update(d) for d in dirs]
    build_index(entries)
    print("Done.")


if __name__ == "__main__":
    main()
