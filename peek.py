# -*- coding: utf-8 -*-
"""Dump formula+value for a set of cells on one sheet of the STB/FPT models.
usage: python3 peek.py <xlsx> <sheetname> <cellspec> ...
       cellspec = 'Y132' or 'X:AA/130-145' (col range / row range)"""
import sys, zipfile, re
from lxml import etree
NS = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
R = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'


def sheetpath(z, name):
    wb = etree.fromstring(z.read('xl/workbook.xml'))
    rels = etree.fromstring(z.read('xl/_rels/workbook.xml.rels'))
    rm = {r.get('Id'): r.get('Target') for r in rels}
    for s in wb.iter(NS + 'sheet'):
        if s.get('name') == name:
            return 'xl/' + rm[s.get(R + 'id')].lstrip('/')
    raise SystemExit('no sheet ' + name)


def expand(spec):
    m = re.match(r'^([A-Z]+):([A-Z]+)/(\d+)-(\d+)$', spec)
    if not m:
        return [spec]
    def n(c):
        v = 0
        for ch in c:
            v = v * 26 + ord(ch) - 64
        return v
    def s(v):
        out = ''
        while v:
            v, r = divmod(v - 1, 26)
            out = chr(65 + r) + out
        return out
    c1, c2, r1, r2 = n(m.group(1)), n(m.group(2)), int(m.group(3)), int(m.group(4))
    return [s(c) + str(r) for r in range(r1, r2 + 1) for c in range(c1, c2 + 1)]


def dump(path, sheet, specs, labelcol='B'):
    z = zipfile.ZipFile(path)
    want = set()
    for sp in specs:
        want |= set(expand(sp))
    rows = sorted({int(re.match(r'[A-Z]+(\d+)', w).group(1)) for w in want})
    want |= {labelcol + str(r) for r in rows}
    sst = []
    if 'xl/sharedStrings.xml' in z.namelist():
        sst = [''.join(t.text or '' for t in si.iter(NS + 't'))
               for si in etree.fromstring(z.read('xl/sharedStrings.xml'))]
    got = {}
    for ev, el in etree.iterparse(z.open(sheetpath(z, sheet)), events=('end',)):
        if el.tag != NS + 'c':
            continue
        ref = el.get('r')
        if ref in want:
            f = el.find(NS + 'f'); v = el.find(NS + 'v')
            val = v.text if v is not None else None
            if el.get('t') == 's' and val is not None:
                val = sst[int(val)]
            elif el.get('t') == 'inlineStr':
                val = ''.join(t.text or '' for t in el.iter(NS + 't'))
            got[ref] = (f.text if f is not None else None, val)
        el.clear()
    return got, rows


if __name__ == '__main__':
    path, sheet = sys.argv[1], sys.argv[2]
    got, rows = dump(path, sheet, sys.argv[3:])
    cols = sorted({re.match(r'([A-Z]+)', k).group(1) for k in got}, key=lambda c: (len(c), c))
    for r in rows:
        lab = (got.get('B%d' % r) or (None, ''))[1] or ''
        print('--- row %d  %s' % (r, str(lab)[:60]))
        for c in cols:
            k = c + str(r)
            if k in got and k != 'B%d' % r:
                f, v = got[k]
                print('    %-6s %-40s %s' % (k, (f or '')[:40], v))
