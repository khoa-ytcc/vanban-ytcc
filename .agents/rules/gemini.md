# QUY TẮC SOẠN THẢO VĂN BẢN HÀNH CHÍNH KHOA Y TẾ CÔNG CỘNG (YTCC)
# ĐẠI HỌC Y DƯỢC THÀNH PHỐ HỒ CHÍ MINH

## 1. NGUYÊN TẮC CỐT LÕI: GÓI GỌN TRONG 1 MẶT GIẤY (1-PAGE RULE)
- **Quy tắc bắt buộc:** Đối với các văn bản hành chính thông thường (Công văn trả lời/đồng ý/đề nghị, Tờ trình ngắn, Giấy giới thiệu, Thông báo ngắn): **Toàn bộ nội dung từ tiêu đề đến chữ ký và nơi nhận BẮT BUỘC phải nằm gọn trong đúng 1 trang A4 (1 mặt giấy)**.
- Tuyệt đối không để xảy ra tình trạng "mồ côi" (chữ ký hoặc nơi nhận bị đẩy tràn sang trang 2).
- Nếu nội dung hơi dài, công cụ sinh văn bản (`generate_document.ps1`) sẽ tự động tinh chỉnh cỡ chữ (11.5 - 12pt) và khoảng cách đoạn (SpaceAfter = 1 - 2pt, LineSpacing = Single) để đảm bảo chuẩn 1 trang hoàn hảo.

---

## 2. THỂ THỨC HEADER CHUẨN KHOA YTCC (THEO THỰC TẾ)

Header được bố trí trong bảng 2 cột không viền (Tổng chiều rộng: 482 pt trên khổ A4 lề trái 25mm, lề phải 15mm):

### Cột trái (Độ rộng cố định: 210 pt):
```
       ĐẠI HỌC Y DƯỢC
   THÀNH PHỐ HỒ CHÍ MINH
    KHOA Y TẾ CÔNG CỘNG
           -----
      Số: .../YTCC-HCTC (hoặc YTCC-VP)
   V/v [Trích yếu nội dung ngắn gọn]
```
- Line 1: `ĐẠI HỌC Y DƯỢC` (Size 10.5, In hoa, đứng, Center)
- Line 2: `THÀNH PHỐ HỒ CHÍ MINH` (Size 10.5, In hoa, đứng, Center)
- Line 3: `KHOA Y TẾ CÔNG CỘNG` (Size 11, In hoa, **Đậm**, Center, có gạch ngang mảnh)
- Line 4: `Số: .../YTCC-HCTC` (hoặc `/YTCC-VP`, Size 10.5, Center)
- Line 5: `V/v [Trích yếu]` (Size 10.5, *Nghiêng*, Center. **Lưu ý:** Chỉ dùng 1 chữ `V/v`, không lặp `V/v V/v`).

### Cột phải (Độ rộng cố định: 272 pt):
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
       Độc lập – Tự do – Hạnh phúc
       -------------------------
 Thành phố Hồ Chí Minh, ngày ... tháng ... năm 2026
```
- Line 1: `CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM` (Size 11, In hoa, **Đậm**, Center. Bắt buộc nằm trên 01 dòng, không bị ngắt chữ `NAM`).
- Line 2: `Độc lập – Tự do – Hạnh phúc` (Size 11.5, **Đậm**, Center, có gạch ngang mảnh).
- Line 3: `Thành phố Hồ Chí Minh, ngày ... tháng ... năm 2026` (Size 11, *Nghiêng*, Center. Bắt buộc nằm trên 01 dòng, không bị ngắt chữ `2026`).

---

## 3. THỂ THỨC KÍNH GỬI & NỘI DUNG (BODY)
- **Kính gửi:**
  - Thụt vào lề trái 3.0 cm (hoặc canh giữa khối):
    ```
    Kính gửi:
        - Ban Giám hiệu Đại học Y Dược TP.HCM;
        - Phòng Tổ chức Cán bộ.
    ```
  - Chữ `Kính gửi:` in đậm, các dòng cơ quan nhận có gạch đầu dòng `-`, giãn dòng đơn.
- **Nội dung:**
  - Font chữ: `Times New Roman` 12 pt.
  - Thụt đầu dòng: `1.0 cm`.
  - Căn đều hai lề (Justified).
  - Giãn dòng: `1.1 lines` (LineSpacing = 13.5 pt). Giãn đoạn sau: `2 - 3 pt`.
  - Lời kết: `Trân trọng kính chào./.` hoặc `Trân trọng cảm ơn./.`

---

## 4. THỂ THỨC NƠI NHẬN & CHỮ KÝ (FOOTER)
Bảng 2 cột không viền:
- **Cột trái (Nơi nhận, 210 pt):**
  - `Nơi nhận:` (Size 10, **Đậm**, *Nghiêng*)
  - `- Như trên;` (Size 9.5)
  - `- [Đơn vị phối hợp];` (Size 9.5)
  - `- BCN Khoa YTCC;` (Size 9.5)
  - `- Lưu: VT, HCTC_VTTH.` (Size 9.5 - Chuẩn ký hiệu lưu trữ của Khoa YTCC).
- **Cột phải (Người ký, 272 pt):**
  - Chức vụ: `TRƯỞNG KHOA` (Size 11.5, In hoa, **Đậm**, Center).
  - Khoảng trống ký tên: 3-4 dòng trống.
  - Họ và tên: `PGS. TS. Nguyễn Duy Phong` (Size 11.5, **Đậm**, Center).
