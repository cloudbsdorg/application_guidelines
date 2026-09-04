# Programming Languages Guidelines for CloudBSD Applications

This document outlines the recommended programming languages for developing CloudBSD applications and the criteria for selecting them.

## 1. Recommended Languages

### C
- **Use Case**: Low-level system tools, kernel components, and performance-critical utilities.
- **Why**: Native to FreeBSD/CloudBSD, minimal overhead, and direct access to system APIs.

### C++
- **Use Case**: Complex system services and performance-oriented applications with modern abstractions.
- **Why**: Powerful standard library and strong typing, while maintaining high performance.

### Rust
- **Use Case**: Modern system programming where memory safety is a priority.
- **Why**: Memory safety without a garbage collector, excellent package management (Cargo), and high performance.

### Go
- **Use Case**: Network services, distributed systems, application backends, and modern TUI/Web-integrated tools. A CloudBSD product with an Angular UI still uses Go (or another systems language from this list) for the backend.
- **Why**: Built-in concurrency support (goroutines), fast compilation, and simple deployment (static binaries). Choosing Angular for the view does not move the controller or domain into Node or TypeScript.

### Python
- **Use Case**: Automation scripts, non-critical management tools, and high-level application logic.
- **Why**: Excellent readability, vast ecosystem of libraries, and rapid development speed.

### JavaScript / TypeScript
- **Use Case**: Web-based user interfaces only. **Angular** (TypeScript) is the CloudBSD web UI framework. It is not the application backend.
- **Why**: TypeScript provides type safety for large-scale frontends; Angular is the standard application framework. React is not the CloudBSD standard.

## 2. Selection Criteria

When choosing a language for a new CloudBSD application, consider the following:
- **Performance Requirements**: Does the application need to be ultra-fast or have low latency?
- **Safety**: How critical is memory safety and type safety for this specific task?
- **Maintainability**: Is the language widely understood by the development community?
- **System Integration**: How easily does the language interface with FreeBSD/CloudBSD system calls?

## 3. Documentation

Every CloudBSD application that ships a binary or an rc.d service MUST include mandoc mdoc man pages: section 8 (or section 1 for user commands) for the program, section 5 for the configuration file. Document flags, JSON keys, signals (SIGHUP reload), files, rc.d names, and examples. Prefer man pages over README-only docs. See `Configuration-Files/CONFIGURATION.md`.

