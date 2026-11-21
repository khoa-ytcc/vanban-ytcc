# Trợ lý văn bản Khoa Y tế Công cộng

Hỗ trợ tra cứu, phân loại, soạn thảo và tạo DOCX/PDF cho Khoa YTCC. Hệ thống đang ở giai đoạn chuẩn bị audit; chưa nghiệm thu bộ template và scripts do AI tạo.

## Bắt đầu

- [AGENTS.md](AGENTS.md): phân vai và quy tắc làm việc của AI.
- [PLAN.md](PLAN.md): phase P0–P4, tiêu chí nghiệm thu, trạng thái và prompt giao P0 tại mục 8.
- [HANDOFF.md](HANDOFF.md): bối cảnh và những kết luận cũ cần kiểm chứng.
- [Runtime](.agents/rules/runtime.md): đường dẫn, công cụ hiện có và giới hạn.

**Planner trực tiếp cập nhật environment/rules/skills. Người dùng tự giao từng phase cho một worker GPT-6.1 Sol duy nhất.** Không tạo subagent.

## Nguồn và sản phẩm cần audit

| Đường dẫn | Vai trò |
|---|---|
| `knowledge_base/sample_pdfs/` | Có 800 file PDF tại lần kiểm kê 14/11/2026; PDF gốc là nguồn đối chiếu, cần kiểm tra liên kết hồ sơ và bản trùng/file thử |
| `D:\Hương\QUANLYVANBAN` | Hệ thống QL văn bản cũ; dữ liệu đăng ký là nguồn đối chiếu, audit dùng chế độ chỉ đọc |
| `knowledge_base/metadata_index/` | JSON dẫn xuất: 2.960 bản ghi đi, 3.873 bản ghi đến; chưa đối chiếu tính đầy đủ với QL văn bản |
| `knowledge_base/templates/` | 5 DOCX do AI tạo, cần kiểm tra từ PDF gốc |
| `tools/` | 9 script PowerShell do AI tạo, cần kiểm tra tính đúng và an toàn thực thi |
| `drafts/` | Bản thảo/output; không dùng làm nguồn chuẩn |
| `.agents/` | Rules và skills do planner duy trì |

Chi tiết: [quy tắc nguồn](.agents/rules/source_provenance.md). Số lượng file/bản ghi không chứng minh chúng đầy đủ, duy nhất hoặc đúng nội dung.

## Công việc trước mắt

P0 phải kiểm tra cả nguồn dữ liệu lẫn DOCX/scripts thực tế. Các vấn đề đã thấy qua đọc mã gồm logic thu nhỏ chữ khi quá một trang và mapping placeholder cần đối chiếu. Chưa chạy kiểm thử đầu cuối hoặc xác nhận các file mẫu đúng thể thức.

Sau P0, một worker lần lượt thực hiện P1 (công cụ), P2 (layout), P3 (dữ liệu ví dụ), P4 (nghiệm thu). Planner rà soát kết quả và cập nhật environment, bao gồm phần tích hợp skills của P3.

## Quy trình nghiệp vụ đích

1. Đọc yêu cầu/văn bản đến, xác định nguồn và dữ kiện.
2. Phân loại, định tuyến nơi nhận, xác minh người ký phù hợp.
3. Soạn nội dung, đánh dấu trường thiếu; không ép tất cả văn bản vào một trang.
4. Dùng công cụ đã được kiểm tra để tạo DOCX/PDF, xem bản render và kiểm tra nội dung.

Đây là quy trình cần nghiệm thu. Trước khi chạy lệnh, xem tham số thật trong script và trạng thái ở PLAN; không suy ra tính năng từ tên file hoặc mô tả cũ.
