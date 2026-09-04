---
name: reverse engineer for port
description: Systematically analyze source code to understand actual behavior before porting, avoiding assumptions based on names or structure.
---

# Skill: reverse-engineer-for-port

**Purpose:** Systematically analyze source code to understand actual behavior before porting, avoiding assumptions based on names or structure.

**Triggers:** When porting an application from one language/framework to another, or when needing to understand an unfamiliar codebase.

## Loading Instructions

Load this skill when the user asks you to:
- Analyze an application for porting
- Understand how an application actually works
- Find the real entry point and initial execution flow
- Discover actual features vs dead code
- Trace request/command handlers

## Core Principle

> **Names lie. Structure misleads. Trace the code.**

A file named `server.go` might serve humans or just JSON APIs. A function named `authenticate()` might do nothing. Only tracing execution reveals truth.

---

## 1. Entry Point Tracer

### 1.1 Find the True Entry Point

Do NOT assume `main()` is where work begins. Follow the actual execution path:

```bash
# Step 1: Find all main() functions
grep -r "func main()" --include="*.go" .

# Step 2: From main(), trace what runs first
# Look for: immediate function calls, init() functions, goroutine starts
```

### 1.2 Execution Order Discovery

```markdown
## Execution Order Template

| Order | Function | File | Line | What It Actually Does |
|-------|----------|------|------|---------------------|
| 1 | main() | main.go | 15 | Parses flags, calls init() |
| 2 | init() | main.go | 8 | Registers routes, does NOT connect to DB |
| 3 | serveAPI() | server.go | 42 | Starts HTTP server on :8080 |
```

### 1.3 Init vs Real Work

```go
// ❌ WRONG: "This app initializes a database connection"
// ✅ RIGHT: "init() registers routes, real DB connection happens on first request"

func init() {
    // This runs at startup but is just registration
    router.HandleFunc("/api/users", handleUsers)
}

func handleUsers(w http.ResponseWriter, r *http.Request) {
    // DB connection created HERE, lazily
    db := getDB()
}
```

### 1.4 Hot Path vs Setup

Distinguish between:
- **Setup** (runs once at startup): config loading, flag parsing, route registration
- **Hot path** (runs per-request/per-command): actual business logic

---

## 2. Actual Feature Finder

### 2.1 CLI Command Discovery

#### Static Registration (most common in Go/Rust/Cobra)

```go
// ❌ WRONG: "App has commands: users, groups, permissions, roles, audit"
// ✅ RIGHT: "Only 3 commands exist: start, stop, status"

func main() {
    rootCmd := &cobra.Command{}
    rootCmd.AddCommand(startCmd)   // EXISTS
    rootCmd.AddCommand(stopCmd)    // EXISTS
    rootCmd.AddCommand(statusCmd)  // EXISTS
    // usersCmd, groupsCmd, etc do NOT exist
    rootCmd.Execute()
}
```

#### Flag Detection

```bash
# These are NOT commands - they're flags on EXISTING commands
--help --version --config --verbose --debug

# These ARE subcommands
program users list
program groups add user group1 alice
```

#### Discovery Steps

```bash
# 1. Find command registration
grep -r "AddCommand\|Command(" --include="*.go" . | head -50

# 2. Find all cobra.Command{} definitions
grep -r "cobra.Command{" --include="*.go" -A 5 .

# 3. Find all click @click.command() decorators
grep -r "@click.command" --include="*.py" .
```

### 2.2 API Endpoint Discovery

```go
// ❌ WRONG: "REST API with full CRUD"
// ✅ RIGHT: "Only 3 endpoints: /health, /metrics, /api/v1/status"

router := mux.NewRouter()
router.HandleFunc("/health", healthHandler)     // EXISTS
router.HandleFunc("/metrics", metricsHandler)   // EXISTS
router.HandleFunc("/api/v1/status", statusHandler)  // EXISTS
// /api/v1/users, /api/v1/groups do NOT exist
```

#### Endpoint Tracing Template

```markdown
## Actual Endpoints

| Method | Path | Handler | Response Type | Evidence |
|--------|------|---------|---------------|----------|
| GET | /health | healthHandler | JSON | `json.NewEncoder(w).Encode()` |
| POST | /api/v1/start | startHandler | plain text | `w.Write([]byte("ok"))` |
```

### 2.3 Configuration Source Discovery

```go
// ❌ WRONG: "Supports YAML, JSON, TOML, ENV configuration"
// ✅ RIGHT: "Only reads from /etc/app.conf and ENV vars"

func loadConfig() {
    // ONLY these two sources are actually checked
    viper.SetConfigName("app")
    viper.AddConfigPath("/etc/")
    viper.AutomaticEnv()  // ENV vars override file

    // TOML, JSON, YAML support code is DEAD - never called
}
```

#### Configuration Evidence Checklist

```markdown
## Configuration Sources (Confirmed)

| Source | Type | Path/Env | Used By | Evidence |
|--------|------|----------|---------|----------|
| File | INI | /etc/app.conf | config.go:23 | `config.ReadFile()` |
| Environment | string | APP_MODE=production | config.go:45 | `viper.GetString("mode")` |

## Configuration Sources (Dead Code)

| Source | Type | Code Exists | Actually Called |
|--------|------|-------------|-----------------|
| YAML | YAML | yes | NO - no viper.SetConfigType() |
| JSON | JSON | yes | NO - no ReadJSON() calls |
| TOML | TOML | yes | NO - no TOML parser imported |
```

### 2.4 Dead Code Eliminator

```bash
# 1. Find all exported functions
grep -r "^func [A-Z]" --include="*.go" .

# 2. Check if each is called from main or other used functions
grep -r "FunctionName(" --include="*.go" .

# 3. Unused? Mark as dead code
```

#### Dead Code Template

```markdown
## Code Reachability Analysis

### Functions in main.go
| Function | Called By | Status |
|----------|-----------|--------|
| main() | OS | ✅ REACHED |
| init() | runtime | ✅ REACHED |
| setup() | main | ✅ REACHED |

### Functions in auth.go
| Function | Called By | Status |
|----------|-----------|--------|
| validateToken() | handleRequest | ✅ REACHED |
| hashPassword() | - | ❌ DEAD - never called |
| verifyAPIKey() | - | ❌ DEAD - never called |

### Import Analysis
| Import | Used By | Status |
|--------|---------|--------|
| bcrypt | validateToken() | ✅ USED |
| ldap | - | ❌ DEAD - imported but never called |
```

---

## 3. Component Role Classifier

### 3.1 Name vs Reality Template

```markdown
## Component Analysis

| File | Name Implies | Actual Role | Evidence |
|------|--------------|-------------|----------|
| `server.go` | HTTP server | API-only (JSON) | No template rendering, only `json.Marshal()` |
| `auth.go` | Authentication | Token validation | `hmac.Equal()` check, no password ops |
| `users.go` | User management | Read-only list | Only GET, no writes |
| `database.go` | DB operations | SQLite wrapper | `sql.Open()`, `Query()` only |
```

### 3.2 Response Type Detection

```go
// How to detect what's actually returned

// JSON responses
json.NewEncoder(w).Encode(resp)
json.Marshal(data)

// HTML responses (if ANY of these exist, it's NOT API-only)
html/template.Execute()
template.ParseFiles()
w.Write([]byte("<html>"))

// Plain text
w.Write([]byte("ok"))
fmt.Fprintf(w, "%s", text)

// gRPC (binary protocol)
proto.Marshal()
```

### 3.3 Middleware Discovery

```go
// ❌ WRONG: "Has authentication, rate limiting, logging middleware"
// ✅ RIGHT: "Only logging middleware exists"

router.Use(loggingMiddleware)    // EXISTS
// rateLimitMiddleware - does NOT exist
// authMiddleware - does NOT exist
```

---

## 4. Request Flow Mapper

### 4.1 HTTP Request Life Cycle

```markdown
## Request Flow: /api/v1/status

```
Client → router (/api/v1/status) → statusHandler (server.go:42)
                                        ↓
                                   validateToken (auth.go:15) ← called?
                                        ↓
                                   getDB() (db.go:8) ← lazy init
                                        ↓
                                   query SELECT... (db.go:23)
                                        ↓
                                   json.NewEncoder(w).Encode(result)
```
```

### 4.2 CLI Command Flow

```markdown
## Command Flow: ./app status

```
main() → rootCmd.Execute() → statusCmd.Run()
                                    ↓
                              loadConfig() (config.go:12)
                                    ↓
                              getStatus() (status.go:8)
                                    ↓
                              fmt.Fprintf(os.Stdout, "%s", status)
```
```

---

## 5. Output: Feature Inventory

### 5.1 Actual Features Document

```markdown
# Feature Inventory: <Application>

## CLI Commands (Confirmed)

| Command | Handler | File:Line | What It Does |
|---------|---------|-----------|--------------|
| `start` | startCmd.Run() | cmd/start.go:15 | Starts HTTP server on :8080 |
| `stop` | stopCmd.Run() | cmd/stop.go:8 | Sends SIGTERM to PID file |
| `status` | statusCmd.Run() | cmd/status.go:12 | Reads /var/run/app.pid, prints "running" or "stopped" |

## API Endpoints (Confirmed)

| Method | Path | Handler | Response | Auth |
|--------|------|---------|----------|------|
| GET | /health | healthHandler | JSON | None |
| GET | /metrics | metricsHandler | Prometheus | None |
| POST | /api/v1/start | startHandler | plain text | None |
| POST | /api/v1/stop | stopHandler | plain text | None |

## Configuration (Confirmed)

| Option | Type | Default | Source |
|--------|------|---------|--------|
| listen_addr | string | ":8080" | /etc/app.conf |
| log_level | string | "info" | ENV:LOG_LEVEL |
| pid_file | string | "/var/run/app.pid" | /etc/app.conf |

## NOT Features (Dead Code)

| Implied Feature | Reality |
|-----------------|---------|
| User management | Dead code - users.go not imported |
| LDAP authentication | Dead code - ldap package imported but unused |
| YAML config support | Dead code - no SetConfigType("yaml") call |
```

---

## Validation Checklist

Before declaring analysis complete:

- [ ] Traced from `main()` to first actual work
- [ ] Listed ONLY commands that exist in `AddCommand()` calls
- [ ] Listed ONLY endpoints that exist in route registration
- [ ] Confirmed response types by looking at `Write()`/`Encode()` calls
- [ ] Identified dead code (imports/functions not reachable from entry)
- [ ] Verified configuration sources by checking actual read calls
- [ ] Created Feature Inventory with evidence for each claim

## Reference

See Planning/PLANNING.md for task generation conventions.