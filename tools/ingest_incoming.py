import os
import sys
import shutil
import datetime
import argparse
import docx
import pymupdf

def extract_text_from_pdf(pdf_path):
    doc = pymupdf.open(pdf_path)
    total_pages = len(doc)
    text_content = []
    for i in range(total_pages):
        page_text = doc[i].get_text()
        text_content.append(f"--- TRANG {i + 1} / {total_pages} ---\n{page_text.strip()}\n")
    doc.close()
    return total_pages, "\n".join(text_content)

def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    lines = []
    for p in doc.paragraphs:
        if p.text.strip():
            lines.append(p.text.strip())
    for tbl in doc.tables:
        for r in tbl.rows:
            row_txt = " | ".join(c.text.strip() for c in r.cells if c.text.strip())
            if row_txt:
                lines.append(f"[BẢNG] {row_txt}")
    return 1, "\n\n".join(lines)

def render_pdf_pages(pdf_path, output_dir, max_pages=5, dpi=150):
    doc = pymupdf.open(pdf_path)
    total_pages = len(doc)
    pages_to_render = min(total_pages, max_pages)
    zoom = dpi / 72.0
    mat = pymupdf.Matrix(zoom, zoom)
    rendered_images = []
    
    for i in range(pages_to_render):
        pix = doc[i].get_pixmap(matrix=mat)
        img_name = f"page_{i + 1:02d}.png"
        img_path = os.path.join(output_dir, img_name)
        pix.save(img_path)
        rendered_images.append(img_path)
        
    doc.close()
    return rendered_images

def ingest_document(file_path, case_name, month_str=None, max_pages=5, base_dir=None):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Không tìm thấy file nguồn: {file_path}")
        
    now = datetime.datetime.now()
    if not month_str:
        month_str = now.strftime("%Y-%m")
        
    date_prefix = now.strftime("%Y%m%d")
    folder_name = f"{date_prefix}_{case_name}"
    
    if not base_dir:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        
    case_dir = os.path.join(base_dir, "drafts", month_str, folder_name)
    incoming_dir = os.path.join(case_dir, "incoming")
    os.makedirs(incoming_dir, exist_ok=True)
    
    # 1. Copy file gốc vào incoming/
    file_ext = os.path.splitext(file_path)[1].lower()
    dest_filename = os.path.basename(file_path)
    dest_file_path = os.path.join(incoming_dir, dest_filename)
    shutil.copy2(file_path, dest_file_path)
    
    # 2. Bóc tách văn bản
    extracted_text = ""
    total_pages = 1
    rendered_images = []
    
    if file_ext == ".pdf":
        total_pages, extracted_text = extract_text_from_pdf(dest_file_path)
        rendered_images = render_pdf_pages(dest_file_path, incoming_dir, max_pages=max_pages, dpi=150)
    elif file_ext in (".docx", ".doc"):
        total_pages, extracted_text = extract_text_from_docx(dest_file_path)
    elif file_ext in (".png", ".jpg", ".jpeg"):
        extracted_text = f"[Văn bản ảnh scan: {dest_filename}]\n(Người dùng vui lòng xem trực tiếp file ảnh để bóc tách nội dung)."
        # Copy chính ảnh đó làm page_01.png nếu tiện lợi
        img_copy = os.path.join(incoming_dir, "page_01.png")
        if not os.path.exists(img_copy):
            shutil.copy2(dest_file_path, img_copy)
        rendered_images.append(img_copy)
    else:
        extracted_text = f"[Định dạng {file_ext} chưa hỗ trợ bóc tách tự động]"
        
    # Ghi file text trích xuất
    txt_out_path = os.path.join(incoming_dir, "extracted_text.txt")
    with open(txt_out_path, "w", encoding="utf-8") as f:
        f.write(extracted_text)
        
    word_count = len(extracted_text.split())
    file_size_kb = round(os.path.getsize(dest_file_path) / 1024, 1)
    
    return {
        "case_dir": case_dir,
        "incoming_dir": incoming_dir,
        "dest_file": dest_file_path,
        "txt_file": txt_out_path,
        "total_pages": total_pages,
        "word_count": word_count,
        "file_size_kb": file_size_kb,
        "rendered_images": rendered_images
    }

def print_ingest_report(result):
    print("=" * 75)
    print("TIẾP NHẬN & TIỀN XỬ LÝ VĂN BẢN ĐẾN THÀNH CÔNG (INGEST COMPLETED)")
    print("=" * 75)
    print(f"Thư mục Case:       {result['case_dir']}")
    print(f"File nguồn đã lưu:  {result['dest_file']} ({result['file_size_kb']} KB)")
    print(f"File text trích xuất: {result['txt_file']} (~{result['word_count']} từ)")
    print(f"Tổng số trang:      {result['total_pages']} trang")
    if result["rendered_images"]:
        print(f"Ảnh render ({len(result['rendered_images'])} trang đầu, 150 DPI):")
        for img in result["rendered_images"]:
            print(f"  - {img}")
    print("=" * 75)

def main():
    parser = argparse.ArgumentParser(description="YTCC Incoming Document Ingest CLI")
    parser.add_argument("--file", required=True, help="Đường dẫn file văn bản đến (.pdf, .docx, .png, .jpg)")
    parser.add_argument("--case", required=True, help="Tên case xử lý (ví dụ: giao_vien_chu_nhiem, tap_huan_y_te)")
    parser.add_argument("--month", help="Thư mục tháng lưu trữ (mặc định lấy tháng hiện tại YYYY-MM)")
    parser.add_argument("--max-pages", type=int, default=5, help="Số trang tối đa render ra ảnh PNG (mặc định 5)")
    
    args = parser.parse_args()
    try:
        res = ingest_document(args.file, args.case, month_str=args.month, max_pages=args.max_pages)
        print_ingest_report(res)
        sys.exit(0)
    except Exception as e:
        print(f"Lỗi tiếp nhận văn bản: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
