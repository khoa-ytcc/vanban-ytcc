# HƯỚNG DẪN NGỮ CẢNH HỆ THỐNG (GEMINI.MD - KHOA YTCC V2.0)

Chào mừng bạn đến với hệ thống tự động hóa văn bản hành chính Khoa Y tế Công cộng (Đại học Y Dược TP.HCM).

---

## 1. Điểm nạp Ngữ cảnh Cốt lõi
Khi bắt đầu bất kỳ phiên làm việc nào, Agent bắt buộc phải đọc và tuân thủ các tài liệu gốc sau:
1. [AGENTS.md](file:///d:/TH/vanban-ytcc/AGENTS.md): Bản quy chuẩn vận hành, phân vai (Reviewer: Gemini Web, Worker: Gemini 3.8 Flash), thứ bậc dữ liệu (S0 > S1 > S2) và chính sách subagent.
2. **Bộ Nhớ Dài Hạn (Memory Loop - Bắt buộc đọc trước khi soạn thảo):**
   - [user_preferences.md](file:///d:/TH/vanban-ytcc/knowledge_base/memory/user_preferences.md): Nắm thói quen chuyên viên, mã lưu hồ sơ và danh sách lãnh đạo ký đã được xác nhận.
   - [lessons_learned.md](file:///d:/TH/vanban-ytcc/knowledge_base/memory/lessons_learned.md): Rà soát các bài học kinh nghiệm hành chính để không lặp lại lỗi cũ.
3. **Bộ Rules chuẩn hóa:**
   - [format_and_style.md](file:///d:/TH/vanban-ytcc/.agents/rules/format_and_style.md): Chuẩn thể thức NĐ 30, Header 2 cột, vạch kẻ S0, bảng biểu nền trắng, bố cục thích ứng (1 trang vs nhiều trang/landscape).
   - [authority_and_routing.md](file:///d:/TH/vanban-ytcc/.agents/rules/authority_and_routing.md): Thẩm quyền ký, quy tắc placeholder, cảnh báo trường `noi_nhan` nội bộ trong CSDL lịch sử.
   - [execution_safety.md](file:///d:/TH/vanban-ytcc/.agents/rules/execution_safety.md): Quy trình bắt buộc 4 bước (JSON → Build → QA Script → Soi ảnh PNG 100%), an toàn Word COM.

---

## 2. Quy trình Thực thi Chuẩn qua 4 Skills
Mọi yêu cầu nghiệp vụ soạn thảo văn bản đều kích hoạt theo chuỗi:
1. **Intake & Search:** [.agents/skills/ytcc-intake-and-search](file:///d:/TH/vanban-ytcc/.agents/skills/ytcc-intake-and-search/SKILL.md)  
   → Bóc tách văn bản đến / yêu cầu, tra cứu SQLite FTS5 qua `tools/search_history.py`, đọc PDF S0 để học văn phong.
2. **Draft & Build:** [.agents/skills/ytcc-draft-and-build](file:///d:/TH/vanban-ytcc/.agents/skills/ytcc-draft-and-build/SKILL.md)  
   → Soạn JSON theo [doc_schema.md](file:///d:/TH/vanban-ytcc/knowledge_base/specs/doc_schema.md), gọi `tools/build_doc.py --pdf` sinh file DOCX và PDF.
3. **QA Review:** [.agents/skills/ytcc-qa-review](file:///d:/TH/vanban-ytcc/.agents/skills/ytcc-qa-review/SKILL.md)  
   → Chạy `tools/inspect_pdf.py`, mở trực tiếp 100% ảnh PNG để soi mắt thường trước khi bàn giao.
4. **Learn & Memorize:** [.agents/skills/ytcc-learn-and-memorize](file:///d:/TH/vanban-ytcc/.agents/skills/ytcc-learn-and-memorize/SKILL.md)  
   → Khi có góp ý hoặc khi so sánh bản Word sửa tay qua `tools/diff_draft.py`, tự động trích lọc quy tắc và cập nhật vào `knowledge_base/memory/`.

---

## 3. Môi trường Thực thi
- Python CLI: `.venv\Scripts\python.exe`
- Không tự `git commit` hay `git push`. Không đóng tiến trình Word bằng `Stop-Process`.
