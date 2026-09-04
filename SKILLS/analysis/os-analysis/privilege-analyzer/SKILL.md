---
name: privilege-analyzer
description: >-
  Document what privileges an application actually needs - UID/GID,
  capabilities, ACLs, chroot, securelevel, Capsicum. Use when porting
  privileged code, when applying least privilege to a service, or when
  deciding what a daemon may drop after start-up.
---

# Skill: privilege-analyzer

**Purpose:** Systematically analyze application privilege requirements, user/group handling, and security mechanisms for cross-platform porting.

**Triggers:** When analyzing applications with privilege requirements, setuid/setgid binaries, or when porting security-sensitive applications.

## Loading Instructions

Load this skill when the user asks you to:
- Analyze user/group requirements
- Document privilege operations
- Understand capability usage
- Map ACL patterns
- Plan privilege porting

---

## 1. User and Group Identifiers

### 1.1 UID/GID Overview

```markdown
## Standard UIDs

| UID | Name | Description |
|-----|------|-------------|
| 0 | root | Superuser |
| 1 | bin | Binaries owner |
| 2 | daemon | System daemon |
| 3 | sys | System |
| 4 | adm | Admin logs |
| 5 | tty | TTY devices |
| 6 | disk | Disk devices |
| 7 | lp | Printer |
| 8 | mail | Mail |
| 9 | games | Games |
| 10 | unknown | - |
| 20 | staff | macOS staff |
| 33-39 | www-data, etc. | Services |
| 80 | www | Apache/nginx |
| 1000+ | user | Regular users |

## Common GIDs

| GID | Name | Description |
|-----|------|-------------|
| 0 | wheel | Admin group (BSD, macOS) |
| 0 | root | Root group |
| 1 | daemon | Daemon group |
| 2 | kmem | Kernel memory |
| 3 | tty | TTY |
| 4 | operator | Operator (BSD) |
| 5 | staff | Staff (macOS) |
| 20 | games | Games |
| 33 | www-data | Web server |
| 80 | www | Apache |
```

### 1.2 User/Group System Calls

```c
#include <sys/types.h>
#include <unistd.h>
#include <pwd.h>
#include <grp.h>

// Get current IDs
uid_t uid = getuid();       // Real UID
uid_t euid = geteuid();     // Effective UID
uid_t suid = getuid();      // Saved UID (not on all)
gid_t gid = getgid();       // Real GID
gid_t egid = getegid();     // Effective GID

// Get user by UID
struct passwd *pw = getpwuid(uid);
if (pw) {
    printf("User: %s\n", pw->pw_name);
    printf("Home: %s\n", pw->pw_dir);
}

// Get user by name
pw = getpwnam("www-data");
if (pw) {
    printf("UID: %d\n", pw->pw_uid);
}

// Get group by GID
struct group *gr = getgrgid(gid);
if (gr) {
    printf("Group: %s\n", gr->gr_name);
}

// Get group by name
gr = getgrnam("www-data");
```

### 1.3 UID/GID in Process Model

```markdown
## Process Credentials

```
Real UID/GID:      Who started the process
Effective UID/GID: Used for permission checks (normally same as real)
Saved UID/GID:     Preserved across setuid operations
```

## Real vs Effective User

```
┌─────────────────────────────────────────────────────────────┐
│ Process                                                     │
│                                                              │
│  Real UID:     1000 (bob) - who ran the program            │
│  Effective UID: 0 (root) - permissions used for file access │
│  Saved UID:    1000 (bob) - what we can restore to         │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Setuid and Setgid

### 2.1 Setuid Bit

```markdown
## Setuid Bit

When a program has the setuid bit set, it runs with the owner's UID,
not the caller's UID.

```
-rwsr-xr-x  root  staff  12345  /usr/bin/passwd
     ^
     └── 's' means setuid bit is set

When bob runs passwd:
- Real UID: 1000 (bob)
- Effective UID: 0 (root) - because of setuid bit
```

## Finding Setuid Programs

```bash
# Find setuid binaries
find /usr -perm -4000 -type f 2>/dev/null

# Find setgid binaries
find /usr -perm -2000 -type f 2>/dev/null

# Find both
find /usr -perm -6000 -type f 2>/dev/null
```

### 2.2 Setuid/Setgid in Code

```c
// Set UID/GID
setuid(0);   // Set effective UID to root
setgid(0);   // Set effective GID to root

// Set all UIDs at once (preferred)
setreuid(0, 0);   // set real and effective UID
setregid(0, 0);   // set real and effective GID

// POSIX version
setuid(0);  // Sets real, effective, and saved UID if _POSIX_SAVED_IDS

// Check capabilities
uid_t uid, euid, suid;
getresuid(&uid, &euid, &suid);
printf("Real: %d, Effective: %d, Saved: %d\n", uid, euid, suid);

// Drop privileges permanently
if (setuid(getuid()) != 0) {
    // Error - can no longer regain privileges
}

// Restore privileges (only if we have saved UID)
if (seteuid(suid) != 0) {
    // Restored
}
```

### 2.3 Secure Privilege Dropping

```c
// SECURE privilege dropping pattern
void drop_privileges() {
    // 1. Ensure we can regain privileges later
    uid_t original_uid = getuid();

    // 2. Start with minimum privileges
    gid_t groups[1];
    groups[0] = getgid();  // Keep current GID
    setgroups(1, groups);

    // 3. Drop to non-privileged GID
    if (setgid(getgid()) != 0) {
        // Error
    }

    // 4. Drop to non-privileged UID
    if (setuid(original_uid) != 0) {
        // Error
    }

    // 5. Verify
    if (geteuid() == 0 || getuid() == 0) {
        // Still root! Security issue!
    }
}

// UNSAFE patterns to avoid:
// setuid(0) without checking
// Not using saved UID before dropping
// Forking after dropping privileges incorrectly
```

---

## 3. Capabilities (Linux)

### 3.1 Capability Overview

```markdown
## Why Capabilities?

Instead of all-or-nothing root, capabilities divide root's power into
fine-grained units.

## Capability Sets

| Set | Description | Used By |
|-----|-------------|---------|
| Effective | Currently active capabilities | Kernel checks this |
| Permitted | Maximum capabilities allowed | Can be enabled |
| Inheritable | Preserved across exec() | For exec'd programs |
| Bounding | Limits what can be gained | Security boundary |

## Common Capabilities

| Capability | What It Allows |
|-----------|---------------|
| CAP_NET_BIND_SERVICE | Bind to ports < 1024 |
| CAP_NET_RAW | Raw sockets |
| CAP_SYS_CHROOT | chroot() |
| CAP_SYS_ADMIN | Many admin operations |
| CAP_DAC_OVERRIDE | Bypass file permission checks |
| CAP_FOWNER | Bypass owner checks |
| CAP_KILL | Send signals to any process |
| CAP_NET_ADMIN | Network admin operations |
| CAP_SYS_PTRACE | ptrace() any process |
| CAP_SYS_TIME | Set system time |

### 3.2 Using Capabilities

```c
#include <sys/capability.h>

// Check capabilities
cap_t caps = cap_get_proc();
if (cap_get_flag(caps, CAP_NET_BIND_SERVICE, CAP_EFFECTIVE) == 1) {
    printf("Can bind to port < 1024\n");
}
cap_free(caps);

// Enable capability
cap_t caps = cap_get_proc();
cap_value_t cap_list[] = { CAP_NET_BIND_SERVICE };
cap_set_flag(caps, CAP_EFFECTIVE, 1, cap_list, CAP_SET);
cap_set_proc(caps);
cap_free(caps);

// Drop all capabilities (keep bounding set for recovery)
cap_t caps = cap_init();
cap_set_proc(caps);
cap_free(caps);
```

### 3.3 Capability Bounding Set

```c
// Remove capability from bounding set (irreversible)
int ret = prctl(PR_CAPBSET_DROP, CAP_NET_RAW, 0, 0, 0);
if (ret == -1) {
    perror("prctl failed");
}

// Check if capability in bounding set
int has_cap = prctl(PR_CAPBSET_READ, CAP_NET_RAW, 0, 0, 0);
```

---

## 4. Access Control Lists (ACLs)

### 4.1 POSIX ACLs (Linux/BSD)

```c
#include <sys/acl.h>

// Get ACL from file
acl_t acl = acl_get_file("/path/to/file", ACL_TYPE_ACCESS);
if (acl == NULL) {
    // Error
}

// Check for specific entry
acl_entry_t entry;
acl_tag_t tag;
uid_t *qualifier;
acl_perm_t perms;

for (int i = ACL_FIRST_ENTRY; ; i = ACL_NEXT_ENTRY) {
    if (acl_get_entry(acl, i, &entry) != 1) break;

    acl_get_tag_type(entry, &tag);
    if (tag == ACL_USER) {
        qualifier = (uid_t *)acl_get_qualifier(entry);
        perms = acl_get_permset(entry);
        printf("User %d has permissions\n", *qualifier);
    }
}
acl_free(acl);

// Set ACL on file
acl_t acl = acl_from_text("u:www-data:rw");
acl_set_file("/path/to/file", ACL_TYPE_ACCESS, acl);
acl_free(acl);
```

### 4.2 Windows ACLs

```c
#include <windows.h>
#include <aclapi.h>

// Get security descriptor
PSECURITY_DESCRIPTOR pSD = NULL;
PACL pDACL = NULL;
GetSecurityInfo(
    hFile,           // Handle or NULL for current process
    SE_FILE_OBJECT,
    DACL_SECURITY_INFORMATION,
    NULL, NULL,
    &pDACL,
    NULL,
    &pSD
);

// Create explicit ACE
EXPLICIT_ACCESS ea = {0};
ea.grfAccessPermissions = FILE_GENERIC_READ;
ea.grfAccessMode = GRANT_ACCESS;
ea.Trustee.TrusteeForm = TRUSTEE_IS_NAME;
ea.Trustee.ptstrName = "Users";

PACL pNewDACL;
DWORD dwResult = SetEntriesInAcl(1, &ea, pDACL, &pNewDACL);

SetSecurityInfo(
    hFile,
    SE_FILE_OBJECT,
    DACL_SECURITY_INFORMATION | UNPROTECTED_DACL_SECURITY_INFORMATION,
    NULL, NULL,
    pNewDACL,
    NULL
);

LocalFree(pNewDACL);
LocalFree(pSD);
```

### 4.3 ACL Comparison

```markdown
## ACL Types

| System | ACL Type | Notes |
|--------|----------|-------|
| Linux | POSIX ACLs | getfacl/setfacl commands |
| FreeBSD | NFSv4 ACLs | Richer, like Windows |
| macOS | NFSv4 ACLs | Using chmod -X |
| Windows | Windows ACLs | security descriptor |

## Common ACL Patterns

| Pattern | Linux | Windows |
|--------|-------|---------|
| Everyone read | ACL_READ:world | Everyone:R |
| Owner full | USER:F | SYSTEM:F |
| Admin read/write | ADMIN:RW | Administrators:RW |
| No access | - | Creator Owner:N |
```

---

## 5. Privilege Escalation Patterns

### 5.1 Sudo Configuration

```bash
# /etc/sudoers examples
user ALL=(ALL:ALL) ALL          # Full sudo for user
%wheel ALL=(ALL) NOPASSWD: ALL  # NOPASSWD for group
john ALL=(www-data) /usr/bin/whoami  # Run as specific user

# Sudoers syntax
# user host=(runas:runas) options command
```

### 5.2 Sudo in Code

```c
// Execute command as another user via sudo
int run_as_user(const char *user, const char *cmd) {
    pid_t pid = fork();
    if (pid == 0) {
        // Child
        execlp("sudo", "sudo", "-u", user, "sh", "-c", cmd, NULL);
        _exit(127);
    }
    // Parent
    int status;
    waitpid(pid, &status, 0);
    return WIFEXITED(status) ? WEXITSTATUS(status) : -1;
}
```

### 5.3 Polkit (Linux)

```c
// Polkit authorization check
#include <polkit/polkit.h>

PolkitAuthority *auth = polkit_authority_get_sync(NULL, NULL);
PolkitAuthorizationResult *result = polkit_authority_check_authorization_sync(
    auth,
    NULL,  // Use default subject
    "org.freedesktop.login1.reboot",
    NULL,  // No details
    POLKIT_CHECK_AUTHORIZATION_FLAGS_NONE,
    NULL
);

if (polkit_authorization_result_get_is_authorized(result) == POLKIT_AUTHORIZATION_YES) {
    // Authorized
}

g_object_unref(result);
g_object_unref(auth);
```

---

## 6. Jail and Containers

### 6.1 FreeBSD Jail

```c
#include <sys/jail.h>

// Create jail parameters
struct jailparam params[] = {
    JAILPARAM_CHROOT, "/var/jails/myjail",
    JAILPARAM_HOSTNAME, "jailedhost",
    JAILPARAM_IP4, "10.0.0.1",
    JAILPARAM_DOMAIN, "example.com"
};

// Create jail
int jid = jail_set(params, JAIL_CREATE);
if (jid < 0) {
    perror("jail_create failed");
}

// Enter jail (child process)
if (jail_attach(jid) != 0) {
    // Error
}

// Or create and enter in one step
struct jailparams params2[] = {
    JAILPARAM_CHROOT, "/var/jails/myjail",
    JAILPARAM_HOSTNAME, "jailedhost"
};
int jid = jail(params2, JAIL_CREATE | JAIL_ATTACH);
```

### 6.2 Linux Namespaces

```c
// Linux namespace isolation
#define _GNU_SOURCE
#include <sched.h>
#include <sys/wait.h>

// Create new namespace
int child_pid = clone(
    child_func,           // Function to run
    child_stack,          // Stack for child
    CLONE_NEWUTS |        // UTS namespace (hostname)
    CLONE_NEWIPC |        // IPC namespace
    CLONE_NEWNET |        // Network namespace
    CLONE_NEWPID |        // PID namespace
    CLONE_NEWNS |         // Mount namespace
    CLONE_NEWUSER,        // User namespace
    NULL
);

// In child:
// Now in isolated namespace
unshare(CLONE_NEWUTS);  // Can unshare later
```

### 6.3 Seccomp

```c
#include <seccomp.h>

// Create seccomp context
scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_KILL);  // Default: kill

// Allow specific syscalls
seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0);
seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(openat), 0);

// Allow with arguments
seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(openat),
    SCMP_A0(SCMP_CMP_EQ, O_RDONLY));

// Load filter
seccomp_load(ctx);
seccomp_release(ctx);

// Now only allowed syscalls work
```

---

## 7. Securelevel (BSD/macOS)

### 7.1 Securelevel Overview

```markdown
## FreeBSD Securelevel

| Level | Name | Restrictions |
|-------|------|--------------|
| -1 | Permanently insecure | No restrictions |
| 0 | Insecure | Can load/unload modules |
| 1 | Highly insecure | Cannot set securelevel |
| 2 | Secure | Cannot mount/umount |
| 3 | Highly secure | Cannot modify kernel |

## Current Securelevel

```bash
sysctl kern.securelevel
```

## Restrictions by Level

| Operation | -1 | 0 | 1 | 2 | 3 |
|-----------|---|---|---|---|---|
| Load kernel modules | Yes | No | No | No | No |
| Write to /dev/mem | Yes | Yes | No | No | No |
| Modify sysctl | Yes | Yes | Yes | No | No |
| Mount filesystem | Yes | Yes | Yes | No | No |
| Set UID to 0 | Yes | Yes | Yes | Yes | No |
```

---

## 8. Privilege Analysis Template

### 8.1 Privilege Requirements

```markdown
## Privilege Analysis

### Application: <Name>
### Target OS: <Target>
### Analysis Date: <Date>

### Required Privileges

| Privilege | Purpose | How Acquired |
|-----------|---------|--------------|
| Root (UID 0) | Bind to port 80 | setuid binary or capability |
| Write to /var/log | Logging | Group 'adm' or ACL |
| Access config | Read /etc/app | Normal user read |

### User/Group Requirements

| User | Group | Home | Purpose |
|------|-------|------|---------|
| app | app | /var/lib/app | Application user |
| www-data | www-data | /nonexistent | Web server |
| root | wheel | /root | Emergency access |

### Privilege Operations

| Operation | Location | Implementation | Portability |
|----------|----------|---------------|-------------|
| setuid(0) | main.c:42 | Gain root | Portable |
| setgid(0) | main.c:43 | Gain root | Portable |
| initgroups("app", 0) | main.c:50 | Set supplementary groups | Portable |
| chroot("/var/jail") | jail.c:20 | Sandbox | BSD/Linux only |
| prctl(PR_SET_DUMPABLE) | debug.c:10 | Core dumps | Linux only |

### Privilege Dropping

| Location | Drop To | When |
|----------|---------|------|
| main.c:100 | www-data:www-data | After binding port |
| worker.c:30 | nobody:nobody | After initialization |

### Security Mechanisms

| Mechanism | Location | Notes |
|-----------|----------|-------|
| Capabilities | caps.c | Linux-only, use setuid as fallback |
| Seccomp | seccomp.c | Linux-only |
| jail | jail.c | BSD-only |
| AppArmor | apparmor.c | Linux-only |
| SELinux | selinux.c | Linux-only |
```

### Recommendations
1. Replace capabilities with setuid for portability
2. Remove chroot(), use containers instead
3. Consider privilege-separated architecture
```

---

## Validation Checklist

Before declaring privilege analysis complete:

- [ ] All UID/GID requirements documented
- [ ] Setuid/setgid programs identified
- [ ] Privilege dropping points mapped
- [ ] Capability usage identified
- [ ] ACL usage documented
- [ ] Chroot/jail usage found
- [ ] Sudo requirements identified
- [ ] Portability issues noted

## Reference

See system-call-analyzer for related system calls.