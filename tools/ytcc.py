#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YTCC Unified Administrative CLI (v2.5A)
Công cụ dòng lệnh hợp nhất cho toàn bộ quy trình văn bản hành chính Khoa Y tế Công cộng.
"""

import os
import sys
import json
import time
import argparse
import subprocess

# Đảm bảo import được các module trong tools/
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from build_doc import build_document, validate_schema, export_to_pdf
from lint_doc import lint_document, print_lint_report
from inspect_pdf import inspect_pdf
from ingest_incoming import ingest_document, print_ingest_report
from search_history import search_documents, search_fulltext, print_results
from diff_draft import analyze_diff
from sync_kb import sync_knowledge_base

def handle_build(args):
    json_path = args.input
    if not os.path.exists(json_path):
        print(f"Lỗi: Không tìm thấy file JSON: {json_path}", file=sys.stderr)
        sys.exit(1)
        
    output_docx = args.output
    if not output_docx:
        output_docx = os.path.splitext(json_path)[0] + ".docx"
        
    with open(json_path, "r", encoding="utf-8-sig") as f:
        data = json.load(f)
        
    print(f"\n[1/3] Kiểm tra cấu trúc Schema & Thể thức hành chính...")
    # 1. Schema check
    schema_errors = validate_schema(data)
    if schema_errors:
        print("❌ LỖI CẤU TRÚC SCHEMA:")
        for err in schema_errors:
            print(f"  - {err}")
        if not args.force:
            print("Đã dừng quá trình tạo tài liệu. Dùng --force nếu muốn bỏ qua.", file=sys.stderr)
            sys.exit(1)
            
    # 2. Linter check
    lint_res = lint_document(data, strict_final=args.strict_final)
    print_lint_report(json_path, lint_res)
    if not lint_res["valid"] and not args.force:
        print("❌ Linter phát hiện lỗi chặn. Đã hủy tạo DOCX (dùng --force để ép buộc tạo).", file=sys.stderr)
        sys.exit(1)
        
    # 3. Build DOCX
    print(f"\n[2/3] Đang tạo file Word (.docx): {output_docx}...")
    build_document(json_path, output_docx)
    
    # 4. Export PDF & Inspect nếu có cờ --pdf
    if args.pdf:
        print(f"\n[3/3] Xuất PDF qua Word COM & Kiểm định...")
        pdf_path = export_to_pdf(output_docx, args.pdf_out)
        target_one_page = data.get("target_one_page", False)
        inspect_pdf(pdf_path, render_dir=args.render_dir, target_one_page=target_one_page)
        
    print("\n✅ Hoàn tất thành công!")

def execute_batch_job(batch_target):
    items = []
    temp_batch_file = None
    
    if os.path.isdir(batch_target):
        json_files = [os.path.join(batch_target, f) for f in os.listdir(batch_target) if f.lower().endswith(".json") and not f.startswith("_")]
        if not json_files:
            print(f"Lỗi: Không tìm thấy file JSON nào trong thư mục: {batch_target}", file=sys.stderr)
            sys.exit(1)
        for jf in json_files:
            docx_out = os.path.splitext(jf)[0] + ".docx"
            pdf_out = os.path.splitext(jf)[0] + ".pdf"
            items.append({"json": jf, "docx": docx_out, "pdf": pdf_out})
    elif os.path.isfile(batch_target):
        with open(batch_target, "r", encoding="utf-8-sig") as f:
            raw = json.load(f)
        if isinstance(raw, list):
            items = raw
        elif isinstance(raw, dict) and "tasks" in raw:
            items = raw["tasks"]
        else:
            print("Lỗi: File batch phải chứa mảng các task JSON hoặc dict có khóa 'tasks'.", file=sys.stderr)
            sys.exit(1)
    else:
        print(f"Lỗi: Không tìm thấy file hoặc thư mục batch: {batch_target}", file=sys.stderr)
        sys.exit(1)
        
    if not items:
        print("Lỗi: Danh sách batch trống.", file=sys.stderr)
        sys.exit(1)
        
    start_time = time.time()
    print(f"\n=== BẮT ĐẦU BATCH XỬ LÝ {len(items)} TÀI LIỆU ===")
    
    # 1. Dựng tất cả các file DOCX nếu có trường 'json'
    batch_pdf_payload = []
    inspect_queue = []
    
    for idx, item in enumerate(items, 1):
        json_path = item.get("json")
        docx_path = item.get("docx")
        pdf_path = item.get("pdf")
        
        if json_path:
            if not docx_path:
                docx_path = os.path.splitext(json_path)[0] + ".docx"
                item["docx"] = docx_path
            if not pdf_path:
                pdf_path = os.path.splitext(json_path)[0] + ".pdf"
                item["pdf"] = pdf_path
                
            print(f"[{idx}/{len(items)}] Dựng DOCX: {os.path.basename(json_path)} -> {os.path.basename(docx_path)}")
            build_document(json_path, docx_path)
            
            with open(json_path, "r", encoding="utf-8-sig") as jf:
                jdata = json.load(jf)
            inspect_queue.append((pdf_path, jdata.get("target_one_page", False)))
        else:
            if docx_path and pdf_path:
                inspect_queue.append((pdf_path, False))
                
        batch_pdf_payload.append({
            "docx": os.path.abspath(docx_path),
            "pdf": os.path.abspath(pdf_path)
        })
        
    # 2. Gọi export_pdf.ps1 -BatchJson
    temp_batch_json = os.path.join(SCRIPT_DIR, "_temp_batch.json")
    with open(temp_batch_json, "w", encoding="utf-8") as f:
        json.dump(batch_pdf_payload, f, ensure_ascii=False, indent=2)
        
    ps1_path = os.path.join(SCRIPT_DIR, "export_pdf.ps1")
    cmd = [
        "powershell.exe",
        "-ExecutionPolicy", "Bypass",
        "-File", ps1_path,
        "-BatchJson", temp_batch_json
    ]
    
    print(f"\nKhởi động Word COM xuất PDF hàng loạt...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(temp_batch_json):
        try: os.remove(temp_batch_json)
        except: pass
        
    if res.returncode != 0:
        print(f"Lỗi xuất PDF batch:\n{res.stderr}", file=sys.stderr)
        sys.exit(1)
    else:
        print(res.stdout.strip())
        
    # 3. Inspect tất cả PDF đã sinh
    print(f"\nKiểm định thể thức các file PDF vừa xuất:")
    all_passed = True
    for p_path, target_one in inspect_queue:
        if os.path.exists(p_path):
            ok = inspect_pdf(p_path, target_one_page=target_one)
            if not ok: all_passed = False
            
    elapsed = round(time.time() - start_time, 2)
    print(f"\n=== HOÀN TẤT BATCH TRONG {elapsed}s (Trung bình {round(elapsed/len(items), 2)}s/file) ===")
    if not all_passed:
        sys.exit(1)

def handle_batch(args):
    execute_batch_job(args.batch_json)

def handle_ingest(args):
    file_path = args.file or args.file_pos
    if not file_path:
        print("Lỗi: Vui lòng cung cấp đường dẫn file cần tiếp nhận (ví dụ: ytcc ingest input.pdf --case case_name).", file=sys.stderr)
        sys.exit(1)
    case_name = args.case or args.case_pos
    if not case_name:
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        case_name = re.sub(r'[^a-zA-Z0-9_]+', '_', base_name).strip('_').lower()
        if not case_name:
            case_name = "incoming_case"
    res = ingest_document(file_path, case_name, month_str=args.month, max_pages=args.max_pages, out_dir=args.out_dir)
    print_ingest_report(res)

def handle_search(args):
    q = args.query or args.query_opt
    if not q:
        print("Lỗi: Vui lòng nhập từ khóa tìm kiếm (ví dụ: ytcc search \"Nghị định 30\" hoặc --q \"Nghị định 30\").", file=sys.stderr)
        sys.exit(1)
    meta_res = search_documents(q, doc_type=args.type, limit=args.limit) if args.mode in ("meta", "all") else []
    ft_res = search_fulltext(q, limit=args.limit) if args.mode in ("fulltext", "all") else []
    print_results(meta_res, ft_res, q, doc_type=args.type, mode=args.mode, limit=args.limit)

def handle_diff(args):
    orig = args.original or args.orig_pos
    rev = args.revised or args.rev_pos
    if not orig or not rev:
        print("Lỗi: Cần cung cấp đủ 2 file để so sánh (ví dụ: ytcc diff orig.docx revised.docx hoặc --original orig.docx --revised revised.docx).", file=sys.stderr)
        sys.exit(1)
    analyze_diff(orig, rev)

def handle_sync(args):
    sync_knowledge_base(from_mysql=args.from_mysql)

def handle_promote(args):
    json_path = args.input
    if not os.path.exists(json_path):
        print(f"Lỗi: Không tìm thấy file JSON: {json_path}", file=sys.stderr)
        sys.exit(1)
        
    with open(json_path, "r", encoding="utf-8-sig") as f:
        data = json.load(f)
        
    print(f"\n[1/3] Kiểm tra điều kiện thăng hạng vào Golden JSONs...")
    schema_errs = validate_schema(data)
    if schema_errs:
        print("❌ Lỗi Schema Validator:")
        for e in schema_errs: print(f"  - {e}")
        sys.exit(1)
        
    lint_res = lint_document(data, strict_final=False)
    if not lint_res["valid"]:
        print("❌ Lỗi Linter Hành chính (yêu cầu 0 ERROR để promote):")
        for e in lint_res["errors"]: print(f"  - {e}")
        sys.exit(1)
        
    name = args.name.strip()
    if not name.endswith(".json"):
        name += ".json"
        
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    golden_dir = os.path.join(root_dir, "knowledge_base", "golden_jsons")
    os.makedirs(golden_dir, exist_ok=True)
    target_path = os.path.join(golden_dir, name)
    
    print(f"[2/3] Lưu bản mẫu chuẩn: {target_path}...")
    import shutil
    shutil.copy2(json_path, target_path)
    
    print(f"[3/3] Đồng bộ vào kho chỉ mục tăng dần SQLite FTS5...")
    sync_knowledge_base()
    
    print(f"\n✅ Đã thăng hạng thành công bản mẫu vàng: {name}")

def main():
    parser = argparse.ArgumentParser(
        prog="ytcc",
        description="YTCC Unified Administrative Automation CLI (Khoa Y tế Công cộng - ĐHYD TP.HCM)"
    )
    subparsers = parser.add_subparsers(dest="command", help="Lệnh chức năng")
    
    # Subcommand: build
    p_build = subparsers.add_parser("build", help="Xây dựng văn bản DOCX & xuất PDF từ file JSON")
    p_build.add_argument("input", help="Đường dẫn file JSON mô tả văn bản")
    p_build.add_argument("-o", "--output", help="Đường dẫn file .docx đầu ra")
    p_build.add_argument("--pdf", action="store_true", help="Tự động gọi Word COM xuất PDF")
    p_build.add_argument("--pdf-out", help="Đường dẫn file .pdf tùy chọn")
    p_build.add_argument("--render-dir", help="Thư mục xuất ảnh PNG để soi trực quan")
    p_build.add_argument("--strict-final", action="store_true", help="Chặn hoàn toàn nếu còn placeholder")
    p_build.add_argument("--force", action="store_true", help="Bỏ qua cảnh báo linter để tiếp tục sinh file")
    p_build.set_defaults(func=handle_build)
    
    # Subcommand: batch
    p_batch = subparsers.add_parser("batch", help="Xây dựng và xuất PDF hàng loạt tối ưu qua 1 phiên Word COM")
    p_batch.add_argument("batch_json", help="Đường dẫn file JSON mô tả danh sách các tài liệu cần xuất (hoặc thư mục chứa các file .json)")
    p_batch.set_defaults(func=handle_batch)
    
    # Subcommand: ingest
    p_ingest = subparsers.add_parser("ingest", help="Tiếp nhận và tiền xử lý văn bản đến (.pdf, .docx, .png)")
    p_ingest.add_argument("file_pos", nargs="?", default=None, help="Đường dẫn file văn bản đến (positional)")
    p_ingest.add_argument("case_pos", nargs="?", default=None, help="Tên case xử lý (positional, tùy chọn)")
    p_ingest.add_argument("--file", default=None, help="Đường dẫn file văn bản đến")
    p_ingest.add_argument("--case", default=None, help="Tên case xử lý")
    p_ingest.add_argument("--month", help="Tháng lưu trữ YYYY-MM")
    p_ingest.add_argument("--out-dir", help="Chỉ định thư mục đích trực tiếp")
    p_ingest.add_argument("--max-pages", type=int, default=5, help="Số trang tối đa render ảnh PNG (mặc định 5)")
    p_ingest.set_defaults(func=handle_ingest)
    
    # Subcommand: search
    p_search = subparsers.add_parser("search", help="Tra cứu văn bản lịch sử qua SQLite FTS5 (Metadata & Toàn văn)")
    p_search.add_argument("query", nargs="?", default=None, help="Từ khóa tìm kiếm (hỗ trợ có dấu hoặc không dấu)")
    p_search.add_argument("-q", "--q", dest="query_opt", default=None, help="Từ khóa tìm kiếm (tùy chọn qua flag --q)")
    p_search.add_argument("--mode", choices=["meta", "fulltext", "all"], default="all", help="Chế độ tra cứu (meta, fulltext, all)")
    p_search.add_argument("--type", choices=["all", "di", "den"], default="all", help="Loại văn bản metadata (all, di, den)")
    p_search.add_argument("--limit", type=int, default=5, help="Giới hạn số kết quả trả về")
    p_search.set_defaults(func=handle_search)
    
    # Subcommand: diff
    p_diff = subparsers.add_parser("diff", help="So sánh khác biệt văn bản giữa bản AI dự thảo và bản sửa tay")
    p_diff.add_argument("orig_pos", nargs="?", default=None, help="Đường dẫn file .docx bản AI ban đầu (positional)")
    p_diff.add_argument("rev_pos", nargs="?", default=None, help="Đường dẫn file .docx bản người dùng sửa (positional)")
    p_diff.add_argument("--original", default=None, help="Đường dẫn file .docx bản AI ban đầu")
    p_diff.add_argument("--revised", default=None, help="Đường dẫn file .docx bản người dùng sửa")
    p_diff.set_defaults(func=handle_diff)
    
    # Subcommand: sync
    p_sync = subparsers.add_parser("sync", help="Đồng bộ tăng dần kho tri thức vào SQLite FTS5")
    p_sync.add_argument("--from-mysql", action="store_true", help="Kiểm tra thêm dữ liệu mới từ CSDL MySQL")
    p_sync.set_defaults(func=handle_sync)
    
    # Subcommand: promote
    p_promote = subparsers.add_parser("promote", help="Thăng hạng văn bản chuẩn vào kho Bản mẫu vàng (Golden JSONs)")
    p_promote.add_argument("input", help="Đường dẫn file JSON mẫu cần thăng hạng")
    p_promote.add_argument("--name", required=True, help="Tên file mẫu vàng (ví dụ: cong_van_khao_sat.json)")
    p_promote.set_defaults(func=handle_promote)
    
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)
        
    args.func(args)

if __name__ == "__main__":
    main()
