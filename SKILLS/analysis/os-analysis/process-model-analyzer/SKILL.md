---
name: process model analyzer
description: Systematically analyze application process models, threading, and inter-process communication patterns for cross-platform porting.
---

# Skill: process-model-analyzer

**Purpose:** Systematically analyze application process models, threading, and inter-process communication patterns for cross-platform porting.

**Triggers:** When analyzing applications with complex process/thread models, or when porting between platforms with different process models.

---

## Loading Instructions

This skill is **modular**. Load only the sub-skill you need:

| Sub-Skill | When to Load |
|-----------|--------------|
| [overview.md](./overview.md) | Process vs thread, coroutines, goroutines |
| [processes.md](./processes.md) | Fork/exec, spawn, POSIX spawn |
| [threads.md](./threads.md) | Pthreads, thread pools, parallelism models |
| [synchronization.md](./synchronization.md) | Mutex, condition variables, semaphores, spinlocks |
| [ipc.md](./ipc.md) | Pipes, shared memory, message queues, Unix sockets |
| [groups.md](./groups.md) | Process groups, sessions, daemon patterns |
| [async.md](./async.md) | Event loop, select/poll/epoll |

---

## Loading This Skill

Load this skill when the user asks you to:
- Analyze process creation patterns
- Understand threading models
- Document IPC mechanisms
- Plan parallel/concurrent porting
- Map thread/process dependencies

---

## Quick-Scan Index

### By Category

| Need | Sub-Skill |
|------|-----------|
| Process vs thread concepts | [overview.md](./overview.md) |
| Process creation (fork/exec) | [processes.md](./processes.md) |
| Threading/pthread patterns | [threads.md](./threads.md) |
| Synchronization primitives | [synchronization.md](./synchronization.md) |
| IPC mechanisms | [ipc.md](./ipc.md) |
| Process groups/sessions | [groups.md](./groups.md) |
| Event-driven patterns | [async.md](./async.md) |

---

## Reference

See system-call-analyzer for low-level system call dependencies.
