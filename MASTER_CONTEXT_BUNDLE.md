# MASTER CONTEXT BUNDLE: HỆ THỐNG SOẠN THẢO & QUẢN LÝ VĂN BẢN KHOA YTCC
*Bản đóng gói toàn bộ ngữ cảnh, tri thức, kỹ thuật và tiến trình làm việc dành cho AI Agents kế tiếp*

---

## 1. THÔNG TIN ĐIỀU HÀNH & BỐI CẢNH DỰ ÁN
* **Đơn vị chủ quản:** Khoa Y tế Công cộng (YTCC) – Đại học Y Dược TP. Hồ Chí Minh (UMP).
* **Người dùng (User):** Thu Hương (`thuhuongytcc`), Chuyên viên phụ trách văn thư, tiếp nhận công văn đến và soạn thảo văn bản đi của Khoa.
* **Mục tiêu dự án:**
  1. Xây dựng môi trường AI Agent hỗ trợ chuyên viên tiếp nhận văn bản đến -> phân tích -> tự động soạn thảo văn bản đi (Word `.docx` và xuất `.pdf`) chuẩn thể thức hành chính theo **Nghị định 30/2020/NĐ-CP** và quy định riêng của Đại học Y Dược TP.HCM / Khoa YTCC.
  2. Số hóa, giải mã và khai thác toàn bộ dữ liệu lịch sử từ ứng dụng cũ (`QLVanBanDi.exe`) và kho lưu trữ thực tế làm cơ sở tri thức (Knowledge Base) cho AI học tập.
  3. Thiết lập hệ thống kiểm toán (audit) độc lập, tự động hóa bằng PowerShell COM, có cơ chế quản trị phân chia vai trò (Planner - Worker).
* **Vị trí Workspace trên máy người dùng:**
  * Workspace hiện tại (mới): `D:\TH\vanban-ytcc` (Git Private Repo: `https://github.com/khoa-ytcc/vanban-ytcc`, nhánh `main`).
  * Thư mục hệ thống cũ: `D:\Hương\QUANLYVANBAN`
* **Môi trường kỹ thuật:** Windows 10/11 x64, Windows PowerShell 5.1 (chú ý: encoding mặc định ANSI/Windows-1252), Microsoft Word COM Automation (`winword.exe`), GitHub CLI (`gh`).

---

## 2. TOÀN CẢNH LỊCH SỬ HỘI THOẠI & CÁC CỘT MỐC ĐÃ ĐẠT ĐƯỢC
1. **Dịch ngược ứng dụng cũ (`QLVanBanDi.exe`):**
   * Người dùng yêu cầu phân tích app quản lý văn bản đi và tải toàn bộ file PDF từ các URL Google Drive.
   * Đã bẻ khóa mật khẩu CSDL đám mây MySQL (`45.117.169.194:3306`) thông qua phân tích mã IL (thuật toán TripleDES, khóa `KDAX19KQK54MZ`, mật khẩu: `D0.4nhuy`).
   * Giải mã nghịch lý số lượng: Bảng `cv_di_qlvb` có 3.316 dòng (do import trùng nhiều lần), nhưng năm 2026 có đúng **944 số đi duy nhất** (với 762 link Google Drive dẫn tới file PDF scan, 4 folder link, 178 ô trống).
   * Giải mã tiêu đề Form *"Tổng cộng đến 18/06/2022: 415 Rec"*: Đây là chuỗi được tác giả (Thầy Dũng - `dvdung@ump.edu.vn`) **viết cứng (hardcode)** trong `Form1_Load` khi đóng gói app năm 2022; CSDL thực tế vẫn chạy liên tục đến năm 2026.
2. **Khai thác và thiết lập Kho tri thức (Knowledge Base):**
   * Trích xuất dữ liệu từ file Excel `CÔNG VĂN ĐẾN, ĐI 2023, 2024.xlsx` và CSDL MySQL ra JSON:
     * `cv_di_history.json`: 2.960 bản ghi văn bản đi (2023–2026) kèm nơi nhận/chuyên viên xử lý.
     * `cv_den_history.json`: 3.873 bản ghi văn bản đến (2025–2026).
     * `recipient_summary.json`: Ma trận thống kê nơi nhận.
   * Xây dựng công cụ tải đa luồng nền `tools/download_all_sample_pdfs.ps1` (10 thread RunspacePool), tải thành công **toàn bộ 762/762 file PDF** từ Google Drive về `knowledge_base/sample_pdfs/` (Tổng cộng 800 files PDF gồm cả các bản test, dung lượng **1.47 GB**, tỷ lệ thành công 100%, 0 lỗi).
3. **Chuẩn hóa Template & Kịch bản tự động hóa:**
   * Tạo 5 mẫu Word chuẩn thể thức Nghị định 30 trong `knowledge_base/templates/` (`Mau_Cong_van.docx`, `Mau_To_trinh.docx`, `Mau_Giay_gioi_thieu.docx`, `Mau_Ke_hoach.docx`, `Mau_Bao_cao.docx`).
   * Viết các kịch bản PowerShell tự động:
     * `generate_document.ps1`: Điền nội dung vào template, tự động gỡ trùng "V/v", thay thế biến.
     * `export_pdf.ps1`: Chuyển đổi DOCX sang PDF qua Word COM.
     * `search_history.ps1`: Tìm kiếm tiền lệ văn bản trong 2.960 bản ghi.
4. **Soạn thảo thực chiến văn bản phúc đáp HTV7:**
   * Nhận văn bản đến: Công văn số `1011/CV2026` của Cty TNHH Truyền hình Kết Nối mời ThS. Trương Nhật Khuê Tường (Bộ môn Dinh dưỡng) ghi hình talkshow "Sức Khỏe 24h" trên HTV7 (Số đến ĐHYD: 5405, BGH phê chuyển P. TCCB đầu mối & Khoa YTCC).
   * Đã hoàn thiện bản dự thảo Công văn đi (cả file `.docx` và `.pdf`) chuẩn 1 mặt giấy A4.
5. **Cải tiến cốt lõi: Quy tắc thích ứng độ dài văn bản (Adaptive Pagination Rules):**
   * *Phản hồi của người dùng:* Ban đầu người dùng yêu cầu gói gọn trong 1 mặt giấy, nhưng sau đó đã chỉnh lý: *"độ dài còn tuỳ thuộc vào nội dung, không được ép cứng mọi văn bản về 1 trang"*.
   * Đã viết script `analyze_corpus_stats.ps1` quét toàn bộ 800 PDF mẫu để có số liệu thực chứng khoa học:
     * **1 trang:** 277 bản (34.6%) — Chủ yếu là Công văn ngắn, Giấy giới thiệu, Tờ trình ngắn 1 nội dung.
     * **2 trang:** 212 bản (26.5%) — Công văn có bảng phân công, tờ trình có giải trình.
     * **3 trang trở lên:** 311 bản (38.9%) — Kế hoạch (TB: 4.2 trang), Báo cáo (TB: 6.5 trang), Tờ trình dự án/kinh phí (TB: 3.6 trang), Quy định (TB: 2.3 trang).
6. **Thiết lập Khung Kiểm toán & Quản trị AI (PLAN.md & AGENTS.md):**
   * Xác lập hợp đồng AI: 1 Planner + 1 Worker (GPT-6.1 Sol do người dùng giao việc trực tiếp).
   * Thiết lập 5 giai đoạn kiểm toán: P0 (Source Baseline), P1 (Scripts & COM), P2 (Layout & Typography), P3 (Knowledge Extraction), P4 (Acceptance).
   * Bổ sung quy tắc: `.agents/rules/worker_protocol.md`, `.agents/rules/source_provenance.md`, `.agents/rules/runtime.md`, skill `.agents/skills/ytcc-system-audit/`.

---

## 3. THÔNG SỐ KỸ THUẬT & DỮ LIỆU ĐÃ GIẢI MÃ (CREDENTIAL & DATA VAULT)
* **Kết nối CSDL MySQL cũ:**
  * Host: `45.117.169.194` | Port: `3306`
  * Database: `dvdung_dbase`
  * Username: `dvdung_user`
  * Password: `D0.4nhuy`
  * Thuật toán mã hóa cũ: TripleDES với Base64 Key `KDAX19KQK54MZ` (trong `CongVanDi.Simple3Des`).
  * Chuỗi kết nối PowerShell mẫu:
    ```powershell
    $connStr = "server=45.117.169.194; port=3306; userid=dvdung_user; password=D0.4nhuy; database=dvdung_dbase; pooling=false; Character Set=utf8; convert zero datetime=True"
    ```
* **Cấu trúc bảng `cv_di_qlvb`:**
  * `so_di` (int): Số đi văn bản.
  * `nam` (int): Năm ban hành (ví dụ 2026).
  * `ngay_vanban` (varchar/datetime): Ngày văn bản.
  * `tenloai_trichyeu` (varchar): Tên loại và trích yếu nội dung văn bản.
  * `nguoi_ki` (varchar): Người ký (chủ yếu PGS. TS. Nguyễn Duy Phong, PGS. TS. Tô Gia Kiên, PGS. TS. Thái Thanh Trúc).
  * `url` (varchar): Đường link Google Drive dẫn tới file scan PDF có dấu mộc đỏ.
  * `faculty` (varchar): Mã khoa (`YTCC`).

---

## 4. QUY TẮC THỂ THỨC HÀNH CHÍNH & ĐỊNH DẠNG (FORMATTING MATRIX)
Áp dụng theo **Nghị định 30/2020/NĐ-CP** kết hợp thực tế thẩm mỹ của Khoa YTCC:

### 4.1. Bảng Tiêu ngữ (Header Table - 2 cột không viền)
* Khổ in: Giấy A4 đứng (210 x 297 mm, tương đương 595.3 x 841.9 pt).
* Căn lề: Trái 30 mm (85.05 pt), Phải 20 mm (56.7 pt), Trên 20 mm (56.7 pt), Dưới 20 mm (56.7 pt).
* Vùng in khả dụng = 595.3 - 85.05 - 56.7 = **453.55 pt**.
* **Độ rộng 2 cột Header:**
  * **Cột 1 (Bên trái):** 195 - 200 pt. Gồm:
    * Dòng 1: `ĐẠI HỌC Y DƯỢC` (10 - 10.5 pt, hoa, đứng).
    * Dòng 2: `THÀNH PHỐ HỒ CHÍ MINH` (10 - 10.5 pt, hoa, đứng).
    * Dòng 3: `KHOA Y TẾ CÔNG CỘNG` (11 pt, hoa, **đậm**, có đường gạch chân nét liền phía dưới bằng độ dài dòng chữ).
    * Dòng 4: `Số:       /YTCC-VP` (hoặc `/TTr-YTCC`, `/GGT-YTCC`, `/KH-YTCC`, `/BC-YTCC`) (11 pt, đứng).
    * Dòng 5 (đối với Công văn): `V/v [Trích yếu]` (11 pt, nghiêng, line-spacing 11.5 - 12 pt).
  * **Cột 2 (Bên phải):** 253 - 258 pt (đảm bảo không bị rớt chữ `NAM` trong Quốc hiệu). Gồm:
    * Dòng 1: `CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM` (10 - 10.5 pt, hoa, **đậm**).
    * Dòng 2: `Độc lập – Tự do – Hạnh phúc` (11 pt, chữ thường, **đậm**, có đường gạch chân nét liền ở giữa).
    * Dòng 3: `Thành phố Hồ Chí Minh, ngày ... tháng ... năm ...` (11 pt, nghiêng).

### 4.2. Quy tắc Thích ứng Số trang (Adaptive Pagination)
1. **Nhóm văn bản ngắn (1 trang):**
   * Áp dụng: Công văn cử/đồng ý viên chức, phúc đáp ngắn, giấy mời, giấy giới thiệu, tờ trình 1 nội dung.
   * Toàn bộ nội dung + nơi nhận + chữ ký phải nằm trọn trong 1 trang duy nhất.
   * Nghiêm cấm lỗi "góa phụ": Đẩy khối chữ ký hoặc nơi nhận sang trang 2.
2. **Nhóm văn bản dài (nhiều trang: 2 đến 10+ trang):**
   * Áp dụng: Kế hoạch (KH), Báo cáo (BC), Tờ trình dự trù kinh phí lớn, Quy định/Quy chế đào tạo.
   * **Bắt buộc đánh số trang:** Từ trang 2 trở đi, font Times New Roman 13-14 pt đứng, đặt ở giữa lề trên hoặc lề dưới.
   * **Quy tắc chữ ký trang cuối:** Bắt buộc phải có **tối thiểu 3 đến 5 dòng nội dung văn bản** trước khối chữ ký. Tuyệt đối không để một trang cuối cùng chỉ trơ trọi mỗi khối chữ ký.
   * **Bảng biểu dài qua trang:** Phải thiết lập thuộc tính `Repeat Header Row` để lặp lại tiêu đề bảng ở mỗi trang mới.

---

## 5. DANH MỤC TÀI LIỆU & FILE TRONG REPOSITORY (`D:\TH\vanban-ytcc`)
```
D:\TH\vanban-ytcc\
├── .agents/
│   ├── rules/
│   │   ├── authority_rules.md      # Quy tắc thẩm quyền ký (Trưởng khoa, Phó Trưởng khoa)
│   │   ├── gemini.md               # Quy chuẩn thể thức NĐ 30 và định dạng Word
│   │   ├── recipient_matrix.md     # Ma trận nơi nhận (BGH, các Phòng chức năng, Bệnh viện)
│   │   ├── runtime.md              # Hướng dẫn môi trường thực thi PowerShell / Word COM
│   │   ├── source_provenance.md    # Nguyên tắc bằng chứng gốc (PDF gốc > JSON > File AI tạo)
│   │   └── worker_protocol.md      # Quy chế hoạt động của Worker agent
│   └── skills/
│       ├── ytcc-classify-doc/      # Phân loại văn bản đến/đi
│       ├── ytcc-docx-export/       # Kỹ thuật sinh DOCX và xuất PDF
│       ├── ytcc-draft-writer/      # Soạn thảo văn bản hành chính
│       ├── ytcc-reply-incoming/    # Soạn công văn phúc đáp văn bản đến
│       └── ytcc-system-audit/      # Kỹ năng kiểm toán hệ thống
├── audit/
│   ├── P0_SOURCE_MANIFEST.csv      # Bảng kê bằng chứng nguồn PDF và metadata
│   ├── PLANNER_ENVIRONMENT_CHECK.md # Biên bản kiểm tra môi trường của Planner
│   └── artifacts/                  # Thư mục lưu kết quả kiểm thử P0-P4
├── drafts/                         # Nơi lưu các văn bản dự thảo đã sinh (theo tháng YYYY-MM)
├── knowledge_base/
│   ├── metadata_index/
│   │   ├── cv_den_history.json     # 3.873 bản ghi văn bản đến (2025-2026)
│   │   ├── cv_di_history.json      # 2.960 bản ghi văn bản đi (2023-2026)
│   │   ├── recipient_summary.json  # Thống kê phân bổ nơi nhận
│   │   └── corpus_page_statistics.json # Thống kê số trang thực tế của 800 PDF
│   ├── sample_pdfs/                # 800 FILE PDF GỐC (1.47 GB) từ Google Drive
│   └── templates/                  # 5 template DOCX chuẩn
├── tools/
│   ├── analyze_corpus_stats.ps1    # Phân tích số trang & thể loại từ kho PDF
│   ├── build_talkshow_cv.ps1       # Script sinh công văn phúc đáp HTV7 mẫu
│   ├── create_templates.ps1        # Script khởi tạo 5 file template Word
│   ├── download_all_sample_pdfs.ps1# Script tải 762 PDF đa luồng từ Google Drive
│   ├── export_pdf.ps1              # Chuyển đổi DOCX -> PDF qua Word COM
│   ├── extract_metadata.ps1        # Trích xuất CSDL sang JSON
│   ├── generate_document.ps1       # Script điền nội dung vào template
│   ├── search_history.ps1          # Tra cứu lịch sử văn bản
│   ├── MySql.Data.dll              # Thư viện MySQL cho .NET/PowerShell
│   └── Newtonsoft.Json.dll         # Thư viện JSON cho .NET/PowerShell
├── AGENTS.md                       # Hợp đồng phân vai Planner - Worker
├── GEMINI.md                       # Cấu hình AI Gemini môi trường
├── HANDOFF.md                      # Bàn giao ngắn gọn của Planner
├── PLAN.md                         # Kế hoạch chi tiết 5 giai đoạn kiểm toán (P0-P4)
└── README.md                       # Giới thiệu tổng quan repository
```

---

## 6. CÁC "CẠM BẪY" KỸ THUẬT & CÁCH KHẮC PHỤC TRIỆT ĐỂ (LESSONS LEARNED)
1. **Lỗi Encoding Tiếng Việt trên Windows PowerShell 5.1:**
   * *Nguyên nhân:* Mặc định PowerShell 5.1 đọc file `.ps1` bằng mã ANSI (Windows-1252). Nếu file `.ps1` lưu UTF-8 không có BOM, các ký tự tiếng Việt có dấu sẽ bị biến thành rác ký tự (`Ä‘á»“ng Ã½`), gây lỗi cú pháp parser.
   * *Giải pháp bắt buộc:* Mọi file script PowerShell `.ps1` phải luôn được ghi với **UTF-8 with BOM** (byte đầu `EF BB BF`).
2. **Lỗi treo Word COM Automation (`winword.exe`):**
   * *Nguyên nhân:* Nếu gọi `$doc.SaveAs2()` với tham số object không tương thích hoặc tài khoản Office hiển thị popup đám mây / OneDrive, Word sẽ hiển thị hộp thoại modal ngầm khiến tiến trình PowerShell bị block vĩnh viễn.
   * *Giải pháp an toàn:* Sử dụng quy trình copy template trước: `Copy-Item $templatePath $outPath` -> `$word.Documents.Open($outPath)` -> chỉnh sửa Range -> `$doc.Save()` (gọi Save() trực tiếp không bao giờ hiện dialog) -> `$doc.ExportAsFixedFormat($pdfPath, 17)` -> `$doc.Close([ref]0)` -> `$word.Quit()` -> giải phóng COM Object.
3. **Giới hạn số ký tự trong Find & Replace của Word COM:**
   * Phương thức `$range.Find.Replacement.Text` bị giới hạn tối đa 255 ký tự. Khi thay thế đoạn văn bản dài (như `{{NOI_DUNG}}`), phải dùng vòng lặp:
     ```powershell
     while ($range.Find.Execute($findText)) {
         $range.Text = $replaceText
         $range.Collapse(0) # wdCollapseEnd
     }
     ```
4. **Hạn chế Subagent Quota (`RESOURCE_EXHAUSTED 429`):**
   * Không spawn subagent qua API nội bộ nếu gặp lỗi hạn mức. Thay vào đó, sử dụng đa luồng PowerShell cục bộ (`[runspacefactory]::CreateRunspacePool(1, 10)`) để xử lý tác vụ nặng (như cào dữ liệu, tải hàng trăm file PDF), tốc độ nhanh hơn và hoàn toàn không tốn quota API.

---

## 7. HƯỚNG DẪN DÀNH CHO AI AGENT TIẾP QUẢN (NEXT AGENT INSTRUCTIONS)
Khi một AI Agent mới (Planner hoặc Worker) bắt đầu phiên làm việc:
1. **Đọc các file cốt lõi theo thứ tự:**
   * Bước 1: Đọc [AGENTS.md](file:///d:/TH/vanban-ytcc/AGENTS.md) để hiểu hợp đồng phân vai và ranh giới.
   * Bước 2: Đọc [PLAN.md](file:///d:/TH/vanban-ytcc/PLAN.md) để nắm lộ trình các Phase (P0 -> P4).
   * Bước 3: Đọc [.agents/rules/source_provenance.md](file:///d:/TH/vanban-ytcc/.agents/rules/source_provenance.md) và [.agents/rules/runtime.md](file:///d:/TH/vanban-ytcc/.agents/rules/runtime.md).
2. **Nếu là Worker:**
   * Kiểm tra phase mà User giao trong `PLAN.md` (hiện tại là **P0: Source Baseline & Evidence Manifest**).
   * Thực hiện nhiệm vụ trong phạm vi phase, ghi chép bằng chứng vào `audit/P0_AUDIT.md`, `audit/P0_SOURCE_MANIFEST.csv`, không tự ý nhảy phase hoặc sửa rules ngoài thẩm quyền.
3. **Nếu là Planner:**
   * Xem xét báo cáo audit của Worker, cập nhật `PLAN.md`, hoàn thiện bộ templates (`1-Page` và `Multi-Page`), và bổ sung dữ liệu Few-shot từ kho 800 PDF vào các skills.

---

## 8. MẪU PROMPT CHUYỂN GIAO NHANH CHO USER (COPY-PASTE READY)
Khi bạn bắt đầu một cuộc trò chuyện mới với AI Agent khác, bạn chỉ cần copy đoạn text dưới đây gửi cho Agent đó:

```text
Xin chào, tôi là Thu Hương (Khoa Y tế Công cộng, Đại học Y Dược TP.HCM). 
Bạn đang làm việc trong workspace "D:\TH\vanban-ytcc" (Private Repo: https://github.com/khoa-ytcc/vanban-ytcc).
Đây là hệ thống quản lý văn bản đến và tự động soạn thảo văn bản đi (Word .docx và PDF) chuẩn thể thức Nghị định 30/2020/NĐ-CP.

Tôi đã đóng gói toàn bộ ngữ cảnh, CSDL, lịch sử nghiên cứu và quy tắc định dạng vào file "MASTER_CONTEXT_BUNDLE.md" ngay tại thư mục gốc của repository.
Hãy đọc các file sau trước khi bắt đầu:
1. MASTER_CONTEXT_BUNDLE.md (Bản tóm tắt toàn diện mọi phát hiện, CSDL, kho 800 PDF và bài học kinh nghiệm).
2. AGENTS.md (Hợp đồng vai trò Planner - Worker).
3. PLAN.md (Kế hoạch triển khai kiểm toán hệ thống từ P0 đến P4).

Hãy xác nhận bạn đã đọc hiểu cấu trúc và cho tôi biết bạn đã sẵn sàng thực hiện phase nào tiếp theo!
```
