---
name: security document generator
description: Create security documentation following the CloudBSD security series standard (1.1-1.6).
---

# Skill: security-document-generator

**Purpose:** Create security documentation following the CloudBSD security series standard (1.1-1.6).

**Triggers:** When creating security documents, threat models, access control documentation, or security implementation plans.

## Loading Instructions

Load this skill when the user asks you to:
- Create security documentation
- Document threat models
- Design access control systems
- Create security implementation tasks
- Document Capsicum sandboxing

## Document Series Overview

The security documentation is split into 6 parts:

| Document | Topic | Purpose |
|----------|-------|---------|
| `1.1` | Threat Model & Isolation | Security overview and threat analysis |
| `1.2` | Access Control & Authorization | Permissions and privileges |
| `1.3` | Custom Emulator Security | Deep-dive on emulator-specific security |
| `1.4` | Filesystem, Devices & Crash Safety | Runtime security |
| `1.5` | Additional Security Analysis | Audit, MAC, hardening |
| `1.6` | Security Implementation | Task tables for security work |

---

## 1.1 Threat Model & Isolation

### Template

```markdown
# <Project> — Threat Model & Isolation

**Document ID:** <Project>-Security-ThreatModel
**Version:** 1.0
**Last Updated:** YYYY-MM-DD
**Maintainer:** <Team>
**Status:** ACTIVE
**Classification:** CONFIDENTIAL

---

## Executive Summary

<Brief overview of security approach and key principles>

## Assets to Protect

| Asset | Classification | Protection Goal |
|-------|---------------|----------------|
| Host kernel memory | Critical | No read/write from guest |
| Userspace processes | Critical | No injection or manipulation |
| Filesystem | High | Guest cannot escape shares |
| Network | High | No unauthorized external access |
| Instance memory | Medium | Isolated between instances |

## Threat Categories

| Category | Description | Example |
|----------|-------------|---------|
| Emulator Escape | Break out of emulation layer | Jump to host code |
| VMM Escape | Break out of VM | Access host resources |
| Instruction Exploit | Malicious instruction causing host crash | Triple fault |
| Memory Corruption | Guest corrupting host memory | Out-of-bounds write |
| Filesystem Escape | Guest accessing host outside shares | Symlink traversal |
| Resource Exhaustion | Guest consuming all host resources | Memory leak, fork bomb |

## Trust Model

| Level | Entity | Trust | Justification |
|-------|--------|-------|---------------|
| T0 | Host kernel | Full trust | Root of trust |
| T1 | Hypervisor (bhyve) | High trust | Isolated VM |
| T2 | Emulation framework | Medium trust | Userland with sandbox |
| T3 | Guest instance | Untrusted | Potentially malicious |
| T4 | External network | Untrusted | Attack vector |

## Isolation Architecture

### bhyve Path

```
Host Kernel (T0)
    │
    ├── bhyve/VMM (T1) ─── Isolated VM
    │
    └── Emulation Framework (T2) ─── Sandboxed
```

### Custom Emulator Path

```
Host Kernel (T0)
    │
    └── Emulation Framework (T2) ─── Capsicum Sandboxed
              │
              └── Guest Instance (T3) ─── Untrusted
```

## Process-Level Isolation

- Each instance runs in isolated process context
- Capsicum capability mode after initialization
- No shared memory between instances
- Network access restricted to configured mode

## Multi-Instance Isolation

- Per-instance ucred tracking
- Instance-visible filtering in listings
- Resource limits per user/group
- No cross-instance memory access

## Kernel Module Security

- Module refcount prevents unload with active instances
- Sysctl tree requires privilege to modify
- No runtime code loading from guest
- Static analysis required before kernel commit

---

## Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | YYYY-MM-DD | Name | Initial version |

**Last Updated:** YYYY-MM-DD HH:MM UTC
**Classification:** CONFIDENTIAL
```

---

## 1.2 Access Control & Authorization

### Template

```markdown
# <Project> — Access Control & Authorization

**Document ID:** <Project>-Security-AccessControl
**Version:** 1.0
**Last Updated:** YYYY-MM-DD
**Maintainer:** <Team>
**Status:** ACTIVE
**Classification:** CONFIDENTIAL

---

## Group Configuration

| Setting | Value | Purpose |
|---------|-------|---------|
| GID_EMU | 979 | Emulation operator group |
| Group name | `emu` | Human-readable name |

### Adding Users to emu Group

```bash
pw groupmod emu -m username
# or
pw groupadd emu -g 979
```

## Ownership Model

| Entity | Owner | Permissions |
|--------|-------|-------------|
| Instance | Creator (uid) | Full control |
| Instance | Root | Full control |
| Instance | emu group | Operational control |
| Other users | None | No access |

## Privilege Definitions

| Privilege | Value | Description |
|-----------|-------|-------------|
| PRIV_EMU_CREATE | 720 | Create new instances |
| PRIV_EMU_DESTROY | 721 | Destroy any instance |
| PRIV_EMU_MODIFY | 722 | Modify own instances |
| PRIV_EMU_ADMIN | 723 | Modify any instance |
| PRIV_EMU_AUDIT | 724 | View all instances |
| PRIV_EMU_BLOB | 725 | Load firmware blobs |

## Permission Matrix

| Operation | Root | emu group | Owner | Other |
|-----------|------|-----------|-------|-------|
| Create instance | ✅ | ✅ (via PRIV_EMU_CREATE) | ❌ | ❌ |
| Destroy own | ✅ | ✅ | ✅ | ❌ |
| Destroy any | ✅ | ❌ | ❌ | ❌ |
| Modify own | ✅ | ✅ | ✅ | ❌ |
| Modify any | ✅ | ❌ | ❌ | ❌ |
| View all | ✅ | ✅ (via PRIV_EMU_AUDIT) | Own only | ❌ |

## Sysctl Interface

```bash
# Enable non-root access
sysctl kern.emulation.allow_nonroot=1

# Require emu group
sysctl kern.emulation.require_group=1
```

## Jail Integration

| Flag | Value | Purpose |
|------|-------|---------|
| PR_ALLOW_EMULATION | 0x01000000 | Permit emulation in jail |

---

## Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | YYYY-MM-DD | Name | Initial version |

**Last Updated:** YYYY-MM-DD HH:MM UTC
**Classification:** CONFIDENTIAL
```

---

## 1.3 Custom Emulator Security

### Template

```markdown
# <Project> — Custom Emulator Security

**Document ID:** <Project>-Security-Emulator
**Version:** 1.0
**Last Updated:** YYYY-MM-DD
**Maintainer:** <Team>
**Status:** ACTIVE
**Classification:** CONFIDENTIAL

---

## Attack Surface Analysis

| Component | Attack Surface | Mitigations |
|-----------|---------------|-------------|
| Instruction decoder | Malicious instructions | Bounds checking, length limits |
| Memory access | Out-of-bounds read/write | Bounds validation |
| ELF loader | Crafted ELF files | Strict validation |
| Syscall interface | Escaped syscalls | Capsicum sandbox |
| Device MMIO | Malicious device access | MMIO validation framework |

## Instruction Decoder Safety

### Length Limits

| Architecture | Max Instruction Length | Justification |
|--------------|----------------------|---------------|
| x86-64 | 15 bytes | Intel SDM limit |
| ARM64 | 4 bytes | Fixed-length ISA |
| RISC-V | 4 bytes (base) | RISC-V spec |

### Bounds Checking

```c
// Required pattern for all memory accesses
if (!emu_mem_check_bounds(addr, size, inst))
    return EMU_ERR_OUT_OF_BOUNDS;
```

## Memory Safety

### Bounds-Checked Accessors

| Function | Purpose |
|----------|---------|
| `emu_mem_check_bounds()` | Validate address range |
| `emu_mem_read()` | Safe read with bounds check |
| `emu_mem_write()` | Safe write with bounds check |

### Overflow Detection

```c
// Required for all size calculations
if (addr + size < addr) // overflow
    return EMU_ERR_OVERFLOW;
```

## ELF Loader Validation

| Check | Purpose |
|-------|---------|
| Magic number (0x7F ELF) | Verify ELF format |
| Class (32/64 bit) | Match architecture |
| Endianness | Match guest endianness |
| Machine type | Match target arch |
| Segment bounds | No out-of-range loads |
| Segment overlap | No memory corruption |

## Capsicum Sandboxing

### Sandbox Architecture

```
emu_init()
    │
    ├── Initialize subsystems
    │
    ├── Enter capability mode
    │   └── cap_enter()
    │
    └── Drop privileges
        └── cap_rights_limit()
```

### Required FD Rights

| Operation | Required Rights |
|-----------|-----------------|
| Memory access | CAP_READ, CAP_MMAP |
| Console output | CAP_WRITE |
| Instance control | CAP_IOCTL |

---

## Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | YYYY-MM-DD | Name | Initial version |

**Last Updated:** YYYY-MM-DD HH:MM UTC
**Classification:** CONFIDENTIAL
```

---

## 1.4 Filesystem, Devices & Crash Safety

### Template

```markdown
# <Project> — Filesystem, Devices & Crash Safety

**Document ID:** <Project>-Security-Runtime
**Version:** 1.0
**Last Updated:** YYYY-MM-DD
**Maintainer:** <Team>
**Status:** ACTIVE
**Classification:** CONFIDENTIAL

---

## Filesystem Security

### Path Validation Rules

| Check | Blocked Patterns | Purpose |
|-------|-----------------|---------|
| Absolute path | `/dev/*`, `/proc/*`, `/sys/*` | Prevent device access |
| Symlink | `..`, `/tmp/../` | Prevent escape |
| Realpath | After open(), verify still in allowed area | TOCTOU protection |

### Share Path Format

```
host_path:guest_path[:ro|rw]
```

### Security Checklist

- [ ] Blocked prefixes checked
- [ ] realpath() resolution
- [ ] Post-open verification
- [ ] Read-only enforcement
- [ ] TOCTOU protection

## Device Attack Surface

| Device | Risk | Mitigation |
|--------|------|------------|
| UART | Data exfiltration | Console-only output |
| virtio-blk | Path traversal | Path validation |
| virtio-net | Network escape | Host-only mode default |
| virtio-9p | Filesystem escape | Restricted shares |
| GDB stub | Remote code execution | Localhost-only binding |

## Crash Containment

### Crash Detection

| Trigger | Detection Method | Action |
|---------|-----------------|--------|
| Triple fault | CPU exception | Terminate instance |
| Invalid opcode | CPU exception | Terminate instance |
| Memory violation | Bounds check | Return error |
| Watchdog timeout | Timer | Terminate instance |

### Host Safety During Crash

- Guest cannot corrupt host memory
- Guest cannot access host filesystem
- Guest cannot access host network
- Crash does not panic host kernel

---

## Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | YYYY-MM-DD | Name | Initial version |

**Last Updated:** YYYY-MM-DD HH:MM UTC
**Classification:** CONFIDENTIAL
```

---

## 1.5 Additional Security Analysis

### Template

```markdown
# <Project> — Additional Security Analysis

**Document ID:** <Project>-Security-Additional
**Version:** 1.0
**Last Updated:** YYYY-MM-DD
**Maintainer:** <Team>
**Status:** ACTIVE
**Classification:** CONFIDENTIAL

---

## Audit Logging

### Event Categories

| Category | Events |
|----------|--------|
| Instance lifecycle | create, start, stop, destroy |
| Security | auth_success, auth_failure, privilege_use |
| Resource | limit_exceeded, quota_exceeded |
| System | module_load, module_unload |

## MAC Framework Integration

### Label Propagation

- MAC label from creator inherited by instance
- Enforced on share/snapshot operations
- Veriexec integration for emulator binaries

## Securelevel Integration

| Securelevel | Restrictions |
|-------------|---------------|
| -1 | Perrasive (devfs rules) |
| 0 | Insecure (default for VMs) |
| 1 | Secure (no kernel module loading) |
| 2 | Highly secure (no raw disk) |

## Memory Scrubbing

On instance destroy:
1. Zero all guest memory pages
2. Zero CPU registers
3. Clear any cached credentials
4. Release all resources

## Core Dump Prevention

```c
setrlimit(RLIMIT_CORE, &(struct rlimit){0, 0});
procctl(PROC_COREDUMP_CTL, PROC_COREDUMP_DISABLE);
```

## ptrace Prevention

```c
procctl(PROC_TRACE_CTL, PROC_TRACE_CTL_DISABLE);
```

## OOM Killer Interaction

```c
procctl(PROC_OOMADJ_CTL, PROC_OOMADJ_MIN); // Least likely to be killed
```

---

## Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | YYYY-MM-DD | Name | Initial version |

**Last Updated:** YYYY-MM-DD HH:MM UTC
**Classification:** CONFIDENTIAL
```

---

## 1.6 Security Implementation

### Template

```markdown
# <Project> — Security Implementation

**Document ID:** <Project>-Security-Implementation
**Version:** 1.0
**Last Updated:** YYYY-MM-DD
**Maintainer:** <Team>
**Status:** ACTIVE
**Classification:** CONFIDENTIAL

---

## Security Recommendations Summary

| Category | Recommendation | Priority |
|----------|--------------|----------|
| Isolation | Capsicum sandboxing | P0 |
| Memory | Bounds-checked access | P0 |
| ELF | Strict validation | P0 |
| Access | Root-only by default | P0 |
| Filesystem | Path validation | P1 |
| Devices | MMIO validation | P1 |
| Audit | Syslog + file logging | P2 |

## Implementation Phases

### Phase S0: Kernel Module Security

| # | Task | Priority | Status | Assigned To | Files |
|---|------|----------|--------|-------------|-------|
| S0.1 | Implement modevent handler | P0 | ⬜ PENDING | | `emu_core.c` |

### Phase S1: Core Security Infrastructure

| # | Task | Priority | Status | Assigned To | Files |
|---|------|----------|--------|-------------|-------|
| S1.1 | Bounds-checked memory access | P0 | ⬜ PENDING | | `emu_mem.c` |

---

## Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | YYYY-MM-DD | Name | Initial version |

**Last Updated:** YYYY-MM-DD HH:MM UTC
**Classification:** CONFIDENTIAL
```

---

## Reference

See [Planning/PLANNING.md](../Planning/PLANNING.md) Section 3.4 for the full security documentation specification.

See [Kernel Emulation Framework Security Docs](https://github.com/cloudbsdorg/freebsd-src-build-emulation/tree/main/.plan) for complete examples.