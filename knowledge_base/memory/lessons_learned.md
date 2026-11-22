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
- [CV] [2026-11-22] TRÁNH: Dùng câu kết kiểu thông báo đối ngoại ("Khoa trân trọng thông báo đến Quý Công ty...") trong công văn trình nội bộ. | NÊN: Dùng câu kết trình duyệt chuẩn mực ("Khoa Y tế công cộng kính trình Ban Giám hiệu và Phòng Tổ chức – Nhân sự xem xét, phê duyệt.\nTrân trọng./.").
- [CV] [2026-11-22] TRÁNH: Trình bày thông tin nhân sự cử đi dạng gạch đầu dòng sơ sài, thiếu thông tin liên lạc. | NÊN: Trình bày thành các đoạn riêng biệt (Họ tên kèm SĐT, Đơn vị công tác đầy đủ tên Bộ môn, Nội dung chủ đề, Thời gian có thứ trong tuần, Địa điểm).
- [TTr] [2026-11-22] TRÁNH: Đưa căn cứ không rõ nguồn gốc vào Tờ trình. | NÊN: Chỉ trích dẫn từ `citations_bank.md`, văn bản đến hoặc giữ placeholder `[CHỜ XÁC NHẬN SỐ/NGÀY]`.

---

## 2. Thể thức & Bố cục Word / PDF
- [ALL] [2026-11-22] TRÁNH: Dòng Số: ... và Địa danh ngày tháng bị lệch cao thấp trong Header. | NÊN: Dùng bảng Header 2 dòng tách biệt để dòng Số: ... và dòng Thành phố Hồ Chí Minh, ngày ... luôn thẳng hàng ngang tuyệt đối.
- [ALL] [2026-11-22] TRÁNH: Để đoạn Căn cứ hoặc dòng Trích yếu Công văn in nghiêng. | NÊN: Cả Căn cứ và Trích yếu Công văn đều dùng chữ đứng bình thường theo chuẩn Khoa YTCC.
- [ALL] [2026-11-22] TRÁNH: Để chữ Kính gửi in đậm (bold) hoặc gạch chân. | NÊN: Kính gửi: dùng chữ đứng bình thường, không in đậm, không gạch chân.
- [ALL] [2026-11-22] TRÁNH: Dùng cỡ chữ không chuẩn cho khối Nơi nhận. | NÊN: Dòng Nơi nhận: cỡ 12pt; các dòng con bên dưới (- Như trên;, - Lưu: ...) cỡ 11pt.
- [ALL] [2026-11-22] TRÁNH: Vẽ vạch kẻ dưới Tiêu ngữ quá dài (28-30 ký tự) hoặc quá ngắn (10-14 ký tự). | NÊN: Dùng đúng 24 ký tự `─` cỡ 8pt để phủ vừa khít 100% độ dài dòng chữ `Độc lập – Tự do – Hạnh phúc` (khớp độ rộng ~136pt với 138pt của chữ).
- [ALL] [2026-11-22] TRÁNH: Để khoảng cách khối chữ ký quá hẹp (dưới 35pt) khi target_one_page làm mất không gian chèn chữ ký số điện tử. | NÊN: Luôn duy trì khoảng trống khối chữ ký từ 48-55pt (hoặc sign_gap_pt: 55) để đủ diện tích đóng dấu/chèn chữ ký số theo NĐ 30.
- [ALL] [2026-11-22] TRÁNH: Tô màu nền xanh (shading) mặc định cho dòng tiêu đề bảng biểu. | NÊN: Giữ nền trắng trong suốt, chữ in đậm theo chuẩn NĐ 30 (chỉ tô màu khi có tùy chọn `header_shading`).
- [TTr] [2026-11-22] TRÁNH: Đặt ô `DUYỆT BAN GIÁM HIỆU` lệch hẳn về cột trái dưới `Nơi nhận:`. | NÊN: Đặt ô phê duyệt BGH căn giữa toàn trang ở dưới cùng theo đúng mẫu thực tế S0 (`To_trinh_SoDi_927.pdf`).
- [KH] [2026-11-22] TRÁNH: Chèn bảng rộng từ 6 cột trở lên vào trang dọc gây tràn lề hoặc co chữ. | NÊN: Tách bảng rộng vào section khổ ngang `landscape_section` (297x210 mm) có lặp lại tiêu đề trang (`tblHeader`).
- [ALL] [2026-11-22] TRÁNH: Để văn bản target_one_page bị tràn 1-2 dòng sang trang 2. | NÊN: Linter & inspect_pdf sẽ báo `OVERFLOW_PAGE_2`; điều chỉnh câu chữ hoặc giãn dòng để vừa khít 1 trang.

---

## 3. Phân loại & Định tuyến Nơi nhận
- [ALL] [2026-11-22] TRÁNH: Nhầm lẫn trường `noi_nhan` trong CSDL lịch sử (nhiều bản ghi thực chất chỉ lưu tên chuyên viên nội bộ như `Luận`, `Quyết`, `Tường`). | NÊN: Xác định cơ quan nhận thật từ văn bản đến, yêu cầu người dùng hoặc đối chiếu PDF gốc S0.
- [CV] [2026-11-22] TRÁNH: Nhầm văn bản đến gửi ĐHYD (BGH bút phê chuyển Khoa) thành công văn phúc đáp đối tác bên ngoài. | NÊN: Soạn Công văn nội bộ trình BGH và Phòng Tổ chức – Nhân sự (mã YTCC-HCTC) để trình Nhà trường cho phép.
- [CV] [2026-11-22] TRÁNH: Đưa đối tác bên ngoài hoặc liệt kê quá nhiều phòng ban vào Kính gửi/Nơi nhận trong công văn trình nội bộ cử viên chức. | NÊN: Kính gửi: Ban Giám hiệu và Phòng Tổ chức – Nhân sự; Nơi nhận chỉ gồm: - Như trên; - Lưu: VT, HCTC_VTTH.
- [GGT] [2026-11-22] TRÁNH: Để Giấy giới thiệu dùng Header cấp Khoa (`header_level: "ytcc"`). | NÊN: Bắt buộc dùng Header cấp Trường (`header_level: "ump"`) và chức danh ký `TL. HIỆU TRƯỞNG\nTRƯỞNG KHOA`.
- [TTr] [2026-11-22] TRÁNH: Tờ trình dùng mã số hiệu `YTCC-VP`. | NÊN: Bắt buộc dùng mã `TTr-YTCC` và gửi đúng cơ quan phê duyệt (Ban Giám hiệu, Phòng TCKT,...).

---

## 4. An toàn Hệ thống & Kỹ thuật
- [ALL] [2026-11-22] TRÁNH: Dùng lệnh `Stop-Process -Name WINWORD` hoặc chạy song song nhiều lệnh Word COM gây treo Office. | NÊN: Điều khiển Word COM tuần tự, xuất batch qua `tools/ytcc.py batch` và đóng sạch trong `finally`.
- [ALL] [2026-11-22] TRÁNH: Bỏ qua bước kiểm tra mắt thường mà chỉ tin vào exit code của script. | NÊN: Bắt buộc mở trực tiếp 100% ảnh PNG bằng công cụ thị giác (`read_file`) để soi vạch kẻ, lề và chữ ký trước khi bàn giao.
- [ALL] [2026-11-22] TRÁNH: Tự động gán cứng họ tên lãnh đạo ký từ dữ liệu cũ khi chưa xác nhận. | NÊN: Luôn dùng placeholder `[HỌ TÊN NGƯỜI KÝ]` và báo cáo rõ ràng cho người dùng.
- [ALL] [2026-11-22] TRÁNH: Dùng cú pháp `para` hoặc block type không chuẩn trong JSON. | NÊN: Sử dụng chuẩn schema v2.5 (`p`, `h1`-`h3`, `quote`, `bullet`, `table`) và chạy `ytcc build` để kiểm tra.
