# Bàn giao hệ thống văn bản YTCC

Cập nhật bởi planner ngày 14/11/2026 theo chỉ đạo của người dùng. Đọc [AGENTS.md](AGENTS.md) và [PLAN.md](PLAN.md) trước khi làm việc.

## Chỉ đạo hiện hành

- Một planner và một worker GPT-6.1 Sol duy nhất; người dùng trực tiếp giao việc.
- Planner tự quản trị environment, rules và skills; worker chỉ thực hiện phase được giao.
- PDF gốc và dữ liệu trong QL văn bản là nguồn chuẩn để đối chiếu nghiệp vụ. Template Word, scripts và rules do AI tạo là đối tượng audit.
- Độ dài phụ thuộc nội dung; không ép mọi văn bản về một trang.

Kế hoạch ba worker và nhiệm vụ worker sửa skills trong bàn giao trước đã được thay bằng PLAN. Tài liệu này không phải bằng chứng rằng hệ thống đã audit thành công.

## Hiện trạng local đã quan sát

- Repo tại `D:\TH\vanban-ytcc`; hệ thống cũ tại `D:\Hương\QUANLYVANBAN`.
- Có 800 file PDF trong `knowledge_base/sample_pdfs/`.
- Chỉ mục JSON: 2.960 bản ghi đi và 3.873 bản ghi đến; `recipient_summary.json` và `corpus_page_statistics.json` là kết quả dẫn xuất.
- Có 5 DOCX template và 9 script PowerShell do AI tạo.
- Thư mục hệ thống cũ có QLVanBanDi.exe, QLVanBanDen.exe, DLL và JSON cấu hình. Chưa thấy Excel được tài liệu dán ban đầu nhắc đến tại thư mục đó khi kiểm kê.

## Các kết luận kế thừa cần kiểm chứng

| Nội dung từ bàn giao trước | Trạng thái trong kế hoạch mới |
|---|---|
| Các bảng QL văn bản có 3.316 dòng đi, 10.141 dòng đến và các số lượng liên kết Drive | Số liệu lịch sử chưa xác minh trực tiếp trong lượt planner; P0 cần thời điểm snapshot và phạm vi lọc |
| Tiêu đề ứng dụng chứa số 415 và ngày 18/06/2022 là chuỗi viết cứng | Nhận định dịch ngược kế thừa; chưa tái kiểm tra, không dùng thay số liệu thật |
| 800 PDF gồm 762 bản tải và một số file thử/mẫu | Cần kiểm tra liên kết, trùng lặp và nguồn của từng nhóm; không coi mọi file trong thư mục đều là bản gốc độc lập |
| Phân bố số trang và loại văn bản trong thống kê cũ | Kết quả từ script AI; cần audit cách phân loại, đếm trang và chọn mẫu |
| Kích thước lề/chữ/cột và các quy tắc số trang | Cần đối chiếu PDF và nguồn pháp lý chính thức; không dùng thông số ép trang làm chuẩn mặc định |
| Phân công người ký, tên phòng ban, ma trận nơi nhận | Cần bằng chứng hồ sơ, thời điểm và thông tin hiện hành cho văn bản mới |

Những thông tin xác thực từng có trong bản bàn giao cũ không được chép sang environment hoặc báo cáo mới. Cấu hình đăng nhập tại nguồn không phải dữ liệu cần in ra để audit.

## Đầu ra tiếp theo

Người dùng có thể giao prompt P0 ở mục 8 của PLAN cho worker. Worker ghi `audit/P0_AUDIT.md`, `audit/P0_SOURCE_MANIFEST.csv`, `audit/P0_TEST_CASES.md` và dừng. Planner nhận báo cáo qua người dùng, rà soát và cập nhật environment/assignment tiếp theo.
