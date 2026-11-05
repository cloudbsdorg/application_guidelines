# CloudBSD — standalone briefing for an agent with no repository

You are working on **CloudBSD**, a FreeBSD-based platform. This document is
self-contained: it can be pasted into a system prompt, handed to a bot, or given
to a model that has no checkout and cannot browse a filesystem. Everything it
points at is an absolute URL.

If you *do* have the repository checked out, read `AGENTS.md` instead — it is the
full law, and this file is a condensation of it.

- Source: <https://github.com/cloudbsdorg/application_guidelines>
- Full law: <https://raw.githubusercontent.com/cloudbsdorg/application_guidelines/main/AGENTS.md>
- Skill index: <https://raw.githubusercontent.com/cloudbsdorg/application_guidelines/main/SKILLS/TOC.md>

---

## 1. Priority order

When instructions conflict, the higher line wins:

1. What the user asks for right now.
2. This law — `AGENTS.md`, and the guideline documents it links.
3. The project's own `.plan/*.md` documents, if it has any.
4. Your own defaults.

If a guideline is ambiguous, take the most restrictive or most secure reading.

## 2. The law, condensed

**Target.** CloudBSD is FreeBSD. Never default to Linux paths, systemd units, or
GNU-only assumptions. Your environment may claim to be Linux; verify the real
target (`uname -s`, `/etc/os-release`) before making a platform assumption.

**Standards are law**, not suggestions. Git author is
`Mark LaPointe <mark@cloudbsd.org>`. Licence is BSD 3-Clause (Copyright REVYTECH,
Inc.), never MIT. UTF-8 everywhere. English first in every language list, and
constructed or fictional languages stay on the i18n list.

**Configuration** is strict JSON (RFC 8259) — no comments, no JSONC. It lives
under XDG (`$XDG_CONFIG_HOME/appname/`) or `/usr/local/etc/cloudbsd/appname/`.
Secrets come from the environment, never the file; files that hold secrets are
mode `0600`. Long-running services validate the new configuration first, then
reload in place on `SIGHUP` — a bad configuration keeps the old process running
and is a no-op failure, not a crash. Pidfiles are owned by the service user and
removed on stop.

**Web stack** is Angular + TypeScript + Tailwind for the view, Go for the
backend. React is not the framework. C, C++, Rust, Go, and Python are systems
and backend languages, not the web stack. Strict MVC: the UI presents state and
sends messages, backends bind loopback or a private mesh unless a public API is
deliberately intended, and a proxy re-wraps every payload — the browser never
speaks a provider's protocol.

**The application root `/` is the login page** or a redirect to it, never a
landing page. The login identifier may be a username *or* an email address.
Password fields carry an eye icon inside the field for show/hide, not a text
button. Remember the username, never the factory password. Factory
`admin`/`admin` must force a first-login wizard *before* any password-manager
save prompt. The product brand on the login screen is REVYTECH; CloudBSD is the
platform, not the product.

**Testing is law.** New work is red-green: a failing test first, then the minimum
code to pass, then refactor. Code that shipped without tests is defective and
must gain them — characterization tests are acceptable to lock behaviour before
changing it. Coverage as close to 100% as possible, critical paths at 100%.
Integration tests must exercise real seams; "it compiled" is not evidence.

**Evidence is required.** A task is not complete until there is captured
evidence that it works — test output, coverage, screenshots and traces for UI,
`mandoc -T lint` for man pages, `--check-config` and reload output for services.
"I ran it" is not evidence. If a required tool is missing, find one or build one;
skipping the check is a defect.

**Every shipped program gets mandoc mdoc man pages** — section 8 (or 1) for the
program, section 5 for its configuration. Every long-running service ships a
`doctor` command that checks configuration, permissions, pidfiles, dependencies,
and resource headroom, prints human-readable *and* JSON output, and exits
non-zero when unhealthy. Services that provision work refuse to start work when
the resources *that operation will consume* have no headroom — unused disk or
GPU must not block it.

**Diagrams** are Mermaid (```` ```mermaid ```` fences) for architecture,
flowcharts, sequence, and graphs; SVG for UI wireframes and mockups. ASCII-art
diagrams are forbidden. DOT and PlantUML are deprecated.

**Interfaces** meet WCAG 2.1 Level AA and are fully keyboard-navigable. They use
the CloudBSD and REVYTECH tokens — CloudBSD blue `#00529B`, slate `#0f172a`;
REVYTECH navy `#001a33`/`#002a55`/`#013a73`, blue `#0066cc`/`#004a99`, cyan
`#00d4ff`; Outfit for headings, Inter for body — and must look like
<https://cloudbsd.org> and <https://revytechinc.com>, not a generic admin theme.

**Safety.** Least privilege, validate every input, never hardcode credentials.
An untested kernel module is never loaded on a development or CI host — kernel
work happens inside an isolated bhyve VM. When real hardware must boot an
unproven kernel, it goes into a **new** boot environment activated for one boot
only, with panic auto-reboot armed, so a failure reverts on its own.

**Build and publish integrity.** Build only from committed source. Published
artifacts must not embed internal hostnames, addresses, or home-directory paths.
Verify the *installed* artifact on a clean machine — a module that loads proves
nothing about the userland that drives it. Never publish something that has not
booted or run.

**Dual-stack.** IPv4 and IPv6 are both first-class. A published hostname is not
finished until it has both an `A` and an `AAAA` record and both have been
observed to answer.

**Design rigor.** Program to an interface, favour composition, isolate each axis
of change and name the pattern. Know the complexity, know the loop invariant,
handle the boundary cases, and measure before optimising.

## 3. How to work

- State your assumptions. If something is ambiguous, ask rather than guessing.
- Write the minimum that solves the problem; nothing speculative.
- Keep changes surgical — every changed line should trace to the request.
- Turn the task into a verifiable goal and loop until the check passes.
- A fact belongs in one place. If you find the same rule written twice, that is a
  defect: delete one copy and link to the other.

## 4. Loading a skill

The repository carries a library of task-specific skills. **Do not load them
all.** Fetch the index once:

```
https://raw.githubusercontent.com/cloudbsdorg/application_guidelines/main/SKILLS/TOC.md
```

It maps trigger keywords to skill paths. Find the one row that matches the task,
then fetch that skill:

```
https://raw.githubusercontent.com/cloudbsdorg/application_guidelines/main/SKILLS/<path>/SKILL.md
```

Each skill is a directory containing `SKILL.md`; other files beside it are that
skill's reference material, fetched only when `SKILL.md` says to. There are
skills for planning documents, API and codebase analysis, porting, FreeBSD
administration, diagramming, security audit, code review, releases, and shipping.

## 5. Before you finish

Check your work against the commit checklist in `AGENTS.md` section 4 —
tests and evidence, i18n, configuration, man pages, diagrams, accessibility,
licence headers, and no internal machine names or credentials in anything
public. Fetch it if you need it:

```
https://raw.githubusercontent.com/cloudbsdorg/application_guidelines/main/AGENTS.md
```
