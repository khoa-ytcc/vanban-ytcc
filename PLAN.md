# PLAN — Kiểm toán và chuẩn hóa hệ thống văn bản YTCC

**Ngày lập:** 14/11/2026

**Workspace:** `D:\TH\vanban-ytcc`

**Mô hình vận hành:** một planner và một worker GPT-6.1 Sol duy nhất

**Trạng thái điều phối:** planner đã hoàn tất environment ban đầu và kiểm tra cấu trúc; P0–P4 chưa được giao và chưa nghiệm thu.
Đây là kế hoạch triển khai, không phải báo cáo đã audit hoặc chứng nhận bộ công cụ hiện có.

## 1. Mục tiêu

Xây dựng lại một quy trình đáng tin cậy để:

1. tra cứu văn bản đến và tiền lệ văn bản đi;
2. phân loại yêu cầu hành chính;
3. soạn văn bản đi đúng thể thức và đúng phong cách thực tế của Khoa YTCC;
4. sinh DOCX và PDF ổn định bằng Word COM;
5. giữ được sự khác nhau giữa văn bản ngắn một trang và văn bản dài nhiều trang;
6. truy nguyên được mỗi quy tắc, ví dụ và kết luận về nguồn dữ liệu.

## 2. Quyền sở hữu và ranh giới

### Planner làm

- duy trì `PLAN.md`, `AGENTS.md`, `.agents/rules/` và `.agents/skills/`;
- xác định nguồn chuẩn, thứ tự phase và tiêu chí nghiệm thu;
- đọc báo cáo worker, kiểm tra bằng chứng và điều chỉnh assignment tiếp theo;
- phê duyệt việc đưa quy tắc hoặc ví dụ mới vào environment.
- trực tiếp sửa environment sau mỗi báo cáo đã được người dùng chuyển lại; ghi nhận thay đổi tại mục 9.

### Worker làm

- thực hiện đúng phase mà người dùng giao;
- sửa scripts, templates, chỉ mục dẫn xuất hoặc tài liệu triển khai khi phase cho phép;
- tạo artifact kiểm chứng và báo cáo kết quả;
- dừng ở ranh giới phase, không tự giao việc cho agent khác, không tự thay đổi vai trò planner.

### Người dùng làm

- chọn và giao phase tiếp theo cho worker GPT-6.1 Sol;
- xem xét kết quả và quyết định có chuyển sang phase kế tiếp hay không.

## 3. Thứ bậc nguồn dữ liệu

| Cấp | Nguồn | Cách sử dụng |
|---|---|---|
| S0 | PDF gốc trong `knowledge_base/sample_pdfs/`, sau khi xác nhận là bản tải từ kho thực tế | Bằng chứng bố cục, câu chữ, số trang, bảng và chữ ký |
| S0 | Dữ liệu/biểu mẫu được kiểm chứng trực tiếp với hệ thống cũ tại `D:\Hương\QUANLYVANBAN` hoặc nguồn QL văn bản tương ứng | Bằng chứng định danh, số đi/số đến, ngày, trích yếu, nơi nhận, người ký |
| S1 | `knowledge_base/metadata_index/*.json` | Chỉ mục dẫn xuất để tìm kiếm; phải có kiểm tra chéo với S0 |
| S2 | `knowledge_base/templates/*.docx`, `tools/*.ps1`, `drafts/`, prompt và skill do AI tạo | Mã và sản phẩm cần audit; không được coi là chuẩn chỉ vì đang có trong repo |

Khi hai nguồn mâu thuẫn, không tự chọn một bên. Ghi lại trường mâu thuẫn, hai bằng chứng và quyết định tạm thời trong báo cáo audit.

PDF và QL văn bản cùng là nguồn gốc, dùng theo từng trường: PDF cho nội dung/bố cục; QL văn bản cho dữ liệu đăng ký và liên kết hồ sơ. Mẫu lịch sử không tự chứng minh thẩm quyền ký hiện hành hoặc tuân thủ pháp luật. Khi cần kết luận pháp lý, phải kiểm tra nguồn chính thức riêng và ghi ngày tra cứu.

## 4. Hiện trạng đã biết và điểm cần xác minh

- Repo hiện có 800 PDF trong `knowledge_base/sample_pdfs/`.
- Bàn giao cũ có nhắc bản tải cùng file thử; P0 phải phân biệt PDF gốc, file trùng và output thử. Không suy ra 800 file là 800 hồ sơ nguồn độc lập.
- Hai JSON chỉ mục hiện có lần lượt 2.960 bản ghi văn bản đi và 3.873 bản ghi văn bản đến; đây là số liệu dẫn xuất, chưa phải số liệu chuẩn cho đến khi đối chiếu với QL văn bản.
- Repo có 5 template DOCX và 9 script PowerShell được tạo trong quá trình phát triển AI; phải audit từ đầu.
- Thư mục hệ thống cũ hiện thấy executable, DLL và các JSON cấu hình; file Excel được nêu trong tài liệu bàn giao chưa được xác nhận đang có tại đường dẫn đó.
- `gemini.md` trước đây chứa quy tắc ép một số văn bản vào một trang. Quy tắc mới phải chọn layout theo nội dung và loại văn bản.
- Không đưa thông tin xác thực CSDL hoặc bí mật giải mã vào bất kỳ artifact mới nào.

## 5. Lộ trình một worker

### P0 — Audit nguồn và baseline

**Mục tiêu:** xác định cái gì là nguồn thật, cái gì là sản phẩm AI, và các lỗi hiện tại có bằng chứng.

**Phạm vi:** PDF, QL văn bản có thể đọc ở chế độ chỉ đọc, JSON index, templates, scripts, skills và rules.

**Đầu ra bắt buộc:**

- `audit/P0_AUDIT.md`;
- `audit/P0_SOURCE_MANIFEST.csv`: inventory và bảng nguồn gốc; khóa QL văn bản, đường dẫn PDF, tình trạng liên kết, hash nếu thu thập, trạng thái xác minh;
- `audit/P0_TEST_CASES.md`: ca kiểm thử đại diện cho văn bản ngắn, dài, có bảng, phụ lục và PDF scan;
- trong báo cáo: danh sách lỗi theo mức **Critical/High/Medium/Low**, tránh nhầm mức lỗi với tên phase P0–P4;
- bảng đối chiếu từng loại DOCX với PDF nguồn và từng placeholder với tham số script; trạng thái đúng/sai/chưa đủ bằng chứng.

**Cách kiểm tra:** kiểm kê toàn bộ file, chọn mẫu phân tầng theo loại văn bản, độ dài và cấu trúc; ghi số PDF thực sự đã đọc. Không suy rộng việc đọc vài PDF thành đã xác minh 800 PDF. Đọc XML trong DOCX để kiểm tra nội dung/styles; nếu cần chạy công cụ cũ để tái hiện lỗi, đọc mã trước và dùng bản sao/output riêng trong `audit/artifacts/P0/`.

**Điểm bắt buộc đối chiếu:** thông tin JSON với QL văn bản theo khóa ổn định (không chỉ số đi vì có thể lặp giữa năm); ánh xạ PDF–hồ sơ; template và scripts do AI tạo; tên người ký, nơi nhận và kết luận thể thức trong rules cũ. Nếu chưa đọc được QL văn bản, báo cáo phần đó chưa xác minh và tiếp tục audit local.

**Không làm:** chưa sửa implementation, chưa ghi vào CSDL, chưa tạo bộ template mới.

### P1 — Ổn định dữ liệu và công cụ

**Mục tiêu:** làm cho luồng nhận dữ liệu, điền placeholder, lưu DOCX và xuất PDF có thể lặp lại.

**Phạm vi:** `tools/`, schema đầu vào, đường dẫn output, encoding, lỗi COM, dọn dẹp tài nguyên Word.

**Nghiệm thu:**

- tất cả placeholder được lập bảng và điền đúng;
- lỗi đầu vào trả về thông báo có thể xử lý;
- Word COM luôn đóng tài liệu và ứng dụng trong cả nhánh thành công/lỗi;
- script không ghi đè PDF/DOCX nguồn;
- có smoke test cho cả Windows PowerShell 5.1 và PowerShell 7 nếu môi trường cho phép.
- timeout/hủy chỉ tác động phiên Word do task tạo; kiểm tra khi có tài liệu Word khác đang mở;
- xử lý tên file trùng, đường dẫn có dấu/khoảng trắng và nội dung Unicode; kết quả số trang là số, không phải Boolean;
- ghi bằng chứng ở `audit/P1_IMPLEMENTATION.md`, dữ liệu thử ở `audit/artifacts/P1/`.

### P2 — Layout thích ứng và template

**Mục tiêu:** tạo layout ngắn và dài dựa trên nội dung thực tế.

**Phạm vi:** template DOCX, header/footer, số trang, repeat header row, khối chữ ký và nơi nhận.

**Nghiệm thu:**

- văn bản ngắn có mục tiêu một trang nhưng không hy sinh nội dung;
- văn bản dài được phép nhiều trang;
- trang cuối không chỉ có chữ ký;
- bảng dài lặp dòng tiêu đề;
- số trang và phụ lục được kiểm tra bằng PDF render;
- mỗi layout có ít nhất một ca đối chiếu với PDF nguồn tương ứng.
- có cơ chế chọn layout dựa trên cấu trúc và kiểm tra phân trang thật, không chỉ đếm ký tự; không bắt buộc nhân đôi tất cả template nếu có thể dùng style/profile chung;
- ghi bằng chứng ở `audit/P2_LAYOUT.md`, bộ DOCX/PDF và ảnh kiểm tra ở `audit/artifacts/P2/`.

### P3 — Worker chuẩn bị corpus; planner cập nhật skills

**Mục tiêu:** thu thập ví dụ có nguồn để planner hoàn thiện rules và skills.

**Worker thực hiện:** tạo `knowledge_base/examples/` gồm chỉ mục và trích đoạn đã đối chiếu; báo cáo `audit/P3_CORPUS.md` nêu đề xuất phân loại, routing và mẫu câu. Ghi nguồn PDF/trang, khóa hồ sơ, cách trích xuất/OCR và trạng thái kiểm chứng. Đây là dữ liệu tham khảo, không phải bộ instructions tự động thực thi.

**Planner thực hiện sau khi nhận báo cáo:** rà soát ví dụ, trực tiếp cập nhật `.agents/rules/`, `.agents/skills/` và `PLAN.md`. Worker không sửa các đường dẫn này.

**Nghiệm thu:**

- mỗi ví dụ có mã nguồn PDF hoặc bản ghi QL văn bản;
- không đưa dữ liệu cá nhân không cần thiết vào prompt;
- skill phân biệt rõ: thông tin đã xác minh, suy luận và trường cần người dùng xác nhận;
- các skill dùng chung source hierarchy, authority rules và recipient matrix.
- worker có thể bàn giao P3 khi dữ liệu và báo cáo đã đủ; toàn phase chỉ được nghiệm thu sau phần cập nhật và kiểm tra skills của planner.

### P4 — Nghiệm thu hệ thống và bàn giao

**Mục tiêu:** chạy quy trình từ yêu cầu đến DOCX/PDF và bàn giao được.

**Đầu ra bắt buộc:**

- `audit/P4_ACCEPTANCE.md`;
- bộ input tối thiểu và output đại diện;
- README cập nhật;
- changelog hoặc bảng thay đổi;
- danh sách giới hạn còn lại và hướng khắc phục.

**Phân công:** worker chạy bộ kiểm tra và đề xuất nội dung hướng dẫn trong báo cáo; planner cập nhật README/HANDOFF, PLAN và environment theo kết quả đã chấp nhận. Không ghi "đã chuẩn hóa" cho chức năng chưa qua nghiệm thu.

## 6. Giao worker theo từng lượt

Mỗi assignment gửi cho worker phải có dạng:

```text
Phase: P0 | P1 | P2 | P3 | P4
Mục tiêu:
Phạm vi file:
Không được làm:
Đầu ra bắt buộc:
Tiêu chí nghiệm thu:
```

Worker chỉ bắt đầu sau khi đọc `AGENTS.md`, `PLAN.md` và rules liên quan. Nếu phát hiện nguồn mâu thuẫn hoặc thiếu quyền đọc dữ liệu, worker ghi nhận trong báo cáo và tiếp tục phần độc lập được.

Báo cáo gửi lại qua người dùng, không tự nhắn sang chat planner. Planner cập nhật trạng thái, phát hành assignment kế tiếp; người dùng quyết định giao. Không tự chuyển phase.

## 7. Tiêu chí dừng

Dừng phase khi đầu ra bắt buộc đã có, kiểm tra đã chạy, và báo cáo nêu rõ lỗi còn lại. Không mở rộng sang phase sau chỉ vì đã chạm vào file liên quan.

## 8. Assignment P0 sẵn sàng gửi

```text
Bạn là worker duy nhất, GPT-6.1 Sol; không tạo subagent.
Đọc AGENTS.md, PLAN.md và .agents/skills/ytcc-system-audit/SKILL.md.
Phase: P0 — Audit nguồn và baseline
Mục tiêu: xác định nguồn chuẩn và audit toàn bộ artifact AI hiện có.
Phạm vi file: HANDOFF.md, README.md, knowledge_base/sample_pdfs/, knowledge_base/metadata_index/, knowledge_base/templates/, tools/, .agents/
Không được làm: không sửa implementation, không tạo template mới, không ghi CSDL, không đưa secrets vào báo cáo.
Đầu ra bắt buộc: audit/P0_AUDIT.md, audit/P0_SOURCE_MANIFEST.csv, audit/P0_TEST_CASES.md; mức lỗi Critical/High/Medium/Low.
Tiêu chí nghiệm thu: mọi kết luận có đường dẫn bằng chứng; JSON được ghi là dẫn xuất cho đến khi đối chiếu QL văn bản; template/script được xem là artifact cần audit.
Dừng sau P0, báo cáo cho người dùng chuyển lại planner. Không sửa PLAN, AGENTS, rules hoặc skills.
```

## 9. Theo dõi và cập nhật

| Hạng mục | Người thực hiện | Trạng thái |
|---|---|---|
| Environment ban đầu, rules, 5 skill và plan | Planner | Hoàn tất; xem báo cáo kiểm tra bên dưới |
| P0 — Audit | Worker | Chưa giao |
| P1 — Dữ liệu/công cụ | Worker | Chờ P0 |
| P2 — Layout/template | Worker | Chờ P1 |
| P3 — Ví dụ có nguồn | Worker | Chờ baseline và hợp đồng dữ liệu ổn định |
| P3 — Tích hợp rules/skills | Planner | Chờ báo cáo corpus |
| P4 — Nghiệm thu | Worker + planner rà soát | Chờ các phần trước |

14/11/2026: xác lập một worker; planner sở hữu environment. PDF gốc và QL văn bản là căn cứ; template/scripts cũ phải audit. Không giữ kế hoạch ba worker của bàn giao cũ.

Bằng chứng kiểm tra environment: [audit/PLANNER_ENVIRONMENT_CHECK.md](audit/PLANNER_ENVIRONMENT_CHECK.md). Báo cáo này không thay thế P0 audit hệ thống.
