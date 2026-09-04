---
name: syscall-debugging
description: Debugging system calls — GDB/LLDB commands, stack frame anatomy, core dump analysis, ASAN, Valgrind, TSAN.
---

# System Call Analyzer — Debugging

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
lldb ./myprogram -c /tmp/core.12345

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
