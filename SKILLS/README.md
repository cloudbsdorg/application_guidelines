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
| [progress-tracker-updater](progress-tracker-updater.md) | Create and maintain TODO Tracker Summary tables | When updating phase progress |
| [quick-reference-generator](quick-reference-generator.md) | Create Quick Reference sections for AGENTS_START_HERE | When creating agent entry points |
| [reverse-engineer-for-port](reverse-engineer-for-port.md) | Analyze source code to understand actual behavior | When porting applications |
| [feature-task-generator](feature-task-generator.md) | Generate tasks from feature analysis | After reverse-engineering analysis |
| [code-quality-analyzer](code-quality-analyzer.md) | Find duplication and plan refactoring | When reviewing ported code quality |
| [ui-ux-analyzer](ui-ux-analyzer.md) | Document UI objects, states, actions, and data flow | When analyzing interfaces for implementation |
| [api-analyzer](api-analyzer.md) | Document REST endpoints, HTTP protocols, request/response formats | When analyzing APIs for implementation |
| [message-queue-analyzer](message-queue-analyzer.md) | Document message brokers, queues, pub/sub patterns, event streaming | When analyzing queue systems (RabbitMQ, Kafka, MQTT, etc.) |

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
     ├──► quick-reference-generator
     │
     ├──► progress-tracker-updater
     │
     └──► build-status-updater

plan-validator (standalone - validates all of the above)

reverse-engineer-for-port
     │
     └──► feature-task-generator
               │
               └──► code-quality-analyzer (optional - for refactoring backlog)

ui-ux-analyzer (standalone - analyzes UI for implementation)

api-analyzer (standalone - analyzes REST APIs and HTTP protocols)

message-queue-analyzer (standalone - analyzes message brokers and queues)
```

## Skill Categories

### Project Initialization
These skills create the initial project structure:

- `plan-document-generator` — Create `.plan/` structure and document templates
- `toc-generator` — Create 000 TOC document
- `agents-start-here-generator` — Create `AGENTS_START_HERE.md`
- `build-status-updater` — Create `0002-<Project>-Build-Status.md`
- `quick-reference-generator` — Create Quick Reference section
- `progress-tracker-updater` — Create TODO Tracker Summary

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

### Code Porting
These skills analyze and port applications from one language/framework to another:

- `reverse-engineer-for-port` — Analyze actual code behavior (entry points, features, dead code)
- `feature-task-generator` — Generate porting tasks from feature analysis
- `code-quality-analyzer` — Identify duplication and plan refactoring after porting
- `ui-ux-analyzer` — Document UI objects, states, actions, and data flow
- `api-analyzer` — Document REST endpoints, HTTP protocols, request/response formats
- `message-queue-analyzer` — Document message brokers, queues, pub/sub patterns, event streaming

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

### Port Application

```
Task: "Port <application> from <source> to <target>"

1. Load reverse-engineer-for-port — to analyze actual code behavior
   - Trace entry points, find dead code, classify components
   - Output: Feature Inventory with evidence

2. Load feature-task-generator — to generate porting tasks
   - Group by workflow, not file
   - Output: Task table with priorities and dependencies

3. Load code-quality-analyzer — to identify refactoring opportunities
   - Find duplication, interface opportunities
   - Output: Refactoring backlog (fix after working port)
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
progress-tracker-updater
quick-reference-generator
reverse-engineer-for-port
feature-task-generator
code-quality-analyzer
ui-ux-analyzer
api-analyzer
message-queue-analyzer
===END SKILL===
```

## Reference

- [Planning/PLANNING.md](../Planning/PLANNING.md) — Full planning standard
- [AGENTS_START_HERE.md](../AGENTS_START_HERE.md) — Primary agent entry point
- [INIT_PROMPT.md](../INIT_PROMPT.md) — System prompt for AI sessions