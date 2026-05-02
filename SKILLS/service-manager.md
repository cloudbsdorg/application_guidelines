# Skill: service-manager

**Purpose:** Manage FreeBSD services using rc.d, service command, and sysrc. Also covers Linux systemd services for Linuxulator binaries.

**Triggers:** When starting/stopping services, enabling services at boot, debugging service issues, or managing service configurations.

---

## 1. Service Management Overview

### 1.1 FreeBSD Service Management

```markdown
## FreeBSD Service Management

| Component | Purpose | Config Location |
|-----------|--------|-----------------|
| rc.d | System startup scripts | /etc/rc.d/ |
| service | Service control command | /usr/sbin/service |
| sysrc | Safe rc.conf editor | /usr/sbin/sysrc |
| rc.conf | System configuration | /etc/rc.conf |
| rc.conf.local | Local overrides | /etc/rc.conf.local |

## rc.d vs systemd

| Feature | rc.d | systemd |
|---------|------|---------|
| Script type | Shell script | Unit file |
| Control | service(8) | systemctl |
| Dependencies | # REQUIRE | Wants=, Requires= |
| Boot order | rcorder | Automatically resolved |
| Enable | rc.conf | systemctl enable |
```

### 1.2 Service Architecture

```
┌─────────────────────────────────────────────────┐
│              Host System                          │
│                                                  │
│  /etc/rc.conf ──────────────────────────────────>│
│      │                                           │
│      ├── /etc/rc.conf.local                      │
│      │                                           │
│      ▼                                           │
│  /etc/rc.d/ <─── service command ───> ┌─────────┐│
│      │                                │ Admin   ││
│  ┌───┴───┐                           └─────────┘│
│  │       │                                       │
│  ┌───┐ ┌───┐ ┌───┐                              │
│  │svc1│ │svc2│ │svc3│  (running services)        │
│  └───┘ └───┘ └───┘                              │
└─────────────────────────────────────────────────┘
```

---

## 2. Basic Service Operations

### 2.1 service Command

```bash
# Start a service
sudo service <service_name> start

# Stop a service
sudo service <service_name> stop

# Restart a service
sudo service <service_name> restart

# Check service status
sudo service <service_name> status

# Reload configuration (if supported)
sudo service <service_name> reload

# Run without enabling (one-shot)
sudo service -f <service_name> start

# Dry run (show what would be done)
sudo service -n <service_name> start

# Debug mode (rcdebug)
rcdebug=1 sudo service <service_name> start
```

### 2.2 Enable/Disable Services

```bash
# Enable service at boot (add to rc.conf)
sudo sysrc <service_name>_enable="YES"

# Disable service
sudo sysrc <service_name>_enable="NO"

# Check current setting
sudo sysrc <service_name>_enable

# List all enabled services
grep "_enable=\"YES\"" /etc/rc.conf*

# Show what services are enabled
service -e
```

### 2.3 Safe Configuration with sysrc

```bash
# Safe way to modify rc.conf
sudo sysrc <variable>=<value>

# Examples
sudo sysrc nginx_enable="YES"
sudo sysrc nginx_flags="--flags-here"
sudo sysrc mysql_dbdir="/var/db/mysql"

# Verify changes
sudo sysrc nginx_enable
# nginx_enable: YES

# Show all current settings
sudo sysrc -a

# Show only modified settings
sudo sysrc -A
```

---

## 3. Service Debugging

### 3.1 Common Debugging Commands

```bash
# Check if service is running
ps aux | grep <service_name>

# Check pidfile
cat /var/run/<service_name>.pid

# View service output
tail -f /var/log/<service_name>.log

# Check startup errors
cat /var/log/rc.log

# Run in foreground for debugging
sudo service <service_name> forcestart

# Check dependencies
service <service_name> requirements
```

### 3.2 RC Script Debugging

```bash
# Enable verbose output
rcverbose="YES"
sudo service <service_name> start

# Trace script execution
sh -x /etc/rc.d/<service_name> start

# Check script syntax
sh -n /etc/rc.d/<service_name>

# List all rc.d scripts
ls /etc/rc.d/

# Check startup order
rcorder /etc/rc.d/*

# Force run even if not enabled
sudo service -f <service_name> start
```

### 3.3 Common Issues

```bash
# Service fails to start
# 1. Check if port is already in use
sockstat | grep <port>

# 2. Check if pidfile exists
rm -f /var/run/<service_name>.pid

# 3. Check permissions
ls -la /etc/rc.d/<service_name>
chmod 555 /etc/rc.d/<service_name>

# 4. Check config file
service <service_name> configtest

# 5. Check logs
tail /var/log/messages
tail /var/log/rc.log
```

---

## 4. Managing Multiple Services

### 4.1 Service Dependencies

```bash
# Start services in order (respecting dependencies)
service jls  # List running jails

# Restart multiple services
for svc in nginx postgresql; do service $svc restart; done

# Check dependency tree
service <service_name> show-depends

# Start all services of a type
service -jail list  # List all jail services
```

### 4.2 Bulk Operations

```bash
# Stop all non-essential services (for maintenance)
sudo service -jail stopall

# Start all enabled services
sudo service netif restart  # Restart networking

# Restart services by pattern
for svc in $(ls /etc/rc.d/ | grep -E '^nginx|^apache'); do
    sudo service $svc restart
done
```

---

## 5. Service Configuration Files

### 5.1 rc.conf Settings

```bash
# /etc/rc.conf format
<service>_enable="YES"     # Enable at boot
<service>_flags="..."      # Additional flags
<service>_pidfile="..."    # Custom pidfile location
<service>_conf="..."       # Config file path

# Example: nginx
nginx_enable="YES"
nginx_flags=""
nginx_pidfile="/var/run/nginx.pid"

# Multiple instances
nginx_profiles="default example"
nginx_example_enable="YES"
```

### 5.2 Per-Service Settings

```bash
# Many services support profiles
# /etc/rc.conf.local or /etc/rc.conf

# Apache24 example
apache24_enable="YES"
apache24_httpd_server_starts="YES"

# PostgreSQL example
postgresql_enable="YES"
postgresql_data="/var/db/postgresql/data"

# MySQL example
mysql_enable="YES"
mysql_args="--skip-grant-tables"
```

---

## 6. Service Logging

### 6.1 Log Configuration

```bash
# Service logs typically go to
/var/log/<service_name>.log
/var/log/messages

# Rotate logs
sudo newsyslog /etc/newsyslog.conf

# Manual log rotation
sudo newsyslog -v /var/log/<service_name>.log

# Check recent log entries
tail -50 /var/log/messages | grep <service_name>
```

### 6.2 Centralized Logging

```bash
# syslog configuration for services
# /etc/syslog.conf
local0.* /var/log/service.log
local1.* @logserver.example.com

# Restart syslog after changes
sudo service syslogd restart
```

---

## 7. Service Security

### 7.1 Running Services with Least Privilege

```bash
# Many services support _user setting
# Check if service supports privilege dropping
grep "^command=" /etc/rc.d/<service>

# Example: nginx running as www
nginx_user="www"
nginx_group="www"

# Create dedicated service users
pw useradd -n myservice -m -s /sbin/nologin
```

### 7.2 Service Sandboxing

```bash
# Some services support chroot
# /etc/rc.conf
service_chroot="YES"
service_chroot_dir="/var/empty"

# Jailed services (see jail-manager skill)
# jexec <jail_id> service <service_name> start
```

---

## 8. Linux Systemd Services (Linuxulator)

### 8.1 Running systemd Services

```bash
# When running Linux binaries via Linuxulator,
# you may need systemd integration

# Check if systemd is available in Linux compat
ls /compat/linux/etc/systemd/system

# Linux service files go in
/compat/linux/etc/systemd/system/

# For Linux services, use
sudo systemctl --system <command>
# or inside the Linux compat environment
sudo chroot /compat/linux /usr/bin/systemctl <command>
```

### 8.2 Converting systemd to rc.d

```bash
# systemd unit file
# /etc/systemd/system/myapp.service
[Unit]
Description=My Application
After=network.target

[Service]
ExecStart=/usr/local/bin/myapp --daemon
Restart=always

[Install]
WantedBy=multi-user.target

# Convert to rc.d script
# /usr/local/etc/rc.d/myapp
#!/bin/sh
#
# PROVIDE: myapp
# REQUIRE: NETWORKING
# KEYWORD: shutdown

. /etc/rc.subr

name="myapp"
rcvar="${name}_enable"
command="/usr/local/bin/${name}"
command_args="--daemon"
pidfile="/var/run/${name}.pid"

load_rc_config $name
run_rc_command "$1"
```

---

## 9. Task Templates

### 9.1 Debug Service Issue

```markdown
## Task: Debug Service <name>

### Symptoms
- [ ] Service fails to start
- [ ] Service crashes on startup
- [ ] Service not responding

### Investigation Steps
```bash
# 1. Check service status
sudo service <name> status

# 2. Check logs
tail -100 /var/log/messages | grep <name>
journalctl -u <name>  # If systemd

# 3. Test configuration
sudo service <name> configtest

# 4. Try starting with debug
rcdebug=1 sudo service <name> start

# 5. Check resources
sockstat | grep <name>
lsof -i | grep <name>
```

### Resolution
- [ ] Fixed configuration
- [ ] Fixed permissions
- [ ] Fixed dependencies
```

### 9.2 Create New Service

```markdown
## Task: Create Service for <application>

### Steps
```bash
# 1. Create rc.d script
sudo vim /usr/local/etc/rc.d/<application>

# 2. Make executable
sudo chmod 555 /usr/local/etc/rc.d/<application>

# 3. Add to rc.conf
sudo sysrc <application>_enable="YES"

# 4. Test
sudo service <application> start
sudo service <application> status

# 5. Verify enabled
grep <application> /etc/rc.conf
```

### Configuration
| Setting | Value |
|---------|-------|
| enable | YES |
| flags | |
| pidfile | /var/run/<application>.pid |
```

---

## 10. Reference

### Quick Commands

```bash
# Service control
service <name> start|stop|restart|status|reload

# Enable/disable
sysrc <name>_enable="YES|NO"

# View settings
sysrc -a | grep <name>

# Check running services
service -e

# List all rc.d scripts
ls /etc/rc.d/

# Debug
rcdebug=1 service <name> start
sh -x /etc/rc.d/<name> start

# Force start
service -f <name> start
```

### Related Skills
- See jail-manager.md for jail-based service isolation
- See rc-script-writer.md for creating rc.d scripts
- See linuxulator-runner.md for Linux services on FreeBSD