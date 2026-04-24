# Testing Infrastructure Guidelines for CloudBSD Applications

This document outlines the standards and best practices for testing CloudBSD applications using VMM virtual machines (bhyve) and FreeBSD jails. The goal is to provide a safe, isolated, and reproducible testing environment for kernel-level and userland components.

**Primary Recommendation:** Use bhyve VMs for kernel-level testing and jails for userland isolation testing, with a unified orchestration layer for machine lifecycle management and output collection.

---

## 1. Executive Summary

CloudBSD applications must be tested in environments that match the production target platform (FreeBSD). Two primary isolation mechanisms are available:

- **VMM / bhyve**: Full virtualization using FreeBSD's native hypervisor. Required for any testing that loads kernel modules, modifies kernel data structures, or exercises kernel code paths.
- **FreeBSD Jails**: OS-level virtualization. Suitable for userland application testing, network service isolation, and rapid iteration where kernel involvement is minimal.

This document establishes how to create testing machines, collect output properly for AI agents to act on, and integrate these environments into CI/CD pipelines.

---

## 2. Current State Analysis

### 2.1 Testing Requirements by Component Type

| Component Type | Example | Requires Kernel? | Recommended Environment |
|--------------|---------|-----------------|----------------------|
| Kernel modules | `ng_pppoe`, custom drivers | **Yes** | bhyve VM |
| System daemons | `pppoed`, `sshd` | No (userland only) | Jail or bhyve VM |
| Network stacks | Custom protocols, netgraph nodes | **Yes** | bhyve VM |
| Web frontends | React applications | No | Jail |
| TUI applications | Console tools | No | Jail |
| Configuration | rc.d scripts, sysctls | Varies | Jail (safe) or VM (kernel-modifying) |

### 2.2 Current Limitations

- **Host system risk:** Loading untested kernel modules on the development host can cause panics, data loss, or security compromise.
- **Reproducibility:** Manual testing environments are often inconsistent between developer machines.
- **Output collection:** Kernel printf/debug output, console messages, and crash dumps require special handling to extract from VMs.
- **CI integration:** Existing CI pipelines typically run on Linux containers, not FreeBSD-native environments.
- **Agent observability:** AI agents need structured, parseable output from test runs to make decisions (pass/fail, retry, fix).

---

## 3. Proposed Architecture: Unified Testing Orchestration

### 3.1 High-Level Design

```
+-------------------------------------------------------------+
|                    CI/CD Controller (GitHub Actions / Jenkins)  |
|                      (Linux or FreeBSD host)                  |
+----------------------------+--------------------------------+
                             |
              +--------------+--------------+
              |                             |
              v                             v
+-------------------------------------------------------------+
|              Testing Orchestration Layer (FreeBSD host)         |
|  - Manages VM lifecycle (create, start, stop, destroy)        |
|  - Manages jail lifecycle (create, start, stop, destroy)    |
|  - Collects output (console, logs, crash dumps, test results) |
|  - Exposes structured API for CI and AI agents               |
+--+-----------+-----------+-----------+-----------+----------+
   |           |           |           |           |
   v           v           v           v           v
+------+   +------+   +------+   +------+   +------+
|bhyve |   |bhyve |   |bhyve |   | Jail |   | Jail |
| VM 0 |   | VM 1 |   | VM 2 |   |  #0  |   |  #1  |
+------+   +------+   +------+   +------+   +------+
```

### 3.2 Key Design Principles

1. **Host safety:** Kernel testing must never run on the development or CI host directly.
2. **Reproducibility:** All test environments are defined as code (VM images, jail templates, configuration scripts).
3. **Structured output:** All test output must be collected in formats parseable by AI agents (JSON, TAP, JUnit XML).
4. **Incremental testing:** Userland tests in jails are fast; kernel tests in VMs are thorough. Run jail tests first, VM tests second.
5. **Snapshot discipline:** VMs and jails start from known-clean snapshots. Any mutation is discarded after the test run.

---

## 4. Implementation Details

### 4.1 bhyve VM Testing Environment

#### 4.1.1 VM Image Preparation

Create a base FreeBSD VM image with all CloudBSD dependencies pre-installed:

```sh
# On FreeBSD host with VMM support
sudo pkg install -y vm-bhyve bhyve-firmware uefi-edk2-bhyve

# Create VM storage pool
sudo zfs create zroot/vm

# Fetch base image (automated in CI)
fetch https://download.freebsd.org/ftp/releases/VM-IMAGES/14.2-RELEASE/amd64/Latest/FreeBSD-14.2-RELEASE-amd64.raw.xz
xz -d FreeBSD-14.2-RELEASE-amd64.raw.xz

# Convert to ZFS volume for snapshotting
sudo zfs create -V 20G zroot/vm/base
sudo dd if=FreeBSD-14.2-RELEASE-amd64.raw of=/dev/zvol/zroot/vm/base bs=1M

# Install CloudBSD base dependencies
sudo pkg -c /zroot/vm/base install -y git cmake python3 py39-pytest

# Create golden snapshot
sudo zfs snapshot zroot/vm/base@golden
```

#### 4.1.2 Host Environment Verification

Before creating or starting bhyve VMs, verify that the host environment is actually FreeBSD and that VMM support is available. AI agents and automated scripts may incorrectly detect the host OS when running inside containers, jails, or over SSH sessions.

```sh
# Verify actual host OS — do not trust language runtime or container reports
uname -s
# Expected output: FreeBSD

# Verify VMM kernel module is loaded
kldstat | grep vmm
# If empty, load it:
sudo kldload vmm

# Verify hardware virtualization support
sysctl hw.vmm
# Expected: hw.vmm: 1
```

**Mandatory checks:**
- **Always run `uname -s`** to confirm the host OS before executing platform-specific commands.
- **Always verify `vmm` is loaded** with `kldstat | grep vmm` before invoking `bhyve` or `vm-bhyve`.
- **Never assume the environment** reported by Python `platform.system()`, Node `os.platform()`, or similar abstractions is accurate.

#### 4.1.3 VM Lifecycle Script

```sh
#!/bin/sh
# /usr/local/libexec/cloudbsd/vm-test-runner.sh

VM_NAME="${VM_NAME:-testvm}"
VM_IMAGE="${VM_IMAGE:-zroot/vm/base}"
VM_CPUS="${VM_CPUS:-2}"
VM_MEM="${VM_MEM:-2G}"
TEST_SCRIPT="${TEST_SCRIPT:-/usr/local/libexec/cloudbsd/default-test.sh}"
OUTPUT_DIR="${OUTPUT_DIR:-/var/tmp/cloudbsd-test-output}"

mkdir -p "${OUTPUT_DIR}"

# Clone from golden snapshot (instant)
sudo zfs clone "${VM_IMAGE}@golden" "zroot/vm/${VM_NAME}"

# Start VM with console output captured to file
sudo /usr/sbin/bhyve \
    -c "${VM_CPUS}" -m "${VM_MEM}" \
    -H -P -s 0:0,hostbridge \
    -s 1:0,virtio-net,tap0 \
    -s 2:0,virtio-blk,/dev/zvol/zroot/vm/${VM_NAME} \
    -s 31:0,lpc \
    -l com1,stdio \
    "${VM_NAME}" > "${OUTPUT_DIR}/console.log" 2>&1 &

BHYVE_PID=$!

# Wait for VM to boot (health check via SSH or serial)
sleep 30

# Copy test script into VM (via mounted ZFS or virtio-9p)
# ... mechanism depends on image capabilities

# Run tests inside VM, collect structured output
ssh -o StrictHostKeyChecking=no -i /usr/local/etc/cloudbsd/vm-test-key \
    root@"${VM_IP}" \
    "sh ${TEST_SCRIPT}" > "${OUTPUT_DIR}/test-results.json" 2> "${OUTPUT_DIR}/test-errors.log"

TEST_EXIT=$?

# Collect kernel messages
dmesg > "${OUTPUT_DIR}/dmesg.log" 2>/dev/null || true

# Collect crash dumps if present
if [ -f /zroot/vm/${VM_NAME}/var/crash/vmcore.* ]; then
    cp /zroot/vm/${VM_NAME}/var/crash/vmcore.* "${OUTPUT_DIR}/"
fi

# Destroy VM and clone
sudo kill "${BHYVE_PID}" 2>/dev/null || true
sleep 2
sudo zfs destroy "zroot/vm/${VM_NAME}"

exit ${TEST_EXIT}
```

#### 4.1.4 Console Output Collection

bhyve VMs must have console output captured for AI agent analysis:

| Output Type | Collection Method | Purpose |
|-------------|------------------|---------|
| Serial console | `-l com1,stdio` redirected to file | Boot messages, kernel panics, early console |
| SSH session | `ssh command > file` | Structured test output, command results |
| Kernel messages | `dmesg` after test run | Module load verification, driver probe status |
| Crash dumps | Copy from `/var/crash` inside VM image | Post-mortem analysis with `kgdb` |
| Network capture | `tcpdump` on host tap interface | Protocol-level verification |

#### 4.1.5 Build Performance Best Practices

When building the FreeBSD kernel, world, or large software projects inside VMs or on the host, always use parallel compilation with the `-j` flag. Building large items single-threaded severely impacts performance and test cycle time.

```sh
# Determine the number of CPUs and use it for parallel builds
make -j$(sysctl -n hw.ncpu) buildworld
make -j$(sysctl -n hw.ncpu) buildkernel

# For kernel module builds inside a test VM
cd /usr/src
make -j$(sysctl -n hw.ncpu) buildkernel KERNCONF=CLOUDBSD
```

- **Always specify `-j`**: Never run `make buildworld`, `make buildkernel`, or large compilations without the `-j` flag.
- **Match to available vCPUs**: Use `-j$(sysctl -n hw.ncpu)` to automatically match the job count to the VM's allocated CPUs.
- **CI pipelines**: Ensure CI configurations set `VM_CPUS` high enough to benefit from parallel builds.

### 4.2 FreeBSD Jail Testing Environment

#### 4.2.1 Jail Template Preparation

```sh
# Create base jail from release
sudo fetch -o /tmp/base.txz https://download.freebsd.org/ftp/releases/amd64/14.2-RELEASE/base.txz
sudo mkdir -p /zroot/jail/base
sudo tar -xJf /tmp/base.txz -C /zroot/jail/base

# Install CloudBSD dependencies
sudo pkg -c /zroot/jail/base install -y git cmake python3 py39-pytest curl

# Create golden snapshot
sudo zfs snapshot zroot/jail/base@golden
```

#### 4.2.2 Jail Host Verification

Before creating jails, verify that the host environment is actually FreeBSD. AI agents and orchestration scripts may run on containerized or remote hosts that do not match the target jail platform.

```sh
# Verify actual host OS — do not trust language runtime or container reports
uname -s
# Expected output: FreeBSD

# Verify jail support is available
sysctl security.jail.jailed
# Expected: security.jail.jailed: 0 (host is not itself jailed)
```

**Mandatory checks:**
- **Always run `uname -s`** to confirm the host OS before executing platform-specific commands.
- **Never assume the environment** reported by Python `platform.system()`, Node `os.platform()`, or similar abstractions is accurate.

#### 4.2.3 Jail Lifecycle Script

```sh
#!/bin/sh
# /usr/local/libexec/cloudbsd/jail-test-runner.sh

JAIL_NAME="${JAIL_NAME:-testjail}"
JAIL_BASE="${JAIL_BASE:-zroot/jail/base}"
OUTPUT_DIR="${OUTPUT_DIR:-/var/tmp/cloudbsd-test-output}"
TEST_SCRIPT="${TEST_SCRIPT:-/usr/local/libexec/cloudbsd/default-test.sh}"

mkdir -p "${OUTPUT_DIR}"

# Clone from golden snapshot
sudo zfs clone "${JAIL_BASE}@golden" "zroot/jail/${JAIL_NAME}"

# Create jail.conf snippet
cat > /tmp/${JAIL_NAME}.conf <<EOF
${JAIL_NAME} {
    host.hostname = "${JAIL_NAME}.cloudbsd.test";
    ip4.addr = 127.0.1.1;
    path = "/zroot/jail/${JAIL_NAME}";
    exec.start = "${TEST_SCRIPT} > /tmp/test-output.json 2> /tmp/test-errors.log; exit 0";
    exec.stop = "";
    persist = false;
}
EOF

# Start jail and run test
sudo jail -f /tmp/${JAIL_NAME}.conf -c "${JAIL_NAME}"

# Collect output
sudo cp "/zroot/jail/${JAIL_NAME}/tmp/test-output.json" "${OUTPUT_DIR}/test-results.json"
sudo cp "/zroot/jail/${JAIL_NAME}/tmp/test-errors.log" "${OUTPUT_DIR}/test-errors.log"

# Destroy jail and clone
sudo jail -r "${JAIL_NAME}"
sudo zfs destroy "zroot/jail/${JAIL_NAME}"
```

#### 4.2.4 Jail Output Collection

| Output Type | Collection Method | Purpose |
|-------------|------------------|---------|
| Test results | Copy from `/tmp/test-output.json` inside jail | Structured pass/fail data |
| Service logs | Copy from `/var/log` inside jail | Application behavior verification |
| Network traces | `tcpdump` on host `lo` interface | Jail network isolation verification |
| Process tree | `ps aux` from host before jail destruction | Resource leak detection |

### 4.3 Unified Orchestration API

Both VM and jail test runners must expose a unified interface:

```json
{
  "test_run_id": "uuid-v4-string",
  "environment_type": "bhyve|jail",
  "environment_name": "test-vm-001",
  "start_time": "2026-04-23T19:46:00Z",
  "end_time": "2026-04-23T19:48:00Z",
  "exit_code": 0,
  "artifacts": {
    "console_log": "/var/tmp/cloudbsd-test-output/uuid/console.log",
    "test_results": "/var/tmp/cloudbsd-test-output/uuid/test-results.json",
    "kernel_messages": "/var/tmp/cloudbsd-test-output/uuid/dmesg.log",
    "crash_dumps": [],
    "network_captures": []
  },
  "structured_results": {
    "tests_total": 150,
    "tests_passed": 148,
    "tests_failed": 2,
    "tests_skipped": 0,
    "duration_ms": 120000
  }
}
```

---

## 5. Testing Strategy

### 5.1 Test Pyramid for CloudBSD

```
        /\
       /  \
      / UI \
     /------\
    /Integration\
   /--------------\
  /   Jail Tests   \
 /------------------\
/     VM Tests       \
/----------------------\
```

**Execution Order:**
1. **Unit tests** (host, fastest) — run first on every commit.
2. **Jail integration tests** (seconds) — run on every PR.
3. **VM kernel tests** (minutes) — run before merge to `main`, nightly, or on kernel-touching PRs.

### 5.2 When to Use bhyve VMs

| Scenario | Justification |
|----------|---------------|
| Kernel module loading | Host isolation mandatory |
| Kernel panic / crash testing | VM can be destroyed without host impact |
| Network stack modifications | Full kernel network path exercised |
| Driver development | Hardware abstraction in VM is safe |
| sysctl / kernel tunable changes | Requires real kernel context |
| Performance benchmarking | Dedicated vCPUs avoid host noise |

### 5.3 When to Use Jails

| Scenario | Justification |
|----------|---------------|
| Userland daemon testing | Fast startup, low overhead |
| Network service isolation | Jail IP stack is sufficient |
| Configuration validation | No kernel involvement needed |
| Rapid iteration | Start/stop in milliseconds |
| Multi-tenant test parallelization | Low resource consumption |

### 5.4 Test Harness Requirements

All test harnesses must produce output in one of these AI-agent-parseable formats:

| Format | Extension | Use Case |
|--------|-----------|----------|
| TAP | `.tap` | Simple pass/fail test suites |
| JUnit XML | `.xml` | CI integration, test metadata |
| JSON | `.json` | Custom metrics, structured logs |
| Subunit | `.subunit` | Streaming test results |

Example JSON output for AI agent consumption:

```json
{
  "harness": "cloudbsd-jail-test",
  "version": "1.0.0",
  "environment": {
    "type": "jail",
    "freebsd_version": "14.2-RELEASE",
    "cloudbsd_packages": ["git", "cmake", "python3"]
  },
  "results": [
    {
      "test_name": "test_pppoe_discovery_packet",
      "status": "PASS",
      "duration_ms": 45,
      "log": "PADI sent, PADO received, session established"
    },
    {
      "test_name": "test_pppoe_multithreaded_throughput",
      "status": "FAIL",
      "duration_ms": 12030,
      "log": "Expected 10000 pps, achieved 8473 pps",
      "artifact_paths": ["/var/tmp/cloudbsd-test-output/uuid/perf-graph.png"]
    }
  ],
  "summary": {
    "total": 2,
    "passed": 1,
    "failed": 1,
    "skipped": 0
  }
}
```

---

## 6. Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| VM boot timeout | Medium | Test flakiness | Health-check polling instead of fixed `sleep`; retry with SSH |
| ZFS snapshot corruption | Low | All tests fail | Maintain multiple golden snapshots; verify with `zfs scrub` |
| Host kernel panic from VMM bug | Low | CI host down | Run VM tests on dedicated CI runners, not shared dev hosts |
| Jail escape | Low | Host compromise | Disable `allow.mount`, `allow.raw_sockets` unless required; run as unprivileged user |
| Output collection failure | Medium | AI agent cannot diagnose | Multiple redundant collection methods (SSH, serial, file copy) |
| Resource exhaustion (VMs too many) | Medium | CI gridlock | Implement VM quota per-pipeline; queue with timeout |
| Inconsistent FreeBSD versions | Medium | "Works on my machine" | Pin exact release version in golden snapshot; version in test output |

---

## 7. Future Enhancements

1. **QEMU fallback:** Support QEMU on non-FreeBSD CI hosts (Linux runners) for cross-platform CI.
2. **Live migration:** Migrate running test VMs between CI runners for load balancing.
3. **Snapshot fuzzing:** Automatically generate ZFS snapshot variants with corrupted state for resilience testing.
4. **GPU passthrough:** Support VMM GPU passthrough for testing graphics drivers.
5. **Distributed jail testing:** Orchestrate jail tests across multiple physical hosts.
6. **eBPF tracing:** Collect kernel eBPF traces from VMs for performance analysis.

---

## 8. Conclusion

The combination of bhyve VMs and FreeBSD jails provides a complete testing spectrum for CloudBSD applications:

- **Jails** offer speed and efficiency for userland testing.
- **bhyve VMs** offer safety and fidelity for kernel testing.
- **Unified orchestration** ensures AI agents and CI pipelines receive consistent, structured output regardless of the underlying isolation mechanism.

All test environments must be defined as code, start from known-clean snapshots, and produce AI-parseable output. This ensures that every test run is reproducible, observable, and actionable.

---

## 9. Actionable Tasks — Step-by-Step Implementation Tracker

This section is the master checklist for implementing the CloudBSD testing infrastructure. Each task includes:
- **Status:** `NOT STARTED` | `IN PROGRESS` | `COMPLETED`
- **Owner:** Who is working on it
- **Start Date:** When work began
- **End Date:** When work finished
- **Dependencies:** What must be done first
- **Files Modified:** What files are touched
- **Notes:** Any blockers, decisions, or context

### Phase 0: Foundation and Setup

| # | Task | Status | Owner | Start | End | Dependencies | Files | Notes |
|---|------|--------|-------|-------|-----|--------------|-------|-------|
| 0.1 | Create `Testing Infrastructure/` directory and `TESTING_INFRASTRUCTURE.md` | COMPLETED | | 2026-04-23 | 2026-04-23 | | `Testing Infrastructure/TESTING_INFRASTRUCTURE.md` | This document |
| 0.2 | Update `README.md` with Testing Infrastructure link | NOT STARTED | | | | 0.1 | `README.md` | Add to Documentation Index |
| 0.3 | Update `INIT_PROMPT.md` with Testing Infrastructure reference | NOT STARTED | | | | 0.1 | `INIT_PROMPT.md` | Add to Repository File Tree and Decision Matrix |
| 0.4 | Verify `test_md.sh` passes with new file | NOT STARTED | | | | 0.1 | `test_md.sh` | Ensure header check includes new file |
| 0.5 | Set up CI runner with VMM support (FreeBSD host) | NOT STARTED | | | | | | Dedicated bare-metal or nested virtualization enabled |
| 0.6 | Verify ZFS pool exists for VM and jail storage | NOT STARTED | | | | 0.5 | | `zroot/vm` and `zroot/jail` datasets |

### Phase 1: bhyve VM Testing Framework

| # | Task | Status | Owner | Start | End | Dependencies | Files | Notes |
|---|------|--------|-------|-------|-----|--------------|-------|-------|
| 1.1 | Create base FreeBSD VM image with CloudBSD deps | NOT STARTED | | | | 0.5 | `zroot/vm/base` | Pre-install git, cmake, python3, pytest |
| 1.2 | Create ZFS golden snapshot for VM base | NOT STARTED | | | | 1.1 | `zroot/vm/base@golden` | Instant clone source |
| 1.3 | Implement `vm-test-runner.sh` lifecycle script | NOT STARTED | | | | 1.2 | `/usr/local/libexec/cloudbsd/vm-test-runner.sh` | Create, start, run tests, collect output, destroy |
| 1.4 | Implement console log capture (`-l com1,stdio`) | NOT STARTED | | | | 1.3 | `vm-test-runner.sh` | Redirect to structured output directory |
| 1.5 | Implement kernel message collection (`dmesg`) | NOT STARTED | | | | 1.3 | `vm-test-runner.sh` | After test run, before VM destroy |
| 1.6 | Implement crash dump collection from VM image | NOT STARTED | | | | 1.3 | `vm-test-runner.sh` | Copy `/var/crash/vmcore.*` if present |
| 1.7 | Implement network capture on host tap interface | NOT STARTED | | | | 1.3 | `vm-test-runner.sh` | Optional `tcpdump` for protocol tests |
| 1.8 | Write VM-based integration test for kernel module loading | NOT STARTED | | | | 1.3 | `tests/kernel/test_module_load_vm.sh` | Verify `kldload` inside VM, check `dmesg` |
| 1.9 | Write VM-based panic recovery test | NOT STARTED | | | | 1.3 | `tests/kernel/test_panic_recovery_vm.sh` | Inject fault, verify host unaffected |
| 1.10 | Document VM test runner usage in `TESTING_INFRASTRUCTURE.md` | NOT STARTED | | | | 1.3 | `TESTING_INFRASTRUCTURE.md` | Update Section 4.1 |

### Phase 2: FreeBSD Jail Testing Framework

| # | Task | Status | Owner | Start | End | Dependencies | Files | Notes |
|---|------|--------|-------|-------|-----|--------------|-------|-------|
| 2.1 | Create base FreeBSD jail template with CloudBSD deps | NOT STARTED | | | | 0.5 | `zroot/jail/base` | Same package set as VM base |
| 2.2 | Create ZFS golden snapshot for jail base | NOT STARTED | | | | 2.1 | `zroot/jail/base@golden` | Instant clone source |
| 2.3 | Implement `jail-test-runner.sh` lifecycle script | NOT STARTED | | | | 2.2 | `/usr/local/libexec/cloudbsd/jail-test-runner.sh` | Create, start, run tests, collect output, destroy |
| 2.4 | Implement jail output collection (`/tmp/test-output.json`) | NOT STARTED | | | | 2.3 | `jail-test-runner.sh` | Copy before jail destruction |
| 2.5 | Implement jail service log collection (`/var/log`) | NOT STARTED | | | | 2.3 | `jail-test-runner.sh` | Application behavior verification |
| 2.6 | Implement jail network isolation verification | NOT STARTED | | | | 2.3 | `jail-test-runner.sh` | `tcpdump` on host `lo` interface |
| 2.7 | Implement jail process tree capture before destruction | NOT STARTED | | | | 2.3 | `jail-test-runner.sh` | Resource leak detection |
| 2.8 | Write jail-based integration test for userland daemon | NOT STARTED | | | | 2.3 | `tests/userland/test_daemon_jail.sh` | Start daemon, verify ports, stop daemon |
| 2.9 | Write jail-based configuration validation test | NOT STARTED | | | | 2.3 | `tests/userland/test_config_jail.sh` | Verify rc.d scripts, sysctls |
| 2.10 | Document jail test runner usage in `TESTING_INFRASTRUCTURE.md` | NOT STARTED | | | | 2.3 | `TESTING_INFRASTRUCTURE.md` | Update Section 4.2 |

### Phase 3: Unified Orchestration and CI Integration

| # | Task | Status | Owner | Start | End | Dependencies | Files | Notes |
|---|------|--------|-------|-------|-----|--------------|-------|-------|
| 3.1 | Design unified JSON output schema for VM and jail tests | NOT STARTED | | | | 1.3, 2.3 | `docs/test-output-schema.json` | Version 1.0.0 |
| 3.2 | Implement `cloudbsd-test-orchestrator` wrapper script | NOT STARTED | | | | 3.1 | `/usr/local/bin/cloudbsd-test-orchestrator` | Dispatches to VM or jail runner based on test type |
| 3.3 | Implement test result aggregation (multiple environments) | NOT STARTED | | | | 3.2 | `cloudbsd-test-orchestrator` | Merge JSON outputs from VM + jail runs |
| 3.4 | Create GitHub Actions workflow for jail tests | NOT STARTED | | | | 2.3, 3.2 | `.github/workflows/jail-tests.yml` | Run on every PR |
| 3.5 | Create GitHub Actions workflow for VM tests | NOT STARTED | | | | 1.3, 3.2 | `.github/workflows/vm-tests.yml` | Run before merge, nightly |
| 3.6 | Create Jenkins pipeline for jail tests | NOT STARTED | | | | 2.3, 3.2 | `Jenkinsfile.jail` | For on-premise CI |
| 3.7 | Create Jenkins pipeline for VM tests | NOT STARTED | | | | 1.3, 3.2 | `Jenkinsfile.vm` | For on-premise CI |
| 3.8 | Implement artifact upload (console logs, crash dumps, captures) | NOT STARTED | | | | 3.3 | CI configs | Store in GitHub Actions artifacts or Jenkins archive |
| 3.9 | Implement AI-agent notification hook (structured result POST) | NOT STARTED | | | | 3.3 | `cloudbsd-test-orchestrator` | POST JSON to agent endpoint on completion |
| 3.10 | Document CI integration in `TESTING_INFRASTRUCTURE.md` | NOT STARTED | | | | 3.4, 3.5 | `TESTING_INFRASTRUCTURE.md` | Update Section 5 |

### Phase 4: AI Agent Output Format and Observability

| # | Task | Status | Owner | Start | End | Dependencies | Files | Notes |
|---|------|--------|-------|-------|-----|--------------|-------|-------|
| 4.1 | Define JSON schema for AI-agent-parseable test results | NOT STARTED | | | | 3.1 | `docs/ai-test-result-schema.json` | Include test name, status, duration, log, artifact paths |
| 4.2 | Implement TAP-to-JSON converter | NOT STARTED | | | | 4.1 | `/usr/local/libexec/cloudbsd/tap-to-json.py` | For legacy test suites |
| 4.3 | Implement JUnit XML-to-JSON converter | NOT STARTED | | | | 4.1 | `/usr/local/libexec/cloudbsd/junit-to-json.py` | For Java/C++ test suites |
| 4.4 | Implement structured log parser for kernel messages | NOT STARTED | | | | 4.1 | `/usr/local/libexec/cloudbsd/dmesg-parser.py` | Extract module load, panic, driver probe lines |
| 4.5 | Implement crash dump summary generator | NOT STARTED | | | | 4.1 | `/usr/local/libexec/cloudbsd/crash-summarize.sh` | Run `kgdb` commands, produce text summary |
| 4.6 | Implement network capture summary generator | NOT STARTED | | | | 4.1 | `/usr/local/libexec/cloudbsd/pcap-summarize.py` | Extract connection stats, errors, retransmits |
| 4.7 | Integrate all parsers into `cloudbsd-test-orchestrator` | NOT STARTED | | | | 4.2-4.6 | `cloudbsd-test-orchestrator` | Unified output regardless of test type |
| 4.8 | Write AI agent decision tree documentation | NOT STARTED | | | | 4.7 | `TESTING_INFRASTRUCTURE.md` | How agents interpret results, when to retry, when to escalate |
| 4.9 | Implement test failure classification (flaky vs. real) | NOT STARTED | | | | 4.7 | `cloudbsd-test-orchestrator` | Compare against historical runs |
| 4.10 | Implement automatic retry with exponential backoff for flaky tests | NOT STARTED | | | | 4.9 | `cloudbsd-test-orchestrator` | Max 3 retries, mark as `FLAKY` if passes on retry |

### Phase 5: Security and Hardening

| # | Task | Status | Owner | Start | End | Dependencies | Files | Notes |
|---|------|--------|-------|-------|-----|--------------|-------|-------|
| 5.1 | Audit jail capabilities (`allow.*` sysctls) | NOT STARTED | | | | 2.1 | `jail-test-runner.sh` | Disable unnecessary privileges |
| 5.2 | Implement jail resource limits (CPU, memory, disk) | NOT STARTED | | | | 2.1 | `jail-test-runner.sh` | `rctl` or `jail` limits |
| 5.3 | Implement VM resource limits (vCPUs, memory caps) | NOT STARTED | | | | 1.1 | `vm-test-runner.sh` | `-c` and `-m` flags enforced |
| 5.4 | Implement network isolation between concurrent test environments | NOT STARTED | | | | 1.3, 2.3 | `cloudbsd-test-orchestrator` | Unique tap interfaces, unique jail IPs |
| 5.5 | Implement secrets scrubbing from all test output | NOT STARTED | | | | 3.3 | `cloudbsd-test-orchestrator` | Regex-based scrubbing before artifact upload |
| 5.6 | Implement test environment access logging | NOT STARTED | | | | 3.3 | `cloudbsd-test-orchestrator` | Who created what, when, for audit |
| 5.7 | Write security hardening guide for test operators | NOT STARTED | | | | 5.1-5.6 | `TESTING_INFRASTRUCTURE.md` | Update Section 6 with hardening details |
| 5.8 | Conduct penetration test of jail escape vectors | NOT STARTED | | | | 5.1 | | Third-party assessment |
| 5.9 | Conduct penetration test of VM escape vectors | NOT STARTED | | | | 1.3 | | Third-party assessment |
| 5.10 | Document security findings and mitigations | NOT STARTED | | | | 5.8, 5.9 | `SECURITY.md` | New file if significant findings |

### Phase 6: Documentation and Training

| # | Task | Status | Owner | Start | End | Dependencies | Files | Notes |
|---|------|--------|-------|-------|-----|--------------|-------|-------|
| 6.1 | Write operator runbook for VM test creation | NOT STARTED | | | | 1.10 | `docs/runbook-vm-testing.md` | Step-by-step for human operators |
| 6.2 | Write operator runbook for jail test creation | NOT STARTED | | | | 2.10 | `docs/runbook-jail-testing.md` | Step-by-step for human operators |
| 6.3 | Write AI agent integration guide | NOT STARTED | | | | 4.8 | `docs/ai-agent-integration.md` | How to consume test output, make decisions |
| 6.4 | Create example GitHub Actions workflow | NOT STARTED | | | | 3.4 | `.github/workflows/example-cloudbsd-test.yml` | Copy-paste template for projects |
| 6.5 | Create example Jenkins pipeline | NOT STARTED | | | | 3.6 | `examples/Jenkinsfile.cloudbsd` | Copy-paste template for projects |
| 6.6 | Record video walkthrough of VM test lifecycle | NOT STARTED | | | | 1.10 | | For onboarding new developers |
| 6.7 | Record video walkthrough of jail test lifecycle | NOT STARTED | | | | 2.10 | | For onboarding new developers |
| 6.8 | Present testing infrastructure to CloudBSD team | NOT STARTED | | | | 6.1-6.3 | | Internal knowledge transfer |
| 6.9 | Gather feedback and iterate on documentation | NOT STARTED | | | | 6.8 | `TESTING_INFRASTRUCTURE.md` | Continuous improvement |
| 6.10 | Final review and sign-off | NOT STARTED | | | | 6.9 | | All stakeholders approve |
