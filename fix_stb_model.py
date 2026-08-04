# -*- coding: utf-8 -*-
"""STB model edits, rebuilt from the pristine upload each run.

Two instructions from the analyst:
  (1) hold coverage at ~50%  ->  the reachable FY26F NPL is 5.5%
  (2) CIR should be ~38-40%  ->  the opex build has to come down from 42.9%

Three things had to change to make (1) true inside the model rather than on
the side of it:

  NPL!N26/N29/N30   the FY26F loan-grading mix          -> NPL 5.5%
  Model!X284        FY25 closing specific allowance     -> ties the roll-forward
                    to the actual balance-sheet reserve of 20,056 (the build
                    opened from 8,869, so every coverage ratio downstream of it
                    was meaningless)
  Model!Y287        FY26F write-off rate                -> the 50% coverage solve
  Model!Y278        specific charge / write-off ratio   -> 1.5x to 0.85x, i.e.
                    the clean-up is funded out of the reserve stock, not the
                    P&L.  Leaving it at 1.5x on a write-off that size is what
                    produced the PBT collapse the analyst rejected.

  Model!Y132/Z132/AA132, Y134, AA134   the opex build   -> CIR 39.9/39.9/38.1%

The provisioning line is NOT driven off the grading mix (only the 0.7% general
allowance on Groups 1-4 is); it is write-off rate x gross loans x the charge
ratio.  That is why NPL and PBT can be set independently here.
"""
import shutil, zipfile
from lxml import etree

SRC = '/home/user/verbose-guide/FinModel_STB_2Q26.xlsx'
PRISTINE = ('/root/.claude/uploads/041665b7-4ff3-507f-a1e8-7a7ed4160156/'
            'f6576dae-FinModel_STB_2Q26.xlsx')
NS = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'

# sheet2 = NPL.  Hardcoded grading mix; M/N/O/P = 2025/2026F/2027F/2028F.
NPL_EDITS = {
    'N26': ('0.9429999999999999',   '0.933', 'Current'),
    'N27': ('1.2E-2',               '0.012', 'Special mention'),
    'N28': ('5.0000000000000001E-3', '0.009', 'Substandard'),
    'N29': ('5.0000000000000001E-3', '0.012', 'Doubtful'),
    'N30': ('3.5000000000000003E-2', '0.034', 'Bad          -> NPL 5.5%'),
    'O26': ('0.96199999999999997',  '0.950', 'Current'),
    'O27': ('0.01',                 '0.010', 'Special mention'),
    'O28': ('4.0000000000000001E-3', '0.007', 'Substandard'),
    'O29': ('8.9999999999999993E-3', '0.010', 'Doubtful'),
    'O30': ('1.7999999999999999E-2', '0.023', 'Bad          -> NPL 4.0%'),
    'P26': ('0.96799999999999997',  '0.965', 'Current      - mix summed to 1.003'),
}

# sheet1 = Model.  (expected_formula, new_formula, expected_value, new_value, note)
MODEL_EDITS = {
    'X284': (None,        None,           '4891.143',  '16078.433',
             'FY25 closing specific allowance -> reserve stock ties to 20,056'),
    'Y287': (None,        None,           '-9.4999999999999998E-3', '-0.0171',
             'FY26F write-off rate -> 11,796bn, the 50% coverage solve'),
    'Y278': ('-Y279*1.5', '-Y279*0.85',   None, None,
             'specific charge 0.85x write-off: reserve-funded clean-up'),
    'Y132': ('Y1010',     'X132*1',       None, None,
             'FY26F staff cost flat vs FY25 (1H26 actual opex is -4.4% YoY)'),
    'Y134': ('X134*1.05', 'X134*0.99',    None, None,
             'FY26F other opex -1%: workout/collection costs roll off'),
    'Z132': ('Z1010',     'Y132*1.08',    None, None, 'FY27F staff cost +8%'),
    'AA132': ('AA1010',   'Z132*1.1',     None, None, 'FY28F staff cost +10%'),
    'AA134': ('Z134*1.1', 'Z134*1.15',    None, None,
              'FY28F other opex +15%: re-investment once the book is clean'),
}


def edit_sheet(data, edits, kind):
    root = etree.fromstring(data)
    log, seen = [], set()
    for c in root.iter(NS + 'c'):
        ref = c.get('r')
        if ref not in edits:
            continue
        seen.add(ref)
        f, v = c.find(NS + 'f'), c.find(NS + 'v')
        if kind == 'npl':
            exp, new, note = edits[ref]
            assert f is None, '%s is a formula, not an input' % ref
            assert abs(float(v.text) - float(exp)) < 1e-9, (ref, v.text, exp)
            log.append('NPL!%-5s %-34s %-9s -> %s' % (ref, note, v.text[:8], new))
            v.text = new
        else:
            ef, nf, ev, nv, note = edits[ref]
            if ef is not None:
                assert f is not None and f.text == ef, (ref, f.text if f is not None else None, ef)
                log.append('Model!%-5s %-52s %-11s -> %s' % (ref, note, ef, nf))
                f.text = nf
            else:
                assert f is None, '%s is a formula, not an input' % ref
                assert abs(float(v.text) - float(ev)) < 1e-9, (ref, v.text, ev)
                log.append('Model!%-5s %-52s %-11s -> %s' % (ref, note, v.text[:10], nv))
                v.text = nv
    missing = set(edits) - seen
    assert not missing, missing
    return etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True), log


def main():
    shutil.copy(PRISTINE, SRC)
    z = zipfile.ZipFile(SRC)
    items = [(i, z.read(i.filename)) for i in z.infolist()]
    z.close()
    log = []
    out = []
    for it, d in items:
        if it.filename == 'xl/worksheets/sheet2.xml':
            d, l = edit_sheet(d, NPL_EDITS, 'npl'); log += l + ['']
        elif it.filename == 'xl/worksheets/sheet1.xml':
            d, l = edit_sheet(d, MODEL_EDITS, 'model'); log += l + ['']
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
# Replicates the model's own formula chain so the deck can be written before
# the workbook is reopened in Excel.  Constants are the cached values of the
# cells this script does not touch.
LOANS = {26: 689832.31655949343, 27: 791226.94267949986, 28: 908671.50802756927}
MIX = {  # current, special mention, G3, G4, G5
    26: (0.933, 0.012, 0.009, 0.012, 0.034),
    27: (0.950, 0.010, 0.007, 0.010, 0.023),
    28: (0.965, 0.008, 0.005, 0.009, 0.013),
}
TOI = {26: 32955.812621392045, 27: 36612.517794481700, 28: 42682.200157502680}
DA = {26: 2880.14265, 27: 3456.17118, 28: 3801.788298}
VAMC = {26: 376.87515392913338, 27: 398.7337926368582, 28: 421.98685138109613}
WO_RATE = {26: 0.0171, 27: 0.009, 28: 0.005}
CHARGE_X = {26: 0.85, 27: 1.0, 28: 1.0}
GEN_OPEN_25, SPEC_OPEN_26 = 3977.512, 16078.433
STAFF_25, OTHER_25 = 6985.597, 3316.289
TAX = 0.22140908033206499


def cascade():
    staff = {26: STAFF_25 * 1.00}
    staff[27] = staff[26] * 1.08
    staff[28] = staff[27] * 1.10
    other = {26: OTHER_25 * 0.99}
    other[27] = other[26] * 1.10
    other[28] = other[27] * 1.15
    gen_open, spec_open = GEN_OPEN_25, SPEC_OPEN_26
    rows = []
    for y in (26, 27, 28):
        L, m = LOANS[y], MIX[y]
        opex = staff[y] + DA[y] + other[y]
        gen_close = 0.007 * sum(m[:4]) * L
        wo = WO_RATE[y] * L
        spec_charge = CHARGE_X[y] * wo
        spec_close = spec_open + spec_charge - wo - 0.4
        prov = (gen_close - gen_open) + spec_charge + VAMC[y]
        pbt = TOI[y] - opex - prov
        npl_amt = sum(m[2:]) * L
        rows.append(dict(
            y=2000 + y, toi=TOI[y], opex=opex, cir=opex / TOI[y],
            ppop=TOI[y] - opex, prov=prov, pbt=pbt, npatmi=pbt * (1 - TAX),
            npl_pct=sum(m[2:]), npl=npl_amt, wo=wo,
            res=gen_close + spec_close, cov=(gen_close + spec_close) / npl_amt))
        gen_open, spec_open = gen_close, spec_close
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
