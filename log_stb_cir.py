# -*- coding: utf-8 -*-
"""Append the 5.5%-NPL / 40-38-36% CIR revision to the internal audit trail."""
import openpyxl
from openpyxl.styles import Font
from fix_stb_model import cascade

WB = '/home/user/verbose-guide/INTERNAL_Sources_and_Assumptions_Aug26.xlsx'
C = {c['y']: c for c in cascade()}

ROWS = [
    ('', 'STB — REVISION 04/08/2026: giữ bao phủ 50% -> NPL 5.5%; CIR 40/38/36% FY26-28F',
     '', '', '', '', ''),
    ('R1', 'Dự phòng đã trích cuối Q2/2026', '27,177', 'VNDbn', 'MODEL',
     'FinModel_STB_2Q26 Model!CA cột quý 2Q26; FY25 20,056 + 7,119 trích 1H26',
     'Bao phủ 56.7% (27,177/47,957), tăng từ 50.0% cuối 2025 — gần như chưa xóa nợ trong 1H26'),
    ('R2', 'Xóa nợ FY26F', '%.0f' % C[2026]['wo'], 'VNDbn', 'DERIVED',
     'Model!Y287 = -1.71% x dư nợ 689,832 (trước: -0.95%)',
     'Nghiệm của bài toán giữ bao phủ 50%; tương đương 37% dư nợ nhóm 5 (~32,000)'),
    ('R3', 'Tỷ lệ trích/xóa FY26F', '0.8845x', 'x', 'MAS',
     'Model!Y278 = -Y279*0.8845 (1.5x -> 0.85x -> 0.8845x)',
     'Xử lý nợ tài trợ từ nguồn dự phòng đã trích, không từ P&L. Giữ 1.5x trên mức xóa nợ '
     'này là nguyên nhân làm LNTT sụt 64% mà CV đã bác'),
    ('R4', 'Dự phòng đã trích cuối FY26F / bao phủ',
     '%.0f / %.1f%%' % (C[2026]['res'], C[2026]['cov'] * 100), 'VNDbn / %', 'DERIVED',
     'gen 4,665 + spec 14,309; NPL 5.5% x 689,832 = 37,941',
     'Đúng mục tiêu "giữ bao phủ 50%" của CV'),
    ('R5', 'NPL FY26F / FY27F / FY28F', '5.5 / 4.0 / 2.7', '%', 'MAS',
     'NPL!N26=0.933 N27=0.012 N28=0.009 N29=0.012 N30=0.034 (tổng 1.000)',
     'Hàm ý nợ xấu phát sinh mới 2H26 = 1,780 tỷ, bằng 23% nhịp 1H26 (7,800) — khớp giả '
     'định "chậm lại còn 20% nhịp 1H" CV đưa ra trước đó'),
    ('R6', 'CIR FY26F / FY27F / FY28F',
     '%.1f / %.1f / %.1f' % tuple(C[y]['cir'] * 100 for y in (2026, 2027, 2028)), '%', 'MAS',
     'Model!Y132=X132*1 và Y134=X134*1 (lương và chi phí khác đi ngang so với FY25); '
     'Z132/Z134 = *1.015; AA132/AA134 = *1.106. Khấu hao Y133/Z133/AA133 giữ nguyên build cũ',
     'CIR 1H26 thực tế 35.6% (opex 6,233 / TOI 17,488). Build cũ cho 42.9/42.6/40.5%, tức opex '
     '2H26 phải tăng 26.7% so với 1H26 — không có cơ sở. Hệ số nhân là nghiệm của mục tiêu CIR '
     'CV đặt ra, áp chung cho cả dòng lương và chi phí khác'),
    ('R6b', 'Ràng buộc của mục tiêu CIR 38% năm FY27F', '+1.5%', '% tăng opex', 'GAP',
     'TOI FY27F +11.1% nhưng khấu hao Z133 = Y133*1.2 (+20%) theo build gốc',
     'Khấu hao nhảy 20% chiếm hết dư địa, nên lương + chi phí khác chỉ được tăng 1.5% để về '
     '38%. Nếu hệ số khấu hao 1.2x không có cơ sở (đây là input của bản gốc, tôi không sửa), '
     'hạ về 1.1x sẽ cho lương + chi phí khác tăng 4.3% — hợp lý hơn. CẦN CV XÁC NHẬN'),
    ('R7', 'Opex 2H26 hàm ý', '%.0f' % (C[2026]['opex'] - 6233.19), 'VNDbn', 'DERIVED',
     'FY26F %.0f - 1H26 thực tế 6,233' % C[2026]['opex'],
     '+%.1f%% so với 1H26 — vẫn phản ánh tính mùa vụ dồn về cuối năm, không phải cắt giảm chi phí'
     % ((C[2026]['opex'] - 6233.19) / 6233.19 * 100 - 100)),
    ('R8', 'LNTT / LNST FY26F',
     '%.0f / %.0f' % (C[2026]['pbt'], C[2026]['npatmi']), 'VNDbn', 'DERIVED',
     'TOI 32,956 - opex %.0f - dự phòng %.0f' % (C[2026]['opex'], C[2026]['prov']),
     '+%.1f%% CK. Hàm ý LNTT 2H26 %.0f tỷ = %.0fx nền 2H25 (297 tỷ) và +%.1f%% so với 1H26'
     % (C[2026]['pbt'] / 7628.025 * 100 - 100, C[2026]['pbt'] - 4136.10,
        (C[2026]['pbt'] - 4136.10) / 297, (C[2026]['pbt'] - 4136.10) / 4136.10 * 100 - 100)),
    ('R9', 'Dự phòng P&L FY26F', '%.0f' % C[2026]['prov'], 'VNDbn', 'DERIVED',
     'chung 687 + cụ thể 10,027 + VAMC 377',
     '-2.6% CK so với 11,384 của FY25; gần như không đổi so với 10,889 của bản trước'),
    ('C1', 'Model!X284 dự phòng cụ thể đầu kỳ', '4,891 -> 16,078', 'VNDbn', 'CONFLICT',
     'Model!X264 (BCĐKT FY25) = 20,056 nhưng bảng chuyển động X274+X284 chỉ 8,869',
     'Lỗi có sẵn trong model: mọi tỷ lệ bao phủ dự phóng trước đây đều vô nghĩa. Đã sửa để '
     'X274+X284 = 20,056'),
    ('G14', 'Cân đối kế toán sau khi sửa X284', '0', 'VNDbn', 'MODEL',
     'Model!Y103 = 0 sau khi CV mở lại bằng Excel (bản 2b63c432)',
     'ĐÃ ĐÓNG — cảnh báo lệch -6,755 tỷ của tôi là SAI. Model tự cân đối; tổng tài sản '
     'Y61 = 1,014,277 (không phải 1,007,118 tôi ước tính)'),
    ('R10', 'Đối chiếu sau khi Excel tính lại', 'khớp', '', 'MODEL',
     'bản 2b63c432 do CV mở lại bằng Excel',
     'Opex Y135 13,182/13,913/15,367 khớp tuyệt đối; dự phòng Y254 11,091 khớp; dự phòng đã '
     'trích Y286 18,973 và bao phủ 50.0% khớp tuyệt đối'),
    ('C2', 'TOI dịch chuyển khi Excel tính lại', '32,662 vs 32,956', 'VNDbn', 'CONFLICT',
     'Model!Y117 = NII + phí + thu nhập khác',
     'Dự phòng đã trích lớn hơn làm cho vay thuần giảm -> thu nhập lãi giảm. NII FY26F về '
     '26,712 (+0.1% CK) từ 27,010. Hệ quả CIR trôi lên 40.36/37.66/36.48%, đã giải lại hệ '
     'số nhân opex về 0.9886/1.039/1.0739 để đúng 40/38/36%'),
    ('N1', 'NPL!DG6:DG11 cột 2Q26', 'BY -> BX', '', 'MAS',
     "trỏ sang 'Notes(Quarter)'!BX81:BX86 (cột chèn thêm đẩy dữ liệu sang BX, BW là cột nhãn)",
     'Tổng 636,029; nhóm 1-5: 571,245 / 16,827 / 7,200 / 8,483 / 32,274. NPL 47,957 = 7.540% '
     '— khớp tuyệt đối con số trên slide'),
    ('G19', 'NPL hàng 19-21 lệch một dòng ở khối theo quý', '', '', 'GAP',
     'DF19 = DF8/DF$22 (nợ nhóm 2 / nợ xấu) trong khi nhãn ghi "3) Substandard"',
     'CHƯA SỬA — lỗi có sẵn ở MỌI cột quý, không riêng 2Q26; hàng 19-21 cộng lại không bằng '
     '100%. Không ảnh hưởng tỷ lệ NPL (hàng 23) vì hàng 22 = SUM(9:11) vẫn đúng. Sửa riêng '
     'cột DG sẽ phá nhóm shared formula'),
    ('G15', 'Giá mục tiêu vs sheet Valuation', '77,800 vs 65,600', 'VND', 'CONFLICT',
     'Valuation!B1 = J16 = P/B hợp lý FY27F x BPS FY27F',
     'Sheet Valuation cho 56,100 trước điều chỉnh và ~65,600 sau (ROE bền vững FY27F lên '
     '15.5%, BPS 37,822). Slide vẫn để 77,800 — CHƯA ĐỊNH GIÁ LẠI, cần CV quyết'),
    ('G16', 'Giá mục tiêu ghi 77,500 trong file stock pick', '77,500 vs 77,800', 'VND', 'CONFLICT',
     'Stock Pick!D6 và Target Price!C13 ghi 77,500; cột J6/L6 lại tính trên 77,800',
     'CHƯA SỬA — chênh 0.4%, cần CV xác nhận số nào đúng'),
    ('R11', 'LNTT FY26F đưa về ngang kế hoạch', '8,100', 'VNDbn', 'MAS',
     'Model!Y278 0.85x -> 0.8845x; dự phòng 11,091 -> 11,498',
     'CV chọn lấy phần chênh 407 tỷ từ chi phí dự phòng thay vì hạ tăng trưởng tín dụng hay '
     'nâng CIR. NPL giữ 5.5%, CIR giữ 40%, bao phủ lên 51.1% từ 50.0%'),
    ('C3', 'Kế hoạch LNTT FY26 8,100 tỷ', 'suy ra', 'VNDbn', 'CONFLICT',
     'Suy ra từ 4,136/51% theo trích dẫn báo chí "hoàn thành 51% mục tiêu"',
     'CHƯA CÓ NGHỊ QUYẾT ĐHĐCĐ TRONG HỒ SƠ. Nay con số này là mỏ neo của dự phóng LNTT nên '
     'cần lấy nguồn gốc trước khi phát hành. KH FY25 ~14,670 (7,628/52%) cũng suy ra tương tự'),
    ('C4', 'Slide ghi "ban lãnh đạo dự kiến ~5.6%" nợ xấu', '5.6%', '%', 'CONFLICT',
     'Dòng 10 ghi 5.6% xuất hiện ở bản 24/07 dưới dạng "ước ~5.6%" — tức ước tính của MAS',
     'CHƯA SỬA — slide đang gán cho ban lãnh đạo. Nếu không có công bố của STB thì phải viết '
     'lại, đây là chỗ duy nhất trong khối STB có nguy cơ trình bày ước tính MAS như guidance'),
    ('G17', 'Tăng trưởng tín dụng FY26F 11.7% vs 1.5% thực hiện 1H26', '', '', 'GAP',
     'Model!Y206 = 10.1%; slide ghi 11.7%',
     'CHƯA XỬ LÝ — CV đã cân nhắc dùng làm đòn bẩy đưa LNTT về kế hoạch nhưng chọn dự phòng. '
     'Dư nợ dựng từ dưới lên theo 6 phân khúc (Model!Y23:Y28) nên phải tính lại bằng Excel'),
    ('G18', 'Model chưa mở lại bằng Excel', '', '', 'GAP',
     'fullCalcOnLoad=1 đã bật',
     'Toàn bộ số ở trên tính lại bằng Python theo đúng chuỗi công thức của model '
     '(fix_stb_model.cascade); cần mở Excel đối chiếu trước khi phát hành'),
]


def main():
    wb = openpyxl.load_workbook(WB)
    ws = wb['STB FPT 31Jul']
    r = ws.max_row + 2
    for vals in ROWS:
        for ci, v in enumerate(vals, start=1):
            if v != '':
                ws.cell(row=r, column=ci, value=v)
        if vals[0] == '':
            ws.cell(row=r, column=2).font = Font(bold=True)
        r += 1
    wb.save(WB)
    print('appended %d rows to "STB FPT 31Jul", now %d rows' % (len(ROWS), ws.max_row))


if __name__ == '__main__':
    main()
