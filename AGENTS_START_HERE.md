# AGENTS START HERE — CloudBSD Application Guidelines

> **Purpose:** This is the primary entry point for autonomous agents working on the CloudBSD Application Guidelines repository. Read this file **first** before consuming any other documents.

> **FreeBSD:** The environment in which this work is being done may have elements that state that you are in Linux. That would be false. You are running in FreeBSD.

---

## What We're Building

The **CloudBSD Application Guidelines** repository is the authoritative source for development standards across all CloudBSD projects. It provides:

- **Planning standards** — The `.plan/` directory structure and document conventions
- **Language guidelines** — Criteria for choosing programming languages
- **Configuration standards** — XDG Base Directory, rc.d scripts, secrets management
- **Testing standards** — Unit testing philosophy, infrastructure requirements
- **UI/UX guidelines** — TUI and WebUI development standards
- **Internationalization** — i18n requirements and encoding standards

This repository is the **standard template** that all CloudBSD projects inherit from.

## Document Structure

| File | What It Covers |
|------|----------------|
| `README.md` | Project overview and documentation index |
| `INIT_PROMPT.md` | System prompt for AI-assisted development |
| `Planning/PLANNING.md` | The `.plan/` directory standard |
| `SKILLS/` | AI skills for common development tasks |
| `Languages/LANGUAGES.md` | Programming language selection criteria |
| `Configuration Files/CONFIGURATION.md` | Configuration management |
| `Unit Testing/UNITTESTS.md` | Testing philosophy and coverage |
| `Testing Infrastructure/TESTING_INFRASTRUCTURE.md` | bhyve VM and jail testing |
| `TUI/TUI.md` | Terminal UI guidelines |
| `Web User Interfaces/WEBUI.md` | Web frontend standards |
| `Internationalization/INTERNATIONALIZATION.md` | i18n and encoding |

## Primary Directives

### 1. Standards as Law
All CloudBSD guidelines are to be interpreted as **mandatory rules**, not suggestions or optional best practices.

### 2. Target Platform: FreeBSD
CloudBSD is built on FreeBSD. All code must be designed for FreeBSD.

### 3. Security First
Apply least-privilege, validate all inputs, encrypt secrets at rest, never hardcode credentials.

### 4. Test-Driven Development
Write tests before implementation. Aim for 80% coverage (100% for critical paths).

### 5. Host Safety
Untested kernel modules must **never** be loaded on the development host. All kernel testing must occur inside an isolated bhyve VM.

## Skills

AI agents should load relevant skills from the `SKILLS/` directory:

| Skill | When to Load |
|-------|--------------|
| `SKILLS/workflow/task-workflow.md` | When claiming or completing tasks |
| `SKILLS/planning/plan-document-generator.md` | When creating new plan documents |
| `SKILLS/planning/sysctl-documenter.md` | When documenting sysctl interfaces |
| `SKILLS/diagramming/ascii-diagrammer.md` | When creating architecture diagrams |
| `SKILLS/security/risk-assessor.md` | When creating risk registers |
| `SKILLS/testing/test-planner.md` | When creating test plans |
| `SKILLS/planning/toc-generator.md` | When creating TOC documents |
| `SKILLS/planning/agents-start-here-generator.md` | When initializing projects |
| `SKILLS/workflow/build-status-updater.md` | When updating build status |

## Workflow Summary

### For This Repository (application_guidelines)

This is a **template repository**. Changes here affect all CloudBSD projects.

1. Changes require review before commit
2. Update corresponding skills when updating Planning/PLANNING.md
3. Test any new skills before committing

### For Projects Using This Template

When creating or updating a project based on these guidelines:

1. **Read first:** `INIT_PROMPT.md` — Contains mandatory rules
2. **Plan projects:** Follow `Planning/PLANNING.md` for `.plan/` structure
3. **Load skills:** Use appropriate skill for the task at hand

## Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Encoding | UTF-8 everywhere | Internationalization requirement |
| Config location | XDG Base Directory | FreeBSD standards compliance |
| Testing | bhyve VMs for kernel | Host safety requirement |
| Languages | C, C++, Rust, Go, Python | Based on task requirements |

## Quick Reference

### Key Files

| File | Purpose |
|------|---------|
| `Planning/PLANNING.md` | `.plan/` directory standard |
| `SKILLS/workflow/task-workflow.md` | Task management |
| `INIT_PROMPT.md` | System prompt for AI sessions |

### Core Principles

1. **FreeBSD first** — Not Linux
2. **Security always** — Least privilege, input validation
3. **Tests required** — 80%+ coverage
4. **No blobs in base** — Firmware via ports
5. **UTF-8 everywhere** — Internationalization

## Reading Order

For new contributors to CloudBSD:

1. **This file** (`AGENTS_START_HERE.md`) — You are here
2. **`README.md`** — Project overview
3. **`INIT_PROMPT.md`** — Mandatory rules for AI sessions
4. **`Planning/PLANNING.md`** — Planning standards
5. **`SKILLS/README.md`** — Available AI skills
6. Relevant guideline document (based on your task):
   - `Languages/LANGUAGES.md`
   - `Configuration Files/CONFIGURATION.md`
   - `Unit Testing/UNITTESTS.md`
   - `Testing Infrastructure/TESTING_INFRASTRUCTURE.md`
   - `TUI/TUI.md`
   - `Web User Interfaces/WEBUI.md`

## Need Help?

1. Check the relevant guideline document
2. Check `Planning/PLANNING.md` for planning questions
3. Load the appropriate skill for your task
4. Review `README.md` for documentation index

---

**Remember:** This repository defines the standards that all other CloudBSD projects follow. Maintain high quality in all changes.