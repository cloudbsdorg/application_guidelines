---
name: api-analyzer-http-fundamentals
description: HTTP Protocol Fundamentals for API analysis — methods, status codes, headers, content-types, connection management.
---

# API Analyzer — HTTP Fundamentals

## 0. HTTP Protocol Fundamentals

### 0.1 HTTP Message Structure

**Request:**
```
GET /api/users HTTP/1.1
Host: api.example.com
Accept: application/json
Authorization: Bearer <token>

<optional body for POST/PUT/PATCH>
```

**Response:**
```
HTTP/1.1 200 OK
Content-Type: application/json
Cache-Control: max-age=3600

{"users": [...]}
```

### 0.2 HTTP Methods Deep Dive

## HTTP Methods

| Method | Purpose | Body | Safe | Idempotent |
|--------|---------|------|------|------------|
| GET | Retrieve resource | None | Yes | Yes |
| POST | Create resource | Yes | No | No |
| PUT | Replace resource | Yes | No | Yes |
| PATCH | Partial update | Yes | No | No |
| DELETE | Remove resource | Optional | No | Yes |
| HEAD | Headers only | None | Yes | Yes |
| OPTIONS | Capabilities | None | Yes | Yes |

### Safe vs Unsafe

| Safe (read-only) | Unsafe (modifies data) |
|------------------|----------------------|
| GET, HEAD, OPTIONS | POST, PUT, PATCH, DELETE |

### Idempotent

| Idempotent (same result) | Non-Idempotent |
|-------------------------|-----------------|
| GET, HEAD, PUT, DELETE, OPTIONS | POST, PATCH |

### 0.3 HTTP Status Codes Quick Reference

## HTTP Status Codes by Class

### 1xx - Informational

| Code | Meaning | When |
|------|---------|------|
| 100 Continue | Client can send body | Large uploads |
| 101 Switching Protocols | Upgrade to WebSocket | Protocol change |

### 2xx - Success

| Code | Meaning | When |
|------|---------|------|
| 200 OK | Success | GET/PUT success |
| 201 Created | Resource created | POST success |
| 202 Accepted | Queued | Async processing |
| 204 No Content | Success, no body | DELETE success |
| 206 Partial Content | Paginated | Range requests |

### 3xx - Redirection

| Code | Meaning | When |
|------|---------|------|
| 301 Moved Permanently | Redirect (cached) | Permanent move |
| 302 Found | Temporary redirect | Keep using original URL |
| 304 Not Modified | Use cached | Cached response |
| 307 Temporary Redirect | Temporary | POST won't change to GET |
| 308 Permanent Redirect | Permanent | POST won't change to GET |

### 4xx - Client Errors

| Code | Meaning | When |
|------|---------|------|
| 400 Bad Request | Malformed request | Invalid syntax |
| 401 Unauthorized | Not authenticated | Missing/invalid auth |
| 403 Forbidden | Not authorized | Authenticated but no permission |
| 404 Not Found | Resource missing | URL doesn't exist |
| 405 Method Not Allowed | Wrong HTTP method | e.g., DELETE on read-only |
| 409 Conflict | State conflict | e.g., duplicate create |
| 410 Gone | Permanently deleted | Resource removed |
| 415 Unsupported Media Type | Wrong Content-Type | POST with wrong type |
| 422 Unprocessable Entity | Validation failed | Semantic errors |
| 429 Too Many Requests | Rate limited | Client over limit |

### 5xx - Server Errors

| Code | Meaning | When |
|------|---------|------|
| 500 Internal Server Error | Generic error | Unhandled exception |
| 501 Not Implemented | Method not supported | e.g., PATCH not coded |
| 502 Bad Gateway | Upstream error | Proxy/load balancer issue |
| 503 Service Unavailable | Down | Maintenance |
| 504 Gateway Timeout | Upstream slow | Proxy timeout |

### 0.4 HTTP Headers Reference

## Standard Request Headers

| Header | Example | Purpose |
|--------|---------|---------|
| Host | `api.example.com` | Target host |
| Accept | `application/json` | Response format |
| Accept-Encoding | `gzip, deflate` | Compression |
| Accept-Language | `en-US` | Localization |
| Authorization | `Bearer <token>` | Authentication |
| Content-Type | `application/json` | Request body format |
| Content-Length | `1234` | Body size |
| User-Agent | `MyApp/1.0` | Client identification |
| X-Request-ID | `uuid` | Tracing/correlation |
| X-API-Key | `<key>` | API key auth |

## Standard Response Headers

| Header | Example | Purpose |
|--------|---------|---------|
| Content-Type | `application/json` | Response format |
| Content-Length | `1234` | Body size |
| Content-Encoding | `gzip` | Compression |
| Cache-Control | `max-age=3600` | Caching directives |
| ETag | `"abc123"` | Caching fingerprint |
| Last-Modified | `Wed, 21 Oct 2026...` | Caching |
| Location | `/users/123` | Created resource URL |
| X-Request-ID | `uuid` | Tracing/correlation |
| Retry-After | `3600` | Rate limit / downtime |

## Custom/X- Headers (Convention)

| Header | Purpose |
|--------|---------|
| X-API-Version | API version |
| X-Rate-Limit-Remaining | Rate limit |
| X-Rate-Limit-Reset | When limit resets |
| X-Correlation-ID | Request chain |
| X-Forwarded-For | Original client IP |

### 0.5 Content-Types

## Common Content-Types

| Type | Format | Use |
|------|--------|-----|
| `application/json` | JSON | REST APIs |
| `application/xml` | XML | SOAP APIs |
| `application/x-www-form-urlencoded` | Key-value | HTML forms |
| `multipart/form-data` | Multipart | File uploads |
| `text/plain` | Plain text | Simple responses |
| `text/html` | HTML | Web pages |
| `application/octet-stream` | Binary | File downloads |
| `application/vnd.api+json` | JSON API | JSON:API spec |

## JSON with Encoding

```json
{
  "string": "Hello, World!",
  "number": 42,
  "boolean": true,
  "null": null,
  "array": [1, 2, 3],
  "object": {
    "nested": "value"
  },
  "unicode": "こんにちは",
  "escaped": "line1\nline2\ttab"
}
```

### 0.6 Connection & Transport

## Connection Management

| Setting | Header | Purpose |
|---------|--------|---------|
| Keep-Alive | `Connection: keep-alive` | Reuse TCP connection |
| Close | `Connection: close` | Close after response |
| Timeout | `Keep-Alive: timeout=5` | Connection idle time |

## HTTP/1.1 vs HTTP/2 vs HTTP/3

| Version | Multiplexing | Header Compression | Connection |
|---------|--------------|-------------------|-----------|
| HTTP/1.1 | No (pipelining) | None | Keep-alive |
| HTTP/2 | Yes (streams) | HPACK | Single TCP |
| HTTP/3 | Yes (streams) | QPACK | QUIC (UDP) |

## Common Ports

| Port | Protocol | Use |
|------|----------|-----|
| 80 | HTTP | Plain web |
| 443 | HTTPS | Secure web |
| 3000 | HTTP | Dev servers |
| 5000 | HTTP | Dev servers |
| 8080 | HTTP | Alt web |
| 8443 | HTTPS | Alt secure |
| 27017 | MongoDB | MongoDB default |

## Timeout Values

## Typical Timeout Configurations

| Type | Client Timeout | Server Timeout | Use |
|------|----------------|----------------|-----|
| Connect | 3-10s | 30s | TCP handshake |
| Read | 10-30s | 30-60s | Response time |
| Write | 10-30s | 30-60s | Request body |
| Idle | 60-300s | 30-120s | Keep-alive |

### 0.7 CORS (Cross-Origin Resource Sharing)

## CORS Headers

| Header | Value | Purpose |
|--------|-------|---------|
| Access-Control-Allow-Origin | `*` or `https://example.com` | Allowed origin |
| Access-Control-Allow-Methods | `GET, POST, PUT, DELETE` | Allowed methods |
| Access-Control-Allow-Headers | `Content-Type, Authorization` | Allowed headers |
| Access-Control-Max-Age | `86400` | Preflight cache |
| Access-Control-Allow-Credentials | `true` | Cookies/auth |

### Preflight Request (OPTIONS)

```
OPTIONS /api/users HTTP/1.1
Host: api.example.com
Origin: https://app.example.com
Access-Control-Request-Method: POST
Access-Control-Request-Headers: Content-Type, Authorization

```

### Preflight Response

```
HTTP/1.1 204 No Content
Access-Control-Allow-Origin: https://app.example.com
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Max-Age: 86400
```

### Simple Request (GET/POST without custom headers)

```
GET /api/users HTTP/1.1
Host: api.example.com
Origin: https://app.example.com

HTTP/1.1 200 OK
Access-Control-Allow-Origin: https://app.example.com
Content-Type: application/json

{"users": [...]}
```

## CORS Scenarios

### All Origins Allowed

```json
{
  "Access-Control-Allow-Origin": "*"
}
```

### Specific Origin with Credentials

```json
{
  "Access-Control-Allow-Origin": "https://app.example.com",
  "Access-Control-Allow-Credentials": true
}
```

### 0.8 Caching Headers

## Cache-Control Directives

| Directive | Purpose | Example |
|-----------|---------|---------|
| `max-age=N` | Cache for N seconds | `max-age=3600` |
| `no-cache` | Revalidate always | Every request |
| `no-store` | Never cache | Sensitive data |
| `private` | Browser only | User-specific |
| `public` | Shared caches | Static assets |
| `must-revalidate` | Stale not used | Fresh required |

## ETag / If-None-Match

**Server Response:**
```
HTTP/1.1 200 OK
ETag: "abc123def456"

{"data": "value"}
```

**Client (cached) Request:**
```
GET /api/data HTTP/1.1
If-None-Match: "abc123def456"

HTTP/1.1 304 Not Modified
ETag: "abc123def456"
```

**Client (stale) Request:**
```
GET /api/data HTTP/1.1
If-None-Match: "abc123def456"

HTTP/1.1 200 OK
ETag: "xyz789new0"
```

## Last-Modified / If-Modified-Since

**Server Response:**
```
HTTP/1.1 200 OK
Last-Modified: Wed, 21 Oct 2026 07:28:00 GMT

{"data": "value"}
```

**Client (cached) Request:**
```
GET /api/data HTTP/1.1
If-Modified-Since: Wed, 21 Oct 2026 07:28:00 GMT

HTTP/1.1 304 Not Modified
```
