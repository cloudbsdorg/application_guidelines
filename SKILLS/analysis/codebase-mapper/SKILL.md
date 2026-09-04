---
name: codebase-mapper
description: >-
  Recursively map a whole codebase into exhaustive tree-view documents under
  .discovery/. Use when starting on an unfamiliar or large project, when asked
  to map structure and dependencies, or when a port or migration needs a
  complete inventory before planning.
---

# Codebase Mapper (Modular)

> **Version:** 2.0 (Modular — split by phase)
> **Purpose:** Recursively map any codebase into exhaustive tree-view markdown documents.
> **Output:** `.discovery/` directory with TOC and per-component files.

This skill now uses **modular sub-skills** — load only the phase you need.

---

## Quick-Load Index

| Phase | Sub-Skill Path | Trigger When... |
|-------|----------------|--------------|
| **Phase 0-1** | `codebase-mapper/phases-0-1.md` | Starting mapping, need entry point + orphan discovery |
| **Phase 2-3** | `codebase-mapper/phases-2-3.md` | Mapping components, decomposition, cross-refs |
| **Phase 4-5** | `codebase-mapper/phases-4-5.md` | Verification + TOC generation |
| **Advanced** | `codebase-mapper/advanced.md` | Monorepos, optimization, visualization, security |

---

## Loading Instructions

Load this skill when the user asks you to:
- Map the codebase
- Create a codebase discovery document
- Generate a tree view of the project structure
- Document what every file and component does
- Create a `.discovery/` directory structure
- Build a codebase map with TOC
- Recursively explore and document the project

---

## Loading Pattern (Load Only What You Need)

```bash
# For a NEW mapping project:
# Load Phase 0-1 first (entry point + orphan discovery)
===SKILL:codebase-mapper/phases-0-1===
  [reads codebase-mapper/phases-0-1.md]
===END SKILL===

# Then load Phase 2-3 (mapping + cross-refs)
===SKILL:codebase-mapper/phases-2-3===
  [reads codebase-mapper/phases-2-3.md]
===END SKILL===

# Finally load Phase 4-5 (verification + TOC)
===SKILL:codebase-mapper/phases-4-5===
  [reads codebase-mapper/phases-4-5.md]
===END SKILL===
```

```bash
# For INCREMENTAL updates (already have .discovery/):
# Load only Phase 4-5 (verification + TOC update)
===SKILL:codebase-mapper/phases-4-5===
  [reads codebase-mapper/phases-4-5.md]
===END SKILL===
```

```bash
# For advanced analysis (monorepo, large codebase, security audit):
===SKILL:codebase-mapper/advanced===
  [reads codebase-mapper/advanced.md]
===END SKILL===
```

---

## Core Principles

- **Standards as Law**: This skill's methodology is mandatory, not optional. Every step must be followed.
- **UTF-8 Everywhere**: All generated markdown documents use UTF-8 encoding.
- **One File Per Component**: No single discovery file exceeds ~200 lines of tree content. If a component is large, split it into sub-files.
- **Recursion Has No Depth Limit**: Map as deep as needed. A single line of code can generate 10 tree levels.
- **No Duplication**: Each discovered item maps to exactly one file. Cross-reference via links, never duplicate content.
- **Evidence-Based Descriptions**: Every node description must be backed by what the code actually does, not what you think it should do.
- **Follow Existing Patterns**: When describing components, reference actual patterns found in the codebase.
- **Do NOT Modify Source**: This skill only reads and generates discovery documents. Never change the codebase.
- **Do NOT Skip "Obvious" Items**: Even simple files get mapped. Assumptions about simplicity cause incomplete maps.

---

## Source of Truth

The `.discovery/` directory is the single source of truth for codebase understanding. When mapping:

1. Always read the actual file contents before generating tree nodes.
2. Never assume what code does — verify by reading it.
3. If a file imports/requires other files, map those dependencies explicitly.
4. When encountering unfamiliar patterns, read surrounding context before classifying.
5. Prefer answers and descriptions backed by specific source content.

---

## Phase Quick-Reference

### Phase 0: Entry Point Identification
- Read `package.json`, `Cargo.toml`, `go.mod`, `pyproject.toml`, `Makefile`
- Identify main executable, server entry, CLI entry, or library entry
- Create root discovery document at `.discovery/000-root.md`

### Phase 1: Directory Structure Scan + Orphan Discovery
- Generate high-level project tree
- **Run orphan-discovery.sh** (generates Master File Tracking Table)
- **CRITICAL**: Every file MUST appear in the table
- Purpose determined for EVERY file (even PNGs know "where used and why")

### Phase 2: Recursive Component Mapping
- Generate tree-view documents for each component
- **Decompose source files**: imports, functions, classes, types, globals
- Use `decompose_source()` function from `phases-2-3.md`
- Map to `.discovery/<NNN>-<name>.md`

### Phase 3: Cross-Reference Generation
- Track every import/require across all files
- Build dependency graph (Mermaid format)
- Identify circular dependencies
- Identify orphans and entry points

### Phase 4: Coverage Verification (MANDATORY)
- **100% coverage required** — re-run orphan check
- All quality gates must pass (see `phases-4-5.md`)
- Fix any failures before proceeding

### Phase 5: TOC Generation
- Create `.discovery/TOC.md` with Master File Tracking Table
- Include project structure tree with links
- Generate dependency graph and entry points list
- Statistics: total files, directories, coverage %

---

## Integration With Other Skills

| Skill | When to Use |
|-------|--------------|
| `migration/codebase-migrator.md` | Before migrating — map source codebase first |
| `analysis/reverse-engineer-for-port.md` | Combine with Phase 2-3 for deep analysis |
| `analysis/code-quality-analyzer.md` | After mapping — find duplication patterns |
| `analysis/ui-analysis/ui-ux-analyzer.md` | Focus on UI components from the map |
| `analysis/api-analysis/api-analyzer.md` | Focus on API routes from the map |
| `planning/feature-task-generator.md` | After mapping — generate tasks from feature inventory |

---

## Checklist

- [ ] Phase 0: Entry point identified, `000-root.md` created
- [ ] Phase 1: Project tree generated, orphan discovery run
- [ ] Master File Tracking Table: 100% coverage (all files accounted for)
- [ ] Phase 2: All components mapped with decomposition
- [ ] Phase 3: Cross-references generated, dependency graph created
- [ ] Phase 4: Coverage verification passed (all quality gates)
- [ ] Phase 5: TOC generated with statistics
- [ ] Advanced (optional): Monorepo handling, optimization, visualization
