---
name: human-interface-review
description: >-
  Get a second opinion on anything a person looks at and uses - a web page, a
  TUI, a desktop window, navigation, user-facing copy, visual design - before
  shipping it. Use when a deliverable is an interface rather than internals,
  and pair it with code-craft, which covers the code behind the interface.
keywords:
  - UI review
  - design review
  - agy
  - polish
  - copy review
  - accessibility review
---

# Human-interface review

CloudBSD law (`AGENTS.md`, "agy for extra UI refinement") requires consulting
the `agy` reviewer for extra polish on **any** user interface, whenever access
to it has been granted. This skill is how to do that well; the rule itself
lives in `AGENTS.md` and is not restated here.

## When to invoke

Any time the deliverable is something a person looks at and interacts with:

- a web page or site - a new page, a redesign, a significant layout change
- UI components, navigation, information architecture
- user-facing copy: tone, hierarchy, readability
- visual design decisions: palette, type, spacing, structure
- a TUI, an operator console, or a desktop window - the law is not web-only

Not for backend, kernel, or CLI-internals work, and not for a one-line tweak.

## How to consult

Single-shot print mode, with the effort turned up:

```sh
agy -p "<self-contained prompt>" --effort high
```

Three things decide whether the answer is useful:

- **Make the prompt self-contained.** Inline the page's structure, its content,
  and the design context, and tell the reviewer *not* to read files or use
  tools. It is agentic; left alone it will go exploring and time out. A long
  prompt belongs in a file: `agy -p "$(cat prompt.txt)"`.
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
apply, and a working interface does not get blocked because the reviewer is
unavailable. It reviews the view layer only - never backend, APIs, or business
logic.

## Related

- [code-craft](../code-craft/SKILL.md) - the same discipline for the code behind the interface
- [ui-ux-analyzer](../../analysis/ui-ux-analyzer/SKILL.md) - specifying an interface before building it
- `Web-User-Interfaces/WEBUI.md`, `TUI/TUI.md`, `Desktop/DESKTOP.md` - the interface law itself
