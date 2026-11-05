---
name: process-model-async
description: Async and event-driven — event loop pattern, select vs poll vs epoll, event dispatcher, I/O multiplexing.
---

# Process Model Analyzer — Async and Event-Driven

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
