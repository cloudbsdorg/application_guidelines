---
name: syscall-signals
description: Signal handling — signal syscalls, signal comparison table, async-signal-safe functions, signal-safe write example.
---

# System Call Analyzer — Signal Handling

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
