# SOURCE PROVENANCE AND EVIDENCE RULES

## 1. Source hierarchy

The system must distinguish evidence from AI-produced implementation:

| Tier | Source | Appropriate use |
|---|---|---|
| S0 | Original PDF samples and records from QL văn bản, as identified by the user | PDF content/layout and QL registration metadata; record the file-to-record mapping and integrity checks |
| S1 | JSON metadata exports, OCR text, corpus statistics | Search and analysis; verify individual claims against S0 |
| S2 | AI-created DOCX templates, PowerShell scripts, drafts, prompts, rules, skills and old handoff notes | Audit targets and implementation; never evidence of the original convention |

The lower levels may help search or automate work, but they cannot override a higher-level source silently.
PDF and QL data have equal source status. Resolve each field against the relevant source; do not silently choose a winner if the two disagree. A prior signature is historical evidence, not proof of current authorization. Use official legal sources for a legal-compliance claim, with retrieval date and provision; do not describe a historical PDF convention as a legal requirement.

## 2. Provenance requirements

For every extracted example or formatting claim, record as much as is available:

- source path or QL văn bản identifier;
- document type and date;
- extraction method;
- PDF page, stable record key including year where needed, and hash when available;
- whether the value was read directly, inferred, or normalized;
- verification status.

When a source is unavailable, write `chưa xác minh` rather than filling the gap from a template or memory.

## 3. Conflict handling

If PDF, QL văn bản, and JSON disagree:

- preserve the original values;
- report the conflicting fields;
- use a verified higher-level source for a provisional decision over a derived copy, explaining the choice; if S0 sources disagree, leave the field unresolved pending clarification;
- do not rewrite the lower-level index until the discrepancy is understood.

## 4. Privacy and secrets

Do not copy credentials, connection strings, decrypted passwords, or unnecessary personal data into skills, reports, examples, commits, or prompts. Use redacted identifiers and local references.
