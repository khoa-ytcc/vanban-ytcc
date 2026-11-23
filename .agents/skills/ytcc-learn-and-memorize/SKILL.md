---
name: ytcc-learn-and-memorize
description: Tự động ghi nhớ thói quen người dùng và bài học kinh nghiệm hành chính khi có góp ý hoặc khi so sánh bản Word sửa tay qua ytcc.py diff, đồng thời hỗ trợ thăng hạng bản mẫu vàng qua ytcc.py promote.
---

# SKILL: Tự học & Ghi nhớ Thói quen Người dùng (ytcc-learn-and-memorize v2.5)

Skill này thiết lập cơ chế vòng lặp phản hồi (Memory Loop), giúp hệ thống AI ngày càng thông minh hơn, nắm bắt chính xác thói quen trình bày và không bao giờ lặp lại lỗi cũ của các phiên làm việc trước.

---

## 1. Khi Nào Kích Hoạt Skill Này?
- Khi người dùng gửi phản hồi chỉnh sửa trực tiếp trên chat (Ví dụ: *"Lần sau trích yếu đừng ghi chữ V/v nữa"*, *"Khoa mình hay dùng dòng lưu VP_NTNM"*).
- Khi người dùng gửi lại một file Word `.docx` đã tự tay sửa từ bản dự thảo do AI tạo ra.
- Khi người dùng duyệt một bản văn bản và yêu cầu: *"Lưu bản này làm mẫu chuẩn"* -> Kích hoạt lệnh `promote`.

---

## 2. Quy trình Thực hiện (Steps)

### Bước 1: So sánh Bản sửa tay bằng `ytcc.py diff`
Khi người dùng gửi file Word sửa tay đối chiếu với bản AI dự thảo:
```powershell
d:\TH\vanban-ytcc\.venv\Scripts\python.exe d:\TH\vanban-ytcc\tools\ytcc.py diff --original "drafts/.../v1.docx" --revised "drafts/.../v1_edited.docx"
```
Script sẽ in ra rõ ràng các dòng bị xóa (`-`) và dòng thêm mới (`+`) trong đoạn văn và bảng biểu.

### Bước 2: Chắt lọc Quy tắc Tái sử dụng & Gắn Tag
Phân loại thông tin thành 2 nhóm rõ ràng:
1. **Chi tiết riêng của sự việc (KHÔNG LƯU):** Số tiền cụ thể, ngày tháng sự kiện, tên sinh viên...
2. **Quy tắc / Thói quen chung lặp lại (BẮT BUỘC LƯU):**
   - Thông tin nhân sự cố định -> Cập nhật vào [user_preferences.md](file:///d:/TH/vanban-ytcc/knowledge_base/memory/user_preferences.md).
   - Quy tắc văn phong, thể thức, bố cục -> Cập nhật vào [lessons_learned.md](file:///d:/TH/vanban-ytcc/knowledge_base/memory/lessons_learned.md) theo mẫu:
     `- [TAG] [YYYY-MM-DD] TRÁNH: ... | NÊN: ...`
     *(Các tag bắt buộc: `[ALL]`, `[CV]`, `[TTr]`, `[KH]`, `[BC]`, `[GGT]`)*

> [!IMPORTANT] NGUYÊN TẮC CHỐNG PHÌNH BỘ NHỚ (TRẦN 50 DÒNG)
> File `lessons_learned.md` có giới hạn trần **tối đa 50 dòng kích hoạt**. Khi chạm 45 dòng, AI bắt buộc phải rà soát, gộp các ý tương tự hoặc lưu trữ bài học cũ.

### Bước 3: Thăng hạng Bản mẫu Vàng (`ytcc.py promote`)
Khi người dùng chốt một mẫu văn bản đẹp và muốn lưu vào kho mẫu chuẩn dùng chung:
```powershell
d:\TH\vanban-ytcc\.venv\Scripts\python.exe d:\TH\vanban-ytcc\tools\ytcc.py promote "drafts/.../final.json" --name "<ten_mau>.json"
```
- Lệnh tự động kiểm tra `validate_schema` + `lint_doc` (bắt buộc 0 ERROR).
- Lưu vào `knowledge_base/golden_jsons/<ten_mau>.json`.
- Tự động đồng bộ ngay vào chỉ mục toàn văn SQLite FTS5 qua `sync_kb`.

### Bước 4: Tự động Commit & Push GitHub (Multi-device Sync)
Theo yêu cầu bắt buộc của người dùng, sau mỗi lần hoàn tất một công việc (soạn thảo văn bản, chỉnh sửa code/template, ghi nhớ bài học hoặc thăng hạng mẫu vàng), Agent tự động thực hiện:
```powershell
git add .
git commit -m "<thông điệp mô tả công việc>"
git push origin main
```
Bảo đảm toàn bộ dữ liệu, bộ nhớ và dự thảo được đồng bộ lên GitHub để làm việc liên tục trên các thiết bị khác.

---

## 3. Đầu ra (Outputs)
1. Cập nhật `knowledge_base/memory/` (user_preferences.md hoặc lessons_learned.md gắn tag chuẩn).
2. Bản mẫu vàng được lưu trong `knowledge_base/golden_jsons/` (nếu có promote).
3. Tự động commit và push toàn bộ thay đổi lên GitHub repository.
4. Thông báo xác nhận ngắn gọn gửi người dùng.
