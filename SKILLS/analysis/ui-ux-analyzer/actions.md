---
name: ui-ux-analyzer-actions
description: Action Discovery — classifying and chaining user interactions and their effects.
---

# UI-UX Analyzer — Actions

## 3. Action Discovery

### 3.1 Action Classification

| Category | Examples | What It Triggers |
|----------|----------|------------------|
| **Navigation** | Link, Tab, Breadcrumb click | Page/view change |
| **Form** | Submit, Reset, Cancel | Form processing |
| **Data** | Create, Read, Update, Delete | CRUD operations |
| **State** | Toggle, Expand, Collapse | UI state change |
| **Communication** | Send, Share, Export | External action |
| **Authentication** | Login, Logout, Register | Auth flow |

### 3.2 Action Inventory Template

```markdown
## Action Inventory

| ID | Action | Type | Object | Trigger | Effect | API Call |
|----|--------|------|--------|---------|--------|----------|
| A1 | SubmitOrder | Form | SubmitButton | Click | Create order | POST /orders |
| A2 | CancelOrder | Data | CancelButton | Click | Set status=cancelled | PATCH /orders/:id |
| A3 | FilterOrders | State | FilterPanel | Change | Update list | None (client) |
| A4 | NavigateToDetail | Navigation | OrderRow | Click | Go to detail view | None (router) |
```

## Action Chains

### Create Order Flow

```
User clicks "Create Order"
        │
        ▼
┌───────────────────┐
│  NewOrderForm     │
│                   │
│  1. Fill fields   │◄── TextField: Item, Quantity
│  2. Add details   │◄── Select: Shipping method
│  3. Review total  │
│                   │
│  [Cancel] [Save]  │
└───────────────────┘
        │
        │ click "Save"
        ▼
┌───────────────────┐
│  Validation       │
│                   │
│  □ Required fields│──► If invalid: show error states
│  □ Valid formats  │
│  □ Positive qty   │
└───────────────────┘
        │
        │ valid
        ▼
┌───────────────────┐
│  API Call         │
│                   │
│  POST /orders     │
│  Body: {...}      │
└───────────────────┘
        │
        │ success
        ▼
┌───────────────────┐
│  State Update     │
│                   │
│  orders.push(new) │
│  Navigate to list │
└───────────────────┘
        │
        ▼
┌───────────────────┐
│  Feedback         │
│                   │
│  Toast: "Created" │
└───────────────────┘
```

### Delete Flow (Bulk)

```
User selects items (checkbox)
        │
        ▼
┌───────────────────┐
│  Selection State  │
│                   │
│  items[0] = true │
│  items[1] = true │
│  items[2] = false│
│                   │
│  [Delete Selected]│──► Button enabled when count > 0
└───────────────────┘
        │
        │ click "Delete Selected"
        ▼
┌───────────────────┐
│  Confirmation     │
│                   │
│  Modal: "Delete   │
│  2 items?"        │
│                   │
│  [Cancel] [Delete]│
└───────────────────┘
        │
        │ click "Delete"
        ▼
┌───────────────────┐
│  API Call         │
│                   │
│  DELETE /items    │
│  Body: {ids:[...]}│
└───────────────────┘
        │
        │ success
        ▼
┌───────────────────┐
│  State Update     │
│                   │
│  items = items    │
│    .filter(!del) │
│  selection = {}   │
└───────────────────┘
        │
        ▼
┌───────────────────┐
│  Feedback         │
│                   │
│  Toast: "Deleted │
│  2 items"        │
└───────────────────┘
```
