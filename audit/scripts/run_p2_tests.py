import os
import sys
import subprocess
import json

def run_tests():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(os.path.dirname(script_dir))
    test_dir = os.path.join(root_dir, "audit", "p2_tests")
    render_dir = os.path.join(test_dir, "renders")
    os.makedirs(render_dir, exist_ok=True)
    
    python_exe = os.path.join(root_dir, ".venv", "Scripts", "python.exe")
    build_script = os.path.join(root_dir, "tools", "build_doc.py")
    inspect_script = os.path.join(root_dir, "tools", "inspect_pdf.py")
    
    test_cases = [
        "01_cong_van_1p",
        "02_to_trinh_1p",
        "03_giay_gioi_thieu_1p",
        "04_ke_hoach_nhieu_trang",
        "05_bao_cao_nhieu_trang",
        "06_cong_van_phu_luc_ngang"
    ]
    
    summary = []
    
    for tc in test_cases:
        json_path = os.path.join(test_dir, f"{tc}.json")
        docx_path = os.path.join(test_dir, f"{tc}.docx")
        pdf_path = os.path.join(test_dir, f"{tc}.pdf")
        
        print("\n" + "=" * 80)
        print(f"BẮT ĐẦU CHẠY KIỂM THỬ: {tc}")
        print("=" * 80)
        
        # 1. Build DOCX & Export PDF
        cmd_build = [python_exe, build_script, "--input", json_path, "--output", docx_path, "--pdf"]
        res_build = subprocess.run(cmd_build, capture_output=True, text=True)
        print(res_build.stdout)
        if res_build.returncode != 0:
            print(f"Lỗi build DOCX/PDF: {res_build.stderr}")
            summary.append({"case": tc, "status": "FAIL_BUILD", "error": res_build.stderr})
            continue
            
        # 2. Inspect PDF & Render PNG
        cmd_inspect = [python_exe, inspect_script, "--pdf", pdf_path, "--render-dir", render_dir, "--dpi", "150"]
        res_inspect = subprocess.run(cmd_inspect, capture_output=True, text=True)
        print(res_inspect.stdout)
        
        summary.append({
            "case": tc,
            "status": "PASS" if res_inspect.returncode == 0 else "WARNING/FAIL",
            "pdf": pdf_path,
            "stdout": res_inspect.stdout
        })
        
    print("\n" + "=" * 80)
    print("TỔNG KẾT KIỂM THỬ 6 CA PHASE 2")
    print("=" * 80)
    for s in summary:
        print(f"- {s['case']:30}: {s['status']}")

if __name__ == "__main__":
    run_tests()
