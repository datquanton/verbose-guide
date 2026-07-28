#!/usr/bin/env python3
"""Turn the TCB HotStock deck into the MBB edition, preserving every layout/geometry."""
import os, re, sys, zipfile

SRC = "tcb_pptx"
OUT = "Ngan_hang_MBB_Hotstock.pptx"

TCB_RED = "E4002B"      # Techcombank brand red
MB_BLUE = "1B4F9C"      # MB Bank brand blue


# --------------------------------------------------------------------------- #
# Run merging: PowerPoint splits headings across runs that differ only by the
# err="1" spell-check flag, so a visible phrase is not a contiguous string.
# --------------------------------------------------------------------------- #
RUN_RE = re.compile(r"<a:r>(<a:rPr\b[^>]*/>|<a:rPr\b.*?</a:rPr>)?<a:t>(.*?)</a:t></a:r>", re.S)


def norm_rpr(rpr):
    if not rpr:
        return ""
    return re.sub(r'\s+(?:err|dirty|smtClean)="[^"]*"', "", rpr)


def replace_paragraphs(xml, edits, seen):
    """Rewrite whole paragraphs: PowerPoint splits a visible phrase across runs
    that differ in spell-check flags and sometimes in size, so the only reliable
    unit to match is the paragraph's concatenated run text. Matching paragraphs
    collapse to a single run carrying the first run's formatting."""
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
        span = body[runs[0].start():runs[-1].end()]
        if "<a:fld" in span:          # never disturb slide-number fields
            out.append(body)
            continue
        text = "".join(r.group(2) for r in runs)
        if text not in lookup:
            out.append(body)
            continue
        seen.add(text)
        new_run = f"<a:r>{norm_rpr(runs[0].group(1))}<a:t>{lookup[text]}</a:t></a:r>"
        out.append(body[:runs[0].start()] + new_run + body[runs[-1].end():])
    out.append(xml[pos:])
    return "".join(out)


# --------------------------------------------------------------------------- #
# Slide copy: TCB -> MBB
# --------------------------------------------------------------------------- #
SLIDE_EDITS = {
1: [
    ("TCB", "MBB"),                                                    # giant watermark
    ("MASVN · Jun 2026", "MASVN · Jul 2026"),
    ("Techcombank", "Ngân hàng MB"),
    ("HOSE · TCB", "HOSE · MBB"),
    ("Dẫn đầu về vốn chủ", "Dẫn đầu về CASA"),
    ("P/B chỉ ~1,23 lần — định giá rẻ trên nền tảng vốn mạnh.",
     "CASA ~38% — chi phí vốn rẻ nhất toàn hệ thống."),
    ("Hấp dẫn", "Hợp lý"),
    ("P/B ~1,23x · CAR 15,2%", "P/B fwd ~1,2x · ROE 21%"),
    ("Hồi phục", "Bứt tốc"),
    ("Mảng cốt lõi đảo chiều · đầu tư công", "Room tín dụng cao nhất · tăng vốn"),
    ("Một case đầu tư giá trị", "Một case tăng trưởng"),
    ("HotStock · TCB", "HotStock · MBB"),
],
2: [
    ("Định giá hấp dẫn, nền tảng vốn vững chắc", "Định giá hợp lý trên nền sinh lời đầu ngành"),
    ("Techcombank", "Ngân hàng MB"),
    ("HOSE · TCB", "HOSE · MBB"),
    ("1,23x", "1,2x"),
    ("P/B HIỆN TẠI", "P/B DỰ PHÓNG"),
    ("Thấp hơn ~8% so với trung bình 5 năm", "Trên giá trị sổ sách dự phóng năm 2026"),
    ("15,2%", "38%"),
    ("CAR Q1/26", "CASA 2025"),
    ("Thuộc nhóm cao nhất khối ngân hàng tư nhân", "Tỷ lệ tiền gửi không kỳ hạn cao nhất hệ thống"),
    ("+60%", "+18,8%"),
    ("CỔ PHIẾU THƯỞNG", "LNTT 2026F"),
    ("Vốn điều lệ dự kiến tăng lên 113.738 tỷ đồng", "Lợi nhuận trước thuế dự phóng 40.726 tỷ đồng"),
    ("Định giá &amp; nền tảng vốn", "Định giá &amp; sinh lời"),
],
3: [
    ("Định giá hấp dẫn, nền tảng vốn vững chắc", "Định giá hợp lý trên nền sinh lời đầu ngành"),
    ("Techcombank", "Ngân hàng MB"),
    ("HOSE · TCB", "HOSE · MBB"),
    ("Ngân hàng trở lại quỹ đạo tăng trưởng ", "Quy mô tài sản và vốn tăng tốc "),
],
4: [
    ("Động lực phục hồi từ mảng kinh doanh cốt lõi", "Lợi thế vốn rẻ và dư địa tín dụng vượt trội"),
    ("Các mảng từng chịu áp lực 2022–2023 đang bước vào chu kỳ hồi phục khi thị trường vốn cải thiện.",
     "CASA dẫn đầu hệ thống giúp MBB giữ chi phí vốn thấp nhất trong khi tín dụng tăng tốc."),
    ("TCBS", "CASA"),
    ("dẫn dắt", "số một"),
    ("CHỨNG KHOÁN &amp; IB", "VỐN RẺ &amp; NIM"),
    ("Lợi nhuận hàng đầu ngành, dẫn đầu tư vấn phát hành trái phiếu doanh nghiệp",
     "CASA ~38% cuối 2025, cao nhất hệ thống, số dư tăng ~27% so với cùng kỳ"),
    ("Dòng vốn", "Tín dụng"),
    ("ngoại", "bứt tốc"),
    ("NÂNG HẠNG FTSE", "CHUYỂN GIAO MBV"),
    ("Kỳ vọng nâng hạng thúc đẩy vốn ngoại; môi giới &amp; margin hồi phục",
     "Hạn mức tăng trưởng tín dụng nhóm cao nhất giai đoạn 2026–2028"),
    ("Chu kỳ", "ROE"),
    ("hồi phục", "21,1%"),
    ("TPDN · CHỨNG KHOÁN · BĐS", "SINH LỜI · HIỆU QUẢ VỐN"),
    ("Các mảng từng chịu áp lực 2022–2023 đảo chiều", "ROE 2025 thuộc nhóm cao nhất khối ngân hàng lớn"),
    ("Động lực phục hồi", "Lợi thế cạnh tranh"),
],
5: [
    ("Động lực phục hồi từ mảng kinh doanh cốt lõi", "Lợi thế vốn rẻ và dư địa tín dụng vượt trội"),
    ("Các mảng từng chịu áp lực 2022–2023 đang bước vào chu kỳ hồi phục khi thị trường vốn cải thiện.",
     "Lợi nhuận trước thuế nối dài chuỗi tăng trưởng, dự phóng vượt 40.000 tỷ đồng trong năm 2026."),
],
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
     "MBB đang được định giá đúng, hay thị trường chưa trả đủ cho ngân hàng có chi phí vốn rẻ nhất? P/B dự phóng 2026 ~1,2x đi cùng ROE trên 21%.")],
2: [("P/B forward ~1,15x, thấp hơn ~15% trung bình 5 năm. CAR 15,2% thuộc nhóm cao nhất khối tư nhân. Cổ phiếu thưởng 60% đưa vốn điều lệ lên 113.738 tỷ.",
     "P/B dự phóng 2026 ~1,2x trên ROE trên 21%. CASA ~38% cuối 2025, cao nhất hệ thống. LNTT 2026 dự phóng 40.726 tỷ, tăng 18,8% so với cùng kỳ.")],
3: [("P/B forward ~1,15x, thấp hơn ~15% trung bình 5 năm. CAR 15,2% thuộc nhóm cao nhất khối tư nhân. Cổ phiếu thưởng 60% đưa vốn điều lệ lên 113.738 tỷ.",
     "Tổng tài sản tăng từ 728.532 tỷ (2022) lên 1.615.764 tỷ cuối 2025, tăng 43%. Mục tiêu vượt 2,1 triệu tỷ năm 2026, vốn điều lệ lên tối đa 102.687 tỷ.")],
4: [("Trái phiếu DN, chứng khoán, BĐS bước vào chu kỳ hồi phục. TCBS dẫn đầu lợi nhuận CTCK và tư vấn phát hành TPDN. Kỳ vọng nâng hạng FTSE thúc đẩy dòng vốn ngoại.",
     "CASA ~38% cuối 2025, dẫn đầu hệ thống. Nhận chuyển giao MBV nên được giao room tín dụng nhóm cao nhất 2026-2028, mục tiêu 30-35%. ROE 2025 đạt 21,1%.")],
5: [("Trái phiếu DN, chứng khoán, BĐS bước vào chu kỳ hồi phục. TCBS dẫn đầu lợi nhuận CTCK và tư vấn phát hành TPDN. Kỳ vọng nâng hạng FTSE thúc đẩy dòng vốn ngoại.",
     "LNTT tăng liên tục: 22.729 tỷ (2022), 26.306 tỷ (2023), 28.829 tỷ (2024), 34.268 tỷ (2025) và dự phóng 40.726 tỷ cho năm 2026.")],
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
# Charts
# --------------------------------------------------------------------------- #
YEARS = ["2022", "2023", "2024", "2025", "2026F"]

# ref fragment -> replacement values (chart1)
CHART1_VALUES = {
    "$U$78:$Z$78": [79613, 96711, 118356, 144549, 175134],          # vốn chủ sở hữu
    "$U$15:$Z$15": [728532, 944954, 1133797, 1615764, 2100000],     # tổng tài sản
    "$U$80:$Z$80": [45340, 52141, 53063, 80550, 102687],            # vốn điều lệ (hidden series)
    "$U$81:$Z$81": [0.274, 0.215, 0.224, 0.221, 0.212],             # tăng trưởng VCSH
}
CHART2_PBT = [22729, 26306, 28829, 34268, 40726]                     # lợi nhuận trước thuế


def year_cache(n):
    pts = "".join(f'<c:pt idx="{i}"><c:v>{y}</c:v></c:pt>' for i, y in enumerate(YEARS))
    return f'<c:ptCount val="{len(YEARS)}"/>{pts}'


def num_cache(fmt, values):
    pts = "".join(f'<c:pt idx="{i}"><c:v>{v}</c:v></c:pt>' for i, v in enumerate(values))
    return f"<c:formatCode>{fmt}</c:formatCode><c:ptCount val=\"{len(values)}\"/>{pts}"


def retarget_categories(xml):
    """Rewrite every cached category list of years to the new 5-year axis."""
    def repl(m):
        inner = m.group(1)
        if not re.search(r"<c:v>20\d\d</c:v>", inner):
            return m.group(0)
        return f"<c:strCache>{year_cache(len(YEARS))}</c:strCache>"
    return re.sub(r"<c:strCache>(.*?)</c:strCache>", repl, xml, flags=re.S)


def set_series_values(xml, ref_fragment, values, fmt):
    """Replace the numCache that follows the given spreadsheet reference."""
    pat = re.compile(
        r"(" + re.escape(ref_fragment) + r".*?<c:numCache>)(.*?)(</c:numCache>)", re.S)
    xml, n = pat.subn(lambda m: m.group(1) + num_cache(fmt, values) + m.group(3), xml, count=1)
    if n != 1:
        sys.exit(f"chart: reference not found once: {ref_fragment}")
    return xml


def build_chart1(path):
    xml = open(path, encoding="utf-8").read()
    xml = retarget_categories(xml)
    for ref, vals in CHART1_VALUES.items():
        fmt = "0.0%" if ref == "$U$81:$Z$81" else "#,##0.00"
        xml = set_series_values(xml, ref, vals, fmt)
    xml = xml.replace("<c:v>Tăng trưởng VCSH (%)</c:v>", "<c:v>Tăng trưởng VCSH (%)</c:v>")
    open(path, "w", encoding="utf-8").write(xml)


def build_chart2(path):
    xml = open(path, encoding="utf-8").read()
    # keep only the "Thu nhập lãi thuần" series slot; re-label it as pre-tax profit
    keep = "'Kết quả kinh doanh'!$A$15"
    sers = list(re.finditer(r"<c:ser>.*?</c:ser>", xml, re.S))
    assert len(sers) == 5, len(sers)
    for m in reversed(sers):
        if keep not in m.group(0):
            xml = xml[:m.start()] + xml[m.end():]
    assert xml.count("<c:ser>") == 1, xml.count("<c:ser>")
    xml = xml.replace('<c:grouping val="stacked"/>', '<c:grouping val="clustered"/>')
    xml = xml.replace("<c:v>Thu nhập lãi thuần</c:v>", "<c:v>Lợi nhuận trước thuế</c:v>")
    xml = xml.replace('<c:showVal val="0"/>', '<c:showVal val="1"/>')   # surface the numbers
    xml = retarget_categories(xml)
    xml = set_series_values(xml, "$U$15:$Y$15", CHART2_PBT, "#,##0.00")
    open(path, "w", encoding="utf-8").write(xml)


# --------------------------------------------------------------------------- #
def main():
    for i, edits in SLIDE_EDITS.items():
        apply_edits(f"{SRC}/ppt/slides/slide{i}.xml", edits)
    for i, edits in NOTES_EDITS.items():
        apply_edits(f"{SRC}/ppt/notesSlides/notesSlide{i}.xml", edits)

    # brand accent: Techcombank red -> MB Bank blue
    swapped = 0
    for i in range(1, 7):
        p = f"{SRC}/ppt/slides/slide{i}.xml"
        x = open(p, encoding="utf-8").read()
        swapped += x.count(TCB_RED)
        open(p, "w", encoding="utf-8").write(x.replace(TCB_RED, MB_BLUE))
    print(f"recoloured {swapped} brand-accent references")

    build_chart1(f"{SRC}/ppt/charts/chart1.xml")
    build_chart2(f"{SRC}/ppt/charts/chart2.xml")

    # document properties
    p = f"{SRC}/docProps/core.xml"
    x = open(p, encoding="utf-8").read()
    x = x.replace("<dc:title>PptxGenJS Presentation</dc:title>",
                  "<dc:title>HotStock · MBB · Ngân hàng MB</dc:title>")
    x = x.replace("<dc:subject>PptxGenJS Presentation</dc:subject>",
                  "<dc:subject>Equity Research · Vietnam Banks</dc:subject>")
    open(p, "w", encoding="utf-8").write(x)

    # leftover check
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
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


main()
