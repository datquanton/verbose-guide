# -*- coding: utf-8 -*-
"""Append the 8% FY26F loan-growth revision to the internal audit trail."""
import openpyxl
from openpyxl.styles import Font
import update_stb_loans as U
from valuation import V

WB = '/home/user/verbose-guide/INTERNAL_Sources_and_Assumptions_Aug26.xlsx'
F = U.F

ROWS = [
    ('', 'STB — REVISION 06/08/2026 c (tăng trưởng tín dụng FY26F 8%)', '', '', '', '', ''),
    ('A24', 'Tăng trưởng tín dụng FY26F', '%.1f%%' % U.LOAN_GROWTH, '%', 'MAS',
     'Model!Y515:Y520 = X5xx*$X$450/$X$521*1.08; dư nợ %.0f tỷ' % U.LOANS26,
     'Từ 2.3%%. 1H26 thực hiện 1.5%% nên 2H26 phải tăng %.1f%% — giả định STB dùng tới '
     'phần room tín dụng chưa dùng. FY27F %.0f, FY28F %.0f tỷ đồng (giữ nguyên tốc độ '
     'tăng theo phân khúc, dòng 533-538)' % (U.H2_LOANS, F['loans'][1], F['loans'][2])),
    ('A25', 'Sửa nền dư nợ FY25 của khối phân khúc', '593,591 -> 626,392', 'VNDbn', 'MODEL',
     'Model!X521 (cộng dồn dòng 515:520) so với X450 = Note!T79 (số báo cáo)',
     'Khối 515:520 được đẩy từ FY24 sang bằng tốc độ tăng chứ không lấy số thực, nên đã '
     'lệch 5.2% dưới dư nợ báo cáo. Đây chính là lý do tốc độ tăng 7.9% ghi trong model '
     'lâu nay chỉ ra 2.3% trên nền báo cáo. Nay rebase trước khi tăng, nên hệ số 1.08 '
     'trong công thức đúng bằng con số hiển thị trên slide'),
    ('A26', 'Dòng 23-28 chuyển từ số cứng sang công thức', '', '', 'MODEL',
     'Model!Y/Z/AA23:28 = Y/Z/AA515:520',
     'Trước đây là số dán tay. Nếu không sửa thì dòng 20 (dư nợ trên bảng CĐKT) không đi '
     'theo dòng 521 và ô kiểm tra 205 sẽ lệch'),
    ('A27', 'NII / TOI / LNTT FY26F', '%.0f / %.0f / %.0f' % (U.NII[0], U.TOI[0], U.PBT[0]),
     'VNDbn', 'MODEL', 'Model!Y121 / Y117 / Y144',
     'NII từ 24,531 lên %.0f (+1,554). LNTT từ 7,461 lên %.0f (%+.1f%% CK, '
     'thấp hơn kế hoạch %.1f%%). LNTT FY27F %.0f (+%.0f%%), FY28F %.0f (+%.0f%%) — cả hai '
     'năm quanh 51%%, sát mục tiêu 50%% CV đặt'
     % (U.NII[0], U.PBT[0], U.PBT_YOY, -U.VS_PLAN, U.PBT[1],
        U.PBT[1] / U.PBT[0] * 100 - 100, U.PBT[2], U.PBT[2] / U.PBT[1] * 100 - 100)),
    ('A28', 'Giữ lộ trình CIR, giải lại hệ số chi phí',
     '%.1f / %.1f / %.1f%%' % U.CIR, '%', 'MAS',
     'Model!Y/Z/AA132,134 = 1.0296 / 1.0923 / 1.0773 (trước là 0.9647 / 1.0279 / 1.0829)',
     'TOI tăng nên nếu giữ nguyên chi phí thì CIR tự rơi về 40.0 / 36.3 / 34.6%% — thay '
     'đổi âm thầm còn lớn hơn. Giữ lộ trình 42.1/40/38%% CV đã đặt: chi phí FY26F lên '
     '%.0f tỷ, tức 2H26 %.0f tỷ so với 6,233 tỷ của 1H26 (%+.1f%%)'
     % (U.OPEX[0], U.OPEX[0] - U.H1_OPEX,
        (U.OPEX[0] - U.H1_OPEX) / U.H1_OPEX * 100 - 100)),
    ('A29', 'Beta định giá 1.02 -> %.3f' % V['beta'], '%.3f' % V['beta'], '', 'MAS',
     'Valuation!B11; chi phí vốn CSH %.3f%%; D74 vẫn %.0f'
     % (V['coe'] * 100, V['fair_value']),
     'Trên nền dư nợ 8%%, để beta 1.02 thì mô hình ra 86,900 — cao hơn giá mục tiêu. '
     'Beta phải nâng lên %.3f mới về đúng 75,000. Vẫn là số giải ngược, nhưng beta 1.22 '
     'cho một ngân hàng đang tái cơ cấu dễ bảo vệ hơn 1.02. Nói cách khác giá mục tiêu '
     '75,000 nay là mức thận trọng so với chính mô hình' % V['beta']),
    ('G26', 'Tăng trưởng tín dụng không tốn chi phí vốn trong model', '', '', 'GAP',
     'Model!Y55 (tài sản khác) = Y102 trừ các khoản mục còn lại — đây là ô cân đối',
     'Dư nợ tăng được tài trợ bằng cách rút tài sản khác không sinh lãi, không phải bằng '
     'huy động: tiền gửi (dòng 647) chạy theo tốc độ riêng nên chi phí lãi không đổi. '
     'Thu nhập lãi tăng 1,554 tỷ FY26F mà không có phần bù. Thực tế phải huy động với '
     'chi phí ~4.4%%, nên phần tăng NII này là mức trần chứ không phải kỳ vọng'),
    ('G27', 'Bao phủ nợ xấu FY26F giảm về %.1f%%' % U.COV26,
     '%.1f%%' % U.COV26, '%', 'GAP',
     'Dự phòng %.0f trên nợ xấu %.0f (5.8%% của %.0f)'
     % (U.RESERVE26, U.NPL26, U.LOANS26),
     'Từ 50.9%% xuống %.1f%%: nợ xấu 5.8%% tính trên mẫu số lớn hơn trong khi dự phòng '
     'chỉ trích đủ bù xóa nợ. Nếu CV muốn giữ 50%% thì phải nâng tỷ lệ trích Model!Y278 '
     'và LNTT FY26F sẽ giảm tương ứng' % U.COV26),
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
