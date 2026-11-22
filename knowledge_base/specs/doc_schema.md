# ĐẶC TẢ CẤU TRÚC DỮ LIỆU ĐẦU VÀO (DOC SCHEMA V2.0)
**Mã tài liệu:** `SCHEMA-DOCX-V2.0`  
**Công cụ áp dụng:** `tools/build_doc.py`  
**Mục đích:** Cung cấp định dạng JSON chuẩn hóa để các Agent sinh văn bản hành chính Khoa Y tế Công cộng (ĐHYD TP.HCM) chuyển đổi tự động sang file Word `.docx` và `.pdf`.

---

## 1. CẤU TRÚC JSON TỔNG THỂ

```json
{
  "doc_type": "cong_van | to_trinh | giay_gioi_thieu | ke_hoach | bao_cao | chung",
  "target_one_page": false,
  "title": "Tiêu đề tùy chọn nếu muốn override (in hoa)",
  "has_bgh_approval": false,
  "bgh_approver_title": "DUYỆT BAN GIÁM HIỆU",
  "bgh_approver_name": "PGS. TS. Trần Diệp Tuấn",
  "header": {
    "header_level": "ytcc | ump",
    "organ_line1": "ĐẠI HỌC Y DƯỢC",
    "organ_line2": "THÀNH PHỐ HỒ CHÍ MINH",
    "organ_line3": "KHOA Y TẾ CÔNG CỘNG",
    "so_hieu": "123",
    "ma_loai": "YTCC-VP | TTr-YTCC | GGT-YTCC | KH-YTCC | BC-YTCC",
    "dia_danh": "Thành phố Hồ Chí Minh",
    "ngay": "22",
    "thang": "11",
    "nam": "2026",
    "trich_yeu": "Về việc cử viên chức tham gia công tác chuyên môn"
  },
  "blocks": [
    { "type": "kinh_gui", "items": ["Ban Giám hiệu...", "Phòng QLĐT..."] },
    { "type": "paragraph", "text": "Nội dung đoạn văn...", "indent": true },
    { "type": "heading", "level": 1, "text": "I. MỤC ĐÍCH, YÊU CẦU" },
    { "type": "bullet", "text": "Nội dung gạch đầu dòng", "bullet_char": "- " },
    { "type": "table", "headers": ["STT", "Nội dung"], "rows": [["1", "Chi tiết"]] }
  ],
  "sign_block": {
    "signer_role": "TRƯỞNG KHOA",
    "signer_name": "PGS. TS. Nguyễn Duy Phong",
    "recipients": [
      "- Như trên;",
      "- Phòng Đào tạo Sau đại học;"
    ],
    "dept_code": "QLĐT",
    "creator_initials": "NTTN",
    "custom_luu": "- Lưu: VT, QLĐT_NTTN."
  }
}
```

---

## 2. QUY CÁCH TỪNG TRƯỜNG DỮ LIỆU

### 2.1. Nhóm thông tin phân loại (`doc_type`)
- `cong_van`: Công văn hành chính thông thường. Trích yếu được đặt ở cột 1 dưới số hiệu dạng `V/v <trích yếu>`. Không có tiêu đề lớn ở giữa.
- `to_trinh`: Tờ trình xin chủ trương, kinh phí, nhân sự. Tiêu đề in hoa `TỜ TRÌNH`, trích yếu in đậm phía dưới. Hỗ trợ cờ `"has_bgh_approval": true` để thêm ô phê duyệt của BGH.
- `giay_gioi_thieu`: Giấy giới thiệu sinh viên/học viên. Tự động chuyển header sang cấp trường (`BỘ Y TẾ / ĐHYD TP.HCM`), chức danh ký mặc định là `TL. HIỆU TRƯỞNG / TRƯỞNG KHOA`.
- `ke_hoach`: Kế hoạch công tác/hoạt động. Tiêu đề `KẾ HOẠCH`.
- `bao_cao`: Báo cáo định kỳ/chuyên đề. Tiêu đề `BÁO CÁO`.
- `chung`: Định dạng văn bản hành chính tổng quát khác.

### 2.2. Cờ tối ưu hóa trang (`target_one_page`)
- `true`: Tự động kích hoạt cơ chế co giãn dòng (1.05 lines), lề trang gọn (top/bottom 18mm, right 18mm), giảm khoảng cách đoạn để toàn bộ văn bản ngắn nằm gọn vừa khít trong **1 trang duy nhất**, triệt tiêu nguy cơ rơi khối chữ ký sang trang 2.
- `false`: Giữ giãn dòng và khoảng cách đoạn chuẩn cho văn bản nhiều trang.

### 2.3. Khối Tiêu ngữ (`header`)
- `header_level`:
  - `"ytcc"` (Mặc định): Cột trái hiển thị 3 dòng: `ĐẠI HỌC Y DƯỢC` / `THÀNH PHỐ HỒ CHÍ MINH` / `KHOA Y TẾ CÔNG CỘNG` (đậm).
  - `"ump"`: Cột trái hiển thị `BỘ Y TẾ` / `ĐẠI HỌC Y DƯỢC` / `THÀNH PHỐ HỒ CHÍ MINH` (chuyên dùng cho Giấy giới thiệu hoặc văn bản ủy quyền).
- `so_hieu` & `ma_loai`: Nếu `so_hieu` chứa dấu `/` (ví dụ `"872/YTCC-QLĐT"`), engine sẽ dùng trực tiếp; nếu chỉ chứa số, engine sẽ tự ghép `so_hieu/ma_loai`.
- `trich_yeu`: Engine tự động loại bỏ các tiền tố trùng lặp (`V/v`, `Về việc`) nếu người dùng vô tình nhập vào.

---

## 3. CÁC KIỂU NỘI DUNG (BLOCKS) VÀ ĐỊNH DẠNG INLINE MARKDOWN

### 3.1. Định dạng Inline Markdown hỗ trợ
Toàn bộ nội dung chuỗi trong `paragraph` (`p`), `bullet`, `quote`, `heading` (`h1`-`h3`) và các ô trong `table` đều hỗ trợ cú pháp định dạng nội dòng (Inline Markdown):
- `***nội dung***`: In đậm và in nghiêng (`bold=True`, `italic=True`).
- `**nội dung**`: In đậm (`bold=True`).
- `*nội dung*`: In nghiêng (`italic=True`).
- Ký tự `*` được xử lý triệt để qua parser, bảo đảm không bị sót ký tự thừa trong Word/PDF.

### 3.2. Bảng quy chuẩn các loại Block

| Loại Block (`type`) | Bí danh (Alias) | Các tham số | Mô tả & Quy chuẩn |
|:---|:---|:---|:---|
| `paragraph` | `p` | `text`, `prefix_bold`, `bold`, `italic`, `align`, `indent` | Đoạn văn thân bài (căn đều, thụt đầu dòng 1.27 cm). |
| `heading` | `h1`, `h2`, `h3` | `level` (1, 2, 3), `text` | Tiêu đề mục. Tự động bật `keep_with_next = True` chống rớt mục. |
| `quote` | `trich_dan` | `text`, `align` | Đoạn trích dẫn lùi lề 2 bên (trái 15mm, phải 10mm), chữ in nghiêng. |
| `bullet` | - | `text`, `bullet_char` (mặc định `"- "`) | Danh sách gạch đầu dòng thụt lề treo. |
| `key_value` | - | `items`: mảng gồm `{key, value, key_bold, value_bold, value_italic}` | Dòng thông tin định dạng Học viên: ..., Ngành: ... |
| `table` | - | `headers`, `rows`, `col_widths` (mảng mm), `header_shading` | Bảng biểu có viền. Tự động bật **Repeat Header Row** (`w:tblHeader`) và chống tách dòng (`w:cantSplit`). |
| `kinh_gui` | - | `items` (mảng) hoặc `text` (chuỗi) | Nơi gửi văn bản chính. Tự động thụt lề chuẩn. |
| `landscape_section`| - | `blocks`: mảng các block bên trong | **Ngắt Section chuyển trang A4 ngang (Landscape)** cho bảng rộng, sau đó tự quay lại dọc nếu cần. |

---

## 4. KHỐI CHỮ KÝ VÀ NƠI NHẬN (`sign_block`)

- `signer_role`: Chức vụ ký (Ví dụ: `"TRƯỞNG KHOA"`, `"KT. TRƯỞNG KHOA\nPHÓ TRƯỞNG KHOA"`, `"TL. HIỆU TRƯỞNG\nTRƯỞNG KHOA"`).
- `signer_name`: Họ và tên người ký (Ví dụ: `"PGS. TS. Nguyễn Duy Phong"` hoặc để trống `"[HỌ TÊN NGƯỜI KÝ]"`).
- `recipients`: Danh sách nơi nhận bên cột trái.
- `dept_code` & `creator_initials`: Mã bộ phận và tên viết tắt chuyên viên soạn thảo để sinh dòng lưu tự động: `- Lưu: VT, <dept_code>_<creator_initials>.` (Ví dụ: `- Lưu: VT, QLĐT_NTTN.`).
- `has_bgh_approval`: Bật `true` để tạo thêm ô chữ ký phê duyệt `DUYỆT BAN GIÁM HIỆU` ở dưới.
