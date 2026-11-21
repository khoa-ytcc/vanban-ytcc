---
name: ytcc-classify-doc
description: >-
  Phân loại yêu cầu hành chính của Khoa YTCC khi chưa rõ loại văn bản;
  đề xuất hướng gửi, thẩm quyền cần xác minh và dữ liệu còn thiếu.
---

# PHÂN LOẠI VĂN BẢN HÀNH CHÍNH YTCC

Use this skill when the user has a task but has not yet selected the document type. Read [source rules](../../rules/source_provenance.md), [recipient routing](../../rules/recipient_matrix.md), and [signing authority](../../rules/authority_rules.md).

## Decision order

1. Identify from the request what action the document must cause: approval, reply, report, plan, introduction, invitation, internal decision, or notice. Ask only if the missing purpose materially changes the choice.
2. Identify the recipient and whether the request goes through a university functional office.
3. Select the type using the purpose:
   - request for policy, funding, staffing, or approval from the university: **Tờ trình**;
   - exchange, reply, request, or official information: **Công văn**;
   - send a person to contact, study, survey, or collect data: **Giấy giới thiệu**;
   - organize a program with schedule, tasks, resources, or budget: **Kế hoạch**;
   - periodic or result reporting: **Báo cáo**;
   - establish a council, issue an internal rule, or assign authority: consider **Quyết định** only after confirming issuing authority; otherwise consider a **Tờ trình** to the competent authority;
   - invite a person or organization to an event: **Giấy mời**;
   - announce information or a deadline to the relevant audience: consider **Thông báo**, with recipient structure based on the source.
4. Confirm signing authority from the authority rule. Treat the signer as a recommendation until the user's current delegation is confirmed.

## Response contract

Return:

1. recommended document type;
2. administrative reason;
3. proposed `Kính gửi` and `Nơi nhận`;
4. proposed signing authority;
5. facts still needed;
6. a short outline if classification alone was requested. If the user already requested a full draft or file, proceed with the drafting/export skill without asking for the same authorization again.

Do not invent a recipient, signer, deadline, legal basis, or budget. Label inferences and ask for confirmation when they affect the final document.

Classification capability is broader than the current five-template generator. Read [runtime guidance](../../rules/runtime.md) before promising DOCX support for Quyết định, Giấy mời or Thông báo. Do not use the wrong template as a substitute.
