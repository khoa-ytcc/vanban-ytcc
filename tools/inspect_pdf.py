import os
import re
import sys
import argparse
import pymupdf

def inspect_pdf(pdf_path, render_dir=None, dpi=150):
    if not os.path.exists(pdf_path):
        print(f"Lỗi: Không tìm thấy file PDF tại: {pdf_path}")
        return False
        
    doc = pymupdf.open(pdf_path)
    total_pages = len(doc)
    
    print("=" * 80)
    print(f"BÁO CÁO KIỂM ĐỊNH PDF: {os.path.basename(pdf_path)}")
    print(f"Đường dẫn: {os.path.abspath(pdf_path)}")
    print(f"Tổng số trang: {total_pages}")
    print("=" * 80)
    
    warnings = []
    errors = []
    
    # 1. Kiểm tra kích thước và hướng từng trang
    print("\n1. KÍCH THƯỚC & ĐỊNH DẠNG TRANG:")
    for i in range(total_pages):
        page = doc[i]
        w, h = page.rect.width, page.rect.height
        w_mm, h_mm = round(w * 25.4 / 72, 1), round(h * 25.4 / 72, 1)
        
        is_landscape = w > h
        orient_str = "A4 Ngang (Landscape)" if is_landscape else "A4 Dọc (Portrait)"
        
        # Dung sai chuẩn A4 khoảng 2-3mm
        is_a4 = (abs(w_mm - 210) < 5 and abs(h_mm - 297) < 5) or (abs(w_mm - 297) < 5 and abs(h_mm - 210) < 5)
        a4_check = "CHUẨN A4" if is_a4 else f"KHÁC BIỆT ({w_mm}x{h_mm} mm)"
        
        print(f"   Trang {i+1}: {w_mm} x {h_mm} mm ({orient_str}) -> {a4_check}")
        if not is_a4:
            warnings.append(f"Trang {i+1} có kích thước không khớp chuẩn A4: {w_mm}x{h_mm} mm")
            
    # 2. Kiểm tra text layer và các lỗi thể thức phổ biến
    print("\n2. KIỂM ĐỊNH THỂ THỨC VÀ NỘI DUNG:")
    all_text = ""
    
    for i in range(total_pages):
        page = doc[i]
        ptext = page.get_text()
        all_text += f"\n--- Trang {i+1} ---\n" + ptext
        
        # Trang 1: Kiểm tra Header, Quốc hiệu, Trích yếu
        if i == 0:
            # Lỗi rớt chữ NAM trong Quốc hiệu
            if re.search(r"CỘNG\s+HÒA\s+XÃ\s+HỘI\s+CHỦ\s+NGHĨA\s+VIỆT\s*\n\s*NAM", ptext, re.IGNORECASE):
                errors.append("Trang 1: Lỗi rớt dòng chữ 'NAM' trong Quốc hiệu (Cột 2 bị hẹp).")
            elif "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM" in ptext.upper():
                print("   [OK] Quốc hiệu đầy đủ trên 1 dòng, không rớt chữ NAM.")
                
            # Lỗi lặp V/v
            if re.search(r"V\/v\s+V\/v|V\/v\s+Về\s+việc", ptext, re.IGNORECASE):
                errors.append("Trang 1: Lỗi lặp chuỗi 'V/v V/v' hoặc 'V/v Về việc' ở trích yếu.")
            else:
                print("   [OK] Không có lỗi lặp 'V/v'.")
                
            # Kiểm tra số trang ở Trang 1 (Phải không có)
            first_lines = [line.strip() for line in ptext.split("\n")[:3] if line.strip()]
            if any(line in ("1", "Trang 1", "1/1", "1/2", "1/3") for line in first_lines):
                warnings.append("Trang 1: Xuất hiện số trang ở đầu trang (Nên ẩn số trang ở trang đầu).")
            else:
                print("   [OK] Trang 1 không xuất hiện số trang (đúng quy chuẩn).")
                
        # Trang 2+: Kiểm tra số trang
        if i >= 1:
            first_lines = [line.strip() for line in ptext.split("\n")[:4] if line.strip()]
            has_pnum = any(line.isdigit() and int(line) == (i + 1) for line in first_lines)
            if has_pnum:
                print(f"   [OK] Trang {i+1}: Có đánh số trang '{i+1}' ở phần đầu trang.")
            else:
                warnings.append(f"Trang {i+1}: Không tìm thấy số trang '{i+1}' ở header.")
                
    # Kiểm tra sót biến mẫu (placeholder)
    placeholders = re.findall(r"(\{\{[^}]+\}\})", all_text)
    if placeholders:
        errors.append(f"Còn sót biến mẫu chưa thay thế: {set(placeholders)}")
    else:
        print("   [OK] Không còn sót biến mẫu {{...}}.")
        
    if "None" in all_text or "undefined" in all_text:
        warnings.append("Phát hiện từ 'None' hoặc 'undefined' trong nội dung văn bản.")
    else:
        print("   [OK] Không có từ khóa rác 'None'/'undefined'.")
        
    # Kiểm tra trang cuối (chống rớt trơ khối chữ ký)
    if total_pages > 1:
        last_page_text = doc[total_pages - 1].get_text().strip()
        last_page_len = len(last_page_text)
        print(f"\n3. KIỂM ĐỊNH TRANG CUỐI (Độ dài text: {last_page_len} ký tự):")
        
        # Nếu trang cuối chỉ có < 120 ký tự (thường chỉ đủ cho TRƯỞNG KHOA + Nơi nhận)
        if last_page_len < 130:
            warnings.append(f"CẢNH BÁO NGUY HIỂM: Trang cuối chỉ có {last_page_len} ký tự, có nguy cơ chỉ có khối chữ ký trơ trọi!")
        else:
            print(f"   [OK] Trang cuối có đủ nội dung dẫn nhập ({last_page_len} ký tự), đi kèm khối chữ ký.")
            
    # 3. Xuất ảnh PNG để soi trực quan
    rendered_images = []
    if render_dir:
        os.makedirs(render_dir, exist_ok=True)
        zoom = dpi / 72.0
        mat = pymupdf.Matrix(zoom, zoom)
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        
        print(f"\n4. XUẤT ẢNH PNG (Độ phân giải: {dpi} DPI):")
        for i in range(total_pages):
            pix = doc[i].get_pixmap(matrix=mat)
            img_name = f"{base_name}_p{i+1}.png"
            img_path = os.path.join(render_dir, img_name)
            pix.save(img_path)
            rendered_images.append(img_path)
            print(f"   Đã lưu: {img_path}")
            
    doc.close()
    
    # Tổng kết
    print("\n" + "=" * 80)
    print("KẾT LUẬN KIỂM ĐỊNH:")
    if errors:
        print(f"❌ PHÁT HIỆN {len(errors)} LỖI NGHIÊM TRỌNG:")
        for e in errors: print(f"   - {e}")
    if warnings:
        print(f"⚠️ CẢNH BÁO ({len(warnings)} điểm cần lưu ý):")
        for w in warnings: print(f"   - {w}")
    if not errors and not warnings:
        print("✅ TẤT CẢ CÁC TIÊU CHÍ ĐỀU ĐẠT CHUẨN THỂ THỨC YTCC.")
    print("=" * 80)
    
    return len(errors) == 0

def main():
    parser = argparse.ArgumentParser(description="Kiểm tra chất lượng và thể thức file PDF văn bản YTCC")
    parser.add_argument("--pdf", required=True, help="Đường dẫn file PDF cần kiểm tra")
    parser.add_argument("--render-dir", help="Thư mục xuất ảnh PNG để soi trực quan")
    parser.add_argument("--dpi", type=int, default=150, help="Độ phân giải ảnh PNG (mặc định 150)")
    
    args = parser.parse_args()
    success = inspect_pdf(args.pdf, args.render_dir, args.dpi)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
