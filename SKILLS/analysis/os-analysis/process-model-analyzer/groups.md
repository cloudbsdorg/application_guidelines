---
name: process-model-groups
description: Process groups and sessions — process group concept, daemon process pattern, setsid, process group commands.
---

# Process Model Analyzer — Process Groups and Sessions

## 6. Process Groups and Sessions

### 6.1 Process Groups

```markdown
## Process Group Concept

```
Session (SID=100)
    │
    └─ Process Group (PGID=101) - Foreground
    │       │
    │       ├─ bash (PID=101) - Group Leader
    │       ├─ process1 (PID=102)
    │       └─ process2 (PID=103)
    │
    └─ Process Group (PGID=104) - Background
            │
            ├─ process3 (PID=104) - Group Leader
            └─ process4 (PID=105)
```

## Process Group Commands

```c
// Create new process group (becomes leader)
setpgid(pid, pid);  // or setpgrp()

// Join existing process group
setpgid(pid, pgid);

// Get process group ID
pid_t pgid = getpgid(pid);

// Get session ID
pid_t sid = getsid(pid);

// Create new session (setsid() - makes process session leader)
setsid();
```

### 6.2 Daemon Process Pattern

```markdown
## Creating a Daemon

```c
void become_daemon() {
    // 1. Fork - parent exits
    if (fork() != 0) {
        exit(0);
    }

    // 2. Start new session (detached from terminal)
    setsid();

    // 3. Fork again (prevents acquiring new terminal)
    if (fork() != 0) {
        exit(0);
    }

    // 4. Change working directory to root
    chdir("/");

    // 5. Close stdin/stdout/stderr
    close(STDIN_FILENO);
    close(STDOUT_FILENO);
    close(STDERR_FILENO);

    // 6. Redirect to /dev/null
    open("/dev/null", O_RDWR);  // stdin
    dup(0);                      // stdout
    dup(0);                      // stderr

    // 7. Reset umask
    umask(0);

    // 8. Write PID file
    FILE *f = fopen("/var/run/mydaemon.pid", "w");
    fprintf(f, "%d\n", getpid());
    fclose(f);
}
```
