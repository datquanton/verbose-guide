# -*- coding: utf-8 -*-
"""Install the analyst's latest STB model and assert the booked state.

Every edit this project made is now inside 8ce85368-FinModel_STB_2Q26.xlsx -
the analyst opened it in Excel, so all formulas are recalculated, and re-cut the
FY27F/FY28F write-off rates on top.  Nothing is applied here any more; the
script only copies the upload into place and verifies that the assumptions the
deck rests on are still the ones in the file.

Booked, and asserted below:
  NPL!N/O/P26:30     grading mix -> NPL 5.5% / 4.0% / 2.7%
  NPL!DG6:DG11       2Q26 column wired to 'Notes(Quarter)'!BX81:BX86
  Model!X284         FY25 opening specific allowance restated to 16,078
  Model!Y287         FY26F write-off rate -1.71% (the 50%-coverage solve)
  Model!Y278         specific charge 0.8802x write-off -> FY26F PBT ~8,150
  Model!Y/Z/AA132,134  opex multipliers -> CIR 40 / 38 / 36%

Set by the analyst in this round, not by us:
  Model!Z287 -1.2% (was -0.9%) and AA287 -0.7% (was -0.5%) - heavier FY27F and
  FY28F write-offs, which lift provisioning and cut PBT in both years.
"""
import shutil, zipfile, re
from lxml import etree

SRC = '/home/user/verbose-guide/FinModel_STB_2Q26.xlsx'
PRISTINE = ('/root/.claude/uploads/041665b7-4ff3-507f-a1e8-7a7ed4160156/'
            '8ce85368-FinModel_STB_2Q26.xlsx')
NS = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'

NPL_VALUES = {'N26': 0.933, 'N27': 0.012, 'N28': 0.009, 'N29': 0.012, 'N30': 0.034,
              'O26': 0.950, 'O27': 0.010, 'O28': 0.007, 'O29': 0.010, 'O30': 0.023,
              'P26': 0.965}
NPL_FORMULAS = {'DG%d' % r: "'Notes(Quarter)'!BX%d" % (75 + r) for r in range(6, 12)}
MODEL_VALUES = {'X284': 16078.433, 'Y287': -0.0171}
MODEL_FORMULAS = {'Y278': '-Y279*0.8802',
                  'Y132': 'X132*0.9886', 'Y134': 'X134*0.9886',
                  'Z132': 'Y132*1.039', 'Z134': 'Y134*1.039',
                  'AA132': 'Z132*1.0739', 'AA134': 'Z134*1.0739'}


def read(z, part, refs):
    out = {}
    for ev, el in etree.iterparse(z.open(part), events=('end',)):
        if el.tag != NS + 'c':      # clearing an <f> wipes its text before <c> ends
            continue
        if el.get('r') in refs:
            f, v = el.find(NS + 'f'), el.find(NS + 'v')
            out[el.get('r')] = (f.text if f is not None else None,
                                v.text if v is not None else None)
        el.clear()
    return out


def verify(path=SRC):
    z = zipfile.ZipFile(path)
    bad = []
    npl = read(z, 'xl/worksheets/sheet2.xml', set(NPL_VALUES) | set(NPL_FORMULAS))
    for ref, exp in NPL_VALUES.items():
        if abs(float(npl[ref][1]) - exp) > 1e-9:
            bad.append('NPL!%s = %s, expected %s' % (ref, npl[ref][1], exp))
    for ref, exp in NPL_FORMULAS.items():
        if npl.get(ref, (None,))[0] != exp:
            bad.append('NPL!%s = %s, expected %s' % (ref, npl.get(ref), exp))
    mdl = read(z, 'xl/worksheets/sheet1.xml', set(MODEL_VALUES) | set(MODEL_FORMULAS))
    for ref, exp in MODEL_VALUES.items():
        if abs(float(mdl[ref][1]) - exp) > 1e-9:
            bad.append('Model!%s = %s, expected %s' % (ref, mdl[ref][1], exp))
    for ref, exp in MODEL_FORMULAS.items():
        if mdl.get(ref, (None,))[0] != exp:
            bad.append('Model!%s = %s, expected %s' % (ref, mdl.get(ref), exp))
    return bad


def main():
    shutil.copy(PRISTINE, SRC)
    bad = verify()
    if bad:
        raise SystemExit('model drifted:\n  ' + '\n  '.join(bad))
    print('installed %s' % PRISTINE.rsplit('/', 1)[-1])
    print('%d assumptions verified in place'
          % (len(NPL_VALUES) + len(NPL_FORMULAS) + len(MODEL_VALUES) + len(MODEL_FORMULAS)))


if __name__ == '__main__':
    main()
