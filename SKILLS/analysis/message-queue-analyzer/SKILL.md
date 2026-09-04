---
name: message queue analyzer
description: Systematically analyze message brokers, queues, and event-driven architectures to understand message flow, patterns, and integration points.
---

# Skill: message-queue-analyzer

**Purpose:** Systematically analyze message brokers, queues, and event-driven architectures to understand message flow, patterns, and integration points.

**Triggers:** When analyzing a system with message queues, event brokers, or async communication patterns.

---

## Loading Instructions

This skill is **modular**. Load only the sub-skill you need:

| Sub-Skill | When to Load |
|-----------|--------------|
| [overview.md](./overview.md) | Broker types comparison, core terminology |
| [rabbitmq.md](./rabbitmq.md) | RabbitMQ exchanges, queues, routing patterns |
| [kafka.md](./kafka.md) | Kafka topics, partitions, consumer groups, producers |
| [mqtt.md](./mqtt.md) | MQTT QoS, topics, IoT sensor patterns |
| [sqs-sns.md](./sqs-sns.md) | AWS SQS queues, SNS fan-out patterns |
| [nats.md](./nats.md) | NATS core, JetStream, request/reply |
| [patterns.md](./patterns.md) | Envelope pattern, event sourcing, CQRS |
| [integration.md](./integration.md) | Pre-integration checklist, message processing |

---

## Loading This Skill

Load this skill when the user asks you to:
- Analyze message queue systems
- Document broker architectures
- Understand pub/sub patterns
- Map message flows
- Plan queue integration
- Analyze MQTT, RabbitMQ, Kafka, or similar

---

## Quick-Scan Index

### By Broker/Technology

| Need | Sub-Skill |
|------|-----------|
| Broker comparison/terminology | [overview.md](./overview.md) |
| RabbitMQ | [rabbitmq.md](./rabbitmq.md) |
| Apache Kafka | [kafka.md](./kafka.md) |
| MQTT | [mqtt.md](./mqtt.md) |
| AWS SQS/SNS | [sqs-sns.md](./sqs-sns.md) |
| NATS | [nats.md](./nats.md) |

### By Analysis Need

| Need | Sub-Skill |
|------|-----------|
| Message schema/envelope | [patterns.md](./patterns.md) |
| Event sourcing/CQRS | [patterns.md](./patterns.md) |
| Pre-integration checklist | [integration.md](./integration.md) |
| Message processing tasks | [integration.md](./integration.md) |

---

## Reference

- api-analyzer for HTTP/REST integration counterpart
