---
name: ui-ux-analyzer-data-flow
description: Data Binding Analysis — one-way, two-way, event bindings and data flow patterns.
---

# UI-UX Analyzer — Data Flow

## 4. Data Binding Analysis

### 4.1 Data Flow Direction

| Direction | Pattern | Description | Example |
|-----------|---------|-------------|---------|
| **One-way** | `{{ value }}` | Data flows to UI only | `{{ user.name }}` - display only |
| **Two-way** | `[(value)]` | UI updates data, data updates UI | `[(username)]` - input syncs |
| **Event** | `(event)` | UI emits, data reacts | `(click)` - button click |
| **Callback** | `@handler` | Parent provides handler | `@onSubmit` - form submission |

### 4.2 Data Binding Template

```markdown
## Data Bindings

### One-Way Bindings (Display)

| ID | Object | Expression | Source | Format |
|----|--------|-----------|--------|--------|
| B1 | UserNameLabel | `{{ user.name }}` | `user.name` | Plain text |
| B2 | OrderTotal | `{{ order.total | currency }}` | `order.total` | $1,234.56 |
| B3 | ItemCount | `{{ items.length }}` | `items.length` | "5 items" |

### Two-Way Bindings (Input)

| ID | Object | Expression | Target | Validation |
|----|--------|-----------|--------|------------|
| B4 | UsernameInput | `[(username)]` | `form.username` | Required, 3-20 chars |
| B5 | EmailInput | `[(email)]` | `form.email` | Email format |
| B6 | QuantityInput | `[(quantity)]` | `form.quantity` | Positive integer |

### Event Bindings

| ID | Object | Event | Handler | Effect |
|----|--------|-------|---------|--------|
| E1 | SubmitBtn | (click) | `onSubmit()` | Validate + API call |
| E2 | CancelBtn | (click) | `onCancel()` | Reset form + close |
| E3 | LogoutLink | (click) | `onLogout()` | Clear auth + redirect |
```

## Data Flow Patterns

### Component Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                         PARENT COMPONENT                         │
│                                                                 │
│  state = { user, orders, loading, error }                       │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ Child: UserProfile                                          │ │
│  │                                                          │ │
│  │  Props: user={user}                                        │ │
│  │  Events: onLogout=handleLogout                            │ │
│  │                                                          │ │
│  │  ┌──────────────────────────────────────────────────────┐ │ │
│  │  │ Grandchild: Avatar                                    │ │ │
│  │  │                                                        │ │ │
│  │  │  Props: src={user.avatarUrl}, name={user.name}     │ │ │
│  │  │  Events: onError=handleAvatarError                   │ │ │
│  │  └──────────────────────────────────────────────────────┘ │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ Child: OrderList                                           │ │
│  │                                                            │ │
│  │  Props: orders={orders}, loading={loading}                │ │
│  │  Events: onSelect=handleSelectOrder                         │ │
│  │                                                            │ │
│  │  ┌──────────────────────────────────────────────────────┐ │ │
│  │  │ Grandchild: OrderRow                                   │ │ │
│  │  │                                                        │ │ │
│  │  │  Props: order={order}, onSelect={onSelect}           │ │ │
│  │  │  Events: onClick → onSelect(order)                    │ │ │
│  │  └──────────────────────────────────────────────────────┘ │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### State Management Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                      STATE MANAGEMENT                           │
│                                                                 │
│  ┌───────────────┐    dispatch     ┌───────────────┐           │
│  │    STORE      │ ◄────────────── │   COMPONENT   │           │
│  │               │                 │               │           │
│  │  user: null   │ ──────────────► │   reads state  │           │
│  │  orders: []   │    subscribe   │   dispatches   │           │
│  │  loading: false│                 │   actions      │           │
│  └───────────────┘                 └───────────────┘           │
│         ▲                                                       │
│         │                                                       │
│    ┌────┴────┐                                                  │
│    │ MUTATION │                                                  │
│    │          │                                                  │
│    │ user = u │  ←── Action payload                             │
│    │ orders = o│                                                  │
│    └───────────┘                                                  │
└─────────────────────────────────────────────────────────────────┘
```
