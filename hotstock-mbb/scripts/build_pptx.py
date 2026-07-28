#!/usr/bin/env python3
"""Build the 4-slide MBB HotStock deck on the FRT research-note template.

The FRT deck's house style is one chart plus one takeaway headline per slide,
under a running report title. We keep four of its ten slides and repoint them at
MBB data:

  1. FRT slide 1  (stacked cols + total line) -> Tổng tài sản 2022-2026F
  2. FRT slide 7  (single column + labels)    -> Lợi nhuận trước thuế 2022-2026F
  3. FRT slide 8  (stacked share cols)        -> Vốn điều lệ 2022-2026F
  4. FRT slide 9  (6x4 table)                 -> Luận điểm đầu tư & định giá

Structural work runs first, then text, then charts and the table.
"""
import os, re, subprocess, sys, zipfile

SRC = "frt"
OUT = "Ngan_hang_MBB_Hotstock.pptx"
CLEAN = "/root/.claude/skills/pptx/scripts/clean.py"

# presentation-level rIds, in the order the finished deck should play them
KEEP = [("rId2", 1), ("rId8", 7), ("rId9", 8), ("rId10", 9)]

RUNNING_TITLE = "Vốn rẻ dẫn đầu, tăng trưởng vượt trội"
YEARS = ["22", "23", "24", "25", "26F"]

# nghìn tỷ đồng, matching the template's unit convention
TOTAL_ASSETS = [728.532, 944.954, 1133.797, 1615.764, 2100.0]
PBT = [22.729, 26.306, 28.829, 34.268, 40.726]
CHARTER_CAPITAL = [45.340, 52.141, 53.063, 80.550, 102.687]


# --------------------------------------------------------------------------- #
# Paragraph-level text replacement (shared by slides and chart titles)
# --------------------------------------------------------------------------- #
RUN_RE = re.compile(r"<a:r>(<a:rPr\b[^>]*/>|<a:rPr\b.*?</a:rPr>)?<a:t>(.*?)</a:t></a:r>", re.S)


def norm_rpr(rpr):
    return re.sub(r'\s+(?:err|dirty|smtClean)="[^"]*"', "", rpr) if rpr else ""


def rewrite_paragraph(body, new_text):
    """Collapse every run in one <a:p> into a single run keeping the first
    run's formatting. PowerPoint splits phrases across runs on spell-check and
    size boundaries, so the paragraph is the only stable unit to match."""
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
        runs = list(RUN_RE.finditer(body))
        text = "".join(r.group(2) for r in runs)
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
1: [   # -> Tổng tài sản
    ("Trong các năm gần đây Long Châu trở thành động lực tăng trưởng doanh thu chủ đạo của FRT",
     "Tổng tài sản tăng 43% trong năm 2025 và hướng tới mốc 2,1 triệu tỷ đồng trong năm 2026"),
    ("Chuyển lợi thế cạnh tranh thành lợi nhuận", RUNNING_TITLE),
    ("Nguồn: Dữ liệu doanh nghiệp, Mirae Asset Research ước tính",
     "Nguồn: Báo cáo tài chính MB, kế hoạch ĐHĐCĐ 2026"),
],
7: [   # -> Lợi nhuận trước thuế
    ("Quy mô trường bán lẻ nhà thuốc vẫn đang trên đà tăng trưởng",
     "Lợi nhuận trước thuế gấp gần 1,8 lần chỉ sau 4 năm, dự phóng vượt 40.000 tỷ đồng"),
    ("Chuyển lợi thế cạnh tranh thành lợi nhuận", RUNNING_TITLE),
    ("Nguồn: Euromonitor, Mirae Asset Research",
     "Nguồn: Báo cáo tài chính MB, dự phóng Mirae Asset Research"),
],
8: [   # -> Vốn điều lệ
    ("Long Châu còn nhiều dư địa mở rộng thị phần và tăng trưởng",
     "Vốn điều lệ tăng hơn gấp đôi sau 4 năm, tạo dư địa cho tín dụng tăng 30–35%"),
    ("Chuyển lợi thế cạnh tranh thành lợi nhuận", RUNNING_TITLE),
    ("Nguồn: Euromonitor, Mirae Asset Research",
     "Nguồn: Công bố thông tin của MB, kế hoạch ĐHĐCĐ 2026"),
],
9: [   # -> Luận điểm & định giá
    ("Việc chuẩn hóa quy định và siết chặt tuân thủ sẽ thúc đẩy quá trình hợp nhất thị phần",
     "Định giá dự phóng 2026 lùi về ~1,2 lần P/B trong khi ROE vẫn duy trì trên 21%"),
    ("Chuyển lợi thế cạnh tranh thành lợi nhuận", RUNNING_TITLE),
    ("Nguồn: Mirae Asset Research tổng hợp từ các văn bản pháp lý hiện hành",
     "Nguồn: BSC, KBSV, Mirae Asset Research, VCBS; Mirae Asset Research tổng hợp"),
],
}

# Table cells are addressed positionally: "7/2025" and "Thông tư " each occur in
# several cells, so a text-keyed lookup would overwrite the wrong ones.
# (row, col) -> list of paragraph texts, one per non-empty paragraph in that cell
TABLE = {
    (0, 0): ["Luận điểm", "đầu tư"],
    (0, 1): ["Số liệu"],
    (0, 2): ["Chỉ tiêu"],
    (0, 3): ["Ý nghĩa với cổ phiếu MBB"],

    (1, 0): ["① Định giá", "(P/B dự phóng)"],
    (1, 1): ["~1,2x"],
    (1, 2): ["P/B trên giá trị sổ sách dự phóng năm 2026, so với 1,39x tại thời điểm hiện tại."],
    (1, 3): ["Thấp hơn cả P/B hiện tại lẫn trung bình 5 năm 1,34x, trong khi khả năng sinh lời không suy giảm."],

    (2, 0): ["② Vốn rẻ (CASA)"],
    (2, 1): ["~38%"],
    (2, 2): ["Tỷ lệ tiền gửi không kỳ hạn tại thời điểm cuối năm 2025."],
    (2, 3): ["Dẫn đầu hệ thống, giúp MBB giữ chi phí huy động ở nhóm thấp nhất khi NIM toàn ngành thu hẹp."],

    (3, 0): ["③ Tăng trưởng", "(room tín dụng)"],
    (3, 1): ["30–35%"],
    (3, 2): ["Mục tiêu tăng trưởng tín dụng năm 2026; đã đạt khoảng 10% tính tới tháng 5."],
    (3, 3): ["Hạn mức thuộc nhóm cao nhất thị trường cho giai đoạn 2026–2028 sau khi nhận chuyển giao MBV."],

    (4, 0): ["Sinh lời", "(ROE 2025)"],
    (4, 1): ["21,1%"],
    (4, 2): ["Tỷ suất sinh lời trên vốn chủ sở hữu cả năm 2025, theo công bố của MB."],
    (4, 3): ["Thuộc nhóm cao nhất trong các ngân hàng quy mô lớn, hỗ trợ cho một mặt bằng định giá cao hơn."],

    (5, 0): ["Giá mục tiêu", "(đồng/cổ phiếu)"],
    (5, 1): ["32.900 – 37.230"],
    (5, 2): ["Vùng giá mục tiêu năm 2026 của BSC, Mirae Asset, KBSV và VCBS."],
    (5, 3): ["Cả bốn nhóm phân tích đều đang duy trì khuyến nghị MUA đối với cổ phiếu MBB."],
}


def edit_table(path):
    xml = open(path, encoding="utf-8").read()
    tbl = re.search(r"<a:tbl>.*?</a:tbl>", xml, re.S)
    assert tbl, "no table on slide"
    body, used = tbl.group(0), set()

    out_rows, pos = [], 0
    for ri, row in enumerate(re.finditer(r"<a:tr\b.*?</a:tr>", body, re.S)):
        out_rows.append(body[pos:row.start()])
        pos = row.end()
        rbody, rpos, cells = row.group(0), 0, []
        for ci, cell in enumerate(re.finditer(r"<a:tc\b[^>]*>.*?</a:tc>", rbody, re.S)):
            cells.append(rbody[rpos:cell.start()])
            rpos = cell.end()
            texts = TABLE.get((ri, ci))
            if texts is None:
                cells.append(cell.group(0))
                continue
            cbody, cpos, paras, n = cell.group(0), 0, [], 0
            for para in re.finditer(r"<a:p>.*?</a:p>", cbody, re.S):
                paras.append(cbody[cpos:para.start()])
                cpos = para.end()
                pb = para.group(0)
                if not RUN_RE.search(pb):            # spacer paragraph
                    paras.append(pb)
                    continue
                if n >= len(texts):
                    sys.exit(f"cell r{ri}c{ci} has more paragraphs than replacements")
                paras.append(rewrite_paragraph(pb, texts[n]) or pb)
                n += 1
            if n != len(texts):
                sys.exit(f"cell r{ri}c{ci}: filled {n} of {len(texts)} paragraphs")
            paras.append(cbody[cpos:])
            cells.append("".join(paras))
            used.add((ri, ci))
        cells.append(rbody[rpos:])
        out_rows.append("".join(cells))
    out_rows.append(body[pos:])

    missing = set(TABLE) - used
    if missing:
        sys.exit(f"table cells never reached: {sorted(missing)}")
    xml = xml[:tbl.start()] + "".join(out_rows) + xml[tbl.end():]
    open(path, "w", encoding="utf-8").write(xml)


# --------------------------------------------------------------------------- #
# Charts
# --------------------------------------------------------------------------- #
def set_categories(xml):
    """Rewrite the category axis as a string cache. Some template charts cache
    their years as numbers, which cannot hold a label like "26F", so the whole
    <c:cat> is replaced rather than patched in place."""
    pts = "".join(f'<c:pt idx="{i}"><c:v>{y}</c:v></c:pt>' for i, y in enumerate(YEARS))

    def repl(m):
        ref = re.search(r"<c:f>(.*?)</c:f>", m.group(0), re.S)
        f = f"<c:f>{ref.group(1)}</c:f>" if ref else ""
        return (f'<c:cat><c:strRef>{f}<c:strCache>'
                f'<c:ptCount val="{len(YEARS)}"/>{pts}</c:strCache></c:strRef></c:cat>')

    xml, n = re.subn(r"<c:cat>.*?</c:cat>", repl, xml, flags=re.S)
    assert n == 1, f"expected one category axis, found {n}"
    return xml


def set_values(xml, values, fmt):
    """Rewrite the cached values of the one surviving series."""
    pts = "".join(f'<c:pt idx="{i}"><c:v>{v}</c:v></c:pt>' for i, v in enumerate(values))
    new = f'<c:formatCode>{fmt}</c:formatCode><c:ptCount val="{len(values)}"/>{pts}'
    val = re.search(r"<c:val>.*?</c:val>", xml, re.S)
    assert val, "no series values left to fill"
    body, n = re.subn(r"<c:numCache>.*?</c:numCache>", f"<c:numCache>{new}</c:numCache>",
                      val.group(0), flags=re.S)
    assert n == 1, f"expected one numCache in <c:val>, found {n}"
    return xml[:val.start()] + body + xml[val.end():]


def keep_one_series(xml, keep_index):
    """Drop every <c:ser> but one, drop any plot group left without series, and
    drop the c15 'filtered series' caches — hidden series PowerPoint keeps around
    that would otherwise still carry the template's original numbers."""
    for tag in ("filteredBarSeries", "filteredLineSeries", "filteredAreaSeries",
                "filteredScatterSeries", "filteredPieSeries"):
        xml = re.sub(rf"<c15:{tag}>.*?</c15:{tag}>", "", xml, flags=re.S)
    sers = list(re.finditer(r"<c:ser>.*?</c:ser>", xml, re.S))
    for i, m in reversed(list(enumerate(sers))):
        if i != keep_index:
            xml = xml[:m.start()] + xml[m.end():]
    for group in ("lineChart", "barChart", "areaChart"):
        for m in reversed(list(re.finditer(rf"<c:{group}>.*?</c:{group}>", xml, re.S))):
            if "<c:ser>" not in m.group(0):
                xml = xml[:m.start()] + xml[m.end():]
    assert xml.count("<c:ser>") == 1
    return xml


def build_chart(path, keep_index, series_name, values, fmt, title=None):
    xml = open(path, encoding="utf-8").read()
    xml = keep_one_series(xml, keep_index)
    # scope the name swap to the series: the chart title is also a <c:tx>, and it
    # comes first in the part
    ser = re.search(r"<c:ser>.*?</c:ser>", xml, re.S)
    assert ser, "no series left to name"
    body, n = re.subn(r"<c:tx>.*?</c:tx>", f"<c:tx><c:v>{series_name}</c:v></c:tx>",
                      ser.group(0), count=1, flags=re.S)
    assert n == 1, "series name not found"
    xml = xml[:ser.start()] + body + xml[ser.end():]
    xml = xml.replace('<c:grouping val="stacked"/>', '<c:grouping val="clustered"/>')
    xml = re.sub(r'<c:max val="[^"]*"/>', "", xml)      # FRT's fixed axis caps
    xml = re.sub(r'<c:numFmt formatCode="(?:0%|0)" sourceLinked="\d"/>',
                 f'<c:numFmt formatCode="{fmt}" sourceLinked="0"/>', xml)
    xml = xml.replace('<c:showVal val="0"/>', '<c:showVal val="1"/>')
    xml = set_categories(xml)
    xml = set_values(xml, values, fmt)
    if title:
        xml = replace_paragraphs(xml, [(title[0], title[1])], path)
    open(path, "w", encoding="utf-8").write(xml)


# --------------------------------------------------------------------------- #
def restructure():
    """Keep four slides, in the order the story needs, and sweep the rest."""
    p = f"{SRC}/ppt/presentation.xml"
    x = open(p, encoding="utf-8").read()
    lst = re.search(r"<p:sldIdLst>.*?</p:sldIdLst>", x, re.S).group(0)
    entries = {m.group(1): m.group(0)
               for m in re.finditer(r'<p:sldId id="\d+" r:id="(rId\d+)"/>', lst)}
    kept = "".join(entries[rid] for rid, _ in KEEP)
    x = x.replace(lst, f"<p:sldIdLst>{kept}</p:sldIdLst>")
    open(p, "w", encoding="utf-8").write(x)
    subprocess.run([sys.executable, CLEAN, SRC], check=True)

    remaining = sorted(int(re.search(r"\d+", f).group())
                       for f in os.listdir(f"{SRC}/ppt/slides") if f.endswith(".xml"))
    assert remaining == sorted(n for _, n in KEEP), remaining


def fix_props():
    p = f"{SRC}/docProps/app.xml"
    x = open(p, encoding="utf-8").read()
    n = len(KEEP)
    x = re.sub(r"<Slides>\d+</Slides>", f"<Slides>{n}</Slides>", x)
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
    edit_table(f"{SRC}/ppt/slides/slide9.xml")

    # chart1 and chart7 already carry the "(Nghìn tỷ đồng)" unit caption
    build_chart(f"{SRC}/ppt/charts/chart1.xml", 0, "Tổng tài sản", TOTAL_ASSETS, "#,##0")
    build_chart(f"{SRC}/ppt/charts/chart7.xml", 0, "Lợi nhuận trước thuế", PBT, "#,##0.0")
    build_chart(f"{SRC}/ppt/charts/chart8.xml", 0, "Vốn điều lệ", CHARTER_CAPITAL,
                "#,##0.0", ("(Thị phần)", "(Nghìn tỷ đồng)"))

    fix_props()

    for root, _d, files in os.walk(f"{SRC}/ppt"):
        for f in files:
            if not f.endswith(".xml"):
                continue
            x = open(os.path.join(root, f), encoding="utf-8").read()
            for bad in ("FRT", "Long Châu", "Pharmacity", "Euromonitor"):
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
