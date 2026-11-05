---
name: syscall-network
description: Network system calls — socket creation, bind/listen/accept/connect, socket options, TCP/UDP operations.
---

# System Call Analyzer — Network Operations

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
