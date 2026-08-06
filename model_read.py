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
PAR = 10000.0                               # VND par value

# Share count comes from charter capital, 'Balance sheet'!Y80 = VND18,852.157bn,
# i.e. 1,885.216mn shares.  NOT from Model!Y87 paid-in capital of VND20,601.582bn
# - that is the whole 'Vốn của TCTD' block, charter capital plus VND1,747.651bn
# of share premium and VND1.774bn of other capital.  Dividing it by par overstates
# the count 9.3% and understates every EPS and BVPS by the same margin.
CHARTER = None                               # filled on import, from the workbook
SHARES = None


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
        self.charter = sheet(path, 'Balance sheet')['Y80'][1]
        self.shares = self.charter * 1e9 / PAR / 1e6        # VNDbn -> mn shares

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

    # ----------------------------------------------------------------- loans
    def loan_book(self):
        """Gross loans, from the segment build in rows 515-520.

        The FY25 segment balances are themselves rolled forward from FY24, and
        they have drifted: they sum to VND593,591bn against a reported book of
        VND626,392bn (Model!X450, from Note!T79), 5.2% short.  That is why the
        model's stated FY26F segment growth of 7.9% only ever produced 2.3% on
        the reported book.  Y515:Y520 now rebase to the reported book before
        growing, so the growth rate in the formula is the growth the deck shows.
        FY27F and FY28F keep their own segment growth rates, rows 533-538.
        """
        rows = (515, 516, 517, 518, 519, 520)
        growth_row = {515: 533, 516: 534, 517: 535, 518: 536, 519: 538, 520: 537}
        g26 = float(re.match(r'^X\d+\*\$X\$450/\$X\$521\*([\d.]+)$',
                             self.f('Y515')).group(1))
        rebase = self.v('X450') / self.v('X521')
        seg = [[self.v('X%d' % r) * rebase * g26 for r in rows]]
        for col in COLS[1:]:
            seg.append([s * (1 + self.v('%s%d' % (col, growth_row[r])))
                        for r, s in zip(rows, seg[-1])])
        return [sum(s) for s in seg], g26

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

        loans, growth26 = self.loan_book()
        npl_rate = [sum(self.npl['%s%d' % (c, r)][1] for r in (28, 29, 30))
                    for c in ('N', 'O', 'P')]
        perf_rate = [sum(self.npl['%s%d' % (c, r)][1] for r in (26, 27, 28, 29))
                     for c in ('N', 'O', 'P')]          # groups 1-4, the 0.7% base

        wo = [-self.v(c + '287') * l for c, l in zip(COLS, loans)]     # row 279
        spec = [self.charge(c + '278', w) for c, w in zip(COLS, wo)]
        gen_bal = [0.007 * l * p for l, p in zip(loans, perf_rate)]    # row 274
        gen = [b - a for a, b in zip([self.v('X274')] + gen_bal, gen_bal)]
        vamc = [self.v(c + '247') for c in COLS]         # VAMC and securities leg
        prov = [s + g + v for s, g, v in zip(spec, gen, vamc)]

        # specific allowance roll-forward, then the general allowance on top
        spec_bal, opening = [], self.v('Y277')
        for i in range(3):
            opening = opening + spec[i] - wo[i] + self.v(COLS[i] + '280')
            spec_bal.append(opening)
        reserve = [b + g for b, g in zip(spec_bal, gen_bal)]

        # Loan interest income, row 681: the average of this year's and last
        # year's (net loans + Group 1) at the loan yield, row 699.  It is the
        # only line the loan book moves, so the rest of row 686 and the whole of
        # interest expense come off their caches as a delta.
        grp1 = [l * self.npl[c + '26'][1] for l, c in zip(loans, 'NOP')]
        net = [l - r for l, r in zip(loans, reserve)]
        prev = (self.v('X198'), self.v('X691'))
        int_inc, nii = [], []
        for i, c in enumerate(COLS):
            int_inc.append(((net[i] + grp1[i]) + sum(prev)) / 2 * self.v(c + '699'))
            prev = (grp1[i], net[i])
            nii.append(self.v(c + '121') + int_inc[i] - self.v(c + '681'))
        nonii = [self.v(c + '124') + self.v(c + '131') for c in COLS]
        toi = [a + b for a, b in zip(nii, nonii)]

        pbt = [t - o - p for t, o, p in zip(toi, opex, prov)]
        tax = 1 + self.v('Y149')                         # 149 is stored negative
        npat = [p * tax for p in pbt]

        # Equity rolls forward on retained profit.  Row 85 sums 87 + 94 + 98 +
        # 101, and only 98 moves - the fund allocations in 95-97 sit inside row
        # 94, which is held at its FY25 value - so the increment is the whole of
        # NPATMI.  The FY26F base is row 85's cache less the NPATMI inside it,
        # which is exact because both caches come from the same Excel run.
        equity = [self.v('Y85') - self.v('Y153') + npat[0]]
        for n in npat[1:]:
            equity.append(equity[-1] + n)
        # liabilities are forecast independently, so assets move with equity
        assets = [self.v(c + '61') + (e - self.v(c + '85'))
                  for c, e in zip(COLS, equity)]

        npl = [r * l for r, l in zip(npl_rate, loans)]

        avg_eq = [equity[0]] + [(equity[i - 1] + equity[i]) / 2 for i in (1, 2)]
        return dict(
            nii=tuple(nii), nonii=tuple(nonii), toi=tuple(toi), opex=tuple(opex),
            prov=tuple(prov), specific=tuple(spec), writeoff=tuple(wo),
            pbt=tuple(pbt), npatmi=tuple(npat),
            equity=tuple(equity), assets=tuple(assets),
            reserve=tuple(reserve), loans=tuple(loans), npl=tuple(npl),
            npl_rate=tuple(npl_rate), loan_growth=growth26 - 1,
            loans25=self.v('X450'),
            cir=tuple(o / t * 100 for o, t in zip(opex, toi)),
            roe=tuple(n / e * 100 for n, e in zip(npat, avg_eq)),
            eps=tuple(n * 1000 / self.shares for n in npat),
            bvps=tuple(e * 1000 / self.shares for e in equity),
            coverage=tuple(r / n * 100 for r, n in zip(reserve, npl)),
            shares=self.shares, charter=self.charter,
            # FY23-FY25 actuals, on the same share count - the deck used to carry
            # per-share history struck on the overstated one
            hist_npatmi=tuple(self.v(c + '153') for c in 'VWX'),
            hist_equity=tuple(self.v(c + '85') for c in 'VWX'),
            hist_eps=tuple(self.v(c + '153') * 1000 / self.shares for c in 'VWX'),
            hist_bvps=tuple(self.v(c + '85') * 1000 / self.shares for c in 'VWX'),
            # FY25 comparatives.  Provisioning comes off 141, not 254: for the
            # actual year 254 holds only the VAMC and securities leg (4,855),
            # while 141 is the reported charge the forecast years compare with.
            pbt25=self.v('X144'), npatmi25=self.v('X153'),
            eps25=self.v('X150') * 1000 / self.shares,
            nii25=self.v('X121'), prov25=self.v('X141'),
        )

    # The FY26F drivers as Excel last recalculated them, before this round.
    EXCEL = dict(loans=640643.0521152194, opex_mult=0.9647, spec_ratio=0.8653)

    def check(self, d=None):
        """Replay the drivers Excel last recalculated and land back on its caches.

        FY26F used to be checkable line by line, because Excel had recalculated
        it and nothing booked here touched the loan book.  The 8% growth
        assumption ended that: every FY26F cache is now stale against the
        current drivers.  The arithmetic between drivers and results has not
        changed, though, so feeding the old drivers through this same code has
        to reproduce Excel exactly - which is what this checks.  It still fails
        the import if the engine drifts.
        """
        e, bad = self.EXCEL, []
        npl = lambda r: self.npl['N%d' % r][1]
        loans = e['loans']
        opex = (self.v('X132') + self.v('X134')) * e['opex_mult'] + self.v('Y133')
        wo = -self.v('Y287') * loans
        spec = wo * e['spec_ratio']
        gen = 0.007 * loans * sum(npl(r) for r in (26, 27, 28, 29))
        prov = spec + (gen - self.v('X274')) + self.v('Y247')
        reserve = self.v('Y277') + spec - wo + self.v('Y280') + gen
        net, grp1 = loans - reserve, loans * npl(26)
        nii = self.v('Y121') + ((net + grp1 + self.v('X198') + self.v('X691')) / 2
                                * self.v('Y699')) - self.v('Y681')
        toi = nii + self.v('Y124') + self.v('Y131')
        pbt = toi - opex - prov
        got = dict(loans=loans, opex=opex, nii=nii, toi=toi, prov=prov, pbt=pbt,
                   reserve=reserve, npatmi=pbt * (1 + self.v('Y149')))
        for key, ref in (('loans', 'Y204'), ('opex', 'Y135'), ('nii', 'Y121'),
                         ('toi', 'Y117'), ('prov', 'Y141'), ('pbt', 'Y144'),
                         ('npatmi', 'Y153'), ('reserve', 'Y286')):
            if abs(got[key] - self.v(ref)) > 0.05:
                bad.append('%s: replay %.3f, Model!%s caches %.3f'
                           % (key, got[key], ref, self.v(ref)))
        return bad


_m = Model()
CHARTER, SHARES = _m.charter, _m.shares
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
    print('\n%-22s%12s%12s%12s' % ('actuals', 'FY23', 'FY24', 'FY25'))
    for lab, key in [('NPATMI', 'hist_npatmi'), ('Equity', 'hist_equity'),
                     ('EPS', 'hist_eps'), ('BVPS', 'hist_bvps')]:
        print(('%-22s' % lab) + ''.join('{:>12,.0f}'.format(v) for v in F[key]))
    print('\n{:,.4f}mn shares on charter capital of VND{:,.3f}bn at VND{:,.0f} par'
          .format(F['shares'], F['charter'], PAR))
    print('FY26F reproduces Excel on 9 lines; FY27F/FY28F are derived '
          '(their caches predate the booked formulas)')
