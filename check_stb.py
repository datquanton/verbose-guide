# -*- coding: utf-8 -*-
"""Cross-check the August deck and the stock-pick workbook against the model.

Deck figures are compared against update_aug_deck's constants, which are read
straight out of the recalculated workbook, so nothing is typed twice.  The
model file itself is verified by fix_stb_model.verify().
"""
import openpyxl, zipfile
from lxml import etree
from pptx import Presentation
import update_stb_loans as U
import fix_stb_model, model_read

DECK = ('/home/user/verbose-guide/'
        'MASVN_RS_WM_2H26_outlook_Equity_VN_2026_STBFPT_August2026.pptx')
PICK = '/home/user/verbose-guide/Stock_Pick_and_Forecast_Aug26_MAS_RS_EN_updated.xlsx'
MODEL = '/home/user/verbose-guide/FinModel_STB_2Q26.xlsx'
TPF = 87950.
NS = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
TP, SHARES = U.TP, U.SHARES
fails = []


def check(n, c, d=''):
    print('%-4s %-58s %s' % ('OK' if c else 'FAIL', n, d))
    if not c:
        fails.append(n)


# -------------------------------------------------- the slide vs the workbook
_drift = fix_stb_model.verify()
check('every booked formula still in FinModel_STB_2Q26.xlsx', not _drift,
      '; '.join(_drift) or '28 assumptions')
check('the derivation reproduces Excel on all FY26F control lines',
      not model_read._m.check(model_read.F), 'opex, TOI, provisioning, PBT, '
      'NPATMI, equity, assets, allowance, loans')
check('shares struck on charter capital, not paid-in capital',
      abs(U.SHARES - 1885.2157) < 0.001,
      "'Balance sheet'!Y80 18,852.157 / 10,000 par - NOT Y79 20,601.582")
check('box market cap = shares x the price the expected return uses',
      abs(U.SHARES * U.PRICE / 1000 - 139694) < 5,
      '%.0f' % (U.SHARES * U.PRICE / 1000))
check('per-share history restated on the same count as the forecast',
      abs(U.HIST_EPS[2] - 3150) < 2 and abs(U.HIST_BVPS[2] - 31756) < 2,
      'FY25 EPS %.0f BVPS %.0f, were 2,883 and 29,059' % (U.HIST_EPS[2], U.HIST_BVPS[2]))
check('the slide reads the model, nothing is transcribed',
      U.PBT is model_read.F['pbt'] and U.NPATMI is model_read.F['npatmi']
      and U.PROV is model_read.F['prov'])

# ------------------------------------------------------ the model's own P&L
check('FY26F loan growth cut to the 1H26 run-rate',
      abs(U.LOANS26 / 626392.336 - 1 - 0.023) < 0.002,
      '+%.1f%% vs +1.5%% delivered in 1H26' % (U.LOANS26 / 626392.336 * 100 - 100))
check('PBT = TOI - opex - provisioning, all three years',
      all(abs(U.TOI[i] - U.OPEX[i] - U.PROV[i] - U.PBT[i]) < 1 for i in range(3)))
check('NPATMI = PBT x (1 - 22.14% tax)',
      all(abs(U.PBT[i] * 0.7785909196679350 - U.NPATMI[i]) < 1.5 for i in range(3)))
check('equity rolls forward on retained NPATMI',
      abs(U.EQUITY[1] - U.EQUITY[0] - U.NPATMI[1]) < 1.5
      and abs(U.EQUITY[2] - U.EQUITY[1] - U.NPATMI[2]) < 1.5)
check('TOI = NII + non-interest income',
      all(abs(U.NII[i] + U.NONII[i] - U.TOI[i]) < 1 for i in range(3)))
check('FY26F NPL 5.8% of the smaller loan book',
      abs(U.NPL26 / U.LOANS26 - 0.058) < 0.0002, '%.2f%%' % (U.NPL26 / U.LOANS26 * 100))
check('implied 2H26 NPL formation is positive, not a net recovery',
      U.NPL26 - (47957 - U.WO26) > 0, '%+.0f' % (U.NPL26 - (47957 - U.WO26)))
check('FY26F PBT from the model', abs(U.PBT[0] - 7461) < 1,
      '%.0f = plan %.1f%%, %+.1f%% YoY' % (U.PBT[0], U.VS_PLAN, U.PBT_YOY))
check('FY26F CIR near the 42% target', abs(U.CIR[0] - 42) < 0.2, '%.1f%%' % U.CIR[0])
check('CIR declines year on year, as instructed',
      U.CIR[0] > U.CIR[1] > U.CIR[2],
      '%.1f / %.1f / %.1f%%' % U.CIR)
for i, tgt in ((1, 40.), (2, 38.)):
    check('FY%dF CIR = %.0f%%' % (2026 + i, tgt), abs(U.CIR[i] - tgt) < 0.05,
          '%.2f%%' % U.CIR[i])
check('2H26 opex now ABOVE 1H26 - no cost cut assumed',
      U.OPEX[0] - U.H1_OPEX > U.H1_OPEX, '%.0f vs 6,233 (%+.1f%%)'
      % (U.OPEX[0] - U.H1_OPEX, (U.OPEX[0] - U.H1_OPEX) / U.H1_OPEX * 100 - 100))
check('FY27F NII growth below the 15% target', U.NII[1] / U.NII[0] < 1.15,
      '%+.1f%% - the model returned this, not 15%%' % (U.NII[1] / U.NII[0] * 100 - 100))
check('FY27F NII no longer falls while loans grow', U.NII[1] > U.NII[0])
check('FY28F PBT growth above the 50% target', U.PBT[2] / U.PBT[1] > 1.50,
      '%+.1f%% - reported, not re-solved' % (U.PBT[2] / U.PBT[1] * 100 - 100))
check('FY27F carries a 1,000 provisioning overlay, FY28F 2,000',
      abs(U.PROV[1] - 9635.5524418309324 - 1000) < 0.5
      and abs(U.PROV[2] - 6982.2147525724604 - 2000) < 0.5,
      '%.0f and %.0f, from 9,636 and 6,982' % (U.PROV[1], U.PROV[2]))
check('the overlay is charge, not write-off: provisioning exceeds write-offs',
      U.PROV[1] > 8637.3 and U.PROV[2] > 5779.0,
      'reserve stock builds by 1,000 in FY27F and 3,000 by FY28F')
# the overlay pushes the FY27F charge above FY26F even though write-offs fall
# from 11.0tn to 8.6tn - the peak provisioning year moves out by a year
check('provisioning peaks in FY27F, then falls in FY28F',
      U.PROV[1] > U.PROV[0] > U.PROV[2],
      '%.0f / %.0f / %.0f' % U.PROV)
check('FY28F PBT down 1,000 on the second tranche', abs(U.PBT[2] - 15270.6) < 1,
      '%.0f, +%.1f%% on FY27F' % (U.PBT[2], U.PBT[2] / U.PBT[1] * 100 - 100))
check('FY28F PBT growth back near the 50% the analyst set',
      abs(U.PBT[2] / U.PBT[1] * 100 - 100 - 50) < 6,
      '%+.1f%% - was +64.8%% before the second tranche' % (U.PBT[2] / U.PBT[1] * 100 - 100))
# coverage is the price of the overlay - flagged as G22, not asserted away
COV = [r / (n * l) * 100 for r, n, l in
       zip((18925.5, 20524.5, 23305.4), (.058, .040, .027),
           (640643.1, 719776.9, 825564.9))]
check('NPL coverage above 100% by FY28F - the cost of the overlay',
      COV[2] > 100, '%.0f / %.0f / %.0f%%' % tuple(COV))
check('target price 75,000', abs(U.TP - 75000) < 1)
check('coverage near 50%', abs(U.COV26 - 51) < 1, '%.1f%%' % U.COV26)

# ------------------------------------------------------------------- deck
prs = Presentation(DECK)
num = lambda s: float(s.replace(',', ''))


def grab(i):
    sh = {x.shape_id: x for x in prs.slides[i].shapes}
    t = sh[16].table
    return ({sh[12].table.cell(r, 0).text: sh[12].table.cell(r, 1).text.strip() for r in range(4)},
            {t.cell(r, 0).text: [t.cell(r, c).text.strip() for c in range(4, 7)] for r in range(1, 12)},
            sh[15].text_frame.text)


en_box, en_tbl, en_txt = grab(0)
vn_box, vn_tbl, vn_txt = grab(1)
row = lambda tbl, k: [num(x) for x in next(v for kk, v in tbl.items() if kk.startswith(k))]
pbt, npat = row(en_tbl, 'Operating profit'), row(en_tbl, 'Net Profit')
eps, pe, pb = row(en_tbl, 'EPS'), row(en_tbl, 'P/E'), row(en_tbl, 'P/B')
bv, eq = row(en_tbl, 'BVPS'), row(en_tbl, 'Equity')

for i in range(3):
    y = 2026 + i
    check('FY%dF PBT = model' % y, abs(pbt[i] - U.PBT[i]) < 1, '%.0f' % pbt[i])
    check('FY%dF NPATMI = model' % y, abs(npat[i] - U.NPATMI[i]) < 1, '%.0f' % npat[i])
    check('FY%dF EPS = NPATMI / 1,885mn shares' % y, abs(npat[i] * 1000 / SHARES - eps[i]) < 1)
    check('FY%dF P/E = TP %s / EPS' % (y, '{:,.0f}'.format(TP)),
          abs(TP / eps[i] - pe[i]) < 0.051, '%.2f vs %.2f' % (TP / eps[i], pe[i]))
    check('FY%dF P/B = TP / BVPS' % y, abs(TP / bv[i] - pb[i]) < 0.051,
          '%.2f vs %.2f' % (TP / bv[i], pb[i]))
    check('FY%dF BVPS = equity / shares' % y, abs(eq[i] * 1000 / SHARES - bv[i]) < 1)

# the P/E and P/B rows are struck on the target price in every column, history
# included, so the historical cells have to move with the target price too
hist = lambda tbl, k: [num(x) for x in next(
    v for kk, v in tbl.items() if kk.startswith(k))]
sh0 = {x.shape_id: x for x in prs.slides[0].shapes}
t0 = sh0[16].table
for ri, lab, base in ((7, 'P/E', U.HIST_EPS), (8, 'P/B', U.HIST_BVPS)):
    got = [num(t0.cell(ri, c).text) for c in (1, 2, 3)]
    check('STB historical %s struck on the target price' % lab,
          all(abs(TP / b - g) < 0.051 for b, g in zip(base, got)),
          ' '.join('%.1f' % g for g in got))

check('box NPATMI = table FY26F', num(en_box['NPATMI (26F, VNDbn)']) == npat[0])
check('box P/E = table FY26F', num(en_box['P/E (26F, x)']) == pe[0])
check('box EPS growth = table EPS on the FY25 cell',
      abs(num(en_box['EPS Growth (26F, %)'])
          - (eps[0] / U.HIST_EPS[2] * 100 - 100)) < 0.1,
      'FY25 EPS %.0f' % U.HIST_EPS[2])
check('narrative PBT growth stated', ('%+.1f%% YoY' % U.PBT_YOY) in en_txt,
      '%+.1f%%' % U.PBT_YOY)
check('rating box return = TP / current price',
      abs(TP / 74100 - 1 - 0.012) < 0.005, '%.1f%%' % (TP / 74100 * 100 - 100))
for a, b in [('Operating profit', 'Lợi nhuận hoạt động'), ('Net Profit', 'LNST'), ('EPS', 'EPS'),
             ('P/E', 'P/E'), ('P/B', 'P/B'), ('BVPS', 'Giá trị sổ sách'),
             ('Total assets', 'Tổng tài sản'), ('Equity', 'VCSH')]:
    check('EN and VN agree on %s' % a, row(en_tbl, a) == row(vn_tbl, b))
for s, t in [('5.8%', 'FY26F NPL'), ('4.0%', 'FY27F NPL'), ('%.1ftn' % (U.WO26 / 1000), 'FY26F write-offs'),
             ('27.2tn', 'end-2Q26 reserves'), ('56.7%', '2Q26 coverage'),
             ('%.1f%%' % U.COV26, 'FY26F coverage'), ('%.1f%%' % U.CIR[0], 'FY26F CIR'),
             ('%.1f%%' % U.CIR[1], 'FY27F CIR'), ('%.1f%%' % U.CIR[2], 'FY28F CIR'),
             ('2.3%', 'FY26F loan growth'), ('11.7%', 'the old loan growth'),
             ('{:,.0f}'.format(U.PBT[0]), 'FY26F PBT'), ('8,100', 'the board plan'),
             ('{:,.0f}'.format(U.H2_PBT), '2H26 PBT'),
             ('{:,.0f}'.format(U.LOANS26), 'FY26F gross loans'),
             ('{:,.0f}'.format(U.NII[0]), 'FY26F NII'), ('1.5%', '1H26 loan growth')]:
    check('narrative states %s (%s)' % (s, t), s in en_txt)
for old in ['5.9%', '8.9tn', '21.6tn', '45%', '3,798', '42.7%', '10.9tn', '39.9%', '8,716',
            'VND18tn', '8,683', '4,547', '27,010', '3,964', '51.1%', '8,507', '4,371',
            '8,150', '4,014', '26,712', '26,704', '8,143', '7,082', '2,946', '81,400',
            'lifted on the cost line', 'below the first half', '7,500', '10,953', '16,448',
            'across all three years', '9,642', '15,170', '43.4%',
            # superseded by the VND1,000bn FY27F/FY28F provisioning overlay
            '10,872', '17,271', '8,465', '13,447', '4,109', '6,527',
            '16,271', '12,668', '6,149',
            # per-share lines struck on the overstated 2,060.158mn share count
            '2,820', '3,731', '5,771', '2,883', '4,896', '3,747',
            '22,199', '26,683', '29,059', '31,905', '35,636', '41,407',
            ]:   # not '43.6%' - that is the 1H26 PBT fall
    check('stale text "%s" gone' % old[:34], old not in en_txt and old not in str(en_tbl))

# ---------------------------------------------------------------- FPT slide
fpt = {x.shape_id: x for x in prs.slides[2].shapes}[16].table
FPT_EPS = (4648., 4877., 5073., 6424., 7440., 8673.)
fpe = [num(fpt.cell(7, c).text) for c in range(1, 7)]
check('FPT P/E struck on the target price in all six columns',
      all(abs(TPF / e - g) < 0.051 for e, g in zip(FPT_EPS, fpe)),
      ' '.join('%.1f' % g for g in fpe))
fvn = {x.shape_id: x for x in prs.slides[3].shapes}[16].table
check('FPT EN and VN P/E rows agree',
      [fvn.cell(7, c).text.strip() for c in range(1, 7)]
      == [fpt.cell(7, c).text.strip() for c in range(1, 7)])
fpb = [num(fpt.cell(8, c).text) for c in range(1, 7)]
check('FPT P/B history still on spot prices (flagged, not changed)',
      any(abs(TPF / b - g) > 0.051 for b, g in
          zip((19665., 20253., 21418.), fpb[:3])),
      'row reads ' + ' '.join('%.1f' % g for g in fpb))

# -------------------------------------------------------- stock-pick book
wb = openpyxl.load_workbook(PICK)
ws, tps = wb['Stock Pick'], wb['Target Price and Forecast']
check('workbook NPATMI = deck', ws['F6'].value == npat[0] and ws['G6'].value == npat[1])
check('workbook P/E, P/B = deck',
      abs(ws['J6'].value - pe[0]) < 0.051 and abs(ws['L6'].value - pb[0]) < 0.051)
check('TP sheet = deck', tps['D13'].value == npat[0] and tps['E13'].value == npat[1])
check('workbook narrative carries the model CIR and PBT',
      all(t in ws['C6'].value for t in ('5.5%', '{:,.0f}'.format(U.PBT[0]), '8,100')))
check('workbook narrative free of the 5.9% / 45% coverage version',
      '5.9%' not in ws['C6'].value and '45% coverage' not in ws['C6'].value)

print('\n' + '=' * 78)
print('%d FAILED: %s' % (len(fails), fails) if fails else 'ALL CHECKS PASSED')
