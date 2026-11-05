---
name: message-queue-rabbitmq
description: RabbitMQ analysis — exchanges, queues, bindings, routing keys, consumer patterns, dead letter queues.
---

# Message Queue Analyzer — RabbitMQ

## 2. RabbitMQ

### 2.1 Architecture

```markdown
## RabbitMQ Architecture

```
┌──────────────┐                    ┌───────────────────┐
│  Producer    │──Publish──────────►│                   │
│              │                    │    Exchange       │
└──────────────┘                    │  (router/director)│
                                    └─────────┬─────────┘
                                              │ Binding
                    ┌─────────────────────────┼─────────────────────────┐
                    │                         │                         │
                    ▼                         ▼                         ▼
            ┌───────────────┐         ┌───────────────┐         ┌───────────────┐
            │    Queue      │         │    Queue      │         │    Queue      │
            │  (orders)    │         │  (payments)   │         │  (emails)    │
            └───────┬───────┘         └───────┬───────┘         └───────┬───────┘
                    │                         │                         │
                    ▼                         ▼                         ▼
            ┌───────────────┐         ┌───────────────┐         ┌───────────────┐
            │   Consumer    │         │   Consumer    │         │   Consumer    │
            │  (order_svc) │         │  (payment_svc)│         │  (email_svc) │
            └───────────────┘         └───────────────┘         └───────────────┘
```

## Exchange Types

| Type | Routing Behavior | Use Case |
|------|------------------|----------|
| Direct | Exact match on routing key | Point-to-point |
| Fanout | Route to all bound queues | Broadcast |
| Topic | Pattern match (# = any, * = one) | Routing keys |
| Headers | Match on headers instead of key | Flexible routing |
```

### 2.2 RabbitMQ Message Flow

```markdown
## Message Publishing Flow

```
1. Producer → Exchange: Publish with routing_key="order.created"
2. Exchange: Lookup bindings matching "order.created"
3. Exchange → Queue: Route message to matching queues
4. Queue: Store message (if persistent, write to disk)
5. Consumer → Queue: Acknowledge receipt (auto or manual)
6. Queue → Consumer: Deliver message
```

## Message Properties

| Property | Description | Example |
|----------|-------------|---------|
| delivery_mode | 1=transient, 2=persistent | 2 |
| content_type | MIME type | application/json |
| message_id | Unique identifier | msg-123 |
| timestamp | When published | 1746192000 |
| headers | Custom headers | {x-source: "order"} |
| routing_key | Routing hint | order.created |
| priority | 0-9, higher first | 5 |
| expiration | TTL in ms | 60000 |
```

### 2.3 Queue Configuration

```markdown
## Queue Properties

| Property | Default | Description |
|----------|---------|-------------|
| durable | false | Survive broker restart |
| auto_delete | false | Delete when no consumers |
| exclusive | false | Single consumer only |
| max_length | unlimited | Max messages in queue |
| message_ttl | infinite | Time before expiration |
| dead_letter_exchange | none | Where to route dead messages |

## Dead Letter Queue Setup

```go
// Configure queue with dead letter exchange
args := amqp.Table{
    "x-dead-letter-exchange":    "dlx.exchange",
    "x-dead-letter-routing-key": "dlq.orders",
}

// DLX Exchange → DLQ Queue flow
// Failed message → Original queue TTL/reject → DLX Exchange → DLQ Queue
```
```

### 2.4 Consumer Patterns

```markdown
## Consumer Patterns

### Simple Consumer
```go
msgs, err := ch.Consume(
    "orders",           // queue
    "",                 // consumer tag
    false,              // auto-ack
    false,              // exclusive
    false,              // no-local
    false,              // no-wait
    nil,                // args
)

for msg := range msgs {
    order := Order{}
    json.Unmarshal(msg.Body, &order)
    processOrder(order)
    msg.Ack(false)  // Manual ack
}
```

### Competing Consumers
```
Queue: orders
        ├──► Consumer A (receives messages 1, 3, 5...)
        ├──► Consumer B (receives messages 2, 4, 6...)
        └──► Consumer C (receives messages 1, 4, 7...)

Round-robin distribution, each message goes to ONE consumer
```

### Work Queues
```go
// Multiple workers processing jobs
for i := 0; i < workers; i++ {
    go func() {
        for msg := range msgs {
            job := Job{}
            json.Unmarshal(msg.Body, &job)
            processJob(job)
            msg.Ack(false)
        }
    }()
}
```
```

### 2.5 RabbitMQ Discovery Template

```markdown
## RabbitMQ Analysis

### Exchanges
| Name | Type | Durable | Bindings |
|------|------|---------|----------|
| orders.exchange | topic | yes | orders.queue (routing: order.*) |
| payments.exchange | direct | yes | payments.queue |
| notifications.exchange | fanout | yes | email.queue, sms.queue, push.queue |

### Queues
| Queue | Durable | Auto-Delete | TTL | DLX |
|-------|---------|-------------|-----|-----|
| orders.queue | yes | no | - | orders.dlx |
| payments.queue | yes | no | - | payments.dlx |
| email.queue | yes | no | 86400000 | - |
| notifications.queue | yes | yes | - | - |

### Routing Keys
| Key | Pattern | Queues |
|-----|---------|--------|
| order.created | exact | orders.queue |
| order.updated | exact | orders.queue |
| order.cancelled | exact | orders.queue |
| payment.succeeded | exact | payments.queue |
| payment.failed | exact | payments.queue |

### Message Flow
```
Producer → orders.exchange (topic)
                │
                ├─► order.created → orders.queue → OrderService
                ├─► order.updated → orders.queue → OrderService
                └─► order.cancelled → orders.queue → OrderService
```
```
