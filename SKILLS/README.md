# CloudBSD Application Guidelines — Skills Index

This directory contains AI skills for CloudBSD project development.

## Available Skills

| Skill | Purpose | When to Load |
|-------|---------|--------------|
| [task-workflow](task-workflow.md) | Task claiming, completion, and status management | When picking/completing tasks |
| [plan-document-generator](plan-document-generator.md) | Create plan documents following standard templates | When creating new documents or initializing projects |
| [sysctl-documenter](sysctl-documenter.md) | Document sysctl MIB hierarchies | When defining configuration interfaces |
| [ascii-diagrammer](ascii-diagrammer.md) | Generate architecture diagrams | When writing architecture documents |
| [risk-assessor](risk-assessor.md) | Create and maintain risk registers | When creating 700 document or risk review |
| [test-planner](test-planner.md) | Generate testing documentation | When creating 401/402/1101 documents |
| [toc-generator](toc-generator.md) | Create table of contents documents | When creating 000 document |
| [agents-start-here-generator](agents-start-here-generator.md) | Generate agent entry point document | When initializing a project |
| [build-status-updater](build-status-updater.md) | Maintain CI/CD build status | When updating build status |

## Loading a Skill

When instructed to load a skill, read the skill file and follow its specifications:

```
User: "Load the task-workflow skill"
Assistant: [reads SKILLS/task-workflow.md and follows its protocols]
```

## Skill Categories

### Project Initialization
- `plan-document-generator` — Create .plan/ structure
- `agents-start-here-generator` — Create AGENTS_START_HERE.md
- `toc-generator` — Create 000 TOC document

### Task Management
- `task-workflow` — Task claiming and completion

### Technical Documentation
- `sysctl-documenter` — Sysctl interface docs
- `ascii-diagrammer` — Architecture diagrams
- `test-planner` — Test plans and cases

### Project Management
- `risk-assessor` — Risk register
- `build-status-updater` — CI/CD status
- `toc-generator` — Document index

## Skill Conventions

All skills follow these conventions:

1. **Purpose** — Clear statement of what the skill does
2. **Triggers** — When to load the skill
3. **Capabilities** — What the skill can do
4. **Templates** — Ready-to-use document structures
5. **Reference** — Link to Planning/PLANNING.md for full specification

## Using Multiple Skills

For complex tasks, load multiple skills:

```
Task: "Create the complete .plan/ structure for my new project"

1. Load plan-document-generator — to create document templates
2. Load toc-generator — to create TOC
3. Load agents-start-here-generator — to create entry point
4. Load risk-assessor — to create initial risk register
```

## Skill Maintenance

Skills are versioned alongside Planning/PLANNING.md:
- When PLANNING.md is updated, relevant skills should be updated
- Skills reference the specific section of PLANNING.md they implement
- Version numbers in skills should match PLANNING.md version

## Reference

See [Planning/PLANNING.md](../Planning/PLANNING.md) for the full planning standard.