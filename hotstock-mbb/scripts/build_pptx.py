#!/usr/bin/env python3
"""Turn the 6-slide TCB HotStock deck into a 4-slide MBB edition.

Structural work happens first (drop two slides, clean orphaned parts), then text,
then the chart — the order the OOXML tooling requires.

Slide arc: cover -> three reasons -> one chart -> catalyst. One idea per slide,
each stat appears exactly once, and the three numbered pillars on slide 2 map
1:1 to the three sections of the voiceover script.
"""
import os, re, subprocess, sys, zipfile

SRC = "tcb_pptx"
OUT = "Ngan_hang_MBB_Hotstock.pptx"
CLEAN = "/root/.claude/skills/pptx/scripts/clean.py"

TCB_RED = "E4002B"      # Techcombank brand red
MB_BLUE = "1B4F9C"      # MB Bank brand blue

# rIds of the slides being cut: the multi-series balance-sheet chart (slide 3)
# and the fundamentals card slide (slide 4), whose content overlapped slide 2.
DROP_RIDS = ["rId4", "rId5"]
KEEP_SLIDES = [1, 2, 5, 6]


# --------------------------------------------------------------------------- #
# Paragraph-level text replacement
# --------------------------------------------------------------------------- #
RUN_RE = re.compile(r"<a:r>(<a:rPr\b[^>]*/>|<a:rPr\b.*?</a:rPr>)?<a:t>(.*?)</a:t></a:r>", re.S)


def norm_rpr(rpr):
    if not rpr:
        return ""
    return re.sub(r'\s+(?:err|dirty|smtClean)="[^"]*"', "", rpr)


def replace_paragraphs(xml, edits, seen):
    """PowerPoint splits a visible phrase across runs that differ in spell-check
    flags and sometimes in size, so the paragraph's concatenated run text is the
    only reliable match unit. A matching paragraph collapses to a single run
    carrying the first run's formatting."""
    lookup = dict(edits)
    out, pos = [], 0
    for para in re.finditer(r"<a:p>.*?</a:p>", xml, re.S):
        out.append(xml[pos:para.start()])
        pos = para.end()
        body = para.group(0)
        runs = list(RUN_RE.finditer(body))
        if not runs:
            out.append(body)
            continue
        if "<a:fld" in body[runs[0].start():runs[-1].end()]:   # slide-number fields
            out.append(body)
            continue
        text = "".join(r.group(2) for r in runs)
        if text not in lookup:
            out.append(body)
            continue
        seen.add(text)
        out.append(body[:runs[0].start()]
                   + f"<a:r>{norm_rpr(runs[0].group(1))}<a:t>{lookup[text]}</a:t></a:r>"
                   + body[runs[-1].end():])
    out.append(xml[pos:])
    return "".join(out)


# --------------------------------------------------------------------------- #
# Slide copy: TCB -> MBB
# --------------------------------------------------------------------------- #
SLIDE_EDITS = {
# 1 — cover. Headline states the differentiator; the two chips tease pillars ①/③
# without numbering, so slide 2 owns the enumeration and nothing is numbered twice.
1: [
    ("TCB", "MBB"),                                                    # giant watermark
    ("MASVN · Jun 2026", "MASVN · Jul 2026"),
    ("Techcombank", "Ngân hàng MB"),
    ("HOSE · TCB", "HOSE · MBB"),
    ("Dẫn đầu về vốn chủ", "Dẫn đầu về CASA"),
    ("P/B chỉ ~1,23 lần — định giá rẻ trên nền tảng vốn mạnh.",
     "Vốn rẻ nhất hệ thống, room tín dụng cao nhất thị trường."),
    ("① ĐỊNH GIÁ", "ĐỊNH GIÁ"),
    ("Hấp dẫn", "Hợp lý"),
    ("P/B ~1,23x · CAR 15,2%", "P/B fwd ~1,2x · ROE 21,1%"),
    ("② CATALYST", "TĂNG TRƯỞNG"),
    ("Hồi phục", "Bứt tốc"),
    ("Mảng cốt lõi đảo chiều · đầu tư công", "Tín dụng 30–35% · LNTT +18,8%"),
    ("Một case đầu tư giá trị", "Một case tăng trưởng"),
    ("HotStock · TCB", "HotStock · MBB"),
],
# 2 — the three reasons, one hero number each: number, pillar name, evidence.
2: [
    ("01 / METRICS", "01 / THESIS"),
    ("Định giá hấp dẫn, nền tảng vốn vững chắc", "Ba lý do MBB đáng theo dõi"),
    ("Techcombank", "Ngân hàng MB"),
    ("HOSE · TCB", "HOSE · MBB"),
    ("1,23x", "1,2x"),
    ("P/B HIỆN TẠI", "① ĐỊNH GIÁ"),
    ("Thấp hơn ~8% so với trung bình 5 năm", "P/B dự phóng 2026 trên ROE 21,1%"),
    ("15,2%", "38%"),
    ("CAR Q1/26", "② VỐN RẺ"),
    ("Thuộc nhóm cao nhất khối ngân hàng tư nhân", "CASA cuối 2025, dẫn đầu toàn hệ thống"),
    ("+60%", "30–35%"),
    ("CỔ PHIẾU THƯỞNG", "③ TĂNG TRƯỞNG"),
    ("Vốn điều lệ dự kiến tăng lên 113.738 tỷ đồng", "Room tín dụng 2026, nhóm cao nhất thị trường"),
    ("Định giá &amp; nền tảng vốn", "Ba lý do đầu tư"),
],
# 5 — the single chart. Headline carries the takeaway, not a description.
5: [
    ("02 / FUNDAMENTALS", "02 / EARNINGS"),
    ("Động lực phục hồi từ mảng kinh doanh cốt lõi", "Lợi nhuận trước thuế tăng liên tục"),
    ("Các mảng từng chịu áp lực 2022–2023 đang bước vào chu kỳ hồi phục khi thị trường vốn cải thiện.",
     "LNTT gấp gần 1,8 lần chỉ sau 4 năm, dự phóng vượt 40.000 tỷ đồng trong năm 2026."),
],
# 6 — catalyst, two cards.
6: [
    ("Mở rộng hệ sinh thái &amp; đầu tư công", "Bứt tốc quy mô &amp; tăng vốn điều lệ"),
    ("TCB có cơ hội mở rộng vai trò trong tài trợ các dự án hạ tầng quy mô lớn và hưởng lợi từ xu hướng tháo gỡ nút thắt thanh khoản.",
     "Sau khi tổng tài sản tăng 43% trong năm 2025, MBB đặt mục tiêu vượt 2,1 triệu tỷ đồng và nâng vốn điều lệ lên hơn 102.000 tỷ đồng năm 2026."),
    ("ĐẦU TƯ CÔNG", "TỔNG TÀI SẢN"),
    ("ĐỘNG LỰC MỚI", "MỤC TIÊU 2026"),
    ("196.000 tỷ", "2,1 triệu tỷ"),
    ("Cảng hàng không Quốc tế Gia Bình — TCB kỳ vọng đồng hành tài trợ các siêu dự án hạ tầng.",
     "Tổng tài sản đạt 1.615.764 tỷ đồng cuối 2025, tăng 43%; mục tiêu vượt 2,1 triệu tỷ năm 2026."),
    ("Mở rộng dư địa tăng trưởng tín dụng", "Tín dụng mục tiêu tăng 30–35% năm 2026"),
    ("THANH KHOẢN", "TĂNG VỐN"),
    ("CHÍNH SÁCH HỖ TRỢ", "CHIA CỔ TỨC 25%"),
    ("Thông tư 22", "102.687 tỷ"),
    ("Định hướng sửa đổi Thông tư 22/2019/TT-NHNN tháo gỡ nút thắt thanh khoản hệ thống.",
     "Vốn điều lệ dự kiến tăng từ 80.550 tỷ đồng lên tối đa 102.687 tỷ đồng trong năm 2026."),
    ("TCB nằm trong nhóm hưởng lợi trực tiếp", "Cổ tức 25%: 10% tiền mặt + 15% cổ phiếu"),
],
}

NOTES_EDITS = {
1: [("TCB đang rẻ vì thị trường lo ngại, hay vì thị trường đang bỏ qua cơ hội? P/B ~1,15x, nền tảng vốn mạnh, nhiều động lực hồi phục phía trước.",
     "MBB đang được định giá đúng, hay thị trường chưa trả đủ cho ngân hàng có chi phí vốn rẻ nhất? P/B dự phóng 2026 ~1,2x đi cùng ROE 21,1%.")],
2: [("P/B forward ~1,15x, thấp hơn ~15% trung bình 5 năm. CAR 15,2% thuộc nhóm cao nhất khối tư nhân. Cổ phiếu thưởng 60% đưa vốn điều lệ lên 113.738 tỷ.",
     "Ba lý do: P/B dự phóng 2026 ~1,2x trên ROE 21,1%; CASA ~38% cuối 2025 dẫn đầu hệ thống; room tín dụng 30-35% nhờ nhận chuyển giao MBV.")],
5: [("Trái phiếu DN, chứng khoán, BĐS bước vào chu kỳ hồi phục. TCBS dẫn đầu lợi nhuận CTCK và tư vấn phát hành TPDN. Kỳ vọng nâng hạng FTSE thúc đẩy dòng vốn ngoại.",
     "LNTT tăng liên tục: 22.729 tỷ (2022), 26.306 tỷ (2023), 28.829 tỷ (2024), 34.268 tỷ (2025) và dự phóng 40.726 tỷ cho 2026, tương đương gấp 1,8 lần sau 4 năm.")],
6: [("TCB có cơ hội tài trợ hạ tầng lớn như Cảng HK Quốc tế Gia Bình (&gt;196.000 tỷ) và hưởng lợi từ định hướng sửa đổi Thông tư 22/2019. Định giá đã phản ánh phần lớn lo ngại.",
     "Tổng tài sản 1.615.764 tỷ cuối 2025, tăng 43%; mục tiêu vượt 2,1 triệu tỷ. Vốn điều lệ lên tối đa 102.687 tỷ, cổ tức 25% gồm 10% tiền mặt và 15% cổ phiếu.")],
}


def apply_edits(path, edits):
    xml = open(path, encoding="utf-8").read()
    seen = set()
    xml = replace_paragraphs(xml, edits, seen)
    missing = [o for o, _ in edits if o not in seen]
    if missing:
        sys.exit(f"{path}: no paragraph matched: {missing}")
    open(path, "w", encoding="utf-8").write(xml)


# --------------------------------------------------------------------------- #
# Chart: pre-tax profit, 2022-2026F
# --------------------------------------------------------------------------- #
YEARS = ["2022", "2023", "2024", "2025", "2026F"]
PBT = [22729, 26306, 28829, 34268, 40726]


def retarget_categories(xml):
    def repl(m):
        if not re.search(r"<c:v>20\d\d</c:v>", m.group(1)):
            return m.group(0)
        pts = "".join(f'<c:pt idx="{i}"><c:v>{y}</c:v></c:pt>' for i, y in enumerate(YEARS))
        return f'<c:strCache><c:ptCount val="{len(YEARS)}"/>{pts}</c:strCache>'
    return re.sub(r"<c:strCache>(.*?)</c:strCache>", repl, xml, flags=re.S)


def build_chart(path):
    xml = open(path, encoding="utf-8").read()
    # keep one series slot; the five-way income/cost split could not be sourced
    keep = "'Kết quả kinh doanh'!$A$15"
    sers = list(re.finditer(r"<c:ser>.*?</c:ser>", xml, re.S))
    assert len(sers) == 5, len(sers)
    for m in reversed(sers):
        if keep not in m.group(0):
            xml = xml[:m.start()] + xml[m.end():]
    assert xml.count("<c:ser>") == 1
    xml = xml.replace('<c:grouping val="stacked"/>', '<c:grouping val="clustered"/>')
    xml = xml.replace("<c:v>Thu nhập lãi thuần</c:v>", "<c:v>Lợi nhuận trước thuế</c:v>")
    xml = xml.replace('<c:showVal val="0"/>', '<c:showVal val="1"/>')   # surface the numbers
    xml = retarget_categories(xml)
    pts = "".join(f'<c:pt idx="{i}"><c:v>{v}</c:v></c:pt>' for i, v in enumerate(PBT))
    pat = re.compile(r"(\$U\$15:\$Y\$15.*?<c:numCache>)(.*?)(</c:numCache>)", re.S)
    xml, n = pat.subn(
        lambda m: m.group(1) + f'<c:formatCode>#,##0.00</c:formatCode>'
                  f'<c:ptCount val="{len(PBT)}"/>{pts}' + m.group(3), xml, count=1)
    assert n == 1, "chart value reference not found"
    open(path, "w", encoding="utf-8").write(xml)


# --------------------------------------------------------------------------- #
def drop_slides():
    """Remove the cut slides from sldIdLst, then let clean.py sweep the orphans
    (slide parts, notes slides, the balance-sheet chart and all their rels)."""
    p = f"{SRC}/ppt/presentation.xml"
    x = open(p, encoding="utf-8").read()
    for rid in DROP_RIDS:
        pat = f'<p:sldId id="\\d+" r:id="{rid}"/>'
        x, n = re.subn(pat, "", x)
        assert n == 1, f"{rid} not in sldIdLst"
    open(p, "w", encoding="utf-8").write(x)
    subprocess.run([sys.executable, CLEAN, SRC], check=True)

    remaining = sorted(int(re.search(r"\d+", f).group())
                       for f in os.listdir(f"{SRC}/ppt/slides") if f.endswith(".xml"))
    assert remaining == KEEP_SLIDES, remaining


def fix_app_props():
    p = f"{SRC}/docProps/app.xml"
    x = open(p, encoding="utf-8").read()
    n = len(KEEP_SLIDES)
    x = x.replace("<Slides>6</Slides>", f"<Slides>{n}</Slides>")
    x = x.replace("<Notes>6</Notes>", f"<Notes>{n}</Notes>")
    x = x.replace("<vt:variant><vt:lpstr>Slide Titles</vt:lpstr></vt:variant>"
                  "<vt:variant><vt:i4>6</vt:i4></vt:variant>",
                  "<vt:variant><vt:lpstr>Slide Titles</vt:lpstr></vt:variant>"
                  f"<vt:variant><vt:i4>{n}</vt:i4></vt:variant>")
    title = "<vt:lpstr>PowerPoint Presentation</vt:lpstr>"
    x = x.replace(title * 6, title * n)
    x = x.replace('<vt:vector size="11" baseType="lpstr">',
                  f'<vt:vector size="{11 - (6 - n)}" baseType="lpstr">')
    open(p, "w", encoding="utf-8").write(x)


def main():
    drop_slides()

    for i in KEEP_SLIDES:
        apply_edits(f"{SRC}/ppt/slides/slide{i}.xml", SLIDE_EDITS[i])
        apply_edits(f"{SRC}/ppt/notesSlides/notesSlide{i}.xml", NOTES_EDITS[i])

    swapped = 0
    for i in KEEP_SLIDES:
        p = f"{SRC}/ppt/slides/slide{i}.xml"
        x = open(p, encoding="utf-8").read()
        swapped += x.count(TCB_RED)
        open(p, "w", encoding="utf-8").write(x.replace(TCB_RED, MB_BLUE))
    print(f"recoloured {swapped} brand-accent references")

    build_chart(f"{SRC}/ppt/charts/chart2.xml")
    fix_app_props()

    p = f"{SRC}/docProps/core.xml"
    x = open(p, encoding="utf-8").read()
    x = x.replace("<dc:title>PptxGenJS Presentation</dc:title>",
                  "<dc:title>HotStock · MBB · Ngân hàng MB</dc:title>")
    x = x.replace("<dc:subject>PptxGenJS Presentation</dc:subject>",
                  "<dc:subject>Equity Research · Vietnam Banks</dc:subject>")
    open(p, "w", encoding="utf-8").write(x)

    for root, _d, files in os.walk(f"{SRC}/ppt"):
        for f in files:
            if not f.endswith(".xml"):
                continue
            x = open(os.path.join(root, f), encoding="utf-8").read()
            for bad in ("TCB", "Techcombank", "TCBS"):
                if bad in x:
                    sys.exit(f"leftover {bad!r} in {f}")

    if os.path.exists(OUT):
        os.remove(OUT)
    zf = zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED)
    for root, _d, files in os.walk(SRC):
        for f in files:
            full = os.path.join(root, f)
            zf.write(full, os.path.relpath(full, SRC))
    zf.close()
    print(f"wrote {OUT} ({len(KEEP_SLIDES)} slides, {os.path.getsize(OUT)} bytes)")


main()
