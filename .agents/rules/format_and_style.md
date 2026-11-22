# QUY CHUẨN THỂ THỨC & VĂN PHONG VĂN BẢN (KHOA YTCC)
> Áp dụng cho toàn bộ quá trình tự động hóa soạn thảo văn bản hành chính theo chuẩn Nghị định 30/2020/NĐ-CP và đặc thù thực tế Khoa Y tế Công cộng (Đại học Y Dược TP.HCM).

---

## 1. Cấu trúc Tiêu ngữ & Header 2 cột
- **Kích thước cột in:** Trang A4 in dọc lề 30/20mm (vùng in khả dụng 160 mm). Bảng header 2 cột: Cột 1 = 68 mm, Cột 2 = 92 mm. Không viền.
- **Cột 1 (Đơn vị ban hành & Số hiệu):**
  - **Mặc định cấp Khoa (`header_level: "ytcc"`):**
    - Dòng 1: `ĐẠI HỌC Y DƯỢC` (10 pt, đứng)
    - Dòng 2: `THÀNH PHỐ HỒ CHÍ MINH` (10 pt, đứng)
    - Dòng 3: `KHOA Y TẾ CÔNG CỘNG` (11 pt, **đậm**). Gạch dưới nét liền 1/2 độ dài dòng chữ (13 ký tự `─` cỡ 8 pt căn giữa).
  - **Ngoại lệ cấp Trường (`header_level: "ump"` — dùng cho Giấy giới thiệu):**
    - Dòng 1: `BỘ Y TẾ` (10.5 pt, đứng)
    - Dòng 2: `ĐẠI HỌC Y DƯỢC` (10.5 pt, **đậm**)
    - Dòng 3: `THÀNH PHỐ HỒ CHÍ MINH` (10.5 pt, **đậm**). Gạch dưới nét liền 1/2 độ dài (14 ký tự `─` cỡ 8 pt).
- **Mã định danh số hiệu từng loại văn bản:**
  - Công văn: `Số: .../YTCC-VP`, `Số: .../YTCC-QLĐT`, `Số: .../YTCC-HCTC` (gắn liền bộ phận tham mưu).
  - Tờ trình: `Số: .../TTr-YTCC` (luôn dùng tiền tố `TTr` trước `YTCC`).
  - Giấy giới thiệu: `Số: .../GGT-YTCC`.
  - Kế hoạch: `Số: .../KH-YTCC`.
  - Báo cáo: `Số: .../BC-YTCC`.
- **Cột 2 (Quốc hiệu, Tiêu ngữ & Ngày tháng):**
  - Dòng 1: `CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM` (10.5 pt, **đậm**, tuyệt đối không để rớt chữ `NAM`).
  - Dòng 2: `Độc lập – Tự do – Hạnh phúc` (11 pt, **đậm**).
  - Vạch kẻ dưới Tiêu ngữ: Nét liền kéo dài 100% độ dài dòng chữ (30 ký tự `─` cỡ 8 pt).
  - Ngày tháng: `Thành phố Hồ Chí Minh, ngày ... tháng ... năm ...` (11 pt, *nghiêng*, chèn số 0 nếu ngày/tháng có 1 chữ số).

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
