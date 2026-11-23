# HƯỚNG DẪN NGỮ CẢNH HỆ THỐNG (GEMINI.MD - KHOA YTCC V2.5)

Chào mừng bạn đến với hệ thống tự động hóa văn bản hành chính Khoa Y tế Công cộng (Đại học Y Dược TP.HCM).

---

## 1. Điểm nạp Ngữ cảnh Cốt lõi
Khi bắt đầu bất kỳ phiên làm việc nào, Agent bắt buộc phải đọc và tuân thủ các tài liệu gốc sau:
1. [AGENTS.md](file:///d:/TH/vanban-ytcc/AGENTS.md): Bản quy chuẩn vận hành, phân vai (Reviewer: Gemini Web, Worker: Gemini 3.8 Flash), thứ bậc dữ liệu (S0 > S1 > S2) và chính sách subagent.
2. **Bộ Nhớ Dài Hạn (Memory Loop - Bắt buộc đọc trước khi soạn thảo):**
   - [user_preferences.md](file:///d:/TH/vanban-ytcc/knowledge_base/memory/user_preferences.md): Nắm thói quen chuyên viên, mã lưu hồ sơ và danh sách lãnh đạo ký đã được xác nhận.
   - [lessons_learned.md](file:///d:/TH/vanban-ytcc/knowledge_base/memory/lessons_learned.md): Rà soát bài học kinh nghiệm hành chính có gắn tag [TAG] để không lặp lại lỗi cũ (trần <= 50 dòng).
   - [citations_bank.md](file:///d:/TH/vanban-ytcc/knowledge_base/memory/citations_bank.md): Ngân hàng căn cứ pháp lý và quy định nội bộ; tuyệt đối không tự đoán số quyết định.
3. **Bộ Rules chuẩn hóa:**
   - [format_and_style.md](file:///d:/TH/vanban-ytcc/.agents/rules/format_and_style.md): Chuẩn thể thức NĐ 30, Header 2 cột, vạch kẻ S0, bảng biểu nền trắng, bố cục thích ứng (1 trang vs nhiều trang/landscape).
   - [authority_and_routing.md](file:///d:/TH/vanban-ytcc/.agents/rules/authority_and_routing.md): Thẩm quyền ký, quy tắc placeholder, cảnh báo trường `noi_nhan` nội bộ trong CSDL lịch sử.
   - [execution_safety.md](file:///d:/TH/vanban-ytcc/.agents/rules/execution_safety.md): Quy trình bắt buộc 4 bước qua `tools/ytcc.py`, linter hành chính, telemetry lố trang, an toàn Word COM.

---

## 2. Quy trình Thực thi Chuẩn qua 4 Skills v2.5
Mọi yêu cầu nghiệp vụ soạn thảo văn bản đều kích hoạt theo chuỗi:
1. **Intake & Search:** [.agents/skills/ytcc-intake-and-search](file:///d:/TH/vanban-ytcc/.agents/skills/ytcc-intake-and-search/SKILL.md)  
   → `ytcc.py ingest` tiền xử lý văn bản đến, `ytcc.py search --mode all` tra cứu FTS5 (metadata & toàn văn snippet), học PDF S0 và tham khảo `knowledge_base/golden_jsons/`.
2. **Draft & Build:** [.agents/skills/ytcc-draft-and-build](file:///d:/TH/vanban-ytcc/.agents/skills/ytcc-draft-and-build/SKILL.md)  
   → Soạn JSON theo [doc_schema.md](file:///d:/TH/vanban-ytcc/knowledge_base/specs/doc_schema.md) (hỗ trợ Inline Markdown), gọi `tools/ytcc.py build --pdf` (hoặc `ytcc.py batch`) tự động lint và sinh file DOCX và PDF.
3. **QA Review:** [.agents/skills/ytcc-qa-review](file:///d:/TH/vanban-ytcc/.agents/skills/ytcc-qa-review/SKILL.md)  
   → Đọc kết quả `inspect_pdf.py` và telemetry `OVERFLOW_PAGE_2`, mở trực tiếp 100% ảnh PNG để soi mắt thường trước khi bàn giao.
4. **Learn & Memorize:** [.agents/skills/ytcc-learn-and-memorize](file:///d:/TH/vanban-ytcc/.agents/skills/ytcc-learn-and-memorize/SKILL.md)  
   → Khi có góp ý hoặc khi so sánh bản Word sửa tay qua `tools/ytcc.py diff`, tự động trích lọc quy tắc gắn tag cập nhật vào `knowledge_base/memory/`, thăng hạng mẫu vàng bằng `tools/ytcc.py promote`.

---

## 3. Môi trường Thực thi & Đồng bộ Git
- Python CLI: `.venv\Scripts\python.exe`
- **Đồng bộ GitHub (Quy chuẩn bắt buộc theo yêu cầu người dùng):** Mỗi lần hoàn tất một tác vụ hoặc phiên làm việc (soạn thảo văn bản, sửa script, cập nhật bộ nhớ...), Agent bắt buộc tự động thực hiện commit và push toàn bộ thay đổi lên GitHub (`origin main`) để người dùng tiếp tục làm việc trên máy khác liền mạch.
- **Office COM:** Không đóng tiến trình Word bằng `Stop-Process`.
