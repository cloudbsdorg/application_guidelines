---
name: system-call-analyzer
description: >-
  Document the system calls an application depends on and how they map across
  operating systems. Use when porting low-level code to FreeBSD, when a Linux-
  only syscall must be replaced, or when analysing file I/O, memory, signals,
  or process syscalls.
---

# Skill: system-call-analyzer

**Purpose:** Systematically analyze application system calls to understand OS-level dependencies and enable cross-platform porting.

**Triggers:** When porting applications between Linux, BSD, macOS, Windows, or when needing to understand low-level OS interactions.

---

## Loading Instructions

This skill is **modular**. Load only the sub-skill you need:

| Sub-Skill | When to Load |
|-----------|--------------|
| [overview.md](./overview.md) | Syscall overview, tracing tools |
| [file-io.md](./file-io.md) | File operations, flags, descriptors |
| [memory.md](./memory.md) | mmap, memory operations, malloc internals |
| [process.md](./process.md) | Fork/exec, process lifecycle |
| [signals.md](./signals.md) | Signal handling, async-signal-safe |
| [network.md](./network.md) | Socket operations |
| [time.md](./time.md) | Time syscalls, clocks |
| [ipc.md](./ipc.md) | Pipes, shared memory, message queues |
| [porting.md](./porting.md) | Cross-platform syscall matrix |
| [debugging.md](./debugging.md) | GDB, LLDB, core dumps, ASAN |

---

## Loading This Skill

Load this skill when the user asks you to:
- Analyze system call dependencies
- Identify OS-specific code paths
- Plan cross-platform adaptations
- Trace kernel interactions
- Document kernel APIs used

---

## Quick-Scan Index

### By Category

| Need | Sub-Skill |
|------|-----------|
| Syscall overview/tracing | [overview.md](./overview.md) |
| File I/O syscalls | [file-io.md](./file-io.md) |
| Memory operations | [memory.md](./memory.md) |
| Process creation | [process.md](./process.md) |
| Signal handling | [signals.md](./signals.md) |
| Network sockets | [network.md](./network.md) |
| Time/clocks | [time.md](./time.md) |
| IPC mechanisms | [ipc.md](./ipc.md) |
| Cross-platform porting | [porting.md](./porting.md) |
| Debugging tools | [debugging.md](./debugging.md) |

---

## Reference

See process-model-analyzer for process/thread creation patterns.
