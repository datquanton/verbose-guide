# -*- coding: utf-8 -*-
"""Evaluate the edited chain straight from the workbook XML - Excel cannot
recalculate here, so the cached values on PL!R9:S9 are stale and revenue is
rebuilt from the Scenarios drivers instead."""
import re, zipfile
from lxml import etree

NS = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
z = zipfile.ZipFile('/home/user/verbose-guide/FPT_2Q26_min_final_tracker.xlsx')


def cells(sheet):
    root = etree.fromstring(z.read('xl/worksheets/%s.xml' % sheet))
    return {c.get('r'): (c.find(NS + 'f'), c.find(NS + 'v')) for c in root.iter(NS + 'c')}


PL, SC, RV = cells('sheet6'), cells('sheet3'), cells('sheet4')
val = lambda d, r: float(d[r][1].text)
frm = lambda d, r: d[r][0].text
pct = lambda s: float(re.search(r'\*([\d.]+)%', s).group(1)) / 100

# revenue: FY26F from the Revenue sheet, FY27-28F rolled with the base-case growth rows
git, dit, edu = (val(RV, 'J%d' % r) for r in (12, 13, 17))
rev = [git + dit + edu]
for c in 'IJ':                                  # FY27F then FY28F
    git *= 1 + val(SC, c + '11'); dit *= 1 + val(SC, c + '17'); edu *= 1 + val(SC, c + '30')
    rev.append(git + dit + edu)

FY25, fails = 9464.16, []
rows = {k: [] for k in ('rev', 'gp', 'opex', 'core', 'fin', 'oth', 'assoc', 'pbt', 'tax', 'npat')}
for i, (col, sc) in enumerate(zip('QRS', ('H45', 'I45', 'J45'))):
    r = rev[i]
    gp = r * (1 - pct(frm(PL, col + '11')))
    opex = r * (val(PL, col + '19') + pct(frm(PL, col + '20')))
    core = gp - opex
    fin = val(PL, col + '32') - val(PL, col + '34')
    oth = val(PL, col + '42') - val(PL, col + '43')
    assoc = r * val(SC, sc)
    pbt = core + fin + oth + assoc
    tax = (pbt - assoc) * pct(frm(PL, col + '50'))
    for k, v in zip(rows, (r, gp, opex, core, fin, oth, assoc, pbt, tax, pbt - tax - val(PL, col + '54'))):
        rows[k].append(v)

print('%-24s %10s %10s %10s' % ('', 'FY26F', 'FY27F', 'FY28F'))
for k, l in [('rev', 'revenue'), ('gp', 'gross profit'), ('opex', 'operating expense'),
             ('core', 'operating profit'), ('fin', 'net financial income'), ('oth', 'other'),
             ('assoc', 'associates'), ('pbt', 'PBT'), ('tax', 'tax'), ('npat', 'NPATMI')]:
    print('%-24s %10.0f %10.0f %10.0f' % (l, *rows[k]))


def check(name, cond, detail=''):
    print('%-4s %-54s %s' % ('OK' if cond else 'FAIL', name, detail))
    if not cond:
        fails.append(name)


print()
TARGET, GROWTH = [10848., 12404., 14100.], [14.6, 14.3, 13.7]
prev = FY25
for i, y in enumerate(('FY26F', 'FY27F', 'FY28F')):
    check('%s NPATMI = %.0f' % (y, TARGET[i]), abs(rows['npat'][i] - TARGET[i]) < 3,
          '%.0f' % rows['npat'][i])
    got = rows['npat'][i] / prev * 100 - 100
    check('%s growth %.1f%%' % (y, GROWTH[i]), abs(got - GROWTH[i]) < 0.06, '%.2f%%' % got)
    prev = rows['npat'][i]
# option A: nothing accelerates
gr = lambda k: [rows[k][i] / rows[k][i - 1] - 1 for i in (1, 2)]
check('Global IT growth held at the FY26F rate',
      abs(val(SC, 'I11') - 0.14668042) < 1e-6 and abs(val(SC, 'J11') - 0.14668042) < 1e-6)
check('Education growth held at 5%', val(SC, 'I30') == 0.05 and val(SC, 'J30') == 0.05)
# every segment growth rate is constant, so blended revenue growth drifts up ~10bp
# a year purely on mix (Global IT is the fastest-growing and largest segment)
check('revenue growth flat within a 20bp mix drift', gr('rev')[1] - gr('rev')[0] < 0.002,
      '%.1f%% then %.1f%% (mix, not an assumption)' % (gr('rev')[0] * 100, gr('rev')[1] * 100))
check('NPATMI growth does not accelerate', gr('npat')[1] <= gr('npat')[0],
      '%.1f%% then %.1f%%' % (gr('npat')[0] * 100, gr('npat')[1] * 100))
check('no operating leverage: opex/revenue flat',
      max(o / r for o, r in zip(rows['opex'], rows['rev']))
      - min(o / r for o, r in zip(rows['opex'], rows['rev'])) < 1e-6,
      ' '.join('%.3f%%' % (o / r * 100) for o, r in zip(rows['opex'], rows['rev'])))
check('gross margin flat at the 1H26 realised 32.448%',
      all(abs(g / r - 0.32448) < 1e-4 for g, r in zip(rows['gp'], rows['rev'])))
check('associates grow at 14% (FPT Telecom 1H26: +13.9%)',
      all(abs(x - 0.14) < 0.002 for x in gr('assoc')))
check('FY26F associates = 2 x the filed 1H26 1,423.4', abs(rows['assoc'][0] - 2846.8) < 2)
check('tax = 15.55% of the block ex-associates',
      all(abs(t / (p - a) - 0.1555) < 1e-4 for t, p, a in zip(rows['tax'], rows['pbt'], rows['assoc'])))
print('\n' + '=' * 76)
print('%d FAILED: %s' % (len(fails), fails) if fails else 'ALL CHECKS PASSED')
print('\nslide rows: revenue %s | operating profit %s | PBT %s | NPATMI %s'
      % tuple([['%.0f' % x for x in rows[k]] for k in ('rev', 'core', 'pbt', 'npat')]))
print('EPS %s | P/E %s' % (['%.0f' % (n / 1.810) for n in rows['npat']],
                           ['%.1f' % (78750 * 1.810 / n) for n in rows['npat']]))
