# CloudBSD skills

Task-specific skills for CloudBSD work. **The list of skills is
[`TOC.md`](TOC.md)** — this file explains the shape of the directory and how to
add to it, and deliberately does not repeat the list. One list, one place.

## The layout rule

```
SKILLS/<category>[/<sub-category>]/<skill-name>/SKILL.md
```

- A directory containing `SKILL.md` **is** a skill, and its directory name **is**
  the skill's name. No exceptions, so the tree can be enumerated mechanically.
- Any other directory is a category.
- Other `.md` files beside a `SKILL.md` are that skill's reference material.
  They are not skills, and they are loaded only when `SKILL.md` says to.

This is plain Markdown in plain directories on purpose. It is what Claude Code
discovers natively, it is what opencode and Cursor read without any conversion,
and it is what a model handed a single file can use. The layout was chosen
because every consumer can read it, not for any one of them.

## Frontmatter

Every `SKILL.md` begins with YAML:

```yaml
---
name: safe-kernel-deploy          # identical to the directory name
description: >-
  What the skill does, in a sentence. Then: Use when <the situations that
  should make an agent reach for it>.
keywords:
  - bectl
  - boot environment
  - rollback
---
```

`description` must contain a sentence beginning **"Use …"**. An agent scanning
the index is deciding *whether to load this at all*, and a description that only
describes gives it nothing to decide with. `keywords` supplies the trigger column
in `TOC.md`.

## Progressive disclosure

`SKILL.md` is the entry point and should stay short: what this is, when it
applies, and the shape of the work. Depth belongs in reference files next to it,
linked from `SKILL.md`, so that loading a skill costs a page rather than a
chapter. `analysis/api-analyzer/` is the worked example — a short `SKILL.md` over
five reference files, loaded individually.

## Adding or changing a skill

1. Create `SKILLS/<category>/<skill-name>/SKILL.md` with the frontmatter above.
2. Keep the entry file short; put detail in sibling reference files and link
   them.
3. Regenerate the index:

   ```sh
   tools/skills-index.py --write
   ```

4. Verify before committing:

   ```sh
   tools/skills-index.py --check
   bash test_md.sh
   ```

`TOC.md` is generated. Do not hand-edit it — change the skill's frontmatter and
regenerate, or the two will drift apart, which is the failure this layout exists
to prevent.

## What a skill is not

- **Not a place for law.** Law lives in [`AGENTS.md`](../AGENTS.md). A skill
  explains *how* to satisfy a rule and links to it. If a skill and `AGENTS.md`
  disagree, `AGENTS.md` wins and the skill is the defect.
- **Not a place for deployment facts.** No machine names, addresses,
  credentials, or credential locations — this repository is public. Those belong
  in the private operations repository. See "What belongs in this repository" in
  `AGENTS.md`.
- **Not something to load in bulk.** Scan `TOC.md`, load one skill.

## Diagrams

Mermaid (```` ```mermaid ```` fences) is the format for architecture, flowcharts,
sequence, class, and ER diagrams. SVG is allowed for UI wireframes and mockups,
kept in-repo as `.svg` files. ASCII-art diagrams are forbidden; DOT and PlantUML
are deprecated. See `diagramming/mermaid-diagrammer/SKILL.md`.

## Reference

- [`TOC.md`](TOC.md) — the index: triggers, paths, and what each skill is for
- [`../AGENTS.md`](../AGENTS.md) — CloudBSD law
- [`../Planning/PLANNING.md`](../Planning/PLANNING.md) — the `.plan/` standard many of these skills implement
