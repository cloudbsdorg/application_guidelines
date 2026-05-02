# Skill: zfs-manager

**Purpose:** Create, manage, and safely operate ZFS pools and datasets on FreeBSD, with emphasis on preventing destructive operations.

**Triggers:** When setting up ZFS pools, creating datasets, managing snapshots, or performing administrative operations.

## Loading Instructions

Load this skill when the user asks you to:
- Create ZFS pools
- Manage datasets and snapshots
- Perform ZFS administrative tasks
- Understand ZFS safety practices
- Recover from ZFS issues

## Core Principle

> **ZFS is powerful but destructive commands are permanent. Always verify before acting, especially with `zfs destroy`, `zpool destroy`, and recursive operations.**

---

## 1. ZFS Safety Rules

### 1.1 CRITICAL: Never Do These

```markdown
## DANGEROUS Commands - Always Verify Before Running

| Command | Why Dangerous | Safer Alternative |
|--------|---------------|-------------------|
| `zfs destroy -r dataset` | Recursively deletes dataset and ALL children | Use `zfs list -t filesystem` first |
| `zpool destroy pool` | Permanently destroys entire pool | Use `zpool status` first |
| `zpool attach -f` | Force attach can cause data loss | Verify pool status first |
| `zpool remove -f` | Force remove can fail | Check with `zpool status` |
| `rm -rf /` | ZFS doesn't protect against this | Never run this |
| `zpool export -f` | Force export can corrupt | Use `zpool export` without -f |

## Pre-Destructive Command Checklist

Before ANY destructive command:
- [ ] Run `zpool status` to verify pool health
- [ ] Run `zfs list` to see affected datasets
- [ ] Run `zfs list -t snapshot` to check for snapshots
- [ ] Verify dataset name is EXACTLY correct
- [ ] Check spelling - ZFS will not ask for confirmation
```

### 1.2 Dry Run Before Destroy

```bash
# ALWAYS dry-run destroy first
# Use -n flag (dry run) with -v (verbose)

zfs destroy -rvn dataset

# Example output:
# would destroy 'tank/home/user1'
# would destroy 'tank/home/user1@daily-2026-05-01'
# would reclaim 50G

# Only remove -n when you are CERTAIN

# For pools, check what's in it first
zpool list -v tank
zpool status tank
```

### 1.3 ZFS Destroy Safety Pattern

```bash
# SAFE destroy workflow

# 1. List all datasets and snapshots
zfs list -t all -r tank

# 2. Check what would be destroyed
zfs destroy -rvn tank/old_dataset

# 3. Create safety snapshot BEFORE destroy
zfs snapshot tank/old_dataset@pre-destroy-$(date +%Y%m%d)

# 4. Wait, verify, then destroy (without -n)
zfs destroy tank/old_dataset

# 5. If disaster strikes, recover from snapshot
zfs rollback tank/old_dataset@pre-destroy-20260501
```

---

## 2. Pool Creation

### 2.1 Basic Pool Creation

```bash
# Create simple pool (single disk)
sudo zpool create -f tank /dev/ada0

# Create mirrored pool
sudo zpool create -f tank mirror /dev/ada0 /dev/ada1

# Create raidz pool
sudo zpool create -f tank raidz /dev/ada0 /dev/ada1 /dev/ada2

# Create with partitions (recommended)
sudo zpool create -f tank /dev/ada0p3

# Create with specific ashift (4K sector support)
sudo zpool create -f -o ashift=12 tank /dev/ada0
```

### 2.2 Pool Creation with Features

```bash
# Create with all FreeBSD recommended features
sudo zpool create -f \
    -O aclmode=posixacl \
    -O aclinherit=posixacl \
    -O atime=off \
    -O compression=lz4 \
    -O normalization=formD \
    -O utf8only=on \
    tank \
    /dev/ada0
```

---

## 3. Dataset Management

### 3.1 Creating Datasets

```bash
# Create dataset
zfs create tank/home

# Create with properties
zfs create \
    -o quota=100G \
    -o recordsize=128K \
    -o atime=off \
    tank/home

# Create child datasets
zfs create tank/home/user1
zfs create tank/home/user2

# Create dataset for VM storage
zfs create -o volsize=20G tank/vm/vm1

# Create dataset with specific block size for databases
zfs create \
    -o recordsize=16K \
    -o primarycache=metadata \
    tank/postgres
```

### 3.2 Dataset Properties

```bash
# List properties
zfs get all tank/home

# Get specific property
zfs get compression tank/home

# Set property
zfs set compression=lz4 tank/home

# Set quota
zfs set quota=50G tank/home/user1

# Set reservation (guaranteed space)
zfs set reservation=10G tank/home/user1

# Remove quota
zfs set quota=none tank/home/user1
```

### 3.3 Dataset Properties Reference

```markdown
## Important Properties

| Property | Values | Purpose |
|----------|--------|---------|
| compression | on/off/lz4/gzip | Enable compression |
| atime | on/off | Access time updates |
| aclmode | posixacl/manditory | ACL behavior |
| aclinherit | posixacl/manditory | ACL inheritance |
| quota | size/none | Max dataset size |
| reservation | size/none | Guaranteed space |
| recordsize | 512-1M | Block size |
| primarycache | all/metadata/none | Cache behavior |
| logbias | latency/throughput | ZIL behavior |
| sync | always/standard/disabled | Sync behavior |
| dedup | on/off | Deduplication |
| checksum | on/off/fletcher | Checksum level |
```

---

## 4. Snapshots

### 4.1 Creating Snapshots

```bash
# Create simple snapshot
zfs snapshot tank/home@monday

# Create recursive snapshot (dataset and children)
zfs snapshot -r tank/home@daily-2026-05-01

# Create snapshot of specific dataset
zfs snapshot tank/vm/vm1-disk0@before-upgrade

# Create bookmark (like snapshot but without space)
zfs bookmark tank/home@monday tank/home#monday
```

### 4.2 Managing Snapshots

```bash
# List snapshots
zfs list -t snapshot
zfs list -t snapshot -r tank/home

# Rename snapshot
zfs rename tank/home@old tank/home@daily

# Rollback to snapshot (DESTRUCTIVE - loses all changes since)
zfs rollback tank/home@monday

# Rollback to recursive snapshot
zfs rollback -r tank/home@monday

# Clone snapshot (creates new dataset from snapshot)
zfs clone tank/home@monday tank/home-clone
```

### 4.3 Snapshot Cleanup

```bash
# Destroy snapshot (be careful!)
zfs destroy tank/home@old

# Destroy recursive snapshots
zfs destroy -r tank/home@cleanup-2026-04-01

# List and destroy old snapshots (keep last 7 days)
for snap in $(zfs list -H -t snapshot -o name -r tank | grep -E '@daily-2026-0[123456]'); do
    echo "Would destroy: $snap"
    # zfs destroy "$snap"
done

# Automatic cleanup with expire
# Add to /etc/periodic.conf:
# weekly_snap_delete="YES"
# snap_keep="7"
```

---

## 5. ZFS Send/Receive (Backup)

### 5.1 Basic Send/Receive

```bash
# Send snapshot to file
zfs send tank/home@monday > /backup/home-monday.zfs

# Send with compression
zfs send tank/home@monday | gzip > /backup/home-monday.zfs.gz

# Incremental send (only changed blocks)
zfs send -i tank/home@monday tank/home@tuesday > /backup/home-mon-tue.zfs

# Receive dataset from snapshot
zfs receive tank/home-restored < /backup/home-monday.zfs

# Receive to new dataset name
zfs receive tank/home-new < /backup/home-monday.zfs
```

### 5.2 Send/Receive Safety

```bash
# DRY RUN first
zfs send -nv tank/home@monday | zfs receive -nv tank/home-test

# Use -v (verbose) to see what's being sent
zfs send -v tank/home@monday | zfs receive -v tank/home-test

# Safe backup script pattern
#!/bin/sh
POOL=tank
DEST=/backup/zfs
DATE=$(date +%Y-%m-%d)

# Check space before send
DEST_AVAIL=$(zfs get -Hp -o value available $DEST)
SNAP_SIZE=$(zfs send -nvp tank/home@$DATE 2>/dev/null | tail -1 | awk '{print $1}')

if [ "$SNAP_SIZE" -gt "$DEST_AVAIL" ]; then
    echo "ERROR: Not enough space. Need $SNAP_SIZE, have $DEST_AVAIL"
    exit 1
fi

# Send
zfs send -v $POOL/home@$DATE | gzip > $DEST/home-$DATE.zfs.gz
```

---

## 6. Pool Operations

### 6.1 Pool Status

```bash
# Check pool health
zpool status

# Check specific pool
zpool status tank

# Check with I/O stats
zpool iostat tank 1

# Check pool properties
zpool get all tank

# Check pool capacity (watch for >80%)
zpool list -o name,size,alloc,free,cap,health
```

### 6.2 Pool Health Reference

```markdown
## Pool Health States

| State | Meaning | Action Required |
|-------|---------|----------------|
| ONLINE | All devices working | None |
| DEGRADED | One or more devices degraded | Replace failed device |
| FAULTED | Device offline, too many failures | Replace and online |
| OFFLINE | Device manually offline | Online or replace |
| REMOVED | Device physically removed | Replace |
| UNAVAIL | Cannot open pool | Check device paths |

## Check Device Health

```bash
# Check SMART status
smartctl -a /dev/ada0

# Check for errors
zpool status -v tank
# Look for errors in 'errors' column

# Check ZFS intent log
zpool status -c tank
```
```

### 6.3 Pool Expansion

```bash
# Add device to pool
zpool add tank /dev/ada2

# Add mirrored devices
zpool add tank mirror /dev/ada2 /dev/ada3

# Replace device (one-by-one)
zpool replace tank /dev/ada0 /dev/ada1

# Online/offline device
zpool offline tank /dev/ada0
zpool online tank /dev/ada0
```

### 6.4 Pool Import/Export

```bash
# List pools available for import
zpool import

# Import specific pool
zpool import tank

# Import with different name
zpool import tank tank2

# Force import (after device changes)
zpool import -f tank

# Export pool (safe - flushes all writes)
zpool export tank

# Emergency export (force, even if busy)
zpool export -f tank
```

---

## 7. Common Mistakes and Prevention

### 7.1 Mistake: Destroying Wrong Dataset

```bash
# WRONG: You meant to type tank/old but typed tank
zfs destroy -r tank  # DESTROYS EVERYTHING

# RIGHT: Always verify first
zfs list -r tank | head -20
zfs destroy -rvn tank/old  # dry run first
# (remove -n only after verification)
```

### 7.2 Mistake: Quota Prevents Writes

```bash
# User complains: "Can't write files, disk says full"
df -h
# Shows 50% used

# Check ZFS quota
zfs get quota tank/home/user1
# Shows quota=10G

# Fix: Increase or remove quota
zfs set quota=none tank/home/user1
```

### 7.3 Mistake: Reservation vs Quota

```bash
# Quota: Maximum size dataset can use
# Reservation: Guaranteed space for dataset

# Dataset at quota but reservation not met
# means other datasets took that space!

# Check both
zfs get reservation,quota,used tank/home
```

### 7.4 Mistake: Forgetting Snapshot Before Risky Operation

```bash
# ALWAYS snapshot before:
# - Upgrade
# - Configuration change
# - Large file operation
# - Anything risky

# Quick safety snapshot
zfs snapshot tank@pre-$(date +%Y%m%d-%H%M%S)

# Verify snapshot exists
zfs list -t snapshot | grep pre-2026
```

---

## 8. ZFS Task Templates

### 8.1 Create VM Storage Dataset

```markdown
## Task: Create VM Storage Dataset

```bash
# 1. Create parent dataset for VMs
zfs create -o mountpoint=none tank/vm

# 2. Create dataset for specific VM
zfs create -o volsize=100G -o sync=standard tank/vm/vm1

# 3. Verify
zfs get volsize,used,available tank/vm/vm1

# 4. Create snapshot before major operation
zfs snapshot tank/vm/vm1@pre-upgrade
```

### 8.2 Setup User Home Dataset

```markdown
## Task: Setup User Home Directories

```bash
# 1. Create home dataset
zfs create \
    -o quota=50G \
    -o atime=off \
    -o compression=lz4 \
    tank/home

# 2. Create user directories
zfs create tank/home/user1
zfs create tank/home/user2

# 3. Set user quotas
zfs set quota=100G tank/home/user1
zfs set quota=50G tank/home/user2

# 4. Enable snapshots for /home
zfs set snapshot-dir=.zfs/snapshot tank/home
```
```

---

## Validation Checklist

Before running destructive commands:

- [ ] `zpool status` shows pool healthy
- [ ] `zfs list` shows correct dataset
- [ ] Dry run (-n) shows expected results
- [ ] Snapshot exists for recovery
- [ ] Dataset name is EXACTLY correct
- [ ] No typos in dataset path
- [ ] Enough space in destination pool
- [ ] Not going to break other datasets

## Reference

See bhyve-manager for using ZFS volumes with bhyve VMs.