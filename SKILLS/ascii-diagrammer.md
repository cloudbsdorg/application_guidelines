# Skill: ascii-diagrammer

**Purpose:** Generate architecture diagrams using ASCII box-drawing characters following CloudBSD conventions.

**Triggers:** When writing architecture documents (200 series), creating component diagrams, or drawing state machines.

## Loading Instructions

Load this skill when the user asks you to:
- Create an architecture diagram
- Draw a state machine
- Illustrate component interactions
- Create a flow diagram

## Box-Drawing Character Set

```
Horizontal: - (or = for thick)
Vertical: |
Corners: + 
Arrows: > v < ^
```

## Component Diagram Template

```
+------------------+     +------------------+     +------------------+
|   Component A    |---->|   Component B    |---->|   Component C    |
|   [Description]  |     |   [Description]  |     |   [Description]  |
+------------------+     +------------------+     +------------------+
         |                        |                        |
         v                        v                        v
+------------------+     +------------------+     +------------------+
|   Component D    |<----|   Component E    |<----|   Component F    |
|   [Description]  |     |   [Description]  |     |   [Description]  |
+------------------+     +------------------+     +------------------+
```

## Data Flow Diagram

```
                    +------------------+
                    |   External Input  |
                    +------------------+
                            |
                            v
     +------------------+   |   +------------------+
     |   Validation     |──►│   │   Processing     │
     |   Layer          |   |   |   Pipeline       │
     +------------------+   |   +------------------+
                            |            |
                            |            v
                            |   +------------------+
                            │   |   Output         |
                            │   │   Handler        |
                            +------------------+
```

## State Machine Template

```
          +-----------+
          |   IDLE    |
          +-----------+
              |
              | start
              v
    +---------------------+
    |      ACTIVE         |
    |  (processing loop)  |
    +---------------------+
              |
              | stop / error
              v
    +---------------------+
    |      DRAINING       |
    |  (graceful shutdown)|
    +---------------------+
              |
              | complete
              v
          +-----------+
          |  REMOVED  |
          +-----------+
```

## Multi-State Machine with Transitions

```
         +------------+      +------------+      +------------+
         |   START    |----->|   ACTIVE   |----->|   STOPPED  |
         +------------+      +------------+      +------------+
               ^                  |                    |
               |                  v                    |
               |            +------------+            |
               +------------|  DRAINING  |<-----------+
                            +------------+
                                   |
                                   v
                            +------------+
                            |  REMOVED   |
                            +------------+
```

Legend:
- `start` / `stop` — commands
- `error` — error condition
- `complete` — graceful completion

## Layered Architecture

```
+=========================================================================+
|                         USER SPACE                                      |
|  +-------------+  +-------------+  +-------------+  +-------------+  |
|  |  CLI Tool   |  |  Config     |  |  Status     |  |  Logging    |  |
|  |  (ngctl)    |  |  Manager    |  |  Reporter   |  |  Agent      |  |
|  +-------------+  +-------------+  +-------------+  +-------------+  |
+=========================================================================+
                                   |
                    (sysctl / netgraph socket)
                                   |
                                   v
+=========================================================================+
|                         KERNEL SPACE                                    |
|  +-------------+  +-------------+  +-------------+  +-------------+  |
|  |   Graph     |  |   Worker    |  |   Session   |  |   Network   |  |
|  |   Node      |  |   Pool      |  |   Manager   |  |   Interface |  |
|  +-------------+  +-------------+  +-------------+  +-------------+  |
+=========================================================================+
                                   |
                                   v
+=========================================================================+
|                         DATA PLANE                                      |
|  +-------------+  +-------------+  +-------------+  +-------------+  |
|  |   Input     |  |   Load      |  |   Output    |  |   Stats     |  |
|  |   Handler   |  |   Balancer  |  |   Distributor| |   Collector | |
|  +-------------+  +-------------+  +-------------+  +-------------+  |
+=========================================================================+
```

## Network Topology

```
    +-------------+         +-------------+         +-------------+
    |   Router    |         |   Router    |         |   Router    |
    |   (WAN)     |         |   (WAN)     |         |   (WAN)     |
    +-------------+         +-------------+         +-------------+
          |                       |                       |
          |                       |                       |
          +-----------------------+-----------------------+
                                  |
                                  v
                        +-------------------+
                        |   Core Switch     |
                        +-------------------+
                                  |
              +-------------------+-------------------+
              |                   |                   |
              v                   v                   v
    +----------------+   +----------------+   +----------------+
    |   Server A     |   |   Server B     |   |   Server C     |
    |   (10.0.1.10)  |   |   (10.0.1.11)  |   |   (10.0.1.12)  |
    +----------------+   +----------------+   +----------------+
```

## Sequence Diagram

```
Agent                  .plan/                  GitHub
  |                       |                       |
  |  git pull --rebase    |                       |
  |----------------------->|                       |
  |                       |                       |
  |                       |  git fetch origin     |
  |                       |----------------------->|
  |                       |                       |
  |  merge conflicts?     |                       |
  |<----------------------|                       |
  |                       |                       |
  |  [resolve if needed]  |                       |
  |                       |                       |
  |  git add -A           |                       |
  |  git commit -m "..."   |                       |
  |----------------------->|                       |
  |                       |                       |
  |                       |  git push             |
  |                       |----------------------->|
```

## Component Symbols

| Symbol | Meaning |
|--------|---------|
| `--->` | Data flow |
| `---->` | Direct call |
| `<--->` | Bidirectional |
| `+---+` | Box border |
| `|   |` | Vertical bar |
| `***` | Separator |

## Validation Checklist

- [ ] All boxes use `+---+` corners
- [ ] Horizontal lines use `-` (or `=` for emphasis)
- [ ] Arrows point in direction of flow
- [ ] Labels are descriptive
- [ ] No overlapping lines
- [ ] Consistent spacing

## Reference

See Planning/PLANNING.md Section 8 (ASCII Diagram Conventions) for additional examples.