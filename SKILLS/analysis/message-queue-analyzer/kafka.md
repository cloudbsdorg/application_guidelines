---
name: message-queue-kafka
description: Apache Kafka analysis — topics, partitions, consumer groups, producers, message schemas, record batch format.
---

# Message Queue Analyzer — Apache Kafka

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
┌──────────────┐                    │  │Topic A │  │Topic A │  │Topic A ││
│  Consumer    │◄──Consume────────│  │Part 0  │  │Part 1  │  │Part 2  ││
│  Group B     │                    │  │Offset  │  │Offset  │  │Offset  ││
└──────────────┘                    │  │  0-99  │  │  0-199  │  │  0-149  ││
                                    │  └─────────┘  └─────────┘  └────────┘│
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
│  Consumer E ──────► Partition 2                            │
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
