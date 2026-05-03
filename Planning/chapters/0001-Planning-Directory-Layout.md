# Chapter 1: The `.plan/` Directory

**Document ID:** PLANNING-001-01
**Chapter:** 1 of 10
**Last Updated:** 2026-05-02

---

## 1.1 Purpose

The `.plan/` directory serves as the single source of truth for:

- **Project scope and architecture** — What is being built and why
- **Security (MANDATORY)** — Threat models, access control, and architectural decisions
- **Implementation roadmap** — Phased approach to delivery
- **Task tracking** — Claimable, trackable work items with dependencies
- **Multi-agent coordination** — Protocols for concurrent work on shared branches
- **Risk management** — Identified risks with mitigations and contingencies
- **Validation and testing** — Comprehensive test strategies and validation reports
- **Operational guidance** — Tooling, examples, and troubleshooting resources

## 1.2 Directory Layout

Every CloudBSD project must have:

```
<project-root>/
├── .plan/
│   ├── 0000-<Project>-TOC.md
│   ├── 0001-<Project>-Workflow.md
│   ├── 0002-<Project>-Build-Status.md
│   ├── 0100-<Project>-Security-Overview.md
│   ├── 0101-<Project>-Security-ThreatModel.md
│   ├── 0102-<Project>-Security-AccessControl.md
│   ├── 0103-<Project>-Security-Emulator.md
│   ├── 0104-<Project>-Security-Runtime.md
│   ├── 0105-<Project>-Security-Additional.md
│   ├── 0106-<Project>-Security-Implementation.md
│   ├── 0200-<Project>-Overview.md
│   ├── 0201-<Project>-Current-Architecture.md
│   ├── 0210-<Project>-Architecture-Design.md
│   ├── 0300-<Project>-Implementation-Tasks.md
│   ├── 0301-<Project>-Kernel-Module.md
│   ├── 0302-<Project>-Userland-Tools.md
│   ├── 0400-<Project>-Testing.md
│   ├── 0401-<Project>-Unit-Tests.md
│   ├── 0402-<Project>-Integration-Tests.md
│   ├── 0403-<Project>-Code-Validation.md
│   ├── 0500-<Project>-Governance.md
│   ├── 0501-<Project>-Sysctl-Interface.md
│   ├── 0510-<Project>-Tooling.md
│   ├── 0511-<Project>-Examples.md
│   ├── 0600-<Project>-Alternative-Approaches.md
│   ├── 0700-<Project>-Risks.md
│   ├── 0800-<Project>-Future-Enhancements.md
│   ├── 0900-<Project>-Validation.md
│   ├── 1000-<Project>-Testing-Framework.md
│   ├── 1100-<Project>-Documentation.md
│   ├── 1101-<Project>-Testing-Scope.md
│   └── AGENTS_START_HERE.md (optional)
├── README.md
└── ...
```

The `.plan/` directory must be committed to version control and kept up to date.

## 1.3 Document Numbering

Plan documents follow the `<Number>-<Project>-<Topic>.md` pattern:

| Prefix | Category | Description |
|--------|----------|-------------|
| `0xxx` | Meta | TOC, workflow, entry points |
| `1xxx` | **Security (MANDATORY)** | Threat model, access control, emulator security, runtime safety |
| `2xxx` | Overview & Architecture | High-level architecture, current state, design |
| `3xxx` | Implementation | Tasks, component specs |
| `4xxx` | Testing | Unit, integration, validation |
| `5xxx` | Operations | Governance, sysctls, tooling, examples |
| `6xxx` | Alternatives | Alternatives considered, trade-offs |
| `7xxx` | Risks | Risk register and mitigations |
| `8xxx` | Future | Roadmap, enhancements |
| `9xxx` | Validation | Validation reports |
| `10xx` | Testing Framework | Test harness documentation |
| `11xx` | Documentation | Documentation planning |

**Numbering Rules:**
- Use 4 digits for all document numbers (e.g., `0000`, `0100`, `0210`)
- Sub-sections use decimal notation within documents (e.g., `1.0.1`, `2.3.4`)
- The first digit indicates the major category, remaining digits for sequence

## 1.4 Mandatory Files

All projects must include these documents:

### Meta (Required)
| File | Purpose |
|------|---------|
| `0000-<Project>-TOC.md` | Master table of contents |
| `0001-<Project>-Workflow.md` | Task claiming and completion protocol |
| `0002-<Project>-Build-Status.md` | CI/CD build and test status |

### Security (MANDATORY)
| File | Purpose |
|------|---------|
| `0100-<Project>-Security-Overview.md` | Security strategy summary |
| `0101-<Project>-Security-ThreatModel.md` | Threat model and isolation architecture |
| `0102-<Project>-Security-AccessControl.md` | Access control and authorization |
| `0103-<Project>-Security-Emulator.md` | Custom emulator security (memory, ELF, decoder) |
| `0104-<Project>-Security-Runtime.md` | Runtime safety (filesystem, devices, crash containment) |
| `0105-<Project>-Security-Additional.md` | Additional analysis (audit, MAC, hardening) |
| `0106-<Project>-Security-Implementation.md` | Security implementation tasks |

### Architecture (Required)
| File | Purpose |
|------|---------|
| `0200-<Project>-Overview.md` | High-level architecture and phases |
| `0201-<Project>-Current-Architecture.md` | Current state analysis |
| `0210-<Project>-Architecture-Design.md` | Detailed architecture with diagrams |

### Implementation (Required)
| File | Purpose |
|------|---------|
| `0300-<Project>-Implementation-Tasks.md` | Implementation roadmap with task tables |
| `0301-<Project>-Kernel-Module.md` | Kernel-level implementation |
| `0302-<Project>-Userland-Tools.md` | Userland tools implementation |

### Testing (Required)
| File | Purpose |
|------|---------|
| `0400-<Project>-Testing.md` | Master testing strategy |
| `0401-<Project>-Unit-Tests.md` | Unit testing plan |
| `0402-<Project>-Integration-Tests.md` | Integration testing plan |
| `0403-<Project>-Code-Validation.md` | Code quality and security audits |

### Operations (Required)
| File | Purpose |
|------|---------|
| `0500-<Project>-Governance.md` | Operational policies |
| `0501-<Project>-Sysctl-Interface.md` | Sysctl MIB hierarchy |

### Optional but Recommended
| File | Purpose |
|------|---------|
| `0510-<Project>-Tooling.md` | Management tools and CLI |
| `0511-<Project>-Examples.md` | Example configurations |
| `0600-<Project>-Alternative-Approaches.md` | Alternatives considered |
| `0700-<Project>-Risks.md` | Risk register |
| `0800-<Project>-Future-Enhancements.md` | Roadmap beyond current phase |
| `0900-<Project>-Validation.md` | Validation reports |
| `1000-<Project>-Testing-Framework.md` | Test framework (e.g., C++ harness) |
| `1100-<Project>-Documentation.md` | Documentation plan |
| `1101-<Project>-Testing-Scope.md` | Detailed test case inventory |
| `AGENTS_START_HERE.md` | Agent entry point (project root) |

---

## 1.5 Pre-Planning Analysis Phase (Phase 0)

Before creating any planning documents, perform source code analysis to understand the actual codebase. This prevents over-generating tasks and ensures plans reflect reality.

### 1.5.1 Analysis Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Phase 0: Source Analysis                            │
│                                                                      │
│  Step 1: Load reverse-engineer-for-port                               │
│           → Trace entry points                                        │
│           → Find dead code                                           │
│           → Classify components                                       │
│           → Output: Feature Inventory with Evidence                   │
│                                                                      │
│  Step 2: Load domain-specific analyzers (as applicable)              │
│           ├── ui-ux-analyzer → UI object inventory                  │
│           ├── api-analyzer → API endpoint inventory                 │
│           ├── message-queue-analyzer → Queue/broker inventory       │
│           └── (OS skills if low-level)                              │
│                                                                      │
│  Step 3: Load code-quality-analyzer                                  │
│           → Identify duplication and interface opportunities          │
│           → Output: Refactoring Backlog                              │
│                                                                      │
│  Step 4: Generate Feature Inventory Report                           │
│           → Consolidate all findings                                 │
│           → Document porting complexity                              │
│           → Identify platform-specific code                          │
└─────────────────────────────────────────────────────────────────────┘
```

### 1.5.2 When to Run Each Analyzer

| Project Type | Required Analyzers |
|--------------|-------------------|
| **Porting from language to language** | All: reverse-engineer, code-quality, then relevant domain |
| **Web Application** | reverse-engineer, ui-ux, api, message-queue |
| **CLI Tool** | reverse-engineer, system-call, process-model, file-system, privilege |
| **Network Service** | reverse-engineer, network-stack, api, message-queue |
| **Kernel Module** | reverse-engineer, system-call, privilege |
| **IoT/Embedded** | reverse-engineer, network-stack (MQTT), privilege, file-system |

### 1.5.3 Analysis Output: Feature Inventory

The Feature Inventory is the key output of Phase 0:

```markdown
# Feature Inventory: <Project>

## Summary
- Total features found: 12
- Actual CLI commands: 3 (not 15)
- Actual API endpoints: 8 (not 50)
- Dead code identified: 35%
- Estimated porting effort: Medium

## Actual Features (vs Assumed)

| Feature | Type | Evidence | Portability |
|---------|------|----------|-------------|
| start command | CLI | main.go:42, cobra AddCommand | Portable |
| Token validation | Core | auth.go:15, HMAC-SHA256 | Portable |
| /health endpoint | API | server.go:50, JSON response | Portable |
| O_DIRECT usage | File I/O | cache.c:30 | Linux only |
| epoll_wait | Network | net.c:42 | Linux only |
| Custom allocator | Memory | mem.c:20 | Complex |

## Dead Code (Will Not Port)

| Code | Location | Reason |
|------|----------|--------|
| LDAP auth | auth_ldap.go | Not used - dead import |
| XML parser | xml.c | Not called from any path |
| Legacy config | config_old.go | Superseded by config.go |

## Component Role Classification

| File | Name Implies | Actual Role | Response Type |
|------|--------------|-------------|---------------|
| server.go | HTTP server | API only | JSON (no HTML) |
| auth.go | Full auth | Token validation only | N/A |
| users.go | User management | Read-only list | JSON |

## Task Generation Input

From this inventory, generate tasks that:
- Match actual features (not assumed)
- Group by workflow
- Skip dead code
- Note platform-specific items
```

### 1.5.4 Analysis Skills Reference

| Skill | Purpose | Output |
|-------|---------|--------|
| reverse-engineer-for-port | Trace entry points, find dead code | Feature Inventory |
| ui-ux-analyzer | Document UI objects and states | UI Component Map |
| api-analyzer | Map REST endpoints and auth | API Specification |
| message-queue-analyzer | Document queues and brokers | Queue Architecture |
| system-call-analyzer | Analyze syscall usage | Syscall Map |
| process-model-analyzer | Document threads and IPC | Process Architecture |
| network-stack-analyzer | Map sockets and protocols | Network Architecture |
| file-system-analyzer | Document paths and permissions | File System Map |
| privilege-analyzer | Document UID/GID and capabilities | Privilege Requirements |
| code-quality-analyzer | Find duplication and interfaces | Refactoring Backlog |