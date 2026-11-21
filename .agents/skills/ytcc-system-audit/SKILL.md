---
name: ytcc-system-audit
description: >-
  Kiểm toán hệ thống văn bản YTCC hoặc nghiệm thu một phase: đối chiếu PDF gốc và QL văn bản
  với template, script, chỉ mục và rules do AI tạo; lập báo cáo có bằng chứng.
---

# KIỂM TOÁN HỆ THỐNG VĂN BẢN YTCC

Use this skill for a baseline audit or a phase acceptance review. Read [AGENTS.md](../../../AGENTS.md), [PLAN.md](../../../PLAN.md), [source rules](../../rules/source_provenance.md), [worker protocol](../../rules/worker_protocol.md), and [runtime guidance](../../rules/runtime.md) first. These links resolve from this skill directory; all other paths below are repository-relative.

## Scope

- Inspect original PDF samples and the legacy QL văn bản workspace in read-only mode.
- Inspect derived JSON indexes, DOCX templates, PowerShell scripts, skills, rules, README, and HANDOFF.
- Separate facts verified from higher-level sources, derived values, AI-produced implementation, and unresolved assumptions.

## Required report

Write the report to the path specified by the phase, normally `audit/P0_AUDIT.md`. Include:

1. inventory with source tier and provenance;
2. findings with file paths, line numbers or record identifiers where possible;
3. conflicts between PDF, QL văn bản, and JSON;
4. risks ranked Critical/High/Medium/Low (P0–P4 identify phases, not severity);
5. representative test cases for short, multi-page, table-heavy, and appendix documents;
6. explicit items that remain `chưa xác minh`;
7. recommendations for the next phase.

For baseline P0 also create `audit/P0_SOURCE_MANIFEST.csv` and `audit/P0_TEST_CASES.md`, as specified in PLAN. Report the inspected sample size and selection method. Identify each of the five AI-created DOCX templates and nine scripts as audit targets; their existence and a successful conversion do not validate them.

Inspect DOCX XML and actual generated content, rather than assuming the template-generation script matches the saved DOCX. Read scripts before executing them, particularly those with external connections. Put reproductions in `audit/artifacts/P0/`; avoid changing implementation to make a baseline test pass.

## Guardrails

- Do not modify source PDFs or legacy-system files.
- Do not write credentials or decrypted secrets to the report.
- Do not promote an AI-created template or script to evidence merely because it renders successfully.
- Do not edit implementation during a baseline audit unless the assignment explicitly changes the phase.
- Do not edit planner-owned environment files. Propose changes with evidence in the report; the user returns that report to the planner.
- If QL access or a linked PDF is unavailable, name the missing evidence, complete independent checks, and keep that item unverified.
