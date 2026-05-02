# Skill: process-model-analyzer

**Purpose:** Systematically analyze application process models, threading, and inter-process communication patterns for cross-platform porting.

**Triggers:** When analyzing applications with complex process/thread models, or when porting between platforms with different process models.

## Loading Instructions

Load this skill when the user asks you to:
- Analyze process creation patterns
- Understand threading models
- Document IPC mechanisms
- Plan parallel/concurrent porting
- Map thread/process dependencies

---

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

---

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

---

## 3. Threading Models

### 3.1 Thread Creation

```markdown
## Pthreads

```c
#include <pthread.h>

void *worker(void *arg) {
    int *value = (int *)arg;
    // Do work
    return result;
}

pthread_t tid;
int arg = 42;
pthread_create(&tid, NULL, worker, &arg);
pthread_join(tid, NULL);  // Wait for thread
```

## Thread Attributes

```c
// Set thread stack size
pthread_attr_t attr;
pthread_attr_init(&attr);
pthread_attr_setstacksize(&attr, 2 * 1024 * 1024);  // 2MB

// Set detached state
pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_DETACHED);

// Create with custom attributes
pthread_create(&tid, &attr, worker, &arg);
pthread_attr_destroy(&attr);
```

## Thread vs Task Parallelism

```markdown
| Approach | When to Use | Example |
|----------|-------------|---------|
| Thread per request | Blocking I/O, long-lived requests | Web servers |
| Thread pool | Bounded concurrency, resource control | Database connections |
| Worker threads | Work queue, task distribution | Build systems |
| Async/Event-driven | High concurrency, I/O-bound | Network servers |
| Process pool | CPU isolation, security | Plugin sandboxing |
```

### 3.2 Thread Pools

```markdown
## Thread Pool Pattern

```
┌─────────────────────────────────────────────────┐
│                 Thread Pool                      │
│                                                  │
│  Task Queue                                      │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐      │
│  │Task1│ │Task2│ │Task3│ │Task4│ │Task5│      │
│  └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘      │
│     │       │       │       │       │          │
│     ▼       ▼       ▼       ▼       ▼          │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐      │
│  │ Thr1│ │ Thr2│ │ Thr3│ │ Thr4│ │ Thr5│      │
│  └─────┘ └─────┘ └─────┘ └─────┘ └─────┘      │
└─────────────────────────────────────────────────┘
```

## Thread Pool Implementation

```c
// Thread pool structure
typedef struct {
    pthread_t *threads;
    int num_threads;
    TaskQueue *queue;
    pthread_mutex_t mutex;
    pthread_cond_t cond;
    int shutdown;
} ThreadPool;

// Worker loop
void *worker(void *arg) {
    ThreadPool *pool = (ThreadPool *)arg;
    while (1) {
        pthread_mutex_lock(&pool->mutex);
        while (TAILQ_EMPTY(pool->queue) && !pool->shutdown) {
            pthread_cond_wait(&pool->cond, &pool->mutex);
        }
        if (pool->shutdown) {
            pthread_mutex_unlock(&pool->mutex);
            break;
        }
        Task *task = TAILQ_FIRST(pool->queue);
        TAILQ_REMOVE(pool->queue, task, next);
        pthread_mutex_unlock(&pool->mutex);
        task->fn(task->arg);
    }
    return NULL;
}
```

---

## 4. Synchronization

### 4.1 Mutex

```markdown
## Pthread Mutex

```c
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;

// Lock
pthread_mutex_lock(&mutex);
// Critical section
pthread_mutex_unlock(&mutex);

// Try lock (non-blocking)
if (pthread_mutex_trylock(&mutex) == 0) {
    // Got lock
    pthread_mutex_unlock(&mutex);
} else {
    // Already locked
}
```

## Mutex Types

| Type | Linux | FreeBSD | macOS | Description |
|------|-------|---------|-------|-------------|
| NORMAL | yes | yes | yes | Deadlock if re-locked |
| RECURSIVE | yes | yes | yes | Allows recursive lock |
| ERRORCHECK | yes | yes | yes | Returns error on deadlock |
| DEFAULT | yes | yes | yes | Implementation-defined |

### 4.2 Condition Variables

```markdown
## Condition Variable Pattern

```c
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t cond = PTHREAD_COND_INITIALIZER;
int ready = 0;

// Waiter
pthread_mutex_lock(&mutex);
while (!ready) {
    pthread_cond_wait(&cond, &mutex);  // Atomically unlocks mutex
}
// Now mutex is locked and ready == true
pthread_mutex_unlock(&mutex);

// Signaler
pthread_mutex_lock(&mutex);
ready = 1;
pthread_cond_signal(&cond);   // Wake one waiter
// or
pthread_cond_broadcast(&cond);  // Wake all waiters
pthread_mutex_unlock(&mutex);
```

## Condition Variable Anti-Patterns

```c
// WRONG: Signal without mutex
pthread_cond_signal(&cond);  // Outside mutex - TOCTOU race

// WRONG: Checking condition outside loop
pthread_mutex_lock(&mutex);
if (!ready) {  // Check outside wait
    pthread_cond_wait(&cond, &mutex);
}
pthread_mutex_unlock(&mutex);

// RIGHT: Always check in loop
while (!ready) {
    pthread_cond_wait(&cond, &mutex);
}
```
```

### 4.3 Other Synchronization Primitives

```markdown
## Semaphore

| Type | Description | Use Case |
|------|-------------|----------|
| Binary | Like mutex but can be across processes | Process sync |
| Counting | Counts resources | Producer/consumer |

```c
sem_t sem;
sem_init(&sem, 0, 1);  // Initial value = 1

sem_wait(&sem);  // Decrement, block if <= 0
// Critical section
sem_post(&sem);  // Increment, wake waiters
```

## Read-Write Lock

```c
pthread_rwlock_t rwlock = PTHREAD_RWLOCK_INITIALIZER;

// Read lock (multiple readers)
pthread_rwlock_rdlock(&rwlock);
// Read shared data
pthread_rwlock_unlock(&rwlock);

// Write lock (exclusive)
pthread_rwlock_wrlock(&rwlock);
// Write exclusive data
pthread_rwlock_unlock(&rwlock);
```

## Spinlock

```c
// Atomic spinlock
volatile int lock = 0;

while (__sync_lock_test_and_set(&lock, 1)) {
    // Spin until we get the lock
    while (lock) {
        __asm__ __volatile__("pause");  // x86 hint
    }
}
// Critical section
__sync_lock_release(&lock, 0);
```

---

## 5. Inter-Process Communication

### 5.1 Pipes

```markdown
## Anonymous Pipe

```c
// Create pipe
int pipe_fd[2];
pipe(pipe_fd);  // pipe_fd[0] = read, pipe_fd[1] = write

pid_t pid = fork();
if (pid == 0) {
    // Child - redirect stdin, exec
    dup2(pipe_fd[0], STDIN_FILENO);
    close(pipe_fd[0]);
    close(pipe_fd[1]);
    execve("/bin/grep", args, envp);
} else {
    // Parent - write to child
    close(pipe_fd[0]);
    write(pipe_fd[1], "input data", 9);
    close(pipe_fd[1]);
    waitpid(pid, NULL, 0);
}
```

## Named Pipe (FIFO)

```c
// Create FIFO
mkfifo("/tmp/my_fifo", 0666);

// Open for reading (blocks until writer opens)
int fd = open("/tmp/my_fifo", O_RDONLY);

// Open for writing (blocks until reader opens)
int fd = open("/tmp/my_fifo", O_WRONLY);
```

### 5.2 Shared Memory

```markdown
## POSIX Shared Memory

```c
// Create shared memory object
int shm_fd = shm_open("/my_shm", O_CREAT | O_RDWR, 0666);
ftruncate(shm_fd, 4096);  // Size

// Map into address space
void *ptr = mmap(NULL, 4096, PROT_READ | PROT_WRITE,
                 MAP_SHARED, shm_fd, 0);

// Use shared memory
*(int *)ptr = 42;

// Clean up
munmap(ptr, 4096);
close(shm_fd);
shm_unlink("/my_shm");
```

## System V Shared Memory

```c
// Get shared memory ID
int shmid = shmget(SHM_KEY, 4096, IPC_CREAT | 0666);

// Attach to process
void *ptr = shmat(shmid, NULL, 0);

// Detach
shmdt(ptr);

// Remove (when done)
shmctl(shmid, IPC_RMID, NULL);
```

### 5.3 Message Queues

```markdown
## POSIX Message Queue

```c
// Open queue
mqd_t mq = mq_open("/my_queue", O_CREAT | O_RDWR, 0666, NULL);

// Send message
mq_send(mq, "hello", 5, 0);

// Receive message
char buf[1024];
ssize_t n = mq_receive(mq, buf, sizeof(buf), NULL);

// Close and unlink
mq_close(mq);
mq_unlink("/my_queue");
```

## System V Message Queue

```c
// Get queue ID
int msqid = msgget(MSG_KEY, IPC_CREAT | 0666);

// Send message
struct msgbuf {
    long mtype;  // Message type (must be > 0)
    char mtext[1024];
} msg = { .mtype = 1, .mtext = "hello" };
msgsnd(msqid, &msg, strlen(msg.mtext), 0);

// Receive
msgrcv(msqid, &msg, sizeof(msg.mtext), 1, 0);

// Control
msgctl(msqid, IPC_RMID, NULL);
```

### 5.4 IPC Comparison

```markdown
## IPC Mechanism Comparison

| Mechanism | Scope | Ordering | Overhead | Use Case |
|-----------|-------|----------|----------|----------|
| Pipe (anonymous) | Related processes | FIFO | Low | Parent-child I/O |
| Pipe (named/FIFO) | Unrelated | FIFO | Low | Simple messaging |
| Socket (Unix) | Unrelated | FIFO | Medium | Network-like |
| Message Queue | Unrelated | FIFO | Medium | Async tasks |
| Shared Memory | Unrelated | None | Lowest | High-throughput data |
| RPC | Any | Asynchronous | High | Remote calls |

## When to Use Each

| Use Case | Recommended IPC |
|----------|-----------------|
| Simple parent-child I/O | pipe() |
| Producer-consumer | mq or pipe |
| High-bandwidth data | shm + semaphores |
| Network-style communication | Unix domain sockets |
| Remote procedure calls | gRPC, Thrift |
| Event notification | signals, eventfd |
```

---

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

---

## 7. Async and Event-Driven

### 7.1 Event-Driven Architecture

```markdown
## Event Loop Pattern

```
┌─────────────────────────────────────────────────┐
│                  Event Loop                      │
│                                                  │
│  ┌────────────────────────────────────────────┐ │
│  │            Event Sources                   │ │
│  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐     │ │
│  │  │ Timer│ │  FD   │ │Signal│ │ Idle │     │ │
│  │  └──┬───┘ └──┬───┘ └──┬───┘ └──┬───┘     │ │
│  └─────┼────────┼────────┼────────┼────────────┘ │
│        │        │        │        │              │
│        ▼        ▼        ▼        ▼              │
│  ┌────────────────────────────────────────────┐ │
│  │              Event Dispatcher               │ │
│  │  ┌──────────────────────────────────────┐ │ │
│  │  │          Event Queue                  │ │ │
│  │  │  [Event1][Event2][Event3]...          │ │ │
│  │  └──────────────────────────────────────┘ │ │
│  └────────────────────────────────────────────┘ │
│        │                                         │
│        ▼                                         │
│  ┌────────────────────────────────────────────┐ │
│  │           Event Handlers                    │ │
│  │  onRead() onWrite() onTimer() onSignal() │ │
│  └────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
```

## select() vs poll() vs epoll()

```c
// select() - limited fd set (FD_SETSIZE typically 1024)
fd_set read_fds;
FD_ZERO(&read_fds);
FD_SET(sock_fd, &read_fds);
struct timeval timeout = { .tv_sec = 5 };
int n = select(max_fd + 1, &read_fds, NULL, NULL, &timeout);

// poll() - no fd limit, more portable
struct pollfd fds[2];
fds[0].fd = sock_fd;
fds[0].events = POLLIN;
fds[1].fd = timer_fd;
fds[1].events = POLLIN;
poll(fds, 2, 5000);  // 5 second timeout

// epoll() - Linux-specific, O(1) notification
int epfd = epoll_create1(0);
struct epoll_event ev = { .events = EPOLLIN, .data.fd = sock_fd };
epoll_ctl(epfd, EPOLL_CTL_ADD, sock_fd, &ev);
struct epoll_event events[10];
int n = epoll_wait(epfd, events, 10, 5000);
```

---

## 8. Process Analysis Template

```markdown
## Process Model Analysis

### Application: <Name>
### Target OS: <Target>
### Analysis Date: <Date>

### Process Architecture

| Process | PID | Relationship | Purpose |
|---------|-----|--------------|---------|
| main | 1234 | leader | Main process |
| worker | 1235 | child of main | Request processing |
| logger | 1236 | child of main | Log aggregation |

### Thread Architecture

| Thread | TID | Function | Purpose |
|--------|-----|----------|---------|
| main | 1234 | main() | Main loop |
| io-1 | 1237 | handle_io() | I/O processing pool |
| io-2 | 1238 | handle_io() | I/O processing pool |
| worker-1 | 1239 | process_task() | Task pool |

### Synchronization Primitives

| Primitive | Type | Location | Purpose |
|-----------|------|----------|---------|
| queue_lock | mutex | queue.c:10 | Protect task queue |
| items_available | condvar | queue.c:20 | Signal when item ready |
| shutdown_flag | atomic | main.c:15 | Graceful shutdown |

### IPC Channels

| Channel | Type | Between | Purpose |
|---------|------|---------|---------|
| task_queue | mq | main → workers | Task distribution |
| result_queue | mq | workers → main | Result collection |
| /tmp/app.sock | unix socket | parent ↔ child | Control messages |

### Process Creation Points

| Location | Function | Creation Type | Purpose |
|----------|----------|---------------|---------|
| main.c:50 | main() | fork() | Worker processes |
| main.c:100 | fork_worker() | fork() | On-demand workers |

### Thread Creation Points

| Location | Function | Pool/Oneshot | Purpose |
|----------|----------|--------------|---------|
| io.c:30 | init_io_threads() | pool (4) | I/O handling |
| worker.c:20 | handle_request() | oneshot | Per-request threads |

### Recommendations
1. Replace pthreads with std::thread for C++ target
2. Replace mq with lock-free queue for lower latency
3. Consider async/event-driven for connection handling
```

---

## Validation Checklist

Before declaring process model analysis complete:

- [ ] All processes identified
- [ ] All threads identified
- [ ] Synchronization primitives documented
- [ ] IPC channels mapped
- [ ] Process/thread creation points located
- [ ] Porting strategy for each OS-specific API
- [ ] Thread safety analysis complete

## Reference

See system-call-analyzer for low-level system call dependencies.