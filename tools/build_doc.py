import os
import re
import sys
import json
import argparse
import subprocess

import docx
from docx import Document
from docx.shared import Inches, Pt, Mm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.section import WD_SECTION, WD_ORIENTATION
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

VALID_DOC_TYPES = ["cong_van", "to_trinh", "giay_gioi_thieu", "ke_hoach", "bao_cao", "chung"]
VALID_BLOCK_TYPES = [
    "paragraph", "p",
    "heading", "h1", "h2", "h3",
    "bullet",
    "key_value",
    "table",
    "quote", "trich_dan",
    "kinh_gui",
    "landscape_section"
]
ALLOWED_ROOT_KEYS = [
    "doc_type", "target_one_page", "title", "trich_yeu",
    "has_bgh_approval", "bgh_approver_title", "bgh_approver_name", "bgh_sign_gap_pt",
    "header", "blocks", "sign_block", "post_sign_blocks"
]

def add_markdown_runs(paragraph, text, font_size=Pt(13), base_bold=False, base_italic=False, font_name="Times New Roman", font_color=None):
    """
    Parser inline markdown chuyển đổi các cú pháp:
      ***đậm nghiêng*** -> bold=True, italic=True
      **in đậm**        -> bold=True, italic=base_italic
      *in nghiêng*      -> bold=base_bold, italic=True
      chữ thường        -> bold=base_bold, italic=base_italic
    Đảm bảo không sót ký tự '*' trong Word và hỗ trợ tiếng Việt có dấu.
    """
    if not text:
        return
    text = str(text)
    pattern = re.compile(r'(\*\*\*.*?\*\*\*|\*\*.*?\*\*|\*.*?\*)', re.DOTALL)
    tokens = pattern.split(text)
    for token in tokens:
        if not token:
            continue
        if token.startswith("***") and token.endswith("***") and len(token) >= 6:
            run_text = token[3:-3]
            is_bold = True
            is_italic = True
        elif token.startswith("**") and token.endswith("**") and len(token) >= 4:
            run_text = token[2:-2]
            is_bold = True
            is_italic = base_italic
        elif token.startswith("*") and token.endswith("*") and len(token) >= 2:
            run_text = token[1:-1]
            is_bold = base_bold
            is_italic = True
        else:
            run_text = token
            is_bold = base_bold
            is_italic = base_italic
            
        r = paragraph.add_run(run_text)
        r.font.name = font_name
        r.font.size = font_size
        if is_bold:
            r.font.bold = True
        if is_italic:
            r.font.italic = True
        if font_color:
            r.font.color.rgb = font_color

def validate_blocks(blocks, prefix="blocks"):
    errors = []
    if not isinstance(blocks, list):
        errors.append(f"{prefix}: phải là danh sách (list)")
        return errors
        
    for idx, b in enumerate(blocks):
        path = f"{prefix}[{idx}]"
        if not isinstance(b, dict):
            errors.append(f"{path}: mỗi block phải là một object (dict)")
            continue
            
        btype = b.get("type")
        if not btype:
            errors.append(f"{path}: thiếu trường 'type'")
            continue
            
        if btype not in VALID_BLOCK_TYPES:
            hint = ""
            if btype == "para":
                hint = ", hãy dùng 'p' hoặc 'paragraph'"
            elif btype in ("h", "head"):
                hint = ", hãy dùng 'heading', 'h1', 'h2' hoặc 'h3'"
            elif btype == "tbl":
                hint = ", hãy dùng 'table'"
            errors.append(f"{path}.type: kiểu '{btype}' không hợp lệ{hint}. Các kiểu hợp lệ: {', '.join(VALID_BLOCK_TYPES)}")
            continue
            
        if btype in ("paragraph", "p"):
            if "text" not in b and "prefix_bold" not in b:
                errors.append(f"{path}: đoạn văn cần có trường 'text' hoặc 'prefix_bold'")
        elif btype in ("heading", "h1", "h2", "h3"):
            if "text" not in b:
                errors.append(f"{path}: tiêu đề mục (heading) cần có trường 'text'")
            if btype == "heading" and "level" in b and b["level"] not in (1, 2, 3):
                errors.append(f"{path}.level: level heading phải là 1, 2 hoặc 3")
        elif btype == "bullet":
            if "text" not in b:
                errors.append(f"{path}: danh sách bullet cần có trường 'text'")
        elif btype in ("quote", "trich_dan"):
            if "text" not in b:
                errors.append(f"{path}: trích dẫn (quote) cần có trường 'text'")
        elif btype == "table":
            if "rows" not in b or not isinstance(b.get("rows"), list):
                errors.append(f"{path}: bảng biểu (table) cần có mảng 'rows'")
        elif btype == "key_value":
            if "items" not in b or not isinstance(b.get("items"), list):
                errors.append(f"{path}: key_value cần có mảng 'items'")
        elif btype == "kinh_gui":
            if "items" not in b and "text" not in b:
                errors.append(f"{path}: kinh_gui cần có trường 'items' (mảng) hoặc 'text' (chuỗi)")
        elif btype == "landscape_section":
            if "blocks" not in b or not isinstance(b.get("blocks"), list):
                errors.append(f"{path}: landscape_section cần có mảng 'blocks'")
            else:
                errors.extend(validate_blocks(b["blocks"], f"{path}.blocks"))
                
    return errors

def validate_schema(data):
    """
    Strict Schema Validator kiểm tra toàn diện cấu trúc dữ liệu JSON đầu vào.
    Trả về danh sách các lỗi phát hiện được.
    """
    errors = []
    if not isinstance(data, dict):
        return ["Dữ liệu JSON gốc phải là một dictionary/object."]
        
    # 1. Kiểm tra các root keys lạ
    for k in data.keys():
        if k not in ALLOWED_ROOT_KEYS:
            errors.append(f"Root key không xác định: '{k}'. Các key hợp lệ: {', '.join(ALLOWED_ROOT_KEYS)}")
            
    # 2. Kiểm tra các trường bắt buộc ở root
    required_root = ["doc_type", "header", "blocks", "sign_block"]
    for req in required_root:
        if req not in data:
            errors.append(f"Thiếu trường bắt buộc ở root: '{req}'")
            
    doc_type = data.get("doc_type")
    if doc_type and doc_type not in VALID_DOC_TYPES:
        errors.append(f"doc_type '{doc_type}' không hợp lệ. Các loại hợp lệ: {', '.join(VALID_DOC_TYPES)}")
        
    # 3. Kiểm tra khối header
    header = data.get("header")
    if header is not None:
        if not isinstance(header, dict):
            errors.append("Trường 'header' phải là một dictionary/object.")
            
    # 4. Kiểm tra khối blocks
    blocks = data.get("blocks")
    if blocks is not None:
        errors.extend(validate_blocks(blocks, "blocks"))
        
    # 5. Kiểm tra post_sign_blocks nếu có
    post_blocks = data.get("post_sign_blocks")
    if post_blocks is not None:
        errors.extend(validate_blocks(post_blocks, "post_sign_blocks"))
        
    # 6. Kiểm tra sign_block
    sign_block = data.get("sign_block")
    if sign_block is not None:
        if not isinstance(sign_block, dict):
            errors.append("Trường 'sign_block' phải là một dictionary/object.")
            
    return errors

def sanitize_trich_yeu(text):
    if not text:
        return ""
    cleaned = text.strip()
    # Loại bỏ tiền tố V/v, V/V, Về việc, v/v nếu người dùng vô tình truyền vào
    cleaned = re.sub(r'^(?:v\/v|về việc|v\/V|V\/v)\s*[:\-–]?\s*', '', cleaned, flags=re.IGNORECASE)
    return cleaned.strip()

def set_cell_margins(cell, top=0, bottom=0, left=0, right=0):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>\n'
        f'  <w:top w:w="{top}" w:type="dxa"/>\n'
        f'  <w:bottom w:w="{bottom}" w:type="dxa"/>\n'
        f'  <w:left w:w="{left}" w:type="dxa"/>\n'
        f'  <w:right w:w="{right}" w:type="dxa"/>\n'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def set_cell_shading(cell, color_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    tcPr.append(shd)

def set_table_no_borders(table):
    tblPr = table._tbl.tblPr
    tblBorders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>\n'
        f'  <w:top w:val="none" w:sz="0" w:space="0" w:color="auto"/>\n'
        f'  <w:left w:val="none" w:sz="0" w:space="0" w:color="auto"/>\n'
        f'  <w:bottom w:val="none" w:sz="0" w:space="0" w:color="auto"/>\n'
        f'  <w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>\n'
        f'  <w:insideH w:val="none" w:sz="0" w:space="0" w:color="auto"/>\n'
        f'  <w:insideV w:val="none" w:sz="0" w:space="0" w:color="auto"/>\n'
        f'</w:tblBorders>'
    )
    tblPr.append(tblBorders)

def set_table_borders(table, color="000000", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    tblBorders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>\n'
        f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'</w:tblBorders>'
    )
    tblPr.append(tblBorders)

def set_row_cant_split(row):
    trPr = row._tr.get_or_add_trPr()
    cantSplit = parse_xml(f'<w:cantSplit {nsdecls("w")}/>')
    trPr.append(cantSplit)

def set_row_repeat_header(row):
    trPr = row._tr.get_or_add_trPr()
    tblHeader = parse_xml(f'<w:tblHeader {nsdecls("w")}/>')
    trPr.append(tblHeader)

def add_page_number_field(run):
    fld1 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="begin"/>')
    instr = parse_xml(f'<w:instrText {nsdecls("w")} xml:space="preserve"> PAGE </w:instrText>')
    fld2 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="separate"/>')
    fld3 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="end"/>')
    run._r.append(fld1)
    run._r.append(instr)
    run._r.append(fld2)
    run._r.append(fld3)

def setup_page_layout(section, is_landscape=False, target_one_page=False, is_first_section=True):
    if is_landscape:
        section.orientation = WD_ORIENTATION.LANDSCAPE
        section.page_width = Mm(297)
        section.page_height = Mm(210)
        section.top_margin = Mm(18 if target_one_page else 20)
        section.bottom_margin = Mm(18 if target_one_page else 20)
        section.left_margin = Mm(25 if target_one_page else 25)
        section.right_margin = Mm(18 if target_one_page else 20)
    else:
        section.orientation = WD_ORIENTATION.PORTRAIT
        section.page_width = Mm(210)
        section.page_height = Mm(297)
        section.top_margin = Mm(20)
        section.bottom_margin = Mm(20)
        section.left_margin = Mm(25)
        section.right_margin = Mm(20)

    if is_first_section:
        # Đánh số trang tự động từ trang 2 ở chính giữa lề trên (Header)
        section.different_first_page_header_footer = True
        header = section.header
        p_head = header.paragraphs[0]
        p_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_head.paragraph_format.space_before = Pt(0)
        p_head.paragraph_format.space_after = Pt(0)
        p_head.text = ""
        r_head = p_head.add_run()
        r_head.font.name = "Times New Roman"
        r_head.font.size = Pt(13)
        add_page_number_field(r_head)
    else:
        # Các section tiếp theo không ẩn trang đầu của section và kế thừa header số trang
        section.different_first_page_header_footer = False
        section.header.is_linked_to_previous = True

def add_header_table(doc, data, target_one_page=False):
    doc_type = data.get("doc_type", "cong_van").lower()
    header_data = data.get("header", {})
    header_level = header_data.get("header_level", "ump" if doc_type == "giay_gioi_thieu" else "ytcc")
    
    # Kích thước 2 cột: 70mm bên trái, 95mm bên phải (Tổng 165mm khớp lề 25/20mm)
    # Dùng bảng 2 dòng (2 rows x 2 cols):
    # Dòng 0: Cơ quan ban hành (trái) và Quốc hiệu, Tiêu ngữ + Vạch kẻ (phải)
    # Dòng 1: Số hiệu + Trích yếu (trái) và Địa danh ngày tháng (phải)
    # -> Đảm bảo "Số: ..." và "Thành phố Hồ Chí Minh, ngày ..." THẲNG HÀNG THỊ GIÁC TUYỆT ĐỐI!
    table = doc.add_table(rows=2, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_no_borders(table)
    
    for r in table.rows:
        set_row_cant_split(r)
        r.cells[0].width = Mm(70)
        r.cells[1].width = Mm(95)
        set_cell_margins(r.cells[0], top=0, bottom=0, left=0, right=36)
        set_cell_margins(r.cells[1], top=0, bottom=0, left=36, right=0)
        
    c00 = table.cell(0, 0)
    c01 = table.cell(0, 1)
    c10 = table.cell(1, 0)
    c11 = table.cell(1, 1)
    
    # 1. DÒNG 0 - CỘT TRÁI: ĐƠN VỊ BAN HÀNH
    p_org = c00.paragraphs[0]
    p_org.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_org.paragraph_format.space_before = Pt(0)
    p_org.paragraph_format.space_after = Pt(0)
    p_org.paragraph_format.line_spacing = 1.05
    
    if header_level == "ump":
        r1 = p_org.add_run("BỘ Y TẾ\n")
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(10.5)
        
        r2 = p_org.add_run("ĐẠI HỌC Y DƯỢC\n")
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(10.5)
        r2.font.bold = True
        
        r3 = p_org.add_run("THÀNH PHỐ HỒ CHÍ MINH")
        r3.font.name = "Times New Roman"
        r3.font.size = Pt(10.5)
        r3.font.bold = True
        
        p_line = c00.add_paragraph()
        p_line.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_line.paragraph_format.space_before = Pt(1)
        p_line.paragraph_format.space_after = Pt(2)
        p_line.paragraph_format.line_spacing = Pt(5)
        r_line = p_line.add_run("─" * 14)
        r_line.font.name = "Times New Roman"
        r_line.font.size = Pt(8)
    else:
        org1 = header_data.get("organ_line1", "ĐẠI HỌC Y DƯỢC")
        org2 = header_data.get("organ_line2", "THÀNH PHỐ HỒ CHÍ MINH")
        org3 = header_data.get("organ_line3", "KHOA Y TẾ CÔNG CỘNG")
        
        r1 = p_org.add_run(f"{org1}\n{org2}\n")
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(10)
        
        r3 = p_org.add_run(org3)
        r3.font.name = "Times New Roman"
        r3.font.size = Pt(11)
        r3.font.bold = True
        
        p_line = c00.add_paragraph()
        p_line.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_line.paragraph_format.space_before = Pt(1)
        p_line.paragraph_format.space_after = Pt(2)
        p_line.paragraph_format.line_spacing = Pt(5)
        r_line = p_line.add_run("─" * 13)
        r_line.font.name = "Times New Roman"
        r_line.font.size = Pt(8)
        
    # 2. DÒNG 0 - CỘT PHẢI: QUỐC HIỆU, TIÊU NGỮ & VẠCH KẺ
    p_qh = c01.paragraphs[0]
    p_qh.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_qh.paragraph_format.space_before = Pt(0)
    p_qh.paragraph_format.space_after = Pt(0)
    p_qh.paragraph_format.line_spacing = 1.05
    
    r_qh = p_qh.add_run("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\n")
    r_qh.font.name = "Times New Roman"
    r_qh.font.size = Pt(10.5)
    r_qh.font.bold = True
    
    r_tn = p_qh.add_run("Độc lập – Tự do – Hạnh phúc")
    r_tn.font.name = "Times New Roman"
    r_tn.font.size = Pt(11)
    r_tn.font.bold = True
    
    p_line2 = c01.add_paragraph()
    p_line2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_line2.paragraph_format.space_before = Pt(1)
    p_line2.paragraph_format.space_after = Pt(2)
    p_line2.paragraph_format.line_spacing = Pt(5)
    r_line2 = p_line2.add_run("─" * 24)
    r_line2.font.name = "Times New Roman"
    r_line2.font.size = Pt(8)
    
    # 3. DÒNG 1 - CỘT TRÁI: SỐ HIỆU & TRÍCH YẾU
    so_raw = str(header_data.get("so_hieu", "....")).strip()
    ma_loai = header_data.get("ma_loai", "")
    if "/" in so_raw:
        full_so = so_raw
    else:
        if not ma_loai:
            if doc_type == "cong_van": ma_loai = "YTCC-VP"
            elif doc_type == "to_trinh": ma_loai = "TTr-YTCC"
            elif doc_type == "giay_gioi_thieu": ma_loai = "GGT-YTCC"
            elif doc_type == "ke_hoach": ma_loai = "KH-YTCC"
            elif doc_type == "bao_cao": ma_loai = "BC-YTCC"
            else: ma_loai = "YTCC"
        full_so = f"{so_raw}/{ma_loai}"
        
    p_so = c10.paragraphs[0]
    p_so.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_so.paragraph_format.space_before = Pt(2)
    p_so.paragraph_format.space_after = Pt(0)
    p_so.paragraph_format.line_spacing = 1.05
    r_so = p_so.add_run(f"Số: {full_so}")
    r_so.font.name = "Times New Roman"
    r_so.font.size = Pt(11)
    
    # Riêng Công văn: Trích yếu đặt ngay dưới Số hiệu ở cột trái
    if doc_type == "cong_van":
        raw_trich_yeu = header_data.get("trich_yeu", "")
        clean_trich_yeu = sanitize_trich_yeu(raw_trich_yeu)
        p_ty = c10.add_paragraph()
        p_ty.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_ty.paragraph_format.space_before = Pt(2)
        p_ty.paragraph_format.space_after = Pt(0)
        p_ty.paragraph_format.line_spacing = 1.05
        r_ty = p_ty.add_run(f"V/v {clean_trich_yeu}")
        r_ty.font.name = "Times New Roman"
        r_ty.font.size = Pt(11)
        r_ty.font.italic = False # CHUẨN MỚI: Text trích yếu KHÔNG NGHIÊNG theo phản hồi người dùng!
        
    # 4. DÒNG 1 - CỘT PHẢI: ĐỊA DANH NGÀY THÁNG (CÙNG DÒNG VỚI SỐ HIỆU)
    dia_danh = header_data.get("dia_danh", "Thành phố Hồ Chí Minh")
    ngay = str(header_data.get("ngay", "....")).strip()
    thang = str(header_data.get("thang", "....")).strip()
    nam = str(header_data.get("nam", "2026")).strip()
    
    # Định dạng chèn số 0 cho ngày tháng 1 chữ số
    if ngay.isdigit() and len(ngay) == 1: ngay = f"0{ngay}"
    if thang.isdigit() and len(thang) == 1: thang = f"0{thang}"
    
    p_date = c11.paragraphs[0]
    p_date.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_date.paragraph_format.space_before = Pt(2)
    p_date.paragraph_format.space_after = Pt(0)
    p_date.paragraph_format.line_spacing = 1.05
    r_date = p_date.add_run(f"{dia_danh}, ngày {ngay} tháng {thang} năm {nam}")
    r_date.font.name = "Times New Roman"
    r_date.font.size = Pt(11)
    r_date.font.italic = True
    
    # Khoảng cách sau Header
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

def add_document_title(doc, data, target_one_page=False):
    doc_type = data.get("doc_type", "cong_van").lower()
    if doc_type == "cong_van":
        # Công văn không có tiêu đề lớn ở giữa
        return
        
    title_override = data.get("title", "")
    header_data = data.get("header", {})
    trich_yeu = sanitize_trich_yeu(header_data.get("trich_yeu", data.get("trich_yeu", "")))
    
    if not title_override:
        if doc_type == "to_trinh": title_str = "TỜ TRÌNH"
        elif doc_type == "giay_gioi_thieu": title_str = "GIẤY GIỚI THIỆU"
        elif doc_type == "ke_hoach": title_str = "KẾ HOẠCH"
        elif doc_type == "bao_cao": title_str = "BÁO CÁO"
        else: title_str = "VĂN BẢN"
    else:
        title_str = title_override.upper()
        
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(4 if target_one_page else 8)
    p_title.paragraph_format.space_after = Pt(2 if target_one_page else 4)
    p_title.paragraph_format.keep_with_next = True
    
    r_title = p_title.add_run(title_str)
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(14)
    r_title.font.bold = True
    
    # Dòng trích yếu dưới tiêu đề
    if trich_yeu and doc_type != "giay_gioi_thieu":
        p_sub = doc.add_paragraph()
        p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_sub.paragraph_format.space_before = Pt(0)
        p_sub.paragraph_format.space_after = Pt(6 if target_one_page else 10)
        p_sub.paragraph_format.keep_with_next = True
        
        prefix = "Về việc " if doc_type == "to_trinh" and not trich_yeu.lower().startswith("về việc") else ""
        r_sub = p_sub.add_run(f"{prefix}{trich_yeu}")
        r_sub.font.name = "Times New Roman"
        r_sub.font.size = Pt(12.5 if target_one_page else 13)
        r_sub.font.bold = True
        
        # Đường kẻ ngang dưới trích yếu của Tờ trình (chuẩn NĐ 30 & S0 To_trinh_SoDi_927)
        if doc_type == "to_trinh":
            p_sub.paragraph_format.space_after = Pt(2)
            p_tline = doc.add_paragraph()
            p_tline.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_tline.paragraph_format.space_before = Pt(0)
            p_tline.paragraph_format.space_after = Pt(6 if target_one_page else 10)
            p_tline.paragraph_format.line_spacing = Pt(5)
            p_tline.paragraph_format.keep_with_next = True
            r_tl = p_tline.add_run("─" * 18)
            r_tl.font.name = "Times New Roman"
            r_tl.font.size = Pt(8)

def render_blocks(doc, blocks, target_one_page=False):
    for idx, b in enumerate(blocks):
        btype = b.get("type", "paragraph")
        is_last = (idx == len(blocks) - 1)
        
        if btype == "kinh_gui":
            items = b.get("items", [])
            text = b.get("text", "")
            if text and not items:
                items = [text]
                
            p_kg = doc.add_paragraph()
            p_kg.paragraph_format.space_before = Pt(6)
            p_kg.paragraph_format.space_after = Pt(2)
            p_kg.paragraph_format.keep_with_next = True
            
            p_kg.paragraph_format.left_indent = Mm(15)
            r_tag = p_kg.add_run("Kính gửi:")
            r_tag.font.name = "Times New Roman"
            r_tag.font.size = Pt(13)
            r_tag.font.bold = False # CHUẨN MỚI: Kính gửi không in đậm theo phản hồi người dùng
            r_tag.font.underline = False # Kính gửi không gạch chân
            
            for item in items:
                p_item = doc.add_paragraph()
                p_item.paragraph_format.left_indent = Mm(25)
                p_item.paragraph_format.space_before = Pt(0)
                p_item.paragraph_format.space_after = Pt(2)
                p_item.paragraph_format.line_spacing = 1.3
                p_item.paragraph_format.keep_with_next = True
                clean_item = item.strip()
                if not clean_item.startswith("-"):
                    clean_item = f"- {clean_item}"
                r_it = p_item.add_run(clean_item)
                r_it.font.name = "Times New Roman"
                r_it.font.size = Pt(13)
                r_it.font.bold = False
                    
        elif btype in ("heading", "h1", "h2", "h3"):
            if btype == "h1":
                level = 1
            elif btype == "h2":
                level = 2
            elif btype == "h3":
                level = 3
            else:
                level = b.get("level", 1)
                
            text = b.get("text", "")
            p_h = doc.add_paragraph()
            p_h.paragraph_format.keep_with_next = True
            
            if level == 1:
                p_h.paragraph_format.space_before = Pt(4 if target_one_page else 8)
                p_h.paragraph_format.space_after = Pt(2 if target_one_page else 3)
                p_h.paragraph_format.left_indent = Mm(0)
                add_markdown_runs(p_h, text, font_size=Pt(13 if not target_one_page else 12.5), base_bold=True)
            elif level == 2:
                p_h.paragraph_format.space_before = Pt(3 if target_one_page else 5)
                p_h.paragraph_format.space_after = Pt(1 if target_one_page else 2)
                p_h.paragraph_format.left_indent = Mm(5)
                add_markdown_runs(p_h, text, font_size=Pt(13 if not target_one_page else 12.5), base_bold=True)
            else:
                p_h.paragraph_format.space_before = Pt(2)
                p_h.paragraph_format.space_after = Pt(1)
                p_h.paragraph_format.left_indent = Mm(10)
                add_markdown_runs(p_h, text, font_size=Pt(13 if not target_one_page else 12.5), base_bold=True, base_italic=True)
                
        elif btype in ("paragraph", "p"):
            text = b.get("text", "")
            prefix_bold = b.get("prefix_bold", "")
            align_str = b.get("align", "justify").lower()
            indent = b.get("indent", True)
            
            p = doc.add_paragraph()
            if align_str == "center":
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            elif align_str == "right":
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            elif align_str == "left":
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                
            if indent and align_str not in ("center", "right"):
                p.paragraph_format.first_line_indent = Mm(12.7) # 1.27 cm chuẩn
                
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.5 # CHUẨN MỚI: Dãn dòng 1.5 lines theo yêu cầu người dùng
            
            # Gắn keep_with_next nếu là đoạn cuối cùng trước khối chữ ký
            if is_last:
                p.paragraph_format.keep_with_next = True
                
            if prefix_bold:
                r_pfx = p.add_run(f"{prefix_bold} ")
                r_pfx.font.name = "Times New Roman"
                r_pfx.font.size = Pt(13)
                r_pfx.font.bold = True
                
            add_markdown_runs(
                p,
                text,
                font_size=Pt(13),
                base_bold=b.get("bold", False),
                base_italic=b.get("italic", False)
            )
            
        elif btype == "bullet":
            text = b.get("text", "")
            bullet_char = b.get("bullet_char", "- ")
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.left_indent = Mm(15)
            p.paragraph_format.first_line_indent = Mm(-5)
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(1 if target_one_page else 2)
            p.paragraph_format.line_spacing = 1.05 if target_one_page else 1.15
            
            if is_last:
                p.paragraph_format.keep_with_next = True
                
            r_b = p.add_run(bullet_char)
            r_b.font.name = "Times New Roman"
            r_b.font.size = Pt(13 if not target_one_page else 12)
            
            add_markdown_runs(
                p,
                text,
                font_size=Pt(13 if not target_one_page else 12),
                base_bold=b.get("bold", False),
                base_italic=b.get("italic", False)
            )
            
        elif btype in ("quote", "trich_dan"):
            text = b.get("text", "")
            align_str = b.get("align", "justify").lower()
            p = doc.add_paragraph()
            if align_str == "center":
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            elif align_str == "right":
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            elif align_str == "left":
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                
            p.paragraph_format.left_indent = Mm(15)
            p.paragraph_format.right_indent = Mm(10)
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2 if target_one_page else 4)
            p.paragraph_format.line_spacing = 1.05 if target_one_page else 1.15
            
            if is_last:
                p.paragraph_format.keep_with_next = True
                
            add_markdown_runs(
                p,
                text,
                font_size=Pt(12 if target_one_page else 12.5),
                base_bold=b.get("bold", False),
                base_italic=True
            )
            
        elif btype == "key_value":
            # Dành cho Giấy giới thiệu hoặc biểu mẫu thông tin
            items = b.get("items", [])
            for it in items:
                p = doc.add_paragraph()
                p.paragraph_format.left_indent = Mm(10)
                p.paragraph_format.space_before = Pt(1)
                p.paragraph_format.space_after = Pt(2 if target_one_page else 3)
                p.paragraph_format.line_spacing = 1.05 if target_one_page else 1.15
                
                k_run = p.add_run(f"{it.get('key', '')}: ")
                k_run.font.name = "Times New Roman"
                k_run.font.size = Pt(13 if not target_one_page else 12)
                k_run.font.bold = it.get("key_bold", False)
                
                v_run = p.add_run(str(it.get("value", "")))
                v_run.font.name = "Times New Roman"
                v_run.font.size = Pt(13 if not target_one_page else 12)
                v_run.font.bold = it.get("value_bold", False)
                v_run.font.italic = it.get("value_italic", False)
                
        elif btype == "table":
            headers = b.get("headers", [])
            rows_data = b.get("rows", [])
            col_widths = b.get("col_widths", []) # Danh sách % hoặc mm
            header_shading = b.get("header_shading")
            
            num_cols = len(headers) if headers else (len(rows_data[0]) if rows_data else 1)
            num_rows = len(rows_data) + (1 if headers else 0)
            
            tbl = doc.add_table(rows=num_rows, cols=num_cols)
            tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
            set_table_borders(tbl, color="000000", sz="4", val="single")
            
            curr_row = 0
            if headers:
                h_row = tbl.rows[0]
                set_row_cant_split(h_row)
                set_row_repeat_header(h_row)
                for ci, htext in enumerate(headers):
                    cell = h_row.cells[ci]
                    set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
                    if header_shading:
                        set_cell_shading(cell, header_shading.lstrip("#"))
                    p = cell.paragraphs[0]
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    p.paragraph_format.space_before = Pt(1)
                    p.paragraph_format.space_after = Pt(1)
                    add_markdown_runs(p, str(htext), font_size=Pt(11.5 if not target_one_page else 10.5), base_bold=True)
                curr_row = 1
                
            for rdata in rows_data:
                row = tbl.rows[curr_row]
                set_row_cant_split(row)
                for ci, val in enumerate(rdata):
                    if ci >= num_cols: break
                    cell = row.cells[ci]
                    set_cell_margins(cell, top=40, bottom=40, left=80, right=80)
                    p = cell.paragraphs[0]
                    p.paragraph_format.space_before = Pt(1)
                    p.paragraph_format.space_after = Pt(1)
                    p.paragraph_format.line_spacing = 1.05
                    
                    # Tự căn giữa nếu là STT hoặc mã số ngắn và không chứa markdown
                    val_str = str(val)
                    if (len(val_str) <= 4 or val_str.isdigit()) and not ('*' in val_str):
                        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    else:
                        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                        
                    add_markdown_runs(p, val_str, font_size=Pt(11 if not target_one_page else 10), base_bold=False, base_italic=False)
                curr_row += 1
                
            # Đặt độ rộng cột nếu có chỉ định (tính theo mm)
            if col_widths and len(col_widths) == num_cols:
                for row in tbl.rows:
                    for ci, w_val in enumerate(col_widths):
                        row.cells[ci].width = Mm(w_val)
                        
            p_space = doc.add_paragraph()
            p_space.paragraph_format.space_after = Pt(4)
            if is_last:
                p_space.paragraph_format.keep_with_next = True
                
        elif btype == "landscape_section":
            # Chuyển sang Section khổ ngang A4
            sec = doc.add_section(WD_SECTION.NEW_PAGE)
            setup_page_layout(sec, is_landscape=True, target_one_page=target_one_page, is_first_section=False)
            
            inner_blocks = b.get("blocks", [])
            render_blocks(doc, inner_blocks, target_one_page=target_one_page)
            
            # Nếu còn block sau đó, tự động chuyển lại khổ đứng Portrait
            if idx < len(blocks) - 1:
                sec_back = doc.add_section(WD_SECTION.NEW_PAGE)
                setup_page_layout(sec_back, is_landscape=False, target_one_page=target_one_page, is_first_section=False)

def add_signature_block(doc, data, target_one_page=False):
    doc_type = data.get("doc_type", "cong_van").lower()
    sign_data = data.get("sign_block", {})
    
    # 1. Bảng chữ ký chính (2 cột)
    table = doc.add_table(rows=1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_no_borders(table)
    
    row = table.rows[0]
    set_row_cant_split(row)
    
    c1 = row.cells[0]
    c2 = row.cells[1]
    c1.width = Mm(70)
    c2.width = Mm(95)
    set_cell_margins(c1, top=0, bottom=0, left=0, right=36)
    set_cell_margins(c2, top=0, bottom=0, left=36, right=0)
    
    # CỘT TRÁI: NƠI NHẬN
    p1 = c1.paragraphs[0]
    p1.paragraph_format.space_before = Pt(0)
    p1.paragraph_format.space_after = Pt(2)
    p1.paragraph_format.line_spacing = 1.05
    p1.paragraph_format.keep_with_next = True
    
    r_nn = p1.add_run("Nơi nhận:")
    r_nn.font.name = "Times New Roman"
    r_nn.font.size = Pt(12) # CHUẨN MỚI: Nơi nhận: cỡ chữ 12 theo yêu cầu người dùng
    r_nn.font.bold = True
    r_nn.font.italic = True
    
    recipients = sign_data.get("recipients", ["- Như trên;"])
    for rec in recipients:
        p_rec = c1.add_paragraph()
        p_rec.paragraph_format.space_before = Pt(0)
        p_rec.paragraph_format.space_after = Pt(1)
        p_rec.paragraph_format.line_spacing = 1.05
        p_rec.paragraph_format.keep_with_next = True
        
        clean_rec = rec.strip()
        if not clean_rec.startswith("-"):
            clean_rec = f"- {clean_rec}"
        r = p_rec.add_run(clean_rec)
        r.font.name = "Times New Roman"
        r.font.size = Pt(11) # CHUẨN MỚI: Các mục nơi nhận cỡ chữ 11 theo yêu cầu người dùng
        
    # Dòng lưu đặc thù Khoa YTCC (chỉ thêm nếu recipients chưa có dòng Lưu:)
    has_luu_in_recipients = any("lưu:" in rec.lower() for rec in recipients)
    if not has_luu_in_recipients:
        custom_luu = sign_data.get("custom_luu", "")
        if custom_luu:
            luu_text = custom_luu
        else:
            dept = sign_data.get("dept_code", "VP")
            initials = sign_data.get("creator_initials", "YTCC")
            luu_text = f"- Lưu: VT, {dept}_{initials}."
            
        p_luu = c1.add_paragraph()
        p_luu.paragraph_format.space_before = Pt(0)
        p_luu.paragraph_format.space_after = Pt(0)
        p_luu.paragraph_format.line_spacing = 1.05
        p_luu.paragraph_format.keep_with_next = True
        r_l = p_luu.add_run(luu_text)
        r_l.font.name = "Times New Roman"
        r_l.font.size = Pt(11) # CHUẨN MỚI: Dòng lưu cỡ chữ 11 theo yêu cầu người dùng
    
    # CỘT PHẢI: QUYỀN HẠN, CHỨC VỤ VÀ HỌ TÊN NGƯỜI KÝ
    p2 = c2.paragraphs[0]
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p2.paragraph_format.space_before = Pt(0)
    p2.paragraph_format.space_after = Pt(0)
    p2.paragraph_format.line_spacing = 1.05
    p2.paragraph_format.keep_with_next = True
    
    default_role = "TL. HIỆU TRƯỞNG\nTRƯỞNG KHOA" if doc_type == "giay_gioi_thieu" else "TRƯỞNG KHOA"
    signer_role = sign_data.get("signer_role", default_role)
    
    # Có thể có nhiều dòng chức vụ (ví dụ TL. HIỆU TRƯỞNG / TRƯỞNG KHOA)
    role_lines = signer_role.split("\n")
    for r_idx, rline in enumerate(role_lines):
        r_r = p2.add_run(rline.strip() + ("\n" if r_idx < len(role_lines) - 1 else ""))
        r_r.font.name = "Times New Roman"
        r_r.font.size = Pt(12.5 if not target_one_page else 12)
        r_r.font.bold = True
        
    # Chừa khoảng trống chữ ký và con dấu (45-60pt để đủ không gian chèn chữ ký số / dấu điện tử theo NĐ 30)
    custom_gap = sign_data.get("sign_gap_pt")
    if custom_gap is not None:
        sign_gap = docx.shared.Pt(float(custom_gap))
    else:
        sign_gap = docx.shared.Pt(48 if target_one_page else 55)
    p_gap = c2.add_paragraph()
    p_gap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_gap.paragraph_format.space_before = sign_gap
    p_gap.paragraph_format.space_after = Pt(0)
    p_gap.paragraph_format.line_spacing = Pt(1)
    p_gap.paragraph_format.keep_with_next = True
    
    # Họ tên người ký
    signer_name = sign_data.get("signer_name", "[HỌ TÊN NGƯỜI KÝ]").strip()
    p_name = c2.add_paragraph()
    p_name.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_name.paragraph_format.space_before = Pt(0)
    p_name.paragraph_format.space_after = Pt(0)
    p_name.paragraph_format.keep_with_next = True
    
    r_n = p_name.add_run(signer_name)
    r_n.font.name = "Times New Roman"
    r_n.font.size = Pt(12.5 if not target_one_page else 12)
    r_n.font.bold = True
    
    # 2. KHỐI PHÊ DUYỆT BAN GIÁM HIỆU (TÙY CHỌN CHO TỜ TRÌNH)
    has_bgh = data.get("has_bgh_approval", False)
    if has_bgh:
        bgh_title = data.get("bgh_approver_title", "DUYỆT BAN GIÁM HIỆU")
        bgh_name = data.get("bgh_approver_name", "").strip()
        
        # BGH phê duyệt đặt ở chính giữa toàn trang phía dưới khối chữ ký & nơi nhận (chuẩn S0 To_trinh_SoDi_927)
        p_bgh = doc.add_paragraph()
        p_bgh.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_bgh.paragraph_format.space_before = Pt(8 if target_one_page else 14)
        p_bgh.paragraph_format.space_after = Pt(0)
        p_bgh.paragraph_format.keep_with_next = True
        
        rb = p_bgh.add_run(bgh_title.upper())
        rb.font.name = "Times New Roman"
        rb.font.size = Pt(12.5 if not target_one_page else 12)
        rb.font.bold = True
        
        # Khoảng trống ký tên BGH (chừa diện tích chèn chữ ký số / con dấu BGH)
        custom_bgh_gap = data.get("bgh_sign_gap_pt")
        if custom_bgh_gap is not None:
            bgh_gap = Pt(float(custom_bgh_gap))
        else:
            bgh_gap = Pt(45 if target_one_page else 55)
            
        p_bgap = doc.add_paragraph()
        p_bgap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_bgap.paragraph_format.space_before = bgh_gap
        p_bgap.paragraph_format.space_after = Pt(0)
        p_bgap.paragraph_format.line_spacing = Pt(1)
        p_bgap.paragraph_format.keep_with_next = True
        
        if bgh_name:
            p_bname = doc.add_paragraph()
            p_bname.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_bname.paragraph_format.space_before = Pt(0)
            p_bname.paragraph_format.space_after = Pt(0)
            p_bname.paragraph_format.keep_with_next = True
            
            rb_n = p_bname.add_run(bgh_name)
            rb_n.font.name = "Times New Roman"
            rb_n.font.size = Pt(12.5 if not target_one_page else 12)
            rb_n.font.bold = True

def build_document(json_path, output_docx_path):
    with open(json_path, "r", encoding="utf-8-sig") as f:
        data = json.load(f)
        
    errors = validate_schema(data)
    if errors:
        err_msg = "Lỗi xác thực cấu trúc JSON (Schema Validation Errors):\n" + "\n".join(f"  - {e}" for e in errors)
        raise ValueError(err_msg)
        
    doc = Document()
    target_one_page = data.get("target_one_page", False)
    
    # Thiết lập Section đầu tiên
    first_sec = doc.sections[0]
    setup_page_layout(first_sec, is_landscape=False, target_one_page=target_one_page)
    
    # 1. Header 2 cột
    add_header_table(doc, data, target_one_page=target_one_page)
    
    # 2. Tiêu đề tài liệu
    add_document_title(doc, data, target_one_page=target_one_page)
    
    # 3. Thân văn bản (Blocks)
    blocks = data.get("blocks", [])
    render_blocks(doc, blocks, target_one_page=target_one_page)
    
    # 4. Khối chữ ký & Nơi nhận
    add_signature_block(doc, data, target_one_page=target_one_page)
    
    # 5. Các khối phụ lục sau chữ ký (nếu có)
    post_blocks = data.get("post_sign_blocks", [])
    if post_blocks:
        render_blocks(doc, post_blocks, target_one_page=target_one_page)
    
    # Lưu file DOCX
    out_dir = os.path.dirname(os.path.abspath(output_docx_path))
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)
    doc.save(output_docx_path)
    print(f"Đã tạo DOCX thành công: {output_docx_path}")

def export_to_pdf(docx_path, pdf_path=None):
    if not pdf_path:
        pdf_path = os.path.splitext(docx_path)[0] + ".pdf"
        
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ps1_path = os.path.join(script_dir, "export_pdf.ps1")
    
    cmd = [
        "powershell.exe",
        "-ExecutionPolicy", "Bypass",
        "-File", ps1_path,
        "-InputDocx", os.path.abspath(docx_path),
        "-OutputPdf", os.path.abspath(pdf_path)
    ]
    
    print(f"Đang xuất PDF qua Word COM: {pdf_path}...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Lỗi xuất PDF: {res.stderr}")
        raise RuntimeError(f"Word COM export failed: {res.stderr}")
    else:
        print(f"Xuất PDF thành công: {pdf_path}")
    return pdf_path

def main():
    parser = argparse.ArgumentParser(description="YTCC JSON-to-DOCX & PDF Engine")
    parser.add_argument("--input", required=True, help="Đường dẫn file JSON mô tả văn bản")
    parser.add_argument("--output", help="Đường dẫn file .docx đầu ra")
    parser.add_argument("--pdf", action="store_true", help="Tự động gọi Word COM xuất PDF")
    parser.add_argument("--pdf-out", help="Đường dẫn file .pdf đầu ra tùy chọn")
    parser.add_argument("--validate-only", action="store_true", help="Chỉ kiểm tra cấu trúc schema, không xuất file")
    
    args = parser.parse_args()
    
    if args.validate_only:
        with open(args.input, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
        errors = validate_schema(data)
        if errors:
            print("Lỗi cấu trúc schema:")
            for e in errors:
                print(f"  - {e}")
            sys.exit(1)
        else:
            print(f"Schema hợp lệ: {args.input}")
            sys.exit(0)
            
    if not args.output:
        parser.error("Cần truyền --output khi không dùng --validate-only")
        
    build_document(args.input, args.output)
    
    if args.pdf:
        export_to_pdf(args.output, args.pdf_out)

if __name__ == "__main__":
    main()
