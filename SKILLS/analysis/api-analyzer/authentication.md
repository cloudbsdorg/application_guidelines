---
name: api-analyzer-authentication
description: API Authentication patterns — API keys, HMAC signing, OAuth 2.0, and webhook signature verification.
---

# API Analyzer — Authentication

## 1. Authentication Patterns

### 1.1 No Authentication

| Use Case | Risk | Example |
|----------|------|---------|
| Public data only | Low | Weather API, public metrics | Low | Weather API, public metrics |

### 1.2 API Key Authentication

## API Key Placement

| Method | Header | Example |
|--------|--------|---------|
| Header | `X-API-Key` | Simple, common |
| Header | `Authorization: ApiKey <key>` | More explicit |
| Query Param | `?api_key=<key>` | For GET requests |
| Basic Auth | `Authorization: Basic <base64>` | Legacy compatibility |

## HMAC-Based Request Signing (AWS, Slack)

### AWS Signature Version 4

```
1. Create canonical request:
GET
/users
timestamp=20260101T120000Z&X-Amz-Algorithm=AWS4-HMAC-SHA256
content-type=application/json
host:api.example.com
x-amz-date:20260101T120000Z

content-type;host;x-amz-date (signed headers)

HASHED_BODY

2. Create string to sign:
AWS4-HMAC-SHA256
20260101T120000Z
20260101/us-east-1/execute-api/aws4_request
HASH(canonical_request)

3. Calculate signature:
kSecret = "AWS4" + secret_key
kDate = HMAC(kSecret, "20260101")
kRegion = HMAC(kDate, "us-east-1")
kService = HMAC(kRegion, "execute-api")
kSigning = HMAC(kService, "aws4_request")
signature = HMAC(kSigning, string_to_sign)

4. Add to header:
Authorization: AWS4-HMAC-SHA256
  Credential=<access_key>/20260101/us-east-1/execute-api/aws4_request
  SignedHeaders=content-type;host;x-amz-date
  Signature=<signature>
```

### Slack Request Signing

```javascript
// 1. Get signing secret from app settings
const signingSecret = process.env.SLACK_SIGNING_SECRET;

// 2. Verify request
const crypto = require('crypto');

function verifySlackRequest(req) {
  const timestamp = req.headers['x-slack-request-timestamp'];
  const slackSignature = req.headers['x-slack-signature'];
  
  // Check timestamp (prevent replay attacks)
  const fiveMinutesAgo = Math.floor(Date.now() / 1000) - 60 * 5;
  if (parseInt(timestamp) < fiveMinutesAgo) {
    throw new Error('Request too old');
  }
  
  // Create signature base
  const sigBase = `v0:${timestamp}:${req.rawBody}`;
  
  // Calculate expected signature
  const mySignature = 'v0=' + crypto
    .createHmac('SHA256', signingSecret)
    .update(sigBase)
    .digest('hex');
  
  // Compare signatures
  return crypto.timingSafeEqual(
    Buffer.from(mySignature),
    Buffer.from(slackSignature)
  );
}
```

## RSA Signature (GitHub, Shopify)

```
1. GitHub Signature
Header: X-Hub-Signature-256

Body: raw request body (JSON)
Secret: webhook secret from settings

Expected:
sha256=HMAC-SHA256(secret, body)

Verification:
const crypto = require('crypto');
const signature = Buffer.from(
  req.headers['x-hub-signature-256'],
  'utf8'
);
const expected = Buffer.from(
  'sha256=' + crypto
    .createHmac('sha256', secret)
    .update(req.rawBody)
    .digest('hex'),
  'utf8'
);
crypto.timingSafeEqual(signature, expected);
```

## 2. OAuth 2.0 Flows

## OAuth 2.0 Flow Types

| Flow | Use Case | Client Type |
|------|----------|-------------|
| Authorization Code | Server-side apps | Confidential |
| Authorization Code + PKCE | SPAs, Mobile | Public |
| Client Credentials | Service-to-service | Confidential |
| Device Code | CLI, TV apps | Public |
| Refresh Token | Token renewal | All |

## Authorization Code Flow

### Step 1: Redirect to Authorization

```
GET https://auth.example.com/authorize?
  response_type=code&
  client_id=YOUR_CLIENT_ID&
  redirect_uri=https://your-app.com/callback&
  scope=read:users write:users&
  state=RANDOM_STATE
```

### Step 2: User Grants Permission

User sees consent screen and approves.

### Step 3: Receive Code

```
Redirect to: https://your-app.com/callback?code=AUTH_CODE&state=RANDOM_STATE
```

### Step 4: Exchange Code for Tokens

```bash
POST https://auth.example.com/token
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code&
code=AUTH_CODE&
redirect_uri=https://your-app.com/callback&
client_id=YOUR_CLIENT_ID&
client_secret=YOUR_CLIENT_SECRET
```

### Step 5: Receive Tokens

```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIs...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "dGhpcyBpcyBhIHJlZnJlc2g...",
  "scope": "read:users write:users"
}
```

### Step 6: Use Access Token

```
GET https://api.example.com/users
Authorization: Bearer eyJhbGciOiJSUzI1NiIs...
```

## Token Refresh

### Refresh Request

```bash
POST https://auth.example.com/token
Content-Type: application/x-www-form-urlencoded

grant_type=refresh_token&
refresh_token=dGhpcyBpcyBhIHJlZnJlc2g...&
client_id=YOUR_CLIENT_ID&
client_secret=YOUR_CLIENT_SECRET
```

### Refresh Response

```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIs...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "new_refresh_token..."
}
```

## 3. JWT (JSON Web Tokens)

### JWT Structure

```
xxxxx.yyyyy.zzzzz
│     │     │
│     │     └─ Signature
│     └─ Payload (claims)
└─ Header (algorithm, type)
```

### Header

```json
{
  "alg": "RS256",
  "typ": "JWT"
}
```

### Payload

```json
{
  "iss": "https://auth.example.com",
  "sub": "user123",
  "aud": "https://api.example.com",
  "exp": 1709301234,
  "iat": 1709297634,
  "scope": "read:users write:users",
  "email": "user@example.com"
}
```

### Token Validation Checklist

- [ ] Signature verified with public key
- [ ] `exp` not in the past
- [ ] `nbf` not in the future (if present)
- [ ] `aud` matches expected audience
- [ ] `iss` matches expected issuer
- [ ] `sub` extracted for user identification

## 4. Security Best Practices

### Token Storage

| Storage | Security | Use |
|---------|----------|-----|
| httpOnly cookie | Most secure | Web apps |
| Secure memory | Secure | SPAs |
| localStorage | Vulnerable to XSS | Last resort |
| URL params | Never | Leaked in logs |

### Token Transmission

- Always use HTTPS
- Set `Secure` cookie flag
- Set `SameSite` cookie flag
- Don't put tokens in URL parameters

### OAuth Security Checklist

- [ ] PKCE enabled for public clients
- [ ] State parameter validated
- [ ] Code exchange happens server-side
- [ ] Secrets stored in environment variables
- [ ] Redirect URIs strictly validated
- [ ] Tokens shorter expiration (15min-1hr)
- [ ] Refresh tokens rotatable
- [ ] Client ID/secret in environment, not code
