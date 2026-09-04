---
name: process-model-ipc
description: Inter-process communication — pipes, named pipes (FIFO), POSIX/shared memory, System V IPC, message queues, IPC comparison.
---

# Process Model Analyzer — IPC

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
