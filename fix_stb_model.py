# -*- coding: utf-8 -*-
"""STB model edits, rebuilt from the analyst's latest upload each run.

The base is now 2b63c432-FinModel_STB_2Q26.xlsx, which is the previous round's
work after the analyst opened it in Excel (so every formula is recalculated,
not cached) and pasted the Q2/2026 actuals into Notes(Quarter).  The earlier
NPL-mix, allowance and write-off edits are already inside it and are asserted
here rather than re-applied - re-applying them from the original pristine file
would wipe the analyst's Q2/2026 work.

This round does two things:

  NPL!DG6:DG11   the 2Q26 quarterly column pointed at 'Notes(Quarter)'!BY,
                 which is empty.  The Q2/2026 actuals landed in BX - the
                 analyst's column insert put a label column at BW - so every
                 cell below DG13 was returning 0 or #DIV/0!.  Everything else
                 in that column is already wired as shared formulas off DF, so
                 six links are the whole fix.

  Model!Y132/Y134/Z132/Z134/AA132/AA134   the opex multipliers, re-solved.
                 Excel's recalculation moved total operating income: the larger
                 loan-loss reserve booked last round cuts net loans, so
                 interest income falls.  TOI came out at 32,662/36,943/42,126
                 against the 32,956/36,613/42,682 the previous multipliers were
                 solved against, which left CIR at 40.36/37.66/36.48% instead
                 of the 40/38/36% asked for.

Recalculation also settled two open items: Model!Y103 (the balance check) came
back 0, so the reserve restatement did NOT break the balance sheet as I warned,
and Y286 landed on 18,973 - coverage 50.0% - exactly as forecast.
"""
import shutil, zipfile
from lxml import etree

SRC = '/home/user/verbose-guide/FinModel_STB_2Q26.xlsx'
PRISTINE = ('/root/.claude/uploads/041665b7-4ff3-507f-a1e8-7a7ed4160156/'
            '2b63c432-FinModel_STB_2Q26.xlsx')
NS = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'

# sheet2 = NPL.  (expected_formula, new_formula, note)
NPL_EDITS = {
    'DG%d' % r: ("'Notes(Quarter)'!BY%d" % (75 + r), "'Notes(Quarter)'!BX%d" % (75 + r), note)
    for r, note in ((6, 'total loans     636,029'), (7, 'Current         571,245'),
                    (8, 'Special ment.    16,827'), (9, 'Substandard       7,200'),
                    (10, 'Doubtful          8,483'), (11, 'Bad              32,274'))
}

# sheet1 = Model.  (expected_formula, new_formula, note)
MODEL_EDITS = {
    'Y132': ('X132*1',       'X132*0.9886',  'FY26F staff cost      -> CIR 40.0%'),
    'Y134': ('X134*1',       'X134*0.9886',  'FY26F other opex      -> CIR 40.0%'),
    'Z132': ('Y132*1.015',   'Y132*1.039',   'FY27F staff cost      -> CIR 38.0%'),
    'Z134': ('Y134*1.015',   'Y134*1.039',   'FY27F other opex      -> CIR 38.0%'),
    'AA132': ('Z132*1.106',  'Z132*1.0739',  'FY28F staff cost      -> CIR 36.0%'),
    'AA134': ('Z134*1.106',  'Z134*1.0739',  'FY28F other opex      -> CIR 36.0%'),
}

# Already booked in the upload - asserted, never re-applied.
ALREADY = {
    'NPL': {'N26': 0.933, 'N27': 0.012, 'N28': 0.009, 'N29': 0.012, 'N30': 0.034,
            'O26': 0.950, 'O27': 0.010, 'O28': 0.007, 'O29': 0.010, 'O30': 0.023,
            'P26': 0.965},
    'Model': {'X284': 16078.433, 'Y287': -0.0171},
}
ALREADY_F = {'Y278': '-Y279*0.85'}


def edit_sheet(data, edits, label, check_vals=None, check_f=None):
    root = etree.fromstring(data)
    log, seen = [], set()
    for c in root.iter(NS + 'c'):
        ref = c.get('r')
        f, v = c.find(NS + 'f'), c.find(NS + 'v')
        if check_vals and ref in check_vals:
            assert abs(float(v.text) - check_vals[ref]) < 1e-9, \
                ('%s!%s drifted' % (label, ref), v.text, check_vals[ref])
        if check_f and ref in check_f:
            assert f is not None and f.text == check_f[ref], ('%s!%s drifted' % (label, ref),)
        if ref not in edits:
            continue
        seen.add(ref)
        ef, nf, note = edits[ref]
        assert f is not None and f.text == ef, (ref, f.text if f is not None else None, ef)
        log.append('%s!%-6s %-34s %-24s -> %s' % (label, ref, note, ef, nf))
        f.text = nf
        if v is not None:            # drop the stale cache so a blank cell is obvious
            v.getparent().remove(v)
    missing = set(edits) - seen
    assert not missing, missing
    return etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True), log


def main():
    shutil.copy(PRISTINE, SRC)
    z = zipfile.ZipFile(SRC)
    items = [(i, z.read(i.filename)) for i in z.infolist()]
    z.close()
    log, out = [], []
    for it, d in items:
        if it.filename == 'xl/worksheets/sheet2.xml':
            d, l = edit_sheet(d, NPL_EDITS, 'NPL', ALREADY['NPL']); log += l + ['']
        elif it.filename == 'xl/worksheets/sheet1.xml':
            d, l = edit_sheet(d, MODEL_EDITS, 'Model', ALREADY['Model'], ALREADY_F); log += l + ['']
        elif it.filename == 'xl/workbook.xml' and 'fullCalcOnLoad' not in d.decode():
            d = d.decode().replace('<calcPr ', '<calcPr fullCalcOnLoad="1" ').encode()
            log.append('workbook.xml: fullCalcOnLoad=1')
        out.append((it, d))
    zo = zipfile.ZipFile(SRC, 'w', zipfile.ZIP_DEFLATED)
    for it, d in out:
        zo.writestr(it, d)
    zo.close()
    print('\n'.join(log))


# ---------------------------------------------------------------- cascade
# Replays the model's formula chain so the deck can be written before the
# workbook is reopened.  Every constant below is now an Excel-recalculated
# value read out of the upload, not a stale cache.
TOI = {26: 32662.3, 27: 36942.6, 28: 42126.4}          # Model!Y117 = NII + fee + other
DA = {26: 2880.14265, 27: 3456.17118, 28: 3801.788298}  # Model!Y133, untouched
PROV = {26: 11090.7, 27: 8228.8, 28: 5816.0}            # Model!Y254
RESERVE = {26: 18973.3, 27: 19703.2, 28: 20567.0}       # Model!Y286
LOANS = {26: 689832.31655949343, 27: 791226.94267949986, 28: 908671.50802756927}
MIX = {  # current, special mention, G3, G4, G5
    26: (0.933, 0.012, 0.009, 0.012, 0.034),
    27: (0.950, 0.010, 0.007, 0.010, 0.023),
    28: (0.965, 0.008, 0.005, 0.009, 0.013),
}
OPEX_X = {26: 0.9886, 27: 1.039, 28: 1.0739}   # applied to staff and other alike
STAFF_25, OTHER_25 = 6985.597, 3316.289
WO_RATE = {26: 0.0171, 27: 0.009, 28: 0.005}
TAX = 0.22140908033206499


def cascade():
    so = STAFF_25 + OTHER_25
    rows, prev = [], None
    for y in (26, 27, 28):
        so *= OPEX_X[y]
        opex = so + DA[y]
        pbt = TOI[y] - opex - PROV[y]
        npl_amt = sum(MIX[y][2:]) * LOANS[y]
        rows.append(dict(
            y=2000 + y, toi=TOI[y], opex=opex, cir=opex / TOI[y],
            ppop=TOI[y] - opex, prov=PROV[y], pbt=pbt, npatmi=pbt * (1 - TAX),
            npl_pct=sum(MIX[y][2:]), npl=npl_amt, wo=WO_RATE[y] * LOANS[y],
            res=RESERVE[y], cov=RESERVE[y] / npl_amt))
        prev = rows[-1]
    return rows


if __name__ == '__main__':
    main()
    print()
    hdr = ('%-26s' + '%14s' * 3) % ('', 'FY26F', 'FY27F', 'FY28F')
    print(hdr); print('-' * len(hdr))
    r = cascade()
    for lab, k, pct in [('Total operating income', 'toi', 0),
                        ('Operating expense', 'opex', 0),
                        ('  CIR', 'cir', 1),
                        ('PPOP', 'ppop', 0),
                        ('Provisioning', 'prov', 0),
                        ('PBT', 'pbt', 0),
                        ('NPATMI', 'npatmi', 0),
                        ('NPL ratio', 'npl_pct', 1),
                        ('  NPL balance', 'npl', 0),
                        ('  write-off', 'wo', 0),
                        ('  loan-loss reserve', 'res', 0),
                        ('  coverage', 'cov', 1)]:
        cells = [format(x[k] * 100, '13.1f') + '%' if pct else format(x[k], '14,.0f')
                 for x in r]
        print(('%-26s' % lab) + ''.join(cells))
