# CloudBSD Application Guidelines — INIT PROMPT

> **Purpose**: This document is designed to be injected into the context window of any AI-assisted development session for CloudBSD projects. It ensures that all generated code, configuration, and documentation adheres to the official CloudBSD standards.
> **Usage**: Include this file as a system prompt or project-level instruction when starting a new CloudBSD project or module.
> **Source**: `git@github.com:cloudbsdorg/application_guidelines.git`

---

## 0. Repository Loading Protocol (MANDATORY)

When this prompt is injected into an AI session, you MUST load and internalize the **entire contents of this repository**. The following files are the authoritative CloudBSD standards and must be treated as **law** for all generated code, configuration, and documentation.

### Repository File Tree
Read every file listed below before generating any output:

- `README.md` — Project overview, documentation index, and getting-started guide.
- `INIT_PROMPT.md` — This file (system prompt and mandatory rules).
- `Languages/LANGUAGES.md` — Programming language selection criteria and recommended languages.
- `Configuration Files/CONFIGURATION.md` — Configuration management, storage standards, and security practices.
- `Internationalization/INTERNATIONALIZATION.md` — i18n requirements, encoding standards, and supported languages.
- `Unit Testing/UNITTESTS.md` — Testing philosophy, coverage targets, and CI integration.
- `TUI/TUI.md` — Text-based user interface design and implementation guidelines.
- `Web User Interfaces/WEBUI.md` — Web frontend standards, accessibility, and security guidelines.
- `LICENSE` — BSD 3-Clause License.

### Loading Instructions
1. **Read `README.md` first** to understand the repository structure and documentation index.
2. **Read all guideline documents** (`Languages/LANGUAGES.md`, `Configuration Files/CONFIGURATION.md`, `Internationalization/INTERNATIONALIZATION.md`, `Unit Testing/UNITTESTS.md`, `TUI/TUI.md`, `Web User Interfaces/WEBUI.md`) in full.
3. **Treat the contents of these files as mandatory rules**, not suggestions or optional best practices.
4. **Before generating any code, configuration, or documentation**, verify compliance against the loaded guidelines.
5. **When the Decision Matrix (Section 3) references a guideline document**, consult the full contents of that document before proceeding.
6. **If a guideline conflict arises**, default to the most restrictive or secure interpretation.

---

## 1. Identity & Attribution

### Mandatory Git Author
For any version control system (CVS, Git, etc.), the author must be set as:

```
Author: Mark LaPointe <mark@cloudbsd.org>
```

Ensure this is configured in the project repository before any commits are made.

---

## 2. Core Principles (Always Apply)

These principles override all other considerations and must never be forgotten:

1. **Standards as Law**: All CloudBSD guidelines are to be interpreted as law, not suggestions.
2. **Target Platform**: FreeBSD (CloudBSD is built on top of FreeBSD).
3. **Primary Language**: English for all technical documentation, code comments, and primary software versions.
4. **Security First**: Apply least-privilege, validate all inputs, encrypt secrets at rest, and never hardcode credentials.
5. **Test-Driven**: Write tests before implementation. Aim for 80% coverage (100% for critical paths).
6. **Accessibility**: All interfaces must be keyboard-navigable and meet WCAG 2.1 Level AA (for Web UI) or equivalent TUI accessibility.
7. **UTF-8 Everywhere**: All source code, configuration, and data files must use UTF-8 encoding.
8. **Observability**: Include configurable log levels, metrics, health checks, and event aggregation.

---

## 3. Quick-Reference Decision Matrix

Use this matrix to select the correct guideline document for your current task:

| Task Domain | Guideline Document | Key Tech Stack |
|-------------|-------------------|--------------|
| Choosing a language | `Languages/LANGUAGES.md` | C, C++, Rust, Go, Python, TypeScript |
| Configuration & settings | `Configuration Files/CONFIGURATION.md` | JSON, XDG Base Directory, rc.d |
| Internationalization | `Internationalization/INTERNATIONALIZATION.md` | gettext, i18next, ICU |
| Unit testing | `Unit Testing/UNITTESTS.md` | Google Test, pytest, Jest, cargo test |
| Console / terminal UI | `TUI/TUI.md` | ncurses, Bubble Tea, ratatui |
| Web frontend | `Web User Interfaces/WEBUI.md` | React, Tailwind CSS, TypeScript |

---

## 4. Mandatory Checklist Before Committing Code

Before any code is committed to a CloudBSD repository, verify the following:

- [ ] Git author is set to `Mark LaPointe <mark@cloudbsd.org>`.
- [ ] All user-facing strings are externalized for i18n (no hardcoded strings).
- [ ] Configuration follows XDG Base Directory Specification or `/usr/local/etc/cloudbsd/appname/`.
- [ ] Secrets are not stored in plain text; use environment variables or encrypted storage.
- [ ] Unit tests exist and pass (80%+ coverage, 100% for critical paths).
- [ ] CI pipeline configuration is present (GitHub Actions, GitLab CI, Jenkins, etc.).
- [ ] Documentation is updated (README, inline comments, configuration examples).
- [ ] Accessibility requirements are met for the chosen UI type.
- [ ] Log levels and health checks are configurable.
- [ ] License header is present (BSD 3-Clause, Copyright CloudBSD).

---

## 5. Context Window Retention Strategy

To prevent the AI from forgetting critical requirements during long sessions:

1. **Re-read this prompt** at the start of every major task or file generation.
2. **Reference the checklist** (Section 4) before finalizing any output.
3. **Consult the matrix** (Section 3) when switching domains (e.g., from backend to frontend).
4. **Restate the target platform** (FreeBSD) when generating system-level code (rc.d scripts, file paths, permissions).
5. **Re-assert the author** (Section 1) whenever generating Git commands, CI configs, or commit messages.

---

## 6. License

All CloudBSD application guidelines and generated artifacts are licensed under the BSD 3-Clause License. See `LICENSE` for full terms.

Copyright (c) 2026, CloudBSD.
