---
name: ship
description: >-
  Deploy only with the evidence CloudBSD law requires - tests, coverage, man
  page lint, PR, then deploy. Use when asked to ship, release, publish, or
  push to production, and to stop a release that has no captured evidence
  behind it.
keywords:
  - ship
  - deploy
  - release
  - publish
  - push to prod
  - cut a release
---

# Ship Skill


## Ship Protocol

Ship is NOT just "git push". Ship means: **verified, tested, documented, deployed**.

## Pre-Ship Checklist

### 1. Tests Pass
- [ ] Unit tests pass: `make test` or `pytest` or `go test`
- [ ] Integration tests pass (if applicable)
- [ ] No regression in existing functionality

### 2. Coverage Acceptable
- [ ] New code has tests
- [ ] Critical paths covered
- [ ] Report generated (if applicable)

### 3. Linting Clean
- [ ] `flake8` / `golangci-lint` / `rustfmt` / `clang-format` passes
- [ ] No new warnings introduced

### 4. Documentation Updated
- [ ] CHANGELOG updated with this change
- [ ] README reflects new behavior (if user-facing)
- [ ] Inline comments for complex logic

### 5. Commit Properly Structured
- [ ] Conventional commits format: `type(scope): description`
- [ ] Types: `fix:`, `feat:`, `docs:`, `refactor:`, `test:`, `chore:`
- [ ] Body explains WHY, not just WHAT
- [ ] References issues: `Fixes #123`

### 6. Pull Request Ready
- [ ] PR description explains motivation and solution
- [ ] Reviewers assigned
- [ ] Labels applied

## Deployment (FreeBSD-Specific)

### Service Deployment
```bash
# Build
make build

# Test in staging
sudo make install-staging
sudo service $name test

# Deploy
sudo make install
sudo service $name restart

# Verify
sudo service $name status
```

### Jail Deployment
```bash
# Snapshot before
zfs snapshot tank/jails/$jail@pre-deploy

# Deploy
jexec $jail service $name restart

# Verify
jexec $jail service $name status
```

### Package Deployment
```bash
# Build package
make pkg

# Upload to repo
make publish

# Clients update
pkg update && pkg upgrade
```

## Rollback Plan

Before every deploy, know how to rollback:
- Git rollback: `git revert $commit`
- Package rollback: reinstall the previous version from the repository
  (`pkg install -f <pkg>-<previous-version>`); there is no `pkg rollback`
- Jail rollback: `jexec $jail zfs rollback tank/jails/$jail@pre-deploy`

## Hard Blocks (NEVER Ship With)

- Failing tests
- Known security vulnerabilities (`pkg audit` failing)
- Credentials or secrets in code
- Hardcoded production endpoints
- Unverified database migrations

## Artifacts

When the thing being shipped is a **binary artifact** - a package, a kernel or
module, install media, a VM image - the change-level checklist above is not
enough. See [artifact-release](../../release/artifact-release/SKILL.md) for
what must be verified about the artifact itself before it is published.

## Post-Ship

- [ ] Smoke test production
- [ ] Monitor error rates
- [ ] Verify healthchecks
- [ ] Announce in relevant channel
