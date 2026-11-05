---
name: process-model-overview
description: Process model overview — process vs thread comparison, threads vs coroutines, goroutine scheduler diagram.
---

# Process Model Analyzer — Overview

## 1. Process Model Overview

### 1.1 Process vs Thread

```markdown
## Process

| Aspect | Description |
|--------|-------------|
| Definition | Running instance of a program with its own memory space |
| Memory | Separate address space, cannot access another's memory |
| Creation | fork(), CreateProcess() |
| Communication | Pipes, sockets, message queues, shared memory |
| Overhead | Higher (copy-on-write for fork) |
| Isolation | Strong - crash in one doesn't affect others |

## Thread

| Aspect | Description |
|--------|-------------|
| Definition | Lighter-weight execution unit within a process |
| Memory | Shares process memory space with other threads |
| Creation | pthread_create(), CreateThread() |
| Communication | Direct memory access, mutexes, condition variables |
| Overhead | Lower (no memory copy) |
| Isolation | Weak - crash can crash entire process |

## Process vs Thread Diagram

```
Process A                           Process B
┌────────────────────────┐          ┌────────────────────────┐
│  Thread 1  ─┐          │          │  Thread 1              │
│  Thread 2  ├─ Shared   │          │  Thread 2              │
│  Thread 3  │  Memory   │          │                        │
│            │  (heap,    │          │                        │
│  Stack A1  │   globals) │          │                        │
│  Stack A2  │           │          │                        │
│  Stack A3  │           │          │                        │
└────────────────────────┘          └────────────────────────┘
     ↑ Separate                      ↑ Separate
     Address Spaces                    Address Spaces
```

### 1.2 Thread vs Coroutine

```markdown
## Threads vs Coroutines

| Aspect | Threads | Coroutines |
|--------|---------|------------|
| Scheduling | Preemptive (OS decides) | Cooperative (code decides) |
| Parallelism | True parallelism (multi-core) | Single-threaded usually |
| Stack | Separate stack per thread (MB) | Lightweight (KB), on heap |
| Context switch | Expensive (kernel involvement) | Cheap (just stack pointer) |
| Use case | CPU-bound, parallelism | I/O-bound, async flows |
| Blocking | Can block entire thread | Yields at await points |

## Goroutine (Go) vs Thread

```go
// Goroutines - managed by Go runtime
go func() { doWork() }()  // Stack starts at 2KB, grows to max
// Go multiplexes thousands of goroutines onto few OS threads

// Threads - OS managed
pthread_create(&tid, NULL, doWork, NULL);  // Stack typically 8MB
// Each thread is 1:1 with OS thread
```

## Goroutine Scheduler

```
┌─────────────────────────────────────────────────────┐
│                  Go Scheduler                        │
│                                                     │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐            │
│  │  OS     │  │  OS     │  │  OS     │  ← OS Threads │
│  │ Thread 1│  │ Thread 2│  │ Thread 3│            │
│  └────┬────┘  └────┬────┘  └────┬────┘            │
│       │            │            │                   │
│   ┌───┴───┐    ┌───┴───┐    ┌───┴───┐            │
│   │G G G G│    │G G G G│    │G G G G│  ← Goroutines │
│   │G G    │    │  G G  │    │G G G  │    (multiplexed) │
│   └───────┘    └───────┘    └───────┘            │
│   Run Queue    Run Queue    Run Queue              │
└─────────────────────────────────────────────────────┘
```
