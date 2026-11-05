---
name: message-queue-mqtt
description: MQTT analysis — QoS levels, topic wildcards, IoT sensor patterns, MQTT packet structure, discovery template.
---

# Message Queue Analyzer — MQTT

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
