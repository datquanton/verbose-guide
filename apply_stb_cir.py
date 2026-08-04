# -*- coding: utf-8 -*-
"""Push the 5.5%-NPL / ~40%-CIR cascade from fix_stb_model.py onto the STB slides.

FY table columns 4/5/6 = FY26F/FY27F/FY28F.  P/E and P/B in that table are
computed on the TARGET price (77,800), not the current price - that is how the
existing rows were built and it is left alone here.
"""
import shutil
from pptx import Presentation

DECK = '/home/user/verbose-guide/MASVN_RS_WM_2H26_outlook_Equity_VN_2026_STBFPT_31July2026.pptx'
SHARES = 2060.158          # Model!X87 paid-in capital / VND10,000 par
TP = 77800.0

# straight from fix_stb_model.cascade()
from fix_stb_model import cascade
_C = cascade()
PBT = tuple(c['pbt'] for c in _C)
NPATMI = tuple(c['npatmi'] for c in _C)
EQ25 = 59920.157                          # Model!Y87+Y94+X98, ex the FY25 FX line
EQUITY = tuple(EQ25 + sum(NPATMI[:i + 1]) for i in range(3))
ASSETS = (1014277, 1129957, 1271622)      # Model!Y61, Excel-recalculated
# Model row 314: FY26F on ending equity, FY27-28F on average - the model's own quirk
ROE = (NPATMI[0] / EQUITY[0] * 100,
       NPATMI[1] / ((EQUITY[0] + EQUITY[1]) / 2) * 100,
       NPATMI[2] / ((EQUITY[1] + EQUITY[2]) / 2) * 100)

EPS = tuple(n * 1000 / SHARES for n in NPATMI)
BVPS = tuple(e * 1000 / SHARES for e in EQUITY)
PE = tuple(TP / e for e in EPS)
PB = tuple(TP / b for b in BVPS)

NII = (26712.4, 29560.5, 34095.0)         # Model!Y121, Excel-recalculated
NONII = tuple(c['toi'] for c in _C)       # non-interest income = TOI - NII
NONII = tuple(t - n for t, n in zip(NONII, NII))

TABLE = {                                  # row -> formatted FY26F/27F/28F
    1: ['{:,.0f}'.format(v) for v in NII],
    2: ['{:,.0f}'.format(v) for v in NONII],
    3: ['{:,.0f}'.format(v) for v in PBT],
    4: ['{:,.0f}'.format(v) for v in NPATMI],
    5: ['{:,.0f}'.format(v) for v in EPS],
    6: ['{:.1f}'.format(v) for v in ROE],
    7: ['{:.1f}'.format(v) for v in PE],
    8: ['{:.1f}'.format(v) for v in PB],
    9: ['{:,.0f}'.format(v) for v in ASSETS],
    10: ['{:,.0f}'.format(v) for v in EQUITY],
    11: ['{:,.0f}'.format(v) for v in BVPS],
}

EPS_GROWTH = EPS[0] / (5939.111 * 1000 / SHARES) - 1
BOX = {0: '{:,.0f}'.format(NPATMI[0]),
       2: '{:.1f}'.format(EPS_GROWTH * 100),
       3: '{:.1f}'.format(PE[0])}

EN = {
 5: 'FY26F PBT lifted on the cost line, against a low 2H25 base: ',
 4: ("The NPL ratio reached 7.54% at end-2Q26, up 1.13%p from the beginning of the year and the "
     "highest in the system, against management guidance of approximately 5.6%. Group 3-5 "
     "balances rose approximately VND7,800bn year-to-date to VND47,957bn, of which around 67% "
     "(approximately VND32,000bn) is Group 5, while Group 4 more than doubled (+156%). We set "
     "FY26F NPL at 5.5%, from below 4.5%, and FY27F at 4.0% from 3.1%. The clean-up is funded "
     "from the reserve stock rather than the P&L: reserves reached VND27.2tn at end-2Q26 — 56.7% "
     "coverage, up from 50.0% at end-FY25 — after VND7.1tn of 1H26 charges and almost no "
     "write-offs. A further VND4.0tn charge in 2H26 funds write-offs of VND11.8tn, or 37% of the "
     "Group 5 balance, leaving reserves at VND19.0tn and coverage back at 50.0%. Holding coverage "
     "at 50% is what caps the improvement at 5.5%, and it also requires 2H26 NPL formation to "
     "slow to roughly a quarter of the 1H26 pace. The former 4.5% assumption needed some VND18tn "
     "of write-offs the reserve stock cannot support."),
 6: ("STB recorded VND7,331bn of PBT in 1H25 but only VND297bn in 2H25, as 4Q25 registered a "
     "pre-tax loss of approximately VND3,360bn on a provisioning charge of around VND9,232bn. We "
     "raise FY26F PBT to VND8,683bn (+13.8% YoY) from VND7,934bn, entirely on the cost line: 1H26 "
     "CIR came in at 35.6% against the 42.9% previously carried for the full year, and we now "
     "assume 40.0% (-0.7%p YoY), easing to 38.0% in FY27F and 36.0% in FY28F. That still allows "
     "2H26 operating expense to run 11.5% above 1H26, and implies 2H26 PBT of approximately "
     "VND4,547bn — around 15x the 2H25 base and 9.9% above the 1H26 level. Other FY26F "
     "assumptions: NII of VND27,010bn (+1.2% YoY), NIM of "
     "2.94% (-38bps YoY) and a provisioning charge of VND11.1tn (-2.6% YoY); we flag that 1H26 "
     "loan growth of 1.5% sits well below the 11.7% carried for the full year. Separately, STB "
     "has taken possession of 507 land-use right certificates at LDG's Viva City project in Dong "
     "Nai against overdue principal of nearly VND350bn; the exposure is immaterial to the "
     "portfolio but illustrates the collateral-resolution channel the 2H26 write-off programme "
     "depends on."),
}

VN = {
 4: 'Nâng dự phóng LNTT FY26F nhờ chi phí hoạt động, trên nền 2H25 thấp: ',
 3: ("Chất lượng tài sản suy giảm vượt mức ban lãnh đạo dự kiến: tỷ lệ nợ xấu đạt 7.54% cuối "
     "Q2/2026, tăng 1.13%p so với đầu năm và cao nhất hệ thống, so với ước tính khoảng 5.6% của "
     "ban lãnh đạo. Dư nợ nhóm 3-5 tăng khoảng 7,800 tỷ đồng so với đầu năm, lên 47,957 tỷ đồng, "
     "trong đó khoảng 67% (32,000 tỷ đồng) xếp nhóm 5, nợ nhóm 4 tăng hơn gấp đôi (+156%). Chúng "
     "tôi đặt giả định nợ xấu FY26F ở 5.5% (từ dưới 4.5%) và FY27F ở 4.0% (từ 3.1%). Quá trình xử "
     "lý được tài trợ từ nguồn dự phòng đã trích, không phải từ lợi nhuận: dự phòng đạt 27.2 "
     "nghìn tỷ đồng cuối Q2/2026 — bao phủ 56.7%, tăng từ 50.0% cuối 2025 — sau khi trích 7.1 "
     "nghìn tỷ đồng trong 1H26 và gần như chưa xóa nợ. Trích thêm 4.0 nghìn tỷ đồng trong 2H26 đủ "
     "để xóa 11.8 nghìn tỷ đồng, tương đương 37% dư nợ nhóm 5, đưa dự phòng còn 19.0 nghìn tỷ "
     "đồng và bao phủ về 50.0%. Chính việc giữ bao phủ ở 50% giới hạn mức cải thiện ở 5.5%, đồng "
     "thời cần nợ xấu phát sinh mới trong 2H26 chậm lại còn khoảng một phần tư nhịp 1H26. Giả "
     "định 4.5% trước đây cần tới khoảng 18 nghìn tỷ đồng xóa nợ, vượt quá nguồn dự phòng hiện "
     "có."),
 5: ("STB ghi nhận 7,331 tỷ đồng LNTT trong 1H25 nhưng chỉ 297 tỷ đồng trong 2H25, do Q4/2025 lỗ "
     "trước thuế khoảng 3,360 tỷ đồng với chi phí dự phòng khoảng 9,232 tỷ đồng. Chúng tôi nâng "
     "dự phóng LNTT FY26F lên 8,683 tỷ đồng (+13.8% CK) từ 7,934 tỷ đồng, hoàn toàn nhờ chi phí "
     "hoạt động: CIR 1H26 chỉ 35.6% so với 42.9% dự phóng cả năm trước đây, và chúng tôi điều "
     "chỉnh về 40.0% (-0.7%p CK), giảm dần về 38.0% năm FY27F và 36.0% năm FY28F. Mức này vẫn "
     "cho phép chi phí hoạt động 2H26 cao hơn 1H26 11.5%, và hàm ý LNTT 2H26 khoảng 4,547 tỷ "
     "đồng — tương đương khoảng 15 lần nền 2H25 và cao hơn 1H26 9.9%."),
 6: ("Các giả định FY26F khác: NII 27,010 tỷ đồng (+1.2% CK), NIM 2.94% (-38bps CK) và chi phí dự "
     "phòng 11.1 nghìn tỷ đồng (-2.6% CK); lưu ý tăng trưởng tín dụng 1H26 chỉ đạt 1.5%, thấp hơn "
     "nhiều so với mức 11.7% dự phóng cả năm. Ở diễn biến khác, Sacombank đã thu giữ 507 giấy "
     "chứng nhận quyền sử dụng đất thuộc dự án Viva City (Đồng Nai) đối với dư nợ gốc quá hạn gần "
     "350 tỷ đồng; quy mô chưa trọng yếu nhưng thể hiện kênh xử lý tài sản đảm bảo mà đà hồi phục "
     "2H26 phụ thuộc vào."),
}


def put(para, txt):
    """Write txt into a paragraph without disturbing its run formatting."""
    assert para.runs, 'no runs to inherit formatting from'
    para.runs[0].text = txt
    for r in para.runs[1:]:
        r.text = ''


def cell(c, txt):
    put(c.text_frame.paragraphs[0], txt)


def main():
    shutil.copy(DECK, DECK + '.bak')
    prs = Presentation(DECK)
    sid = lambda sl, i: next(s for s in sl.shapes if s.shape_id == i)
    for slide_i, spec in ((0, EN), (1, VN)):
        sl = prs.slides[slide_i]
        tf = sid(sl, 15).text_frame
        for pi, txt in spec.items():
            put(tf.paragraphs[pi], txt)
        tbl = sid(sl, 16).table
        for ri, vals in TABLE.items():
            for off, v in enumerate(vals):
                cell(tbl.rows[ri].cells[4 + off], v)
        box = sid(sl, 12).table
        for ri, v in BOX.items():
            cell(box.rows[ri].cells[1], v)
    prs.save(DECK)


if __name__ == '__main__':
    main()
    print('%-22s %10s %10s %10s' % ('', 'FY26F', 'FY27F', 'FY28F'))
    for lab, vs, f in [('PBT (VNDbn)', PBT, '{:,.0f}'), ('NPATMI (VNDbn)', NPATMI, '{:,.0f}'),
                       ('EPS (VND)', EPS, '{:,.0f}'), ('ROE (%)', ROE, '{:.1f}'),
                       ('P/E (x, on TP)', PE, '{:.1f}'), ('P/B (x, on TP)', PB, '{:.1f}'),
                       ('Total assets (VNDbn)', ASSETS, '{:,.0f}'),
                       ('Equity (VNDbn)', EQUITY, '{:,.0f}'), ('BVPS (VND)', BVPS, '{:,.0f}')]:
        print(('%-22s' % lab) + ''.join('%10s' % f.format(v) for v in vs))
    print('\nEPS growth 26F: %+.1f%%' % (EPS_GROWTH * 100))
    prs = Presentation(DECK)
    sid = lambda sl, i: next(s for s in sl.shapes if s.shape_id == i)
    for i, nm in enumerate(('STB EN', 'STB VN')):
        tf = sid(prs.slides[i], 15).text_frame
        print('%-8s %d words' % (nm, sum(len(p.text.split()) for p in tf.paragraphs)))
