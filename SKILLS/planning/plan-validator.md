---
name: plan validator
description: Validate that plan documents follow the CloudBSD Planning Guidelines standard.
---

# Skill: plan-validator

**Purpose:** Validate that plan documents follow the CloudBSD Planning Guidelines standard.

**Triggers:** On PR review, before committing changes to `.plan/` directory, or when validating project structure.

## Loading Instructions

Load this skill when the user asks you to:
- Validate plan documents
- Check document compliance
- Review a project's `.plan/` structure
- Pre-validate before committing

## Validation Categories

### 1. Document Naming Convention

Check that files match: `<Number>-<Project>-<Topic>.md`

```markdown
## Validation: Document Naming

| File | Expected Pattern | Status |
|------|-----------------|--------|
| `000-MyProject-TOC.md` | `000-MyProject-TOC.md` | ✅ VALID |
| `001-MyProject-Workflow.md` | `001-MyProject-Workflow.md` | ✅ VALID |
| `100-MyProject-Overview.md` | `100-MyProject-Overview.md` | ✅ VALID |
| `TOC.md` | `000-Project-TOC.md` | ❌ INVALID: Missing prefix |
| `Overview.md` | `100-Project-Overview.md` | ❌ INVALID: Missing prefix |
```

### 2. Required Sections Per Document Type

#### TOC Document (000)
- [ ] Document header block
- [ ] Document map table
- [ ] Dependency graph
- [ ] Recommended reading order
- [ ] Cross-reference index
- [ ] Change log footer

#### Workflow Document (001)
- [ ] Document header block
- [ ] Task claiming protocol
- [ ] Task completion protocol
- [ ] Merge conflict resolution
- [ ] Change log footer

#### Overview Document (100)
- [ ] Document header block
- [ ] Executive summary
- [ ] Problem statement
- [ ] High-level architecture diagram
- [ ] Implementation phases
- [ ] Success criteria
- [ ] Change log footer

#### Risks Document (700)
- [ ] Document header block
- [ ] Risk register table
- [ ] Risk categories
- [ ] High-priority risks section
- [ ] Change log footer

#### Sysctl Document (501)
- [ ] Document header block
- [ ] Sysctl table with Node, Type, Default, Range, Description
- [ ] State enumeration tables (if applicable)
- [ ] Change log footer

### 3. Task Table Format

```markdown
| ID | Task | Priority | Status | Assigned To | Owner | Phase | Start | End | Dependencies | Files | Spec | Notes |
|----|------|----------|--------|-------------|-------|-------|-------|-----|--------------|-------|------|-------|
```

**Required Columns:**
- ID
- Task
- Priority
- Status
- Dependencies
- Files
- **Spec** (link to detailed specification)

**Status Values (must be one of):**
- ⬜ PENDING
- 🔄 IN PROGRESS
- 🟡 BLOCKED
- ⏸️ PAUSED
- ✅ DONE
- ❌ FAILED

**Spec Column Validation:**
- Must contain a link reference (`[Spec](#<id>)` or `[Spec](file.md#<id>)`)
- Anchor must match the task ID (with dots removed)
- Example: Task `300.1` → Spec `[Spec](#3001)`

### 4. Document Header Block

Every document must have:

```markdown
**Document ID:** <Unique-ID>
**Version:** <Version>
**Last Updated:** <YYYY-MM-DD>
**Maintainer:** <Team or Contact>
**Status:** DRAFT | ACTIVE | STALE | DEPRECATED
**Classification:** INTERNAL | CONFIDENTIAL | PUBLIC
```

### 5. Document Footer Block

Every document must end with:

```markdown
---

## Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | YYYY-MM-DD | Name | Initial version |

**Last Updated:** YYYY-MM-DD HH:MM UTC
**Classification:** INTERNAL
```

## Validation Report Template

```markdown
# Plan Document Validation Report

**Project:** <Project Name>
**Validated:** YYYY-MM-DD HH:MM UTC
**Validator:** <Agent/Person>

---

## Summary

| Category | Passed | Failed | Warnings |
|----------|--------|--------|----------|
| Naming Convention | 12 | 0 | 0 |
| Required Sections | 10 | 1 | 2 |
| Task Tables | 5 | 0 | 0 |
| Header/ Footer | 8 | 0 | 0 |

**Overall Result:** ✅ PASS | ⚠️ WARNINGS | ❌ FAIL

---

## Issues Found

### ❌ Failed Checks

1. **File:** `300-Tasks.md`
   - **Issue:** Missing Phase column in task table
   - **Fix:** Add Phase column with values (Phase 1, Phase 2, etc.)

### ⚠️ Warnings

1. **File:** `100-Overview.md`
   - **Warning:** No ASCII diagram in architecture section
   - **Suggestion:** Add architecture diagram using box-drawing characters

---

## Recommendations

1. Add `0002-<Project>-Build-Status.md` to `.plan/` directory
2. Create `AGENTS_START_HERE.md` at project root
3. Update 0000-<Project>-TOC.md with link to 0002-<Project>-Build-Status.md

---

## Validation Checklist

- [x] All documents follow naming convention
- [x] All required sections present
- [x] Task tables formatted correctly
- [x] Header/footer blocks present
- [x] Cross-references valid
- [x] Change logs updated
```

## Cross-Document Reference Validation

Check that references between documents are valid:

```markdown
| Referenced Document | Referenced By | Status |
|---------------------|---------------|--------|
| `100-Overview.md` | `000-TOC.md` | ✅ VALID |
| `200-Architecture.md` | `100-Overview.md` | ✅ VALID |
| `300-Tasks.md` | `100-Overview.md` | ✅ VALID |
| `999-Missing.md` | `000-TOC.md` | ❌ INVALID: File does not exist |
```

## Validation Script Template

```bash
#!/bin/sh
# validate_plan.sh - Validate .plan/ directory structure

set -e

PROJECT_ROOT="$(git rev-parse --show-toplevel)"
PLAN_DIR="$PROJECT_ROOT/.plan"

echo "Validating .plan/ directory..."

# Check required files exist
required_files="
    000-*-TOC.md
    001-*-Workflow.md
    100-*-Overview.md
"

# Check naming convention
for f in "$PLAN_DIR"/*.md; do
    basename "$f" | grep -qE '^[0-9]{3,4}-.*\.md$' || {
        echo "INVALID: $f"
        exit 1
    }
done

echo "Validation passed"
```

## Validation Rules Summary

| Rule ID | Rule | Severity |
|---------|------|----------|
| V001 | Document naming must match `<Number>-<Project>-<Topic>.md` | ERROR |
| V002 | Required sections must be present per document type | ERROR |
| V003 | Task tables must have all required columns | ERROR |
| V004 | Status values must be valid emoji | ERROR |
| V005 | Header block must have all required fields | ERROR |
| V006 | Footer block must have change log | ERROR |
| V007 | Cross-references must point to existing files | ERROR |
| V008 | Change logs must be updated | WARNING |
| V009 | ASCII diagrams should be present in architecture docs | WARNING |
| V010 | 0002-<Project>-Build-Status.md should exist | WARNING |

## Reference

See [Planning/PLANNING.md](../Planning/PLANNING.md) for the complete planning standard against which to validate.