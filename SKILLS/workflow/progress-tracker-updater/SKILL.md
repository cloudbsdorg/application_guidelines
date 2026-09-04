---
name: progress-tracker-updater
description: >-
  Create and update the TODO Tracker Summary tables that show phase progress
  across a project's plan. Use when tasks change state, when a phase
  completes, or when the tracker has drifted from the task tables it
  summarises.
---

# Skill: progress-tracker-updater

**Purpose:** Create and maintain TODO Tracker Summary tables for project phase progress tracking.

**Triggers:** When creating Implementation Tasks document (0300), or when user asks to update progress.

## Loading Instructions

Load this skill when the user asks you to:
- Create a TODO Tracker Summary table
- Update task completion percentages
- Generate progress reports
- Track phase completion

## TODO Tracker Summary Table Format

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

## Task States

| Emoji | State | Meaning |
|-------|-------|---------|
| `⬜` | PENDING | Not yet started, available to claim |
| `🔄` | IN PROGRESS | Claimed and being worked on |
| `✅` | DONE | Completed and verified |
| `🟡` | BLOCKED | Cannot proceed |
| `❌` | FAILED | Could not be completed |

## Update Protocol

1. **When claiming a task:**
   - Update phase `Completed` count (if applicable)
   - Recalculate phase `Progress` percentage
   - Recalculate total `Completed` and `Progress`

2. **When completing a task:**
   - Increment phase `Completed` count
   - Recalculate: `Progress = (Completed / Total) * 100`
   - Format to 1 decimal place: `42.9%`

3. **Always include:**
   - Emoji state in `Completed` column: `✅ 5` vs `⬜ 0`
   - Updated timestamp in commit message

## Progress Calculation Formulas

```markdown
Per-phase progress:
  Phase Progress = (Phase Completed / Phase Total) × 100

Overall progress:
  Total Progress = (Sum of Completed / Sum of Total) × 100
```

## Example: Before and After

**Before completing Phase 1 Task 3:**

| Phase | Focus | Completed | Total | Progress |
|-------|-------|-----------|-------|----------|
| Phase 1 | Kernel | ✅ 2 | 20 | 10.0% |

**After completing Phase 1 Task 3:**

| Phase | Focus | Completed | Total | Progress |
|-------|-------|-----------|-------|----------|
| Phase 1 | Kernel | ✅ 3 | 20 | 15.0% |

## Integration with Task Tables

The TODO Tracker Summary should be placed at the top of the Implementation Tasks document (`0300-<Project>-Implementation-Tasks.md`), directly above the detailed task tables.

Each task row in the detailed table should use emoji states:
```markdown
| 300.1 | Create module entry point | P0 | ✅ DONE | | Phase 1 | ...
```

## Multi-Phase Tracking

For projects with phases spanning multiple documents:

```markdown
## Phase 1 Summary

| Component | Tasks | Completed | Total | Progress |
|-----------|-------|-----------|-------|----------|
| Kernel Module | Kernel tasks | ✅ 5 | 10 | 50.0% |
| Sysctl Tree | Sysctl tasks | ⬜ 0 | 5 | 0.0% |
| **Phase 1 Total** | | **5** | **15** | **33.3%** |
```

## Progress Bar Visualization

Optionally add ASCII progress bars:

```markdown
Phase 1: [████████░░░░░░░░░░░░] 40.0% (8/20 tasks)
Phase 2: [░░░░░░░░░░░░░░░░░░░] 0.0% (0/15 tasks)
Overall: [███░░░░░░░░░░░░░░░░] 17.1% (8/47 tasks)
```

## Validation

Before updating, verify:
- [ ] All task statuses in the phase are accurate
- [ ] Completed count matches `✅ DONE` tasks
- [ ] Progress percentage is mathematically correct
- [ ] Total row sums are correct
- [ ] Changes are committed immediately after update