#!/usr/bin/env python3
"""Swap the TCB HotStock script text for the MBB version, keeping every style intact."""
import io, os, re, shutil, sys, zipfile

SRC_DIR = "tcb_docx"
OUT = "HotStock_MBB_2026.docx"

REPLACEMENTS = [
    # 1. hook
    ("TCB đang rẻ vì rủi ro, hay vì thị trường đang bỏ lỡ cơ hội? ",
     "MBB đang được định giá đúng, hay thị trường vẫn chưa trả đủ cho ngân hàng có chi phí vốn rẻ nhất hệ thống? "),
    # 2. intro
    ("Với nền tảng vốn vững mạnh và nhiều động lực hồi phục ở phía trước, chúng tôi cho rằng TCB là một cổ phiếu rất đáng để theo dõi. Dưới đây là ba lý do chính. ",
     "Với tỷ lệ CASA dẫn đầu toàn ngành, hạn mức tăng trưởng tín dụng thuộc nhóm cao nhất thị trường và một lộ trình tăng vốn rõ ràng, chúng tôi cho rằng MBB là một cổ phiếu rất đáng để theo dõi. Dưới đây là ba lý do chính. "),
    # 3. heading 1
    ("Thứ nhất, định giá đang hấp dẫn trên một nền tảng vốn vững chắc.",
     "Thứ nhất, định giá vẫn hợp lý so với khả năng sinh lời thuộc nhóm dẫn đầu."),
    # 4-6. pillar 1 bullets
    ("TCB hiện giao dịch ở mức P/B forward khoảng 1,23 lần, thấp hơn ~8% so với trung bình 5 năm – thị trường vẫn đang chiết khấu rủi ro liên quan đến ngành bất động sản.",
     "MBB hiện giao dịch quanh mức P/B khoảng 1,4 lần, nhưng tính trên giá trị sổ sách dự phóng năm 2026 thì P/B chỉ còn khoảng 1,2 lần – một mức hợp lý với ngân hàng đạt ROE 21,1% trong năm 2025."),
    ("Tuy nhiên, xét về sức khỏe tài chính, TCB trong nhiều năm nay nằm trong top đầu về tỷ lệ an toàn vốn với hệ số CAR 15,2%. ",
     "Đây là mức sinh lời thuộc nhóm cao nhất trong các ngân hàng quy mô lớn. Các nhóm phân tích trên thị trường hiện đưa ra giá mục tiêu cho MBB trong vùng 32.900 – 37.230 đồng mỗi cổ phiếu. "),
    ("Sắp tới đây, TCB sẽ tiếp tục chia cổ phiếu thưởng tăng vốn điều lệ lên 113.800 tỷ đồng, đây cũng có thể cải thiện tâm lý giao dịch mã cổ phiếu này. ",
     "Sắp tới đây, MBB sẽ tăng vốn điều lệ từ 80.550 tỷ đồng lên tối đa 102.687 tỷ đồng và chi trả cổ tức tỷ lệ 25%, gồm 10% tiền mặt và 15% cổ phiếu, đây cũng có thể cải thiện tâm lý giao dịch mã cổ phiếu này. "),
    # 7. heading 2
    ("Động lực phục hồi từ các mảng kinh doanh cốt lõi",
     "Lợi thế vốn rẻ từ tỷ lệ CASA dẫn đầu toàn hệ thống"),
    # 8-9. pillar 2 bullets
    ("Các lĩnh vực từng chịu áp lực trong giai đoạn 1-2 năm trở lại đây như trái phiếu doanh nghiệp, chứng khoán và bất động sản đang bước vào chu kỳ hồi phục khi thị trường vốn cải thiện. ",
     "Trong bối cảnh biên lãi ròng toàn ngành thu hẹp, MBB vẫn giữ tỷ lệ tiền gửi không kỳ hạn CASA quanh 38% vào cuối năm 2025 – mức cao nhất hệ thống, với số dư CASA tăng khoảng 27% so với cùng kỳ. "),
    ("Với TCBS – công ty chứng khoán của TCB và là đơn vị dẫn đầu mảng tư vấn phát hành trái phiếu doanh nghiệp – việc thị trường trái phiếu khởi động lại giúp công ty hưởng lợi rõ nét. Đồng thời, nâng hạng FTSE có thể kích hoạt dòng vốn vay margin cho TCBS, tạo thêm động lực tăng trưởng thu nhập.",
     "Nguồn vốn giá rẻ này giúp MBB giữ chi phí huy động ở nhóm thấp nhất và bảo vệ biên lãi ròng tốt hơn phần còn lại của ngành. Đồng thời, thu nhập từ phí dịch vụ năm 2025 tăng hơn 50%, giúp cơ cấu thu nhập bớt phụ thuộc vào tín dụng."),
    # 10. heading 3
    ("Triển vọng tăng trưởng từ mở rộng hệ sinh thái và đầu tư công",
     "Triển vọng tăng trưởng từ hạn mức tín dụng đặc biệt và mở rộng quy mô"),
    # 11-12. pillar 3 bullets
    ("Không chỉ BĐS, TCB tiếp tục mở rộng hoạt động vào các dự án hạ tầng quy mô lớn, trong đó có siêu dự án như Cảng hàng không Quốc tế Gia Bình với tổng mức đầu tư hơn 196.000 tỷ đồng. ",
     "Sau khi nhận chuyển giao bắt buộc ngân hàng MBV, MBB được giao hạn mức tăng trưởng tín dụng thuộc nhóm cao nhất thị trường cho giai đoạn 2026 – 2028, với mục tiêu tăng trưởng tín dụng năm nay trong khoảng 30 – 35%. "),
    ("Đồng thời, ngân hàng cũng là một trong những cái tên hưởng lợi từ xu hướng tháo gỡ nút thắt thanh khoản theo định hướng sửa đổi Thông tư 22/2019/TT-NHNN. ",
     "Quy mô cũng đang bứt tốc: tổng tài sản đạt hơn 1,61 triệu tỷ đồng vào cuối năm 2025, tăng 43% chỉ trong một năm, và ngân hàng đặt mục tiêu vượt 2,1 triệu tỷ đồng trong năm 2026, đi cùng nhu cầu vốn lớn từ các dự án hạ tầng và đầu tư công. "),
    # 13. closing
    ("Với nền tảng vốn vững mạnh và dư địa tăng trưởng tín dụng dồi dào, chúng tôi cho rằng mức định giá hiện tại đã phản ánh phần lớn những lo ngại của thị trường. Nếu vĩ mô ổn định và nền kinh tế bước vào chu kỳ hồi phục, TCB được kỳ vọng sẽ là một trong những cổ phiếu có thể bứt phá trong thời gian sắp tới. ",
     "Với chi phí vốn thấp nhất hệ thống, dư địa tăng trưởng tín dụng vượt trội và lộ trình tăng vốn rõ ràng, chúng tôi cho rằng MBB vẫn còn dư địa để mở rộng định giá. Nếu vĩ mô ổn định và tín dụng tiếp tục tăng tốc, MBB được kỳ vọng sẽ là một trong những cổ phiếu ngân hàng dẫn dắt trong thời gian sắp tới. "),
]

path = os.path.join(SRC_DIR, "word", "document.xml")
xml = open(path, encoding="utf-8").read()

for old, new in REPLACEMENTS:
    assert "&" not in new and "<" not in new and ">" not in new, new
    n = xml.count(old)
    if n != 1:
        sys.exit(f"expected 1 occurrence, got {n}: {old[:60]!r}")
    xml = xml.replace(old, new)

assert "TCB" not in xml and "Techcombank" not in xml, "TCB reference survived"
open(path, "w", encoding="utf-8").write(xml)

if os.path.exists(OUT):
    os.remove(OUT)
zf = zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED)
for root, _dirs, files in os.walk(SRC_DIR):
    for f in files:
        full = os.path.join(root, f)
        zf.write(full, os.path.relpath(full, SRC_DIR))
zf.close()
print("wrote", OUT, os.path.getsize(OUT), "bytes")
