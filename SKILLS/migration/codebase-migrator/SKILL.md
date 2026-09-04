---
name: codebase-migrator
description: >-
  Migrate a legacy application to a modern platform and language - DOS,
  Pascal, old Unix, retro codebases moving to FreeBSD, Rust, Go, or
  TypeScript. Use when asked to port, convert, or modernise an old codebase,
  after the analysis skills have produced an inventory.
---

# Skill: codebase-migrator

**Purpose:** Systematically migrate legacy applications (DOS, old Unix, retro platforms) to modern targets (FreeBSD, Rust, TypeScript) using codebase-mapper for analysis and structured conversion workflows.

**Triggers:** When migrating legacy code, porting DOS applications to FreeBSD, converting Pascal/C to Rust, modernizing 90s applications, or converting from any `source_lang`/`source_platform` to `target_lang`/`target_platform`.

---

## Loading Instructions

Load this skill when the user asks you to:
- Migrate a legacy application to a modern platform
- Convert an old codebase from one language to another
- Port a DOS/Windows 3.x/Win9x application to FreeBSD/Linux
- Modernize a 90s/00s application using Rust, Go, TypeScript
- Analyze and rewrite a forgotten/abandoned codebase

---

## Core Principle

> **Preserve first, then map, then convert. Never lose the original.**

The original codebase is the source of truth. Map it exhaustively with `codebase-mapper`, then use the map to drive conversion.

---

## Migration Workflow

### Phase 0: Initialize Migration

```bash
# User provides:
#   - SOURCE_REPO: URL or path to legacy code
#   - SOURCE_LANG: Pascal, C, C++, BASIC, Assembly, etc.
#   - SOURCE_PLATFORM: DOS, Windows 3.1, Win95, OS/2, Amiga, etc.
#   - TARGET_LANG: Rust, Go, TypeScript, etc.
#   - TARGET_PLATFORM: FreeBSD, Linux, etc.

# 0.1 Create migration directory structure
mkdir -p migration-{project}/
cd migration-{project}/
mkdir -p original/     # Preserved source (read-only)
mkdir -p .discovery/   # Codebase mapper output
mkdir -p port/          # New target code
mkdir -p .plan/         # Planning documents
```

### Phase 1: Preserve Original

```bash
# 1.1 Clone or copy original source
git clone {SOURCE_REPO} original/  # If git repo
# OR
cp -r {SOURCE_PATH}/* original/  # If local files

# 1.2 Create preservation commit (never modify original/)
cd original/
git init
git add -A
git commit -m "PRESERVATION: Original {SOURCE_LANG} code for {SOURCE_PLATFORM}"
cd ..

# 1.3 Document source environment
cat > SOURCE_ENV.md << 'EOF'
# Source Environment

- **Language:** {SOURCE_LANG}
- **Platform:** {SOURCE_PLATFORM}
- **Compiler/Interpreter:** {compiler name and version if known}
- **Year:** {approximate year}
- **Dependencies:** {known dependencies or "unknown"}
- **Build System:** {Makefile, Turbo Pascal, etc.}
EOF
```

### Phase 2: Map Original with Codebase-Mapper

```bash
# 2.1 Load codebase-mapper skill
# (Read SKILLS/analysis/codebase-mapper.md)

# 2.2 Run orphan discovery first
cd original/
bash << 'DISCOVERY_SCRIPT'
#!/bin/bash
EXCLUDES="! -path ./discovery/* ! -path ./node_modules/* ! -path ./git/* ! -path ./dist/*"

echo "=== Orphan Discovery ==="
eval "find . -type f $EXCLUDES" | sort > /tmp/all_files.txt
grep -h "**Path:**" .discovery/*.md 2>/dev/null | sed 's/.*`//; s/`.*//' | sort -u > /tmp/mapped_files.txt
comm -23 /tmp/all_files.txt /tmp/mapped_files.txt > /tmp/orphan_files.txt

echo "Total: $(wc -l < /tmp/all_files.txt)"
echo "Mapped: $(wc -l < /tmp/mapped_files.txt)"
echo "Orphans: $(wc -l < /tmp/orphan_files.txt)"
DISCOVERY_SCRIPT

# 2.3 Generate Master File Tracking Table
# (See codebase-mapper Phase 1.5 for full script)
# This creates .discovery/TOC.md with:
#   - File | Mapped | Timestamp | Where Used | Purpose
#   - EVERY file accounted for

# 2.4 Map each source file (Phase 2 of codebase-mapper)
# For each file in original/, generate .discovery/XXX-file.md with:
#   - Decomposition (imports, functions, globals, types)
#   - Tree-view structure
#   - Data flow analysis
#   - Side effects documented

# 2.5 Generate cross-references (Phase 3)
#   - Dependency graph
#   - Circular dependencies
#   - Entry points identified
#   - Orphan files documented

# 2.6 Verification (Phase 4)
#   - 100% coverage confirmed
#   - All files mapped or purpose-justified
```

### Phase 3: Create Migration Plan

```bash
# 3.1 Load planning skills
# (Read SKILLS/planning/plan-document-generator.md)
# (Read SKILLS/planning/toc-generator.md)

# 3.2 Create plan documents
cd ..
cat > .plan/000-migration-TOC.md << 'EOF'
# Migration Table of Contents

| File | Title | Status | Description |
|------|-------|--------|-------------|
| `000-migration-TOC.md` | TOC | ACTIVE | This document |
| `001-migration-Workflow.md` | Workflow | ACTIVE | Task claiming |
| `100-Source-Analysis.md` | Analysis | DRAFT | Original codebase analysis |
| `200-Target-Architecture.md` | Architecture | DRAFT | Target system design |
| `300-Conversion-Tasks.md` | Tasks | DRAFT | Conversion task list |
| `400-Testing.md` | Testing | DRAFT | Test strategy |
| `700-Risks.md` | Risks | DRAFT | Migration risks |
EOF

# 3.3 Analyze source with analysis skills
# Load relevant analyzers based on SOURCE_LANG:
#   - C/C++ → SKILLS/analysis/os-analysis/system-call-analyzer.md
#   - Pascal → Read .discovery/ docs, manual analysis
#   - Basic → Manual analysis
#   - UI apps → SKILLS/analysis/ui-analysis/ui-ux-analyzer.md

# 3.4 Generate conversion tasks
# (Read SKILLS/planning/feature-task-generator.md)
# Tasks grouped by workflow, not file:
#   - Task 1: Port core logic (functions X, Y, Z)
#   - Task 2: Convert data structures (structs, types)
#   - Task 3: Port UI to target (TUI/WebUI)
#   - Task 4: Implement platform-specific features
```

### Phase 4: Convert to Target

```bash
# 4.1 Use .discovery/ docs as reference
# Every conversion decision references original/ and .discovery/

# 4.2 Create target project structure in port/
cd port/
# Initialize new project (cargo init, npm init, etc.)

# 4.3 Convert file-by-file using the map
# For each .discovery/XXX-file.md:
#   1. Read original source file from original/
#   2. Read decomposition in .discovery/XXX-file.md
#   3. Convert to TARGET_LANG
#   4. Document conversion decisions
#   5. Write to port/ with matching structure

# 4.4 Document conversions
cat >> CONVERSION_LOG.md << 'EOF'
## Converted: original/src/main.pas → port/src/main.rs

**Original:** Pascal, 245 lines
**Target:** Rust, ~300 lines
**Decisions:**
- Replaced `writeln()` with `println!()`
- Converted `record` to `struct`
- Replaced `procedure` with `fn`
- Added error handling (Result<T, E>)
EOF
```

### Phase 5: Validate & Test

```bash
# 5.1 Run original if possible (DOSBox, emulator)
# Compare behavior with port/

# 5.2 Test target on TARGET_PLATFORM
cd port/
# Run test suite
# Verify feature parity

# 5.3 Document differences
cat > MIGRATION_REPORT.md << 'EOF'
# Migration Report

## Summary
- **Source:** {SOURCE_LANG} on {SOURCE_PLATFORM}
- **Target:** {TARGET_LANG} on {TARGET_PLATFORM}
- **Files Convert:** X/Y (remaining: ...)
- **Feature Parity:** Z%

## Challenges
1. {challenge description}

## Differences
| Feature | Original | Port |
|---------|-----------|------|
| {feature} | {behavior} | {behavior} |
EOF
```

---

## Example: Pascal/DOS → Rust/FreeBSD

```bash
# User: "Migrate this Turbo Pascal DOS application to Rust on FreeBSD"

# Phase 0: Initialize
mkdir -p turbo-app-migration/ && cd turbo-app-migration/
mkdir -p original/ .discovery/ port/ .plan/

# Phase 1: Preserve
git clone https://github.com/user/turbo-app.git original/
cd original/ && git commit -m "PRESERVATION: Turbo Pascal DOS app" && cd ..

# Phase 2: Map
cd original/
# Load SKILLS/analysis/codebase-mapper.md
# Run mapping → generates .discovery/*.md files
# Now we have:
#   .discovery/TOC.md (Master File Tracking Table)
#   .discovery/001-main-pas.md (decomposed: functions, vars, types)
#   .discovery/002-utils-pas.md
#   etc.

# Phase 3: Plan
cd ..
# Load SKILLS/planning/*.md
# Create .plan/ documents
# Generate conversion tasks:
#   - Task 1: Port main.pas logic → main.rs
#   - Task 2: Convert data structures (record → struct)
#   - Task 3: Replace DOS interrupts with FreeBSD syscalls

# Phase 4: Convert
cd port/
cargo init --name turbo-app
# Read .discovery/001-main-pas.md
# Convert Pascal → Rust:
#   - program → fn main()
#   - uses → use
#   - record → struct
#   - procedure → fn
#   - writeln → println!
#   - DOS interrupts → nix crate or libc

# Phase 5: Validate
cargo test
# Compare behavior with original (run in DOSBox if needed)
```

---

## Skill Dependencies

This skill orchestrates multiple sub-skills:

| Phase | Skill Required | Path |
|-------|-----------------|------|
| Mapping | codebase-mapper | `analysis/codebase-mapper.md` |
| Planning | plan-document-generator | `planning/plan-document-generator.md` |
| Planning | toc-generator | `planning/toc-generator.md` |
| Analysis | language-specific analyzers | `analysis/os-analysis/` or manual |
| UI | ui-ux-analyzer | `analysis/ui-analysis/ui-ux-analyzer.md` |
| Tasks | feature-task-generator | `planning/feature-task-generator.md` |
| Risks | risk-assessor | `security/risk-assessor.md` |
| Validation | test-planner | `testing/test-planner.md` |

---

## Quick-Scan Triggers

| Trigger | Action |
|---------|--------|
| `migrate`, `port`, `convert` | Load this skill |
| `legacy`, `DOS`, `retro`, `Pascal`, `Turbo` | Load this skill |
| `modernize`, `old code`, `forgotten app` | Load this skill |

---

## Checklist

- [ ] Migration directory structure created
- [ ] Original code preserved in `original/` (read-only)
- [ ] Master File Tracking Table generated (all files accounted for)
- [ ] Codebase fully mapped with `.discovery/` docs
- [ ] Source environment documented (`SOURCE_ENV.md`)
- [ ] Migration plan created (`.plan/` documents)
- [ ] Conversion tasks generated
- [ ] Target project initialized in `port/`
- [ ] Files converted referencing `.discovery/` docs
- [ ] Conversion log maintained
- [ ] Migration report generated
- [ ] Feature parity validated
