# HỆ THỐNG TỰ ĐỘNG HÓA VĂN BẢN HÀNH CHÍNH KHOA YTCC (V2.0)
> Giải pháp soạn thảo, tra cứu tiền lệ và xuất bản tài liệu chuẩn Nghị định 30/2020/NĐ-CP dành riêng cho Khoa Y tế Công cộng – Đại học Y Dược TP.HCM.

---

## 1. Cấu trúc Thư mục v2.0
```text
vanban-ytcc/
├── .agents/
│   ├── rules/                # Bộ quy tắc vận hành, thể thức, thẩm quyền, an toàn
│   └── skills/               # 4 kỹ năng tác nghiệp: Intake -> Draft -> QA -> Learn
├── audit/
│   ├── p2_tests/             # Dữ liệu nghiệm thu 6 test case chuẩn hóa
│   └── scripts/              # Các kịch bản chạy test tự động (P2, P3)
├── drafts/
│   └── YYYY-MM/              # Thư mục lưu các bản nháp DOCX, PDF và JSON theo tháng
├── knowledge_base/
│   ├── memory/               # Bộ nhớ tự học: thói quen người dùng & bài học kinh nghiệm
│   ├── metadata_index/       # SQLite FTS5 (ytcc_history.db) & JSON lịch sử
│   ├── sample_pdfs/          # Kho 800 file PDF thực tế (S0 - Nguồn chân lý gốc)
│   └── specs/                # Bảng đặc tả thể thức (ytcc_format_spec.md) & Schema (doc_schema.md)
├── tools/
│   ├── build_doc.py          # Core Engine biên dịch JSON -> Word DOCX (+ xuất PDF)
│   ├── build_index.py        # Tạo/cập nhật chỉ mục tìm kiếm SQLite FTS5 từ CSDL cũ
│   ├── diff_draft.py         # So sánh khác biệt giữa bản AI tạo và bản người dùng đã sửa
│   ├── export_pdf.ps1        # Script xuất PDF an toàn qua Word COM
│   ├── inspect_pdf.py        # Công cụ tự động kiểm định thể thức PDF & render ảnh
│   └── search_history.py     # CLI tra cứu nhanh tiền lệ lịch sử có/không dấu
├── AGENTS.md                 # Quy chuẩn vận hành AI, phân vai & an toàn tiến trình
├── GEMINI.md                 # Ngữ cảnh nạp nhanh cho trợ lý AI
└── PLAN.md                   # Kế hoạch & tiến độ triển khai dự án
```

---

## 2. Các Lệnh CLI Chính

Mọi lệnh chạy trong môi trường ảo Python đã được thiết lập sẵn:

### A. Tra cứu Tiền lệ Văn bản Cũ (`search_history.py`)
Tìm kiếm theo từ khóa có dấu hoặc không dấu trong toàn bộ kho 6.800+ văn bản lịch sử:
```powershell
.venv\Scripts\python.exe tools/search_history.py --q "ghi hình" --type all --limit 5
.venv\Scripts\python.exe tools/search_history.py --q "kinh phí" --type di --limit 5
```

### B. Sinh Tài liệu Word và PDF Cố định (`build_doc.py`)
Biên dịch file dữ liệu JSON thành tài liệu Word `.docx` và tự động xuất bản PDF:
```powershell
.venv\Scripts\python.exe tools/build_doc.py --input "drafts/2026-11/cv_phuc_dap.json" --output "drafts/2026-11/cv_phuc_dap.docx" --pdf
```

### C. Kiểm định Thể thức & Xuất ảnh Soi trực quan (`inspect_pdf.py`)
Kiểm tra tự động kích thước A4, chống rớt chữ `NAM`, đánh số trang, chống mồ côi chữ ký và render ảnh PNG:
```powershell
.venv\Scripts\python.exe tools/inspect_pdf.py "drafts/2026-11/cv_phuc_dap.pdf" --render-dir "drafts/2026-11/renders"
```

### D. So sánh Bản Word Người dùng Đã Sửa (`diff_draft.py`)
Soi các điểm khác biệt khi người dùng tự tay sửa file Word để AI học theo:
```powershell
.venv\Scripts\python.exe tools/diff_draft.py --ai "drafts/2026-11/ban_ai.docx" --final "drafts/2026-11/ban_sua.docx"
```

---

## 3. Mẫu Câu Lệnh Giao Việc Nhanh Hằng Ngày Cho AI

Chuyên viên chỉ cần gửi văn bản đến hoặc mô tả yêu cầu trong khung chat theo các mẫu sau:

### Mẫu 1: Phúc đáp Công văn Đến
> *"Có công văn đến số 10-11/CV2026 của Cty TNHH Truyền hình Kết Nối về việc mời ThS. Trương Nhật Khuê Tường tham gia ghi hình chương trình tư vấn sức khỏe. Hãy tra cứu tiền lệ tương tự của Khoa, soạn công văn phúc đáp đồng ý cử viên chức tham gia, xuất file DOCX/PDF vào `drafts/2026-11/` và kiểm định thể thức."*

### Mẫu 2: Soạn Tờ trình Nội dung Mới (Trình Ban Giám hiệu)
> *"Hãy tra cứu văn phong Tờ trình xin kinh phí của Khoa và soạn Tờ trình mới: 'Xin phê duyệt chủ trương và kinh phí tổ chức Hội thảo chuyên đề ứng dụng Trí tuệ nhân tạo (AI) trong công tác Y tế Công cộng năm 2026'. Kèm bảng dự trù kinh phí 4-5 hạng mục, có ô DUYỆT BAN GIÁM HIỆU căn giữa ở dưới."*

### Mẫu 3: Soạn Kế hoạch Dài Nhiều Trang kèm Bảng biểu Khổ ngang
> *"Soạn Kế hoạch: 'Tổ chức đợt Thực tế cộng đồng cho sinh viên khóa 2026 tại tỉnh Đồng Nai'. Phần đầu khổ dọc gồm mục đích, thời gian, tiến độ; trang cuối chuyển sang khổ ngang (Landscape) chứa Phụ lục bảng phân công giảng viên hướng dẫn nhiều cột. Đánh số trang tự động từ trang 2."*

### Mẫu 4: Soạn Giấy Giới Thiệu
> *"Làm Giấy giới thiệu cho học viên Lê Văn Hùng, lớp CK2-2024 đến Trung tâm Kiểm soát bệnh tật TP.HCM (HCDC) thu thập số liệu luận văn chuyên khoa. Header cấp Trường UMP, chức danh ký TL. Hiệu trưởng / Trưởng khoa."*

---

## 4. Cách Dạy AI Hiểu Ý Hơn Mỗi Ngày (Cơ chế Memory Loop)

Chuyên viên có thể "huấn luyện" AI ghi nhớ thói quen soạn thảo qua 2 cách đơn giản:

### Cách 1: Nhắc nhở Trực tiếp trên Chat
> *"Hãy ghi nhớ: Từ nay chuyên viên soạn thảo chính của mảng Quản lý Đào tạo là cô Nguyễn Thị Tuyết Nhung, mã lưu hồ sơ tại nơi nhận là `QLĐT_NTTN`."*  
> → AI sẽ tự động ghi vào `knowledge_base/memory/user_preferences.md` để tự áp dụng cho mọi văn bản sau này.

### Cách 2: Gửi File Word Đã Chỉnh Sửa Tay
> *"Tôi vừa chỉnh sửa lại câu chữ trong file `drafts/2026-11/ca1_phuc_dap_ghi_hinh_htv7.docx`. Hãy chạy so sánh và ghi nhớ bài học kinh nghiệm để lần sau viết chuẩn hơn."*  
> → AI sẽ chạy `diff_draft.py`, bóc tách các điểm sửa và tự đúc kết thành bài học trong `knowledge_base/memory/lessons_learned.md`.
