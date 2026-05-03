---
name: syscall-memory
description: Memory system calls — mmap flags, brk/sbrk, malloc implementation internals across OSes.
---

# System Call Analyzer — Memory Operations

## 3. Memory Operations

### 3.1 Memory Mapping

```markdown
## mmap() Flags

| Flag | Linux | FreeBSD | macOS | Windows |
|------|-------|---------|-------|---------|
| MAP_ANONYMOUS | yes | yes | yes | (use VirtualAlloc) |
| MAP_SHARED | yes | yes | yes | (use CreateFileMapping + MapViewOfFile) |
| MAP_PRIVATE | yes | yes | yes | yes |
| MAP_FIXED | yes | yes | yes | yes |
| MAP_HUGETLB | yes | yes | no | no |
| MAP_NOCACHE | no | no | yes | no |
| MAP_STACK | yes | yes | yes | no |

## mmap() Usage Patterns

```c
// Anonymous mapping (Linux, BSD, macOS)
void *buf = mmap(NULL, size, PROT_READ | PROT_WRITE,
                 MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);

// File-backed mapping
void *buf = mmap(NULL, size, PROT_READ,
                 MAP_PRIVATE, fd, offset);

// Device memory (Linux specific - not portable)
void *dev = mmap(NULL, size, PROT_READ | PROT_WRITE,
                 MAP_SHARED, dev_fd, 0);

// Windows
void *buf = VirtualAlloc(NULL, size, MEM_COMMIT | MEM_RESERVE,
                         PAGE_READWRITE);
```

### 3.2 brk/sbrk (Legacy)

```markdown
## brk/sbrk vs mmap

| Aspect | brk/sbrk | mmap |
|--------|----------|------|
| Allocation | Contiguous heap | Any size, any alignment |
| Fragmentation | Can fragment | No internal fragmentation |
| Linux | Default for small | Default for large |
| FreeBSD | Supported | Preferred |
| macOS | Deprecated | Preferred |
| Windows | N/A | VirtualAlloc |

## malloc() Implementation

```markdown
## malloc() Internals

| Size Range | Linux | FreeBSD | macOS |
|-----------|-------|---------|-------|
| < 128B | brk arena | umem_cache | nano_malloc |
| 128B - 64KB | mmap (small) | umem_cache | small_malloc |
| > 64KB | mmap (large) | mmap | large_malloc |
```
