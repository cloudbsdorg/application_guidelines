---
name: safe-kernel-deploy
description: >-
  Install an unproven kernel, kernel module, or world onto a FreeBSD machine so
  that a panic, a hang, or a kernel that will not boot reverts to the last
  known-good state on its own. Use whenever booting a build that has not been
  proven on that machine, or when asked to deploy with automatic rollback, a
  one-shot boot environment, or a bectl-based upgrade.
keywords:
  - bectl
  - boot environment
  - one-shot
  - rollback
  - unproven kernel
  - kldload
  - panic
  - watchdogd
  - META_MODE
---

# Safe FreeBSD deploy with a one-shot boot environment

Install unproven boot artifacts into a **new** boot environment, boot it
**once**, and guarantee that a failure reverts to the previous known-good
environment with nobody at the console.

This is the mechanism behind the CloudBSD host-safety law: an untested kernel
module is never loaded on a development or CI host, and kernel-level work
happens inside an isolated VM (see `Testing-Infrastructure/TESTING_INFRASTRUCTURE.md`
and [bhyve-manager](../bhyve-manager/SKILL.md)). When a real machine must boot
an unproven kernel anyway, this is how.

## Why two mechanisms, not one

1. **One-shot activation.** `bectl activate -t <candidate>` marks the candidate
   as the next-boot target only. The loader consumes that flag at boot, so if
   the machine reboots again for any reason it comes back on the permanent,
   known-good environment. A hang or a panic-triggered reboot reverts itself.
2. **Panic and hang auto-reboot.** Sysctls make a panic power-cycle instead of
   dropping into the debugger, and `watchdogd` catches a wedge. Without these a
   bad kernel simply sits there, and one-shot never gets the second reboot that
   makes it work.

Never make the candidate permanent - `bectl activate` without `-t`, or
`zpool set bootfs=` - until after you have verified it booted and is healthy.
Flipping `bootfs` to the candidate is precisely how a failed environment
never reverts.

## Procedure

Run as root. `$BE` is the candidate name, `$MNT` a mountpoint.

1. **Record the known-good environment.**
   ```sh
   bectl list                                  # the row marked "NR" is running
   zpool get -H -o value bootfs zroot          # remember this value
   ```

2. **Arm the fail-reboot contract on the running system**, so both this reboot
   and the candidate's power-cycle on panic:
   ```sh
   sysctl debug.debugger_on_panic=0 kern.powercycle_on_panic=1 \
          kern.panic_reboot_wait_time=5
   ```
   Persist it in `/etc/sysctl.conf`. If a hang that leaves the box alive but
   unreachable is a concern, arm `watchdogd` with a reachability probe in
   `watchdogd_flags`.

3. **Build the artifacts, with META_MODE on.** Load `filemon` and set
   `WITH_META_MODE=yes` (in `/etc/src-env.conf`, or on the make line) **before
   the first build of the campaign**. META_MODE records what each target read,
   so a rebuild re-runs only the targets whose inputs changed - a header fix
   becomes seconds instead of a full `buildkernel`. Turning it on after the
   slow build you were trying to avoid does not help: the first meta build over
   a non-meta object tree still does a near-full pass. Reuse one
   `MAKEOBJDIRPREFIX` across iterations so the cache survives.

4. **Create and mount a fresh boot environment** - never install into the
   running one:
   ```sh
   bectl create "$BE"
   bectl mount  "$BE" "$MNT"
   ```

5. **Install into it through `DESTDIR`:**
   ```sh
   make installkernel KERNCONF=GENERIC DESTDIR="$MNT"
   # or a single module:
   install -m 555 vmm.ko "$MNT"/boot/kernel/vmm.ko
   ```

6. **Apply the fail-reboot contract to the candidate too** - edit the files
   under `$MNT`, not only the live root. A candidate that boots with the
   debugger enabled and no watchdog cannot revert. For a development kernel,
   also disable autoloading of the module under test, so a module that panics
   on load cannot create a panic loop that outruns the one-shot flag.

7. **Unmount and activate for one boot only:**
   ```sh
   bectl umount "$BE"
   good=$(zpool get -H -o value bootfs zroot)
   bectl activate -t "$BE"
   [ "$(zpool get -H -o value bootfs zroot)" = "$good" ] || \
       echo "ABORT: bootfs changed - one-shot would not revert"
   ```
   `bootfs` MUST still name the known-good environment. If it changed, restore
   it before rebooting.

8. **Reboot**, then **verify - this is the entire point:**
   - `bectl list`: which environment is active now?
   - `uname -v`, the kernel ident, or a checksum of `/boot/kernel/kernel`: is
     this the new build or the old one?
   - Exercise the artifact itself, not just its presence.
   - **Booted and healthy:** only now may you make it permanent, and only if
     that was the intent. Otherwise leave it one-shot; the next reboot returns
     to known-good by design.
   - **Failed:** the machine has already reverted. Confirm that it did rather
     than assuming, and report the failure with the boot log if you captured
     one.

## Guardrails

- Confirm which machine you are deploying to before rebooting it. Approval to
  deploy on one host does not extend to another.
- Keep the known-good environment until the candidate is proven. Do not destroy
  it to reclaim space.
- On a shared machine, coordinate before rebooting - someone else may have work
  in flight.
- **A hot-loaded module lives in RAM only.** A reboot silently reverts to
  whatever is on disk, so a result measured against a hot-loaded module says
  nothing about what the machine will run tomorrow.
- **Verify the identity of what is actually loaded before trusting any test
  result taken against it.** Checksum the file, check `kldstat -v`, and look for
  a symbol that the change under test introduces. A stale module invalidates
  every measurement made against it, and that failure mode reads exactly like a
  real defect.

## Related

- [bhyve-manager](../bhyve-manager/SKILL.md) - the isolated VM that kernel work belongs in
- [zfs-manager](../zfs-manager/SKILL.md) - boot environments are ZFS datasets
- [artifact-release](../../release/artifact-release/SKILL.md) - shipping the build once it is proven
