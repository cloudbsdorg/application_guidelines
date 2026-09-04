---
name: feature-task-generator
description: >-
  Turn a feature inventory produced by analysis into concrete implementation
  tasks. Use after reverse-engineering or source analysis, when planning a
  port, and specifically to avoid inventing tasks for functionality that is
  not actually reachable in the source.
---

# Skill: feature-task-generator

**Purpose:** Generate implementation tasks from actual feature discovery, avoiding over-generation by only capturing reachable, used functionality.

**Triggers:** After using reverse-engineer-for-port to analyze a codebase, when you need to generate porting tasks.

## Loading Instructions

Load this skill when the user asks you to:
- Generate tasks for a porting project
- Create implementation tasks from feature analysis
- Turn features into actionable work items
- Avoid over-generating tasks for dead code

## Core Principle

> **One task per workflow, not one task per file.**

A file might contain 5 functions but only 1 is called. Generate 1 task for that 1 function, not 5.

---

## 1. Task Generation Rules

### 1.1 Anti-Patterns

| Anti-Pattern | Wrong Result | Correct Approach |
|---------------|--------------|------------------|
| One task per source file | 50 tasks for 50 files | One task per workflow |
| List all possible features | 200 tasks | Only 12 actual features |
| "Implement X module" | Too vague | "Port `handleUsers()` at server.go:42" |
| "Comprehensive test suite" | 50 test tasks | "Port 3 integration tests from test/" |

### 1.2 Task Naming Convention

```
WRONG:  "Implement user authentication module"
RIGHT:  "Port validateToken() - HMAC-SHA256 at auth.go:15"

WRONG:  "Create API endpoints"
RIGHT:  "Port /health, /metrics, /api/v1/status endpoints"

WRONG:  "Implement CLI commands"
RIGHT:  "Port start/stop/status commands from cmd/*.go"
```

### 1.3 Task Granularity

```markdown
## Too Granular (BAD)

| ID | Task |
|----|------|
| T1 | Port auth.go |
| T2 | Port auth.go:validateToken() |
| T3 | Port auth.go:hashPassword() (DEAD CODE) |
| T4 | Port auth.go:getSession() |
| T5 | Port users.go |
| T6 | Port users.go:getUser() |
| ... |

## Right Granularity (GOOD)

| ID | Task | Evidence |
|----|------|----------|
| T1 | Port token validation (HMAC-SHA256) | auth.go:15, called by all handlers |
| T2 | Port /health and /metrics endpoints | server.go:42-50, JSON response |
| T3 | Port user list endpoint (read-only) | users.go:8, SELECT only, no writes |
```

---

## 2. Task Template

### 2.1 Standard Task Format

```markdown
## <Task ID>: <Concise Description>

**Feature:** <Feature name from inventory>
**Type:** CLI | API | Core | Config
**Priority:** P0 | P1 | P2 | P3

### Evidence
- **Source file:** `src/auth.go:15`
- **Called by:** `server.go:42`, `api.go:38`
- **Dependencies:** None | Other task ID

### What to Port
1. Function/class name and signature
2. Input parameters and sources
3. Output format (JSON, plain text, etc.)
4. Any side effects (files, network, DB)

### Acceptance Criteria
- [ ] Function compiles in target language
- [ ] Same input produces same output
- [ ] Called correctly by existing code
- [ ] Tests ported and passing

### Notes
- Original uses bcrypt, target should use [equivalent]
- Thread-safe, no global state
```

### 2.2 Task Type Definitions

| Type | Description | Example |
|------|-------------|---------|
| `CLI` | Command-line interface | `./app start` |
| `API` | HTTP/gRPC endpoint | `GET /health` |
| `Core` | Core business logic | Token validation |
| `Config` | Configuration handling | Config file parsing |
| `Util` | Utility/helper functions | Date formatting |

---

## 3. Workflow-Based Task Grouping

### 3.1 Group by User-Facing Operation

```markdown
## Task Group: Status Command

| ID | Sub-task | File | Line |
|----|----------|------|------|
| CLI-1 | Parse start/stop/status subcommands | main.go | 15 |
| CLI-1 | Implement start handler | cmd/start.go | 8 |
| CLI-1 | Implement stop handler | cmd/stop.go | 8 |
| CLI-1 | Implement status handler | cmd/status.go | 8 |

**Single task:** "Port status CLI command (start/stop/status)"

## Task Group: Health Monitoring

| ID | Sub-task | File | Line |
|----|----------|------|------|
| API-1 | /health endpoint | server.go | 42 |
| API-1 | /metrics endpoint | server.go | 55 |
| API-1 | Prometheus format | metrics.go | 12 |

**Single task:** "Port health/metrics endpoints"
```

### 3.2 Dependency Analysis

```markdown
## Dependency Graph

```
[Token Validation] ← CLI-1, API-1 (both depend on this)
       ↑
       │
[Config Loading] ← [Token Validation] ← [Health Endpoints]
       ↑
   (no deps - port first)
```

## Porting Order
1. **Config Loading** (P0) - everything depends on this
2. **Token Validation** (P0) - CLI and API depend on this
3. **Health Endpoints** (P1) - independent, port in parallel
4. **CLI Commands** (P1) - depends on config + auth
5. **API Endpoints** (P1) - depends on config + auth
```

---

## 4. CLI Command Tasks

### 4.1 Template

```markdown
## <Task ID>: Port `<command>` command

**Source:** `cmd/<command>.go`
**Handler:** `func <command>Cmd.Run(cmd *cobra.Command, args []string)`
**Called by:** `main()` via `rootCmd.AddCommand()`

### What It Does (Evidence)
1. Loads config from `/etc/app.conf`
2. Reads PID from `/var/run/app.pid`
3. Prints "running" or "stopped" to stdout

### Porting Notes
- Uses `cobra` - find equivalent in target (e.g., `click`, `urfave/cli`)
- No external API calls
- Exit codes: 0=running, 1=stopped, 2=error

### Acceptance Criteria
- [ ] `program status` returns same exit codes
- [ ] Output format matches original
```

### 4.2 CLI Task Example

```markdown
## CLI-1: Port start/stop/status commands

**Feature:** CLI command interface
**Type:** CLI
**Priority:** P1
**Source:** cmd/start.go, cmd/stop.go, cmd/status.go

### What to Port

| Command | Handler | Key Operations |
|---------|---------|----------------|
| `start` | startCmd.Run() | Read config, write PID file, start goroutine |
| `stop` | stopCmd.Run() | Read PID, send SIGTERM, remove PID file |
| `status` | statusCmd.Run() | Read PID, check process, print status |

### Dependencies
- Core-1: Config loading (must port first)

### Acceptance Criteria
- [ ] All 3 commands compile
- [ ] `start` creates PID file
- [ ] `stop` terminates process from PID file
- [ ] `status` reports correct state
```

---

## 5. API Endpoint Tasks

### 5.1 Template

```markdown
## <Task ID>: Port <method> <path> endpoint

**Source:** `server.go:<line>`
**Handler:** `func <handler>(w http.ResponseWriter, r *http.Request)`
**Response:** JSON | plain text | HTML

### Request Handling (Evidence)
1. Parse request (path params, query, body)
2. Validate auth token (if any)
3. Call core logic
4. Return response

### Porting Notes
- Uses `net/http` - target uses [framework]
- No middleware exists (no auth, no rate limiting)
- Response is JSON: `{"status": "ok", "time": 1234567890}`

### Acceptance Criteria
- [ ] Endpoint responds at correct path
- [ ] Same response format
- [ ] Same status codes
```

### 5.2 API Task Example

```markdown
## API-1: Port health and metrics endpoints

**Feature:** Health monitoring API
**Type:** API
**Priority:** P1
**Source:** server.go:42-70

### Endpoints to Port

| Method | Path | Handler | Response |
|--------|------|---------|----------|
| GET | /health | healthHandler | `{"status": "ok"}` |
| GET | /metrics | metricsHandler | Prometheus text format |

### What to Port
- Two HTTP handlers returning JSON/Prometheus format
- No authentication required
- No middleware

### Dependencies
- None (can port independently)

### Acceptance Criteria
- [ ] GET /health returns `{"status": "ok"}`
- [ ] GET /metrics returns Prometheus format
- [ ] No auth required
```

---

## 6. Core Logic Tasks

### 6.1 Template

```markdown
## <Task ID>: Port <function>

**Source:** `<file>:<line>`
**Signature:** `func <name>(<params>) <returns>`
**Called by:** <callers>

### Evidence of Use
```go
// How it's actually called
result := validateToken(token)
```

### What to Port
1. Function signature
2. Logic (HMAC-SHA256 validation)
3. Error handling

### Porting Notes
- Uses `crypto/hmac` and `crypto/sha256`
- Target should use equivalent hash package
- Returns (bool, error) - true if valid

### Acceptance Criteria
- [ ] Same HMAC output for same input
- [ ] Returns false for invalid tokens
- [ ] Returns error on hmac failure
```

### 6.2 Core Task Example

```markdown
## CORE-1: Port token validation (HMAC-SHA256)

**Feature:** Authentication
**Type:** Core
**Priority:** P0
**Source:** auth.go:15

### Signature
```go
func validateToken(token string) (bool, error)
```

### Evidence of Use
```go
// Called at server.go:42 before every API request
valid, err := validateToken(token)
if !valid { http.Error(w, "unauthorized", 401) }
```

### What to Port
- HMAC-SHA256 comparison using secret key
- Constant-time comparison to prevent timing attacks
- Error on empty token, invalid format

### Dependencies
- None (pure function)

### Acceptance Criteria
- [ ] Same valid/invalid results as original
- [ ] Constant-time comparison
- [ ] Error on empty/invalid input
```

---

## 7. Configuration Tasks

### 7.1 Template

```markdown
## <Task ID>: Port config loading

**Source:** `config.go:<line>`
**Format:** INI | JSON | ENV | custom
**Path:** `/etc/app.conf` | ENV vars | both

### What to Port
1. Config file reading
2. ENV var override
3. Default values
4. Validation

### Confirmed Options
| Option | Type | Default | ENV Override |
|--------|------|---------|--------------|
| listen_addr | string | ":8080" | LISTEN_ADDR |
| log_level | string | "info" | LOG_LEVEL |
| pid_file | string | "/var/run/app.pid" | (none) |
```

### 7.2 Config Task Example

```markdown
## CORE-2: Port configuration loading

**Feature:** Configuration
**Type:** Config
**Priority:** P0
**Source:** config.go:12-45

### What to Port
- INI file parser at /etc/app.conf
- ENV var override via viper.AutomaticEnv()
- Default values
- Type conversion

### Config Options (Confirmed)
| Option | Type | Default | Source |
|--------|------|---------|--------|
| mode | string | "production" | ENV:APP_MODE |
| workers | int | 4 | ENV:WORKERS |
| timeout | int | 30 | ENV:TIMEOUT |

### Dependencies
- None (port first)

### Acceptance Criteria
- [ ] Reads /etc/app.conf correctly
- [ ] ENV vars override file values
- [ ] Defaults applied when neither set
- [ ] Same validation as original
```

---

## 8. Task Table Output

### 8.1 Final Task Table Format

```markdown
## Implementation Tasks

| ID | Task | Type | Priority | Dependencies | Evidence |
|----|------|------|----------|--------------|----------|
| CORE-1 | Token validation (HMAC-SHA256) | Core | P0 | - | auth.go:15 |
| CORE-2 | Config loading (INI+ENV) | Config | P0 | - | config.go:12 |
| CORE-3 | PID file management | Core | P1 | CORE-2 | pid.go:8 |
| CLI-1 | Port start/stop/status commands | CLI | P1 | CORE-2, CORE-3 | cmd/*.go |
| API-1 | Port health/metrics endpoints | API | P1 | CORE-2 | server.go:42 |
| API-2 | Port status API endpoint | API | P1 | CORE-1, CORE-2 | server.go:55 |
```

### 8.2 Summary Statistics

```markdown
## Task Summary

| Category | Count | P0 | P1 | P2 |
|----------|-------|-----|-----|-----|
| Core | 3 | 2 | 1 | 0 |
| CLI | 1 | 0 | 1 | 0 |
| API | 2 | 0 | 2 | 0 |
| **Total** | **6** | **2** | **4** | **0** |

**Note:** Only 6 tasks for 50+ source files. Dead code eliminated.
```

---

## Validation Checklist

Before finalizing task list:

- [ ] Each task has evidence (file:line) proving feature exists
- [ ] No tasks for dead code (functions never called)
- [ ] No tasks for unused imports
- [ ] Tasks grouped by workflow, not by file
- [ ] Dependencies correctly identified
- [ ] Priority reflects dependency order
- [ ] Summary count is realistic (likely <20 tasks for most apps)

## Reference

See Planning/PLANNING.md Section 4 (Task Tables) for format specification.