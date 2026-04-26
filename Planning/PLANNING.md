# Planning Guidelines for CloudBSD Projects

This document defines the standard for project planning in all CloudBSD repositories. Every CloudBSD project must include a `.plan/` directory at its root containing structured planning documents that guide development, track tasks, and enable multi-agent collaboration.

## 1. The `.plan/` Directory

### 1.1 Purpose

The `.plan/` directory serves as the single source of truth for:

- **Project scope and architecture** — What is being built and why
- **Implementation roadmap** — Phased approach to delivery
- **Task tracking** — Claimable, trackable work items with dependencies
- **Security and design rationale** — Threat models, access control, and architectural decisions
- **Multi-agent coordination** — Protocols for concurrent work on shared branches

### 1.2 Location

Every CloudBSD project must have:

```
<project-root>/
├── .plan/
│   ├── 0.0-<Project>-TOC.md
│   ├── 0.1-<Project>-Workflow.md
│   ├── 1.0-<Project>-Overview.md
│   └── ...
├── README.md
└── ...
```

The `.plan/` directory must be committed to version control and kept up to date.

### 1.3 Mandatory Files

| File | Purpose |
|------|---------|
| `0.0-<Project>-TOC.md` | Master table of contents linking all plan documents |
| `0.1-<Project>-Workflow.md` | Task claiming, completion protocol, and multi-agent coordination |
| `1.0-<Project>-Overview.md` | High-level architecture, implementation phases, and design principles |

## 2. Document Naming Convention

Plan documents follow the `<Major>.<Minor>-<Project>-<Topic>.md` pattern:

- **`<Major>`** — Document category:
  - `0` — Meta documents (TOC, workflow, entry points)
  - `1` — Overview and security
  - `2` — Architecture and design
  - `3` — Implementation details
  - `4` — Testing and validation
  - `5` — Build, release, and operations
- **`<Minor>`** — Sequential within the major category
- **`<Project>`** — Short project identifier (e.g., `Emulation`, `Guidelines`, `WebUI`)
- **`<Topic>`** — Descriptive topic name using Title-Case with hyphens

Examples:
- `0.0-Emulation-TOC.md`
- `1.0-Emulation-Overview.md`
- `1.1-Emulation-Security-p1-ThreatModel-Isolation.md`
- `2.0-Emulation-Arch-amd64.md`

## 3. Document Structure

### 3.1 Table of Contents (`0.0`)

The TOC must include:

- A document map table with file, title, status, and description
- A dependency graph showing relationships between documents
- A recommended reading order for new contributors
- A cross-reference index for topics that span multiple documents

### 3.2 Workflow (`0.1`)

The workflow document must define:

- How to select and claim tasks
- The task table format (see Section 4)
- Commit and push requirements after claiming and completing
- How to handle blocked or impossible tasks
- Merge conflict resolution for multi-agent scenarios

### 3.3 Overview (`1.0`)

The overview document must cover:

- Executive summary and motivation
- Problem statement and target use cases
- High-level architecture with diagrams
- Supported platforms or configurations
- Implementation phases with milestones
- Risk assessment and mitigations

## 4. Task Tables

Plan documents that contain implementation tasks must use a standardized task table:

```markdown
| ID | Task | Status | Assigned To | Owner | Start | End | Dependencies | Files | Notes |
|----|------|--------|-------------|-------|-------|-----|--------------|-------|-------|
| 1.1 | Create module entry point | ⬜ PENDING | | | | | | `sys/foo/foo_mod.c` | |
```

### 4.1 Status Values

| Status | Meaning |
|--------|---------|
| `⬜ PENDING` | Not yet started, available to claim |
| `🔄 IN PROGRESS` | Claimed and being worked on |
| `🟡 BLOCKED` | Cannot proceed; reason noted in `Notes` |
| `✅ DONE` | Completed and verified |
| `❌ FAILED` | Could not be completed; reason noted in `Notes` |

### 4.2 Claiming Protocol

1. Verify all dependencies are `✅ DONE`
2. Set `Status` to `🔄 IN PROGRESS`
3. Set `Assigned To` to your identifier (hostname for agents)
4. Set `Start` to current UTC timestamp (`YYYY-MM-DD HH:MM UTC`)
5. Commit and push immediately so other agents see the claim

### 4.3 Completion Protocol

1. Implement the task and verify all tests pass
2. Set `Status` to `✅ DONE`
3. Set `End` to current UTC timestamp
4. Update `Notes` with a brief summary
5. Commit and push immediately

## 5. Agent Entry Point

Projects may optionally include an `AGENTS_START_HERE.md` file at the repository root. This file serves as the primary entry point for autonomous agents and must:

- State that the agent may see items in the environment that say Linux, and to ignore them because the agent is running in FreeBSD. 
- Summarize what the project builds
- List all plan documents with descriptions
- State primary directives (security, modularity, traceability)
- Provide a condensed workflow summary
- Link to the full workflow document in `.plan/`

## 6. Maintenance

- Plans must be updated when scope changes
- Completed tasks must remain in the tables for historical reference
- New documents must be added to the TOC and cross-reference index
- Outdated documents should be marked with a `⚠️ STALE` status in the TOC

## 7. Example `.plan/` Layout

```
my-project/
├── .plan/
│   ├── 0.0-MyProject-TOC.md
│   ├── 0.1-MyProject-Workflow.md
│   ├── 1.0-MyProject-Overview.md
│   ├── 1.1-MyProject-Security-ThreatModel.md
│   ├── 2.0-MyProject-Architecture.md
│   ├── 3.0-MyProject-Implementation.md
│   └── 4.0-MyProject-Testing.md
├── AGENTS_START_HERE.md
├── README.md
└── src/
    └── ...
```

## 8. References

- [Kernel Emulation Framework Plans](https://github.com/cloudbsdorg/freebsd-src-build-emulation/tree/main/.plan) — Reference implementation of the `.plan` structure
