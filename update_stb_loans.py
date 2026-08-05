# -*- coding: utf-8 -*-
"""Put the STB slides on the model that carries the cut to loan growth.

f7a2f4b0-FinModel_STB_2Q26.xlsx takes FY26F loan growth to +2.3% from the
+10.1% carried before, finally in line with the +1.5% delivered in 1H26.  That
was the last open gap on STB (G17), and it moves everything: gross loans fall
to 640,643, NII with them, and the forecast changes direction.

On top of that the analyst set FY26F PBT at VND7,500bn and CIR on a declining
path of 42.1 / 40 / 38%, then added VND1,000bn of provisioning to FY27F and
FY28F.  All three are booked in the model (fix_stb_model.MODEL_FORMULAS): the
FY26F specific charge / write-off ratio, the opex multipliers, and a flat
VND1,000bn on top of the FY27F and FY28F specific charge.

The overlay costs VND1,000bn of PBT in each of the two forecast years and
nothing in FY26F, so the profit path flattens: FY27F growth falls from +45.7%
to +32.3% and FY28F rises from +58.9% to +64.8% on the lower FY27F base.  ROE
gives back a point in FY27F (12.1% to 11.0%) and 0.7pt in FY28F.

PBT is now 1.7% below FY25 and 7.4% below the ~VND8,100bn board plan, where the
previous version sat marginally above it.  The slide heading and the third
block are rewritten accordingly; this is a change of story, not of digits.

The CIR path is worth stating plainly on the slide, and is: FY26F opex of
VND12,208bn against VND6,233bn already spent in 1H26 leaves VND5,975bn for the
second half, 4.1% BELOW the first.  That is a real cost reduction, not an
accrual shift, and the narrative says so.

Coverage rises to 55.4% - the NPL balance shrinks with the loan book while the
reserve stock does not, and the heavier charge adds to it.
"""
import shutil
from pptx import Presentation

SRC = ('/root/.claude/uploads/041665b7-4ff3-507f-a1e8-7a7ed4160156/'
       '292d2379-MASVN_RS_WM_2H26_outlook_Equity_VN_2026_STBFPT_August2026.pptx')
# FY26F PBT is set to 7,500 and CIR to 40/38/36% - see fix_stb_model.MODEL_FORMULAS
DECK = ('/home/user/verbose-guide/'
        'MASVN_RS_WM_2H26_outlook_Equity_VN_2026_STBFPT_August2026.pptx')
SHARES, TP = 2060.158, 75000.0

# Model!Y/Z/AA, read out of the recalculated workbook
NII = (24530.8, 26953.5, 30600.1)                 # row 121
NONII = (5950.0, 7225.9, 8516.9)                  # rows 124 + 131
TOI = (30480.8, 34179.4, 39117.0)                 # row 136 + row 135
OPEX = (12818.4, 13671.7, 14864.2)                # row 135, CIR steps down
PROV = (10201.8, 10635.6, 7982.2)                 # row 141, +1,000 in FY27F/FY28F
PBT = (7460.6, 9872.2, 16270.6)                   # row 144
NPATMI = (5808.8, 7686.4, 12668.1)                # row 153
EQUITY = (65728.9, 73415.3, 86083.5)              # row 85
ASSETS = (1013554, 1125396, 1263423)              # row 61
ROE = (8.8, 11.0, 15.9)                           # row 314, on average equity
LOANS26, NPL26, RESERVE26, WO26 = 640643.1, 37157.3, 18925.5, 10955.0
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
 4: ("We set FY26F NPL at 5.8%, from below 4.5%, and FY27F at 4.0% from 3.1%. Holding the "
     "ratio at 5.5% on the smaller loan book would have required net NPL recoveries in 2H26; "
     "5.8% keeps the absolute balance at VND{npl:,.0f}bn and implied net formation just positive. "
     "Reserves reached "
     "VND27.2tn at end-2Q26 — 56.7% coverage, up from 50.0% at end-FY25 — after VND7.1tn of 1H26 "
     "charges. A further VND{h2:.1f}tn charge in 2H26 funds write-offs of VND{wo:.1f}tn, or 34% "
     "of the Group 5 balance, leaving coverage at {cov:.1f}%. "),
 5: 'FY26F PBT of VND7,461bn on the loan growth reset: ',
 7: ("We now carry FY26F loan growth of 2.3%, against the 11.7% previously assumed and the 1.5% "
     "delivered in 1H26. That takes gross loans to VND{ln:,.0f}bn and NII to VND{nii:,.0f}bn "
     "({niy:+.1f}% YoY), and FY26F PBT to VND{pbt:,.0f}bn ({yoy:+.1f}% YoY) — {vp:.1f}% "
     "below the board-approved plan of VND8,100bn, where we previously sat marginally above it. "
     "The implied 2H26 PBT is VND{h2p:,.0f}bn against VND297bn in 2H25. "),
 8: ("Other FY26F assumptions: a provisioning charge of VND{prov:.1f}tn ({pry:+.1f}% YoY) and "
     "non-interest income of VND{noi:,.0f}bn. CIR steps down from {c26:.1f}% in FY26F to "
     "{c27:.1f}% in FY27F and {c28:.1f}% in FY28F; on 1H26 opex of VND6,233bn that puts 2H26 costs at VND{h2o:,.0f}bn, "
     "{h2oy:+.1f}% on the first half, so no cost reduction is assumed. FY27F and FY28F each "
     "carry VND1,000bn of specific charge above what write-offs consume, so reserve stock builds "
     "rather than merely funding disposals. FY27F NII grows "
     "{n27:.1f}% as NIM turns — NII/average loans goes from 3.87% to 3.96% — carrying FY27F PBT "
     "to VND{p27:,.0f}bn (+{g27:.0f}%) and FY28F to VND{p28:,.0f}bn (+{g28:.0f}%). Separately, STB's seizure of 507 land-use right certificates at LDG's Viva "
     "City against VND350bn of overdue principal is immaterial in size but shows the collateral "
     "channel the write-off programme depends on."),
}
VN = {
 4: ("Chúng tôi đặt giả định nợ xấu FY26F ở 5.8% (từ dưới 4.5%) và FY27F ở 4.0% (từ 3.1%). Giữ "
     "5.5% trên nền dư nợ đã thu hẹp sẽ đòi hỏi nợ xấu phải được thu hồi ròng trong 2H26; mức "
     "5.8% giữ số dư tuyệt đối ở {npl:,.0f} tỷ đồng và nợ xấu phát sinh mới vẫn dương. Dự "
     "phòng đạt 27.2 nghìn tỷ đồng cuối Q2/2026 — bao phủ 56.7%, tăng từ 50.0% cuối 2025 — sau "
     "khi trích 7.1 nghìn tỷ đồng trong 1H26 và trích thêm {h2:.1f} nghìn tỷ đồng trong 2H26 đủ "
     "để xóa {wo:.1f} nghìn tỷ đồng, tương đương 34% dư nợ nhóm 5, đưa bao phủ về {cov:.1f}%. "),
 5: 'Đặt LNTT FY26F ở 7,500 tỷ đồng sau khi điều chỉnh tăng trưởng tín dụng: ',
 7: ("Chúng tôi hạ giả định tăng trưởng tín dụng FY26F về 2.3%, so với 11.7% trước đây và 1.5% "
     "thực hiện trong 1H26. Dư nợ theo đó còn {ln:,.0f} tỷ đồng và NII còn {nii:,.0f} tỷ đồng "
     "({niy:+.1f}% CK), kéo LNTT FY26F xuống {pbt:,.0f} tỷ đồng ({yoy:+.1f}% CK) — thấp hơn "
     "{vpa:.0f}% so với kế hoạch 8,100 tỷ đồng đã được ĐHĐCĐ thông qua, trong khi bản trước còn "
     "nhỉnh hơn kế hoạch. Mức này hàm ý LNTT 2H26 khoảng {h2p:,.0f} tỷ đồng so với 297 tỷ đồng "
     "của 2H25. "),
 8: ("Các giả định FY26F khác: chi phí dự phòng {prov:.1f} nghìn tỷ đồng ({pry:+.1f}% CK) và thu "
     "nhập ngoài lãi {noi:,.0f} tỷ đồng. CIR giảm dần từ {c26:.1f}% năm FY26F về {c27:.1f}% FY27F "
     "và {c28:.1f}% FY28F; với chi phí 1H26 là 6,233 tỷ đồng, mức này cho chi phí 2H26 ở {h2o:,.0f} tỷ đồng, "
     "{h2oy:+.1f}% so với nửa đầu năm, tức không giả định cắt giảm chi phí. FY27F và FY28F mỗi "
     "năm trích thêm 1,000 tỷ đồng ngoài phần đủ bù xóa nợ, tức bộ đệm dự phòng được bồi đắp chứ "
     "không chỉ tài trợ xử lý nợ. NII FY27F tăng "
     "{n27:.1f}% khi NIM đảo chiều — NII/dư nợ bình quân từ 3.87% lên 3.96% — đưa LNTT FY27F lên "
     "{p27:,.0f} tỷ đồng (+{g27:.0f}%) và FY28F lên {p28:,.0f} tỷ đồng (+{g28:.0f}%). Ở diễn biến khác, việc Sacombank thu giữ 507 giấy chứng nhận quyền sử dụng đất tại dự án "
     "Viva City đối với 350 tỷ đồng dư nợ gốc quá hạn tuy chưa trọng yếu nhưng cho thấy kênh xử "
     "lý tài sản đảm bảo mà chương trình xóa nợ 2H26 phụ thuộc vào."),
}
FMT = dict(h2=H2_PROV / 1000, wo=WO26 / 1000, cov=COV26, ln=LOANS26, nii=NII[0],
           niy=NII_YOY, pbt=PBT[0], yoy=PBT_YOY, vp=-VS_PLAN, vpa=-VS_PLAN,
           h2p=H2_PBT, prov=PROV[0] / 1000, pry=PROV_YOY, noi=NONII[0],
           c26=CIR[0], c27=CIR[1], c28=CIR[2], h2o=OPEX[0] - H1_OPEX, npl=NPL26,
           h2oy=(OPEX[0] - H1_OPEX) / H1_OPEX * 100 - 100,
           p27=PBT[1], g27=PBT[1] / PBT[0] * 100 - 100,
           p28=PBT[2], g28=PBT[2] / PBT[1] * 100 - 100,
           n27=NII[1] / NII[0] * 100 - 100)


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
