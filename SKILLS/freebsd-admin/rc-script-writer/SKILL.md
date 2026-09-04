---
name: rc-script-writer
description: >-
  Write FreeBSD rc.d startup scripts that follow the conventions -
  PROVIDE/REQUIRE/KEYWORD, rcvar, pidfiles, and a reload that honours the
  SIGHUP contract. Use whenever a CloudBSD service needs to start at boot or
  be controlled with service(8).
---

# Skill: rc-script-writer

**Purpose:** Write FreeBSD rc.d startup scripts for services, following FreeBSD conventions for service management.

**Triggers:** When creating a new FreeBSD service, porting a service to FreeBSD, or documenting service startup configuration.

## Loading Instructions

Load this skill when the user asks you to:
- Create an rc.d script for a service
- Port a service to FreeBSD
- Configure service startup
- Debug rc.d scripts
- Document rc.d conventions

---

## 1. RC Script Overview

### 1.1 What is an RC Script?

```markdown
## FreeBSD RC Scripts

| Aspect | Description |
|--------|-------------|
| Location | /etc/rc.d/ for system, /usr/local/etc/rc.d/ for ports |
| Purpose | Start/stop/restart services at boot/shutdown |
| Framework | /etc/rc.subr library functions |
| Compatibility | System V init scripts are different |

## RC Script vs Systemd

| Feature | RC Script | systemd |
|---------|-----------|---------|
| Syntax | Shell script | Unit files |
| Location | /etc/rc.d/ | /etc/systemd/system/ |
| Commands | service(8) | systemctl |
| Dependencies | # REQUIRE, # BEFORE | Wants=, Requires= |
| Boot order | Defined by rcorder | Automatically resolved |
```

### 1.2 Basic RC Script Template

```bash
#!/bin/sh
#
# PROVIDE: myservice
# REQUIRE: NETWORKING
# KEYWORD: shutdown
#
# Add to /etc/rc.conf.local:
# myservice_enable="YES"
# myservice_flags="--default flags"

. /etc/rc.subr

name="myservice"
rcvar=myservice_enable
command="/usr/local/bin/myservice"
command_args="--config /usr/local/etc/myservice.conf"

load_rc_config $name
run_rc_command "$1"
```

---

## 2. RC Script Components

### 2.1 Required Headers

```bash
#!/bin/sh
#
# PROVIDE: servicename           # Name that other scripts can depend on
# REQUIRE: NETWORKING syslogd   # What must run before this
# KEYWORD: shutdown             # Run during shutdown
#                                (or: nojail nostart)
#
# Add to /etc/rc.conf.local:
# servicename_enable="YES"
```

### 2.2 Header Keywords

```markdown
## PROVIDE
Names this service. Other scripts can depend on this name.

## REQUIRE
Dependencies that must start before this service.

| Common Values | Description |
|---------------|-------------|
| NETWORKING | Network must be up |
| syslogd | System logger must be running |
| mysql | MySQL must be running |
| postgresql | PostgreSQL must be running |
| DAEMON | Generic daemon (used with respawn) |
| shutdown | Clean shutdown (runs at shutdown) |

## KEYWORD
When this script should run.

| Value | Description |
|-------|-------------|
| shutdown | Run at shutdown |
| nojail | Don't run in jail environment |
| nostart | Don't run at startup (manual only) |
| barefoot | Don't run until explicitly started |
```

### 2.3 RC Subroutines

```bash
# Include rc.subr (REQUIRED)
. /etc/rc.subr

# Load configuration
load_rc_config "$name"

# Define command
name="myservice"
rcvar="${name}_enable"
command="/usr/local/bin/${name}"
command_args="--config /usr/local/etc/${name}.conf"
pidfile="/var/run/${name}.pid"

# Run standard rc commands
run_rc_command "$1"
```

---

## 3. RC Script Examples

### 3.1 Simple Daemon

```bash
#!/bin/sh
#
# PROVIDE: mydaemon
# REQUIRE: NETWORKING
# KEYWORD: shutdown

. /etc/rc.subr

name="mydaemon"
rcvar="${name}_enable"
command="/usr/local/bin/${name}"
pidfile="/var/run/${name}.pid"
command_args="--pidfile ${pidfile}"

load_rc_config $name
run_rc_command "$1"
```

### 3.2 With Extra Flags

```bash
#!/bin/sh
#
# PROVIDE: webapp
# REQUIRE: NETWORKING postgresql
# KEYWORD: shutdown

. /etc/rc.subr

name="webapp"
rcvar="${name}_enable"
command="/usr/local/bin/${name}"
command_args="--config /usr/local/etc/webapp.conf ${webapp_flags}"
pidfile="/var/run/${name}.pid"
required_files="/usr/local/etc/webapp.conf"

# Check config exists before starting
start_precmd="check_config"

check_config() {
    if [ ! -f /usr/local/etc/webapp.conf ]; then
        warn "/usr/local/etc/webapp.conf not found"
        return 1
    fi
}

load_rc_config $name
run_rc_command "$1"
```

### 3.3 With Environment Variables

```bash
#!/bin/sh
#
# PROVIDE: app
# REQUIRE: NETWORKING
# KEYWORD: shutdown

. /etc/rc.subr

name="app"
rcvar="${name}_enable"
command="/usr/local/bin/${name}"
command="/usr/local/bin/${name}"

# Set environment
export HOME="/var/db/app"
export LOGFILE="/var/log/app.log"

# Clear environment before starting
export HOME LOGFILE

command_args="--daemon --pidfile /var/run/app.pid"
pidfile="/var/run/app.pid"

load_rc_config $name
run_rc_command "$1"
```

### 3.4 Respawning Service

```bash
#!/bin/sh
#
# PROVIDE: watchdog
# REQUIRE: NETWORKING
# KEYWORD: shutdown

. /etc/rc.subr

name="watchdog"
rcvar="${name}_enable"
command="/usr/local/bin/watchdog"
command_args="--daemon"
pidfile="/var/run/watchdog.pid"

# Enable respawn
procname="/usr/local/bin/watchdog"

# Respawn if crashes within 60 seconds
force_respawn="YES"

load_rc_config $name
run_rc_command "$1"
```

---

## 4. RC Subroutines Reference

### 4.1 run_rc_command Options

Long-running services must expose `reload` (nginx-style). Validate the new
config first, then send `SIGHUP`. A failed check must not kill the running
daemon: reload is a no-op failure, not a crash or restart.

```bash
run_rc_command "$1"

# Supports: start, stop, restart, status, poll, etc.

# Custom commands. reload is required for long-running services:
# --check-config, then SIGHUP. A failed check must not kill the daemon.
extra_commands="reload configtest"
reload_cmd="do_reload"
configtest_cmd="do_configtest"

do_configtest() {
    echo "Testing ${name} configuration..."
    ${command} --check-config
}

do_reload() {
    if ! do_configtest; then
        warn "${name}: config check failed; keeping old config (not sending SIGHUP)"
        return 1
    fi
    echo "Reloading ${name}..."
    kill -HUP $(cat $pidfile)
}
```

### 4.2 Common RC Functions

```bash
# Debug output
debug "message"           # Only if rcdebug is set

# Warning output
warn "message"           # Always shown

# Informational output
info "message"           # When not quiet

# Check for required files
check_required_files      # Exits if files missing

# Force kill process
force_stop               # Sends SIGKILL if SIGTERM fails

# Wait for pidfile
wait_for_pids 123        # Wait for PIDs

# Check if running
is_running               # Returns 0 if running
```

### 4.3 RC Variables

```bash
# Built-in variables
rc_pidfile               # Set by pidfile= in script
rcvar                    # Set by rcvar= in script
rc_fast=$(rc_flags)      # -f flag passed
rc_flags                 # Additional flags from rc.conf
rc_force               # -f force flag passed

# Common rc.conf variables
${name}_enable          # Enable service (YES/NO)
${name}_flags           # Additional flags
${name}_pidfile         # Override pidfile location
```

---

## 5. Enabling the Service

### 5.1 Installation

```bash
# Install rc script
sudo cp myservice.sh /etc/rc.d/myservice
sudo chmod 555 /etc/rc.d/myservice

# For ports-installed software
sudo cp myservice.sh /usr/local/etc/rc.d/myservice
sudo chmod 555 /usr/local/etc/rc.d/myservice
```

### 5.2 Configuration

```bash
# /etc/rc.conf.local (not rc.conf - use .local)
# Add these lines:

# Enable service
myservice_enable="YES"

# Additional flags
myservice_flags="--verbose"

# Custom pidfile
myservice_pidfile="/var/run/myservice.pid"
```

### 5.3 Managing the Service

```bash
# Start
sudo service myservice start

# Stop
sudo service myservice stop

# Restart
sudo service myservice restart

# Status
sudo service myservice status

# Reload (validate with --check-config, then SIGHUP; failed check leaves the daemon running)
sudo service myservice reload

# Force start (even if not enabled)
sudo service -f myservice start
```

---

## 6. Service Configuration Template

### 6.1 RC Script Template

```markdown
## RC Script: myservice

```bash
#!/bin/sh
#
# PROVIDE: myservice
# REQUIRE: NETWORKING
# KEYWORD: shutdown

. /etc/rc.subr

name="myservice"
rcvar="${name}_enable"
command="/usr/local/bin/${name}"
pidfile="/var/run/${name}.pid"
command_args="--config /usr/local/etc/${name}.conf ${myservice_flags}"

# Required config file
required_files="/usr/local/etc/${name}.conf"

# Custom pre-start check
start_precmd="check_config"

# nginx-style reload: validate, then SIGHUP. Failed check must not kill the daemon.
extra_commands="reload configtest"
reload_cmd="do_reload"
configtest_cmd="do_configtest"

check_config() {
    if [ ! -e /usr/local/etc/${name}.conf ]; then
        warn "${name} config not found at /usr/local/etc/${name}.conf"
        return 1
    fi
}

do_configtest() {
    ${command} --check-config
}

do_reload() {
    if ! do_configtest; then
        warn "${name}: config check failed; keeping old config (not sending SIGHUP)"
        return 1
    fi
    kill -HUP $(cat ${pidfile})
}

load_rc_config $name
run_rc_command "$1"
```

### 6.2 Configuration File

```bash
# /etc/rc.conf.local

# Enable myservice
myservice_enable="YES"

# Additional flags
myservice_flags="--verbose --daemon"

# PID file location
myservice_pidfile="/var/run/myservice/myservice.pid"
```

### 6.3 Service Documentation

```markdown
## Service: myservice

### Files
| File | Purpose |
|------|---------|
| /etc/rc.d/myservice | RC script |
| /usr/local/etc/myservice.conf | Configuration |
| /var/run/myservice.pid | PID file |
| /var/log/myservice.log | Log file |

### Configuration
| Variable | Default | Description |
|----------|---------|-------------|
| myservice_enable | NO | Enable service |
| myservice_flags | "" | Additional flags |
| myservice_pidfile | /var/run/myservice.pid | PID file location |

### Dependencies
| Service | Required |
|---------|----------|
| NETWORKING | Yes |

### Commands
| Command | Description |
|---------|-------------|
| start | Start service |
| stop | Stop service |
| restart | Restart service |
| status | Check if running |
| reload | Validate with `--check-config`, then send SIGHUP; failed check must not kill the daemon |
```

---

## 7. Debugging RC Scripts

### 7.1 Debug Mode

```bash
# Run with debug output
rcdebug=1 service myservice start

# Or in rc.conf
rcdebug="YES"
```

### 7.2 Common Issues

```bash
# Script not executable
chmod +x /etc/rc.d/myservice

# Wrong shell
# Use #!/bin/sh not #!/bin/bash

# Missing variables in rc.conf
# Check /etc/rc.conf.local exists

# Debug script execution
sh -x /etc/rc.d/myservice start
```

### 7.3 Testing

```bash
# Dry run
service -n myservice start  # Don't actually start

# Check syntax
sh -n /etc/rc.d/myservice

# Check required files
service myservice forcestart  # Start even if not enabled
```

---

## Validation Checklist

Before deploying rc script:

- [ ] Script is executable (chmod 555)
- [ ] PROVIDE/REQUIRE headers correct
- [ ] rcvar set to ${name}_enable
- [ ] command path is absolute
- [ ] pidfile path exists or can be created
- [ ] Configuration in /etc/rc.conf.local
- [ ] Service starts with `service name start`
- [ ] Service stops with `service name stop`
- [ ] Status shows correct state
- [ ] extra_commands includes reload; do_reload runs `--check-config` then SIGHUP
- [ ] A failed config check does not kill or restart the running daemon

## Reference

See service-manager for service management commands.