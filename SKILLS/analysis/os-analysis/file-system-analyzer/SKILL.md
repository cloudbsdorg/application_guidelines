---
name: file-system-analyzer
description: >-
  Document how an application uses the filesystem - paths, permissions,
  locking, extended attributes. Use when porting software across operating
  systems, when hardcoded paths or permission assumptions need auditing, or
  when file locking behaves differently on the target.
keywords:
  - file system
  - path
  - permission
  - file locking
  - extended attribute
  - xattr
---

# Skill: file-system-analyzer

**Purpose:** Systematically analyze application file system usage, paths, permissions, and operations for cross-platform porting.

**Triggers:** When analyzing applications with file system dependencies, or when porting between Linux, BSD, macOS, and Windows.

## Loading Instructions

Load this skill when the user asks you to:
- Analyze file path patterns
- Document file operations
- Understand permissions and ACLs
- Map file locking usage
- Plan file system porting

---

## 1. Path Conventions

### 1.1 Path Separators

```markdown
## Path Separators

| OS | Separator | Example |
|----|-----------|---------|
| Linux | / | /home/user/file |
| macOS | / | /Users/user/file |
| Windows | \ | C:\Users\user\file |
| Cygwin | / | /cygdrive/c/users/user |

## Path Length Limits

| OS | Max Path | Max Component |
|----|----------|---------------|
| Linux | 4096 bytes | 255 bytes |
| macOS | 1024 bytes (HFS+), 4096 (APFS) | 255 bytes |
| Windows | 260 chars (classic), 32767 (long path) | 255 chars |

## Portable Path Handling

```c
// Use path separator macros
#ifdef _WIN32
    #define PATH_SEP "\\"
    #define PATH_LIST_SEP ";"
#else
    #define PATH_SEP "/"
    #define PATH_LIST_SEP ":"
#endif

// Or use realpath() for absolute paths
char *realpath(const char *path, char *resolved);

// Use dirname() and basename()
char path[] = "/home/user/file.txt";
printf("dir: %s\n", dirname(path));  // "/home/user"
printf("base: %s\n", basename(path));  // "file.txt"
```
```

### 1.2 Path Environment Variables

```markdown
## Home Directories

| OS | Environment | Typical Value |
|----|-------------|---------------|
| Linux | $HOME | /home/username |
| macOS | $HOME | /Users/username |
| Windows | %USERPROFILE% | C:\Users\username |
| Windows | %APPDATA% | C:\Users\username\AppData\Roaming |
| Windows | %LOCALAPPDATA% | C:\Users\username\AppData\Local |

## Standard Directories

| Directory | Linux | macOS | Windows |
|-----------|-------|-------|---------|
| Temp | /tmp | /tmp | %TEMP% |
| Config | /etc | /etc | %PROGRAMDATA% |
| Logs | /var/log | /var/log | %PROGRAMDATA%\Logs |
| Cache | /var/cache | /Library/Caches | %LOCALAPPDATA%\Cache |

## XDG Base Directory (Linux)

```bash
# XDG Base Directory Specification
$HOME/.config/       # User configuration files
$HOME/.local/share/  # User data files
$HOME/.cache/       # User cache files

# Environment variables
XDG_CONFIG_HOME=${XDG_CONFIG_HOME:-$HOME/.config}
XDG_DATA_HOME=${XDG_DATA_HOME:-$HOME/.local/share}
XDG_CACHE_HOME=${XDG_CACHE_HOME:-$HOME/.cache}
```
```

### 1.3 Special Paths

```markdown
## Special Paths

| Path | Linux | macOS | Windows |
|------|-------|-------|---------|
| Current dir | . | . | . |
| Parent dir | .. | .. | .. |
| Temp | /tmp | /tmp | %TEMP% or %TMP% |
| Null device | /dev/null | /dev/null | NUL |
| Stdin | /dev/stdin | /dev/stdin | CON (stdin) |
| Stdout | /dev/stdout | /dev/stdout | CON (stdout) |
| Stderr | /dev/stderr | /dev/stderr | CON (stderr) |

## Windows Special Devices

```c
// Windows special device names
// These are not actually paths but special filenames
"NUL"        // /dev/null equivalent
"CON"       // Console (stdin/stdout)
"PRN"       // Printer
"LPT1"      // Parallel port
"COM1"      // Serial port

// But CreateFile() uses special syntax
CreateFile("\\\\.\\NUL", ...);  // Access NUL device
CreateFile("\\\\.\\COM1", ...); // Access COM1
```

---

## 2. File Operations

### 2.1 Opening Files

```c
// Basic open
int fd = open("/path/to/file", O_RDONLY);
int fd = open("/path/to/file", O_WRONLY | O_CREAT | O_TRUNC, 0644);

// Open flags
O_RDONLY    // Read only
O_WRONLY    // Write only
O_RDWR      // Read and write
O_CREAT     // Create if not exists
O_EXCL      // Fail if exists (with O_CREAT)
O_TRUNC     // Truncate to zero length
O_APPEND    // Append to end
O_NONBLOCK  // Non-blocking I/O
O_SYNC      // Synchronous writes

// macOS-specific
O_SHLOCK    // Shared lock (can share with others)
O_EXLOCK    // Exclusive lock

// Linux-specific
O_DIRECT    // Bypass page cache (direct I/O)
O_NOATIME   // Don't update access time
O_TMPFILE   // Create anonymous temp file
```

### 2.2 Reading and Writing

```c
// Read
ssize_t bytes = read(fd, buffer, count);
if (bytes < 0) {
    perror("read failed");
}

// Write
ssize_t written = write(fd, buffer, count);

// Pread/pwrite - read/write at offset without changing file position
pread(fd, buffer, count, offset);   // Like read but at offset
pwrite(fd, buffer, count, offset); // Like write but at offset

// Vectored I/O - readv/writev
struct iovec iov[3];
iov[0].iov_base = "Header";
iov[0].iov_len = 6;
iov[1].iov_base = "Body";
iov[1].iov_len = 4;
iov[2].iov_base = "Footer";
iov[2].iov_len = 6;

readv(fd, iov, 3);   // Scatter read
writev(fd, iov, 3);  // Gather write

// Synchronized I/O
fdatasync(fd);  // Sync data only (not metadata)
fsync(fd);      // Sync data and metadata
sync();         // Sync all filesystems
```

### 2.3 File Position

```c
// Seek
off_t pos = lseek(fd, offset, SEEK_SET);  // From start
off_t pos = lseek(fd, offset, SEEK_CUR);  // From current
off_t pos = lseek(fd, offset, SEEK_END);  // From end

// Tell position
off_t pos = lseek(fd, 0, SEEK_CUR);

// Truncate
ftruncate(fd, new_length);  // Truncate file at current position
truncate("/path/to/file", new_length);  // Truncate by path
```

---

## 3. Directory Operations

### 3.1 Directory Traversal

```c
// Open directory
DIR *dir = opendir("/path/to/dir");
struct dirent *entry;
while ((entry = readdir(dir)) != NULL) {
    printf("%s\n", entry->d_name);  // Just the name
    // entry->d_type tells type:
    // DT_REG = regular file
    // DT_DIR = directory
    // DT_LNK = symbolic link
}
closedir(dir);

// Use fstatat() for full info
struct stat st;
fstatat(dirfd(dir), entry->d_name, &st, 0);

// Recursive directory scan
int walk_dir(const char *path) {
    DIR *dir = opendir(path);
    struct dirent *entry;
    while ((entry = readdir(dir)) != NULL) {
        if (strcmp(entry->d_name, ".") == 0 ||
            strcmp(entry->d_name, "..") == 0) {
            continue;
        }
        // Build full path
        char full_path[PATH_MAX];
        snprintf(full_path, sizeof(full_path), "%s/%s", path, entry->d_name);

        if (entry->d_type == DT_DIR) {
            walk_dir(full_path);
        } else {
            process_file(full_path);
        }
    }
    closedir(dir);
}
```

### 3.2 Creating and Removing Directories

```c
// Create directory
mkdir("/path/to/dir", 0755);

// Create directory hierarchy
mkdirp("/a/b/c", 0755);  // Create /a, /a/b, /a/b/c

// Remove empty directory
rmdir("/path/to/dir");

// Remove directory and contents (recursive)
int rmrf(const char *path) {
    DIR *dir = opendir(path);
    struct dirent *entry;
    int ret = 0;
    while ((entry = readdir(dir)) != NULL) {
        if (strcmp(entry->d_name, ".") == 0 ||
            strcmp(entry->d_name, "..") == 0) {
            continue;
        }
        char full_path[PATH_MAX];
        snprintf(full_path, sizeof(full_path), "%s/%s", path, entry->d_name);
        if (entry->d_type == DT_DIR) {
            ret = rmrf(full_path);
        } else {
            ret = unlink(full_path);
        }
    }
    closedir(dir);
    return rmdir(path);
}
```

---

## 4. File Metadata

### 4.1 Stat Structure

```c
struct stat {
    dev_t     st_dev;      // Device ID
    ino_t     st_ino;      // Inode number
    mode_t    st_mode;     // File mode (permissions + type)
    nlink_t   st_nlink;    // Number of hard links
    uid_t     st_uid;      // Owner UID
    gid_t     st_gid;      // Owner GID
    dev_t     st_rdev;     // Device ID (for special files)
    off_t     st_size;     // Size in bytes
    blksize_t st_blksize;  // Block size for I/O
    blkcnt_t  st_blocks;   // Number of blocks
    time_t    st_atime;    // Last access time
    time_t    st_mtime;    // Last modification time
    time_t    st_ctime;    // Last status change time
};
```

### 4.2 File Type Detection

```c
// Check file type via st_mode
struct stat st;
stat("/path", &st);

if (S_ISREG(st.st_mode))   // Regular file
if (S_ISDIR(st.st_mode))   // Directory
if (S_ISLNK(st.st_mode))   // Symbolic link
if (S_ISCHR(st.st_mode))   // Character device
if (S_ISBLK(st.st_mode))   // Block device
if (S_ISFIFO(st.st_mode))  // FIFO/pipe
if (S_ISSOCK(st.st_mode))  // Socket

// File type constants
S_IFREG  0100000  // Regular
S_IFDIR  0040000  // Directory
S_IFLNK  0120000  // Symbolic link
S_IFCHR  0020000  // Character device
S_IFBLK  0060000  // Block device
S_IFIFO  0010000  // FIFO
S_IFSOCK 0140000  // Socket
```

### 4.3 Permissions

```c
// Permission bits
// st_mode contains: S_IFMT (type) | permissions
// Permissions: S_IRWXU | S_IRWXG | S_IRWXO

// User permissions
S_IRUSR (0400)  // Read by owner
S_IWUSR (0200)  // Write by owner
S_IXUSR (0100)  // Execute by owner

// Group permissions
S_IRGRP (0040)  // Read by group
S_IWGRP (0020)  // Write by group
S_IXGRP (0010)  // Execute by group

// Other permissions
S_IROTH (0004)  // Read by others
S_IWOTH (0002)  // Write by others
S_IXOTH (0001)  // Execute by others

// Common permission sets
0755  // rwxr-xr-x
0644  // rw-r--r--
0600  // rw-------
0777  // rwxrwxrwx

// Check permissions
if (access("/path/to/file", R_OK) == 0)  // Read OK
if (access("/path/to/file", W_OK) == 0)  // Write OK
if (access("/path/to/file", X_OK) == 0)  // Execute OK
if (access("/path/to/file", F_OK) == 0)   // Exists
```

---

## 5. Links and Symbolic Links

### 5.1 Hard Links

```c
// Create hard link
link("/original/file", "/new/link");

// Hard link restrictions
// - Cannot link across filesystems
// - Cannot link to directory (except by root)
// - Link count increases

// Count links
stat("/file", &st);
printf("Link count: %ld\n", (long)st.st_nlink);

// Remove hard link (doesn't delete file until last link removed)
unlink("/link/name");
```

### 5.2 Symbolic Links

```c
// Create symbolic link
symlink("/real/file", "/symlink");

// Read symbolic link
char target[PATH_MAX];
ssize_t len = readlink("/symlink", target, sizeof(target) - 1);
target[len] = '\0';

// lstat - like stat but doesn't follow symlink
struct stat st;
lstat("/symlink", &st);  // Returns info about symlink itself

// realpath - resolve symlinks
char resolved[PATH_MAX];
realpath("/symlink", resolved);

// Check if path is symlink
if (S_ISLNK(st.st_mode)) {
    // It's a symbolic link
}
```

### 5.3 Link Comparison

```markdown
## Hard vs Symbolic Links

| Aspect | Hard Link | Symbolic Link |
|---------|-----------|---------------|
| Across filesystems | No | Yes |
| Link to directory | No (root only) | Yes |
| Works without target exists | Yes | No |
| Ownership | Same inode | Own inode |
| Link count | Increments | No count |
| Windows | No | Junction or symlink |
| Portable symlinks | N/A | With special flags on Windows |

## Use Cases

| Use Case | Link Type |
|----------|-----------|
| Multiple names for same file | Hard link |
| Shortcuts to files | Symbolic link |
| Versioned binaries (ls -> ls-1.2) | Symbolic link |
| Build system aliases | Symbolic link |
```

---

## 6. File Locking

### 6.1 Advisory Locking (flock)

```c
// BSD-style flock - advisory only
int fd = open("/path/to/lock", O_CREAT, 0666);
flock(fd, LOCK_EX);  // Exclusive lock
// Do work...
flock(fd, LOCK_UN);  // Unlock

// Lock types
LOCK_SH  // Shared lock (multiple readers)
LOCK_EX  // Exclusive lock (single writer)
LOCK_NB  // Non-blocking (don't block, return error)

// Non-blocking example
if (flock(fd, LOCK_EX | LOCK_NB) != 0) {
    if (errno == EWOULDBLOCK) {
        // Already locked
    }
}
```

### 6.2 POSIX Record Locking (fcntl)

```c
// POSIX record locking - more control than flock
struct flock fl = {
    .l_type = F_WRLCK,    // F_RDLCK, F_WRLCK, F_UNLCK
    .l_whence = SEEK_SET, // SEEK_SET, SEEK_CUR, SEEK_END
    .l_start = 0,          // Offset from l_whence
    .l_len = 0,           // 0 = lock entire file
    .l_pid = getpid()
};

// Set lock
fcntl(fd, F_SETLKW, &fl);  // BLOCKING

// Check lock (non-blocking)
fl.l_type = F_WRLCK;
if (fcntl(fd, F_GETLK, &fl) == 0) {
    if (fl.l_type != F_UNLCK) {
        // File is locked by PID: fl.l_pid
    }
}

// Unlock
fl.l_type = F_UNLCK;
fcntl(fd, F_SETLK, &fl);

// Lock byte range
fl.l_start = 100;
fl.l_len = 50;  // Lock bytes 100-149
```

### 6.3 Windows Locking

```c
// Windows file locking
OVERLAPPED overlapped = { 0 };
overlapped.Offset = 100;   // Byte offset
overlapped.Length = 50;    // Bytes to lock

// Lock exclusive
LockFileEx(handle,
           LOCKFILE_EXCLUSIVE_LOCK,
           0,              // Reserved
           100,            // Bytes low
           100 >> 32,      // Bytes high
           &overlapped);

// Unlock
UnlockFileEx(handle,
             100,          // Bytes low
             100 >> 32,    // Bytes high
             &overlapped);
```

---

## 7. Extended Attributes

### 7.1 Linux Extended Attributes

```c
// List extended attributes
ssize_t list = listxattr("/path", NULL, 0);
// Or
ssize_t list = flistxattr(fd, NULL, 0);

// Get attribute
char value[256];
ssize_t len = getxattr("/path", "user.mydata", value, sizeof(value));
// Or
ssize_t len = fgetxattr(fd, "user.mydata", value, sizeof(value));

// Set attribute
setxattr("/path", "user.mydata", value, len, XATTR_CREATE);  // Fail if exists
// Or
setxattr("/path", "user.mydata", value, len, XATTR_REPLACE); // Fail if doesn't exist
setxattr("/path", "user.mydata", value, len, 0);  // Create or replace

// Remove attribute
removexattr("/path", "user.mydata");
```

### 7.2 macOS Extended Attributes

```c
// macOS extended attributes (also works on some BSD)
#include <sys/xattr.h>

// List attributes
ssize_t list = listxattr("/path", NULL, 0, 0);

// Get attribute
char value[256];
ssize_t len = getxattr("/path", "com.apple.quarantine", value, sizeof(value), 0, 0);

// Set attribute
setxattr("/path", "user.mydata", value, len, 0, XATTR_CREATE);

// Remove attribute
removexattr("/path", "user.mydata", 0);

// Common macOS attributes
"com.apple.quarantine"    // Download safety flag
"com.apple.FinderInfo"    // Finder metadata
"com.apple.ResourceFork"  // Resource fork
```

---

## 8. Temporary Files

### 8.1 mkstemp (Secure Temp File)

```c
// mkstemp - creates temp file with unique name, returns open fd
char template[] = "/tmp/myapp.XXXXXX";
int fd = mkstemp(template);
// template now contains actual filename
// File has 0600 permissions

// mkstemps - with suffix
char template[] = "/tmp/myapp.XXXXXX.txt";
int fd = mkstemps(template, 4);  // 4 chars for suffix

// Write and close
write(fd, "data", 4);
close(fd);
unlink(template);  // Delete when done
```

### 8.2 tmpfile (Anonymous Temp File)

```c
// tmpfile - creates anonymous temp file, auto-deleted on close
FILE *f = tmpfile();  // Returns FILE*
// On Linux, creates in /tmp or /var/tmp
// On macOS, creates in /tmp

fputs("data\n", f);
fclose(f);  // Automatically deleted
```

### 8.3 mkdtemp (Temp Directory)

```c
// mkdtemp - creates unique temp directory
char template[] = "/tmp/myapp.XXXXXX";
char *dir = mkdtemp(template);
// dir now contains actual directory name
// Permissions: 0700

// Clean up directory
rmrf(dir);
```

---

## 9. Memory-Mapped Files

### 9.1 mmap File Mapping

```c
// Memory-map a file
int fd = open("/path/to/file", O_RDWR);
off_t size = lseek(fd, 0, SEEK_END);

void *mapped = mmap(NULL,           // Let OS choose address
                   size,           // Size of mapping
                   PROT_READ|PROT_WRITE,  // Read/write
                   MAP_SHARED,     // Share with other processes
                   fd,             // File descriptor
                   0);              // Offset

if (mapped == MAP_FAILED) {
    perror("mmap failed");
}

// Use memory like regular pointer
strcpy(mapped, "Hello");
printf("%s\n", (char *)mapped);

// Sync changes to disk
msync(mapped, size, MS_SYNC);

// Unmap when done
munmap(mapped, size);
```

### 9.2 Anonymous Mapping

```c
// Anonymous mapping - not backed by file (like malloc but with mmap)
void *mem = mmap(NULL,
                 4096,
                 PROT_READ | PROT_WRITE,
                 MAP_PRIVATE | MAP_ANONYMOUS,
                 -1,   // No file
                 0);   // No offset

// Use as regular memory
memset(mem, 0, 4096);
munmap(mem, 4096);
```

---

## 10. File System Analysis Template

### 10.1 Path Usage Analysis

```markdown
## File System Analysis

### Application: <Name>
### Target OS: <Target>
### Analysis Date: <Date>

### Path Usage

| Path | Type | Usage | Portability |
|------|------|-------|-------------|
| /tmp | Directory | Temp files | Portable (use GetTempPath on Windows) |
| /var/log | Directory | Log files | Linux/BSD only (use Event Log on Windows) |
| /etc/app | Directory | Config | Linux/BSD (use Registry/ProgramData on Windows) |
| /home/user/.config | File | Config | Linux (use AppData on Windows) |

### File Operations

| Operation | Count | Location | Portability Notes |
|-----------|-------|----------|-------------------|
| open(O_DIRECT) | 3 | cache.c:42 | Linux only - remove or fallback |
| O_TMPFILE | 1 | temp.c:20 | Linux only - use mkstemp |
| /proc/self | 2 | proc.c:15 | Linux only - use other methods |

### Permissions Usage

| Check | Location | Notes |
|-------|----------|-------|
| access(R_OK) | file.c:30 | Portable |
| S_ISUID check | perm.c:25 | Portable |
| ACL operations | acl.c:40 | Linux-specific (use Windows ACL on Windows) |

### Locking Mechanisms

| Type | Location | Portability |
|------|----------|-------------|
| flock() | lock.c:20 | BSD/Linux, Windows (via _open_osfhandle) |
| fcntl() | lock.c:50 | POSIX only - use LockFileEx on Windows |
| lockf() | lock.c:70 | POSIX - use LockFileEx on Windows |

### Recommendations
1. Replace /var/log with Event Log on Windows
2. Replace /etc with ProgramData on Windows
3. Replace flock() with platform-specific locking
4. Use GetTempPath() instead of hardcoded /tmp
```
```

---

## Validation Checklist

Before declaring file system analysis complete:

- [ ] All path constants identified
- [ ] File operations mapped
- [ ] Permission checks documented
- [ ] Locking mechanisms identified
- [ ] Temporary file usage found
- [ ] Extended attribute usage noted
- [ ] Platform-specific paths identified
- [ ] Portable alternatives defined

## Reference

See system-call-analyzer for underlying system calls.