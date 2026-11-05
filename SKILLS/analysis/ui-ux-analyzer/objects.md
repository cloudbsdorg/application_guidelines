---
name: ui-ux-analyzer-objects
description: UI Object Inventory — classifying and documenting display, input, action, container, collection, navigation, feedback, and composite objects.
---

# UI-UX Analyzer — Objects

## 1. UI Object Inventory

### 1.1 Object Classification

Every UI element falls into one of these categories:

| Category | Examples | What It Represents |
|----------|----------|-------------------|
| **Display** | Label, Text, Image, Icon, Badge | Read-only information |
| **Input** | TextField, Checkbox, Select, Slider, DatePicker | User provides data |
| **Action** | Button, Link, MenuItem, IconButton | User triggers behavior |
| **Container** | Panel, Card, Modal, Dialog, Sidebar | Groups other objects |
| **Collection** | Table, List, Tree, Grid, Tabs | Iterates over items |
| **Navigation** | Breadcrumb, TabBar, Pagination | Shows location or scope |
| **Feedback** | Toast, Alert, ProgressBar, Spinner | System responds to user/system |
| **Composite** | Form, SearchBar, FilterPanel | Combines multiple categories |

### 1.2 Object Properties Template

```markdown
## Object Inventory

### Display Objects

| ID | Object | Type | Content Source | Visibility | States |
|----|--------|------|----------------|------------|--------|
| D1 | PageTitle | Label | `user.name` | Always | Default only |
| D2 | StatusBadge | Badge | `order.status` | Always | pending=Yellow, complete=Green, cancelled=Red |
| D3 | UserAvatar | Image | `user.avatarUrl` | Logged in | Default, Loading, Error (fallback initials) |

### Input Objects

| ID | Object | Type | Bound To | Validation | Default |
|----|--------|------|----------|------------|---------|
| I1 | UsernameField | TextInput | `form.username` | Required, 3-20 chars | Empty |
| I2 | AcceptTerms | Checkbox | `form.accepted` | Must be true | false |
| I3 | CountrySelect | Select | `form.country` | Required | "Select country" |
```

## 2. Object State Machine

### 2.1 States Per Object

Document all states each object can be in:

#### Button States

| State | Appearance | Trigger |
|-------|------------|---------|
| Default | Blue background, white text | Idle |
| Hover | Lighter blue | Mouse over |
| Active | Darker blue | Clicking |
| Focus | Blue outline ring | Keyboard focus |
| Disabled | Gray background | `disabled=true` |
| Loading | Spinner icon, disabled | `loading=true` |

#### Input States

| State | Appearance | Trigger |
|-------|------------|---------|
| Default | Gray border | Idle |
| Focus | Blue border, outline | Input focused |
| Filled | Black text | Has value |
| Error | Red border, error message | Validation failed |
| Disabled | Gray background | `disabled=true` |
| ReadOnly | Gray text, no cursor | `readonly=true` |

### 2.2 State Transition Example

```markdown
## State Machine: SubmitButton

```
┌─────────┐   hover    ┌─────────┐   active   ┌─────────┐
│ DEFAULT │ ─────────► │  HOVER  │ ─────────► │ ACTIVE  │
└─────────┘            └─────────┘            └─────────┘
     ▲                                              │
     │              click                          │
     └──────────────────────────────────────────────┘

     │
     ▼ click (if form valid)
┌─────────┐   success   ┌──────────┐
│ LOADING │ ──────────► │ SUCCESS  │
└─────────┘            └──────────┘
     │
     │ error
     ▼
┌─────────┐
│  ERROR  │
└─────────┘
```

**Transitions:**
- Default → Hover: on mouseover
- Hover → Active: on mousedown
- Active → Default: on mouseup
- Active → Loading: on click (if valid)
- Loading → Success: on success response
- Loading → Error: on error response
```
