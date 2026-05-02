# Skill: source-analysis-orchestrator

**Purpose:** Coordinate pre-planning source code analysis by sequencing and invoking appropriate analysis skills, producing a consolidated report that feeds into task and document generation.

**Triggers:** When starting a new porting project, planning implementation from existing codebase, or needing comprehensive code analysis before planning.

## Loading Instructions

Load this skill when the user asks you to:
- Analyze an existing codebase before planning
- Start a porting project
- Generate tasks from existing source code
- Understand a foreign codebase quickly

## Core Principle

> **Analyze before planning. Know what exists before deciding what to build.**

Never generate implementation tasks without first analyzing what the code actually does.

---

## 1. Analysis Workflow

### 1.1 When to Run This Skill

```markdown
## Prerequisites

This skill should be run BEFORE:
- plan-document-generator
- feature-task-generator
- Any implementation planning

This skill produces:
- Feature Inventory (from reverse-engineer-for-port)
- UI Object Inventory (from ui-ux-analyzer)
- API Inventory (from api-analyzer)
- Queue Inventory (from message-queue-analyzer)
- OS Dependency Report (from relevant OS skills)
- Refactoring Backlog (from code-quality-analyzer)
```

### 1.2 Analysis Sequence

```
┌─────────────────────────────────────────────────────────────────────┐
│                     ANALYSIS PHASE                                    │
│                                                                      │
│  Step 1: Project Triage                                             │
│  ┌───────────────────────────────────────────────────────────────┐   │
│  │ Load: reverse-engineer-for-port                              │   │
│  │   → Identify project type (CLI, API, Web, Service, Library) │   │
│  │   → Determine which skills to load next                       │   │
│  └───────────────────────────────────────────────────────────────┘   │
│                              │                                        │
│                              ▼                                        │
│  Step 2: Core Analysis (always run)                                 │
│  ┌───────────────────────────────────────────────────────────────┐   │
│  │ Load: system-call-analyzer                                    │   │
│  │ Load: process-model-analyzer                                 │   │
│  │ Load: file-system-analyzer                                   │   │
│  │ Load: privilege-analyzer (if privileged)                     │   │
│  └───────────────────────────────────────────────────────────────┘   │
│                              │                                        │
│                              ▼                                        │
│  Step 3: Domain Analysis (based on project type)                    │
│  ┌───────────────────────────────────────────────────────────────┐   │
│  │ Network Service/API → Load: network-stack-analyzer            │   │
│  │ Web Application    → Load: ui-ux-analyzer                     │   │
│  │                   → Load: api-analyzer                        │   │
│  │ Message Queue App  → Load: message-queue-analyzer             │   │
│  │ Database App       → Load: database-analyzer (future)         │   │
│  └───────────────────────────────────────────────────────────────┘   │
│                              │                                        │
│                              ▼                                        │
│  Step 4: Quality Analysis                                           │
│  ┌───────────────────────────────────────────────────────────────┐   │
│  │ Load: code-quality-analyzer                                    │   │
│  │   → Identify duplication and refactoring opportunities         │   │
│  └───────────────────────────────────────────────────────────────┘   │
│                              │                                        │
│                              ▼                                        │
│  Step 5: Consolidate                                               │
│  ┌───────────────────────────────────────────────────────────────┐   │
│  │ Create: Analysis Report (this document)                       │   │
│  │ Create: Feature Inventory with evidence                        │   │
│  │ Create: Task Recommendations                                   │   │
│  └───────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. Step 1: Project Triage

### 2.1 Project Type Detection

```markdown
## Project Type Indicators

| Indicator | Type | Skills to Load |
|----------|------|----------------|
| `main()` with flags/args | CLI Tool | system-call, process, file, privilege |
| HTTP handlers, REST/GraphQL | API Service | network-stack, api |
| HTML templates, React/Vue | Web App | ui-ux, api |
| Queue publishers/consumers | Message Queue App | message-queue |
| Database ORM, SQL queries | Data App | database-analyzer (future) |
| Kernel modules, syscalls | Kernel/Driver | system-call, privilege |
| .proto files | gRPC Service | network-stack, api |
| MQTTsubscribe/publish | IoT | network-stack, mqtt |
```

### 2.2 Triage Template

```markdown
## Project Triage

### Project: <Name>
### Source Language: <Lang>
### Target Language: <Lang>

### Detected Type: [CLI | API | Web | Service | Library | Kernel]
### Confidence: [High | Medium | Low]

### Evidence:
| File Pattern | Count | Interpretation |
|-------------|-------|---------------|
| `main.go` | 1 | Entry point found |
| `handler*.go` | 12 | HTTP handlers |
| `*.html` | 45 | Web UI |

### Recommended Analysis Path:
1. [First skill to load]
2. [Second skill to load]
3. ...
```

---

## 3. Step 2: Core Analysis

### 3.1 System Call Analysis

```markdown
## System Call Summary

### Critical Syscalls Used
| Call | Count | Purpose | Portability |
|------|-------|---------|-------------|
| read | 45 | File I/O | Portable |
| write | 38 | File I/O | Portable |
| epoll_create | 5 | Event loop | Linux only |
| getuid | 12 | Privilege check | Portable |
| mmap | 8 | Memory mapping | Mostly portable |

### OS-Specific Code Found
| Location | Feature | Impact |
|----------|---------|--------|
| event_linux.c:42 | epoll | Must use libevent |
| sys_freebsd.c:15 | kqueue | Must use libevent |
| priv_bsd.c:20 | setkey() | Remove or replace |
```

### Portability Assessment
| Category | Status | Action Required |
|----------|--------|----------------|
| File I/O | ✅ Portable | None |
| Memory | ⚠️ Mostly | Remove O_DIRECT |
| Network | ⚠️ Linux-specific | Use libevent |
| Process | ✅ Portable | None |
```

### 3.2 Process Model Summary

```markdown
## Process Architecture

### Threading Model
| Pattern | Count | Location | Portability |
|---------|-------|----------|-------------|
| pthreads | 8 | thread.c | Portable |
| goroutines | 45 | handler.go | Go-specific |
| async/await | 12 | client.go | Native only |

### IPC Mechanisms
| Mechanism | Usage | Between | Portability |
|----------|-------|---------|-------------|
| pipes | 4 | main→workers | Portable |
| Unix sockets | 2 | main→logger | POSIX |
| message queues | 1 | main→workers | POSIX |

### Synchronization
| Primitive | Count | Location |
|----------|-------|----------|
| mutex | 15 | various |
| condition variable | 8 | queue.c |
| semaphore | 2 | sync.c |
```

### 3.3 File System Summary

```markdown
## File System Dependencies

### Paths Used
| Path | Access | Purpose | Portability |
|------|--------|---------|-------------|
| /etc/app.conf | R | Config | Linux/BSD |
| /var/log/app.log | W | Logging | Linux/BSD |
| /tmp | RW | Temp files | Portable |
| ~/.config/app | RW | User config | Linux/macOS |

### Special Operations
| Operation | Location | Notes |
|-----------|----------|-------|
| inotify_init | fs.c:42 | Linux only - use FSEvents on macOS |
| O_DIRECT | cache.c:15 | Linux only - remove |
| ACL operations | perm.c:30 | Use libacl |
```

### 3.4 Privilege Summary

```markdown
## Privilege Requirements

### Drop Privilege Points
| Location | From | To | Purpose |
|----------|-------|-----|---------|
| main.c:100 | root | nobody | After binding port |
| worker.c:45 | root | app-user | After initialization |

### Capability Requirements
| Capability | Needed For | Current |
|-----------|------------|---------|
| CAP_NET_BIND_SERVICE | Port 80 | setuid binary |
| CAP_SYS_ADMIN | Mount fs | No - good |

### Security Assessment
- Uses privilege dropping: ✅ Yes
- Uses setuid binary: ⚠️ Yes (passwd-like)
- Uses capabilities: ❌ No
```

---

## 4. Step 3: Domain Analysis

### 4.1 Network/API Analysis (if applicable)

```markdown
## Network/Protocol Summary

### Ports
| Port | Protocol | Service | Access |
|------|----------|---------|--------|
| 8080 | TCP | HTTP API | Public |
| 6379 | TCP | Redis | Internal |

### API Endpoints (count = 23)
| Prefix | Count | Example |
|--------|-------|---------|
| /api/v1/users | 5 | GET /api/v1/users, POST /api/v1/users |
| /api/v1/orders | 8 | CRUD operations |
| /api/v1/auth | 3 | login, logout, refresh |

### Message Queues
| Queue | Type | Purpose | Publishers | Consumers |
|-------|------|---------|------------|------------|
| orders.created | RabbitMQ | Async order processing | order-service | payment-service, notification-service |
| users.created | RabbitMQ | User provisioning | auth-service | email-service |

### WebSockets
| Endpoint | Protocol | Channels |
|----------|----------|----------|
| /ws/events | ws | orders, users, notifications |
```

### 4.2 UI Analysis (if applicable)

```markdown
## UI Component Summary

### Views/Pages
| View | Type | Components | Complexity |
|------|------|------------|------------|
| Dashboard | Web | 12 | Medium |
| UserList | Web | 8 | Low |
| OrderDetail | Web | 15 | High |

### Key UI Objects
| Category | Count | Examples |
|----------|-------|----------|
| Display | 45 | Labels, badges, tables |
| Input | 23 | Forms, filters, search |
| Action | 18 | Buttons, links |
| Navigation | 8 | Tabs, breadcrumbs |

### State Machines
| Component | States | Transitions |
|-----------|--------|-------------|
| OrderForm | idle, validating, submitting, success, error | 8 |
| LoginButton | default, hover, loading, disabled | 4 |
```

---

## 5. Step 4: Quality Analysis

### 5.1 Duplication Summary

```markdown
## Code Duplication Found

### Exact Duplicates
| Location 1 | Location 2 | Lines | Fix |
|------------|------------|-------|-----|
| auth.c:42-52 | auth2.c:42-52 | 11 | Extract to auth_common.c |

### Near-Duplicates
| Group | Similarity | Merge Candidate |
|-------|------------|-----------------|
| Handler A,B,C | 78% | BaseHandler class |

### Dead Code
| Function | Location | Called By | Status |
|----------|----------|-----------|--------|
| legacy_auth() | auth.c:200 | Nobody | Dead - can skip |
| deprecated_format() | format.c:50 | Old code | Dead |
```

### 5.2 Refactoring Opportunities

```markdown
## Recommended Refactoring

### Priority 1 (High Impact, Low Effort)
| Issue | Location | Fix |
|-------|----------|-----|
| Extract auth duplication | auth.c:42, auth2.c:42 | Create auth_common.c |

### Priority 2 (High Impact, High Effort)
| Issue | Location | Fix |
|-------|----------|-----|
| Handler base class | handler_*.c | Extract BaseHandler |

### Priority 3 (Low Impact, High Effort)
| Issue | Location | Fix |
|-------|----------|-----|
| Custom memory allocator | mem.c | Use standard malloc |
```

---

## 6. Step 5: Consolidated Output

### 6.1 Feature Inventory

```markdown
## Feature Inventory (Actual, Not Assumed)

### Confirmed Features (with evidence)
| Feature | File:Line | Type | Porting Effort |
|---------|------------|------|----------------|
| Token validation (HMAC-SHA256) | auth.go:15 | Core | Low |
| User CRUD | users.go:8-45 | API | Medium |
| Order creation | orders.go:20-80 | API | Medium |
| WebSocket notifications | ws.go:10-50 | Real-time | High |
| Redis caching | cache.go:5-30 | Infra | Low |

### NOT Features (Dead Code)
| Implied Feature | Reality | Evidence |
|-----------------|---------|----------|
| LDAP auth | Dead code | ldap.go imported but never called |
| XML export | Dead code | xml.* functions never called |
| Legacy API v1 | Dead code | No routes registered |

### Feature Groups
| Group | Features | Cohesion |
|-------|----------|----------|
| Authentication | Token validation, Session management | High |
| User Management | CRUD, Profile, Permissions | High |
| Order Processing | Create, Update, Cancel, Notify | Medium |
```

### 6.2 Task Recommendations

```markdown
## Recommended Implementation Approach

### Option A: Port as-is (Fastest)
- Port all confirmed features
- Skip dead code
- Keep existing architecture
- Estimated tasks: 15-20

### Option B: Port + Refactor (Recommended)
- Port confirmed features
- Apply Priority 1 refactoring during port
- Fix architectural issues found
- Estimated tasks: 25-30

### Option C: Rewrite (If Architecture is Unsuitable)
- Do not port - start fresh
- Use feature inventory as requirements
- Estimated tasks: 40+

### Recommended: Option B
```

### 6.3 Analysis Report Template

```markdown
# Analysis Report: <Project>

**Date:** YYYY-MM-DD
**Analyst:** <Name>
**Source:** <Repository/Path>
**Target:** <Language/Platform>

## Executive Summary

[2-3 sentences on what was found]

## Key Findings

### Confirmed Features
- [List confirmed features with evidence]

### Dead Code
- [List code that appears to exist but is not called]

### Portability Issues
- [List OS-specific code requiring changes]

### Duplication
- [List duplicate code requiring refactoring]

## Recommendation

[Choose A, B, or C with rationale]

## Appendix: Full Inventories

[Links to detailed inventories from each analysis skill]
```

---

## 7. Using Output with Other Skills

### 7.1 Feeding feature-task-generator

```markdown
## Input for feature-task-generator

From this analysis, feature-task-generator should:

1. Use Feature Inventory (Section 6.1)
   - Only generate tasks for CONFIRMED features
   - Skip dead code features

2. Use Task Recommendations (Section 6.2)
   - Follow Option B approach

3. Use Quality Analysis (Section 5)
   - Include refactoring tasks in backlog
   - Prioritize refactoring after working port
```

### 7.2 Feeding plan-document-generator

```markdown
## Input for plan-document-generator

From this analysis, plan-document-generator should:

1. Update 0300-Implementation-Tasks.md with accurate tasks
2. Update 0210-Architecture-Design.md with actual architecture found
3. Add 0301-Kernel-Module.md or 0302-Userland-Tools.md as appropriate
4. Reference this analysis report in relevant documents
```

---

## Validation Checklist

Before declaring analysis complete:

- [ ] Project type determined
- [ ] All analysis skills run (as applicable)
- [ ] Feature Inventory created with evidence
- [ ] Dead code identified
- [ ] Portability issues documented
- [ ] Duplication identified
- [ ] Refactoring backlog created
- [ ] Task recommendation made
- [ ] Analysis Report consolidated

## Reference

This skill orchestrates:
- reverse-engineer-for-port
- system-call-analyzer
- process-model-analyzer
- network-stack-analyzer
- file-system-analyzer
- privilege-analyzer
- ui-ux-analyzer
- api-analyzer
- message-queue-analyzer
- code-quality-analyzer