# QUY CHUẨN THỂ THỨC & VĂN PHONG VĂN BẢN (KHOA YTCC)
> Áp dụng cho toàn bộ quá trình tự động hóa soạn thảo văn bản hành chính theo chuẩn Nghị định 30/2020/NĐ-CP và đặc thù thực tế Khoa Y tế Công cộng (Đại học Y Dược TP.HCM).

---

## 1. Cấu trúc Tiêu ngữ & Header 2 cột
- **Kích thước & Căn lề chuẩn:** Trang A4 in dọc lề Trái 25 mm (2.5 cm), Trên 20 mm, Dưới 20 mm, Phải 20 mm (vùng in khả dụng 165 mm).
- **Cấu trúc Bảng Header 2 dòng (2 rows x 2 cols):**
  - **Dòng 0:**
    - Cột 1 (70 mm): Đơn vị ban hành (Dòng 1-2: `ĐẠI HỌC Y DƯỢC` / `THÀNH PHỐ HỒ CHÍ MINH` cỡ 10pt đứng; Dòng 3: `KHOA Y TẾ CÔNG CỘNG` cỡ 11pt **đậm**) + Vạch kẻ liền 13 ký tự `─` cỡ 8pt ở giữa.
    - Cột 2 (95 mm): `CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM` (10.5pt **đậm**) / `Độc lập – Tự do – Hạnh phúc` (11pt **đậm**) + Vạch kẻ liền 24 ký tự `─` cỡ 8pt vừa khít dòng chữ (độ rộng ~136pt khớp với 138pt chữ).
  - **Dòng 1:**
    - Cột 1: `Số: .../YTCC-HCTC` (11pt đứng) và dòng trích yếu `V/v ...` (11pt, **CHỮ ĐỨNG, KHÔNG NGHIÊNG**).
    - Cột 2: `Thành phố Hồ Chí Minh, ngày ... tháng ... năm ...` (11pt, nghiêng).
  - *Ý nghĩa:* Tách thành 2 dòng bảng bảo đảm dòng `Số: ...` và dòng `Thành phố Hồ Chí Minh, ngày ...` luôn **thẳng hàng ngang thị giác tuyệt đối 100%**.

---

## 2. Quy chuẩn Font chữ, Căn lề & Dãn dòng Thân bài
- **Cỡ chữ & Dãn dòng thân bài:** Toàn bộ các đoạn thân bài dùng cỡ chữ **13 pt** Times New Roman, dãn dòng **1.5 lines**, thụt đầu dòng 1.27 cm.
- **Căn cứ văn bản:** Tuyệt đối dùng **chữ đứng (KHÔNG in nghiêng)**.
- **Kính gửi:** Chữ đứng bình thường cỡ 13pt, **KHÔNG in đậm (bold), KHÔNG gạch chân (line)**. Các đơn vị nhận bên dưới thụt lề 2.5 cm, dấu gạch đầu dòng `-`.
- **Khối Nơi nhận:** Dòng tiêu đề `Nơi nhận:` cỡ **12 pt** (đậm nghiêng); các dòng danh sách bên dưới (`- Như trên;`, `- Lưu: ...`) cỡ **11 pt**.
- **Khối Chữ ký & Chữ ký số:** Chừa khoảng trống giữa chức vụ (`TRƯỞNG KHOA`) và họ tên người ký từ **50–55 pt** để đủ không gian đóng dấu điện tử và chèn chữ ký số theo Nghị định 30.

---

## 2. Bố cục Thích ứng (Adaptive Layout)
- **Văn bản ngắn 1 trang (`target_one_page: true`):**
  - Tự động co giãn dòng hợp lý (`line_spacing = 1.05`, khoảng cách đoạn 1–2 pt, lề trên/dưới 18 mm).
  - Giữ nguyên cỡ chữ chuẩn 13–14 pt của thân bài theo NĐ 30, không co nhỏ cỡ chữ gây mất thẩm mỹ.
  - Toàn bộ nội dung, nơi nhận và khối chữ ký phải nằm gọn trong 1 trang duy nhất, tuyệt đối không để rớt chữ ký sang trang 2.
- **Văn bản dài nhiều trang:**
  - Tự động đánh số trang từ trang thứ 2 (`2`, `3`...) bằng chữ số Ả Rập tại chính giữa lề trên (Header). Trang 1 tuyệt đối không đánh số trang.
  - Bắt buộc kích hoạt `w:cantSplit` cho các hàng và `w:tblHeader` cho dòng tiêu đề bảng để tự động lặp lại header ở đầu trang sau.
  - Đoạn kết luận và khối chữ ký ở trang cuối bắt buộc có ít nhất 1–2 đoạn dẫn nhập (`keep_with_next = True`), không để trang cuối cô lập một mình chữ ký.
- **Bảng biểu rộng nhiều cột xoay ngang (`landscape_section`):**
  - Bảng từ 5 cột trở lên có nhiều nội dung text phải được đặt trong section khổ ngang ($297 \times 210$ mm).
  - Đảm bảo số trang kế thừa liên tục và căn đúng chính giữa lề trên của trang ngang.

---

## 3. Tiêu chuẩn Bảng biểu theo Nghị định 30
- Bảng biểu mặc định sử dụng **nền trắng (trong suốt)**, viền nét đơn đen `000000` độ dày 0.5 pt (sz="4").
- Dòng tiêu đề bảng (`headers`): Chữ in hoa/thường theo nội dung, kiểu chữ **đậm**, căn giữa ô. Tuyệt đối không tự ý tô nền màu mè nếu không có yêu cầu đặc biệt.
- Cột số thứ tự (STT) và mã số ngắn căn giữa; cột văn bản mô tả căn lề trái.

---

## 4. Dòng lưu trữ đặc thù Khoa YTCC
- Đặt tại dòng cuối cùng của khối `Nơi nhận:` bên cột trái chữ ký.
- Định dạng bắt buộc: `- Lưu: VT, <MÃ_BỘ_PHẬN>_<TÊN_VIẾT_TẮT>.`
  - Ví dụ chuyên viên Nguyễn Thị Ngọc Mai thuộc Văn phòng: `- Lưu: VT, VP_NTNM.`
  - Chuyên viên phòng Đào tạo: `- Lưu: VT, QLĐT_NTTN.`
  - Nếu chưa rõ người soạn: `- Lưu: VT, HCTC_VTTH.` hoặc để placeholder `[MÃ_LƯU]`.

---

## 5. Nguyên tắc Soạn thảo Nội dung mới
- **Tra tiền lệ để nắm văn phong:** Tra cứu các văn bản cùng loại trong SQLite/PDF để học các cấu trúc lập luận quy chuẩn của Khoa YTCC (Ví dụ: căn cứ pháp lý mở đầu, cấu trúc bảng dự trù, câu kết chuyển tiếp `Kính trình Ban Giám hiệu...` hoặc `Khoa Y tế Công cộng trân trọng thông báo...`).
- **Nội dung mới linh hoạt:** Tuyệt đối không rập khuôn hay sao chép mù quáng nội dung từ văn bản cũ sang sự việc mới. Lắp ráp đúng các khối `blocks` (`paragraph`, `heading`, `table`, `bullet`) phản ánh trung thực yêu cầu công việc mới.
