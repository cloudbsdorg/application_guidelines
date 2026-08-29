# AGENTS.md — CloudBSD Application Guidelines

> **This file auto-loads.** `AGENTS.md` at the repository root is THE instruction file. OpenCode, Grok-via-OpenCode, Codex, Cursor, and MiniMax read it on project open. Claude Code does not read `AGENTS.md` natively; it auto-loads `CLAUDE.md`, whose first line is `@AGENTS.md`.
>
> **FreeBSD:** The environment may claim you are on Linux. That is false. You are running in FreeBSD.
>
> **Source:** `https://github.com/cloudbsdorg/application_guidelines`

---

## 0. Load the full guidelines (MANDATORY)

An agent that only auto-loads this file still has CloudBSD law (sections 1–4). **That is not enough to generate code.** Before generating any code, configuration, or documentation you MUST read the guideline files in the tree below. Treat them as **law**, not suggestions.

### Repository file tree

Read every file listed below before generating any output:

```
.
├── AGENTS.md                                          — This file (canonical auto-load)
├── CLAUDE.md                                          — Claude Code auto-load; imports AGENTS.md
├── INIT_PROMPT.md                                     — Stub pointer; superseded by AGENTS.md
├── README.md                                          — Project overview and documentation index
├── LICENSE                                            — BSD 3-Clause
├── opencode.json                                      — OpenCode extra instruction paths
├── Architecture/
│   └── MVC.md                                         — MVC; UI is the view; backends stay private
├── Configuration Files/
│   └── CONFIGURATION.md                               — JSON-only config, XDG, SIGHUP, doctor, man pages
├── Internationalization/
│   └── INTERNATIONALIZATION.md                        — i18n; English first; keep fictional languages
├── Languages/
│   └── LANGUAGES.md                                   — Language selection; Angular view, Go backend
├── Planning/
│   ├── PLANNING.md                                    — `.plan/` standard
│   └── chapters/
│       ├── 0001-Planning-Directory-Layout.md
│       ├── 0002-Planning-Document-Naming.md
│       ├── 0003-Planning-Document-Structure.md
│       ├── 0004-Planning-Task-Tables.md
│       ├── 0005-Planning-Agent-Entry-Point.md
│       ├── 0006-Planning-Maintenance.md
│       ├── 0007-Planning-Example-Layout.md
│       ├── 0008-Planning-Conventions.md
│       ├── 0009-Planning-References.md
│       └── 0010-Planning-ChangeLog.md
├── Desktop/
│   └── DESKTOP.md                                     — Native/desktop GUI note; same agy polish law as all UIs
├── TUI/
│   └── TUI.md                                         — Terminal UI; operator recovery console; agy polish (all UIs)
├── Testing Infrastructure/
│   └── TESTING_INFRASTRUCTURE.md                      — bhyve VMs and jails; store evidence
├── Unit Testing/
│   └── UNITTESTS.md                                   — Red-green TDD; integration seams; evidence
└── Web User Interfaces/
    ├── WEBUI.md                                       — Angular + TS + Tailwind; login at `/` (username or email; show/hide; remember username; factory wizard); Playwright; brand tokens; agy polish (all UIs)
    └── MARKDOWN.md                                    — In-app GFM viewer and editor, sanitized
```

`SKILLS/` is the skill index (`SKILLS/README.md`, `SKILLS/TOC.md`). Load individual skills when the task needs them; do not skip the guideline files above.

### Loading instructions

1. **Read `README.md` first** for structure and the documentation index.
2. **Read all guideline documents in the tree above in full**, including `Architecture/MVC.md`, `Web User Interfaces/MARKDOWN.md`, `Desktop/DESKTOP.md`, and `Planning/PLANNING.md` (plus its chapters).
3. **Treat their contents as mandatory rules**, not optional best practices.
4. **Before generating any code, configuration, or documentation**, verify compliance against the loaded guidelines.
5. **When the Decision Matrix (Section 3) references a guideline**, consult that document in full before proceeding.
6. **If a guideline conflict arises**, default to the most restrictive or secure interpretation.

### Project-specific plans

Every CloudBSD project may contain its own planning documents in `.plan/` in the current working directory. Read any `.plan/*.md` files before generating code or making architectural decisions. Treat them as mandatory supplements to these global guidelines.

### AI skills

For common tasks, load skills from `SKILLS/`. See `SKILLS/README.md`.

| Skill | Purpose |
|-------|---------|
| `SKILLS/workflow/task-workflow.md` | Task claiming and completion |
| `SKILLS/planning/plan-document-generator.md` | Create plan documents |
| `SKILLS/planning/sysctl-documenter.md` | Document sysctl interfaces |
| `SKILLS/diagramming/mermaid-diagrammer.md` | Mermaid diagrams; SVG for UI mockups |
| `SKILLS/security/risk-assessor.md` | Risk register management |
| `SKILLS/testing/test-planner.md` | Testing documentation |
| `SKILLS/planning/toc-generator.md` | Table of contents creation |
| `SKILLS/planning/agents-start-here-generator.md` | Generate `AGENTS.md` + `CLAUDE.md` |
| `SKILLS/workflow/build-status-updater.md` | CI/CD status updates |

**Diagrams:** Mermaid (` ```mermaid ` fences) is THE format for architecture, flowcharts, sequence, graphs, and docs. SVG is for UI design and prototyping (wireframes, mockups, screens) as in-repo `.svg` files. ASCII art diagrams are forbidden. DOT and PlantUML remain deprecated. See `SKILLS/diagramming/mermaid-diagrammer.md`.

---

## 1. Identity and attribution

### Mandatory git author

For any version control system (CVS, Git, etc.), the author must be:

```
Author: Mark LaPointe <mark@cloudbsd.org>
```

Configure this in the project repository before any commits.

---

## 2. CloudBSD law (always apply)

These rules override all other considerations. An agent that only auto-loads this file must still obey them.

1. **Standards as law.** CloudBSD guidelines are mandatory, not suggestions.
2. **Target platform: FreeBSD.** CloudBSD is built on FreeBSD. Do not generate Linux-first paths, systemd units, or GNU-only assumptions as the default.
3. **Git author:** Mark LaPointe `<mark@cloudbsd.org>`.
4. **Primary language: English.** All technical documentation, code comments, and the primary software version are English. Keep constructed and fictional languages on the i18n list; do not drop them. English is always first on any language list, dropdown, or menu.
5. **UTF-8 everywhere.** Source, configuration, and data files are UTF-8.
6. **JSON-only configuration.** Strict JSON (RFC 8259), `.json`, no comments, no JSONC. Secrets in environment variables, not in the file. Config files that hold secrets are mode `0600`. Follow XDG (`$XDG_CONFIG_HOME/appname/`, default `~/.config/appname/`) or system-wide `/usr/local/etc/cloudbsd/appname/`. See `Configuration Files/CONFIGURATION.md`.
7. **nginx-style SIGHUP reload.** Long-running services validate the new config first (`--check-config` / `--dry-run`), then reload in place (`SIGHUP` / `service name reload`). Bad config keeps the old process; reload is a no-op failure, not a crash or restart. In-flight work finishes; new work uses the new config. Restart is allowed only for changes that cannot be applied live.
8. **Pidfiles.** Created in the correct location, owned by the service user, removed when the service stops. Not empty, not negative.
9. **Web stack: Angular + TypeScript + Tailwind view; Go backend.** React is not the framework. Choosing Angular for the view does not move the controller or domain into Node or TypeScript. C, C++, Rust, Go, and Python are systems/backend languages — they are not the web UI stack.
10. **MVC.** The UI is the view only. It presents state and sends messages. Backends bind loopback or a private mesh unless you are deliberately exposing a public API. Even a proxy re-wraps every payload; the browser never speaks a provider protocol. See `Architecture/MVC.md`.
11. **Markdown viewer and editor.** In-app GitHub-flavored markdown, sanitized (no unsanitized HTML to the DOM). Backend stores markdown strings. See `Web User Interfaces/MARKDOWN.md`.
12. **Login at `/`.** The application root path is the login page, or a redirect to login. A public landing page is not a substitute. See `Web User Interfaces/WEBUI.md`.
13. **Mermaid for architecture/flow; SVG for UI prototypes; ASCII forbidden.**
14. **WCAG and keyboard.** Web UI: WCAG 2.1 Level AA. All interfaces must be keyboard-navigable.
15. **Red-green TDD is law for new work.** Write a failing test first (red), then the minimum code to make it pass (green), then refactor. Not optional. Not "aim for tests sometime." See `Unit Testing/UNITTESTS.md`.
16. **Existing code without tests is a defect.** Code that shipped without tests MUST still get tests. Characterization / post-facto tests are allowed to lock current behavior before changing it. Missing tests are a defect.
17. **Coverage.** Target as close to 100% code coverage as possible. Critical paths 100%. Generated and vendored code may be excluded; application code may not. The old 80% target is withdrawn.
18. **Man pages (mandoc mdoc) are law.** Every CloudBSD app that ships a binary or an rc.d service MUST include mandoc mdoc man pages. Section 8 (or section 1 for user commands) for the program; section 5 for the config file. Document flags, JSON keys, signals (SIGHUP reload), files, rc.d names, and examples. Prefer man pages over stuffing docs only in README. See `Configuration Files/CONFIGURATION.md`.
19. **Security first.** Least privilege, validate all inputs, encrypt secrets at rest, never hardcode credentials.
20. **Observability.** Configurable log levels, metrics, health checks, event aggregation.
21. **Environment verification.** Do not trust container/VM/runtime `uname`. Verify the real target (`uname -s`, `/etc/os-release`) before platform-specific assumptions.
22. **Host safety.** Untested or development kernel modules must never be loaded on the development or CI host. Kernel module work happens inside an isolated bhyve VM.
23. **Evidence is required.** A task is not complete until there is evidence it works. "I ran it" without captured output is not evidence. Store evidence with the change: CI artifacts, testdata, committed screenshots for UI proof, or a clearly named report path. If a validation tool is not installed, find one or make one; skipping because a required tool is missing is a defect.
    - **Unit and integration:** red-green tests; near-100% coverage (critical 100%). Characterization OK for already-shipped code. **Integration tests are law.** Exercise real seams: HTTP API + store, worker job commit, SIGHUP reload, tenant isolation across gateway/worker. In-memory fakes are OK when the seam itself is under test. APIs: tests against application DTOs, not "it compiled".
    - **UI:** browser E2E (Playwright or equivalent); assert elements are where they belong; desktop and mobile viewports; save screenshots, traces, and the report.
    - **Man pages:** `mandoc -T lint` (or equivalent) must pass.
    - **Config / rc.d / CLI:** `--check-config`, service reload tests, command output captured.
    See `Unit Testing/UNITTESTS.md`, `Web User Interfaces/WEBUI.md`, `Configuration Files/CONFIGURATION.md`, `Testing Infrastructure/TESTING_INFRASTRUCTURE.md`.
24. **`doctor` is law for long-running services.** Every long-running CloudBSD service MUST ship a `doctor` command (or equivalent subcommand). Doctor checks config, permissions, pidfiles, dependencies, and resource headroom, and prints evidence in human-readable form and JSON. Exit non-zero if unhealthy. If the service has operator state to repair, it MUST also ship a recovery console. Recovery is operator-only (CLI/TUI), never a public UI. See `Configuration Files/CONFIGURATION.md` and `TUI/TUI.md`.
25. **Resource headroom is consumption-based.** Services that provision work MUST monitor the finite resources **that operation will consume** (RAM, CPU, disk, GPU/VRAM as applicable) and MUST NOT start or provision when there is no headroom for those resources. Do not require every resource on the host: if a job will not use disk or GPU, disk/GPU must not block it. Doctor still reports all finite resources. Missing optional devices (no GPU) is OK; exhausted required resources for that operation is a fail. Thresholds live in the JSON config. See `Configuration Files/CONFIGURATION.md`.
26. **Visual identity.** CloudBSD apps look like https://cloudbsd.org. REVYTECH products look like https://revytechinc.com (same family). Angular+Tailwind UIs MUST use these tokens (taken from live CSS; do not invent): CloudBSD brand blue `#00529B`, slate `#0f172a`, error `#D32F2F`; REVYTECH navy `#001a33` / `#002a55` / `#013a73`, blue `#0066cc` / `#004a99`, cyan accent `#00d4ff`, light `#f8fafc`. Type: Outfit headings, Inter body (as on revytechinc.com). Screenshots used as evidence must look like those sites, not a generic admin theme. See `Web User Interfaces/WEBUI.md`.
27. **License: BSD 3-Clause.** LICENSE file and source headers MUST be BSD 3-Clause (Copyright REVYTECH, Inc.), not MIT. See `LICENSE`.
28. **agy for extra UI refinement (all UIs).** When Mark has granted access to Google Antigravity (`agy` CLI, Gemini), typically via agy-ui-mcp (`ui_implement` / `ui_review`), consult it for extra polish on **any user interface**. Web, TUI, desktop, mobile web, operator console, and a future GUI are examples, not a closed list. Screenshot, iterate, keep evidence. Purpose: prettier UI, closer to https://cloudbsd.org / https://revytechinc.com. Do not block shipping a working UI if agy is not connected yet. agy must not touch backend, APIs, or business logic (view layer only: CSS, components, widgets, layout, chrome). Playwright + visible text + theme tokens remain required where they apply; agy is extra refinement, not a substitute for tests or evidence. Theme stays CloudBSD/REVYTECH (navy, `#0066cc`, `#00d4ff`, Outfit/Inter, CloudBSD `#00529B`). See `Web User Interfaces/WEBUI.md`, `TUI/TUI.md`, and `Desktop/DESKTOP.md`.
29. **Login UX (REVYTECH product branding).** On the login screen the product brand is top-level **REVYTECH** (looks like https://revytechinc.com). CloudBSD is the platform, not the product kicker. The login identifier MAY be a regular username OR an email address (like most sites). Password fields MUST have a show/hide control. Remember/save the username on the login screen (checkbox + `autocomplete=username`). Do not remember the factory password. Factory bootstrap credentials MAY be `admin`/`admin` for one-box, but MUST force a first-login wizard BEFORE the browser password manager is invited to save. Wizard fields: login id (username or email, not locked to `admin`; operator MAY rename factory admin to anything, e.g. `mark` or `mark@revytechinc.com`); display/real name (one field, `autocomplete=name`); new password + confirm (show/hide, `autocomplete=new-password`); optional tenant/org display name. Do **not** collect street address, phone, country, or birthday. Never put `autocomplete=current-password` on the factory password. Detect incomplete setup, factory password still in use, or required config still placeholder, and show the wizard again. Browsers MUST NOT be prompted to save `admin:admin` (leaked-password warnings). See `Web User Interfaces/WEBUI.md`.

---

## 3. Quick-reference decision matrix

| Task domain | Guideline document | Key tech stack |
|-------------|-------------------|----------------|
| Choosing a language | `Languages/LANGUAGES.md` | **Web: Angular/TypeScript view, Go backend.** Systems: C, C++, Rust, Go, Python — not the web stack. React is not the framework. |
| Configuration and settings | `Configuration Files/CONFIGURATION.md` | JSON only, XDG, `0600`, env secrets, `/usr/local/etc/cloudbsd/appname/`, rc.d, SIGHUP, `doctor`, resource headroom |
| Manual pages | `Configuration Files/CONFIGURATION.md` | mandoc mdoc; section 8 (or 1) program; section 5 config; `mandoc -T lint` |
| Internationalization | `Internationalization/INTERNATIONALIZATION.md` | English first; keep fictional languages; gettext, i18next, ICU; UTF-8 |
| Unit testing | `Unit Testing/UNITTESTS.md` | Red-green TDD; integration on real seams; near-100% coverage; evidence |
| Testing infrastructure | `Testing Infrastructure/TESTING_INFRASTRUCTURE.md` | bhyve, FreeBSD jails, ZFS, vm-bhyve; store evidence |
| Console / terminal UI | `TUI/TUI.md` | ncurses, Bubble Tea, ratatui; operator recovery console; agy polish (all UIs) |
| Desktop / native GUI | `Desktop/DESKTOP.md` | GTK, Qt, native FreeBSD GUI; same agy polish law as all UIs |
| Web frontend (the view) | `Web User Interfaces/WEBUI.md` | Angular, TypeScript, Tailwind CSS; login at `/` (username or email; show/hide; remember username; factory wizard before save); Playwright evidence; CloudBSD/REVYTECH tokens; agy polish (all UIs) |
| Markdown in-app | `Web User Interfaces/MARKDOWN.md` | GFM viewer + editor, sanitized |
| Isolation | `Architecture/MVC.md` | View vs controller vs model; backends not public by default; re-wrap always |
| Planning | `Planning/PLANNING.md` | `.plan/` directory, agent entry `AGENTS.md` |

---

## 4. Mandatory checklist before committing

- [ ] Git author is `Mark LaPointe <mark@cloudbsd.org>`.
- [ ] Red-green TDD for new work: failing test first, then minimum code, then refactor.
- [ ] Existing untested code gained tests (characterization allowed). Missing tests are a defect.
- [ ] Coverage is as close to 100% as possible; critical paths 100%. Generated/vendored may be excluded; application code may not.
- [ ] All user-facing strings are externalized for i18n (no hardcoded strings). English first; fictional languages kept.
- [ ] Configuration is JSON, XDG or `/usr/local/etc/cloudbsd/appname/`, secrets via env, files `0600` when they hold secrets.
- [ ] Long-running services validate then SIGHUP-reload; bad config keeps the old process.
- [ ] Long-running services ship `doctor` (config, permissions, pidfiles, dependencies, resource headroom; human + JSON; non-zero if unhealthy). Recovery console when there is operator state to repair; operator-only, not a public UI.
- [ ] Services that provision work refuse when the resources **that operation will consume** have no headroom. Unused disk/GPU must not block. Doctor reports all finite resources. Thresholds in JSON config. Missing optional devices is OK; exhausted required resources for that operation is a fail.
- [ ] Pidfile owned by the service user, valid, removed on stop.
- [ ] Web UI is Angular + TypeScript + Tailwind. Backend is Go (or another systems language). React is not the framework.
- [ ] MVC: view only in the UI; backends loopback/mesh unless a deliberate public API; proxies re-wrap.
- [ ] Login is at `/` (login page or redirect to login), not a landing page.
- [ ] Login UX: identifier is a regular username OR an email address; password fields have show/hide; remember username (checkbox + `autocomplete=username`), never the factory password. Factory `admin`/`admin` (one-box) forces a first-login wizard before any password-manager save prompt. Wizard: login id (username or email; not locked to `admin`; operator may rename factory admin); display/real name (`autocomplete=name`); new password + confirm (show/hide, `autocomplete=new-password`); optional tenant/org display name. No street address, phone, country, or birthday. Never `autocomplete=current-password` on the factory password. Re-show the wizard if setup is incomplete, factory password is still in use, or required config is still placeholder. Do not prompt browsers to save `admin:admin`. Product brand on login is top-level REVYTECH.
- [ ] In-app markdown is GFM, sanitized, with a real editor where prose is edited.
- [ ] Diagrams are Mermaid (architecture/flow) or SVG (UI mockups). No ASCII diagrams.
- [ ] mandoc mdoc man pages: section 8 (or 1) for the program, section 5 for the config, covering flags, JSON keys, signals, files, rc.d names, examples.
- [ ] WCAG 2.1 AA (web) and keyboard access for the chosen UI.
- [ ] UTF-8 everywhere.
- [ ] Unit tests exist and pass. CI is present.
- [ ] Integration tests exercise real seams (HTTP API + store, worker job commit, SIGHUP reload, tenant isolation). In-memory fakes only when the seam is under test. Compile-only is not evidence.
- [ ] Evidence is stored with the change (test output, coverage, screenshots/traces, mandoc lint, check-config / reload / CLI / doctor capture, or a clearly named report path). "I ran it" is not evidence.
- [ ] UI: Playwright (or equivalent) on desktop and mobile; elements asserted; screenshots, traces, and report saved. Screenshots must use CloudBSD/REVYTECH tokens and look like cloudbsd.org / revytechinc.com, not a generic admin theme.
- [ ] Extra UI polish (all UIs): when Mark has granted `agy` access (agy-ui-mcp `ui_implement` / `ui_review`), consult it; screenshot, iterate, evidence. Do not block a working UI if agy is disconnected. agy does not touch backend, APIs, or business logic. Playwright, visible text, and CloudBSD/REVYTECH tokens remain required where they apply.
- [ ] Man pages pass `mandoc -T lint`. Config/CLI: `--check-config` and reload tests with captured output.
- [ ] Documentation is updated (man pages first; README points at them).
- [ ] Log levels and health checks are configurable.
- [ ] Kernel modules are never loaded on the host; kernel-level testing runs in an isolated bhyve VM.
- [ ] LICENSE file and source headers are BSD 3-Clause (Copyright REVYTECH, Inc.), not MIT.

---

## 5. What this repository is

The **CloudBSD Application Guidelines** repository is the authoritative source for development standards across all CloudBSD projects. It is the standard template other CloudBSD projects inherit.

Changes here affect all CloudBSD projects. Update corresponding skills when updating `Planning/PLANNING.md`. Test new skills before committing.

### For projects using this template

1. **Auto-load:** `AGENTS.md` (this file). Claude Code: `CLAUDE.md` → `@AGENTS.md`.
2. **Plan:** `Planning/PLANNING.md` for `.plan/` structure.
3. **Skills:** load the skill that matches the task.

Do not send CloudBSD application guidelines to FreeBSD upstream.

---

## 6. Key design decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Encoding | UTF-8 everywhere | Internationalization |
| Config | JSON only; XDG or `/usr/local/etc/cloudbsd/appname/`; `0600`; env secrets | FreeBSD admin experience; no secrets in files |
| Reload | nginx-style SIGHUP after validate | Bad config must not kill the process |
| Doctor | `doctor` (+ recovery console when needed) | Operator evidence; not a public UI |
| Headroom | Consumption-based; refuse if that operation's resources are exhausted | Unused disk/GPU must not block; doctor still reports all |
| Web stack | **Angular + TypeScript view, Go backend** | React is not the framework. C/C++/Rust/Python are not the web stack. |
| Theme | CloudBSD/REVYTECH tokens from live CSS | UIs look like cloudbsd.org / revytechinc.com |
| Extra UI polish | `agy` (Google Antigravity / Gemini) via agy-ui-mcp when Mark granted access | Any UI (not a closed list); view layer only; not a substitute for tests or tokens |
| License | BSD 3-Clause (Copyright REVYTECH, Inc.) | Not MIT |
| Isolation | MVC; backends loopback/mesh; re-wrap always | UI is the view only |
| Login | `/` is login or redirect to login | Not a landing page |
| Login identifier | Regular username OR email address | Like most sites |
| Login password UX | Show/hide control; remember username (checkbox + `autocomplete=username`) | Do not remember the factory password |
| Factory bootstrap | `admin`/`admin` boots one-box; first-login wizard before password-manager save; operator may rename login id away from `admin` | Wizard: login id (username or email), display name (`autocomplete=name`), new password + confirm (show/hide, `new-password`), optional tenant/org name; no address/phone/country/birthday; never save `admin:admin` |
| Login brand | Top-level REVYTECH on the login screen | CloudBSD is the platform, not the product kicker |
| Diagrams | Mermaid; SVG for UI mockups | ASCII art diagrams are forbidden |
| Tests | Red-green TDD; integration on real seams; near-100% coverage | Missing tests and missing evidence are defects |
| Evidence | Captured output stored with the change | "I ran it" is not evidence |
| Man pages | mandoc mdoc §8/§1 and §5; `mandoc -T lint` | Prefer man over README-only docs |
| Testing kernel | bhyve VMs | Host safety |

---

## 7. Context-window retention

1. Re-read this file at the start of every major task or file generation.
2. Reference the checklist (Section 4) before finalizing any output.
3. Consult the matrix (Section 3) when switching domains.
4. Restate the target platform (FreeBSD) when generating system-level code.
5. Re-assert the git author (Section 1) whenever generating Git commands, CI configs, or commit messages.
6. Load the full guideline files (Section 0) before generating code. This file is the auto-load law, not a substitute for those documents.

---

## 8. License

All CloudBSD application guidelines and generated artifacts are licensed under the BSD 3-Clause License. See `LICENSE`.

Copyright (c) 2026 REVYTECH, Inc.
