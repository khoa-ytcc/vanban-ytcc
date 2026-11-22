# PLAN.md - KẾ HOẠCH TRIỂN KHAI V2.0 (HỆ THỐNG VĂN BẢN KHOA YTCC)

## Mục tiêu tổng thể
Xây dựng hệ thống tự động hóa soạn thảo, chuẩn hóa và xuất văn bản hành chính cho Khoa Y tế Công cộng (ĐHYD TP.HCM) theo Nghị định 30/2020/NĐ-CP và dữ liệu mẫu thực tế, đạt độ ổn định cao trên nền tảng Windows PowerShell 5.1 và Word COM.

---

## Tiến độ Triển khai theo 4 Phase

### ✅ Phase 0: Dọn dẹp Repo & Khởi tạo Khung v2.0 (HOÀN THÀNH)
- **Kết quả:** Đã archive toàn bộ v1 vào `_archive/v1_legacy/`.
- Bảo lưu nguyên vẹn 800 PDF mẫu S0, 2 file JSON lịch sử S1 và DLL kết nối.
- Cập nhật `.gitignore` loại bỏ theo dõi các file bí mật, log, và render tạm.
- Ban hành quy chuẩn vận hành `AGENTS.md` v2.0.

### ✅ Phase 1: Rút chuẩn Thể thức (S0) & Công cụ Tìm kiếm SQLite FTS5 (HOÀN THÀNH)
- **Kết quả:** Xây dựng CSDL SQLite `ytcc_history.db` với FTS5 và cột không dấu `text_no_accent`, nạp 2.960 CV đi, 3.873 CV đến và 800 PDF.
- Công cụ CLI `tools/search_history.py` tìm kiếm tức thì cả tiếng Việt có dấu và không dấu.
- Khảo sát 15 PDF mẫu thực tế, render 30 ảnh PNG và ban hành đặc tả chuẩn `knowledge_base/specs/ytcc_format_spec.md`.

### ✅ Phase 2: Engine Sinh DOCX Linh hoạt & Pipeline Xuất PDF An toàn (HOÀN THÀNH)
- **Kết quả:** Xây dựng Engine `tools/build_doc.py` và script xuất PDF qua Word COM `tools/export_pdf.ps1` an toàn (try/finally, 0 tiến trình treo).
- Ban hành đặc tả cấu trúc dữ liệu `knowledge_base/specs/doc_schema.md`.
- Xây dựng công cụ kiểm định tự động `tools/inspect_pdf.py` (PyMuPDF).
- Nghiệm thu 6/6 test case chuẩn hóa (1 trang, nhiều trang, landscape phụ lục, ô duyệt BGH, bảng lặp header) đạt **100% PASS** qua script và đối soát trực quan mắt thường.

### ✅ Phase 3: Hoàn thiện Rules, Skills Nghiệp vụ & Thử nghiệm Thực chiến (HOÀN THÀNH)
- **Kết quả:** Ban hành 3 Rules cốt lõi (`format_and_style.md`, `authority_and_routing.md`, `execution_safety.md`).
- Ban hành 3 Skills tác nghiệp (`ytcc-intake-and-search`, `ytcc-draft-and-build`, `ytcc-qa-review`).
- Chạy thử nghiệm thành công 3 ca thực chiến khép kín trong `drafts/2026-11/`: Ca 1 (Phúc đáp CV ghi hình HTV7 - 1 trang), Ca 2 (Tờ trình Hội thảo AI - 2 trang kèm ô duyệt BGH), Ca 3 (Kế hoạch thực tế Đồng Nai - 3 trang kèm Phụ lục khổ ngang). Đạt 100% PASS tự động và kiểm tra mắt thường.

### ✅ Phase 3.5: Lắp Hệ thống Tự học (Memory Loop), Dọn gọn & Đồng bộ v2.0 (HOÀN THÀNH)
- **Kết quả:** Dọn gọn `tools/`, di chuyển các script kiểm thử sang `audit/scripts/`.
- Xây dựng hệ thống bộ nhớ tự học: `knowledge_base/memory/user_preferences.md` và `lessons_learned.md`.
- Phát triển công cụ so sánh bản sửa tay `tools/diff_draft.py` và Skill `ytcc-learn-and-memorize`.
- Cập nhật điểm nạp ngữ cảnh `GEMINI.md`, `AGENTS.md` và hướng dẫn sử dụng `README.md`.
- Kiểm tra bảo mật và đồng bộ sạch lên GitHub.
