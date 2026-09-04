---
name: linuxulator-runner
description: >-
  Run Linux binaries on FreeBSD through the Linuxulator compatibility layer.
  Use when a required tool ships only as a Linux binary, when validating that
  /compat/linux is set up correctly, or when deciding whether to run something
  natively instead.
keywords:
  - Linuxulator
  - Linux binary
  - /compat/linux
  - linux compat
---

# Skill: linux-binary-runner

**Purpose:** Run Linux binaries on FreeBSD using the Linux compatibility layer (Linuxulator), validate the execution environment, and execute commands in a purely FreeBSD context when needed.

**Triggers:** When running Linux binaries on FreeBSD, debugging compatibility issues, or verifying the execution environment.

---

## 1. Linuxulator Overview

### 1.1 What is the Linuxulator?

```markdown
## FreeBSD Linux Compatibility Layer (Linuxulator)

| Aspect | Description |
|--------|-------------|
| Name | Linuxulator |
| Purpose | Run Linux binaries natively on FreeBSD |
| Kernel | Modified FreeBSD kernel |
| Uname | Still shows "FreeBSD" but environment can be Linux |
| Userspace | Linux-style /compat/linux |

## Linuxulator vs Native FreeBSD

| Feature | Linuxulator | Native FreeBSD |
|---------|-------------|----------------|
| Binary compatibility | Linux ELF | FreeBSD ELF |
| `/usr/bin/uname` | Shows FreeBSD | Shows FreeBSD |
| Environment vars | Can be mixed | Pure FreeBSD |
| `/etc/os-release` | Rocky/Alma style | FreeBSD style |
| `sysctl` | Linux kernel version | FreeBSD version |

## The Problem

When a Linux binary runs via Linuxulator:
- `uname -a` still shows "FreeBSD" because it's the host kernel
- But the Linux binary sees `/etc/os-release` as Rocky Linux
- Environment variables can be mixed
- Some binaries check `/etc/os-release` not `uname`

## The Solution

Use `su -m` or `sudo -u` to execute commands with a purely FreeBSD environment,
stripping Linux compatibility layer environment variables.
```

### 1.2 Linuxulator Architecture

```
┌─────────────────────────────────────────────────┐
│              FreeBSD Host System                  │
│                                                  │
│  ┌────────────────────────────────────────────┐ │
│  │           Linuxulator Layer                 │ │
│  │                                              │ │
│  │   /compat/linux (Linux userspace emulation)        │ │
│  │   /etc/os-release (Rocky Linux)             │ │
│  │   /lib, /usr/lib (Linux libraries)          │ │
│  │                                              │ │
│  │   sysctl compat.linux.osrelease             │ │
│  │   (Reports Linux kernel version to binaries)│ │
│  └────────────────────────────────────────────┘ │
│                        │                        │
│         Linux binary ──┼──> executes here        │
│         uname -a ──────┼──> shows FreeBSD        │
│         /etc/os-release ──> shows Rocky         │
└─────────────────────────────────────────────────┘
```

---

## 2. Checking Linuxulator Status

### 2.1 System Checks

```bash
# Check if Linuxulator is loaded
kldstat | grep linux

# Or via sysctl
sysctl compat.linux.osrelease

# Enable Linuxulator if not loaded
sudo kldload linux
sudo kldload linux64

# Make it persistent across reboots
echo 'kld_list="linux linux64"' | sudo tee -a /etc/rc.conf

# Check FreeBSD version
freebsd-version

# Check kernel
uname -r
```

### 2.2 Environment Validation

```bash
# What Linux binaries see
cat /compat/linux/etc/os-release

# Check sysctl for Linux kernel version reported to binaries
sysctl compat.linux.osrelease

# Environment variables a Linux binary sees
env | grep -i linux
```

---

## 3. Detecting Mixed Environment Issues

### 3.1 The Detection Problem

```bash
# This looks FreeBSD:
uname -a
# FreeBSD hostname 14.0-RELEASE FreeBSD 14.0-RELEASE ...

# But a Linux binary might see:
cat /etc/os-release
# NAME=Rocky Linux
# VERSION="9.4 (Blue Split)"
# ID=rocky
# ID_LIKE="rhel centos fedora"

# Some binaries check os-release, not uname!
# This causes issues when:
# - Binary expects specific Linux distro features
# - Installation scripts check distro version
# - Package managers assume specific paths
```

### 3.2 Environment Variables to Watch

```bash
# Linux compatibility layer sets these:
# (can interfere with FreeBSD-native commands)

AUDITWARE_LINUX_BACKTRACE=1
LINUX_LD_LIBRARY_PATH=/usr/lib:/lib
LINUX_PATH=/compat/linux/usr/bin

# These can cause mixed behavior:
# - Some Linux binaries ignore uname and use os-release
# - Some use both and get confused
# - Scripts might source /etc/os-release and behave Linux-like
```

---

## 4. Pure FreeBSD Execution

### 4.1 Using `su -m` (Minimal Environment)

```bash
# su -m preserves the current user's environment but does NOT
# set up Linux compatibility environment variables

# Execute a command purely in FreeBSD context
su -m $USER -c 'uname -a'

# Compare:
su -m $USER -c 'cat /etc/os-release'
# (should show FreeBSD-style or no file)

# Verify with a command that checks both
su -m $USER -c 'env | grep -i rocky'
# (should return nothing in pure FreeBSD context)
```

### 4.2 Using `sudo -u` (Specific User)

```bash
# Run as another user with clean environment
sudo -u username env -i PATH=/usr/bin:/bin uname -a

# With additional PATH entries
sudo -u username env -i PATH=/usr/local/bin:/usr/bin:/bin HOME=/home/username uname -a

# Clean environment example
sudo -u username env -i /usr/bin/env
# Shows minimal environment without Linux layer vars
```

### 4.3 Mixed Execution Pattern

```bash
# Pattern: Use su/sudo to escape Linuxulator environment
# For commands that MUST run in pure FreeBSD

# WRONG: Linux binary sees Rocky Linux via os-release
/usr/local/bin/some-linux-binary --version

# RIGHT: Execute in pure FreeBSD context
su -m $USER -c '/usr/local/bin/some-linux-binary --version'

# OR: Unset Linux environment variables first
unset LINUX_LD_LIBRARY_PATH
unset LINUX_PATH
/usr/local/bin/some-linux-binary --version
```

---

## 5. Validation Commands

### 5.1 Validate Pure FreeBSD Environment

```bash
# These commands should ALWAYS show FreeBSD, never Linux

# Check 1: uname should show FreeBSD
uname -s  # Expected: FreeBSD

# Check 2: /etc/os-release should NOT exist or be FreeBSD
[ -f /etc/os-release ] && cat /etc/os-release || echo "No os-release (pure FreeBSD)"

# Check 3: sysctl should show FreeBSD kernel
sysctl kern.osrelease | grep -v Linux

# Check 4: Check for Linux-specific paths
ls -la /compat/linux 2>/dev/null && echo "Linux compat present" || echo "No Linux compat"

# Check 5: Verify no Linux environment pollution
env | grep -E '(ROCKY|REDHAT|CENTOS|UBUNTU|DEBIAN)' || echo "No Linux distro env vars"
```

### 5.2 Validation Script

```bash
#!/bin/sh
# validate-freebsd-env.sh - Validate pure FreeBSD execution context

echo "=== FreeBSD Environment Validation ==="

echo "1. Kernel: $(uname -s) $(uname -r)"
[ "$(uname -s)" = "FreeBSD" ] && echo "   [PASS]" || echo "   [FAIL]"

echo "2. OS release file:"
if [ -f /etc/os-release ]; then
    grep -q "FreeBSD" /etc/os-release && echo "   [PASS] FreeBSD detected" || echo "   [FAIL] Linux distro detected"
else
    echo "   [PASS] No os-release (pure FreeBSD)"
fi

echo "3. Linux compatibility layer:"
sysctl -n compat.linux.osrelease 2>/dev/null && echo "   [INFO] Linuxulator active" || echo "   [INFO] No Linuxulator"

echo "4. Environment variables:"
env | grep -q "ROCKY\|REDHAT\|CENTOS" && echo "   [FAIL] Linux env vars present" || echo "   [PASS] No Linux env vars"

echo "=== Validation Complete ==="
```

### 5.3 Quick Validation One-Liners

```bash
# Fast check if running in pure FreeBSD
uname -s | grep -q FreeBSD && echo "Kernel: FreeBSD" || echo "Kernel: NOT FreeBSD"

# Check if Linux environment vars are set
env | grep -q LINUX_LD_LIBRARY_PATH && echo "Linux compat ACTIVE" || echo "Linux compat not active"

# Verify binary is FreeBSD ELF
file /bin/sh  # Should show "FreeBSD" not "Linux"
```

---

## 6. Practical Examples

### 6.1 Running Linux Binaries Correctly

```bash
# Problem: Linux binary expects Rocky Linux environment
/usr/local/bin/linux-binary --install

# Solution 1: Use su to get pure FreeBSD context
su -m $USER -c '/usr/local/bin/linux-binary --install'

# Solution 2: Clear Linux environment variables
env -i HOME=$HOME PATH=$PATH /usr/local/bin/linux-binary --install

# Solution 3: Use sudo with clean environment
sudo -u $USER env -i PATH=$PATH /usr/local/bin/linux-binary --install
```

### 6.2 Mixed Environment Debugging

```bash
# Debug: What does the Linux binary actually see?
# Use su -m to execute diagnostic in pure FreeBSD

su -m $USER -c '
echo "=== Inside su -m context ==="
uname -a
echo "---"
cat /etc/os-release 2>/dev/null || echo "No os-release"
echo "---"
env | head -20
'

# Compare with Linuxulator environment
echo "=== Inside Linuxulator context ==="
uname -a
echo "---"
cat /etc/os-release
echo "---"
env | head -20
```

### 6.3 Service Execution

```bash
# RC script: Ensure service runs in correct context

# /usr/local/etc/rc.d/linux-binary-service

#!/bin/sh
#
# PROVIDE: linux-binary-service
# REQUIRE: NETWORKING
# KEYWORD: shutdown

. /etc/rc.subr

name="linux-binary-service"
rcvar="${name}_enable"
command="/usr/local/bin/linux-binary"
command_args="--daemon"

# Run with pure FreeBSD environment
start_precmd="ensure_freebsd_env"

ensure_freebsd_env() {
    # Verify we're in FreeBSD context
    if [ "$(uname -s)" != "FreeBSD" ]; then
        warn "Not running on FreeBSD!"
        return 1
    fi
}

load_rc_config $name
run_rc_command "$1"
```

---

## 7. Security Considerations

### 7.1 Privilege Escalation with su/sudo

```bash
# Using su -m (preserves current user, minimal env)
# Safer than su - (which tries to be a login shell)

# Using sudo requires proper configuration
# /usr/local/etc/sudoers.d/linux-binary-runner
# username ALL=(ALL) NOPASSWD: /usr/local/bin/linux-binary

# Never run untrusted binaries with elevated privileges
```

### 7.2 Environment Sanitization

```bash
# Commands that strip ALL environment (safest)
env -i /bin/sh -c 'command'

# Commands that preserve PATH but nothing else
env -i PATH=/usr/bin:/bin /bin/sh -c 'command'

# Commands that preserve HOME and PATH
env -i HOME=$HOME PATH=$PATH /bin/sh -c 'command'
```

---

## 8. Task Template

### 8.1 Linux Binary Deployment Task

```markdown
## Task: Deploy Linux Binary on FreeBSD with Linuxulator

### Prerequisites
- [ ] Linuxulator loaded (`kldload linux linux64`)
- [ ] Linux binary compiled for x86_64-linux-gnu
- [ ] Required Linux libraries in /compat/linux

### Steps

```bash
# 1. Verify Linuxulator is active
kldstat | grep linux
sysctl compat.linux.osrelease

# 2. Test binary in Linux context first
/compat/linux/usr/bin/ldd /usr/local/bin/linux-binary
# Should show Linux libraries

# 3. Test in pure FreeBSD context
su -m $USER -c '/usr/local/bin/linux-binary --version'

# 4. Validate environment
./validate-freebsd-env.sh

# 5. If validation fails, debug with:
su -m $USER -c 'env | grep -E "LINUX|ROCKY|REDHAT"'

# 6. Create rc script with proper context
# (see section 6.3)
```

### Validation Checklist
- [ ] `uname -s` returns FreeBSD
- [ ] `/etc/os-release` absent or FreeBSD
- [ ] No Linux environment variables in execution context
- [ ] Binary executes correctly
- [ ] Service starts on boot (if applicable)

### Troubleshooting
| Issue | Solution |
|-------|----------|
| Binary segfaults | Check Linux libraries with `ldd` |
| Wrong behavior | Use `su -m` to escape Linux environment |
| Script detects Linux | Use `env -i` to clear environment |
| Path issues | Use absolute paths with `su -m -c 'command'` |
```

---

## 9. Reference Commands

```bash
# Linuxulator management
kldload linux          # Load Linuxulator
kldload linux64        # Load 64-bit Linux support
kldstat                # Check loaded kernel modules
sysctl compat.linux.osrelease  # Check Linux kernel version

# Environment inspection
uname -a               # Shows FreeBSD kernel
cat /etc/os-release    # Shows Linux distro (if Linuxulator active)
env | grep LINUX       # Check Linux env vars
file /bin/sh           # Check ELF type

# Pure FreeBSD execution
su -m $USER -c 'command'
sudo -u user env -i PATH=/usr/bin:/bin command
env -i PATH=/usr/bin:/bin command

# Validation
./validate-freebsd-env.sh
uname -s | grep -q FreeBSD
env | grep -q ROCKY && echo "Linux env" || echo "FreeBSD env"
```

---

## 10. Related Skills

- See jail-manager.md for running isolated environments
- See rc-script-writer.md for service startup scripts
- See zfs-manager.md for storage management