---
name: sysctl-documenter
description: >-
  Document a sysctl MIB hierarchy in the standard CloudBSD format. Use when
  defining or describing kernel tunables and configuration interfaces exposed
  through sysctl, including the 501 series planning document.
keywords:
  - sysctl
  - MIB
  - kernel parameter
  - tunable
  - 501 document
---

# Skill: sysctl-documenter

**Purpose:** Document sysctl MIB hierarchies in the standard CloudBSD format.

**Triggers:** When defining configuration interfaces, documenting sysctl nodes, or creating the 501 document.

## Loading Instructions

Load this skill when the user asks you to:
- Document sysctl interfaces
- Create the 501-<Project>-Sysctl-Interface.md
- Define a new sysctl namespace
- Document state enumerations

## Sysctl Namespace Convention

All CloudBSD project sysctls live under:

```
net.graph.<project>.<node>
```

## Document Format

### Sysctl Table

```markdown
### net.graph.<project>

| Node | Type | Default | Range | Description |
|------|------|---------|-------|-------------|
| `net.graph.<project>.enable` | int | 0 | {0,1} | Enable/disable the project |
| `net.graph.<project>.mode` | int | 0 | {0,1,2} | Algorithm selection |
| `net.graph.<project>.max_workers` | int | 16 | 1-256 | Maximum concurrent workers |
| `net.graph.<project>.timeout` | int | 300 | 1-3600 | Operation timeout in seconds |
```

### State Enumeration Table

```markdown
### Worker States

| Value | State | Description |
|-------|-------|-------------|
| 0 | `ACTIVE` | Worker is active and processing |
| 1 | `DRAINING` | Graceful shutdown in progress |
| 2 | `PENDING_REMOVAL` | Marked for removal |
```

### Algorithm Enumeration Table

```markdown
### Load Balancing Algorithms

| Value | Algorithm | Description |
|-------|-----------|-------------|
| 0 | `ROUND_ROBIN` | Cyclic distribution |
| 1 | `HASH` | Session hash-based |
| 2 | `LEAST_LOADED` | Minimum active sessions |
```

## Required Fields Per Sysctl Node

| Field | Description |
|-------|-------------|
| Node | Full sysctl name with path |
| Type | int, string, uint64, etc. |
| Default | Default value |
| Range | Valid range or set of values |
| Description | Clear description of effect |

## Common Patterns

### Binary Enable/Disable

```markdown
| `net.graph.<project>.enable` | int | 0 | {0,1} | 0=disabled, 1=enabled |
```

### Numeric Limit

```markdown
| `net.graph.<project>.max_connections` | int | 1024 | 1-65535 | Maximum connections |
```

### Timeout

```markdown
| `net.graph.<project>.session_timeout` | int | 3600 | 60-86400 | Session timeout in seconds |
```

### Read-Only Statistics

```markdown
| `net.graph.<project>.stat.active_workers` | uint64 | N/A | RO | Current active workers |
| `net.graph.<project>.stat.total_sessions` | uint64 | N/A | RO | Total sessions processed |
```

## Hierarchical Structure

For nested sysctls:

```markdown
### net.graph.<project>

| Node | Type | Default | Range | Description |
|------|------|---------|-------|-------------|

### net.graph.<project>.worker

| Node | Type | Default | Range | Description |
|------|------|---------|-------|-------------|

### net.graph.<project>.worker.<id>

| Node | Type | Default | Range | Description |
|------|------|---------|-------|-------------|
```

## OID Convention

For SNMP integration, document OIDs:

```markdown
### OID Mapping

| Sysctl | OID | Type |
|--------|-----|------|
| net.graph.<project>.enable | 1.3.6.1.4.1.1234.1.1 | Integer |
```

## Validation Script Template

```bash
#!/bin/sh
# Validate sysctl hierarchy

echo "Checking net.graph.<project> sysctls..."

# Check type
type=$(sysctl -n net.graph.<project>.enable 2>/dev/null)
if [ $? -ne 0 ]; then
    echo "ERROR: net.graph.<project>.enable not found"
    exit 1
fi

echo "net.graph.<project>.enable = $type"
echo "Validation passed"
```

## Reference

See Planning/PLANNING.md Section 9 (Sysctl Interface Conventions) for full specification.