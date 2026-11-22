import os
import re
import json
import sqlite3
import datetime
import unicodedata
import pymupdf
import docx

def remove_accents(input_str):
    if not input_str:
        return ""
    nfkd_form = unicodedata.normalize('NFKD', str(input_str))
    res = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
    res = res.replace('đ', 'd').replace('Đ', 'D')
    return res.lower().strip()

def extract_docx_text(path):
    try:
        doc = docx.Document(path)
        lines = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
        for tbl in doc.tables:
            for r in tbl.rows:
                row_str = " | ".join(c.text.strip() for c in r.cells if c.text.strip())
                if row_str:
                    lines.append(row_str)
        return "\n".join(lines)
    except Exception:
        return ""

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
        return "\n".join(texts)
    except Exception:
        return ""

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    meta_dir = os.path.join(root_dir, "knowledge_base", "metadata_index")
    pdf_dir = os.path.join(root_dir, "knowledge_base", "sample_pdfs")
    golden_dir = os.path.join(root_dir, "knowledge_base", "golden_jsons")
    drafts_dir = os.path.join(root_dir, "drafts")
    db_path = os.path.join(meta_dir, "ytcc_history.db")
    
    cv_di_path = os.path.join(meta_dir, "cv_di_history.json")
    cv_den_path = os.path.join(meta_dir, "cv_den_history.json")
    
    print(f"=== KHỞI TẠO & CẬP NHẬT INDEX SQLITE FTS5 (v2.5B): {db_path} ===")
    
    # 1. Quét toàn bộ file PDF trong sample_pdfs
    print("\n1. Đang quét 100% file PDF trong knowledge_base/sample_pdfs/...")
    pdf_files = [f for f in os.listdir(pdf_dir) if f.lower().endswith(".pdf")]
    total_pdfs = len(pdf_files)
    print(f"   Tìm thấy {total_pdfs} file PDF.")
    
    pdf_records = []
    pdf_by_nam_sodi = {}
    matched_pdf_count = 0
    
    page_dist = {"1_page": 0, "2_pages": 0, "3_plus_pages": 0}
    scan_counts = {"scan": 0, "has_text": 0}
    
    for fname in pdf_files:
        fpath = os.path.join(pdf_dir, fname)
        fsize = os.path.getsize(fpath)
        mtime = os.path.getmtime(fpath)
        
        # Đọc qua pymupdf
        try:
            doc = pymupdf.open(fpath)
            num_pages = len(doc)
            total_text = "".join(page.get_text() for page in doc)
            text_len = len(total_text.strip())
            is_scan = 1 if text_len < 50 else 0
            doc.close()
        except Exception:
            num_pages = 0
            text_len = 0
            total_text = ""
            is_scan = 1
        
        if num_pages == 1: page_dist["1_page"] += 1
        elif num_pages == 2: page_dist["2_pages"] += 1
        else: page_dist["3_plus_pages"] += 1
            
        if is_scan: scan_counts["scan"] += 1
        else: scan_counts["has_text"] += 1
            
        m1 = re.match(r"^CVDi_(\d+)_SoDi_(\d+)_", fname, re.IGNORECASE)
        m2 = re.match(r"^([A-Za-z_]+)_SoDi_(\d+)\.pdf", fname, re.IGNORECASE)
        
        rel_path = os.path.relpath(fpath, root_dir).replace("\\", "/")
        matched_nam = None
        matched_sodi = None
        
        if m1:
            matched_nam = int(m1.group(1))
            matched_sodi = str(m1.group(2)).strip()
        elif m2:
            matched_nam = 2026
            matched_sodi = str(m2.group(2)).strip()
            
        item = {
            "filename": fname,
            "filepath": rel_path,
            "abs_path": fpath,
            "file_size": fsize,
            "mtime": mtime,
            "page_count": num_pages,
            "is_scan": is_scan,
            "text_len": text_len,
            "text": total_text if not is_scan else "",
            "so_di": matched_sodi,
            "nam": matched_nam
        }
        pdf_records.append(item)
        
        if matched_nam and matched_sodi:
            matched_pdf_count += 1
            key = (matched_nam, matched_sodi)
            if key not in pdf_by_nam_sodi or fname.startswith("CVDi_"):
                pdf_by_nam_sodi[key] = item
                
    # 2. Khởi tạo CSDL SQLite
    if os.path.exists(db_path):
        os.remove(db_path)
        
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # Bảng pdf_samples
    cur.execute("""
        CREATE TABLE pdf_samples (
            filename TEXT PRIMARY KEY,
            filepath TEXT,
            file_size INTEGER,
            page_count INTEGER,
            is_scan INTEGER,
            text_len INTEGER,
            so_di TEXT,
            nam INTEGER
        )
    """)
    for p in pdf_records:
        cur.execute("""
            INSERT INTO pdf_samples (filename, filepath, file_size, page_count, is_scan, text_len, so_di, nam)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["filename"], p["filepath"], p["file_size"], p["page_count"], p["is_scan"], p["text_len"], p["so_di"], p["nam"]))
        
    # Bảng documents chính
    cur.execute("""
        CREATE TABLE documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doc_type TEXT,
            nam INTEGER,
            so_hieu TEXT,
            ngay_vanban TEXT,
            ngay_nhan TEXT,
            trich_yeu TEXT,
            nguoi_ky TEXT,
            tac_gia TEXT,
            noi_nhan TEXT,
            pdf_path TEXT,
            pdf_pages INTEGER,
            pdf_size INTEGER,
            pdf_is_scan INTEGER,
            text_no_accent TEXT
        )
    """)
    
    # Bảng FTS5 Metadata
    cur.execute("""
        CREATE VIRTUAL TABLE documents_fts USING fts5(
            doc_id UNINDEXED,
            doc_type,
            so_hieu,
            ngay_vanban,
            trich_yeu,
            nguoi_ky_tac_gia,
            noi_nhan,
            text_no_accent,
            pdf_path UNINDEXED,
            pdf_pages UNINDEXED,
            pdf_is_scan UNINDEXED
        )
    """)
    
    # Bảng đồng bộ tăng dần indexed_files (v2.5B)
    cur.execute("""
        CREATE TABLE indexed_files (
            file_path TEXT PRIMARY KEY,
            mtime REAL,
            file_size INTEGER,
            source_type TEXT,
            page_count INTEGER,
            indexed_at TEXT
        )
    """)
    
    # Bảng FTS5 Toàn văn fulltext_fts (v2.5B)
    cur.execute("""
        CREATE VIRTUAL TABLE fulltext_fts USING fts5(
            file_path UNINDEXED,
            title,
            content,
            content_no_accent,
            source_type UNINDEXED,
            page_count UNINDEXED
        )
    """)
    
    # 3. Nạp cv_di_history.json
    print("\n2. Đang nạp cv_di_history.json...")
    with open(cv_di_path, "r", encoding="utf-8-sig") as f:
        cv_di_list = json.load(f)
        
    di_matched_records = 0
    for row in cv_di_list:
        nam = int(row.get("nam")) if row.get("nam") else None
        so_di = str(row.get("so_di", "")).strip()
        ngay_vb = str(row.get("ngay_vanban", "")).strip()
        trich_yeu = str(row.get("tenloai_trichyeu", "")).strip()
        nguoi_ky = str(row.get("nguoi_ky", "")).strip()
        noi_nhan = str(row.get("noi_nhan", "")).strip()
        
        pdf_info = None
        if nam and (nam, so_di) in pdf_by_nam_sodi:
            pdf_info = pdf_by_nam_sodi[(nam, so_di)]
            
        pdf_path = pdf_info["filepath"] if pdf_info else None
        pdf_pages = pdf_info["page_count"] if pdf_info else None
        pdf_size = pdf_info["file_size"] if pdf_info else None
        pdf_is_scan = pdf_info["is_scan"] if pdf_info else None
        if pdf_info: di_matched_records += 1
            
        combined_text = f"{trich_yeu} {so_di} {nguoi_ky} {noi_nhan}"
        unaccent = remove_accents(combined_text)
        
        cur.execute("""
            INSERT INTO documents (doc_type, nam, so_hieu, ngay_vanban, ngay_nhan, trich_yeu, nguoi_ky, tac_gia, noi_nhan,
                                   pdf_path, pdf_pages, pdf_size, pdf_is_scan, text_no_accent)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, ("di", nam, so_di, ngay_vb, None, trich_yeu, nguoi_ky, None, noi_nhan, pdf_path, pdf_pages, pdf_size, pdf_is_scan, unaccent))
        
        doc_id = cur.lastrowid
        cur.execute("""
            INSERT INTO documents_fts (doc_id, doc_type, so_hieu, ngay_vanban, trich_yeu, nguoi_ky_tac_gia, noi_nhan, text_no_accent, pdf_path, pdf_pages, pdf_is_scan)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (doc_id, "di", so_di, ngay_vb, trich_yeu, nguoi_ky, noi_nhan, unaccent, pdf_path, pdf_pages, pdf_is_scan))
        
    print(f"   Đã nạp {len(cv_di_list)} bản ghi CV đi ({di_matched_records} bản ghi liên kết file PDF).")
    
    # 4. Nạp cv_den_history.json
    print("\n3. Đang nạp cv_den_history.json...")
    with open(cv_den_path, "r", encoding="utf-8-sig") as f:
        cv_den_list = json.load(f)
        
    for row in cv_den_list:
        nam = int(row.get("nam")) if row.get("nam") else None
        ngay_nhan = str(row.get("ngay_nhan", "")).strip()
        tac_gia = str(row.get("tac_gia", "")).strip()
        so_kihieu = str(row.get("so_kihieu", "")).strip()
        ngay_vb = str(row.get("ngay_vanban", "")).strip()
        trich_yeu = str(row.get("trich_yeu", "")).strip()
        donvi_nhan = str(row.get("donvi_nhan", "")).strip()
        
        combined_text = f"{trich_yeu} {so_kihieu} {tac_gia} {donvi_nhan}"
        unaccent = remove_accents(combined_text)
        
        cur.execute("""
            INSERT INTO documents (doc_type, nam, so_hieu, ngay_vanban, ngay_nhan, trich_yeu, nguoi_ky, tac_gia, noi_nhan,
                                   pdf_path, pdf_pages, pdf_size, pdf_is_scan, text_no_accent)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, ("den", nam, so_kihieu, ngay_vb, ngay_nhan, trich_yeu, None, tac_gia, donvi_nhan, None, None, None, None, unaccent))
        
        doc_id = cur.lastrowid
        cur.execute("""
            INSERT INTO documents_fts (doc_id, doc_type, so_hieu, ngay_vanban, trich_yeu, nguoi_ky_tac_gia, noi_nhan, text_no_accent, pdf_path, pdf_pages, pdf_is_scan)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (doc_id, "den", so_kihieu, ngay_vb, trich_yeu, tac_gia, donvi_nhan, unaccent, None, None, None))
        
    print(f"   Đã nạp {len(cv_den_list)} bản ghi CV đến.")
    
    # 5. ĐÁNH CHỈ MỤC TOÀN VĂN (FULL-TEXT FTS5) (v2.5B)
    print("\n4. Đang nạp toàn văn (Full-text FTS5) từ các file PDF có text...")
    now_iso = datetime.datetime.now().isoformat()
    fulltext_count = 0
    
    for p in pdf_records:
        if p["is_scan"] == 0 and p["text"]:
            c_text = p["text"]
            c_unaccent = remove_accents(c_text)
            rel_p = p["filepath"]
            title = p["filename"]
            
            cur.execute("""
                INSERT INTO fulltext_fts (file_path, title, content, content_no_accent, source_type, page_count)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (rel_p, title, c_text, c_unaccent, "sample_pdf", p["page_count"]))
            
            cur.execute("""
                INSERT INTO indexed_files (file_path, mtime, file_size, source_type, page_count, indexed_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (rel_p, p["mtime"], p["file_size"], "sample_pdf", p["page_count"], now_iso))
            
            fulltext_count += 1
            
    print(f"   Đã nạp toàn văn thành công {fulltext_count} file PDF mẫu.")
    
    # Quét thêm golden_jsons nếu đã có
    if os.path.exists(golden_dir):
        for gf in os.listdir(golden_dir):
            if gf.lower().endswith(".json"):
                gpath = os.path.join(golden_dir, gf)
                gtxt = extract_json_text(gpath)
                if gtxt:
                    rel_g = os.path.relpath(gpath, root_dir).replace("\\", "/")
                    cur.execute("""
                        INSERT INTO fulltext_fts (file_path, title, content, content_no_accent, source_type, page_count)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (rel_g, gf, gtxt, remove_accents(gtxt), "golden_json", 1))
                    cur.execute("""
                        INSERT INTO indexed_files (file_path, mtime, file_size, source_type, page_count, indexed_at)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (rel_g, os.path.getmtime(gpath), os.path.getsize(gpath), "golden_json", 1, now_iso))
                    fulltext_count += 1
                    
    # Quét thêm drafts docx/json nếu có
    if os.path.exists(drafts_dir):
        for root, _, files in os.walk(drafts_dir):
            if "incoming" in root or "renders" in root:
                continue
            for df in files:
                ext = os.path.splitext(df)[1].lower()
                if ext in (".docx", ".json"):
                    dpath = os.path.join(root, df)
                    dtxt = extract_docx_text(dpath) if ext == ".docx" else extract_json_text(dpath)
                    if dtxt and len(dtxt) > 30:
                        rel_d = os.path.relpath(dpath, root_dir).replace("\\", "/")
                        cur.execute("""
                            INSERT INTO fulltext_fts (file_path, title, content, content_no_accent, source_type, page_count)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (rel_d, df, dtxt, remove_accents(dtxt), f"draft_{ext.lstrip('.')}", 1))
                        cur.execute("""
                            INSERT INTO indexed_files (file_path, mtime, file_size, source_type, page_count, indexed_at)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (rel_d, os.path.getmtime(dpath), os.path.getsize(dpath), f"draft_{ext.lstrip('.')}", 1, now_iso))
                        fulltext_count += 1

    conn.commit()
    conn.close()
    
    db_size_mb = round(os.path.getsize(db_path) / (1024 * 1024), 2)
    print(f"\n=== TỔNG KẾT BUILD INDEX v2.5B ===")
    print(f"- CSDL SQLite: {db_path} ({db_size_mb} MB)")
    print(f"- Tổng tài liệu Metadata (CV đi + đến): {len(cv_di_list) + len(cv_den_list)}")
    print(f"- Tổng tài liệu Full-text FTS5: {fulltext_count}")
    print("=== HOÀN TẤT BUILD INDEX ===")

if __name__ == "__main__":
    main()
