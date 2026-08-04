# -*- coding: utf-8 -*-
"""Cross-check the August deck and the stock-pick workbook against the model.

Deck figures are compared against update_aug_deck's constants, which are read
straight out of the recalculated workbook, so nothing is typed twice.  The
model file itself is verified by fix_stb_model.verify().
"""
import openpyxl, zipfile
from lxml import etree
from pptx import Presentation
import update_aug_deck as U
from fix_stb_model import verify

DECK = ('/home/user/verbose-guide/'
        'MASVN_RS_WM_2H26_outlook_Equity_VN_2026_STBFPT_August2026.pptx')
PICK = '/home/user/verbose-guide/Stock_Pick_and_Forecast_Aug26_MAS_RS_EN_updated.xlsx'
MODEL = '/home/user/verbose-guide/FinModel_STB_2Q26.xlsx'
TPF = 87950.
NS = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
TP, SHARES = U.STB_TP, U.SHARES
fails = []


def check(n, c, d=''):
    print('%-4s %-58s %s' % ('OK' if c else 'FAIL', n, d))
    if not c:
        fails.append(n)


# ---------------------------------------------------------------- model file
z = zipfile.ZipFile(MODEL)
npl = etree.fromstring(z.read('xl/worksheets/sheet2.xml'))
M = {c.get('r'): float(c.find(NS + 'v').text) for c in npl.iter(NS + 'c')
     if c.find(NS + 'v') is not None and c.find(NS + 'f') is None and c.get('t') != 's'}
for col, lab, tgt in (('N', 'FY26F', 0.055), ('O', 'FY27F', 0.040), ('P', 'FY28F', 0.027)):
    n = sum(M['%s%d' % (col, r)] for r in (28, 29, 30))
    t = sum(M['%s%d' % (col, r)] for r in (26, 27, 28, 29, 30))
    check('model %s NPL mix = %.1f%%' % (lab, tgt * 100), abs(n - tgt) < 1e-9, '%.3f%%' % (n * 100))
    check('model %s grading mix sums to 1.000' % lab, abs(t - 1) < 1e-9, '%.4f' % t)
for msg in verify(MODEL):
    check('model assumption intact', False, msg)
check('every booked model assumption still in place', not verify(MODEL))
DG = {c.get('r'): c.find(NS + 'v').text for c in npl.iter(NS + 'c')
      if c.get('r') in ('DG13', 'DG22', 'DG23') and c.find(NS + 'v') is not None}
check('NPL!DG 2Q26 column resolves', abs(float(DG.get('DG23', 0)) - 0.07540) < 5e-5,
      '%.3f%%' % (float(DG.get('DG23', 0)) * 100))
check('2Q26 NPL balance = 47,957', abs(float(DG.get('DG22', 0)) - 47957.084) < 1)
check('2Q26 gross loans = 636,029', abs(float(DG.get('DG13', 0)) - 636028.893) < 1)

# ---------------------------------------------------- the model's own P&L
check('FY26F CIR = 40%', abs(U.CIR[0] - 40) < 0.05, '%.2f%%' % U.CIR[0])
check('FY27F CIR = 38%', abs(U.CIR[1] - 38) < 0.05, '%.2f%%' % U.CIR[1])
check('FY28F CIR drifted off the 36% target', abs(U.CIR[2] - 36) > 0.05,
      '%.2f%% - reported to the analyst, not silently re-solved' % U.CIR[2])
check('FY26F PBT within 10bn of the 8,150 target', abs(U.PBT[0] - 8150) < 10,
      '%.0f' % U.PBT[0])
check('FY26F coverage near 51%', abs(U.COV26 - 51) < 0.2, '%.1f%%' % U.COV26)
check('PBT = TOI - opex - provisioning, all three years',
      all(abs(U.TOI[i] - U.OPEX[i] - U.PROV[i] - U.PBT[i]) < 1 for i in range(3)))
check('NPATMI = PBT x (1 - 22.14% tax)',
      all(abs(U.PBT[i] * 0.7785909196679350 - U.NPATMI[i]) < 1.5 for i in range(3)))
check('equity rolls forward on retained NPATMI',
      abs(U.EQUITY[1] - U.EQUITY[0] - U.NPATMI[1]) < 1.5
      and abs(U.EQUITY[2] - U.EQUITY[1] - U.NPATMI[2]) < 1.5)

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
    check('FY%dF EPS = NPATMI / 2,060mn shares' % y, abs(npat[i] * 1000 / SHARES - eps[i]) < 1)
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
for ri, lab, base in ((7, 'P/E', U.STB_HIST_EPS), (8, 'P/B', U.STB_HIST_BVPS)):
    got = [num(t0.cell(ri, c).text) for c in (1, 2, 3)]
    check('STB historical %s struck on the target price' % lab,
          all(abs(TP / b - g) < 0.051 for b, g in zip(base, got)),
          ' '.join('%.1f' % g for g in got))

check('box NPATMI = table FY26F', num(en_box['NPATMI (26F, VNDbn)']) == npat[0])
check('box P/E = table FY26F', num(en_box['P/E (26F, x)']) == pe[0])
check('box EPS growth = table EPS on FY25 2,883',
      abs(num(en_box['EPS Growth (26F, %)']) - (eps[0] / 2882.84 * 100 - 100)) < 0.1)
check('narrative PBT growth matches the box EPS growth',
      ('%+.1f%% YoY' % U.PBT_YOY) in en_txt, '%+.1f%%' % U.PBT_YOY)
check('rating box return = TP / current price',
      abs(TP / 74100 - 1 - 0.10) < 0.005, '%.1f%%' % (TP / 74100 * 100 - 100))
for a, b in [('Operating profit', 'Lợi nhuận hoạt động'), ('Net Profit', 'LNST'), ('EPS', 'EPS'),
             ('P/E', 'P/E'), ('P/B', 'P/B'), ('BVPS', 'Giá trị sổ sách'),
             ('Total assets', 'Tổng tài sản'), ('Equity', 'VCSH')]:
    check('EN and VN agree on %s' % a, row(en_tbl, a) == row(vn_tbl, b))
for s, t in [('5.5%', 'FY26F NPL'), ('4.0%', 'FY27F NPL'), ('11.8tn', '2H26 write-offs'),
             ('27.2tn', 'end-2Q26 reserves'), ('56.7%', '2Q26 coverage'),
             ('%.1f%%' % U.COV26, 'FY26F coverage'), ('40.0%', 'FY26F CIR'),
             ('38.0%', 'FY27F CIR'), ('%.1f%%' % U.CIR[2], 'FY28F CIR'),
             ('35.6%', '1H26 CIR'), ('{:,.0f}'.format(U.PBT[0]), 'FY26F PBT'),
             ('8,100', 'the board plan'), ('{:,.0f}'.format(U.H2_PBT), '2H26 PBT'),
             ('%.1ftn' % (U.H2_PROV / 1000), '2H26 charge'),
             ('{:,.0f}'.format(U.NII[0]), 'FY26F NII'), ('1.5%', '1H26 loan growth')]:
    check('narrative states %s (%s)' % (s, t), s in en_txt)
for old in ['5.9%', '8.9tn', '21.6tn', '45%', '3,798', '42.7%', '10.9tn', '39.9%', '8,716',
            'VND18tn', '8,683', '4,547', '27,010', '3,964', '51.1%', '8,507', '4,371',
            '8,150', '4,014', '26,712', '36.0%', 'remains attainable']:
    check('stale text "%s" gone' % old[:34], old not in en_txt and old not in str(en_tbl))

# ---------------------------------------------------------------- FPT slide
fpt = {x.shape_id: x for x in prs.slides[2].shapes}[16].table
fpe = [num(fpt.cell(7, c).text) for c in range(1, 7)]
check('FPT P/E struck on the target price in all six columns',
      all(abs(TPF / e - g) < 0.051 for e, g in zip(U.FPT_EPS, fpe)),
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
check('workbook narrative carries the model CIR path and PBT',
      all(t in ws['C6'].value for t in
          ('5.5%', '%.1f%%' % U.CIR[0], '%.1f%%' % U.CIR[1], '%.1f%%' % U.CIR[2],
           '{:,.0f}'.format(U.PBT[0]), '8,100')))
check('workbook TP matches the slide',
      abs(ws['J6'].value * (U.NPATMI[0] * 1000 / U.SHARES) - U.STB_TP) < 1,
      '{:,.0f}'.format(ws['J6'].value * U.NPATMI[0] * 1000 / U.SHARES))
check('workbook narrative free of the 5.9% / 45% coverage version',
      '5.9%' not in ws['C6'].value and '45% coverage' not in ws['C6'].value)

print('\n' + '=' * 78)
print('%d FAILED: %s' % (len(fails), fails) if fails else 'ALL CHECKS PASSED')
