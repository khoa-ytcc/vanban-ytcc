import os
import re
import sys
import json
import sqlite3
import datetime
import argparse
import subprocess
import pymupdf
import docx

def remove_accents(input_str):
    if not input_str:
        return ""
    import unicodedata
    nfkd_form = unicodedata.normalize('NFKD', str(input_str))
    res = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
    res = res.replace('đ', 'd').replace('Đ', 'D')
    return res.lower().strip()

def extract_pdf_text(path):
    try:
        doc = pymupdf.open(path)
        pages = len(doc)
        text = "".join(page.get_text() for page in doc)
        doc.close()
        return pages, text.strip()
    except Exception:
        return 0, ""

def extract_docx_text(path):
    try:
        doc = docx.Document(path)
        lines = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
        for tbl in doc.tables:
            for r in tbl.rows:
                row_str = " | ".join(c.text.strip() for c in r.cells if c.text.strip())
                if row_str:
                    lines.append(row_str)
        return 1, "\n".join(lines)
    except Exception:
        return 0, ""

def extract_json_text(path):
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
        texts = []
        if "header" in data and isinstance(data["header"], dict):
            for v in data["header"].values():
                if isinstance(v, str): texts.append(v)
        if "blocks" in data and isinstance(data["blocks"], list):
            for b in data["blocks"]:
                if isinstance(b, dict):
                    if "text" in b: texts.append(str(b["text"]))
                    if "prefix_bold" in b: texts.append(str(b["prefix_bold"]))
                    if "items" in b and isinstance(b["items"], list):
                        texts.extend(str(it) for it in b["items"])
                    if b.get("type") == "table":
                        for row in b.get("rows", []):
                            texts.append(" | ".join(str(c) for c in row))
        return 1, "\n".join(texts)
    except Exception:
        return 0, ""

def sync_knowledge_base(from_mysql=False):
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    meta_dir = os.path.join(root_dir, "knowledge_base", "metadata_index")
    pdf_dir = os.path.join(root_dir, "knowledge_base", "sample_pdfs")
    golden_dir = os.path.join(root_dir, "knowledge_base", "golden_jsons")
    drafts_dir = os.path.join(root_dir, "drafts")
    db_path = os.path.join(meta_dir, "ytcc_history.db")
    
    if not os.path.exists(db_path):
        print(f"CSDL chưa khởi tạo. Vui lòng chạy build_index.py trước.")
        return
        
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # Đọc bản đồ các file đã index
    cur.execute("SELECT file_path, mtime, file_size FROM indexed_files")
    indexed_map = {row[0]: (row[1], row[2]) for row in cur.fetchall()}
    
    added_count = 0
    updated_count = 0
    skipped_count = 0
    now_iso = datetime.datetime.now().isoformat()
    
    # 1. Quét sample_pdfs
    if os.path.exists(pdf_dir):
        for fname in os.listdir(pdf_dir):
            if fname.lower().endswith(".pdf"):
                fpath = os.path.join(pdf_dir, fname)
                rel_path = os.path.relpath(fpath, root_dir).replace("\\", "/")
                fsize = os.path.getsize(fpath)
                fmtime = os.path.getmtime(fpath)
                
                if rel_path in indexed_map:
                    old_mtime, old_size = indexed_map[rel_path]
                    if abs(fmtime - old_mtime) < 0.001 and fsize == old_size:
                        skipped_count += 1
                        continue
                    else:
                        is_update = True
                else:
                    is_update = False
                    
                pages, text = extract_pdf_text(fpath)
                if len(text) >= 50:
                    text_unaccent = remove_accents(text)
                    if is_update:
                        cur.execute("DELETE FROM fulltext_fts WHERE file_path = ?", (rel_path,))
                        cur.execute("DELETE FROM indexed_files WHERE file_path = ?", (rel_path,))
                        updated_count += 1
                    else:
                        added_count += 1
                        
                    cur.execute("""
                        INSERT INTO fulltext_fts (file_path, title, content, content_no_accent, source_type, page_count)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (rel_path, fname, text, text_unaccent, "sample_pdf", pages))
                    
                    cur.execute("""
                        INSERT INTO indexed_files (file_path, mtime, file_size, source_type, page_count, indexed_at)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (rel_path, fmtime, fsize, "sample_pdf", pages, now_iso))
                else:
                    skipped_count += 1

    # 2. Quét golden_jsons
    if os.path.exists(golden_dir):
        for fname in os.listdir(golden_dir):
            if fname.lower().endswith(".json"):
                fpath = os.path.join(golden_dir, fname)
                rel_path = os.path.relpath(fpath, root_dir).replace("\\", "/")
                fsize = os.path.getsize(fpath)
                fmtime = os.path.getmtime(fpath)
                
                if rel_path in indexed_map:
                    old_mtime, old_size = indexed_map[rel_path]
                    if abs(fmtime - old_mtime) < 0.001 and fsize == old_size:
                        skipped_count += 1
                        continue
                    else:
                        is_update = True
                else:
                    is_update = False
                    
                pages, text = extract_json_text(fpath)
                if text:
                    text_unaccent = remove_accents(text)
                    if is_update:
                        cur.execute("DELETE FROM fulltext_fts WHERE file_path = ?", (rel_path,))
                        cur.execute("DELETE FROM indexed_files WHERE file_path = ?", (rel_path,))
                        updated_count += 1
                    else:
                        added_count += 1
                        
                    cur.execute("""
                        INSERT INTO fulltext_fts (file_path, title, content, content_no_accent, source_type, page_count)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (rel_path, fname, text, text_unaccent, "golden_json", 1))
                    
                    cur.execute("""
                        INSERT INTO indexed_files (file_path, mtime, file_size, source_type, page_count, indexed_at)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (rel_path, fmtime, fsize, "golden_json", 1, now_iso))
                else:
                    skipped_count += 1
                    
    # 3. Quét drafts
    if os.path.exists(drafts_dir):
        for root, _, files in os.walk(drafts_dir):
            if "incoming" in root or "renders" in root:
                continue
            for fname in files:
                ext = os.path.splitext(fname)[1].lower()
                if ext in (".docx", ".json"):
                    fpath = os.path.join(root, fname)
                    rel_path = os.path.relpath(fpath, root_dir).replace("\\", "/")
                    fsize = os.path.getsize(fpath)
                    fmtime = os.path.getmtime(fpath)
                    
                    if rel_path in indexed_map:
                        old_mtime, old_size = indexed_map[rel_path]
                        if abs(fmtime - old_mtime) < 0.001 and fsize == old_size:
                            skipped_count += 1
                            continue
                        else:
                            is_update = True
                    else:
                        is_update = False
                        
                    pages, text = extract_docx_text(fpath) if ext == ".docx" else extract_json_text(fpath)
                    if text and len(text) > 30:
                        text_unaccent = remove_accents(text)
                        if is_update:
                            cur.execute("DELETE FROM fulltext_fts WHERE file_path = ?", (rel_path,))
                            cur.execute("DELETE FROM indexed_files WHERE file_path = ?", (rel_path,))
                            updated_count += 1
                        else:
                            added_count += 1
                            
                        cur.execute("""
                            INSERT INTO fulltext_fts (file_path, title, content, content_no_accent, source_type, page_count)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (rel_path, fname, text, text_unaccent, f"draft_{ext.lstrip('.')}", pages))
                        
                        cur.execute("""
                            INSERT INTO indexed_files (file_path, mtime, file_size, source_type, page_count, indexed_at)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (rel_path, fmtime, fsize, f"draft_{ext.lstrip('.')}", pages, now_iso))
                    else:
                        skipped_count += 1

    conn.commit()
    conn.close()
    
    # 4. Tùy chọn MySQL delta sync
    mysql_delta_count = 0
    if from_mysql:
        ps1_path = os.path.join(root_dir, "tools", "fetch_mysql_delta.ps1")
        if os.path.exists(ps1_path):
            print("\nĐang gọi fetch_mysql_delta.ps1 kiểm tra bản ghi mới...")
            cmd = ["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", ps1_path]
            res = subprocess.run(cmd, capture_output=True, text=True)
            print(res.stdout.strip())
            
    print(f"\n=== ĐỒNG BỘ TĂNG DẦN HOÀN TẤT (SYNC KB) ===")
    print(f"- File thêm mới (added)   : {added_count}")
    print(f"- File cập nhật (updated) : {updated_count}")
    print(f"- File bỏ qua (skipped)   : {skipped_count} (không đổi)")
    print("==========================================")
    return {"added": added_count, "updated": updated_count, "skipped": skipped_count}

def main():
    parser = argparse.ArgumentParser(description="YTCC Incremental Knowledge Base Synchronizer")
    parser.add_argument("--from-mysql", action="store_true", help="Kiểm tra thêm dữ liệu mới từ CSDL MySQL")
    args = parser.parse_args()
    
    sync_knowledge_base(from_mysql=args.from_mysql)

if __name__ == "__main__":
    main()
