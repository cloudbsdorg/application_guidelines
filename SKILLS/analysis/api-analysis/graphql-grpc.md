---
name: api-analyzer-graphql
description: GraphQL and gRPC analysis — schemas, queries, mutations, subscriptions, proto files, RPC patterns.
---

# API Analyzer — GraphQL & gRPC

## 12. GraphQL

### 12.1 GraphQL vs REST

```markdown
## Comparison

| Aspect | REST | GraphQL |
|--------|------|---------|
| Data fetching | Multiple endpoints | Single endpoint |
| Over-fetching | Often returns too much | Exactly what client needs |
| Under-fetching | May need multiple requests | Single request |
| Versioning | New version /v2 | No versioning (additive) |
| Caching | HTTP caching | No native caching |
| Error handling | HTTP status codes | 200 + errors array |
| Learning curve | Easy | Steeper |
| Documentation | Swagger/OpenAPI | Schema introspection |
```

### When GraphQL Makes Sense

```markdown
| Good for GraphQL | Bad for GraphQL |
|-----------------|-----------------|
| Mobile apps (bandwidth) | Simple CRUD apps |
| Complex nested data | Public APIs with caching |
| Multiple clients (web, mobile, IoT) | Microservices (use REST/gRPC) |
| Rapid iteration | Static content sites |
| Analytics dashboards | Microservices communication |
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
    posts(first: 10) {
      edges {
        node {
          id
          title
          publishedAt
        }
      }
      pageInfo {
        hasNextPage
        endCursor
      }
    }
  }
}

# Variables:
{
  "id": "123"
}
```

### Variables

```graphql
query GetUsers($limit: Int, $offset: Int, $filter: UserFilter) {
  users(limit: $limit, offset: $offset, filter: $filter) {
    totalCount
    edges {
      node {
        id
        name
        email
      }
    }
  }
}

# Variables:
{
  "limit": 20,
  "offset": 0,
  "filter": {
    "role": "admin",
    "active": true
  }
}
```

### Response

```json
{
  "data": {
    "user": {
      "id": "123",
      "name": "Alice",
      "email": "alice@example.com",
      "posts": {
        "edges": [
          {
            "node": {
              "id": "456",
              "title": "First Post",
              "publishedAt": "2026-05-01T10:00:00Z"
            }
          }
        ],
        "pageInfo": {
          "hasNextPage": true,
          "endCursor": "cursor_abc"
        }
      }
    }
  },
  "errors": [
    {
      "message": "Field 'posts' is forbidden for role 'guest'",
      "locations": [{ "line": 6, "column": 5 }],
      "path": ["user", "posts"],
      "extensions": {
        "code": "FORBIDDEN",
        "field": "posts"
      }
    }
  ]
}
```

## Mutation (Write)

```graphql
mutation CreatePost($input: CreatePostInput!) {
  createPost(input: $input) {
    post {
      id
      title
      content
      author {
        id
        name
      }
    }
    errors {
      field
      message
    }
  }
}

# Variables:
{
  "input": {
    "title": "My New Post",
    "content": "Post content here...",
    "authorId": "123"
  }
}
```

### Variables

```graphql
mutation UpdateUser($id: ID!, $input: UpdateUserInput!) {
  updateUser(id: $id, input: $input) {
    user {
      id
      name
      email
    }
    errors {
      field
      message
    }
  }
}

# Variables:
{
  "id": "123",
  "input": {
    "name": "Alice Updated",
    "email": "alice.new@example.com"
  }
}
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
  role: UserRole!
  createdAt: DateTime!
  updatedAt: DateTime!
  posts: PostConnection!
  profile: Profile
}

type Post {
  id: ID!
  title: String!
  slug: String!
  content: String!
  status: PostStatus!
  author: User!
  tags: [Tag!]!
  createdAt: DateTime!
  publishedAt: DateTime
}

enum UserRole {
  ADMIN
  EDITOR
  AUTHOR
  GUEST
}

enum PostStatus {
  DRAFT
  PUBLISHED
  ARCHIVED
}

union SearchResult = User | Post | Comment

type Query {
  user(id: ID!): User
  users(filter: UserFilter, limit: Int, offset: Int): UserConnection!
  post(slug: String!): Post
  posts(filter: PostFilter, limit: Int, offset: Int): PostConnection!
  search(query: String!): [SearchResult!]!
  me: User
}

type Mutation {
  createPost(input: CreatePostInput!): CreatePostPayload!
  updatePost(id: ID!, input: UpdatePostInput!): UpdatePostPayload!
  deletePost(id: ID!): DeletePostPayload!
  publishPost(id: ID!): PublishPostPayload!
}

input CreatePostInput {
  title: String!
  content: String!
  authorId: ID!
  tagIds: [ID!]
}

input UserFilter {
  role: UserRole
  active: Boolean
  search: String
}

type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type UserEdge {
  node: User!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}
```

### Operations Discovery

```markdown
## Query Operations

| Operation | Type | Variables | Description |
|----------|------|----------|-------------|
| `user(id)` | query | `id: ID!` | Get user by ID |
| `users(filter, limit, offset)` | query | `UserFilter, Int, Int` | List users |
| `post(slug)` | query | `slug: String!` | Get post by slug |
| `search(query)` | query | `query: String!` | Search all types |

## Mutation Operations

| Operation | Type | Variables | Description |
|----------|------|----------|-------------|
| `createPost(input)` | mutation | `CreatePostInput!` | Create new post |
| `updatePost(id, input)` | mutation | `ID!, UpdatePostInput!` | Update post |
| `deletePost(id)` | mutation | `id: ID!` | Delete post |
| `publishPost(id)` | mutation | `id: ID!` | Publish draft |

## Subscriptions

```graphql
type Subscription {
  postCreated: Post!
  postUpdated(id: ID!): Post!
  postDeleted: Post!
  messageReceived(userId: ID!): Message!
}
```

### Fields Analysis

| Field | Type | Resolver | Complexity |
|-------|------|----------|-------------|
| `user.posts` | PostConnection | `postsByUser(userId)` | N+1 risk |
| `post.author` | User | `userById(post.authorId)` | Simple |
| `user.profile` | Profile | `nullable, lazy` | Nullable |

## 13. gRPC

### 13.1 gRPC Concepts

```markdown
## When to Use gRPC

| Use Case | Why gRPC |
|----------|----------|
| Microservices | Low latency, bidirectional streaming |
| Mobile apps | Bandwidth efficient, code generation |
| IoT | Small payloads, real-time |
| Polyglot services | Multi-language support |
| Internal APIs | Fast, type-safe |

## gRPC vs REST Performance

| Aspect | REST/JSON | gRPC/protobuf |
|--------|----------|---------------|
| Payload size | Large (JSON text) | Small (binary) |
| Parsing speed | Slow (text) | Fast (binary) |
| Code generation | OpenAPI/Swagger | Proto compiler |
| Browser support | Universal | Requires proxy |
| Streaming | Limited | Native support |
```

### 13.2 Protocol Buffer Schema

```protobuf
// .proto File Template

syntax = "proto3";

package user.v1;

option go_package = "github.com/example/gen/go/user/v1";
option java_package = "com.example.user.v1";
option java_multiple_files = true;

// Service definition
service UserService {
  // Unary (REST-like)
  rpc GetUser(GetUserRequest) returns (User);
  rpc CreateUser(CreateUserRequest) returns (CreateUserResponse);
  rpc UpdateUser(UpdateUserRequest) returns (User);
  rpc DeleteUser(DeleteUserRequest) returns (Empty);

  // Server streaming (SSE-like)
  rpc ListUsers(ListUsersRequest) returns (stream User);

  // Client streaming (upload)
  rpc BatchCreateUsers(stream CreateUserRequest) returns (BatchCreateResponse);

  // Bidirectional streaming (WebSocket-like)
  rpc StreamUserEvents(StreamUserEventsRequest) returns (stream UserEvent);
}

// Messages
message User {
  string id = 1;
  string name = 2;
  string email = 3;
  UserRole role = 4;
  int64 created_at = 5;
}

enum UserRole {
  USER_ROLE_UNSPECIFIED = 0;
  USER_ROLE_ADMIN = 1;
  USER_ROLE_USER = 2;
}

message GetUserRequest {
  string id = 1;
}

message CreateUserRequest {
  string name = 1;
  string email = 2;
  UserRole role = 3;
}

message CreateUserResponse {
  User user = 1;
}

message UpdateUserRequest {
  string id = 1;
  string name = 2;
  string email = 3;
}

message DeleteUserRequest {
  string id = 1;
}

message ListUsersRequest {
  int32 page_size = 1;
  string page_token = 2;
}

message StreamUserEventsRequest {
  string user_id = 1;
  repeated string event_types = 2;
}

message UserEvent {
  string event_id = 1;
  string event_type = 2;
  User user = 3;
  int64 timestamp = 4;
}

message Empty {}
```

### 13.3 gRPC Patterns

```markdown
## Unary RPC (REST-like)

```bash
# Request
rpc GetUser(GetUserRequest) returns (User);

# HTTP mapping
POST /user.v1.UserService/GetUser
Content-Type: application/grpc+proto

# Response
HTTP/2 200
Content-Type: application/grpc+proto
grpc-status: 0 (OK)
```

## Server Streaming (SSE-like)

```bash
# Request
rpc ListUsers(ListUsersRequest) returns (stream User);

# Client sends one request, server streams multiple responses
# Used for: List operations, real-time updates, notifications
```

## Client Streaming (Upload)

```bash
# Request
rpc BatchCreateUsers(stream CreateUserRequest) returns (BatchCreateResponse);

# Client streams multiple requests, server sends one response
# Used for: Batch operations, file uploads
```

## Bidirectional Streaming (WebSocket-like)

```bash
# Request
rpc StreamUserEvents(StreamUserEventsRequest) returns (stream UserEvent);

# Both client and server stream independently
# Used for: Chat, collaborative editing, real-time games
```

### 13.4 gRPC Discovery Template

```markdown
## gRPC API Analysis

### Service
| Property | Value |
|----------|-------|
| Package | `user.v1` |
| Service | `UserService` |
| Proto file | `user/v1/service.proto` |

### Methods
| Method | Type | Request | Response | Description |
|-------|------|---------|---------|-------------|
| `GetUser` | Unary | `GetUserRequest` | `User` | Get user by ID |
| `CreateUser` | Unary | `CreateUserRequest` | `CreateUserResponse` | Create user |
| `ListUsers` | Server Stream | `ListUsersRequest` | `stream User` | List users |
| `BatchCreateUsers` | Client Stream | `stream CreateUserRequest` | `BatchCreateResponse` | Batch create |
| `StreamUserEvents` | Bidirectional | `stream StreamUserEventsRequest` | `stream UserEvent` | Real-time events |

### Message Types
| Type | Fields | Description |
|------|--------|-------------|
| `User` | id, name, email, role, created_at | User entity |
| `GetUserRequest` | id | Get user request |
| `CreateUserRequest` | name, email, role | Create user request |

### Authentication
| Method | Implementation |
|-------|---------------|
| Token | Metadata `authorization: Bearer <token>` |
| TLS | mTLS for service-to-service |
```

## 14. Other Protocols & Patterns

### 14.1 Long Polling

```markdown
## Long Polling (Comet)

### Flow
```
Client ───► Server
           │
           │ 1. GET /events (long timeout)
           │◄── 200 OK + event (or timeout)
           │
           │ 2. GET /events (immediately)
           │◄── 200 OK + event
           │
           │ ... repeat
```

### Comparison

| Aspect | WebSocket | SSE | Long Polling |
|--------|----------|-----|--------------|
| Browser support | All | Modern | All |
| Server complexity | Medium | Low | High |
| Real-time | Yes | Yes | Yes (delay) |
| Reconnection | Manual | Auto | Auto |
| Scalability | Medium | Easy | Hard |
| Proxy/firewall | Issues | Issues | Usually works |
```

### 14.2 Webhook Signature Verification Patterns

```markdown
## HMAC-SHA256 (Most Common)

```javascript
// Verify webhook signature
const crypto = require('crypto');

function verifyWebhook(req, secret) {
  const signature = req.headers['x-signature-256'];
  const timestamp = req.headers['x-signature-timestamp'];
  
  // Check timestamp (prevent replay attacks)
  const age = Date.now() - parseInt(timestamp);
  if (age > 300000) return false; // 5 min max
  
  // Create signature base
  const base = `${timestamp}.${req.rawBody}`;
  
  // Calculate expected
  const expected = 'sha256=' + crypto
    .createHmac('sha256', secret)
    .update(base)
    .digest('hex');
  
  // Secure compare
  return crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(expected)
  );
}
```

## RSA Signature (GitHub, Shopify)

```javascript
const crypto = require('crypto');

function verifyRSASignature(req, publicKey) {
  const signature = Buffer.from(
    req.headers['x-hub-signature-256'].replace('sha256=', ''),
    'hex'
  );
  
  const verify = crypto.createVerify('RSA-SHA256');
  verify.update(req.rawBody);
  
  return verify.verify(publicKey, signature);
}
```

### 14.3 API Key Authentication Patterns

```markdown
## API Key Placement

| Method | Header | Use |
|--------|--------|-----|
| Header | `X-API-Key: <key>` | Most common |
| Header | `Authorization: ApiKey <key>` | Explicit |
| Query | `?api_key=<key>` | For GET requests |
| Basic | `Authorization: Basic <base64>` | Legacy |

## HMAC-Based Request Signing (AWS, Slack)

See `authentication.md` sub-skill for full AWS v4 signing example.
```

## 15. Protocol Decision Matrix

```markdown
## Choosing the Right Protocol

| Use Case | Protocol | Reason |
|----------|----------|--------|
| Public REST API | REST/JSON | Simple, cacheable, universal |
| Internal microservices | gRPC | Fast, type-safe, streaming |
| Real-time bidirectional | WebSocket | Full duplex, low latency |
| Server → Client only | SSE | Simple, auto-reconnect |
| Mobile app (bandwidth) | GraphQL | Exactly needed data |
| IoT devices | gRPC | Small binary, streaming |
| Third-party webhooks | REST + HMAC | Simple, secure |
| Long-running tasks | REST + async | Polling or webhooks |

## Bandwidth Comparison

| Protocol | 100 requests | 1MB payload |
|---------|-------------|--------------|
| REST/JSON | ~500KB | ~1MB |
| gRPC/protobuf | ~50KB | ~200KB |
| GraphQL | ~100KB | ~300KB |
| WebSocket | ~10KB | ~200KB + frames |
```

## 16. Integration Planning

### Pre-Integration Checklist

- [ ] API specification obtained (OpenAPI, Proto, Schema)
- [ ] Authentication method identified
- [ ] Rate limits documented
- [ ] Error responses cataloged
- [ ] Pagination strategy confirmed
- [ ] Webhook endpoints identified (if applicable)
- [ ] Sandbox/test environment available
- [ ] Rate limits understood

### Integration Test Cases

```markdown
## Task: Implement API Client for Orders

### Endpoints to Implement
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /orders | List orders |
| GET | /orders/:id | Get order |
| POST | /orders | Create order |
| PATCH | /orders/:id | Update order |
| DELETE | /orders/:id | Cancel order |

### Implementation Requirements

```typescript
interface OrderClient {
  // List orders with pagination
  listOrders(params: ListOrdersParams): Promise<OrderList>;
  
  // Get single order
  getOrder(id: string): Promise<Order>;
  
  // Create new order
  createOrder(input: CreateOrderInput): Promise<Order>;
  
  // Update existing order
  updateOrder(id: string, input: UpdateOrderInput): Promise<Order>;
  
  // Cancel order
  cancelOrder(id: string): Promise<void>;
}

interface ListOrdersParams {
  pageSize?: number;
  pageToken?: string;
  status?: OrderStatus;
  customerId?: string;
}
```

### Types

```typescript
interface Order {
  id: string;
  status: OrderStatus;
  customer: Customer;
  items: OrderItem[];
  total: Money;
  createdAt: string;
  updatedAt: string;
}

interface OrderItem {
  id: string;
  productId: string;
  quantity: number;
  price: Money;
}

type OrderStatus = 'pending' | 'confirmed' | 'shipped' | 'delivered' | 'cancelled';

interface Money {
  amount: number;
  currency: string;
}
```

### Acceptance Criteria

- [ ] All 5 endpoints implemented
- [ ] Authentication working (Bearer token)
- [ ] Error handling for all HTTP status codes
- [ ] Retry logic for 429 (rate limit)
- [ ] Pagination handling (hasNextPage)
- [ ] Timeout configuration (30s default)
- [ ] Request/response logging
- [ ] Unit tests (>80% coverage)
```
