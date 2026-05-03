# Planning Guidelines for CloudBSD Projects

**Document ID:** PLANNING-001
**Version:** 3.0
**Last Updated:** 2026-05-02
**Maintainer:** CloudBSD Architecture Team
**Status:** ACTIVE

This document defines the standard for project planning in all CloudBSD repositories. Every CloudBSD project must include a `.plan/` directory at its root containing structured planning documents that guide development, track tasks, and enable multi-agent collaboration.

---

## Chapter Index

This document has been split into focused chapters for easier navigation:

| Chapter | File | Description |
|---------|------|-------------|
| 1 | [0001-Planning-Directory-Layout.md](chapters/0001-Planning-Directory-Layout.md) | `.plan/` directory structure, numbering, mandatory files, Phase 0 |
| 2 | [0002-Planning-Document-Naming.md](chapters/0002-Planning-Document-Naming.md) | Document naming conventions |
| 3 | [0003-Planning-Document-Structure.md](chapters/0003-Planning-Document-Structure.md) | Header/footer format, TOC, workflow, security docs |
| 4 | [0004-Planning-Task-Tables.md](chapters/0004-Planning-Task-Tables.md) | Task table format, claiming protocol, TODO tracker |
| 5 | [0005-Planning-Agent-Entry-Point.md](chapters/0005-Planning-Agent-Entry-Point.md) | `AGENTS_START_HERE.md` content requirements |
| 6 | [0006-Planning-Maintenance.md](chapters/0006-Planning-Maintenance.md) | Maintenance and update procedures |
| 7 | [0007-Planning-Example-Layout.md](chapters/0007-Planning-Example-Layout.md) | Complete `.plan/` layout examples |
| 8 | [0008-Planning-Conventions.md](chapters/0008-Planning-Conventions.md) | ASCII diagrams, sysctl conventions |
| 9 | [0009-Planning-References.md](chapters/0009-Planning-References.md) | External references |
| 10 | [0010-Planning-ChangeLog.md](chapters/0010-Planning-ChangeLog.md) | Version history |

---

## Quick Reference

### Document Numbering

| Prefix | Category |
|--------|----------|
| `0xxx` | Meta |
| `1xxx` | **Security (MANDATORY)** |
| `2xxx` | Overview & Architecture |
| `3xxx` | Implementation |
| `4xxx` | Testing |
| `5xxx` | Operations |
| `6xxx` | Alternatives |
| `7xxx` | Risks |
| `8xxx` | Future |
| `9xxx` | Validation |
| `10xx` | Testing Framework |
| `11xx` | Documentation |

### Mandatory Files

Every project must include:

**Meta:**
- `0000-<Project>-TOC.md`
- `0001-<Project>-Workflow.md`
- `0002-<Project>-Build-Status.md`

**Security (MANDATORY):**
- `0100-<Project>-Security-Overview.md`
- `0101-<Project>-Security-ThreatModel.md`
- `0102-<Project>-Security-AccessControl.md`
- `0103-<Project>-Security-Emulator.md`
- `0104-<Project>-Security-Runtime.md`
- `0105-<Project>-Security-Additional.md`
- `0106-<Project>-Security-Implementation.md`

**Architecture:**
- `0200-<Project>-Overview.md`
- `0201-<Project>-Current-Architecture.md`
- `0210-<Project>-Architecture-Design.md`

**Implementation:**
- `0300-<Project>-Implementation-Tasks.md`
- `0301-<Project>-Kernel-Module.md`
- `0302-<Project>-Userland-Tools.md`

**Testing:**
- `0400-<Project>-Testing.md`
- `0401-<Project>-Unit-Tests.md`
- `0402-<Project>-Integration-Tests.md`
- `0403-<Project>-Code-Validation.md`

**Operations:**
- `0500-<Project>-Governance.md`
- `0501-<Project>-Sysctl-Interface.md`

---

## See Also

- [AGENTS_START_HERE.md](../AGENTS_START_HERE.md) — Primary agent entry point
- [SKILLS/README.md](../SKILLS/README.md) — AI skills for planning tasks