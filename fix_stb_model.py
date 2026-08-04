# -*- coding: utf-8 -*-
"""Book the NPL path: 7.54% (2Q26) -> 5.9% (end-26) -> 4.0% (end-27).
NPL!26:31 is the hardcoded loan-grading mix; everything downstream keys off it."""
import shutil, zipfile
from lxml import etree
SRC='/home/user/verbose-guide/FinModel_STB_2Q26.xlsx'
shutil.copy('/root/.claude/uploads/041665b7-4ff3-507f-a1e8-7a7ed4160156/f6576dae-FinModel_STB_2Q26.xlsx',SRC)
NS='{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
EDITS={  # cell: (expected, new, note)
 'N26':('0.9429999999999999','0.929','Current'),   'N27':('1.2E-2','0.012','Special mention'),
 'N28':('5.0000000000000001E-3','0.009','Substandard'),
 'N29':('5.0000000000000001E-3','0.011','Doubtful'),
 'N30':('3.5000000000000003E-2','0.039','Bad'),
 'O26':('0.96199999999999997','0.950','Current'),  'O27':('0.01','0.010','Special mention'),
 'O28':('4.0000000000000001E-3','0.007','Substandard'),
 'O29':('8.9999999999999993E-3','0.010','Doubtful'),
 'O30':('1.7999999999999999E-2','0.023','Bad'),
 'P26':('0.96799999999999997','0.965','Current - fixes a mix summing to 1.003'),
}
zin=zipfile.ZipFile(SRC+'.src') if False else zipfile.ZipFile(SRC)
data=zin.read('xl/worksheets/sheet2.xml'); zin.close()
root=etree.fromstring(data); log=[]; seen=set()
for c in root.iter(NS+'c'):
    ref=c.get('r')
    if ref not in EDITS: continue
    exp,new,note=EDITS[ref]; seen.add(ref)
    assert c.find(NS+'f') is None, '%s is a formula, not an input'%ref
    v=c.find(NS+'v')
    assert abs(float(v.text)-float(exp))<1e-9, (ref,v.text,exp)   # float text varies
    log.append('NPL!%-4s %-22s %-8s -> %-6s  %s'%(ref,note,v.text[:8],new,''))
    v.text=new
assert not set(EDITS)-seen, set(EDITS)-seen
out=etree.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
zin=zipfile.ZipFile(SRC); items=[(i,zin.read(i.filename)) for i in zin.infolist()]; zin.close()
zout=zipfile.ZipFile(SRC,'w',zipfile.ZIP_DEFLATED)
for it,d in items:
    if it.filename=='xl/worksheets/sheet2.xml': d=out
    elif it.filename=='xl/workbook.xml' and 'fullCalcOnLoad' not in d.decode():
        d=d.decode().replace('<calcPr ','<calcPr fullCalcOnLoad="1" ').encode()
        log.append('workbook.xml: fullCalcOnLoad=1')
    zout.writestr(it,d)
zout.close()
print('\n'.join(log))
print('\nresulting NPL ratios:  FY26F %.1f%%   FY27F %.1f%%   FY28F %.1f%% (unchanged)'
      %((0.009+0.011+0.039)*100,(0.007+0.010+0.023)*100,(0.005+0.009+0.013)*100))
