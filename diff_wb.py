# -*- coding: utf-8 -*-
"""Cell-level diff of two .xlsx files. usage: python3 diff_wb.py old.xlsx new.xlsx [sheetname]"""
import sys, zipfile, re
from lxml import etree
NS = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
R = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'


def sheets(z):
    wb = etree.fromstring(z.read('xl/workbook.xml'))
    rels = {r.get('Id'): r.get('Target') for r in etree.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
    return {s.get('name'): 'xl/' + rels[s.get(R + 'id')].lstrip('/') for s in wb.iter(NS + 'sheet')}


def cells(z, path):
    sst = []
    if 'xl/sharedStrings.xml' in z.namelist():
        sst = [''.join(t.text or '' for t in si.iter(NS + 't'))
               for si in etree.fromstring(z.read('xl/sharedStrings.xml'))]
    out = {}
    for ev, el in etree.iterparse(z.open(path), events=('end',)):
        if el.tag != NS + 'c':
            continue
        f, v = el.find(NS + 'f'), el.find(NS + 'v')
        val = v.text if v is not None else None
        if el.get('t') == 's' and val is not None:
            val = sst[int(val)]
        elif el.get('t') == 'inlineStr':
            val = ''.join(t.text or '' for t in el.iter(NS + 't'))
        if f is not None or val is not None:
            out[el.get('r')] = (f.text if f is not None else None, val)
        el.clear()
    return out


def key(ref):
    m = re.match(r'([A-Z]+)(\d+)$', ref)
    c = 0
    for ch in m.group(1):
        c = c * 26 + ord(ch) - 64
    return (int(m.group(2)), c)


def same(a, b):
    if a == b:
        return True
    if a is None or b is None:
        return False
    fa, va = a; fb, vb = b
    if fa != fb:
        return False
    try:
        return abs(float(va) - float(vb)) < 1e-9
    except (TypeError, ValueError):
        return va == vb


def main():
    zo, zn = zipfile.ZipFile(sys.argv[1]), zipfile.ZipFile(sys.argv[2])
    so, sn = sheets(zo), sheets(zn)
    only = sys.argv[3] if len(sys.argv) > 3 else None
    for name in sn:
        if only and name != only:
            continue
        if name not in so:
            print('== NEW SHEET %s' % name); continue
        co, cn = cells(zo, so[name]), cells(zn, sn[name])
        diffs = [r for r in set(co) | set(cn) if not same(co.get(r), cn.get(r))]
        if not diffs:
            continue
        print('== %s  (%d cells differ)' % (name, len(diffs)))
        for r in sorted(diffs, key=key)[:60]:
            o, n = co.get(r), cn.get(r)
            fmt = lambda x: 'absent' if x is None else ('=%s' % x[0] if x[0] else str(x[1])[:34])
            print('   %-7s %-38s -> %s' % (r, fmt(o), fmt(n)))
        if len(diffs) > 60:
            print('   ... +%d more' % (len(diffs) - 60))


if __name__ == '__main__':
    main()
