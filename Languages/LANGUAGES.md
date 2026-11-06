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

### Shell scripts: zsh
- **Use Case**: Glue scripts, test drivers, build and deploy helpers -- anything written as a shell script where no particular shell is required.
- **Why**: One shell everywhere is easier to read and review than a mix of sh, bash and zsh dialects, and zsh is on every machine we use (`/usr/bin/zsh` on Linux, `/usr/local/bin/zsh` from the FreeBSD package).

**This rule is about shell scripts only.** It turns sh and bash scripts into zsh scripts. It never applies to any other language: a TypeScript, Python, Go, C or other program is not converted to zsh, and a program is not rewritten as a shell script.

**Convert lazily, on the spot.** There is no mass conversion. Write every new shell script in zsh. When a change touches an existing sh or bash script, and that script does not need its shell, convert it to zsh in the same change. Behaviour must stay the same, and the script's tests run under zsh before the change is committed. A script nobody touches stays as it is.

**When the shell is a requirement, keep it.** These stay `/bin/sh`, or whatever shell they are written for:
- rc.d scripts and anything sourced by rc.subr(8);
- the installer, and pkg install and deinstall scripts;
- anything that runs at boot, in single-user mode, or before packages are installed, because zsh is a package and is not there yet;
- scripts in the base system or a base overlay;
- upstream trees (FreeBSD src and ports, vendored code): they stay as upstream wrote them, so they still sync.

A script whose shell is fixed by an outside contract stays too: a Makefile recipe, a hook that another tool runs with `sh -c`, a CI step whose runner chooses the shell.

**Writing zsh (zsh 5.9 or later):**
- A new script starts with this preamble, in this order. `emulate` resets every option, so a `setopt` placed before it is lost:

      #!/usr/bin/env zsh
      emulate -L zsh
      setopt err_exit no_unset pipe_fail

  The shebang uses `env` because zsh is in `/usr/bin` on Linux and `/usr/local/bin` on FreeBSD. A script run where `PATH` may lack `/usr/local/bin` (a user crontab, a service, `at`) sets `PATH` or names the interpreter by its absolute path. `no_unset` makes an unset parameter an error, and `pipe_fail` makes a pipeline fail when any stage fails. Where an empty value is legitimate, write `${var:-}`.
- A converted script keeps the strictness it had. Use `emulate -L zsh`, then turn on exactly the strictness the old script had, in whatever form it used (`set -e`, `set -euo pipefail`, `set -o errexit`, or flags on the `#!` line): `err_exit` for `-e`, `no_unset` for `-u`, `pipe_fail` for `pipefail`. Adding any of them changes when the script stops, so that is a separate, deliberate change.

**Converting from sh or bash:** these are the differences that silently change behaviour.
- **Word splitting:** zsh does not split unquoted `$var` on spaces. Where the old script relied on splitting, use `${=var}` (`${=var:-}` under `no_unset`) or an array.
- **Arrays** start at 1, not 0.
- **Globs:** a glob that matches nothing is an error (`NOMATCH`). Add the `(N)` qualifier to the pattern itself, as in `*.log(N)`, where an empty match is fine.
- **`**`** is recursive in zsh. Without `globstar`, bash reads `**/*.c` as `*/*.c`, so a converted script starts matching files in every subdirectory.
- **Braces:** zsh expands an unquoted `{a,b}`; plain sh does not. A script that came from `/bin/sh` and has literal braces needs quoting.
- **Pipelines:** the last stage runs in the current shell, so a variable set in a piped `while read` loop keeps its value after the loop, where sh and bash lost it. Check every variable set inside such a loop and used after it.
- **Echo:** `echo` interprets backslashes. Use `print -r --`, or `printf '%s\n'`, which prints the trailing newline that echo adds.
- **This list is not complete.** Re-read every line of a converted script.
- **Run it:** run the converted script under zsh on both Linux and FreeBSD, because a successful `zsh -n` syntax check alone proves nothing about behaviour.

## 2. Selection Criteria

When choosing a language for a new CloudBSD application, consider the following:
- **Performance Requirements**: Does the application need to be ultra-fast or have low latency?
- **Safety**: How critical is memory safety and type safety for this specific task?
- **Maintainability**: Is the language widely understood by the development community?
- **System Integration**: How easily does the language interface with FreeBSD/CloudBSD system calls?

## 3. Documentation

Every CloudBSD application that ships a binary or an rc.d service MUST include mandoc mdoc man pages: section 8 (or section 1 for user commands) for the program, section 5 for the configuration file. Document flags, JSON keys, signals (SIGHUP reload), files, rc.d names, and examples. Prefer man pages over README-only docs. See `Configuration-Files/CONFIGURATION.md`.

