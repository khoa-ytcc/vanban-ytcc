import os
import re
import sys
import sqlite3
import argparse
import unicodedata

def remove_accents(input_str):
    if not input_str:
        return ""
    nfkd_form = unicodedata.normalize('NFKD', str(input_str))
    res = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
    res = res.replace('đ', 'd').replace('Đ', 'D')
    return res.lower().strip()

def sanitize_term(term):
    cleaned = re.sub(r'["\'\*\^\:\(\)\{\}\[\]\~\-]', ' ', term)
    tokens = [t.strip() for t in cleaned.split() if t.strip()]
    return tokens

def search_documents(query_str, doc_type="all", limit=5):
    """Tìm kiếm metadata trong bảng documents_fts."""
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(root_dir, "knowledge_base", "metadata_index", "ytcc_history.db")
    
    if not os.path.exists(db_path):
        print(f"Lỗi: Không tìm thấy CSDL tại {db_path}. Vui lòng chạy tools/build_index.py trước.")
        return []
        
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    tokens_raw = sanitize_term(query_str)
    if not tokens_raw:
        conn.close()
        return []
        
    tokens_unaccent = [remove_accents(t) for t in tokens_raw]
    raw_phrase = " ".join(tokens_raw)
    unaccent_phrase = " ".join(tokens_unaccent)
    
    # Ưu tiên 1 (Exact Phrase): Tìm khớp chính xác cả cụm từ
    if len(tokens_raw) > 1:
        fts_match_expr = f'"{raw_phrase}" OR "{unaccent_phrase}"'
    else:
        t_raw = tokens_raw[0]
        t_un = tokens_unaccent[0]
        if t_raw == t_un:
            fts_match_expr = f'"{t_raw}"'
        else:
            fts_match_expr = f'"{t_raw}" OR "{t_un}"'
            
    type_condition = ""
    params = [fts_match_expr]
    
    if doc_type in ("di", "den"):
        type_condition = "AND doc_type = ?"
        params.append(doc_type)
        
    params.append(limit)
    
    sql = f"""
        SELECT doc_id, doc_type, so_hieu, ngay_vanban, trich_yeu, nguoi_ky_tac_gia, noi_nhan,
               pdf_path, pdf_pages, pdf_is_scan, rank
        FROM documents_fts
        WHERE documents_fts MATCH ? {type_condition}
        ORDER BY rank
        LIMIT ?
    """
    
    rows = []
    try:
        cur.execute(sql, params)
        rows = cur.fetchall()
    except sqlite3.OperationalError:
        pass
        
    # Ưu tiên 2 (Fallback khi cụm chính xác ra ít hơn limit): Đủ tất cả từ nguyên vẹn (AND các token, KHÔNG có *)
    if len(rows) < limit and len(tokens_raw) > 1:
        existing_ids = set(r[0] for r in rows)
        and_expr_raw = " AND ".join(f'"{t}"' for t in tokens_raw)
        and_expr_un = " AND ".join(f'"{t}"' for t in tokens_unaccent)
        fallback_expr = f'({and_expr_raw}) OR ({and_expr_un})'
        
        fb_params = [fallback_expr]
        if doc_type in ("di", "den"):
            fb_params.append(doc_type)
        fb_params.append(limit - len(rows))
        
        fb_sql = f"""
            SELECT doc_id, doc_type, so_hieu, ngay_vanban, trich_yeu, nguoi_ky_tac_gia, noi_nhan,
                   pdf_path, pdf_pages, pdf_is_scan, rank
            FROM documents_fts
            WHERE documents_fts MATCH ? {type_condition}
            ORDER BY rank
            LIMIT ?
        """
        try:
            cur.execute(fb_sql, fb_params)
            for r in cur.fetchall():
                if r[0] not in existing_ids:
                    rows.append(r)
        except sqlite3.OperationalError:
            pass

    conn.close()
    return rows

def search_fulltext(query_str, limit=5):
    """Tìm kiếm toàn văn trong bảng fulltext_fts (v2.5B)."""
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(root_dir, "knowledge_base", "metadata_index", "ytcc_history.db")
    
    if not os.path.exists(db_path):
        return []
        
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    tokens_raw = sanitize_term(query_str)
    if not tokens_raw:
        conn.close()
        return []
        
    tokens_unaccent = [remove_accents(t) for t in tokens_raw]
    raw_phrase = " ".join(tokens_raw)
    unaccent_phrase = " ".join(tokens_unaccent)
    
    # Ưu tiên 1 (Exact Phrase): Tìm khớp chính xác cả cụm từ
    if len(tokens_raw) > 1:
        fts_match_expr = f'"{raw_phrase}" OR "{unaccent_phrase}"'
    else:
        t_raw = tokens_raw[0]
        t_un = tokens_unaccent[0]
        if t_raw == t_un:
            fts_match_expr = f'"{t_raw}"'
        else:
            fts_match_expr = f'"{t_raw}" OR "{t_un}"'
            
    sql = """
        SELECT file_path, title, snippet(fulltext_fts, 2, '【', '】', '...', 25), source_type, page_count, rank
        FROM fulltext_fts
        WHERE fulltext_fts MATCH ?
        ORDER BY rank
        LIMIT ?
    """
    
    rows = []
    try:
        cur.execute(sql, (fts_match_expr, limit))
        rows = cur.fetchall()
    except sqlite3.OperationalError:
        pass
        
    # Ưu tiên 2 (Fallback khi cụm chính xác ra ít hơn limit): Đủ tất cả từ nguyên vẹn (AND các token, KHÔNG có *)
    if len(rows) < limit and len(tokens_raw) > 1:
        existing_paths = set(r[0] for r in rows)
        and_expr_raw = " AND ".join(f'"{t}"' for t in tokens_raw)
        and_expr_un = " AND ".join(f'"{t}"' for t in tokens_unaccent)
        fb_expr = f'({and_expr_raw}) OR ({and_expr_un})'
        try:
            cur.execute(sql, (fb_expr, limit - len(rows)))
            for r in cur.fetchall():
                if r[0] not in existing_paths:
                    rows.append(r)
        except sqlite3.OperationalError:
            pass
        except sqlite3.OperationalError:
            pass
            
    conn.close()
    return rows

def print_results(meta_results, fulltext_results, query, doc_type="all", mode="all", limit=5):
    print("=" * 80)
    print(f"KẾT QUẢ TÌM KIẾM (Từ khóa: '{query}' | Chế độ: {mode.upper()} | Giới hạn: {limit})")
    
    meta_count = len(meta_results) if meta_results else 0
    ft_count = len(fulltext_results) if fulltext_results else 0
    print(f"Tổng kết quả: {meta_count} bản ghi metadata | {ft_count} văn bản toàn văn")
    print("=" * 80)
    
    if mode in ("meta", "all") and meta_results:
        print("\n--- 1. KẾT QUẢ METADATA (SỔ CÔNG VĂN ĐI / ĐẾN) ---")
        for idx, r in enumerate(meta_results, 1):
            doc_id, dtype, so_hieu, ngay_vb, trich_yeu, author, noi_nhan, pdf_path, pages, is_scan, _ = r
            type_str = "CV ĐI" if dtype == "di" else "CV ĐẾN"
            author_label = "Người ký" if dtype == "di" else "Tác giả / Nơi gửi"
            dest_label = "Nơi nhận" if dtype == "di" else "Đơn vị nhận"
            
            pdf_info = "Không có"
            if pdf_path:
                scan_str = "SCAN" if is_scan else "TEXT"
                pdf_info = f"{pdf_path} ({pages} trang, {scan_str})"
                
            print(f"[{idx}] [{type_str}] Số: {so_hieu or 'N/A'} | Ngày: {ngay_vb or 'N/A'}")
            print(f"    Trích yếu : {trich_yeu or 'N/A'}")
            print(f"    {author_label:10}: {author or 'N/A'}")
            if noi_nhan:
                print(f"    {dest_label:10}: {noi_nhan}")
            print(f"    File PDF  : {pdf_info}")
            print("-" * 60)
            
    if mode in ("fulltext", "all") and fulltext_results:
        print("\n--- 2. KẾT QUẢ TOÀN VĂN (TRÍCH ĐOẠN NGỮ CẢNH TRONG FILE GỐC) ---")
        for idx, r in enumerate(fulltext_results, 1):
            file_path, title, snippet, stype, pages, _ = r
            # Làm sạch ký tự xuống dòng trong snippet
            clean_snippet = re.sub(r'\s+', ' ', snippet).strip()
            print(f"[{idx}] File: {title} ({stype}, {pages} trang)")
            print(f"    Đường dẫn : {file_path}")
            print(f"    Đoạn trích: {clean_snippet}")
            print("-" * 60)
            
    if not meta_results and not fulltext_results:
        print("Không tìm thấy bản ghi hoặc đoạn trích nào phù hợp.")
        print("-" * 80)

def main():
    parser = argparse.ArgumentParser(description="Tra cứu văn bản lịch sử YTCC qua SQLite FTS5 (Metadata & Full-text)")
    parser.add_argument("--q", required=True, help="Từ khóa tìm kiếm (có dấu hoặc không dấu)")
    parser.add_argument("--type", choices=["di", "den", "all"], default="all", help="Loại văn bản: di, den, all (dành cho metadata)")
    parser.add_argument("--mode", choices=["meta", "fulltext", "all"], default="all", help="Chế độ tra cứu: meta, fulltext, all")
    parser.add_argument("--limit", type=int, default=5, help="Số lượng kết quả tối đa")
    
    args = parser.parse_args()
    meta_res = search_documents(args.q, args.type, args.limit) if args.mode in ("meta", "all") else []
    ft_res = search_fulltext(args.q, args.limit) if args.mode in ("fulltext", "all") else []
    print_results(meta_res, ft_res, args.q, doc_type=args.type, mode=args.mode, limit=args.limit)

if __name__ == "__main__":
    main()
