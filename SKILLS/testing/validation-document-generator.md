---
name: validation document generator
description: Create validation reports and validation corrections reports following the CloudBSD standard format.
---

# Skill: validation-document-generator

**Purpose:** Create validation reports and validation corrections reports following the CloudBSD standard format.

**Triggers:** When validating implementation tasks, creating validation reports, or documenting corrections.

## Loading Instructions

Load this skill when the user asks you to:
- Create a validation report
- Validate implementation tasks
- Document validation corrections
- Calculate validation summary statistics

## Document Types

### 1. Validation Report (9XX)

Independent validation of all implemented tasks.

### 2. Validation Corrections Report (9XX.1)

Document discrepancies between implementation plan and validation report.

---

## Validation Report Structure

```markdown
# <Project> Validation Report

> **Purpose:** Independent validation of all implemented tasks
> **Validation Method:** Code review, compilation verification, and implementation accuracy check
> **Generated:** YYYY-MM-DD

---

## Validation Status Legend

| Status | Meaning |
|--------|---------|
| ✅ Valid | Implementation is correct, complete, and matches task description |
| ❌ Invalid | Implementation has errors, is incomplete, or doesn't match task description |
| ⚠️ Partial | Implementation is partially complete or has minor issues |
| ⏳ Not Started | Task not yet implemented or not yet validated |

---

## Table of Contents

1. [Validation Status Legend](#validation-status-legend)
2. [Phase S0: <Name>](#phase-s0-<name>) - N tasks (N validated)
3. [Validation Summary](#validation-summary)
4. [Detailed Validation Findings](#detailed-validation-findings)
```

---

## Per-Phase Task Table Format

```markdown
## Phase S0: <Phase Name>

| # | Task | Status | Assigned To | Validation Status | Validated By | Validation Date | Validation Comments |
|---|------|--------|------------|-------------------|--------------|-----------------|---------------------|
| S0.1 | Implement module entry point | ✅ DONE | freedev002 | ✅ Valid | freedev003 | 2026-04-27 | Verified... [Task Link](path/to/task.md#anchor) |
| S0.2 | Implement sysctl interface | ✅ DONE | freedev002 | ✅ Valid | freedev003 | 2026-04-27 | Verified... |
```

### Columns:
- **#** — Task ID from implementation plan
- **Task** — Brief task description
- **Status** — Implementation status (⬜ PENDING, 🔄 IN PROGRESS, ✅ DONE, etc.)
- **Assigned To** — Agent/developer who implemented
- **Validation Status** — ✅ Valid, ❌ Invalid, ⚠️ Partial, ⏳ Not Started
- **Validated By** — Agent/developer who validated
- **Validation Date** — Date of validation (YYYY-MM-DD)
- **Validation Comments** — Detailed findings and verification notes

---

## Validation Summary Table

```markdown
## Validation Summary

| Phase | Total Tasks | Valid | Invalid | Partial | Not Started | % Valid (Completed) | % Valid (Overall) |
|-------|-------------|-------|---------|---------|-------------|---------------------|-------------------|
| S0 | 8 | 8 | 0 | 0 | 0 | 100.0% | 100.0% |
| S1 | 7 | 7 | 0 | 0 | 0 | 100.0% | 100.0% |
| S2 | 10 | 10 | 0 | 0 | 0 | 100.0% | 100.0% |
| **Total** | **94** | **77** | **0** | **0** | **17** | **100.0%** | **81.9%** |
```

### Calculation Formulas

**For each phase row:**
```
% Valid (Completed) = Valid / (Valid + Invalid + Partial) × 100
% Valid (Overall) = Valid / Total × 100
```

**For totals row:**
```
Total Tasks = SUM(phase Total Tasks)
Valid = SUM(phase Valid)
Invalid = SUM(phase Invalid)
Partial = SUM(phase Partial)
Not Started = SUM(phase Not Started)
% Valid (Completed) = Valid / (Valid + Invalid + Partial) × 100
% Valid (Overall) = Valid / Total Tasks × 100
```

### Calculation Examples

**Example 1: Phase with all tasks validated**
```
Total = 8, Valid = 8, Invalid = 0, Partial = 0, Not Started = 0
% Valid (Completed) = 8 / (8 + 0 + 0) × 100 = 100.0%
% Valid (Overall) = 8 / 8 × 100 = 100.0%
```

**Example 2: Phase with some tasks not started**
```
Total = 10, Valid = 6, Invalid = 0, Partial = 0, Not Started = 4
% Valid (Completed) = 6 / (6 + 0 + 0) × 100 = 100.0%
% Valid (Overall) = 6 / 10 × 100 = 60.0%
```

**Example 3: Phase with partial implementations**
```
Total = 10, Valid = 5, Invalid = 0, Partial = 3, Not Started = 2
% Valid (Completed) = 5 / (5 + 0 + 3) × 100 = 62.5%
% Valid (Overall) = 5 / 10 × 100 = 50.0%
```

---

## Validation Corrections Report Structure

```markdown
# <Project> — Validation Corrections Report

> **Purpose:** Document discrepancies between implementation plan and validation report
> **Generated:** YYYY-MM-DD
> **Updated:** YYYY-MM-DD HH:MM
> **Validated by:** <Agent>

---

## Executive Summary

| Metric | Value |
|--------|-------|
| Total Tasks in Implementation Plan | 188 |
| Total Tasks in Validation Report | 79 |
| Tasks Validated as Complete | 188 |
| Tasks NOT STARTED | 0 |
| Implementation Completion Rate | 100% |
```

---

## Implementation Status by Phase

```markdown
## Implementation Status by Phase

### All Tasks Completed

| Phase | Tasks | Status |
|-------|-------|--------|
| S0-S6 | Core infrastructure | ✅ DONE |
| S7 | Memory Management | ✅ DONE |
| S8 | Audit Logging | ✅ DONE |
```

---

## Discrepancies Resolution

```markdown
## Discrepancies Resolution

### Resolution Status

| Issue | Resolution |
|-------|------------|
| Audit Logging (S8) | ✅ Verified: `emu_audit.c` exists |
| Securelevel (S10) | ✅ Verified: `emu_securelevel.c` exists |
```

---

## Implementation Summary

```markdown
## Implementation Summary

### Final Task Count

| Document | Total Tasks | Done | Blocked |
|----------|-------------|------|---------|
| Implementation Plan | 188 | 188 | 0 |
| Test Coverage (TC) | 79 | 79 | 0 |
| **Total** | **267** | **267** | **0** |
```

---

## Verification Checklist

```markdown
## Verification Checklist

All items have been verified:

- [x] Source files exist for all tasks
- [x] All phases completed with proper implementation
- [x] Test coverage implemented for all major components
- [x] No remaining blockers
- [x] Implementation plan shows 100% completion
```

---

## Detailed Validation Findings

Include a full repeating of all phase tables from the main validation report for reference.

---

## Document Footer

```markdown
---

*This document is part of the <project> documentation suite.*
*Last Updated: YYYY-MM-DD HH:MM by <Agent>*
```

---

## Validation Checklist

When creating a validation report, verify:

- [ ] Validation status legend is present and correct
- [ ] Table of contents matches document structure
- [ ] Each phase has its own task table
- [ ] All tasks have validation status
- [ ] Validation comments reference specific code/verification
- [ ] Task links point to correct implementation document
- [ ] Summary table calculations are correct
- [ ] Totals row is accurate
- [ ] Footer with last updated timestamp

## Common Pitfalls

1. **Miscounting tasks in summary** — Always double-check by summing phase totals
2. **Wrong percentage calculation** — Remember: Completed excludes Not Started
3. **Missing task links** — Every validated task should link to its implementation spec
4. **Stale validation dates** — Ensure dates are in chronological order
5. **Inconsistent status values** — Use exact emoji from legend

## Reference Documents

- [Planning/PLANNING.md](../Planning/PLANNING.md) Section 3.13 — Validation specification
- [PPPoE Validation Report](https://github.com/cloudbsdorg/freebsd-src-pppoe/tree/main/.plan) — Example implementation
- [Emulation Validation Report](https://github.com/cloudbsdorg/freebsd-src-build-emulation/tree/main/.plan) — Comprehensive example