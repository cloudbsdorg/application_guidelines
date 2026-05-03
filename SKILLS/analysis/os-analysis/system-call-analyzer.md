---
name: system call analyzer
description: Systematically analyze application system calls to understand OS-level dependencies and enable cross-platform porting.
---

# Skill: system-call-analyzer

**Purpose:** Systematically analyze application system calls to understand OS-level dependencies and enable cross-platform porting.

**Triggers:** When porting applications between Linux, BSD, macOS, Windows, or when needing to understand low-level OS interactions.

## Loading Instructions

Load this skill when the user asks you to:
- Analyze system call dependencies
- Identify OS-specific code paths
- Plan cross-platform adaptations
- Trace kernel interactions
- Document kernel APIs used

---

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

---

## 2. File Operations

### 2.1 Core File Syscalls

```markdown
## File System Calls

| Call | Purpose | Linux | FreeBSD | macOS | Windows |
|------|---------|-------|---------|-------|---------|
| open | Open file | yes | yes | yes | NtCreateFile |
| close | Close file descriptor | yes | yes | yes | NtClose |
| read | Read from fd | yes | yes | yes | NtReadFile |
| write | Write to fd | yes | yes | yes | NtWriteFile |
| lseek | Seek position | yes | yes | yes | NtSetInformationFile |
| stat | Get file metadata | yes | yes | yes | NtQueryInformationFile |
| access | Check permissions | yes | yes | yes | NtAccessCheck |
| unlink | Delete file | yes | yes | yes | NtSetInformationFile |

## open() Flags Comparison

```c
// POSIX
int fd = open(path, O_RDONLY | O_CREAT | O_EXCL, 0644);

// Linux-specific
int fd = open(path, O_RDWR | O_CREAT | O_DIRECT | O_NOATIME, 0644);

// macOS-specific
int fd = open(path, O_RDWR | O_CREAT | O_SHLOCK, 0644);

// FreeBSD-specific
int fd = open(path, O_RDWR | O_CREAT | O_EXLOCK, 0644);
```

### 2.2 File Descriptor Operations

```markdown
## File Descriptor Flags

| Flag | Linux | FreeBSD | macOS | Description |
|------|-------|---------|-------|-------------|
| O_NONBLOCK | yes | yes | yes | Non-blocking I/O |
| O_NOCTTY | yes | yes | yes | Don't become controlling TTY |
| O_CLOEXEC | yes | yes | yes | Close on exec |
| O_DIRECT | yes | yes (with compat) | no | Bypass page cache |
| O_NOATIME | yes | yes | no | Don't update atime |
| O_SHLOCK | no | no | yes | Shared lock |
| O_EXLOCK | no | no | yes | Exclusive lock |

## Portable open() Wrapper

```c
// Portable open with flags
int portable_open(const char *path, int flags, mode_t mode) {
    #ifdef __APPLE__
        flags |= O_SHLOCK;  // macOS
    #elif defined(__FreeBSD__)
        flags |= O_EXLOCK;  // FreeBSD
    #endif
    return open(path, flags, mode);
}
```

---

## 3. Memory Operations

### 3.1 Memory Mapping

```markdown
## mmap() Flags

| Flag | Linux | FreeBSD | macOS | Windows |
|------|-------|---------|-------|---------|
| MAP_ANONYMOUS | yes | yes | yes | (use VirtualAlloc) |
| MAP_SHARED | yes | yes | yes | (use CreateFileMapping + MapViewOfFile) |
| MAP_PRIVATE | yes | yes | yes | yes |
| MAP_FIXED | yes | yes | yes | yes |
| MAP_HUGETLB | yes | yes | no | no |
| MAP_NOCACHE | no | no | yes | no |
| MAP_STACK | yes | yes | yes | no |

## mmap() Usage Patterns

```c
// Anonymous mapping (Linux, BSD, macOS)
void *buf = mmap(NULL, size, PROT_READ | PROT_WRITE,
                 MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);

// File-backed mapping
void *buf = mmap(NULL, size, PROT_READ,
                 MAP_PRIVATE, fd, offset);

// Device memory (Linux specific - not portable)
void *dev = mmap(NULL, size, PROT_READ | PROT_WRITE,
                 MAP_SHARED, dev_fd, 0);

// Windows
void *buf = VirtualAlloc(NULL, size, MEM_COMMIT | MEM_RESERVE,
                         PAGE_READWRITE);
```

### 3.2 brk/sbrk (Legacy)

```markdown
## brk/sbrk vs mmap

| Aspect | brk/sbrk | mmap |
|--------|----------|------|
| Allocation | Contiguous heap | Any size, any alignment |
| Fragmentation | Can fragment | No internal fragmentation |
| Linux | Default for small | Default for large |
| FreeBSD | Supported | Preferred |
| macOS | Deprecated | Preferred |
| Windows | N/A | VirtualAlloc |

## malloc() Implementation

```markdown
## malloc() Internals

| Size Range | Linux | FreeBSD | macOS |
|-----------|-------|---------|-------|
| < 128B | brk arena | umem_cache | nano_malloc |
| 128B - 64KB | mmap (small) | umem_cache | small_malloc |
| > 64KB | mmap (large) | mmap | large_malloc |
```

---

## 4. Process Operations

### 4.1 Fork/Exec

```markdown
## Process Creation

| Call | Linux | FreeBSD | macOS | Windows |
|------|-------|---------|-------|---------|
| fork | yes | yes | yes | (CreateProcess) |
| vfork | yes | yes | yes | no |
| clone | yes | yes | yes | no |
| execve | yes | yes | yes | (CreateProcess) |
| posix_spawn | yes | yes | yes | no |

## Fork Semantics

```c
// POSIX fork
pid_t pid = fork();
if (pid == 0) {
    // Child process
    execve("/bin/sh", argv, envp);
} else if (pid > 0) {
    // Parent process
    waitpid(pid, &status, 0);
}

// Linux-specific clone (threads in same process)
clone(SIGCHLD, stack, CLONE_VM | CLONE_FS | CLONE_FILES, NULL);
```

### 4.2 Process Lifecycle

```markdown
## Process States

┌─────────┐
│  READY   │ ← Created or ready to run
└────┬────┘
     │ scheduler
     ▼
┌─────────┐     run      ┌──────────┐
│ RUNNING  │ ──────────► │ TERMINATED│
└────┬────┘             └───────────┘
     │ wait/I/O
     ▼
┌─────────┐
│ BLOCKED  │
└─────────┘
```

## Process Information

| Call | Linux | FreeBSD | macOS | Windows |
|------|-------|---------|-------|---------|
| getpid | yes | yes | yes | GetCurrentProcessId |
| getppid | yes | yes | yes | no |
| getuid | yes | yes | yes | no |
| getgid | yes | yes | yes | no |
| geteuid | yes | yes | yes | no |
| getegid | yes | yes | yes | no |
| getpriority | yes | yes | yes | no |
| nice | yes | yes | yes | (SetPriorityClass) |

---

## 5. Signal Handling

### 5.1 Signal Syscalls

```markdown
## Signal System Calls

| Call | Linux | FreeBSD | macOS | Description |
|------|-------|---------|-------|-------------|
| signal | yes | yes | yes | Set signal handler |
| sigaction | yes | yes | yes | Advanced signal handling |
| kill | yes | yes | yes | Send signal to process |
| sigprocmask | yes | yes | yes | Block/unblock signals |
| sigaltstack | yes | yes | yes | Alternative stack |
| raise | yes | yes | yes | Send signal to self |

## Signal Comparison

| Signal | Linux | FreeBSD | macOS | Default | Purpose |
|--------|-------|---------|-------|---------|---------|
| SIGTERM | yes | yes | yes | terminate | Graceful termination |
| SIGKILL | yes | yes | yes | terminate | Immediate kill |
| SIGINT | yes | yes | yes | terminate | Interrupt (Ctrl+C) |
| SIGUSR1 | yes | yes | yes | ignore | User-defined |
| SIGUSR2 | yes | yes | yes | ignore | User-defined |
| SIGHUP | yes | yes | yes | ignore | Hangup (reconf) |
| SIGPIPE | yes | yes | yes | terminate | Broken pipe |
| SIGCHLD | yes | yes | yes | ignore | Child exit |
| SIGSEGV | yes | yes | yes | core | Segfault |
| SIGBUS | yes | yes | yes | core | Bus error |
| SIGABRT | yes | yes | yes | core | Abort |
```

### 5.2 Signal Safety

```markdown
## Async-Signal-Safe Functions

These can be safely called from signal handlers:

| Function | Linux | FreeBSD | macOS |
|----------|-------|---------|-------|
| _exit | yes | yes | yes |
| abort | yes | yes | yes |
| kill | yes | yes | yes |
| getpid | yes | yes | yes |
| write | yes | yes | yes |
| open | yes | yes | yes |
| close | yes | yes | yes |
| read | yes | yes | yes |
| write | yes | yes | yes |
| malloc | no | no | no |
| printf | no | no | no |

## Signal-Safe Write Example

```c
// Signal-safe logging
volatile sig_atomic_t got_signal = 0;

void handler(int sig) {
    got_signal = 1;
}

int main() {
    struct sigaction sa = { .sa_handler = handler };
    sigaction(SIGUSR1, &sa, NULL);

    // Later, in main loop:
    if (got_signal) {
        write(STDOUT_FILENO, "Signal received\n", 16);
        got_signal = 0;
    }
}
```

---

## 6. Network Operations

### 6.1 Socket Creation

```markdown
## Socket System Calls

| Call | Linux | FreeBSD | macOS | Windows |
|------|-------|---------|-------|---------|
| socket | yes | yes | yes | socket() |
| bind | yes | yes | yes | bind() |
| listen | yes | yes | yes | listen() |
| accept | yes | yes | yes | accept() |
| connect | yes | yes | yes | connect() |
| send | yes | yes | yes | send() |
| recv | yes | yes | yes | recv() |
| close | yes | yes | yes | closesocket() |
| shutdown | yes | yes | yes | shutdown() |

## Socket Options

```c
// Common socket options
int flag = 1;
setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &flag, sizeof(flag));
setsockopt(sockfd, SOL_SOCKET, SO_KEEPALIVE, &flag, sizeof(flag));

// TCP-specific
setsockopt(sockfd, IPPROTO_TCP, TCP_NODELAY, &flag, sizeof(flag));

// Linux-specific
setsockopt(sockfd, SOL_SOCKET, SO_BINDTODEVICE, device, strlen(device));
```

---

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

---

## 8. IPC Operations

### 8.1 IPC Syscalls

```markdown
## Inter-Process Communication

| Mechanism | Linux | FreeBSD | macOS | Windows |
|-----------|-------|---------|-------|---------|
| pipe | yes | yes | yes | CreatePipe |
| socketpair | yes | yes | yes | (Unix only) |
| shmget | yes | yes (compat) | yes (compat) | (see shm_open) |
| shm_open | yes | yes | yes | (via CreateFileMapping) |
| msgget | yes | yes (compat) | yes (compat) | (no native) |
| semget | yes | yes (compat) | yes (compat) | (no native) |
| msgctl | yes | yes (compat) | yes (compat) | (no native) |
| semctl | yes | yes (compat) | yes (compat) | (no native) |

## Unix Domain Sockets

```c
// Unix domain socket - not available on Windows
int sockfd = socket(AF_UNIX, SOCK_STREAM, 0);

struct sockaddr_un addr;
addr.sun_family = AF_UNIX;
strcpy(addr.sun_path, "/tmp/my.sock");
bind(sockfd, (struct sockaddr *)&addr, sizeof(addr));

// For abstract sockets (Linux only, not BSD/macOS)
strcpy(addr.sun_path + 1, "my_abstract_socket");
```

---

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

---

## 10. Debugging and Stack Tracing

### 10.1 GDB (GNU Debugger)

```markdown
## GDB Commands

| Command | Shortcut | Purpose |
|---------|----------|---------|
| run | r | Start program |
| break | b | Set breakpoint |
| continue | c | Continue execution |
| next | n | Step over (next line) |
| step | s | Step into (into function) |
| finish | fin | Run until function returns |
| print | p | Print variable value |
| backtrace | bt | Show call stack |
| info threads | i th | Show all threads |
| thread apply all bt | | Backtrace all threads |
| disassemble | disas | Show assembly code |
| x/100x | | Examine memory |
| watch | | Watch variable for changes |

## GDB Usage Examples

```bash
# Start debugging
gdb ./myprogram

# Run with arguments
gdb --args ./myprogram --config=/path/to/config

# Attach to running process
gdb -p <pid>

# Load core dump
gdb ./myprogram core.12345

# Debug with TUI (text UI)
gdb -tui ./myprogram

# Set breakpoints
(gdb) break main
(gdb) break file.c:42
(gdb) break *0x00401520  # Break at address

# Conditional breakpoint
(gdb) break file.c:42 if count > 10

# Watchpoints
(gdb) watch global_var
(gdb) rwatch *0x12345678  # Read watchpoint

# Backtrace
(gdb) bt                 # Current thread
(gdb) bt full            # With local variables
(gdb) thread apply all bt  # All threads
```

### 10.2 LLDB (LLVM Debugger)

```markdown
## LLDB Commands

| Command | Shortcut | Purpose |
|---------|----------|---------|
| run | r | Start program |
| breakpoint set | br s | Set breakpoint |
| thread step-over | n | Step over |
| thread step-inst | si | Step into instruction |
| thread step-inst-over | ni | Step over instruction |
| frame variable | fr v | Show local variables |
| thread backtrace | bt | Show call stack |
| thread list | th l | Show all threads |
| image lookup -a | im lookup -a | Lookup address |
| disassemble | dis | Show assembly |

## LLDB Usage Examples

```bash
# Start debugging
lldb ./myprogram

# Run with arguments
(lldb) settings set target.run-args -- --config=/path/to/config

# Attach to process
lldb -p <pid>

# Load core dump
lldb ./myprogram -c core.12345

# Set breakpoints
(lldb) br s -n main
(lldb) br s -f file.c -l 42
(lldb) br s -a 0x00401520

# Backtrace
(lldb) bt                  # Current thread
(lldb) bt all              # All threads
(lldb) frame info           # Current frame info

# Examine memory
(lldb) memory read 0x1000 0x2000
(lldb) x/100x 0x1000        # Hex dump

# Stepping
(lldb) n                   # Next line
(lldb) s                   # Step into
(lldb) ni                  # Next instruction
(lldb) si                  # Step instruction
```

### 10.3 Stack Frame Anatomy

```markdown
## x86-64 Stack Frame

```
┌──────────────────────────────┐ High addresses
│      Return Address          │ ← Saved RIP
├──────────────────────────────┤
│      Saved RBP              │ ← Old base pointer
├──────────────────────────────┤
│      Local Variables         │
│      ...                    │
├──────────────────────────────┤
│      Saved Registers         │
│      ...                    │
├──────────────────────────────┤
│      Function Arguments      │ ← For called functions
│      arg4 (via r9)         │
│      arg3 (via r8)         │
│      arg2 (via rdx)        │
│      arg1 (via rsi)        │
│      arg0 (via rdi)        │
└──────────────────────────────┘ Low addresses
```

## Stack Unwinding

```c
// Frame pointer chain for unwinding
// Each frame saves old RBP, then sets RBP = RSP at function start

void level3() {
    // RBP points here, RSP points here
    int x = 1;  // Local
}

void level2() {
    // RBP points to level2's frame
    level3();    // Call, pushes return address
}

void level1() {
    // RBP points to level1's frame
    level2();    // Call
}

// Backtrace via RBP chain:
// level1's RBP → level2's RBP → level3's RBP → (0 sentinel)
```

### 10.4 Core Dump Analysis

```markdown
## Core Dump Configuration

```bash
# Check current limits
ulimit -c

# Set unlimited (Linux)
ulimit -c unlimited

# Set core dump filename pattern (Linux)
echo '/tmp/core.%e.%p.%t' > /proc/sys/kernel/core_pattern

# Traditional location
mkdir -p /var/coredumps
chmod 1777 /var/coredumps

# macOS core dump location
# Defaults to /cores/core.%pid.%procname
```

## Core Dump Analysis

```bash
# Load core dump in GDB
gdb ./myprogram /tmp/core.myprogram.12345

# Load core dump in LLDB
lldb ./myprogram -c /tmp/core.myprogram.12345

# Common analysis commands
(gdb) bt                  # Full backtrace
(gdb) bt 20              # First 20 frames
(gdb) info registers      # Register state
(gdb) info locals         # Local variables
(gdb) x/100x $rsp        # Stack around RSP
(gdb) x/100x $rbp         # Stack around RBP
(gdb) info threads        # What was running
(gdb) thread apply all bt # All thread backtraces
```

### 10.5 Memory Debugging

```markdown
## Address Sanitizer (ASAN)

```bash
# Compile with ASAN
gcc -fsanitize=address -g program.c -o program

# ASAN detects:
# - Use after free
# - Buffer overflow
# - Double free
# - Memory leaks (with ASAN_OPTIONS=detect_leaks=1)
```

## Valgrind (memcheck)

```bash
# Run valgrind
valgrind --leak-check=full ./myprogram

# Valgrind detects:
# - Invalid memory access
# - Uninitialized memory use
# - Memory leaks
# - Wrong free/delete
# - Free on non-heap memory

# Common options
valgrind --track-origins=yes  # Show where uninitialized values come from
valgrind --vgdb=yes           # Interactive debugging
```

## Thread Sanitizer (TSAN)

```bash
# Compile with TSAN
gcc -fsanitize=thread -g program.c -o program

# TSAN detects:
# - Data races
# - Race conditions
# - Concurrent access without synchronization
```

## Malloc Debug (macOS)

```bash
# macOS malloc debugging
MallocStackLogging=1 ./myprogram  # Track allocations
MallocStackLoggingNoCompact=1 ./myprogram  # More detail

# Use leaks utility
leaks --atExit -- ./myprogram

# Use leaks with PID
leaks <pid>
```

### 10.6 Crash Analysis Template

```markdown
## Crash Analysis Report

### Crash Information
| Field | Value |
|-------|-------|
| Signal | SIGSEGV (11) |
| Address | 0x0000000000000000 |
| Instruction | mov %rax,(%rax) |
| Code State | RIP = 0x401234 |

### Backtrace (GDB/LLDB)

```
#0  0x0000000000401234 in process_buffer (buf=0x0) at processor.c:42
#1  0x0000000000401567 in handle_request (req=0x7fff5000) at handler.c:100
#2  0x0000000000401890 in main (argc=3, argv=0x7fff5a00) at main.c:45
```

### Root Cause Analysis

| Item | Finding |
|------|---------|
| NULL Pointer | buf parameter was NULL |
| Called From | handle_request at handler.c:100 |
| Why NULL | load_config() failed but return value not checked |
| Fix | Check load_config() return value before calling process_buffer() |

### Prevention
1. Add NULL check after load_config()
2. Enable -Werror=maybe-uninitialized
3. Add assertion in process_buffer()
```

---

## Validation Checklist

Before declaring syscall analysis complete:

- [ ] All system calls identified via tracing
- [ ] OS-specific flags noted
- [ ] Non-portable features documented
- [ ] Replacement strategies defined
- [ ] Third-party libraries identified for replacement
- [ ] Performance implications considered

## Reference

See process-model-analyzer for process/thread creation patterns.