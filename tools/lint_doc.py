import os
import re
import sys
import json
import datetime
import argparse

VN_WEEKDAY_MAP = {
    "hai": 0, "2": 0,
    "ba": 1, "3": 1,
    "tư": 2, "tu": 2, "bốn": 2, "bon": 2, "4": 2,
    "năm": 3, "nam": 3, "5": 3,
    "sáu": 4, "sau": 4, "6": 4,
    "bảy": 5, "bay": 5, "7": 5,
    "chủ nhật": 6, "chu nhat": 6, "cn": 6
}

VN_WEEKDAY_NAMES = {
    0: "Thứ Hai",
    1: "Thứ Ba",
    2: "Thứ Tư",
    3: "Thứ Năm",
    4: "Thứ Sáu",
    5: "Thứ Bảy",
    6: "Chủ nhật"
}

def parse_vn_number(val_str):
    """Bóc tách số thực từ chuỗi số kiểu Việt Nam (hỗ trợ dấu . hoặc , phân cách hàng nghìn, đơn vị đồng/VNĐ)."""
    if val_str is None:
        return None
    cleaned = re.sub(r'[*_]', '', str(val_str)).strip()
    cleaned = re.sub(r'(?:đồng|VNĐ|VND|đ|\$)', '', cleaned, flags=re.I).strip()
    if not cleaned:
        return None
        
    # Kiểu 1.000.000 hoặc 1.000.000,50
    if re.fullmatch(r'\d{1,3}(?:\.\d{3})+(?:,\d+)?', cleaned):
        num_str = cleaned.replace('.', '').replace(',', '.')
        try:
            return float(num_str)
        except ValueError:
            return None
    # Kiểu 1,000,000 hoặc 1,000,000.50
    elif re.fullmatch(r'\d{1,3}(?:,\d{3})+(?:\.\d+)?', cleaned):
        num_str = cleaned.replace(',', '')
        try:
            return float(num_str)
        except ValueError:
            return None
    # Số nguyên hoặc số thập phân thuần túy
    elif re.fullmatch(r'\d+(?:[.,]\d+)?', cleaned):
        num_str = cleaned.replace(',', '.')
        try:
            return float(num_str)
        except ValueError:
            return None
    return None

def extract_all_text(data):
    """Trích xuất toàn bộ text từ JSON văn bản kèm đường dẫn vị trí."""
    items = []
    
    # Header
    hdr = data.get("header", {})
    if isinstance(hdr, dict):
        for k, v in hdr.items():
            if isinstance(v, str):
                items.append((f"header.{k}", v))
                
    # Title
    if "title" in data and isinstance(data["title"], str):
        items.append(("title", data["title"]))
    if "trich_yeu" in data and isinstance(data["trich_yeu"], str):
        items.append(("trich_yeu", data["trich_yeu"]))
        
    # Blocks
    def collect_blocks(blocks, prefix="blocks"):
        if not isinstance(blocks, list):
            return
        for idx, b in enumerate(blocks):
            if not isinstance(b, dict):
                continue
            path = f"{prefix}[{idx}]"
            btype = b.get("type", "")
            if "text" in b and isinstance(b["text"], str):
                items.append((f"{path}.text", b["text"]))
            if "prefix_bold" in b and isinstance(b["prefix_bold"], str):
                items.append((f"{path}.prefix_bold", b["prefix_bold"]))
            if "items" in b and isinstance(b["items"], list):
                for i_idx, item in enumerate(b["items"]):
                    if isinstance(item, str):
                        items.append((f"{path}.items[{i_idx}]", item))
                    elif isinstance(item, dict):
                        for ik, iv in item.items():
                            if isinstance(iv, str):
                                items.append((f"{path}.items[{i_idx}].{ik}", iv))
            if btype == "table":
                headers = b.get("headers", [])
                for h_idx, h in enumerate(headers):
                    items.append((f"{path}.headers[{h_idx}]", str(h)))
                rows = b.get("rows", [])
                for r_idx, row in enumerate(rows):
                    for c_idx, cell in enumerate(row):
                        items.append((f"{path}.rows[{r_idx}][{c_idx}]", str(cell)))
            if btype == "landscape_section":
                collect_blocks(b.get("blocks", []), f"{path}.blocks")

    collect_blocks(data.get("blocks", []), "blocks")
    collect_blocks(data.get("post_sign_blocks", []), "post_sign_blocks")
    
    # Sign block
    sb = data.get("sign_block", {})
    if isinstance(sb, dict):
        for k, v in sb.items():
            if isinstance(v, str):
                items.append((f"sign_block.{k}", v))
            elif isinstance(v, list):
                for i_idx, item in enumerate(v):
                    if isinstance(item, str):
                        items.append((f"sign_block.{k}[{i_idx}]", item))
                        
    return items

def check_table_sums(blocks, prefix="blocks"):
    """Kiểm tra logic cộng dồn của các bảng trong blocks."""
    errors = []
    if not isinstance(blocks, list):
        return errors
        
    for b_idx, b in enumerate(blocks):
        if not isinstance(b, dict):
            continue
        path = f"{prefix}[{b_idx}]"
        btype = b.get("type", "")
        if btype == "table":
            rows = b.get("rows", [])
            headers = b.get("headers", [])
            if not rows:
                continue
                
            for r_idx, row in enumerate(rows):
                # Nhận diện dòng tổng cộng: có từ khóa ở bất kỳ cột nào
                row_str = " ".join(str(cell).lower() for cell in row)
                is_sum_row = any(kw in row_str for kw in ["tổng cộng", "tổng kinh phí", "tổng số", "tổng chi phí", "tổng kinh phí dự kiến", "cộng:"])
                if not is_sum_row and row:
                    # Kiểm tra riêng cột 0 hoặc 1 có chữ "cộng"
                    first_cell = str(row[0]).strip().lower()
                    second_cell = str(row[1]).strip().lower() if len(row) > 1 else ""
                    if first_cell in ("cộng", "tổng cộng") or second_cell in ("cộng", "tổng cộng"):
                        is_sum_row = True
                        
                if is_sum_row:
                    # Duyệt qua các cột xem cột nào có số
                    for c_idx, cell in enumerate(row):
                        stated_val = parse_vn_number(cell)
                        if stated_val is not None:
                            # Tính tổng các hàng trước đó tại cùng cột c_idx
                            prev_sum = 0.0
                            count = 0
                            for prev_r in range(r_idx):
                                prev_cell = rows[prev_r][c_idx] if c_idx < len(rows[prev_r]) else None
                                num = parse_vn_number(prev_cell)
                                if num is not None:
                                    prev_sum += num
                                    count += 1
                                    
                            if count > 0 and abs(stated_val - prev_sum) > 0.01:
                                errors.append(
                                    f"TABLE_SUM_MISMATCH: Tại {path} hàng {r_idx + 1} (dòng '{row[0] or (row[1] if len(row) > 1 else '')}'), "
                                    f"cột {c_idx + 1}: giá trị ghi là {stated_val:,.0f} nhưng tổng thực tế của {count} hàng bên trên là {prev_sum:,.0f} "
                                    f"(sai lệch {stated_val - prev_sum:,.0f})."
                                )
        elif btype == "landscape_section":
            errors.extend(check_table_sums(b.get("blocks", []), f"{path}.blocks"))
            
    return errors

def check_calendar_consistency(all_texts):
    """Rà soát và kiểm tra đối chiếu ngày trong tuần với lịch thực tế."""
    errors = []
    
    # Regex 1: Thứ [X], ngày DD/MM/YYYY hoặc DD-MM-YYYY
    p1 = re.compile(
        r'thứ\s+(hai|ba|tư|tu|bốn|bon|năm|nam|sáu|sau|bảy|bay|chủ\s+nhật|chu\s+nhat|cn|[2-7])[,\s]+ngày\s+(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{4})',
        re.IGNORECASE
    )
    # Regex 2: Thứ [X], ngày DD tháng MM năm YYYY
    p2 = re.compile(
        r'thứ\s+(hai|ba|tư|tu|bốn|bon|năm|nam|sáu|sau|bảy|bay|chủ\s+nhật|chu\s+nhat|cn|[2-7])[,\s]+ngày\s+(\d{1,2})\s+tháng\s+(\d{1,2})\s+năm\s+(\d{4})',
        re.IGNORECASE
    )
    
    for path, text in all_texts:
        for p in (p1, p2):
            for m in p.finditer(text):
                full_match = m.group(0)
                raw_day = m.group(1).lower().strip()
                dd = int(m.group(2))
                mm = int(m.group(3))
                yyyy = int(m.group(4))
                
                # Chuẩn hóa thứ
                normalized_day_key = re.sub(r'\s+', ' ', raw_day)
                stated_weekday = VN_WEEKDAY_MAP.get(normalized_day_key)
                if stated_weekday is None:
                    continue
                    
                try:
                    target_date = datetime.date(yyyy, mm, dd)
                    actual_weekday = target_date.weekday()
                    if stated_weekday != actual_weekday:
                        errors.append(
                            f"CALENDAR_DAY_MISMATCH: Tại {path}: '{full_match}' không khớp với lịch thực tế. "
                            f"Ngày {dd:02d}/{mm:02d}/{yyyy} là {VN_WEEKDAY_NAMES[actual_weekday]}, không phải {VN_WEEKDAY_NAMES[stated_weekday]}."
                        )
                except ValueError as e:
                    errors.append(f"CALENDAR_INVALID_DATE: Tại {path}: '{full_match}' là ngày không hợp lệ ({e}).")
                    
    return errors

def check_administrative_rules(data, all_texts, strict_final=False):
    """Kiểm tra nhất quán hành chính: lặp trích yếu, quy cách doc_type, và placeholder."""
    errors = []
    warnings = []
    
    doc_type = data.get("doc_type", "").lower()
    header = data.get("header", {})
    sign_block = data.get("sign_block", {})
    
    # 1. Kiểm tra lặp trích yếu
    trich_yeu = header.get("trich_yeu", "") or data.get("trich_yeu", "")
    if trich_yeu:
        ty_clean = trich_yeu.strip()
        if re.search(r'^(?:v\/v|về việc)\s+(?:v\/v|về việc)', ty_clean, flags=re.IGNORECASE):
            errors.append(f"REPEAT_TRICH_YEU: Trích yếu bị lặp tiền tố: '{trich_yeu}'")
            
    # 2. Kiểm tra tính nhất quán giữa doc_type và header/ma_loai/so_hieu
    header_level = header.get("header_level", "ytcc").lower()
    ma_loai = str(header.get("ma_loai", "")).strip().upper()
    so_hieu = str(header.get("so_hieu", "")).strip().upper()
    full_code = f"{so_hieu}/{ma_loai}" if ma_loai and "/" not in so_hieu else so_hieu

    if doc_type == "to_trinh":
        if ("YTCC-VP" in full_code or "GGT" in full_code or "KH-YTCC" in full_code or "BC-YTCC" in full_code) and "TTR" not in full_code:
            errors.append(f"DOC_TYPE_CODE_MISMATCH: doc_type là 'to_trinh' nhưng số hiệu/mã loại là '{full_code}' (kỳ vọng chứa 'TTr' như 'TTr-YTCC').")
        elif ma_loai and "TTR" not in ma_loai:
            errors.append(f"DOC_TYPE_CODE_MISMATCH: doc_type là 'to_trinh' nhưng mã loại là '{ma_loai}' (kỳ vọng chứa 'TTr' như 'TTr-YTCC').")
    elif doc_type == "giay_gioi_thieu":
        if header_level != "ump":
            errors.append("DOC_TYPE_CODE_MISMATCH: doc_type là 'giay_gioi_thieu' bắt buộc dùng header_level 'ump' (cấp Trường ĐHYD TP.HCM).")
        if ("YTCC-VP" in full_code or "TTR" in full_code or "KH-YTCC" in full_code or "BC-YTCC" in full_code) and "GGT" not in full_code:
            errors.append(f"DOC_TYPE_CODE_MISMATCH: doc_type là 'giay_gioi_thieu' nhưng số hiệu/mã loại là '{full_code}' (kỳ vọng chứa 'GGT' như 'GGT-YTCC').")
    elif doc_type == "ke_hoach":
        if ("TTR" in full_code or "GGT" in full_code or "BC-YTCC" in full_code) and "KH" not in full_code:
            errors.append(f"DOC_TYPE_CODE_MISMATCH: doc_type là 'ke_hoach' nhưng số hiệu/mã loại là '{full_code}' (kỳ vọng chứa 'KH' như 'KH-YTCC').")
    elif doc_type == "bao_cao":
        if ("TTR" in full_code or "GGT" in full_code or "KH" in full_code) and "BC" not in full_code:
            errors.append(f"DOC_TYPE_CODE_MISMATCH: doc_type là 'bao_cao' nhưng số hiệu/mã loại là '{full_code}' (kỳ vọng chứa 'BC' như 'BC-YTCC').")
    elif doc_type == "cong_van":
        if any(bad in full_code for bad in ["TTR-", "GGT-", "KH-", "BC-"]):
            errors.append(f"DOC_TYPE_CODE_MISMATCH: doc_type là 'cong_van' nhưng số hiệu/mã loại là '{full_code}' (kỳ vọng mã loại công văn hành chính thông thường như 'YTCC' hoặc 'YTCC-VP').")
            
    # 3. Kiểm tra placeholder còn sót
    # Các mẫu placeholder phổ biến
    placeholder_patterns = [
        (re.compile(r'\[[A-ZÀÁẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬĐÈÉẺẼẸÊẾỀỂỄỆÌÍỈĨỊÒÓỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÙÚỦŨỤƯỨỪỬỮỰỲÝỶỸỴ\s_0-9\-\.\,]{2,}\]'), "Dạng [CHỮ IN HOA]"),
        (re.compile(r'\b(?:xxx|XXX)\b'), "Ký tự 'xxx'"),
    ]
    
    # Placeholder riêng cho số hiệu, ngày tháng trong header nếu chưa điền
    if "...." in so_hieu or "..." in so_hieu:
        msg = f"Số hiệu văn bản chưa điền: '{so_hieu}'"
        if strict_final: errors.append(f"ERROR_UNFILLED_PLACEHOLDER: {msg}")
        else: warnings.append(f"WARNING_UNFILLED_PLACEHOLDER: {msg}")
        
    for k in ("ngay", "thang", "nam"):
        v = str(header.get(k, "")).strip()
        if "..." in v or "...." in v:
            msg = f"Trường header.{k} chưa điền: '{v}'"
            if strict_final: errors.append(f"ERROR_UNFILLED_PLACEHOLDER: {msg}")
            else: warnings.append(f"WARNING_UNFILLED_PLACEHOLDER: {msg}")
            
    for path, text in all_texts:
        for pat, desc in placeholder_patterns:
            matches = pat.findall(text)
            for m in matches:
                msg = f"Tại {path}: chứa placeholder chưa điền '{m}' ({desc})"
                if strict_final:
                    errors.append(f"ERROR_UNFILLED_PLACEHOLDER: {msg}")
                else:
                    warnings.append(f"WARNING_UNFILLED_PLACEHOLDER: {msg}")
                    
    return errors, warnings

def lint_document(json_path_or_dict, strict_final=False):
    """
    Hàm linter trung tâm:
    Trả về dict: { 'valid': bool, 'errors': list, 'warnings': list }
    """
    if isinstance(json_path_or_dict, dict):
        data = json_path_or_dict
    else:
        with open(json_path_or_dict, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
            
    all_texts = extract_all_text(data)
    
    errors = []
    warnings = []
    
    # 1. Bảng biểu
    tbl_errors = check_table_sums(data.get("blocks", []), "blocks")
    if "post_sign_blocks" in data:
        tbl_errors.extend(check_table_sums(data.get("post_sign_blocks", []), "post_sign_blocks"))
    errors.extend(tbl_errors)
    
    # 2. Lịch hành chính
    cal_errors = check_calendar_consistency(all_texts)
    errors.extend(cal_errors)
    
    # 3. Quy chuẩn hành chính & placeholder
    adm_errors, adm_warnings = check_administrative_rules(data, all_texts, strict_final=strict_final)
    errors.extend(adm_errors)
    warnings.extend(adm_warnings)
    
    is_valid = (len(errors) == 0)
    return {
        "valid": is_valid,
        "errors": errors,
        "warnings": warnings
    }

def print_lint_report(file_path, results):
    print("=" * 70)
    print(f"BÁO CÁO KIỂM TRA HÀNH CHÍNH (LINTER REPORT): {file_path}")
    status_str = "HỢP LỆ (PASS)" if results["valid"] else "CÓ LỖI CHẶN (FAIL)"
    print(f"Trạng thái: [{status_str}] - {len(results['errors'])} lỗi, {len(results['warnings'])} cảnh báo")
    print("-" * 70)
    
    if results["errors"]:
        print("DANH SÁCH LỖI (ERRORS):")
        for idx, err in enumerate(results["errors"], 1):
            print(f"  {idx}. [LỖI] {err}")
            
    if results["warnings"]:
        print("\nDANH SÁCH CẢNH BÁO (WARNINGS):")
        for idx, warn in enumerate(results["warnings"], 1):
            print(f"  {idx}. [CẢNH BÁO] {warn}")
            
    if not results["errors"] and not results["warnings"]:
        print("Tuyệt vời! Không phát hiện bất kỳ lỗi hay cảnh báo nào.")
    print("=" * 70)

def main():
    parser = argparse.ArgumentParser(description="YTCC Administrative Document Linter")
    parser.add_argument("--input", required=True, help="Đường dẫn file JSON mô tả văn bản")
    parser.add_argument("--strict-final", action="store_true", help="Bật chế độ nghiệm thu gắt gao (chặn mọi placeholder còn sót)")
    
    args = parser.parse_args()
    results = lint_document(args.input, strict_final=args.strict_final)
    print_lint_report(args.input, results)
    
    sys.exit(0 if results["valid"] else 1)

if __name__ == "__main__":
    main()
