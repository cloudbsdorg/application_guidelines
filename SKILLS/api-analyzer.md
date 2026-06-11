441113# Skill: api-analyzer

**Purpose:** Systematically analyze REST APIs and web services to understand endpoints, request/response formats, authentication, and data flow.

**Triggers:** When analyzing an API for porting, rewriting, or integration planning.

## Loading Instructions

Load this skill when the user asks you to:
- Analyze an API for porting
- Document REST endpoints
- Understand request/response formats
- Map API authentication flows
- Generate API specifications
- Plan API integration

---

## 0. HTTP Protocol Fundamentals

### 0.1 HTTP Message Structure

```
┌─ Request Line ─────────────────────────────────────────────────────────────┐
│ GET /api/v1/users?page=2&limit=20 HTTP/1.1                               │
├─ General Headers ──────────────────────────────────────────────────────────┤
│ Host: api.example.com                                                     │
│ User-Agent: MyApp/1.0                                                     │
│ Accept: application/json                                                  │
│ Authorization: Bearer eyJhbGciOiJIUzI1NiIs...                            │
├─ Request Headers ────────────────────────────────────────────────────────┤
│ Content-Type: application/json                                            │
│ Content-Length: 256                                                       │
│ X-Request-ID: abc-123-def                                                │
├─ Empty Line ──────────────────────────────────────────────────────────────┤
├─ Request Body (for POST/PUT/PATCH) ──────────────────────────────────────┤
│ {"name": "John", "email": "john@example.com"}                             │
└──────────────────────────────────────────────────────────────────────────┘

┌─ Status Line ────────────────────────────────────────────────────────────┐
│ HTTP/1.1 200 OK                                                          │
├─ Response Headers ────────────────────────────────────────────────────────┤
│ Date: Sat, 02 May 2026 12:00:00 GMT                                      │
│ Server: nginx/1.24.0                                                      │
│ Content-Type: application/json                                            │
│ Content-Length: 512                                                       │
│ X-Request-ID: abc-123-def                                                │
│ X-RateLimit-Limit: 100                                                    │
│ X-RateLimit-Remaining: 47                                                 │
│ X-RateLimit-Reset: 1746192000                                            │
│ Cache-Control: no-cache                                                    │
│ Set-Cookie: session=abc123; HttpOnly; Secure; SameSite=Strict             │
├─ Empty Line ──────────────────────────────────────────────────────────────┤
├─ Response Body ──────────────────────────────────────────────────────────┤
│ {"data": [...], "meta": {"page": 2, "total": 100}}                       │
└──────────────────────────────────────────────────────────────────────────┘
```

### 0.2 HTTP Methods Deep Dive

```markdown
## HTTP Methods

| Method | Safe | Idempotent | Body | Description |
|--------|------|------------|------|-------------|
| GET | Yes | Yes | No | Retrieve resource |
| HEAD | Yes | Yes | No | Same as GET but headers only |
| POST | No | No | Yes | Create resource or trigger action |
| PUT | No | Yes | Yes | Replace entire resource |
| PATCH | No | No | Yes | Partial update |
| DELETE | No | Yes | No | Remove resource |
| OPTIONS | Yes | Yes | No | CORS preflight, list methods |
| CONNECT | No | No | No | Create tunnel (proxy) |
| TRACE | Yes | Yes | No | Debug loopback (rarely used) |

### Safe vs Unsafe
- **Safe**: Doesn't modify server state (GET, HEAD, OPTIONS)
- **Unsafe**: May modify server state (POST, PUT, PATCH, DELETE)

### Idempotent
- **Idempotent**: Same request produces same result (GET, PUT, DELETE, HEAD, OPTIONS)
- **Non-idempotent**: Multiple calls may have different effects (POST, PATCH)
```

### 0.3 HTTP Status Codes Quick Reference

```markdown
## HTTP Status Codes by Class

### 1xx - Informational
| Code | Name | Meaning |
|------|------|---------|
| 100 | Continue | Client should continue with request |
| 101 | Switching Protocols | Server switching protocols (e.g., HTTP → WebSocket) |

### 2xx - Success
| Code | Name | Meaning |
|------|------|---------|
| 200 | OK | Request succeeded |
| 201 | Created | Resource created (use Location header) |
| 202 | Accepted | Request queued, processing async |
| 204 | No Content | Success, no body (DELETE) |

### 3xx - Redirection
| Code | Name | Meaning |
|------|------|---------|
| 301 | Moved Permanently | Resource moved permanently (update bookmarks) |
| 302 | Found | Temporary redirect (POST doesn't resubmit) |
| 303 | See Other | Redirect to GET (POST result) |
| 304 | Not Modified | Cached version still valid (use If-None-Match) |
| 307 | Temporary Redirect | Keep method (POST preserved) |
| 308 | Permanent Redirect | Keep method, permanent |

### 4xx - Client Errors
| Code | Name | Meaning |
|------|------|---------|
| 400 | Bad Request | Malformed syntax, invalid JSON |
| 401 | Unauthorized | No/invalid authentication |
| 403 | Forbidden | Authenticated but not permitted |
| 404 | Not Found | Resource doesn't exist |
| 405 | Method Not Allowed | Method not supported for this URL |
| 408 | Request Timeout | Client took too long |
| 409 | Conflict | State conflict (version mismatch, duplicate) |
| 410 | Gone | Resource deleted permanently |
| 415 | Unsupported Media Type | Content-Type not accepted |
| 422 | Unprocessable Entity | Validation failed |
| 429 | Too Many Requests | Rate limited |

### 5xx - Server Errors
| Code | Name | Meaning |
|------|------|---------|
| 500 | Internal Server Error | Unexpected server fault |
| 501 | Not Implemented | Feature not supported |
| 502 | Bad Gateway | Upstream returned invalid response |
| 503 | Service Unavailable | Server down for maintenance |
| 504 | Gateway Timeout | Upstream didn't respond in time |
```

### 0.4 HTTP Headers Reference

```markdown
## Standard Request Headers

| Header | Example | Purpose |
|--------|---------|---------|
| Host | api.example.com | Target host (required in HTTP/1.1) |
| User-Agent | MyApp/2.1 | Client identification |
| Accept | application/json | Acceptable response formats |
| Accept-Language | en-US, fr-FR | Preferred languages |
| Accept-Encoding | gzip, deflate, br | Acceptable encodings |
| Content-Type | application/json | Request body format |
| Content-Length | 256 | Body size in bytes |
| Authorization | Bearer xxx | Authentication credentials |
| Cookie | session=abc123 | Session data |
| Referer | https://app.com/page | Previous page (note: misspelled in spec) |
| Origin | https://app.com | CORS origin |
| X-Requested-With | XMLHttpRequest | AJAX indicator |
| X-HTTP-Method-Override | PUT | Override method (for proxies) |

## Standard Response Headers

| Header | Example | Purpose |
|--------|---------|---------|
| Content-Type | application/json | Response body format |
| Content-Length | 1024 | Body size in bytes |
| Content-Encoding | gzip | Body encoding |
| Cache-Control | no-cache, max-age=3600 | Caching directives |
| ETag | "abc123" | Resource version for caching |
| Last-Modified | Sat, 02 May 2026 12:00:00 GMT | Resource modification time |
| Location | /api/users/123 | For 201 Created redirects |
| Set-Cookie | session=abc; HttpOnly; Secure | Set client cookie |
| Access-Control-Allow-Origin | https://app.com | CORS |
| Access-Control-Allow-Methods | GET, POST, PUT, DELETE | CORS allowed methods |
| Access-Control-Allow-Headers | Content-Type, Authorization | CORS allowed headers |
| X-Request-ID | abc-123-def | Request tracing |

## Custom/X- Headers (Convention)

| Header | Example | Purpose |
|--------|---------|---------|
| X-API-Key | sk_live_xxxx | API key authentication |
| X-RateLimit-Limit | 100 | Rate limit ceiling |
| X-RateLimit-Remaining | 47 | Requests left in window |
| X-RateLimit-Reset | 1746192000 | When rate limit resets |
| X-Total-Count | 150 | Total records (for lists) |
| X-Page-Number | 2 | Current page |
| X-Page-Size | 20 | Items per page |
```

### 0.5 Content-Types

```markdown
## Common Content-Types

| Type | Value | Use Case |
|------|-------|----------|
| JSON | application/json | REST APIs |
| XML | application/xml | SOAP APIs |
| Form URL-encoded | application/x-www-form-urlencoded | Simple HTML forms |
| Multipart | multipart/form-data | File uploads |
| Plain text | text/plain | Simple text responses |
| HTML | text/html | Web pages |
| JavaScript | application/javascript | JS files |
| CSS | text/css | Stylesheets |
| Image PNG | image/png | Image responses |
| Image JPEG | image/jpeg | Image responses |
| PDF | application/pdf | Document responses |
| Octet stream | application/octet-stream | Binary data |

## JSON with Encoding

| Encoding | Header Value | Notes |
|----------|--------------|-------|
| UTF-8 | application/json; charset=utf-8 | Default for JSON |
| ASCII | application/json | 7-bit safe |
```

### 0.6 Connection & Transport

```markdown
## Connection Management

| Concept | Description |
|---------|-------------|
| Keep-Alive | Reuse TCP connection for multiple requests |
| Connection: close | Close connection after response |
| Content-Length | Prevents chunked encoding, exact body size |
| Transfer-Encoding: chunked | Stream response in chunks |

## HTTP/1.1 vs HTTP/2 vs HTTP/3

| Version | Multiplexing | Header Compression | Transport |
|---------|--------------|-------------------|-----------|
| HTTP/1.1 | No (pipelining rare) | None | TCP |
| HTTP/2 | Yes (streams) | HPACK | TCP |
| HTTP/3 | Yes (streams) | QPACK | QUIC (UDP) |

## Common Ports

| Port | Service |
|------|---------|
| 80 | HTTP |
| 443 | HTTPS |
| 8080 | HTTP (development) |
| 8443 | HTTPS (development) |
| 3000 | Node.js dev server |
| 5000 | Python dev server |

## Timeout Values

```markdown
## Typical Timeout Configurations

| Timeout | Value | Purpose |
|---------|-------|---------|
| Connect | 5s | TCP connection establishment |
| TLS | 5s | SSL/TLS handshake |
| First Byte | 30s | Wait for first byte |
| Total | 60s | Maximum request time |
| Idle | 60s | Keep-alive connection |
| Read | 30s | Response body download |
```

### 0.7 CORS (Cross-Origin Resource Sharing)

```markdown
## CORS Headers

### Preflight Request (OPTIONS)
```
OPTIONS /api/users HTTP/1.1
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
Origin: https://app.example.com

Response:
Access-Control-Allow-Origin: https://app.example.com
```

## CORS Scenarios

| Scenario | Required Headers |
|----------|------------------|
| Same origin | None |
| Different origin, simple GET | Access-Control-Allow-Origin |
| Different origin, POST with JSON | Access-Control-Allow-Origin, Content-Type |
| Credentials (cookies) | Access-Control-Allow-Origin (must be specific), Access-Control-Allow-Credentials: true |
| Custom headers | Access-Control-Allow-Headers |
| Non-simple methods | Preflight required |
```

### 0.8 Caching Headers

```markdown
## Cache-Control Directives

| Directive | Meaning |
|-----------|---------|
| no-store | Don't cache at all |
| no-cache | Cache but revalidate on each request |
| private | Cache only in browser, not CDN |
| public | Can be cached by proxies/CDN |
| max-age=3600 | Cache for 1 hour |
| s-maxage=7200 | CDN cache for 2 hours |
| must-revalidate | Stale content must revalidate |
| proxy-revalidate | Same but for proxies |
| immutable | Content never changes |

## ETag / If-None-Match

```
Request:
GET /api/users/123 HTTP/1.1
If-None-Match: "abc123"

Response (not modified):
HTTP/1.1 304 Not Modified
ETag: "abc123"

Response (modified):
HTTP/1.1 200 OK
ETag: "def456"
{"id": 123, "name": "John"}
```

## Last-Modified / If-Modified-Since

```
Request:
GET /api/users/123 HTTP/1.1
If-Modified-Since: Sat, 02 May 2026 10:00:00 GMT

Response (not modified since):
HTTP/1.1 304 Not Modified
Last-Modified: Sat, 02 May 2026 10:00:00 GMT

Response (modified since):
HTTP/1.1 200 OK
Last-Modified: Sat, 02 May 2026 11:00:00 GMT
{"id": 123, "name": "John"}
```

---

## 1. Endpoint Discovery

### 1.1 Common REST Patterns

| Method | Path | Purpose | Example |
|--------|------|---------|---------|
| GET | `/resources` | List/Read | `GET /users` - list all users |
| GET | `/resources/{id}` | Read one | `GET /users/123` - get user 123 |
| POST | `/resources` | Create | `POST /users` - create new user |
| PUT | `/resources/{id}` | Replace | `PUT /users/123` - replace user 123 |
| PATCH | `/resources/{id}` | Update partial | `PATCH /users/123` - update user 123 |
| DELETE | `/resources/{id}` | Delete | `DELETE /users/123` - delete user 123 |

### 1.2 Non-REST Patterns

```go
// RPC-style
POST /api/login          // "login" is action, not resource
POST /api/logout
POST /api/calculate

// Query-style (often for complex operations)
GET /api/reports?type=sales&date=2026-05
GET /api/search?q=keyword&filters=active:true

// Bulk operations
POST /api/users/bulk-delete
POST /api/orders/bulk-update

// File uploads
POST /api/documents/upload
POST /api/avatars/{userId}/upload
```

### 1.3 Endpoint Inventory Template

```markdown
## API Endpoints

| Method | Path | Handler | Auth | Description |
|--------|------|---------|------|-------------|
| GET | /api/v1/users | UserHandler.List | Bearer | List all users |
| GET | /api/v1/users/{id} | UserHandler.Get | Bearer | Get user by ID |
| POST | /api/v1/users | UserHandler.Create | Bearer | Create new user |
| PUT | /api/v1/users/{id} | UserHandler.Update | Bearer | Replace user |
| PATCH | /api/v1/users/{id} | UserHandler.Patch | Bearer | Partial update |
| DELETE | /api/v1/users/{id} | UserHandler.Delete | Bearer | Delete user |
```

### 1.4 Discovery Commands

```bash
# Find route registration in Go
grep -r "HandleFunc\|Handle\|Route\|Get\|Post\|Put\|Delete\|Patch" \
  --include="*.go" server.go router.go routes.go

# Find route decorators in Python (Flask)
grep -r "@app.route\|@bp.route\|@router.route" --include="*.py"

# Find route decorators in TypeScript/Node
grep -r "router\.(get\|post\|put\|patch\|delete)" --include="*.ts"

# Find OpenAPI/Swagger specs
find . -name "*.yaml" -o -name "*.json" | xargs grep -l "openapi\|swagger"
```

---

## 2. Request Format Analysis

### 2.1 Request Components

```markdown
## Request Structure

| Component | Location | Example |
|-----------|----------|---------|
| Method | Line 1 | POST |
| Path | Line 1 | /api/v1/orders |
| Query | Line 1 | ?status=pending&page=2 |
| Headers | Lines 2+ | Authorization: Bearer xxx |
| Body | After headers | {"customerId": 123, "items": [...]} |
```

### 2.2 Common Header Patterns

```markdown
## Request Headers

| Header | Purpose | Example |
|--------|---------|---------|
| Authorization | Auth token | Bearer eyJhbGciOiJIUzI1NiIs... |
| Content-Type | Body format | application/json |
| Accept | Response format | application/json |
| X-Request-ID | Tracing | abc-123-def |
| X-API-Key | API key auth | sk_live_xxxxxxxxxxxx |
| User-Agent | Client identification | MyApp/1.0 |
| Accept-Language | i18n | en-US, fr-FR |
```

### 2.3 Request Body Templates

```markdown
## Request Body Formats

### JSON (most common)
```json
{
  "field1": "value",
  "field2": 123,
  "nested": {
    "key": "value"
  },
  "array": ["a", "b", "c"]
}
```

### Form Data (application/x-www-form-urlencoded)
```
username=john&password=secret&remember=true
```

### Multipart (file uploads)
```
Content-Type: multipart/form-data

------Boundary
Content-Disposition: form-data; name="file"; filename="avatar.png"
Content-Type: image/png

[binary data]
------Boundary--
```

### Query Parameters
```
GET /api/search?q=keyword&filters=type:sale,status:active&sort=date:desc&page=1&limit=20
```
```

---

## 3. Response Format Analysis

### 3.1 Response Structure

```markdown
## Response Structure

| Component | Status | Example |
|-----------|--------|---------|
| Status Code | 200 | 200 OK, 201 Created, 400 Bad Request |
| Headers | Metadata | Content-Type, X-Total-Count |
| Body | Data | {"id": 123, "name": "John"} |
```

### 3.2 Common Status Codes

```markdown
## HTTP Status Codes

### Success
| Code | Meaning | When Used |
|------|---------|-----------|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST (new resource) |
| 202 | Accepted | Async operation queued |
| 204 | No Content | Successful DELETE |

### Client Errors
| Code | Meaning | When Used |
|------|---------|-----------|
| 400 | Bad Request | Invalid request body, malformed syntax |
| 401 | Unauthorized | Missing or invalid auth |
| 403 | Forbidden | Authenticated but not allowed |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate resource, version conflict |
| 422 | Unprocessable | Validation errors |
| 429 | Too Many Requests | Rate limited |

### Server Errors
| Code | Meaning | When Used |
|------|---------|-----------|
| 500 | Internal Error | Unexpected server error |
| 502 | Bad Gateway | Upstream service error |
| 503 | Unavailable | Service down, maintenance |
| 504 | Timeout | Upstream timeout |
```

### 3.3 Response Body Templates

```markdown
## Response Body Formats

### Single Resource (200)
```json
{
  "id": 123,
  "name": "John Smith",
  "email": "john@example.com",
  "createdAt": "2026-05-01T10:30:00Z"
}
```

### Collection (200)
```json
{
  "data": [
    {"id": 1, "name": "Item 1"},
    {"id": 2, "name": "Item 2"}
  ],
  "meta": {
    "total": 47,
    "page": 1,
    "perPage": 20,
    "totalPages": 3
  }
}
```

### Error (4xx)
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request",
    "details": [
      {"field": "email", "message": "Must be valid email"}
    ]
  }
}
```

### Created Resource (201)
```json
{
  "id": 124,
  "name": "New Item",
  "createdAt": "2026-05-02T14:00:00Z",
  "_links": {
    "self": "/api/v1/items/124"
  }
}
```

### No Content (204)
(No body - just empty response)
```

---

## 4. Authentication Analysis

### 4.1 Auth Methods

| Method | How | When Used |
|--------|-----|-----------|
| **None** | No auth | Public APIs |
| **API Key** | X-API-Key header | Server-to-server |
| **Basic Auth** | Authorization: Basic base64(user:pass) | Simple, legacy |
| **Bearer Token** | Authorization: Bearer {token} | OAuth2, JWT |
| **JWT** | Bearer with signed token | Stateless auth |
| **OAuth2** | Token exchange flow | Third-party access |
| **Session** | Cookie-based | Browser clients |

### 4.2 Auth Flow Analysis Template

```markdown
## Authentication Flow

### Current Implementation
| Step | Where | What Happens |
|------|-------|--------------|
| 1 | Login handler (auth.go:15) | Validates credentials |
| 2 | Token generation (auth.go:45) | Creates JWT with 1hr expiry |
| 3 | Response | Sets cookie or returns token |
| 4 | Subsequent requests | Token validated in middleware |

### Token Structure (JWT)
```json
{
  "header": {"alg": "HS256", "typ": "JWT"},
  "payload": {
    "sub": "user:123",
    "exp": 1746192000,
    "iat": 1746188400
  },
  "signature": "..."
}
```

### Protected vs Public Endpoints
| Endpoint | Auth Required | Notes |
|----------|---------------|-------|
| POST /api/auth/login | No | Public login |
| POST /api/auth/register | No | Public registration |
| GET /api/v1/users | Yes | Requires valid JWT |
| GET /api/v1/public/status | No | Public health check |
```

### 4.3 Auth Middleware Detection

```go
// Go middleware example
router.Use(authMiddleware)        // Applied to all routes
router.Use("/api/public", publicMiddleware)  // Exception

// Node/Express middleware
app.use('/api', authenticate)

// Flask decorator
@app.route('/api/protected')
@require_auth
```

---

## 5. Pagination & Filtering

### 5.1 Pagination Patterns

```markdown
## Pagination Patterns

### Offset-based
```
GET /api/users?page=2&per_page=20
```
```json
{
  "data": [...],
  "pagination": {
    "offset": 20,
    "limit": 20,
    "total": 100
  }
}
```

### Cursor-based
```
GET /api/users?cursor=eyJpZCI6MTB9&limit=20
```
```json
{
  "data": [...],
  "pagination": {
    "nextCursor": "eyJpZCI6MzB9",
    "hasMore": true
  }
}
```

### Page-based
```
GET /api/users?page=2
```
```json
{
  "data": [...],
  "pagination": {
    "currentPage": 2,
    "totalPages": 5,
    "perPage": 20
  }
}
```
```

### 5.2 Filtering & Sorting

```markdown
## Filtering Patterns

### Query string filters
```
GET /api/orders?status=pending&customer_id=123
GET /api/products?category=electronics&in_stock=true
```

### Filter operators
```
GET /api/users?age_gte=18&age_lte=65
GET /api/orders?created_after=2026-01-01
GET /api/users?name_like=john
```

### Sorting
```
GET /api/users?sort=created_at:desc
GET /api/users?sort=name:asc,created_at:desc
```

### Search
```
GET /api/users?q=john
GET /api/products?search=widget+pro
```

### Field selection
```
GET /api/users?fields=id,name,email
GET /api/users?include=orders,profile
```
```

---

## 6. Error Handling

### 6.1 Error Response Format

```markdown
## Error Response Format

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "User with ID 123 not found",
    "details": {
      "resource": "user",
      "id": "123"
    },
    "traceId": "abc-123-def-456"
  }
}
```

### Error Code Catalog

| Code | HTTP Status | Description |
|------|-------------|-------------|
| VALIDATION_ERROR | 400 | Invalid request data |
| INVALID_CREDENTIALS | 401 | Wrong username/password |
| TOKEN_EXPIRED | 401 | JWT or session expired |
| ACCESS_DENIED | 403 | Insufficient permissions |
| RESOURCE_NOT_FOUND | 404 | Item doesn't exist |
| DUPLICATE_RESOURCE | 409 | Conflict creating/updating |
| RATE_LIMIT_EXCEEDED | 429 | Too many requests |
| INTERNAL_ERROR | 500 | Unexpected server error |
| SERVICE_UNAVAILABLE | 503 | Down for maintenance |
```
```

### 6.2 Error Handling Flow

```markdown
## Error Handling Flow

```
Client sends request
        │
        ▼
┌───────────────────┐
│ Validate request  │──OK──► Continue
└───────────────────┘
        │ FAIL
        ▼
┌───────────────────┐
│ Return 4xx error  │──► Client shows error message
└───────────────────┘

        │
        ▼ Continue to handler
┌───────────────────┐
│ Execute handler   │──OK──► Return 2xx response
└───────────────────┘
        │ Exception
        ▼
┌───────────────────┐
│ Log error         │
│ Return 5xx error  │──► Client shows generic error
└───────────────────┘
```

---

## 7. Rate Limiting

### 7.1 Rate Limit Headers

```markdown
## Rate Limit Headers

| Header | Description |
|--------|-------------|
| X-RateLimit-Limit | Max requests per window |
| X-RateLimit-Remaining | Requests left in window |
| X-RateLimit-Reset | Unix timestamp when window resets |
| Retry-After | Seconds to wait (only on 429) |

Example:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 47
X-RateLimit-Reset: 1746192000
```
```

### 7.2 Rate Limit Patterns

```markdown
## Rate Limit Strategies

| Strategy | Description | Example |
|----------|-------------|---------|
| Per-user | Each user has limit | 100 req/user/min |
| Per-IP | Each IP has limit | 1000 req/IP/hour |
| Per-endpoint | Each endpoint has limit | 10 req/sec on /search |
| Global | Total API has limit | 10,000 req/min total |

### Common Limits
| Tier | Limit | Window |
|------|-------|--------|
| Free | 100 | per minute |
| Basic | 1,000 | per minute |
| Pro | 10,000 | per minute |
| Enterprise | Unlimited | - |
```

---

## 8. API Documentation Template

### 8.1 Endpoint Documentation

```markdown
## GET /api/v1/users/{id}

Retrieves a single user by ID.

### Request

**Headers:**
| Header | Required | Description |
|--------|----------|-------------|
| Authorization | Yes | Bearer {token} |

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| id | integer | User ID |

### Response

**200 OK:**
```json
{
  "id": 123,
  "name": "John Smith",
  "email": "john@example.com",
  "role": "customer",
  "createdAt": "2026-01-15T10:30:00Z"
}
```

**401 Unauthorized:**
```json
{
  "error": {
    "code": "TOKEN_EXPIRED",
    "message": "Authentication token has expired"
  }
}
```

**404 Not Found:**
```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "User with ID 123 not found"
  }
}
```

### Example

```bash
curl -X GET "https://api.example.com/api/v1/users/123" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
```
```

### 8.2 API Specification Output

```markdown
# API Specification: <Project>

## Base URL
`https://api.example.com/api/v1`

## Authentication
- Type: Bearer JWT
- Header: `Authorization: Bearer {token}`
- Token expiry: 1 hour

## Endpoints

### Users

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | /users | List users | Yes |
| GET | /users/{id} | Get user | Yes |
| POST | /users | Create user | Yes |
| PUT | /users/{id} | Replace user | Yes |
| PATCH | /users/{id} | Update user | Yes |
| DELETE | /users/{id} | Delete user | Yes |

### Orders

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | /orders | List orders | Yes |
| GET | /orders/{id} | Get order | Yes |
| POST | /orders | Create order | Yes |
| DELETE | /orders/{id} | Cancel order | Yes |

### Authentication

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | /auth/login | Login | No |
| POST | /auth/logout | Logout | Yes |
| POST | /auth/refresh | Refresh token | No |

## Common Headers

| Header | Value |
|--------|-------|
| Content-Type | application/json |
| Accept | application/json |

## Rate Limits

- Default: 100 requests per minute per user
- Headers: X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset

## Error Format

All errors follow this format:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message"
  }
}
```
```

---

## 9. Webhooks

### 9.1 Webhook Concepts

```markdown
## What is a Webhook?

A webhook is a reverse-API mechanism where the server PUSHES data to the client when an event occurs, instead of the client polling for updates.

### Push vs Poll

| Approach | Client Behavior | Server Behavior | Use Case |
|----------|-----------------|-----------------|----------|
| Polling | Client requests every N seconds | Returns current state | Infrequent updates |
| Webhook | Server pushes on event | Sends HTTP POST on event | Real-time updates |
| WebSocket | Bidirectional connection | Server pushes on event | Very frequent updates |
```

### 9.2 Webhook Flow

```markdown
## Webhook Flow

```
┌──────────┐                    ┌──────────┐                    ┌──────────┐
│  Server  │                    │  Webhook │                    │  Client  │
│   (API)  │                    │ Endpoint │                    │ (Your App)│
└────┬─────┘                    └────┬─────┘                    └────┬─────┘
     │                               │                               │
     │  1. User sets up webhook      │                               │
     │  POST /webhooks {url, events} │                               │
     │──────────────────────────────►│                               │
     │                               │                               │
     │  2. Event occurs              │                               │
     │  (e.g., order placed)         │                               │
     │                               │                               │
     │  3. Server sends webhook      │                               │
     │  POST https://client/webhook  │                               │
     │──────────────────────────────┼──────────────────────────────►│
     │                               │                               │
     │                               │  4. Client responds           │
     │  200 OK (or 2xx)             │◄──────────────────────────────│
     │◄─────────────────────────────┼──────────────────────────────│
     │                               │                               │
     │  (If failed: retry with backoff)                               │
```

### 9.3 Webhook Payload Template

```markdown
## Webhook Payload Format

```json
{
  "id": "evt_1234567890",
  "type": "order.created",
  "timestamp": "2026-05-02T12:00:00Z",
  "api_version": "v1",
  "data": {
    "object": {
      "id": "ord_abc123",
      "customer_id": "cus_123",
      "total": 99.99,
      "currency": "USD",
      "status": "pending",
      "created_at": "2026-05-02T12:00:00Z"
    }
  }
}
```

### Webhook Event Types

| Category | Events | Description |
|----------|--------|-------------|
| Orders | `order.created`, `order.updated`, `order.cancelled`, `order.completed` | Order lifecycle |
| Payments | `payment.succeeded`, `payment.failed`, `payment.refunded` | Payment events |
| Users | `user.created`, `user.updated`, `user.deleted` | User lifecycle |
| Products | `product.created`, `product.stock_low`, `product.out_of_stock` | Product events |
| Sessions | `session.started`, `session.ended` | User sessions |
```

### 9.4 Webhook Security

```markdown
## Webhook Security

### Signature Verification
```json
// Header sent with webhook
X-Webhook-Signature: sha256=abc123...
X-Webhook-Timestamp: 1746192000

// How to verify (pseudocode)
payload = request.body
timestamp = request.headers['X-Webhook-Timestamp']
signature = request.headers['X-Webhook-Signature']

// Check timestamp is recent (prevent replay)
if (now - timestamp > 300) reject()

// Verify signature
expected = hmac_sha256(payload, webhook_secret)
if (signature !== expected) reject()
```

### Secret Rotation
| Strategy | Description |
|----------|-------------|
| Static secret | Single secret, rotate manually |
| Rotating secrets | New secret, old still valid for grace period |
| Per-endpoint secrets | Different secret per webhook endpoint |

### Security Checklist
- [ ] Verify signature on every webhook
- [ ] Reject requests older than 5 minutes
- [ ] Use HTTPS endpoint
- [ ] Respond within 30 seconds or queue for async processing
- [ ] Log all webhook deliveries for debugging
- [ ] Implement idempotency (same event may be delivered multiple times)
```

### 9.5 Webhook Discovery Template

```markdown
## Webhook Analysis

| Event | Handler | Trigger Condition | Payload Keys |
|-------|---------|-------------------|--------------|
| `order.created` | `webhook.go:42` | New order placed | `id`, `customer_id`, `total` |
| `order.cancelled` | `webhook.go:55` | Order cancelled by user | `id`, `reason` |
| `payment.succeeded` | `payment.go:20` | Payment confirmed | `id`, `order_id`, `amount` |

## Webhook Endpoints (Receiver Side)

| Endpoint | Method | Auth | Purpose |
|----------|--------|------|---------|
| /webhooks/stripe | POST | Signature | Handle Stripe events |
| /webhooks/github | POST | Secret | Handle GitHub events |

## Idempotency Keys
```go
// Store processed event IDs to prevent double-processing
processed := redis.Get("webhook:" + eventID)
if processed != nil {
    return 200  // Already processed
}
processEvent(event)
redis.Set("webhook:" + eventID, "1", 24*time.Hour)
```
```

---

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
    "action": "subscribe",
    "order_id": "ord_123"
  }
}

// Event from server
{
  "type": "event",
  "channel": "orders",
  "payload": {
    "event": "order.updated",
    "data": {"id": "ord_123", "status": "shipped"}
  }
}

// Ping/Pong
{"type": "ping"}
{"type": "pong"}
```
```

### 10.5 WebSocket Discovery Template

```markdown
## WebSocket Analysis

### Connection Endpoint
| URI | Protocol | Auth | Notes |
|-----|----------|------|-------|
| wss://api.example.com/socket | wss | Token in first message | First msg contains auth |

### Channels/Topics
| Channel | Subscribe | Events Sent |
|---------|-----------|-------------|
| `orders` | `{"action": "subscribe", "channel": "orders"}` | order.created, order.updated, order.cancelled |
| `users/{id}` | `{"action": "subscribe", "channel": "users/123"}` | user.updated, user.deleted |
| `notifications` | `{"action": "subscribe", "channel": "notifications"}` | notification.created |

### Message Flow
```
1. Connect to wss://api.example.com/socket
2. Send auth: {"type": "auth", "token": "jwt_xxx"}
3. Server responds: {"type": "auth_ok"}
4. Subscribe to channel: {"action": "subscribe", "channel": "orders"}
5. Receive events: {"type": "event", "channel": "orders", "data": {...}}
```

### Heartbeat/Keepalive
```json
// Client sends ping every 30s
{"type": "ping"}

// Server responds
{"type": "pong"}

// Or use WebSocket ping/pong frames (0x9/0xA)
```
```

---

## 11. Server-Sent Events (SSE)

### 11.1 SSE Concepts

```markdown
## When to Use SSE vs WebSockets

| Feature | SSE | WebSocket |
|---------|-----|-----------|
| Direction | Server → Client only | Bidirectional |
| Complexity | Simple | More complex |
| Browser support | Native | Requires library |
| Automatic reconnection | Yes (built-in) | Manual |
| HTTP/2 multiplexing | Yes | Yes |
| firewalls/proxies | Usually works | May be blocked |
| Binary data | No (text only) | Yes |

## Use Cases
- **SSE**: Notifications, live feeds, progress updates, dashboards
- **WebSocket**: Chat, collaborative editing, gaming, bidirectional sync
```

### 11.2 SSE Format

```markdown
## SSE Response Format

```
Content-Type: text/event-stream
Cache-Control: no-cache
Connection: keep-alive

event: order_update
id: 123
data: {"order_id": "ord_123", "status": "shipped"}

event: notification
id: 124
data: {"message": "Your order has shipped!"}

: This is a comment

event: heartbeat
id: 125
data: {"timestamp": 1746192000}
```

## SSE Fields

| Field | Description |
|-------|-------------|
| `event` | Event type name (optional) |
| `data` | Event data (can have multiple lines) |
| `id` | Event ID (for resumption) |
| `retry` | Reconnection time in ms |
| `:` | Comment (ignored) |

## Multi-line Data

```
event: message
data: First line
data: Second line
data: Third line

// Becomes: "First line\nSecond line\nThird line"
```
```

### 11.3 SSE Discovery Template

```markdown
## SSE Analysis

### Endpoint
| URL | Auth | Description |
|-----|------|-------------|
| GET /events | Bearer token | Main SSE endpoint |
| GET /events/orders | Bearer token | Order-specific events |

### Event Types
| Event | Payload | Trigger |
|-------|---------|---------|
| `order_update` | `{order_id, status}` | Order status change |
| `notification` | `{message, type}` | New notification |
| `heartbeat` | `{timestamp}` | Keep-alive every 30s |

### Client Implementation
```javascript
const eventSource = new EventSource('/events?token=' + token);

eventSource.addEventListener('order_update', (e) => {
    const data = JSON.parse(e.data);
    console.log('Order update:', data);
});

eventSource.onerror = () => {
    console.error('SSE connection error');
    // Automatic reconnection will happen
};
```
```

---

## 12. GraphQL

### 12.1 GraphQL vs REST

```markdown
## Comparison

| Aspect | REST | GraphQL |
|--------|------|---------|
| Endpoints | Multiple | Single `/graphql` |
| Data fetching | Fixed response | Client specifies fields |
| Over-fetching | Common | Avoided |
| Under-fetching | Multiple round trips | Single request |
| Caching | HTTP caching | No native caching |
| Documentation | Separate | Built-in (introspection) |
| Learning curve | Lower | Higher |

## When GraphQL Makes Sense
- Complex/nested data relationships
- Mobile apps (bandwidth sensitive)
- Multiple clients with different data needs
- Rapid iteration on UI
```

### 12.2 GraphQL Request Format

```markdown
## Query (Read)

```graphql
query GetUser($id: ID!) {
  user(id: $id) {
    id
    name
    email
    orders(first: 10) {
      edges {
        node {
          id
          total
          status
        }
      }
    }
  }
}
```

### Variables
```json
{
  "id": "123"
}
```

### Response
```json
{
  "data": {
    "user": {
      "id": "123",
      "name": "John",
      "email": "john@example.com",
      "orders": {
        "edges": [...]
      }
    }
  }
}
```

## Mutation (Write)

```graphql
mutation CreateOrder($input: CreateOrderInput!) {
  createOrder(input: $input) {
    id
    total
    status
    errors {
      field
      message
    }
  }
}
```

### Variables
```json
{
  "input": {
    "customerId": "123",
    "items": [{"productId": "p1", "quantity": 2}]
  }
}
```
```

### 12.3 GraphQL Schema Template

```markdown
## GraphQL Schema Analysis

### Types
```graphql
type User {
  id: ID!
  name: String!
  email: String!
  orders: OrderConnection!
  createdAt: DateTime!
}

type Order {
  id: ID!
  customer: User!
  items: [OrderItem!]!
  total: Float!
  status: OrderStatus!
  createdAt: DateTime!
}

enum OrderStatus {
  PENDING
  PROCESSING
  SHIPPED
  DELIVERED
  CANCELLED
}

type Query {
  user(id: ID!): User
  users(limit: Int, offset: Int): UserConnection!
  order(id: ID!): Order
}

type Mutation {
  createUser(input: CreateUserInput!): User!
  createOrder(input: CreateOrderInput!): Order!
  cancelOrder(id: ID!): Order!
}

input CreateOrderInput {
  customerId: ID!
  items: [OrderItemInput!]!
}
```

### Operations Discovery

| Operation | Type | Variables | Purpose |
|-----------|------|-----------|---------|
| `getUser` | Query | `id` | Fetch user with orders |
| `listUsers` | Query | `limit`, `offset` | Paginated user list |
| `createOrder` | Mutation | `input` | Create new order |
| `cancelOrder` | Mutation | `id` | Cancel an order |

### Fields Analysis

| Field | Type | Resolver | Notes |
|-------|------|----------|-------|
| `user.orders` | Connection | `ordersByUserId()` | Lazy load |
| `order.customer` | User | `getUser()` | Join |
| `order.total` | Float | Computed | Sum of items |
```
```

---

## 13. gRPC

### 13.1 gRPC Concepts

```markdown
## When to Use gRPC

| Feature | REST | gRPC |
|---------|------|------|
| Protocol | HTTP/1.1 or HTTP/2 | HTTP/2 |
| Format | JSON, XML | Protocol Buffers (binary) |
| Streaming | Limited | Native support |
| Code generation | OpenAPI/Swagger | .proto files |
| Browser support | Universal | Requires grpc-web |
| Use case | Public APIs, mobile | Internal microservices |

## gRPC vs REST Performance
- gRPC is 5-10x faster for same payload (binary vs JSON)
- Smaller message sizes (Protocol Buffers)
- Built-in streaming (no polling)
```

### 13.2 Protocol Buffer Schema

```markdown
## .proto File Template

```protobuf
syntax = "proto3";

package orders;

service OrderService {
  rpc GetOrder(GetOrderRequest) returns (Order);
  rpc ListOrders(ListOrdersRequest) returns (OrderList);
  rpc CreateOrder(CreateOrderRequest) returns (Order);
  rpc CancelOrder(CancelOrderRequest) returns (Order);
  rpc StreamOrders(StreamOrdersRequest) returns (stream Order);  // Server streaming
}

message Order {
  string id = 1;
  string customer_id = 2;
  double total = 3;
  OrderStatus status = 4;
  repeated OrderItem items = 5;
  google.protobuf.Timestamp created_at = 6;
}

message OrderItem {
  string product_id = 1;
  int32 quantity = 2;
  double price = 3;
}

enum OrderStatus {
  PENDING = 0;
  PROCESSING = 1;
  SHIPPED = 2;
  DELIVERED = 3;
  CANCELLED = 4;
}

message GetOrderRequest {
  string id = 1;
}

message ListOrdersRequest {
  int32 page_size = 1;
  string page_token = 2;
}
```
```

### 13.3 gRPC Patterns

```markdown
## Unary RPC (REST-like)

```protobuf
rpc GetOrder(GetOrderRequest) returns (Order);
// Client sends one request, server returns one response
```

## Server Streaming (SSE-like)

```protobuf
rpc StreamOrders(StreamOrdersRequest) returns (stream Order);
// Client sends one request, server streams multiple responses
```

## Client Streaming (Upload)

```protobuf
rpc UploadOrderData(stream OrderChunk) returns (Order);
// Client streams multiple chunks, server returns one response
```

## Bidirectional Streaming (WebSocket-like)

```protobuf
rpc ProcessOrders(stream OrderRequest) returns (stream OrderResponse);
// Both client and server stream
```

## gRPC Discovery Template

| Pattern | REST Equivalent | Use Case |
|---------|-----------------|----------|
| Unary | GET/POST | Simple requests |
| Server streaming | SSE | Live feeds |
| Client streaming | File upload | Large uploads |
| Bidirectional | WebSocket | Chat, collaborative |
```

---

## 14. Other Protocols & Patterns

### 14.1 Long Polling

```markdown
## Long Polling (Comet)

```
┌──────────┐                    ┌──────────┐
│  Client  │                    │  Server  │
└────┬─────┘                    └────┬─────┘
     │                               │
     │  1. GET /events (long poll)   │
     │──────────────────────────────►│
     │                               │ (wait for event or timeout)
     │                               │
     │  2. Event occurs              │
     │◄──────────────────────────────│
     │  200: {event: "order.created"}
     │                               │
     │  3. Immediately request again │
     │──────────────────────────────►│
     │       (repeat)                │
```

### Comparison
| Aspect | Polling | Long Polling | WebSocket | SSE |
|--------|---------|--------------|-----------|-----|
| Latency | High | Low | Lowest | Low |
| Server load | High | Medium | Low | Low |
| Complexity | Low | Medium | High | Low |
```

### 14.2 Webhook Signature Verification Patterns

```markdown
## HMAC-SHA256 (Most Common)

```python
# Server side (generates signature)
import hmac, hashlib, time

def sign_webhook(payload: bytes, secret: str) -> str:
    timestamp = str(int(time.time()))
    message = timestamp + "." + payload.decode()
    signature = hmac.new(
        secret.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()
    return f"t={timestamp},v1={signature}"

# Client side (verifies signature)
def verify_webhook(payload: bytes, header: str, secret: str) -> bool:
    parts = dict(p.split("=", 1) for p in header.split(","))
    timestamp, signature = parts["t"], parts["v1"]

    # Check timestamp (prevent replay)
    if abs(time.time() - int(timestamp)) > 300:
        return False

    # Verify signature
    message = timestamp + "." + payload.decode()
    expected = hmac.new(
        secret.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(signature, expected)
```

## RSA Signature (GitHub, Shopify)

```python
# GitHub uses RSA-SHA256
import base64, hashlib, rsa, binascii

def verify_github_webhook(payload: bytes, signature: str, pub_key_pem: str) -> bool:
    decoded_sig = base64.b64decode(signature.split("=")[1])
    pub_key = rsa.PublicKey.load_pkcs1(pem_bytes)
    digest = hashlib.sha256(payload).digest()
    try:
        rsa.verify(digest, decoded_sig, pub_key)
        return True
    except rsa.VerificationError:
        return False
```
```

### 14.3 API Key Authentication Patterns

```markdown
## API Key Placement

| Header | Example | Use Case |
|--------|---------|----------|
| X-API-Key | `X-API-Key: sk_live_xxxx` | Custom header |
| Authorization | `Authorization: ApiKey sk_live_xxxx` | Generic header |
| Query param | `/api?api_key=sk_live_xxxx` | When headers not possible |

## HMAC-Based Request Signing (AWS, Slack)

```python
# Slack signing secret
import hmac, hashlib, time, base64

def verify_slack_request(
    body: str,
    timestamp: str,
    signature: str,
    signing_secret: str
) -> bool:
    # Check timestamp (prevent replay)
    if abs(time.time() - int(timestamp)) > 300:
        return False

    # Create signing base
    version = "v0"
    signing_base = f"{version}:{timestamp}:{body}"

    # Calculate signature
    my_signature = "v0=" + hmac.new(
        signing_secret.encode(),
        signing_base.encode(),
        hashlib.sha256
    ).hexdigest()

    # Constant-time comparison
    return hmac.compare_digest(my_signature, signature)
```
```

### 14.4 OAuth 2.0 Flows

```markdown
## OAuth 2.0 Flow Types

| Grant | Use Case | Diagram |
|-------|----------|---------|
| Authorization Code | Web apps with server | Browser → Auth → Code → Token |
| PKCE | Mobile/SPA (no secrets) | Like Auth Code but with verifier |
| Client Credentials | Server-to-server | No user, just client_id/secret |
| Refresh Token | Keep sessions alive | Refresh token → New access token |
| Device Code | CLI tools, smart TVs | User visits URL, device polls |

## Authorization Code Flow

```
1. User clicks "Login" on Client App
   Client → Browser → https://auth.example.com/authorize?
     client_id=app_id
     redirect_uri=https://app.com/callback
     response_type=code
     scope=read write
     state=random_state

2. User authenticates, grants permission
   Browser → https://app.com/callback?code=auth_code&state=random_state

3. Client exchanges code for tokens
   Client → POST https://auth.example.com/token
   { code, client_id, client_secret, redirect_uri }

4. Auth server returns tokens
   { access_token, refresh_token, expires_in }
```

## Token Refresh

```
Request:
POST /oauth/token
{
  "grant_type": "refresh_token",
  "refresh_token": "refresh_xxx",
  "client_id": "app_id",
  "client_secret": "app_secret"
}

Response:
{
  "access_token": "new_access_xxx",
  "refresh_token": "new_refresh_xxx",  // Optional rotation
  "expires_in": 3600
}
```
```

---

## 15. Protocol Decision Matrix

```markdown
## Choosing the Right Protocol

| Need | Best Choice | Alternative |
|------|-------------|-------------|
| REST API for external clients | REST/JSON | GraphQL |
| Internal microservice calls | gRPC | REST |
| Real-time updates to browser | WebSocket | SSE |
| Server → Browser notifications | SSE | WebSocket |
| Webhook to external service | HTTP POST + signature | - |
| Mobile real-time | WebSocket | SSE |
| CLI tool → API | REST | - |
| Streaming large data | gRPC streaming | REST chunked |
| Complex query with relations | GraphQL | REST (may need multiple calls) |

## Bandwidth Comparison

| Format | Example Size | Relative |
|--------|--------------|----------|
| JSON | 1,234 bytes | 1.0x |
| MessagePack | 856 bytes | 0.69x |
| Protocol Buffers | 523 bytes | 0.42x |
| FlatBuffers | 456 bytes | 0.37x |
```

---

## 16. Integration Planning

### 9.1 API Integration Checklist

```markdown
## Pre-Integration Checklist

- [ ] All endpoints documented
- [ ] Request/response formats verified
- [ ] Authentication flow understood
- [ ] Error codes cataloged
- [ ] Rate limits identified
- [ ] Pagination behavior verified
- [ ] Filtering options noted
- [ ] Timeout values identified
```

### 9.2 Client Implementation Task

```markdown
## Task: Implement API Client for Orders

**Type:** API Integration
**Priority:** P1

### Endpoints to Implement

| Method | Path | Purpose |
|--------|------|---------|
| GET | /api/v1/orders | List orders (paginated) |
| GET | /api/v1/orders/{id} | Get single order |
| POST | /api/v1/orders | Create order |
| DELETE | /api/v1/orders/{id} | Cancel order |

### Implementation Requirements

1. **Base Client**
   - Configure base URL
   - Add auth header to all requests
   - Handle rate limiting (429 responses)
   - Retry on 5xx errors (max 3 retries)

2. **List Orders**
   - Support pagination (page, per_page)
   - Support filtering (status, customer_id)
   - Support sorting (created_at:desc)
   - Return typed Order structs

3. **Get Order**
   - Accept order ID
   - Return full Order with line items

4. **Create Order**
   - Accept OrderInput struct
   - Return created Order
   - Handle 422 validation errors

5. **Cancel Order**
   - Accept order ID
   - Return success/no content
   - Handle 404 (already cancelled)

### Types

```go
type Order struct {
    ID        int64     `json:"id"`
    CustomerID int64    `json:"customerId"`
    Status    string    `json:"status"`
    Total     float64   `json:"total"`
    Items     []Item    `json:"items"`
    CreatedAt time.Time `json:"createdAt"`
}

type OrderInput struct {
    CustomerID int64   `json:"customerId"`
    Items     []ItemInput `json:"items"`
}

type ListOptions struct {
    Page    int
    PerPage int
    Status  string
}
```

### Acceptance Criteria
- [ ] All CRUD operations work
- [ ] Auth header automatically added
- [ ] 429 triggers rate limit wait
- [ ] 5xx triggers retry
- [ ] Types match API responses
- [ ] Pagination works correctly
```

---

## Validation Checklist

Before declaring API analysis complete:

- [ ] All endpoints discovered and documented
- [ ] HTTP methods verified
- [ ] Request formats confirmed
- [ ] Response formats confirmed
- [ ] Auth method identified
- [ ] Auth flow traced
- [ ] Error codes cataloged
- [ ] Rate limits identified
- [ ] Pagination pattern verified
- [ ] Filtering options documented

## Reference

See ui-ux-analyzer for UI counterparts to API flows.