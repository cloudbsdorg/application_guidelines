---
name: message queue analyzer
description: Systematically analyze message brokers, queues, and event-driven architectures to understand message flow, patterns, and integration points.
---

# Skill: message-queue-analyzer

**Purpose:** Systematically analyze message brokers, queues, and event-driven architectures to understand message flow, patterns, and integration points.

**Triggers:** When analyzing a system with message queues, event brokers, or async communication patterns.

## Loading Instructions

Load this skill when the user asks you to:
- Analyze message queue systems
- Document broker architectures
- Understand pub/sub patterns
- Map message flows
- Plan queue integration
- Analyze MQTT, RabbitMQ, Kafka, or similar

---

## 1. Message Broker Overview

### 1.1 Broker Types

```markdown
## Message Broker Comparison

| Broker | Type | Best For | Throughput | Persistence |
|--------|------|----------|------------|--------------|
| RabbitMQ | Traditional | Task queues, Work distribution | Medium | Optional |
| Apache Kafka | Log-based | Event streaming, Audit logs | Very High | Always |
| MQTT Broker | Lightweight | IoT, Sensor data | Medium | Optional |
| Redis Pub/Sub | In-memory | Simple pub/sub, Cache invalidation | High | None |
| Amazon SQS | Cloud queue | Fully managed, Decoupling | High | Yes |
| Amazon SNS | Pub/Sub | Fan-out, Push notifications | High | Optional |
| Google Pub/Sub | Cloud | GCP integration, Enterprise | High | Yes |
| NATS | Lightweight | Cloud native, Simple | Very High | Optional |

### 1.2 Core Concepts

```markdown
## Core Terminology

| Term | Definition |
|------|------------|
| Producer | Sends messages (also: Publisher) |
| Consumer | Receives messages (also: Subscriber) |
| Message | Data payload sent through broker |
| Topic | Channel for routing messages (Kafka, MQTT) |
| Queue | Point-to-point message storage (RabbitMQ, SQS) |
| Exchange | Router in RabbitMQ that routes to queues |
| Binding | Connection between exchange and queue |
| Partition | Kafka's data distribution unit |
| Offset | Kafka's message position in partition |
| Consumer Group | Set of consumers sharing workload |
| Dead Letter Queue | Failed messages for later analysis |
| Message Broker | Central server managing queues |
```
```

---

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

---

## 3. Apache Kafka

### 3.1 Architecture

```markdown
## Kafka Architecture

```
┌──────────────┐                    ┌─────────────────────────────────────┐
│  Producer    │───Produce────────►│           Kafka Cluster              │
│              │                    │                                     │
└──────────────┘                    │  ┌─────────┐  ┌─────────┐  ┌───────┐│
                                    │  │Broker 1│  │Broker 2│  │Broker ││
┌──────────────┐                    │  │         │  │         │  │   N   ││
│  Consumer    │◄──Consume────────│  └────┬────┘  └────┬────┘  └───┬───┘│
│  Group A     │                    │       │            │            │    │
└──────────────┘                    │       ▼            ▼            ▼    │
                                    │  ┌─────────┐  ┌─────────┐  ┌────────┐│
                                    │  │Topic A │  │Topic A │  │Topic A ││
┌──────────────┐                    │  │Part 0  │  │Part 1  │  │Part 2  ││
│  Consumer    │◄──Consume────────│  │Offset  │  │Offset  │  │Offset  ││
│  Group B     │                    │  │  0-99  │  │ 0-199  │  │ 0-149  ││
└──────────────┘                    │  └─────────┘  └─────────┘  └────────┘│
                                    └─────────────────────────────────────┘
```

## Topic and Partition

```markdown
## Topic Structure

Topic: "orders"
├── Partition 0 (Leader: Broker 1)
│   ├── Offset 0: {id: 1, customer: "Alice", total: 100}
│   ├── Offset 1: {id: 2, customer: "Bob", total: 200}
│   └── Offset 2: {id: 3, customer: "Carol", total: 150}
├── Partition 1 (Leader: Broker 2)
│   ├── Offset 0: {id: 4, customer: "Dave", total: 300}
│   └── Offset 1: {id: 5, customer: "Eve", total: 400}
└── Partition 2 (Leader: Broker N)
    ├── Offset 0: {id: 6, customer: "Frank", total: 250}
    └── Offset 1: {id: 7, customer: "Grace", total: 350}

## Partition Assignment

| Consumer | Partitions Assigned |
|----------|---------------------|
| Consumer A | Partition 0 |
| Consumer B | Partition 1, Partition 2 |

Each partition can have different offsets per consumer group.
```
```

### 3.2 Kafka Message Structure

```markdown
## Kafka Message Anatomy

```
┌─────────────────────────────────────────────────────────────────┐
│                        Record                                   │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ Key (optional) - determines partition                    │  │
│  │ Bytes: []byte{1, 2, 3} or null                          │  │
│  └─────────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ Value - the actual payload                              │  │
│  │ Bytes: {"order_id": "123", "total": 99.99}             │  │
│  └─────────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ Headers - metadata key-value pairs                      │  │
│  │ correlation-id: "req-123"                               │  │
│  │ content-type: "application/json"                        │  │
│  └─────────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ Timestamp - when produced or consumed                    │  │
│  │ 1746192000000 (milliseconds since epoch)                │  │
│  └─────────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ Offset - position in partition                          │  │
│  │ 42                                                     │  │
│  └─────────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ Partition - which partition this went to                │  │
│  │ 0                                                       │  │
│  └─────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Record Batch (Wire Format)

```markdown
## Batch Structure

```
┌─ Record Batch ─────────────────────────────────────────────────┐
│  BaseOffset: int64 (relative to topic partition)               │
│  BatchLength: int32                                            │
│  PartitionLeaderEpoch: int32                                   │
│  Magic: int8 (current is 2)                                    │
│  CRC: int32                                                    │
│  Attributes: int16 (compression, timestamp type, etc.)          │
│  LastOffsetDelta: int32                                        │
│  FirstTimestamp: int64                                         │
│  MaxTimestamp: int64                                            │
│  ProducerId: int64                                             │
│  ProducerEpoch: int16                                          │
│  BaseSequence: int32                                           │
│  Records: [Record] × N                                         │
└─────────────────────────────────────────────────────────────────┘
```
```

### 3.3 Consumer Groups

```markdown
## Consumer Group Behavior

```
Kafka Topic: "orders" (3 partitions)

Consumer Group A (3 consumers):
┌────────────────────────────────────────────────────────────┐
│  Consumer A ──────► Partition 0 (offsets 0-100)            │
│  Consumer B ──────► Partition 1 (offsets 0-200)            │
│  Consumer C ──────► Partition 2 (offsets 0-150)            │
└────────────────────────────────────────────────────────────┘

Consumer Group B (2 consumers):
┌────────────────────────────────────────────────────────────┐
│  Consumer D ──────► Partition 0 + Partition 1              │
│  Consumer E ──────► Partition 2                           │
└────────────────────────────────────────────────────────────┘

Consumer Group C (4 consumers):
┌────────────────────────────────────────────────────────────┐
│  Consumer F ──────► Partition 0 (some offsets)            │
│  Consumer G ──────► Partition 0 (other offsets)            │
│  Consumer H ──────► Partition 1 (some offsets)            │
│  Consumer I ──────► Partition 1 (other offsets)           │
└────────────────────────────────────────────────────────────┘
```

## Consumer Group States

| State | Meaning |
|-------|---------|
| PreparingRebalance | Group is forming, members joining |
| AwashingSync | Members negotiating partition assignment |
| Stable | Normal operation, assignments stable |
| Dead | All members left, offsets deleted |
| Empty | Active members but no assignments |
```

### 3.4 Producer Patterns

```markdown
## Producer Configuration

```go
producer := &kafka.Producer{
    // Delivery guarantees
    Acks: 1,  // 0=none, 1=leader, -1=all in-sync replicas

    // Retries
    Retry: &kafka.RetryConfig{
        MaxRetries: 3,
        Backoff:    time.Millisecond * 100,
    },

    // Compression
    Compression: kafka.CompressionSnappy,  // snappy, gzip, lz4, zstd

    // Batching
    BatchSize: 16384,  // bytes per batch
    Linger:    time.Millisecond * 5,  // wait to batch
}
```

## Idempotent Producer

```go
// Exactly-once semantics (Kafka 0.11+)
producer := &kafka.Producer{
    EnableIdempotence: true,  // ensures exactly-once delivery
    Acks: -1,                 // must be -1 for idempotence
    MaxInFlightRequests: 5,   // must be <= 5 for idempotence
}
```
```

### 3.5 Kafka Discovery Template

```markdown
## Kafka Analysis

### Topics
| Topic | Partitions | Replication | Retention | Cleanup Policy |
|-------|------------|-------------|-----------|----------------|
| orders | 6 | 3 | 7 days | delete |
| payments | 6 | 3 | 30 days | delete |
| audit-log | 12 | 3 | 90 days | delete |
| user-events | 3 | 3 | 1 hour | delete |

### Producers
| Producer | Topics | Key | Compression | Acks |
|----------|--------|-----|-------------|------|
| order-service | orders | order_id | snappy | 1 |
| payment-service | payments | order_id | lz4 | -1 |
| analytics | audit-log | user_id | gzip | 0 |

### Consumer Groups
| Group | Topics | Lag | Members |
|-------|--------|-----|---------|
| order-processing | orders | 150 | 3 |
| fraud-detection | orders, payments | 0 | 2 |
| analytics-pipeline | audit-log | 2000 | 5 |
| notifications | orders, payments | 50 | 1 |

### Message Schemas (Avro/Schema Registry)
| Topic | Key Schema | Value Schema |
|-------|------------|--------------|
| orders | `{"type": "string"}` | OrderRecord |
| payments | `{"type": "string"}` | PaymentRecord |
```

---

## 4. MQTT (Message Queuing Telemetry Transport)

### 4.1 Architecture

```markdown
## MQTT Architecture

```
┌─────────────┐                    ┌─────────────────┐                    ┌─────────────┐
│   MQTT     │                    │                 │                    │   MQTT      │
│  Publisher  │───────────────────►│   MQTT Broker   │◄───────────────────│  Subscriber │
│  (Sensor)   │   PUBLISH         │                 │   SUBSCRIBE       │  (Dashboard)│
└─────────────┘                    │                 │                    └─────────────┘
                                   │  mosquitto /    │
┌─────────────┐                    │  HiveMQ /       │                    ┌─────────────┐
│   MQTT     │────────────────────►│  EMQX /         │◄──────────────────│   MQTT      │
│  Publisher │   PUBLISH          │  AWS IoT Core   │   SUBSCRIBE       │  Subscriber │
│  (Actuator)│                    │                 │                    │  (Alert)    │
└─────────────┘                    └─────────────────┘                    └─────────────┘
```

## MQTT vs REST

| Aspect | MQTT | REST |
|--------|------|------|
| Protocol | TCP/IP (binary) | HTTP |
| Connection | Persistent | Request-response |
| Payload | Binary (small) | JSON (larger) |
| QoS | 0, 1, 2 | N/A |
| Keep-alive | Yes (heartbeat) | No |
| Use case | IoT, sensors | Web APIs |
| Battery | Efficient | Less efficient |
```

### 4.2 MQTT Quality of Service

```markdown
## QoS Levels

### QoS 0: At Most Once (Fire and Forget)
```
Publisher ──────► Broker ──────► Subscriber
                      │
                      └── (no acknowledgment)
```

- **Use**: High throughput, tolerates loss (weather sensors)
- **Guarantee**: Message may be lost, never duplicated

### QoS 1: At Least Once (Acknowledged)
```
Publisher ──────► Broker ──────► Subscriber
    ▲                      │
    │                      │
    └─────── PUBACK ──────┘
```

- **Use**: Every message must arrive (commands)
- **Guarantee**: Message always arrives, may be duplicated

### QoS 2: Exactly Once (Handshake)
```
Publisher ──────► Broker ──────► Subscriber
    ▲                      │
    │ PUBREC               │
    │◄──────              │
    │                      │
    │ PUBREL               │
    │──────►               │
    ▲                      │
    │ PUBCOMP              │
    │◄──────              │
    ▼                      │
```

- **Use**: Critical commands (alarm systems)
- **Guarantee**: Message arrives exactly once
- **Cost**: Higher latency, more overhead

## QoS Selection Guide

| Scenario | QoS | Rationale |
|----------|-----|----------|
| Temperature sensor | 0 | Occasional loss acceptable |
| Door unlock command | 2 | Must not duplicate |
| Periodic status | 1 | Should arrive, duplicates OK |
| Fire alarm | 2 | Critical, must not duplicate |
```

### 4.3 MQTT Topic Structure

```markdown
## Topic Naming Convention

```
┌─────────────────────────────────────────────────────────────┐
│  Topic Hierarchy (slash-separated)                          │
│                                                              │
│  building/floor/room/sensor                                 │
│                                                              │
│  Examples:                                                   │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ home/living-room/temperature    → 22.5°C              │ │
│  │ home/living-room/humidity       → 45%                 │ │
│  │ home/bedroom/temperature        → 21.0°C             │ │
│  │ home/garage/motion              → true                │ │
│  │ home/garage/door                → open                │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Wildcards

| Wildcard | Meaning | Example |
|----------|---------|---------|
| `#` | Multi-level (end only) | `home/#` matches all home/* |
| `+` | Single level | `home/+/temperature` matches all room temps |

```markdown
## Topic Examples with Wildcards

| Subscription | Matches | Doesn't Match |
|--------------|---------|---------------|
| `home/#` | home/living-room/temp, home/garage/door | building/lobby |
| `home/+/temperature` | home/living-room/temp, home/bedroom/temp | home/living-room/humidity |
| `building/+/room/#` | building/floor1/room/temp | building/floor1/hallway |
```

### 4.4 MQTT Message Format

```markdown
## MQTT Packet Structure

### CONNECT Packet
```
┌────────────────────────────────────────────────────────────┐
│ Fixed Header (2-5 bytes)                                    │
│   Byte 1: Packet type (0x10)                               │
│   Byte 2+: Remaining length                                │
├────────────────────────────────────────────────────────────┤
│ Variable Header                                            │
│   Protocol Name: "MQTT"                                    │
│   Protocol Level: 4 (MQTT 3.1.1) or 5 (MQTT 5.0)         │
│   Connect Flags: clean session, will, password, user        │
│   Keep Alive: 60-65535 seconds                             │
├────────────────────────────────────────────────────────────┤
│ Payload                                                    │
│   Client ID: Unique identifier                             │
│   Will Topic (if will flag set)                           │
│   Will Payload (if will flag set)                         │
│   Username (if user flag set)                             │
│   Password (if password flag set)                         │
└────────────────────────────────────────────────────────────┘
```

### CONNECT Packet Example

```go
// MQTT CONNECT to broker
conn, err := mqtt.Dial("tcp://broker.example.com:1883")
if err != nil {
    log.Fatal(err)
}

opts := mqtt.NewClientOptions().
    SetClientID("sensor-living-room-001").
    SetUsername("sensor").
    SetPassword("secret123").
    SetKeepAlive(30 * time.Second).
    SetCleanSession(false)  // false = persistent session

client := mqtt.NewClient(opts)
if token := client.Connect(); token.Wait() && token.Error() != nil {
    log.Fatal(token.Error())
}
```

### PUBLISH Packet

```go
// Publish temperature reading
temp := 22.5
payload, _ := json.Marshal(map[string]float64{"temperature": temp})

token := client.Publish(
    "home/living-room/temperature",  // topic
    1,                               // QoS 1
    false,                           // retained
    payload,                         // message
)
token.Wait()
```

### SUBSCRIBE Packet

```go
// Subscribe to topics
topics := []mqtt.TopicHandler{
    {"home/+/temperature", qos0Handler},
    {"home/garage/#", qos1Handler},
    {"alerts/#", qos2Handler},
}

token := client.SubscribeMultiple(topics, func(c mqtt.Client, msg mqtt.Message) {
    fmt.Printf("Topic: %s, Payload: %s\n", msg.Topic(), msg.Payload())
})
token.Wait()
```

### 4.5 MQTT Discovery Template

```markdown
## MQTT Analysis

### Broker Configuration
| Setting | Value | Notes |
|---------|-------|-------|
| Broker | Mosquitto 2.x | Docker container |
| Port | 1883 (unencrypted), 8883 (TLS) | |
| WebSocket | 9001 | For web clients |
| Auth | Username/Password | |

### Topics
| Topic | QoS | Retained | Payload | Publisher |
|-------|-----|----------|---------|-----------|
| home/living-room/temperature | 0 | yes | `{"value": 22.5, "unit": "c"}` | temp_sensor_01 |
| home/living-room/humidity | 0 | yes | `{"value": 45, "unit": "%"}` | hum_sensor_01 |
| home/garage/door | 1 | yes | `{"state": "open"|"closed"}` | door_sensor_01 |
| home/garage/motion | 0 | no | `{"detected": true, "ts": 1746192000}` | motion_sensor_01 |
| alerts/security | 2 | no | `{"type": "motion", "location": "garage"}` | alert_service |
| commands/home/lights | 2 | no | `{"device": "light_01", "action": "on"|"off"}` | home_controller |

### Subscribers
| Client | ID | Subscriptions | Purpose |
|--------|-----|---------------|---------|
| dashboard | dash-001 | home/# | Display all home sensor data |
| alert_service | alert-001 | alerts/# | Process and forward alerts |
| history_logger | hist-001 | home/living-room/# | Store temperature history |

### Last Will and Testament
| Setting | Value |
|---------|-------|
| Will Topic | home/sensors/{client_id}/status |
| Will Payload | `{"status": "offline", "ts": 1746192000}` |
| Will QoS | 1 |
| Will Retained | true |
| Trigger | Clean disconnect only |

## Message Examples

### Temperature Reading
```json
// Topic: home/living-room/temperature
// QoS: 0
// Retained: true
{
  "value": 22.5,
  "unit": "celsius",
  "timestamp": 1746192000
}
```

### Door Sensor
```json
// Topic: home/garage/door
// QoS: 1
// Retained: true
{
  "state": "open",
  "battery": 85,
  "timestamp": 1746192000
}
```

### Alert
```json
// Topic: alerts/security
// QoS: 2
// Retained: false
{
  "type": "intrusion",
  "location": "garage",
  "sensor": "motion_sensor_01",
  "confidence": 0.95,
  "timestamp": 1746192000
}
```
```

---

## 5. Amazon SQS & SNS

### 5.1 SQS (Simple Queue Service)

```markdown
## SQS Queue Types

| Type | Description | Use Case |
|------|-------------|----------|
| Standard | Best-effort ordering, at-least-once | High throughput, order not critical |
| FIFO | Exactly-once processing, preserved order | Order critical (orders, transactions) |

## SQS Message Flow

```
┌──────────────┐                    ┌────────────────┐                    ┌──────────────┐
│  Producer    │───SendMessage────►│                │                    │  Consumer    │
│              │                    │   SQS Queue    │◄──ReceiveMessage──│              │
└──────────────┘                    │  (messages     │                    └──────┬───────┘
                                   │   stored       │                           │
                                   │   up to 14 days)│                           │
                                   │                │◄────DeleteMessage───────┘
                                   └────────────────┘
```

## SQS Configuration

```go
// Create queue
sqs.CreateQueue(&sqs.CreateQueueInput{
    QueueName: aws.String("orders-queue"),
    Attributes: map[string]*string{
        "FifoQueue":                    aws.String("true"),           // FIFO queue
        "ContentBasedDeduplication":    aws.String("true"),           // Auto dedup
        "VisibilityTimeout":           aws.String("30"),             // 30 seconds
        "ReceiveMessageWaitTimeSeconds": aws.String("20"),           // Long polling
        "MessageRetentionPeriod":       aws.String("1209600"),        // 14 days
    },
})

// Send message
sqs.SendMessage(&sqs.SendMessageInput{
    QueueUrl:    aws.String(queueURL),
    MessageBody: aws.String(`{"order_id": "123", "total": 99.99}`),
    MessageDeduplicationId: aws.String("order-123"),  // FIFO only
    MessageGroupId: aws.String("orders"),              // FIFO only
})

// Receive messages
result, _ := sqs.ReceiveMessage(&sqs.ReceiveMessageInput{
    QueueUrl:            aws.String(queueURL),
    MaxNumberOfMessages: aws.Int64(10),
    WaitTimeSeconds:     aws.Int64(20),  // Long polling
})

for _, msg := range result.Messages {
    processMessage(msg)
    sqs.DeleteMessage(&sqs.DeleteMessageInput{
        QueueUrl:      aws.String(queueURL),
        ReceiptHandle: msg.ReceiptHandle,
    })
}
```
```

### 5.2 SNS (Simple Notification Service)

```markdown
## SNS Architecture

```
┌──────────────┐
│   Publisher  │───Publish────────────►┌─────────────────┐
└──────────────┘                       │                 │
                                      │   SNS Topic     │
                                      │                 │
                                      │  (fan-out)      │
                                      └────────┬────────┘
                                               │
                    ┌──────────────────────────┼──────────────────────────┐
                    │                          │                          │
                    ▼                          ▼                          ▼
            ┌───────────────┐          ┌───────────────┐          ┌───────────────┐
            │   SQS Queue   │          │    Email     │          │    SMS       │
            │ (order_svc)  │          │ (admin@...) │          │ (+1234567890)│
            └───────────────┘          └───────────────┘          └───────────────┘
                    │
                    ▼
            ┌───────────────┐
            │   Lambda      │
            │ (notification)│
            └───────────────┘
```

## SNS Message Format

```go
// Publish to SNS
sns.Publish(&sns.PublishInput{
    TopicArn: aws.String("arn:aws:sns:us-east-1:123456:orders"),
    Message: aws.String(`{
        "order_id": "123",
        "customer": "Alice",
        "total": 99.99,
        "status": "created"
    }`),
    MessageStructure: aws.String("json"),  // For different protocols
    Attributes: map[string]*sns.MessageAttributeValue{
        "priority": {
            DataType:    aws.String("String"),
            StringValue: aws.String("high"),
        },
    },
})
```

### 5.3 SNS + SQS Fan-Out Pattern

```markdown
## Fan-Out Architecture

```
Publisher → SNS Topic ─────────────────────────────────────────► SQS Queue A
                        ──────────────────────────────────────► Lambda 1
                        ──────────────────────────────────────► SQS Queue B
                        ──────────────────────────────────────► Lambda 2
                        ──────────────────────────────────────► Email
                        ──────────────────────────────────────► SMS
                        ──────────────────────────────────────► Webhook
```

## Benefits
- **Decoupling**: Publishers don't know subscribers
- **Reliability**: SQS queues persist messages
- **Scalability**: Each subscriber scales independently
- **Flexibility**: Easy to add/remove subscribers
```

---

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
```

---

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
│ │    Event     │ │              │        │         │
│ │    Store     │ │              │        ▼         │
│ └──────────────┘ │              │ ┌──────────────┐ │
└──────────────────┘              │ │   Database   │ │
                                  │ │  (optimized) │ │
                                  │ └──────────────┘ │
                                  └──────────────────┘
```
```

---

## 8. Integration Planning

### 8.1 Queue Integration Checklist

```markdown
## Pre-Integration Checklist

### Producer Side
- [ ] Message schema defined (JSON, Avro, Protobuf)
- [ ] Topic/Queue naming convention established
- [ ] Message envelope format standardized
- [ ] Serialization (JSON, binary) chosen
- [ ] Compression configured (if needed)
- [ ] Error handling for failed publishes
- [ ] Retry/backoff strategy defined

### Consumer Side
- [ ] Consumer group ID defined
- [ ] Acknowledgment strategy (auto vs manual)
- [ ] Error handling for failed processing
- [ ] Dead letter queue configured
- [ ] Idempotency implemented (prevent duplicates)
- [ ] Concurrency/parallelism configured
- [ ] Ordering guarantees understood

### Infrastructure
- [ ] Broker/cluster setup complete
- [ ] Authentication configured
- [ ] TLS/encryption enabled
- [ ] Monitoring/alerting set up
- [ ] Retention policies configured
- [ ] Backup/disaster recovery planned
```

### 8.2 Message Processing Task

```markdown
## Task: Implement Order Event Processor

**Type:** Message Queue Integration
**Priority:** P1
**Broker:** RabbitMQ

### Configuration
| Setting | Value |
|---------|-------|
| Exchange | orders.events (topic) |
| Queue | order-processor.queue |
| Routing Keys | order.created, order.updated, order.cancelled |
| Prefetch | 10 |
| Auto-Ack | false |

### Message Format
```json
{
  "id": "msg-123",
  "type": "order.created",
  "version": "1.0",
  "timestamp": "2026-05-02T12:00:00Z",
  "data": {
    "orderId": "ord-123",
    "customerId": "cus-456",
    "total": 99.99
  }
}
```

### Processing Logic
1. Parse message JSON
2. Validate schema version
3. Check idempotency (skip if already processed)
4. Process based on event type:
   - `order.created`: Create order record, send notification
   - `order.updated`: Update order record, notify if status changed
   - `order.cancelled`: Mark order cancelled, trigger refund
5. Acknowledge message

### Error Handling
| Error | Action |
|-------|--------|
| Invalid JSON | Log error, reject (no requeue) |
| Schema version unknown | Log warning, acknowledge |
| Processing error | Requeue with delay (max 3 retries) |
| Permanent failure | Send to DLQ, acknowledge |

### Acceptance Criteria
- [ ] All event types handled correctly
- [ ] Idempotent (reprocessing same message is safe)
- [ ] Failed messages go to DLQ
- [ ] Metrics: messages processed, errors, latency
- [ ] Unit tests for processing logic
```

---

## Validation Checklist

Before declaring queue analysis complete:

- [ ] All topics/queues/exchanges documented
- [ ] Message schemas captured
- [ ] Producer → Consumer flows mapped
- [ ] QoS/acknowledgment strategy defined
- [ ] Dead letter handling documented
- [ ] Error handling flows specified
- [ ] Consumer groups identified
- [ ] Ordering guarantees understood
- [ ] Security (auth/TLS) documented
- [ ] Monitoring requirements noted

## Reference

See api-analyzer for HTTP/REST integration counterpart.