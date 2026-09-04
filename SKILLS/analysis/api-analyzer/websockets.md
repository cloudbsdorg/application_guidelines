---
name: api-analyzer-websockets
description: WebSocket and Server-Sent Events (SSE) analysis — connection lifecycle, frame types, message formats, security.
---

# API Analyzer — WebSockets & SSE

## 10. WebSockets

### 10.1 WebSocket Concepts

```markdown
## WebSocket vs HTTP

| Aspect | HTTP | WebSocket |
|--------|------|-----------|
| Direction | Half-duplex (request/response) | Full-duplex |
| Connection | New connection per request | Persistent connection |
| Initiation | Client initiates | Either side can send |
| Overhead | Headers every request | Minimal after handshake |
| Use case | REST APIs | Real-time, bidirectional |

## WebSocket URI
```
ws://example.com/socket        // Unencrypted
wss://example.com/socket       // Encrypted (preferred)
```

### Connection Lifecycle

```
┌──────────┐                    ┌──────────┐
│  Client  │                    │  Server  │
└────┬─────┘                    └────┬─────┘
     │                               │
     │  1. HTTP Upgrade Request      │
     │  GET /socket HTTP/1.1         │
     │  Connection: Upgrade           │
     │  Upgrade: websocket           │
     │  Sec-WebSocket-Key: abc123    │
     │──────────────────────────────►│
     │                               │
     │  2. HTTP Upgrade Response     │
     │  HTTP/1.1 101 Switching       │
     │  Protocols                    │
     │◄──────────────────────────────│
     │                               │
     │  3. WebSocket Frames          │
     │◄══════════════════════════════►│
     │  (bidirectional)              │
     │                               │
     │  4. Close Frame               │
     │◄────────────────────────────────│
```

### 10.2 WebSocket Frame Types

```markdown
## Frame Types

| Opcode | Name | Direction | Description |
|--------|------|-----------|-------------|
| 0x0 | Continuation | Either | Continuation of fragmented message |
| 0x1 | Text | Either | UTF-8 text message |
| 0x2 | Binary | Either | Binary message |
| 0x8 | Close | Either | Connection close |
| 0x9 | Ping | Either | Heartbeat/ping |
| 0xA | Pong | Either | Pong response |

## Sample Frames

```
// Text message from server to client
Frame: 0x81 0x0B "Hello World"
// 0x81 = FIN + text opcode
// 0x0B = 11 bytes

// Binary message
Frame: 0x82 0x04 0x01 0x02 0x03 0x04
// 0x82 = FIN + binary opcode
// 0x04 = 4 bytes
// [01 02 03 04] = binary data
```

### 10.3 WebSocket Protocol (ws) vs Secure (wss)

```markdown
## Security Comparison

| Aspect | ws:// | wss:// |
|--------|-------|--------|
| Encryption | None | TLS encrypted |
| Port | 80 | 443 |
| Use in production | No | Yes |
| Proxy compatibility | May be blocked | Works like HTTPS |
```

### 10.4 Message Format Patterns

```markdown
## JSON Message Envelope

```json
// Command/Message
{
  "type": "message",
  "channel": "orders",
  "payload": {
    "action": "create",
    "data": { ... }
  }
}

// Event/Notification
{
  "type": "event",
  "event": "order.created",
  "data": { ... },
  "timestamp": "2026-05-03T12:00:00Z"
}

// Acknowledgment
{
  "type": "ack",
  "messageId": "msg_123",
  "status": "delivered"
}

// Error
{
  "type": "error",
  "code": "INVALID_MESSAGE",
  "message": "Channel not found"
}
```
```

### 10.5 WebSocket Security

```markdown
## Security Best Practices

| Practice | Implementation |
|----------|---------------|
| Use wss:// | TLS encryption |
| Validate origin | Check Origin header |
| Authenticate | Token in first message |
| Sanitize input | Validate all payload data |
| Rate limiting | Limit connections per IP |
| Heartbeat | Ping/pong every 30s |
| Max message size | 1MB default |
| Close on error | Don't leak connection state |
```

### 10.6 WebSocket Analysis Template

```markdown
## WebSocket Analysis

### Endpoint
| Property | Value |
|----------|-------|
| URI | `wss://api.example.com/socket` |
| Protocol | JSON over WebSocket |
| Port | 443 |

### Connection
| Property | Value |
|----------|-------|
| Authentication | Token in first message |
| Reconnection | Automatic with backoff |
| Heartbeat | 30 second interval |

### Channels
| Channel | Purpose | Direction |
|---------|---------|-----------|
| `orders` | Order events | Server → Client |
| `user:{id}` | User notifications | Server → Client |
| `chat:{room}` | Chat messages | Bidirectional |

### Message Types
| Type | Description |
|------|-------------|
| `event` | Server-initiated event |
| `command` | Client-initiated action |
| `ack` | Acknowledgment |
| `error` | Error response |
```

## 11. Server-Sent Events (SSE)

### When to Use SSE vs WebSockets

```markdown
| Aspect | SSE | WebSockets |
|--------|-----|-----------|
| Direction | Server → Client only | Bidirectional |
| Complexity | Simple | Complex |
| Browser support | Native | Fallback needed |
| Automatic reconnection | Built-in | Manual |
| Binary data | Base64 encoding | Native |
| HTTP/2 | Multiplexed | Separate connection |
| Best for | Notifications, feeds | Games, chat |
```

### Use Cases

```markdown
| Use Case | Protocol | Reason |
|----------|----------|--------|
| Live news feed | SSE | Simple, one-way |
| Stock ticker | SSE | One direction, high freq |
| Chat application | WebSocket | Bidirectional |
| Online gaming | WebSocket | Low latency, bidirectional |
| Notifications | SSE | Simple, reliable |
| Collaborative editing | WebSocket | Real-time sync |
```

### SSE Response Format

```bash
# Server sends:
Content-Type: text/event-stream
Cache-Control: no-cache
Connection: keep-alive

# Event format:
event: message
data: {"user": "Alice", "message": "Hello"}

event: notification
id: 123
data: {"title": "New order", "body": "Order #1042 received"}

# Comment (keepalive):
: keepalive heartbeat

# Multiple lines:
data: line 1
data: line 2
data: line 3

# Final event:
event: close
data: Connection closing
```

### SSE Fields

```markdown
| Field | Description |
|-------|-------------|
| `event` | Event type name |
| `data` | Payload (can be multiline) |
| `id` | Event ID for retry tracking |
| `retry` | Reconnection time in ms |
| `:` | Comment (keepalive) |

### Multi-line Data

```bash
# Multiline JSON:
data: {
data:   "user": "Alice",
data:   "message": "Hello"
data: }

# Becomes:
{ "user": "Alice", "message": "Hello" }
```

### SSE Analysis Template

```markdown
## SSE Analysis

### Endpoint
| Property | Value |
|----------|-------|
| URL | `/api/events` |
| Method | GET |
| Auth | Bearer token |

### Event Types
| Event | Payload | Trigger |
|-------|---------|---------|
| `message` | User message | New message |
| `notification` | Alert | System notification |
| `update` | Entity update | Data changed |
| `close` | - | Connection end |

### Client Implementation
```javascript
const eventSource = new EventSource('/api/events', {
  headers: { 'Authorization': `Bearer ${token}` }
});

eventSource.addEventListener('message', (e) => {
  const data = JSON.parse(e.data);
  // Handle message
});

eventSource.addEventListener('notification', (e) => {
  showNotification(JSON.parse(e.data));
});
```
```
