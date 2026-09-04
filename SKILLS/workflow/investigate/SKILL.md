---
name: investigate
description: >-
  Find the root cause of a broken system using an evidence-based protocol
  rather than guesswork. Use when debugging a failure, when asked why
  something is broken, when tracing an error, and specifically when the
  obvious explanation has already turned out to be wrong.
---

# Investigation Skill


## Iron Law (MANDATORY)

> **"No fix without investigation. No assumption without evidence."**

Every debugging session starts with evidence collection. You MUST investigate before proposing fixes.

## Investigation Protocol

### Phase 1: Gather Evidence

1. **Reproduce** - Can you observe the failure yourself?
2. **Scope** - When did it start? What changed? What still works?
3. **Logs** - Extract relevant log entries (timestamps, error codes)
4. **Environment** - FreeBSD version, packages installed, config files
5. **State** - Running processes (ps), open files (lsof), network connections (sockstat)

### Phase 2: Generate Hypotheses

Form testable hypotheses:
- Hypothesis A: Cause X → predicts observation Y
- Hypothesis B: Cause Z → predicts observation Y
- Only one needs to be true

### Phase 3: Test Rigorously

For each hypothesis:
1. State what you expect to observe
2. Run the test
3. Compare actual vs expected
4. Eliminate or confirm

### Phase 4: Root Cause

Once confirmed:
- State the root cause clearly
- Confirm the fix addresses the cause (not symptoms)
- Verify fix doesn't introduce new failures

## FreeBSD-Specific Tools

| Situation | Command |
|-----------|---------|
| Process state | `ps auxwww`, `ps -p $pid -j` |
| File handles | `lsof -p $pid`, `fstat` |
| Network | `sockstat`, `netstat -an` |
| Kernel | `sysctl -a`, `dmesg` |
| Jails | `jls`, `jexec` |
| Services | `service $name status`, `rcctl` |
| Logs | `/var/log/messages`, `/var/log/$service` |

## Anti-Patterns (BLOCKING)

- **Guessing** - "I think it's probably X" → MUST test
- **Symptom fixing** - Treating headache instead of finding brain tumor
- **Shotgun debugging** - Random changes hoping something works
- **Single evidence** - One symptom is not enough

## Example Investigation

```
User: "Service won't start after reboot"

You:
1. Gather: Check `service $name status`, `rcctl ls all`, /var/log/rc.log
2. Hypothesis: Service not in /etc/rc.conf OR dependency failed
3. Test: `grep $service /etc/rc.conf`, `rcorder /etc/rc.d/*`
4. Root cause: Missing $service_enable="YES" in rc.conf
5. Fix: Add rc.conf entry, verify `service $name start` works
```

## Completion Checklist

- [ ] Evidence gathered (logs, commands, state)
- [ ] At least 2 hypotheses generated
- [ ] Each hypothesis tested with actual commands
- [ ] Root cause stated explicitly
- [ ] Fix verified to address cause
