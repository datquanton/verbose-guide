# -*- coding: utf-8 -*-
"""Append the FY27F/FY28F provisioning overlay to the internal audit trail."""
import openpyxl
from openpyxl.styles import Font
import update_stb_loans as U

WB = '/home/user/verbose-guide/INTERNAL_Sources_and_Assumptions_Aug26.xlsx'

LOANS = (640643.1, 719776.9, 825564.9)          # Model!Y/Z/AA204
NPLR = (0.058, 0.040, 0.027)                    # NPL!N/O/P 28+29+30
RESERVE = (18925.5, 20524.5, 23305.4)           # Model!Y/Z/AA286 after the overlay
COV = tuple(r / (n * l) * 100 for r, n, l in zip(RESERVE, NPLR, LOANS))

ROWS = [
    ('', 'STB — REVISION 05/08/2026 b (dự phòng FY27F +1,000, FY28F +2,000)', '', '', '', '', ''),
    ('A8', 'Trích thêm dự phòng FY27F và FY28F', '1,000 / 2,000', 'VNDbn', 'MAS',
     'Model!Z278 = -Z279+1000, AA278 = -AA279+2000 (trước đó = -Z279*1, -AA279*1)',
     'Viết dạng cộng thẳng thay vì hệ số nhân để phần trích thêm hiện rõ trong ô. '
     'Tỷ lệ xóa nợ -1.2%/-0.7% giữ nguyên nên phần trích thêm không dùng để xóa nợ '
     'mà bồi đắp bộ đệm: dự phòng đã trích tăng 1,000 tỷ năm FY27F và 3,000 tỷ lũy kế FY28F. '
     'Đợt 2,000 tỷ ở FY28F là yêu cầu hạ LNTT FY28F thêm 1,000 tỷ — dùng cùng một đòn bẩy '
     'để CIR 38% và các dòng thu nhập giữ nguyên'),
    ('A9', 'Chi phí dự phòng FY26F / FY27F / FY28F',
     '%.0f / %.0f / %.0f' % U.PROV, 'VNDbn', 'MODEL', 'Model!Y/Z/AA141',
     'FY27F từ 9,636 lên 10,636; FY28F từ 6,982 lên 8,982'),
    ('A10', 'LNTT FY27F / FY28F', '%.0f / %.0f' % U.PBT[1:], 'VNDbn', 'MODEL',
     'Model!Z144 / AA144',
     'FY27F từ 10,872 xuống %.0f (+%.1f%% CK, trước là +45.7%%); FY28F từ 17,271 xuống '
     '%.0f (+%.1f%% CK, trước là +58.9%%) — sát mục tiêu 50%% CV đặt ở vòng trước'
     % (U.PBT[1], U.PBT[1] / U.PBT[0] * 100 - 100,
        U.PBT[2], U.PBT[2] / U.PBT[1] * 100 - 100)),
    ('A11', 'LNST / ROE FY27F / FY28F',
     '%.0f / %.0f' % U.NPATMI[1:], 'VNDbn', 'MODEL', 'Model!Z153, AA153, Z314, AA314',
     'ROE FY27F %.1f%% (từ 12.1%%), FY28F %.1f%% (từ 16.6%%). Vốn chủ cuối FY28F '
     '%.0f tỷ, thấp hơn 2,336 tỷ so với bản trước do lợi nhuận giữ lại giảm'
     % (U.ROE[1], U.ROE[2], U.EQUITY[2])),
    ('A12', 'P/E, P/B FY27F / FY28F trên giá mục tiêu 75,000',
     '%.1f / %.1f x' % (U.TP / U.EPS[1], U.TP / U.EPS[2]), 'x', 'DERIVED',
     'EPS FY27F %.0f, FY28F %.0f trên %.0f triệu cổ phiếu'
     % (U.EPS[1], U.EPS[2], U.SHARES),
     'P/E FY27F từ 18.3 lên %.1f, FY28F từ 11.5 lên %.1f'
     % (U.TP / U.EPS[1], U.TP / U.EPS[2])),
    ('G21', 'Đỉnh dự phòng dời từ FY26F sang FY27F', '', '', 'GAP',
     'Dự phòng %.0f / %.0f / %.0f trong khi xóa nợ 10,955 / 8,637 / 5,779' % U.PROV,
     'Phần trích thêm đẩy chi phí FY27F vượt FY26F dù xóa nợ giảm 21%. Đây là hệ quả '
     'trực tiếp của yêu cầu, không phải lỗi, nhưng làm chậm câu chuyện hồi phục một năm'),
    ('G22', 'Bao phủ nợ xấu FY28F chạm ~100%',
     '%.0f / %.0f / %.0f%%' % COV, '%', 'GAP',
     'Dự phòng đã trích %.0f / %.0f / %.0f trên nợ xấu %.0f / %.0f / %.0f'
     % (RESERVE + tuple(n * l for n, l in zip(NPLR, LOANS))),
     'Trước khi trích thêm là 50.9 / 67.8 / 91.1%. Bao phủ trên 100% ở một ngân hàng '
     'vừa xử lý xong tồn đọng là mức của nhóm đầu ngành — CV cân nhắc có muốn giữ hay '
     'chuyển phần hạ LNTT FY28F sang dòng thu nhập (xem G23)'),
    ('G23', 'Đòn bẩy thay thế: hệ số 1.7x ở thu nhập khác FY28F', '', '', 'GAP',
     'Model!AA129 = Z129/Z130*AA130*1.7 — thu hồi nợ đã xóa tăng 34% trong khi xóa nợ '
     'giảm 33% (8,637 -> 5,779)',
     'CHƯA SỬA. Bỏ hệ số 1.7 sẽ hạ thu nhập khác FY28F 1,123 tỷ, tức cũng đạt mục tiêu '
     'hạ LNTT, nhưng kéo CIR FY28F từ 38.0% lên 39.1% nên phải giải lại hệ số chi phí'),
    ('A13', 'Slide dựng thẳng từ file model, không gõ tay', '', '', 'MODEL',
     'model_read.py đọc FinModel_STB_2Q26.xlsx, tính lại các công thức dự án này đặt',
     'Trước đây các hằng số trên slide được chép tay từ workbook, mỗi vòng sửa là một '
     'lần chép lại. Nay update_stb_loans đọc thẳng. Cột FY26F đã được Excel tính lại '
     'nên dùng làm đối chứng: 9 dòng (chi phí HĐ, TOI, dự phòng, LNTT, LNST, vốn chủ, '
     'tổng tài sản, dự phòng đã trích, dư nợ) khớp tuyệt đối với cache của Excel'),
    ('A14', 'Sửa SLCP lưu hành và vốn hóa ở ô thông tin', '2,060 / 152,658',
     'triệu cp / tỷ đồng', 'MODEL',
     "Vốn điều lệ 20,601.582 tỷ ('Balance sheet'!Y79) / mệnh giá 10,000 đồng; giá 74,100",
     'Ô thông tin ghi 1,885 triệu cp và vốn hóa 139,694 tỷ trong khi toàn bộ EPS, BVPS, '
     'P/E, P/B của bảng FY tính trên 2,060.158 triệu cp — chênh 9.3%. P/E 26F nếu tính '
     'trên 1,885 triệu cp sẽ là 24.3 chứ không phải 26.6. ĐÃ SỬA ô thông tin theo model'),
    ('G15', 'Giá mục tiêu STB vs sheet Valuation', '75,000 vs ~46,500', 'VND', 'CONFLICT',
     'Valuation: P/B hợp lý (ROE 12.1% - 2.5%) / (10.01% - 2.5%) = 1.29x x BPS 36,014',
     'ROE FY27F nay chỉ còn %.1f%% nên P/B hợp lý tính lại còn thấp hơn nữa. '
     'CHƯA ĐỊNH GIÁ LẠI' % U.ROE[1]),
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
    print('coverage %.1f / %.1f / %.1f%%' % COV)


if __name__ == '__main__':
    main()
