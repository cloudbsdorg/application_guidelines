# Chapter 4: Task Tables

**Document ID:** PLANNING-001-04
**Chapter:** 4 of 10
**Last Updated:** 2026-05-02

---

## Task Table Format

Plan documents that contain implementation tasks must use a standardized task table:

```markdown
| ID | Task | Priority | Status | Assigned To | Owner | Phase | Start | End | Dependencies | Files | Spec | Notes |
|----|------|----------|--------|-------------|-------|-------|-------|-----|--------------|-------|------|-------|
| 300.1 | Create module entry point | P0 | ⬜ PENDING | | | Phase 1 | | | | `sys/foo/foo_mod.c` | [Spec](#3001) | |
```

## Spec Column — Linking to Detailed Specifications

The `Spec` column provides a link to the detailed specification for that task.

**Format:**
- `[Spec](#<task-id>)` — Anchor link to section within same document
- `[Spec](300-Impl.md#<task-id>)` — Link to section in external document

**Example task with specification:**

In the task table:
```
| 300.1 | Create module entry point | P0 | ⬜ PENDING | | | Phase 1 | | | | `sys/foo/foo_mod.c` | [Spec](#3001) | |
```

In the detailed spec section:
```markdown
### 300.1 Create module entry point {#3001}

**Detailed Specification:**

- Create `sys/foo/foo_mod.c` with module metadata
- Register module with `MODULE_DEPEND`
- Initialize sysctl tree under `net.graph.foo`

**Acceptance Criteria:**
- [ ] Module loads without panic
- [ ] `kldstat` shows module loaded
- [ ] Sysctl `net.graph.foo.enable` exists

**Test Steps:**
1. `sudo kldload foo`
2. `sysctl net.graph.foo.enable`
3. Verify output is `0` (disabled by default)
```

**Task ID Anchor Convention:**
- Task ID `300.1` → Anchor `#3001` (dots removed)
- Task ID `700.12` → Anchor `#70012`
- Task ID `301.3` → Anchor `#3013`

---

## Priority Values

| Priority | Meaning |
|----------|---------|
| `P0` | Critical path blocker, must complete before anything else |
| `P1` | Important but can be worked in parallel |
| `P2` | Standard task, normal priority |
| `P3` | Nice to have, can be deferred |

## Status Values

| Status | Meaning |
|--------|---------|
| `⬜ PENDING` | Not yet started, available to claim |
| `🔄 IN PROGRESS` | Claimed and being worked on |
| `🟡 BLOCKED` | Cannot proceed; reason noted in `Notes` |
| `⏸️ PAUSED` | Temporarily suspended; will resume later |
| `✅ DONE` | Completed and verified |
| `❌ FAILED` | Could not be completed; reason noted in `Notes` |

---

## Phase Structure

Implementation is organized into phases:

| Phase | Focus | Description |
|-------|-------|-------------|
| Phase 1 | Kernel | Core kernel module implementation |
| Phase 1.5 | Auto-scaling | Dynamic scaling infrastructure |
| Phase 2 | Userland | Userland tools and utilities |
| Phase 3 | Integration | Full system integration and testing |
| Phase 4 | Validation | Comprehensive validation and sign-off |

---

## Claiming Protocol

1. Verify all dependencies are `✅ DONE`
2. Set `Status` to `🔄 IN PROGRESS`
3. Set `Assigned To` to your identifier (hostname for agents)
4. Set `Start` to current UTC timestamp (`YYYY-MM-DD HH:MM UTC`)
5. Commit and push immediately so other agents see the claim

## Completion Protocol

1. Implement the task and verify all tests pass
2. Set `Status` to `✅ DONE`
3. Set `End` to current UTC timestamp
4. Update `Notes` with a brief summary
5. Commit and push immediately

---

## TODO Tracker Summary Table

The TODO Tracker provides a high-level progress overview across all phases. Include this summary table in the Implementation Tasks document (`0300`) and update it after each task completion:

```markdown
## TODO Tracker Summary

| Phase | Focus | Tasks | Completed | Total | Progress |
|-------|-------|-------|-----------|-------|----------|
| Phase 1 | Kernel | Core kernel module | 0 | 20 | 0% |
| Phase 2 | Userland | Userland tools | 0 | 15 | 0% |
| Phase 3 | Integration | Full system integration | 0 | 25 | 0% |
| Phase 4 | Validation | Comprehensive validation | 0 | 30 | 0% |
| **Total** | | | **0** | **90** | **0%** |
```

**Update Protocol:**
1. After completing a task, update both the task row and recalculate the phase and total progress
2. Commit the TODO Tracker update alongside the task completion
3. Use emoji states: `⬜` not started, `🔄` in progress, `✅` completed

---

## Build Status Integration

Each project must maintain a `0002-<Project>-Build-Status.md` file:

```markdown
# Build Status

**Last Updated:** YYYY-MM-DD HH:MM UTC

## CI/CD Pipeline

| Component | Build | Test | Deploy |
|-----------|-------|------|--------|
| Kernel Module | ✅ PASS | ✅ PASS | N/A |
| Userland Tools | 🔄 BUILDING | ⏳ PENDING | ⏳ PENDING |

## Artifacts

- `sys/modules/pppoe_lb/` — Kernel module build artifacts
- `usr.sbin/pppoe_lb/` — Userland tool build artifacts
```