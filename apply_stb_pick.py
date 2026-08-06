# -*- coding: utf-8 -*-
"""Push the current STB cascade into the stock-pick workbook.
Sheet1 'Stock Pick' row 6 = STB; Sheet2 'Target Price and Forecast' row 13 = STB.
All strings are inlineStr - this workbook has no sharedStrings part."""
import zipfile
from lxml import etree
import update_stb_loans as U

WB = '/home/user/verbose-guide/Stock_Pick_and_Forecast_Aug26_MAS_RS_EN_updated.xlsx'
NS = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
SHARES = U.SHARES        # 1,885.216mn, on charter capital
NPATMI_25 = U.F['npatmi25']
NPATMI_26, NPATMI_27 = U.NPATMI[0], U.NPATMI[1]
TP = U.TP
EQ_26, EQ_27 = U.EQUITY[0], U.EQUITY[1]
eps = lambda n: n * 1000 / SHARES
bvps = lambda e: e * 1000 / SHARES

C6 = ("- We cut FY26F loan growth to 2.3% from 11.7%, in line with the 1.5% delivered in 1H26. "
      "NII falls to VND24,531bn (-8.1% YoY), then recovers 9.9% in FY27F as NIM turns.\n"
      "- NIM troughs in FY26F as elevated NPLs freeze accrued interest income while funding costs "
      "remain sticky, before recovering in FY27F.\n"
      "- We set FY26F NPL at 5.8%, from below 4.5%, and FY27F at 4.0% from 3.1%. Reserves reached "
      "VND27.2tn at end-2Q26 (56.7% coverage) on VND7.1tn of 1H26 charges and almost no "
      "write-offs; a further VND{h2:.1f}tn charge in 2H26 funds VND{wo:.1f}tn of write-offs, or "
      "34% of the Group 5 balance, leaving coverage at {cov:.1f}%. Holding coverage near 50% is "
      "what caps the improvement at 5.8%: on the smaller loan book, 5.5% would have required net "
      "NPL recoveries in 2H26 rather than merely slower formation.\n"
      "- We set FY26F PBT at VND{pbt:,.0f}bn ({yoy:+.1f}% YoY), {vp:.1f}% below the "
      "board-approved plan of VND8,100bn, on CIR of {c26:.1f}% easing to {c27:.1f}% in FY27F "
      "and {c28:.1f}% in FY28F, with 2H26 costs {h2oy:+.1f}% on the first half. FY27F carries "
      "VND1,000bn of specific charge above what write-offs consume and FY28F VND2,000bn, taking PBT to "
      "VND{p27:,.0f}bn (+{g27:.0f}%) and VND{p28:,.0f}bn (+{g28:.0f}%).").format(
          pbt=U.PBT[0], yoy=U.PBT_YOY, vp=-U.VS_PLAN, c26=U.CIR[0], c27=U.CIR[1],
          c28=U.CIR[2], h2oy=(U.OPEX[0] - U.H1_OPEX) / U.H1_OPEX * 100 - 100,
          h2=U.H2_PROV / 1000, wo=U.WO26 / 1000, cov=U.COV26,
          p27=U.PBT[1], g27=U.PBT[1] / U.PBT[0] * 100 - 100,
          p28=U.PBT[2], g28=U.PBT[2] / U.PBT[1] * 100 - 100)

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
