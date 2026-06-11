---
name: codebase-mapper-advanced
description: Advanced phases (2.5-9+) of codebase-mapper — enhanced analysis, integrations, optimization, and visualization.
---

# Codebase Mapper — Advanced Phases

## Phase2.5: Enhanced Dependency Analysis

Beyond basic imports, analyze deeper dependency patterns:

### Dynamic Imports Detection

```bash
# Find dynamic imports (lazy loading, require() calls)
grep -rn "import(" . --include="*.js" --include="*.ts" 2>/dev/null
grep -rn "require(" . --include="*.js" --include="*.ts" 2>/dev/null | grep -v "const\|let\|var"
```

### Dependency Depth Analysis

```markdown
## Dependency Depth

| File | Direct Deps | Max Depth | Critical Path |
|------|------------|-----------|---------------|
| `src/main.ts` | 5 | 3 | main → config → validator → utils |
| `src/server.ts` | 8 | 4 | server → db → pool → config |
```

### Circular Dependency Detection

```bash
# Find circular dependencies
# For Node.js: npm install -g madge && madge --circular .
# For Python: pip install pydeps && pydeps --show-cycles <module>
# For Go: go install github.com/kisielk/modgraph@latest && modgraph | grep -E "(-->.*-->|\.\*-->)"
```

## Phase3.5: Integration With Other Skills

The codebase map feeds into other analysis skills:

### Integration Points:

| Skill | What It Consumes from .discovery/ | What It Produces |
|-------|---------------------------|-------------------|
| `analysis/reverse-engineer-for-port.md` | Source structure, entry points, data flow | Feature inventory |
| `analysis/code-quality-analyzer.md` | Function list, duplication patterns | Refactoring backlog |
| `analysis/ui-analysis/ui-ux-analyzer.md` | UI component trees, state | UI spec |
| `analysis/api-analysis/api-analyzer.md` | Route definitions, handlers | API spec |
| `planning/feature-task-generator.md` | Features, workflows | Task list |
| `migration/codebase-migrator.md` | Full map, all files | Conversion plan |

### Reading the Map:

```markdown
## For Reverse-Engineer

Read these .discovery/ files first:
1. `000-root.md` — Entry points, project structure
2. `0.1-*-Overview.md` — High-level architecture
3. Files with [export] tags — What the system exposes
4. Files with [import] tags — What the system depends on

## For UI-UX Analyzer

Focus on:
1. `**Pattern:** REACT_COMPONENT` files
2. `**Pattern:** VUE_COMPONENT` files
3. Files under `src/components/`, `src/views/`
4. State management: `src/store/`, `src/state/`
```

## Phase4.5: Performance Optimization (Large Codebases)

For codebases with 1000+ files:

### Incremental Mapping

```bash
# Only re-map files modified since last run
LAST_RUN=$(stat -f "%m" .discovery/TOC.md 2>/dev/null || echo 0)
find . -type f -newermt "@$LAST_RUN" ! -path "./.discovery/*" | sort > /tmp/changed_files.txt

echo "Files changed since last mapping: $(wc -l < /tmp/changed_files.txt)"
# Re-map only changed files
```

### Parallel Processing

```bash
# Split file list and process in parallel
split -l 50 /tmp/all_files.txt /tmp/batch_
for batch in /tmp/batch_*; do
  # Process batch in background
  (while read f; do map_file "$f"; done < "$batch") &
done
wait
```

### Smart Caching

```bash
# Cache file hashes to skip unchanged files
md5sum "$f" > "/tmp/cache/$(echo "$f" | md5).md5"
# On next run, compare hashes before re-mapping
```

## Phase5.5: Language-Agnostic Parsing

For languages without tree-sitter support:

### Fallback Parsing Strategies

| Language | Strategy | Tools |
|-----------|-----------|-------|
| Pascal, Delphi | Regex patterns for `procedure`, `function`, `unit` | `grep -E` |
| Assembly (x86, ARM) | Symbol tables, entry points | `nm`, `objdump` |
| COBOL | Division/Section structure | `grep -E "DIVISION|SECTION"` |
| Fortran | PROGRAM, SUBROUTINE, FUNCTION | `grep -E` |
| Shell scripts | Function defs, source includes | `grep -E "^function|source "` |

### Example: Pascal Parser

```bash
# Extract Pascal procedures/functions
grep -E "^(procedure|function) [a-zA-Z0-9_]+" "$file" | \
  sed 's/procedure //; s/function //; s/(.*//' | tr '\n' ', '

# Extract uses/imports
grep -E "^uses " "$file" | sed 's/uses //; s/;//' | tr ';' '\n' | grep -v "^$"
```

## Phase6: Tree-Sitter Integration (Optional)

For languages with tree-sitter support, use structured parsing:

```bash
# Install tree-sitter
npm install -g tree-sitter-cli

# Parse with tree-sitter (if available)
if command -v tree-sitter &> /dev/null; then
  tree-sitter parse "$file" --quiet 2>/dev/null | \
    python3 -c "
import sys, json
# Convert tree-sitter output to structured JSON
# Then convert JSON to markdown tree
"
fi
```

**Supported Languages:** JavaScript, TypeScript, Python, Go, Rust, C, C++, Java, Ruby, PHP, and 50+ more.

## Phase6.5: Output Formats Beyond Markdown

The `.discovery/` directory can also generate:

### Mermaid Diagrams

```bash
# Generate Mermaid dependency graph from .discovery/TOC.md
echo "```mermaid"
echo "graph TD"
grep "| ✅ true |" .discovery/TOC.md | while read line; do
  file=$(echo "$line" | cut -d'|' -f2 | tr -d '`')
  # Extract imports from corresponding .discovery/ file
  discovery_file=$(grep -l "$file" .discovery/*.md)
  grep "\[import\]" "$discovery_file" 2>/dev/null | sed 's/.*→ //; s/\.md//' | \
    while read dep; do
      echo "  $(echo "$file" | sed 's/[^a-zA-Z0-9]//g') --> $(echo "$dep" | sed 's/[^a-zA-Z0-9]//g')"
    done
done
echo "```"
```

### JSON Export

```bash
# Export Master File Tracking Table as JSON
echo "{"files": [" > .discovery/toc.json
grep "| ✅ true |" .discovery/TOC.md | while read line; do
  file=$(echo "$line" | cut -d'|' -f2 | tr -d '` ')
  mapped=$(echo "$line" | grep -o "✅ true\|❌ false")
  purpose=$(echo "$line" | cut -d'|' -f5 | sed 's/^ *//; s/ *$//')
  echo "  {\"path\": \"$file\", \"mapped\": \"$mapped\", \"purpose\": \"$purpose\"}," >> .discovery/toc.json
done
echo "]}" >> .discovery/toc.json
```

## Phase7: Incremental Updates (CI/CD Integration)

### GitHub Action for Automatic Updates

```yaml
# .github/workflows/codebase-mapping.yml
name: Update Codebase Map

on:
  push:
    branches: [main, develop]
  pull_request:

jobs:
  update-map:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run Codebase Mapper
        run: |
          bash .discovery/scripts/orphan-discovery.sh
          # Re-map changed files only
          git diff --name-only ${{ github.event.before }} ${{ github.sha }} | \
            while read f; do
              bash .discovery/scripts/map-file.sh "$f"
            done
      
      - name: Commit Updated Map
        uses: stefanzweifel/git-auto-commit-action@v4
        with:
          commit_message: "chore: update codebase map [skip ci]"
          file_pattern: '.discovery/*.md'
```

## Phase8: Visualization & Interactive Reports

### HTML Report Generation

```bash
# Generate interactive HTML report from .discovery/
python3 << 'EOF'
import markdown
import json

# Read TOC
with open('.discovery/TOC.md', 'r') as f:
    toc = f.read()

# Convert to HTML with interactive features
html = f"""
<html>
<head><title>Codebase Map</title>
<style>
  .file {{ cursor: pointer; }}
  .file:hover {{ background: #eee; }}
</style>
</head>
<body>
<h1>Codebase Discovery Report</h1>
{markdown.markdown(toc)}
</body>
</html>
"""

with open('.discovery/report.html', 'w') as f:
    f.write(html)
EOF
```

## Phase9: Security Analysis Deep Dive

### Security-Relevant Patterns to Flag

```markdown
## Security Observations

| File | Pattern Found | Severity | Recommendation |
|------|----------------|----------|-------------------|
| `src/auth.ts` | Hardcoded secret: `const API_KEY = "abc123"` | 🔴 CRITICAL | Move to env vars |
| `src/utils.ts` | `eval()` usage | 🔴 CRITICAL | Replace with safe alternative |
| `src/api.ts` | No input validation on `req.body` | 🟠 HIGH | Add validation schema |
| `src/config.ts` | File permissions: `chmod 0644` on secrets | 🟡 MEDIUM | Use 0600 for secrets |
| `src/server.ts` | Runs as root (no user switch) | 🟠 HIGH | Switch to dedicated user |
```

### Privilege Analysis Integration

After mapping, run `analysis/os-analysis/privilege-analyzer.md` to:
1. Identify setuid/setgid binaries
2. Map capability requirements
3. Document chroot/jail needs
4. Flag privilege escalation risks
