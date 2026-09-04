#!/bin/bash

# Markdown sanity check script for CloudBSD Application Guidelines
# Run from project root: bash test_md.sh

ERRORS=0

echo "=== CloudBSD Markdown Sanity Checks ==="
echo ""

# Check 1: No empty Markdown files
echo "[Check 1] Empty Markdown files..."
EMPTY_FILES=$(find . -name "*.md" -type f -empty ! -path "./.junie/*")
if [ -n "$EMPTY_FILES" ]; then
    echo "  FAIL: The following Markdown files are empty:"
    echo "$EMPTY_FILES" | sed 's/^/    /'
    ERRORS=$((ERRORS + 1))
else
    echo "  PASS: No empty Markdown files found."
fi
echo ""

# Check 2: README.md starts with a Level 1 header
echo "[Check 2] README.md Level 1 header..."
if [ -f "README.md" ]; then
    FIRST_LINE=$(head -n 1 README.md)
    if echo "$FIRST_LINE" | grep -qE '^# .+'; then
        echo "  PASS: README.md starts with a Level 1 header."
    else
        echo "  FAIL: README.md does not start with a Level 1 header."
        echo "    First line: $FIRST_LINE"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo "  FAIL: README.md not found."
    ERRORS=$((ERRORS + 1))
fi
echo ""

# Check 3: AGENTS.md starts with a Level 1 header
echo "[Check 3] AGENTS.md Level 1 header..."
if [ -f "AGENTS.md" ]; then
    FIRST_LINE=$(head -n 1 AGENTS.md)
    if echo "$FIRST_LINE" | grep -qE '^# .+'; then
        echo "  PASS: AGENTS.md starts with a Level 1 header."
    else
        echo "  FAIL: AGENTS.md does not start with a Level 1 header."
        echo "    First line: $FIRST_LINE"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo "  FAIL: AGENTS.md not found."
    ERRORS=$((ERRORS + 1))
fi
echo ""

# Check 4: Testing-Infrastructure/TESTING_INFRASTRUCTURE.md starts with a Level 1 header
echo "[Check 4] TESTING_INFRASTRUCTURE.md Level 1 header..."
if [ -f "Testing-Infrastructure/TESTING_INFRASTRUCTURE.md" ]; then
    FIRST_LINE=$(head -n 1 "Testing-Infrastructure/TESTING_INFRASTRUCTURE.md")
    if echo "$FIRST_LINE" | grep -qE '^# .+'; then
        echo "  PASS: TESTING_INFRASTRUCTURE.md starts with a Level 1 header."
    else
        echo "  FAIL: TESTING_INFRASTRUCTURE.md does not start with a Level 1 header."
        echo "    First line: $FIRST_LINE"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo "  FAIL: TESTING_INFRASTRUCTURE.md not found."
    ERRORS=$((ERRORS + 1))
fi
echo ""

# Check 5: Planning/PLANNING.md starts with a Level 1 header
echo "[Check 5] PLANNING.md Level 1 header..."
if [ -f "Planning/PLANNING.md" ]; then
    FIRST_LINE=$(head -n 1 "Planning/PLANNING.md")
    if echo "$FIRST_LINE" | grep -qE '^# .+'; then
        echo "  PASS: PLANNING.md starts with a Level 1 header."
    else
        echo "  FAIL: PLANNING.md does not start with a Level 1 header."
        echo "    First line: $FIRST_LINE"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo "  FAIL: PLANNING.md not found."
    ERRORS=$((ERRORS + 1))
fi
echo ""

# Check 6: every relative Markdown link resolves
echo "[Check 6] Markdown link targets..."
if python3 tools/check-links.py > /tmp/cloudbsd-links.$$ 2>&1; then
    echo "  PASS: every relative Markdown link resolves."
else
    echo "  FAIL: broken Markdown links:"
    sed 's/^/    /' /tmp/cloudbsd-links.$$
    ERRORS=$((ERRORS + 1))
fi
rm -f /tmp/cloudbsd-links.$$
echo ""

# Check 7: SKILLS/TOC.md is generated from, and agrees with, the skill tree
echo "[Check 7] SKILLS/TOC.md is current..."
if python3 tools/skills-index.py --check > /tmp/cloudbsd-toc.$$ 2>&1; then
    echo "  PASS: $(cat /tmp/cloudbsd-toc.$$)"
else
    echo "  FAIL: $(cat /tmp/cloudbsd-toc.$$)"
    ERRORS=$((ERRORS + 1))
fi
rm -f /tmp/cloudbsd-toc.$$
echo ""

# Summary
echo "======================================="
if [ "$ERRORS" -eq 0 ]; then
    echo "All checks passed."
    exit 0
else
    echo "$ERRORS check(s) failed."
    exit 1
fi
