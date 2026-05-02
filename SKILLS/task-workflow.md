# Skill: task-workflow

**Purpose:** Enforce the claiming and completion protocols defined in the Planning Guidelines.

**Triggers:** When an agent needs to pick a task, claim a task, complete a task, or update task status.

## Loading Instructions

Load this skill when the user asks you to:
- Pick a task / Claim a task
- Complete a task / Mark task as done
- Update task status
- Work on an implementation task

## Capabilities

### 1. Parse Task Tables

Given a plan document with task tables, extract and validate:
- Task ID, description, priority, status
- Dependencies (must be `✅ DONE` before claiming)
- Assigned To, Start, End timestamps
- Files associated with the task

### 2. Claim Task Protocol

Execute these steps in order:

```
1. Verify all dependencies in the task's "Dependencies" column are ✅ DONE
2. Set Status → 🔄 IN PROGRESS
3. Set Assigned To → <hostname> (agent identifier)
4. Set Start → current UTC timestamp (YYYY-MM-DD HH:MM UTC)
5. Commit: git add <file>.md && git commit -m "Claim task <ID>: <description>" && git push
```

### 3. Complete Task Protocol

Execute these steps in order:

```
1. Implement the task following the plan document specifications
2. Run all unit tests and verify they pass
3. Set Status → ✅ DONE
4. Set End → current UTC timestamp
5. Update Notes with a brief summary of changes
6. Commit: git add -A && git commit -m "Complete task <ID>: <description>" && git push
```

### 4. Status Transitions

| Current | Valid Transitions |
|---------|-------------------|
| ⬜ PENDING | 🔄 IN PROGRESS, ❌ FAILED |
| 🔄 IN PROGRESS | ✅ DONE, 🟡 BLOCKED, ⏸️ PAUSED |
| 🟡 BLOCKED | 🔄 IN PROGRESS (when unblocked) |
| ⏸️ PAUSED | 🔄 IN PROGRESS |
| ✅ DONE | (no transitions - historical) |
| ❌ FAILED | 🔄 IN PROGRESS (retry) |

### 5. Handle Blocked Tasks

When a task cannot proceed:
1. Set Status → 🟡 BLOCKED
2. In Notes column, document the blocking issue
3. Commit and push: `git add <file>.md && git commit -m "Block task <ID>: <reason>" && git push`

### 6. Detect Impossible Dependencies

If a task claims dependency on a non-existent task or a task marked ❌ FAILED:
- Report the issue to the user
- Do not claim the task

## Task Table Format

```
| ID | Task | Priority | Status | Assigned To | Owner | Phase | Start | End | Dependencies | Files | Notes |
|----|------|----------|--------|-------------|-------|-------|-------|-----|--------------|-------|-------|
| 300.1 | Create module entry point | P0 | ⬜ PENDING | | | Phase 1 | | | | `sys/foo/foo_mod.c` | |
```

## Priority Levels

| Priority | Meaning |
|----------|---------|
| P0 | Critical path blocker - must complete before anything else |
| P1 | Important but can be worked in parallel |
| P2 | Standard task, normal priority |
| P3 | Nice to have, can be deferred |

## Phase Structure

| Phase | Focus |
|-------|-------|
| Phase 1 | Kernel |
| Phase 1.5 | Auto-scaling |
| Phase 2 | Userland |
| Phase 3 | Integration |
| Phase 4 | Validation |

## Reference

See Planning/PLANNING.md Section 4 (Task Tables) for full specification.