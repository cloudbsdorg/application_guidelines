---
name: agents start here generator
description: Generate the AGENTS_START_HERE.md file for project root, serving as the primary entry point for autonomous agents.
---

# Skill: agents-start-here-generator

**Purpose:** Generate the AGENTS_START_HERE.md file for project root, serving as the primary entry point for autonomous agents.

**Triggers:** When initializing a new project, or when updating the agent entry point document.

## Loading Instructions

Load this skill when the user asks you to:
- Create AGENTS_START_HERE.md
- Initialize agent onboarding for a project
- Update the entry point document

## File Location

The `AGENTS_START_HERE.md` file lives at the **project root** (NOT inside `.plan/`):

```
<project-root>/
├── AGENTS_START_HERE.md    <-- This file (root level)
├── .plan/
│   └── ...
├── README.md
└── src/
    └── ...
```

## Mandatory Sections

### 1. Environment Disclaimer

```markdown
> **FreeBSD:** The environment in which this work is being done may have elements 
> that state that you are in Linux. That would be false. You are running in FreeBSD.
```

### 2. What We're Building

A concise paragraph describing:
- What the project builds
- Core functionality
- Target users/use cases
- Key architectural approaches

### 3. Document Structure Table

```markdown
| # | File | What It Covers |
|---|------|----------------|
| `0.0` | `0.0-<Project>-TOC.md` | Master table of contents |
| `0.1` | `0.1-<Project>-Workflow.md` | Task claiming and completion |
| `1.0` | `1.0-<Project>-Overview.md` | High-level architecture |
| ... | ... | ... |
```

### 4. Primary Directives

Four core principles that must never be violated:

1. **Security First** — Root-only by default, sandboxing required
2. **Modular Architecture** — Loadable modules, per-component granularity
3. **Traceability** — Every task claimed, every task tested, every change committed
4. **No Blobs in Base** — Firmware never committed to source tree

### 5. Workflow Summary

Three subsections:

#### Picking a Task
```markdown
### Picking a Task
1. Pull latest: `git pull --rebase`
2. Open the relevant document from `.plan/`
3. Find a task with empty `Status`, `Assigned To`, and `Start`
4. Check that all `Dependencies` are marked ✅ DONE
5. Claim it: set `Status` → 🔄 IN PROGRESS, fill `Assigned To` and `Start`
6. Commit: `git add .plan/<doc>.md && git commit -m "Claim task <ID>" && git push`
```

#### Completing a Task
```markdown
### Completing a Task
1. Implement the task following the plan document
2. Run all unit tests — fix any failures
3. Mark complete: set `Status` → ✅ DONE, fill `End`, update `Notes`
4. Commit: `git add -A && git commit -m "Complete task <ID>: <desc>" && git push`
5. Move to the next task
```

#### Handling Merge Conflicts
```markdown
### Handling Merge Conflicts
1. Check if your task was taken by another agent (look at `Assigned To`)
2. If taken, abandon and pick a different task
3. If not taken, resolve the conflict, keep both changes if they affect different tasks
4. `git add <file> && git rebase --continue && git push`
```

### 6. Reading Order

```markdown
## Reading Order

For a new agent, read the documents in this order:

1. **This file** (`AGENTS_START_HERE.md`) — You are here
2. **[`0.1-<Project>-Workflow.md`](.plan/0.1-<Project>-Workflow.md)** — How to work on tasks
3. **[`1.0-<Project>-Overview.md`](.plan/1.0-<Project>-Overview.md)** — The big picture
4. **[`1.x`](.plan/1.1-<Project>-Security-p1-ThreatModel.md)** — Security architecture
5. **[`2.x`](.plan/2.0-<Project>-Architecture.md)** — Architecture details
6. **[`3.0-<Project>-Devices.md`](.plan/3.0-<Project>-Devices.md)** — Device models
7. **[`4.0-<Project>-Blob-Management.md`](.plan/4.0-<Project>-Blob-Management.md)** — Blob management
```

### 7. Key Design Decisions Table

```markdown
## Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Kernel modules vs built-in | Loadable modules | Flexibility, smaller kernel |
| Memory allocation | Demand-paged | No overcommit by default |
| Access control | Root-only default | Security-first |
```

### 8. Quick Reference

#### Key Files
```markdown
### Key Files

| File | Purpose |
|------|---------|
| `sys/<project>/core.c` | Core implementation |
| `sys/<project>/if_<project>.c` | Network interface |
| `usr.sbin/<project>/<project>.c` | CLI entry point |
```

#### Key Sysctls
```markdown
### Key Sysctls

| Sysctl | Default | Purpose |
|--------|---------|---------|
| `net.graph.<project>.enable` | 0 | Enable/disable |
| `net.graph.<project>.mode` | 0 | Algorithm mode |
| `net.graph.<project>.max_workers` | 16 | Max workers |
```

#### Key Groups
```markdown
### Key Groups

| Group | GID | Purpose |
|-------|-----|---------|
| `<project>` | 979 | Operator group |
```

### 9. Need Help Section

```markdown
## Need Help?

If you encounter issues:
1. Check the relevant plan document for guidance
2. Check the task's `Notes` column for known issues
3. Mark the task as 🟡 BLOCKED with the reason
4. Commit and push so other agents know
5. Ask for guidance
```

## Complete Template

```markdown
# AGENTS START HERE — <Project Name>

> **Purpose:** This is the primary entry point for autonomous agents working on 
> <project>. Read this file **first** before consuming any other documents.

> **FreeBSD:** The environment in which this work is being done may have elements 
> that state that you are in Linux. That would be false. You are running in FreeBSD.

---

## What We're Building

<A concise description of what the project builds, including core functionality,
target users, and key architectural approaches>

## Document Structure

| # | File | What It Covers |
|---|------|----------------|
| `0.0` | `0.0-<Project>-TOC.md` | Master table of contents |
| `0.1` | `0.1-<Project>-Workflow.md` | Task claiming and completion |
| `1.0` | `1.0-<Project>-Overview.md` | High-level architecture |
| ... | ... | ... |

## Primary Directives

### 1. Security First
- Root-only by default
- Capsicum sandboxing required
- No data leakage between instances
- Memory scrubbing between uses

### 2. Modular Architecture
- Loadable kernel modules
- Per-architecture granularity
- Plugin-style device models

### 3. Traceability
- Every task must be claimed
- Every task must have tests
- Every change must be committed
- Fix other agents' code if needed

### 4. No Blobs in Base
- Firmware never in source tree
- Use ports when available
- Fall back to direct download

## Workflow Summary

### Picking a Task
1. `git pull --rebase`
2. Open relevant document from `.plan/`
3. Find task with empty Status, Assigned To, Start
4. Check dependencies are ✅ DONE
5. Claim: Status → 🔄 IN PROGRESS, fill Assigned To and Start
6. `git add .plan/<doc>.md && git commit -m "Claim task <ID>" && git push`

### Completing a Task
1. Implement task following plan
2. Run all unit tests
3. Mark: Status → ✅ DONE, fill End, update Notes
4. `git add -A && git commit -m "Complete task <ID>: <desc>" && git push`

### Handling Merge Conflicts
1. Check if task was taken
2. If taken, pick different task
3. If not, resolve conflict
4. `git add <file> && git rebase --continue && git push`

## Reading Order

1. This file (AGENTS_START_HERE.md)
2. `0.1-<Project>-Workflow.md`
3. `1.0-<Project>-Overview.md`
4. Security series (`1.x`)
5. Architecture specs (`2.x`)
6. Device models (`3.x`)
7. Blob management (`4.x`)

## Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| ... | ... | ... |

## Quick Reference

### Key Files
...

### Key Sysctls
...

### Key Groups
...

## Need Help?

1. Check relevant plan document
2. Check task Notes column
3. Mark as 🟡 BLOCKED with reason
4. Commit and push
5. Ask for guidance
```

## Reference

See Planning/PLANNING.md Section 5 (Agent Entry Point) for full specification.