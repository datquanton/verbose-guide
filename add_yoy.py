# -*- coding: utf-8 -*-
"""Insert % YoY rows under Revenue and NPATMI on both FPT slides.
Only two fit: the table starts at 11.62cm on a 19.05cm slide, so 15 rows at
0.45cm ends at 18.37cm; 17 rows would finish 0.6mm from the edge."""
import copy, shutil
from pptx import Presentation
from pptx.util import Cm

DECK='/home/user/verbose-guide/MASVN_RS_WM_2H26_outlook_Equity_VN_2026_STBFPT_31July2026.pptx'
A='{http://schemas.openxmlformats.org/drawingml/2006/main}'
REV=['—','+19.4%','+11.7%','-18.4%*','+15.3%','+16.1%']
NPAT=['—','+21.5%','+20.5%','+15.6%','+15.8%','+16.6%']
NOTE={2:('Note: FPT Telecom equity-accounted from FY26F, consolidated in FY23-25. * against a '
 'restated FY25 revenue of VND50,607bn the change is +13.2%; NPATMI is unaffected by the change '
 'of basis. Source: Company data, Mirae Asset Vietnam Research'),
      3:('Ghi chú: FPT Telecom hợp nhất theo phương pháp VCSH từ FY26F, hợp nhất toàn bộ giai đoạn '
 'FY23-25. * so với doanh thu FY25 tính lại 50,607 tỷ đồng, mức tăng là +13.2%; LNST-CĐTS không '
 'đổi khi chuyển phương pháp. Nguồn: Dữ liệu công ty, Mirae Asset Vietnam Research')}

shutil.copy(DECK, DECK+'.bak')
prs=Presentation(DECK); log=[]

def write(cell, text):
    """Overwrite a cell using its own first run, keeping the template formatting."""
    para=cell.text_frame.paragraphs[0]
    assert para.runs, cell.text
    para.runs[0].text=text
    for r in para.runs[1:]: r.text=''
    for p in cell.text_frame.paragraphs[1:]:
        for r in p.runs: r.text=''

for si in (2,3):
    tbl=next(x for x in prs.slides[si].shapes if x.shape_id==16).table._tbl
    for prefixes,vals in [(('NPATMI','LNST-CĐTS'),NPAT),(('Revenue','Doanh thu'),REV)]:
        t=next(x for x in prs.slides[si].shapes if x.shape_id==16).table
        idx=next(i for i in range(len(t.rows)) if t.cell(i,0).text.startswith(prefixes))
        rows=tbl.findall(A+'tr')
        rows[idx].addnext(copy.deepcopy(rows[idx]))
        t=next(x for x in prs.slides[si].shapes if x.shape_id==16).table
        write(t.cell(idx+1,0),'   % YoY')
        for c,v in enumerate(vals,start=1): write(t.cell(idx+1,c),v)
        log.append('slide %d: %% YoY inserted after %s'%(si+1,t.cell(idx,0).text[:16]))
    t=next(x for x in prs.slides[si].shapes if x.shape_id==16).table
    for r in t.rows: r.height=Cm(0.45)
    write(t.cell(len(t.rows)-1,0), NOTE[si])
    log.append('slide %d: %d rows, note rewritten'%(si+1,len(t.rows)))
prs.save(DECK)

prs=Presentation(DECK)
sh=next(x for x in prs.slides[2].shapes if x.shape_id==16); t=sh.table
print('%d rows, %.2fcm tall, bottom %.2fcm on a %.2fcm slide\n'
      %(len(t.rows),sh.height/360000,(sh.top+sh.height)/360000,prs.slide_height/360000))
for r in range(len(t.rows)):
    print('  %-26s %s'%(t.cell(r,0).text[:26],[t.cell(r,c).text for c in range(1,7)]))
print('\n'+'\n'.join(log))
