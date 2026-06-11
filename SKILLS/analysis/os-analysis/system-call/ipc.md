---
name: syscall-ipc
description: IPC system calls — pipes, socketpair, shmget/shm_open, msgget, semget, Unix domain sockets.
---

# System Call Analyzer — IPC Operations

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
