# Chapter 2: Document Naming Convention

**Document ID:** PLANNING-001-02
**Chapter:** 2 of 10
**Last Updated:** 2026-05-02

---

## Document Naming Format

- **`<Number>`** — Four-digit prefix indicating category (see Chapter 1, Section 1.3)
- **`<Project>`** — Short identifier (e.g., `Emulation`, `PPPoE`)
- **`<Topic>`** — Title-Case with hyphens (e.g., `ThreatModel`, `AccessControl`)

## Examples

| Document | Filename |
|----------|----------|
| Table of Contents | `0000-Emulation-TOC.md` |
| Threat Model | `0101-Emulation-Security-ThreatModel.md` |
| Security Implementation | `0106-Emulation-Security-Implementation.md` |
| Overview | `0200-Emulation-Overview.md` |
| Architecture Design | `0210-Emulation-Architecture-Design.md` |
| Implementation Tasks | `0300-Emulation-Implementation-Tasks.md` |
| Sysctl Interface | `0501-Emulation-Sysctl-Interface.md` |

## Naming Rules

1. Use hyphens to separate words (not underscores)
2. Use Title-Case for `<Topic>` (e.g., `ThreatModel`, not `Threat_model`)
3. Keep `<Project>` short and consistent across all documents
4. Always use 4 digits for the number prefix
5. End with `.md` extension