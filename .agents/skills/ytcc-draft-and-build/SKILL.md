---
name: ytcc-draft-and-build
description: Lắp ráp cấu trúc JSON theo doc_schema.md, soạn thảo nội dung hành chính chuẩn Khoa YTCC và tự động sinh file DOCX/PDF qua Word COM.
---

# SKILL: Soạn thảo Dữ liệu & Sinh Văn bản (ytcc-draft-and-build)

Skill này chuyển đổi các thông tin nghiệp vụ và văn phong tiền lệ thành file dữ liệu JSON chuẩn, sau đó gọi Engine `build_doc.py` để tạo tài liệu Word và xuất bản PDF cố định.

---

## 1. Đầu vào (Inputs)
- Dữ liệu bóc tách từ yêu cầu mới hoặc văn bản đến (kết quả từ `ytcc-intake-and-search`).
- Mẫu câu, lập luận học từ văn bản tiền lệ.
- Thư mục lưu trữ: `drafts/YYYY-MM/` (Ví dụ: `drafts/2026-11/`).

---

## 2. Quy trình Thực hiện (Steps)

### Bước 1: Xác định Loại Văn bản & Thiết lập Khung
Chọn 1 trong các loại văn bản chính:
- `cong_van`: Trích yếu đặt ở góc trái dưới số hiệu. Phù hợp trao đổi công tác với cơ quan bên ngoài hoặc thông báo nội bộ.
- `to_trinh`: Tiêu đề lớn in hoa `TỜ TRÌNH`, trích yếu có đường kẻ ngang bên dưới. Bật `"has_bgh_approval": true` nếu trình cấp Ban Giám hiệu.
- `giay_gioi_thieu`: Header tự động đổi thành cấp Trường (`header_level: "ump"`), chức danh ký `TL. HIỆU TRƯỞNG\nTRƯỞNG KHOA`.
- `ke_hoach`: Kế hoạch hoạt động có tiến độ, phân công nhiệm vụ.
- `bao_cao`: Báo cáo đánh giá, tổng kết.
- `chung`: Định dạng chung khác.

Nếu văn bản ngắn dự kiến chỉ trong 1 trang, bắt buộc bật `"target_one_page": true`.

### Bước 2: Soạn thảo Nội dung & Xử lý Placeholder
1. **Kết hợp linh hoạt:** Đưa các thông tin mới của sự việc vào cấu trúc lập luận chuẩn mực của Khoa YTCC.
2. **Quy tắc Placeholder cho thông tin chưa rõ:**
   - Số hiệu văn bản đi: để `"...."` (Ví dụ: `Số: ..../YTCC-HCTC`).
   - Ngày tháng ký: để `"...."` nếu chưa rõ ngày phát hành chính thức.
   - Họ tên người ký: nếu người dùng chưa chỉ định rõ đích danh người ký hiện thời, bắt buộc ghi `"[HỌ TÊN NGƯỜI KÝ]"`.
   - Chức danh ký: nếu chưa rõ ai ký thay, dùng `"[CHỨC VỤ NGƯỜI KÝ]"` hoặc `TRƯỞNG KHOA`.
   - Chuyên viên soạn thảo: để `[TÊN_VIẾT_TẮT]` trong dòng lưu trữ nếu chưa rõ.
3. **Lưu file JSON:** Lưu tại `drafts/YYYY-MM/<Ten_file_gon>.json` với mã hóa UTF-8.

### Bước 3: Biên dịch sang DOCX và Xuất PDF qua Word COM
Chạy lệnh bằng môi trường ảo Python:
```powershell
d:\TH\vanban-ytcc\.venv\Scripts\python.exe d:\TH\vanban-ytcc\tools\build_doc.py --input "drafts/2026-11/<Ten_file>.json" --output "drafts/2026-11/<Ten_file>.docx" --pdf
```
- Lệnh trên sẽ tự động gọi `tools/export_pdf.ps1` để kích hoạt Word COM xuất file PDF cùng tên trong cùng thư mục.
- Kiểm tra kết quả trả về `exit code 0` và xác nhận file `.docx` và `.pdf` đã xuất hiện trên đĩa.

---

## 3. Đầu ra (Outputs)
1. File dữ liệu JSON: `drafts/YYYY-MM/<Ten_file>.json`
2. File Word có thể chỉnh sửa: `drafts/YYYY-MM/<Ten_file>.docx`
3. File PDF xuất bản: `drafts/YYYY-MM/<Ten_file>.pdf`
4. **Bảng liệt kê "Các mục cần chuyên viên bổ sung/xác nhận":** Liệt kê chi tiết các vị trí placeholder vừa dùng để người dùng dễ dàng hoàn thiện trước khi trình ký.
