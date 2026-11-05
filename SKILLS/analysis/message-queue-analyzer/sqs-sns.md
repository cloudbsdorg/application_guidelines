---
name: message-queue-sqs-sns
description: AWS SQS and SNS analysis — standard vs FIFO queues, fan-out patterns, SNS + SQS integration, message persistence.
---

# Message Queue Analyzer — Amazon SQS & SNS

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
