# -*- coding: utf-8 -*-
"""Cross-check the STB slides against the booked NPL path and the workbook."""
import openpyxl, zipfile
from lxml import etree
from pptx import Presentation
DECK='/home/user/verbose-guide/MASVN_RS_WM_2H26_outlook_Equity_VN_2026_STBFPT_31July2026.pptx'
PICK='/home/user/verbose-guide/Stock_Pick_and_Forecast_Aug26_MAS_RS_EN_updated.xlsx'
MODEL='/home/user/verbose-guide/FinModel_STB_2Q26.xlsx'
NS='{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
TP,L26,L27=77800.,689832.3,791226.9
fails=[]
def check(n,c,d=''):
    print('%-4s %-58s %s'%('OK' if c else 'FAIL',n,d))
    if not c: fails.append(n)
z=zipfile.ZipFile(MODEL); root=etree.fromstring(z.read('xl/worksheets/sheet2.xml'))
M={c.get('r'):float(c.find(NS+'v').text) for c in root.iter(NS+'c')
   if c.find(NS+'v') is not None and c.find(NS+'f') is None and c.get('t')!='s'}
for col,lab,tgt in (('N','FY26F',0.059),('O','FY27F',0.040)):
    npl=sum(M['%s%d'%(col,r)] for r in (28,29,30))
    tot=sum(M['%s%d'%(col,r)] for r in (26,27,28,29,30))
    check('model %s NPL mix = %.1f%%'%(lab,tgt*100), abs(npl-tgt)<1e-9,'%.3f%%'%(npl*100))
    check('model %s grading mix sums to 1.000'%lab, abs(tot-1)<1e-9,'%.4f'%tot)
check('model FY28F mix now sums to 1.000',
      abs(sum(M['P%d'%r] for r in (26,27,28,29,30))-1)<1e-9)
prs=Presentation(DECK); num=lambda s: float(s.replace(',',''))
def grab(i):
    sh={x.shape_id:x for x in prs.slides[i].shapes}
    t=sh[16].table
    return ({sh[12].table.cell(r,0).text: sh[12].table.cell(r,1).text.strip() for r in range(4)},
            {t.cell(r,0).text:[t.cell(r,c).text.strip() for c in range(4,7)] for r in range(1,12)},
            sh[15].text_frame.text)
en_box,en_tbl,en_txt=grab(0); vn_box,vn_tbl,vn_txt=grab(1)
row=lambda tbl,k:[num(x) for x in next(v for kk,v in tbl.items() if kk.startswith(k))]
pbt=row(en_tbl,'Operating profit'); npat=row(en_tbl,'Net Profit')
eps=row(en_tbl,'EPS'); pe=row(en_tbl,'P/E'); pb=row(en_tbl,'P/B'); bv=row(en_tbl,'BVPS')
check('FY26F PBT 7,934 (model)', pbt[0]==7934); check('FY26F NPATMI 6,177 (model)', npat[0]==6177)
check('FY27F NPATMI 9,890 (model)', npat[1]==9890)
check('FY26F PBT growth +4.0% on FY25 7,628', abs(pbt[0]/7628-1.040)<0.001,'%.1f%%'%(pbt[0]/7628*100-100))
check('2H26 PBT = FY26F - 1H26 4,136', abs(pbt[0]-4136-3798)<1,'%.0f'%(pbt[0]-4136))
for i,y in enumerate((26,27,28)):
    check('FY%dF P/E = TP / EPS'%y, abs(TP/eps[i]-pe[i])<0.06,'%.2f vs %.2f'%(TP/eps[i],pe[i]))
    check('FY%dF P/B = TP / BVPS'%y, abs(TP/bv[i]-pb[i])<0.051   # slide shows one decimal,'%.2f vs %.2f'%(TP/bv[i],pb[i]))
check('EPS consistent with NPATMI and a 2,060mn share count',
      all(abs(n/2.0604-e)<3 for n,e in zip(npat,eps)))
check('box NPATMI = table FY26F', num(en_box['NPATMI (26F, VNDbn)'])==npat[0])
check('box P/E = table FY26F', num(en_box['P/E (26F, x)'])==pe[0])
for a,b in [('Operating profit','Lợi nhuận hoạt động'),('Net Profit','LNST'),('EPS','EPS'),
            ('P/E','P/E'),('P/B','P/B'),('BVPS','Giá trị sổ sách')]:
    check('EN and VN agree on %s'%a, row(en_tbl,a)==row(vn_tbl,b))
for s,t in [('5.9%','FY26F NPL'),('4.0%','FY27F NPL'),('8.9tn','2H26 write-offs'),
            ('21.6tn','existing reserves'),('45%','coverage'),('7,934','FY26F PBT'),
            ('3,798','2H26 PBT'),('1.5%','1H26 loan growth')]:
    check('narrative states %s (%s)'%(s,t), s in en_txt)
for old in ['8,455','6,583','12,311','below 4.5% is no longer attainable','11.7% loan growth',
            '4,319','+10.8%']:
    check('stale text "%s" gone'%old[:34], old not in en_txt and old not in str(en_tbl))
ws=openpyxl.load_workbook(PICK)['Stock Pick']; tp=openpyxl.load_workbook(PICK)['Target Price and Forecast']
check('workbook NPATMI = deck', ws['F6'].value==npat[0] and ws['G6'].value==npat[1])
check('workbook P/E, P/B = deck', abs(ws['J6'].value-pe[0])<0.06 and abs(ws['L6'].value-pb[0])<0.051)
check('TP sheet = deck', tp['D13'].value==npat[0] and tp['E13'].value==npat[1])
print('\n'+'='*78)
print('%d FAILED: %s'%(len(fails),fails) if fails else 'ALL CHECKS PASSED')
