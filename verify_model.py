# -*- coding: utf-8 -*-
"""Evaluate the edited PL chain straight from the workbook XML (Excel cannot
recalculate in this environment) and check it lands on the carried forecast."""
import re, zipfile
from lxml import etree

NS = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
z = zipfile.ZipFile('/home/user/verbose-guide/FPT_2Q26_min_final_tracker.xlsx')


def cells(sheet):
    root = etree.fromstring(z.read('xl/worksheets/%s.xml' % sheet))
    out = {}
    for c in root.iter(NS + 'c'):
        f, v = c.find(NS + 'f'), c.find(NS + 'v')
        out[c.get('r')] = (f.text if f is not None else None, v.text if v is not None else None)
    return out


PL, SC = cells('sheet6'), cells('sheet3')
num = lambda x: float(x[1])
pct = lambda s: float(re.search(r'\*([\d.]+)%', s).group(1)) / 100

FY25, TARGET = 9464.16, [10848., 12549., 14608.]
fails, prev = [], FY25
print('%-24s %10s %10s %10s' % ('', 'FY26F', 'FY27F', 'FY28F'))
rows = {k: [] for k in ('rev', 'cogs', 'gp', 'sell', 'admin', 'core', 'fin', 'oth',
                        'assoc', 'pbt', 'tax', 'npatmi')}
for col, sc in zip('QRS', ('H45', 'I45', 'J45')):
    rev = num(PL[col + '9'])
    cogs = rev * pct(PL[col + '11'][0])
    gp = rev - cogs
    sell = rev * num(PL[col + '19'])
    admin = rev * pct(PL[col + '20'][0])
    core = gp - sell - admin
    fin = num(PL[col + '32']) - num(PL[col + '34'])
    oth = num(PL[col + '42']) - num(PL[col + '43'])
    assoc = rev * float(SC[sc][1])
    pbt = core + fin + oth + assoc
    tax = (pbt - assoc) * float(re.search(r'\*([\d.]+)%', PL[col + '50'][0]).group(1)) / 100
    npatmi = pbt - tax - num(PL[col + '54'])
    for k, v in zip(rows, (rev, cogs, gp, sell, admin, core, fin, oth, assoc, pbt, tax, npatmi)):
        rows[k].append(v)
for k, lab in [('rev', 'revenue'), ('cogs', 'COGS'), ('gp', 'gross profit'),
               ('sell', 'selling'), ('admin', 'admin'), ('core', 'core operating profit'),
               ('fin', 'net financial income'), ('oth', 'other'), ('assoc', 'associates'),
               ('pbt', 'PBT'), ('tax', 'tax'), ('npatmi', 'NPATMI')]:
    print('%-24s %10.0f %10.0f %10.0f' % (lab, *rows[k]))


def check(name, cond, detail=''):
    print('%-4s %-52s %s' % ('OK' if cond else 'FAIL', name, detail))
    if not cond:
        fails.append(name)


print()
for i, y in enumerate(('FY26F', 'FY27F', 'FY28F')):
    check('%s NPATMI ties to the carried forecast' % y, abs(rows['npatmi'][i] - TARGET[i]) < 3,
          '%.0f vs %.0f' % (rows['npatmi'][i], TARGET[i]))
for i, (y, g) in enumerate(zip(('FY26F', 'FY27F', 'FY28F'), (14.6, 15.7, 16.4))):
    got = rows['npatmi'][i] / prev * 100 - 100
    check('%s growth %.1f%%' % (y, g), abs(got - g) < 0.06, '%.2f%%' % got)
    prev = rows['npatmi'][i]
# every ratio must equal what 1H26 actually delivered
check('gross margin = 1H26 realised 32.448%', all(abs(g / r - 0.32448) < 1e-4
      for g, r in zip(rows['gp'], rows['rev'])))
check('total opex ~ 1H26 realised 17.68%', all(abs((s + a) / r - 0.1768) < 0.002
      for s, a, r in zip(rows['sell'], rows['admin'], rows['rev'])),
      ' '.join('%.2f%%' % ((s + a) / r * 100) for s, a, r in zip(rows['sell'], rows['admin'], rows['rev'])))
check('FY26F associates = 2 x the 1H26 filed 1,423.4', abs(rows['assoc'][0] - 2846.8) < 2,
      '%.0f' % rows['assoc'][0])
check('associates grow 14% p.a.', abs(rows['assoc'][1] / rows['assoc'][0] - 1.14) < 0.002)
check('FY26F net financial income = 830', abs(rows['fin'][0] - 830) < 1, '%.0f' % rows['fin'][0])
check('tax rate = 1H26 realised 15.55% ex-associates',
      all(abs(t / (p - a) - 0.1555) < 1e-4 for t, p, a in zip(rows['tax'], rows['pbt'], rows['assoc'])))
print('\n' + '=' * 74)
print('%d FAILED: %s' % (len(fails), fails) if fails else 'ALL CHECKS PASSED')
print('\nPBT row for the slide: %s' % ['%.0f' % p for p in rows['pbt']])
