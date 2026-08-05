# -*- coding: utf-8 -*-
"""Push the STB 5.5%-NPL / 40-38-36% CIR cascade into the stock-pick workbook.
Sheet1 'Stock Pick' row 6 = STB; Sheet2 'Target Price and Forecast' row 13 = STB.
All strings are inlineStr - this workbook has no sharedStrings part."""
import zipfile
from lxml import etree

WB = '/home/user/verbose-guide/Stock_Pick_and_Forecast_Aug26_MAS_RS_EN_updated.xlsx'
NS = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
SHARES = 2060.158

import update_stb_loans as U
NPATMI_25 = 5939.111
NPATMI_26, NPATMI_27 = U.NPATMI[0], U.NPATMI[1]
TP = U.TP
EQ_26, EQ_27 = U.EQUITY[0], U.EQUITY[1]
eps = lambda n: n * 1000 / SHARES
bvps = lambda e: e * 1000 / SHARES

C6 = ("- We cut FY26F loan growth to 2.3% from 11.7%, in line with the 1.5% delivered in 1H26. "
      "NII falls to VND24,570bn (-7.9% YoY) and gross loans to VND640,643bn.\n"
      "- NIM troughs in FY26F as elevated NPLs freeze accrued interest income while funding costs "
      "remain sticky, before recovering in FY27F.\n"
      "- We set FY26F NPL at 5.5%, from below 4.5%, and FY27F at 4.0% from 3.1%. Reserves reached "
      "VND27.2tn at end-2Q26 (56.7% coverage) on VND7.1tn of 1H26 charges and almost no "
      "write-offs; a further VND4.0tn charge in 2H26 funds VND11.8tn of write-offs, or 37% of the "
      "Group 5 balance, leaving coverage at 54.2%. Holding coverage near 50% is what caps the "
      "improvement at 5.5%, and it needs 2H26 NPL formation to slow to roughly a quarter of the "
      "1H26 pace.\n"
      "- FY26F PBT falls to VND{pbt:,.0f}bn ({yoy:+.1f}% YoY), {vp:.0f}% below the board-approved "
      "plan of VND8,100bn. The opex build is unchanged while total operating income has fallen, "
      "so CIR now reads {c26:.1f}% against the 40.0% previously targeted.").format(
          pbt=U.PBT[0], yoy=U.PBT_YOY, vp=-U.VS_PLAN, c26=U.CIR[0])

SHEET1 = {
    'C6': ('str', C6),
    'F6': ('num', '%.0f' % NPATMI_26),
    'G6': ('num', '%.0f' % NPATMI_27),
    'H6': ('num', repr(eps(NPATMI_26) / eps(NPATMI_25) - 1)),
    'I6': ('num', repr(NPATMI_27 / NPATMI_26 - 1)),
    'J6': ('num', repr(TP / eps(NPATMI_26))),
    'K6': ('num', repr(TP / eps(NPATMI_27))),
    'L6': ('num', repr(TP / bvps(EQ_26))),
    'M6': ('num', repr(TP / bvps(EQ_27))),
}
SHEET2 = {
    'D13': ('num', '%.0f' % NPATMI_26),
    'E13': ('num', '%.0f' % NPATMI_27),
}


def patch(data, edits):
    root = etree.fromstring(data)
    seen = []
    for c in root.iter(NS + 'c'):
        ref = c.get('r')
        if ref not in edits:
            continue
        kind, val = edits[ref]
        if kind == 'str':
            assert c.get('t') == 'inlineStr', ref
            t = c.find(NS + 'is').find(NS + 't')
            t.text = val
        else:
            assert c.find(NS + 'f') is None, '%s is a formula' % ref
            v = c.find(NS + 'v')
            seen.append('%-5s %-14s -> %s' % (ref, v.text[:14], val[:14]))
            v.text = val
            continue
        seen.append('%-5s (text, %d chars)' % (ref, len(val)))
    assert len(seen) == len(edits), (len(seen), len(edits))
    return etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True), seen


def main():
    z = zipfile.ZipFile(WB)
    items = [(i, z.read(i.filename)) for i in z.infolist()]
    z.close()
    log, out = [], []
    for it, d in items:
        if it.filename == 'xl/worksheets/sheet1.xml':
            d, l = patch(d, SHEET1); log += ['Stock Pick:'] + ['  ' + x for x in l]
        elif it.filename == 'xl/worksheets/sheet2.xml':
            d, l = patch(d, SHEET2); log += ['Target Price and Forecast:'] + ['  ' + x for x in l]
        out.append((it, d))
    zo = zipfile.ZipFile(WB, 'w', zipfile.ZIP_DEFLATED)
    for it, d in out:
        zo.writestr(it, d)
    zo.close()
    print('\n'.join(log))


if __name__ == '__main__':
    main()
