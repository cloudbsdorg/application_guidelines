---
name: review
description: >-
  Review code for correctness, security, and FreeBSD/CloudBSD conventions. Use
  when reviewing a pull request or a diff, when asked to check work before it
  lands, and before approving anything that touches configuration, privilege,
  or persistence.
keywords:
  - review
  - code review
  - check my work
  - lgtm
  - approve
---

# Code Review Skill


## Review Protocol

Code review is NOT just style checking. Review for: **correctness, security, maintainability, FreeBSD conventions.**

## Review Checklist

### Correctness
- [ ] Does it do what the PR/issue claims?
- [ ] Edge cases handled?
- [ ] Error paths tested?
- [ ] No off-by-one errors
- [ ] No race conditions (for concurrent code)

### Security
- [ ] Input validated?
- [ ] Credentials not logged or exposed?
- [ ] File permissions correct?
- [ ] Jails properly isolated (if applicable)?
- [ ] No shell injection in system calls?

### FreeBSD Conventions
- [ ] Uses rc.d for services (not systemd)
- [ ] Correctly uses ZFS datasets (not LVM)
- [ ] Respects FreeBSD filesystem hierarchy (`/usr/local` for third-party)
- [ ] Uses `sysctl` for kernel parameters, not procfs hacks
- [ ] Capsicum ready (if sandboxing needed)

### Maintainability
- [ ] Code is readable (self-documenting names)
- [ ] Complex logic has comments
- [ ] No magic numbers (constants with names)
- [ ] Functions are small and single-purpose
- [ ] No copy-paste duplication

### Style (Accept Project Norms)
- [ ] Indentation consistent
- [ ] No trailing whitespace
- [ ] Line lengths reasonable (80-100 chars)
- [ ] Imports/packages sorted

## Review Comments Format

```
**File**: `src/service.c` line 42
**Issue**: Potential null dereference
**Severity**: High
**Suggestion**: Check `$ptr` before use at line 41
```

Or for nitpicks:
```
nit: Consider renaming `x` to `bytes_read` for clarity
```

## Approval Criteria

For approval, code must be:
1. **Correct** - Does the job, no obvious bugs
2. **Safe** - No security vulnerabilities
3. **FreeBSD-native** - Uses platform conventions
4. **Maintainable** - Others can understand and modify

## Review States

| State | Meaning |
|-------|---------|
| **APPROVED** | Ready to merge |
| **CHANGES_REQUESTED** | Author must address specific issues |
| **BLOCKED** | Major problems found |
| **COMMENT_ONLY** | Feedback provided, no blocking issues |

## FreeBSD-Specific Review Focus

### Kernel Modules
- Correct locking primitives
- Proper memory allocation (uma(9), not malloc)
- adherence to style(9)

### Userland Services
- rc.d script conventions
- Proper daemonization (newsyslog, pidfile)
- Signal handling correctness

### Scripts
- Shellcheck clean (for shell scripts)
- `/bin/sh` compatibility (not bashisms)
- Proper error handling with `set -e`

## Completion

- [ ] All files reviewed
- [ ] Security concerns raised if any
- [ ] FreeBSD conventions verified
- [ ] Specific feedback provided
- [ ] Decision stated (approve/request changes/blocked)
