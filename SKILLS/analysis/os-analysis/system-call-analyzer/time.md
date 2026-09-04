---
name: syscall-time
description: Time system calls — gettimeofday, clock_gettime, nanosleep, timer_create, clock types across OSes.
---

# System Call Analyzer — Time Operations

## 7. Time Operations

### 7.1 Time Syscalls

```markdown
## Time System Calls

| Call | Linux | FreeBSD | macOS | Description |
|------|-------|---------|-------|-------------|
| gettimeofday | yes | yes | yes | Wall clock (deprecated) |
| clock_gettime | yes | yes | yes | Monotonic clock |
| time | yes | yes | yes | Simple time |
| nanosleep | yes | yes | yes | High-precision sleep |
| usleep | yes (deprecated) | yes | yes | Microsecond sleep |
| alarm | yes | yes | yes | SIGALRM |
| setitimer | yes | yes | yes | Interval timer |
| timer_create | yes | yes | yes | POSIX timers |

## Clock Types

```c
// POSIX clock types
struct timespec ts;

// CLOCK_REALTIME - wall clock, can be set by admin
clock_gettime(CLOCK_REALTIME, &ts);

// CLOCK_MONOTONIC - not settable, for measuring elapsed time
clock_gettime(CLOCK_MONOTONIC, &ts);

// CLOCK_PROCESS_CPUTIME_ID - per-process CPU time
clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &ts);

// CLOCK_THREAD_CPUTIME_ID - per-thread CPU time
clock_gettime(CLOCK_THREAD_CPUTIME_ID, &ts);

// macOS-specific
clock_gettime(CLOCK_UPTIME_RAW, &ts);  // FreeBSD also
```
