---
name: artifact-release
description: >-
  Build, verify, and publish binary artifacts - packages, kernels and modules,
  install media, VM images - so that what ships is what was tested. Use when
  cutting a release, producing installable media, publishing a package
  repository, or deciding whether an artifact is fit to publish. Complements
  the ship skill, which gates the change; this gates the artifact.
keywords:
  - release
  - package
  - pkgbase
  - install media
  - ISO
  - VM image
  - publish
  - repository catalog
  - build stamp
---

# Building and publishing artifacts

Every rule below is here because skipping it once shipped something broken.
[ship](../../workflow/ship/SKILL.md) covers the change - tests, review, deploy.
This covers the artifact: what was built, from what, and whether it works when
somebody else installs it.

## 1. Build only from committed source

- **Commit before building.** Build from a clean checkout, or a `git worktree`
  cut from the commit you intend to ship. Never build from a tree with
  uncommitted edits and then publish the result.
- **Do not let the builder's tree drift.** Verify by checksum that the builder's
  files match the commit. A shipped module was once unloadable at the customer's
  end - undefined symbol - because the builder's tree still carried debug
  counters that were referenced but never defined, and the commit did not.
- **Never edit upstream files to inject branding.** Package prefixes,
  maintainer, and homepage go through the environment, the command line, or a
  `SRCCONF`. Files inherited from upstream must stay byte-identical to upstream,
  or the next merge is a conflict and the provenance is a lie.

## 2. Keep the build stamp neutral

The build system bakes `user@host` into the kernel version string and the loader
banner. Override it to something neutral before shipping. After building, grep
the artifacts - `strings` on the kernel, the media, the packages - and confirm
no internal hostname, no IP address, and no `/home/<user>` path is embedded in
anything published.

## 3. Verify what you are about to ship, not what you hope you built

- **A module that loads proves nothing about the userland that drives it.** One
  project shipped several consecutive releases whose command-line tool could not
  start anything at all, because the ship check only confirmed the kernel module
  loaded. From the **installed package**, on a **clean machine**, run the tool
  and complete a real operation end to end.
- **Install the full package payload, not just the binary directory.** A tool
  that also ships a private shared library will not run without it.
- **Check for undefined symbols** in any module before packaging it.
- **Checksum the artifact you tested and confirm the packaged one matches.**
  If they differ, you tested something else.

## 4. Regression-test every supported target

- Test on **every architecture you claim to support**. One codebase means a fix
  on one must not regress another, and only running it proves that.
- Watch for interface-version mismatches: a module built against one kernel
  version can be refused by a host at a different one. Match them deliberately
  rather than discovering it at install time.
- If the change touches a deeper layer than your usual smoke test reaches, test
  that layer too. A shallow test once let a deeper regression ship.

## 5. Publish a repository that actually resolves

- **Generate the catalog.** A package directory without its repository metadata
  returns 404s and the client install fails. This has shipped broken.
- Point installed systems at the repository through their own configuration
  file, leaving the upstream configuration intact.
- **Preserve the previous version** as a rollback target. Do not overwrite it
  with the new one.
- Record, for every artifact: wire size, uncompressed size, checksum, and the
  CPU, memory, and disk it needs. The download page needs all of it.

## 6. Boot-verify every artifact type separately

An ISO, a memstick image, and a VM image are three different boot paths, and
they fail independently:

- **ISO** - reaches the installer.
- **Memstick** - attached as a raw disk to a throwaway VM, reaches the installer.
- **VM image** - boots to multi-user and a login prompt.

Then confirm on the booted system that the version stamp is the neutral one,
the feature you shipped is present, and the package client can reach your
repository.

**Never publish an artifact that has not booted.** Publishing a verified subset
is fine - say which ones passed and which were not tested.

## 7. Publish-time hygiene

- Verify the public URLs return 200, and that a range request returns 206 so
  downloads resume.
- Install from the **public URL** into a throwaway stock machine, reboot, and
  confirm it comes up. That is the only test that covers the whole path.
- Carry any experimental or not-for-production warning on both the download page
  and the installer, where somebody will actually read it.

## Related

- [ship](../../workflow/ship/SKILL.md) - the change-level gate
- [safe-kernel-deploy](../../freebsd-admin/safe-kernel-deploy/SKILL.md) - booting an unproven build safely
- [pre-publish-review](../../platform/opencode/pre-publish-review/SKILL.md) - a heavier review gate for npm publishes
- `Unit-Testing/UNITTESTS.md` - the evidence requirement these checks satisfy
