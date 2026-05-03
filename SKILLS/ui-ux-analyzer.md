---
name: ui ux analyzer
description: Systematically analyze user interfaces to understand objects, states, actions, and data flow - producing implementation-ready specifications.
---

# Skill: ui-ux-analyzer

**Purpose:** Systematically analyze user interfaces to understand objects, states, actions, and data flow - producing implementation-ready specifications.

**Triggers:** When analyzing a UI for porting, rewriting, or feature implementation.

## Loading Instructions

Load this skill when the user asks you to:
- Analyze a UI/UX for implementation
- Document UI objects and their types
- Understand user interaction flows
- Generate UI specifications from existing code
- Plan UI feature implementation
- Draw wireframes with ASCII art

## Core Principle

> **A UI is not its widgets. It's a projection of state through objects, shaped by actions.**

A button is meaningless without knowing: what state it reflects, what action it triggers, what state it leaves behind.

---

## 0. ASCII Wireframing Conventions

### 0.1 Box Drawing Characters

```
┌ ─ ┐    Top corners and top border
└ ─ ┘    Bottom corners and bottom border
│       Vertical border
─       Horizontal border
├ ┤     Left/right T-junctions
┼       Cross junction
┬ ┴     Top/bottom T-junctions
```

### 0.2 Component Symbols

```
┌─────┐           Simple box
│ txt │           Content with vertical bars
└─────┘

┌───────────────┐
│   [Button]    │   Button in box
└───────────────┘

┌─ Tab1 ─┐      Tabbed interface

╔═══════╗       Double-line box (modal)
║ Modal ║
╚═══════╝

┌ ┐             Checkbox unchecked
☑             Checkbox checked

▶             Collapsed tree node
▼             Expanded tree node

●             Filled circle (status indicator)
○             Empty circle
✓             Checkmark
✗             X mark
```

### 0.3 Layout Grid

```
┌─────────────────────────────────────────────────┐
│                    HEADER                        │
├─────────────────────────────────────────────────┤
│                                                 │
│                  CONTENT                         │
│                                                 │
├─────────────────────────────────────────────────┤
│                    FOOTER                        │
└─────────────────────────────────────────────────┘
```

### 0.4 Form Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  ┌─ Personal Information ───────────────────────────────────────┐  │
│  │                                                                 │  │
│  │  First Name *                     Last Name *                   │  │
│  │  ┌────────────────────────┐     ┌────────────────────────┐    │  │
│  │  │ John                   │     │ Smith                  │    │  │
│  │  └────────────────────────┘     └────────────────────────┘    │  │
│  │                                                                 │  │
│  │  Email Address *                                              │  │
│  │  ┌─────────────────────────────────────────────────────────┐│  │
│  │  │ john.smith@example.com                                   ││  │
│  │  └─────────────────────────────────────────────────────────┘│  │
│  │                                                                 │  │
│  │  ┌─ Shipping Address ──────────────────────────────────────┐│  │
│  │  │                                                                 ││  │
│  │  │  Street Address *                                           ││  │
│  │  │  ┌─────────────────────────────────────────────────────┐││  │
│  │  │  │ 123 Main Street                                      │││  │
│  │  │  └─────────────────────────────────────────────────────┘││  │
│  │  │                                                                 ││  │
│  │  │  City *                    State *           ZIP *        ││  │
│  │  │  ┌──────────────────┐     ┌──────┐    ┌────────────┐    ││  │
│  │  │  │ San Francisco    │     │ CA ▼  │    │ 94102      │    ││  │
│  │  │  └──────────────────┘     └──────┘    └────────────┘    ││  │
│  │  │                                                                 ││  │
│  └─ ──────────────────────────────────────────────────────────────┘│  │
│                                                                     │
│                              [ Cancel ]      [ ✓ Save ]              │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 0.5 Table Layout

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Orders                                           [+ New Order]         │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │ 🔍 Search orders...                              [Status: All ▼]   │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  ┌────┬────────┬──────────────────┬────────────┬──────────┬─────────┐ │
│  │    │  ID    │ Customer          │ Date       │ Total    │ Status │ │
│  ├────┼────────┼──────────────────┼────────────┼──────────┼─────────┤ │
│  │ ☐  │ #1042  │ Alice M           │ 2026-05-01 │ $1,234.56│ ●Pendng │ │
│  ├────┼────────┼──────────────────┼────────────┼──────────┼─────────┤ │
│  │ ☑  │ #1041  │ Bob S             │ 2026-04-28 │   $89.00│ ✓Compl. │ │
│  ├────┼────────┼──────────────────┼────────────┼──────────┼─────────┤ │
│  │ ☐  │ #1040  │ Carol K           │ 2026-04-15 │   $45.00│ ✗Canceld│ │
│  └────┴────────┴──────────────────┴────────────┴──────────┴─────────┘ │
│                                                                         │
│  Showing 1-3 of 47 orders                        < Prev │ 1 2 3 ... 16 │ │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐ │
│  │  With selected:  [📧 Email]  [📄 Export]  [🗑️ Delete]            │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

### 0.6 Modal/Dialog

```
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ╔═ Confirm Delete ═══════════════════════════════════════════════════╗   ║
║   ║                                                                     ║   ║
║   ║   Are you sure you want to delete these 3 orders?                    ║   ║
║   ║                                                                     ║   ║
║   ║   This action cannot be undone.                                       ║   ║
║   ║                                                                     ║   ║
║   ║   ┌─────────┬─────────┬──────────────┐                              ║   ║
║   ║   │  ID     │Customer │   Total      │                              ║   ║
║   ║   ├─────────┼─────────┼──────────────┤                              ║   ║
║   ║   │ #1041   │ Bob S   │    $89.00    │                              ║   ║
║   ║   │ #1038   │ David L │   $234.50    │                              ║   ║
║   ║   │ #1035   │ Emma R  │    $67.00    │                              ║   ║
║   ║   └─────────┴─────────┴──────────────┘                              ║   ║
║   ║                                                                     ║   ║
║   ║                           [ Cancel ]      [ 🗑️ Delete Orders ]       ║   ║
║   ╚═══════════════════════════════════════════════════════════════════════╝   ║
║                                                                              ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### 0.7 Sidebar Layout

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ ┌─────────────┬───────────────────────────────────────────────────────────┐ │
│ │             │  Dashboard                                              │ │
│ │  ┌───────┐  ├───────────────────────────────────────────────────────────┤ │
│ │  │ Logo  │  │                                                           │ │
│ │  └───────┘  │  ┌─ Stats ──────────────────────────────────────────────┐│ │
│ │             │  │                                                           ││ │
│ │  Dashboard  │  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ││ │
│ │  ─────────  │  │  │ Orders  │  │ Revenue │  │Customers│  │Products │  ││ │
│ │  📦 Orders  │  │  │   47    │  │ $12,845 │  │    23   │  │   156   │  ││ │
│ │  👥 Customers│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘  ││ │
│ │  📦 Products │  │                                                           ││ │
│ │  📊 Reports  │  └─────────────────────────────────────────────────────────┘│ │
│ │             │  │                                                           ││ │
│ │  ─────────  │  │  ┌─ Recent Orders ─────────────────────────────────────┐│ │
│ │  ⚙️ Settings │  │  │                                                           ││ │
│ │  ❓ Help     │  │  │  #1042  Alice M      2026-05-01      $1,234.56  ●    ││ │
│ │             │  │  │  #1041  Bob S        2026-04-28        $89.00    ✓    ││ │
│ │             │  │  │  #1040  Carol K      2026-04-15        $45.00    ✗    ││ │
│ │             │  │  └─────────────────────────────────────────────────────────┘│ │
│ │             │  │                                                           │ │
│ └─────────────┘  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 0.8 Wizard/Stepper

```
     Complete Your Order
     ─────────────────────
        ●────────●────────○────────○
      Review   Payment  Confirm   Done

┌─────────────────────────────────────────────────────────────────────────────┐
│  Step 2: Payment                                           Step 2 of 4      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─ Payment Method ──────────────────────────────────────────────────────┐  │
│  │                                                                           │  │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐        │  │
│  │  │  💳 Credit Card │  │  🏦 Bank Transfer│  │   💵    PayPal  │        │  │
│  │  │    (selected)   │  │                  │  │                 │        │  │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘        │  │
│  │                                                                           │  │
│  └─────────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌─ Card Details ────────────────────────────────────────────────────────┐  │
│  │                                                                           │  │
│  │  Card Number *                                                          │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐    │  │
│  │  │ 4242 4242 4242 4242                                               │    │  │
│  │  └─────────────────────────────────────────────────────────────────┘    │  │
│  │                                                                           │  │
│  │  Cardholder Name *                    Expiry *         CVC *          │  │
│  │  ┌─────────────────────────────────┐ ┌─────────┐ ┌─────────┐          │  │
│  │  │ John Smith                      │ │ 12/28 ▼ │ │  123    │          │  │
│  │  └─────────────────────────────────┘ └─────────┘ └─────────┘          │  │
│  │                                                                           │  │
│  └─────────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│                        [ ← Back ]               [ Continue → ]              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 0.9 Empty State

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                                                                             │
│                         ┌───────────────────────────┐                     │
│                         │                           │                     │
│                         │         📦               │                     │
│                         │                           │                     │
│                         └───────────────────────────┘                     │
│                                                                             │
│                              No orders yet                                  │
│                                                                             │
│                    You haven't created any orders.                          │
│                  Get started by creating your first order.                  │
│                                                                             │
│                                                                             │
│                        ┌─────────────────────┐                             │
│                        │   + Create Order    │                             │
│                        └─────────────────────┘                             │
│                                                                             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 0.10 Loading State

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                                                                             │
│                              ┌─────────────────┐                           │
│                              │                 │                           │
│                              │      ◌◌◌       │                           │
│                              │                 │                           │
│                              │   Loading...    │                           │
│                              │                 │                           │
│                              │  Fetching orders│                           │
│                              │                 │                           │
│                              └─────────────────┘                           │
│                                                                             │
│                                                                             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 0.11 Error State

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                                                                             │
│                            ┌─────────────────────┐                         │
│                            │                     │                         │
│                            │    ⚠️              │                         │
│                            │                     │                         │
│                            │   Something         │                         │
│                            │   went wrong        │                         │
│                            │                     │                         │
│                            └─────────────────────┘                         │
│                                                                             │
│                       We couldn't load your orders.                        │
│                       This might be a temporary issue.                      │
│                                                                             │
│                                                                             │
│                         ┌─────────────────────┐                             │
│                         │   🔄 Try Again      │                             │
│                         └─────────────────────┘                             │
│                                                                             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 0.12 Responsive Breakpoints

```
Mobile (< 768px)                     Tablet (768px - 1024px)
┌─────────────────────┐              ┌─────────────────────────────────────────┐
│ ┌─────────────────┐ │              │ ┌───────────┬─────────────────────────┐ │
│ │ ≡  MyApp    [👤] │ │              │ │           │  Dashboard              │ │
│ └─────────────────┘ │              │ │  ┌─────┐  ├─────────────────────────┤ │
│ ├───────────────────┤ │              │ │  │     │  │                         │ │
│ │                   │ │              │ │  │ S   │  │   ┌─────┐ ┌─────┐      │ │
│ │  ┌─────────────┐  │ │              │ │  │ I   │  │   │     │ │     │      │ │
│ │  │             │  │ │              │ │  │ D   │  │   └─────┘ └─────┘      │ │
│ │  │   Content   │  │ │              │ │  │ E   │  │                         │ │
│ │  │             │  │              │ │  │ B   │  │   ┌─────┐ ┌─────┐      │ │
│ │  │             │  │              │ │  │ A   │  │   │     │ │     │      │ │
│ │  └─────────────┘  │ │              │ │  │ R   │  │   └─────┘ └─────┘      │ │
│ │                   │ │              │ │  │     │  │                         │ │
│ │  ┌─────────────┐  │ │              │ │  └─────┘  │                         │ │
│ │  │   Content   │  │ │              │ │           │                         │ │
│ │  └─────────────┘  │ │              │ └───────────┴─────────────────────────┘ │
│ │                   │ │              │                                         │
│ │  ┌─────────────┐  │ │              └─────────────────────────────────────────┘
│ │  │   Content   │  │ │
│ │  └─────────────┘  │ │
│ └───────────────────┘ │
└─────────────────────┘

Desktop (≥ 1024px)
┌─────────────────────────────────────────────────────────────────────────────┐
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │  Logo    Dashboard   Orders   Customers   Reports        [🔔] [👤] John │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│ ┌──────────┬──────────────────────────────────────────────────────────────┐ │
│ │          │                                                              │ │
│ │  SIDEBAR │  MAIN CONTENT AREA                                          │ │
│ │          │                                                              │ │
│ │  • Home  │  ┌───────────────────────────────────────────────────────┐   │ │
│ │  • Orders│  │                                                       │   │ │
│ │  • Stats │  │   Content fills the remaining space                   │   │ │
│ │          │  │                                                       │   │ │
│ │          │  │   Tables, forms, cards - all responsive               │   │ │
│ │          │  │                                                       │   │ │
│ │          │  │                                                       │   │ │
│ │          │  └───────────────────────────────────────────────────────┘   │ │
│ │          │                                                              │ │
│ └──────────┴──────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 0.13 Component State Indicators

```
Button States:
┌───────────────────────────────────────────────────────────────────────────┐
│                                                                           │
│  ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐          │
│  │   Submit Order  │   │   Submit Order  │   │   Submit Order  │          │
│  │   (default)     │   │    (hover)      │   │   (active)      │          │
│  │   bg: blue      │   │   bg: lightblue │   │   bg: darkblue   │          │
│  └─────────────────┘   └─────────────────┘   └─────────────────┘          │
│                                                                           │
│  ┌─────────────────┐   ┌─────────────────┐                               │
│  │   Submit Order  │   │   Submit Order  │                               │
│  │   (disabled)    │   │   (loading)     │                               │
│  │   bg: gray      │   │   spinner       │                               │
│  │   opacity: 0.5  │   │   text: "..."   │                               │
│  └─────────────────┘   └─────────────────┘                               │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

Input States:
┌───────────────────────────────────────────────────────────────────────────┐
│                                                                           │
│  Default:                         Focus:                                  │
│  ┌───────────────────────────┐   ┌───────────────────────────┐           │
│  │ Enter your name           │   │ John Smith               │           │
│  │                           │   │▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│           │
│  └───────────────────────────┘   └───────────────────────────┘           │
│   border: gray                     border: blue (2px)                     │
│                                                                           │
│  Valid:                           Invalid:                                 │
│  ┌───────────────────────────┐   ┌───────────────────────────┐           │
│  │ john@example.com          │   │ john@invalid              │           │
│  └───────────────────────────┘   └───────────────────────────┘           │
│   border: green ✓               border: red ✗                             │
│                                   ┌───────────────────────┐               │
│                                   │ Enter valid email     │               │
│                                   └───────────────────────┘               │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

Dropdown States:
┌───────────────────────────────────────────────────────────────────────────┐
│                                                                           │
│  Closed:                            Open:                                 │
│  ┌───────────────────────────┐   ┌───────────────────────────┐           │
│  │ United States          ▼ │   │ United States          ▼ │           │
│  └───────────────────────────┘   ├───────────────────────────┤           │
│                                   │ ✓ United States         │           │
│                                   │   Canada                │           │
│                                   │   Mexico                │           │
│                                   │   United Kingdom        │           │
│                                   └───────────────────────────┘           │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘
```

### 0.14 Full Page Wireframe Template

```markdown
## Wireframe: OrderDetailView

```
╔═══════════════════════════════════════════════════════════════════════════╗
║  Order #1042                                                    [Edit]   ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                            ║
║  ┌─ Order Info ────────────────────────────────────────────────────────┐  ║
║  │                                                                        ║  ║
║  │  Status: ● Pending         Order Date: May 1, 2026                   ║  ║
║  │  Customer: Alice M         Payment: Credit Card (•••• 4242)           ║  ║
║  │                                                                        ║  ║
║  └────────────────────────────────────────────────────────────────────────╝  ║
║                                                                            ║
║  ┌─ Line Items ────────────────────────────────────────────────────────┐  ║
║  │                                                                        ║  ║
║  │  ┌──────────┬─────────────────────────────┬──────────┬───────────┐  ║  ║
║  │  │  Item    │  Description                │  Qty     │    Price  │  ║  ║
║  │  ├──────────┼─────────────────────────────┼──────────┼───────────┤  ║  ║
║  │  │  #SKU123 │  Premium Widget              │    2     │  $199.99  │  ║  ║
║  │  │  #SKU456 │  Basic Component            │    5     │   $24.99  │  ║  ║
║  │  ├──────────┼─────────────────────────────┼──────────┼───────────┤  ║  ║
║  │  │          │                             │  Subtotal│  $524.93  │  ║  ║
║  │  │          │                             │  Tax    │   $52.49  │  ║  ║
║  │  │          │                             │  Total  │  $577.42  │  ║  ║
║  │  └──────────┴─────────────────────────────┴──────────┴───────────┘  ║  ║
║  │                                                                        ║  ║
║  └────────────────────────────────────────────────────────────────────────╝  ║
║                                                                            ║
║  ┌─ Shipping Address ────────────────────┐  ┌─ Actions ─────────────────┐  ║
║  │                                        │  │                          │  ║
║  │  Alice M                               │  │  [📧 Send Invoice]       │  ║
║  │  123 Main Street                       │  │  [📦 Mark Shipped]       │  ║
║  │  San Francisco, CA 94102               │  │  [✗ Cancel Order]        │  ║
║  │  United States                         │  │                          │  ║
║  │                                        │  └──────────────────────────┘  ║
║  └────────────────────────────────────────┘                                ║
║                                                                            ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

**Legend:**
- `┌─┐` Box borders
- `─` Horizontal lines
- `│` Vertical lines
- `╔═╗` Double-line box for modals
- `[Button]` Action buttons
- `● ✓ ✗` Status indicators
- `•••• 4242` Masked card numbers
- [Action] = Icon button
- Column headers = Sortable columns
- Data cells = Clickable rows
```

---

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

---

## 2. Object State Machine

### 2.1 States Per Object

```markdown
### Button States

| State | Trigger | Visual | Behavior |
|-------|---------|--------|----------|
| Default | No interaction | Primary color, full opacity | Clickable |
| Hover | Mouse over | Lightened 10%, cursor:pointer | Clickable |
| Active/Pressed | Mouse down | Darkened 10% | Triggers action |
| Disabled | `disabled=true` | Grayed out, 50% opacity | Non-clickable |
| Loading | `loading=true` | Spinner replaces text | Non-clickable |

### Input States

| State | Trigger | Visual | Behavior |
|-------|---------|--------|----------|
| Default | No interaction | Border: gray | Editable |
| Focus | Tab/Click | Border: blue | Editable |
| Valid | Passes validation | Border: green | Submittable |
| Invalid | Fails validation | Border: red, error message | Shows error |
| Disabled | `disabled=true` | Grayed out | Non-editable |
```

### 2.2 State Transition Example

```markdown
## State Machine: SubmitButton

```
[Default] ──hover──► [Hover]
[Hover] ──mouseleave──► [Default]
[Hover] ──click──► [Active]
[Active] ──mouseup──► [Loading] (if form valid)
[Active] ──mouseup──► [Default] (if form invalid)
[Loading] ──response──► [Default] (success) or [Error]
[Error] ──click──► [Loading] (retry)
```
```

---

## 3. Action Discovery

### 3.1 Action Classification

| Type | Description | Examples |
|------|-------------|----------|
| **Direct** | Immediately changes state | Toggle checkbox, click button |
| **Deferred** | Queues for later processing | Submit form, batch delete |
| **Navigation** | Moves to another view | Click link, select tab |
| **Data** | Reads/writes data | Search, filter, sort, paginate |
| **Composition** | Triggers multiple actions | Wizard steps, bulk operations |

### 3.2 Action Inventory Template

```markdown
## Action Inventory

| ID | Action | Trigger | Object | Pre-condition | Effect | Post-state |
|----|--------|---------|--------|---------------|--------|------------|
| A1 | SubmitOrder | Click | SubmitButton | All fields valid | POST /api/orders | Redirect to ConfirmationView |
| A2 | CancelOrder | Click | CancelButton | Order status = pending | DELETE /api/orders/{id} | Show confirmation modal |
| A3 | FilterResults | Select change | FilterDropdown | None | GET /api/orders?filter=X | Table refreshes |
| A4 | SelectItem | Checkbox click | ItemCheckbox | None | Toggle `selected[id]` | Selection count updates |
```

### 3.3 Action Chaining

```markdown
## Action Chains

### Create Order Flow
```
1. User clicks "New Order" (A1 → opens NewOrderModal)
2. User fills form (I1-I5 → updates form state)
3. User clicks "Add Item" (A2 → adds item to order.items)
4. User clicks "Submit" (A3 → validates, then A4)
5. System shows loading (SubmitButton → Loading state)
6. System calls API (POST /api/orders)
7. System redirects to OrderDetail (Navigation)
```

### Delete Flow (Bulk)
```
1. User checks items (A4 → toggles selection, updates count)
2. User clicks "Delete Selected" (A5 → enabled only when count > 0)
3. System shows confirmation modal (Feedback)
4. User confirms (A6)
5. System calls DELETE /api/items/{ids}
6. Table refreshes, toast shows "X items deleted"
```
```

---

## 4. Data Binding Analysis

### 4.1 Data Flow Direction

| Pattern | Description | Example |
|---------|-------------|---------|
| **One-way** | Data flows to UI only | `{{ user.name }}` - display only |
| **Two-way** | UI changes update data | `v-model="username"` |
| **Event-driven** | User action triggers data change | `onClick → API call` |

### 4.2 Data Binding Template

```markdown
## Data Bindings

| Object | Type | Bound To | Direction | Source/Target |
|--------|------|----------|-----------|---------------|
| PageTitle | Display | `user.name` | → UI | Computed from store |
| UsernameField | Input | `form.username` | ↔ UI↔Store | Two-way |
| SubmitButton | Action | `form.$invalid` | → UI | Disabled when true |
| ItemCount | Display | `selected.size()` | → UI | Computed |
| DeleteButton | Action | `selected.size() > 0` | → UI | Disabled when 0 |
```

---

## 5. Form Analysis

### 5.1 Form Structure Template

```markdown
## Form Analysis: NewOrderForm

### Fields

| Field | Type | Required | Validation | Default | Error Message |
|-------|------|----------|-----------|--------|---------------|
| customerName | Text | Yes | min:2, max:100 | "" | "Name must be 2-100 characters" |
| email | Email | Yes | email format | "" | "Enter a valid email" |
| items | Collection | Yes | min:1 | [] | "Add at least one item" |
| shipping | Select | Yes | must select | null | "Select shipping method" |
| termsAccepted | Checkbox | Yes | must be true | false | "You must accept terms" |

### Submission

| Condition | Behavior |
|-----------|---------|
| All valid | Enable SubmitButton, POST on click |
| Any invalid | Disable SubmitButton, show inline errors |
| Submitting | Show Loading state on button, disable all fields |
| Success | Redirect to /orders/{id} |
| Failure | Show error toast, re-enable form |
```

### 5.2 Validation Rules

```markdown
## Validation Rules

### Field-level
- Required: Not empty, not null
- Format: email, phone, URL, regex
- Range: min/max for numbers, length for strings
- Custom: business logic validation

### Form-level
- Cross-field: `password === confirmPassword`
- Async: Check username uniqueness via API
- Conditional: `shipping === 'express'` requires phone

### Submission-level
- Duplicate prevention: Disable button during submission
- Timeout: Show error after 30s
- Retry: Allow retry on network failure
```

---

## 6. View/Page Analysis

### 6.1 View Structure Template

```markdown
## View: OrderListView

### Purpose
Displays paginated list of orders with filtering and bulk actions.

### Layout Structure
```
┌─────────────────────────────────────────────────┐
│ Header: "Orders" + "New Order" button           │
├─────────────────────────────────────────────────┤
│ FilterBar: Search | Status | Date Range | Clear │
├─────────────────────────────────────────────────┤
│ TableHeader: ☑ | ID | Customer | Status | Total │
├─────────────────────────────────────────────────┤
│ TableBody: [OrderRow] × N                       │
│   ...                                           │
├─────────────────────────────────────────────────┤
│ Pagination: < Prev | 1 2 3 | Next >             │
├─────────────────────────────────────────────────┤
│ Footer: "X orders found" | Bulk Actions         │
└─────────────────────────────────────────────────┘
```

### 6.2 View States

```markdown
### OrderListView States

| State | Condition | Content Shown |
|-------|-----------|---------------|
| Loading | Initial load | Skeleton rows |
| Empty | No orders | "No orders found" illustration |
| Populated | Has orders | Table with data |
| Filtered | Filter active | Filtered table + "X results" |
| Error | API failure | Error message + Retry button |
```

### 6.3 Navigation Paths

```markdown
### Navigation From OrderListView

| Action | Destination | Pass State |
|--------|-------------|------------|
| Click "New Order" | NewOrderView | None |
| Click order row | OrderDetailView | `orderId` |
| Click customer name | CustomerDetailView | `customerId` |
| Click pagination | OrderListView | `page=N` |
| Click "Export" | Download CSV | Filter state |
```

---

## 7. Interaction Flow Documentation

### 7.1 User Journey Template

```markdown
## User Journey: Place Order

### Steps
1. **Navigate to Orders** → URL: /orders, View: OrderListView
2. **Click "New Order"** → Action: A1, Opens: NewOrderModal
3. **Fill form fields** → Data: form state updated
4. **Add line items** → Action: A2, Updates: form.items[]
5. **Review total** → Display: Computed from items
6. **Accept terms** → Action: Toggle checkbox
7. **Submit** → Action: A3, Validation runs
8. **View confirmation** → Navigate: /orders/{newId}

### Alternative Paths
- **Empty cart** → Step 4: "Add at least one item" error
- **Invalid email** → Step 7: Inline error on email field
- **Network error** → Step 7: Toast "Submission failed, retry?"
```

### 7.2 Error Handling Flows

```markdown
## Error Flows

### Network Error
```
Click Submit
  → Button: Loading
  → API: timeout after 30s
  → Button: Default
  → Toast: "Network error. Check connection." [Retry] [Cancel]
  → [Retry]: repeat submission
  → [Cancel]: form preserved
```

### Validation Error
```
Click Submit
  → Validate all fields
  → Field1: valid
  → Field2: invalid (format)
    → Field2: border=red, error message below
  → Field3: valid
  → SubmitButton: disabled
  → User fixes Field2
  → User clicks Submit again
  → Validate: all valid
  → Proceed to submission
```

---

## 8. Accessibility (a11y) Inventory

### 8.1 Semantic Elements

```markdown
## Semantic Mapping

| Element | Semantic Tag | ARIA Role | Notes |
|---------|-------------|-----------|-------|
| Page title | `<h1>` | heading | One per page |
| Section title | `<h2>` | heading | Logical hierarchy |
| Button | `<button>` | button | Not <div> |
| Link | `<a>` | link | Not <span> |
| Form | `<form>` | form | With submit handler |
| Input | `<input>` | textbox | With label |
```

### 8.2 Keyboard Navigation

```markdown
## Keyboard Support

| Element | Tab | Enter | Space | Esc |
|---------|-----|-------|-------|-----|
| Button | Focus | Activate | Activate | - |
| Checkbox | Focus | Toggle | Toggle | - |
| Modal | Trap focus | - | - | Close |
| Dropdown | Focus | Open/Select | Open/Select | Close |
| Tabs | Focus | - | - | - |
```

---

## 9. UI Specification Output

### 9.1 Complete Specification Template

```markdown
# UI Specification: <View Name>

## Overview
<Brief description of what this view does>

## Objects

### Display Objects
| ID | Object | Type | Content | States |
|----|--------|------|---------|--------|
| D1 | Title | Label | `{orderId}` | Default |

### Input Objects
| ID | Object | Type | Bound To | Validation |
|----|--------|------|----------|------------|
| I1 | Notes | Textarea | `form.notes` | max:500 |

### Action Objects
| ID | Object | Type | Action | Effect |
|----|--------|------|--------|--------|
| A1 | Save | Button | Click | PUT /api/orders/{id} |

## State Machine
[As per Section 2]

## Data Bindings
[As per Section 4]

## Actions
[As per Section 3]

## Accessibility
[As per Section 8]
```

### 9.2 Feature Implementation Task

```markdown
## Feature: Edit Order Notes

**View:** OrderDetailView
**Type:** UI Feature
**Priority:** P2

### What Exists
- Notes field: D1 (display), I1 (input)
- Current: Display-only, shows `order.notes`
- No edit capability

### What to Implement
1. Add Edit button (A2) next to Notes
2. On click A2: I1 becomes editable, A2 → "Save" / "Cancel"
3. Save: PUT /api/orders/{id}/notes with `form.notes`
4. Cancel: Revert to original value
5. Success: Toast "Notes saved", remain in edit mode
6. Error: Toast "Failed to save", keep edit mode

### Changes

| Change | File | What |
|--------|------|------|
| Add A2 | OrderDetailView | EditButton component |
| Modify I1 | OrderDetailView | Add `readonly` → editable transition |
| Add A3 | OrderDetailView | SaveNotes action |
| Add A4 | OrderDetailView | CancelEdit action |
| Add API | orders.js | PUT /orders/{id}/notes |

### Acceptance Criteria
- [ ] Click Edit → Notes becomes editable
- [ ] Edit button shows "Save" / "Cancel"
- [ ] Save → API called, success toast
- [ ] Cancel → Original value restored
- [ ] Empty notes → Show placeholder "No notes"
```

---

## Validation Checklist

Before declaring UI analysis complete:

- [ ] All objects identified and typed
- [ ] All states documented per object
- [ ] All actions catalogued with pre/post conditions
- [ ] Data bindings traced (source to UI)
- [ ] Form validation rules specified
- [ ] Navigation paths mapped
- [ ] Error handling flows documented
- [ ] Accessibility requirements noted

## Reference

See Planning/PLANNING.md for task conventions.