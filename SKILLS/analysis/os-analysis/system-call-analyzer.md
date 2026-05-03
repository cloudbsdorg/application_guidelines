---
name: system call analyzer
description: Systematically analyze application system calls to understand OS-level dependencies and enable cross-platform porting.
---

# Skill: system-call-analyzer

**Purpose:** Systematically analyze application system calls to understand OS-level dependencies and enable cross-platform porting.

**Triggers:** When porting applications between Linux, BSD, macOS, Windows, or when needing to understand low-level OS interactions.

---

## Loading Instructions

This skill is **modular**. Load only the sub-skill you need:

| Sub-Skill | When to Load |
|-----------|--------------|
| [overview.md](./system-call/overview.md) | Syscall overview, tracing tools |
| [file-io.md](./system-call/file-io.md) | File operations, flags, descriptors |
| [memory.md](./system-call/memory.md) | mmap, memory operations, malloc internals |
| [process.md](./system-call/process.md) | Fork/exec, process lifecycle |
| [signals.md](./system-call/signals.md) | Signal handling, async-signal-safe |
| [network.md](./system-call/network.md) | Socket operations |
| [time.md](./system-call/time.md) | Time syscalls, clocks |
| [ipc.md](./system-call/ipc.md) | Pipes, shared memory, message queues |
| [porting.md](./system-call/porting.md) | Cross-platform syscall matrix |
| [debugging.md](./system-call/debugging.md) | GDB, LLDB, core dumps, ASAN |

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
| Syscall overview/tracing | [overview.md](./system-call/overview.md) |
| File I/O syscalls | [file-io.md](./system-call/file-io.md) |
| Memory operations | [memory.md](./system-call/memory.md) |
| Process creation | [process.md](./system-call/process.md) |
| Signal handling | [signals.md](./system-call/signals.md) |
| Network sockets | [network.md](./system-call/network.md) |
| Time/clocks | [time.md](./system-call/time.md) |
| IPC mechanisms | [ipc.md](./system-call/ipc.md) |
| Cross-platform porting | [porting.md](./system-call/porting.md) |
| Debugging tools | [debugging.md](./system-call/debugging.md) |

---

## Reference

See process-model-analyzer for process/thread creation patterns.
