@AGENTS.md
@Agent-Behavior/AGENT_BEHAVIOR.md

# CLAUDE.md — Claude Code adapter

This file exists only to load the shared guidance above. It carries **no rules of
its own**; every rule lives in `AGENTS.md`, and the working guidelines live in
`Agent-Behavior/AGENT_BEHAVIOR.md`. Both are tool-neutral and are read by the
other agent tools too. If a rule seems to be missing, add it there, not here.

## Claude-Code-specific notes

- **Skills.** Each skill in `SKILLS/` is a directory containing `SKILL.md` with
  `name` and `description` frontmatter, which is exactly the layout Claude Code
  discovers. Do not load them all: scan `SKILLS/TOC.md`, then read the one
  `SKILL.md` that matches the task, and its reference files only if that skill
  says to.
- **`@` imports.** The two lines at the top of this file are Claude Code import
  syntax. Other tools reach the same content their own way - `opencode.json`,
  `.cursor/rules/cloudbsd.mdc`, or `INIT_PROMPT.md` for a model with no
  checkout. Keep them in step: adding a shared document means adding it to all
  of the adapters, or to none.
