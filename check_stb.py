# -*- coding: utf-8 -*-
"""Cross-check the STB slides and the stock-pick workbook against the model.

The deck is validated against fix_stb_model.cascade(), which replays the
model's own formula chain in Python, rather than against numbers typed twice.
"""
import openpyxl, zipfile
from lxml import etree
from pptx import Presentation
from fix_stb_model import cascade, NPL_EDITS, MODEL_EDITS, ALREADY, ALREADY_F

DECK = '/home/user/verbose-guide/MASVN_RS_WM_2H26_outlook_Equity_VN_2026_STBFPT_31July2026.pptx'
PICK = '/home/user/verbose-guide/Stock_Pick_and_Forecast_Aug26_MAS_RS_EN_updated.xlsx'
MODEL = '/home/user/verbose-guide/FinModel_STB_2Q26.xlsx'
NS = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
TP, SHARES, EQ25 = 77800., 2060.158, 59920.157
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
for ref, exp in ALREADY['NPL'].items():
    check('NPL!%s still %s' % (ref, exp), abs(M[ref] - exp) < 1e-9, '%.3f' % M[ref])
for col, lab, tgt in (('N', 'FY26F', 0.055), ('O', 'FY27F', 0.040), ('P', 'FY28F', 0.027)):
    n = sum(M['%s%d' % (col, r)] for r in (28, 29, 30))
    t = sum(M['%s%d' % (col, r)] for r in (26, 27, 28, 29, 30))
    check('model %s NPL mix = %.1f%%' % (lab, tgt * 100), abs(n - tgt) < 1e-9, '%.3f%%' % (n * 100))
    check('model %s grading mix sums to 1.000' % lab, abs(t - 1) < 1e-9, '%.4f' % t)

mdl = {}
WANT = set(MODEL_EDITS) | set(ALREADY['Model']) | set(ALREADY_F)
for ev, el in etree.iterparse(z.open('xl/worksheets/sheet1.xml'), events=('end',)):
    if el.tag != NS + 'c':
        continue
    if el.get('r') in WANT:
        f, v = el.find(NS + 'f'), el.find(NS + 'v')
        mdl[el.get('r')] = (f.text if f is not None else None,
                            v.text if v is not None else None)
    el.clear()
for ref, (ef, nf, note) in MODEL_EDITS.items():
    check('Model!%s booked' % ref, mdl.get(ref, (None,))[0] == nf, nf)
for ref, exp in ALREADY['Model'].items():
    check('Model!%s still %s' % (ref, exp), abs(float(mdl[ref][1]) - exp) < 1e-9)
for ref, exp in ALREADY_F.items():
    check('Model!%s still =%s' % (ref, exp), mdl[ref][0] == exp)
npl_dg = {}
for ev, el in etree.iterparse(z.open('xl/worksheets/sheet2.xml'), events=('end',)):
    if el.tag != NS + 'c':      # clearing an <f> wipes its text before <c> ends
        continue
    if el.get('r') in NPL_EDITS:
        f = el.find(NS + 'f')
        npl_dg[el.get('r')] = f.text if f is not None else None
    el.clear()
for ref, (ef, nf, note) in NPL_EDITS.items():
    check('NPL!%s -> Q2/2026 actuals (%s)' % (ref, note.split()[0]), npl_dg.get(ref) == nf)
check('workbook set to recalculate on open',
      'fullCalcOnLoad="1"' in z.read('xl/workbook.xml').decode())

# ------------------------------------------------------------- the cascade
C = {c['y']: c for c in cascade()}
for y, tgt in ((2026, 0.40), (2027, 0.38), (2028, 0.36)):
    check('FY%dF CIR = %.0f%% as instructed' % (y, tgt * 100),
          abs(C[y]['cir'] - tgt) < 0.0005, '%.2f%%' % (C[y]['cir'] * 100))
check('CIR declines year on year', C[2026]['cir'] > C[2027]['cir'] > C[2028]['cir'])
check('FY26F coverage held at 50%', abs(C[2026]['cov'] - 0.50) < 0.005,
      '%.1f%%' % (C[2026]['cov'] * 100))
check('FY26F NPL = 5.5%', abs(C[2026]['npl_pct'] - 0.055) < 1e-9)
check('FY26F PBT = 5% above the ~8,100 board-approved plan',
      abs(C[2026]['pbt'] / 8100 - 1.05) < 0.002, '%.0f = plan +%.1f%%, +%.1f%% YoY'
      % (C[2026]['pbt'], C[2026]['pbt'] / 81 - 100, C[2026]['pbt'] / 7628.025 * 100 - 100))
check('2H26 opex above 1H26 actual of 6,233 (no back-end cost cut)',
      C[2026]['opex'] - 6233.19 > 6233.19, '+%.1f%%' % ((C[2026]['opex'] - 6233.19) / 6233.19 * 100 - 100))
check('2H26 write-off leaves NPL formation positive but slower than 1H26',
      0 < C[2026]['wo'] - (47957 - C[2026]['npl']) < 7800,
      'implied 2H26 formation %.0f vs 7,800 in 1H26' % (C[2026]['wo'] - (47957 - C[2026]['npl'])))

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

for i, y in enumerate((2026, 2027, 2028)):
    check('FY%dF PBT = model cascade' % y, abs(pbt[i] - C[y]['pbt']) < 1,
          '%.0f vs %.0f' % (pbt[i], C[y]['pbt']))
    check('FY%dF NPATMI = model cascade' % y, abs(npat[i] - C[y]['npatmi']) < 1,
          '%.0f vs %.0f' % (npat[i], C[y]['npatmi']))
    check('FY%dF EPS = NPATMI / 2,060mn shares' % y, abs(npat[i] * 1000 / SHARES - eps[i]) < 1)
    check('FY%dF P/E = TP / EPS' % y, abs(TP / eps[i] - pe[i]) < 0.051,
          '%.2f vs %.2f' % (TP / eps[i], pe[i]))
    check('FY%dF P/B = TP / BVPS' % y, abs(TP / bv[i] - pb[i]) < 0.051,
          '%.2f vs %.2f' % (TP / bv[i], pb[i]))
    check('FY%dF BVPS = equity / shares' % y, abs(eq[i] * 1000 / SHARES - bv[i]) < 1)
check('equity rolls forward on retained NPATMI',   # 1.5 absorbs rounded rows
      abs(eq[0] - (EQ25 + npat[0])) < 1.5 and abs(eq[1] - (eq[0] + npat[1])) < 1.5
      and abs(eq[2] - (eq[1] + npat[2])) < 1.5)
check('box NPATMI = table FY26F', num(en_box['NPATMI (26F, VNDbn)']) == npat[0])
check('box P/E = table FY26F', num(en_box['P/E (26F, x)']) == pe[0])
check('box EPS growth = table EPS on FY25 2,883',
      abs(num(en_box['EPS Growth (26F, %)']) - (eps[0] / 2882.84 * 100 - 100)) < 0.1)
for a, b in [('Operating profit', 'Lợi nhuận hoạt động'), ('Net Profit', 'LNST'), ('EPS', 'EPS'),
             ('P/E', 'P/E'), ('P/B', 'P/B'), ('BVPS', 'Giá trị sổ sách'),
             ('Total assets', 'Tổng tài sản'), ('Equity', 'VCSH')]:
    check('EN and VN agree on %s' % a, row(en_tbl, a) == row(vn_tbl, b))
for s, t in [('5.5%', 'FY26F NPL'), ('4.0%', 'FY27F NPL'), ('11.8tn', '2H26 write-offs'),
             ('27.2tn', 'end-2Q26 reserves'), ('56.7%', '2Q26 coverage'),
             ('50.0%', 'FY26F coverage'), ('40.0%', 'FY26F CIR'), ('38.0%', 'FY27F CIR'),
             ('36.0%', 'FY28F CIR'), ('35.6%', '1H26 CIR'),
             ('8,507', 'FY26F PBT'), ('8,100', 'the board plan'), ('4,371', '2H26 PBT'),
             ('1.5%', '1H26 loan growth')]:
    check('narrative states %s (%s)' % (s, t), s in en_txt)
# 7,934 survives on purpose - the narrative now cites it as the prior forecast
for old in ['5.9%', '8.9tn', '21.6tn', '45%', '3,798', '42.7%', '10.9tn', '39.9%', '8,716',
            'VND18tn', '8,683', '4,547', '27,010', '3,964', '51.1%', 'remains attainable']:
    check('stale text "%s" gone' % old[:34], old not in en_txt and old not in str(en_tbl))

# -------------------------------------------------------- stock-pick book
wb = openpyxl.load_workbook(PICK)
ws, tps = wb['Stock Pick'], wb['Target Price and Forecast']
check('workbook NPATMI = deck', ws['F6'].value == npat[0] and ws['G6'].value == npat[1])
check('workbook P/E, P/B = deck',
      abs(ws['J6'].value - pe[0]) < 0.051 and abs(ws['L6'].value - pb[0]) < 0.051)
check('TP sheet = deck', tps['D13'].value == npat[0] and tps['E13'].value == npat[1])
check('workbook narrative carries 5.5% and the 40/38/36 CIR path',
      all(t in ws['C6'].value for t in ('5.5%', '40.0%', '38.0%', '36.0%', '8,507', '8,100')))
check('workbook narrative free of the 5.9% / 45% coverage version',
      '5.9%' not in ws['C6'].value and '45% coverage' not in ws['C6'].value)

print('\n' + '=' * 78)
print('%d FAILED: %s' % (len(fails), fails) if fails else 'ALL CHECKS PASSED')
