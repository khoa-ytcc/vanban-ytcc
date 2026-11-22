# HỆ THỐNG TỰ ĐỘNG HÓA VĂN BẢN HÀNH CHÍNH KHOA YTCC (V2.5)
> Giải pháp soạn thảo, tra cứu toàn văn FTS5, thẩm định tự động và xuất bản tài liệu chuẩn Nghị định 30/2020/NĐ-CP dành riêng cho Khoa Y tế Công cộng – Đại học Y Dược TP.HCM.

---

## 1. Cấu trúc Thư mục v2.5
```text
vanban-ytcc/
├── .agents/
│   ├── rules/                # Bộ quy tắc vận hành, thể thức, thẩm quyền, an toàn
│   └── skills/               # 4 kỹ năng tác nghiệp: Intake -> Draft -> QA -> Learn
├── audit/
│   ├── p2_tests/             # Dữ liệu nghiệm thu 6 test case chuẩn hóa P2
│   ├── p25_tests/            # Thư mục kiểm thử hồi quy v2.5 (được gitignore)
│   └── scripts/              # Kịch bản kiểm thử tự động (run_regression.py)
├── drafts/
│   └── YYYY-MM/              # Thư mục vụ việc: incoming/, v1, v2, final, renders/
├── knowledge_base/
│   ├── golden_jsons/         # Kho 5 bản mẫu vàng chuẩn hóa (0 ERROR)
│   ├── memory/               # Bộ nhớ dài hạn v2: user_preferences, lessons_learned, citations_bank
│   ├── metadata_index/       # SQLite FTS5 (ytcc_history.db: metadata + toàn văn) & JSON lịch sử
│   ├── sample_pdfs/          # Kho 800 file PDF thực tế (S0 - Nguồn chân lý gốc)
│   └── specs/                # Bảng đặc tả thể thức (ytcc_format_spec.md) & Schema (doc_schema.md)
├── tools/
│   ├── ytcc.py               # Unified CLI hợp nhất (build, batch, ingest, search, diff, sync, promote)
│   ├── build_doc.py          # Core Engine JSON -> Word DOCX (Inline Markdown, Schema Validator)
│   ├── lint_doc.py           # Linter hành chính (bảng tính, lịch thực tế, thể thức, placeholder)
│   ├── export_pdf.ps1        # Script xuất PDF đơn lẻ & batch an toàn qua Word COM (UTF-8 BOM)
│   ├── inspect_pdf.py        # Kiểm định thể thức PDF & Telemetry lố trang (target_one_page)
│   ├── ingest_incoming.py    # Tiếp nhận & tiền xử lý văn bản đến (trích text, render ảnh)
│   ├── search_history.py     # Tra cứu FTS5 (Metadata & Toàn văn kèm snippet ngữ cảnh)
│   ├── sync_kb.py            # Đồng bộ tăng dần kho tri thức vào SQLite FTS5
│   ├── fetch_mysql_delta.ps1 # Script phụ đồng bộ delta từ CSDL MySQL (nếu cấu hình)
│   └── diff_draft.py         # So sánh khác biệt giữa bản AI tạo và bản người dùng đã sửa
├── AGENTS.md                 # Quy chuẩn vận hành AI, phân vai & an toàn tiến trình v2.5
├── GEMINI.md                 # Ngữ cảnh nạp nhanh cho trợ lý AI v2.5
└── PLAN.md                   # Kế hoạch & tiến độ triển khai dự án v2.5
```

---

## 2. Hướng Dẫn Sử Dụng Unified CLI (`tools/ytcc.py`)

Mọi thao tác quản lý và vận hành văn bản đều được thực hiện qua công cụ dòng lệnh hợp nhất `tools/ytcc.py`:

### A. Soạn thảo, Kiểm định & Xuất PDF (`build`)
Kiểm tra Schema -> Chạy Linter -> Dựng DOCX -> Xuất PDF -> Kiểm định tự động:
```powershell
.venv\Scripts\python.exe tools/ytcc.py build "drafts/2026-11/case_01/v1.json" --pdf
```
- Bật cờ `--strict-final`: Nghiệm thu gắt gao, chặn hoàn toàn nếu còn placeholder.
- Bật cờ `--force`: Bỏ qua cảnh báo linter để tiếp tục xuất file khi cần.

### B. Xuất PDF Hàng loạt Siêu tốc qua 1 Phiên Word COM (`batch`)
```powershell
.venv\Scripts\python.exe tools/ytcc.py batch "audit/p25_tests/batch_p2/batch_tasks.json"
```

### C. Tiếp nhận Văn bản Đến & Tiền xử lý (`ingest`)
Tạo thư mục vụ việc, copy file gốc, trích xuất text và render ảnh PNG:
```powershell
.venv\Scripts\python.exe tools/ytcc.py ingest --file "duong/dan/CV_Den.pdf" --case "phuc_dap_tap_huan"
```

### D. Tra cứu Tiền lệ & Toàn văn FTS5 (`search`)
Hỗ trợ tìm kiếm theo từ khóa có dấu/không dấu, hiển thị đoạn trích (snippet):
```powershell
.venv\Scripts\python.exe tools/ytcc.py search "Nghị định 30" --mode fulltext --limit 3
.venv\Scripts\python.exe tools/ytcc.py search "dự toán" --mode all --limit 5
```

### E. So sánh Khác biệt Bản sửa tay (`diff`)
```powershell
.venv\Scripts\python.exe tools/ytcc.py diff --original "drafts/.../v1.docx" --revised "drafts/.../final.docx"
```

### F. Đồng bộ Tăng dần Kho Tri thức (`sync`)
Chỉ cập nhật các file mới hoặc vừa sửa trong < 1-2 giây:
```powershell
.venv\Scripts\python.exe tools/ytcc.py sync
```

### G. Thăng hạng Bản mẫu Vàng (`promote`)
Kiểm tra đạt 0 ERROR và lưu mẫu chuẩn vào `knowledge_base/golden_jsons/`:
```powershell
.venv\Scripts\python.exe tools/ytcc.py promote "drafts/.../final.json" --name "to_trinh_mau_moi.json"
```
