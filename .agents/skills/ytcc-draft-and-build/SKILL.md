---
name: ytcc-draft-and-build
description: Lắp ráp cấu trúc JSON theo doc_schema.md v2.5, soạn thảo nội dung hành chính chuẩn Khoa YTCC (hỗ trợ Inline Markdown) và tự động sinh file DOCX/PDF qua Word COM bằng lệnh ytcc.py.
---

# SKILL: Soạn thảo Dữ liệu & Sinh Văn bản (ytcc-draft-and-build v2.5)

Skill này chuyển đổi các thông tin nghiệp vụ và văn phong tiền lệ thành file dữ liệu JSON chuẩn v2.5, tự động chạy qua Validator & Linter, sau đó gọi Engine tạo tài liệu Word và xuất bản PDF cố định bằng **01 lệnh duy nhất**.

---

## 1. Đầu vào (Inputs)
- Dữ liệu bóc tách từ yêu cầu mới hoặc văn bản đến (kết quả từ `ytcc-intake-and-search`).
- Mẫu câu, lập luận học từ văn bản tiền lệ hoặc bản mẫu vàng `knowledge_base/golden_jsons/`.
- Thư mục vụ việc: `drafts/YYYY-MM/<YYYYMMDD_case>/`.

---

## 2. Quy trình Thực hiện (Steps)

### Bước 1: Soạn thảo JSON Chuẩn v2.5
1. **Thiết lập loại văn bản & cờ tối ưu:**
   - `cong_van`: Trích yếu ở cột 1 dưới số hiệu.
   - `to_trinh`: Tiêu đề `TỜ TRÌNH`, mã loại bắt buộc chứa `TTr` (ví dụ `TTr-YTCC`), bật `"has_bgh_approval": true` nếu trình BGH.
   - `giay_gioi_thieu`: Bắt buộc `"header_level": "ump"` và mã loại `GGT-YTCC`.
   - `ke_hoach`: Mã loại `KH-YTCC`.
   - `bao_cao`: Mã loại `BC-YTCC`.
   - Bật `"target_one_page": true` nếu văn bản ngắn (1 trang).
2. **Sử dụng cú pháp linh hoạt v2.5:**
   - Dùng bí danh: `p` (thay paragraph), `h1`, `h2`, `h3` (thay heading), `quote` (trích dẫn lùi lề nghiêng).
   - Dùng cú pháp **Inline Markdown**: `***đậm nghiêng***`, `**in đậm**`, `*in nghiêng*` trong đoạn văn, gạch đầu dòng, ô bảng biểu.
3. **Quy tắc Placeholder thông tin chưa rõ:**
   - `so_hieu`: để `"...."` (Ví dụ: `Số: ..../YTCC-VP`).
   - `signer_name`: để `"[HỌ TÊN NGƯỜI KÝ]"`.
   - Căn cứ nội bộ: trích từ `citations_bank.md` hoặc để `"[CHỜ NGƯỜI DÙNG XÁC NHẬN SỐ/NGÀY]"`.
4. **Lưu file JSON:** Lưu tại `drafts/YYYY-MM/<YYYYMMDD_case>/v1.json` (hoặc `v2.json`, `final.json`).

### Bước 2: Sinh DOCX & Xuất PDF bằng 1 Lệnh Duy Nhất (`ytcc.py build`)
Chạy lệnh bằng môi trường ảo Python:
```powershell
d:\TH\vanban-ytcc\.venv\Scripts\python.exe d:\TH\vanban-ytcc\tools\ytcc.py build "drafts/YYYY-MM/<YYYYMMDD_case>/v1.json" --pdf
```
- Lệnh trên tự động thực hiện tuần tự:
  1. Kiểm tra cấu trúc Schema (`validate_schema`).
  2. Kiểm tra tính toán bảng, lịch thực tế và thể thức (`lint_doc`).
  3. Dựng file Word `.docx` tương ứng.
  4. Mở Word COM xuất file `.pdf`.
  5. Tự động chạy `inspect_pdf` kiểm tra kích thước và telemetry lố trang (`OVERFLOW_PAGE_2`).
- Nếu cần nghiệm thu gắt gao không còn placeholder, thêm cờ `--strict-final`.
- Nếu cần xuất hàng loạt nhiều văn bản cùng lúc, dùng lệnh `ytcc.py batch <batch.json>`.

---

## 3. Đầu ra (Outputs)
1. File dữ liệu JSON: `drafts/YYYY-MM/<YYYYMMDD_case>/v1.json`
2. File Word có thể chỉnh sửa: `drafts/YYYY-MM/<YYYYMMDD_case>/v1.docx`
3. File PDF xuất bản: `drafts/YYYY-MM/<YYYYMMDD_case>/v1.pdf`
4. **Bảng checklist placeholder:** Liệt kê rõ các vị trí cần chuyên viên/lãnh đạo điền trước khi ký chính thức.
