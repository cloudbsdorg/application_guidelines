---
name: risk assessor
description: Create and maintain risk registers following CloudBSD risk management conventions.
---

# Skill: risk-assessor

**Purpose:** Create and maintain risk registers following CloudBSD risk management conventions.

**Triggers:** When creating the 700 document, during risk review, or when new risks are identified.

## Loading Instructions

Load this skill when the user asks you to:
- Create a risk register
- Add a new risk
- Review and update risks
- Assess risk probability and impact
- Create mitigation strategies

## Risk Register Table Format

```markdown
| Risk ID | Description | Probability | Impact | Mitigation | Status |
|---------|-------------|-------------|--------|------------|--------|
| R001 | Kernel panic under peak load | Low | High | Rate limiting, circuit breakers | OPEN |
| R002 | Memory leak in worker pool | Medium | High | Memory profiling, automatic restart | OPEN |
| R003 | Network partition causing split-brain | Low | Critical | Quorum mechanism, fencing | OPEN |
```

## Risk ID Convention

Format: `R<Category><Number>`

| Category | Description |
|----------|-------------|
| T | Technical risks |
| S | Schedule risks |
| R | Resource risks |
| E | External risks |

Examples:
- `R001` — First technical risk
- `S001` — First schedule risk
- `E001` — First external risk

## Probability Scale

| Level | Description | Annual Likelihood |
|-------|-------------|-------------------|
| Very Low | Almost never | < 5% |
| Low | Unlikely | 5-20% |
| Medium | Possible | 20-50% |
| High | Likely | 50-80% |
| Very High | Almost certain | > 80% |

## Impact Scale

| Level | Description | Effect |
|-------|-------------|--------|
| Low | Minor | Easily recoverable |
| Medium | Moderate | recoverable with effort |
| High | Significant | Major delays, substantial cost |
| Critical | Severe | Project failure, safety issue |

## Risk Score Calculation

```
Risk Score = Probability × Impact

Very Low × Low      = 1  (Accept)
Low × Medium        = 2  (Monitor)
Medium × High       = 6  (Mitigate)
High × Critical     = 12 (Critical - immediate action)
```

## Risk Score Matrix

|          | Low Impact | Medium Impact | High Impact | Critical Impact |
|----------|-----------|---------------|-------------|-----------------|
| Very Low | 1 | 2 | 3 | 4 |
| Low      | 2 | 4 | 6 | 8 |
| Medium   | 3 | 6 | 9 | 12 |
| High     | 4 | 8 | 12 | 16 |
| Very High| 5 | 10 | 15 | 20 |

## Action Thresholds

| Score | Action |
|-------|--------|
| 1-3 | Accept (monitor) |
| 4-6 | Mitigate (plan within current sprint) |
| 7-12 | High priority (immediate attention) |
| 13+ | Critical (escalate immediately) |

## Risk Response Strategies

### Avoid
Change architecture or approach to eliminate the risk entirely.

### Mitigate
Reduce probability or impact through controls.

### Transfer
Shift risk to third party (insurance, contracts).

### Accept
Acknowledge risk and prepare contingency.

## Common Risk Patterns

### Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Kernel module crash | Medium | High | Strict testing in VM, panic handlers |
| Memory corruption | Low | Critical | ASAN/MSAN, memory scrubbers |
| Race conditions | Medium | High | Thread sanitizer, careful locking |
| Performance degradation | Medium | Medium | Profiling, benchmarks |

### Schedule Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Missing expertise | Medium | High | Training, external consultants |
| Requirement changes | High | Medium | Agile approach, scope management |
| Integration delays | Medium | Medium | Early integration testing |

### Resource Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Budget overrun | Low | High | Contingency budget (20%) |
| Resource availability | Medium | Medium | Multi-skilled team |
| Hardware access | Low | Medium | Emulation environments |

### External Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Dependency failure | Low | High | Multiple sources |
| Third-party API changes | Medium | Medium | Abstraction layer |
| Regulatory changes | Low | High | Compliance monitoring |

## Risk Review Protocol

1. Review risk register monthly
2. Update status (OPEN → MITIGATED → CLOSED)
3. Add new risks as identified
4. Remove risks that no longer apply
5. Re-assess probability/impact after mitigations

## Contingency Planning

For each high-priority risk:

```markdown
### R<Id>: <Risk Title>

**Current Status**: OPEN
**Risk Score**: <score>

**Mitigation Plan**:
- <Step 1>
- <Step 2>

**Contingency Plan** (if mitigation fails):
- <Fallback action 1>
- <Fallback action 2>

**Escalation Path**:
1. <Team lead>
2. <Engineering manager>
3. <CTO>
```

## Document Structure

```markdown
# <Project> Planning — Risks

**Document ID:** <Project>-Risks
**Version:** 1.0
**Last Updated:** YYYY-MM-DD
**Maintainer:** <Team>
**Status:** ACTIVE
**Classification:** INTERNAL

---

## Executive Summary

<Overview of risk landscape>

## Risk Register

| Risk ID | Description | Probability | Impact | Mitigation | Status |
|---------|-------------|-------------|--------|------------|--------|
| ... | ... | ... | ... | ... | ... |

## High-Priority Risks

### R001: <Title>
...

## Risk Trend

<Chart or description of risk evolution>

---

## Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | YYYY-MM-DD | Name | Initial version |

**Last Updated:** YYYY-MM-DD HH:MM UTC
**Classification:** INTERNAL
```

## Reference

See Planning/PLANNING.md Section 3.11 (Risks) for full specification.