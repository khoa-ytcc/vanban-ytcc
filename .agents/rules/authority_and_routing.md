# QUY ĐỊNH THẨM QUYỀN KÝ & ĐỊNH TUYẾN NƠI NHẬN (KHOA YTCC)

---

## 1. Nguyên tắc Thẩm quyền Ký & Nhân sự
- **Không suy diễn nhân sự ký:** Các họ tên lãnh đạo xuất hiện trong CSDL lịch sử (như PGS. TS. Nguyễn Duy Phong, PGS. TS. Đỗ Văn Dũng, PGS. TS. Tô Gia Kiên, ThS. Nguyễn Ngọc Khôi...) chỉ là **tiền lệ tham khảo** của các giai đoạn trước.
- **Quy tắc gán người ký:**
  - AI **tuyệt đối không tự ý điền cứng** tên người ký nếu người dùng chưa chỉ định rõ ràng.
  - Khi người dùng chưa cung cấp hoặc chưa chốt người ký, bắt buộc sử dụng placeholder tường minh:
    - Chức vụ: `[CHỨC VỤ NGƯỜI KÝ]` (hoặc chức danh mặc định của loại văn bản: `TRƯỞNG KHOA`, `KT. TRƯỞNG KHOA\nPHÓ TRƯỞNG KHOA`).
    - Họ tên: `[HỌ TÊN NGƯỜI KÝ]`.
  - Trong báo cáo hoàn thành dự thảo, bắt buộc có danh mục **"Các mục cần người dùng bổ sung/xác nhận"** nêu rõ việc điền họ tên người ký.
- **Đặc thù theo thể loại văn bản:**
  - **Giấy giới thiệu (`giay_gioi_thieu`):** Bắt buộc dùng quyền hạn ký thay Hiệu trưởng:
    - Chức danh ký: `TL. HIỆU TRƯỞNG\nTRƯỞNG KHOA` (hoặc `TL. HIỆU TRƯỞNG\nKT. TRƯỞNG KHOA\nPHÓ TRƯỞNG KHOA`).
    - Header góc trái bắt buộc là cấp Trường (`header_level: "ump"`).
  - **Tờ trình trình Ban Giám hiệu (`to_trinh`):**
    - Trưởng khoa là người ký trình văn bản ở cột phải (`TRƯỞNG KHOA`).
    - Bắt buộc bật `"has_bgh_approval": true` để tạo thêm ô phê duyệt `DUYỆT BAN GIÁM HIỆU` căn giữa toàn trang ở phía dưới.
    - Họ tên lãnh đạo BGH duyệt: để placeholder `[HỌ TÊN LÃNH ĐẠO BGH]` hoặc điền tên cụ thể nếu người dùng yêu cầu.

---

## 2. Cảnh báo Định tuyến Nơi nhận & Xử lý Dữ liệu Lịch sử
> [!WARNING] CẢNH BÁO QUAN TRỌNG VỀ TRƯỜNG `Nơi nhận` TRONG CSDL LỊCH SỬ (`cv_di_history.json`)
> Trong CSDL quản lý văn bản cũ, trường `noi_nhan` ở rất nhiều bản ghi thực chất chỉ lưu **tên hoặc mã viết tắt của chuyên viên xử lý nội bộ** trong Khoa (ví dụ: `Luận`, `Quyết`, `Phương`, `Thảo`, `Tường`...), hoàn toàn **KHÔNG PHẢI** là tên cơ quan, đơn vị nhận văn bản bên ngoài.

### Quy tắc xác định nơi nhận chuẩn xác:
1. **Phân biệt Luồng Văn bản Đến & Thẩm quyền Ban hành:**
   - **Trường hợp A — Văn bản đến gửi thẳng Khoa YTCC:** Khoa là cơ quan nhận chính -> Soạn Công văn phúc đáp gửi trực tiếp Đơn vị đối tác (`Kính gửi: Tên đơn vị đối tác`).
   - **Trường hợp B — Văn bản đến gửi ĐẠI HỌC Y DƯỢC TPHCM (BGH bút phê chuyển P. TCNL đầu mối, Khoa YTCC phối hợp):** Thẩm quyền quyết định và ban hành văn bản cử viên chức hoặc phúc đáp đối ngoại thuộc về Nhà trường -> Khoa **KHÔNG** gửi văn bản cho đối tác bên ngoài mà soạn **Công văn nội bộ trình Ban Giám hiệu và Phòng Tổ chức – Nhân sự** (mã số hiệu `YTCC-HCTC`) để đề xuất Nhà trường cho phép.
2. **Đối với Công văn trình nội bộ BGH & Phòng chức năng (như TH B):**
   - `Kính gửi:`
     - `Ban Giám hiệu Đại học Y Dược Thành phố Hồ Chí Minh;`
     - `Phòng Tổ chức – Nhân sự.`
   - `Nơi nhận:` Tối giản, chỉ gồm:
     - `- Như trên;`
     - `- Lưu: VT, HCTC_<TÊN_VIẾT_TẮT>.` (ví dụ: `- Lưu: VT, HCTC_VTTH.`).
   - Câu kết thúc: Dùng văn phong trình duyệt (`Khoa Y tế công cộng kính trình Ban Giám hiệu và Phòng Tổ chức – Nhân sự xem xét, phê duyệt.\nTrân trọng./.`).
3. **Đối với Công văn phúc đáp đối tác bên ngoài (như TH A):**
   - `Kính gửi:` Đơn vị phát hành văn bản đến.
   - `Nơi nhận:` Gồm `Như trên;`, `BCN Khoa (để b/c);`, các Bộ môn/cá nhân phối hợp, `- Lưu: VT, <MÃ_PHÒNG>_<TÊN_VIẾT_TẮT>.`
4. **Đối với Tờ trình nội bộ:**
   - `Kính gửi:` Ban Giám hiệu Đại học Y Dược TP.HCM và các phòng chức năng liên quan (Tổ chức cán bộ, Kế hoạch tài chính, Quản lý khoa học...).
   - `Nơi nhận:`
     - `Như trên;`
     - Các phòng ban phối hợp;
     - `- Lưu: VT, <MÃ_PHÒNG>_<VIẾT_TẮT>.`
3. **Đối chiếu S0 khi tra cứu:**
   - Khi tra cứu SQLite FTS5 thấy bản ghi tiền lệ liên quan, nếu trường `noi_nhan` chỉ có 1-2 từ tên người, Agent phải đọc trực tiếp text layer hoặc file PDF gốc (S0) trong `knowledge_base/sample_pdfs/` để trích xuất đúng danh sách nơi nhận chuẩn hành chính.
