---
name: cloudflare-platform-dns
description: >-
  DNS record rules for CloudBSD domains on Cloudflare - dual-stack A and AAAA,
  when a record may be proxied and when it must not be, and how to verify.
  Reference material for the cloudflare-platform skill.
---

# DNS records on Cloudflare

Reference for [cloudflare-platform](SKILL.md). These are the rules that decide
whether a hostname works; the Cloudflare product map is in `SKILL.md`.

## Every hostname is dual-stack: an A record *and* an AAAA record

A hostname is not finished until it has **both** an `A` and an `AAAA` record and
**both have been observed to answer**. IPv4-only is not "done".

- **Read the real addresses off the machine** (`ifconfig`); never derive one from
  the other. IPv6 addresses do not follow the IPv4 pattern in any reliable way -
  an autoconfigured EUI-64 address has no relationship to the host's IPv4
  address, so a guessed AAAA will resolve and then fail to connect, which is
  worse than no record.
- **Verify from a machine that actually has the address family.** A failed
  `ping6` from a workstation with no IPv6 route proves nothing about the record.
  Test from a host with working IPv6 before concluding the target lacks it.
- If a dynamic DNS client maintains the record, configure it to maintain **both**
  families, not just IPv4.

## Proxied or DNS-only: get this right or the name silently breaks

Cloudflare's proxy - the orange cloud, `"proxied": true` - carries **HTTP and
HTTPS only**.

| Kind of hostname | Setting | Why |
|---|---|---|
| Web hostname | `proxied: true` | Cloudflare terminates TLS; the name resolves to Cloudflare addresses, not the origin |
| SSH, mail, or any non-HTTP service | `proxied: false` | A proxied record resolves fine and then refuses every connection |

A proxied record in front of SSH is the classic failure: DNS looks correct,
`dig` returns an answer, and nothing can connect. If a name is for a machine
people log in to, it is grey-cloud.

## A new web hostname needs both halves

Adding the DNS record is half the job. The origin web server must also
recognise the hostname - add it to `server_name` (both the redirect block and
the TLS block) and reload - and the origin certificate must cover the new name,
or the origin-facing connection fails depending on the zone's SSL mode. Check
the certificate's SANs and the zone's SSL setting before assuming it works.

## Do not fight a dynamic DNS client

If a dynamic DNS daemon owns a hostname, it will overwrite whatever you set by
hand, on its own schedule. Change it in the daemon's configuration, not in the
DNS API or dashboard. Records for names the daemon does not manage are safe to
edit directly.

## Credentials

The API token is a secret and follows CloudBSD configuration law: it lives in
the environment or a secrets store, never in a file in a repository, and never
in a configuration file that gets published. Use it on the machine that holds
it so it does not transit another host or land in a transcript, and never print
it. Operator-specific detail - which machine holds which token, and which zones
it is scoped to - is deployment information and does not belong in this public
repository.

## Verify, always

After any change, resolve the name for **both** families and confirm the answer
matches what you intended:

```sh
dig +short A    <name>
dig +short AAAA <name>
```

Then read the record back from the API. A record that was created successfully
and points somewhere wrong looks identical to success until someone tries to
use it.
