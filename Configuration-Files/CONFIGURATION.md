# Configuration Guidelines for CloudBSD Applications

This document outlines the standard practices for configuration management in CloudBSD applications to ensure consistency and ease of administration.

All applications should follow these guidelines to ensure a consistent and reliable configuration experience.
The target platform is FreeBSD, CloudBSD is built on top of FreeBSD.

## 1. Storage Standards

### XDG Base Directory Specification
Applications should follow the [XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html) whenever possible:
- **Configuration files**: `$XDG_CONFIG_HOME/appname/` (defaults to `~/.config/appname/`)
- **Data files**: `$XDG_DATA_HOME/appname/` (defaults to `~/.local/share/appname/`)
- **Cache files**: `$XDG_CACHE_HOME/appname/` (defaults to `~/.cache/appname/`)

### System-Wide Configuration
For system-wide defaults:
- Primary location: `/usr/local/etc/cloudbsd/appname/`

## 2. Configuration File Formats

**JSON is the only configuration format** for CloudBSD applications.

- File extension: `.json`. Encoding: UTF-8. Syntax: strict JSON (RFC 8259).
- No comments, no trailing commas, no JSONC, no `$comment` keys or other dialects.
- Ship `config.example.json`. Install `config.json.sample`. Document every key in the **section 5 man page**, not inside the JSON file. README may point at the man page; it is not a substitute.
- `appname init` (or equivalent) must emit valid JSON.

### Escape hatch

Use a different format **only when JSON cannot represent the configuration at all**. Wanting comments, familiarity with TOML/YAML, or editor highlighting is not a reason.

If you take the hatch:

1. Record in the application's README what JSON could not express.
2. Use one alternate format for the whole application. Do not mix JSON and the alternate in the same app.
3. Prefer a format already common on FreeBSD (UCL, then TOML) when an alternate is required.

Human-edited files are still JSON when JSON works. Secrets still belong in environment variables, not in the file.

## 3. Best Practices

### Service Management
- **Service Management**: Create rc.d init scripts for services that need to be managed by the system. This ensures that services can be started, stopped, and restarted using standard system tools.
- Make sure the pidfile is created in the correct location and is owned by the correct user, and removed when the service stops. This file should not have any negative values, nor be empty.

### Validation
- **Dry-run mode**: Applications should support a `--check-config` or `--dry-run` flag to validate the configuration file without starting the service.
- **Strict Parsing**: Reject invalid configurations with clear, actionable error messages and non-zero exit codes.

### Evidence (LAW)

Config, rc.d, CLI, and man-page work is not complete until there is captured evidence:

- `--check-config` / `--dry-run`: valid config exits 0; invalid config exits non-zero with an actionable message. Capture stdout/stderr.
- Service reload: SIGHUP / `service name reload`; bad config keeps the old process; good config is applied. Capture command output.
- CLI: capture command output for the flags you claim to have implemented.
- Man pages: `mandoc -T lint` (or equivalent) must pass on every shipped page. Capture the lint output.

If a required tool is not installed, find one or make one. Skipping because a tool is missing is a defect.
Store evidence with the change (CI artifacts, testdata, or a clearly named report path). "I ran it" without output is not evidence.

### Defaults
- **Safe Defaults**: Applications should have sensible, safe default values that allow them to run out-of-the-box when minimal configuration is provided.
- **Template Generation**: Provide an example JSON configuration file or a command to generate one (e.g., `appname init`).
- **Privileged Resources**: Ensure that configuration files do not grant excessive privileges to users or processes. Create a user for the application to run as once privileged resources are obtained. For example a web server needs root privileges to bind to port 80, but we can get the port and drop to the application user that was created to isolate the application.

### Security
- **Permissions**: Ensure configuration files containing secrets (like API keys or passwords) are created with restricted permissions (e.g., `0600`).
- **Environment Variables**: Allow sensitive configuration values to be set via environment variables to avoid storing secrets in plain text files.
- **Encryption**: Consider encrypting sensitive configuration files at rest using industry-standard encryption algorithms (e.g., AES-256) and secure key management practices.
- **Access Control**: Ensure that configuration files are only accessible by authorized users and processes, and that access is logged for auditing purposes.

### Observability
- **Log Level**: Always include a configuration option for log levels (DEBUG, INFO, WARN, ERROR).
- **Reloading**: Long-running services must soft-reload configuration in place, nginx-style (`nginx -s reload`):
  - Validate the new config first (`--check-config` or `--dry-run`).
  - If valid, apply it without exiting the process (`SIGHUP` / `service name reload`).
  - If validation fails, keep serving with the old config. Reload is a no-op failure, not a crash or restart.
  - In-flight work finishes; new work uses the new config.
  - Restart remains allowed for changes that cannot be applied live (binary upgrade, listen-address bind that cannot be swapped, and similar). Reload is the default for config.
- **Monitoring**: Applications should provide metrics and health checks to monitor their health and performance.
- **Logging**: All log events should be made into an event object and sent to a logging service if possible, a file or database.
- **Event Aggregation**: Implement a mechanism to aggregate and normalize log events for easier analysis and correlation.

## 4. Manual Pages (mandoc mdoc) — LAW

Every CloudBSD application that ships a **binary** or an **rc.d service** MUST include [mandoc](https://mandoc.bsd.lv/) **mdoc** man pages.

- **Section 8** for daemons and administrative programs. **Section 1** for user commands.
- **Section 5** for the configuration file.
- Write **mdoc** macros, not groff-man, not Markdown-as-man.
- **`mandoc -T lint` (or equivalent) must pass** on every shipped page. Capture the lint output as evidence. A man page that was not linted is a defect.
- Document: command-line flags (including `doctor` and `--check-config`), JSON keys (including resource-headroom thresholds), signals (including **SIGHUP reload**: validate then reload, bad config keeps the old process), files and directories (XDG and `/usr/local/etc/cloudbsd/appname/`), rc.d names, and examples.
- Prefer man pages over stuffing documentation only in README. README may link to the man pages.
- Install with the package (`share/man/man8/`, `share/man/man5/`, or the section-1 equivalent).

See also `Languages/LANGUAGES.md` (Documentation).


## 5. `doctor` and recovery (LAW)

Every long-running CloudBSD service MUST ship a `doctor` command (or equivalent subcommand).

Doctor MUST:
- Check config (same rules as `--check-config` / `--dry-run`).
- Check permissions (config files, pidfile directory, data dirs, `0600` where secrets live).
- Check pidfiles (present when running, owned by the service user, not empty, not negative).
- Check dependencies (required binaries, sockets, stores).
- Check resource headroom (see Section 6). Doctor **reports all** finite resources even when a given job will not consume them.
- Print evidence in **human-readable form and JSON**.
- Exit **non-zero if unhealthy**.

If the service has operator state to repair, it MUST also ship a **recovery console**.
Recovery is operator-only (CLI or TUI). It is **not a public UI** and must not be reachable as an unauthenticated web page.
See `TUI/TUI.md`.

Document `doctor` and recovery in the section 8 (or 1) man page. Capture doctor JSON/human output as evidence for the change.
## 6. Resource headroom (LAW)

Headroom is **consumption-based**, not a blanket host checklist.

Services that provision work MUST monitor the finite resources **that operation will consume**
(RAM, CPU, disk, GPU/VRAM as applicable) and MUST NOT start or provision when there is no
headroom for those resources.

- If a job will not use disk or GPU, disk/GPU **must not block** it.
- Doctor still **reports all** finite resources (present, missing, used, free).
- Missing optional devices (no GPU) is OK.
- Exhausted **required** resources for that operation is a fail: do not start or provision.
- Thresholds live in the JSON config (RFC 8259). Document every key in the section 5 man page.

Example keys (names may vary; JSON only): `resources.ram_min_free_bytes`, `resources.cpu_max_pct`,
`resources.disk_min_free_bytes`, `resources.gpu_vram_min_free_bytes`. Omit or null a threshold
when that resource is not consumed by the operation.
