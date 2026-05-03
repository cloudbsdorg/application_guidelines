---
name: codebase-mapper
description: Recursively map any codebase into exhaustive tree-view markdown documents in a .discovery/ directory
---

# Codebase Mapper

This skill performs exhaustive, recursive mapping of any codebase into tree-view markdown documents. Every component, file, function, and significant line of code gets its own mapped entry. The output lives in a `.discovery/` directory with a master TOC as the entry point.

## Source Of Truth

The `.discovery/` directory is the single source of truth for codebase understanding. When mapping:

1. Always read the actual file contents before generating tree nodes.
2. Never assume what code does — verify by reading it.
3. If a file imports/requires other files, map those dependencies explicitly.
4. When encountering unfamiliar patterns, read surrounding context before classifying.
5. Prefer answers and descriptions backed by specific source content.

## Guidelines

- **Standards as Law**: This skill's methodology is mandatory, not optional. Every step must be followed.
- **UTF-8 Everywhere**: All generated markdown documents use UTF-8 encoding.
- **One File Per Component**: No single discovery file exceeds ~200 lines of tree content. If a component is large, split it into sub-files.
- **Recursion Has No Depth Limit**: Map as deep as needed. A single line of code can generate 10 tree levels if it involves imports, function calls, object construction, method chains, callbacks, and nested arguments.
- **No Duplication**: Each discovered item maps to exactly one file. Cross-reference via links, never duplicate content.
- **Evidence-Based Descriptions**: Every node description must be backed by what the code actually does, not what you think it should do.
- **Follow Existing Patterns**: When describing components, reference the actual patterns found in the codebase (conventions, naming, architecture).
- **Do NOT modify source code**: This skill only reads and generates discovery documents. Never change the codebase being mapped.
- **Do NOT skip "obvious" items**: Even simple files get mapped. Assumptions about simplicity are the #1 cause of incomplete maps.

## Loading Instructions

Load this skill when the user asks you to:
- Map the codebase
- Create a codebase discovery document
- Generate a tree view of the project structure
- Document what every file and component does
- Create a `.discovery/` directory structure
- Build a codebase map with TOC
- Recursively explore and document the project

## Core Directives (from CloudBSD Application Guidelines)

These directives from the CloudBSD standards govern all mapping behavior:

### Target Platform Awareness
- The codebase being mapped may target any platform. Document the target platform when identified.
- Do not assume the detected environment reflects the real target. Verify via `uname -s`, package managers, config files, and build scripts.
- If the codebase is FreeBSD-targeting (CloudBSD), note this in the root discovery document.

### Security Observations
- When mapping, flag any hardcoded credentials, secrets, or security-relevant patterns.
- Document authentication flows, authorization checks, and input validation points.
- Note least-privilege patterns and privilege escalation paths.

### Configuration Patterns
- Document all configuration file formats and locations discovered.
- Map XDG Base Directory usage if present (`$XDG_CONFIG_HOME`, `$XDG_DATA_HOME`, `$XDG_CACHE_HOME`).
- Map system-wide config paths (e.g., `/usr/local/etc/`, `/etc/`).
- Document environment variable usage for configuration.

### Testing Infrastructure
- Map all test files, test frameworks, and test configurations.
- Document CI/CD pipeline configurations found (GitHub Actions, Jenkins, etc.).
- Note bhyve VM or jail testing patterns if present (FreeBSD-specific).

### Internationalization
- Map all i18n/l10n files, translation directories, and locale configurations.
- Document the i18n framework used (gettext, i18next, etc.).
- Note UTF-8 compliance across source files.

## Mapping Methodology

### Phase 0: Entry Point Identification

Identify the starting point of the application:
1. Read `package.json`, `Cargo.toml`, `go.mod`, `pyproject.toml`, `Makefile`, or equivalent to find entry points.
2. Identify the main executable, server entry, CLI entry, or library entry.
3. Read the entry point file completely before proceeding.
4. Create the root discovery document at `.discovery/000-root.md`.

### Phase 1: Directory Structure Scan

Generate a high-level tree of the entire project structure:

```
project-root/
├── .discovery/          # Discovery documents (output)
├── src/
│   ├── main.ts          # Entry point → maps to 100-main.md
│   ├── config/          # Configuration module → maps to 200-config/
│   └── server/          # Server module → maps to 300-server/
├── test/
│   └── ...
├── package.json
└── ...
```

Each directory entry in this tree links to its own discovery file.

### Phase 2: Recursive Component Mapping

For each discovered item, generate a tree-view document following this structure:

#### File-Level Tree

```markdown
# Component: <filename>

**Path:** `relative/path/to/file.ext`
**Type:** File | Directory | Module | Service | Component
**Maps to:** `.discovery/<NNN>-<name>.md`
**Dependencies:** [list of imported files with links]
**Dependents:** [list of files that import this, with links]

## Structure

```
filename.ext
├── [import] "module-a" → .discovery/XXX-module-a.md
├── [import] "module-b" → .discovery/XXX-module-b.md
├── export function main() { ... }
│   ├── Initializes the application
│   ├── Loads configuration from config.ts
│   ├── Starts the HTTP server
│   └── Sets up error handlers
├── export class AppServer
│   ├── constructor(options: ServerOptions)
│   │   ├── Validates server options
│   │   ├── Creates Express/Koa/Hono instance
│   │   └── Registers middleware stack
│   ├── async start()
│   │   ├── Binds to configured port
│   │   ├── Logs startup message
│   │   └── Returns server instance
│   └── async stop()
│       ├── Closes database connections
│       ├── Stops background workers
│       └── Unbinds from port
├── const ROUTES = { ... }
│   ├── GET /health → healthCheck handler
│   ├── POST /auth/login → login handler
│   └── GET /api/users → users handler
└── [re-export] from "./utils" → .discovery/XXX-utils.md
```

## Description

<What this file/component does, in 2-3 sentences based on actual code content.>

## Data Flow

<How data moves through this component. Reference specific functions and their inputs/outputs.>

## Side Effects

<Any I/O, network calls, file writes, process spawning, or external system interactions.>
```

#### Directory-Level Tree

```markdown
# Directory: src/config/

**Path:** `src/config/`
**Type:** Directory | Module Group
**Child files:**
- `config.ts` → `.discovery/200-config.md`
- `schema.ts` → `.discovery/201-config-schema.md`
- `defaults.json` → `.discovery/202-config-defaults.md`

## Structure

```
src/config/
├── config.ts          # Main configuration loader → 200-config.md
│   ├── Loads and validates configuration
│   ├── Supports JSON, YAML, env vars
│   └── Exports typed Config object
├── schema.ts          # Zod/JSON schema definitions → 201-config-schema.md
│   ├── Defines ConfigSchema
│   ├── Validates required fields
│   └── Provides default values
└── defaults.json      # Default configuration values → 202-config-defaults.md
    ├── Port: 3000
    ├── Log level: "info"
    └── Database URL: null (required)
```

## Purpose

<What this directory groups together and why.>
```

#### Deep Dive: Single Line Decomposition

When a single line of code warrants multiple tree levels, decompose it:

```
const result = await authService.login(username, password).then(r => r.token);
│
├── authService (imported from "./services/auth")
│   └── .login(username, password) → async function
│       ├── Validates username format → validateUsername()
│       │   └── Regex: /^[a-zA-Z0-9_]{3,30}$/
│       ├── Hashes password → hashPassword(password, salt)
│       │   └── Uses bcrypt with cost factor 12
│       ├── Queries database → db.users.findOne({ username })
│       │   └── SQL: SELECT * FROM users WHERE username = $1
│       ├── Compares hash → bcrypt.compare(inputHash, storedHash)
│       ├── Generates JWT → jwt.sign({ sub: user.id, role: user.role })
│       │   ├── Algorithm: RS256
│       │   ├── Expires: 15 minutes
│       │   └── Signs with private key from config
│       └── Returns { token, refreshToken, user }
│
├── .then(r => r.token) (Promise chain)
│   └── Extracts token property from response object
│
└── await (async/await context)
    └── Suspends execution until Promise resolves
    └── result: string (JWT token)
```

### Phase 3: Cross-Reference Generation

After mapping all components, generate cross-references:
1. Track every import/require statement across all files.
2. Build a dependency graph showing which components depend on which.
3. Identify circular dependencies.
4. Identify orphan files (not imported by anything).
5. Identify entry points (imported by nothing, but referenced in build config).

### Phase 4: TOC Generation

Create the master Table of Contents at `.discovery/TOC.md`:

```markdown
# Codebase Discovery — Table of Contents

**Project:** <project-name>
**Generated:** YYYY-MM-DD
**Root:** <entry-point-path>
**Total files mapped:** <count>
**Total directories mapped:** <count>

---

## Project Structure

```
<Full project tree with links to discovery files>
```

## Document Map

| File | Component | Type | Description |
|------|-----------|------|-------------|
| [000-root.md](./000-root.md) | Project root | Entry point | Main application entry |
| [100-main.md](./100-main.md) | main.ts | File | Application bootstrap |
| [200-config.md](./200-config.md) | config.ts | Module | Configuration loader |
| ... | ... | ... | ... |

## Dependency Graph

```
<ASCII dependency graph showing component relationships>
```

## Entry Points

| Entry Point | Type | Description |
|-------------|------|-------------|
| `src/main.ts` | Application | Main server entry |
| `src/cli/index.ts` | CLI | Command-line interface |
| `test/setup.ts` | Test | Test configuration |

## Orphan Files

| File | Why Orphaned |
|------|-------------|
| `scripts/migrate.ts` | Standalone migration script |
| `docs/examples/usage.ts` | Documentation example |

## Circular Dependencies

| Cycle | Severity |
|-------|----------|
| `auth.ts` ↔ `users.ts` | Warning |

## Statistics

| Metric | Count |
|--------|-------|
| Total files | |
| Total directories | |
| Total functions | |
| Total classes | |
| Total exports | |
| Total imports | |
| Max nesting depth | |
| Orphan files | |
| Circular dependencies | |
```

## Naming Convention

Discovery documents follow: `.discovery/<NNN>-<name>.md`

| Pattern | Example |
|---------|---------|
| Root entry | `.discovery/000-root.md` |
| Single file | `.discovery/100-main.md` |
| Directory group | `.discovery/200-config/` (directory of files) |
| Sub-component | `.discovery/201-config-schema.md` |
| Deep component | `.discovery/201-01-config-validation.md` |

Numbering rules:
- Start at 000 for the root.
- Increment by 100 for top-level components.
- Use sequential numbers for sibling components.
- Use `<parent>-<sub>` notation for deeply nested items.
- Keep numbers consistent — never renumber existing files.

## Tree Node Format

Every node in a tree follows this format:

```
├── [type] identifier
│   ├── <description of what it does>
│   ├── <secondary behavior>
│   └── <tertiary behavior or output>
```

Where `[type]` is one of:
- `[import]` — External or internal import
- `[export]` — Exported symbol
- `[function]` — Function definition
- `[class]` — Class definition
- `[const]` — Constant/variable
- `[type]` — Type/interface definition
- `[enum]` — Enum definition
- `[route]` — API route/endpoint
- `[handler]` — Event/request handler
- `[middleware]` — Middleware function
- `[config]` — Configuration value
- `[hook]` — React/custom hook
- `[method]` — Class/instance method
- `[re-export]` — Re-exported from another module
- `[side-effect]` — Side-effectful operation

## Description Guidelines

Descriptions must be:
1. **Specific**: "Validates username against regex `/^[a-zA-Z0-9_]{3,30}$/`" not "Validates input"
2. **Evidence-based**: Derived from reading the actual code, not assumptions
3. **Action-oriented**: Start with verbs (validates, creates, sends, queries)
4. **Complete**: Cover all branches, error paths, and edge cases found in code
5. **Linked**: Reference other discovery documents when behavior crosses component boundaries

## Splitting Rules

Split a discovery document when:
1. The tree structure exceeds 200 lines.
2. A single component has more than 10 child nodes with descriptions.
3. A class has more than 5 methods with complex behavior.
4. A function has more than 3 levels of nesting.
5. The description section exceeds 50 lines.

When splitting:
1. Create a new file with the next available number.
2. Replace the inline tree with a link: `├── [see] full details → .discovery/XXX-name.md`
3. Update the TOC with the new file.
4. Maintain the link chain in both directions.

## Recursion Termination

Recursion terminates when:
1. A file has been fully mapped (all exports, imports, and significant internals documented).
2. A node is a primitive value (string literal, number, boolean) with no behavior.
3. A node references a standard library API already well-documented elsewhere (e.g., `console.log`, `Array.map`).
4. Maximum practical depth is reached (the tree would become unreadable beyond this point).

**Never terminate early** because something "seems simple." Verify by reading the code.

## Quality Checklist

Before marking mapping as complete:

- [ ] Every file in the project (except `.discovery/` itself) is mapped
- [ ] Every import has a linked discovery document
- [ ] Every export is documented with its behavior
- [ ] Directory trees show all children with descriptions
- [ ] The TOC links to every discovery document
- [ ] The dependency graph is accurate
- [ ] Circular dependencies are identified
- [ ] Orphan files are listed
- [ ] Entry points are identified
- [ ] No discovery file exceeds 200 lines without being split
- [ ] All descriptions are evidence-based (from actual code, not assumptions)
- [ ] Cross-references between documents are correct
- [ ] Statistics in TOC are accurate
- [ ] UTF-8 encoding throughout
- [ ] No duplicate content across files (use links instead)

## Example: Complete Mapping of a Small File

Given `src/utils/logger.ts`:

```typescript
import winston from "winston"
import { config } from "../config"

export const logger = winston.createLogger({
  level: config.logLevel,
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: "error.log", level: "error" }),
    new winston.transports.File({ filename: "combined.log" }),
  ],
})

if (config.env !== "production") {
  logger.add(new winston.transports.Console({
    format: winston.format.simple(),
  }))
}
```

Maps to `.discovery/300-logger.md`:

```markdown
# Component: logger.ts

**Path:** `src/utils/logger.ts`
**Type:** Module
**Maps to:** `.discovery/300-logger.md`
**Dependencies:**
- `winston` (external) — Logging framework
- `../config` → `.discovery/200-config.md` — Configuration module

## Structure

```
logger.ts
├── [import] winston from "winston"
│   └── External logging library (npm package)
├── [import] { config } from "../config" → .discovery/200-config.md
│   └── Imports application configuration object
├── [export] const logger
│   ├── Creates winston logger instance
│   ├── Level: set by config.logLevel (from .discovery/200-config.md)
│   ├── Format: JSON structured logging
│   ├── Transports:
│   │   ├── File: error.log — captures error-level and above
│   │   └── File: combined.log — captures all levels
│   └── Side effect: creates log files on disk
└── [side-effect] conditional console transport
    ├── Condition: config.env !== "production"
    ├── When true: adds Console transport
    │   └── Format: simple text (human-readable)
    └── When false: no console output (production)
```

## Description

Configures a Winston logger with environment-aware transports. In production, logs go to files only (`error.log` for errors, `combined.log` for everything). In development, also outputs human-readable text to the console. Log level is configurable via the application config.

## Data Flow

```
config.logLevel ──┐
                  ▼
config.env ───► logger creation ──► File transports (always)
                  │
                  └──► Console transport (dev only)
```

## Side Effects

- Creates `error.log` and `combined.log` files in working directory
- Writes log entries on every logger invocation
- Adds console output when `config.env !== "production"`
```

## Reference

- CloudBSD Application Guidelines: `https://github.com/cloudbsdorg/application_guidelines`
- Planning standards: `.plan/` directory conventions
- ASCII diagram conventions from `ascii-diagrammer` skill
- TOC generation patterns from `toc-generator` skill
