# PLAN.md - KẾ HOẠCH TRIỂN KHAI V2.5 (HỆ THỐNG VĂN BẢN KHOA YTCC)

## Mục tiêu tổng thể
Xây dựng hệ thống tự động hóa soạn thảo, chuẩn hóa, tra cứu toàn văn và xuất văn bản hành chính cho Khoa Y tế Công cộng (ĐHYD TP.HCM) theo Nghị định 30/2020/NĐ-CP và dữ liệu mẫu thực tế, đạt độ ổn định và an toàn cao trên nền tảng Windows PowerShell 5.1 và Word COM.

---

## Tiến độ Triển khai theo các Giai đoạn

### ✅ Phase 0: Dọn dẹp Repo & Khởi tạo Khung v2.0 (HOÀN THÀNH)
- Lưu trữ toàn bộ bản cũ vào `_archive/v1_legacy/`.
- Bảo lưu nguyên vẹn 800 PDF mẫu S0, 2 file JSON lịch sử S1 và DLL kết nối.
- Cập nhật `.gitignore` loại bỏ theo dõi các file bí mật, log, và render tạm.

### ✅ Phase 1: Rút chuẩn Thể thức (S0) & Công cụ Tìm kiếm SQLite FTS5 (HOÀN THÀNH)
- Xây dựng CSDL SQLite `ytcc_history.db` với FTS5 và cột không dấu `text_no_accent`, nạp 2.960 CV đi, 3.873 CV đến và 800 PDF.
- Công cụ CLI `tools/search_history.py` tìm kiếm tức thì cả tiếng Việt có dấu và không dấu.
- Khảo sát 15 PDF mẫu thực tế, render 30 ảnh PNG và ban hành đặc tả chuẩn `knowledge_base/specs/ytcc_format_spec.md`.

### ✅ Phase 2: Engine Sinh DOCX Linh hoạt & Pipeline Xuất PDF An toàn (HOÀN THÀNH)
- Xây dựng Engine `tools/build_doc.py` và script xuất PDF qua Word COM `tools/export_pdf.ps1` an toàn (try/finally, 0 tiến trình treo).
- Ban hành đặc tả cấu trúc dữ liệu `knowledge_base/specs/doc_schema.md`.
- Xây dựng công cụ kiểm định tự động `tools/inspect_pdf.py` (PyMuPDF).
- Nghiệm thu 6/6 test case chuẩn hóa đạt **100% PASS** qua script và đối soát trực quan mắt thường.

### ✅ Phase 3 & 3.5: Rules, Skills, Thử nghiệm Thực chiến & Memory Loop (HOÀN THÀNH)
- Ban hành 3 Rules cốt lõi và 4 Skills tác nghiệp.
- Thử nghiệm thành công 3 ca thực chiến khép kín trong `drafts/2026-11/`.
- Xây dựng hệ thống bộ nhớ tự học: `user_preferences.md` và `lessons_learned.md`.
- Phát triển công cụ so sánh bản sửa tay `tools/diff_draft.py`.

### ✅ Phase 2.5A: CLI Hợp nhất, Linter Hành chính & Batch Word COM (HOÀN THÀNH)
- Nâng cấp `build_doc.py`: Hỗ trợ **Inline Markdown** (`***đậm nghiêng***`, `**in đậm**`, `*in nghiêng*`), bí danh `p`, `h1`-`h3`, `quote`, và strict schema validator `validate_schema`.
- Xây dựng Linter Hành chính `tools/lint_doc.py`: Logic cộng dồn bảng, đối chiếu lịch vạn niên thực tế, phát hiện lặp trích yếu, kiểm tra nhất quán doc_type và placeholder (`--strict-final`).
- Nâng cấp `tools/export_pdf.ps1`: Chế độ `-BatchJson` khởi tạo 1 phiên `Word.Application` duy nhất, xuất siêu tốc (1.71s/file), định dạng UTF-8 with BOM.
- Nâng cấp `tools/inspect_pdf.py`: Telemetry lố trang `--target-one-page` đo lường số dòng, ký tự và % chiều cao chiếm dụng ở trang 2 (`OVERFLOW_PAGE_2`).
- Xây dựng CLI tiền xử lý văn bản đến `tools/ingest_incoming.py` bóc tách text và render PNG.
- Hợp nhất toàn bộ vào Unified CLI `tools/ytcc.py`.

### ✅ Phase 2.5B: Full-text FTS5, Sync KB, Golden JSONs, Memory v2 & Chốt sổ (HOÀN THÀNH)
- Đánh chỉ mục toàn văn `fulltext_fts` (FTS5) trích xuất nội dung từ 500+ file PDF mẫu, kèm bảng `indexed_files` đồng bộ tăng dần.
- Nâng cấp `search_history.py` và `ytcc.py search` hỗ trợ `--mode meta|fulltext|all` in kèm đoạn trích ngữ cảnh (snippet).
- Xây dựng công cụ đồng bộ tăng dần `tools/sync_kb.py` (chạy < 1-2s, nhận diện 0 file thay đổi) và script phụ MySQL delta `tools/fetch_mysql_delta.ps1`.
- Thiết lập kho Bản mẫu vàng `knowledge_base/golden_jsons/` với 5 bộ JSON mẫu chuẩn 0 ERROR và lệnh `ytcc.py promote`.
- Nâng cấp Memory v2: Ngân hàng căn cứ `knowledge_base/memory/citations_bank.md` và chuẩn hóa gắn tag `[TAG]` + trần 50 dòng trong `lessons_learned.md`.
- Đồng bộ toàn diện hệ thống Rules, Skills, tài liệu và đẩy lên Git.
