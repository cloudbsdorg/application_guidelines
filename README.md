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

### 🖼️ User Interfaces
Guidelines for building interfaces that follow the CloudBSD aesthetic and usability standards.

- [**Text-based User Interfaces (TUI)**](TUI/TUI.md)
  - Design and implementation of modern, responsive console-based applications.
- [**Web User Interfaces (Web UI)**](Web%20User%20Interfaces/WEBUI.md)
  - Guidelines for modern, secure, and accessible web-based frontends.

---

## 🚀 Getting Started

If you are new to CloudBSD development, follow these steps:

1.  **Read the Core Standards**: Start with [Programming Languages](Languages/LANGUAGES.md) to choose the right tool for your project.
2.  **Understand Configuration**: Review the [Configuration Guidelines](Configuration%20Files/CONFIGURATION.md) to ensure your app integrates well with the system.
3.  **Plan your UI**: Choose between [TUI](TUI/TUI.md) and [Web UI](Web%20User%20Interfaces/WEBUI.md) based on your application's needs.
4.  **Implement Testing**: Ensure your project follows the [Unit Testing Standards](Unit%20Testing/UNITTESTS.md) from the start.

## 🤖 AI-Assisted Development

When using AI tools (e.g., GitHub Copilot, Claude, ChatGPT) to generate code for CloudBSD projects, always start by loading the initialization prompt:

- [**INIT_PROMPT.md**](INIT_PROMPT.md)
  - The mandatory system prompt to inject into any AI session. It ensures the AI remembers the CloudBSD standards, the mandatory git author, and the target platform (FreeBSD).

## 🎯 Purpose

The goal of these guidelines is to provide a clear roadmap for developers, ensuring that every application—whether it's a low-level system tool or a complex web service—follows the same core principles of CloudBSD development.

Developers are expected to traverse this documentation and adhere to these standards before starting a new project or contributing to existing ones.

