---
name: message-queue-nats
description: NATS analysis — core pub/sub, request/reply, JetStream persistence, subject wildcards, NATS vs other brokers.
---

# Message Queue Analyzer — NATS

## 6. NATS

### 6.1 NATS Architecture

```markdown
## NATS vs Other Brokers

| Feature | NATS | RabbitMQ | Kafka |
|---------|------|----------|-------|
| Delivery | At-most-once or at-least-once | At-least-once | At-least-once |
| Persistence | Optional (NATS JetStream) | Optional | Always |
| Protocol | TEXT (simple) | AMQP | Binary |
| Learning curve | Low | Medium | High |
| Performance | Very high | Medium | Very high |
| Cloud native | Yes | No | Yes |
| Streaming | JetStream | N/A | N/A |

## NATS Core (Pub/Sub Only)

```
┌─────────────┐                    ┌─────────────┐
│  Publisher  │───────────────────►│   NATS      │
└─────────────┘                    │   Server    │
                                   │  (nats-server)│
┌─────────────┐                    │             │
│  Subscriber │◄──────────────────│             │
└─────────────┘                    └─────────────┘
                                   │             │
┌─────────────┐                    │             │
│  Subscriber │◄──────────────────│             │
└─────────────┘                    └─────────────┘
```

## NATS Request/Reply

```
┌─────────────┐                    ┌─────────────┐
│  Requester  │────request────────►│   NATS      │◄───request─────┐
└─────────────┘                    │   Server    │                │
                                   └─────────────┘                │
                    ┌───────────────────────────────────────────┘
                    │
                    ▼
            ┌─────────────┐
            │  Responder  │
            │  (service)  │
            └─────────────┘
                    │
                    ▼
            ┌─────────────┐
            │   Reply     │────response─────────────────────────┐
            └─────────────┘                                    │
                                                               │
            ┌─────────────┐                                    │
            │  Requester  │◄───response────────────────────────┘
            └─────────────┘
```

## NATS Subjects vs Topics

```markdown
| Concept | NATS | Kafka | RabbitMQ |
|---------|------|-------|----------|
| Channel name | Subject | Topic | Exchange + Routing Key |
| Hierarchy | dot-separated | flat | flat or wildcard |
| Wildcards | `*` (single), `>` (multi) | N/A | N/A |
| Pattern | `orders.created`, `orders.*` | `orders` | `orders.created` |

## Subject Examples

```go
// Subject naming
"orders"                    // All order messages
"orders.created"            // Order creation events
"orders.created.us-east"    // US East order creations
"orders.>"                  // All orders (recursive wildcard)
"orders.*"                  // Any single level (created, updated, cancelled)
```
```

### 6.2 NATS JetStream (Streaming)

```markdown
## JetStream vs Core NATS

| Feature | Core NATS | JetStream |
|---------|-----------|----------|
| At-most-once | Yes | Yes |
| At-least-once | No | Yes |
| Message persistence | No | Yes |
| Message replay | No | Yes (by sequence/time) |
| Consumer groups | No | Yes |
| Key-value store | No | Yes |
| Object store | No | Yes |

## JetStream Consumer

```go
// JetStream consumer with at-least-once
js, _ := nc.JetStream()

// Pull-based consumer
sub, _ := js.PullSubscribe("orders.>", "order-processor")
sub.Consume(func(msg *nats.Msg) {
    order := Order{}
    json.Unmarshal(msg.Data, &order)
    processOrder(order)
    msg.Ack()  // Acknowledge
})
```
