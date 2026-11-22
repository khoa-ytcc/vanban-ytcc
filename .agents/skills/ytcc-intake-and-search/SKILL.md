---
name: ytcc-intake-and-search
description: Tiếp nhận văn bản đến hoặc yêu cầu soạn thảo mới và tra cứu tiền lệ văn bản Khoa YTCC qua SQLite FTS5 và kho PDF S0.
---

# SKILL: Tiếp nhận Yêu cầu & Tra cứu Tiền lệ (ytcc-intake-and-search)

Skill này giúp Agent tiếp nhận thông tin đầu vào (văn bản đến, tin nhắn yêu cầu của lãnh đạo hoặc chuyên viên), phân tích cấu trúc sự việc và tự động tra cứu tiền lệ tương đồng trong lịch sử văn bản Khoa YTCC.

---

## 1. Đầu vào (Inputs)
- File văn bản đến (PDF, ảnh scan, Word) hoặc nội dung chỉ đạo từ người dùng.
- Thể loại dự kiến (Công văn, Tờ trình, Kế hoạch, Báo cáo, Giấy giới thiệu).

---

## 2. Quy trình Thực hiện (Steps)

### Bước 1: Tiếp nhận & Bóc tách thực thể (Intake)
Trích xuất đầy đủ 5 thông tin cốt lõi:
1. **Đơn vị phát hành văn bản đến:** Tên chính xác của cơ quan gửi (Ví dụ: Cty TNHH Truyền hình Kết Nối, Bệnh viện ĐK Khu vực Thủ Đức...).
2. **Số hiệu & Ngày văn bản đến:** Để đưa vào câu căn cứ phúc đáp (Ví dụ: *Căn cứ Công văn số 10-11/CV2026 ngày 10/11/2026 của...*).
3. **Nội dung yêu cầu / Sự việc:** Tóm tắt nhiệm vụ (cử cán bộ tham gia hội đồng, xin kinh phí bảo trì, tổ chức thực tế cộng đồng...).
4. **Nhân sự liên quan:** Họ tên, học hàm học vị, chức danh, bộ môn phụ trách nếu có.
5. **Hạn xử lý (Deadline):** Ngày cần hoàn tất văn bản phúc đáp hoặc trình duyệt.

### Bước 2: Tra cứu Tiền lệ Lịch sử (Search History)
Chạy script tìm kiếm FTS5 SQLite với 2–3 biến thể từ khóa tiếng Việt (có dấu hoặc không dấu):
```powershell
d:\TH\vanban-ytcc\.venv\Scripts\python.exe d:\TH\vanban-ytcc\tools\search_history.py --q "<từ_khóa_1>" --type all --limit 5
d:\TH\vanban-ytcc\.venv\Scripts\python.exe d:\TH\vanban-ytcc\tools\search_history.py --q "<từ_khóa_2>" --type di --limit 5
```
- **Tiêu chí chọn lọc tiền lệ:**
  - Ưu tiên các bản ghi có đường dẫn file PDF thực tế (`pdf_path` khác rỗng).
  - Chọn 1–2 văn bản có nội dung và thẩm quyền xử lý tương tự nhất.

### Bước 3: Rút trích Văn phong & Căn cứ từ S0 (Inspect Reference)
- Sử dụng subagent READ-ONLY hoặc Python PyMuPDF để đọc nhanh nội dung hoặc trích xuất text của PDF tiền lệ:
  - Học cấu trúc câu văn mở đầu và kết luận đặc thù Khoa YTCC.
  - Lấy mẫu các căn cứ pháp lý thường dùng.
  - Kiểm tra danh sách `Kính gửi:` và `Nơi nhận:` thực tế (không tin cậy cột `noi_nhan` trong DB lịch sử).

---

## 3. Đầu ra (Outputs)
Một bảng tóm tắt nghiệp vụ gồm:
1. **Thông tin bóc tách văn bản đến / yêu cầu mới.**
2. **Tiền lệ sát nhất:** Số hiệu, trích yếu, trích đoạn văn phong phù hợp.
3. **Đề xuất loại văn bản và hướng soạn thảo** cho Skill tiếp theo (`ytcc-draft-and-build`).
