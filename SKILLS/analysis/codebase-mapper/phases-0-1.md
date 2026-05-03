---
name: codebase-mapper-phases-0-1
description: Phase 0 (Entry Point) and Phase 1 (Directory Scan + Orphan Discovery) of codebase-mapper.
---

# Codebase Mapper — Phases 0-1

## Phase0: Entry Point Identification

Identify the starting point of the application:

1. Read `package.json`, `Cargo.toml`, `go.mod`, `pyproject.toml`, `Makefile`, or equivalent to find entry points.
2. Identify the main executable, server entry, CLI entry, or library entry.
3. Read the entry point file completely before proceeding.
4. Create the root discovery document at `.discovery/000-root.md`.

## Phase1: Directory Structure Scan

Generate a high-level tree of the entire project structure:

```
project-root/
├── .discovery/          # Discovery documents (output)
├── src/
│   ├── main.ts          # Entry point → maps to 100-main.md
│   ├── config/          # Configuration module → maps to 200-config/
│   └── server/          # Server module → maps to 300-server/
├── test/
│   └── ...
├── package.json
└── ...
```

### Phase1.5: Orphan Discovery (CRITICAL)

**Orphan Discovery Script (all-in-one):**

```bash
#!/bin/bash
# orphan-discovery.sh - Find and categorize all unmapped files
# Generates Master File Tracking Table with: File | Mapped | UTC Timestamp | Where Used | Purpose

EXCLUDES="! -path ./discovery/* ! -path ./node_modules/* ! -path ./git/* ! -path ./dist/* ! -path ./build/*"

echo "=== Orphan Discovery ==="

# Step 1: Find ALL project files (the 'find *' at codebase root)
eval "find . -type f $EXCLUDES" | sort > /tmp/all_files.txt

# Step 2: Find already-mapped files from .discovery/ documents
grep -h "**Path:**" .discovery/*.md 2>/dev/null | sed 's/.*`//; s/`.*//' | sort -u > /tmp/mapped_files.txt

# Step 3: Find orphans (in project but not in discovery docs)
comm -23 /tmp/all_files.txt /tmp/mapped_files.txt > /tmp/orphan_files.txt

echo "Total project files: $(wc -l < /tmp/all_files.txt)"
echo "Mapped files: $(wc -l < /tmp/mapped_files.txt)"
echo "Orphan files: $(wc -l < /tmp/orphan_files.txt)"

# Step 4: Generate Master File Tracking Table (.discovery/TOC.md section)
TOC_FILE=".discovery/TOC.md"
[[ -f "$TOC_FILE" ]] || echo "# Codebase Discovery — Table of Contents

## 📋 Master File Tracking Table

> **CRITICAL:** EVERY file in the project MUST appear in this table.
> NO file is "not interesting" — every file has a purpose.
> Source file decomposition (imports, functions, classes, types) happens in Phase 2 individual reports.

| File | Mapped (true/false) | Timestamp (UTC) | Where Used | Purpose |
|------|----------------------|-------------------|-------------|---------|" > /tmp/master_table.txt

# Process ALL files (not just orphans — we want EVERY file)
while read f; do
  # Check if mapped
  MAPPED=$(grep -q "$f" /tmp/mapped_files.txt && echo "✅ true" || echo "❌ false")
  
  # Get timestamp (use file mtime as approximation, or TOC generation time)
  TIMESTAMP=$(date -u -r "$f" "+%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || echo "-")
  
  # Find where this file is used (grep for filename in source dirs)
  BASENAME=$(basename "$f")
  WHERE_USED=$(grep -rl "$BASENAME" src/ 2>/dev/null | head -3 | xargs -I {} echo "\`{}\`" | tr '\n' ',' | sed 's/,$//')
  [[ -z "$WHERE_USED" ]] && WHERE_USED="(not referenced)"
  
  # Determine purpose based on file type and location
  PURPOSE=""
  case "$f" in
    *config*/*.json|*package.json|*Makefile|*Dockerfile)
      PURPOSE="Configuration file - $(file -b "$f" 2>/dev/null || echo "config")" ;;
    *test*/*|*__tests__*/*|*.test.*|*.spec.*)
      PURPOSE="Test file - $(wc -l < "$f" 2>/dev/null || echo "0") lines" ;;
    *src/*|*lib/*|*app/*)
      PURPOSE="Source code ($(wc -l < "$f" 2>/dev/null || echo 0) lines) — decomposed in Phase 2" ;;
    *.md|*docs/*)
      PURPOSE="Documentation - $(head -3 "$f" 2>/dev/null | grep -o '^#.*' | head -1 || echo "doc")" ;;
    *.png|*.jpg|*.gif|*.svg)
      PURPOSE="Image asset - $(file -b "$f" 2>/dev/null), used in UI" ;;
    *.pdf)
      PURPOSE="PDF document - $(file -b "$f" 2>/dev/null)" ;;
    *.po|*.mo|*locales/*|*i18n/*)
      PURPOSE="Localization file - $(basename "$f")" ;;
    *.min.js|*.bundle.js|*dist/*)
      PURPOSE="[GENERATED] Compiled/bundled output - do NOT decompose" ;;
    *.github/*|*Jenkinsfile|*docker-compose.yml)
      PURPOSE="CI/CD configuration - $(basename "$f")" ;;
    *)
      PURPOSE="$(file -b "$f" 2>/dev/null || echo "Unknown")" ;;
  esac
  
  echo "| \`$f\` | $MAPPED | $TIMESTAMP | $WHERE_USED | $PURPOSE |" >> /tmp/master_table.txt
done < /tmp/all_files.txt

# Append the master table to TOC
cat /tmp/master_table.txt >> "$TOC_FILE"

echo "=== Master File Tracking Table generated in $TOC_FILE ==="
```

**Run this script FIRST** before any mapping. It ensures:
1. EVERY file is captured (from `find *` at codebase root)
2. Mapped status is tracked (true/false)
3. UTC timestamp recorded
4. Where Used shows which source files reference it
5. Purpose is determined for every file (even PNGs know "where used and why")
6. Source files show "decomposed in Phase 2" — actual decomposition happens in the individual `.discovery/XXX-file.md` report

**Phase 2 individual reports** contain the full decomposition:
- **Imports/Includes** — what this file depends on
- **Functions/Methods** — what this file defines  
- **Classes/Structs/Types** — the data structures
- **Global Variables** — stateful elements
- **Interfaces/Traits** — contracts and abstractions

Then systematically map each orphan file, updating the Mapped column to ✅ true as you go.
