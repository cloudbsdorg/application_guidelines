# Chapter 5: Agent Entry Point

**Document ID:** PLANNING-001-05
**Chapter:** 5 of 10
**Last Updated:** 2026-05-02

---

## AGENTS_START_HERE.md

### 5.1 Purpose and Location

The `AGENTS_START_HERE.md` file lives at the **project root** (not inside `.plan/`), serving as the primary entry point for autonomous agents. It is the first document an agent should read when joining a project.

```
<project-root>/
├── AGENTS_START_HERE.md    <-- Primary agent entry point (root level)
├── .plan/
│   └── ...
├── README.md
└── src/
    └── ...
```

### 5.2 Mandatory Content

Every `AGENTS_START_HERE.md` must include the following sections:

#### 5.2.1 Environment Disclaimer

```markdown
> **FreeBSD:** The environment in which this work is being done may have elements
> that state that you are in Linux. That would be false. You are running in FreeBSD.
```

#### 5.2.2 Project Summary

A concise description of what the project builds, including:

- Core functionality
- Target users/use cases
- Key architectural approaches (e.g., kernel module, userland tools)

#### 5.2.3 Document Map

A table linking all plan documents with brief descriptions:

| # | File | What It Covers |
|---|------|----------------|
| `0.0` | `0.0-<Project>-TOC.md` | Master table of contents |
| `0.1` | `0.1-<Project>-Workflow.md` | Task claiming and completion |
| `1.0` | `1.0-<Project>-Overview.md` | High-level architecture |

#### 5.2.4 Primary Directives

Four core principles that govern all agent behavior:

1. **Security First** — Root-only by default, sandboxing required, no data leakage
2. **Modular Architecture** — Loadable modules, per-component granularity
3. **Traceability** — Every task claimed, every task tested, every change committed
4. **No Blobs in Base** — Firmware never committed to source tree

#### 5.2.5 Workflow Summary

Condensed instructions for:

- **Picking a Task** — Claiming protocol with git commands
- **Completing a Task** — Implementation, testing, and commit requirements
- **Handling Merge Conflicts** — Resolution strategy for multi-agent scenarios

#### 5.2.6 Reading Order

Recommended document sequence for new agents:

1. `AGENTS_START_HERE.md` (this file)
2. `0.1-<Project>-Workflow.md` — How to work on tasks
3. `1.0-<Project>-Overview.md` — The big picture
4. Security series (`1.x`)
5. Architecture specs (`2.x`)
6. Device models (`3.x`)
7. Blob management (`4.x`)

#### 5.2.7 Key Design Decisions

A table summarizing major architectural choices:

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Kernel modules vs built-in | Loadable modules | Flexibility, smaller kernel |

#### 5.2.8 Quick Reference

Provide compact lookup information for fast reference:

```markdown
## Quick Reference

### Key Files

| File | Purpose |
|------|---------|
| `sys/module/foo/foo_mod.c` | Module entry point |
| `sys/module/foo/foo_main.c` | Core implementation |

### Key Sysctls

| Sysctl | Default | Purpose |
|--------|---------|---------|
| `net.graph.foo.enable` | 0 | Enable/disable module |
| `net.graph.foo.mode` | 0 | Operation mode |

### Key Groups

| Group | GID | Purpose |
|-------|-----|---------|
| `operator` | 5 | Read-only access |
| `kmem` | 2 | Kernel memory access |

### Key Commands

```bash
# Load module
sudo kldload foo

# Check status
sysctl net.graph.foo

# Unload module
sudo kldunload foo
```

#### 5.2.9 Need Help?

Guidance for blocked agents:

1. Check relevant plan document
2. Check task `Notes` column
3. Mark as `🟡 BLOCKED` with reason
4. Commit and push
5. Seek guidance

### 5.3 Example Structure

```markdown
# AGENTS START HERE — <Project Name>

> **Purpose:** This is the primary entry point for autonomous agents working on
> <project>. Read this file **first** before consuming any other documents.

> **FreeBSD:** The environment may have elements that state you are in Linux.
> That would be false. You are running in FreeBSD.

---

## What We're Building

<A concise description of the project>

## Document Structure

| # | File | What It Covers |
|---|------|----------------|
| ...

## Primary Directives

### 1. Security First
...

### 2. Modular Architecture
...

### 3. Traceability
...

### 4. No Blobs in Base
...

## Workflow Summary

### Picking a Task
...

### Completing a Task
...

### Handling Merge Conflicts
...

## Reading Order

1. This file (AGENTS_START_HERE.md)
2. ...

## Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| ...

## Quick Reference

### Key Files
...

### Key Sysctls
...

### Key Groups
...

## Need Help?
...
```

### 5.4 Reference Implementation

See the [Kernel Emulation Framework](https://github.com/cloudbsdorg/freebsd-src-build-emulation/blob/main/AGENTS_START_HERE.md) for a complete example.