---
name: message-queue-integration
description: Message queue integration planning — pre-integration checklist, message processing tasks, validation checklist.
---

# Message Queue Analyzer — Integration

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
