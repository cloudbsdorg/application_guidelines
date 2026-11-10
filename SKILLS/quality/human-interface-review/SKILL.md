---
name: human-interface-review
description: >-
  Get a second opinion on anything a person looks at and uses - a web page, a
  TUI, a desktop window, navigation, user-facing copy, visual design - before
  shipping it. Run the review through a gateway model, never agy. Use when a
  deliverable is an interface rather than internals, and pair it with
  code-craft, which covers the code behind the interface.
keywords:
  - UI review
  - design review
  - gateway model
  - agy (banned)
  - polish
  - copy review
  - accessibility review
---

# Human-interface review

CloudBSD law (`AGENTS.md` rule 28, "Interface review through a gateway model
(all UIs), never agy") requires an independent interface review for extra
polish on **any** user interface. **Never use agy (Antigravity CLI) for
anything: not as a review voice, not as a fallback, not as a coding agent
(owner order, repeated many times; restated 2026-11-10 2:51 AM CT).** This
skill is how to do that well; the rule itself lives in `AGENTS.md`.

The ordered chain is: a gateway model at `https://llm.cloudbsd.org/v1` (for
example `dgx/minimax` or `dgx/default`); if that model or the gateway is
unavailable, another live gateway model; then Ollama Cloud; then free models
through the `opencode-free-model-shim`. Never agy. A panel that counted agy as
a member must be rebuilt without it, not reported as degraded because agy
failed.

## When to invoke

Any time the deliverable is something a person looks at and interacts with:

- a web page or site - a new page, a redesign, a significant layout change
- UI components, navigation, information architecture
- user-facing copy: tone, hierarchy, readability
- visual design decisions: palette, type, spacing, structure
- a TUI, an operator console, or a desktop window - the law is not web-only

Not for backend, kernel, or CLI-internals work, and not for a one-line tweak.

## How to consult

Prefer a gateway model, for example:

```sh
review-opencode --model dgx/minimax
```

or the commit-review gate's interface voice. If that model or the gateway is
unavailable, try another live gateway model, then Ollama Cloud, then free
models through the `opencode-free-model-shim`. Never invoke `agy`.

Three things decide whether the answer is useful:

- **Make the prompt self-contained.** Inline the page's structure, its content,
  and the design context, and tell the reviewer *not* to read files or use
  tools. A long prompt belongs in a file passed to the reviewer, not in argv
  of a banned CLI.
- **Ask for a short, prioritised list of concrete changes**, not general
  praise. "What are the five things most worth fixing, in order" beats "what do
  you think".
- **Give it the constraints it must respect** - the CloudBSD and REVYTECH theme
  tokens, WCAG 2.1 AA, keyboard navigability - or it will suggest a redesign
  that violates law.

## What to do with the feedback

Apply the substantive points: missing content, structure, interaction,
accessibility, tone for the actual audience. But **keep the author's own voice
and their own sentences** where a page elaborates words a person wrote - polish
the elaboration, do not overwrite the authored lines. Then rebuild, re-screenshot,
and keep the before and after as evidence.

This is extra refinement, not a substitute for evidence. Playwright coverage,
asserted visible text, and the theme tokens are still required where they
apply, and a working interface does not get blocked because every allowed
reviewer is unavailable; record that unavailability. It reviews the view
layer only - never backend, APIs, or business logic.

## Related

- [code-craft](../code-craft/SKILL.md) - the same discipline for the code behind the interface
- [ui-ux-analyzer](../../analysis/ui-ux-analyzer/SKILL.md) - specifying an interface before building it
- `Web-User-Interfaces/WEBUI.md`, `TUI/TUI.md`, `Desktop/DESKTOP.md` - the interface law itself
- `AGENTS.md` rule 28 - the law this skill carries out
