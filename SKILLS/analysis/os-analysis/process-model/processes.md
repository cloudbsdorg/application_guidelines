---
name: process-model-processes
description: Process creation — fork/exec patterns, Windows CreateProcess, POSIX spawn, clone flags, fork variations across OSes.
---

# Process Model Analyzer — Process Creation

## 2. Process Creation

### 2.1 Fork/Exec Model (Unix)

```markdown
## Fork + Exec Pattern

```c
// Classic Unix pattern: fork then exec
pid_t pid = fork();

if (pid == 0) {
    // Child process
    // Often close unnecessary file descriptors
    close(pipe_fd[0]);
    close(pipe_fd[1]);

    // Replace with new program
    execve("/path/to/program", argv, envp);

    // If exec fails:
    _exit(127);
} else if (pid > 0) {
    // Parent process
    int status;
    waitpid(pid, &status, 0);  // Wait for child
}
```

## Fork Variations

| Function | Linux | FreeBSD | macOS | Description |
|----------|-------|---------|-------|-------------|
| fork | yes | yes | yes | Standard fork |
| vfork | yes | yes | yes | Lightweight fork (don't copy page tables) |
| clone | yes | yes | yes | Flexible fork (specify what to share) |
| rfork | no | yes | yes (as rfork) | BSD-specific, shares everything |

## Clone Flags (Linux)

```c
// clone() creates a new process/thread with specified sharing
clone(int (*fn)(void *), void *stack, int flags, void *arg);

// Share nothing (like fork)
clone(SIGCHLD, stack, 0, NULL);

// Share everything (like threads)
clone(CLONE_VM | CLONE_FS | CLONE_FILES | CLONE_SIGHAND | CLONE_THREAD, stack, 0, NULL);

// Share VM (threads in same process)
clone(CLONE_VM, stack, 0, NULL);
```

### 2.2 Spawn Pattern (Windows)

```markdown
## Windows CreateProcess

```c
// Windows spawn pattern
STARTUPINFO si = { sizeof(si) };
PROCESS_INFORMATION pi = { 0 };

BOOL success = CreateProcess(
    "C:\\path\\to\\program.exe",  // Module name
    "program.exe -arg1 -arg2",    // Command line
    NULL,                          // Process security
    NULL,                          // Thread security
    TRUE,                          // Inherit handles
    0,                             // Creation flags
    NULL,                          // Environment
    NULL,                          // Current directory
    &si,                           // Startup info
    &pi                            // Process info
);

if (success) {
    WaitForSingleObject(pi.hProcess, INFINITE);
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);
}
```

## Fork+Exec vs Spawn

| Aspect | Unix (fork+exec) | Windows (CreateProcess) |
|--------|------------------|------------------------|
| Creation | 2 syscalls | 1 syscall |
| Memory | Copy-on-write fork | Separate process, no copy |
| Inheritance | Explicit fd passing | Inherit handles flag |
| Security | Set UID before exec | CreateProcess with security |
```

### 2.3 POSIX Spawn (Portable)

```markdown
## posix_spawn

```c
// Portable way to spawn processes (macOS, BSD, Linux)
pid_t pid;
posix_spawn_file_actions_t fa;
posix_spawnattr_t attr;

// Set up file actions (redirect stdin/stdout)
posix_spawn_file_actions_init(&fa);
posix_spawn_file_actions_adddup2(&fa, pipe_fd[1], STDOUT_FILENO);
posix_spawn_file_actions_addclose(&fa, pipe_fd[0]);

// Set up spawn attributes
posix_spawnattr_init(&attr);
short flags = POSIX_SPAWN_SETSIGMASK;
posix_spawnattr_setflags(&attr, flags);

// Spawn
int result = posix_spawn(&pid, "/path/to/program",
                          &fa, &attr, argv, envp);

if (result == 0) {
    waitpid(pid, NULL, 0);
}
```
