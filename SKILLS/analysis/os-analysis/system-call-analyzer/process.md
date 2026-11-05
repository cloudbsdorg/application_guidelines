---
name: syscall-process
description: Process system calls — fork/exec/clone, process lifecycle, process states, process information syscalls.
---

# System Call Analyzer — Process Operations

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
