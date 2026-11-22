import os
import pymupdf

def main():
    root_dir = "D:/TH/vanban-ytcc"
    pdf_dir = os.path.join(root_dir, "knowledge_base", "sample_pdfs")
    out_dir = os.path.join(root_dir, "audit", "p1_renders")
    os.makedirs(out_dir, exist_ok=True)
    
    samples = [
        # Công văn
        ("Cong_van", "Cong_van_SoDi_872.pdf"),
        ("Cong_van", "Cong_van_SoDi_920.pdf"),
        ("Cong_van", "Cong_van_SoDi_843.pdf"),
        # Tờ trình
        ("To_trinh", "To_trinh_SoDi_927.pdf"),
        ("To_trinh", "To_trinh_SoDi_857.pdf"),
        ("To_trinh", "To_trinh_SoDi_913.pdf"),
        # Giấy giới thiệu
        ("Giay_gioi_thieu", "Giay_gioi_thieu_SoDi_932.pdf"),
        ("Giay_gioi_thieu", "Giay_gioi_thieu_SoDi_907.pdf"),
        ("Giay_gioi_thieu", "Giay_gioi_thieu_SoDi_931.pdf"),
        # Kế hoạch
        ("Ke_hoach", "CVDi_2026_SoDi_161_Kế hoạch đào tạo.viên chức, người lao động năm học 2025-2026.pdf"),
        ("Ke_hoach", "Ke_hoach_SoDi_881.pdf"),
        ("Ke_hoach", "Ke_hoach_SoDi_754.pdf"),
        # Báo cáo
        ("Bao_cao", "CVDi_2026_SoDi_345_Báo cáo cơ cấu tổ chức của Khoa Y tế Công cộng.pdf"),
        ("Bao_cao", "Bao_cao_SoDi_937.pdf"),
        ("Bao_cao", "Bao_cao_SoDi_816.pdf")
    ]
    
    zoom = 150 / 72.0
    mat = pymupdf.Matrix(zoom, zoom)
    
    rendered_info = []
    
    for idx, (doc_type, fname) in enumerate(samples, 1):
        fpath = os.path.join(pdf_dir, fname)
        doc = pymupdf.open(fpath)
        total_p = len(doc)
        
        # Xác định các trang cần render (0-indexed)
        if total_p == 1:
            pages_to_render = [0]
        elif total_p == 2:
            pages_to_render = [0, 1]
        else:
            pages_to_render = [0, 1, total_p - 1]
            
        print(f"[{idx:02d}] {doc_type:15} | {fname[:40]:40} | Tổng: {total_p} trang -> Render: {[p+1 for p in pages_to_render]}")
        
        # Tên định danh ngắn cho file ảnh
        safe_name = os.path.splitext(fname)[0]
        if len(safe_name) > 40:
            safe_name = safe_name[:40].rstrip("._")
            
        for pno in pages_to_render:
            page = doc[pno]
            pix = page.get_pixmap(matrix=mat)
            out_name = f"{idx:02d}_{doc_type}_p{pno+1}_{safe_name}.png"
            out_path = os.path.join(out_dir, out_name)
            pix.save(out_path)
            
            # Trích xuất thông tin text và layout
            text = page.get_text()
            rendered_info.append({
                "index": idx,
                "type": doc_type,
                "filename": fname,
                "total_pages": total_p,
                "page_no": pno + 1,
                "png_name": out_name,
                "png_path": out_path,
                "text_snippet": text[:400] if text else "[SCAN/IMAGE ONLY]"
            })
            
        doc.close()
        
    print(f"\nĐã xuất toàn bộ {len(rendered_info)} ảnh PNG tại: {out_dir}")

if __name__ == "__main__":
    main()
