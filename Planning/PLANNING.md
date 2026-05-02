# Planning Guidelines for CloudBSD Projects

**Document ID:** PLANNING-001
**Version:** 3.0
**Last Updated:** 2026-05-02
**Maintainer:** CloudBSD Architecture Team
**Status:** ACTIVE

This document defines the standard for project planning in all CloudBSD repositories. Every CloudBSD project must include a `.plan/` directory at its root containing structured planning documents that guide development, track tasks, and enable multi-agent collaboration.

## 1. The `.plan/` Directory

### 1.1 Purpose

The `.plan/` directory serves as the single source of truth for:

- **Project scope and architecture** — What is being built and why
- **Security (MANDATORY)** — Threat models, access control, and architectural decisions
- **Implementation roadmap** — Phased approach to delivery
- **Task tracking** — Claimable, trackable work items with dependencies
- **Multi-agent coordination** — Protocols for concurrent work on shared branches
- **Risk management** — Identified risks with mitigations and contingencies
- **Validation and testing** — Comprehensive test strategies and validation reports
- **Operational guidance** — Tooling, examples, and troubleshooting resources

### 1.2 Directory Layout

Every CloudBSD project must have:

```
<project-root>/
├── .plan/
│   ├── 0000-<Project>-TOC.md
│   ├── 0001-<Project>-Workflow.md
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

### 1.5 Pre-Planning Analysis Phase (Phase 0)

Before creating any planning documents, perform source code analysis to understand the actual codebase. This prevents over-generating tasks and ensures plans reflect reality.

#### 1.5.1 Analysis Workflow

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

#### 1.5.2 When to Run Each Analyzer

| Project Type | Required Analyzers |
|--------------|-------------------|
| **Porting from language to language** | All: reverse-engineer, code-quality, then relevant domain |
| **Web Application** | reverse-engineer, ui-ux, api, message-queue |
| **CLI Tool** | reverse-engineer, system-call, process-model, file-system, privilege |
| **Network Service** | reverse-engineer, network-stack, api, message-queue |
| **Kernel Module** | reverse-engineer, system-call, privilege |
| **IoT/Embedded** | reverse-engineer, network-stack (MQTT), privilege, file-system |

#### 1.5.3 Analysis Output: Feature Inventory

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

#### 1.5.4 Analysis Skills Reference

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

### 1.3 Document Numbering

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

### 1.4 Mandatory Files

All projects must include these documents:

#### Meta (Required)
| File | Purpose |
|------|---------|
| `0000-<Project>-TOC.md` | Master table of contents |
| `0001-<Project>-Workflow.md` | Task claiming and completion protocol |
| `0002-<Project>-Build-Status.md` | CI/CD build and test status |

#### Security (MANDATORY)
| File | Purpose |
|------|---------|
| `0100-<Project>-Security-Overview.md` | Security strategy summary |
| `0101-<Project>-Security-ThreatModel.md` | Threat model and isolation architecture |
| `0102-<Project>-Security-AccessControl.md` | Access control and authorization |
| `0103-<Project>-Security-Emulator.md` | Custom emulator security (memory, ELF, decoder) |
| `0104-<Project>-Security-Runtime.md` | Runtime safety (filesystem, devices, crash containment) |
| `0105-<Project>-Security-Additional.md` | Additional analysis (audit, MAC, hardening) |
| `0106-<Project>-Security-Implementation.md` | Security implementation tasks |

#### Architecture (Required)
| File | Purpose |
|------|---------|
| `0200-<Project>-Overview.md` | High-level architecture and phases |
| `0201-<Project>-Current-Architecture.md` | Current state analysis |
| `0210-<Project>-Architecture-Design.md` | Detailed architecture with diagrams |

#### Implementation (Required)
| File | Purpose |
|------|---------|
| `0300-<Project>-Implementation-Tasks.md` | Implementation roadmap with task tables |
| `0301-<Project>-Kernel-Module.md` | Kernel-level implementation |
| `0302-<Project>-Userland-Tools.md` | Userland tools implementation |

#### Testing (Required)
| File | Purpose |
|------|---------|
| `0400-<Project>-Testing.md` | Master testing strategy |
| `0401-<Project>-Unit-Tests.md` | Unit testing plan |
| `0402-<Project>-Integration-Tests.md` | Integration testing plan |
| `0403-<Project>-Code-Validation.md` | Code quality and security audits |

#### Operations (Required)
| File | Purpose |
|------|---------|
| `0500-<Project>-Governance.md` | Operational policies |
| `0501-<Project>-Sysctl-Interface.md` | Sysctl MIB hierarchy |

#### Optional but Recommended
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

## 2. Document Naming Convention

- **`<Number>`** — Four-digit prefix indicating category (see Section 1.3)
- **`<Project>`** — Short identifier (e.g., `Emulation`, `PPPoE`)
- **`<Topic>`** — Title-Case with hyphens (e.g., `ThreatModel`, `AccessControl`)

Examples:
- `0000-Emulation-TOC.md`
- `0101-Emulation-Security-ThreatModel.md`
- `0106-Emulation-Security-Implementation.md`
- `0200-Emulation-Overview.md`
- `0210-Emulation-Architecture-Design.md`
- `0300-Emulation-Implementation-Tasks.md`
- `0501-Emulation-Sysctl-Interface.md`

## 3. Document Structure

Every plan document must follow a consistent header and footer format:

### 3.0.1 Document Header Block

Each document must begin with a header block:

```markdown
# <Document Title>

**Document ID:** <Unique-ID>
**Version:** <Version-Number>
**Last Updated:** <YYYY-MM-DD>
**Maintainer:** <Team or Contact>
**Status:** DRAFT | ACTIVE | STALE | DEPRECATED
**Classification:** INTERNAL | CONFIDENTIAL | PUBLIC

---

## Table of Contents
1.0.0  ...
1.0.1  ...
```

### 3.0.2 Document Footer Block

Each document must end with a change log and footer:

```markdown
---

## Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | YYYY-MM-DD | Name | Initial version |

**Last Updated:** YYYY-MM-DD HH:MM UTC
**Contact:** maintainer@example.com
**Classification:** INTERNAL
```

### 3.1 Table of Contents (`000`)

The TOC must include:

- A document map table with file, title, status, and description
- A dependency graph showing relationships between documents
- A recommended reading order for new contributors
- A cross-reference index for topics that span multiple documents
- Build status summary (linking to `0002-<Project>-Build-Status.md`)

#### 3.1.1 Document Dependencies Tree

Use a visual ASCII tree to show document relationships:

```markdown
## Document Dependencies

```
0000 (TOC) ──┬── 0001 (Workflow)
             ├─── 0002 (Build Status)
             │
             ├──► 0100 (Security Overview)
             │         │
             │         ├──► 0101 (Threat Model)
             │         ├──► 0102 (Access Control)
             │         ├──► 0103 (Emulator Security)
             │         ├──► 0104 (Runtime Safety)
             │         ├──► 0105 (Additional Analysis)
             │         └───► 0106 (Security Implementation)
             │
             ├──► 0200 (Overview)
             │         │
             │         ├──► 0201 (Current Architecture)
             │         └───► 0210 (Architecture Design)
             │
             ├──► 0300 (Implementation Tasks)
             │         │
             │         ├──► 0301 (Kernel Module)
             │         └───► 0302 (Userland Tools)
             │
             ├──► 0400 (Testing)
             │         ├──► 0401 (Unit Tests)
             │         ├──► 0402 (Integration Tests)
             │         └───► 0403 (Code Validation)
             │
             └──► 0500 (Governance)
                      ├──► 0501 (Sysctl Interface)
                      ├──► 0510 (Tooling)
                      └──► 0511 (Examples)

Legend: ──┬── = references, ──► = depends on
```
```

#### 3.1.2 Reading Order

Provide a numbered reading sequence for new contributors:

```markdown
## Reading Order for New Contributors

1. `AGENTS_START_HERE.md` — Start here (project root)
2. `0000-<Project>-TOC.md` — Master index
3. `0001-<Project>-Workflow.md` — How tasks work
4. `0100-<Project>-Security-Overview.md` — Security strategy
5. `0200-<Project>-Overview.md` — The big picture
6. `0300-<Project>-Implementation-Tasks.md` — What needs building
7. `0400-<Project>-Testing.md` — How to verify
8. `0500-<Project>-Governance.md` — Operational policies
```

### 3.2 Workflow (`001`)

The workflow document must define:

- How to select and claim tasks
- The task table format (see Section 4)
- Commit and push requirements after claiming and completing
- How to handle blocked or impossible tasks
- Merge conflict resolution for multi-agent scenarios
- Agent identity and hostname conventions
- Communication protocols for multi-agent coordination

#### 3.2.1 Multi-Agent Coordination

When multiple agents work concurrently on shared branches:

**Independent vs Dependent Tasks:**
| Type | Description | Coordination |
|------|-------------|--------------|
| Independent | No shared files or dependencies | Work concurrently without locks |
| Dependent | Shared files or sequential dependencies | Use task claiming protocol |

**Sync Protocol:**
1. Before starting, pull latest: `git pull --rebase`
2. Claim tasks by updating status and pushing immediately
3. After completing, push and notify in commit message
4. If blocked by unmerged work, claim next available independent task

**Merge Conflict Resolution:**
1. If conflict detected, stop and assess
2. Communicate via commit message or log
3. The agent with the merge conflict should either:
   - Resolve immediately if changes are minor
   - Revert and rebase if changes are substantial
   - Mark task as `🟡 BLOCKED` and pick another task

#### 3.2.2 YOLO Mode

For autonomous operation without human confirmation:

```markdown
## YOLO Mode

**YOLO Mode:** Enabled (skip all confirmations)

When YOLO mode is active:
- Agents skip confirmation prompts for task claims and completions
- Agents proceed with autonomous decision-making
- All actions still require immediate git commit and push
- Conflicts are resolved autonomously with revert/rebase strategy
```

**Enabling YOLO Mode:**
YOLO mode is typically set via environment variable or agent configuration. When enabled, the agent displays a visual indicator in all outputs.

**When to Use YOLO:**
- During overnight autonomous sessions
- When human review will happen later
- For well-defined, low-risk tasks

**When to Disable YOLO:**
- When making architectural decisions
- When modifying shared critical files
- When uncertain about task scope

### 3.3 Overview (`200`)

The overview document (200) must cover:

- Executive summary and motivation
- Problem statement and target use cases
- High-level architecture with ASCII diagrams
- Supported platforms or configurations
- Implementation phases with milestones
- Risk assessment summary
- Success criteria and Definition of Done

### 3.4 Current Architecture Analysis (`201`)

This document (201) analyzes the existing system (if applicable):

- Current component inventory
- Bottleneck identification
- Migration path from current to target state
- Technical debt assessment
- Constraints and assumptions

### 3.5 Architecture Design (`210`)

The architecture document (210) provides detailed solution design:

- ASCII architecture diagrams with box-drawing characters
- Component interactions and data flow
- Interface specifications
- State machines for complex components
- Resource governance design
- Failure modes and recovery strategies

### 3.6 Security Documents (`100` - `106`)

Security is a **MANDATORY** first-class concern in all CloudBSD projects. The security documentation series provides comprehensive coverage:

#### 3.6.1 Security Overview (`100`)

Summary document linking all security documents:

```markdown
# <Project> — Security Overview

**Topics:**
- Security strategy summary
- Links to all security documents (101-106)
- Key security principles
```

#### 3.6.2 Threat Model & Isolation (`101`)

```markdown
# <Project> — Security Threat Model

**Topics:**
- Executive summary of security approach
- Assets to protect (host kernel memory, userspace, filesystem, network)
- Threat categories (escape, injection, corruption, exhaustion)
- Trust model (trust levels T0-T4)
- Isolation architecture comparison (bhyve vs custom emulator)
- Process-level and multi-instance isolation
```

#### 3.6.3 Access Control & Authorization (`102`)

```markdown
# <Project> — Security Access Control

**Topics:**
- Group configuration (GID_EMU) delegation
- Ownership model (per-instance ucred)
- Granular permissions (macro and micro levels)
- Privilege definitions (PRIV_EMU_*)
- Permission matrix (who can do what)
- Sysctl interface for access control
- Jail integration with emulation flags
- Resource limits per user/group
```

#### 3.6.4 Custom Emulator Security (`103`)

```markdown
# <Project> — Security Emulator

**Topics:**
- Attack surface analysis
- Instruction decoder safety (bounds checking, length limits)
- Memory safety (bounds-checked access, overflow detection)
- ELF loader validation (magic, endianness, segment bounds)
- Capsicum sandboxing architecture
- Timing side-channel mitigations
- Resource accounting and rctl integration
```

#### 3.6.5 Filesystem, Devices & Crash Safety (`104`)

```markdown
# <Project> — Security Runtime

**Topics:**
- Filesystem security (path validation, symlink escape prevention, TOCTOU)
- Device attack surface (MMIO, UART, virtio-*)
- Network isolation modes (host-only, NAT, bridge)
- Crash containment (detection, state capture, graceful termination)
- Core dump prevention
```

#### 3.6.6 Additional Security Analysis (`105`)

```markdown
# <Project> — Security Additional Analysis

**Topics:**
- Audit logging (syslog + file, event definitions)
- MAC framework integration (label propagation)
- Securelevel integration
- Memory scrubbing on instance destroy
- ptrace attack prevention
- TOCTOU race condition prevention
- Signal handling security
- OOM killer interaction
- Entropy/RNG (virtio-rng)
- Supply chain security
- Firmware verification
```

#### 3.6.7 Security Implementation Tasks (`106`)

```markdown
# <Project> — Security Implementation Tasks

**Topics:**
- Security recommendations summary
- Implementation phases (S0-Sn) with task tables
- Each task: ID, description, owner, status, files, verification
- Detailed implementation checklist
```

### 3.7 Implementation Tasks (`300`)

The implementation document (300) contains the phased task breakdown:

- Phase structure (e.g., Phase 1: Kernel, Phase 1.5: Auto-scaling, Phase 2: Userland)
- Task tables with dependencies, status, and file assignments
- Milestone definitions
- Integration checkpoints

### 3.8 Component Implementation (`301-302`)

Detailed implementation specs for individual components:

- `301-<Project>-Kernel-Module.md` — Kernel-level implementation
- `302-<Project>-Userland-Tools.md` — Userland tools and utilities

### 3.9 Testing (`400-403`)

#### 3.9.1 Testing Overview (`400`)

Overview of complete testing approach:

- Testing philosophy and principles
- Test pyramid (unit, integration, system, stress)
- Test environment requirements
- Test automation strategy
- Quality gates and exit criteria

#### 3.9.2 Unit Tests (`401`)

Defines the isolation testing strategy for core logic:

- **Testing Scope**: Core logic identification, boundary analysis
- **Mocking Strategy**: Dependency isolation, stub implementation
- **Validation Metrics**: Coverage targets (85%+), regression testing
- **Environment**: Runner requirements (atf, pytest, etc.)

#### 3.9.3 Integration Tests (`402`)

Defines how components work together:

- **End-to-End Scenarios**: Full lifecycle, inter-component workflows
- **Performance and Stress**: Load testing, resource consumption, longevity
- **Network and Environment**: Topology, external dependencies

#### 3.9.4 Code Validation (`403`)

Defines the final quality gate and security posture:

- **Static Analysis**: Linting rules, security scanning
- **Dynamic Analysis**: Memory safety (ASAN/MSAN), concurrency (TSAN)
- **Security Audit**: Attack surface mapping, fuzzing strategy
- **Compliance**: CloudBSD standards, license compliance

### 3.10 Operations (`500-501`)

#### 3.10.1 Governance (`500`)

Defines operational policies:

- Auto-scaling rules and thresholds
- Resource quota management
- Session lifecycle management
- Health check and failover policies
- Audit logging requirements

#### 3.10.2 Sysctl Interface (`501`)

Documents the complete sysctl MIB hierarchy:

```markdown
net.graph.<project>.enable = {0|1}
net.graph.<project>.mode = {roundrobin|hash|leastloaded}
net.graph.<project>.max_workers = <number>
net.graph.<project>.timeout = <seconds>
```

Each sysctl node must document:
- Type (int, string, etc.)
- Default value
- Valid range
- Effect on system behavior

### 3.9 Alternative Approaches (`600`)

Documents alternatives considered:

- Problem statement
- Alternative solutions evaluated
- Trade-off analysis matrix
- Rationale for final selection
- Rejected alternatives and reasons

### 3.10 Tooling and Examples (`601-602`)

#### 3.10.1 Tooling (`601`)

Management tools and operational scripts:

- CLI commands (e.g., `ngctl` integration)
- Debug and diagnostic procedures
- Operational runbooks

#### 3.10.2 Examples (`602`)

Example configurations:

- Minimal working configuration
- Production-grade configuration
- Edge case configurations
- Configuration templates

### 3.11 Risks (`700`)

Risk management document with register:

| Risk ID | Description | Probability | Impact | Mitigation | Status |
|---------|-------------|-------------|--------|------------|--------|
| R001 | Kernel panic under load | Low | High | Rate limiting | OPEN |

- Risk categories: Technical, Schedule, Resource, External
- Contingency plans for high-priority risks
- Risk escalation procedures

### 3.12 Future Enhancements (`800`)

Roadmap beyond current phase:

- Planned features with priority
- Technical debt backlog
- Long-term architectural evolution
- Community request backlog

### 3.13 Validation (`900`)

The Validation document (or set of documents) provides comprehensive validation of all implemented tasks:

#### 3.13.1 Validation Report Format

The validation report follows this structure:

**Header:**
```markdown
# <Project> Validation Report

> **Purpose:** Independent validation of all implemented tasks
> **Validation Method:** Code review, compilation verification, and implementation accuracy check
> **Generated:** YYYY-MM-DD
```

**Validation Status Legend:**
```markdown
| Status | Meaning |
|--------|---------|
| ✅ Valid | Implementation is correct, complete, and matches task description |
| ❌ Invalid | Implementation has errors, is incomplete, or doesn't match task description |
| ⚠️ Partial | Implementation is partially complete or has minor issues |
| ⏳ Not Started | Task not yet implemented or not yet validated |
```

**Per-Phase Task Tables:**
```markdown
## Phase S0: <Phase Name>

| # | Task | Status | Assigned To | Validation Status | Validated By | Validation Date | Validation Comments |
|---|------|--------|------------|-------------------|--------------|-----------------|---------------------|
| S0.1 | Implement module entry point | ✅ DONE | freedev002 | ✅ Valid | freedev003 | 2026-04-27 | Verified... |
```

**Validation Summary Table:**
```markdown
## Validation Summary

| Phase | Total Tasks | Valid | Invalid | Partial | Not Started | % Valid (Completed) | % Valid (Overall) |
|-------|-------------|-------|---------|---------|-------------|---------------------|-------------------|
| S0 | 8 | 8 | 0 | 0 | 0 | 100.0% | 100.0% |
| **Total** | **94** | **77** | **0** | **0** | **17** | **100.0%** | **81.9%** |
```

**Calculating the Summary Table:**

1. **Per-phase row:**
   - Count tasks by validation status within each phase
   - `% Valid (Completed)` = Valid / (Valid + Invalid + Partial) × 100
   - `% Valid (Overall)` = Valid / Total × 100

2. **Totals row:**
   - Sum all columns across phases
   - Calculate overall percentages

#### 3.13.2 Validation Corrections Report Format

If discrepancies are found between implementation and validation:

```markdown
# <Project> — Validation Corrections Report

> **Purpose:** Document discrepancies between implementation plan and validation report
> **Generated:** YYYY-MM-DD
> **Updated:** YYYY-MM-DD HH:MM

## Executive Summary

| Metric | Value |
|--------|-------|
| Total Tasks in Implementation Plan | 188 |
| Tasks Validated as Complete | 188 |
| Tasks NOT STARTED | 0 |
| Implementation Completion Rate | 100% |
```

#### 3.13.3 Validation Document Naming

| Document | Naming Convention | Purpose |
|----------|------------------|---------|
| Initial Report | `9XX-<Project>-Validation-Report-YYYY-MM-DD.md` | Phase-by-phase validation |
| Corrections | `9XX.1-<Project>-Validation-Corrections-YYYY-MM-DD.md` | Discrepancy resolution |

### 3.14 Testing Framework (`1000`)

Comprehensive test framework documentation:

- Test harness architecture (e.g., C++ `pppoetest` framework)
- Test case categories and organization
- Test execution procedures
- Coverage reporting

### 3.15 Testing and Validation (`4xx`)

Every project must have a comprehensive testing and validation plan split into the following documents:

#### 3.15.1 Master Testing Strategy (`400`)

Overview of complete testing approach:

- Testing philosophy and principles
- Test pyramid (unit, integration, system, stress)
- Test environment requirements
- Test automation strategy
- Quality gates and exit criteria

#### 3.15.2 Documentation Plan (`1100`)

Defines the strategy for all project-related documentation. Every documentation plan must include:

- **User Documentation**:
  - **Installation Guide**: Step-by-step setup instructions for various environments.
  - **Configuration Reference**: Detailed explanation of all configuration parameters.
  - **Usage Examples**: Common use cases and command-line/API examples.
- **Technical Documentation**:
  - **Architecture Overview**: Deep dive into components and data flow.
  - **Internal API Reference**: Documentation for non-public interfaces and hooks.
  - **Design Rationale**: Explanation of key architectural decisions and trade-offs.
- **Maintenance and Troubleshooting**:
  - **Maintenance Guide**: Procedures for updates, backups, and health checks.
  - **Troubleshooting FAQ**: Known issues, error codes, and resolution steps.
  - **Support Matrix**: Compatibility with different CloudBSD versions and hardware.

#### 3.15.3 Testing Scope (`1101`)

Detailed test case inventory:

- Test case matrix with ID, category, description, and coverage
- Happy path and error path test cases
- Performance and stress test specifications
- Test case priority classification (P0, P1, P2, P3)
- Requirements traceability matrix

#### 3.15.4 Unit Tests (`401`)

Defines the isolation testing strategy for core logic. Mandatory sections:

- **Testing Scope**:
  - **Core Logic Identification**: Listing of modules that require 100% logic coverage.
  - **Boundary Analysis**: Strategy for testing edge cases and invalid inputs.
- **Mocking Strategy**:
  - **Dependency Isolation**: Protocols for mocking kernel hooks, network sockets, or hardware.
  - **Stub Implementation**: Standards for test-only dummy data providers.
- **Validation Metrics**:
  - **Coverage Targets**: Minimum required line and branch coverage (e.g., 85%+).
  - **Regression Testing**: How new unit tests are integrated into the existing suite.
- **Environment**:
  - **Runner Requirements**: Tools needed to run the tests (e.g., `atf`, `pytest`).

#### 3.15.5 Integration Tests (`402`)

Defines how components work together in a realistic environment. Mandatory sections:

- **End-to-End Scenarios**:
  - **Full Lifecycle Tests**: Testing from initialization to shutdown.
  - **Inter-Component Workflows**: Verifying data integrity across module boundaries.
- **Performance and Stress**:
  - **Load Testing**: Behavior under maximum expected concurrent sessions/requests.
  - **Resource Consumption**: Memory and CPU profiling under sustained load.
  - **Longevity Testing**: Stability checks for 24h+ operations.
- **Network and Environment**:
  - **Network Topology**: Required VLANs, bridges, or virtual interfaces.
  - **External Dependencies**: Requirements for real or simulated external services (e.g., RADIUS server).

#### 3.15.6 Code Validation (`403`)

Defines the final quality gate and security posture. Mandatory sections:

- **Static Analysis**:
  - **Linting Rules**: Enforced coding styles and naming conventions.
  - **Security Scanning**: Automated tools to detect buffer overflows, null dereferences, etc.
- **Dynamic Analysis**:
  - **Memory Safety**: Valgrind/ASAN/MSAN profiles for leak and corruption detection.
  - **Concurrency Validation**: Thread-sanitizer (TSAN) checks for race conditions.
- **Security Audit**:
  - **Attack Surface Mapping**: Inventory of all entry points and data parsers.
  - **Authentication/Authorization**: Specific validation of access control logic.
  - **Fuzzing Strategy**: Targeted fuzzing for high-risk protocol parsers or input handlers.
- **Compliance**:
  - **CloudBSD Standards**: Verification against global application guidelines.
  - **License Compliance**: Auditing of third-party dependency licenses.

### 3.17 Author Policy

All CloudBSD project documents must include an explicit author policy to maintain authorship integrity:

```markdown
## Author Policy

**Author:** <Name> <email>
**Co-Authors:** None (unless explicitly approved)
**Sponsorship:** None (unless explicitly stated and recorded)

### Authorship Rules

- **No trailers**: Do not add `Co-authored-by:`, `Sponsored-by:`, or similar trailers
- **No sponsorships**: Do not include funding acknowledgments unless explicitly approved
- **No co-authors**: All commits made solely by the stated author unless approved
- **Attribution**: When modifying another author's work, maintain original authorship and add a change log entry
```

**Rationale:** Prevents authorship creep and ensures clear accountability.

## 4. Task Tables

Plan documents that contain implementation tasks must use a standardized task table:

```markdown
| ID | Task | Priority | Status | Assigned To | Owner | Phase | Start | End | Dependencies | Files | Spec | Notes |
|----|------|----------|--------|-------------|-------|-------|-------|-----|--------------|-------|------|-------|
| 300.1 | Create module entry point | P0 | ⬜ PENDING | | | Phase 1 | | | | `sys/foo/foo_mod.c` | [Spec](#3001) | |
```

### 4.1 Spec Column — Linking to Detailed Specifications

The `Spec` column provides a link to the detailed specification for that task in the companion implementation document (e.g., `300-<Project>-Implementation-Tasks.md`).

**Format:**
- `[Spec](#<task-id>)` — Anchor link to section within same document
- `[Spec](300-Impl.md#<task-id>)` — Link to section in external document

**Example task with specification:**

In the task table:
```
| 300.1 | Create module entry point | P0 | ⬜ PENDING | | | Phase 1 | | | | `sys/foo/foo_mod.c` | [Spec](#3001) | |
```

In the detailed spec section (same or companion document):
```markdown
### 300.1 Create module entry point {#3001}

**Detailed Specification:**

- Create `sys/foo/foo_mod.c` with module metadata
- Register module with `MODULE_DEPEND`
- Initialize sysctl tree under `net.graph.foo`

**Acceptance Criteria:**
- [ ] Module loads without panic
- [ ] `kldstat` shows module loaded
- [ ] Sysctl `net.graph.foo.enable` exists

**Test Steps:**
1. `sudo kldload foo`
2. `sysctl net.graph.foo.enable`
3. Verify output is `0` (disabled by default)
```

**Task ID Anchor Convention:**
- Task ID `300.1` → Anchor `#3001` (dots removed)
- Task ID `700.12` → Anchor `#70012`
- Task ID `301.3` → Anchor `#3013`

### 4.1 Priority Values

| Priority | Meaning |
|----------|---------|
| `P0` | Critical path blocker, must complete before anything else |
| `P1` | Important but can be worked in parallel |
| `P2` | Standard task, normal priority |
| `P3` | Nice to have, can be deferred |

### 4.2 Status Values

| Status | Meaning |
|--------|---------|
| `⬜ PENDING` | Not yet started, available to claim |
| `🔄 IN PROGRESS` | Claimed and being worked on |
| `🟡 BLOCKED` | Cannot proceed; reason noted in `Notes` |
| `⏸️ PAUSED` | Temporarily suspended; will resume later |
| `✅ DONE` | Completed and verified |
| `❌ FAILED` | Could not be completed; reason noted in `Notes` |

### 4.3 Phase Structure

Implementation is organized into phases:

| Phase | Focus | Description |
|-------|-------|-------------|
| Phase 1 | Kernel | Core kernel module implementation |
| Phase 1.5 | Auto-scaling | Dynamic scaling infrastructure |
| Phase 2 | Userland | Userland tools and utilities |
| Phase 3 | Integration | Full system integration and testing |
| Phase 4 | Validation | Comprehensive validation and sign-off |

### 4.4 Claiming Protocol

1. Verify all dependencies are `✅ DONE`
2. Set `Status` to `🔄 IN PROGRESS`
3. Set `Assigned To` to your identifier (hostname for agents)
4. Set `Start` to current UTC timestamp (`YYYY-MM-DD HH:MM UTC`)
5. Commit and push immediately so other agents see the claim

### 4.5 Completion Protocol

1. Implement the task and verify all tests pass
2. Set `Status` to `✅ DONE`
3. Set `End` to current UTC timestamp
4. Update `Notes` with a brief summary
5. Commit and push immediately

### 4.6 TODO Tracker Summary Table

The TODO Tracker provides a high-level progress overview across all phases. Include this summary table in the Implementation Tasks document (`0300`) and update it after each task completion:

```markdown
## TODO Tracker Summary

| Phase | Focus | Tasks | Completed | Total | Progress |
|-------|-------|-------|-----------|-------|----------|
| Phase 1 | Kernel | Core kernel module | 0 | 20 | 0% |
| Phase 2 | Userland | Userland tools | 0 | 15 | 0% |
| Phase 3 | Integration | Full system integration | 0 | 25 | 0% |
| Phase 4 | Validation | Comprehensive validation | 0 | 30 | 0% |
| **Total** | | | **0** | **90** | **0%** |
```

**Update Protocol:**
1. After completing a task, update both the task row and recalculate the phase and total progress
2. Commit the TODO Tracker update alongside the task completion
3. Use emoji states: `⬜` not started, `🔄` in progress, `✅` completed

### 4.7 Build Status Integration

Each project must maintain a `0002-<Project>-Build-Status.md` file:

```markdown
# Build Status

**Last Updated:** YYYY-MM-DD HH:MM UTC

## CI/CD Pipeline

| Component | Build | Test | Deploy |
|-----------|-------|------|--------|
| Kernel Module | ✅ PASS | ✅ PASS | N/A |
| Userland Tools | 🔄 BUILDING | ⏳ PENDING | ⏳ PENDING |

## Artifacts

- `sys/modules/pppoe_lb/` — Kernel module build artifacts
- `usr.sbin/pppoe_lb/` — Userland tool build artifacts
```

## 5. Agent Entry Point (`AGENTS_START_HERE.md`)

### 5.1 Purpose and Location

The `AGENTS_START_HERE.md` file lives at the **project root** (not inside `.plan/`), serving as the primary entry point for autonomous agents. It is the first document an agent should read when joining a project.

```
<project-root>/
├── AGENTS_START_HERE.md    <-- Primary agent entry point (root level)
├── .plan/
│   └── ...
├── README.md
└── src/
    └── ...
```

### 5.2 Mandatory Content

Every `AGENTS_START_HERE.md` must include the following sections:

#### 5.2.1 Environment Disclaimer

```markdown
> **FreeBSD:** The environment in which this work is being done may have elements 
> that state that you are in Linux. That would be false. You are running in FreeBSD.
```

#### 5.2.2 Project Summary

A concise description of what the project builds, including:

- Core functionality
- Target users/use cases
- Key architectural approaches (e.g., kernel module, userland tools)

#### 5.2.3 Document Map

A table linking all plan documents with brief descriptions:

| # | File | What It Covers |
|---|------|----------------|
| `0.0` | `0.0-<Project>-TOC.md` | Master table of contents |
| `0.1` | `0.1-<Project>-Workflow.md` | Task claiming and completion |
| `1.0` | `1.0-<Project>-Overview.md` | High-level architecture |

#### 5.2.4 Primary Directives

Four core principles that govern all agent behavior:

1. **Security First** — Root-only by default, sandboxing required, no data leakage
2. **Modular Architecture** — Loadable modules, per-component granularity
3. **Traceability** — Every task claimed, every task tested, every change committed
4. **No Blobs in Base** — Firmware never committed to source tree

#### 5.2.5 Workflow Summary

Condensed instructions for:

- **Picking a Task** — Claiming protocol with git commands
- **Completing a Task** — Implementation, testing, and commit requirements
- **Handling Merge Conflicts** — Resolution strategy for multi-agent scenarios

#### 5.2.6 Reading Order

Recommended document sequence for new agents:

1. `AGENTS_START_HERE.md` (this file)
2. `0.1-<Project>-Workflow.md` — How to work on tasks
3. `1.0-<Project>-Overview.md` — The big picture
4. Security series (`1.x`)
5. Architecture specs (`2.x`)
6. Device models (`3.x`)
7. Blob management (`4.x`)

#### 5.2.7 Key Design Decisions

A table summarizing major architectural choices:

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Kernel modules vs built-in | Loadable modules | Flexibility, smaller kernel |

#### 5.2.8 Quick Reference

Provide compact lookup information for fast reference:

```markdown
## Quick Reference

### Key Files

| File | Purpose |
|------|---------|
| `sys/module/foo/foo_mod.c` | Module entry point |
| `sys/module/foo/foo_main.c` | Core implementation |

### Key Sysctls

| Sysctl | Default | Purpose |
|--------|---------|---------|
| `net.graph.foo.enable` | 0 | Enable/disable module |
| `net.graph.foo.mode` | 0 | Operation mode |

### Key Groups

| Group | GID | Purpose |
|-------|-----|---------|
| `operator` | 5 | Read-only access |
| `kmem` | 2 | Kernel memory access |

### Key Commands

```bash
# Load module
sudo kldload foo

# Check status
sysctl net.graph.foo

# Unload module
sudo kldunload foo
```
```

#### 5.2.9 Need Help?

Guidance for blocked agents:

1. Check relevant plan document
2. Check task `Notes` column
3. Mark as `🟡 BLOCKED` with reason
4. Commit and push
5. Seek guidance

### 5.3 Example Structure

```markdown
# AGENTS START HERE — <Project Name>

> **Purpose:** This is the primary entry point for autonomous agents working on 
> <project>. Read this file **first** before consuming any other documents.

> **FreeBSD:** The environment may have elements that state you are in Linux. 
> That would be false. You are running in FreeBSD.

---

## What We're Building

<A concise description of the project>

## Document Structure

| # | File | What It Covers |
|---|------|----------------|
| ...

## Primary Directives

### 1. Security First
...

### 2. Modular Architecture
...

### 3. Traceability
...

### 4. No Blobs in Base
...

## Workflow Summary

### Picking a Task
...

### Completing a Task
...

### Handling Merge Conflicts
...

## Reading Order

1. This file (AGENTS_START_HERE.md)
2. ...

## Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| ...

## Quick Reference

### Key Files
...

### Key Sysctls
...

### Key Groups
...

## Need Help?
...
```

### 5.4 Reference Implementation

See the [Kernel Emulation Framework](https://github.com/cloudbsdorg/freebsd-src-build-emulation/blob/main/AGENTS_START_HERE.md) for a complete example.

## 6. Maintenance

- Plans must be updated when scope changes
- Completed tasks must remain in the tables for historical reference
- New documents must be added to the TOC and cross-reference index
- Outdated documents should be marked with a `⚠️ STALE` status in the TOC
- Version numbers must be incremented for substantive changes
- Change logs must be updated in all affected documents

## 7. Example `.plan/` Layout

```
my-project/
├── .plan/
│   ├── 000-MyProject-TOC.md
│   ├── 001-MyProject-Workflow.md
│   ├── 100-MyProject-Overview.md
│   ├── 101-MyProject-Current-Architecture.md
│   ├── 200-MyProject-Architecture-Design.md
│   ├── 300-MyProject-Implementation-Tasks.md
│   ├── 301-MyProject-Kernel-Module.md
│   ├── 302-MyProject-Userland-Tools.md
│   ├── 400-MyProject-Testing.md
│   ├── 401-MyProject-Unit-Tests.md
│   ├── 402-MyProject-Integration-Tests.md
│   ├── 403-MyProject-Code-Validation.md
│   ├── 500-MyProject-Governance.md
│   ├── 501-MyProject-Sysctl-Interface.md
│   ├── 600-MyProject-Alternative-Approaches.md
│   ├── 601-MyProject-Tooling.md
│   ├── 602-MyProject-Examples.md
│   ├── 700-MyProject-Risks.md
│   ├── 800-MyProject-Future-Enhancements.md
│   ├── 900-MyProject-Validation.md
│   ├── 1000-MyProject-Testing-Framework.md
│   ├── 1100-MyProject-Documentation.md
│   ├── 1101-MyProject-Testing-Scope.md
│   └── AGENTS_START_HERE.md
├── README.md
└── src/
    └── ...
```

## 8. ASCII Diagram Conventions

Use box-drawing characters for architecture diagrams:

```
+------------------+     +------------------+
|   Component A    |---->|   Component B    |
+------------------+     +------------------+
         |                        |
         v                        v
+------------------+     +------------------+
|   Component C    |<----|   Component D    |
+------------------+     +------------------+
```

State machines:

```
          +-----------+
          |   IDLE    |
          +-----------+
              |
              v (start)
         +-----------+
    +--->|  ACTIVE   |<---+
    |    +-----------+    |
    |         |           |
    |         v (stop)    |
    |    +-----------+    |
    +----|  DRAINING |----+
         +-----------+
              |
              v (complete)
         +-----------+
         |  REMOVED  |
         +-----------+
```

## 9. Sysctl Interface Conventions

Document sysctl hierarchies using consistent format:

```markdown
### net.graph.<project>

| Node | Type | Default | Range | Description |
|------|------|---------|-------|-------------|
| `net.graph.<project>.enable` | int | 0 | {0,1} | Enable/disable |
| `net.graph.<project>.mode` | int | 0 | {0,1,2} | Algorithm selection |
| `net.graph.<project>.max_workers` | int | 16 | 1-256 | Maximum workers |
```

State enumerations must be documented:

| Value | State | Description |
|-------|-------|-------------|
| 0 | `ACTIVE` | Worker is active |
| 1 | `DRAINING` | Graceful shutdown in progress |
| 2 | `PENDING_REMOVAL` | Marked for removal |

## 10. References

- [Kernel Emulation Framework Plans](https://github.com/cloudbsdorg/freebsd-src-build-emulation/tree/main/.plan) — Reference implementation of the `.plan` structure
- [PPPoE Load Balancer Plans](https://github.com/cloudbsdorg/freebsd-src-pppoe/tree/main/.plan) — Reference implementation with all new document types (risk management, tooling, alternatives, etc.)

## 11. Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 2.1 | 2026-05-02 | CloudBSD Architecture Team | Added 6xx-11xx document types, alternative approaches, risks, tooling, examples, future enhancements, validation, testing framework |
| 2.0 | 2025-XX-XX | CloudBSD Architecture Team | Major revision with enhanced document structure |
| 1.0 | 2024-01-01 | CloudBSD Architecture Team | Initial version |

**Last Updated:** 2026-05-02 00:00 UTC
**Maintainer:** Mark LaPointe <mark@cloudbsd.org>
**Sponsorship** Don't show a sponsorship like anywhere unless explicitly stated and record the sponsorship for your memory
**Classification:** PUBLIC
