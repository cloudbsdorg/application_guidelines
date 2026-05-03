---
name: quick reference generator
description: Create and maintain Quick Reference sections for agent entry point documents.
---

# Skill: quick-reference-generator

**Purpose:** Create and maintain Quick Reference sections for agent entry point documents.

**Triggers:** When creating AGENTS_START_HERE.md, or when key files/sysctls/commands change.

## Loading Instructions

Load this skill when the user asks you to:
- Create a Quick Reference section
- Update Quick Reference after code changes
- Generate a fast-lookup guide
- Document key files and commands

## Required Quick Reference Sections

1. **Key Files** — Important source files and their purposes
2. **Key Sysctls** — Common sysctl nodes with defaults and purposes
3. **Key Groups** — Relevant system groups and GIDs
4. **Key Commands** — Essential CLI commands with examples

## Key Files Table

```markdown
### Key Files

| File | Purpose |
|------|---------|
| `sys/module/foo/foo_mod.c` | Module entry point, module metadata |
| `sys/module/foo/foo_main.c` | Core implementation, sysctl tree |
| `sys/module/foo/foo_var.h` | Global variables and structures |
```

## Key Sysctls Table

```markdown
### Key Sysctls

| Sysctl | Type | Default | Purpose |
|--------|------|---------|---------|
| `net.graph.foo.enable` | int | 0 | Enable/disable module |
| `net.graph.foo.mode` | int | 0 | Operation mode (0=pass-through, 1=endpoint) |
| `net.graph.foo.max_workers` | int | 16 | Maximum concurrent workers |
| `net.graph.foo.timeout` | int | 30 | Worker timeout in seconds |
```

## Key Groups Table

```markdown
### Key Groups

| Group | GID | Purpose |
|-------|-----|---------|
| `operator` | 5 | Read-only access to management commands |
| `kmem` | 2 | Kernel memory access (required for debugging) |
| `wheel` | 0 | Administrative access |
```

## Key Commands Section

```markdown
### Key Commands

```bash
# Load the kernel module
sudo kldload foo

# Unload the kernel module
sudo kldunload foo

# Check if module is loaded
kldstat | grep foo

# View module sysctl tree
sysctl net.graph.foo

# Enable the module
sudo sysctl net.graph.foo.enable=1

# View runtime statistics
sysctl net.graph.foo.stats
```
```

## Auto-Generated Quick Reference Template

When generating for a new project, use this template:

```markdown
## Quick Reference

### Key Files

| File | Purpose |
|------|---------|
| `sys/module/<project>/<project>_mod.c` | Module entry point |
| `sys/module/<project>/<project>_main.c` | Core implementation |
| `usr.sbin/<project>_ctl/` | Userland management tool |

### Key Sysctls

| Sysctl | Default | Purpose |
|--------|---------|---------|
| `net.graph.<project>.enable` | 0 | Enable/disable |
| `net.graph.<project>.mode` | 0 | Operation mode |

### Key Groups

| Group | GID | Purpose |
|-------|-----|---------|
| `<project>` | (assigned) | Project-specific operations |

### Key Commands

```bash
# Load
sudo kldload <project>

# Configure
sudo sysctl net.graph.<project>.enable=1

# Check status
sysctl net.graph.<project>
```
```

## Validation Checklist

Before finalizing a Quick Reference:

- [ ] All file paths are accurate and match actual codebase
- [ ] Sysctl defaults are verified from source code
- [ ] Commands are tested or known to work
- [ ] GIDs are correct for the target FreeBSD version
- [ ] Format is consistent with other Quick Reference sections