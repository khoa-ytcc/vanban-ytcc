# Kiểm tra environment do planner cập nhật

Ngày: 14/11/2026. Phạm vi: hướng dẫn AI trong repo, không phải audit/kiểm thử bộ sinh văn bản.

## Đã thay đổi

- Tạo AGENTS.md, GEMINI.md và PLAN.md: một planner, một worker GPT-6.1 Sol do người dùng trực tiếp giao việc.
- Cập nhật ba rules cũ về layout, nơi nhận và thẩm quyền ký; bổ sung nguồn gốc dữ liệu, worker protocol và runtime.
- Cập nhật bốn skills nghiệp vụ, thêm skill `ytcc-system-audit`.
- Đồng bộ README/HANDOFF; bỏ mô hình ba worker và các khẳng định chưa có bằng chứng; không mang thông tin xác thực cũ vào bản bàn giao mới.
- Tách P3 thành worker chuẩn bị ví dụ có nguồn, planner trực tiếp tích hợp vào environment.

## Kiểm tra cấu trúc

- Chạy `quick_validate.py` của skill-creator qua Python cho từng skill: 5/5 hợp lệ.
- Kiểm tra các liên kết Markdown nội bộ trong environment: không có liên kết hỏng.
- Kiểm tra đọc UTF-8 và ký tự thay thế: không phát hiện lỗi.
- Kiểm tra whitespace bằng `git diff --check`: đạt sau khi chuẩn hóa dòng trống cuối file.

Runtime Python ban đầu thiếu PyYAML; dependency kiểm tra được đặt riêng trong thư mục tạm `ytcc-skill-validation-20261114`, không cài vào môi trường AI toàn máy hoặc repo.

## Rà soát tình huống bằng đọc instructions

Đây là walkthrough của planner, không phải kiểm thử độc lập bằng worker/agent khác.

| Tình huống | Hành vi đã được ghi trong hướng dẫn |
|---|---|
| Worker được giao P0 và thấy template tạo được PDF | Vẫn đối chiếu PDF gốc; không coi chuyển đổi thành công là chứng minh đúng |
| Công văn dài có danh sách | Cho phép nhiều trang, không ép thu nhỏ chữ để vừa một trang |
| JSON và PDF khác nơi nhận | Giữ nguồn và trường xung đột; không sửa im lặng hoặc dùng JSON làm chuẩn |
| Mẫu cũ có tên người ký | Ghi là tiền lệ lịch sử, không tự gán vào văn bản mới |
| Người dùng đã yêu cầu tạo file | Tiếp tục trong phạm vi được giao; không yêu cầu phê duyệt lại chỉ vì skill |
| Cần layout/loại văn bản công cụ chưa hỗ trợ | Kiểm tra năng lực thật, nêu giới hạn; không gọi tham số/template tưởng tượng |
| Worker P3 đề xuất đổi skill | Ghi đề xuất vào báo cáo; planner sửa skill sau khi rà soát |

## Chưa thực hiện

Chưa chạy Word COM, render mẫu, kết nối QL văn bản, xác minh quy định pháp lý hoặc audit nguồn corpus. Chưa sửa scripts, DOCX template, dữ liệu gốc hoặc file cấu hình hệ thống cũ. Các việc đó nằm trong phase worker tương ứng.

P0 sẵn sàng để người dùng giao. Tính hợp lệ của skill/frontmatter không chứng minh công cụ hoặc nghiệp vụ đã đạt nghiệm thu.
