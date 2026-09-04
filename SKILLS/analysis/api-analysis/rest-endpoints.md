---
name: api-analyzer-rest-endpoints
description: REST API endpoint analysis — discovery patterns, request/response formats, authentication, versioning.
---

# API Analyzer — REST Endpoints

## 1. Endpoint Discovery

### 1.1 Common REST Patterns

| Pattern | Endpoint | Method | Purpose |
|---------|----------|--------|---------|
| List | `/users` | GET | Get all users |
| Get One | `/users/:id` | GET | Get user by ID |
| Create | `/users` | POST | Create new user |
| Replace | `/users/:id` | PUT | Replace user |
| Update | `/users/:id` | PATCH | Partial update |
| Delete | `/users/:id` | DELETE | Remove user |
| Search | `/users/search?q=...` | GET | Search users |

### 1.2 Non-REST Patterns

| Pattern | Example | Use |
|---------|---------|-----|
| RPC-style | `/users/123/activate` | Actions |
| Batch | `POST /users/batch` | Bulk operations |
| Custom | `POST /users/123/permissions` | Complex operations |

## 2. REST Analysis Template

```markdown
# REST API Analysis

## Base URL
`https://api.example.com/v1`

## Authentication
- Type: Bearer Token
- Header: `Authorization: Bearer <token>`

## Endpoints

### Users

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | /users | List all users | Yes |
| POST | /users | Create user | Yes |
| GET | /users/:id | Get user | Yes |
| PUT | /users/:id | Replace user | Yes |
| PATCH | /users/:id | Update user | Yes |
| DELETE | /users/:id | Delete user | Yes |

### Orders

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | /orders | List orders | Yes |
| POST | /orders | Create order | Yes |
| GET | /orders/:id | Get order | Yes |
```

## 3. Request/Response Patterns

### List Response

```json
{
  "data": [
    {
      "id": "123",
      "type": "user",
      "attributes": {
        "name": "Alice",
        "email": "alice@example.com"
      }
    }
  ],
  "meta": {
    "total": 100,
    "page": 1,
    "per_page": 20
  },
  "links": {
    "self": "/users?page=1",
    "next": "/users?page=2",
    "prev": null
  }
}
```

### Error Response

```json
{
  "errors": [
    {
      "status": "422",
      "title": "Validation Error",
      "detail": "The email field is required",
      "source": {
        "pointer": "/data/attributes/email"
      }
    }
  ]
}
```

### Pagination Patterns

| Style | Parameter | Example |
|-------|-----------|---------|
| Page-based | `?page=2&per_page=20` | Offset |
| Cursor-based | `?cursor=abc123` | Keyset |
| Offset | `?offset=20&limit=20` | SQL-like |

## 4. Authentication Methods

### Bearer Token

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

### Basic Auth

```
Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ=
```

### API Key

```
X-API-Key: your-api-key-here
```

### 5. API Versioning

| Strategy | Example | Pros | Cons |
|----------|---------|------|------|
| URL Path | `/api/v1/users` | Clear | URL pollution |
| Query Param | `/api/users?version=1` | Easy | Caching issues |
| Header | `API-Version: 1` | Clean URLs | Hidden |
| Content Negotiation | `Accept: application/vnd.api+json;version=1` | RESTful | Complex |

## 6. Rate Limiting

### Response Headers

| Header | Description |
|--------|-------------|
| X-RateLimit-Limit | Max requests per window |
| X-RateLimit-Remaining | Requests left |
| X-RateLimit-Reset | When window resets |
| Retry-After | Seconds to wait (on 429) |

### Rate Limit Response (429)

```json
{
  "error": {
    "status": 429,
    "title": "Too Many Requests",
    "detail": "Rate limit exceeded. Retry in 60 seconds.",
    "retry_after": 60
  }
}
```

### Rate Limit Strategies

| Strategy | Description | Example |
|----------|-------------|---------|
| Per-user | Each authenticated user has a limit | 100 req/user/min |
| Per-IP | Each source address has a limit | 1000 req/IP/hour |
| Per-endpoint | Expensive endpoints limited separately | 10 req/sec on `/search` |
| Global | Whole API has a ceiling | 10,000 req/min total |

Record which strategy applies: a per-user limit and a per-IP limit behave very
differently behind a shared NAT or a proxy, and porting the wrong one produces a
service that throttles the wrong callers.

### Idempotency Keys

Any endpoint that can be safely retried should accept an idempotency key
(commonly an `Idempotency-Key` request header) and de-duplicate on it. This is
also the receiving side of the webhook contract: store the processed event id
and return success without re-applying the effect if it is seen again.

```go
// Reject a replay before doing any work.
if store.Seen(eventID) {
    return http.StatusOK // already processed; do not apply twice
}
```

## 7. Common REST Conventions

### Resource Naming

| Good | Bad | Reason |
|------|-----|--------|
| `/users` | `/getUsers` | Nouns, not verbs |
| `/users/:id` | `/users/:id/details` | Nested for sub-resources |
| `/orders/:id/items` | `/getOrderItems(orderId=1)` | RESTful path |

### HTTP Status Conventions

| Action | Success | Error |
|--------|---------|-------|
| Create | 201 + Location header | 400, 409 |
| Read | 200 | 404 |
| Update | 200 | 400, 404, 409 |
| Delete | 204 (no body) | 400, 404 |

## 8. Async Operations

### Polling Pattern

```
POST /orders
→ 202 Accepted
  Location: /orders/123/status

GET /orders/123/status
→ 200 OK
  { "status": "processing" }

GET /orders/123/status
→ 200 OK
  { "status": "completed" }
```

### Webhook Pattern

```
POST /orders
→ 202 Accepted

Server later calls:
POST /your-webhook-url
{ "event": "order.completed", "order_id": "123" }
```

## 9. OpenAPI/Swagger Integration

### Discovery from OpenAPI

```yaml
openapi: 3.0.0
info:
  title: User API
  version: 1.0.0
paths:
  /users:
    get:
      summary: List users
      responses:
        '200':
          description: Success
```

## 10. REST Discovery Checklist

- [ ] Base URL identified
- [ ] Authentication method identified
- [ ] All endpoints documented
- [ ] HTTP methods mapped to CRUD
- [ ] Request/response formats documented
- [ ] Error response format documented
- [ ] Pagination strategy identified
- [ ] Rate limiting documented
- [ ] Versioning strategy identified
- [ ] Filtering/searching documented
