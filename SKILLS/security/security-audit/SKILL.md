# Security Audit Skill

## Metadata
```
author: Mark LaPointe <mark@cloudbsd.org>
version: 1.0.0
platform: CloudBSD / FreeBSD
triggers:
  - "security"
  - "audit"
  - "vulnerability"
  - "threat model"
  - "pen test"
  - "owasp"
  - "stride"
  - "CVE"
  - "exploit"
```

## Security Review Frameworks

### OWASP Top 10 (Web Application)
1. Broken Access Control
2. Cryptographic Failures
3. Injection
4. Insecure Design
5. Security Misconfiguration
6. Vulnerable Components
7. Auth Failures
8. Data Integrity Failures
9. Logging Failures
10. SSRF

### STRIDE Model (Threat Categories)
| Threat | What it violates | Common on FreeBSD |
|--------|------------------|-------------------|
| **S**poofing | Authentication | SSH keys, certificates |
| **T**ampering | Integrity | File permissions, ZFS snapshots |
| **R**epudiation | Non-repudiation | Audit logs, syslog |
| **I**nformation Disclosure | Confidentiality | File permissions, Jails |
| **D**enial of Service | Availability | Resource limits, firewall |
| **E**levation of Privilege | Authorization | sudo, setuid, Capsicum |

## Audit Protocol

### Phase 1: Asset Inventory
- Running services (`sockstat`, `ps aux`)
- Open ports (`netstat -an`)
- Installed packages (`pkg info`)
- Configuration files (`/etc`, `/usr/local/etc`)

### Phase 2: Threat Mapping (STRIDE)
For each asset:
1. Identify authentication mechanisms
2. Check file/object integrity controls
3. Verify audit logging
4. Assess data confidentiality
5. Evaluate DoS mitigations
6. Review privilege boundaries

### Phase 3: Vulnerability Check
- CVEs for installed packages (`pkg audit`)
- Default credentials
- Unencrypted services
- Outdated software
- Overly permissive firewall rules

### Phase 4: Report
Format:
```
## Finding: [Title]
**Severity**: Critical / High / Medium / Low
**STRIDE**: [Category]
**Asset**: [Affected component]
**Description**: [What the issue is]
**Impact**: [How it could be exploited]
**Recommendation**: [Concrete fix]
```

## FreeBSD-Specific Checks

| Check | Command |
|-------|---------|
| Package vulnerabilities | `pkg audit -F` |
| Open ports | `sockstat -4l` or `netstat -anp` |
| Firewall rules | `ipfw list`, `pfctl -sr` |
| File permissions | `find / -perm -4000` (setuid) |
| Jails isolation | `jls`, `jexec` isolation |
| Encrypted disks | `geli status`, `camcontrol` |
| SSL/TLS | `openssl s_client`, `certctl` |

## Hard Blocks

- Never suggest disabling security features as a "quick fix"
- Never propose storing credentials in plaintext
- Never recommend disabling ASLR or other hardening features

## Completion

- [ ] Asset inventory completed
- [ ] STRIDE threat mapping for each asset
- [ ] CVE scan performed (`pkg audit`)
- [ ] All findings documented with severity
- [ ] Recommendations are actionable and specific
