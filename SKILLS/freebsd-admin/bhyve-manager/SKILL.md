---
name: bhyve-manager
description: >-
  Create, configure, run, and troubleshoot bhyve virtual machines on FreeBSD,
  with vm-bhyve or bhyve(8) directly. Use when setting up a VM, configuring
  bridge/tap networking or virtio storage, or building the isolated VM that
  kernel-level testing is required to run in.
---

# Skill: bhyve-manager

**Purpose:** Create, configure, start, stop, and manage bhyve virtual machines on FreeBSD.

**Triggers:** When setting up bhyve VMs, managing virtualized environments, or documenting bhyve configurations.

## Loading Instructions

Load this skill when the user asks you to:
- Create a bhyve virtual machine
- Configure bhyve networking (bridge, tap)
- Start/stop bhyve VMs
- Manage bhyve storage
- Document bhyve configurations

---

## 1. Bhyve Overview

### 1.1 What is bhyve?

```markdown
## Bhyve (BSD Hypervisor)

| Aspect | Description |
|--------|-------------|
| Type | Type-2 hypervisor (hardware-assisted virtualization) |
| License | BSD 2-Clause (`vmm.ko` kernel module) |
| Guest Support | FreeBSD, Linux, Windows, OpenBSD, NetBSD |
| Hardware | Requires CPU with VT-x/AMD-V |
| Kernel Module | vmm.ko |

## Bhyve vs Other Hypervisors

| Feature | bhyve | VirtualBox | VMware |
|---------|-------|------------|--------|
| License | BSD | GPL | Proprietary |
| Performance | Near-native | Medium | High |
| Windows Support | Yes (UEFI + virtio drivers) | Yes | Yes |
| Maturity | Mature | Very | Very |
| Live migration | Not supported | Yes | Yes |
| Runs on FreeBSD as host | Native | Port | No |
```

### 1.2 Check Hardware Support

```bash
# Check if CPU supports VT-x/AMD-V
grep -E "vmx|svm" /var/run/dmesg.boot

# Or
sysctl hw.model
grep -E "VMX|SVM" /var/run/dmesg.boot

# Check if vmm module is loaded
kldstat | grep vmm

# Load vmm module if not loaded
sudo kldload vmm

# Make permanent
echo 'vmm_load="YES"' >> /boot/loader.conf

# CloudBSD law: NEVER kldload an unproven/development vmm.ko on a development or
# CI host (AGENTS.md host safety). Test kernel-module changes inside an isolated
# bhyve VM, and install unproven kernels through a one-shot boot environment -
# see SKILLS/freebsd-admin/safe-kernel-deploy/.
```

---

## 2. Bhyve Networking

### 2.1 Network Types

```markdown
## Network Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| Bridge | VM connected to host bridge | Full network access |
| NAT | Host acts as NAT gateway | VM isolation |
| Host-only | VM only sees host | Testing |
| TAP | Custom bridging with firewall | Production |

## Bridge Mode (Most Common)

```
┌─────────────────────────────────────────────────────────┐
│  Host                                                  │
│                                                         │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐           │
│  │  em0    │    │  bridge0│    │   vm1   │           │
│  │(physical)│───►│(bridge)│◄───│  (tap0)│           │
│  └─────────┘    └────┬────┘    └─────────┘           │
│                      │                                  │
│                      │    ┌─────────┐                  │
│                      └───►│   vm2   │                  │
│                      TAP1 └─────────┘                  │
└─────────────────────────────────────────────────────────┘
```

### 2.2 Setup Bridge Networking

```bash
# 1. Load required modules
sudo kldload if_bridge
sudo kldload if_tuntap
sudo kldload bridgestp

# Make permanent
echo 'if_bridge_load="YES"' >> /boot/loader.conf
echo 'if_tuntap_load="YES"' >> /boot/loader.conf
echo 'bridgestp_load="YES"' >> /boot/loader.conf

# 2. Create bridge and add interface
sudo ifconfig bridge create name bridge0
sudo ifconfig bridge0 addm em0
sudo ifconfig bridge0 addm tap0
sudo ifconfig bridge0 up

# 3. Enable forwarding for NAT (if needed)
sudo sysctl net.inet.ip.forwarding=1

# 4. Setup NAT using pf or ipfw
# (See pf.conf example below)

# 5. Make permanent in /etc/rc.conf
sysrc cloned_interfaces="bridge0 tap0"
sysrc ifconfig_bridge0="addm em0 addm tap0 up"
```

### 2.3 TAP Device Setup

```bash
# Create tap device with permissions for non-root user
sudo ifconfig tap0 create
sudo ifconfig tap0 create
# Non-root use requires the vmm device permission, not chown on /dev/tapN:
sudo sysctl net.link.tap.user_open=1

# Or for persistent tap devices
sysrc autobridge_tap="tap0 tap1 tap2 tap3"
sysrc cloned_interfaces+="tap1 tap2 tap3"
```

---

## 3. Creating a VM

### 3.1 Disk Image

```bash
# Create a raw disk image
truncate -s 20G /var/vm/vm1.img

# Or using dd
dd if=/dev/zero of=/var/vm/vm1.img bs=1M count=20480

# Create a ZVOL (better performance)
sudo zfs create -V20G tank/vm/vm1
# Device: /dev/zvol/tank/vm/vm1
```

### 3.2 VM Configuration

```bash
# Create VM with vmrun
sudo sysrc vm_enable="YES"

# Using bhyve directly
bhyve \
    -c 2 \                    # 2 vCPUs
    -m 4G \                  # 4GB RAM
    -w \                     # UEFI boot
    -s 0,hostbridge \       # Host bridge
    -s 1,lpc \              # LPC device
    -s 2,virtio-blk,/var/vm/vm1.img \  # Disk
    -s 3,virtio-net,tap0 \ # Network
    -s 4,ahci-cd,/path/to/install.iso \  # CDROM
    -s 5,nvme,/dev/zvol/tank/vm/vm2 \   # Another disk
    vm1

# With serial console (for FreeBSD installation)
bhyve \
    -c 4 \
    -m 8G \
    -w \
    -s 0,hostbridge \
    -s 1,lpc \
    -s 2,virtio-blk,/var/vm/vm1.img \
    -s 3,virtio-net,tap0 \
    -s 4,ahci-cd,/path/to/FreeBSD-14.0.iso \
    -s 5,nvme,/dev/zvol/tank/vm/vm2 \
    -s 29,fbuf,tcp=0.0.0.0:5900 \  # VNC on port 5900
    -s 30,xhci,tablet \
    -A \
    -H \
    -P \
    -s 31,uart,off \
    vm1
```

### 3.3 UEFI Firmware

```bash
# FreeBSD 14+ includes uefi firmware
# For older versions or other OS, download OVMF

# Install uefi firmware
pkg install uefi-edk2-bhyve

# Verify firmware location
ls /usr/local/share/uefi-firmware/
# Should contain BHYVE_*.fd files
```

---

## 4. VM Lifecycle

### 4.1 Starting a VM

```bash
# Simple start (foreground, Ctrl+C to stop)
bhyve -c 2 -m 4G -w -s 0,hostbridge -s 1,lpc \
    -s 2,virtio-blk,/var/vm/vm1.img \
    -s 3,virtio-net,tap0 \
    vm1

# With console (serial)
bhyve -c 2 -m 4G -w -s 0,hostbridge -s 1,lpc \
    -s 2,virtio-blk,/var/vm/vm1.img \
    -s 3,virtio-net,tap0 \
    -l com1,stdio \
    vm1

# As background service
bhyve -c 2 -m 4G -w -s 0,hostbridge -s 1,lpc \
    -s 2,virtio-blk,/var/vm/vm1.img \
    -s 3,virtio-net,tap0 \
    -l com1,/dev/nmdm-0A \
    vm1 &

# Use vm-bhyve framework (recommended)
vm init
vm create -t freebsd -s 20G vm1
vm install vm1 FreeBSD-14.0-RELEASE.iso
vm start vm1
```

### 4.2 Stopping a VM

```bash
# Graceful shutdown (via ACPI)
# Inside VM: shutdown -p now

# Force kill
bhyvectl --destroy --vm=vm1        # tear down a stopped VM
bhyvectl --force-poweroff --vm=vm1 # forcibly power off a running VM

# Or via kill
pkill -f "bhyve.*vm1"

# With vm-bhyve
vm stop vm1
vm destroy vm1
```

### 4.3 Persistent VMs with rc.d

```bash
# /etc/rc.d/bhyveVM (example rc script)

#!/bin/sh
#
# PROVIDE: bhyveVM
# REQUIRE: NETWORKING
# KEYWORD: shutdown

. /etc/rc.subr

name="bhyveVM"
rcvar="bhyveVM_enable"
command="/usr/sbin/bhyve"
command_args="-c 2 -m 4G -w -s 0,hostbridge -s 1,lpc \
    -s 2,virtio-blk,/var/vm/vm1.img \
    -s 3,virtio-net,tap0 \
    -l com1,/dev/nmdm-0A \
    vm1"

load_rc_config $name
run_rc_command "$1"
```

---

## 5. Using vm-bhyve (Recommended Framework)

### 5.1 Installation and Setup

```bash
# Install vm-bhyve
pkg install vm-bhyve

# Initialize
vm init

# Configure switch (equivalent to bridge)
vm switch create public
vm switch add public em0

# Or with private switch
vm switch create private
vm switch add private tap0

# List switches
vm switch list
```

### 5.2 VM Templates

```bash
# Available templates
ls /usr/local/share/vm-bhyve/templates/

# Create from template
vm create -t freebsd -s 20G -n public vm1
vm create -t debian12 -s 40G -n public webserver

# Custom configuration
vm create -t custom -s 20G -n public vm1
# Edit: /vm/vm1/vm.conf
```

### 5.3 VM Management

```bash
# List VMs
vm list

# Start VM
vm start vm1

# Stop VM
vm stop vm1

# Console access
vm console vm1
# Exit console: ~.

# Live configure (requires stop)
vm configure vm1

# Delete VM
vm destroy vm1

# Clone VM
vm clone vm1 vm1-copy

# Snapshot (with ZFS)
zfs snapshot tank/vm/vm1@clean
zfs rollback tank/vm/vm1@clean
```

### 5.4 vm-bhyve Configuration

```bash
# /etc/rc.conf additions
vm_enable="YES"
vm_dir="zfs:tank/vm"

# /vm/vm1/vm.conf example
loader="uefi"
cpu="2"
memory="4G"
network0_type="virtio-net"
network0_switch="public"
disk0_type="virtio-blk"
disk0_dev="zvol:tank/vm/vm1/disk0"
```

---

## 6. Storage Configuration

### 6.1 Virtio Block

```bash
# Raw file
-s 2,virtio-blk,/var/vm/vm1.img

# ZVOL
-s 2,virtio-blk,/dev/zvol/tank/vm/vm1

# With discard support (TRIM)
-s 2,virtio-blk,/var/vm/vm1.img,nocache,direct
```

### 6.2 AHCI (SATA Compatible)

```bash
# For Windows or other OS without virtio drivers
-s 2,ahci,/var/vm/vm1.img

# With CDROM
-s 3,ahci-cd,/path/to/install.iso
```

### 6.3 NVMe

```bash
# Best performance
-s 2,nvme,/dev/nvme0n1

# Raw disk (AHCI) - for guests without virtio/nvme drivers
-s 2,ahci-hd,/dev/ada0
```

---

## 7. Device Passthrough

### 7.1 PCIe Passthrough

```bash
# Enable in /boot/loader.conf
pptdevs="1/0/0"          # reserve 01:00.0 for passthrough at boot

# Or for specific devices
# Find device
pciconf -lv | grep -A3 vgapci

# Add to VM
bhyve -s 0,hostbridge \
      -s 1,lpc \
      -s 2,virtio-blk,/var/vm/vm1.img \
      -s 4,passthru,01/0/0 \  # PCIe slot
      vm1
```

### 7.2 USB Passthrough

```bash
# Find USB device
usbconfig
# Look for ugen0.2

# Pass through
-s 5,xhci,1-2
```

---

## 8. Bhyve Configuration Template

### 8.1 Complete VM Configuration

```markdown
## VM: <Name>

### Resources
| Resource | Value |
|----------|-------|
| vCPUs | 2 |
| RAM | 4G |
| Disk | 20G (ZVOL) |
| Network | virtio-net (tap0) |

### Devices
| Slot | Device | Config |
|------|--------|--------|
| 0 | hostbridge | - |
| 1 | lpc | - |
| 2 | virtio-blk | /dev/zvol/tank/vm/vm1/disk0 |
| 3 | virtio-net | tap0 |
| 4 | ahci-cd | /path/to/install.iso |

### Networking
| Type | Config |
|------|--------|
| Switch | public |
| IP | DHCP |
| Gateway | Via bridge0 |

### Installation
1. Create disk: `zfs create -V20G tank/vm/vm1`
2. Start with ISO mounted
3. Connect to console: `vm console vm1`
4. Install FreeBSD
5. Remove ISO, reboot
```

---

## Validation Checklist

Before deploying VM:

- [ ] CPU has VT-x/AMD-V support
- [ ] vmm module loaded
- [ ] Network bridge configured
- [ ] Disk image/ZVOL created
- [ ] UEFI firmware available
- [ ] VM can boot and install OS
- [ ] Network connectivity verified
- [ ] RC script created for persistence

## Reference

See jail-manager for FreeBSD jail management.