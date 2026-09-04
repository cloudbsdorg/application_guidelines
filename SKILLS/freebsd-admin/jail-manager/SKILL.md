---
name: jail manager
description: Create, configure, start, stop, and manage FreeBSD jails using common tools like `jail(8)`, `ezjail`, `iocage`, `bastille`, and `pot` (Prison on Trust).
---

# Skill: jail-manager

**Purpose:** Create, configure, start, stop, and manage FreeBSD jails using common tools like `jail(8)`, `ezjail`, `iocage`, `bastille`, and `pot` (Prison on Trust).

**Triggers:** When setting up FreeBSD jails, managing isolated environments, or documenting jail configurations.

## Loading Instructions

Load this skill when the user asks you to:
- Create a FreeBSD jail
- Configure jail networking
- Manage jail lifecycle
- Setup jail with common tools
- Document jail configurations

---

## 1. Jail Overview

### 1.1 What is a Jail?

```markdown
## FreeBSD Jails

| Aspect | Description |
|--------|-------------|
| Type | Operating-system-level virtualization |
| Isolation | Separate filesystem, process, network space |
| Overhead | Very low (kernel-level) |
| Guest OS | FreeBSD only |
| Tools | jail(8), ezjail, iocage, bastille, pot |

## Jail vs Other Virtualization

| Feature | Jail | bhyve | Docker |
|---------|------|-------|--------|
| Guest OS | FreeBSD | Any | Any |
| Overhead | Minimal | Medium | Low |
| Isolation | Strong | Strong | Medium |
| Complexity | Medium | Medium | Low |
| Stateful | Yes | Yes | Usually not |
```

### 1.2 Jail Structure

```
┌─────────────────────────────────────────────────┐
│                   Host System                     │
│                                                  │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐│
│  │   Jail 1   │  │   Jail 2   │  │   Jail 3   ││
│  │  /jail/j1  │  │  /jail/j2  │  │  /jail/j3  ││
│  │     │       │  │     │       │  │     │       ││
│  │  Processes  │  │  Processes  │  │  Processes  ││
│  │     │       │  │     │       │  │     │       ││
│  │  10.0.0.1  │  │  10.0.0.2  │  │  10.0.0.3  ││
│  └────────────┘  └────────────┘  └────────────┘│
│       │               │               │            │
│       └───────────────┴───────────────┘            │
│                  IP sharing (via host)             │
└─────────────────────────────────────────────────┘
```

---

## 2. Native jail(8)

### 2.1 Basic Jail Creation

```bash
# Create jail root directory
sudo mkdir -p /jail/jail1

# Create basic jail structure
sudo mkdir -p /jail/jail1/{bin,etc,root,usr,var,tmp}

# Extract FreeBSD base system
sudo bsdtar -xf /path/to/base.txz -C /jail/jail1

# Or using makefs (for testing)
# For production, use release files or jail utility

# Create jail.conf
sudo vim /etc/jail.conf
```

### 2.2 jail.conf Configuration

```conf
# /etc/jail.conf

# Global settings
path = "/jail/$name";
host.hostname = "$name";
exec.start = "/bin/sh /etc/rc";
exec.stop = "/bin/sh /etc/rc.shutdown";
exec.clean;
mount.devfs;

# Define jails
jail1 {
    ip4.addr = 10.0.0.1/24;
    interface = epair0b;
}

jail2 {
    ip4.addr = 10.0.0.2/24;
    interface = epair0b;
}

# Simple jail (IP-less)
jail3 {
    ip4.addr = "none";
}
```

### 2.3 Managing Native Jails

```bash
# Start jail
sudo jail -c jail1

# Start with console
sudo jail -c jail1 console=1

# List running jails
sudo jls

# Attach to jail console
sudo jexec -u root jail1 sh

# Stop jail
sudo jail -r jail1

# Restart jail
sudo jail -r jail1 && jail -c jail1

# Start all jails defined in jail.conf
sudo service jail start

# Check jail status
sudo service jail status
```

---

## 3. ezjail (Simple Jail Manager)

### 3.1 Installation and Setup

```bash
# Install ezjail
sudo pkg install ezjail

# Initialize ezjail
sudo ezjail-admin install

# Or with custom base.txz
sudo ezjail-admin install -m -p /path/to/base.txz

# Configure networking
# Edit /usr/local/etc/ezjail.conf
ezjail_physics_if="em0"  # Physical interface to use
ezjail_jailzfs="zpool/jails"  # ZFS dataset for jails
```

### 3.2 Managing Jails with ezjail

```bash
# Create new jail
sudo ezjail-admin create jail1 'em0|10.0.0.1'

# Create with specific FreeBSD version
sudo ezjail-admin create -f 14.0-RELEASE jail1 'em0|10.0.0.1'

# List jails
sudo ezjail-admin list

# Start jail
sudo ezjail-admin start jail1

# Stop jail
sudo ezjail-admin stop jail1

# Console access
sudo ezjail-admin console jail1

# Delete jail
sudo ezjail-admin delete jail1

# Update jail (re-fetch base)
sudo ezjail-admin update -i
```

### 3.3 ezjail Configuration

```bash
# /usr/local/etc/ezjail.conf
ezjail_physics_if="em0"
ezjail_jailzfs="zpool/jails"

# Or for simple setup without ZFS
# Leave ezjail_jailzfs commented out

# Per-jail configuration in /usr/local/etc/ezjail/
# Create jail1 file for custom settings
```

---

## 4. iocage (Advanced Jail Manager)

### 4.1 Installation and Setup

```bash
# Install iocage
sudo pkg install iocage

# Initialize iocage
sudo iocage activate zpool/jails

# Download FreeBSD RELEASE
sudo iocage fetch release=14.0-RELEASE
```

### 4.2 Managing Jails with iocage

```bash
# Create jail
sudo iocage create -n jail1 -r 14.0-RELEASE

# With custom IP
sudo iocage create -n jail1 -r 14.0-RELEASE \
    ip4_addr="em0|10.0.0.1/24"

# List jails
sudo iocage list

# Start jail
sudo iocage start jail1

# Stop jail
sudo iocage stop jail1

# Restart jail
sudo iocage restart jail1

# Console access
sudo iocage console jail1

# Destroy jail
sudo iocage destroy -f jail1
```

### 4.3 iocage Properties

```bash
# Get property
sudo iocage get all jail1

# Set property
sudo iocage set boot=on jail1
sudo iocage set ip4_addr="em0|10.0.0.1/24" jail1

# Commonly used properties
sudo iocage set boot=on \
    ip4_addr="em0|10.0.0.1/24" \
    defaultrouter="10.0.0.1" \
    hostname="jail1.example.com" \
    jail1
```

### 4.4 iocage Templates

```bash
# Create custom template
sudo iocage set template=yes jail1
sudo iocage stop jail1

# Clone from template
sudo iocage clone template_jail1 name=jail2
```

---

## 5. bastille (Container-style Manager)

### 5.1 Installation and Setup

```bash
# Install bastille
sudo pkg install bastille

# Initialize bastille
sudo bastille bootstrap 14.0-RELEASE

# Configure /usr/local/etc/bastille.conf
```

### 5.2 Managing Jails with bastille

```bash
# Create jail
sudo bastille create jail1 14.0-RELEASE 10.0.0.1 em0

# List jails
sudo bastille list

# Start jail
sudo bastille start jail1

# Stop jail
sudo bastille stop jail1

# Console access
sudo bastille console jail1

# Destroy jail
sudo bastille destroy jail1
```

### 5.3 bastille Commands

```bash
# Package management inside jail
sudo bastille pkg jail1 update
sudo bastille pkg jail1 upgrade

# Bastille file management
sudo bastille fstab jail1

# Clone jail
sudo bastille clone jail1 jail2

# Template support
sudo bastille template jail1 /path/to/template
```

---

## 6. pot (Prison on Trust)

### 6.1 Overview

```markdown
## pot (Prison on Trust)

| Aspect | Description |
|--------|-------------|
| Type | Jail management framework |
| Style | Simple, chef-like recipes |
| ZFS | Native ZFS support |
| Unique | Uses "flavors" for customization |

## pot vs Other Jail Managers

| Feature | pot | iocage | bastille |
|---------|-----|--------|----------|
| ZFS integration | Native | Yes | Optional |
| Flavors | Yes | Templates | Templates |
| Learning curve | Low | Medium | Medium |
| Native ZFS snapshots | Yes | Yes | Via rc.d |

### 6.2 Installation and Setup

```bash
# Install pot
sudo pkg install pot

# Initialize pot
sudo pot init

# Configure pot
# Edit /usr/local/etc/pot.conf
```

### 6.3 Managing Jails with pot

```bash
# Create jail
sudo pot create -p myjail -t 14.0-RELEASE -N public

# Start jail
sudo pot start myjail

# Stop jail
sudo pot stop myjail

# List jails
sudo pot list

# Console access
sudo pot console myjail

# Delete jail
sudo pot destroy myjail
```

### 6.4 pot Flavors

```bash
# Flavors are customization scripts
# Create flavor: /usr/local/etc/pot/flavors/myflavor.sh
#!/bin/sh
pkg install -y nginx
sysrc nginx_enable="YES"

# Apply flavor to jail
sudo pot create -p webjail -t 14.0-RELEASE -f myflavor -N public

# List available flavors
ls /usr/local/etc/pot/flavors/
```

### 6.5 pot Commands Reference

```bash
# Jail lifecycle
pot create -p <name> -t <release> [options]
pot start <jail>
pot stop <jail>
pot restart <jail>
pot destroy <jail>

# Information
pot list
pot info <jail>
pot console <jail>

# Snapshots (ZFS)
pot snapshot -p <jail> -s <snap>
pot rollback -p <jail> -s <snap>

# Networking
pot networking <jail>  # Show IP config
```

---

## 7. Jail Networking

### 7.1 Virtual Networking (epair)

```bash
# Create epair interface pair
sudo ifconfig epair0 create

# Configure host side
sudo ifconfig epair0a 10.0.0.254/24 up

# Add to jail (in jail.conf)
jail1 {
    interface = "epair0b";
    ip4.addr = "10.0.0.1/24";
}

# Or with ezjail
ezjail-admin create -c epair jail1 'epair0b|10.0.0.1/24'

# Or with iocage
sudo iocage create -n jail1 ip4_addr="epair0b|10.0.0.1/24"
```

### 7.2 NAT for Jails

```bash
# /etc/pf.conf for NAT
ext_if="em0"
int_net="10.0.0.0/24"

# NAT outgoing traffic from jails
nat on $ext_if from $int_net to any -> ($ext_if)

# Load pf
sudo pfctl -f /etc/pf.conf
sudo pfctl -e
```

---

## 8. Jail Management Task Template

### 8.1 Create Production Jail

```markdown
## Task: Create Production Jail

### Prerequisites
- [ ] ZFS pool available for jail storage
- [ ] Network interface configured
- [ ] FreeBSD RELEASE downloaded

### Steps

```bash
# 1. Choose tool (iocage recommended)
pkg install iocage
iocage activate tank/jails
iocage fetch release=14.0-RELEASE

# 2. Create jail
iocage create -n webserver -r 14.0-RELEASE \
    ip4_addr="em0|10.0.0.10/24" \
    defaultrouter="10.0.0.1" \
    boot=on \
    onboot=yes

# 3. Configure resources
iocage set cpu=2 webserver
iocage set ram=2G webserver
iocage set setvifvar=on webserver

# 4. Start and verify
iocage start webserver
iocage list
jexec -u root webserver /bin/sh

# 5. Install packages inside jail
iocage console webserver
pkg update && pkg install nginx
```

### Configuration

| Property | Value |
|----------|-------|
| Name | webserver |
| IP | 10.0.0.10/24 |
| Gateway | 10.0.0.1 |
| vCPUs | 2 |
| RAM | 2G |
| Boot | on |

### Verification
- [ ] Jail starts on host boot
- [ ] Network accessible from jail
- [ ] Can reach external network from jail
- [ ] Services start correctly
```

---

## Validation Checklist

Before deploying jail:

- [ ] Network interface exists and configured
- [ ] IP address available and not in use
- [ ] Sufficient resources (CPU, RAM)
- [ ] Jail tool installed and configured
- [ ] Firewall rules allow required traffic
- [ ] Backup strategy in place

## Reference

See bhyve-manager for VM alternatives.