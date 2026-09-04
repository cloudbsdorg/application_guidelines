@AGENTS.md

# CLAUDE.md

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed. CloudBSD law lives in `AGENTS.md` (imported above).

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

## 5. Red-green TDD and evidence (law)

**Not optional. Not "aim for tests sometime." A task is not complete until there is evidence it works.**

- **New work:** write a failing test first (red), then the minimum production code to pass (green), then refactor.
- **Existing code that shipped without tests:** missing tests are a defect. You MUST still add tests. Characterization / post-facto tests are allowed to lock current behavior before changing it.
- **Coverage:** as close to 100% as possible; critical paths 100%. Generated/vendored code may be excluded; application code may not.
- **Integration tests are law.** Exercise real seams (HTTP API + store, worker job commit, SIGHUP reload, tenant isolation). In-memory fakes OK when the seam is under test. Compile-only is not evidence.
- **Store evidence** with the change. If a tool is missing, find or make one.
- **License:** BSD 3-Clause (Copyright REVYTECH, Inc.), not MIT.

See `Unit-Testing/UNITTESTS.md` and `AGENTS.md`.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, clarifying questions come before implementation rather than after mistakes, and new code never lands without a failing test written first.
