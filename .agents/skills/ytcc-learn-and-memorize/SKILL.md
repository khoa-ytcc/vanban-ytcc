---
name: ytcc-learn-and-memorize
description: Tự động ghi nhớ thói quen người dùng và bài học kinh nghiệm hành chính khi có góp ý hoặc khi so sánh bản Word sửa tay qua diff_draft.py.
---

# SKILL: Tự học & Ghi nhớ Thói quen Người dùng (ytcc-learn-and-memorize)

Skill này thiết lập cơ chế vòng lặp phản hồi (Memory Loop), giúp hệ thống AI ngày càng thông minh hơn, nắm bắt chính xác thói quen trình bày và không bao giờ lặp lại lỗi cũ của các phiên làm việc trước.

---

## 1. Khi Nào Kích Hoạt Skill Này?
- Khi người dùng gửi phản hồi chỉnh sửa trực tiếp trên chat (Ví dụ: *"Lần sau trích yếu đừng ghi chữ V/v nữa"*, *"Khoa mình hay dùng dòng lưu VP_NTNM"*, *"Nhớ là Thầy Phong hiện đã chuyển công tác"*).
- Khi người dùng nói các từ khóa: *"rút kinh nghiệm"*, *"ghi nhớ"*, *"lưu thói quen này"*, *"học theo cách này"*.
- Khi người dùng gửi lại một file Word `.docx` đã tự tay sửa từ bản dự thảo do AI tạo ra.

---

## 2. Quy trình Thực hiện 3 Bước (Steps)

### Bước 1: Thu nhận Thay đổi & Phân tích Khác biệt
- **Trường hợp người dùng gửi file `.docx` sửa tay:**
  Chạy ngay công cụ so sánh `diff_draft.py` để trích xuất dòng xóa/thêm:
  ```powershell
  d:\TH\vanban-ytcc\.venv\Scripts\python.exe d:\TH\vanban-ytcc\tools\diff_draft.py --ai "<file_ai_cu.docx>" --final "<file_nguoi_dung_sua.docx>"
  ```
- **Trường hợp góp ý bằng văn bản trên chat:**
  Đọc kỹ nội dung phản hồi để xác định rõ mong muốn của người dùng.

### Bước 2: Chắt lọc Quy tắc Tái sử dụng
Phân loại thông tin thành 2 nhóm rõ ràng:
1. **Chi tiết riêng của sự việc (KHÔNG LƯU):** Các số liệu, ngày tháng, tên người cụ thể chỉ áp dụng cho một vụ việc đơn lẻ thì không đưa vào bộ nhớ dài hạn.
2. **Quy tắc / Thói quen chung lặp lại (BẮT BUỘC LƯU):**
   - Thông tin nhân sự cố định (Tên chuyên viên, mã lưu văn thư).
   - Thói quen câu từ, cách xưng hô, nơi nhận quen thuộc.
   - Chuẩn trình bày thể thức, lề trang, cách bố trí bảng biểu.

### Bước 3: Cập nhật Bộ nhớ & Báo cáo Tinh gọn
Căn cứ vào bản chất thông tin để ghi vào đúng file trong `knowledge_base/memory/`:
- **Thông tin nhân sự / thói quen người dùng:** Cập nhật vào [user_preferences.md](file:///d:/TH/vanban-ytcc/knowledge_base/memory/user_preferences.md).
- **Quy tắc văn phong / thể thức / lỗi cần tránh:** Cập nhật vào [lessons_learned.md](file:///d:/TH/vanban-ytcc/knowledge_base/memory/lessons_learned.md) theo mẫu:
  `- [YYYY-MM-DD] TRÁNH: ... | NÊN: ...`

> [!IMPORTANT] NGUYÊN TẮC CHỐNG PHÌNH BỘ NHỚ
> Trước khi thêm dòng mới, bắt buộc phải rà soát xem trong file đã có ý tương tự chưa. Nếu đã có, phải **chủ động gộp và làm sắc bén ý cũ**, không ghi lặp lại làm loãng file.

Sau khi cập nhật xong, phản hồi cho người dùng đúng 1–2 câu xác nhận ngắn gọn về điều AI vừa ghi nhớ.

---

## 3. Đầu ra (Outputs)
1. File `knowledge_base/memory/user_preferences.md` hoặc `knowledge_base/memory/lessons_learned.md` được cập nhật sạch sẽ.
2. Dòng thông báo xác nhận ngắn gọn gửi người dùng.
