# Agent Behavior Guidelines

How an AI agent should *work* on a CloudBSD project. `AGENTS.md` says what the
software must be; this says how to go about producing it. It applies to every
agent and every tool - it is not specific to any one of them, and nothing here
repeats a rule that `AGENTS.md` already states.

**Tradeoff:** these guidelines bias toward caution over speed. For a trivial
task, use judgement.

## 1. Think before coding

**Do not assume. Do not hide confusion. Surface tradeoffs.**

Before implementing:

- State your assumptions explicitly. If you are uncertain, ask.
- If several interpretations exist, present them - do not silently pick one.
- If a simpler approach exists, say so. Push back when it is warranted.
- If something is unclear, stop. Name what is confusing. Ask.

## 2. Simplicity first

**The minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked for.
- No abstraction for single-use code.
- No flexibility or configurability that nobody requested.
- No error handling for scenarios that cannot occur.
- If you wrote 200 lines and it could be 50, rewrite it.

Ask: would a senior engineer call this overcomplicated? If yes, simplify.

This is not in tension with the design rigor `AGENTS.md` requires. A pattern
earns its place by removing real duplication or isolating a real axis of change.
Applied to code that has neither, it is just more code.

## 3. Surgical changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:

- Do not "improve" adjacent code, comments, or formatting.
- Do not refactor what is not broken.
- Match the existing style, even where you would have done it differently.
- If you notice unrelated dead code, mention it - do not delete it.

When your change orphans something:

- Remove the imports, variables, and functions that *your* change made unused.
- Do not remove pre-existing dead code unless you were asked to.

The test: every changed line traces directly to the request.

## 4. Goal-driven execution

**Define success criteria. Loop until they are verified.**

Turn the task into something checkable:

- "Add validation" becomes "write tests for the invalid inputs, then make them pass".
- "Fix the bug" becomes "write a test that reproduces it, then make it pass".
- "Refactor X" becomes "tests pass before and after".

For a multi-step task, state the plan first, with a check against each step:

```
1. <step> -> verify: <check>
2. <step> -> verify: <check>
3. <step> -> verify: <check>
```

Strong criteria let you work independently. Weak criteria - "make it work" -
force you back for clarification at every turn.

## 5. Do not multiply the truth

A fact belongs in one place.

- Editing a rule means editing `AGENTS.md`, not a copy of it.
- Adding a skill means adding a row to `SKILLS/TOC.md`, not to a second list.
- If you find the same statement in two documents, that is a defect. Delete one
  and link to the other, and say so in the commit message.

## 6. Load only what you need

`SKILLS/TOC.md` exists so you can decide what to read without reading it all.
Scan it, load the single skill that matches, and follow that skill's links only
when it tells you to. Loading everything is not thoroughness; it spends the
context you were going to need for the actual work.

---

**These guidelines are working when:** diffs contain fewer unnecessary changes,
fewer rewrites are caused by overcomplication, clarifying questions arrive
before the implementation rather than after the mistake, and no new code lands
without a failing test having been written first.

See `AGENTS.md` for CloudBSD law, `Unit-Testing/UNITTESTS.md` for the testing
and evidence requirements, and `SKILLS/quality/code-craft/SKILL.md` for the
design and algorithm discipline.
