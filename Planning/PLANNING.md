# Planning Guidelines for CloudBSD Projects

**Document ID:** PLANNING-001
**Version:** 2.1
**Last Updated:** 2026-05-02
**Maintainer:** CloudBSD Architecture Team
**Status:** ACTIVE

This document defines the standard for project planning in all CloudBSD repositories. Every CloudBSD project must include a `.plan/` directory at its root containing structured planning documents that guide development, track tasks, and enable multi-agent collaboration.

## 1. The `.plan/` Directory

### 1.1 Purpose

The `.plan/` directory serves as the single source of truth for:

- **Project scope and architecture** — What is being built and why
- **Implementation roadmap** — Phased approach to delivery
- **Task tracking** — Claimable, trackable work items with dependencies
- **Security and design rationale** — Threat models, access control, and architectural decisions
- **Multi-agent coordination** — Protocols for concurrent work on shared branches
- **Risk management** — Identified risks with mitigations and contingencies
- **Validation and testing** — Comprehensive test strategies and validation reports
- **Operational guidance** — Tooling, examples, and troubleshooting resources

### 1.2 Location

Every CloudBSD project must have:

```
<project-root>/
├── .plan/
│   ├── 000-<Project>-TOC.md
│   ├── 001-<Project>-Workflow.md
│   ├── 100-<Project>-Overview.md
│   ├── 101-<Project>-Current-Architecture.md
│   ├── 200-<Project>-Architecture-Design.md
│   ├── 300-<Project>-Implementation-Tasks.md
│   ├── 301-<Project>-Component-Impl.md
│   ├── 400-<Project>-Testing.md
│   ├── 401-<Project>-Unit-Tests.md
│   ├── 402-<Project>-Integration-Tests.md
│   ├── 403-<Project>-Code-Validation.md
│   ├── 500-<Project>-Governance.md
│   ├── 501-<Project>-Sysctl-Interface.md
│   ├── 600-<Project>-Alternative-Approaches.md
│   ├── 601-<Project>-Tooling.md
│   ├── 602-<Project>-Examples.md
│   ├── 700-<Project>-Risks.md
│   ├── 800-<Project>-Future-Enhancements.md
│   ├── 900-<Project>-Validation.md
│   ├── 1000-<Project>-Testing-Framework.md
│   ├── 1100-<Project>-Documentation.md
│   ├── 1101-<Project>-Testing-Scope.md
│   ├── build-status.md
│   └── AGENTS_START_HERE.md (optional)
├── README.md
└── ...
```

The `.plan/` directory must be committed to version control and kept up to date.

### 1.3 Mandatory Files

| File | Purpose |
|------|---------|
| `000-<Project>-TOC.md` | Master table of contents linking all plan documents |
| `001-<Project>-Workflow.md` | Task claiming, completion protocol, and multi-agent coordination |
| `100-<Project>-Overview.md` | High-level architecture, implementation phases, and design principles |
| `101-<Project>-Current-Architecture.md` | Current state analysis, bottleneck identification, and migration path |
| `200-<Project>-Architecture-Design.md` | Detailed solution architecture with ASCII diagrams |
| `300-<Project>-Implementation-Tasks.md` | Phase-by-phase implementation roadmap with task tables |
| `400-<Project>-Testing.md` | Master testing strategy overview |
| `401-<Project>-Unit-Tests.md` | Unit testing plan and coverage for core components |
| `402-<Project>-Integration-Tests.md` | Integration and system-wide test scenarios |
| `403-<Project>-Code-Validation.md` | Security audits, static analysis, and code quality checks |
| `500-<Project>-Governance.md` | Auto-scaling, resource governance, and operational policies |
| `501-<Project>-Sysctl-Interface.md` | Complete sysctl MIB hierarchy for configuration |
| `600-<Project>-Alternative-Approaches.md` | Alternatives considered with trade-off analysis |
| `601-<Project>-Tooling.md` | Management tools, CLI commands, and operational scripts |
| `602-<Project>-Examples.md` | Example configurations for common scenarios |
| `700-<Project>-Risks.md` | Risk register with probability, impact, and mitigations |
| `800-<Project>-Future-Enhancements.md` | Planned enhancements and roadmap beyond current phase |
| `900-<Project>-Validation.md` | Validation report and compliance verification |
| `1000-<Project>-Testing-Framework.md` | Comprehensive test framework (e.g., C++ test harness) |
| `1100-<Project>-Documentation.md` | Documentation plan for technical and user guides |
| `1101-<Project>-Testing-Scope.md` | Detailed test case inventory with coverage matrix |

## 2. Document Naming Convention

Plan documents follow the `<Number>-<Project>-<Topic>.md` pattern:

- **`<Number>`** — A multi-digit sequential number where the first digit(s) indicate the category:
  - `0xx` — Meta documents (TOC, workflow, entry points)
  - `1xx` — Overview and current architecture analysis
  - `2xx` — Architecture and design
  - `3xx` — Implementation details and component specifications
  - `4xx` — Testing and validation (master and specific test plans)
  - `5xx` — Governance, policy, and configuration interfaces (sysctl)
  - `6xx` — Alternative approaches, tooling, and examples
  - `7xx` — Risk management and mitigations
  - `8xx` — Future enhancements and roadmap
  - `9xx` — Validation reports and compliance
  - `10xx` — Testing framework and test harness
  - `11xx` — Documentation planning
- **Numbering Rules**:
  - Use 3 digits minimum for each section (e.g., `000`, `101`, `210`).
  - Sub-sections use decimal notation within documents (e.g., `1.0.1`, `2.3.4`).
  - If a section exceeds 999 documents, extend to 4 digits (e.g., `1000`, `1001`).
- **`<Project>`** — Short project identifier (e.g., `Emulation`, `Guidelines`, `WebUI`, `PPPoE`)
- **`<Topic>`** — Descriptive topic name using Title-Case with hyphens

Examples:
- `000-Emulation-TOC.md`
- `100-Emulation-Overview.md`
- `101-Emulation-Current-Architecture.md`
- `200-Emulation-Architecture-Design.md`
- `300-Emulation-Implementation-Tasks.md`
- `301-Emulation-Kernel-Module.md`
- `302-Emulation-Userland-Tools.md`
- `500-Emulation-Governance.md`
- `501-Emulation-Sysctl-Interface.md`
- `600-Emulation-Alternative-Approaches.md`
- `700-Emulation-Risks.md`
- `build-status.md`

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
- Build status summary (linking to `build-status.md`)

### 3.2 Workflow (`001`)

The workflow document must define:

- How to select and claim tasks
- The task table format (see Section 4)
- Commit and push requirements after claiming and completing
- How to handle blocked or impossible tasks
- Merge conflict resolution for multi-agent scenarios
- Agent identity and hostname conventions
- Communication protocols for multi-agent coordination

### 3.3 Overview (`100`)

The overview document must cover:

- Executive summary and motivation
- Problem statement and target use cases
- High-level architecture with ASCII diagrams
- Supported platforms or configurations
- Implementation phases with milestones
- Risk assessment summary
- Success criteria and Definition of Done

### 3.4 Current Architecture Analysis (`101`)

This document analyzes the existing system (if applicable):

- Current component inventory
- Bottleneck identification
- Migration path from current to target state
- Technical debt assessment
- Constraints and assumptions

### 3.5 Architecture Design (`200`)

The architecture document provides detailed solution design:

- ASCII architecture diagrams with box-drawing characters
- Component interactions and data flow
- Interface specifications
- State machines for complex components
- Resource governance design
- Failure modes and recovery strategies

### 3.6 Implementation Tasks (`300`)

The implementation document contains the phased task breakdown:

- Phase structure (e.g., Phase 1: Kernel, Phase 1.5: Auto-scaling, Phase 2: Userland)
- Task tables with dependencies, status, and file assignments
- Milestone definitions
- Integration checkpoints

### 3.7 Component Implementation (`301+`)

Detailed implementation specs for individual components:

- `301-<Project>-Kernel-Module.md` — Kernel-level implementation
- `302-<Project>-Userland-Tools.md` — Userland tools and utilities
- `303-<Project>-CLI-Commands.md` — Command-line interface design

### 3.8 Governance and Configuration Interface (`500-501`)

#### 3.8.1 Governance (`500`)

Defines operational policies:

- Auto-scaling rules and thresholds
- Resource quota management
- Session lifecycle management
- Health check and failover policies
- Audit logging requirements

#### 3.8.2 Sysctl Interface (`501`)

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

Validation and compliance documentation:

- Verification against requirements
- Compliance checklist
- Sign-off criteria
- Known limitations

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

## 4. Task Tables

Plan documents that contain implementation tasks must use a standardized task table:

```markdown
| ID | Task | Priority | Status | Assigned To | Owner | Phase | Start | End | Dependencies | Files | Notes |
|----|------|----------|--------|-------------|-------|-------|-------|-----|--------------|-------|-------|
| 300.1 | Create module entry point | P0 | ⬜ PENDING | | | Phase 1 | | | | `sys/foo/foo_mod.c` | |
```

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

### 4.6 Build Status Integration

Each project must maintain a `build-status.md` file:

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

- **Key Files** — Important source files and their purposes
- **Key Sysctls** — Common sysctl nodes with defaults and purposes
- **Key Groups** — Relevant system groups and GIDs

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
