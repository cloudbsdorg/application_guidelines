# Codebase Skill

## Metadata
```
author: Mark LaPointe <mark@cloudbsd.org>
version: 1.0.0
platform: CloudBSD / FreeBSD
triggers:
  - "understand"
  - "explore"
  - "codebase"
  - "find in code"
  - "trace"
  - "where is"
  - "how does"
  - "what does"
```

## Purpose

Read-only codebase exploration and analysis. Understand structure, patterns, and behavior WITHOUT making changes.

## Exploration Protocol

### Phase 1: Orient
- What language(s) and framework(s)?
- What's the directory structure?
- Where is the entry point?
- What are the main modules?

### Phase 2: Trace
- Find the code that does X
- Follow the call chain
- Identify data flow
- Map dependencies

### Phase 3: Document (Mentally)
- How it works (in your head)
- Key files and their roles
- Patterns in use
- FreeBSD integration points

## FreeBSD Codebase Exploration

### Finding Kernel Code
```
/usr/src/sys/          # Kernel source
/usr/src/sys/kern/    # Core kernel
/usr/src/sys/dev/     # Device drivers
```

### Finding Userland Code
```
/usr/src/bin/          # Userland binaries
/usr/src/usr.bin/      # More utilities
/usr/src/lib/          # Libraries
```

### Useful Commands
```bash
# Find function definition
grep -n "^$FUNC()" /usr/src/sys/kern/*.c

# Find file in src tree
find /usr/src -name "$FILE" -type f

# Trace system calls
ktrace -i -t c -c $PROGRAM

# DTrace for runtime
dtrace -n 'syscall:::entry { @[execname] = count(); }'
```

## Codebase Patterns

### Structural Patterns
- **Monolith**: Single large codebase
- **Modular**: Clear separation of concerns
- **Microservices**: Distributed across processes
- **Layered**: Clear hierarchy (app → domain → infra)

### FreeBSD Patterns
- **rc.d scripts**: Service lifecycle in `/etc/rc.d/`
- **Kernel modules**: `.ko` files loaded via `kldload`
- **Device drivers**: Attach via `device_if.m` or `DEV_MATCH`
- **ZFS datasets**: Dataset hierarchy under `tank/`

## Output Format

```
## Codebase Overview: [Project Name]

**Language**: [Language]
**Framework**: [If applicable]
**Structure**: [Monolith/Modular/etc]

**Entry Point**: [Main file]
**Key Modules**:
- `module/file`: [Purpose]

**FreeBSD Integration**:
- Services: [rc.d scripts]
- Kernel: [Modules if applicable]
- Storage: [ZFS datasets if applicable]

**Key Patterns**:
- [Pattern 1]
- [Pattern 2]

**Notable Findings**:
- [Interesting thing 1]
- [Interesting thing 2]
```

## Anti-Patterns

- Do NOT make changes during exploration
- Do NOT run commands that modify state
- Do NOT assume without reading code
- Do NOT summarize without evidence

## Completion

- [ ] Project structure understood
- [ ] Key files identified
- [ ] Data flow traced (if requested)
- [ ] FreeBSD integration points identified
- [ ] Findings documented in output format
