#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Công cụ so sánh (Diff) văn bản Word giữa bản AI sinh ra và bản Người dùng chỉnh sửa.
Chỉ sử dụng python-docx và difflib (chuẩn thư viện Python), không cần cài đặt thêm.
"""

import os
import sys
import argparse
import difflib
import docx

def extract_text_items(docx_path):
    """Trích xuất toàn bộ văn bản trong các đoạn và bảng biểu của tài liệu Word."""
    if not os.path.exists(docx_path):
        raise FileNotFoundError(f"Không tìm thấy file: {docx_path}")
        
    doc = docx.Document(docx_path)
    items = []
    
    for element in doc.element.body:
        # Xử lý đoạn văn (paragraph)
        if element.tag.endswith('p'):
            p = docx.text.paragraph.Paragraph(element, doc)
            text = p.text.strip()
            if text:
                items.append(text)
        # Xử lý bảng biểu (table)
        elif element.tag.endswith('tbl'):
            tbl = docx.table.Table(element, doc)
            for r_idx, row in enumerate(tbl.rows):
                # Lấy text từng ô, loại bỏ ô trùng (merged cells)
                cell_texts = []
                seen_cells = set()
                for cell in row.cells:
                    if cell._tc not in seen_cells:
                        seen_cells.add(cell._tc)
                        c_text = " ".join(cell.text.strip().split())
                        cell_texts.append(c_text if c_text else "-")
                if cell_texts and any(c != "-" for c in cell_texts):
                    items.append(f"[Bảng - Dòng {r_idx+1}] " + " | ".join(cell_texts))
                    
    return items

def analyze_diff(ai_path, final_path):
    print("=" * 80)
    print("KẾT QUẢ SO SÁNH (DIFF DRAFT):")
    print(f"(-) Bản AI dự thảo  : {ai_path}")
    print(f"(+) Bản người dùng sửa: {final_path}")
    print("=" * 80)
    
    ai_lines = extract_text_items(ai_path)
    final_lines = extract_text_items(final_path)
    
    diff = list(difflib.unified_diff(
        ai_lines,
        final_lines,
        fromfile="AI_DRAFT",
        tofile="USER_EDITED",
        lineterm="",
        n=2
    ))
    
    if not diff:
        print("\n✅ KHÔNG CÓ KHÁC BIỆT: Hai file có nội dung hoàn toàn trùng khớp!")
        return 0
        
    additions = 0
    deletions = 0
    
    print("\n--- CHI TIẾT CÁC ĐIỂM NGƯỜI DÙNG ĐÃ CHỈNH SỬA ---")
    for line in diff:
        if line.startswith("---") or line.startswith("+++") or line.startswith("@@"):
            print(f"\033[90m{line}\033[0m" if sys.stdout.isatty() else line)
        elif line.startswith("-"):
            deletions += 1
            print(f"[-] XÓA / THAY THẾ: {line[1:].strip()}")
        elif line.startswith("+"):
            additions += 1
            print(f"[+] THÊM MỚI / SỬA: {line[1:].strip()}")
        else:
            print(f"    {line.strip()}")
            
    print("\n" + "=" * 80)
    print(f"TỔNG KẾT: {deletions} dòng bị xóa/thay thế, {additions} dòng được thêm mới/hiệu chỉnh.")
    print("Gợi ý cho AI: Hãy chắt lọc xem thay đổi nào là thói quen chung để lưu vào memory.")
    print("=" * 80)
    return 1

def main():
    parser = argparse.ArgumentParser(
        description="So sánh sự khác biệt giữa bản Word dự thảo của AI và bản người dùng đã sửa."
    )
    parser.add_argument("--ai", required=True, help="Đường dẫn file .docx do AI sinh ra ban đầu")
    parser.add_argument("--final", required=True, help="Đường dẫn file .docx do người dùng đã chỉnh sửa")
    
    args = parser.parse_args()
    try:
        analyze_diff(args.ai, args.final)
    except Exception as e:
        print(f"Lỗi khi so sánh: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
