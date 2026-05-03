---
name: codebase-mapper-phases-2-3
description: Phase 2 (Recursive Component Mapping) and Phase 3 (Cross-Reference Generation) of codebase-mapper.
---

# Codebase Mapper — Phases 2-3

## Phase2: Recursive Component Mapping

**Source File Decomposition (MANDATORY for source files):**

Before generating the tree-view document, DECOMPOSE each source file to extract its structure:

```bash
# Function to decompose source files - extract real code structure
decompose_source() {
  local file="$1"
  local ext="${file##*.}"
  local structure=""

  case "$ext" in
    js|jsx|ts|tsx)
      # Extract imports
      IMPORTS=$(grep -E "^import |^const .* = require\(|^let .* = require\(|^var .* = require\(" "$file" 2>/dev/null | head -10)
      [[ -n "$IMPORTS" ]] && structure="${structure}\n#### Imports\n\`\`\`javascript\n${IMPORTS}\n\`\`\`\n"

      # Extract exports
      EXPORTS=$(grep -E "^export |^module.exports" "$file" 2>/dev/null | head -10)
      [[ -n "$EXPORTS" ]] && structure="${structure}\n#### Exports\n\`\`\`javascript\n${EXPORTS}\n\`\`\`\n"

      # Extract function names
      FUNCTIONS=$(grep -oE "(function|const|let|var) [a-zA-Z0-9_]+" "$file" 2>/dev/null | sed 's/function //; s/const //; s/let //; s/var //' | sort -u | tr '\n' ', ' | sed 's/, $//')
      [[ -n "$FUNCTIONS" ]] && structure="${structure}\n#### Functions\n$FUNCTIONS\n"

      # Extract class names
      CLASSES=$(grep -oE "class [a-zA-Z0-9_]+" "$file" 2>/dev/null | sed 's/class //' | tr '\n' ', ' | sed 's/, $//')
      [[ -n "$CLASSES" ]] && structure="${structure}\n#### Classes\n$CLASSES\n"

      # Extract type/interface names (TypeScript)
      TYPES=$(grep -oE "(type|interface) [a-zA-Z0-9_]+" "$file" 2>/dev/null | sed 's/type //; s/interface //' | tr '\n' ', ' | sed 's/, $//')
      [[ -n "$TYPES" ]] && structure="${structure}\n#### Types/Interfaces\n$TYPES\n"

      # Extract global variables (all caps or at file scope)
      GLOBALS=$(grep -E "^(const|let|var) [A-Z_][A-Z0-9_]*" "$file" 2>/dev/null | head -5)
      [[ -n "$GLOBALS" ]] && structure="${structure}\n#### Global Variables\n\`\`\`javascript\n${GLOBALS}\n\`\`\`\n"
      ;;

    c|cpp|cxx)
      # Extract #includes
      INCLUDES=$(grep -E "^#include " "$file" 2>/dev/null | head -10)
      [[ -n "$INCLUDES" ]] && structure="${structure}\n#### Includes\n\`\`\`c\n${INCLUDES}\n\`\`\`\n"

      # Extract function signatures
      FUNCTIONS=$(grep -E "^[a-zA-Z_].*\(.*\)\s*{" "$file" 2>/dev/null | sed 's/{//' | head -10 | tr '\n' ', ' | sed 's/, $//')
      [[ -n "$FUNCTIONS" ]] && structure="${structure}\n#### Functions\n$FUNCTIONS\n"

      # Extract struct names
      STRUCTS=$(grep -oE "struct [a-zA-Z0-9_]+" "$file" 2>/dev/null | sed 's/struct //' | tr '\n' ', ' | sed 's/, $//')
      [[ -n "$STRUCTS" ]] && structure="${structure}\n#### Structs\n$STRUCTS\n"

      # Extract global variables
      GLOBALS=$(grep -E "^(const |static )?(int|char|float|double|void|long) [A-Z_][A-Z0-9_]*" "$file" 2>/dev/null | head -5)
      [[ -n "$GLOBALS" ]] && structure="${structure}\n#### Global Variables\n\`\`\`c\n${GLOBALS}\n\`\`\`\n"
      ;;

    py)
      # Extract imports
      IMPORTS=$(grep -E "^import |^from .* import" "$file" 2>/dev/null | head -10)
      [[ -n "$IMPORTS" ]] && structure="${structure}\n#### Imports\n\`\`\`python\n${IMPORTS}\n\`\`\`\n"

      # Extract function defs
      FUNCTIONS=$(grep -oE "^def [a-zA-Z0-9_]+" "$file" 2>/dev/null | sed 's/def //' | tr '\n' ', ' | sed 's/, $//')
      [[ -n "$FUNCTIONS" ]] && structure="${structure}\n#### Functions\n$FUNCTIONS\n"

      # Extract class defs
      CLASSES=$(grep -oE "^class [a-zA-Z0-9_]+" "$file" 2>/dev/null | sed 's/class //' | tr '\n' ', ' | sed 's/, $//')
      [[ -n "$CLASSES" ]] && structure="${structure}\n#### Classes\n$CLASSES\n"

      # Extract global variables (all caps)
      GLOBALS=$(grep -E "^[A-Z_][A-Z0-9_]*\s*=" "$file" 2>/dev/null | head -5)
      [[ -n "$GLOBALS" ]] && structure="${structure}\n#### Global Variables\n\`\`\`python\n${GLOBALS}\n\`\`\`\n"
      ;;

    go)
      # Extract imports
      IMPORTS=$(grep -A 20 "^import (" "$file" 2>/dev/null | grep '"' | head -10)
      [[ -n "$IMPORTS" ]] && structure="${structure}\n#### Imports\n\`\`\`go\n${IMPORTS}\n\`\`\`\n"

      # Extract function defs
      FUNCTIONS=$(grep -oE "^func [a-zA-Z0-9_]+" "$file" 2>/dev/null | sed 's/func //' | tr '\n' ', ' | sed 's/, $//')
      [[ -n "$FUNCTIONS" ]] && structure="${structure}\n#### Functions\n$FUNCTIONS\n"

      # Extract type/struct defs
      TYPES=$(grep -oE "^(type|struct) [a-zA-Z0-9_]+" "$file" 2>/dev/null | sed 's/type //; s/struct //' | tr '\n' ', ' | sed 's/, $//')
      [[ -n "$TYPES" ]] && structure="${structure}\n#### Types/Structs\n$TYPES\n"
      ;;

    rs)
      # Extract use/mod statements
      IMPORTS=$(grep -E "^use |^mod " "$file" 2>/dev/null | head -10)
      [[ -n "$IMPORTS" ]] && structure="${structure}\n#### Imports\n\`\`\`rust\n${IMPORTS}\n\`\`\`\n"

      # Extract fn defs
      FUNCTIONS=$(grep -oE "fn [a-zA-Z0-9_]+" "$file" 2>/dev/null | sed 's/fn //' | tr '\n' ', ' | sed 's/, $//')
      [[ -n "$FUNCTIONS" ]] && structure="${structure}\n#### Functions\n$FUNCTIONS\n"

      # Extract struct/enum/trait defs
      TYPES=$(grep -oE "^(struct|enum|trait) [a-zA-Z0-9_]+" "$file" 2>/dev/null | sed 's/struct //; s/enum //; s/trait //' | tr '\n' ', ' | sed 's/, $//')
      [[ -n "$TYPES" ]] && structure="${structure}\n#### Types\n$TYPES\n"
      ;;

    java)
      # Extract imports
      IMPORTS=$(grep -E "^import " "$file" 2>/dev/null | head -10)
      [[ -n "$IMPORTS" ]] && structure="${structure}\n#### Imports\n\`\`\`java\n${IMPORTS}\n\`\`\`\n"

      # Extract class/interface defs
      CLASSES=$(grep -oE "^(public |private |protected )?(class|interface) [a-zA-Z0-9_]+" "$file" 2>/dev/null | sed 's/class //; s/interface //; s/public //; s/private //; s/protected //' | tr '\n' ', ' | sed 's/, $//')
      [[ -n "$CLASSES" ]] && structure="${structure}\n#### Classes/Interfaces\n$CLASSES\n"

      # Extract method defs
      FUNCTIONS=$(grep -oE "(public|private|protected).*\(.*\)" "$file" 2>/dev/null | head -10 | tr '\n' ', ' | sed 's/, $//')
      [[ -n "$FUNCTIONS" ]] && structure="${structure}\n#### Methods\n$FUNCTIONS\n"
      ;;

    *)
      structure="\n*Source file ($(wc -l < "$file" 2>/dev/null || echo 0) lines)*"
      ;;
  esac

  echo -e "$structure"
}
```

For each discovered item, generate a tree-view document following this structure:

#### File-Level Tree

**Source file decomposition** (run `decompose_source()` above, insert results here):

```markdown
# Component: <filename>

**Path:** `relative/path/to/file.ext`
**Type:** File | Directory | Module | Service | Component
**Maps to:** `.discovery/<NNN>-<name>.md`
**Dependencies:** [list of imported files with links]
**Dependents:** [list of files that import this, with links]

## Decomposition

<INSERT decompose_source() output here — Imports, Functions, Classes, Types, Globals>

Example for a TypeScript file:
#### Imports
```javascript
import { UserService } from './services/user'
import type { User } from './types'
```

#### Exports
```javascript
export function createUser()
export class UserManager
```

#### Functions
createUser, deleteUser, updateUser

#### Classes
UserManager, UserValidator

#### Types/Interfaces
User, CreateUserInput, UpdateUserInput

#### Global Variables
API_BASE_URL, DEFAULT_TIMEOUT

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

## Phase3: Cross-Reference Generation

After mapping all components, generate cross-references:

1. Track every import/require statement across all files.
2. Build a dependency graph showing which components depend on which.
3. Identify circular dependencies.
4. Identify orphan files (not imported by anything).
5. Identify entry points (imported by nothing, but referenced in build config).
