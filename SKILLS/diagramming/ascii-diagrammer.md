# Skill: ascii-diagrammer (Mermaid)

**Purpose:** Generate architecture diagrams using Mermaid following CloudBSD conventions. Mermaid is the preferred drawing methodology for all CloudBSD documentation.

**Triggers:** When writing architecture documents (200 series), creating component diagrams, or drawing state machines.

## Loading Instructions

Load this skill when the user asks you to:
- Create an architecture diagram
- Draw a state machine
- Illustrate component interactions
- Create a flow diagram
- Generate any technical diagram (use Mermaid)

## Mermaid Diagram Types

### Flowchart (Graph)
```mermaid
graph TD
    A[Component A] --> B[Component B]
    B --> C[Component C]
    A --> C
```

### State Diagram
```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Active: start
    Active --> Draining: stop / error
    Draining --> Removed: complete
    Removed --> [*]
```

### Sequence Diagram
```mermaid
sequenceDiagram
    participant Agent
    participant Plan as .plan/
    participant GitHub
    Agent->>Plan: git pull --rebase
    Plan->>GitHub: git fetch origin
    GitHub-->>Plan: return
    Agent->>Plan: merge conflicts?
    Note right of Agent: Resolve if needed
    Agent->>Plan: git add -A && git commit
    Plan->>GitHub: git push
```

### Class Diagram
```mermaid
classDiagram
    class ComponentA {
        +description: string
        +start()
        +stop()
    }
    class ComponentB {
        +process(data)
    }
    ComponentA --> ComponentB: uses
```

### ER Diagram (Entity Relationship)
```mermaid
erDiagram
    USERS ||--o{ ORDERS : places
    USERS {
        int id PK
        string email
        string password_hash
    }
    ORDERS ||--|{ ORDER_ITEMS : contains
    ORDERS {
        int id PK
        int user_id FK
        datetime created_at
    }
```

## Diagram Templates

### Component Diagram Template
```mermaid
graph TD
    A[Component A<br/>Description] --> B[Component B<br/>Description]
    B --> C[Component C<br/>Description]
    A --> C
    style A fill:#e1f5fe
    style B fill:#fce4ec
    style C fill:#d4edda
```

### Data Flow Diagram
```mermaid
flowchart LR
    Input[External Input] --> Validation[Validation Layer]
    Validation --> Processing[Processing Pipeline]
    Processing --> Output[Output Handler]
    Output --> Logging[Logging]
```

### Layered Architecture
```mermaid
graph TD
    subgraph UserSpace["User Space"]
        CLI[CLI Tool<br/>ngctl]
        Config[Config Manager]
        Status[Status Reporter]
        Log[Logging Agent]
    end
    subgraph KernelSpace["Kernel Space"]
        Graph[Graph Node]
        Worker[Worker Pool]
        Session[Session Manager]
        Net[Network Interface]
    end
    subgraph DataPlane["Data Plane"]
        Input[Input Handler]
        LB[Load Balancer]
        Output[Output Distributor]
        Stats[Stats Collector]
    end
    UserSpace -->|sysctl / netgraph socket| KernelSpace
    KernelSpace --> DataPlane
```

### Network Topology
```mermaid
graph TD
    Router1[Router<br/>WAN] --- Router2[Router<br/>WAN] --- Router3[Router<br/>WAN]
    Router1 --- CoreSwitch[Core Switch]
    CoreSwitch --- ServerA[Server A<br/>10.0.1.10]
    CoreSwitch --- ServerB[Server B<br/>10.0.1.11]
    CoreSwitch --- ServerC[Server C<br/>10.0.1.12]
```

### Test Pyramid
```mermaid
graph TD
    S[Stress Testing] --> I[Integration Testing]
    I --> U[Unit Testing<br/>per component]
    style S fill:#ff9999
    style I fill:#ffcc99
    style U fill:#99ff99
```

## Conversion from ASCII

When you encounter ASCII art diagrams (e.g., `+---+`, `|   |`), convert them to Mermaid syntax.

**Example ASCII to Mermaid:**

ASCII:
```
+------------------+     +------------------+
|   Component A    |---->|   Component B    |
+------------------+     +------------------+
```

Mermaid:
```mermaid
graph LR
    A[Component A] --> B[Component B]
```

## Validation Checklist

- [ ] Diagram uses valid Mermaid syntax (test at https://mermaid.live)
- [ ] Nodes have descriptive labels (use `<br/>` for line breaks)
- [ ] Arrows indicate direction of flow or dependency (`-->`, `-.->`, `-->>`)
- [ ] Consistent styling (optional `style` directives)
- [ ] No overlapping lines (Mermaid handles layout automatically)
- [ ] Diagram is wrapped in ` ```mermaid ` code block

## Mermaid Syntax Cheat Sheet

| Syntax | Meaning |
|---------|---------|
| `graph TD` | Top-down graph |
| `graph LR` | Left-right graph |
| `A[Label]` | Node with text |
| `A-->B` | Arrow connection |
| `A---B` | Line without arrow |
| `A-.->B` | Dotted arrow |
| `style A fill:#color` | Node styling |
| `subgraph Name["Label"]` | Group nodes |

## Reference

- [Mermaid Official Docs](https://mermaid.js.org/)
- [Mermaid Live Editor](https://mermaid.live/)
- CloudBSD Planning/PLANNING.md Section 8 (Diagram Conventions)
