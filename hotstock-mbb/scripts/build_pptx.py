#!/usr/bin/env python3
"""Build the 4-slide MBB HotStock deck on the FRT research-note template.

The FRT template's house style is one chart plus one takeaway headline per slide
under a running report title. Four of its ten slides are kept and repointed at
the four charts that actually decide a bank case:

  1. FRT slide 1 (2 bar series)  -> Dư nợ tín dụng & tiền gửi   — the volume engine
  2. FRT slide 8 (stacked bars)  -> NIM & chi phí vốn            — the margin engine
  3. FRT slide 3 (clustered bar) -> Nợ xấu & chi phí tín dụng    — the risk
  4. FRT slide 7 (single bar)    -> ROE                          — the return behind the P/B

Every figure comes from the Mirae Asset MBB model (FinModel_MBB_1Q26), sheets
'A-Chart' and 'Valuation'. No third-party research is cited anywhere in the deck.

Structural work runs first, then text, then charts.
"""
import os, re, subprocess, sys, zipfile

SRC = "frt"
OUT = "Ngan_hang_MBB_Hotstock.pptx"
CLEAN = "/root/.claude/skills/pptx/scripts/clean.py"

# presentation-level rIds, in the order the finished deck should play them
KEEP = [("rId2", 1), ("rId9", 8), ("rId4", 3), ("rId8", 7)]

RUNNING_TITLE = "Vốn rẻ dẫn đầu, tăng trưởng vượt trội"
SOURCE = "Nguồn: Dữ liệu doanh nghiệp, Mirae Asset Research"
SOURCE_EST = "Nguồn: Dữ liệu doanh nghiệp, Mirae Asset Research ước tính"
YEARS = ["22", "23", "24", "25", "26F"]

# --- A-Chart, nghìn tỷ đồng (rows 31, 32) ---------------------------------- #
CREDIT = [460.574, 611.049, 776.658, 1048.247, 1344.157]
DEPOSITS = [443.606, 567.533, 714.154, 923.460, 1163.655]
# --- A-Chart, % (rows 4, 9) ------------------------------------------------ #
NIM = [5.76, 4.87, 4.13, 3.76, 3.69]
COST_OF_FUNDS = [2.83, 4.30, 3.51, 3.24, 3.10]
# --- A-Chart, % (rows 99, 100) --------------------------------------------- #
NPL = [1.09, 1.61, 1.62, 1.90, 1.50]
CREDIT_COST = [1.75, 1.00, 1.23, 1.57, 1.22]
# --- Valuation, % (row 23) ------------------------------------------------- #
ROE = [24.61, 23.45, 21.18, 20.67, 20.51]


# --------------------------------------------------------------------------- #
# Paragraph-level text replacement (shared by slides and chart titles)
# --------------------------------------------------------------------------- #
RUN_RE = re.compile(r"<a:r>(<a:rPr\b[^>]*/>|<a:rPr\b.*?</a:rPr>)?<a:t>(.*?)</a:t></a:r>", re.S)


def norm_rpr(rpr):
    return re.sub(r'\s+(?:err|dirty|smtClean)="[^"]*"', "", rpr) if rpr else ""


def rewrite_paragraph(body, new_text):
    """Collapse every run in one <a:p> into a single run keeping the first run's
    formatting. PowerPoint splits phrases across runs on spell-check and size
    boundaries, so the paragraph is the only stable unit to match."""
    runs = list(RUN_RE.finditer(body))
    if not runs or "<a:fld" in body[runs[0].start():runs[-1].end()]:
        return None
    return (body[:runs[0].start()]
            + f"<a:r>{norm_rpr(runs[0].group(1))}<a:t>{new_text}</a:t></a:r>"
            + body[runs[-1].end():])


def replace_paragraphs(xml, edits, path):
    lookup, seen = dict(edits), set()
    out, pos = [], 0
    for para in re.finditer(r"<a:p>.*?</a:p>", xml, re.S):
        out.append(xml[pos:para.start()])
        pos = para.end()
        body = para.group(0)
        text = "".join(r.group(2) for r in RUN_RE.finditer(body))
        rewritten = rewrite_paragraph(body, lookup[text]) if text in lookup else None
        if rewritten is None:
            out.append(body)
        else:
            seen.add(text)
            out.append(rewritten)
    out.append(xml[pos:])
    missing = [o for o, _ in edits if o not in seen]
    if missing:
        sys.exit(f"{path}: no paragraph matched: {missing}")
    return "".join(out)


def edit_text(path, edits):
    xml = open(path, encoding="utf-8").read()
    open(path, "w", encoding="utf-8").write(replace_paragraphs(xml, edits, path))


# --------------------------------------------------------------------------- #
# Slide copy
# --------------------------------------------------------------------------- #
SLIDE_EDITS = {
1: [
    ("Trong các năm gần đây Long Châu trở thành động lực tăng trưởng doanh thu chủ đạo của FRT",
     "Tín dụng tăng 35% trong năm 2025 và liên tục mở rộng nhanh hơn tốc độ huy động"),
    ("Chuyển lợi thế cạnh tranh thành lợi nhuận", RUNNING_TITLE),
    ("Nguồn: Dữ liệu doanh nghiệp, Mirae Asset Research ước tính", SOURCE_EST),
],
8: [
    ("Long Châu còn nhiều dư địa mở rộng thị phần và tăng trưởng",
     "CASA gần 38% kéo chi phí vốn về 3,1%, bù lại phần lớn áp lực thu hẹp của biên lãi ròng"),
    ("Chuyển lợi thế cạnh tranh thành lợi nhuận", RUNNING_TITLE),
    ("Nguồn: Euromonitor, Mirae Asset Research", SOURCE_EST),
],
3: [
    ("Long Châu đã thiết lập khoảng cách đáng kể về quy mô so với các đối thủ",
     "Nợ xấu nhích lên 1,9% trong năm 2025 nhưng chi phí tín dụng được dự báo hạ nhiệt"),
    ("Chuyển lợi thế cạnh tranh thành lợi nhuận", RUNNING_TITLE),
    ("Nguồn: Dữ liệu doanh nghiệp, Euromonitor, Mirae Asset Research", SOURCE_EST),
],
7: [
    ("Quy mô trường bán lẻ nhà thuốc vẫn đang trên đà tăng trưởng",
     "ROE duy trì trên 20% suốt chu kỳ, trong khi P/B dự phóng 2026 chỉ quanh 1,2 lần"),
    ("Chuyển lợi thế cạnh tranh thành lợi nhuận", RUNNING_TITLE),
    ("Nguồn: Euromonitor, Mirae Asset Research", SOURCE_EST),
],
}


# --------------------------------------------------------------------------- #
# Charts
# --------------------------------------------------------------------------- #
def keep_series(xml, indices):
    """Keep the listed <c:ser> blocks, drop the rest, drop any plot group left
    empty, and drop the c15 'filtered series' caches — hidden series PowerPoint
    keeps around that would otherwise still carry the template's numbers."""
    for tag in ("filteredBarSeries", "filteredLineSeries", "filteredAreaSeries",
                "filteredScatterSeries", "filteredPieSeries"):
        xml = re.sub(rf"<c15:{tag}>.*?</c15:{tag}>", "", xml, flags=re.S)
    sers = list(re.finditer(r"<c:ser>.*?</c:ser>", xml, re.S))
    for i, m in reversed(list(enumerate(sers))):
        if i not in indices:
            xml = xml[:m.start()] + xml[m.end():]
    for group in ("lineChart", "barChart", "areaChart"):
        for m in reversed(list(re.finditer(rf"<c:{group}>.*?</c:{group}>", xml, re.S))):
            if "<c:ser>" not in m.group(0):
                xml = xml[:m.start()] + xml[m.end():]
    assert xml.count("<c:ser>") == len(indices), xml.count("<c:ser>")
    return xml


def fill_series(xml, series, fmt):
    """Rewrite each surviving series' name, categories and cached values.

    The category axis is replaced wholesale rather than patched: some template
    charts cache their years as numbers, which cannot hold a label like "26F".
    """
    cat_pts = "".join(f'<c:pt idx="{i}"><c:v>{y}</c:v></c:pt>' for i, y in enumerate(YEARS))
    out, pos = [], 0
    for i, m in enumerate(re.finditer(r"<c:ser>.*?</c:ser>", xml, re.S)):
        out.append(xml[pos:m.start()])
        pos = m.end()
        body = m.group(0)
        name, values = series[i]

        # the chart title is also a <c:tx> — scope the name swap to the series
        body, n = re.subn(r"<c:tx>.*?</c:tx>", f"<c:tx><c:v>{name}</c:v></c:tx>",
                          body, count=1, flags=re.S)
        assert n == 1, f"series {i}: name not found"

        def cat(mm):
            ref = re.search(r"<c:f>(.*?)</c:f>", mm.group(0), re.S)
            f = f"<c:f>{ref.group(1)}</c:f>" if ref else ""
            return (f'<c:cat><c:strRef>{f}<c:strCache>'
                    f'<c:ptCount val="{len(YEARS)}"/>{cat_pts}</c:strCache></c:strRef></c:cat>')

        body, n = re.subn(r"<c:cat>.*?</c:cat>", cat, body, flags=re.S)
        assert n == 1, f"series {i}: expected one category axis, found {n}"

        pts = "".join(f'<c:pt idx="{j}"><c:v>{v}</c:v></c:pt>' for j, v in enumerate(values))
        cache = (f'<c:numCache><c:formatCode>{fmt}</c:formatCode>'
                 f'<c:ptCount val="{len(values)}"/>{pts}</c:numCache>')
        val = re.search(r"<c:val>.*?</c:val>", body, re.S)
        assert val, f"series {i}: no values"
        vbody, n = re.subn(r"<c:numCache>.*?</c:numCache>", cache, val.group(0), flags=re.S)
        assert n == 1, f"series {i}: expected one numCache in <c:val>, found {n}"
        body = body[:val.start()] + vbody + body[val.end():]

        out.append(body)
    out.append(xml[pos:])
    return "".join(out)


def build_chart(path, indices, series, fmt, title=None):
    xml = open(path, encoding="utf-8").read()
    xml = keep_series(xml, indices)
    xml = fill_series(xml, series, fmt)
    xml = xml.replace('<c:grouping val="stacked"/>', '<c:grouping val="clustered"/>')
    xml = re.sub(r'<c:(max|min) val="[^"]*"/>', "", xml)   # the template's fixed axis caps
    xml = re.sub(r'<c:numFmt formatCode="(?:0%|0|#,##0)" sourceLinked="\d"/>',
                 f'<c:numFmt formatCode="{fmt}" sourceLinked="0"/>', xml)
    xml = xml.replace('<c:showVal val="0"/>', '<c:showVal val="1"/>')
    if title:
        xml = replace_paragraphs(xml, [title], path)
    open(path, "w", encoding="utf-8").write(xml)


# --------------------------------------------------------------------------- #
def restructure():
    p = f"{SRC}/ppt/presentation.xml"
    x = open(p, encoding="utf-8").read()
    lst = re.search(r"<p:sldIdLst>.*?</p:sldIdLst>", x, re.S).group(0)
    entries = {m.group(1): m.group(0)
               for m in re.finditer(r'<p:sldId id="\d+" r:id="(rId\d+)"/>', lst)}
    kept = "".join(entries[rid] for rid, _ in KEEP)
    open(p, "w", encoding="utf-8").write(x.replace(lst, f"<p:sldIdLst>{kept}</p:sldIdLst>"))
    subprocess.run([sys.executable, CLEAN, SRC], check=True)

    remaining = sorted(int(re.search(r"\d+", f).group())
                       for f in os.listdir(f"{SRC}/ppt/slides") if f.endswith(".xml"))
    assert remaining == sorted(n for _, n in KEEP), remaining


def fix_props():
    p = f"{SRC}/docProps/app.xml"
    x = open(p, encoding="utf-8").read()
    x = re.sub(r"<Slides>\d+</Slides>", f"<Slides>{len(KEEP)}</Slides>", x)
    x = re.sub(r"<Notes>\d+</Notes>", "<Notes>0</Notes>", x)
    open(p, "w", encoding="utf-8").write(x)

    p = f"{SRC}/docProps/core.xml"
    x = open(p, encoding="utf-8").read()
    x = re.sub(r"<dc:title>.*?</dc:title>",
               "<dc:title>HotStock · MBB · Ngân hàng MB</dc:title>", x, flags=re.S)
    open(p, "w", encoding="utf-8").write(x)


def main():
    restructure()
    for n, edits in SLIDE_EDITS.items():
        edit_text(f"{SRC}/ppt/slides/slide{n}.xml", edits)

    pct = ("(%)",)
    build_chart(f"{SRC}/ppt/charts/chart1.xml", {0, 1},
                [("Dư nợ tín dụng", CREDIT), ("Tiền gửi khách hàng", DEPOSITS)],
                "#,##0")
    build_chart(f"{SRC}/ppt/charts/chart8.xml", {0, 1},
                [("NIM", NIM), ("Chi phí vốn", COST_OF_FUNDS)],
                "#,##0.0", ("(Thị phần)", *pct))
    build_chart(f"{SRC}/ppt/charts/chart3.xml", {0, 1},
                [("Tỷ lệ nợ xấu", NPL), ("Chi phí tín dụng", CREDIT_COST)],
                "#,##0.0", ("(số lượng cửa hàng)", *pct))
    build_chart(f"{SRC}/ppt/charts/chart7.xml", {0},
                [("ROE", ROE)], "#,##0.0", ("(Nghìn tỷ đồng)", *pct))

    fix_props()

    banned = ("FRT", "Long Châu", "Pharmacity", "Euromonitor", "An Khang",
              "BSC", "KBSV", "VCBS", "SSI", "VNDirect", "Bloomberg")
    for root, _d, files in os.walk(f"{SRC}/ppt"):
        for f in files:
            if not f.endswith(".xml"):
                continue
            x = open(os.path.join(root, f), encoding="utf-8").read()
            for bad in banned:
                if bad in x:
                    sys.exit(f"leftover {bad!r} in {root}/{f}")

    if os.path.exists(OUT):
        os.remove(OUT)
    zf = zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED)
    for root, _d, files in os.walk(SRC):
        for f in files:
            full = os.path.join(root, f)
            zf.write(full, os.path.relpath(full, SRC))
    zf.close()
    print(f"wrote {OUT} ({len(KEEP)} slides, {os.path.getsize(OUT)} bytes)")


main()
