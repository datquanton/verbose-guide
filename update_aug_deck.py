# -*- coding: utf-8 -*-
"""Bring the analyst's August deck onto the latest STB model, and put the FPT
P/E row on the slide's target price.

Base is 816e5c79-...August2026.pptx - the analyst's own version, which carries a
new STB target price (81,400), refreshed market data, a re-split STB narrative
and an FPT table with the two % YoY rows removed.  Nothing here re-imposes the
older structure; only the figures the model drives are touched.

STB numbers come from 8ce85368-FinModel_STB_2Q26.xlsx, which the analyst
recalculated in Excel after re-cutting the FY27F and FY28F write-off rates
(-0.9% -> -1.2% and -0.5% -> -0.7%).  That lifts provisioning in both years and
takes FY27F PBT to 12,293 from 14,676 and FY28F to 20,064 from 21,145.

FPT: the P/E row mixed conventions - FY23-25 were struck on each year's own
price, FY26F-28F on the target price.  All six columns now use the target
price of 87,950, matching how the STB row has always been built.
"""
import shutil
from pptx import Presentation

SRC = ('/root/.claude/uploads/041665b7-4ff3-507f-a1e8-7a7ed4160156/'
       '816e5c79-MASVN_RS_WM_2H26_outlook_Equity_VN_2026_STBFPT_August2026.pptx')
DECK = ('/home/user/verbose-guide/'
        'MASVN_RS_WM_2H26_outlook_Equity_VN_2026_STBFPT_August2026.pptx')

SHARES = 2060.158          # Model!X87 paid-in capital / VND10,000 par
STB_TP = 81400.0           # slide 0/1 rating box, raised from 77,800
FPT_TP = 87950.0           # slide 2/3 rating box, unchanged

# --- Model!Y/Z/AA, read out of the recalculated workbook -------------------
NII = (26704.4, 29544.5, 34079.0)                       # row 121
NONII = (3385.3 + 2564.7, 3839.4 + 3542.7, 4372.0 + 4406.7)   # rows 124 + 131
PBT = (8142.8, 12293.4, 20064.4)                        # row 144
NPATMI = (6339.9, 9571.5, 15621.9)                      # row 153
EQUITY = (66260.0, 75831.5, 91453.5)                    # row 85
ASSETS = (1014084.8, 1127812.1, 1268792.6)              # row 61
ROE = (9.6, 13.5, 18.7)                                 # row 314
PROV = (11447.0, 10595.4, 7627.9)                       # row 141
OPEX = (13064.6, 14037.8, 15165.4)                      # row 135
TOI = (32654.3, 36926.6, 42857.6)                       # row 136 + row 135
RESERVE_26, NPL_26 = 19329.5, 37940.777410772149        # row 286; NPL!N22
PBT25, EPS25 = 7628.025, 2882.84
H1_PBT, H1_PROV = 4136.10, 7119.0

EPS = tuple(n * 1000 / SHARES for n in NPATMI)
BVPS = tuple(e * 1000 / SHARES for e in EQUITY)
STB_HIST_EPS = (3747.0, 4896.0, 2883.0)
STB_HIST_BVPS = (22199.0, 26683.0, 29059.0)
FPT_EPS = (4648.0, 4877.0, 5073.0, 6424.0, 7440.0, 8673.0)

# derived figures the narrative quotes
CIR = tuple(o / t * 100 for o, t in zip(OPEX, TOI))
COV26 = RESERVE_26 / NPL_26 * 100
H2_PROV = PROV[0] - H1_PROV
H2_PBT = PBT[0] - H1_PBT
PBT_YOY = PBT[0] / PBT25 * 100 - 100
EPS_GROWTH = EPS[0] / EPS25 * 100 - 100

STB_TABLE = {                       # row -> the three forecast columns
    1: ['{:,.0f}'.format(v) for v in NII],
    2: ['{:,.0f}'.format(v) for v in NONII],
    3: ['{:,.0f}'.format(v) for v in PBT],
    4: ['{:,.0f}'.format(v) for v in NPATMI],
    5: ['{:,.0f}'.format(v) for v in EPS],
    6: ['{:.1f}'.format(v) for v in ROE],
    9: ['{:,.0f}'.format(v) for v in ASSETS],
    10: ['{:,.0f}'.format(v) for v in EQUITY],
    11: ['{:,.0f}'.format(v) for v in BVPS],
}
# P/E and P/B run across all six columns because both are struck on the target
# price - raising it to 81,400 moves the history too.
STB_FULL = {
    7: ['{:.1f}'.format(STB_TP / e) for e in STB_HIST_EPS + EPS],
    8: ['{:.1f}'.format(STB_TP / b) for b in STB_HIST_BVPS + BVPS],
}
STB_BOX = {0: '{:,.0f}'.format(NPATMI[0]),
           2: '{:.1f}'.format(EPS_GROWTH),
           3: '{:.1f}'.format(STB_TP / EPS[0])}

FPT_PE = ['{:.1f}'.format(FPT_TP / e) for e in FPT_EPS]

EN = {
 4: ("We set FY26F NPL at 5.5%, from below 4.5%, and FY27F at 4.0% from 3.1%. Reserves reached "
     "VND27.2tn at end-2Q26 — 56.7% coverage, up from 50.0% at end-FY25 — after VND7.1tn of 1H26 "
     "charges. A further VND{h2:.1f}tn charge in 2H26 funds write-offs of VND11.8tn, or 37% of "
     "the Group 5 balance, leaving coverage at {cov:.1f}%. "),
 7: ("We set FY26F PBT at VND{pbt:,.0f}bn ({yoy:+.1f}% YoY), marginally above the board-approved "
     "plan of VND8,100bn. The cost line does the lifting — 1H26 CIR came in at 35.6% against the "
     "42.9% previously carried, and we now assume {c26:.1f}% (-0.7%p YoY), {c27:.1f}% in FY27F "
     "and {c28:.1f}% in FY28F — with the balance taken back in provisioning. That implies 2H26 "
     "PBT of VND{h2pbt:,.0f}bn, around {x:.0f}x the 2H25 base. "),
 8: ("Other FY26F assumptions: NII of VND{nii:,.0f}bn (+0.1% YoY), NIM of 2.92% (-40bps YoY) and "
     "provisioning of VND{prov:.1f}tn ({pyoy:+.1f}% YoY); we flag 1H26 loan growth of 1.5% "
     "against the 11.7% carried for the full year. "),
}
VN = {
 4: ("Chúng tôi đặt giả định nợ xấu FY26F ở 5.5% (từ dưới 4.5%) và FY27F ở 4.0% (từ 3.1%). Dự "
     "phòng đạt 27.2 nghìn tỷ đồng cuối Q2/2026 — bao phủ 56.7%, tăng từ 50.0% cuối 2025 — sau "
     "khi trích 7.1 nghìn tỷ đồng trong 1H26 và trích thêm {h2:.1f} nghìn tỷ đồng trong 2H26 đủ "
     "để xóa 11.8 nghìn tỷ đồng, tương đương 37% dư nợ nhóm 5, đưa bao phủ về {cov:.1f}%. Việc "
     "giữ bao phủ quanh 50% giới hạn mức cải thiện ở 5.5%. "),
 7: ("Chúng tôi đặt dự phóng LNTT FY26F ở {pbt:,.0f} tỷ đồng ({yoy:+.1f}% CK), nhỉnh hơn kế "
     "hoạch 8,100 tỷ đồng đã được ĐHĐCĐ thông qua. Chi phí hoạt động là động lực chính — CIR "
     "1H26 chỉ 35.6% so với 42.9% dự phóng trước đây, và chúng tôi điều chỉnh về {c26:.1f}% "
     "(-0.7%p CK), {c27:.1f}% FY27F và {c28:.1f}% FY28F — phần chênh còn lại đưa vào chi phí dự "
     "phòng. Mức này hàm ý LNTT 2H26 khoảng {h2pbt:,.0f} tỷ đồng, tương đương khoảng {x:.0f} lần "
     "nền 2H25. "),
 8: ("Các giả định FY26F khác: NII {nii:,.0f} tỷ đồng (+0.1% CK), NIM 2.92% (-40bps CK) và chi "
     "phí dự phòng {prov:.1f} nghìn tỷ đồng ({pyoy:+.1f}% CK); lưu ý tăng trưởng tín dụng 1H26 "
     "chỉ 1.5% so với 11.7% dự phóng cả năm. "),
}
FMT = dict(h2=H2_PROV / 1000, cov=COV26, pbt=PBT[0], yoy=PBT_YOY,
           c26=CIR[0], c27=CIR[1], c28=CIR[2], h2pbt=H2_PBT, x=H2_PBT / 297,
           nii=NII[0], prov=PROV[0] / 1000, pyoy=PROV[0] / 11383.775 * 100 - 100)


def put(para, txt):
    assert para.runs, 'no runs to inherit formatting from'
    para.runs[0].text = txt
    for r in para.runs[1:]:
        r.text = ''


def cell(c, txt):
    put(c.text_frame.paragraphs[0], txt)


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
        for ri, vals in STB_TABLE.items():
            for off, v in enumerate(vals):
                cell(tbl.rows[ri].cells[4 + off], v)
        for ri, vals in STB_FULL.items():
            for off, v in enumerate(vals):
                cell(tbl.rows[ri].cells[1 + off], v)
        box = sid(sl, 12).table
        for ri, v in STB_BOX.items():
            cell(box.rows[ri].cells[1], v)
    for slide_i in (2, 3):           # FPT P/E onto the target price
        tbl = sid(prs.slides[slide_i], 16).table
        for off, v in enumerate(FPT_PE):
            cell(tbl.rows[7].cells[1 + off], v)
    prs.save(DECK)


if __name__ == '__main__':
    main()
    print('STB, on the recalculated model and TP %s' % '{:,.0f}'.format(STB_TP))
    print('%-22s%12s%12s%12s' % ('', 'FY26F', 'FY27F', 'FY28F'))
    for lab, vs, f in [('PBT', PBT, '{:,.0f}'), ('NPATMI', NPATMI, '{:,.0f}'),
                       ('EPS', EPS, '{:,.0f}'), ('ROE %', ROE, '{:.1f}'),
                       ('CIR %', CIR, '{:.1f}'), ('provisioning', PROV, '{:,.0f}'),
                       ('P/E on TP', tuple(STB_TP / e for e in EPS), '{:.1f}'),
                       ('P/B on TP', tuple(STB_TP / b for b in BVPS), '{:.1f}')]:
        print(('%-22s' % lab) + ''.join('%12s' % f.format(v) for v in vs))
    print('\nFY26F PBT %+.1f%% YoY · 2H26 PBT %,.0f (%.1fx 2H25) · 2H26 provisioning %.1ftn'
          .replace('%,', '%') % (PBT_YOY, H2_PBT, H2_PBT / 297, H2_PROV / 1000))
    print('coverage %.1f%% · EPS growth %+.1f%%' % (COV26, EPS_GROWTH))
    print('\nFPT P/E on TP 87,950: ' + ' '.join(FPT_PE) + '   (was 19.7 18.8 18.1 13.7 11.8 10.1)')
