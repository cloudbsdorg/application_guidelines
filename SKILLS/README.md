# CloudBSD Application Guidelines — Skills Index

This directory contains AI skills for CloudBSD project development.

## Available Skills

| Skill | Purpose | When to Load |
|-------|---------|--------------|
| [task-workflow](task-workflow.md) | Task claiming, completion, and status management | When picking/completing tasks |
| [plan-document-generator](plan-document-generator.md) | Create plan documents following standard templates | When creating new documents or initializing projects |
| [plan-validator](plan-validator.md) | Validate plan document compliance | On PR review or before commits |
| [sysctl-documenter](sysctl-documenter.md) | Document sysctl MIB hierarchies | When defining configuration interfaces |
| [ascii-diagrammer](ascii-diagrammer.md) | Generate architecture diagrams | When writing architecture documents |
| [risk-assessor](risk-assessor.md) | Create and maintain risk registers | When creating 700 document or risk review |
| [test-planner](test-planner.md) | Generate testing documentation | When creating 401/402/1101 documents |
| [toc-generator](toc-generator.md) | Create table of contents documents | When creating 000 document |
| [agents-start-here-generator](agents-start-here-generator.md) | Generate agent entry point document | When initializing a project |
| [build-status-updater](build-status-updater.md) | Maintain CI/CD build status | When updating build status |
| [validation-document-generator](validation-document-generator.md) | Create validation reports and corrections | When validating implementation tasks |
| [security-document-generator](security-document-generator.md) | Create security documentation (threat model, access control, etc.) | When creating 1.1-1.6 security documents |

## Skill Invocation Format

When instructed to load a skill, read the skill file and wrap the content with invocation markers:

```
===SKILL:task-workflow===
[skill content]
===END SKILL===
```

**Example:**

```
User: "Load the task-workflow skill"

Assistant:
===SKILL:task-workflow===
# Skill: task-workflow
**Purpose:** Enforce the claiming and completion protocols...
[skill content]
===END SKILL===

[Now follows the skill's protocols]
```

## Skill Dependency Graph

Skills depend on each other as follows:

```
agents-start-here-generator
    │
    ├──► toc-generator
    │        └──► plan-document-generator
    │
    ├──► task-workflow
    │
    ├──► plan-document-generator
    │        │
    │        ├──► ascii-diagrammer
    │        ├──► sysctl-documenter
    │        ├──► risk-assessor
    │        ├──► test-planner
    │        └──► toc-generator
    │
    └──► build-status-updater

plan-validator (standalone - validates all of the above)
```

## Skill Categories

### Project Initialization
These skills create the initial project structure:

- `plan-document-generator` — Create `.plan/` structure and document templates
- `toc-generator` — Create 000 TOC document
- `agents-start-here-generator` — Create `AGENTS_START_HERE.md`
- `build-status-updater` — Create `0002-<Project>-Build-Status.md`

### Task Management
- `task-workflow` — Task claiming and completion

### Technical Documentation
These skills generate specific document types:

- `sysctl-documenter` — Generate `501-*-Sysctl-Interface.md`
- `ascii-diagrammer` — Generate architecture diagrams for any document
- `test-planner` — Generate `401/402/1101` test documents
- `risk-assessor` — Generate `700-*-Risks.md`

### Quality Assurance
- `plan-validator` — Validate all plan documents for compliance

## Skill Conventions

All skills follow these conventions:

1. **Purpose** — Clear statement of what the skill does
2. **Triggers** — When to load the skill
3. **Capabilities** — What the skill can do
4. **Templates** — Ready-to-use document structures
5. **Reference** — Link to Planning/PLANNING.md for full specification

## Using Multiple Skills

For complex tasks, load multiple skills in dependency order:

### Initialize New Project

```
Task: "Create the complete .plan/ structure for my new project"

1. Load plan-document-generator — to create document templates
2. Load toc-generator — to create TOC
3. Load agents-start-here-generator — to create entry point
4. Load risk-assessor — to create initial risk register
5. Load build-status-updater — to create build status
```

### Create Architecture Document

```
Task: "Create the 200 architecture document"

1. Load plan-document-generator — to get document structure
2. Load ascii-diagrammer — to create architecture diagrams
3. Load sysctl-documenter — to document sysctl interfaces
```

### Validate Project

```
Task: "Validate my project's .plan/ directory"

1. Load plan-validator — to check compliance
2. Load task-workflow — to verify task states
```

## Skill Maintenance

Skills are versioned alongside Planning/PLANNING.md:

- When PLANNING.md is updated, relevant skills must be updated
- Skills reference the specific section of PLANNING.md they implement
- Version numbers in skills should match PLANNING.md version (currently v2.1)

## Master Planning Skill

For complex planning tasks, load all planning-related skills:

```
===SKILL:all-planning===
task-workflow
plan-document-generator
plan-validator
sysctl-documenter
ascii-diagrammer
risk-assessor
test-planner
toc-generator
agents-start-here-generator
build-status-updater
===END SKILL===
```

## Reference

- [Planning/PLANNING.md](../Planning/PLANNING.md) — Full planning standard
- [AGENTS_START_HERE.md](../AGENTS_START_HERE.md) — Primary agent entry point
- [INIT_PROMPT.md](../INIT_PROMPT.md) — System prompt for AI sessions