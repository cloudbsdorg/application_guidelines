---
name: ui-ux-analyzer-wireframing
description: SVG wireframing conventions and templates for UI-UX analysis.
---

# UI-UX Analyzer — Wireframing

UI design and prototyping artifacts are **SVG**, kept in-repo as `.svg` files. Do not draw ASCII boxes. Do not use Mermaid for pixel-layout screens (Mermaid is for architecture, flow, sequence, and graphs).

The live CloudBSD web UI is the Angular + Tailwind application. SVG is for design and prototyping only.

## Law

- Produce or edit `.svg` files (for example `docs/ui/wireframes/<screen>.svg`).
- Include `xmlns`, a `viewBox`, `role="img"`, and `aria-label` (and a `<title>`).
- Use simple rectangles, lines, and text. This is a wireframe, not a visual design system.
- Match CloudBSD Web UI rules: desktop and mobile. Prefer a desktop frame plus a stacked mobile frame, or note Tailwind breakpoints (`sm` / `md` / `lg`) in the SVG.
- Never replace an architecture diagram with SVG — load `SKILLS/diagramming/mermaid-diagrammer/SKILL.md` for those.

## Loading Instructions

Load this sub-skill when you need to:

- Draw a wireframe, mockup, or screen
- Document layout for UI-UX analysis
- Produce prototyping artifacts for a CloudBSD web UI

## Checked-in example

See `ui-analysis/ui-ux-analyzer/examples/layout-grid.svg` (header / content / footer).

Minimal inline pattern:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 480" width="800" height="480" role="img" aria-label="Layout wireframe: header, content, footer">
  <title>Layout grid wireframe</title>
  <rect x="8" y="8" width="784" height="464" fill="#ffffff" stroke="#333333" stroke-width="2"/>
  <rect x="8" y="8" width="784" height="56" fill="#eeeeee" stroke="#333333" stroke-width="2"/>
  <text x="400" y="42" text-anchor="middle" font-family="sans-serif" font-size="18">HEADER</text>
  <text x="400" y="250" text-anchor="middle" font-family="sans-serif" font-size="18">CONTENT</text>
  <rect x="8" y="416" width="784" height="56" fill="#eeeeee" stroke="#333333" stroke-width="2"/>
  <text x="400" y="450" text-anchor="middle" font-family="sans-serif" font-size="18">FOOTER</text>
</svg>
```

## Screens to produce as SVG

Create one `.svg` file per view (or per breakpoint pair). Cover at least:

| Screen | What to show |
|--------|----------------|
| Layout grid | Header, content, footer (or sidebar + main) |
| Form | Labels, fields, primary/secondary actions, required markers |
| Table / collection | Title, search, columns, row actions, pagination |
| Modal / dialog | Overlay, title, body, confirm/cancel |
| Sidebar app chrome | Nav items, main canvas, stats or list |
| Wizard / stepper | Step indicators, current step body, back/continue |
| Empty state | Message and a single primary action |
| Loading state | Placeholder and “Loading…” |
| Error state | Error copy and retry |

## SVG conventions

| Element | How to draw it |
|---------|----------------|
| Region / panel | `<rect>` with a 1–2px stroke |
| Button | Labeled `<rect>` (or rounded rect) |
| Field | `<rect>` plus a `<text>` label above |
| Selected / focus | Heavier stroke or a second outline rect |
| Disabled | Lower-contrast fill/text |
| Status | Short `<text>` (`Pending`, `Done`, `Error`) — not ASCII status art |

## Responsive breakpoints

| Breakpoint | Width | Devices |
|-----------|-------|---------|
| Mobile | < 640px | Phone |
| Tablet | 640-1024px | Tablet, small laptop |
| Desktop | 1024-1440px | Standard monitors |
| Wide | > 1440px | Large monitors, TVs |

## Component state indicators

| State | Indicator | When |
|-------|-----------|------|
| Default | Normal appearance | Idle |
| Hover | Highlight, cursor change | Mouse over |
| Active/Pressed | Slightly darker | Clicking |
| Focus | Outline or ring | Keyboard navigation |
| Disabled | Grayed out, no pointer | Not interactive |
| Loading | Spinner or skeleton | Async operation |
| Error | Red border, error icon | Validation failed |
| Success | Green checkmark | Operation complete |

## File template

```markdown
## Wireframe: [ViewName]

File: `docs/ui/wireframes/[view-name].svg`

- Breakpoints: mobile + desktop
- Primary action:
- Notes:
```

## Checklist

- [ ] Each screen is an in-repo `.svg` file
- [ ] No ASCII art boxes or `+---+` diagrams
- [ ] Architecture/flow remains Mermaid, not SVG
- [ ] Mobile and desktop layouts are represented
- [ ] Interactive regions are labeled (buttons, fields, nav)
