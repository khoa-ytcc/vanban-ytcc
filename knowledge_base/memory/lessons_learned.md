# BÀI HỌC KINH NGHIỆM HÀNH CHÍNH (LESSONS LEARNED V2.5)
> Bộ nhớ dài hạn lưu trữ tri thức, phản hồi hiệu chỉnh và bài học thể thức thực tế.
> 
> **QUY CHUẨN GẮN TAG & QUẢN TRỊ NGỮ CẢNH (CHỐNG PHÌNH BỘ NHỚ):**
> 1. Mỗi dòng bài học bắt buộc mang tiền tố tag phân loại: `[ALL]`, `[CV]` (Công văn), `[TTr]` (Tờ trình), `[KH]` (Kế hoạch), `[BC]` (Báo cáo), `[GGT]` (Giấy giới thiệu).
> 2. Định dạng chuẩn: `- [TAG] [YYYY-MM-DD] TRÁNH: ... | NÊN: ...`
> 3. **Trần tối đa 50 dòng kích hoạt:** Toàn bộ file không vượt quá 50 mục đang kích hoạt. Khi chạm ngưỡng 45 mục, AI tự động rà soát, gộp các ý trùng lặp hoặc di chuyển bài học cũ vào mục lưu trữ.

---

## 1. Văn phong & Câu chữ Hành chính
- [ALL] [2026-11-22] TRÁNH: Dùng văn phong dài dòng, mang tính văn xuôi ("chúc sức khỏe", "rất mong nhận phản hồi"). | NÊN: Dùng văn phong chuẩn mực YTCC ("Khoa trân trọng thông báo đến Quý Đơn vị để phối hợp thực hiện./.").
- [CV] [2026-11-22] TRÁNH: Lặp lại tiền tố "V/v" hoặc "Về việc" trong nội dung trích yếu. | NÊN: Để trích yếu tự nhiên ("Cử viên chức tham gia...", "Phúc đáp đề nghị..."), engine sẽ tự chèn tiền tố phù hợp.
- [CV] [2026-11-22] TRÁNH: Viết căn cứ văn bản đến chung chung ("Theo công văn của đối tác"). | NÊN: Ghi rõ số, ngày tháng và cơ quan ("Căn cứ Công văn số ... ngày ... của ... về việc ...").
- [TTr] [2026-11-22] TRÁNH: Đưa căn cứ không rõ nguồn gốc vào Tờ trình. | NÊN: Chỉ trích dẫn từ `citations_bank.md`, văn bản đến hoặc giữ placeholder `[CHỜ XÁC NHẬN SỐ/NGÀY]`.

---

## 2. Thể thức & Bố cục Word / PDF
- [ALL] [2026-11-22] TRÁNH: Vẽ vạch kẻ dưới Tiêu ngữ quá ngắn (10-14 ký tự) làm mất cân xứng. | NÊN: Dùng 30 ký tự `─` cỡ 8pt phủ kín 100% dòng `Độc lập – Tự do – Hạnh phúc` chuẩn NĐ 30.
- [ALL] [2026-11-22] TRÁNH: Tô màu nền xanh (shading) mặc định cho dòng tiêu đề bảng biểu. | NÊN: Giữ nền trắng trong suốt, chữ in đậm theo chuẩn NĐ 30 (chỉ tô màu khi có tùy chọn `header_shading`).
- [TTr] [2026-11-22] TRÁNH: Đặt ô `DUYỆT BAN GIÁM HIỆU` lệch hẳn về cột trái dưới `Nơi nhận:`. | NÊN: Đặt ô phê duyệt BGH căn giữa toàn trang ở dưới cùng theo đúng mẫu thực tế S0 (`To_trinh_SoDi_927.pdf`).
- [KH] [2026-11-22] TRÁNH: Chèn bảng rộng từ 6 cột trở lên vào trang dọc gây tràn lề hoặc co chữ. | NÊN: Tách bảng rộng vào section khổ ngang `landscape_section` (297x210 mm) có lặp lại tiêu đề trang (`tblHeader`).
- [ALL] [2026-11-22] TRÁNH: Để văn bản target_one_page bị tràn 1-2 dòng sang trang 2. | NÊN: Linter & inspect_pdf sẽ báo `OVERFLOW_PAGE_2`; điều chỉnh câu chữ hoặc giãn dòng để vừa khít 1 trang.

---

## 3. Phân loại & Định tuyến Nơi nhận
- [ALL] [2026-11-22] TRÁNH: Nhầm lẫn trường `noi_nhan` trong CSDL lịch sử (nhiều bản ghi thực chất chỉ lưu tên chuyên viên nội bộ như `Luận`, `Quyết`, `Tường`). | NÊN: Xác định cơ quan nhận thật từ văn bản đến, yêu cầu người dùng hoặc đối chiếu PDF gốc S0.
- [GGT] [2026-11-22] TRÁNH: Để Giấy giới thiệu dùng Header cấp Khoa (`header_level: "ytcc"`). | NÊN: Bắt buộc dùng Header cấp Trường (`header_level: "ump"`) và chức danh ký `TL. HIỆU TRƯỞNG\nTRƯỞNG KHOA`.
- [TTr] [2026-11-22] TRÁNH: Tờ trình dùng mã số hiệu `YTCC-VP`. | NÊN: Bắt buộc dùng mã `TTr-YTCC` và gửi đúng cơ quan phê duyệt (Ban Giám hiệu, Phòng TCKT,...).

---

## 4. An toàn Hệ thống & Kỹ thuật
- [ALL] [2026-11-22] TRÁNH: Dùng lệnh `Stop-Process -Name WINWORD` hoặc chạy song song nhiều lệnh Word COM gây treo Office. | NÊN: Điều khiển Word COM tuần tự, xuất batch qua `tools/ytcc.py batch` và đóng sạch trong `finally`.
- [ALL] [2026-11-22] TRÁNH: Bỏ qua bước kiểm tra mắt thường mà chỉ tin vào exit code của script. | NÊN: Bắt buộc mở trực tiếp 100% ảnh PNG bằng công cụ thị giác (`read_file`) để soi vạch kẻ, lề và chữ ký trước khi bàn giao.
- [ALL] [2026-11-22] TRÁNH: Tự động gán cứng họ tên lãnh đạo ký từ dữ liệu cũ khi chưa xác nhận. | NÊN: Luôn dùng placeholder `[HỌ TÊN NGƯỜI KÝ]` và báo cáo rõ ràng cho người dùng.
- [ALL] [2026-11-22] TRÁNH: Dùng cú pháp `para` hoặc block type không chuẩn trong JSON. | NÊN: Sử dụng chuẩn schema v2.5 (`p`, `h1`-`h3`, `quote`, `bullet`, `table`) và chạy `ytcc build` để kiểm tra.
