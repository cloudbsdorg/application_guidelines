---
name: secure-coding
description: >-
  Code-level defences against the bug classes that turn untrusted input into
  a vulnerability, with the safe pattern and the trap in C, Java, Python,
  TypeScript and Go, and the FreeBSD and OpenBSD hardening APIs we adopt. Use
  while writing or reviewing code that parses input, builds paths or
  commands, allocates from a size it was given, extracts archives, compares
  secrets, logs, handles credentials, runs SQL, fetches URLs, deserializes,
  creates temporary files or generates tokens.
keywords:
  - secure coding
  - CWE
  - path traversal
  - command injection
  - integer overflow
  - out-of-bounds read
  - archive extraction
  - secrets in logs
  - SQL injection
  - SSRF
  - deserialization
  - format string
  - temporary file
  - random token
  - timing attack
  - Capsicum
  - pledge
  - unveil
---

# Secure coding

<!-- Copyright (c) 2026 REVYTECH, Inc. SPDX-License-Identifier: BSD-3-Clause -->

This skill is the code level. Every check fails closed: it has three
outcomes, pass, fail and could not look, and "could not look" is a fail. The
review frameworks (OWASP, STRIDE) are in
[security-audit](../security-audit/SKILL.md). The general per-language traps
(comparators, recursion depth, hash flooding) are in
[language-idioms](../../quality/language-idioms/SKILL.md). Rows below that
overlap with it (overflow, bounds) are here only for the form in which they
become a vulnerability.

**Scanners do not replace this.** Run the project's static scanners (for
example semgrep, bandit, gitleaks) on every change, but a missing or
mis-matching rule is silent. This skill is for writing the code right the
first time, and for the cases no rule sees.

## Bug classes

Each row: the rule, then the trap in the language where it bites. The CWE
links go to MITRE's definitions.

| Class | Rule | Traps |
|---|---|---|
| Path traversal ([CWE-22](https://cwe.mitre.org/data/definitions/22.html)) | Open the untrusted path relative to an open directory descriptor, and let the kernel refuse escapes. Lexical checks (`..`, `normalize`, prefix compare) miss symlinks. | C on FreeBSD: `openat(dirfd, p, O_RESOLVE_BENEATH)`; on Linux: `openat2` with `RESOLVE_BENEATH`. Go 1.24+: `os.Root`. Python: `os.path.join(base, "/etc")` returns `/etc`; open each component with `os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_DIRECTORY, dir_fd=fd)`, starting from the base directory's descriptor, and refuse `..`; resolving the path and then opening it by name is a race. Java: `normalize()` is lexical; use `SecureDirectoryStream`, which opens relative to a directory. TypeScript (Node): `path.resolve` and `path.relative` are lexical, and Node has no descriptor-relative open. Do file access with untrusted paths in a helper that opens beneath a descriptor, or do not accept untrusted paths in Node at all; a `fs.realpathSync` check followed by an open is a race. |
| Symlink following, TOCTOU ([CWE-59](https://cwe.mitre.org/data/definitions/59.html), [CWE-367](https://cwe.mitre.org/data/definitions/367.html)) | Check and use the same object: open it once, then act on the descriptor. | `stat` then `open` is a race. Open with `O_NOFOLLOW` (and `O_CREAT|O_EXCL` for new files), then `fstat` the descriptor. |
| Archive extraction ([CWE-22](https://cwe.mitre.org/data/definitions/22.html)) | Refuse members by type and target before extraction, and extract with the library's safe filter. | Python: before 3.14, `tarfile.extractall` defaults to trusting the archive (symlinks and absolute paths); pass `filter="data"` explicitly, and never `filter="fully_trusted"` on untrusted input. libarchive (`tar -x`) refuses `..` and writing through a symlink, but still creates a symlink member that points outside (measured on FreeBSD). Count only regular files, by `lstat`. |
| Integer overflow before allocation ([CWE-190](https://cwe.mitre.org/data/definitions/190.html), [CWE-680](https://cwe.mitre.org/data/definitions/680.html)) | Compute `count * size + header` with overflow checks, and refuse on overflow. | C: `malloc(n * size)` wraps; use `reallocarray(NULL, n, size)` or `__builtin_mul_overflow`. Java: `int` arithmetic wraps silently; use `Math.multiplyExact`. Go: integers wrap; check before `make`. |
| Out-of-bounds read or write ([CWE-125](https://cwe.mitre.org/data/definitions/125.html), [CWE-787](https://cwe.mitre.org/data/definitions/787.html)) | Never trust a length field: check it against the bytes you actually have, before you use it. | C: test with ASan and UBSan, and fuzz the parser (see [oracle-and-property-tests](../../testing/oracle-and-property-tests/SKILL.md)). `strncpy` does not terminate; use `strlcpy`. Go and Java slices panic or throw, which is still a denial of service if it is not caught at the boundary. TypeScript: `Buffer.readUInt32BE(off)` throws past the end, but `buf.subarray(a, b)` silently clamps; check the length first. |
| OS command injection ([CWE-78](https://cwe.mitre.org/data/definitions/78.html)) | Run programs with an argument vector. Never build a shell string from input. | Python: `subprocess.run([...])`, never `shell=True`. Go: `exec.Command(name, args...)`. Node: `execFile`, not `exec`. Shell: quote every expansion, and put `--` before untrusted arguments, which may start with `-`. |
| SQL injection ([CWE-89](https://cwe.mitre.org/data/definitions/89.html)) | Bind parameters, or go through the project's ORM or query builder. | Building `WHERE` clauses with string formatting, including for "trusted" values. |
| Encoding validation ([CWE-176](https://cwe.mitre.org/data/definitions/176.html)) | Validate strictly at the boundary, then compare in one canonical form. | Overlong UTF-8 and surrogates must be refused. Python `decode(errors="replace")` hides bad input; use `errors="strict"` at a security boundary. TypeScript: `new TextDecoder()` replaces bad bytes; use `new TextDecoder("utf-8", { fatal: true })`. |
| Allowlist and SSRF bypass ([CWE-918](https://cwe.mitre.org/data/definitions/918.html)) | Parse the address with the standard library, normalize it, then match. Never match text. | IPv4-mapped IPv6 (`::ffff:10.0.0.1`) bypasses an IPv4-only deny list. Go: `netip.Addr.Unmap()`. Python: `a = ipaddress.ip_address(x)`, then `if a.version == 6 and a.ipv4_mapped: a = a.ipv4_mapped`. TypeScript: normalize `::ffff:` addresses before matching, for example with Node's `net.BlockList`, which checks both families. Check the address you connect to, not the name you resolved earlier (DNS can change between the two). |
| Secrets in logs ([CWE-532](https://cwe.mitre.org/data/definitions/532.html)) | Keep secrets in types or fields the logger redacts. Never format a request, header map or config struct whole. | Logging `err` from an HTTP client that includes the URL with a token. Printing `os.environ`. A bearer header in a debug dump. |
| Resource consumption ([CWE-400](https://cwe.mitre.org/data/definitions/400.html), [CWE-409](https://cwe.mitre.org/data/definitions/409.html)) | Bound every read, decompression, recursion and collection that untrusted input can grow, and give every network call a deadline. | `io.ReadAll` on a request body. Decompressing without an output cap. A recursive parser on nested input. |
| Insecure temporary files ([CWE-377](https://cwe.mitre.org/data/definitions/377.html)) | Create with `mkstemp` or `mkdtemp` (or the language's wrapper), in a private directory. | A fixed name under `/tmp`. Python `tempfile.mktemp`. |
| Weak randomness ([CWE-338](https://cwe.mitre.org/data/definitions/338.html)) | Tokens, keys and nonces come from the system CSPRNG. | C: `rand()`; use `arc4random_buf` or `getrandom`. Python: `random`; use `secrets`. Go: `math/rand`; use `crypto/rand`. TypeScript: `Math.random`; use `crypto.randomBytes`, `crypto.randomUUID` or `crypto.getRandomValues`. |
| Timing comparison of secrets ([CWE-208](https://cwe.mitre.org/data/definitions/208.html)) | Compare MACs, tokens and password hashes in constant time. This is a review rule: timing tests are not reliable on shared hosts. | C: `timingsafe_bcmp`. Go: `crypto/subtle.ConstantTimeCompare`. Python: `hmac.compare_digest`. Java: `MessageDigest.isEqual`. TypeScript: `crypto.timingSafeEqual` (lengths must match first). |
| Deserialization of untrusted data ([CWE-502](https://cwe.mitre.org/data/definitions/502.html)) | Parse untrusted input only into plain data (JSON into a typed struct), never into objects that run code. | Python `pickle`, `yaml.load` without `SafeLoader`; Java `ObjectInputStream`. TypeScript: `JSON.parse` into `any`; validate against a schema before use, and refuse `__proto__` keys when merging. |
| Format strings ([CWE-134](https://cwe.mitre.org/data/definitions/134.html)) | The format is always a literal. | C: `printf(msg)`; write `printf("%s", msg)`. Build with `-Wformat=2 -Werror=format-security`. |

## Hardening APIs we adopt

These are from the upstream projects. Each FreeBSD function and flag below
compiled and behaved as expected on FreeBSD 16-CURRENT (2026-11-05).

- **FreeBSD and OpenBSD libc:** `strlcpy` and `strlcat`, `reallocarray`,
  `explicit_bzero` (clears a secret so the compiler cannot drop it),
  `arc4random_buf` and `arc4random_uniform`, and `timingsafe_bcmp`. glibc has
  most of them in recent versions; check the target before using them in
  portable code.
- **FreeBSD only:** `openat(dirfd, p, O_RESOLVE_BENEATH)`. OpenBSD has no
  such flag; there, confine the process with `unveil` instead. Linux has
  `openat2` with `RESOLVE_BENEATH`.
- **FreeBSD Capsicum:** open what the program needs, limit each descriptor
  with `cap_rights_limit`, then call `cap_enter`. After that, the process
  cannot open new paths or sockets by name. Use `libcasper` for DNS and
  similar services a sandboxed process still needs.
- **OpenBSD `pledge` and `unveil`:** the same idea as Capsicum, by promise
  set and path list. Our OpenBSD template uses them where it ships programs.
- **Build flags:** `-fstack-protector-strong`, `-D_FORTIFY_SOURCE=2` (needs
  optimization), PIE, RELRO and `-Wformat=2`. FreeBSD's base build sets
  most of these; ports and our own Makefiles must not drop them.

## Checklist

- [ ] Every untrusted length, count, size and index is checked against what
      is actually there before use.
- [ ] Paths from input are opened beneath a directory descriptor, never
      checked by name and then reopened.
- [ ] Archives are filtered by member type and target before extraction.
- [ ] No shell string is built from input; every external program runs from
      an argument vector.
- [ ] Every read, decompression and network call that input can grow has a
      bound and a deadline.
- [ ] No secret can reach a log, an error message or a URL.
- [ ] Secrets are compared in constant time and created from the CSPRNG.
- [ ] SQL binds parameters; untrusted data is never deserialized into
      objects; format strings are literals; temporary files come from
      `mkstemp` or its wrapper.
- [ ] Allowlists match parsed, normalized addresses (IPv4-mapped IPv6
      included), not text.
- [ ] C code builds clean with ASan and UBSan, and its parsers are fuzzed.

## Related

- [language-idioms](../../quality/language-idioms/SKILL.md): per-language
  traps for algorithms.
- [oracle-and-property-tests](../../testing/oracle-and-property-tests/SKILL.md):
  sanitizers, fuzzing and hostile inputs as tests.
- [security-audit](../security-audit/SKILL.md): review frameworks and the
  FreeBSD host checks.
