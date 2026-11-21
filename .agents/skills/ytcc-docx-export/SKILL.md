---
name: ytcc-docx-export
description: >-
  Sinh hoặc chuyển đổi DOCX/PDF văn bản YTCC bằng công cụ hiện có,
  kiểm tra dữ liệu, phân trang và bố cục; nhận diện giới hạn của template/script chưa nghiệm thu.
---

# XUẤT DOCX VÀ PDF YTCC

Read [PLAN.md](../../../PLAN.md), [layout rules](../../rules/gemini.md), [source rules](../../rules/source_provenance.md), and [runtime guidance](../../rules/runtime.md) before using the tools. Other file paths below are repository-relative.

## Preconditions

- Use the document type and facts supplied or established for this request. A request to create DOCX/PDF authorizes local generation; do not require another approval solely because this skill is used.
- Every unresolved placeholder is listed; do not silently fill missing facts.
- The source template is identified as an implementation artifact and its PDF comparison sample is recorded when available.
- If the user requests only conversion of an existing DOCX, convert that file without imposing a new template or inventing missing fields.

## Workflow

1. Validate input fields and normalize only values explicitly allowed by the draft.
2. Inspect actual files and script parameters. Select an available, verified layout suited to the content. Adaptive profiles are a P2 target until acceptance; do not assume `_MultiPage` files or layout parameters exist. If the current generator would damage the requested layout, report the limitation and use a suitable authorized document workflow rather than forcing the content through it.
3. Copy the template to `drafts/YYYY-MM/`; never edit the source template in place.
4. Run the Word COM generation and PDF export with deterministic cleanup on success and failure.
5. Extract text and render the PDF for visual checks using available document/PDF tools. If only DOCX was requested, use a temporary PDF for QA when available; report any visual check that could not be completed.
6. Check page count, header continuity, table header repetition, signature placement, distribution list, and leftover placeholders.

## Failure handling

Report the exact stage and error. Close the document and Word application in a `finally` path. Do not kill unrelated `WINWORD.EXE` processes. Do not overwrite an existing output without an explicit, logged choice.

Inspect unreviewed scripts before running them; cleanup requirements above are requirements for the execution path, not claims about the current code. Prefer a distinct output filename over an approval interruption for a name collision.

## Evidence

The completion note must include input summary, selected template, output paths, page count, checks run, comparison sample, and unresolved risks. A successful file conversion alone does not prove legal or formatting compliance.
