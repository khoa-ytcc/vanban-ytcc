---
name: ytcc-reply-incoming
description: >-
  Đọc văn bản đến, trích xuất định danh và thời hạn có nguồn,
  đề xuất hình thức phúc đáp và soạn trả lời cho Khoa YTCC.
---

# PHÚC ĐÁP VĂN BẢN ĐẾN YTCC

Use this skill when the user supplies an incoming PDF, image, copied text, or a QL văn bản identifier. Read [source rules](../../rules/source_provenance.md), [recipient routing](../../rules/recipient_matrix.md), and [signing authority](../../rules/authority_rules.md). Locate and verify a supplied record identifier before treating it as evidence.

## Extraction

Extract and label the evidence for:

1. issuing organization;
2. document number and symbol;
3. issue date;
4. document type and subject;
5. requested action, deadline, attachments, and responsible unit.

If a field is unreadable or appears only in a derived index, mark it `chưa xác minh`.

## Routing

- report, ordinary comment, confirmation, or ordinary personnel nomination: usually a **Công văn phúc đáp**;
- a request that requires university approval, funding, or a major policy decision: usually a **Tờ trình đề xuất**;
- an invitation requiring attendance or nomination: usually a reply công văn, an official nomination, or a giấy giới thiệu depending on the requested action.

Use the recipient rule to establish the route from the incoming document and verified precedents. The reply recipient may differ from the issuing organization. The signer is a recommendation until supplied for the current task or verified through current authority/delegation evidence.

## Output

Produce:

- an evidence table with source paths or record identifiers;
- the recommended response type and reason;
- an opening sentence referring to verified incoming-document identifiers, for example "Thực hiện..." or "Phúc đáp...". An incoming letter is a procedural basis, not automatically a legal rule; do not force every reply to begin with "Căn cứ";
- `Kính gửi`, `Nơi nhận`, signer recommendation, and deadline;
- missing facts and questions for the user;
- a draft using the available facts; clearly mark missing fields. Ask only for gaps that affect a material decision and continue the independent portions.

Never fabricate a document number, date, deadline, legal basis, recipient, or signer.
