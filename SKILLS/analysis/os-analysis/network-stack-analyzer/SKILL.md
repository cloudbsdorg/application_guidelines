---
name: network-stack-analyzer
description: >-
  Document an application's networking - sockets, TCP/UDP, epoll/kqueue, TLS,
  DNS. Use when porting network-heavy code to FreeBSD, when replacing epoll
  with kqueue, or when auditing how a service binds, listens, and encrypts.
---

# Skill: network-stack-analyzer

**Purpose:** Systematically analyze application networking code to understand socket usage, protocol handling, and network APIs for cross-platform porting.

**Triggers:** When analyzing applications with network dependencies, or when porting network applications between Linux, BSD, macOS, and Windows.

## Loading Instructions

Load this skill when the user asks you to:
- Analyze socket usage patterns
- Understand network protocol handling
- Map event-driven I/O mechanisms
- Plan network porting
- Document network architecture

---

## 1. Socket Fundamentals

### 1.1 Socket Types

```markdown
## Socket Address Families

| Family | Constant | Description | Windows |
|--------|----------|-------------|---------|
| IPv4 | AF_INET | Internet Protocol v4 | AF_INET |
| IPv6 | AF_INET6 | Internet Protocol v6 | AF_INET6 |
| Unix | AF_UNIX | Unix domain sockets | AF_UNIX |
| Packet | AF_PACKET | Raw link-layer | AF_PACKET (Linux only) |
| Netlink | AF_NETLINK | Kernel communication | N/A |

## Socket Types

| Type | Description | Use Case |
|------|-------------|----------|
| SOCK_STREAM | Byte stream (TCP) | Reliable, ordered, connection-oriented |
| SOCK_DGRAM | Datagrams (UDP) | Connectionless, unordered |
| SOCK_RAW | Raw packets | Direct IP access |
| SOCK_SEQPACKET | Sequenced packet | Like stream but message boundaries |

## Socket Creation

```c
// Create TCP socket
int sock = socket(AF_INET, SOCK_STREAM, 0);

// Create UDP socket
int sock = socket(AF_INET, SOCK_DGRAM, 0);

// Create raw socket (Linux only)
int sock = socket(AF_INET, SOCK_RAW, protocol);

// Create Unix domain socket
int sock = socket(AF_UNIX, SOCK_STREAM, 0);
```

### 1.2 Socket Address Structures

```c
// IPv4 socket address
struct sockaddr_in {
    sa_family_t sin_family;  // AF_INET
    in_port_t   sin_port;    // Port (network byte order!)
    struct in_addr sin_addr; // IP address
    char        sin_zero[8];
};

// IPv6 socket address
struct sockaddr_in6 {
    sa_family_t sin6_family;   // AF_INET6
    in_port_t   sin6_port;    // Port
    uint32_t    sin6_flowinfo; // Flow label
    struct in6_addr sin6_addr; // IPv6 address
    uint32_t    sin6_scope_id; // Scope ID
};

// Unix domain socket address
struct sockaddr_un {
    sa_family_t sun_family;  // AF_UNIX
    char       sun_path[108]; // Socket file path
};

// Generic socket address (for casting)
struct sockaddr {
    sa_family_t sa_family;
    char        sa_data[14];
};
```

### 1.3 Byte Order

```markdown
## Byte Order (Endianness)

| Order | Description | Used By |
|-------|-------------|---------|
| Big Endian | Most significant byte first | Network byte order (TCP/IP) |
| Little Endian | Least significant byte first | x86, x86_64 |

## Conversion Functions

```c
#include <arpa/inet.h>

// Convert host to network byte order (16-bit)
uint16_t htons(uint16_t host16);  // host-to-network short

// Convert network to host byte order (16-bit)
uint16_t ntohs(uint16_t net16);  // network-to-host short

// Same for 32-bit values
uint32_t htonl(uint32_t host32);  // host-to-network long
uint32_t ntohl(uint32_t net32);  // network-to-host long

// IP address conversion
in_addr_t inet_addr("192.168.1.1");  // ASCII to network
char *inet_ntoa(struct in_addr in);   // Network to ASCII

// IPv6 versions
int inet_pton(int af, const char *src, void *dst);  // ASCII to binary
const char *inet_ntop(int af, const void *src, char *dst, socklen_t size);
```

---

## 2. TCP Connections

### 2.1 Connection Lifecycle

```markdown
## TCP State Machine

```
CLOSED ──listen──► LISTEN ──accept──► ESTABLISHED ──close──► CLOSE_WAIT
                                                            │
                                                            ▼
                                              LAST_ACK ─────► CLOSED

LISTEN ── SYN ──► SYN_SENT ──SYN+ACK──► ESTABLISHED
SYN_SENT ──RST──► CLOSED
ESTABLISHED ──FIN──► FIN_WAIT_1 ──ACK──► FIN_WAIT_2 ──FIN──► TIME_WAIT ──► CLOSED
```

## TCP Socket Options

```c
// Important socket options
int flag = 1;
setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &flag, sizeof(flag));  // Allow bind reuse
setsockopt(sockfd, SOL_SOCKET, SO_KEEPALIVE, &flag, sizeof(flag));  // Keep alive
setsockopt(sockfd, IPPROTO_TCP, TCP_NODELAY, &flag, sizeof(flag));   // Disable Nagle
setsockopt(sockfd, IPPROTO_TCP, TCP_QUICKACK, &flag, sizeof(flag));  // Quick ack
setsockopt(sockfd, IPPROTO_TCP, TCP_KEEPIDLE, &flag, sizeof(flag)); // Keepalive time
```

### 2.2 TCP Server Pattern

```c
// TCP Server
int server_fd = socket(AF_INET, SOCK_STREAM, 0);

// Set reuse address (prevents EADDRINUSE on restart)
int opt = 1;
setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

// Bind
struct sockaddr_in addr = {
    .sin_family = AF_INET,
    .sin_port = htons(8080),
    .sin_addr.s_addr = INADDR_ANY  // Any interface
};
bind(server_fd, (struct sockaddr *)&addr, sizeof(addr));

// Listen (queue backlog)
listen(server_fd, 128);

// Accept connections
struct sockaddr_in client_addr;
socklen_t client_len = sizeof(client_addr);
int client_fd = accept(server_fd, (struct sockaddr *)&client_addr, &client_len);

// Handle client...
close(client_fd);
close(server_fd);
```

### 2.3 TCP Client Pattern

```c
// TCP Client
int sock_fd = socket(AF_INET, SOCK_STREAM, 0);

// Connect
struct sockaddr_in server_addr = {
    .sin_family = AF_INET,
    .sin_port = htons(80),
    .sin_addr.s_addr = inet_addr("93.184.216.34")
};
connect(sock_fd, (struct sockaddr *)&server_addr, sizeof(server_addr));

// Send
send(sock_fd, "GET / HTTP/1.1\r\n\r\n", 17, 0);

// Receive
char buf[4096];
ssize_t n = recv(sock_fd, buf, sizeof(buf), 0);

close(sock_fd);
```

---

## 3. UDP Operations

### 3.1 UDP Server Pattern

```c
// UDP Server
int sock_fd = socket(AF_INET, SOCK_DGRAM, 0);

struct sockaddr_in addr = {
    .sin_family = AF_INET,
    .sin_port = htons(53),
    .sin_addr.s_addr = INADDR_ANY
};
bind(sock_fd, (struct sockaddr *)&addr, sizeof(addr));

// Receive datagram
char buf[4096];
struct sockaddr_in client_addr;
socklen_t client_len = sizeof(client_addr);
ssize_t n = recvfrom(sock_fd, buf, sizeof(buf), 0,
                      (struct sockaddr *)&client_addr, &client_len);

// Reply
sendto(sock_fd, response, response_len, 0,
       (struct sockaddr *)&client_addr, client_len);
```

### 3.2 UDP vs TCP

```markdown
## UDP vs TCP Characteristics

| Aspect | UDP | TCP |
|--------|-----|-----|
| Connection | Connectionless | Connection-oriented |
| Reliability | Unreliable | Reliable |
| Ordering | None | Ordered |
| Overhead | 8 bytes header | 20+ bytes header |
| Speed | Faster | Slower |
| Flow Control | None | Yes (sliding window) |
| Congestion Control | None | Yes |
| State | Stateless | Stateful |
| Broadcasting | Yes | No (unless connected) |

## When to Use Each

| Use Case | Protocol |
|----------|----------|
| Web, API, Database | TCP |
| DNS | UDP (or TCP for large) |
| Video streaming | UDP (sacrifice reliability for speed) |
| VoIP | UDP (latency over reliability) |
| DHCP | UDP |
| SNMP | UDP |
| HTTP/2, HTTP/3 | TCP |
| QUIC | UDP |
```

---

## 4. Event-Driven I/O

### 4.1 select()

```c
// select() - wait for multiple file descriptors
fd_set read_fds, write_fds, error_fds;
FD_ZERO(&read_fds);
FD_SET(sock_fd, &read_fds);
FD_SET(pipe_fd, &read_fds);

struct timeval timeout = {
    .tv_sec = 5,
    .tv_usec = 0
};

int nfds = sock_fd + 1;  // Highest fd + 1
int n = select(nfds, &read_fds, &write_fds, &error_fds, &timeout);

if (n > 0) {
    if (FD_ISSET(sock_fd, &read_fds)) {
        // sock_fd is readable
    }
}
```

### 4.2 poll()

```c
// poll() - more scalable than select
struct pollfd fds[2];

fds[0].fd = sock_fd;
fds[0].events = POLLIN;   // Want to read
fds[0].revents = 0;       // Result

fds[1].fd = pipe_fd;
fds[1].events = POLLIN;
fds[1].revents = 0;

int timeout_ms = 5000;
int n = poll(fds, 2, timeout_ms);

if (n > 0) {
    if (fds[0].revents & POLLIN) {
        // sock_fd is readable
    }
    if (fds[0].revents & POLLHUP) {
        // Hangup detected
    }
    if (fds[0].revents & POLLERR) {
        // Error on fd
    }
}
```

### 4.3 epoll (Linux)

```c
// epoll_create1() - Linux-specific event notification
int epfd = epoll_create1(0);

// Add file descriptor to watch
struct epoll_event ev = {
    .events = EPOLLIN | EPOLLOUT | EPOLLET,  // Edge-triggered
    .data.fd = sock_fd
};
epoll_ctl(epfd, EPOLL_CTL_ADD, sock_fd, &ev);

// Add timerfd (Linux-specific)
int timerfd = timerfd_create(CLOCK_MONOTONIC, 0);
ev.events = EPOLLIN;
ev.data.fd = timerfd;
epoll_ctl(epfd, EPOLL_CTL_ADD, timerfd, &ev);

// Wait for events
struct epoll_event events[64];
int nfds = epoll_wait(epfd, events, 64, timeout_ms);

for (int i = 0; i < nfds; i++) {
    int fd = events[i].data.fd;
    uint32_t mask = events[i].events;

    if (mask & EPOLLIN) {
        // fd is readable
    }
    if (mask & EPOLLOUT) {
        // fd is writable
    }
    if (mask & EPOLLHUP) {
        // Hangup
    }
}
```

### 4.4 kqueue (BSD/macOS)

```c
// kqueue() - BSD/macOS event notification
int kq = kqueue();

// Register socket
struct kevent ke;
EV_SET(&ke, sock_fd, EVFILT_READ, EV_ADD | EV_ENABLE, 0, 0, NULL);
kevent(kq, &ke, 1, NULL, 0, NULL);

// Register timer (macOS)
struct kevent timer_event;
EV_SET(&timer_event, fd, EVFILT_TIMER, EV_ADD, 0, 1000, NULL);  // 1 second
kevent(kq, &timer_event, 1, NULL, 0, NULL);

// Wait for events
struct kevent events[64];
struct timespec timeout = { .tv_sec = 5 };

int n = kevent(kq, NULL, 0, events, 64, &timeout);

for (int i = 0; i < n; i++) {
    int fd = events[i].ident;
    int filter = events[i].filter;

    if (filter == EVFILT_READ) {
        // fd is readable
    }
    if (filter == EVFILT_TIMER) {
        // Timer fired
    }
}
```

### 4.5 IOCP (Windows)

```c
// Input/Output Completion Port - Windows async I/O
HANDLE comp_port = CreateIoCompletionPort(INVALID_HANDLE_VALUE, NULL, 0, 0);

// Associate socket with completion port
CreateIoCompletionPort((HANDLE)sock_fd, comp_port, 0, 0);

// Issue async read
OVERLAPPED overlapped = { 0 };
WSABUF buf = { .buf = buffer, .len = sizeof(buffer) };
DWORD flags = 0;
WSARecv(sock_fd, &buf, 1, NULL, &flags, &overlapped, NULL);

// Get completion result
DWORD bytes_transferred;
ULONG_PTR key;
OVERLAPPED *overlapped_result;
GetQueuedCompletionStatus(comp_port, &bytes_transferred, &key, &overlapped_result, INFINITE);
```

### 4.6 Event Mechanism Comparison

```markdown
## I/O Multiplexing Comparison

| Mechanism | OS | Max FDs | Scalability | Features |
|-----------|-----|---------|-------------|----------|
| select() | POSIX | FD_SETSIZE (usually 1024) | Poor | All POSIX |
| poll() | POSIX | Unlimited (but linear scan) | Medium | All POSIX |
| epoll | Linux | Unlimited | Excellent | Linux only |
| kqueue | BSD/macOS | Unlimited | Excellent | BSD/macOS only |
| IOCP | Windows | Unlimited | Excellent | Windows only |

## Edge-Triggered vs Level-Triggered

| Mode | epoll | Description |
|------|-------|-------------|
| Level-triggered | EPOLLLT (default) | Notify when ready |
| Edge-triggered | EPOLLET | Notify only on state change |

```c
// Edge-triggered (must drain buffer completely)
while (1) {
    int n = epoll_wait(epfd, events, MAX_EVENTS, -1);
    for (int i = 0; i < n; i++) {
        // Must read ALL data until EAGAIN
        while (recv(fd, buf, sizeof(buf), 0) > 0) { }
    }
}
```

---

## 5. DNS Resolution

### 5.1 DNS Functions

```c
// Get host by name (IPv4)
struct hostent *he = gethostbyname("example.com");
if (he) {
    struct in_addr **addr_list = (struct in_addr **)he->h_addr_list;
    printf("IP: %s\n", inet_ntoa(*addr_list[0]));
}

// Get host by address
struct in_addr addr;
inet_pton(AF_INET, "93.184.216.34", &addr);
struct hostent *he = gethostbyaddr(&addr, sizeof(addr), AF_INET);

// FreeBSD/macOS also have getaddrinfo (preferred)
struct addrinfo hints = {
    .ai_family = AF_UNSPEC,    // AF_INET or AF_INET6
    .ai_socktype = SOCK_STREAM
};
struct addrinfo *result;
int rc = getaddrinfo("example.com", "80", &hints, &result);

for (struct addrinfo *rp = result; rp; rp = rp->ai_next) {
    int sock = socket(rp->ai_family, rp->ai_socktype, rp->ai_protocol);
    connect(sock, rp->ai_addr, rp->ai_addrlen);
}
freeaddrinfo(result);
```

### 5.2 DNS and /etc/hosts

```markdown
## DNS Resolution Order

| OS | Order |
|----|-------|
| Linux (glibc) | /etc/hosts → /etc/resolv.conf → DNS |
| macOS | /etc/hosts → DNS (scoped queries) |
| Windows | DNS → /etc/hosts (lmhosts) |

## /etc/resolv.conf

```
nameserver 8.8.8.8          # Primary DNS
nameserver 8.8.4.4          # Secondary DNS
search localdomain          # Search suffix
options timeout:2          # Timeout per server
options attempts:3         # Retries
```
```

---

## 6. Unix Domain Sockets

### 6.1 Unix Socket Server

```c
// Unix domain stream socket
int sock_fd = socket(AF_UNIX, SOCK_STREAM, 0);

struct sockaddr_un addr = {
    .sun_family = AF_UNIX
};
strcpy(addr.sun_path, "/tmp/my_service.sock");
unlink(addr.sun_path);  // Remove if exists
bind(sock_fd, (struct sockaddr *)&addr, sizeof(addr));

listen(sock_fd, 5);

// Accept connections
int client_fd = accept(sock_fd, NULL, NULL);
```

### 6.2 Abstract Sockets (Linux)

```c
// Abstract sockets - Linux-only, don't need filesystem
struct sockaddr_un addr = {
    .sun_family = AF_UNIX
};
// First byte must be \0 for abstract
addr.sun_path[0] = '\0';
strcpy(addr.sun_path + 1, "my_abstract_socket");

// No need to unlink() - automatically cleaned up on close
```

### 6.3 Datagram Unix Sockets

```c
// Unix datagram - like UDP but local
int sock_fd = socket(AF_UNIX, SOCK_DGRAM, 0);

struct sockaddr_un addr = { .sun_family = AF_UNIX };
strcpy(addr.sun_path, "/tmp/my_dgram.sock");

sendto(sock_fd, "hello", 5, 0, (struct sockaddr *)&addr, sizeof(addr));
recvfrom(sock_fd, buf, sizeof(buf), 0, NULL, NULL);
```

---

## 7. SSL/TLS

### 7.1 OpenSSL Server

```c
#include <openssl/ssl.h>
#include <openssl/err.h>

// Initialize SSL
SSL_library_init();
SSL_load_error_strings();
OpenSSL_add_all_algorithms();

// Create SSL context
SSL_CTX *ctx = SSL_CTX_new(TLS_server_method());
SSL_CTX_use_certificate_file(ctx, "server.crt", SSL_FILETYPE_PEM);
SSL_CTX_use_PrivateKey_file(ctx, "server.key", SSL_FILETYPE_PEM);

// Wrap socket with SSL
SSL *ssl = SSL_new(ctx);
SSL_set_fd(ssl, client_fd);

// Accept TLS connection
SSL_accept(ssl);

// Read/write
SSL_read(ssl, buf, sizeof(buf));
SSL_write(ssl, "HTTP/1.1 200 OK\r\n\r\n", 17);

// Cleanup
SSL_shutdown(ssl);
SSL_free(ssl);
SSL_CTX_free(ctx);
```

### 7.2 TLS Versions

```markdown
## TLS Version Support

| Version | Status | Notes |
|---------|--------|-------|
| SSL 2.0 | Deprecated | Insecure, don't use |
| SSL 3.0 | Deprecated | Insecure, don't use |
| TLS 1.0 | Deprecated | Legacy only |
| TLS 1.1 | Deprecated | Legacy only |
| TLS 1.2 | Recommended | Wide support |
| TLS 1.3 | Recommended | Modern, faster |

## TLS Cipher Suites

```c
// Set minimum TLS version
SSL_CTX_set_min_proto_version(ctx, TLS1_2_VERSION);

// Disable weak ciphers
SSL_CTX_set_cipher_list(ctx, "HIGH:!aNULL:!MD5:!RC4");

// Modern configuration (TLS 1.3 only)
SSL_CTX_set_min_proto_version(ctx, TLS1_3_VERSION);
```
```

---

## 8. Network Analysis Template

### 8.1 Socket Usage Analysis

```markdown
## Network Analysis

### Application: <Name>
### Target OS: <Target>
### Analysis Date: <Date>

### Socket Types Used

| Type | Count | Purpose |
|------|-------|---------|
| SOCK_STREAM (TCP) | 5 | HTTP connections, API calls |
| SOCK_DGRAM (UDP) | 2 | DNS, syslog |
| SOCK_RAW | 1 | ICMP monitoring |

### Event Mechanism

| Mechanism | OS | Usage |
|-----------|-----|-------|
| epoll | Linux | High-volume connections (1000+) |
| kqueue | macOS | High-volume connections (1000+) |
| select/poll | Cross-platform | Lower connection counts |

### Connection Patterns

| Pattern | Count | Example |
|---------|-------|---------|
| Server listen | 2 | HTTP (80), Admin (8080) |
| Client connect | 10 | Upstream APIs |
| Unix socket | 3 | Internal services |

### Identified Issues

| Issue | Location | Porting Impact |
|-------|----------|----------------|
| SO_REUSEPORT | net.c:42 | Linux only - use SO_REUSEADDR on BSD |
| epoll_create1 | net.c:50 | Linux only - use kqueue on BSD |
| IP_PKTINFO | net.c:60 | Linux only - not portable |

### Recommendations
1. Replace epoll with libevent for cross-platform
2. Use getaddrinfo instead of gethostbyname
3. Consider using cURL for HTTP (handles cross-platform)
```
```

---

## Validation Checklist

Before declaring network analysis complete:

- [ ] All socket types identified
- [ ] All event mechanisms mapped
- [ ] IP vs Unix socket usage documented
- [ ] TCP vs UDP usage identified
- [ ] DNS resolution patterns found
- [ ] SSL/TLS usage documented
- [ ] Portability issues identified

## Reference

See system-call-analyzer for underlying system calls.