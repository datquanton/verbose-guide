# -*- coding: utf-8 -*-
"""STB + FPT mobile report, EN and VN in one deck.

Built on the MBB mobile template (portrait 28.57 x 38.10 cm, 5 slides).  Its
five slides are duplicated three times so the file carries four blocks -
STB EN, STB VN, FPT EN, FPT VN - and then the text, tables and figures are
replaced block by block.  The English template is used for the Vietnamese
blocks too: the layouts are identical, only the wording differs.

Slide duplication copies each source relationship into the new slide and then
rewrites the r:id / r:embed references inside the copied shape XML, because
python-pptx assigns its own rIds and the shapes would otherwise point at
nothing.  The SmartArt on slide 1 and the charts on slides 2-3 are dropped and
replaced with text and PNGs, which keeps the deck editable without dragging
four diagram parts and two chart workbooks along.
"""
import copy
from pptx import Presentation
from pptx.util import Emu, Pt

SRC = ('/root/.claude/uploads/041665b7-4ff3-507f-a1e8-7a7ed4160156/'
       'ad4f5d0b-Mobile_Report_MBB_1Q26_EN.pptx')
OUT = '/home/user/verbose-guide/MASVN_Mobile_Report_STB_FPT_2Q26_EN_VN.pptx'
R = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'
NAVY, AMBER = '01437C', 'F38120'

DATE = '05.08.2026'
BLOCKS = [
 dict(tick='stb', lang='en', sector='Banks',
      name='Sacombank\n(HOSE: STB)',
      head='Clean-up funded from the reserve stock, not the P&L',
      tp='81,400', ret='+10.0%', tplab='Target price',
      t1='STB — 2Q26 in brief', t2='STB — I/S performance', t3='STB — Valuation',
      t4='Estimates',
      sub2='FY26F: PBT +6.9%, CIR 40.0%, NPL 5.5%',
      sub3='P/E and P/B struck on the VND81,400 target price',
      points=[
        ('1H26 PBT VND4,136bn (-43.6% YoY)',
         '51% of the VND8,100bn plan. NIM compression and a heavier provisioning '
         'charge did the damage.'),
        ('NPL 7.54% at end-2Q26, the highest in the system',
         'Up 1.13%p YTD. Group 3-5 rose ~VND7,800bn to VND47,957bn, two-thirds of it '
         'Group 5.'),
        ('We set FY26F NPL at 5.5%, coverage at 51%',
         'Reserves of VND27.2tn at end-2Q26 fund VND11.8tn of 2H26 write-offs — 37% of '
         'the Group 5 balance. The reserve stock does the work, not the P&L.'),
        ('FY26F PBT VND8,143bn (+6.9% YoY), marginally above plan',
         'On CIR of 40.0% against 42.9% carried before; 1H26 came in at 35.6%.'),
        ('HOLD, target price VND81,400',
         'Loan growth of 1.5% in 1H26 against 11.7% carried for the year is the next '
         'assumption to re-cut.')],
      rows=[('NII (VNDbn)', ['26,681', '26,704', '29,545', '34,079']),
            ('Non-II (VNDbn)', ['5,376', '5,950', '7,382', '8,779']),
            ('Operating profit (VNDbn)', ['7,628', '8,143', '12,293', '20,064']),
            ('NP (VNDbn)', ['5,939', '6,340', '9,572', '15,622']),
            ('EPS (VND)', ['2,883', '3,077', '4,646', '7,583']),
            ('ROE (%)', ['10.3', '9.6', '13.5', '18.7']),
            ('P/E (x)', ['28.2', '26.5', '17.5', '10.7']),
            ('P/B (x)', ['2.8', '2.5', '2.2', '1.8'])]),
 dict(tick='stb', lang='vn', sector='Ngân hàng',
      name='Sacombank\n(HOSE: STB)',
      head='Xử lý nợ xấu bằng nguồn dự phòng đã trích, không bằng lợi nhuận',
      tp='81,400', ret='+10.0%', tplab='Giá mục tiêu',
      t1='STB — Tóm tắt Q2/2026', t2='STB — Kết quả kinh doanh',
      t3='STB — Định giá', t4='Dự phóng',
      sub2='FY26F: LNTT +6.9%, CIR 40.0%, nợ xấu 5.5%',
      sub3='P/E và P/B tính theo giá mục tiêu 81,400 đồng',
      points=[
        ('LNTT 1H26 đạt 4,136 tỷ đồng (-43.6% CK)',
         'Hoàn thành 51% kế hoạch 8,100 tỷ đồng. NIM thu hẹp và chi phí dự phòng tăng '
         'mạnh là hai nguyên nhân chính.'),
        ('Nợ xấu 7.54% cuối Q2/2026, cao nhất hệ thống',
         'Tăng 1.13%p so với đầu năm. Nợ nhóm 3-5 tăng khoảng 7,800 tỷ đồng lên 47,957 '
         'tỷ đồng, hai phần ba là nhóm 5.'),
        ('Đặt giả định nợ xấu FY26F ở 5.5%, bao phủ 51%',
         'Dự phòng 27.2 nghìn tỷ đồng cuối Q2/2026 đủ để xóa 11.8 nghìn tỷ đồng trong '
         '2H26 — tương đương 37% dư nợ nhóm 5. Nguồn dự phòng gánh phần lớn, không '
         'phải lợi nhuận.'),
        ('LNTT FY26F 8,143 tỷ đồng (+6.9% CK), nhỉnh hơn kế hoạch',
         'Trên giả định CIR 40.0% so với 42.9% dự phóng trước đây; CIR 1H26 thực tế '
         'chỉ 35.6%.'),
        ('NẮM GIỮ, giá mục tiêu 81,400 đồng',
         'Tăng trưởng tín dụng 1H26 chỉ 1.5% so với 11.7% dự phóng cả năm — đây là giả '
         'định cần điều chỉnh tiếp theo.')],
      rows=[('Thu nhập lãi thuần (tỷ đồng)', ['26,681', '26,704', '29,545', '34,079']),
            ('Thu nhập ngoài lãi (tỷ đồng)', ['5,376', '5,950', '7,382', '8,779']),
            ('LNHĐ (tỷ đồng)', ['7,628', '8,143', '12,293', '20,064']),
            ('LNST (tỷ đồng)', ['5,939', '6,340', '9,572', '15,622']),
            ('EPS (đồng)', ['2,883', '3,077', '4,646', '7,583']),
            ('ROE (%)', ['10.3', '9.6', '13.5', '18.7']),
            ('P/E (lần)', ['28.2', '26.5', '17.5', '10.7']),
            ('P/B (lần)', ['2.8', '2.5', '2.2', '1.8'])]),
 dict(tick='fpt', lang='en', sector='IT',
      name='FPT Corporation\n(HOSE: FPT)',
      head='Growth held, and the AI line started paying',
      tp='87,950', ret='+22.7%', tplab='Target price',
      t1='FPT — 2Q26 in brief', t2='FPT — I/S performance', t3='FPT — Valuation',
      t4='Estimates',
      sub2='FY26F: NPATMI +15.6%, PBT margin 22.8%',
      sub3='P/E and P/B struck on the VND87,950 target price',
      points=[
        ('1H26 revenue +12.6%, PBT +18.1% on the restated base',
         'Group PBT margin widened to 21.8% from 20.7%. 2Q26 revenue VND13,789bn and '
         'PBT VND2,910bn.'),
        ('AI revenue grew 55%, to 8.0% of Technology',
         'VND1,842bn in 1H26 against +15% for Technology overall. Both AI Factories ran '
         'above 90% utilisation and turned profitable in 2Q26.'),
        ('Signed contract value +32.3%, book-to-bill 1.39x',
         'VND26,338bn for Global IT including 14 deals above USD10mn, against 1.07-1.22x '
         'through FY21-25.'),
        ('Domestic IT the fastest-growing line, +22.5%',
         'Segment PBT doubled to VND308bn on national digital-transformation awards, '
         'though its 7.3% margin dilutes the blend.'),
        ('BUY, target price VND87,950',
         'FY26F NPATMI VND10,944bn (+15.6%). At VND71,700 the stock trades at 11.2x '
         'FY26F against a five-year median above 18x.')],
      rows=[('Revenue (VNDbn)', ['70,208', '57,284', '66,048', '76,654']),
            ('Operating profit (VNDbn)', ['11,079', '9,807', '11,044', '13,053']),
            ('PBT (VNDbn)', ['13,134', '13,070', '15,159', '17,671']),
            ('NPATMI (VNDbn)', ['9,464', '10,944', '12,674', '14,774']),
            ('EPS (VND)', ['5,073', '6,424', '7,440', '8,673']),
            ('ROE (%)', ['28.6', '27.6', '27.1', '26.5']),
            ('P/E (x)', ['17.3', '13.7', '11.8', '10.1']),
            ('P/B (x)', ['4.3', '3.5', '3.0', '2.5'])]),
 dict(tick='fpt', lang='vn', sector='Công nghệ',
      name='CTCP FPT\n(HOSE: FPT)',
      head='Tăng trưởng bền bỉ, mảng AI bắt đầu có lãi',
      tp='87,950', ret='+22.7%', tplab='Giá mục tiêu',
      t1='FPT — Tóm tắt Q2/2026', t2='FPT — Kết quả kinh doanh',
      t3='FPT — Định giá', t4='Dự phóng',
      sub2='FY26F: LNST-CĐTS +15.6%, biên LNTT 22.8%',
      sub3='P/E và P/B tính theo giá mục tiêu 87,950 đồng',
      points=[
        ('Doanh thu 1H26 +12.6%, LNTT +18.1% trên nền tính lại',
         'Biên LNTT tập đoàn mở rộng lên 21.8% từ 20.7%. Q2/2026 doanh thu 13,789 tỷ '
         'đồng và LNTT 2,910 tỷ đồng.'),
        ('Doanh thu AI tăng 55%, chiếm 8.0% mảng Công nghệ',
         'Đạt 1,842 tỷ đồng trong 1H26 so với +15% của cả mảng. Hai cụm AI Factory đạt '
         'hiệu suất trên 90% và có lãi từ Q2/2026.'),
        ('Doanh thu ký mới +32.3%, tỷ lệ ký mới/doanh thu 1.39 lần',
         'Đạt 26,338 tỷ đồng cho CNTT nước ngoài, gồm 14 dự án trên 10 triệu USD, so '
         'với 1.07-1.22 lần giai đoạn FY21-25.'),
        ('CNTT trong nước tăng nhanh nhất, +22.5%',
         'LNTT mảng tăng gấp đôi lên 308 tỷ đồng nhờ trúng thầu chuyển đổi số quốc gia, '
         'tuy biên 7.3% làm loãng biên chung.'),
        ('MUA, giá mục tiêu 87,950 đồng',
         'LNST-CĐTS FY26F 10,944 tỷ đồng (+15.6%). Tại 71,700 đồng, cổ phiếu giao dịch '
         'ở 11.2x P/E FY26F so với trung vị 5 năm trên 18x.')],
      rows=[('Doanh thu (tỷ đồng)', ['70,208', '57,284', '66,048', '76,654']),
            ('LNHĐ (tỷ đồng)', ['11,079', '9,807', '11,044', '13,053']),
            ('LNTT (tỷ đồng)', ['13,134', '13,070', '15,159', '17,671']),
            ('LNST-CĐTS (tỷ đồng)', ['9,464', '10,944', '12,674', '14,774']),
            ('EPS (đồng)', ['5,073', '6,424', '7,440', '8,673']),
            ('ROE (%)', ['28.6', '27.6', '27.1', '26.5']),
            ('P/E (lần)', ['17.3', '13.7', '11.8', '10.1']),
            ('P/B (lần)', ['4.3', '3.5', '3.0', '2.5'])]),
]
COLS = ['FY25', 'FY26F', 'FY27F', 'FY28F']


def dup(prs, slide):
    """Copy a slide, carrying its parts over and remapping the rIds."""
    new = prs.slides.add_slide(slide.slide_layout)
    for shp in list(new.shapes):
        shp._element.getparent().remove(shp._element)
    remap = {}
    for rid, rel in slide.part.rels.items():
        if rel.reltype.endswith('slideLayout'):
            continue
        remap[rid] = new.part.rels.get_or_add(rel.reltype, rel._target)
    for shp in slide.shapes:
        el = copy.deepcopy(shp._element)
        for node in el.iter():
            for attr, val in list(node.attrib.items()):
                if attr.startswith(R) and val in remap:
                    node.set(attr, remap[val])
        new.shapes._spTree.append(el)
    return new


def sid(slide, i):
    return next(s for s in slide.shapes if s.shape_id == i)


def put(tf, lines):
    """Write lines into a text frame, keeping the first run's formatting."""
    paras = tf.paragraphs
    for i, txt in enumerate(lines):
        if i < len(paras):
            p = paras[i]
        else:
            p = tf.add_paragraph()
            p._pPr = copy.deepcopy(paras[0]._pPr) if paras[0]._pPr is not None else None
        if not p.runs:
            r = copy.deepcopy(paras[0].runs[0]._r)
            p._p.append(r)
        p.runs[0].text = txt
        for r in p.runs[1:]:
            r.text = ''
    for p in paras[len(lines):]:
        for r in p.runs:
            r.text = ''


def swap_for_png(slide, shape_id, png):
    sh = sid(slide, shape_id)
    l, t, w, h = sh.left, sh.top, sh.width, sh.height
    sh._element.getparent().remove(sh._element)
    # keep the aspect ratio of the PNG inside the old frame
    from PIL import Image
    iw, ih = Image.open(png).size
    scale = min(w / iw, h / ih)
    nw, nh = int(iw * scale), int(ih * scale)
    slide.shapes.add_picture(png, l + (w - nw) // 2, t + (h - nh) // 2, nw, nh)


def fill_table(tbl, rows, cols):
    for ci, c in enumerate(cols):
        put(tbl.cell(0, ci + 1).text_frame, [c])
    for ri, (label, vals) in enumerate(rows):
        put(tbl.cell(ri + 1, 0).text_frame, [label])
        for ci, v in enumerate(vals):
            put(tbl.cell(ri + 1, ci + 1).text_frame, [v])


def main():
    prs = Presentation(SRC)
    base = list(prs.slides)[:5]
    for _ in range(3):
        for s in base:
            dup(prs, s)
    for bi, b in enumerate(BLOCKS):
        sl = [prs.slides[bi * 5 + k] for k in range(5)]
        # cover
        put(sid(sl[0], 6).text_frame, [b['sector']])
        put(sid(sl[0], 7).text_frame, [DATE])
        put(sid(sl[0], 2).text_frame, b['name'].split('\n'))
        put(sid(sl[0], 4).text_frame, [b['head']])
        t = sid(sl[0], 12).table
        put(t.cell(0, 0).text_frame, [b['tplab']])
        put(t.cell(1, 0).text_frame, [b['tp']])
        put(t.cell(1, 1).text_frame, [b['ret']])
        # key points - the SmartArt is dropped and rebuilt as text
        put(sid(sl[1], 9).text_frame, [b['t1']])
        d = sid(sl[1], 7)
        l, tp_, w, h = d.left, d.top, d.width, d.height
        d._element.getparent().remove(d._element)
        box = sl[1].shapes.add_textbox(l, tp_, w, h)
        tf = box.text_frame
        tf.word_wrap = True
        first = True
        for head, body in b['points']:
            p = tf.paragraphs[0] if first else tf.add_paragraph()
            first = False
            r = p.add_run(); r.text = head
            r.font.size = Pt(23); r.font.bold = True; r.font.name = 'SVN-Gilroy XBold'
            r.font.color.rgb = __import__('pptx.dml.color', fromlist=['RGBColor']).RGBColor.from_string(AMBER)
            p.space_after = Pt(4)
            q = tf.add_paragraph()
            r2 = q.add_run(); r2.text = body
            r2.font.size = Pt(19); r2.font.name = 'SVN-Gilroy'
            r2.font.color.rgb = __import__('pptx.dml.color', fromlist=['RGBColor']).RGBColor.from_string(NAVY)
            q.space_after = Pt(18)
        # income statement
        put(sid(sl[2], 9).text_frame, [b['t2']])
        put(sid(sl[2], 3).text_frame, [b['sub2']])
        swap_for_png(sl[2], 7, '/home/user/verbose-guide/m_%s_is_%s.png' % (b['tick'], b['lang']))
        # valuation
        put(sid(sl[3], 9).text_frame, [b['t3']])
        put(sid(sl[3], 3).text_frame, [b['sub3']])
        put(sid(sl[3], 7).text_frame, ['Source: Company data, Mirae Asset Vietnam Research'])
        swap_for_png(sl[3], 2, '/home/user/verbose-guide/m_%s_val_%s.png' % (b['tick'], b['lang']))
        # estimates
        put(sid(sl[4], 11).text_frame, [b['t4']])
        fill_table(sid(sl[4], 2).table, b['rows'], COLS)
    prs.save(OUT)
    print('wrote %s  (%d slides)' % (OUT, len(prs.slides)))


if __name__ == '__main__':
    main()
