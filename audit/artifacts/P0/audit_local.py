"""P0 read-only inspection. Writes only audit outputs; never connects to QL/DB."""
from pathlib import Path
import collections
import csv
import hashlib
import json
import logging
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "audit/artifacts/P0"
LEGACY = Path("D:/Hương/QUANLYVANBAN")
WORKBOOK = Path("D:/TH/CÔNG VĂN ĐẾN, ĐI 2023, 2024.xlsx")
logging.getLogger("pypdf").setLevel(logging.ERROR)
sys.stdout.reconfigure(encoding="utf-8")


def rel(p):
    return p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT) else str(p)


def digest(p):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def save(name, data):
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def source_files():
    files = [ROOT / n for n in ("AGENTS.md", "PLAN.md", "GEMINI.md", "README.md", "HANDOFF.md")]
    for name in ("knowledge_base/sample_pdfs", "knowledge_base/metadata_index",
                 "knowledge_base/templates", "tools", ".agents"):
        files.extend(p for p in (ROOT / name).rglob("*") if p.is_file())
    files.extend(p for p in LEGACY.rglob("*") if p.is_file())
    if WORKBOOK.exists():
        files.append(WORKBOOK)
    return sorted(set(files), key=str)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    files = source_files()
    hashes = {rel(p): {"sha256": digest(p), "bytes": p.stat().st_size} for p in files}
    baseline = OUT / "source_hashes_before.json"
    if not baseline.exists():
        save(baseline.name, hashes)
    save("source_hashes_current.json", hashes)
    print("Hashed source files:", len(files), flush=True)

    meta = ROOT / "knowledge_base/metadata_index"
    records = {}
    quality = {}
    for scope in ("di", "den"):
        data = json.loads((meta / f"cv_{scope}_history.json").read_text(encoding="utf-8-sig"))
        records[scope] = data
        cols = sorted(set().union(*(r.keys() for r in data)))
        keycols = ("nam", "so_di") if scope == "di" else ("nam", "so_kihieu", "ngay_vanban", "tac_gia")
        groups = collections.defaultdict(list)
        for i, row in enumerate(data, 1):
            groups[tuple(str(row.get(c, "")) for c in keycols)].append(i)
        quality[scope] = {
            "count": len(data), "columns": cols, "candidate_key_columns": keycols,
            "years": dict(collections.Counter(str(r.get("nam", "")) for r in data)),
            "blank_fields": {c: sum(not str(r.get(c, "")).strip() for r in data) for c in cols},
            "hash_display_fields": {c: sum(bool(re.fullmatch(r"#+", str(r.get(c, "")))) for r in data) for c in cols},
            "duplicate_key_groups": [{"key": list(k), "rows_1based": v} for k, v in groups.items() if len(v) > 1],
            "exact_duplicate_excess": len(data) - len({json.dumps(r, sort_keys=True, ensure_ascii=False) for r in data}),
        }
    save("metadata_quality.json", quality)

    from pypdf import PdfReader
    pdfs = sorted((ROOT / "knowledge_base/sample_pdfs").glob("*.pdf"))
    bykey = collections.defaultdict(list)
    bynum = collections.defaultdict(list)
    for i, row in enumerate(records["di"], 1):
        bykey[(str(row["nam"]), str(row["so_di"]))].append(i)
        bynum[str(row["so_di"])].append(i)

    def inspect_pdf(p):
        item = {"path": rel(p), **hashes[rel(p)], "pages": None, "parse_status": "ok"}
        m = re.match(r"CVDi_(\d{4})_SoDi_(\d+)_(.*)\.pdf$", p.name)
        old = re.match(r"(.+)_SoDi_(\d+)\.pdf$", p.name)
        if m:
            item.update(name_year=m[1], name_number=m[2],
                        json_candidates=bykey[(m[1], m[2])], link_method="filename_year_number_only")
        elif old:
            item.update(name_year="", name_number=old[2],
                        json_candidates=bynum[old[2]], link_method="filename_number_only")
        else:
            item.update(name_year="", name_number="", json_candidates=[], link_method="unknown")
        try:
            with p.open("rb") as f:
                reader = PdfReader(f, strict=False)
                item["pages"] = len(reader.pages)
                item["encrypted"] = reader.is_encrypted
                item["first_page_images"] = len(reader.pages[0].get("/Resources", {}).get_object().get("/XObject", {})) if reader.pages else 0
        except Exception as exc:
            item["parse_status"] = type(exc).__name__
        raw = p.read_bytes()
        match = re.search(rb"/Count\s+(\d+)", raw)
        item["legacy_regex_pages"] = int(match[1]) if match else 1
        return item

    with ThreadPoolExecutor(max_workers=4) as pool:
        pdf_info = list(pool.map(inspect_pdf, pdfs))
    hash_groups = collections.defaultdict(list)
    for item in pdf_info:
        hash_groups[item["sha256"]].append(item["path"])
    duplicates = [v for v in hash_groups.values() if len(v) > 1]
    summary = {
        "files": len(pdf_info), "unique_hashes": len(hash_groups),
        "duplicate_excess": sum(len(g) - 1 for g in duplicates),
        "duplicate_groups": duplicates,
        "parse_errors": [i for i in pdf_info if i["parse_status"] != "ok"],
        "page_distribution": dict(collections.Counter(str(i["pages"]) for i in pdf_info)),
        "regex_mismatches": [i for i in pdf_info if i["pages"] != i["legacy_regex_pages"]],
        "filename_link_counts": dict(collections.Counter((i["link_method"], len(i["json_candidates"])) for i in pdf_info)),
    }
    summary["filename_link_counts"] = {str(k): v for k, v in summary["filename_link_counts"].items()}
    save("pdf_inventory.json", pdf_info)
    save("pdf_summary.json", summary)
    print("PDF structures inspected:", len(pdf_info), "unique hashes:", len(hash_groups), flush=True)

    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    w = "{%s}" % ns["w"]
    docx = []
    generator = (ROOT / "tools/generate_document.ps1").read_text(encoding="utf-8-sig")
    replacements = re.findall(r'Replace-Placeholder "(\{\{[^"]+\}\})"\s+(.+)', generator)
    for p in sorted((ROOT / "knowledge_base/templates").glob("*.docx")):
        with zipfile.ZipFile(p) as z:
            parts = {}
            for name in z.namelist():
                if name.startswith("word/") and name.endswith(".xml"):
                    tree = ET.fromstring(z.read(name))
                    text = "\n".join("".join(t.itertext()) for t in tree.findall(".//w:t", ns))
                    joined = "".join("".join(t.itertext()) for t in tree.findall(".//w:t", ns))
                    placeholders = sorted(set(re.findall(r"\{\{[^{}]+\}\}", joined)))
                    if placeholders or name in ("word/document.xml", "word/styles.xml"):
                        parts[name] = {"placeholders": placeholders}
                    if name == "word/document.xml":
                        parts[name].update(
                            paragraphs=["".join(n.text or "" for n in par.findall(".//w:t", ns)) for par in tree.findall(".//w:p", ns)],
                            section_properties=[ET.tostring(n, encoding="unicode") for n in tree.findall(".//w:sectPr", ns)],
                            explicit_halfpoint_sizes=sorted(set(n.get(w + "val") for n in tree.findall(".//w:sz", ns))),
                            page_fields=[n.text for n in tree.findall(".//w:instrText", ns)],
                            table_count=len(tree.findall(".//w:tbl", ns)),
                            repeat_table_headers=len(tree.findall(".//w:tblHeader", ns)),
                            keep_next_count=len(tree.findall(".//w:keepNext", ns)),
                            cant_split_count=len(tree.findall(".//w:cantSplit", ns)),
                        )
            ph = sorted(set(x for v in parts.values() for x in v["placeholders"]))
            docx.append({"path": rel(p), "parts": parts, "all_placeholders": ph,
                         "unmapped_placeholders": sorted(set(ph) - {a for a, b in replacements}),
                         "generator_replacements_absent": sorted({a for a, b in replacements} - set(ph)),
                         "zip_crc_error": z.testzip()})
    save("docx_xml_inspection.json", docx)
    save("placeholder_mapping.json", {"replacement_calls": replacements, "templates": [
        {"path": d["path"], "placeholders": d["all_placeholders"], "unmapped": d["unmapped_placeholders"]} for d in docx]})

    scripts = []
    for p in sorted((ROOT / "tools").glob("*.ps1")):
        raw = p.read_bytes()
        text = raw.decode("utf-8-sig")
        # Retain only line numbers for secrets. Never persist their values or full lines.
        sensitive = [i for i, line in enumerate(text.splitlines(), 1)
                     if re.search(r"(?i)(password|pwd)\s*=", line)]
        scripts.append({"path": rel(p), "utf8_bom": raw.startswith(b"\xef\xbb\xbf"),
                        "non_ascii": any(ord(c) > 127 for c in text),
                        "credential_literal_lines": sensitive,
                        "lines": len(text.splitlines())})
    save("script_inspection.json", scripts)

    try:
        import openpyxl
        wb = openpyxl.load_workbook(WORKBOOK, read_only=True, data_only=True)
        compare = {"path": str(WORKBOOK), "sha256": digest(WORKBOOK),
                   "status": "Excel intermediary only; NOT direct QL verification",
                   "sheets": [{"name": s.title, "rows": s.max_row, "columns": s.max_column} for s in wb],
                   "comparisons": {}}
        maps = {
            "di": {1: "so_di", 2: "ngay_vanban", 3: "tenloai_trichyeu", 4: "nguoi_ky"},
            "den": {2: "ngay_nhan", 4: "tac_gia", 5: "so_kihieu", 6: "ngay_vanban", 7: "trich_yeu", 8: "donvi_nhan"},
        }
        from datetime import datetime, date
        def display(value):
            if value is None:
                return ""
            if isinstance(value, (datetime, date)):
                return value.strftime("%d/%m/%Y")
            if isinstance(value, float) and value.is_integer():
                return str(int(value))
            return str(value).strip()
        def canonical(field, value):
            text = str(value).strip()
            if field.startswith("ngay"):
                for fmt in ("%d/%m/%Y", "%d/%m/%y", "%Y-%m-%d", "%d-%m-%Y", "%d.%m.%Y"):
                    try:
                        return datetime.strptime(text, fmt).strftime("%Y-%m-%d")
                    except ValueError:
                        pass
            return text
        for scope, years in (("di", (2023, 2024, 2025, 2026)), ("den", (2025, 2026))):
            rows = []
            for year in years:
                sheet = f"CV {'đi' if scope == 'di' else 'đến'} {year}"
                if sheet not in wb.sheetnames:
                    continue
                mapping = dict(maps[scope])
                if scope == "di" and year >= 2025:
                    mapping[5] = "noi_nhan"
                for rownum, cells in enumerate(wb[sheet].iter_rows(min_row=2, max_col=8), 2):
                    r = {name: display(cells[col-1].value) for col, name in mapping.items()}
                    r["nam"] = year
                    if scope == "di":
                        r.setdefault("noi_nhan", "")
                        keep = r.get("so_di", "") or r.get("tenloai_trichyeu", "")
                    else:
                        keep = r.get("so_kihieu", "") or r.get("trich_yeu", "")
                    if keep:
                        rows.append((sheet, rownum, r))
            mismatches = []
            canonical_mismatches = []
            for i, (source, target) in enumerate(zip(rows, records[scope]), 1):
                sheet, rownum, source_record = source
                fields = [k for k in source_record if str(source_record[k]) != str(target.get(k, ""))]
                if fields:
                    # No people, subjects, credentials or contact details in this evidence.
                    mismatch = {"json_row_1based": i, "sheet": sheet, "excel_row": rownum, "fields": fields}
                    if "ngay_nhan" in fields:
                        mismatch["excel_receive_date"] = source_record["ngay_nhan"]
                        mismatch["json_receive_date_is_hash_display"] = bool(re.fullmatch(r"#+", target.get("ngay_nhan", "")))
                    mismatches.append(mismatch)
                fields_canonical = [k for k in source_record if canonical(k, source_record[k]) != canonical(k, target.get(k, ""))]
                if fields_canonical:
                    cm = {"json_row_1based": i, "sheet": sheet, "excel_row": rownum, "fields": fields_canonical}
                    if "ngay_nhan" in fields_canonical:
                        cm["excel_receive_date"] = source_record["ngay_nhan"]
                        cm["json_receive_date_is_hash_display"] = bool(re.fullmatch(r"#+", target.get("ngay_nhan", "")))
                    canonical_mismatches.append(cm)
            compare["comparisons"][scope] = {
                "excel_accepted_rows": len(rows), "json_rows": len(records[scope]),
                "ordered_row_comparison": True, "different_rows": len(mismatches),
                "different_fields_counts": dict(collections.Counter(k for m in mismatches for k in m["fields"])),
                "mismatches": mismatches,
                "canonical_comparison_note": "In-memory only: integer display and unambiguous day/month/year formats; no source rewritten. Differences do not prove which source is correct.",
                "canonical_different_rows": len(canonical_mismatches),
                "canonical_different_fields_counts": dict(collections.Counter(k for m in canonical_mismatches for k in m["fields"])),
                "canonical_mismatches": canonical_mismatches,
                "column_headers": {s: [display(c.value) for c in next(wb[s].iter_rows(min_row=1, max_row=1, max_col=8))] for s in wb.sheetnames if s.startswith(f"CV {'đi' if scope == 'di' else 'đến'} ")},
            }
        wb.close()
        save("workbook_comparison.json", compare)
        print("Workbook compared read-only.", flush=True)
    except Exception as exc:
        save("workbook_comparison.json", {"status": "not verified", "error_type": type(exc).__name__})
        print("Workbook inspection unavailable:", type(exc).__name__, flush=True)

    columns = ["entry_kind", "source_tier", "path", "record_locator", "candidate_key",
               "ql_stable_key", "pdf_path", "link_status", "verification_status",
               "sha256", "bytes", "pages", "duplicate_group"]
    manifest = []
    dupe_index = {p: f"SHA256_GROUP_{n:03}" for n, g in enumerate(duplicates, 1) for p in g}
    for p in files:
        path = rel(p)
        tier = "S2"
        status = "artifact_AI_can_audit"
        if p.is_relative_to(LEGACY):
            tier, status = "legacy_system_file", "inventory_only_no_QL_records_read"
        elif p == WORKBOOK:
            tier, status = "S1_candidate", "Excel_intermediary_not_QL_verified"
        elif "metadata_index/" in path:
            tier, status = "S1", "derived_not_QL_verified"
        elif "sample_pdfs/" in path:
            tier, status = ("S0_candidate", "local_file_download_origin_not_QL_verified") if p.suffix.lower() == ".pdf" else ("S1_candidate", "image_origin_not_verified")
        manifest.append({"entry_kind": "file", "source_tier": tier, "path": path,
                         "verification_status": status, **hashes[path]})
    for i in pdf_info:
        row = next(r for r in manifest if r["path"] == i["path"])
        row.update(pdf_path=i["path"], pages=i["pages"], candidate_key=f"di|{i['name_year']}|{i['name_number']}",
                   record_locator=";".join(f"cv_di_history.json#row={n}" for n in i["json_candidates"]),
                   link_status=f"{i['link_method']};candidates={len(i['json_candidates'])};unverified",
                   duplicate_group=dupe_index.get(i["path"], ""))
    for scope, data in records.items():
        for i, r in enumerate(data, 1):
            key = f"di|{r['nam']}|{r['so_di']}" if scope == "di" else f"den|{r['nam']}|{r.get('so_kihieu', '')}|{r.get('ngay_vanban', '')}"
            matches = [p["path"] for p in pdf_info if i in p["json_candidates"]] if scope == "di" else []
            manifest.append({"entry_kind": "derived_record", "source_tier": "S1",
                             "path": f"knowledge_base/metadata_index/cv_{scope}_history.json",
                             "record_locator": f"row={i}", "candidate_key": key,
                             "pdf_path": ";".join(matches),
                             "link_status": "filename_candidates_only" if matches else "no_local_candidate",
                             "verification_status": "derived_not_QL_verified"})
    with (ROOT / "audit/P0_SOURCE_MANIFEST.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(manifest)
    print("Manifest entries:", len(manifest), flush=True)
    print(json.dumps({"metadata": {s: {k: v for k, v in q.items() if k not in ("duplicate_key_groups",)} for s, q in quality.items()},
                      "pdf_summary": {k: v for k, v in summary.items() if k not in ("duplicate_groups", "regex_mismatches", "parse_errors")}},
                     ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
