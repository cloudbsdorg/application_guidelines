

# Unit Testing Guidelines for CloudBSD Applications

This document describes the standards for unit testing to ensure the reliability and maintainability of CloudBSD software.

## 1. Testing Philosophy

### Test-Driven Development (TDD) — LAW

Red-green TDD is **mandatory**, not optional, not "aim for tests sometime."

For **new work** (features, bug fixes, new modules):

1. **Red**: Write a failing test first. Confirm it fails for the right reason.
2. **Green**: Write the minimum production code to make that test pass.
3. **Refactor**: Clean up while tests stay green.

Do not write production code before a failing test exists.

For **existing code that shipped without tests**: missing tests are a **defect**. You MUST still add tests. Characterization / post-facto tests are allowed: lock current behavior with tests before changing it, then apply red-green for the change. Shipping or modifying untested application code without adding tests is a violation.

### Scope of Unit Tests
- **Isolated**: Unit tests should test a single unit of work (e.g., a function or a method) in isolation.
- **Fast**: Unit tests must be fast to encourage frequent execution during development.

## 2. Best Practices

### Writing Effective Tests
- **Clear Names**: Use descriptive test names that explain the expected behavior (e.g., `test_calculate_tax_for_zero_income`).
- **Single Assertion**: Aim for a single logical assertion per test to make failures easier to diagnose.
- **Independence**: Tests must not depend on each other or on a specific execution order.

### Code Coverage
- **Target Coverage**: As close to **100%** code coverage as possible. Critical paths (e.g., security, data processing, auth, reload, config parsing) **must be 100%**. The old 80% target is withdrawn.
- **Exclusions**: Generated and vendored code may be excluded from coverage. **Application code may not.**
- **Meaningful Coverage**: Coverage percentage is not a substitute for high-quality, diverse test cases (including edge cases and negative cases).

### Mocking and Stubs
- **External Dependencies**: Use mocks and stubs for external dependencies like databases, networks, or file systems to maintain test speed and isolation.
- **Mocking Overuse**: Be careful not to over-mock to the point where the test no longer reflects real-world behavior.

## 3. Tooling and Frameworks

### Recommended Frameworks
- **C/C++**: `Google Test` or `cmocka`.
- **Go**: Use the built-in `testing` package. Use `testify` for assertions if needed.
- **Rust**: Use the built-in testing framework with `cargo test`.
- **Python**: `pytest` is the preferred choice for its power and simplicity.
- **Java**: Use JUnit for testing. Consider Mockito for mocking.
- **TypeScript**: `Jest` is a popular choice for unit testing.

## 4. Continuous Integration (CI)

### CI Integration
- **Mandatory Checks**: All tests must pass before code is merged into the main branch.
- **Automated Execution**: Use CI pipelines (e.g., GitHub Actions, GitLab CI, Jenkins) to run tests automatically on every commit and pull request.
- **Coverage Reports**: Integrate coverage reports into the CI pipeline to monitor trends over time.
- **Create Configurations**: Create separate configurations for different environments (e.g., development, staging, production) to ensure tests are run with the appropriate settings. Make Jenkinsfiles, TeamCity configurations, GitHub Actions workflows, Azure Pipelines, bazel if needed.


## 5. Evidence and integration (LAW)

A task is not complete until there is evidence it works. "I ran it" without captured output is not evidence.

### What counts
- Red-green unit and integration tests, with output (TAP, JUnit XML, JSON, or the runner log) stored with the change.
- Coverage reports. Target near-100%; critical paths 100%.
- Characterization tests for already-shipped untested code.

### Integration tests are law

Unit tests alone are not enough. Integration tests MUST exercise real seams, including:
- HTTP API + store
- Worker job commit
- SIGHUP reload (validate then apply; bad config keeps the old process)
- Tenant isolation across gateway/worker

In-memory fakes are allowed when the seam itself is under test. Substituting a fake for the seam you claim to be testing is a defect. Compile-only is not evidence.

### APIs

API tests hit application DTOs (request/response shapes the product actually uses), not compiler success or generated stubs.

### Missing tools

If a test tool is not installed, find one. Make one if needed. Skipping validation because a required tool is missing is a defect.

### Store evidence with the change

CI artifacts, `testdata/`, committed screenshots for UI proof, or a clearly named report path (for example `artifacts/test-report/`). The path must be findable from the PR or commit.

