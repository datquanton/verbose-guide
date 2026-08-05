# -*- coding: utf-8 -*-
"""Put the STB slides on the model that carries the cut to loan growth.

f7a2f4b0-FinModel_STB_2Q26.xlsx takes FY26F loan growth to +2.3% from the
+10.1% carried before, finally in line with the +1.5% delivered in 1H26.  That
was the last open gap on STB (G17), and it moves everything: gross loans fall
to 640,643, NII with them, and the forecast changes direction.

FY26F PBT is now VND7,082bn - down 7.2% YoY and 12.6% BELOW the ~VND8,100bn
board plan, where the previous version sat marginally above it.  The slide
heading and the whole third block are rewritten accordingly; this is a change
of story, not of digits.

Two consequences reported rather than silently repaired:
  - CIR comes out at 42.8 / 44.4 / 42.1%, not the 40 / 38 / 36% asked for.
    The opex build is untouched while TOI fell, so the ratio rose.
  - Coverage rises to 54.2% because the NPL balance shrinks with the loan book
    while the reserve stock does not.
"""
import shutil
from pptx import Presentation

SRC = ('/root/.claude/uploads/041665b7-4ff3-507f-a1e8-7a7ed4160156/'
       '292d2379-MASVN_RS_WM_2H26_outlook_Equity_VN_2026_STBFPT_August2026.pptx')
DECK = ('/home/user/verbose-guide/'
        'MASVN_RS_WM_2H26_outlook_Equity_VN_2026_STBFPT_August2026.pptx')
SHARES, TP = 2060.158, 81400.0

# Model!Y/Z/AA, read out of the recalculated workbook
NII = (24570.2, 24387.6, 27512.4)                 # row 121
NONII = (5950.0, 7225.9, 8516.9)                  # rows 124 + 131
TOI = (30520.2, 31613.6, 36029.3)                 # row 136 + row 135
OPEX = (13064.6, 14037.8, 15165.4)                # row 135
PROV = (10374.0, 9626.6, 6982.2)                  # row 141
PBT = (7081.6, 7949.2, 13881.6)                   # row 144
NPATMI = (5513.7, 6189.2, 10808.1)                # row 153
EQUITY = (65433.8, 71623.0, 82431.1)              # row 85
ASSETS = (1013258.6, 1123603.5, 1259770.2)        # row 61
ROE = (8.4, 9.0, 14.0)                            # row 314
LOANS26, NPL26, RESERVE26, WO26 = 640643.1, 35235.4, 19097.7, 10955.0
PBT25, EPS25, PLAN = 7628.025, 2882.84, 8100.0
H1_PBT, H1_PROV, H1_OPEX = 4136.10, 7119.0, 6233.19

EPS = tuple(n * 1000 / SHARES for n in NPATMI)
BVPS = tuple(e * 1000 / SHARES for e in EQUITY)
CIR = tuple(o / t * 100 for o, t in zip(OPEX, TOI))
COV26 = RESERVE26 / NPL26 * 100
H2_PROV, H2_PBT = PROV[0] - H1_PROV, PBT[0] - H1_PBT
PBT_YOY = PBT[0] / PBT25 * 100 - 100
VS_PLAN = PBT[0] / PLAN * 100 - 100
NII_YOY = NII[0] / 26680.6 * 100 - 100
PROV_YOY = PROV[0] / 11383.775 * 100 - 100
EPS_GROWTH = EPS[0] / EPS25 * 100 - 100

TABLE = {1: ['{:,.0f}'.format(v) for v in NII],
         2: ['{:,.0f}'.format(v) for v in NONII],
         3: ['{:,.0f}'.format(v) for v in PBT],
         4: ['{:,.0f}'.format(v) for v in NPATMI],
         5: ['{:,.0f}'.format(v) for v in EPS],
         6: ['{:.1f}'.format(v) for v in ROE],
         9: ['{:,.0f}'.format(v) for v in ASSETS],
         10: ['{:,.0f}'.format(v) for v in EQUITY],
         11: ['{:,.0f}'.format(v) for v in BVPS]}
HIST_EPS, HIST_BVPS = (3747.0, 4896.0, 2883.0), (22199.0, 26683.0, 29059.0)
FULL = {7: ['{:.1f}'.format(TP / e) for e in HIST_EPS + EPS],
        8: ['{:.1f}'.format(TP / b) for b in HIST_BVPS + BVPS]}
BOX = {0: '{:,.0f}'.format(NPATMI[0]), 2: '{:.1f}'.format(EPS_GROWTH),
       3: '{:.1f}'.format(TP / EPS[0])}

EN = {
 4: ("We set FY26F NPL at 5.5%, from below 4.5%, and FY27F at 4.0% from 3.1%. Reserves reached "
     "VND27.2tn at end-2Q26 — 56.7% coverage, up from 50.0% at end-FY25 — after VND7.1tn of 1H26 "
     "charges. A further VND{h2:.1f}tn charge in 2H26 funds write-offs of VND{wo:.1f}tn, or 34% "
     "of the Group 5 balance, leaving coverage at {cov:.1f}%. "),
 5: 'FY26F PBT cut on the loan growth reset: ',
 7: ("We now carry FY26F loan growth of 2.3%, against the 11.7% previously assumed and the 1.5% "
     "delivered in 1H26. That takes gross loans to VND{ln:,.0f}bn and NII to VND{nii:,.0f}bn "
     "({niy:+.1f}% YoY), and cuts FY26F PBT to VND{pbt:,.0f}bn ({yoy:+.1f}% YoY) — {vp:.0f}% "
     "below the board-approved plan of VND8,100bn, where we previously sat marginally above it. "
     "The implied 2H26 PBT is VND{h2p:,.0f}bn against VND297bn in 2H25. "),
 8: ("Other FY26F assumptions: a provisioning charge of VND{prov:.1f}tn ({pry:+.1f}% YoY) and "
     "non-interest income of VND{noi:,.0f}bn. We flag that the opex build is unchanged while "
     "total operating income has fallen, so CIR now reads {c26:.1f}% against the 40.0% we "
     "targeted — on 1H26 opex of VND6,233bn, holding 40.0% would need 2H26 costs below the "
     "first half. Separately, STB's seizure of 507 land-use right certificates at LDG's Viva "
     "City against VND350bn of overdue principal is immaterial in size but shows the collateral "
     "channel the write-off programme depends on."),
}
VN = {
 4: ("Chúng tôi đặt giả định nợ xấu FY26F ở 5.5% (từ dưới 4.5%) và FY27F ở 4.0% (từ 3.1%). Dự "
     "phòng đạt 27.2 nghìn tỷ đồng cuối Q2/2026 — bao phủ 56.7%, tăng từ 50.0% cuối 2025 — sau "
     "khi trích 7.1 nghìn tỷ đồng trong 1H26 và trích thêm {h2:.1f} nghìn tỷ đồng trong 2H26 đủ "
     "để xóa {wo:.1f} nghìn tỷ đồng, tương đương 34% dư nợ nhóm 5, đưa bao phủ về {cov:.1f}%. "),
 5: 'Hạ dự phóng LNTT FY26F do điều chỉnh tăng trưởng tín dụng: ',
 7: ("Chúng tôi hạ giả định tăng trưởng tín dụng FY26F về 2.3%, so với 11.7% trước đây và 1.5% "
     "thực hiện trong 1H26. Dư nợ theo đó còn {ln:,.0f} tỷ đồng và NII còn {nii:,.0f} tỷ đồng "
     "({niy:+.1f}% CK), kéo LNTT FY26F xuống {pbt:,.0f} tỷ đồng ({yoy:+.1f}% CK) — thấp hơn "
     "{vpa:.0f}% so với kế hoạch 8,100 tỷ đồng đã được ĐHĐCĐ thông qua, trong khi bản trước còn "
     "nhỉnh hơn kế hoạch. Mức này hàm ý LNTT 2H26 khoảng {h2p:,.0f} tỷ đồng so với 297 tỷ đồng "
     "của 2H25. "),
 8: ("Các giả định FY26F khác: chi phí dự phòng {prov:.1f} nghìn tỷ đồng ({pry:+.1f}% CK) và thu "
     "nhập ngoài lãi {noi:,.0f} tỷ đồng. Lưu ý cấu phần chi phí hoạt động giữ nguyên trong khi "
     "tổng thu nhập hoạt động giảm, nên CIR hiện ở {c26:.1f}% thay vì mục tiêu 40.0% — với chi "
     "phí 1H26 là 6,233 tỷ đồng, muốn giữ 40.0% thì chi phí 2H26 phải thấp hơn cả nửa đầu năm. "
     "Ở diễn biến khác, việc Sacombank thu giữ 507 giấy chứng nhận quyền sử dụng đất tại dự án "
     "Viva City đối với 350 tỷ đồng dư nợ gốc quá hạn tuy chưa trọng yếu nhưng cho thấy kênh xử "
     "lý tài sản đảm bảo mà chương trình xóa nợ 2H26 phụ thuộc vào."),
}
FMT = dict(h2=H2_PROV / 1000, wo=WO26 / 1000, cov=COV26, ln=LOANS26, nii=NII[0],
           niy=NII_YOY, pbt=PBT[0], yoy=PBT_YOY, vp=-VS_PLAN, vpa=-VS_PLAN,
           h2p=H2_PBT, prov=PROV[0] / 1000, pry=PROV_YOY, noi=NONII[0], c26=CIR[0])


def put(para, txt):
    assert para.runs, 'no runs to inherit formatting from'
    para.runs[0].text = txt
    for r in para.runs[1:]:
        r.text = ''


def main():
    shutil.copy(SRC, DECK)
    prs = Presentation(DECK)
    sid = lambda sl, i: next(s for s in sl.shapes if s.shape_id == i)
    for slide_i, spec in ((0, EN), (1, VN)):
        sl = prs.slides[slide_i]
        tf = sid(sl, 15).text_frame
        for pi, tmpl in spec.items():
            put(tf.paragraphs[pi], tmpl.format(**FMT))
        tbl = sid(sl, 16).table
        for ri, vals in TABLE.items():
            for off, v in enumerate(vals):
                put(tbl.rows[ri].cells[4 + off].text_frame.paragraphs[0], v)
        for ri, vals in FULL.items():
            for off, v in enumerate(vals):
                put(tbl.rows[ri].cells[1 + off].text_frame.paragraphs[0], v)
        box = sid(sl, 12).table
        for ri, v in BOX.items():
            put(box.rows[ri].cells[1].text_frame.paragraphs[0], v)
    prs.save(DECK)


if __name__ == '__main__':
    main()
    print('%-24s%12s%12s%12s' % ('', 'FY26F', 'FY27F', 'FY28F'))
    for lab, vs, f in [('Gross loans', (LOANS26, 719777, 825565), '{:,.0f}'),
                       ('NII', NII, '{:,.0f}'), ('TOI', TOI, '{:,.0f}'),
                       ('Opex', OPEX, '{:,.0f}'), ('CIR %', CIR, '{:.1f}'),
                       ('Provisioning', PROV, '{:,.0f}'), ('PBT', PBT, '{:,.0f}'),
                       ('NPATMI', NPATMI, '{:,.0f}'), ('EPS', EPS, '{:,.0f}'),
                       ('P/E on TP', tuple(TP / e for e in EPS), '{:.1f}'),
                       ('P/B on TP', tuple(TP / b for b in BVPS), '{:.1f}')]:
        print(('%-24s' % lab) + ''.join('%12s' % f.format(v) for v in vs))
    print('\nFY26F PBT %+.1f%% YoY, %.1f%% vs the 8,100 plan · 2H26 PBT %.0f'
          % (PBT_YOY, VS_PLAN, H2_PBT))
    print('coverage %.1f%% on NPL %.0f and reserve %.0f · write-off %.0f'
          % (COV26, NPL26, RESERVE26, WO26))
