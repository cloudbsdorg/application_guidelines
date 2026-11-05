---
name: message-queue-overview
description: Message broker overview — broker types comparison, core terminology, producer/consumer concepts.
---

# Message Queue Analyzer — Overview

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
```

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
