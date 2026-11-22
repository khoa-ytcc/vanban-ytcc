import os
import sys
import subprocess

script_dir = os.path.dirname(os.path.abspath(__file__))
repo_dir = os.path.dirname(os.path.dirname(script_dir))
tools_dir = os.path.join(repo_dir, "tools")
if tools_dir not in sys.path:
    sys.path.insert(0, tools_dir)

from build_doc import build_document, export_to_pdf
from inspect_pdf import inspect_pdf

def run_case(case_name):
    base_dir = os.path.join(repo_dir, "drafts", "2026-11")
    
    json_path = os.path.join(base_dir, f"{case_name}.json")
    docx_path = os.path.join(base_dir, f"{case_name}.docx")
    pdf_path = os.path.join(base_dir, f"{case_name}.pdf")
    render_dir = os.path.join(base_dir, "renders")
    
    print("\n" + "="*80)
    print(f"BẮT ĐẦU CHẠY THỰC CHIẾN: {case_name}")
    print("="*80)
    
    # 1. Sinh DOCX
    build_document(json_path, docx_path)
    
    # 2. Xuất PDF qua Word COM
    export_to_pdf(docx_path, pdf_path)
    
    # 3. Kiểm định PDF và render ảnh PNG
    success = inspect_pdf(pdf_path, render_dir=render_dir)
    return success

def main():
    cases = [
        "ca1_phuc_dap_ghi_hinh_htv7",
        "ca2_to_trinh_hoi_thao_ai",
        "ca3_ke_hoach_thuc_te_dong_nai"
    ]
    
    results = {}
    for c in cases:
        try:
            ok = run_case(c)
            results[c] = "PASS" if ok else "FAIL"
        except Exception as e:
            print(f"LỖI KHI CHẠY {c}: {e}")
            results[c] = f"ERROR: {e}"
            
    print("\n" + "="*80)
    print("TỔNG KẾT KIỂM THỬ THỰC CHIẾN 3 CA PHASE 3")
    print("="*80)
    for c, status in results.items():
        print(f"- {c:<30}: {status}")

if __name__ == "__main__":
    main()
