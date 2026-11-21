"""Render selected local evidence pages and measure PDF text without OCR."""
import json
import shutil
import subprocess
import sys
from pathlib import Path
from pypdf import PdfReader
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "audit/artifacts/P0"
RENDER = OUT / "source_render"
RENDER.mkdir(exist_ok=True)
sys.stdout.reconfigure(encoding="utf-8")
selected = {
    "Cong_van_SoDi_925.pdf": [1],
    "To_trinh_SoDi_890.pdf": [1],
    "To_trinh_SoDi_922.pdf": [1, 2, 4],
    "Giay_gioi_thieu_SoDi_932.pdf": [1],
    "Giay_gioi_thieu_SoDi_902.pdf": [1, 2, 8],
    "Ke_hoach_SoDi_754.pdf": [1, 2, 5],
    "Bao_cao_SoDi_859.pdf": [1, 2, 13],
    "Quyet_dinh_SoDi_721.pdf": [1, 2],
    "CVDi_2026_SoDi_140_GGT_ SV YHDP xin thông tin làm KLTN.pdf": [1, 5],
    "CVDi_2026_SoDi_785_Tờ trình Về việc đăng ký tổ chức Workshop chương  trình lãnh.pdf": [1, 67],
}
results = []
poppler = shutil.which("pdftoppm")
for case, (name, pages) in enumerate(selected.items(), 1):
    p = ROOT / "knowledge_base/sample_pdfs" / name
    r = PdfReader(p)
    chars = [len((page.extract_text() or "").strip()) for page in r.pages]
    entry = {"case": f"S{case:02}", "path": p.relative_to(ROOT).as_posix(),
             "total_pages": len(r.pages), "text_chars_by_page": chars,
             "rendered_pages": pages, "page_boxes_pt": [
                 [round(float(page.mediabox.width), 2), round(float(page.mediabox.height), 2)] for page in r.pages]}
    for page in pages:
        prefix = RENDER / f"S{case:02}_p{page:02}"
        subprocess.run([poppler, "-f", str(page), "-l", str(page), "-scale-to", "1400",
                        "-png", "-singlefile", str(p), str(prefix)], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    results.append(entry)
    print(entry["case"], name, len(r.pages), "pages; text chars", sum(chars), flush=True)

font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 21)
for i in range(0, len(results), 2):
    sheets = []
    for e in results[i:i+2]:
        page = e["rendered_pages"][0]
        im = Image.open(RENDER / f"{e['case']}_p{page:02}.png").convert("RGB")
        im.thumbnail((950, 1344))
        canvas = Image.new("RGB", (970, 1410), "white")
        canvas.paste(im, ((970-im.width)//2, 55))
        ImageDraw.Draw(canvas).text((15, 10), f"{e['case']} | p{page} / {e['total_pages']}", fill="black", font=font)
        sheets.append(canvas)
    sheet = Image.new("RGB", (970*len(sheets), 1410), "#dddddd")
    for j, canvas in enumerate(sheets):
        sheet.paste(canvas, (j*970, 0))
    sheet.save(RENDER / f"contact_{i//2+1:02}.png")

templates = []
for p in sorted((OUT / "template_render").glob("*.pdf")):
    r = PdfReader(p)
    entry = {"path": p.relative_to(ROOT).as_posix(), "pages": len(r.pages),
             "page_boxes_pt": [[float(page.mediabox.width), float(page.mediabox.height)] for page in r.pages],
             "placeholders_in_pdf": sorted(set(__import__("re").findall(r"\{\{[^{}]+\}\}", "\n".join(page.extract_text() or "" for page in r.pages))))}
    templates.append(entry)
    subprocess.run([poppler, "-f", "1", "-l", "1", "-scale-to", "1400", "-png",
                    "-singlefile", str(p), str(p.with_suffix(""))], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
(OUT / "sample_inspection.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
(OUT / "template_pdf_inspection.json").write_text(json.dumps(templates, ensure_ascii=False, indent=2), encoding="utf-8")
