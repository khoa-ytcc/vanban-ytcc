# BẢNG ĐẶC TẢ QUY CHUẨN THỂ THỨC VĂN BẢN KHOA Y TẾ CÔNG CỘNG (S0)
**Mã tài liệu:** `SPECS-YTCC-V2.0`  
**Cơ sở dữ liệu:** Khảo sát thực chứng 15 file PDF mẫu đại diện từ kho lưu trữ `knowledge_base/sample_pdfs/` (S0) kết hợp Nghị định 30/2020/NĐ-CP.  
**Ngày lập:** 22/11/2026.

---

## 1. DANH MỤC 15 FILE PDF ĐẠI DIỆN ĐƯỢC KHẢO SÁT
Toàn bộ quy chuẩn dưới đây được trích xuất trực tiếp từ 15 văn bản thực tế, chia đều 5 loại văn bản cốt lõi với đầy đủ các dạng độ dài:

| STT | Loại văn bản | Tên file PDF mẫu | Số trang | Dạng dữ liệu | Trích yếu tóm tắt |
|:---:|:---|:---|:---:|:---:|:---|
| 01 | **Công văn** | `Cong_van_SoDi_872.pdf` | 1 | TEXT | Báo cáo tình hình học tập học viên tại ĐHYD TP.HCM |
| 02 | **Công văn** | `Cong_van_SoDi_920.pdf` | 2 | TEXT | Cử giảng viên tham gia công tác chuyên môn, hỗ trợ đào tạo |
| 03 | **Công văn** | `Cong_van_SoDi_843.pdf` | 4 | TEXT | Đề nghị thay đổi tên đề tài, giảng viên hướng dẫn khóa luận |
| 04 | **Tờ trình** | `To_trinh_SoDi_927.pdf` | 1 | TEXT | Xin phép cho viên chức tham dự họp Tổ soạn thảo |
| 05 | **Tờ trình** | `To_trinh_SoDi_857.pdf` | 2 | TEXT | Phê duyệt kế hoạch định hướng nghiên cứu và đào tạo Bộ môn |
| 06 | **Tờ trình** | `To_trinh_SoDi_913.pdf` | 3 | TEXT | Xin kinh phí sửa chữa, bảo trì thiết bị phòng máy tính |
| 07 | **Giấy giới thiệu** | `Giay_gioi_thieu_SoDi_932.pdf` | 1 | SCAN | Giới thiệu học viên chuyên khoa 2 thu thập số liệu nghiên cứu |
| 08 | **Giấy giới thiệu** | `Giay_gioi_thieu_SoDi_907.pdf` | 2 | SCAN | Tập hợp giấy giới thiệu học viên cao học đi thực hành |
| 09 | **Giấy giới thiệu** | `Giay_gioi_thieu_SoDi_931.pdf` | 3 | SCAN | Giới thiệu học viên ThS YTCC thu thập số liệu luận văn |
| 10 | **Kế hoạch** | `CVDi_2026_SoDi_161_Kế hoạch đào tạo.viên chức, người lao động năm học 2025-2026.pdf` | 1 | TEXT | Kế hoạch đào tạo viên chức, người lao động năm học |
| 11 | **Kế hoạch** | `Ke_hoach_SoDi_881.pdf` | 2 | TEXT | Kế hoạch tổ chức tập huấn chuyên môn Bộ môn GDSC-TLYH |
| 12 | **Kế hoạch** | `Ke_hoach_SoDi_754.pdf` | 5 | TEXT | Kế hoạch tổ chức Hội nghị viên chức, người lao động |
| 13 | **Báo cáo** | `CVDi_2026_SoDi_345_Báo cáo cơ cấu tổ chức của Khoa Y tế Công cộng.pdf` | 1 | TEXT | Báo cáo cơ cấu tổ chức, nhân sự Khoa YTCC |
| 14 | **Báo cáo** | `Bao_cao_SoDi_937.pdf` | 2 | SCAN | Báo cáo tình hình triển khai kỳ kiểm thử cấu trúc đề thi |
| 15 | **Báo cáo** | `Bao_cao_SoDi_816.pdf` | 4 | TEXT | Báo cáo chấp hành pháp luật về vệ sinh an toàn lao động |

---

## 2. QUY CHUẨN KHỐI TIÊU NGỮ (HEADER)

### 2.1. Tên cơ quan, tổ chức ban hành (Cột bên trái)
- **Cấu trúc dòng tiêu chuẩn (Áp dụng cho Công văn, Tờ trình, Kế hoạch, Báo cáo):**
  - **Dòng 1:** `ĐẠI HỌC Y DƯỢC` (Chữ in hoa, đứng, cỡ chữ 10 – 10.5 pt, font Times New Roman).
  - **Dòng 2:** `THÀNH PHỐ HỒ CHÍ MINH` (Chữ in hoa, đứng, cỡ chữ 10 – 10.5 pt). *Lưu ý:* Bắt buộc tách thành dòng riêng, không viết gộp `ĐẠI HỌC Y DƯỢC TP.HCM`.
  - **Dòng 3:** `KHOA Y TẾ CÔNG CỘNG` (Chữ in hoa, kiểu chữ **đậm**, cỡ chữ 11 pt). Phía dưới có đường gạch ngang nét liền, thanh mảnh, có chiều dài bằng 100% độ dài dòng chữ.
  - *Dẫn chứng thực tế:*
    - `Cong_van_SoDi_872.pdf` (Trang 1): Khối cơ quan tọa độ top `y=50.3pt`, gồm 3 dòng đúng chuẩn.
    - `To_trinh_SoDi_927.pdf` (Trang 1): Khối cơ quan tọa độ `x=76.0pt, y=57.3pt`.
    - `Bao_cao_SoDi_816.pdf` (Trang 1): 3 dòng cơ quan rõ ràng ở góc trên bên trái.

- **Ngoại lệ đặc thù: Giấy giới thiệu (GGT):**
  - Cơ quan ban hành cấp trên là Bộ Y tế, ủy quyền cấp trường:
    - **Dòng 1:** `BỘ Y TẾ` (In hoa, đứng, cỡ 11 – 12 pt).
    - **Dòng 2:** `ĐẠI HỌC Y DƯỢC` (In hoa, **đậm**, cỡ 11 – 12 pt).
    - **Dòng 3:** `THÀNH PHỐ HỒ CHÍ MINH` (In hoa, **đậm**, cỡ 11 – 12 pt).
    - Không để tên `KHOA Y TẾ CÔNG CỘNG` ở header mà thể hiện thẩm quyền ký thừa lệnh tại khối ký chân trang.
  - *Dẫn chứng thực tế:* `Giay_gioi_thieu_SoDi_932.pdf` (Trang 1), `Giay_gioi_thieu_SoDi_907.pdf` (Trang 1, 2).

### 2.2. Quốc hiệu và Tiêu ngữ (Cột bên phải)
- **Dòng 1 (Quốc hiệu):** `CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM` (Chữ in hoa, **đậm**, cỡ chữ 10 – 10.5 pt). Độ rộng cột phải thiết kế đủ rộng (250 – 260 pt) để từ `NAM` không bị rớt xuống dòng thứ 2.
- **Dòng 2 (Tiêu ngữ):** `Độc lập – Tự do – Hạnh phúc` (Chữ in thường, **đậm**, cỡ chữ 11 pt). Ký tự nối giữa các từ là dấu gạch ngang dài (`–`, en-dash) có dấu cách hai bên. Phía dưới có đường kẻ ngang nét liền đặt chính giữa, chiều dài bằng độ dài dòng chữ.
- *Dẫn chứng thực tế:* `Cong_van_SoDi_872.pdf` (Trang 1), `Ke_hoach_SoDi_754.pdf` (Trang 1).

### 2.3. Địa danh và Ngày tháng ban hành
- Đặt dưới Quốc hiệu & Tiêu ngữ, căn lề giữa hoặc căn phải:
  - Định dạng: `Thành phố Hồ Chí Minh, ngày ... tháng ... năm 2026` (Chữ in thường, kiểu chữ *nghiêng*, cỡ chữ 11 – 12 pt).
  - Đối với ngày từ 1 đến 9 và tháng 1, 2: thực tế thường ghi chèn thêm số 0 hoặc viết tay (`ngày 03 tháng 11 năm 2026`).
  - *Dẫn chứng thực tế:* `To_trinh_SoDi_913.pdf` (Trang 1: `ngày 03 tháng 11 năm 2026`), `Cong_van_SoDi_920.pdf` (Trang 2: `ngày 05 tháng 11 năm 2026`).

### 2.4. Ký hiệu số văn bản theo từng thể loại
Thực tế văn bản Khoa YTCC phân định rõ mã định danh phụ trách:
- **Công văn:** `Số: .../YTCC-VP`, `Số: .../YTCC-QLĐT`, `Số: .../YTCC-HCTC` (gắn liền bộ phận tham mưu).
  - *Dẫn chứng:* `Cong_van_SoDi_872.pdf` mang số `872/YTCC-QLĐT`; `Cong_van_SoDi_920.pdf` mang số `920/YTCC-HCTC`.
- **Tờ trình:** `Số: .../TTr-YTCC` (luôn dùng mã loại `TTr` đứng trước `YTCC`).
  - *Dẫn chứng:* `To_trinh_SoDi_927.pdf` ghi `Số: 927/TTr-YTCC`; `To_trinh_SoDi_857.pdf` ghi `Số: 857/TTr-YTCC`.
- **Giấy giới thiệu:** `Số: .../GGT-YTCC`.
  - *Dẫn chứng:* `Giay_gioi_thieu_SoDi_932.pdf` ghi `Số: 932/GGT-YTCC`.
- **Kế hoạch:** `Số: .../KH-YTCC`.
  - *Dẫn chứng:* `Ke_hoach_SoDi_881.pdf` ghi `Số: 881/KH-YTCC`; `Ke_hoach_SoDi_754.pdf` ghi `Số: 754/KH-YTCC`.
- **Báo cáo:** `Số: .../BC-YTCC`.
  - *Dẫn chứng:* `Bao_cao_SoDi_816.pdf` ghi `Số: 816/BC-YTCC`; `Bao_cao_SoDi_937.pdf` ghi `Số: 937/BC-YTCC`.

---

## 3. THÂN VĂN BẢN VÀ TRÍCH YẾU

### 3.1. Thể thức Trích yếu nội dung
- **Dạng Công văn (Không có tiêu đề lớn ở giữa):**
  - Trích yếu đặt ngay dưới Số hiệu văn bản ở cột 1 bên trái.
  - Cú pháp: `V/v <trích yếu nội dung văn bản>` (Cỡ chữ 11 – 12 pt, chữ in thường, đứng hoặc hơi nghiêng).
  - *Dẫn chứng:* `Cong_van_SoDi_872.pdf` (Trang 1: `V/v báo cáo tình hình học tập học viên`); `Cong_van_SoDi_920.pdf` (Trang 1: `V/v cử giảng viên tham gia công tác chuyên môn...`).
- **Dạng Tờ trình / Kế hoạch / Báo cáo / Giấy giới thiệu (Có tiêu đề chính ở giữa):**
  - Tên loại văn bản đặt chính giữa trang, in hoa, **đậm**, cỡ 14 – 15 pt: `TỜ TRÌNH`, `KẾ HOẠCH`, `BÁO CÁO`, `GIẤY GIỚI THIỆU`.
  - Dòng trích yếu đặt ngay dưới tên loại, in thường, **đậm**, cỡ 12 – 13 pt: `Về việc xin phép cho viên chức tham dự họp...` hoặc ghi thẳng chủ đề `Báo cáo cơ cấu tổ chức của Khoa...`.
  - *Dẫn chứng:* `To_trinh_SoDi_927.pdf` (Trang 1: `TỜ TRÌNH / Về việc xin phép...`), `Bao_cao_SoDi_816.pdf` (Trang 1: `BÁO CÁO / Về việc chấp hành pháp luật...`).

### 3.2. Cấu trúc Kính gửi
- Đặt dưới dòng ngày tháng (đối với Công văn) hoặc dưới tiêu đề trích yếu (đối với Tờ trình/Báo cáo).
- Chữ `Kính gửi:` in **đậm**, theo sau là các cơ quan/đơn vị nhận chính.
- *Dẫn chứng:* `To_trinh_SoDi_927.pdf` (Trang 1: `Kính gửi: Ban Giám hiệu Đại học Y Dược Thành phố Hồ Chí Minh.`); `Bao_cao_SoDi_937.pdf` (Trang 1).

### 3.3. Quy cách đánh mục và phân cấp nội dung
- Văn bản hành chính nhiều trang phân cấp theo trật tự:
  - Cấp 1: Số La Mã (`I.`, `II.`, `III.`) – In hoa, **đậm**.
  - Cấp 2: Số Ả Rập (`1.`, `2.`, `3.`) – Chữ thường, **đậm**.
  - Cấp 3: Chữ cái thường (`a)`, `b)`, `c)`) hoặc gạch đầu dòng (`−`, `-`).
- *Dẫn chứng thực tế:* `Ke_hoach_SoDi_754.pdf` (Trang 1, 2) và `Bao_cao_SoDi_816.pdf` (Trang 1, 2, 3, 4).

---

## 4. BỐ CỤC NHIỀU TRANG, BẢNG BIỂU VÀ SỐ TRANG

### 4.1. Đánh số trang
- **Thực tế mẫu S0:**
  - Văn bản 1 trang: Tuyệt đối không đánh số trang (`Cong_van_SoDi_872.pdf`, `To_trinh_SoDi_927.pdf`, `Giay_gioi_thieu_SoDi_932.pdf`).
  - Văn bản nhiều trang: Trong các file Word xuất scan cũ, nhiều văn bản bị thiếu số trang do người soạn thảo không chèn trường Page. Một số văn bản có đánh số `1`, `2` tại lề trên (`Ke_hoach_SoDi_881.pdf`).
- **Chuẩn hóa áp dụng v2.0 (Khắc phục hạn chế lịch sử theo NĐ 30):**
  - Đánh số trang tự động từ trang thứ 2 trở đi bằng chữ số Ả Rập (`2`, `3`...).
  - Vị trí: Đặt tại chính giữa lề trên của trang (Header), cỡ chữ 13 – 14 pt, đứng. Trang đầu tiên không hiển thị số trang.

### 4.2. Bảng biểu và Phụ lục (Table Layout)
- **Đặc thù chuyển khổ giấy (Portrait sang Landscape):**
  - Đối với văn bản có danh sách nhân sự hoặc thời khóa biểu chi tiết, Khoa chuyển linh hoạt trang bảng biểu sang **khổ ngang (Landscape)** để chứa đủ các cột thông tin mà không bị co ép chữ.
  - *Dẫn chứng thực tế:* `Cong_van_SoDi_920.pdf` (Trang 1 khổ đứng `w=612, h=792 pt`; Trang 2 khổ ngang `w=792, h=612 pt` thể hiện bảng phân công giảng viên).
- **Lặp lại hàng tiêu đề (Repeat Header Row):**
  - Bảng biểu kéo dài qua nhiều trang (như phân công công việc Hội nghị) phải tự động lặp lại hàng tiêu đề trên các trang tiếp theo để người đọc dễ theo dõi.
  - *Dẫn chứng thực tế:* `Ke_hoach_SoDi_754.pdf` (Trang 2, 3, 5).

### 4.3. Nguyên tắc chống trang mồ côi (Orphan Prevention)
- Trang cuối cùng của văn bản nhiều trang bắt buộc phải có ít nhất 1–2 đoạn nội dung dẫn nhập (ví dụ: các điều khoản gửi kèm, câu kết luận `Kính trình Ban Giám hiệu...` hoặc `Trân trọng./.`) đi cùng khối chữ ký.
- Tuyệt đối không để trang cuối chỉ xuất hiện đơn độc một mình khối chữ ký và nơi nhận.
- *Dẫn chứng thực tế:* `Bao_cao_SoDi_937.pdf` (Trang 2 có phần liệt kê 3 tài liệu đính kèm trước chữ ký); `To_trinh_SoDi_857.pdf` (Trang 2 có 3 đoạn kiến nghị trước chữ ký).

---

## 5. KHỐI CHỮ KÝ VÀ NƠI NHẬN

Khối kết thúc văn bản luôn được bố trí thành **2 cột song song** (sử dụng cấu trúc bảng 1 hàng 2 cột, không viền):

```
+------------------------------------------+------------------------------------------+
| Nơi nhận:                                | THẨM QUYỀN / CHỨC VỤ KÝ                  |
| - Như trên;                              | (Khoảng trống 35-45pt để ký & đóng dấu)  |
| - Phòng/Bộ phận liên quan;               |                                          |
| - Lưu: VT, <MÃ_ĐƠN_VỊ>_<VIẾT_TẮT_TÊN>.   | HỌ VÀ TÊN NGƯỜI KÝ                       |
+------------------------------------------+------------------------------------------+
```

### 5.1. Cột bên trái: Nơi nhận & Ký hiệu lưu hồ sơ
- Tiêu đề: `Nơi nhận:` (In thường, **nghiêng đậm**, cỡ 12 pt).
- Các dòng địa chỉ nhận: `- Như trên;`, `- Các đơn vị phối hợp;` (cỡ 10 – 11 pt).
- **Quy tắc ký hiệu lưu đặc thù Khoa YTCC:**
  - Luôn kết thúc bằng: `- Lưu: VT, <MÃ_PHÒNG>_<CHỮ_CÁI_TÊN_CHUYÊN_VIÊN>.`
  - *Dẫn chứng thực tế:*
    - `Cong_van_SoDi_872.pdf`: `- Lưu: VT, QLĐT_NTTN.` (Chuyên viên Nguyễn Thị Thu Nga - QLĐT).
    - `Cong_van_SoDi_920.pdf`: `- Lưu: VT, HCTC_VTTH.` (Chuyên viên Vũ Thị Thu Hương - HCTC).
    - `Bao_cao_SoDi_937.pdf`: `- Lưu: VT, ĐBCL&KT_NTYN.` (Chuyên viên Nguyễn Thị Yến Nhi - ĐBCL).
    - `Bao_cao_SoDi_816.pdf`: `- Lưu: VT, HCTC_NTHM.` (Chuyên viên Nguyễn Thị Hồng Mơ - HCTC).

### 5.2. Cột bên phải: Thẩm quyền ký & Họ tên
- **Thẩm quyền ký văn bản của Khoa:**
  - Trưởng khoa ký chính thức: `TRƯỞNG KHOA` (In hoa, **đậm**, cỡ 13 – 14 pt).
  - Phó Trưởng khoa ký thay: `KT. TRƯỞNG KHOA / PHÓ TRƯỞNG KHOA`.
  - Ký thừa lệnh Hiệu trưởng (đối với Giấy giới thiệu): `TL. HIỆU TRƯỞNG / TRƯỞNG KHOA`.
  - Duyệt của cấp trên (đối với Tờ trình gửi Trường): Có thêm ô phê duyệt `DUYỆT BAN GIÁM HIỆU` (Dẫn chứng: `To_trinh_SoDi_927.pdf`, Trang 1 có chữ ký PGS. TS. Trần Diệp Tuấn).
- **Quy tắc về Họ và Tên:**
  - In chữ thường đậm hoặc hoa đậm, căn giữa theo chức vụ ký (ví dụ: `Nguyễn Duy Phong`).
  - **LƯU Ý QUAN TRỌNG:** Tên các cá nhân xuất hiện trong văn bản mẫu (PGS. TS. Nguyễn Duy Phong, PGS. TS. Đỗ Văn Dũng, PGS. TS. Tô Gia Kiên, ThS. Nguyễn Ngọc Khôi...) chỉ là **tiền lệ lịch sử** trong kho dữ liệu cũ. Khi tạo văn bản mới, AI tuyệt đối không tự ý gán mặc định mà phải điền theo đúng nhân sự và thẩm quyền được người dùng chỉ định.

---

## 6. SO SÁNH THỰC TẾ KHOA YTCC VÀ NGHỊ ĐỊNH 30/2020/NĐ-CP

| Tiêu chí | Nghị định 30/2020/NĐ-CP | Thực tế Khoa YTCC (S0) | Hướng xử lý chuẩn hóa v2.0 |
|:---|:---|:---|:---|
| **Tên cơ quan** | Gồm cơ quan chủ quản và tên cơ quan ban hành | 3 dòng: `ĐẠI HỌC Y DƯỢC` / `THÀNH PHỐ HỒ CHÍ MINH` / `KHOA Y TẾ CÔNG CỘNG` | Tuân thủ tuyệt đối cấu trúc 3 dòng thực tế của ĐHYD TP.HCM |
| **Ký hiệu số** | `.../<Tên loại>-<Cơ quan>` (Ví dụ: `12/TTr-YTCC`) | Công văn có thêm mã bộ phận tham mưu (`/YTCC-QLĐT`, `/YTCC-HCTC`) | Giữ nguyên quy ước mã bộ phận để phục vụ phân loại công việc |
| **Ký hiệu lưu** | Chỉ ghi `- Lưu: VT, <đơn vị>.` | Ghi rõ tên viết tắt chuyên viên: `- Lưu: VT, QLĐT_NTTN.` | Tự động hóa sinh mã chuyên viên theo người soạn thảo |
| **Đánh số trang** | Bắt buộc đánh số từ trang 2 ở giữa mép trên | Nhiều file PDF cũ không có số trang | **Chuẩn hóa bắt buộc:** Tự động chèn số trang từ trang 2 ở Header |
| **Định dạng bảng** | Thường giữ chung khổ giấy portrait | Chuyển trang sang Landscape nếu bảng có từ 5-6 cột trở lên | Hỗ trợ Section break chuyển khổ ngang thích ứng tự động |

---
*Tài liệu này là chuẩn mực căn cứ kỹ thuật bắt buộc để xây dựng 5 Word Templates và script Word COM tại Phase 2.*
