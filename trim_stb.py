# -*- coding: utf-8 -*-
"""Take 100 words out of the STB investment-points block on both slides.

What goes: the FY25 provisioning cross-reference already implied by the reserve
walk, the superseded "the old 4.5% needed VND18tn" sentence, the second-order
comparisons in the PBT paragraph, and the qualifiers around the Viva City item.
Every figure that carries an assumption stays.
"""
import shutil
from pptx import Presentation
from apply_stb_cir import put, DECK

EN = {
 2: ("1H26 PBT reached VND4,136bn (-43.6% YoY), 51% of the VND8,100bn FY26 plan, of which "
     "VND2,106bn came in 1Q26. The shortfall stems from NIM compression amid deposit competition "
     "and a heavier provisioning charge."),
 4: ("The NPL ratio reached 7.54% at end-2Q26, up 1.13%p year-to-date and the highest in the "
     "system, against management guidance of approximately 5.6%. Group 3-5 balances rose "
     "approximately VND7,800bn to VND47,957bn, of which about 67% (VND32,000bn) is Group 5, while "
     "Group 4 more than doubled (+156%). We set FY26F NPL at 5.5%, from below 4.5%, and FY27F at "
     "4.0% from 3.1%. The clean-up is reserve-funded, not P&L-funded: reserves "
     "reached VND27.2tn at end-2Q26 — 56.7% coverage, up from 50.0% at end-FY25 — after VND7.1tn "
     "of 1H26 charges and almost no write-offs. A further VND4.0tn charge in 2H26 funds write-offs "
     "of VND11.8tn, or 37% of the Group 5 balance, leaving coverage at 51.1%. Holding coverage "
     "near 50% is what caps the improvement at 5.5%, and it needs 2H26 NPL formation at roughly "
     "a quarter of the 1H26 pace."),
 6: ("STB recorded VND7,331bn of PBT in 1H25 but only VND297bn in 2H25, as 4Q25 registered a "
     "pre-tax loss of VND3,360bn. We set FY26F PBT at VND8,100bn (+6.2% YoY), in line with the "
     "board-approved plan. The cost line does the lifting — 1H26 CIR came in at 35.6% against the "
     "42.9% previously carried, and we now assume 40.0% (-0.7%p YoY), 38.0% in FY27F and 36.0% "
     "in FY28F — with the balance taken back in provisioning. That implies 2H26 PBT of "
     "VND3,964bn, around 13x the 2H25 base. Other "
     "FY26F assumptions: NII of VND26,712bn (+0.1% YoY), NIM of 2.92% (-40bps YoY) and "
     "provisioning of VND11.5tn (+1.0% YoY); we flag 1H26 loan growth of 1.5% against the 11.7% "
     "carried for the full year. Separately, STB's seizure of 507 land-use right certificates at "
     "LDG's Viva City against VND350bn of overdue principal is immaterial in size but shows the "
     "collateral channel the write-off programme depends on."),
}

VN = {
 2: ("LNTT 1H26 đạt 4,136 tỷ đồng (-43.6% CK), hoàn thành 51% kế hoạch năm 8,100 tỷ đồng, trong "
     "đó Q1/2026 đóng góp 2,106 tỷ đồng. Mức sụt giảm đến từ NIM thu hẹp trong bối cảnh cạnh tranh "
     "huy động gay gắt và chi phí dự phòng tăng đáng kể."),
 3: ("Chất lượng tài sản suy giảm vượt mức ban lãnh đạo dự kiến: tỷ lệ nợ xấu đạt 7.54% cuối "
     "Q2/2026, tăng 1.13%p so với đầu năm và cao nhất hệ thống, so với ước tính khoảng 5.6% của "
     "ban lãnh đạo. Dư nợ nhóm 3-5 tăng khoảng 7,800 tỷ đồng lên 47,957 tỷ đồng, trong đó khoảng "
     "67% (32,000 tỷ đồng) xếp nhóm 5, nợ nhóm 4 tăng hơn gấp đôi (+156%). Chúng tôi đặt giả định "
     "nợ xấu FY26F ở 5.5% (từ dưới 4.5%) và FY27F ở 4.0% (từ 3.1%). Quá trình xử lý tài trợ từ "
     "nguồn dự phòng đã trích, không phải từ lợi nhuận: dự phòng đạt 27.2 nghìn tỷ đồng cuối "
     "Q2/2026 — bao phủ 56.7%, tăng từ 50.0% cuối 2025 — sau khi trích 7.1 nghìn tỷ đồng trong "
     "1H26 và gần như chưa xóa nợ. Trích thêm 4.0 nghìn tỷ đồng trong 2H26 đủ để xóa 11.8 nghìn tỷ "
     "đồng, tương đương 37% dư nợ nhóm 5, đưa bao phủ về 51.1%. Việc giữ bao phủ quanh 50% giới "
     "hạn mức cải thiện ở 5.5%, đồng thời cần nợ xấu phát sinh mới 2H26 chỉ bằng khoảng một phần "
     "tư nhịp 1H26."),
 5: ("STB ghi nhận 7,331 tỷ đồng LNTT trong 1H25 nhưng chỉ 297 tỷ đồng trong 2H25, do Q4/2025 lỗ "
     "trước thuế 3,360 tỷ đồng. Chúng tôi đặt dự phóng LNTT FY26F ở 8,100 tỷ đồng (+6.2% CK), "
     "ngang kế hoạch đã được ĐHĐCĐ thông qua. Chi phí hoạt động là động lực chính — CIR 1H26 "
     "chỉ 35.6% so với 42.9% dự phóng trước đây, và chúng tôi điều chỉnh về 40.0% (-0.7%p CK), "
     "38.0% FY27F và 36.0% FY28F — phần chênh còn lại đưa vào chi phí dự phòng. Mức này hàm ý "
     "LNTT 2H26 khoảng 3,964 tỷ đồng, tương đương khoảng 13 lần nền 2H25."),
 6: ("Các giả định FY26F khác: NII 26,712 tỷ đồng (+0.1% CK), NIM 2.92% (-40bps CK) và chi phí dự "
     "phòng 11.5 nghìn tỷ đồng (+1.0% CK); lưu ý tăng trưởng tín dụng 1H26 chỉ 1.5% so với 11.7% "
     "dự phóng cả năm. Ở diễn biến khác, việc Sacombank thu giữ 507 giấy chứng nhận quyền sử dụng "
     "đất tại dự án Viva City đối với 350 tỷ đồng dư nợ gốc quá hạn tuy chưa trọng yếu nhưng cho "
     "thấy kênh xử lý tài sản đảm bảo mà chương trình xóa nợ 2H26 phụ thuộc vào."),
}


def main():
    shutil.copy(DECK, DECK + '.bak')
    prs = Presentation(DECK)
    sid = lambda sl, i: next(s for s in sl.shapes if s.shape_id == i)
    for slide_i, spec in ((0, EN), (1, VN)):
        tf = sid(prs.slides[slide_i], 15).text_frame
        for pi, txt in spec.items():
            put(tf.paragraphs[pi], txt)
    prs.save(DECK)


if __name__ == '__main__':
    main()
    prs = Presentation(DECK)
    for i, (nm, before) in enumerate((('STB EN', 462), ('STB VN', 614))):
        tf = next(s for s in prs.slides[i].shapes if s.shape_id == 15).text_frame
        tot = sum(len(p.text.split()) for p in tf.paragraphs)
        print('%-8s %d -> %d words  (%+d)' % (nm, before, tot, tot - before))
