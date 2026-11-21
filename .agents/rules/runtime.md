# MÔI TRƯỜNG THỰC THI YTCC

## Phạm vi cấu hình

Environment của dự án gồm `AGENTS.md`, `GEMINI.md`, `PLAN.md` và `.agents/`. Planner duy trì các file này. Không thay cấu hình AI toàn máy, cài thêm plugin hay đổi model của chat chỉ để thực hiện một phase.

`AGENTS.md` là điểm vào chính. `GEMINI.md` là điểm vào đọc thủ công/tương thích cho phiên dùng hướng dẫn Gemini. Cả hai cùng dẫn tới một bộ rules; không duy trì hai bộ quy tắc độc lập.

## Đường dẫn và ngày tháng

- Repo: `D:\TH\vanban-ytcc`; suy ra repo root từ vị trí script khi worker sửa công cụ.
- Hệ thống cũ: `D:\Hương\QUANLYVANBAN`, chỉ đọc trong audit.
- Múi giờ nghiệp vụ: `Asia/Saigon`; lấy ngày văn bản từ người dùng hoặc nguồn. Ngày tạo file và ngày ban hành là hai trường khác nhau.
- Output thật: `drafts/YYYY-MM/`; bằng chứng kiểm tra: `audit/artifacts/<phase>/`; báo cáo: `audit/`.
- Không coi tên PDF, số đi đơn lẻ hoặc tên output là khóa định danh hồ sơ duy nhất.

## Năng lực hiện tại, chưa nghiệm thu

Kiểm tra mã nguồn ngày 14/11/2026 cho thấy:

| Thành phần | Điều đã thấy | Giới hạn |
|---|---|---|
| `tools/generate_document.ps1` | Nhận 5 loại: To_trinh, Cong_van, Giay_gioi_thieu, Ke_hoach, Bao_cao | Có logic thu nhỏ khi quá một trang; chưa có tham số layout; mapping placeholder cần audit |
| `tools/create_templates.ps1` | Tạo 5 DOCX | Script và DOCX hiện có đều là sản phẩm AI cần kiểm chứng |
| `tools/export_pdf.ps1` | Có gọi Word COM xuất PDF | Chưa xác nhận dọn tài nguyên, timeout, đường dẫn và báo lỗi đạt yêu cầu |
| `tools/search_history.ps1` | Tìm trong JSON local | Kết quả là dữ liệu dẫn xuất, không xác minh được bằng việc tìm thấy |

Không tự gọi lệnh với tham số dự kiến như `-Layout` hoặc chọn file `_MultiPage.docx` khi chưa tồn tại. Xem `param(...)`, template thực tế và báo cáo phase đã nghiệm thu trước khi dùng. Không map ép Quyết định/Giấy mời/Thông báo sang một trong năm template chỉ để tạo được file.

## Thực thi

- Đọc scripts trước khi chạy, nhất là script tải dữ liệu/trích xuất metadata có kết nối ngoài.
- Phát hiện Word và runtime thực có; không suy ra Word dùng được từ sự tồn tại của script.
- Nếu dùng Windows PowerShell 5.1, kiểm tra UTF-8 BOM cho `.ps1` chứa tiếng Việt. JSON/Markdown đọc và ghi UTF-8 rõ ràng; không chuyển BOM hàng loạt mọi định dạng.
- Khi sửa COM ở P1: đóng tài liệu/ứng dụng do task sở hữu, có nhánh cleanup khi lỗi và timeout giới hạn; không kết thúc mọi tiến trình WINWORD.
- Thiếu Word hoặc renderer: ghi rõ bước chưa thực hiện, giữ bản thảo và nêu giới hạn; không báo đã kiểm tra trực quan.
- Không ghi/đổi CSDL, cấu hình đăng nhập hay dữ liệu nguồn theo mặc định audit. Ghi nhận quyền truy cập thiếu trong báo cáo và tiếp tục phần độc lập.

Planner cập nhật bảng năng lực sau khi nhận bằng chứng nghiệm thu. Quy tắc mong muốn không đồng nghĩa mã nguồn đã thực hiện được.
