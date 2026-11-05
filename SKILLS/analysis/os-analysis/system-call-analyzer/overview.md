---
name: syscall-overview
description: System call overview — syscall flow diagram, syscall numbers by OS/arch, tracing tools (strace, truss, dtruss).
---

# System Call Analyzer — Overview

## 1. System Call Overview

### 1.1 What is a System Call?

```markdown
## System Call Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Space                                │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Application                                                │   │
│  │  ┌───────────┐                                             │   │
│  │  │  printf() │ ← Library function (libc)                   │   │
│  │  └─────┬─────┘                                             │   │
│  │        │                                                   │   │
│  └────────┼───────────────────────────────────────────────────┘   │
│           │                                                     │
│           ▼ syscall instruction                                  │
├─────────────────────────────────────────────────────────────────┤
│                        Kernel Space                              │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  System Call Interface                                    │   │
│  │  ┌───────────────────────────────────────────────────┐  │   │
│  │  │  sys_write() → kernel buffer management          │  │   │
│  │  └───────────────────────────────────────────────────┘  │   │
│  │  ┌───────────────────────────────────────────────────┐  │   │
│  │  │  Virtual File System (VFS)                        │  │   │
│  │  └───────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 System Call Numbers

```markdown
## System Call Identification

| OS | Arch | open | read | write | socket | mmap |
|----|------|------|------|-------|--------|------|
| Linux x86_64 | amd64 | 2 | 0 | 1 | 41 | 9 |
| Linux ARM64 | arm64 | 56 | 63 | 64 | 198 | 222 |
| FreeBSD amd64 | amd64 | 5 | 3 | 4 | 97 | 477 |
| macOS x86_64 | x86_64 | 5 | 3 | 4 | 97 | 197 |
| macOS ARM64 | arm64 | 5 | 3 | 4 | 97 | 197 |
| Windows x64 | x64 | (NTCreateFile) | (NtReadFile) | (NtWriteFile) |
```

### 1.3 Tracing System Calls

```bash
# Linux: strace
strace -e trace=open,read,write, socket -f ./myapp

# Linux: see all system calls
strace -c ./myapp  # Summary counts

# FreeBSD: truss
truss -f -e ./myapp

# macOS: dtruss (requires sudo)
sudo dtruss -f ./myapp

# Windows: strace (via sysinternals)
procmon -i ./myapp

# Static analysis: find syscalls in binary
objdump -d ./myapp | grep -E "syscall|int 0x80|sysenter"
```
