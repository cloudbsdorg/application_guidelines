---
name: build-status-updater
description: >-
  Maintain a project's build status document for CI/CD tracking. Use when a
  build result changes, when CI is added or reconfigured, or when the recorded
  status no longer matches reality.
keywords:
  - build status
  - CI
  - CD
  - 0002 document
---

# Skill: build-status-updater

**Purpose:** Maintain the build-status.md file for CI/CD tracking and status reporting.

**Triggers:** After build/test events, when components change state, or when updating build status.

## Loading Instructions

Load this skill when the user asks you to:
- Update build status
- Track CI/CD pipeline status
- Create build-status.md
- Report on component build health

## File Location

The `0002-<Project>-Build-Status.md` file lives in the `.plan/` directory:

```
<project-root>/
├── .plan/
│   ├── 0002-<Project>-Build-Status.md    <-- This file
│   └── ...
```

## Document Structure

```markdown
# Build Status

**Last Updated:** YYYY-MM-DD HH:MM UTC
**Pipeline:** <CI system> (e.g., GitHub Actions, Jenkins)

---

## CI/CD Pipeline

| Component | Build | Unit Tests | Integration Tests | Deploy |
|-----------|-------|------------|------------------|--------|
| Kernel Module | ✅ PASS | ✅ PASS | 🔄 IN PROGRESS | N/A |
| Userland Tools | ✅ PASS | ⏳ PENDING | ⏳ PENDING | ⏳ PENDING |
| Documentation | ✅ PASS | N/A | N/A | 🔄 IN PROGRESS |

## Component Details

### Kernel Module

| Metric | Value |
|--------|-------|
| Last Build | 2026-05-02 10:30 UTC |
| Build Duration | 45s |
| Test Coverage | 87% |
| Artifacts | `sys/modules/pppoe_lb/` |

### Userland Tools

| Metric | Value |
|--------|-------|
| Last Build | 2026-05-02 10:35 UTC |
| Build Duration | 12s |
| Test Coverage | 92% |
| Artifacts | `usr.sbin/pppoe_lb/` |

## Recent Activity

| Timestamp | Component | Event | Status |
|-----------|-----------|-------|--------|
| 10:35 UTC | Userland Tools | Build #142 | ✅ PASS |
| 10:30 UTC | Kernel Module | Build #142 | ✅ PASS |
| 10:28 UTC | Kernel Module | Test #142.3 | 🔄 IN PROGRESS |

## Artifacts

| Artifact | Location | Last Updated |
|----------|----------|-------------|
| Kernel module (KO) | `sys/modules/pppoe_lb/pppoe_lb.ko` | 2026-05-02 10:30 |
| Userland binary | `usr.sbin/pppoe_lb/pppoe_lb` | 2026-05-02 10:35 |
| Test report | `tests/report.html` | 2026-05-02 10:32 |

## Validation Status

| Check | Status |
|-------|--------|
| Code linting | ✅ PASS |
| Security scan | ✅ PASS |
| Memory sanitizers | 🔄 IN PROGRESS |
| Concurrency tests | ⏳ PENDING |

---

**Next Update:** YYYY-MM-DD HH:MM UTC
```

## Status Values

| Status | Meaning |
|--------|---------|
| ✅ PASS | Completed successfully |
| ❌ FAIL | Failed |
| 🔄 IN PROGRESS | Currently running |
| ⏳ PENDING | Queued, not yet started |
| N/A | Not applicable |

## CI/CD Stage Definitions

| Stage | Description |
|-------|-------------|
| Build | Compile source code, generate binaries |
| Unit Tests | Run isolated component tests |
| Integration Tests | Run system-wide tests |
| Deploy | Package and publish artifacts |

## Update Protocol

When status changes:

1. Update the relevant component row
2. Add entry to Recent Activity table
3. Update "Last Updated" timestamp
4. Commit: `git add .plan/0002-<Project>-Build-Status.md && git commit -m "Update build status: <component> <status>" && git push`

## Artifact Registry

| Component | Artifact Path | Build Command |
|-----------|---------------|--------------|
| Kernel Module | `sys/modules/<project>/` | `make -C sys/modules/<project>` |
| Userland Tools | `usr.sbin/<project>/` | `make -C usr.sbin/<project>` |
| Tests | `tests/` | `atf-sh tests/` |

## Validation Gates

```markdown
## Quality Gates

| Gate | Threshold | Current |
|------|-----------|---------|
| Line coverage | as close to 100% as possible | 99% ✅ |
| Branch coverage | as close to 100% as possible | 98% ✅ |
| Critical paths | 100% | 100% ✅ |
| Security findings | 0 Critical | 0 ✅ |
| Lint errors | 0 | 2 ⚠️ |
```

## Badge URLs (for README)

```markdown
[![Build Status](https://github.com/cloudbsdorg/<project>/actions/workflows/ci.yaml/badge.svg)](https://github.com/cloudbsdorg/<project>/actions)
[![Test Coverage](https://codecov.io/gh/cloudbsdorg/<project>/branch/main/graph/badge.svg)](https://codecov.io/gh/cloudbsdorg/<project>)
```

## Template for New build-status.md

```markdown
# Build Status

**Last Updated:** YYYY-MM-DD HH:MM UTC
**Pipeline:** GitHub Actions
**Main Branch:** main

---

## CI/CD Pipeline

| Component | Build | Unit Tests | Integration Tests | Deploy |
|-----------|-------|------------|------------------|--------|
| Kernel Module | ⬜ PENDING | ⬜ PENDING | ⬜ PENDING | N/A |
| Userland Tools | ⬜ PENDING | ⬜ PENDING | ⬜ PENDING | ⬜ PENDING |
| Documentation | ⬜ PENDING | N/A | N/A | ⬜ PENDING |

## Artifacts

| Artifact | Location |
|----------|----------|
| Kernel module | `sys/modules/<project>/<project>.ko` |
| Userland binary | `usr.sbin/<project>/<project>` |

---

**Next Update:** YYYY-MM-DD HH:MM UTC
```

## Integration with Plan Documents

The build-status.md should be referenced in:
- `000-<Project>-TOC.md` (Quick Links section)
- `000-<Project>-TOC.md` (Build Status Summary section)

## Validation Checklist

- [ ] All components are listed
- [ ] Status values are valid
- [ ] Timestamps are in UTC
- [ ] Recent Activity is chronological
- [ ] Artifacts paths are accurate
- [ ] Git push after updates

## Reference

See Planning/PLANNING.md Section 4.6 (Build Status Integration) for full specification.