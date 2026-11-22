# BÀI HỌC KINH NGHIỆM HÀNH CHÍNH (LESSONS LEARNED)
> Kho lưu trữ tri thức rút tỉa từ các góp ý và hiệu chỉnh thực tế. AI bắt buộc đọc file này trước mỗi phiên soạn thảo để không lặp lại lỗi cũ.
> 
> **NGUYÊN TẮC QUẢN TRỊ FILE (CHỐNG PHÌNH BỘ NHỚ):**
> - Luôn ghi ngắn gọn đúng 1–2 dòng theo cấu trúc: `- [YYYY-MM-DD] TRÁNH: ... | NÊN: ...`.
> - Khi phát sinh kinh nghiệm mới, phải chủ động rà soát và gộp ý nếu đã có nội dung tương tự, giữ tổng thể tài liệu súc tích, dễ tra cứu.

---

## 1. Văn phong & Câu chữ Hành chính
- [2026-11-22] TRÁNH: Dùng câu văn dài dòng hoặc từ ngữ mang tính văn xuôi ("kính chuyển lời chúc sức khỏe", "rất mong nhận được phản hồi sớm"). | NÊN: Dùng văn phong chuẩn mực YTCC ("Khoa Y tế Công cộng trân trọng thông báo đến Quý Đơn vị để phối hợp thực hiện./.").
- [2026-11-22] TRÁNH: Lặp lại từ "V/v" hoặc "Về việc" trong nội dung trích yếu. | NÊN: Để trích yếu tự nhiên ("Đồng ý để viên chức tham gia...", "Xin phê duyệt chủ trương..."), engine sẽ tự chèn tiền tố phù hợp theo từng thể loại.
- [2026-11-22] TRÁNH: Viết tên văn bản đến một cách chung chung ("Theo công văn của đối tác"). | NÊN: Ghi đích danh số, ngày tháng và cơ quan ban hành ("Căn cứ Công văn số 10-11/CV2026 ngày 10/11/2026 của Công ty TNHH...").

---

## 2. Thể thức & Bố cục Word / PDF
- [2026-11-22] TRÁNH: Vẽ vạch kẻ dưới Tiêu ngữ quá ngắn (chỉ 10-14 ký tự) làm mất cân xứng với Quốc hiệu. | NÊN: Dùng 30 ký tự `─` cỡ 8pt để vạch kẻ phủ kín 100% độ dài dòng chữ `Độc lập – Tự do – Hạnh phúc` theo chuẩn NĐ 30.
- [2026-11-22] TRÁNH: Tô màu nền xanh (shading) mặc định cho dòng tiêu đề bảng biểu. | NÊN: Giữ nền trắng trong suốt, chữ in đậm theo chuẩn NĐ 30 (chỉ tô màu khi người dùng yêu cầu rõ ràng).
- [2026-11-22] TRÁNH: Đặt ô `DUYỆT BAN GIÁM HIỆU` lệch hẳn về cột trái dưới `Nơi nhận:`. | NÊN: Đặt ô phê duyệt BGH căn giữa toàn trang ở dưới cùng theo đúng mẫu thực tế S0 (`To_trinh_SoDi_927.pdf`).
- [2026-11-22] TRÁNH: Chèn bảng rộng từ 6 cột trở lên vào trang dọc gây tràn lề hoặc cắt chữ. | NÊN: Tách bảng rộng vào section khổ ngang `landscape_section` ($297 \times 210$ mm) để các cột dàn trải thoáng đãng.

---

## 3. Phân loại & Định tuyến Nơi nhận
- [2026-11-22] TRÁNH: Nhầm lẫn trường `noi_nhan` trong CSDL lịch sử (nhiều bản ghi thực chất chỉ lưu tên chuyên viên nội bộ như `Luận`, `Quyết`, `Tường`). | NÊN: Xác định cơ quan nhận thật từ văn bản đến, yêu cầu người dùng hoặc đối chiếu PDF gốc (S0).
- [2026-11-22] TRÁNH: Để Giấy giới thiệu dùng Header cấp Khoa (`header_level: "ytcc"`). | NÊN: Luôn dùng Header cấp Trường (`header_level: "ump"`) và chức danh ký `TL. HIỆU TRƯỞNG\nTRƯỞNG KHOA`.

---

## 4. Lỗi Kỹ thuật & An toàn Hệ thống
- [2026-11-22] TRÁNH: Dùng lệnh `Stop-Process -Name WINWORD` hoặc chạy song song nhiều lệnh Word COM gây treo hoặc xung đột Office. | NÊN: Điều khiển Word COM tuần tự, mở ReadOnly và đóng sạch trong khối `try / finally`.
- [2026-11-22] TRÁNH: Bỏ qua bước kiểm tra mắt thường và chỉ dựa vào exit code của script. | NÊN: Bắt buộc mở trực tiếp 100% ảnh PNG bằng công cụ thị giác (`read_file`) để soi lề, vạch kẻ và chữ ký trước khi bàn giao.
- [2026-11-22] TRÁNH: Tự động gán cứng họ tên lãnh đạo ký từ kho dữ liệu cũ khi người dùng chưa xác nhận. | NÊN: Luôn dùng placeholder `[HỌ TÊN NGƯỜI KÝ]` và liệt kê rõ ràng trong báo cáo bàn giao.
