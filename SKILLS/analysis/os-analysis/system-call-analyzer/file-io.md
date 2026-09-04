---
name: syscall-file-io
description: File I/O system calls — open/close/read/write, flags by OS, file descriptor operations, portable wrappers.
---

# System Call Analyzer — File I/O

## 2. File Operations

### 2.1 Core File Syscalls

```markdown
## File System Calls

| Call | Purpose | Linux | FreeBSD | macOS | Windows |
|------|---------|-------|---------|-------|---------|
| open | Open file | yes | yes | yes | NtCreateFile |
| close | Close file descriptor | yes | yes | yes | NtClose |
| read | Read from fd | yes | yes | yes | NtReadFile |
| write | Write to fd | yes | yes | yes | NtWriteFile |
| lseek | Seek position | yes | yes | yes | NtSetInformationFile |
| stat | Get file metadata | yes | yes | yes | NtQueryInformationFile |
| access | Check permissions | yes | yes | yes | NtAccessCheck |
| unlink | Delete file | yes | yes | yes | NtSetInformationFile |

## open() Flags Comparison

```c
// POSIX
int fd = open(path, O_RDONLY | O_CREAT | O_EXCL, 0644);

// Linux-specific
int fd = open(path, O_RDWR | O_CREAT | O_DIRECT | O_NOATIME, 0644);

// macOS-specific
int fd = open(path, O_RDWR | O_CREAT | O_SHLOCK, 0644);

// FreeBSD-specific
int fd = open(path, O_RDWR | O_CREAT | O_EXLOCK, 0644);
```

### 2.2 File Descriptor Operations

```markdown
## File Descriptor Flags

| Flag | Linux | FreeBSD | macOS | Description |
|------|-------|---------|-------|-------------|
| O_NONBLOCK | yes | yes | yes | Non-blocking I/O |
| O_NOCTTY | yes | yes | yes | Don't become controlling TTY |
| O_CLOEXEC | yes | yes | yes | Close on exec |
| O_DIRECT | yes | yes (with compat) | no | Bypass page cache |
| O_NOATIME | yes | yes | no | Don't update atime |
| O_SHLOCK | no | no | yes | Shared lock |
| O_EXLOCK | no | no | yes | Exclusive lock |

## Portable open() Wrapper

```c
// Portable open with flags
int portable_open(const char *path, int flags, mode_t mode) {
    #ifdef __APPLE__
        flags |= O_SHLOCK;  // macOS
    #elif defined(__FreeBSD__)
        flags |= O_EXLOCK;  // FreeBSD
    #endif
    return open(path, flags, mode);
}
```
