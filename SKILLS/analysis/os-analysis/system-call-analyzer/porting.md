---
name: syscall-porting
description: Cross-platform syscall porting — syscall matrix, Linux-to-BSD/macOS/Windows mappings, replacement libraries.
---

# System Call Analyzer — Porting Analysis

## 9. Porting Analysis

### 9.1 System Call Porting Matrix

```markdown
## Common Porting Issues

| Linux | FreeBSD | macOS | Windows | Solution |
|-------|---------|-------|---------|----------|
| epoll | kqueue | kqueue | IOCP | Use libevent |
| inotify | kqueue | FSEvents | ReadDirectoryChangesW | Use library |
| /proc | /proc (limited) | no | (Registry) | Use library |
| /dev/shm | /tmp | /tmp | (no) | Use mkstemp |
| eventfd | kqueue | (via pipe) | (no) | Use pipe |
| timerfd | kqueue | (via libdispatch) | (no) | Use library |

## Replacement Libraries

| Linux | Portable Alternative |
|-------|---------------------|
| epoll | libevent, libev |
| inotify | libevent (kqueue backend) |
| /proc filesystem | sysctl ( BSD), sysinfo (all) |
| eventfd | pipe() |
| timerfd | setitimer or libdispatch |
| tee() | splice() with /dev/null |
```

### 9.2 Syscall Discovery Template

```markdown
## System Call Analysis

### Application: <Name>
### Target OS: <Target>
### Source OS: <Source>

### Identified System Calls

| Category | Call | Source Location | Porting Strategy |
|----------|------|-----------------|------------------|
| File I/O | open | file.c:42 | Portable |
| File I/O | O_DIRECT | file.c:45 | Remove or conditional |
| Memory | mmap (MAP_HUGETLB) | mem.c:20 | Use mmap with large pages |
| Process | clone | proc.c:15 | Use pthread on all |
| Network | epoll_create | net.c:30 | Use libevent |
| IPC | eventfd | ipc.c:10 | Use pipe |
| Time | clock_gettime(CLOCK_BOOTTIME) | time.c:8 | Use CLOCK_MONOTONIC |

### OS-Specific Code Locations

| File | Line | OS-Specific Feature |
|------|------|---------------------|
| file.c | 42 | O_DIRECT flag |
| net.c | 30 | epoll_wait |
| ipc.c | 10 | eventfd |

### Recommendations
1. Replace epoll with libevent for cross-platform
2. Remove O_DIRECT - not portable
3. Use pthread for thread creation instead of clone
```
