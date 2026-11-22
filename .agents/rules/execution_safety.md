# QUY CHUẨN AN TOÀN HỆ THỐNG & ĐIỀU KHIỂN TIẾN TRÌNH (KHOA YTCC)

---

## 1. Thứ bậc Nguồn Dữ liệu (S0 > S1 > S2)
- **S0 (Nguồn Chân lý Gốc):** Toàn bộ các file PDF thực tế được lưu tại `knowledge_base/sample_pdfs/` và bản chụp/scan văn bản thực tế. Đây là căn cứ tối thượng để xác định thể thức, vạch kẻ, tọa độ và bố cục trang.
- **S1 (Nguồn Dẫn xuất Tra cứu):** CSDL SQLite `ytcc_history.db` và các tệp JSON lịch sử (`cv_di_history.json`, `cv_den_history.json`). Chỉ dùng cho mục đích tra cứu nhanh từ khóa, trích yếu, số hiệu và tìm PDF liên quan.
- **S2 (Tạo phẩm Phái sinh):** Toàn bộ file JSON kịch bản, file DOCX, PDF do AI tạo ra. Bắt buộc phải đối chiếu và kiểm chứng với chuẩn S0 trước khi nghiệm thu bàn giao.

---

## 2. Quy trình 4 Bước Bắt buộc Trước khi Bàn giao Văn bản
Mọi văn bản trước khi bàn giao cho người dùng hoặc chuyển Reviewer nghiệm thu bắt buộc phải trải qua đủ 4 bước tuần tự khép kín:
```mermaid
flowchart LR
    A["1. Soạn JSON"] --> B["2. build_doc.py + export_pdf.ps1"]
    B --> C["3. inspect_pdf.py (Auto QA)"]
    C --> D["4. Mở PNG soi trực quan 100% trang"]
    D --> E["Bàn giao Dự thảo"]
```
1. **Bước 1 — Soạn JSON:** Lắp ráp file dữ liệu JSON chuẩn theo `knowledge_base/specs/doc_schema.md`.
2. **Bước 2 — Sinh DOCX & PDF:** Gọi `tools/build_doc.py --input <file.json> --output <file.docx> --pdf` để chuyển đổi tự động qua Word COM.
3. **Bước 3 — Kiểm định Tự động:** Chạy `tools/inspect_pdf.py <file.pdf>` để rà soát:
   - Kích thước trang chuẩn A4 (210 × 297 mm hoặc 297 × 210 mm).
   - Không bị rớt chữ `NAM` trên dòng Quốc hiệu.
   - Không lặp từ `V/v` trong trích yếu.
   - Trang 1 không có số trang; trang 2+ có số trang hợp lệ.
   - Không sót placeholder dạng `{{...}}` hoặc giá trị `None` / `undefined`.
   - Trang cuối không bị nguy cơ mồ côi khối chữ ký.
4. **Bước 4 — Thẩm định Thị giác 100%:** Agent bắt buộc phải **mở trực tiếp toàn bộ ảnh PNG** được render ra để kiểm tra bằng mắt thường (độ liền nét vạch kẻ, cân đối lề trang, tiêu đề bảng, ô phê duyệt BGH). Nếu phát hiện lỗi thẩm mỹ, phải quay lại sửa JSON hoặc engine cho đến khi đạt độ hoàn thiện cao nhất.

---

## 3. Ràng buộc Kỹ thuật Windows & An toàn Word COM
- **Định dạng file mã nguồn PowerShell:** Mọi file `.ps1` có chứa tiếng Việt bắt buộc phải được lưu ở định dạng **UTF-8 with BOM** để PowerShell 5.1 xử lý đúng chuỗi Unicode tiếng Việt.
- **Tuyệt đối không dùng lệnh kill tiến trình hàng loạt:**
  - **CẤM:** Không được chạy `Stop-Process -Name WINWORD` hoặc `taskkill /F /IM WINWORD.EXE`. Lệnh này sẽ làm tắt đột ngột các tài liệu Word cá nhân mà người dùng đang mở trên máy tính.
  - **ĐÚNG:** Mọi thao tác xuất Word COM phải gói trong khối `try { ... } finally { $doc.Close(0); $word.Quit(); [Marshal]::ReleaseComObject(...) }` như đã thiết kế trong `tools/export_pdf.ps1`.
- **Không chạy song song nhiều tiến trình Word COM:**
  - Các tác vụ xuất PDF phải được Main Worker thực thi tuần tự, từng file một. Tuyệt đối không spawn subagent để xuất Word COM đồng thời.
- **Bảo mật thông tin:**
  - Tuyệt đối không ghi thông tin tài khoản, mật khẩu CSDL MySQL, IP mạng nội bộ hay khóa giải mã vào bất kỳ file mã nguồn, file cấu hình hay báo cáo markdown nào.
