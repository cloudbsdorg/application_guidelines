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

# Check 3: INIT_PROMPT.md starts with a Level 1 header
echo "[Check 3] INIT_PROMPT.md Level 1 header..."
if [ -f "INIT_PROMPT.md" ]; then
    FIRST_LINE=$(head -n 1 INIT_PROMPT.md)
    if echo "$FIRST_LINE" | grep -qE '^# .+'; then
        echo "  PASS: INIT_PROMPT.md starts with a Level 1 header."
    else
        echo "  FAIL: INIT_PROMPT.md does not start with a Level 1 header."
        echo "    First line: $FIRST_LINE"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo "  FAIL: INIT_PROMPT.md not found."
    ERRORS=$((ERRORS + 1))
fi
echo ""

# Check 4: Testing Infrastructure/TESTING_INFRASTRUCTURE.md starts with a Level 1 header
echo "[Check 4] TESTING_INFRASTRUCTURE.md Level 1 header..."
if [ -f "Testing Infrastructure/TESTING_INFRASTRUCTURE.md" ]; then
    FIRST_LINE=$(head -n 1 "Testing Infrastructure/TESTING_INFRASTRUCTURE.md")
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

# Summary
echo "======================================="
if [ "$ERRORS" -eq 0 ]; then
    echo "All checks passed."
    exit 0
else
    echo "$ERRORS check(s) failed."
    exit 1
fi
