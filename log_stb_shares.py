# -*- coding: utf-8 -*-
"""Append the share-count correction to the internal audit trail.

Supersedes row A14 of the previous block, which had it backwards.
"""
import openpyxl
from openpyxl.styles import Font
import update_stb_loans as U

WB = '/home/user/verbose-guide/INTERNAL_Sources_and_Assumptions_Aug26.xlsx'

ROWS = [
    ('', 'STB — REVISION 06/08/2026 (SLCP lưu hành 1,885.216 triệu)', '', '', '', '', ''),
    ('A15', 'SLCP lưu hành', '%.4f' % U.SHARES, 'triệu cp', 'MODEL',
     "'Balance sheet'!Y80 vốn điều lệ 18,852.157 tỷ / mệnh giá 10,000 đồng",
     'SỬA LẠI A14. A14 lấy nhầm Y79 (20,601.582 tỷ) — đó là toàn bộ "Vốn của TCTD", '
     'gồm vốn điều lệ 18,852.157 + thặng dư vốn cổ phần 1,747.651 + vốn khác 1.774. '
     'Chia dòng đó cho mệnh giá là tính thặng dư vốn thành cổ phiếu, thổi SLCP lên 9.3%. '
     'Vốn điều lệ là Y80. CV chỉ ra chỗ này'),
    ('A16', 'EPS và BVPS tính lại toàn bộ 6 cột',
     'EPS %.0f / %.0f / %.0f' % U.EPS, 'VND', 'DERIVED',
     'LNST và vốn chủ chia %.4f triệu cp thay vì 2,060.158' % U.SHARES,
     'Không chỉ dự phóng: cột FY23-FY25 trên slide cũng đang tính theo 2,060.158. '
     'EPS FY25 từ 2,883 lên %.0f, FY24 từ 4,896 lên %.0f, FY23 từ 3,747 lên %.0f. '
     'BVPS FY25 từ 29,059 lên %.0f. Mọi dòng /cp trên bảng FY đều tăng 9.3%%'
     % (U.HIST_EPS[2], U.HIST_EPS[1], U.HIST_EPS[0], U.HIST_BVPS[2])),
    ('A17', 'P/E và P/B tính lại trên giá mục tiêu 75,000',
     'P/E %.1f / %.1f / %.1f' % tuple(U.TP / e for e in U.EPS), 'x', 'DERIVED',
     'Giá mục tiêu 75,000 chia EPS và BVPS mới',
     'P/E 26F từ 26.6 về %.1f, 27F từ 20.1 về %.1f, 28F từ 13.0 về %.1f. '
     'P/B 26F từ 2.4 về %.1f. Định giá rẻ đi 9.3%% trên mọi năm — không phải do dự '
     'phóng thay đổi mà do mẫu số trước đây sai'
     % (U.TP / U.EPS[0], U.TP / U.EPS[1], U.TP / U.EPS[2], U.TP / U.BVPS[0])),
    ('A18', 'Vốn hóa và SLCP ở ô thông tin', '139,694 / 1,885',
     'tỷ đồng / triệu cp', 'DERIVED', 'Giá 74,100 x %.4f triệu cp' % U.SHARES,
     'Trả về đúng giá trị ban đầu của ô. Ô thông tin vốn dĩ đã đúng; bảng FY mới là '
     'chỗ sai, và nay đã khớp'),
    ('G24', 'Ảnh hưởng tới sheet Valuation', '', '', 'GAP',
     'Valuation dùng BPS FY27F 36,014 (theo 2,060.158 triệu cp); nay BPS FY27F là %.0f'
     % U.BVPS[1],
     'CHƯA TÍNH LẠI. Giá hợp lý = P/B hợp lý x BPS, nên BPS tăng 9.3%% thì giá hợp lý '
     'từ ~46,500 lên ~50,800 — khoảng cách với giá mục tiêu 75,000 thu hẹp nhưng vẫn còn'),
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
    print('shares %.4fmn · EPS %.0f / %.0f / %.0f · BVPS %.0f / %.0f / %.0f'
          % ((U.SHARES,) + U.EPS + U.BVPS))


if __name__ == '__main__':
    main()
