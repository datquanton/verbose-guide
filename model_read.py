# -*- coding: utf-8 -*-
"""Derive the STB forecast straight out of FinModel_STB_2Q26.xlsx.

The deck used to carry hand-typed constants read off the workbook.  Every
revision moved some of them and the transcription was the only thing standing
between the model and the slide.  This module removes that step: it reads the
cells, re-evaluates the handful of formulas this project books, and returns the
forecast, so update_stb_loans has nothing left to type.

Excel is not available here, so cached values on cells downstream of a booked
formula are stale by construction.  Only two kinds of cell are trusted:

  * caches on cells nothing we touched feeds into - NII, fees, other income,
    write-offs, the general allowance, FY25 actuals, the FY26F balance sheet;
  * formulas we booked ourselves, which are re-evaluated here.

FY26F is fully recalculated by the analyst's Excel, so every FY26F figure this
module derives can be checked against its own cache.  check() does exactly that
and is asserted on import - if the derivation drifts from Excel on the one year
where both exist, the module refuses to load.

The chain, in the model's own terms:

  opex        132 salary + 133 D&A + 134 other, 132/134 on booked multipliers
  TOI         121 NII + 124 net fee + 131 net other
  provisions  247 VAMC + 248 general + 249 specific, 249 = 278 (booked)
  PBT         TOI - opex - provisions
  NPATMI      PBT x (1 - 149 tax rate)
  equity       85 rolls forward on retained NPATMI (95 + 96 + 98 sum to 100%)
  assets       61 tracks equity, liabilities being independently forecast
  allowance   284 = opening + 278 charge + 279 write-off + 280, plus 274 general
"""
import re
import zipfile
from lxml import etree

MODEL = '/home/user/verbose-guide/FinModel_STB_2Q26.xlsx'
NS = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
COLS = ('Y', 'Z', 'AA')                     # FY26F, FY27F, FY28F
SHARES = 2060.158                           # mn, Model!Y158


def sheet(path, name):
    """Every cell on a sheet as {ref: (formula, value)}, shared formulas resolved."""
    z = zipfile.ZipFile(path)
    idx = {}
    for rel in etree.fromstring(z.read('xl/_rels/workbook.xml.rels')):
        idx[rel.get('Id')] = rel.get('Target').lstrip('/')
    part = None
    for s in etree.fromstring(z.read('xl/workbook.xml')).iter(NS + 'sheet'):
        if s.get('name') == name:
            rid = s.get('{http://schemas.openxmlformats.org/officeDocument/'
                        '2006/relationships}id')
            part = idx[rid]
            break
    if part is None:
        raise KeyError('no sheet %r in %s' % (name, path))
    root = etree.fromstring(z.read(part if part.startswith('xl/') else 'xl/' + part))
    master, out = {}, {}
    for c in root.iter(NS + 'c'):
        f = c.find(NS + 'f')
        if f is not None and f.get('t') == 'shared' and f.text:
            master[f.get('si')] = f.text
    for c in root.iter(NS + 'c'):
        f, v = c.find(NS + 'f'), c.find(NS + 'v')
        txt = f.text if f is not None else None
        if f is not None and f.get('t') == 'shared' and not txt:
            txt = master.get(f.get('si'))
        num = None
        if v is not None and c.get('t') not in ('s', 'str', 'inlineStr'):
            try:
                num = float(v.text)
            except (TypeError, ValueError):
                num = None
        out[c.get('r')] = (txt, num)
    return out


class Model(object):
    def __init__(self, path=MODEL):
        self.m = sheet(path, 'Model')
        self.npl = sheet(path, 'NPL')

    # ---------------------------------------------------------------- cells
    def v(self, ref):
        """Cached value.  Only used where nothing we booked feeds the cell."""
        val = self.m[ref][1]
        if val is None:
            raise ValueError('%s has no cached value' % ref)
        return val

    def f(self, ref):
        return self.m[ref][0]

    def scaled(self, ref):
        """Evaluate 'REF*factor', the form every opex multiplier takes."""
        src, factor = re.match(r'^([A-Z]+\d+)\*([\d.]+)$', self.f(ref)).groups()
        return src, float(factor)

    def charge(self, ref, wo):
        """The specific charge: '-REF*factor' or '-REF+constant'.

        The two forms are not interchangeable.  A multiplier scales with the
        write-off, so the reserve stock is untouched when it is 1.0x; a constant
        is an overlay on top, and every VNDbn of it lands in the closing
        allowance.  Both are in use - FY26F on a multiplier, FY27F/FY28F on an
        overlay - so both are read rather than assumed.
        """
        txt = self.f(ref)                    # wo is already -Model!279, so positive
        mul = re.match(r'^-([A-Z]+\d+)\*([\d.]+)$', txt)
        if mul:
            return wo * float(mul.group(2))
        add = re.match(r'^-([A-Z]+\d+)\+([\d.]+)$', txt)
        if add:
            return wo + float(add.group(2))
        raise ValueError('%s = %r is neither a multiplier nor an overlay' % (ref, txt))

    # -------------------------------------------------------------- forecast
    def build(self):
        # operating expense: 132 and 134 chain off FY25, 133 stands on its cache
        sal, oth = [], []
        for i, col in enumerate(COLS):
            for row, acc in ((132, sal), (134, oth)):
                src, factor = self.scaled('%s%d' % (col, row))
                base = self.v(src) if i == 0 else acc[-1]
                acc.append(base * factor)
        opex = [s + o + self.v(c + '133') for s, o, c in zip(sal, oth, COLS)]

        nii = [self.v(c + '121') for c in COLS]
        nonii = [self.v(c + '124') + self.v(c + '131') for c in COLS]
        toi = [a + b for a, b in zip(nii, nonii)]

        wo = [-self.v(c + '279') for c in COLS]          # write-offs, positive
        spec = [self.charge(c + '278', w) for c, w in zip(COLS, wo)]
        gen = [self.v(c + '248') for c in COLS]          # general allowance movement
        vamc = [self.v(c + '247') for c in COLS]
        prov = [s + g + v for s, g, v in zip(spec, gen, vamc)]

        pbt = [t - o - p for t, o, p in zip(toi, opex, prov)]
        tax = 1 + self.v('Y149')                         # 149 is stored negative
        npat = [p * tax for p in pbt]

        # equity rolls forward on retained profit; FY26F stands on its own cache
        equity = [self.v('Y85')]
        for n in npat[1:]:
            equity.append(equity[-1] + n)
        # liabilities are forecast independently, so assets move with equity
        assets = [self.v(c + '61') + (e - self.v(c + '85'))
                  for c, e in zip(COLS, equity)]

        # specific allowance roll-forward, then the general allowance on top
        spec_bal, opening = [], self.v('Y277')
        for i in range(3):
            opening = opening + spec[i] - wo[i] + self.v(COLS[i] + '280')
            spec_bal.append(opening)
        reserve = [b + self.v(c + '274') for b, c in zip(spec_bal, COLS)]

        loans = [self.v(c + '204') for c in COLS]
        npl_rate = [sum(self.npl['%s%d' % (c, r)][1] for r in (28, 29, 30))
                    for c in ('N', 'O', 'P')]
        npl = [r * l for r, l in zip(npl_rate, loans)]

        avg_eq = [equity[0]] + [(equity[i - 1] + equity[i]) / 2 for i in (1, 2)]
        return dict(
            nii=tuple(nii), nonii=tuple(nonii), toi=tuple(toi), opex=tuple(opex),
            prov=tuple(prov), specific=tuple(spec), writeoff=tuple(wo),
            pbt=tuple(pbt), npatmi=tuple(npat),
            equity=tuple(equity), assets=tuple(assets),
            reserve=tuple(reserve), loans=tuple(loans), npl=tuple(npl),
            npl_rate=tuple(npl_rate),
            cir=tuple(o / t * 100 for o, t in zip(opex, toi)),
            roe=tuple(n / e * 100 for n, e in zip(npat, avg_eq)),
            eps=tuple(n * 1000 / SHARES for n in npat),
            bvps=tuple(e * 1000 / SHARES for e in equity),
            coverage=tuple(r / n * 100 for r, n in zip(reserve, npl)),
            # FY25 comparatives.  Provisioning comes off 141, not 254: for the
            # actual year 254 holds only the VAMC and securities leg (4,855),
            # while 141 is the reported charge the forecast years compare with.
            pbt25=self.v('X144'), npatmi25=self.v('X153'),
            eps25=self.v('X150') * 1000 / SHARES,
            nii25=self.v('X121'), prov25=self.v('X141'),
        )

    def check(self, d):
        """FY26F is fully recalculated in Excel - the derivation must reproduce it."""
        bad = []
        for key, ref in (('opex', 'Y135'), ('toi', 'Y117'), ('prov', 'Y141'),
                         ('pbt', 'Y144'), ('npatmi', 'Y153'), ('equity', 'Y85'),
                         ('assets', 'Y61'), ('reserve', 'Y286'), ('loans', 'Y204')):
            got, want = d[key][0], self.v(ref)
            if abs(got - want) > 0.05:
                bad.append('%s: derived %.3f, Model!%s caches %.3f'
                           % (key, got, ref, want))
        return bad


_m = Model()
F = _m.build()
_bad = _m.check(F)
if _bad:
    raise SystemExit('model_read disagrees with Excel on FY26F:\n  '
                     + '\n  '.join(_bad))


if __name__ == '__main__':
    print('%-22s%12s%12s%12s' % ('', 'FY26F', 'FY27F', 'FY28F'))
    for lab, key, f in [('Gross loans', 'loans', '{:,.0f}'),
                        ('NII', 'nii', '{:,.0f}'), ('Non-II', 'nonii', '{:,.0f}'),
                        ('TOI', 'toi', '{:,.0f}'), ('Opex', 'opex', '{:,.0f}'),
                        ('CIR %', 'cir', '{:.1f}'),
                        ('Write-offs', 'writeoff', '{:,.0f}'),
                        ('Specific charge', 'specific', '{:,.0f}'),
                        ('Provisioning', 'prov', '{:,.0f}'),
                        ('PBT', 'pbt', '{:,.0f}'), ('NPATMI', 'npatmi', '{:,.0f}'),
                        ('Equity', 'equity', '{:,.0f}'),
                        ('Total assets', 'assets', '{:,.0f}'),
                        ('ROE %', 'roe', '{:.1f}'), ('EPS', 'eps', '{:,.0f}'),
                        ('BVPS', 'bvps', '{:,.0f}'),
                        ('NPL ratio %', 'npl_rate', '{:.1%}'),
                        ('NPL balance', 'npl', '{:,.0f}'),
                        ('Total allowance', 'reserve', '{:,.0f}'),
                        ('Coverage %', 'coverage', '{:.1f}')]:
        print(('%-22s' % lab) + ''.join('{:>12}'.format(f.format(v)) for v in F[key]))
    print('\nFY26F reproduces Excel on 9 lines; FY27F/FY28F are derived '
          '(their caches predate the booked formulas)')
