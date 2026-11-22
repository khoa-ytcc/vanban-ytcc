import os
import re
import json
import sqlite3
import unicodedata
import pymupdf

def remove_accents(input_str):
    if not input_str:
        return ""
    nfkd_form = unicodedata.normalize('NFKD', str(input_str))
    res = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
    res = res.replace('đ', 'd').replace('Đ', 'D')
    return res.lower().strip()

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    meta_dir = os.path.join(root_dir, "knowledge_base", "metadata_index")
    pdf_dir = os.path.join(root_dir, "knowledge_base", "sample_pdfs")
    db_path = os.path.join(meta_dir, "ytcc_history.db")
    
    cv_di_path = os.path.join(meta_dir, "cv_di_history.json")
    cv_den_path = os.path.join(meta_dir, "cv_den_history.json")
    
    print(f"=== KHỞI TẠO INDEX SQLITE FTS5: {db_path} ===")
    
    # 1. Quét toàn bộ file PDF trong sample_pdfs
    print("\n1. Đang quét 100% file PDF trong knowledge_base/sample_pdfs/...")
    pdf_files = [f for f in os.listdir(pdf_dir) if f.lower().endswith(".pdf")]
    total_pdfs = len(pdf_files)
    print(f"   Tìm thấy {total_pdfs} file PDF.")
    
    pdf_records = []
    # Map theo (nam, so_di) -> pdf item (ưu tiên file có tên CVDi_...)
    pdf_by_nam_sodi = {}
    matched_pdf_count = 0
    
    page_dist = {"1_page": 0, "2_pages": 0, "3_plus_pages": 0}
    scan_counts = {"scan": 0, "has_text": 0}
    
    for fname in pdf_files:
        fpath = os.path.join(pdf_dir, fname)
        fsize = os.path.getsize(fpath)
        
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
            is_scan = 1
        
        # Phân bố trang
        if num_pages == 1:
            page_dist["1_page"] += 1
        elif num_pages == 2:
            page_dist["2_pages"] += 1
        else:
            page_dist["3_plus_pages"] += 1
            
        if is_scan:
            scan_counts["scan"] += 1
        else:
            scan_counts["has_text"] += 1
            
        # Parse tên file lấy so_di và nam
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
            "file_size": fsize,
            "page_count": num_pages,
            "is_scan": is_scan,
            "text_len": text_len,
            "so_di": matched_sodi,
            "nam": matched_nam
        }
        pdf_records.append(item)
        
        if matched_nam and matched_sodi:
            matched_pdf_count += 1
            key = (matched_nam, matched_sodi)
            # Ưu tiên lưu file có tên dài CVDi_ nếu trùng
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
    
    # Bảng FTS5
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
        if pdf_info:
            di_matched_records += 1
            
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
    
    conn.commit()
    conn.close()
    
    # 5. In báo cáo tổng kết
    print("\n=== THỐNG KÊ KHO DỮ LIỆU ===")
    print(f"- Tổng CV đi nạp: {len(cv_di_list)}")
    print(f"- Tổng CV đến nạp: {len(cv_den_list)}")
    print(f"- Tổng PDF quét: {total_pdfs}")
    print(f"  + Tỷ lệ scan vs text: {scan_counts['scan']} scan ({scan_counts['scan']/total_pdfs*100:.1f}%) | {scan_counts['has_text']} has_text ({scan_counts['has_text']/total_pdfs*100:.1f}%)")
    print(f"  + Phân bố trang:")
    print(f"    * 1 trang: {page_dist['1_page']} ({page_dist['1_page']/total_pdfs*100:.1f}%)")
    print(f"    * 2 trang: {page_dist['2_pages']} ({page_dist['2_pages']/total_pdfs*100:.1f}%)")
    print(f"    * 3+ trang: {page_dist['3_plus_pages']} ({page_dist['3_plus_pages']/total_pdfs*100:.1f}%)")
    print(f"- Số file PDF khớp với số đi trong lịch sử: {matched_pdf_count}/{total_pdfs} ({matched_pdf_count/total_pdfs*100:.1f}%)")
    print(f"- Số bản ghi CV đi có file PDF liên kết: {di_matched_records}/{len(cv_di_list)} ({di_matched_records/len(cv_di_list)*100:.1f}%)")
    print("=== HOÀN TẤT BUILD INDEX ===")

if __name__ == "__main__":
    main()
