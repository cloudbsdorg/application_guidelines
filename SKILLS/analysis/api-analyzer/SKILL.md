---
name: api-analyzer
description: >-
  Document a REST or HTTP API - endpoints, request/response shapes,
  authentication, pagination, rate limits, webhooks. Use when analysing an API
  for porting, rewriting, or integration, when asked about REST, HTTP,
  endpoints, OpenAPI, GraphQL, gRPC, WebSockets, or SSE, or before writing a
  client against a service you did not build.
keywords:
  - API
  - REST
  - endpoint
  - HTTP
  - OpenAPI
  - Swagger
  - GraphQL
  - gRPC
  - WebSocket
  - SSE
  - webhook
---

# Skill: api-analyzer

**Purpose:** Systematically analyze REST APIs and web services to understand endpoints, request/response formats, authentication, and data flow.

**Triggers:** When analyzing an API for porting, rewriting, or integration planning.

---

## Loading Instructions

This skill is **modular**. Load only the sub-skill you need:

| Sub-Skill | When to Load |
|-----------|--------------|
| [http-fundamentals.md](./http-fundamentals.md) | HTTP methods, status codes, headers, content-types, connection management |
| [rest-endpoints.md](./rest-endpoints.md) | REST endpoint discovery, request/response formats, versioning |
| [authentication.md](./authentication.md) | API keys, HMAC signing, OAuth 2.0, JWT, webhook verification |
| [websockets.md](./websockets.md) | WebSocket lifecycle, frames, SSE, real-time protocols |
| [graphql-grpc.md](./graphql-grpc.md) | GraphQL schemas/queries, gRPC proto files, RPC patterns |

---

## Loading This Skill

Load this skill when the user asks you to:
- Analyze an API for porting
- Document REST endpoints
- Understand request/response formats
- Map API authentication flows
- Generate API specifications
- Plan API integration

---

## Quick-Scan Index

### By Analysis Need

| Need | Sub-Skill |
|------|-----------|
| HTTP methods/status codes/headers | [http-fundamentals.md](./http-fundamentals.md) |
| REST endpoint patterns | [rest-endpoints.md](./rest-endpoints.md) |
| Authentication schemes | [authentication.md](./authentication.md) |
| Real-time bidirectional | [websockets.md](./websockets.md) |
| GraphQL queries/mutations | [graphql-grpc.md](./graphql-grpc.md) |
| gRPC services | [graphql-grpc.md](./graphql-grpc.md) |

---

## Modular Sub-Skills

### 1. HTTP Fundamentals (`http-fundamentals.md`)

Covers: HTTP message structure, methods (GET/POST/PUT/PATCH/DELETE/HEAD/OPTIONS), status codes (1xx-5xx), headers, content-types, connection management, caching, CORS.

### 2. REST Endpoints (`rest-endpoints.md`)

Covers: Endpoint discovery patterns, CRUD operations, request/response formats, query parameters, path variables, pagination, filtering, sorting, API versioning strategies.

### 3. Authentication (`authentication.md`)

Covers: API keys, Bearer tokens, Basic Auth, HMAC request signing (AWS Signature V4), OAuth 2.0 flows, JWT structure/validation, webhook signature verification (Slack, Stripe).

### 4. WebSockets & SSE (`websockets.md`)

Covers: WebSocket handshake/upgrade, frame types (text/binary/close/ping/pong), connection lifecycle, reconnection strategies, Server-Sent Events, STOMP protocol.

### 5. GraphQL & gRPC (`graphql-grpc.md`)

Covers: GraphQL schemas, queries/mutations/subscriptions, introspection, variables/fragments, error handling, gRPC proto files, RPC method patterns, protobuf serialization.

---

## Analysis Output Template

When analyzing an API, produce:

```markdown
# API Analysis Report

## 1. Protocol Overview
- HTTP/HTTPS, version
- Authentication type
- Content-Type(s)

## 2. Endpoints

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | /users | List users | Bearer |
| POST | /users | Create user | Bearer |
| ... | ... | ... | ... |

## 3. Authentication Flow
[Document auth mechanism]

## 4. Request/Response Formats
[Document body schemas]

## 5. Error Handling
[Document error response format]

## 6. Real-time Features (if any)
[WebSocket/SSE/GraphQL subscriptions]
```

---

## Reference

- Planning/PLANNING.md — Full planning standard
- source-analysis-orchestrator — Coordinates all analysis skills
