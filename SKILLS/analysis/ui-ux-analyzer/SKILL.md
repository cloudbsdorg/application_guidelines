---
name: ui-ux-analyzer
description: >-
  Turn an existing user interface into an implementation-ready specification -
  objects, states, actions, forms, data flow, SVG wireframes. Use when
  analysing an interface for reimplementation, when documenting screens and
  their behaviour, or when producing wireframes before building a UI.
---

# Skill: ui-ux-analyzer (Modular)

> **Version:** 2.0 (Modular — sub-skills by phase)
> **Purpose:** Analyze UIs and produce implementation-ready specs.

This skill uses **modular sub-skills** — load only what you need.

---

## Quick-Load Index

| Phase | Sub-Skill Path | Trigger When... |
|-------|----------------|--------------|
| **Wireframing** | `ui-analysis/ui-ux-analyzer/wireframing.md` | Need SVG wireframes/mockups |
| **Objects** | `ui-analysis/ui-ux-analyzer/objects.md` | Building UI object inventory |
| **States** | `ui-analysis/ui-ux-analyzer/states.md` | Documenting object states |
| **Actions** | `ui-analysis/ui-ux-analyzer/actions.md` | Mapping user interactions |
| **Data Flow** | `ui-analysis/ui-ux-analyzer/data-flow.md` | Analyzing bindings/patterns |
| **Forms** | `ui-analysis/ui-ux-analyzer/forms.md` | Documenting form validation |

---

## Loading Pattern

```bash
# Load only what you need:
===SKILL:ui-ux-analyzer/wireframing===
  [reads ui-analysis/ui-ux-analyzer/wireframing.md]
===END SKILL===

# Or load multiple if needed:
===SKILL:ui-ux-analyzer/objects===
  [reads ui-analysis/ui-ux-analyzer/objects.md]
===END SKILL===

===SKILL:ui-ux-analyzer/states===
  [reads ui-analysis/ui-ux-analyzer/states.md]
===END SKILL===
```

---

## Core Principle

> **A UI is not its widgets. It's a projection of state through objects, shaped by actions.**

A button is meaningless without knowing: what state it reflects, what action it triggers, what state it leaves behind.

---

## Loading Instructions

Load this skill when the user asks you to:
- Analyze a UI/UX for implementation
- Document UI objects and their types
- Understand user interaction flows
- Generate UI specifications from existing code
- Plan UI feature implementation
- Draw wireframes and UI mockups as in-repo SVG files

---

## Integration

This skill feeds into:
- `migration/codebase-migrator.md` — When porting UI apps
- `analysis/codebase-mapper.md` — UI components get mapped as objects
- `planning/feature-task-generator.md` — UI features → tasks

---

## Checklist

- [ ] UI objects inventoried (display, input, action, container, collection, nav, feedback, composite)
- [ ] States mapped per object (default, hover, active, disabled, loading, error, etc.)
- [ ] Actions discovered and chained (click, submit, navigate, etc.)
- [ ] Data bindings documented (one-way, two-way, event)
- [ ] Forms analyzed with validation rules
- [ ] Wireframes generated for key views
