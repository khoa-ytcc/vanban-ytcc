# AGENTS.md - QUY CHUẨN VẬN HÀNH AI V2.0 (KHOA YTCC)

Tài liệu này xác lập quy chuẩn vận hành, phân vai và các ràng buộc kỹ thuật bắt buộc cho toàn bộ dự án tự động hóa văn bản hành chính Khoa Y tế Công cộng (Đại học Y Dược TP.HCM).

---

## 1. Phân vai và nguyên tắc điều phối
- **Reviewer / Planner:** Gemini Web (chịu trách nhiệm quy hoạch tổng thể, duyệt kế hoạch từng Phase, kiểm tra và nghiệm thu kết quả).
- **Worker thực thi:** Gemini 3.8 Flash trên Antigravity local.
- **Quy tắc làm việc:** Worker thực hiện tuần tự, đúng phạm vi công việc của Phase được giao. Khi hoàn tất mục tiêu Phase, Worker dừng lại và lập báo cáo kết quả kèm bằng chứng để Reviewer thẩm định trước khi chuyển sang Phase tiếp theo.

---

## 2. Bảng Định tuyến Rules & Skills Nghiệp vụ v2.0

### A. Bộ Rules Cốt lõi (`.agents/rules/`)
| Quy tắc | Đường dẫn | Trọng tâm áp dụng |
|:---|:---|:---|
| **Thể thức & Văn phong** | [.agents/rules/format_and_style.md](file:///d:/TH/vanban-ytcc/.agents/rules/format_and_style.md) | Header 2 cột, vạch kẻ chuẩn S0, adaptive layout 1 trang vs nhiều trang, bảng nền trắng NĐ 30, dòng lưu Khoa YTCC. |
| **Thẩm quyền & Định tuyến** | [.agents/rules/authority_and_routing.md](file:///d:/TH/vanban-ytcc/.agents/rules/authority_and_routing.md) | Thẩm quyền ký, quy tắc placeholder người ký, cảnh báo trường `noi_nhan` nội bộ trong CSDL lịch sử, cách xác định cơ quan nhận thật. |
| **An toàn & Tiến trình** | [.agents/rules/execution_safety.md](file:///d:/TH/vanban-ytcc/.agents/rules/execution_safety.md) | Thứ bậc S0 > S1 > S2, quy trình bắt buộc 4 bước (soạn JSON → DOCX/PDF → QA script → soi ảnh PNG 100%), cấm kill WINWORD hàng loạt. |

### B. Bộ Skills Thực chiến (`.agents/skills/`)
| Kỹ năng | Đường dẫn | Nhiệm vụ chính |
|:---|:---|:---|
| **ytcc-intake-and-search** | [.agents/skills/ytcc-intake-and-search/SKILL.md](file:///d:/TH/vanban-ytcc/.agents/skills/ytcc-intake-and-search/SKILL.md) | Tiếp nhận văn bản đến/yêu cầu mới, bóc tách thực thể, tra cứu FTS5 SQLite và đối chiếu PDF S0 để học cấu trúc lập luận. |
| **ytcc-draft-and-build** | [.agents/skills/ytcc-draft-and-build/SKILL.md](file:///d:/TH/vanban-ytcc/.agents/skills/ytcc-draft-and-build/SKILL.md) | Soạn thảo JSON chuẩn schema, tích hợp placeholder thông tin thiếu, gọi `build_doc.py --pdf` tạo song song Word DOCX và PDF. |
| **ytcc-qa-review** | [.agents/skills/ytcc-qa-review/SKILL.md](file:///d:/TH/vanban-ytcc/.agents/skills/ytcc-qa-review/SKILL.md) | Chạy kiểm định tự động `inspect_pdf.py` và thẩm định thị giác trực tiếp bằng mắt thường qua 100% ảnh PNG trước khi bàn giao. |
| **ytcc-learn-and-memorize** | [.agents/skills/ytcc-learn-and-memorize/SKILL.md](file:///d:/TH/vanban-ytcc/.agents/skills/ytcc-learn-and-memorize/SKILL.md) | Tự học thói quen người dùng qua góp ý chat hoặc chạy `diff_draft.py` khi người dùng sửa Word, cập nhật bộ nhớ dài hạn. |

---

## 3. Hệ thống Tự học & Bộ nhớ Dài hạn (Memory Loop)
> [!IMPORTANT] NGUYÊN TẮC BẮT BUỘC TRƯỚC MỖI PHIÊN SOẠN THẢO
> Trước khi tạo bất kỳ văn bản nào, Agent bắt buộc phải đọc 2 file bộ nhớ sau:
> 1. [knowledge_base/memory/user_preferences.md](file:///d:/TH/vanban-ytcc/knowledge_base/memory/user_preferences.md): Nắm thói quen chuyên viên, mã lưu văn thư và danh sách lãnh đạo ký đã được xác nhận.
> 2. [knowledge_base/memory/lessons_learned.md](file:///d:/TH/vanban-ytcc/knowledge_base/memory/lessons_learned.md): Rà soát các bài học kinh nghiệm về câu từ, thể thức và kỹ thuật để tuyệt đối không lặp lại lỗi cũ.

---

## 4. Chính sách phân nhiệm Subagent
- **Cho phép (Read-only):** Được phép spawn tối đa 2–3 subagents song song **CHỈ** phục vụ các tác vụ đọc/tra cứu độc lập (đọc hiểu PDF mẫu, tra cứu dữ liệu lịch sử JSON, soát lỗi chính tả/thể thức bản nháp).
- **Nghiêm cấm:** Tuyệt đối không spawn subagent cho các tác vụ ghi/chỉnh sửa file, can thiệp code/template, hoặc tương tác với tiến trình Word COM (`WINWORD.EXE`). Mọi tác vụ ghi hoặc điều khiển Office COM đều do Main Worker đảm nhiệm tuần tự.

---

## 5. Thứ bậc nguồn dữ liệu (S0 > S1 > S2)
- **S0 (Nguồn chân lý gốc):** Các file PDF thực tế được lưu tại `knowledge_base/sample_pdfs/` và bản ghi đối chiếu từ phần mềm Quản lý văn bản.
- **S1 (Nguồn dẫn xuất):** Các tệp JSON lịch sử (`cv_di_history.json`, `cv_den_history.json`) và SQLite DB (`ytcc_history.db`) dùng để tra cứu tiền lệ, số hiệu, trích yếu, nơi nhận.
- **S2 (Tạo phẩm phái sinh):** Toàn bộ template Word (`.docx`), script tự động hóa (`.ps1`, `.py`), bảng đặc tả (`specs/`), rules và skills do AI sinh ra. Bắt buộc phải đối chiếu và kiểm chứng với S0 trước khi nghiệm thu.

---

## 6. Ràng buộc kỹ thuật Windows & PowerShell 5.1
- **Định dạng file:** Mọi file mã nguồn PowerShell (`.ps1`) có chứa ký tự tiếng Việt bắt buộc phải được lưu ở định dạng **UTF-8 with BOM** để PowerShell 5.1 hiển thị và xử lý chính xác.
- **Quy trình Word COM an toàn (Export PDF):**
  1. Mở file qua Word COM (`$doc = $word.Documents.Open(..., $true)` ở chế độ ReadOnly).
  2. Xuất PDF cố định (`$doc.ExportAsFixedFormat($pdfPath, 17)`).
  3. Đóng tài liệu an toàn trong khối finally (`$doc.Close([ref]$false)`).
  4. Thoát Word và giải phóng COM object (`$word.Quit()`, `[System.Runtime.InteropServices.Marshal]::ReleaseComObject(...)`).
  5. *Lưu ý:* Chỉ đóng đúng phiên Word COM do script khởi tạo; tuyệt đối không dùng lệnh kill hàng loạt (`Stop-Process -Name WINWORD`) làm ảnh hưởng tài liệu người dùng đang mở.
- **Quy tắc Thẩm định Thị giác:** Mọi văn bản xuất bản phải được render ra ảnh PNG và Agent tự mở xem trực tiếp bằng mắt thường trước khi bàn giao.
