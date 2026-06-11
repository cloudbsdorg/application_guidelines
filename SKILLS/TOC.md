# Skills Table of Contents

> **For Agents**: Scan this TOC to identify relevant skills by trigger. Load ONLY the skill you need — do NOT load all skills.

## Quick-Scan Index (Triggers → Skill Path)

| Trigger Keyword | Skill Path | One-Line Description |
|----------------|-----------|----------------------|
| `agent SDK`, `Cloudflare Agent`, `stateful agent` | `platform/cloudflare/agents-sdk.md` | Build AI agents on Cloudflare Workers |
| `agent start`, `entry point`, `AGENTS_START_HERE` | `planning/agents-start-here-generator.md` | Generate agent entry point document |
| `API`, `REST`, `endpoint`, `HTTP` | `analysis/api-analysis/api-analyzer.md` | Document REST endpoints and HTTP protocols |
| `audit`, `vulnerability`, `OWASP`, `STRIDE` | `security/security-audit/security-audit.md` | Security audit with OWASP and STRIDE |
| `bhyve`, `VM`, `virtual machine` | `freebsd-admin/bhyve-manager.md` | Create and manage bhyve VMs |
| `build status`, `CI`, `0002` | `workflow/build-status-updater.md` | Maintain CI/CD build status |
| `Cloudflare`, `Worker`, `Pages`, `KV`, `R2` | `platform/cloudflare/cloudflare.md` | Comprehensive Cloudflare platform skill |
| `code quality`, `duplication`, `refactor` | `analysis/code-quality-analyzer.md` | Find duplication and plan refactoring |
| `codebase`, `explore`, `understand`, `find in code` | `analysis/codebase/codebase.md` | Read-only codebase exploration |
| `consult`, `advice`, `opinion`, `should I` | `planning/office-hours/office-hours.md` | Direct consulting with recommendations |
| `debug`, `investigate`, `root cause`, `trace` | `workflow/investigate/investigate.md` | Root cause debugging with evidence |
| `diagram`, `architecture`, `flowchart` | `diagramming/ascii-diagrammer.md` | Generate Mermaid diagrams |
| `effect`, `Effect v4`, `effect-smol` | `platform/opencode/effect.md` | Work with Effect-based TypeScript |
| `feature`, `task generation` | `planning/feature-task-generator.md` | Generate tasks from feature analysis |
| `file system`, `path`, `permission`, `locking` | `analysis/os-analysis/file-system-analyzer.md` | Document filesystem dependencies |
| `GitHub`, `triage`, `issue`, `PR` | `platform/opencode/github-triage.md` | Read-only GitHub triage |
| `jail`, `iocage`, `bastille`, `pot` | `freebsd-admin/jail-manager.md` | Manage FreeBSD jails |
| `Linuxulator`, `Linux binary` | `freebsd-admin/linuxulator-runner.md` | Run Linux binaries on FreeBSD |
| `map codebase`, `discovery`, `.discovery/` | `analysis/codebase-mapper.md` (modular — load `phases-0-1.md`, `phases-2-3.md`, etc.) | Map codebase to tree-view documents |
| `message queue`, `RabbitMQ`, `Kafka`, `MQTT` | `analysis/message-queue-analyzer.md` (modular — load `rabbitmq.md`, `kafka.md`, etc.) | Document message brokers and queues |
| `migrate`, `port`, `convert`, `legacy`, `DOS`, `Pascal`, `retro` | `migration/codebase-migrator.md` | Migrate legacy apps to modern platforms |
| `orchestrate`, `pre-planning`, `coordinate` | `analysis/source-analysis-orchestrator.md` | Coordinate all analysis skills |
| `plan`, `document`, `initialize` | `planning/plan-document-generator.md` | Create plan documents and `.plan/` structure |
| `plan`, `document`, `initialize` | `planning/plan-document-generator.md` | Create plan documents and `.plan/` structure |
| `plan-ceo-review`, `scope challenge`, `is this right` | `planning/plan-ceo-review/plan-ceo-review.md` | Strategic scope challenge |
| `pre-publish`, `release gate`, `npm publish` | `platform/opencode/pre-publish-review.md` | Nuclear-grade 16-agent release gate |
| `PR`, `pull request`, `worktree`, `merge` | `platform/opencode/work-with-pr.md` | Full PR lifecycle |
| `privilege`, `UID`, `GID`, `capability`, `chroot` | `analysis/os-analysis/privilege-analyzer.md` | Document privilege requirements |
| `progress`, `tracker`, `TODO` | `workflow/progress-tracker-updater.md` | Create TODO Tracker Summary tables |
| `quick reference`, `AGENTS_START_HERE` | `planning/quick-reference-generator.md` | Create Quick Reference sections |
| `rc.d`, `startup script`, `rc script` | `freebsd-admin/rc-script-writer.md` | Write FreeBSD rc.d startup scripts |
| `review`, `code review`, `lgtm`, `approve` | `workflow/review/review.md` | Code review for correctness/security |
| `reverse engineer`, `port`, `analyze source` | `analysis/reverse-engineer-for-port.md` | Analyze source code for porting |
| `risk`, `threat`, `700 document` | `security/risk-assessor.md` | Create and maintain risk registers |
| `scope`, `challenge plan`, `effort estimate` | `planning/plan-ceo-review/plan-ceo-review.md` | Strategic scope challenge |
| `security`, `threat model`, `access control`, `1.1-1.6` | `security/security-document-generator.md` | Create security documents |
| `service`, `rc.d`, `sysrc` | `freebsd-admin/service-manager.md` | Manage FreeBSD services |
| `ship`, `deploy`, `release`, `push to prod` | `workflow/ship/ship.md` | Verified deployment workflow |
| `socket`, `TCP`, `UDP`, `epoll`, `kqueue` | `analysis/os-analysis/network-stack-analyzer.md` | Document network stack dependencies |
| `syscall`, `file I/O`, `memory`, `signal` | `analysis/os-analysis/system-call-analyzer.md` (modular — load `file-io.md`, `signals.md`, etc.) | Analyze syscalls for porting |
| `sysctl`, `MIB`, `kernel parameter` | `planning/sysctl-documenter.md` | Document sysctl MIB hierarchies |
| `task`, `claim`, `complete` | `workflow/task-workflow.md` | Task claiming and completion |
| `test`, `401`, `402`, `1101` | `testing/test-planner.md` | Generate testing documentation |
| `thread`, `process`, `IPC`, `synchronization` | `analysis/os-analysis/process-model-analyzer.md` (modular — load `threads.md`, `synchronization.md`, etc.) | Document threads and IPC patterns |
| `TOC`, `table of contents`, `000` | `planning/toc-generator.md` | Create table of contents documents |
| `UI`, `UX`, `interface`, `wireframe` | `analysis/ui-analysis/ui-ux-analyzer.md` (modular — load `wireframing.md`, `objects.md`, `actions.md`, etc.) | Document UI objects, states, actions |
| `validation report`, `corrections` | `testing/validation-document-generator.md` | Create validation reports |
| `ZFS`, `pool`, `snapshot` | `freebsd-admin/zfs-manager.md` | ZFS pool management and snapshots |

## Skill Categories

### Planning (`planning/`)
| Skill | Path | Purpose |
|-------|------|---------|
| task-workflow | `workflow/task-workflow.md` | Task claiming and completion |
| plan-document-generator | `planning/plan-document-generator.md` | Create plan documents |
| plan-validator | `planning/plan-validator.md` | Validate plan compliance |
| sysctl-documenter | `planning/sysctl-documenter.md` | Document sysctl MIBs |
| toc-generator | `planning/toc-generator.md` | Create TOC documents |
| agents-start-here-generator | `planning/agents-start-here-generator.md` | Generate entry points |
| quick-reference-generator | `planning/quick-reference-generator.md` | Create Quick Reference |
| feature-task-generator | `planning/feature-task-generator.md` | Generate tasks from features |
| office-hours | `planning/office-hours/office-hours.md` | Consulting with recommendations |
| plan-ceo-review | `planning/plan-ceo-review/plan-ceo-review.md` | Strategic scope challenge |

### Analysis (`analysis/`)
| Skill | Path | Purpose |
|-------|------|---------|
| reverse-engineer-for-port | `analysis/reverse-engineer-for-port.md` | Analyze source for porting |
| code-quality-analyzer | `analysis/code-quality-analyzer.md` | Find duplication |
| ui-ux-analyzer | `analysis/ui-analysis/ui-ux-analyzer.md` | Document UI/UX |
| api-analyzer | `analysis/api-analysis/api-analyzer.md` | Document REST APIs |
| message-queue-analyzer | `analysis/message-queue-analyzer.md` | Document message queues |
| codebase-mapper | `analysis/codebase-mapper.md` | Map codebase structure |
| source-analysis-orchestrator | `analysis/source-analysis-orchestrator.md` | Coordinate analysis |
| codebase | `analysis/codebase/codebase.md` | Read-only codebase exploration |

#### OS Analysis (`analysis/os-analysis/`)
| Skill | Path | Purpose |
|-------|------|---------|
| system-call-analyzer | `analysis/os-analysis/system-call-analyzer.md` | Analyze syscalls |
| process-model-analyzer | `analysis/os-analysis/process-model-analyzer.md` | Document threads/IPC |
| network-stack-analyzer | `analysis/os-analysis/network-stack-analyzer.md` | Document network stack |
| file-system-analyzer | `analysis/os-analysis/file-system-analyzer.md` | Document filesystem |
| privilege-analyzer | `analysis/os-analysis/privilege-analyzer.md` | Document privileges |

### FreeBSD Admin (`freebsd-admin/`)
| Skill | Path | Purpose |
|-------|------|---------|
| bhyve-manager | `freebsd-admin/bhyve-manager.md` | Manage bhyve VMs |
| jail-manager | `freebsd-admin/jail-manager.md` | Manage FreeBSD jails |
| zfs-manager | `freebsd-admin/zfs-manager.md` | ZFS pool management |
| linuxulator-runner | `freebsd-admin/linuxulator-runner.md` | Run Linux binaries |
| rc-script-writer | `freebsd-admin/rc-script-writer.md` | Write rc.d scripts |
| service-manager | `freebsd-admin/service-manager.md` | Manage services |

### Workflow (`workflow/`)
| Skill | Path | Purpose |
|-------|------|---------|
| task-workflow | `workflow/task-workflow.md` | Task claiming/completion |
| build-status-updater | `workflow/build-status-updater.md` | Maintain build status |
| progress-tracker-updater | `workflow/progress-tracker-updater.md` | Update TODO trackers |
| investigate | `workflow/investigate/investigate.md` | Root cause debugging |
| review | `workflow/review/review.md` | Code review |
| ship | `workflow/ship/ship.md` | Verified deployment |

### Security (`security/`)
| Skill | Path | Purpose |
|-------|------|---------|
| risk-assessor | `security/risk-assessor.md` | Create risk registers |
| security-audit | `security/security-audit/security-audit.md` | Security audit (OWASP/STRIDE) |
| security-document-generator | `security/security-document-generator.md` | Create security docs |

### Testing (`testing/`)
| Skill | Path | Purpose |
|-------|------|---------|
| test-planner | `testing/test-planner.md` | Generate test documents |
| validation-document-generator | `testing/validation-document-generator.md` | Create validation reports |

### Diagramming (`diagramming/`)
| Skill | Path | Purpose |
|-------|------|---------|
| ascii-diagrammer | `diagramming/ascii-diagrammer.md` | Generate Mermaid diagrams |

### Platform - OpenCode (`platform/opencode/`)
| Skill | Path | Purpose |
|-------|------|---------|
| effect | `platform/opencode/effect.md` | Work with Effect TypeScript |
| github-triage | `platform/opencode/github-triage.md` | GitHub triage |
| pre-publish-review | `platform/opencode/pre-publish-review.md` | Release gate |
| work-with-pr | `platform/opencode/work-with-pr.md` | PR lifecycle |

### Platform - Cloudflare (`platform/cloudflare/`)
| Skill | Path | Purpose |
|-------|------|---------|
| agents-sdk | `platform/cloudflare/agents-sdk.md` | Build Cloudflare Agents |
| cloudflare | `platform/cloudflare/cloudflare.md` | Cloudflare platform |

### Migration (`migration/`)
| Skill | Path | Purpose |
|-------|------|---------|
| codebase-migrator | `migration/codebase-migrator.md` | Migrate legacy apps to modern platforms |

## Agent Consumption Pattern

```
1. Agent receives task → scans Quick-Scan Index above (alphabetical by trigger)
2. Finds matching trigger → identifies skill path
3. Loads ONLY that skill file:
   ===SKILL:task-workflow===
   [reads workflow/task-workflow.md]
   ===END SKILL===
4. Executes skill instructions
```

**DO NOT** load all skills. Load only what you need.
