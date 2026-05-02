# Skill: code-quality-analyzer

**Purpose:** Identify code duplication, extract interfaces and abstractions, and plan refactoring during or after porting.

**Triggers:** During code analysis for porting, or when reviewing ported code for quality issues.

## Loading Instructions

Load this skill when the user asks you to:
- Analyze code for duplication
- Find interface opportunities
- Refactor repeated code patterns
- Plan abstraction improvements
- Review ported code quality

## Core Principle

> **Duplication is easier to spot than abstraction is to design. Find the duplication first, then decide if abstraction earns its keep.**

---

## 1. Duplication Detection

### 1.1 Types of Duplication

| Type | Description | Severity |
|------|-------------|----------|
| **Exact copy-paste** | Same code repeated verbatim | High |
| **Near-duplicate** | Same logic, different variable names | High |
| **Structural** | Same loop/condition pattern repeated | Medium |
| **Semantic** | Same purpose, different implementation | Low |

### 1.2 Detection Strategy

```bash
# Exact duplication (same file)
grep -n "func.*(" file.go | uniq -d

# Similar functions in same file
grep -A 20 "func.*(" file.go > funcs.txt
diff funcs.txt funcs.txt  # manual inspection

# Copy-paste detection across files
rg "TODO\|FIXME\|XXX" --type go  # comments might indicate copy-paste
```

### 1.3 Duplication Report Template

```markdown
## Duplication Report

### Exact Duplicates

| Location 1 | Location 2 | Lines | Evidence |
|------------|------------|-------|----------|
| auth.go:15-25 | auth.go:30-40 | 11 | Identical validation logic |
| handler.go:50-62 | handler.go:70-82 | 13 | Same error handling pattern |

### Near-Duplicates

| Location 1 | Location 2 | Similarity | Merge Candidate |
|------------|------------|------------|-----------------|
| users.go:10-25 | groups.go:10-25 | 85% | Yes - extract to base class |

### Recommendations
- **Priority 1:** Merge auth.go:15-25 and auth.go:30-40 (exact duplicate)
- **Priority 2:** Extract base class for users.go and groups.go (85% similar)
```

---

## 2. Interface Opportunity Detection

### 2.1 Signs an Interface Is Needed

```go
// Multiple implementations of same concept
func processUsers(u *MySQLUserStore) { ... }
func processUsers(u *PostgresUserStore) { ... }
func processUsers(u *InMemoryUserStore) { ... }

// Functions accepting many similar concrete types
func validate(v *ValidatorA) { ... }
func validate(v *ValidatorB) { ... }
func validate(v *ValidatorC) { ... }

// Switch statements on type
switch v := node.(type) {
case *UserNode: ...
case *GroupNode: ...
case *PermNode: ...
}
```

### 2.2 Interface Detection Template

```markdown
## Interface Opportunities

### Store Pattern

**Current:** Multiple concrete store implementations

| Implementation | File | Methods |
|----------------|------|---------|
| MySQLUserStore | mysql.go | Create, Read, Update, Delete |
| PostgresUserStore | postgres.go | Create, Read, Update, Delete |
| InMemoryUserStore | memory.go | Create, Read, Update, Delete |

**Proposed Interface:**
```go
type UserStore interface {
    Create(user *User) error
    Read(id string) (*User, error)
    Update(user *User) error
    Delete(id string) error
}
```

**Benefit:** Swap implementations without changing business logic.

### Validator Pattern

**Current:** Type switch for validation

```go
switch v := node.(type) {
case *UserNode: validateUser(v)
case *GroupNode: validateGroup(v)
case *PermNode: validatePerm(v)
}
```

**Proposed Interface:**
```go
type Validatable interface {
    Validate() error
}
```

**Benefit:** Remove type switch, each type validates itself.
```

### 2.3 Interface Extraction Steps

```markdown
## Interface Extraction Workflow

1. **Identify common operations**
   - List all methods with same/similar names across types
   - Note parameter types and return types

2. **Define minimal interface**
   - Only include methods that are ACTUALLY CALLED in common code
   - Don't model the full type, model the usage

3. **Verify with existing implementations**
   - Confirm each concrete type has matching methods
   - Note any missing method implementations

4. **Refactor callers**
   - Change function signatures to accept interface
   - Verify behavior unchanged
```

---

## 3. Abstract Class / Base Class Detection

### 3.1 Signs a Base Class Is Needed

```go
// Almost identical structs with tiny differences
type UserHandler struct {
    db *MySQL
    logger *Logger
    metrics *Prometheus
}

type GroupHandler struct {
    db *MySQL
    logger *Logger
    metrics *Prometheus
    // Same fields as UserHandler!
}

type PermissionHandler struct {
    db *MySQL
    logger *Logger
    metrics *Prometheus
    // Same fields again!
}
```

### 3.2 Base Class Detection Template

```markdown
## Base Class Opportunities

### Handler Pattern

**Current:** Three nearly identical structs

| Field | UserHandler | GroupHandler | PermissionHandler |
|-------|-------------|--------------|-------------------|
| db | *MySQL | *MySQL | *MySQL |
| logger | *Logger | *Logger | *Logger |
| metrics | *Prometheus | *Prometheus | *Prometheus |
| cache | *Cache | *Cache | *Cache |
| -- | -- | customField | -- |

**Observation:** 4/5 fields identical. Extract BaseHandler.

**Proposed:**
```go
type BaseHandler struct {
    db      *MySQL
    logger  *Logger
    metrics *Prometheus
    cache   *Cache
}

type UserHandler struct {
    *BaseHandler  // embedding = inheritance
}

type GroupHandler struct {
    *BaseHandler
    customField string
}
```

### Similar Code Patterns

```go
// Same initialization sequence
func NewUserHandler() *UserHandler {
    h := &UserHandler{}
    h.db = connectDB()
    h.logger = newLogger()
    h.metrics = newMetrics()
    h.cache = newCache()
    return h
}

func NewGroupHandler() *GroupHandler {
    h := &GroupHandler{}
    h.db = connectDB()        // Same
    h.logger = newLogger()    // Same
    h.metrics = newMetrics()  // Same
    h.cache = newCache()      // Same
    return h
}
```

**Proposed:** Extract `initBase()` method or constructor helper.
```

---

## 4. Design Pattern Opportunities

### 4.1 Common Patterns in Enterprise Code

| Pattern | When to Use | Sign |
|---------|-------------|------|
| **Strategy** | Multiple algorithms for same task | `switch algo` statements |
| **Template Method** | Same skeleton, different steps | Overridden methods calling hooks |
| **Factory** | Complex object creation | `NewX()`, `NewY()` with switch |
| **Decorator** | Add behavior dynamically | Wrapping/wrapper functions |
| **Observer** | Event notification | Callback lists, event listeners |
| **Repository** | Data access abstraction | Store pattern above |

### 4.2 Strategy Pattern Detection

```go
// BEFORE: Switch on algorithm type
func Process(data []byte, algo string) ([]byte, error) {
    switch algo {
    case "gzip":
        return gzipCompress(data)
    case "zstd":
        return zstdCompress(data)
    case "lz4":
        return lz4Compress(data)
    }
}

// AFTER: Strategy interface
type Compressor interface {
    Compress([]byte) ([]byte, error)
}

func Process(data []byte, c Compressor) ([]byte, error) {
    return c.Compress(data)
}
```

### 4.3 Template Method Detection

```go
// BEFORE: Similar methods with slight differences
func (h *UserHandler) Create(ctx context.Context, u *User) error {
    h.log("creating user")
    h.metrics.Inc("user.create")
    if err := h.db.Create(ctx, u); err != nil {
        h.log("create failed: %v", err)
        return err
    }
    h.log("user created")
    return nil
}

func (h *GroupHandler) Create(ctx context.Context, g *Group) error {
    h.log("creating group")        // Same
    h.metrics.Inc("group.create") // Different metric
    if err := h.db.Create(ctx, g); err != nil {
        h.log("create failed: %v", err) // Same
        return err
    }
    h.log("group created")         // Same
    return nil
}

// AFTER: Template Method
type Creatable interface {
    ResourceName() string
    TableName() string
}

func (h *BaseHandler) Create(ctx context.Context, res Creatable) error {
    h.log("creating %s", res.ResourceName())
    h.metrics.Inc(res.ResourceName() + ".create")
    if err := h.db.Create(ctx, res); err != nil {
        h.log("create failed: %v", err)
        return err
    }
    h.log("%s created", res.ResourceName())
    return nil
}
```

---

## 5. Refactoring Planning

### 5.1 Refactoring Priority

| Priority | Pattern | Impact | Effort | When |
|----------|---------|--------|--------|------|
| P0 | Exact duplicates | High | Low | Always fix |
| P1 | Interface extraction | High | Medium | When 3+ implementations |
| P2 | Base class extraction | Medium | High | When 3+ handlers |
| P3 | Design pattern refactor | Medium | High | After basic structure |

### 5.2 Refactoring Task Template

```markdown
## Refactoring Task: <Name>

**Problem:** <Description of duplication or design issue>
**Impact:** <Why this matters>
**Effort:** <Low/Medium/High>

### Current State
```go
// code before
```

### Proposed State
```go
// code after
```

### Migration Steps
1. Define interface/base class
2. Update one consumer to use abstraction
3. Test thoroughly
4. Update remaining consumers
5. Remove old duplicate code

### Risk
- <What could go wrong>
- <How to mitigate>
```

---

## 6. Application to Porting

### 6.1 Porting-Specific Considerations

When porting code, you have a choice:

| Option | Pros | Cons |
|--------|------|------|
| **Port as-is** | Faster, lower risk | Technical debt remains |
| **Port + refactor** | Better quality | Longer, more risk |
| **Refactor after port** | Clean separation | Might miss issues during port |

**Recommendation:** Port as-is first, refactor after working port is complete.

### 6.2 Document Issues for Later

```markdown
## Refactoring Backlog

| Issue | Type | Severity | Port Issue | Fix After |
|-------|------|----------|------------|-----------|
| UserStore, GroupStore identical | Base class | Medium | Already exists | Port complete |
| Type switch in validator | Interface | High | Port as-is | Port complete |
| 5 identical NewHandler funcs | Extract helper | Low | Already exists | Cleanup phase |
```

### 6.3 Preserve Behavior

> **When refactoring, the output must be identical. If tests pass before and after, you're doing it right.**

---

## Validation Checklist

Before declaring analysis complete:

- [ ] Scanned for exact duplicates
- [ ] Found near-duplicate patterns
- [ ] Identified interface opportunities (3+ implementations)
- [ ] Identified base class opportunities (5+ shared fields)
- [ ] Found switch/type-case patterns convertible to interfaces
- [ ] Created refactoring backlog with priorities
- [ ] Distinguished "port now" vs "refactor after port"

## Reference

See Planning/PLANNING.md for task conventions.