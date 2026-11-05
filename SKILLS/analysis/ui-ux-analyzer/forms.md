---
name: ui-ux-analyzer-forms
description: Form Analysis — structure, fields, submission, and validation rules.
---

# UI-UX Analyzer — Forms

## 5. Form Analysis

### 5.1 Form Structure Template

```markdown
## Form Analysis: [FormName]

### Fields

| ID | Field | Type | Required | Bound To | Validation |
|----|-------|------|----------|----------|------------|
| F1 | Username | TextInput | Yes | `form.username` | 3-20 chars, alphanumeric |
| F2 | Email | TextInput | Yes | `form.email` | Email format |
| F3 | Password | PasswordInput | Yes | `form.password` | Min 8 chars |
| F4 | ConfirmPassword | PasswordInput | Yes | `form.confirm` | Must match password |
| F5 | AcceptTerms | Checkbox | Yes | `form.accepted` | Must be true |

### Submission

| Property | Value |
|----------|-------|
| Endpoint | `POST /api/users` |
| Payload | `{ username, email, password, accepted }` |
| Success | Redirect to `/dashboard` |
| Error | Show inline field errors |

### 5.2 Validation Rules

## Validation Rules

### Field-level

| Field | Rule | Error Message |
|-------|------|---------------|
| Username | Required | "Username is required" |
| Username | 3-20 chars | "Username must be 3-20 characters" |
| Username | alphanumeric | "Username must be alphanumeric" |
| Username | unique | "Username already taken" |
| Email | Required | "Email is required" |
| Email | Email format | "Please enter a valid email" |
| Password | Required | "Password is required" |
| Password | Min 8 chars | "Password must be at least 8 characters" |
| ConfirmPassword | Must match | "Passwords do not match" |
| AcceptTerms | Must be true | "You must accept the terms" |

### Form-level

| Rule | Condition | Error Message |
|------|-----------|---------------|
| Password strength | `password.match(/[A-Z]/)` | "Password must contain an uppercase letter" |
| Password strength | `password.match(/[0-9]/)` | "Password must contain a number" |
| Email uniqueness | API check | "An account with this email already exists" |

### Validation Flow

```
User fills form
        │
        ▼
┌───────────────────┐
│  Field Validation │
│                   │
│  On blur / change │
│  Validate each    │
│  field            │
│                   │
│  Show inline      │
│  errors if invalid│
└───────────────────┘
        │
        │ all fields valid
        ▼
┌───────────────────┐
│  Submit Click     │
│                   │
│  Validate all     │
│  fields again     │
│                   │
│  If invalid:      │
│  scroll to first  │
│  error            │
└───────────────────┘
        │
        │ valid
        ▼
┌───────────────────┐
│  API Submission    │
│                   │
│  Show loading     │
│  state            │
│                   │
│  Disable submit   │
└───────────────────┘
        │
        ▼
┌───────────────────┐
│  Success/Error    │
│                   │
│  Success: redirect│
│  Error: show     │
│  form-level error │
└───────────────────┘
```
