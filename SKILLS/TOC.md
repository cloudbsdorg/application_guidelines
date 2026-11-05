# Skills — Table of Contents

> **Generated file.** Produced from the frontmatter of every
> `SKILLS/**/SKILL.md` by `tools/skills-index.py`. Do not hand-edit it:
> change the skill's frontmatter and regenerate. This is the *only* list
> of skills in the repository, so that no second list can contradict it.

**For agents:** scan the trigger table, find the row that matches your task,
and load **that one skill**. Do not load the tree. Loading everything is not
thoroughness — it spends the context you needed for the work.

Each skill is a directory containing `SKILL.md`. Other `.md` files beside it
are that skill's reference material; load them only when `SKILL.md` says to.

If you cannot browse a filesystem, every path below resolves as:

```
https://raw.githubusercontent.com/cloudbsdorg/application_guidelines/main/SKILLS/<path>/SKILL.md
```

There are **51 skills**.

---

## Trigger index

| If the task mentions… | Load | What it is |
|---|---|---|
| `agent entry point`, `AGENTS.md`, `CLAUDE.md`, `project init` | `planning/agents-start-here-generator/SKILL.md` | Generate a project's agent entry point: AGENTS.md as the canonical auto-load file plus a thin CLAUDE.md that imports it |
| `API`, `REST`, `endpoint`, `HTTP`, `OpenAPI`, `Swagger`, `GraphQL`, `gRPC`, `WebSocket`, `SSE`, `webhook` | `analysis/api-analyzer/SKILL.md` | Document a REST or HTTP API - endpoints, request/response shapes, authentication, pagination, rate limits, webhooks |
| `bectl`, `boot environment`, `one-shot`, `rollback`, `unproven kernel`, `kldload`, `panic`, `watchdogd`, `META_MODE` | `freebsd-admin/safe-kernel-deploy/SKILL.md` | Install an unproven kernel, kernel module, or world onto a FreeBSD machine so that a panic, a hang, or a kernel that will not boot reverts to the last known-good state on its own |
| `bhyve`, `VM`, `virtual machine`, `vm-bhyve`, `virtio`, `tap`, `bridge` | `freebsd-admin/bhyve-manager/SKILL.md` | Create, configure, run, and troubleshoot bhyve virtual machines on FreeBSD, with vm-bhyve or bhyve(8) directly |
| `build status`, `CI`, `CD`, `0002 document` | `workflow/build-status-updater/SKILL.md` | Maintain a project's build status document for CI/CD tracking |
| `Cloudflare`, `Worker`, `Pages`, `KV`, `D1`, `R2`, `Queues`, `Workers AI`, `Tunnel`, `WAF`, `DNS`, `AAAA`, `proxied` | `platform/cloudflare/cloudflare-platform/SKILL.md` | Choose the right Cloudflare product and understand how it fits together - Workers, Pages, KV, D1, R2, Queues, Workers AI, Vectorize, Tunnel, WAF, and the Terraform/Pulumi providers |
| `Cloudflare Agents`, `Agents SDK`, `stateful agent`, `Durable Object agent`, `Workflows`, `MCP server` | `platform/cloudflare/cloudflare-agents-sdk/SKILL.md` | Build agents on Cloudflare Workers with the Agents SDK - the Agent class, persistent state, callable RPC, scheduling, Workflows, MCP servers, and React hooks |
| `code quality`, `duplication`, `refactor`, `extract interface`, `DRY` | `analysis/code-quality-analyzer/SKILL.md` | Find duplication and plan the refactoring that removes it |
| `codebase`, `explore`, `understand`, `find in code`, `where is`, `read-only` | `analysis/codebase/SKILL.md` | Read-only exploration of an unfamiliar codebase |
| `consult`, `advice`, `opinion`, `recommend`, `best practice`, `should I` | `planning/office-hours/SKILL.md` | Give a direct consulting recommendation with the reasoning behind it, rather than a list of options |
| `debug`, `investigate`, `root cause`, `trace error`, `why is X broken`, `diagnose` | `workflow/investigate/SKILL.md` | Find the root cause of a broken system using an evidence-based protocol rather than guesswork |
| `design pattern`, `GoF`, `Knuth`, `TAOCP`, `complexity`, `invariant`, `refactor`, `code review` | `quality/code-craft/SKILL.md` | Apply the enduring lessons of the Gang of Four "Design Patterns" and Knuth's "The Art of Computer Programming" to code you write, refactor, or review |
| `diagram`, `architecture`, `flowchart`, `sequence`, `mermaid`, `SVG`, `wireframe`, `ASCII art` | `diagramming/mermaid-diagrammer/SKILL.md` | Produce diagrams in the format CloudBSD law requires: Mermaid for architecture, flowcharts, sequence, state, class and ER diagrams; in-repo SVG for UI wireframes and mockups |
| `Effect`, `Effect v4`, `effect-smol`, `TypeScript service`, `Layer`, `Schema` | `platform/opencode/effect/SKILL.md` | Work with Effect v4 / effect-smol TypeScript code - services, layers, schemas, and the Effect idioms |
| `feature`, `task generation`, `task table`, `from inventory` | `planning/feature-task-generator/SKILL.md` | Turn a feature inventory produced by analysis into concrete implementation tasks |
| `file system`, `path`, `permission`, `file locking`, `extended attribute`, `xattr` | `analysis/os-analysis/file-system-analyzer/SKILL.md` | Document how an application uses the filesystem - paths, permissions, locking, extended attributes |
| `jail`, `iocage`, `bastille`, `pot`, `ezjail`, `isolation` | `freebsd-admin/jail-manager/SKILL.md` | Create and operate FreeBSD jails with jail(8), ezjail, iocage, bastille, or pot |
| `Linuxulator`, `Linux binary`, `/compat/linux`, `linux compat` | `freebsd-admin/linuxulator-runner/SKILL.md` | Run Linux binaries on FreeBSD through the Linuxulator compatibility layer |
| `map codebase`, `discovery`, `.discovery/`, `project structure`, `dependency map` | `analysis/codebase-mapper/SKILL.md` | Recursively map a whole codebase into exhaustive tree-view documents under .discovery/ |
| `message queue`, `broker`, `pub/sub`, `RabbitMQ`, `Kafka`, `MQTT`, `NATS`, `SQS`, `SNS`, `event stream` | `analysis/message-queue-analyzer/SKILL.md` | Document message brokers and event-driven architecture - queues, topics, pub/sub, delivery guarantees |
| `migrate`, `port`, `convert`, `legacy`, `DOS`, `Pascal`, `retro`, `modernise` | `migration/codebase-migrator/SKILL.md` | Migrate a legacy application to a modern platform and language - DOS, Pascal, old Unix, retro codebases moving to FreeBSD, Rust, Go, or TypeScript |
| `orchestrate`, `pre-planning`, `coordinate analysis`, `full analysis pass` | `analysis/source-analysis-orchestrator/SKILL.md` | Coordinate the whole pre-planning analysis pass by sequencing the individual analysis skills into one consolidated report |
| `plan`, `plan document`, `.plan/`, `initialize project`, `template` | `planning/plan-document-generator/SKILL.md` | Create .plan/ documents from the CloudBSD Planning standard templates |
| `PR`, `pull request`, `worktree`, `implement and PR`, `land this`, `merge` | `platform/opencode/work-with-pr/SKILL.md` | Carry implementation work through the full pull-request lifecycle: worktree, atomic commits, PR, CI and review gates, merge, cleanup |
| `pre-publish`, `release gate`, `npm publish`, `safe to publish`, `release review` | `platform/opencode/pre-publish-review/SKILL.md` | Multi-agent release gate that reviews everything changed since the last npm release before publishing |
| `privilege`, `UID`, `GID`, `capability`, `ACL`, `chroot`, `securelevel`, `Capsicum`, `least privilege` | `analysis/os-analysis/privilege-analyzer/SKILL.md` | Document what privileges an application actually needs - UID/GID, capabilities, ACLs, chroot, securelevel, Capsicum |
| `progress`, `tracker`, `TODO`, `phase progress` | `workflow/progress-tracker-updater/SKILL.md` | Create and update the TODO Tracker Summary tables that show phase progress across a project's plan |
| `quick reference`, `AGENTS.md section`, `cheat sheet` | `planning/quick-reference-generator/SKILL.md` | Write the Quick Reference section that sits at the top of an agent entry point document |
| `rc.d`, `rc script`, `startup script`, `PROVIDE`, `REQUIRE`, `rcvar` | `freebsd-admin/rc-script-writer/SKILL.md` | Write FreeBSD rc.d startup scripts that follow the conventions - PROVIDE/REQUIRE/KEYWORD, rcvar, pidfiles, and a reload that honours the SIGHUP contract |
| `release`, `package`, `pkgbase`, `install media`, `ISO`, `VM image`, `publish`, `repository catalog`, `build stamp` | `release/artifact-release/SKILL.md` | Build, verify, and publish binary artifacts - packages, kernels and modules, install media, VM images - so that what ships is what was tested |
| `reverse engineer`, `analyze source`, `dead code`, `actual behavior`, `before porting` | `analysis/reverse-engineer-for-port/SKILL.md` | Establish what code actually does before porting it, instead of trusting names and structure |
| `review`, `code review`, `check my work`, `lgtm`, `approve` | `workflow/review/SKILL.md` | Review code for correctness, security, and FreeBSD/CloudBSD conventions |
| `risk`, `risk register`, `700 document`, `threat` | `security/risk-assessor/SKILL.md` | Create and maintain a project risk register in the CloudBSD format |
| `scope`, `challenge plan`, `plan review`, `is this right`, `too big`, `effort estimate` | `planning/plan-ceo-review/SKILL.md` | Challenge the scope of a plan before anything gets built - is this the right problem, is it too big, is it too small, what would be cut |
| `security audit`, `vulnerability`, `OWASP`, `STRIDE`, `threat model`, `pen test` | `security/security-audit/SKILL.md` | Audit code or a design for vulnerabilities using OWASP Top 10 and STRIDE |
| `security document`, `access control`, `data protection`, `1.1-1.6` | `security/security-document-generator/SKILL.md` | Produce the CloudBSD security document series - threat model, access control, data protection, and the rest of the 1.1-1.6 set |
| `service`, `sysrc`, `rc.conf`, `enable at boot`, `reload`, `SIGHUP` | `freebsd-admin/service-manager/SKILL.md` | Operate FreeBSD services with service(8), sysrc, and rc.conf, including the SIGHUP validate-then-reload contract |
| `ship`, `deploy`, `release`, `publish`, `push to prod`, `cut a release` | `workflow/ship/SKILL.md` | Deploy only with the evidence CloudBSD law requires - tests, coverage, man page lint, PR, then deploy |
| `socket`, `TCP`, `UDP`, `epoll`, `kqueue`, `TLS`, `network stack` | `analysis/os-analysis/network-stack-analyzer/SKILL.md` | Document an application's networking - sockets, TCP/UDP, epoll/kqueue, TLS, DNS |
| `syscall`, `system call`, `file I/O`, `memory`, `signal`, `strace`, `truss`, `porting` | `analysis/os-analysis/system-call-analyzer/SKILL.md` | Document the system calls an application depends on and how they map across operating systems |
| `sysctl`, `MIB`, `kernel parameter`, `tunable`, `501 document` | `planning/sysctl-documenter/SKILL.md` | Document a sysctl MIB hierarchy in the standard CloudBSD format |
| `task`, `claim`, `complete`, `task table`, `status` | `workflow/task-workflow/SKILL.md` | Claim, work, and complete tasks under the CloudBSD Planning protocol, keeping task tables truthful when several agents share a plan |
| `test plan`, `test case matrix`, `401`, `402`, `1101`, `testing scope` | `testing/test-planner/SKILL.md` | Generate testing documentation - test case matrices, test plans, and testing scope documents (the 401, 402, and 1101 series) |
| `thread`, `process`, `IPC`, `synchronization`, `mutex`, `fork`, `concurrency` | `analysis/os-analysis/process-model-analyzer/SKILL.md` | Document processes, threads, IPC, and synchronisation in an application |
| `TOC`, `table of contents`, `000 document`, `index` | `planning/toc-generator/SKILL.md` | Generate and maintain the table-of-contents document that indexes a project's planning set |
| `triage`, `GitHub issue`, `GitHub PR`, `issue triage`, `read-only report` | `platform/opencode/github-triage/SKILL.md` | Read-only triage of open GitHub issues and pull requests, producing evidence-backed reports where every claim carries a permalink |
| `UI`, `UX`, `interface`, `wireframe`, `mockup`, `screen`, `form`, `data binding` | `analysis/ui-ux-analyzer/SKILL.md` | Turn an existing user interface into an implementation-ready specification - objects, states, actions, forms, data flow, SVG wireframes |
| `UI review`, `design review`, `agy`, `polish`, `copy review`, `accessibility review` | `quality/human-interface-review/SKILL.md` | Get a second opinion on anything a person looks at and uses - a web page, a TUI, a desktop window, navigation, user-facing copy, visual design - before shipping it |
| `validate plan`, `plan compliance`, `PR review`, `planning standard` | `planning/plan-validator/SKILL.md` | Check that .plan/ documents comply with the CloudBSD Planning standard - naming, structure, task tables, cross-references |
| `validation report`, `corrections`, `evidence record` | `testing/validation-document-generator/SKILL.md` | Write validation reports and validation corrections reports in the CloudBSD format |
| `ZFS`, `zpool`, `dataset`, `snapshot`, `zvol`, `destroy` | `freebsd-admin/zfs-manager/SKILL.md` | Manage ZFS pools, datasets, and snapshots on FreeBSD, with the safety rules that keep destructive commands from running by accident |

---

## By category

### `analysis/`

Understand code you did not write, before changing or porting it.

| Skill | Path | Use it when |
|---|---|---|
| **api-analyzer** | `analysis/api-analyzer/SKILL.md` | Use when analysing an API for porting, rewriting, or integration, when asked about REST, HTTP, endpoints, OpenAPI, GraphQL, gRPC, WebSockets, or SSE, or before writing a client against a service you did not build. |
| **code-quality-analyzer** | `analysis/code-quality-analyzer/SKILL.md` | Use when reviewing freshly ported or generated code, when the same logic appears in several places, or when asked to extract interfaces and abstractions before a codebase grows further. |
| **codebase** | `analysis/codebase/SKILL.md` | Use when asked to understand, explore, or map a project, to find where something is implemented, to trace a call path, or to answer "where is X" without changing any code. |
| **codebase-mapper** | `analysis/codebase-mapper/SKILL.md` | Use when starting on an unfamiliar or large project, when asked to map structure and dependencies, or when a port or migration needs a complete inventory before planning. |
| **message-queue-analyzer** | `analysis/message-queue-analyzer/SKILL.md` | Use when analysing RabbitMQ, Kafka, MQTT, NATS, AWS SQS or SNS, when tracing how events flow between services, or when planning an integration with a broker. |
| **reverse-engineer-for-port** | `analysis/reverse-engineer-for-port/SKILL.md` | Establish what code actually does before porting it, instead of trusting names and structure. Use at the start of any port or rewrite, when documenting an application you did not write, or when you need to separate live behaviour from dead code. |
| **source-analysis-orchestrator** | `analysis/source-analysis-orchestrator/SKILL.md` | Use when starting a new project or a port, before any plan documents are generated, so the plan reflects the real code rather than assumptions. |
| **ui-ux-analyzer** | `analysis/ui-ux-analyzer/SKILL.md` | Use when analysing an interface for reimplementation, when documenting screens and their behaviour, or when producing wireframes before building a UI. |

<details><summary>Reference files inside these skills</summary>

- `analysis/api-analyzer/` — `authentication.md`, `graphql-grpc.md`, `http-fundamentals.md`, `rest-endpoints.md`, `websockets.md`
- `analysis/codebase-mapper/` — `advanced.md`, `phases-0-1.md`, `phases-2-3.md`, `phases-4-5.md`
- `analysis/message-queue-analyzer/` — `integration.md`, `kafka.md`, `mqtt.md`, `nats.md`, `overview.md`, `patterns.md`, `rabbitmq.md`, `sqs-sns.md`
- `analysis/ui-ux-analyzer/` — `actions.md`, `data-flow.md`, `forms.md`, `objects.md`, `wireframing.md`

</details>

### `analysis/os-analysis/`

Operating-system dependencies, for cross-platform porting.

| Skill | Path | Use it when |
|---|---|---|
| **file-system-analyzer** | `analysis/os-analysis/file-system-analyzer/SKILL.md` | Use when porting software across operating systems, when hardcoded paths or permission assumptions need auditing, or when file locking behaves differently on the target. |
| **network-stack-analyzer** | `analysis/os-analysis/network-stack-analyzer/SKILL.md` | Use when porting network-heavy code to FreeBSD, when replacing epoll with kqueue, or when auditing how a service binds, listens, and encrypts. |
| **privilege-analyzer** | `analysis/os-analysis/privilege-analyzer/SKILL.md` | Use when porting privileged code, when applying least privilege to a service, or when deciding what a daemon may drop after start-up. |
| **process-model-analyzer** | `analysis/os-analysis/process-model-analyzer/SKILL.md` | Use when analysing concurrent or multi-process software, when porting fork/exec or threading code between operating systems, or when reasoning about pipes, shared memory, and locking. |
| **system-call-analyzer** | `analysis/os-analysis/system-call-analyzer/SKILL.md` | Use when porting low-level code to FreeBSD, when a Linux- only syscall must be replaced, or when analysing file I/O, memory, signals, or process syscalls. |

<details><summary>Reference files inside these skills</summary>

- `analysis/os-analysis/process-model-analyzer/` — `async.md`, `groups.md`, `ipc.md`, `overview.md`, `processes.md`, `synchronization.md`, `threads.md`
- `analysis/os-analysis/system-call-analyzer/` — `debugging.md`, `file-io.md`, `ipc.md`, `memory.md`, `network.md`, `overview.md`, `porting.md`, `process.md`, `signals.md`, `time.md`

</details>

### `diagramming/`

Producing diagrams in the formats CloudBSD law allows.

| Skill | Path | Use it when |
|---|---|---|
| **mermaid-diagrammer** | `diagramming/mermaid-diagrammer/SKILL.md` | Use whenever a diagram is being added or edited, and whenever ASCII-art, DOT, or PlantUML must be converted away. |

### `freebsd-admin/`

Running FreeBSD itself: VMs, jails, storage, services, safe deploys.

| Skill | Path | Use it when |
|---|---|---|
| **bhyve-manager** | `freebsd-admin/bhyve-manager/SKILL.md` | Use when setting up a VM, configuring bridge/tap networking or virtio storage, or building the isolated VM that kernel-level testing is required to run in. |
| **jail-manager** | `freebsd-admin/jail-manager/SKILL.md` | Use when building an isolated userland environment, when a service should be confined to a jail, or when setting up per-service isolation for testing. |
| **linuxulator-runner** | `freebsd-admin/linuxulator-runner/SKILL.md` | Use when a required tool ships only as a Linux binary, when validating that /compat/linux is set up correctly, or when deciding whether to run something natively instead. |
| **rc-script-writer** | `freebsd-admin/rc-script-writer/SKILL.md` | Use whenever a CloudBSD service needs to start at boot or be controlled with service(8). |
| **safe-kernel-deploy** | `freebsd-admin/safe-kernel-deploy/SKILL.md` | Use whenever booting a build that has not been proven on that machine, or when asked to deploy with automatic rollback, a one-shot boot environment, or a bectl-based upgrade. |
| **service-manager** | `freebsd-admin/service-manager/SKILL.md` | Use when enabling, starting, stopping, or reloading a service, when editing rc.conf, or when diagnosing a service that will not start. |
| **zfs-manager** | `freebsd-admin/zfs-manager/SKILL.md` | Use when creating storage for VMs or jails, taking or rolling back snapshots, or before running any zfs destroy or zpool destroy. |

### `migration/`

Moving a legacy application to a modern platform.

| Skill | Path | Use it when |
|---|---|---|
| **codebase-migrator** | `migration/codebase-migrator/SKILL.md` | Use when asked to port, convert, or modernise an old codebase, after the analysis skills have produced an inventory. |

### `planning/`

The .plan/ standard: creating, validating, and indexing plan documents.

| Skill | Path | Use it when |
|---|---|---|
| **agents-start-here-generator** | `planning/agents-start-here-generator/SKILL.md` | Use when initialising a new CloudBSD project or when an existing project has no agent entry point. Never generate AGENTS_START_HERE.md - that filename does not auto-load anywhere. |
| **feature-task-generator** | `planning/feature-task-generator/SKILL.md` | Turn a feature inventory produced by analysis into concrete implementation tasks. Use after reverse-engineering or source analysis, when planning a port, and specifically to avoid inventing tasks for functionality that is not actually reachable in the source. |
| **office-hours** | `planning/office-hours/SKILL.md` | Use when asked for advice, an opinion, a best practice, or "what should I do here" - and when a decision, not a survey, is what is wanted. |
| **plan-ceo-review** | `planning/plan-ceo-review/SKILL.md` | Use when a new feature or project is being planned, or when asked whether a plan is right- sized. |
| **plan-document-generator** | `planning/plan-document-generator/SKILL.md` | Use when initialising a project's .plan/ directory, when adding a numbered plan document, or when existing planning documents need to be brought onto the standard structure. |
| **plan-validator** | `planning/plan-validator/SKILL.md` | Check that .plan/ documents comply with the CloudBSD Planning standard - naming, structure, task tables, cross-references. Use on pull-request review, before committing planning changes, or when a project's plan directory has drifted. |
| **quick-reference-generator** | `planning/quick-reference-generator/SKILL.md` | Use when creating or refreshing AGENTS.md for a project, so an agent gets the critical commands and paths without reading everything. |
| **sysctl-documenter** | `planning/sysctl-documenter/SKILL.md` | Use when defining or describing kernel tunables and configuration interfaces exposed through sysctl, including the 501 series planning document. |
| **toc-generator** | `planning/toc-generator/SKILL.md` | Use when creating the 000 TOC document or when documents have been added or renumbered and the index no longer matches the tree. |

### `platform/cloudflare/`

Building and publishing on Cloudflare.

| Skill | Path | Use it when |
|---|---|---|
| **cloudflare-agents-sdk** | `platform/cloudflare/cloudflare-agents-sdk/SKILL.md` | Use when creating stateful agents, durable workflows, real-time WebSocket applications, or scheduled tasks on Workers. |
| **cloudflare-platform** | `platform/cloudflare/cloudflare-platform/SKILL.md` | Choose the right Cloudflare product and understand how it fits together - Workers, Pages, KV, D1, R2, Queues, Workers AI, Vectorize, Tunnel, WAF, and the Terraform/Pulumi providers. Use for any Cloudflare development or deployment task, and to decide which product a requirement calls for. DNS records for CloudBSD domains follow the rules in dns-records.md alongside this file. |

<details><summary>Reference files inside these skills</summary>

- `platform/cloudflare/cloudflare-platform/` — `dns-records.md`

</details>

### `platform/opencode/`

Workflows driven through the opencode tooling.

| Skill | Path | Use it when |
|---|---|---|
| **effect** | `platform/opencode/effect/SKILL.md` | Use when editing or reviewing TypeScript that imports Effect, or when asked how to model an operation as an Effect. |
| **github-triage** | `platform/opencode/github-triage/SKILL.md` | Use when asked to triage issues or PRs. It never comments, labels, closes, or merges - it only reports. |
| **pre-publish-review** | `platform/opencode/pre-publish-review/SKILL.md` | Multi-agent release gate that reviews everything changed since the last npm release before publishing. Use before every npm publish, and whenever asked "is this safe to publish", "ready to release", or for a pre-release review. |
| **work-with-pr** | `platform/opencode/work-with-pr/SKILL.md` | Use when asked to create a PR, implement an issue end to end, or land a change as a PR. |

### `quality/`

Standing review disciplines, for code and for interfaces.

| Skill | Path | Use it when |
|---|---|---|
| **code-craft** | `quality/code-craft/SKILL.md` | Apply the enduring lessons of the Gang of Four "Design Patterns" and Knuth's "The Art of Computer Programming" to code you write, refactor, or review. Use at the start of any non-trivial code change and again as a checklist before finishing, and in every code review. Not for one-line edits or config tweaks. |
| **human-interface-review** | `quality/human-interface-review/SKILL.md` | Use when a deliverable is an interface rather than internals, and pair it with code-craft, which covers the code behind the interface. |

### `release/`

Turning a verified change into a published artifact.

| Skill | Path | Use it when |
|---|---|---|
| **artifact-release** | `release/artifact-release/SKILL.md` | Use when cutting a release, producing installable media, publishing a package repository, or deciding whether an artifact is fit to publish. Complements the ship skill, which gates the change; this gates the artifact. |

### `security/`

Risk, audit, and the security document series.

| Skill | Path | Use it when |
|---|---|---|
| **risk-assessor** | `security/risk-assessor/SKILL.md` | Use when writing the 700-series risk document, during a risk review, or when a design decision introduces a risk that must be recorded and tracked. |
| **security-audit** | `security/security-audit/SKILL.md` | Use when asked for a security audit or threat model, before shipping anything that handles authentication, secrets, or untrusted input, and when reviewing code that crosses a trust boundary. |
| **security-document-generator** | `security/security-document-generator/SKILL.md` | Use when a project needs its security documentation created or brought up to the standard. |

### `testing/`

Planning tests and recording the evidence they produce.

| Skill | Path | Use it when |
|---|---|---|
| **test-planner** | `testing/test-planner/SKILL.md` | Use when planning how a feature will be proven, before implementation starts, so the evidence requirement is defined up front. |
| **validation-document-generator** | `testing/validation-document-generator/SKILL.md` | Use when an implementation task has been checked and the result must be recorded as evidence, or when a previous validation was wrong and needs correcting. |

### `workflow/`

Day-to-day development: tasks, debugging, review, shipping.

| Skill | Path | Use it when |
|---|---|---|
| **build-status-updater** | `workflow/build-status-updater/SKILL.md` | Use when a build result changes, when CI is added or reconfigured, or when the recorded status no longer matches reality. |
| **investigate** | `workflow/investigate/SKILL.md` | Use when debugging a failure, when asked why something is broken, when tracing an error, and specifically when the obvious explanation has already turned out to be wrong. |
| **progress-tracker-updater** | `workflow/progress-tracker-updater/SKILL.md` | Use when tasks change state, when a phase completes, or when the tracker has drifted from the task tables it summarises. |
| **review** | `workflow/review/SKILL.md` | Use when reviewing a pull request or a diff, when asked to check work before it lands, and before approving anything that touches configuration, privilege, or persistence. |
| **ship** | `workflow/ship/SKILL.md` | Use when asked to ship, release, publish, or push to production, and to stop a release that has no captured evidence behind it. |
| **task-workflow** | `workflow/task-workflow/SKILL.md` | Use when picking up a task, marking one done, or resolving a task table that two agents have edited. |

---

## How to use this index

```
1. Match the task against the trigger index above.
2. Read that one SKILL.md.
3. Follow its links to reference files only if it tells you to.
```

The law itself is in [`AGENTS.md`](../AGENTS.md); a skill explains *how* to
carry out a rule and links to it rather than restating it. If a skill and
`AGENTS.md` ever disagree, `AGENTS.md` wins and the skill is the defect.
