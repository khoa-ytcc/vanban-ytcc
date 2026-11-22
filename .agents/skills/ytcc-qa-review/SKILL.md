---
name: ytcc-qa-review
description: Kiểm định tự động chất lượng thể thức văn bản PDF bằng inspect_pdf.py (kèm telemetry lố trang v2.5) và thẩm định trực quan bằng mắt thường qua 100% ảnh PNG trước khi bàn giao.
---

# SKILL: Kiểm định Chất lượng & Thẩm định Thị giác (ytcc-qa-review v2.5)

Skill này đóng vai trò là "Cổng gác chất lượng" cuối cùng trước khi bất kỳ dự thảo văn bản nào được gửi đến người dùng hoặc trình lãnh đạo.

---

## 1. Đầu vào (Inputs)
- File PDF vừa sinh ra: `drafts/YYYY-MM/<YYYYMMDD_case>/v1.pdf`.
- Thư mục lưu ảnh render tạm: `drafts/YYYY-MM/<YYYYMMDD_case>/renders/` (đã được cấu hình trong `.gitignore`).

---

## 2. Quy trình Thực hiện (Steps)

### Bước 1: Kiểm tra Thể thức Tự động & Telemetry Lố trang
Chạy lệnh kiểm định chuyên sâu bằng PyMuPDF:
```powershell
d:\TH\vanban-ytcc\.venv\Scripts\python.exe d:\TH\vanban-ytcc\tools\inspect_pdf.py "drafts/YYYY-MM/<YYYYMMDD_case>/v1.pdf" --render-dir "drafts/YYYY-MM/<YYYYMMDD_case>/renders" --target-one-page
```
*(Lưu ý: Lệnh `ytcc.py build --pdf` đã tự động tích hợp bước này).*

Script tự động kiểm tra 7 tiêu chí kỹ thuật:
1. **Telemetry Lố trang (v2.5):** Khi văn bản bật `target_one_page`, nếu bị tràn sang trang 2, script lập tức báo lỗi `OVERFLOW_PAGE_2` kèm chi tiết số dòng, số ký tự và % chiều cao trang 2 bị chiếm dụng -> **Bắt buộc quay lại sửa rút gọn nội dung hoặc chỉnh lề để thu về 1 trang.**
2. **Kích thước trang:** Chuẩn A4 (210 × 297 mm cho Portrait hoặc 297 × 210 mm cho Landscape).
3. **Quốc hiệu:** `CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM` nằm trọn vẹn trên 1 dòng duy nhất, không bị rớt chữ `NAM`.
4. **Trích yếu:** Không xuất hiện lỗi lặp `V/v V/v` hoặc `V/v Về việc`.
5. **Đánh số trang:** Trang 1 không có số trang; các trang từ trang 2 trở đi có số trang nằm chính giữa lề trên.
6. **Dữ liệu rác & Biến mẫu:** Không còn sót biến chưa giải quyết dạng `{{...}}`, không chứa các từ khóa lỗi như `None`, `undefined`.
7. **Chống mồ côi chữ ký:** Trang cuối của văn bản nhiều trang phải có đủ nội dung dẫn nhập kèm khối chữ ký (vượt ngưỡng an toàn ký tự).

### Bước 2: Thẩm định Thị giác Trực quan (Visual Inspection)
Agent **bắt buộc** phải dùng công cụ `read_file` để **mở và nhìn trực tiếp 100% số ảnh PNG** trong thư mục `renders/`. Rà soát bằng mắt thường các điểm sau:
- **Vạch kẻ:** Vạch kẻ dưới Quốc hiệu / Tiêu ngữ có liền nét và phủ trọn dòng chữ không? Vạch kẻ dưới tên Khoa có đặt cân đối ở tỷ lệ 1/2 không?
- **Căn lề Header:** Cột đơn vị ban hành và cột Quốc hiệu có thẳng hàng, cân xứng không?
- **Bảng biểu:** Dòng tiêu đề có nền trắng sạch sẽ theo NĐ 30 không? Bảng có bị tràn lề phải không? Nếu bảng kéo dài qua trang, dòng tiêu đề có lặp lại ở đầu trang tiếp theo không?
- **Khối chữ ký:** Nơi nhận và chữ ký Trưởng khoa có cân đối không? Nếu có ô `DUYỆT BAN GIÁM HIỆU`, ô này có nằm ngay ngắn ở chính giữa toàn trang ở dưới cùng không?
- **Định dạng Inline:** Các từ khóa in đậm, in nghiêng, đậm nghiêng có hiển thị sạch sẽ, không còn sót ký tự `*` nào không?

### Bước 3: Đóng phiên & Xác nhận An toàn
- Xác nhận không có tiến trình `WINWORD.EXE` bị treo ngầm (`Get-Process -Name WINWORD` trả về 0).
- Các ảnh PNG render tạm được bảo vệ trong `.gitignore`, không đưa vào git tracking.

---

## 3. Đầu ra (Outputs)
1. **Báo cáo kiểm định tự động:** Trạng thái PASS/FAIL chi tiết của từng tiêu chí.
2. **Biên bản thẩm định thị giác:** Nhận xét bằng mắt thường về độ cân đối, thẩm mỹ của văn bản.
3. **Đánh giá sẵn sàng (Ready for Signoff):** Khẳng định tài liệu đủ điều kiện bàn giao cho chuyên viên/người dùng.
