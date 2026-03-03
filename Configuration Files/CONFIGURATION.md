

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

- **JSON**: Best for machine-to-machine interfaces; avoid for manual user editing due to lack of comments.
 JSON is widely supported by most programming languages and can be easily parsed by most tools, that is why we recommend it for configuration files. 
- It provides a clear and consistent format that is easy to read and write, making it ideal for both humans and machines.

## 3. Best Practices

### Service Management
- **Service Management**: Create rc.d init scripts for services that need to be managed by the system. This ensures that services can be started, stopped, and restarted using standard system tools.
- Make sure the pidfile is created in the correct location and is owned by the correct user, and removed when the service stops. This file should not have any negative values, nor be empty. 

### Validation
- **Dry-run mode**: Applications should support a `--check-config` or `--dry-run` flag to validate the configuration file without starting the service.
- **Strict Parsing**: Reject invalid configurations with clear, actionable error messages and non-zero exit codes.

### Defaults
- **Safe Defaults**: Applications should have sensible, safe default values that allow them to run out-of-the-box when minimal configuration is provided.
- **Template Generation**: Provide a commented example configuration file or a command to generate one (e.g., `appname init`).
- **Privileged Resources**: Ensure that configuration files do not grant excessive privileges to users or processes. Create a user for the application to run as once privileged resources are obtained. For example a web server needs root privileges to bind to port 80, but we can get the port and drop to the application user that was created to isolate the application.
- 

### Security
- **Permissions**: Ensure configuration files containing secrets (like API keys or passwords) are created with restricted permissions (e.g., `0600`).
- **Environment Variables**: Allow sensitive configuration values to be set via environment variables to avoid storing secrets in plain text files.
- **Encryption**: Consider encrypting sensitive configuration files at rest using industry-standard encryption algorithms (e.g., AES-256) and secure key management practices.
- **Access Control**: Ensure that configuration files are only accessible by authorized users and processes, and that access is logged for auditing purposes.


### Observability
- **Log Level**: Always include a configuration option for log levels (DEBUG, INFO, WARN, ERROR).
- **Reloading**: Long-running services should support configuration reloading without restart (e.g., via `SIGHUP`).
- **Monitoring**: Applications should provide metrics and health checks to monitor their health and performance.
- **Logging**: All log events should be made into an event object and sent to a logging service if possible, a file or database.
- **Event Aggregation**: Implement a mechanism to aggregate and normalize log events for easier analysis and correlation.