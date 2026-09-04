---
name: message-queue-patterns
description: Message schema patterns — envelope pattern, event vs command, event sourcing, CQRS, message reliability patterns.
---

# Message Queue Analyzer — Patterns

## 7. Message Schema Patterns

### 7.1 Envelope Pattern

```markdown
## Standard Message Envelope

```json
{
  "id": "msg-12345678-1234-1234-1234-123456789012",
  "type": "order.created",
  "version": "1.0",
  "timestamp": "2026-05-02T12:00:00Z",
  "source": "order-service",
  "correlationId": "req-abc-123",
  "tenantId": "tenant-001",
  "data": {
    "orderId": "ord-123",
    "customerId": "cus-456",
    "total": 99.99,
    "currency": "USD"
  }
}
```

## Envelope Fields

| Field | Required | Description |
|-------|----------|-------------|
| id | Yes | Unique message ID |
| type | Yes | Event type (domain.event) |
| version | Yes | Schema version |
| timestamp | Yes | When event occurred |
| source | Yes | Originating service |
| correlationId | No | For tracing across services |
| tenantId | No | For multi-tenant systems |
| data | Yes | Actual payload |
```

### 7.2 Event vs Command Pattern

```markdown
## Events (Facts that Happened)

| Aspect | Description |
|--------|-------------|
| Naming | past-tense noun.verb: `order.created`, `payment.processed` |
| Immutability | Events are facts, never change |
| Audience | Multiple consumers may care |
| Behavior | Reactive - system reacts to events |

## Commands (Intent to Do Something)

| Aspect | Description |
|--------|-------------|
| Naming | imperative verb: `CreateOrder`, `ProcessPayment` |
| Authority | One specific consumer should handle |
| Response | Commands can expect reply/acknowledgment |
| Behavior | Direct - system tells another to do something |

## Event Sourcing

```markdown
## Event Sourcing Pattern

Traditional:
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Command   │─────►│    State    │◄────│   Snapshot  │
│   (write)   │      │  (current)  │      │  (optional) │
└─────────────┘      └─────────────┘      └─────────────┘

Event Sourcing:
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Command   │─────►│   Events    │─────►│    State    │
│             │      │  (append)   │      │  (derived)  │
└─────────────┘      └─────────────┘      └─────────────┘
                             │
                             ▼ (replay)
                      ┌─────────────┐
                      │   Replay    │
                      │  from start│
                      └─────────────┘
```

## CQRS (Command Query Responsibility Segregation)

```markdown
## CQRS Pattern

┌──────────────────┐              ┌──────────────────┐
│     Command       │              │      Query       │
│      Side         │              │      Side        │
│                   │              │                  │
│ ┌──────────────┐ │              │ ┌──────────────┐ │
│ │   Commands   │ │              │ │    Queries   │ │
│ │ CreateOrder  │ │              │ │ GetOrder     │ │
│ │ UpdateOrder  │ │─────────────►│ │ ListOrders   │ │
│ │ CancelOrder  │ │  Projections │ │ OrderStats   │ │
│ └──────────────┘ │              │ └──────────────┘ │
│        │         │              │        │         │
│        ▼         │              │        ▼         │
│ ┌──────────────┐ │              │ ┌──────────────┐ │
│ │    Events    │ │              │ │   Read       │ │
│ │  (ordered)   │ │              │ │   Models     │ │
│ └──────────────┘ │              │ └──────────────┘ │
│        │         │              │        │         │
│        ▼         │              │        │         │
│ ┌──────────────┐ │              │        │         │
│ │    Event     │ │              │        ▼         │
│ │    Store     │ │              │ ┌──────────────┐ │
│ └──────────────┘ │              │ │   Database   │ │
└──────────────────┘              │ │  (optimized) │ │
                                   │ └──────────────┘ │
                                   └──────────────────┘
```
