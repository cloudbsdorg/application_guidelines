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
- [**Configuration-Files**](Configuration-Files/CONFIGURATION.md)
  - Best practices for settings, data storage, and administrator experience.
- [**Internationalization (i18n)**](Internationalization/INTERNATIONALIZATION.md)
  - Ensuring global accessibility and localizability for all users.
- [**Unit-Testing**](Unit-Testing/UNITTESTS.md)
  - Standards for code reliability, testing practices, and CI integration.
- [**Testing-Infrastructure**](Testing-Infrastructure/TESTING_INFRASTRUCTURE.md)
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
- [**Web-User-Interfaces (Web UI)**](Web-User-Interfaces/WEBUI.md)
  - Guidelines for modern, secure, and accessible web-based frontends. Login at `/`; username or email; show/hide; remember username; factory first-login wizard; REVYTECH product brand.
- [**Markdown viewer and editor**](Web-User-Interfaces/MARKDOWN.md)
  - In-app GitHub-flavored markdown, sanitized, with a real editor.

---

## 🚀 Getting Started

If you are new to CloudBSD development, follow these steps:

1.  **Read the Core Standards**: Start with [Programming Languages](Languages/LANGUAGES.md) to choose the right tool for your project.
2.  **Understand Configuration**: Review the [Configuration Guidelines](Configuration-Files/CONFIGURATION.md) to ensure your app integrates well with the system.
3.  **Plan your Project**: Follow the [Planning Guidelines](Planning/PLANNING.md) to set up your `.plan/` directory and task tracking before writing code.
4.  **Plan your UI**: Choose between [TUI](TUI/TUI.md) and [Web UI](Web-User-Interfaces/WEBUI.md) based on your application's needs.
5.  **Implement Testing**: Ensure your project follows the [Unit Testing Standards](Unit-Testing/UNITTESTS.md) from the start.

## 🤖 Agents and AI-assisted development

This repository is written to be consumed by **any** agent tool, not one in
particular. There is a single tool-neutral source of truth and a thin adapter
per tool; adapters point at the shared content and never carry a rule of their
own.

| Consumer | What it reads | Notes |
|---|---|---|
| Any tool following the `AGENTS.md` convention (opencode, Codex, …) | [`AGENTS.md`](AGENTS.md) | Read directly on project open |
| Claude Code | [`CLAUDE.md`](CLAUDE.md) | Two `@` imports: `AGENTS.md` and `Agent-Behavior/AGENT_BEHAVIOR.md` |
| opencode | [`opencode.json`](opencode.json) | Lists the same documents in the same order |
| Cursor | `.cursor/rules/cloudbsd.mdc` | Points at `AGENTS.md` |
| A model with no checkout (pasted context, or a bot with a fixed prompt) | [`INIT_PROMPT.md`](INIT_PROMPT.md) | Self-contained; absolute URLs throughout |

- [**AGENTS.md**](AGENTS.md) — **the law.** Tool-neutral and authoritative. If a
  rule needs to change, it changes here.
- [**Agent-Behavior/AGENT_BEHAVIOR.md**](Agent-Behavior/AGENT_BEHAVIOR.md) — how to
  work: think before coding, minimum solution, surgical diffs, verifiable goals.
- [**INIT_PROMPT.md**](INIT_PROMPT.md) — a standalone condensation of the law for a
  model that cannot browse the repository.

### Skills

[`SKILLS/`](SKILLS/README.md) holds task-specific skills — one directory per
skill, each containing `SKILL.md` with `name`, `description`, and `keywords`
frontmatter. Categories cover analysis and porting, planning documents, FreeBSD
administration, diagramming, security, testing, releases, quality disciplines,
and platform work.

**[`SKILLS/TOC.md`](SKILLS/TOC.md) is the index** — trigger keywords mapped to
skill paths. It is generated from the tree by `tools/skills-index.py`, so it
cannot drift away from what is actually there, and it is the only list of skills
in the repository. Scan it, load the one skill you need; do not load the tree.

**🎨 Diagram standard.** Mermaid (```` ```mermaid ```` fences) is the format for
architecture, flowcharts, sequence diagrams, graphs, and docs. SVG is
additionally allowed for UI design and prototyping (wireframes, mockups,
screens) as in-repo `.svg` files — do not replace Mermaid with SVG for
architecture. ASCII-art diagrams are forbidden. DOT and PlantUML remain
deprecated.

### Scope: what belongs here

This repository is public and holds **general CloudBSD law** — how software
should be built and behave. It does not hold operational facts about any
particular deployment: machine names, addresses, credentials, and where
credentials are kept belong in a private operations repository, never here, not
even as an example. See "What belongs in this repository" in
[`AGENTS.md`](AGENTS.md).

### Checking your changes

```sh
bash test_md.sh                 # markdown sanity checks
tools/skills-index.py --check   # SKILLS/TOC.md matches the tree
```

## 🎯 Purpose

The goal of these guidelines is to provide a clear roadmap for developers, ensuring that every application—whether it's a low-level system tool or a complex web service—follows the same core principles of CloudBSD development.

Developers are expected to traverse this documentation and adhere to these standards before starting a new project or contributing to existing ones.

