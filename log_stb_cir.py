# -*- coding: utf-8 -*-
"""Append the 5.5%-NPL / 39.9%-CIR revision to the internal audit trail."""
import openpyxl
from openpyxl.styles import Font
from fix_stb_model import cascade

WB = '/home/user/verbose-guide/INTERNAL_Sources_and_Assumptions_Aug26.xlsx'
C = {c['y']: c for c in cascade()}

ROWS = [
    ('', 'STB — REVISION 04/08/2026: giữ bao phủ 50% -> NPL 5.5%; CIR về 38-40%',
     '', '', '', '', ''),
    ('R1', 'Dự phòng đã trích cuối Q2/2026', '27,177', 'VNDbn', 'MODEL',
     'FinModel_STB_2Q26 Model!CA cột quý 2Q26; FY25 20,056 + 7,119 trích 1H26',
     'Bao phủ 56.7% (27,177/47,957), tăng từ 50.0% cuối 2025 — gần như chưa xóa nợ trong 1H26'),
    ('R2', 'Xóa nợ FY26F', '%.0f' % C[2026]['wo'], 'VNDbn', 'DERIVED',
     'Model!Y287 = -1.71% x dư nợ 689,832 (trước: -0.95%)',
     'Nghiệm của bài toán giữ bao phủ 50%; tương đương 37% dư nợ nhóm 5 (~32,000)'),
    ('R3', 'Tỷ lệ trích/xóa FY26F', '0.85x', 'x', 'MAS',
     'Model!Y278 = -Y279*0.85 (trước: *1.5)',
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
     'Model!Y132=X132*1 (lương đi ngang), Y134=X134*0.99, Z132=Y132*1.08, AA132=Z132*1.1, '
     'AA134=Z134*1.15',
     'CIR 1H26 thực tế 35.6% (opex 6,233 / TOI 17,488). Build cũ cho 42.9% FY26F, tức opex '
     '2H26 phải tăng 26.7% so với 1H26 — không có cơ sở'),
    ('R7', 'Opex 2H26 hàm ý', '%.0f' % (C[2026]['opex'] - 6233.19), 'VNDbn', 'DERIVED',
     'FY26F %.0f - 1H26 thực tế 6,233' % C[2026]['opex'],
     '+10.9% so với 1H26 — vẫn phản ánh tính mùa vụ dồn về cuối năm, không phải cắt giảm chi phí'),
    ('R8', 'LNTT / LNST FY26F',
     '%.0f / %.0f' % (C[2026]['pbt'], C[2026]['npatmi']), 'VNDbn', 'DERIVED',
     'TOI 32,956 - opex %.0f - dự phòng %.0f' % (C[2026]['opex'], C[2026]['prov']),
     '+14.3% CK. Hàm ý LNTT 2H26 4,580 tỷ = 15x nền 2H25 (297 tỷ) và +10.7% so với 1H26'),
    ('R9', 'Dự phòng P&L FY26F', '%.0f' % C[2026]['prov'], 'VNDbn', 'DERIVED',
     'chung 687 + cụ thể 10,027 + VAMC 377',
     '-2.6% CK so với 11,384 của FY25; gần như không đổi so với 10,889 của bản trước'),
    ('C1', 'Model!X284 dự phòng cụ thể đầu kỳ', '4,891 -> 16,078', 'VNDbn', 'CONFLICT',
     'Model!X264 (BCĐKT FY25) = 20,056 nhưng bảng chuyển động X274+X284 chỉ 8,869',
     'Lỗi có sẵn trong model: mọi tỷ lệ bao phủ dự phóng trước đây đều vô nghĩa. Đã sửa để '
     'X274+X284 = 20,056'),
    ('G14', 'Cân đối kế toán lệch sau khi sửa X284', '-6,755', 'VNDbn', 'GAP',
     'Model!Y103 = Y61 - Y102; dự phòng tăng làm cho vay thuần giảm 6,146, VCSH tăng 609',
     'CHƯA XỬ LÝ — cần chốt khoản mục bù (huy động hoặc tiền gửi liên ngân hàng) trước khi '
     'phát hành. Tổng tài sản trên slide = số đã công bố trừ 6,146'),
    ('G15', 'Giá mục tiêu vs sheet Valuation', '77,800 vs 61,400', 'VND', 'CONFLICT',
     'Valuation!B1 = J16 = P/B hợp lý FY27F x BPS FY27F',
     'Sheet Valuation cho 56,100 trước điều chỉnh và ~61,400 sau (ROE bền vững FY27F lên '
     '14.8%, BPS 37,570). Slide vẫn để 77,800 — CHƯA ĐỊNH GIÁ LẠI, cần CV quyết'),
    ('G16', 'Giá mục tiêu ghi 77,500 trong file stock pick', '77,500 vs 77,800', 'VND', 'CONFLICT',
     'Stock Pick!D6 và Target Price!C13 ghi 77,500; cột J6/L6 lại tính trên 77,800',
     'CHƯA SỬA — chênh 0.4%, cần CV xác nhận số nào đúng'),
    ('G17', 'Tăng trưởng tín dụng FY26F 11.7% vs 1.5% thực hiện 1H26', '', '', 'GAP',
     'Model!Y206 = 10.1%; slide ghi 11.7%',
     'CHƯA XỬ LÝ — hạ giả định này sẽ kéo NII, TOI và cả mẫu số của NPL/CIR'),
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
