---
name: codebase-mapper-phases-4-5
description: Phase4 (Coverage Verification) and Phase5 (TOC Generation) of codebase-mapper.
---

# Codebase Mapper — Phases 4-5

## Phase4: Coverage Verification (MANDATORY)

**BEFORE generating the TOC, verify 100% coverage:**

```bash
# Step 1: Re-run orphan check
find . -type f ! -path "./.discovery/*" ! -path "./node_modules/*" ! -path "./.git/*" | sort > /tmp/verify_all.txt
grep -h "**Path:**" .discovery/*.md 2>/dev/null | sed 's/.*`//; s/`.*//' | sort -u > /tmp/verify_mapped.txt
comm -23 /tmp/verify_all.txt /tmp/verify_mapped.txt > /tmp/still_orphans.txt

if [ -s /tmp/still_orphans.txt ]; then
  echo "ERROR: Still have unmapped files!"
  cat /tmp/still_orphans.txt
  echo "Go back to Phase1.5 and map these files."
  exit 1
fi

echo "✅ 100% Coverage Verified"
```

**Coverage Quality Gates:**

| Gate | Check | Failure Action |
|------|-------|----------------|
| **Count Match** | `all_files - mapped_files = 0` | Map remaining orphans |
| **Import Links** | Every import has a linked .discovery/ file | Create missing discovery docs |
| **Export Docs** | Every export is documented with behavior | Add missing export descriptions |
| **Dir Children** | Directory trees show all children with descriptions | Add missing child entries |
| **TOC Links** | TOC links to every discovery document | Add missing TOC entries |
| **Dep Graph** | Dependency graph is accurate and complete | Fix missing edges |
| **Circular Depts** | All circular dependencies identified | Run cycle detection |
| **Entry Points** | All entry points identified and documented | Add missing entry points |
| **File Size** | No discovery file exceeds 200 lines without split | Split large files |
| **Evidence-Based** | All descriptions backed by actual code (not assumptions) | Re-read and fix descriptions |
| **Cross-Refs** | Cross-references between documents are correct | Fix broken links |
| **Statistics** | Statistics in TOC are accurate | Recalculate and update |
| **UTF-8** | All files use UTF-8 encoding | Re-save with UTF-8 |
| **No Dupes** | No duplicate content across files (use links) | Replace dupes with links |

## Phase5: TOC Generation

Create the master Table of Contents at `.discovery/TOC.md`:

```markdown
# Codebase Discovery — Table of Contents

**Project:** <project-name>
**Generated:** YYYY-MM-DD
**Root:** <entry-point-path>
**Total files mapped:** <count>
**Total directories mapped:** <count>
**Coverage:** 100% ✅ (verified)

---

## 📋 Master File Tracking Table

> **CRITICAL:** EVERY file in the project MUST appear in this table.
> NO file is "not interesting" — every file has a purpose.

| File | Mapped (true/false) | Timestamp (UTC) | Where Used | Purpose |
|------|----------------------|-------------------|-------------|---------|
| `src/main.ts` | ✅ true | 2026-05-03T14:23:45Z | `src/server.ts` (imports), `tests/` (tested) | Application entry point, Express server setup |
| `src/config.ts` | ✅ true | 2026-05-03T14:25:12Z | `src/main.ts`, `src/services/*` (imports) | Configuration loader, validates env vars |
| `public/logo.png` | ✅ true | 2026-05-03T14:30:00Z | `src/App.tsx:15` (import), `README.md` (display) | Main logo, 200x80, used in header |
| `docs/README.md` | ✅ true | 2026-05-03T14:31:00Z | External readers | Project documentation, setup instructions |
| `scripts/migrate.ts` | ✅ true | 2026-05-03T14:32:00Z | `package.json` (npm script) | Standalone migration script, run once on deploy |
| `node_modules/` | ❌ false | - | - | External dependencies (excluded from mapping) |
| ... | ... | ... | ... | ... |

**How to Read This Table:**
- **Mapped (true/false):** ✅ true = has `.discovery/<NNN>.md` file; ❌ false = NOT yet mapped (MUST be mapped!)
- **Timestamp (UTC):** When the file was last mapped (from `.discovery/TOC.md` update time)
- **Where Used:** Which source files import/reference this file (run `grep -r "filename" src/` to find)
- **Purpose:** Why this file exists — every file has a purpose, even `logo.png` (used in UI) or `migrate.ts` (run once on deploy)

---

## Project Structure

```
<Full project tree with links to discovery files>
```

### Generation Script (Phase1.5 + Phase5 combined):

```bash
# Generate Master File Tracking Table
echo "## 📋 Master File Tracking Table" >> .discovery/TOC.md
echo "" >> .discovery/TOC.md
echo "> **CRITICAL:** EVERY file in the project MUST appear in this table." >> .discovery/TOC.md
echo "> NO file is \"not interesting\" — every file has a purpose." >> .discovery/TOC.md
echo "" >> .discovery/TOC.md
echo "| File | Mapped (true/false) | Timestamp (UTC) | Where Used | Purpose |" >> .discovery/TOC.md
echo "|------|----------------------|-------------------|-------------|---------|" >> .discovery/TOC.md

TOC_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

for f in $(eval "find . -type f $EXCLUDES" | sort); do
  # Check if mapped
  MAPPED=$(grep -q "**Path:**.*\`$f\`" .discovery/*.md 2>/dev/null && echo "✅ true" || echo "❌ false")
  
  # Get timestamp (from discovery doc or file mtime)
  if [ "$MAPPED" = "✅ true" ]; then
    TIMESTAMP=$TOC_TIME  # Use TOC generation time for simplicity
  else
    TIMESTAMP="-"
  fi
  
  # Find where used (grep for filename in source dirs)
  BASENAME=$(basename "$f")
  WHERE_USED=$(grep -rl "$BASENAME" src/ 2>/dev/null | head -3 | xargs -I {} echo "\`{}\`" | tr '\n' ',' | sed 's/,$//')
  [ -z "$WHERE_USED" ] && WHERE_USED="(not referenced)"
  
  # Determine purpose (from orphan category or manual)
  PURPOSE=$(grep -q "\`$f\`" .discovery/TOC.md 2>/dev/null && grep "\`$f\`" .discovery/TOC.md | sed 's/.*| //; s/|$//' || echo "TODO: determine purpose")
  
  echo "| \`$f\` | $MAPPED | $TIMESTAMP | $WHERE_USED | $PURPOSE |" >> .discovery/TOC.md
done
```

---

## Phase1.75: Monorepo Detection & Handling

For monorepos or pluralistic repositories:

```markdown
## Monorepo Detection

If the project has multiple `package.json`, `Cargo.toml`, or top-level directories with their own build systems:

### Detection Heuristics:
1. Multiple `package.json` files (not in `node_modules/`)
2. Top-level dirs: `packages/`, `apps/`, `services/`, `libs/`
3. Workspace configs: `pnpm-workspace.yaml`, `lerna.json`, `nx.json`

### Mapping Strategy:
- Create `.discovery/<NNN>-<package-name>.md` for each package
- Cross-reference between packages (shared deps, imports)
- Generate unified TOC with per-package sections

### Example Structure:
```
.discovery/
├── 000-root.md              # Root workspace config
├── 100-apps-web.md        # packages/web
├── 101-apps-mobile.md     # packages/mobile
├── 200-libs-core.md       # packages/core
└── 300-services-api.md   # services/api
```
```

**Monorepo Mapping Workflow:**

```bash
# Detect monorepo
if [ $(find . -name "package.json" ! -path "*/node_modules/*" | wc -l) -gt 1 ]; then
  echo "MONOREPO DETECTED"
  # Map each package separately
  for pkg in $(find . -name "package.json" ! -path "*/node_modules/*" | sort); do
    pkg_dir=$(dirname "$pkg")
    echo "Mapping package: $pkg_dir"
    # Run Phase 0-5 for each package
  done
fi
```
