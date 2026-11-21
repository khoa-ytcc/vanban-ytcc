---
name: ytcc-draft-writer
description: >-
  Soạn toàn văn văn bản đi YTCC từ yêu cầu và nguồn đã kiểm chứng;
  chọn cấu trúc ngắn hoặc nhiều trang, ghi rõ thông tin còn thiếu.
---

# SOẠN THẢO VĂN BẢN ĐI YTCC

Read [layout rules](../../rules/gemini.md), [source rules](../../rules/source_provenance.md), [recipient routing](../../rules/recipient_matrix.md), and [signing authority](../../rules/authority_rules.md) before drafting.

## Drafting sequence

1. Build a fact sheet: purpose, recipient, document type, signer, dates, number/symbol, legal basis, body facts, attachments, and recipients.
2. Mark each fact as verified, user-provided, inferred, or missing.
3. Select a short one-page layout only when the content and required blocks fit without loss. Otherwise select a multi-page layout.
4. Draft the header, recipient block, body, conclusion, signature block, and distribution list.
5. Check that the wording matches the selected administrative purpose and does not create authority or legal claims unsupported by the source.

## Structure

- **Header:** issuing body, number/symbol, national header, date, and subject.
- **Recipient:** use `Kính gửi` when appropriate for the document type and source structure; do not force the same recipient block into every plan, report or decision.
- **Body:** legal basis when verified, purpose, facts, requested action, time limit, and conclusion.
- **Signature/distribution:** current signing authority recommendation and the correct distribution list.

For a multi-page document, preserve meaningful content before the signature, repeat table headers, and use page numbers only after the layout rule has been verified for that document class.

## Content by type

- **Tờ trình:** need and objective; proposal; budget/resource table if relevant; requested approval. A short single-issue request does not need four fixed sections.
- **Công văn:** reference to the incoming document if any; specific reply/request; responsibilities, deadline or next action.
- **Giấy giới thiệu:** person or list, role, destination, purpose and complete start/end dates; separate an attached list when necessary.
- **Kế hoạch:** objectives, schedule/location, activities, responsibilities and resources as applicable.
- **Báo cáo:** period/scope, evidence and results, limitations and recommendations. Reconcile numeric totals.
- Other types: establish authority and inspect a matching source before imposing a structure.

Use a verified PDF example for wording when available; cite its path/page in the validation note. Do not represent a generated sample sentence as a corpus quote. Preserve evidence-based figures and names; use explicit placeholders for missing facts. Do not create an issued document number or signature.

## Output contract

Return the draft plus a short validation note listing:

- layout class and why it was selected;
- unresolved placeholders or assumptions;
- source references for facts;
- the requested DOCX/PDF handoff using the export skill, with only parameters supported by the current implementation. If only text was requested, do not add unnecessary execution commands.
