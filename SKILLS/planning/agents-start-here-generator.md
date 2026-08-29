---
name: agents start here generator
description: Generate AGENTS.md (canonical auto-load) and CLAUDE.md (@AGENTS.md) at the project root.
---

# Skill: agents-start-here-generator

**Purpose:** Generate `AGENTS.md` and `CLAUDE.md` at the project root. `AGENTS.md` is THE auto-load file. `CLAUDE.md` starts with `@AGENTS.md` then the short behavioral section. Do **not** generate `AGENTS_START_HERE.md` — that name never auto-loads.

**Triggers:** When initializing a new project, or when updating the agent entry point document.

## Loading Instructions

Load this skill when the user asks you to:
- Create `AGENTS.md` / `CLAUDE.md`
- Initialize agent onboarding for a project
- Update the entry point document
- Create AGENTS_START_HERE.md (legacy name — generate `AGENTS.md` + `CLAUDE.md` instead)

## File Location

These files live at the **project root** (NOT inside `.plan/`):

```
<project-root>/
├── AGENTS.md               <-- Auto-load (OpenCode, Grok, Codex, Cursor, MiniMax)
├── CLAUDE.md               <-- Claude Code; first line @AGENTS.md
├── .plan/
│   └── ...
├── README.md
└── src/
    └── ...
```

## AGENTS.md Mandatory Sections

Include CloudBSD law in full enough form that an agent that only auto-loads `AGENTS.md` still has: FreeBSD; git author Mark LaPointe <mark@cloudbsd.org>; JSON-only config + 0600 + env secrets + XDG + `/usr/local/etc/cloudbsd/appname/`; nginx-style SIGHUP reload; `doctor` + consumption-based resource headroom; Angular+TS+Tailwind view and Go backend (React is not the framework); CloudBSD/REVYTECH visual tokens; MVC; login at `/`; Mermaid/SVG (no ASCII); English-first i18n keeping fictional languages; pidfiles owned by the service user; WCAG/keyboard; UTF-8; red-green TDD; integration tests on real seams; evidence required; near-100% coverage; mandoc mdoc man pages (section 8 or 1, section 5) with `mandoc -T lint`; BSD 3-Clause (Copyright REVYTECH, Inc.), not MIT. Mandate reading the full guideline files from `application_guidelines` before generating code.

Then include the project sections below.

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
2. Red-green TDD: failing test first, then minimum code, then refactor. Unit AND integration tests. Capture evidence. "I ran it" is not evidence.
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

1. **This file** (`AGENTS.md`) — You are here. Claude Code: `CLAUDE.md` → `@AGENTS.md`.
2. **[`0.1-<Project>-Workflow.md`](.plan/0.1-<Project>-Workflow.md)** — How to work on tasks
3. **[`1.0-<Project>-Overview.md`](.plan/1.0-<Project>-Overview.md)** — The big picture
4. **[`1.x`](.plan/1.1-<Project>-Security-p1-ThreatModel.md)** — Security architecture
5. **[`2.x`](.plan/2.0-<Project>-Architecture.md)** — Architecture details
6. **[`3.0-<Project>-Devices.md`](.plan/3.0-<Project>-Devices.md)** — Device models
7. **[`4.0-<Project>-Blob-Management.md`](.plan/4.0-<Project>-Blob-Management.md)** — Blob management
```

### 7. Key Design Decisions Table

Web stack, if the project has a UI: **Angular/TypeScript view, Go backend**. Do not list C, C++, Rust, Go, Python as the web stack.

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

## CLAUDE.md (always generate with AGENTS.md)

First line MUST be `@AGENTS.md`. Then keep the short behavioral section: think before coding, simplicity first, surgical changes, goal-driven execution, red-green TDD as law.

```markdown
@AGENTS.md

# CLAUDE.md

Behavioral guidelines to reduce common LLM coding mistakes.

## 1. Think Before Coding
Don't assume. Don't hide confusion. Surface tradeoffs.

## 2. Simplicity First
Minimum code that solves the problem. Nothing speculative.

## 3. Surgical Changes
Touch only what you must. Clean up only your own mess.

## 4. Goal-Driven Execution
Define success criteria. Loop until verified.

## 5. Red-green TDD (law)
Write a failing test first, then the minimum code to pass, then refactor.
Existing code without tests MUST still get tests (characterization allowed).
Coverage: as close to 100% as possible; critical paths 100%.
```

## Complete AGENTS.md Template

```markdown
# AGENTS.md — <Project Name>

> **This file auto-loads.** Claude Code uses `CLAUDE.md`, which imports this file via `@AGENTS.md`.

> **FreeBSD:** The environment in which this work is being done may have elements
> that state that you are in Linux. That would be false. You are running in FreeBSD.

---

## CloudBSD Law

- Target: FreeBSD. Git author: Mark LaPointe <mark@cloudbsd.org>.
- Config: JSON only, `0600` if secrets, env for secrets, XDG or `/usr/local/etc/cloudbsd/appname/`.
- Reload: nginx-style SIGHUP (validate then reload; bad config keeps the old process).
- Web: Angular + TypeScript + Tailwind view, Go backend. React is not the framework.
- MVC: UI is the view; backends loopback/mesh unless a public API; proxies re-wrap.
- Login at `/` (login page or redirect to login).
- Mermaid for architecture/flow; SVG for UI mockups; ASCII forbidden.
- i18n: English first; keep fictional languages. UTF-8. WCAG/keyboard.
- Pidfiles owned by the service user.
- Red-green TDD for new work. Existing untested code MUST get tests (characterization allowed). Missing tests are a defect.
- Coverage: as close to 100% as possible; critical paths 100%. Generated/vendored may be excluded; application code may not.
- mandoc mdoc man pages: section 8 (or 1) for the program, section 5 for the config.

Before generating code, read the CloudBSD application guidelines in full (`Architecture/MVC.md`, `Web User Interfaces/MARKDOWN.md`, `Planning/PLANNING.md`, and the rest of that tree).

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
2. Red-green TDD; run all unit tests
3. Mark: Status → ✅ DONE, fill End, update Notes
4. `git add -A && git commit -m "Complete task <ID>: <desc>" && git push`

### Handling Merge Conflicts
1. Check if task was taken
2. If taken, pick different task
3. If not, resolve conflict
4. `git add <file> && git rebase --continue && git push`

## Reading Order

1. This file (`AGENTS.md`). Claude Code: `CLAUDE.md` → `@AGENTS.md`.
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

See Planning/PLANNING.md Chapter 5 (Agent Entry Point) for the full specification.
