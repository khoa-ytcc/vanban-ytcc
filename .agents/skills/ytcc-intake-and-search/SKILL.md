---
name: ytcc-intake-and-search
description: Tiếp nhận văn bản đến hoặc yêu cầu soạn thảo mới và tra cứu tiền lệ văn bản Khoa YTCC qua SQLite FTS5 (Metadata & Full-text) và kho PDF S0.
---

# SKILL: Tiếp nhận Yêu cầu & Tra cứu Tiền lệ (ytcc-intake-and-search v2.5)

Skill này giúp Agent tiếp nhận thông tin đầu vào (văn bản đến, tin nhắn yêu cầu của lãnh đạo hoặc chuyên viên), tự động tiền xử lý, phân tích cấu trúc sự việc và tra cứu tiền lệ tương đồng trong lịch sử văn bản Khoa YTCC.

---

## 1. Đầu vào (Inputs)
- File văn bản đến (.pdf, .docx, ảnh scan) hoặc nội dung chỉ đạo từ người dùng.
- Thể loại dự kiến (Công văn, Tờ trình, Kế hoạch, Báo cáo, Giấy giới thiệu).

---

## 2. Quy trình Thực hiện (Steps)

### Bước 1: Tiếp nhận & Tiền xử lý (Ingest)
Khi có file văn bản đến từ người dùng, chạy ngay lệnh ingest để tạo thư mục vụ việc chuẩn hóa:
```powershell
d:\TH\vanban-ytcc\.venv\Scripts\python.exe d:\TH\vanban-ytcc\tools\ytcc.py ingest --file "<đường_dẫn_file>" --case "<tên_case_viết_thường>"
```
- Lệnh tự động tạo thư mục: `drafts/YYYY-MM/<YYYYMMDD_case>/incoming/`
- Trích xuất toàn bộ text vào: `incoming/extracted_text.txt`
- Tự động render các trang đầu ra ảnh PNG 150 DPI để Agent mở xem trực tiếp bằng `read_file`.

### Bước 2: Tra cứu Tiền lệ & Toàn văn (Search History & Full-text)
Chạy lệnh tìm kiếm FTS5 hợp nhất với cả chế độ metadata và toàn văn:
```powershell
d:\TH\vanban-ytcc\.venv\Scripts\python.exe d:\TH\vanban-ytcc\tools\ytcc.py search "<từ_khóa>" --mode all --limit 5
```
- **Tra cứu toàn văn (`--mode fulltext`):** Giúp bóc tách ngay câu văn, căn cứ pháp lý và lập luận nằm sâu trong thân bài các file PDF cũ qua đoạn trích (snippet).
- **Tham khảo bản mẫu vàng:** Đối chiếu ngay kho bản mẫu chuẩn tại `knowledge_base/golden_jsons/` để chọn khung JSON phù hợp nhất.
- **Tham khảo ngân hàng căn cứ:** Mở `knowledge_base/memory/citations_bank.md` để lấy câu căn cứ chuẩn xác 100%, tuyệt đối không tự đoán số quyết định.

### Bước 3: Rút trích Văn phong & Căn cứ từ S0 (Inspect Reference)
- Sử dụng subagent READ-ONLY hoặc Python để đọc PDF tiền lệ:
  - Học cấu trúc câu văn mở đầu và kết luận đặc thù Khoa YTCC.
  - Lấy mẫu các căn cứ pháp lý thường dùng từ `citations_bank.md`.
  - Kiểm tra danh sách `Kính gửi:` và `Nơi nhận:` thực tế (không tin cậy cột `noi_nhan` nội bộ trong DB lịch sử).

---

## 3. Đầu ra (Outputs)
Một bảng tóm tắt nghiệp vụ gồm:
1. **Thư mục vụ việc đã tạo:** `drafts/YYYY-MM/<YYYYMMDD_case>/`
2. **Thông tin bóc tách văn bản đến:** Số hiệu, ngày ban hành, đơn vị gửi, nội dung chính.
3. **Tiền lệ sát nhất:** File PDF nguồn, đoạn trích câu chữ phù hợp.
4. **Bản mẫu vàng đề xuất:** Bản JSON tương ứng trong `knowledge_base/golden_jsons/`.
