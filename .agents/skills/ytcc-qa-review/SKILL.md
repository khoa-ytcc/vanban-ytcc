---
name: ytcc-qa-review
description: Kiểm định tự động chất lượng thể thức văn bản PDF bằng inspect_pdf.py và thẩm định trực quan bằng mắt thường qua ảnh PNG trước khi bàn giao.
---

# SKILL: Kiểm định Chất lượng & Thẩm định Thị giác (ytcc-qa-review)

Skill này đóng vai trò là "Cổng gác chất lượng" cuối cùng trước khi bất kỳ dự thảo văn bản nào được gửi đến người dùng hoặc trình lãnh đạo.

---

## 1. Đầu vào (Inputs)
- File PDF vừa sinh ra: `drafts/YYYY-MM/<Ten_file>.pdf`.
- Thư mục lưu ảnh render tạm: `drafts/YYYY-MM/renders/` (đã được cấu hình trong `.gitignore`).

---

## 2. Quy trình Thực hiện (Steps)

### Bước 1: Kiểm tra Thể thức Tự động bằng Script
Chạy lệnh kiểm định chuyên sâu bằng PyMuPDF:
```powershell
d:\TH\vanban-ytcc\.venv\Scripts\python.exe d:\TH\vanban-ytcc\tools\inspect_pdf.py "drafts/2026-11/<Ten_file>.pdf" --render-dir "drafts/2026-11/renders"
```
Script sẽ tự động kiểm tra 6 tiêu chí kỹ thuật:
1. **Kích thước trang:** Chuẩn A4 (210 × 297 mm cho Portrait hoặc 297 × 210 mm cho Landscape).
2. **Quốc hiệu:** `CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM` nằm trọn vẹn trên 1 dòng duy nhất, không bị rớt chữ `NAM`.
3. **Trích yếu:** Không xuất hiện lỗi lặp `V/v V/v` hoặc `V/v Về việc`.
4. **Đánh số trang:** Trang 1 không có số trang; các trang từ trang 2 trở đi có số trang nằm chính giữa lề trên.
5. **Dữ liệu rác & Biến mẫu:** Không còn sót biến chưa giải quyết dạng `{{...}}`, không chứa các từ khóa lỗi như `None`, `undefined`.
6. **Chống mồ côi chữ ký:** Trang cuối của văn bản nhiều trang phải có đủ nội dung dẫn nhập kèm khối chữ ký (vượt ngưỡng an toàn ký tự).

Nếu script phát hiện lỗi: **Dừng lại, quay lại sửa file JSON và xuất lại PDF.**

### Bước 2: Thẩm định Thị giác Trực quan (Visual Inspection)
Agent bắt buộc phải dùng công cụ `read_file` để **mở và nhìn trực tiếp 100% số ảnh PNG** trong thư mục render tạm. Rà soát bằng mắt thường các điểm sau:
- **Vạch kẻ:** Vạch kẻ dưới Quốc hiệu / Tiêu ngữ có liền nét và phủ trọn dòng chữ không? Vạch kẻ dưới tên Khoa có đặt cân đối ở tỷ lệ 1/2 không?
- **Căn lề Header:** Cột đơn vị ban hành và cột Quốc hiệu có thẳng hàng, cân xứng không?
- **Bảng biểu:** Dòng tiêu đề có nền trắng sạch sẽ theo NĐ 30 không? Bảng có bị tràn lề phải không? Nếu bảng kéo dài qua trang, dòng tiêu đề có lặp lại ở đầu trang tiếp theo không?
- **Khối chữ ký:** Nơi nhận và chữ ký Trưởng khoa có cân đối không? Nếu có ô `DUYỆT BAN GIÁM HIỆU`, ô này có nằm ngay ngắn ở chính giữa toàn trang ở dưới cùng không?

### Bước 3: Đóng phiên & Dọn dẹp
- Xác nhận không có tiến trình `WINWORD.EXE` bị treo bằng lệnh:
  ```powershell
  Get-Process -Name WINWORD -ErrorAction SilentlyContinue | Measure-Object | Select-Object -ExpandProperty Count
  ```
- Đảm bảo các ảnh PNG render tạm nằm gọn trong thư mục đã được `.gitignore` bảo vệ, không gây rác repository.

---

## 3. Đầu ra (Outputs)
1. **Báo cáo kiểm định tự động:** Trạng thái PASS/FAIL chi tiết của từng tiêu chí.
2. **Biên bản thẩm định thị giác:** Nhận xét bằng mắt thường về độ cân đối, thẩm mỹ của văn bản.
3. **Đánh giá sẵn sàng (Ready for Signoff):** Khẳng định tài liệu đủ điều kiện bàn giao cho chuyên viên/người dùng.
