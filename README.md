# CloudBSD Application Guidelines

Welcome to the official documentation for CloudBSD application development. This repository provides the definitive set of standards and best practices that developers must follow when building software for the CloudBSD ecosystem.

## 🏛️ Standards as Law

These documents are not mere suggestions; they are to be interpreted as **law** for all CloudBSD products. Compliance ensures a consistent, secure, and high-quality experience across the entire ecosystem.

---

## 📚 Documentation Index

### ⚙️ Core Standards
The fundamental building blocks of every CloudBSD application.

- [**Programming Languages**](Languages/LANGUAGES.md)
  - Recommended languages and selection criteria for different use cases.
- [**Configuration Files**](Configuration%20Files/CONFIGURATION.md)
  - Best practices for settings, data storage, and administrator experience.
- [**Internationalization (i18n)**](Internationalization/INTERNATIONALIZATION.md)
  - Ensuring global accessibility and localizability for all users.
- [**Unit Testing**](Unit%20Testing/UNITTESTS.md)
  - Standards for code reliability, testing practices, and CI integration.
- [**Testing Infrastructure**](Testing%20Infrastructure/TESTING_INFRASTRUCTURE.md)
  - VMM/bhyve VMs and FreeBSD jails for safe, isolated kernel and userland testing.
- [**Planning**](Planning/PLANNING.md)
  - Standards for `.plan/` directories, task tracking, and multi-agent coordination in all CloudBSD projects.

### 🧩 Architecture
- [**MVC and Isolation**](Architecture/MVC.md)
  - Views present and send messages. Backends stay private unless you expose an API.

### 🖼️ User Interfaces
Guidelines for building interfaces that follow the CloudBSD aesthetic and usability standards.

- [**Text-based User Interfaces (TUI)**](TUI/TUI.md)
  - Design and implementation of modern, responsive console-based applications.
- [**Desktop and native UI**](Desktop/DESKTOP.md)
  - Short note for GTK/Qt/native GUIs; same agy polish law as all UIs.
- [**Web User Interfaces (Web UI)**](Web%20User%20Interfaces/WEBUI.md)
  - Guidelines for modern, secure, and accessible web-based frontends. Login at `/`; username or email; show/hide; remember username; factory first-login wizard; REVYTECH product brand.
- [**Markdown viewer and editor**](Web%20User%20Interfaces/MARKDOWN.md)
  - In-app GitHub-flavored markdown, sanitized, with a real editor.

---

## 🚀 Getting Started

If you are new to CloudBSD development, follow these steps:

1.  **Read the Core Standards**: Start with [Programming Languages](Languages/LANGUAGES.md) to choose the right tool for your project.
2.  **Understand Configuration**: Review the [Configuration Guidelines](Configuration%20Files/CONFIGURATION.md) to ensure your app integrates well with the system.
3.  **Plan your Project**: Follow the [Planning Guidelines](Planning/PLANNING.md) to set up your `.plan/` directory and task tracking before writing code.
4.  **Plan your UI**: Choose between [TUI](TUI/TUI.md) and [Web UI](Web%20User%20Interfaces/WEBUI.md) based on your application's needs.
5.  **Implement Testing**: Ensure your project follows the [Unit Testing Standards](Unit%20Testing/UNITTESTS.md) from the start.

## 🤖 AI-Assisted Development

Agents auto-load **`AGENTS.md`** at the repository root. That file is CloudBSD law. Do not inject `INIT_PROMPT.md` (it is a stub pointer).

- [**AGENTS.md**](AGENTS.md)
  - Canonical auto-load file. OpenCode, Grok-via-OpenCode, Codex, Cursor, and MiniMax read it on project open.
- [**CLAUDE.md**](CLAUDE.md)
  - Claude Code auto-load. First line is `@AGENTS.md`; then short behavioral rules (think before coding, surgical changes, red-green TDD).

### AI Skills

**🎨 Diagram Standard**: Mermaid (`` ```mermaid `` fences) is THE diagramming format for architecture, flowcharts, sequence diagrams, graphs, and docs. SVG is additionally allowed for UI design and prototyping (wireframes, mockups, screens) as in-repo `.svg` files — do not replace Mermaid with SVG for architecture. ASCII art diagrams are forbidden. DOT and PlantUML remain deprecated.

AI agents can load specialized skills from the `SKILLS/` directory for common development tasks:

| Skill | Purpose |
|-------|---------|
| [SKILLS/workflow/task-workflow.md](SKILLS/workflow/task-workflow.md) | Task claiming, completion, and status management |
| [SKILLS/planning/plan-document-generator.md](SKILLS/planning/plan-document-generator.md) | Create new plan documents and `.plan/` structure |
| [SKILLS/planning/plan-validator.md](SKILLS/planning/plan-validator.md) | Validate plan document compliance |
| [SKILLS/planning/toc-generator.md](SKILLS/planning/toc-generator.md) | Generate table of contents documents |
| [SKILLS/planning/agents-start-here-generator.md](SKILLS/planning/agents-start-here-generator.md) | Create agent entry point documents |
| [SKILLS/planning/sysctl-documenter.md](SKILLS/planning/sysctl-documenter.md) | Document sysctl MIB hierarchies |
| [SKILLS/diagramming/mermaid-diagrammer.md](SKILLS/diagramming/mermaid-diagrammer.md) | Generate Mermaid diagrams; SVG for UI mockups |
| [SKILLS/security/risk-assessor.md](SKILLS/security/risk-assessor.md) | Create and maintain risk registers |
| [SKILLS/testing/test-planner.md](SKILLS/testing/test-planner.md) | Generate testing documentation |
| [SKILLS/workflow/build-status-updater.md](SKILLS/workflow/build-status-updater.md) | Maintain CI/CD build status |
| [SKILLS/testing/validation-document-generator.md](SKILLS/testing/validation-document-generator.md) | Create validation reports and corrections |
| [SKILLS/security/security-document-generator.md](SKILLS/security/security-document-generator.md) | Create security documents (threat model, access control, etc.) |
| [SKILLS/analysis/codebase-mapper.md](SKILLS/analysis/codebase-mapper.md) | Map any codebase into exhaustive tree-view markdown documents |
| [SKILLS/platform/opencode/effect.md](SKILLS/platform/opencode/effect.md) | Work with Effect v4 / effect-smol TypeScript code |
| [SKILLS/platform/opencode/github-triage.md](SKILLS/platform/opencode/github-triage.md) | Read-only GitHub triage for issues and PRs |
| [SKILLS/platform/opencode/pre-publish-review.md](SKILLS/platform/opencode/pre-publish-review.md) | Nuclear-grade 16-agent pre-publish release gate |
| [SKILLS/platform/opencode/work-with-pr.md](SKILLS/platform/opencode/work-with-pr.md) | Full PR lifecycle: worktree → implement → PR → merge |
| [SKILLS/platform/cloudflare/agents-sdk.md](SKILLS/platform/cloudflare/agents-sdk.md) | Build AI agents on Cloudflare Workers using Agents SDK |
| [SKILLS/platform/cloudflare/cloudflare.md](SKILLS/platform/cloudflare/cloudflare.md) | Comprehensive Cloudflare platform skill (Workers, Pages, storage, AI, networking) |

See [AGENTS.md](AGENTS.md) for CloudBSD law and the agent entry point, and [SKILLS/README.md](SKILLS/README.md) for the complete skill index.

## 🎯 Purpose

The goal of these guidelines is to provide a clear roadmap for developers, ensuring that every application—whether it's a low-level system tool or a complex web service—follows the same core principles of CloudBSD development.

Developers are expected to traverse this documentation and adhere to these standards before starting a new project or contributing to existing ones.

