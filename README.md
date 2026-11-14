# HỆ THỐNG TRỢ LÝ AI SOẠN THẢO VĂN BẢN ĐI (YTCC DOC COPILOT)
**Khoa Y Tế Công Cộng – Đại học Y Dược TP. Hồ Chí Minh**

Hệ thống được thiết kế theo chuẩn **Antigravity Best Practice**, chuyên dụng hỗ trợ soạn thảo văn bản đi chuẩn Nghị định 30/2020/NĐ-CP, tích hợp cơ sở tri thức mẫu hơn 4.000 văn bản thực tế của Khoa YTCC giai đoạn 2023 - 2026.

---

## 1. CẤU TRÚC THƯ MỤC HỆ THỐNG

```
D:\TH\vanban-ytcc\
│
├── .agents/                                # Cấu hình AI Antigravity
│   ├── rules/
│   │   ├── gemini.md                       # Thể thức chuẩn NĐ 30/2020, font chữ, lề, xưng hô
│   │   ├── recipient_matrix.md             # Ma trận nơi nhận, kính gửi các phòng ban ĐHYD & đối tác
│   │   └── authority_rules.md              # Quy tắc thẩm quyền ký (Trưởng khoa, Phó Trưởng khoa)
│   └── skills/
│       ├── ytcc-classify-doc/SKILL.md     # Kỹ năng phân loại và gợi ý loại văn bản
│       ├── ytcc-reply-incoming/SKILL.md   # Kỹ năng đọc hiểu văn bản đến & soạn phúc đáp
│       ├── ytcc-draft-writer/SKILL.md     # Kỹ năng soạn thảo chi tiết văn phong y tế
│       └── ytcc-docx-export/SKILL.md      # Kỹ năng xuất file Word .docx & PDF
│
├── knowledge_base/                         # Cơ sở tri thức mẫu
│   ├── templates/                          # 5 mẫu Word (.docx) chuẩn thể thức NĐ 30
│   │   ├── Mau_To_trinh.docx
│   │   ├── Mau_Cong_van.docx
│   │   ├── Mau_Giay_gioi_thieu.docx
│   │   ├── Mau_Ke_hoach.docx
│   │   └── Mau_Bao_cao.docx
│   ├── metadata_index/                     # Dữ liệu tra cứu lịch sử 2023 - 2026
│   │   ├── cv_di_history.json              # 2.960 văn bản đi đã phân loại & nơi nhận
│   │   ├── cv_den_history.json             # 3.873 văn bản đến (cơ quan gửi, số ký hiệu, trích yếu)
│   │   └── recipient_summary.json          # Thống kê phân bổ nơi nhận
│   └── sample_pdfs/                        # 38 file PDF mẫu tải từ Google Drive (Tờ trình, CV, GGT, KH...)
│
├── drafts/                                 # Thư mục lưu bản thảo Word & PDF đang soạn
│   └── YYYY-MM/                            # Tự động chia theo tháng (VD: 2026-11/)
│
└── tools/                                  # Công cụ tự động hóa
    ├── generate_document.ps1               # Tạo bản thảo Word .docx từ mẫu
    ├── export_pdf.ps1                      # 1-Click chuyển đổi .docx sang .pdf
    ├── search_history.ps1                  # Tra cứu nhanh văn bản cũ tương tự
    └── download_samples.ps1                # Tải bổ sung file PDF mẫu từ Cloud CSDL
```

---

## 2. HƯỚNG DẪN SỬ DỤNG HÀNG NGÀY VỚI ANTIGRAVITY

### Kịch bản 1: Chưa biết nên làm loại văn bản gì
- **Bạn chỉ cần chat:**
  > *"Tôi cần gửi Trường xin cấp kinh phí 20 triệu để bảo trì hệ thống máy lạnh phòng thực hành, nên làm văn bản gì và gửi ai?"*
- **AI sẽ tự động:**
  1. Phân loại thành **TỜ TRÌNH**.
  2. Gợi ý Kính gửi: **Ban Giám hiệu (qua Phòng Quản trị - Thiết bị và Phòng Tài chính - Kế toán)**.
  3. Gợi ý Nơi nhận: Ban Giám hiệu, Phòng QTTB, Phòng TCKT, BCN Khoa, Lưu VT.
  4. Xác định người ký: **Trưởng khoa PGS. TS. Nguyễn Duy Phong**.
  5. Soạn khung nội dung và xuất file Word `.docx` sẵn sàng.

---

### Kịch bản 2: Dùng Văn bản đến để soạn trả lời Văn bản đi
- **Bạn chỉ cần chat:**
  > *"Trường vừa gửi Công văn số 407/TCNS ngày 10/11/2026 về việc lấy ý kiến góp ý Dự thảo Quy định bổ nhiệm chức danh quản lý. Hãy soạn công văn trả lời thống nhất với dự thảo."*
- **AI sẽ tự động:**
  1. Trích dẫn chuẩn: *"Căn cứ Công văn số 407/TCNS ngày 10/11/2026 của Đại học Y Dược TP. Hồ Chí Minh về việc..."*
  2. Chọn hình thức: **CÔNG VĂN** (Số ký hiệu: `.../YTCC-VP`).
  3. Kính gửi: **Ban Giám hiệu (qua Phòng Tổ chức Cán bộ)**.
  4. Lập luận nội dung góp ý theo văn phong hành chính chuẩn mực.
  5. Sinh file Word `.docx` lưu vào `drafts/2026-11/`.

---

### Kịch bản 3: Tra cứu tiền lệ văn bản cũ trong lịch sử Khoa
- **Chạy lệnh nhanh trong terminal:**
  ```powershell
  powershell -File "D:\TH\vanban-ytcc\tools\search_history.ps1" -Keyword "máy lạnh" -Scope di
  ```
  *(Sẽ tìm thấy ngay các tờ trình, công văn về máy lạnh năm 2023, 2024 để tham khảo cách viết)*.

---

### Kịch bản 4: Xuất file Word sang PDF
- Sau khi chỉnh sửa xong bản thảo Word:
  ```powershell
  powershell -File "D:\TH\vanban-ytcc\tools\export_pdf.ps1" -docxPath "D:\TH\vanban-ytcc\drafts\2026-11\Draft_To_trinh_....docx"
  ```
  *(File PDF sẽ được tạo ngay cạnh file Word, giữ nguyên 100% định dạng)*.
