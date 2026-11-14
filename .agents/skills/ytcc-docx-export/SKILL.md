---
name: ytcc-docx-export
description: >-
  Tự động sinh file Microsoft Word (.docx) chuẩn thể thức Nghị định 30/2020/NĐ-CP từ bản thảo văn bản
  và xuất trực tiếp sang file PDF chất lượng cao thông qua công cụ tự động hóa Word COM.
---

# KỸ NĂNG XUẤT BẢN FILE WORD (.DOCX) & PDF

Kỹ năng này chịu trách nhiệm chuyển đổi nội dung văn bản mà AI đã soạn thảo thành tập tin thực tế trên máy tính người dùng:

## 1. QUY TRÌNH XUẤT BẢN
1. Nhận dữ liệu văn bản hoàn chỉnh từ AI (Loại văn bản, Số đi, Ngày tháng, Trích yếu, Kính gửi, Nội dung, Nơi nhận, Người ký).
2. Lựa chọn Template Word tương ứng trong thư mục `knowledge_base/templates/` (`Mau_To_trinh.docx`, `Mau_Cong_van.docx`, `Mau_Giay_gioi_thieu.docx`...).
3. Gọi script PowerShell điều khiển Word COM để tạo file Word hoàn chỉnh lưu vào `drafts/YYYY-MM/`.
4. Nếu người dùng yêu cầu xuất PDF, gọi lệnh `export_pdf.ps1` để chuyển đổi file `.docx` sang `.pdf` tức thì.

## 2. CÁC LỆNH TIỆN ÍCH
Người dùng hoặc AI có thể chạy trực tiếp:
- `powershell -File "D:\TH\vanban-ytcc\tools\export_pdf.ps1" -docxPath "<đường_dẫn_file_docx>"`
