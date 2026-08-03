# -*- coding: utf-8 -*-
"""-15% on the FPT investment-points block, mirrored in Vietnamese."""
import shutil
from pptx import Presentation
DECK='/home/user/verbose-guide/MASVN_RS_WM_2H26_outlook_Equity_VN_2026_STBFPT_31July2026.pptx'

EN={1:("1H26 tracking ahead of plan: revenue VND26,269bn (+12.6% YoY) and PBT VND5,714bn (+18.1% "
 "YoY), 45%/49% of the FY26 plan, with the group PBT margin widening to 21.8%. In 2Q26: revenue "
 "VND13,789bn, PBT VND2,910bn, NPATMI VND2,568bn (+14% YoY). Technology revenue VND23,138bn (+15% "
 "YoY; 88% of group) and PBT VND3,314bn (+16.9%); Education, investment and others fell 2.1% to "
 "VND3,131bn yet contributed 42% of group PBT on a ~77% margin."),
 2:("Public-sector digitalization underpins the domestic pipeline: Domestic IT grew fastest in "
 "6M26 at VND4,236bn (+22.5% YoY), segment PBT doubling to VND308bn on national "
 "digital-transformation wins — multi-year work outside the global IT cycle, though its 7.3% "
 "margin dilutes the blend. Signed contract value for Global IT reached VND26,338bn in 1H26, "
 "+32.3% YoY, including 14 deals above USD10mn — a book-to-bill of 1.39x against 1.07-1.22x "
 "through FY21-25. On that basis we look for Global IT to reaccelerate to +16.7% in FY27F and "
 "+17.7% in FY28F, from +14.7% in FY26F and +13.4% in 1H26, with the US book cut to +5.9%."),
 4:("Projection and valuation: we forecast FY26F NPATMI of VND10,944bn (+15.6% YoY), FY27F "
 "VND12,674bn (+15.8%) and FY28F VND14,774bn (+16.6%). Associate income — FPT Telecom (45.66%), "
 "equity-accounted from FY26, with FPT Retail, Synnex FPT and FPT Online — rises to VND2,608bn in "
 "FY26F and VND3,449bn by FY28F, and grew 40.8% YoY in 1H26. Operating leverage carries the rest: "
 "SG&A falls from 17.6% of sales to 16.5% by FY28F, gross margin unchanged. ROE holds near 27% on "
 "net cash of around 60% of equity and a maintained DPS of VND2,000. We raise our DCF (FCFF) "
 "target price to VND87,950 from VND78,750, cutting the assumed cost of debt to 9.0% from 11.5% — "
 "FPT's realised funding cost in 1H26 was 4.0% — which lowers WACC to 11.4%; the equity risk "
 "premium stays at 8.97% and long-term growth at 1.5% to carry the risk that AI lowers IT "
 "services pricing. At VND71,700 the stock trades at 11.2x FY26F earnings against a five-year "
 "median above 18x; at the target price, 13.7x FY26F and 11.8x FY27F, implying 23% upside (BUY). "
 "AI newsflow remains supportive, including an expanded Microsoft partnership across ASEAN, Japan "
 "and Korea and data-intermediary certification with the Ministry of Public Security's National "
 "Data Centre. Risks: (1) AI-driven price deflation outpacing our long-term growth assumption (2) "
 "subdued US and global IT spending and tariff-related contract delays (3) JPY/USD volatility.")}

VN={1:("KQKD 1H26 vượt tiến độ kế hoạch: doanh thu 26,269 tỷ đồng (+12.6% CK) và LNTT 5,714 tỷ "
 "(+18.1% CK), đạt 45%/49% kế hoạch năm, biên LNTT mở rộng lên 21.8%. Q2/2026: doanh thu 13,789 "
 "tỷ, LNTT 2,910 tỷ, LNST-CĐTS 2,568 tỷ (+14% CK). Công nghệ đạt 23,138 tỷ (+15% CK; 88% doanh "
 "thu tập đoàn) và LNTT 3,314 tỷ (+16.9%); Giáo dục, đầu tư và khác giảm 2.1% về 3,131 tỷ nhưng "
 "vẫn đóng góp 42% LNTT tập đoàn."),
 2:("Số hóa khu vực công là nền tảng của danh mục trong nước: CNTT trong nước tăng nhanh nhất "
 "6T26, đạt 4,236 tỷ đồng (+22.5% CK), LNTT mảng tăng gấp đôi lên 308 tỷ nhờ trúng thầu chuyển "
 "đổi số quốc gia — nguồn việc nhiều năm, ngoài chu kỳ CNTT toàn cầu, tuy biên 7.3% làm loãng "
 "biên chung. Doanh thu ký mới CNTT nước ngoài đạt 26,338 tỷ trong 1H26 (+32.3% CK), gồm 14 dự án "
 "trên 10 triệu USD — tỷ lệ ký mới/doanh thu 1.39 lần so với 1.07-1.22 lần giai đoạn FY21-25. "
 "Trên cơ sở đó, dự phóng CNTT nước ngoài tăng lên +16.7% FY27F và +17.7% FY28F, từ +14.7% FY26F "
 "và +13.4% của 1H26; Mỹ hạ về +5.9%."),
 4:("Dự phóng và định giá: LNST-CĐTS FY26F đạt 10,944 tỷ đồng (+15.6% CK), FY27F 12,674 tỷ "
 "(+15.8%) và FY28F 14,774 tỷ (+16.6%). Lợi nhuận từ công ty liên kết — FPT Telecom (45.66%, hạch "
 "toán theo phương pháp VCSH từ FY26), FPT Retail, Synnex FPT và FPT Online — tăng lên 2,608 tỷ "
 "FY26F và 3,449 tỷ FY28F, đã tăng 40.8% CK trong 1H26. Phần còn lại đến từ đòn bẩy hoạt động: "
 "chi phí bán hàng và quản lý giảm từ 17.6% doanh thu xuống 16.5% vào FY28F, biên gộp giữ nguyên. "
 "ROE quanh 27% nhờ tiền ròng khoảng 60% VCSH và cổ tức 2,000 đồng/cp. Chúng tôi nâng giá mục "
 "tiêu DCF (FCFF) lên 87,950 đồng từ 78,750 đồng, hạ chi phí nợ vay về 9.0% từ 11.5% — mức thực "
 "tế 1H26 là 4.0% — đưa WACC xuống 11.4%; phần bù rủi ro vốn cổ phần giữ 8.97% và tăng trưởng dài "
 "hạn 1.5% để phản ánh rủi ro AI làm giảm giá dịch vụ CNTT. Tại 71,700 đồng, cổ phiếu giao dịch ở "
 "11.2x P/E FY26F so với trung vị 5 năm trên 18x; tại giá mục tiêu là 13.7x FY26F và 11.8x FY27F, "
 "hàm ý tiềm năng tăng 23% (MUA). Rủi ro: (1) giảm phát giá do AI nhanh hơn giả định tăng trưởng "
 "dài hạn (2) chi tiêu CNTT tại Mỹ và toàn cầu thấp cùng hợp đồng trì hoãn do thuế quan (3) biến "
 "động tỷ giá JPY/USD.")}

shutil.copy(DECK,DECK+'.bak')
prs=Presentation(DECK)
for slide_i,spec in [(2,EN),(3,VN)]:
    tf=next(x for x in prs.slides[slide_i].shapes if x.shape_id==15).text_frame
    for pi,txt in spec.items():
        para=tf.paragraphs[pi]; para.runs[0].text=txt
        for r in para.runs[1:]: r.text=''
prs.save(DECK)

prs=Presentation(DECK)
BEFORE={'FPT EN':(79,112,238),'FPT VN':(97,143,265)}
for si,nm in [(2,'FPT EN'),(3,'FPT VN')]:
    tf=next(x for x in prs.slides[si].shapes if x.shape_id==15).text_frame
    w=[len(''.join(r.text for r in p.runs).split()) for p in tf.paragraphs]
    blk=w[0]+w[1]+w[2]+w[4]; b=2+sum(BEFORE[nm])
    print('%-7s pasted block %d -> %d  (%+.1f%%)   P1 %d->%d  P2 %d->%d  P4 %d->%d'
          % (nm,b,blk,blk/b*100-100,BEFORE[nm][0],w[1],BEFORE[nm][1],w[2],BEFORE[nm][2],w[4]))
    print('        deck total incl. the AI-debate line: %d' % sum(w))
