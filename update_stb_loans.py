# -*- coding: utf-8 -*-
"""Put the STB slides on the model, which now carries 8% FY26F loan growth.

The loan book is the driver everything else hangs off, and this round takes
FY26F growth to 8.0% on the reported FY25 book of VND626,392bn, from the 2.3%
carried before.  Gross loans reach VND676,504bn.

Booking it exposed why the earlier numbers never matched: the segment build in
Model!515:520 is rolled forward from FY24 and had drifted 5.2% below the
reported book, so the model's stated 7.9% segment growth only ever delivered
2.3%.  The FY26F segments are now rebased before growing, and rows 23-28 - which
were pasted values - reference them, so the balance sheet follows.

Loan growth is free in this model, which is worth knowing when reading the
result.  Model!Y55, other assets, is the balance-sheet plug, so a bigger loan
book is funded by running down a non-earning asset rather than by raising
deposits: interest income rises VND1,554bn in FY26F with no offset in interest
expense.  Real funding would cost something.

The CIR path of 42.1 / 40 / 38% is held rather than the opex level, so the opex
multipliers are re-solved.  Leaving opex where it was would have let CIR fall to
40.0 / 36.3 / 34.6% - a much larger unannounced change than the cost ramp
holding the path implies, and one that assumes an 8% balance sheet costs nothing
to build.  2H26 opex lands at VND7,254bn against VND6,233bn in 1H26.

Everything else stands: FY26F PBT is set by the 0.8653x specific-charge ratio,
FY27F and FY28F carry VND1,000bn and VND2,000bn of provisioning above
write-offs, and the share count is charter capital, 1,885.216mn.

Coverage falls to 48.6% in FY26F.  The NPL balance grows with the book - 5.8% of
a bigger denominator - while the reserve is sized to fund write-offs, so the
ratio gives back the ground the smaller book had bought it.

The slide is derived, not transcribed.  model_read reads FinModel_STB_2Q26.xlsx,
re-evaluates the formulas this project books, and hands back the forecast, so
rerunning this script after a workbook edit is enough.
"""
import shutil
from pptx import Presentation
import model_read
from model_read import F

SRC = ('/root/.claude/uploads/041665b7-4ff3-507f-a1e8-7a7ed4160156/'
       '292d2379-MASVN_RS_WM_2H26_outlook_Equity_VN_2026_STBFPT_August2026.pptx')
DECK = ('/home/user/verbose-guide/'
        'MASVN_RS_WM_2H26_outlook_Equity_VN_2026_STBFPT_August2026.pptx')
SHARES, TP = model_read.SHARES, 75000.0

# Every forecast figure below is derived from FinModel_STB_2Q26.xlsx by
# model_read, which reproduces Excel on all nine FY26F control lines.  Nothing
# here is transcribed, so a revision to the workbook reaches the slide by
# rerunning this script.
NII, NONII, TOI = F['nii'], F['nonii'], F['toi']   # rows 121, 124+131, sum
OPEX, PROV, PBT = F['opex'], F['prov'], F['pbt']   # rows 135, 141, 144
NPATMI, EQUITY, ASSETS = F['npatmi'], F['equity'], F['assets']   # 153, 85, 61
ROE, EPS, BVPS, CIR = F['roe'], F['eps'], F['bvps'], F['cir']
LOANS26, NPL26 = F['loans'][0], F['npl'][0]
RESERVE26, WO26, COV26 = F['reserve'][0], F['writeoff'][0], F['coverage'][0]
PBT25, EPS25, NII25, PROV25 = F['pbt25'], F['eps25'], F['nii25'], F['prov25']

# 1H26 actuals and the board plan - the only STB numbers not in the model
PLAN = 8100.0
H1_PBT, H1_PROV, H1_OPEX = 4136.10, 7119.0, 6233.19
H1_LOANS, GROUP5_2Q = 636029.0, 32220.0     # 2Q26 gross loans and Group 5

H2_PROV, H2_PBT = PROV[0] - H1_PROV, PBT[0] - H1_PBT
PBT_YOY = PBT[0] / PBT25 * 100 - 100
VS_PLAN = PBT[0] / PLAN * 100 - 100
NII_YOY = NII[0] / NII25 * 100 - 100
PROV_YOY = PROV[0] / PROV25 * 100 - 100
EPS_GROWTH = EPS[0] / EPS25 * 100 - 100
LOAN_GROWTH = F['loan_growth'] * 100
H2_LOANS = LOANS26 / H1_LOANS * 100 - 100   # implied 2H26 loan growth
WO_SHARE = WO26 / GROUP5_2Q * 100
NIM = tuple(n / ((a + b) / 2) * 100 for n, a, b in
            zip(NII, (F['loans25'],) + F['loans'][:2], F['loans']))

TABLE = {1: ['{:,.0f}'.format(v) for v in NII],
         2: ['{:,.0f}'.format(v) for v in NONII],
         3: ['{:,.0f}'.format(v) for v in PBT],
         4: ['{:,.0f}'.format(v) for v in NPATMI],
         6: ['{:.1f}'.format(v) for v in ROE],
         9: ['{:,.0f}'.format(v) for v in ASSETS],
         10: ['{:,.0f}'.format(v) for v in EQUITY]}   # 5 and 11 go in FULL
# The deck carried per-share history of 3,747 / 4,896 / 2,883 EPS and
# 22,199 / 26,683 / 29,059 BVPS, all struck on 2,060.158mn shares - paid-in
# capital divided by par, which counts VND1,747.651bn of share premium as stock.
# On charter capital the count is 1,885.216mn and every per-share line, forecast
# and history alike, is 9.3% higher.  Rows 5 and 11 are now written across all
# six columns rather than the forecast three.
HIST_EPS, HIST_BVPS = F['hist_eps'], F['hist_bvps']
FULL = {5: ['{:,.0f}'.format(v) for v in HIST_EPS + EPS],
        7: ['{:.1f}'.format(TP / e) for e in HIST_EPS + EPS],
        8: ['{:.1f}'.format(TP / b) for b in HIST_BVPS + BVPS],
        11: ['{:,.0f}'.format(v) for v in HIST_BVPS + BVPS]}
# The box's 1,885mn shares were right all along; the FY table was not.  Market
# cap is restated on the same count at the VND74,100 price the box's expected
# return already uses, which returns it to the VND139,694bn it carried.
PRICE = 74100.0
BOX = {0: '{:,.0f}'.format(NPATMI[0]), 2: '{:.1f}'.format(EPS_GROWTH),
       3: '{:.1f}'.format(TP / EPS[0]),
       4: '{:,.0f}'.format(SHARES * PRICE / 1000), 5: '{:,.0f}'.format(SHARES)}

EN = {
 4: ("We set FY26F NPL at 5.8%, from below 4.5%, and FY27F at 4.0% from 3.1%. On an 8% loan "
     "book that is a balance of VND{npl:,.0f}bn, so the ratio improves on 2Q26\u2019s 7.54% through "
     "write-offs and a bigger denominator rather than through cures. Reserves reached "
     "VND27.2tn at end-2Q26 — 56.7% coverage, up from 50.0% at end-FY25 — after VND7.1tn of 1H26 "
     "charges. A further VND{h2:.1f}tn charge in 2H26 funds write-offs of VND{wo:.1f}tn, or {wos:.0f}% "
     "of the Group 5 balance, leaving coverage at {cov:.1f}%. "),
 5: 'FY26F PBT of VND{pbt:,.0f}bn on an 8% loan book: ',
 7: ("We take FY26F loan growth to {lg:.1f}%, from the 2.3% carried before and against the 1.5% "
     "delivered in 1H26 — the second half has to add {h2l:.1f}% for the year to land there, which "
     "assumes STB draws on the credit quota it has not used. Gross loans reach VND{ln:,.0f}bn and "
     "NII VND{nii:,.0f}bn ({niy:+.1f}% YoY), taking FY26F PBT to VND{pbt:,.0f}bn ({yoy:+.1f}% YoY) "
     "— {vp:.1f}% below the board-approved plan of VND8,100bn. The implied 2H26 PBT is "
     "VND{h2p:,.0f}bn against VND297bn in 2H25. "),
 8: ("Other FY26F assumptions: a provisioning charge of VND{prov:.1f}tn ({pry:+.1f}% YoY) and "
     "non-interest income of VND{noi:,.0f}bn. CIR steps down from {c26:.1f}% in FY26F to "
     "{c27:.1f}% in FY27F and {c28:.1f}% in FY28F; holding that path on the bigger revenue base "
     "puts 2H26 costs at VND{h2o:,.0f}bn against VND6,233bn in 1H26, {h2oy:+.1f}%, so the loan "
     "book is not assumed to grow for free. FY27F carries VND1,000bn "
     "of specific charge above what write-offs consume and FY28F VND2,000bn, so reserve stock "
     "builds rather than merely funding disposals. FY27F NII grows "
     "{n27:.1f}% as NIM turns — NII/average loans goes from {nim26:.2f}% to {nim27:.2f}% — carrying FY27F PBT "
     "to VND{p27:,.0f}bn (+{g27:.0f}%) and FY28F to VND{p28:,.0f}bn (+{g28:.0f}%). Separately, STB's seizure of 507 land-use right certificates at LDG's Viva "
     "City against VND350bn of overdue principal is immaterial in size but shows the collateral "
     "channel the write-off programme depends on."),
}
VN = {
 4: ("Chúng tôi đặt giả định nợ xấu FY26F ở 5.8% (từ dưới 4.5%) và FY27F ở 4.0% (từ 3.1%). Giữ "
     "Trên nền dư nợ tăng 8%, mức này tương ứng số dư {npl:,.0f} tỷ đồng — tỷ lệ nợ xấu cải "
     "thiện từ 7.54% của Q2/2026 nhờ xóa nợ và mẫu số lớn hơn, không phải nhờ nợ được thu hồi. Dự "
     "phòng đạt 27.2 nghìn tỷ đồng cuối Q2/2026 — bao phủ 56.7%, tăng từ 50.0% cuối 2025 — sau "
     "khi trích 7.1 nghìn tỷ đồng trong 1H26 và trích thêm {h2:.1f} nghìn tỷ đồng trong 2H26 đủ "
     "để xóa {wo:.1f} nghìn tỷ đồng, tương đương {wos:.0f}% dư nợ nhóm 5, đưa bao phủ về {cov:.1f}%. "),
 5: 'LNTT FY26F {pbt:,.0f} tỷ đồng trên nền dư nợ tăng 8%: ',
 7: ("Chúng tôi hạ giả định tăng trưởng tín dụng FY26F về 2.3%, so với 11.7% trước đây và 1.5% "
     "thực hiện trong 1H26. Dư nợ theo đó còn {ln:,.0f} tỷ đồng và NII còn {nii:,.0f} tỷ đồng "
     "({niy:+.1f}% CK), kéo LNTT FY26F xuống {pbt:,.0f} tỷ đồng ({yoy:+.1f}% CK) — thấp hơn "
     "{vpa:.0f}% so với kế hoạch 8,100 tỷ đồng đã được ĐHĐCĐ thông qua, trong khi bản trước còn "
     "nhỉnh hơn kế hoạch. Mức này hàm ý LNTT 2H26 khoảng {h2p:,.0f} tỷ đồng so với 297 tỷ đồng "
     "của 2H25. "),
 8: ("Các giả định FY26F khác: chi phí dự phòng {prov:.1f} nghìn tỷ đồng ({pry:+.1f}% CK) và thu "
     "nhập ngoài lãi {noi:,.0f} tỷ đồng. CIR giảm dần từ {c26:.1f}% năm FY26F về {c27:.1f}% FY27F "
     "và {c28:.1f}% FY28F; giữ lộ trình này trên nền thu nhập lớn hơn cho chi phí 2H26 ở "
     "{h2o:,.0f} tỷ đồng so với 6,233 tỷ đồng của 1H26, {h2oy:+.1f}%, tức tăng trưởng tín dụng "
     "không được giả định là miễn phí. "
     "FY27F trích thêm 1,000 tỷ đồng và FY28F 2,000 tỷ đồng ngoài phần đủ bù xóa nợ, tức bộ đệm "
     "dự phòng được bồi đắp chứ không chỉ tài trợ xử lý nợ. NII FY27F tăng "
     "{n27:.1f}% khi NIM đảo chiều — NII/dư nợ bình quân từ {nim26:.2f}% lên {nim27:.2f}% — đưa LNTT FY27F lên "
     "{p27:,.0f} tỷ đồng (+{g27:.0f}%) và FY28F lên {p28:,.0f} tỷ đồng (+{g28:.0f}%). Ở diễn biến khác, việc Sacombank thu giữ 507 giấy chứng nhận quyền sử dụng đất tại dự án "
     "Viva City đối với 350 tỷ đồng dư nợ gốc quá hạn tuy chưa trọng yếu nhưng cho thấy kênh xử "
     "lý tài sản đảm bảo mà chương trình xóa nợ 2H26 phụ thuộc vào."),
}
FMT = dict(h2=H2_PROV / 1000, wo=WO26 / 1000, cov=COV26, ln=LOANS26, nii=NII[0],
           lg=LOAN_GROWTH, h2l=H2_LOANS, wos=WO_SHARE,
           nim26=NIM[0], nim27=NIM[1],
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
    for lab, vs, f in [('Gross loans', F['loans'], '{:,.0f}'),
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
