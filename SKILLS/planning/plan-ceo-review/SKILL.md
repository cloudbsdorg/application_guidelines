# Plan CEO Review Skill

## Metadata
```
author: Mark LaPointe <mark@cloudbsd.org>
version: 1.0.0
platform: CloudBSD / FreeBSD
triggers:
  - "scope"
  - "plan review"
  - "challenge plan"
  - "is this right"
  - "too big"
  - "too small"
  - "effort estimate"
  - "should we do this"
```

## Purpose

Before building, challenge the plan. Is this the RIGHT thing to build? Are we solving the REAL problem?

## CEO Questions (Ask These First)

### 1. Scope Challenge
- "What is the smallest version that delivers value?"
- "What can we cut and still meet the core need?"
- "Is this feature creep disguised as a feature?"

### 2. Effort Challenge
- "What's the realistic timeline?"
- "What are we NOT doing while we do this?"
- "Is the effort proportional to the impact?"

### 3. Problem Challenge
- "Have we confirmed this is a real problem?"
- "Who asked for this? How many others want it?"
- "What happens if we don't do it?"

### 4. Solution Challenge
- "Is there a simpler solution?"
- "Can we solve this with configuration instead of code?"
- "Is this the right approach for FreeBSD?"

## Analysis Framework

### Impact vs Effort Matrix
```
                    Low Effort          High Effort
High Impact    ┌─────────────────┬─────────────────┐
               │  DO FIRST        │  PLAN CAREFULLY │
               │  Quick wins      │  Strategic      │
High Impact    ├─────────────────┼─────────────────┤
               │  DEPENDS         │  CHALLENGE       │
Low Impact     │  Is it really    │  Why bother?     │
               │  high impact?    │  Defer or skip   │
               └─────────────────┴─────────────────┘
```

### FreeBSD-Specific Considerations
- Is bhyve, jails, ZFS, or rc.d involvement necessary?
- Does this need kernel-level changes?
- Will this survive a version upgrade?
- Is this portable across FreeBSD versions?

## Output Format

After review, produce:
```
## Plan Review

**Verdict**: APPROVE / CHALLENGE / REDUCE / REJECT

**If CHALLENGE/REDUCE:**
- Specific concerns
- What needs rethinking
- Proposed alternative scope

**If APPROVE:**
- Confirmed core scope
- Key milestones
- Success criteria

**If REJECT:**
- Reasons
- What would need to change for reconsideration
```

## Completion

- [ ] Scope has been challenged
- [ ] Effort estimate validated
- [ ] Problem confirmed (not assumed)
- [ ] Alternative solutions considered
- [ ] FreeBSD fit assessed
- [ ] Decision documented
