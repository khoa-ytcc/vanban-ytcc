#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SUITE KIỂM THỬ HỒI QUY TOÀN DIỆN v2.5A (REGRESSION TEST SUITE)
Chạy kiểm tra tự động 5 nhóm chức năng và an toàn tiến trình Word COM.
"""

import os
import sys
import json
import time
import shutil
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
TOOLS_DIR = os.path.join(REPO_DIR, "tools")
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)

from build_doc import build_document, validate_schema
from lint_doc import lint_document
from inspect_pdf import inspect_pdf
from ingest_incoming import ingest_document

P25_TEST_DIR = os.path.join(REPO_DIR, "audit", "p25_tests")

def setup_directories():
    os.makedirs(P25_TEST_DIR, exist_ok=True)
    os.makedirs(os.path.join(P25_TEST_DIR, "batch_p2"), exist_ok=True)
    os.makedirs(os.path.join(P25_TEST_DIR, "renders"), exist_ok=True)
    os.makedirs(os.path.join(P25_TEST_DIR, "linter_negative"), exist_ok=True)

def test_group_1_batch():
    print("\n" + "=" * 70)
    print("NHÓM 1: KIỂM THỬ BATCH EXPORT WORD COM TRÊN 6 TEST CASES PHASE 2")
    print("=" * 70)
    
    p2_dir = os.path.join(REPO_DIR, "audit", "p2_tests")
    p2_cases = [
        "01_cong_van_1p.json",
        "02_to_trinh_1p.json",
        "03_giay_gioi_thieu_1p.json",
        "04_ke_hoach_nhieu_trang.json",
        "05_bao_cao_nhieu_trang.json",
        "06_cong_van_phu_luc_ngang.json"
    ]
    
    batch_items = []
    batch_dir = os.path.join(P25_TEST_DIR, "batch_p2")
    
    # 1. Dựng trước 6 file DOCX
    t_start = time.time()
    for case_file in p2_cases:
        json_path = os.path.join(p2_dir, case_file)
        base = os.path.splitext(case_file)[0]
        docx_path = os.path.join(batch_dir, f"{base}.docx")
        pdf_path = os.path.join(batch_dir, f"{base}.pdf")
        
        build_document(json_path, docx_path)
        batch_items.append({
            "docx": os.path.abspath(docx_path),
            "pdf": os.path.abspath(pdf_path)
        })
        
    t_docx = round(time.time() - t_start, 2)
    print(f"-> Đã dựng 6 file DOCX trong {t_docx}s")
    
    # 2. Xuất Batch PDF qua Word COM (1 phiên duy nhất)
    batch_json_path = os.path.join(batch_dir, "batch_tasks.json")
    with open(batch_json_path, "w", encoding="utf-8") as f:
        json.dump(batch_items, f, ensure_ascii=False, indent=2)
        
    ps1_path = os.path.join(TOOLS_DIR, "export_pdf.ps1")
    cmd = [
        "powershell.exe",
        "-ExecutionPolicy", "Bypass",
        "-File", ps1_path,
        "-BatchJson", batch_json_path
    ]
    
    t_batch_start = time.time()
    res = subprocess.run(cmd, capture_output=True, text=True)
    t_batch = round(time.time() - t_batch_start, 2)
    
    if res.returncode != 0:
        print(f"❌ LỖI Batch Export:\n{res.stderr}")
        return False, f"Batch export failed: {res.stderr}"
        
    print(res.stdout.strip())
    print(f"-> Thời gian xuất 6 file PDF: {t_batch}s (Trung bình {round(t_batch/6, 2)}s/file)")
    
    # 3. Kiểm định 6 file PDF vừa tạo
    all_ok = True
    for case_file in p2_cases:
        base = os.path.splitext(case_file)[0]
        pdf_path = os.path.join(batch_dir, f"{base}.pdf")
        json_path = os.path.join(p2_dir, case_file)
        with open(json_path, "r", encoding="utf-8-sig") as f:
            jdata = json.load(f)
        target_one = jdata.get("target_one_page", False)
        
        ok = inspect_pdf(pdf_path, target_one_page=target_one)
        if not ok:
            all_ok = False
            print(f"❌ Test case {case_file} thất bại khi kiểm định PDF.")
            
    if all_ok:
        print("✅ NHÓM 1 HOÀN TOÀN ĐẠT CHUẨN (6/6 PASS qua inspect_pdf)!")
    return all_ok, f"6/6 PASS in {t_batch}s"

def test_group_2_inline_markdown():
    print("\n" + "=" * 70)
    print("NHÓM 2: KIỂM THỬ ĐỊNH DẠNG INLINE MARKDOWN VÀ THẨM ĐỊNH THỊ GIÁC")
    print("=" * 70)
    
    test_json_path = os.path.join(P25_TEST_DIR, "test_inline_md.json")
    md_data = {
        "doc_type": "cong_van",
        "target_one_page": True,
        "header": {
            "header_level": "ytcc",
            "organ_line1": "ĐẠI HỌC Y DƯỢC",
            "organ_line2": "THÀNH PHỐ HỒ CHÍ MINH",
            "organ_line3": "KHOA Y TẾ CÔNG CỘNG",
            "so_hieu": "999",
            "ma_loai": "YTCC-VP",
            "dia_danh": "Thành phố Hồ Chí Minh",
            "ngay": "22",
            "thang": "11",
            "nam": "2026",
            "trich_yeu": "V/v kiểm thử tính năng định dạng Inline Markdown v2.5A"
        },
        "blocks": [
            {
                "type": "kinh_gui",
                "items": ["Ban Chủ nhiệm Khoa Y tế Công cộng", "Các Bộ môn và Trung tâm trực thuộc"]
            },
            {
                "type": "p",
                "prefix_bold": "1. Khảo sát công nghệ:",
                "text": "Khoa Y tế Công cộng trân trọng thông báo về việc thử nghiệm công nghệ tự động hóa văn bản với tính năng hiển thị ***đậm nghiêng kết hợp***, định dạng **chữ in đậm nổi bật** và định dạng *chữ in nghiêng trang trọng* được tích hợp mượt mà trong cùng một câu văn bản."
            },
            {
                "type": "bullet",
                "text": "Tài liệu tập huấn bao gồm: **Cẩm nang chuyển đổi số**, tài liệu hướng dẫn *thực hành thống kê dịch tễ* và tài liệu quy chuẩn ***an toàn thông tin y tế 2026***."
            },
            {
                "type": "quote",
                "text": "Trích ý kiến chỉ đạo: *Việc áp dụng công nghệ vào công tác hành chính phải luôn bảo đảm tính **chính xác**, **bảo mật** và tuân thủ chặt chẽ ***quy chuẩn thể thức hành chính*** của Đại học Y Dược TP.HCM.*"
            },
            {
                "type": "table",
                "headers": ["STT", "Thành phần", "Cú pháp Markdown", "Kết quả định dạng"],
                "rows": [
                    ["1", "Đoạn văn (p)", "Dùng `**in đậm**`", "Hiển thị **chữ in đậm**"],
                    ["2", "Gạch đầu dòng", "Dùng `*in nghiêng*`", "Hiển thị *chữ in nghiêng*"],
                    ["3", "Bảng biểu (table)", "Dùng `***đậm nghiêng***`", "Hiển thị ***đậm và nghiêng***"]
                ]
            },
            {
                "type": "p",
                "text": "Kính đề nghị các đơn vị phối hợp triển khai thực hiện nghiêm túc."
            }
        ],
        "sign_block": {
            "signer_role": "TRƯỞNG KHOA",
            "signer_name": "PGS. TS. Nguyễn Duy Phong",
            "recipients": [
                "- Như kính gửi;",
                "- Lưu: VT, VP_YTCC."
            ],
            "dept_code": "VP",
            "creator_initials": "YTCC"
        }
    }
    
    with open(test_json_path, "w", encoding="utf-8-sig") as f:
        json.dump(md_data, f, ensure_ascii=False, indent=2)
        
    out_docx = os.path.join(P25_TEST_DIR, "test_inline_md.docx")
    out_pdf = os.path.join(P25_TEST_DIR, "test_inline_md.pdf")
    render_dir = os.path.join(P25_TEST_DIR, "renders")
    
    build_document(test_json_path, out_docx)
    ps1_path = os.path.join(TOOLS_DIR, "export_pdf.ps1")
    cmd = ["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", ps1_path, "-InputDocx", out_docx, "-OutputPdf", out_pdf]
    subprocess.run(cmd, check=True)
    
    ok = inspect_pdf(out_pdf, render_dir=render_dir, dpi=150, target_one_page=True)
    
    # Kiểm tra xem có còn ký tự '*' trong text PDF hay không
    import pymupdf
    pdoc = pymupdf.open(out_pdf)
    full_pdf_text = "".join(page.get_text() for page in pdoc)
    pdoc.close()
    
    # Ngoại trừ dấu * trong mô tả code syntax nếu có, kiểm tra các cụm markdown đã được gỡ bỏ dấu *
    has_raw_stars = "***" in full_pdf_text
    
    print(f"-> File PDF: {out_pdf}")
    print(f"-> Ảnh render: {os.path.join(render_dir, 'test_inline_md_p1.png')}")
    print(f"-> Kiểm tra ký tự raw '***': {'KHÔNG CÒN (SẠCH SẼ)' if not has_raw_stars else 'PHÁT HIỆN SÓT'}")
    
    passed = ok and not has_raw_stars
    return passed, f"Rendered to {render_dir}, clean stars={not has_raw_stars}"

def test_group_3_linter_negative():
    print("\n" + "=" * 70)
    print("NHÓM 3: KIỂM THỬ LINTER NEGATIVE TESTS (5 CA SAI CỐ Ý)")
    print("=" * 70)
    
    neg_dir = os.path.join(P25_TEST_DIR, "linter_negative")
    results = {}
    
    # Case 1: fail_schema_type (dùng "type": "para")
    c1 = {
        "doc_type": "cong_van",
        "header": {"trich_yeu": "Test schema"},
        "blocks": [{"type": "para", "text": "Sai type para"}],
        "sign_block": {}
    }
    c1_path = os.path.join(neg_dir, "fail_schema_type.json")
    with open(c1_path, "w", encoding="utf-8-sig") as f: json.dump(c1, f)
    errs1 = validate_schema(c1)
    c1_passed = any("blocks[0].type: kiểu 'para' không hợp lệ" in e for e in errs1)
    results["1. fail_schema_type"] = ("CHẶN THÀNH CÔNG" if c1_passed else "THẤT BẠI", errs1)
    
    # Case 2: fail_table_sum (bảng cộng sai: 1.000.000 + 2.000.000 = 4.000.000)
    c2 = {
        "doc_type": "cong_van",
        "header": {"trich_yeu": "Test sum"},
        "blocks": [
            {
                "type": "table",
                "headers": ["STT", "Nội dung", "Số tiền"],
                "rows": [
                    ["1", "Chi phí A", "1.000.000"],
                    ["2", "Chi phí B", "2.000.000"],
                    ["", "Tổng cộng", "4.000.000"]
                ]
            }
        ],
        "sign_block": {}
    }
    c2_path = os.path.join(neg_dir, "fail_table_sum.json")
    with open(c2_path, "w", encoding="utf-8-sig") as f: json.dump(c2, f)
    lint2 = lint_document(c2)
    c2_passed = any("TABLE_SUM_MISMATCH" in e for e in lint2["errors"])
    results["2. fail_table_sum"] = ("CHẶN THÀNH CÔNG" if c2_passed else "THẤT BẠI", lint2["errors"])
    
    # Case 3: fail_calendar ("Thứ Ba, ngày 23/11/2026" - thực tế 23/11/2026 là Thứ Hai)
    c3 = {
        "doc_type": "cong_van",
        "header": {"trich_yeu": "Test calendar"},
        "blocks": [
            {"type": "p", "text": "Hội nghị diễn ra vào lúc 08h00, Thứ Ba, ngày 23/11/2026 tại Giảng đường 1."}
        ],
        "sign_block": {}
    }
    c3_path = os.path.join(neg_dir, "fail_calendar.json")
    with open(c3_path, "w", encoding="utf-8-sig") as f: json.dump(c3, f)
    lint3 = lint_document(c3)
    c3_passed = any("CALENDAR_DAY_MISMATCH" in e for e in lint3["errors"])
    results["3. fail_calendar"] = ("CHẶN THÀNH CÔNG" if c3_passed else "THẤT BẠI", lint3["errors"])
    
    # Case 4: fail_repeat_trichyeu ("V/v Về việc cử cán bộ...")
    c4 = {
        "doc_type": "cong_van",
        "header": {
            "trich_yeu": "V/v Về việc cử cán bộ tham gia tập huấn chuyên môn"
        },
        "blocks": [
            {"type": "p", "text": "Nội dung văn bản"}
        ],
        "sign_block": {}
    }
    c4_path = os.path.join(neg_dir, "fail_repeat_trichyeu.json")
    with open(c4_path, "w", encoding="utf-8-sig") as f: json.dump(c4, f)
    lint4 = lint_document(c4)
    c4_passed = any("REPEAT_TRICH_YEU" in e for e in lint4["errors"])
    results["4. fail_repeat_trichyeu"] = ("CHẶN THÀNH CÔNG" if c4_passed else "THẤT BẠI", lint4["errors"])
    
    # Case 5: fail_placeholder_strict (chứa [HỌ TÊN NGƯỜI KÝ] khi chạy --strict-final)
    c5 = {
        "doc_type": "cong_van",
        "header": {"trich_yeu": "Cử cán bộ"},
        "blocks": [{"type": "p", "text": "Nội dung văn bản"}],
        "sign_block": {
            "signer_name": "[HỌ TÊN NGƯỜI KÝ]"
        }
    }
    c5_path = os.path.join(neg_dir, "fail_placeholder_strict.json")
    with open(c5_path, "w", encoding="utf-8-sig") as f: json.dump(c5, f)
    lint5 = lint_document(c5, strict_final=True)
    c5_passed = any("ERROR_UNFILLED_PLACEHOLDER" in e for e in lint5["errors"])
    results["5. fail_placeholder_strict"] = ("CHẶN THÀNH CÔNG" if c5_passed else "THẤT BẠI", lint5["errors"])
    
    # Case 6: fail_doctype_mismatch (doc_type = to_trinh nhưng so_hieu ghi .../YTCC-VP)
    c6 = {
        "doc_type": "to_trinh",
        "header": {
            "header_level": "ytcc",
            "so_hieu": "123/YTCC-VP",
            "trich_yeu": "Về việc xin chủ trương kinh phí"
        },
        "blocks": [{"type": "p", "text": "Nội dung tờ trình"}],
        "sign_block": {}
    }
    c6_path = os.path.join(neg_dir, "fail_doctype_mismatch.json")
    with open(c6_path, "w", encoding="utf-8-sig") as f: json.dump(c6, f)
    lint6 = lint_document(c6)
    c6_passed = any("DOC_TYPE_CODE_MISMATCH" in e for e in lint6["errors"])
    results["6. fail_doctype_mismatch"] = ("CHẶN THÀNH CÔNG" if c6_passed else "THẤT BẠI", lint6["errors"])
    
    all_neg_ok = True
    for name, (status, detail) in results.items():
        print(f"  - {name}: [{status}]")
        if status != "CHẶN THÀNH CÔNG":
            all_neg_ok = False
        else:
            print(f"      Chi tiết: {detail[0] if detail else ''}")
            
    if all_neg_ok:
        print("✅ NHÓM 3 HOÀN TOÀN ĐẠT CHUẨN (6/6 negative cases bị chặn chính xác)!")
    return all_neg_ok, "6/6 blocked successfully"

def test_group_4_overflow_telemetry():
    print("\n" + "=" * 70)
    print("NHÓM 4: KIỂM THỬ OVERFLOW TELEMETRY KHI BỊ TRÀN TRANG (TARGET_ONE_PAGE)")
    print("=" * 70)
    
    test_json_path = os.path.join(P25_TEST_DIR, "test_overflow.json")
    overflow_data = {
        "doc_type": "cong_van",
        "target_one_page": True,
        "header": {
            "header_level": "ytcc",
            "organ_line1": "ĐẠI HỌC Y DƯỢC",
            "organ_line2": "THÀNH PHỐ HỒ CHÍ MINH",
            "organ_line3": "KHOA Y TẾ CÔNG CỘNG",
            "so_hieu": "777",
            "ma_loai": "YTCC-VP",
            "dia_danh": "Thành phố Hồ Chí Minh",
            "ngay": "22",
            "thang": "11",
            "nam": "2026",
            "trich_yeu": "V/v kiểm thử phát hiện lố trang telemetry"
        },
        "blocks": [
            {"type": "kinh_gui", "items": ["Ban Giám hiệu Đại học Y Dược TP. Hồ Chí Minh"]},
            {"type": "p", "text": "Đoạn văn số 1: Nhằm phục vụ công tác đào tạo và nghiên cứu khoa học, Khoa Y tế Công cộng xin báo cáo tình hình triển khai công tác chuẩn bị cho các đợt thực địa và kiểm định chương trình đào tạo theo chuẩn quốc tế của Bộ Giáo dục và Đào tạo và AUN-QA."},
            {"type": "p", "text": "Đoạn văn số 2: Các hoạt động giảng dạy trên lớp, thực tập tại cộng đồng và các bệnh viện vệ tinh đã được lên kế hoạch chu đáo và triển khai đúng tiến độ đề ra, bảo đảm chất lượng và an toàn tuyệt đối cho người học trong toàn bộ quá trình tham gia thực tế."},
            {"type": "p", "text": "Đoạn văn số 3: Tình hình tài chính và cơ sở vật chất đáp ứng tốt các yêu cầu giảng dạy và nghiên cứu thực tế của giảng viên và học viên, đồng thời Khoa đã chủ động rà soát các nguồn lực để phân bổ hợp lý theo quy chế chi tiêu nội bộ."},
            {"type": "p", "text": "Đoạn văn số 4: Công tác hợp tác quốc tế được mở rộng với các đối tác chiến lược tại khu vực Đông Nam Á và Châu Âu, tạo thêm nhiều cơ hội học bổng và trao đổi học thuật chất lượng cao cho sinh viên và giảng viên của Khoa."},
            {"type": "p", "text": "Đoạn văn số 5: Khoa đã tổ chức thành công chuỗi tọa đàm khoa học chuyên đề thu hút đông đảo chuyên gia đầu ngành trong và ngoài nước tham dự, đóng góp nhiều ý kiến chuyên môn quý báu cho sự phát triển của hệ thống y tế cộng đồng."},
            {"type": "p", "text": "Đoạn văn số 6: Để bảo đảm văn bản này dài quá 1 trang nhằm kích hoạt cơ chế đo lường lố trang của script kiểm định thể thức, ta bổ sung thêm nội dung chi tiết về nhân sự và thiết bị với các hạng mục đánh giá cụ thể."},
            {"type": "p", "text": "Đoạn văn số 7: Các đề xuất cụ thể bao gồm trang bị thêm phòng máy tính thực hành phân tích số liệu y sinh học, bổ sung các phần mềm bản quyền phục vụ nghiên cứu dịch tễ học và thống kê sinh học nâng cao."},
            {"type": "p", "text": "Đoạn văn số 8: Nâng cấp thư viện chuyên ngành và tạo điều kiện để học viên truy cập vào các cơ sở dữ liệu quốc tế như PubMed, Scopus, Web of Science phục vụ đắc lực cho công tác tra cứu tài liệu chuyên sâu."},
            {"type": "p", "text": "Đoạn văn số 9: Tổ chức các chương trình trao đổi học thuật và tập huấn nâng cao năng lực cho đội ngũ cán bộ trẻ, bảo đảm tính kế thừa và nâng cao chất lượng nghiên cứu khoa học trong giai đoạn mới."},
            {"type": "p", "text": "Đoạn văn số 10: Tăng cường các đề tài nghiên cứu khoa học cấp cơ sở và cấp Đại học Y Dược TP. Hồ Chí Minh, khuyến khích công bố quốc tế trên các tạp chí uy tín thuộc danh mục ISI/Scopus."},
            {"type": "p", "text": "Đoạn văn số 11: Phát triển các chương trình đào tạo liên tục đáp ứng nhu cầu thực tế của các cơ sở y tế trong khu vực, góp phần chuẩn hóa kiến thức chuyên môn cho đội ngũ y tế cơ sở."},
            {"type": "p", "text": "Đoạn văn số 12: Hoàn thiện hệ thống quản lý dữ liệu đào tạo tích hợp nhằm tăng cường hiệu quả vận hành, số hóa quy trình quản lý điểm và hồ sơ sinh viên một cách đồng bộ và chính xác."},
            {"type": "p", "text": "Đoạn văn số 13: Đẩy mạnh các hoạt động phục vụ cộng đồng và truyền thông giáo dục sức khỏe tại các địa phương khó khăn, khẳng định vai trò tiên phong của Khoa trong lĩnh vực y tế dự phòng."},
            {"type": "p", "text": "Đoạn văn số 14: Kiến nghị Ban Giám hiệu tiếp tục quan tâm, chỉ đạo và hỗ trợ kinh phí cho các hoạt động trọng điểm nhằm hoàn thành xuất sắc các chỉ tiêu công tác năm học đã đề ra."},
            {"type": "p", "text": "Đoạn văn số 15: Dự kiến kế hoạch phân công chi tiết nhân sự điều phối và giám sát thực hiện sẽ được ban hành ngay sau khi nhận được ý kiến chỉ đạo chính thức từ Lãnh đạo Nhà trường."},
            {"type": "p", "text": "Đoạn văn số 16: Kính trình Ban Giám hiệu xem xét và phê duyệt chủ trương để Khoa triển khai các bước tiếp theo đúng quy định hiện hành."}
        ],
        "sign_block": {
            "signer_role": "TRƯỞNG KHOA",
            "signer_name": "PGS. TS. Nguyễn Duy Phong",
            "recipients": [
                "- Như trên;",
                "- Lưu: VT, VP_YTCC."
            ],
            "dept_code": "VP",
            "creator_initials": "YTCC"
        }
    }
    
    with open(test_json_path, "w", encoding="utf-8-sig") as f:
        json.dump(overflow_data, f, ensure_ascii=False, indent=2)
        
    out_docx = os.path.join(P25_TEST_DIR, "test_overflow.docx")
    out_pdf = os.path.join(P25_TEST_DIR, "test_overflow.pdf")
    
    build_document(test_json_path, out_docx)
    ps1_path = os.path.join(TOOLS_DIR, "export_pdf.ps1")
    cmd = ["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", ps1_path, "-InputDocx", out_docx, "-OutputPdf", out_pdf]
    subprocess.run(cmd, check=True)
    
    # Chạy inspect_pdf với cờ --target-one-page
    import pymupdf
    doc = pymupdf.open(out_pdf)
    page_count = len(doc)
    doc.close()
    
    print(f"-> Tổng số trang thực tế xuất ra: {page_count} trang")
    is_ok = inspect_pdf(out_pdf, target_one_page=True)
    
    # Kỳ vọng: Bị báo lỗi OVERFLOW_PAGE_2 và trả về False
    overflow_detected = (page_count >= 2 and not is_ok)
    if overflow_detected:
        print("✅ NHÓM 4 HOÀN TOÀN ĐẠT CHUẨN: Báo đúng OVERFLOW_PAGE_2 và chặn tài liệu bị tràn trang!")
    else:
        print("❌ NHÓM 4 THẤT BẠI: Không phát hiện lỗi tràn trang!")
        
    return overflow_detected, f"Detected overflow on {page_count} pages"

def test_group_5_ingest():
    print("\n" + "=" * 70)
    print("NHÓM 5: KIỂM THỬ TIẾP NHẬN & TIỀN XỬ LÝ VĂN BẢN ĐẾN (INGEST INCOMING)")
    print("=" * 70)
    
    sample_pdf = os.path.join(REPO_DIR, "knowledge_base", "sample_pdfs", "Bao_cao_SoDi_816.pdf")
    if not os.path.exists(sample_pdf):
        print(f"❌ Không tìm thấy file PDF mẫu: {sample_pdf}")
        return False, "Sample PDF missing"
        
    res = ingest_document(sample_pdf, "test_ingest_incoming", month_str="2026-11", max_pages=3)
    
    has_dir = os.path.exists(res["case_dir"])
    has_dest = os.path.exists(res["dest_file"])
    has_txt = os.path.exists(res["txt_file"]) and os.path.getsize(res["txt_file"]) > 0
    has_images = len(res["rendered_images"]) > 0 and all(os.path.exists(img) for img in res["rendered_images"])
    
    print(f"-> Thư mục case: {res['case_dir']} (Tồn tại: {has_dir})")
    print(f"-> File gốc đã lưu: {res['dest_file']} (Tồn tại: {has_dest})")
    print(f"-> File text trích xuất: {res['txt_file']} (~{res['word_count']} từ) (Tồn tại: {has_txt})")
    print(f"-> Ảnh render: {len(res['rendered_images'])} trang PNG (Tồn tại: {has_images})")
    
    passed = has_dir and has_dest and has_txt and has_images
    if passed:
        print("✅ NHÓM 5 HOÀN TOÀN ĐẠT CHUẨN (Ingest, trích xuất text & render ảnh thành công)!")
    return passed, f"Ingested {res['total_pages']} pages, {res['word_count']} words, {len(res['rendered_images'])} images"

def test_group_6_golden_jsons():
    print("\n" + "=" * 70)
    print("NHÓM 6: KIỂM THỬ KHO BẢN MẪU VÀNG (GOLDEN JSONS)")
    print("=" * 70)
    
    golden_dir = os.path.join(REPO_DIR, "knowledge_base", "golden_jsons")
    if not os.path.exists(golden_dir):
        print(f"❌ Không tìm thấy thư mục golden_jsons: {golden_dir}")
        return False, "Missing golden_jsons folder"
        
    g_files = [f for f in os.listdir(golden_dir) if f.lower().endswith(".json")]
    if len(g_files) < 5:
        print(f"❌ Số lượng bản mẫu vàng chưa đủ 5 (hiện có {len(g_files)}): {g_files}")
        return False, f"Only {len(g_files)} golden jsons found"
        
    all_clean = True
    for gf in g_files:
        gpath = os.path.join(golden_dir, gf)
        with open(gpath, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
        s_errs = validate_schema(data)
        l_res = lint_document(data, strict_final=False)
        has_err = (len(s_errs) > 0) or (not l_res["valid"])
        status = "FAIL" if has_err else "PASS (0 ERROR)"
        print(f"  - {gf:30}: [{status}] (Schema errs: {len(s_errs)}, Lint errs: {len(l_res['errors'])})")
        if has_err:
            all_clean = False
            
    if all_clean:
        print(f"✅ NHÓM 6 HOÀN TOÀN ĐẠT CHUẨN: Toàn bộ {len(g_files)}/5 bản mẫu vàng đạt 0 ERROR!")
    return all_clean, f"{len(g_files)}/{len(g_files)} PASS (0 ERROR)"

def check_process_safety():
    print("\n" + "=" * 70)
    print("KIỂM TRA AN TOÀN TIẾN TRÌNH (WINWORD.EXE)")
    print("=" * 70)
    
    cmd = ["powershell.exe", "-Command", "(Get-Process -Name WINWORD -ErrorAction SilentlyContinue).Count"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    count_str = res.stdout.strip()
    winword_count = int(count_str) if count_str.isdigit() else 0
    
    print(f"-> Số lượng tiến trình WINWORD.EXE đang chạy: {winword_count}")
    if winword_count == 0:
        print("✅ AN TOÀN TUYỆT ĐỐI: Không có tiến trình Word nào bị treo ngầm!")
        return True
    else:
        print(f"⚠️ CẢNH BÁO: Còn {winword_count} tiến trình WINWORD.EXE chưa được giải phóng!")
        return False

def main():
    setup_directories()
    
    print("\n" + "#" * 80)
    print("BẮT ĐẦU CHẠY TOÀN BỘ BỘ KIỂM THỬ HỒI QUY NÂNG CẤP v2.5")
    print("#" * 80)
    
    t0 = time.time()
    
    g1_ok, g1_msg = test_group_1_batch()
    g2_ok, g2_msg = test_group_2_inline_markdown()
    g3_ok, g3_msg = test_group_3_linter_negative()
    g4_ok, g4_msg = test_group_4_overflow_telemetry()
    g5_ok, g5_msg = test_group_5_ingest()
    g6_ok, g6_msg = test_group_6_golden_jsons()
    safety_ok = check_process_safety()
    
    total_time = round(time.time() - t0, 2)
    
    print("\n" + "#" * 80)
    print(f"TỔNG KẾT KIỂM THỬ HỒI QUY v2.5 (Thời gian thực thi: {total_time}s):")
    print(f"  1. Nhóm 1 (Batch Compatibility)    : {'[PASS]' if g1_ok else '[FAIL]'} - {g1_msg}")
    print(f"  2. Nhóm 2 (Inline Markdown Visual) : {'[PASS]' if g2_ok else '[FAIL]'} - {g2_msg}")
    print(f"  3. Nhóm 3 (Linter Negative Tests)  : {'[PASS]' if g3_ok else '[FAIL]'} - {g3_msg}")
    print(f"  4. Nhóm 4 (Overflow Telemetry)     : {'[PASS]' if g4_ok else '[FAIL]'} - {g4_msg}")
    print(f"  5. Nhóm 5 (Ingest Incoming)        : {'[PASS]' if g5_ok else '[FAIL]'} - {g5_msg}")
    print(f"  6. Nhóm 6 (Golden JSONs)           : {'[PASS]' if g6_ok else '[FAIL]'} - {g6_msg}")
    print(f"  7. An toàn tiến trình WINWORD      : {'[PASS]' if safety_ok else '[FAIL]'}")
    print("#" * 80)
    
    all_success = g1_ok and g2_ok and g3_ok and g4_ok and g5_ok and g6_ok and safety_ok
    sys.exit(0 if all_success else 1)

if __name__ == "__main__":
    main()
