# Privileged Action Policy

## Approval required

The following require explicit user approval before host execution:

- `sudo` operations outside a narrowly documented safe allowlist
- package installation/removal when not explicitly requested
- edits to `/etc`, boot files, firewall rules, or core networking configuration
- partitioning and filesystem operations
- bootloader changes
- firmware / BIOS / UEFI updates
- raw block-device or device-node operations
- destructive deletion
- changing authentication/authorization policy
- repository pushes or destructive Git history changes

## Safe baseline examples

Generally safe without escalation: read-only diagnostics, status queries, file inspection inside the Gary workspace, package metadata queries, and harmless tests/capability probes.

For an approval-gated operation, Gary should communicate what will change, why, expected impact, rehearsal status, rollback/recovery path, exact privilege required, and verification plan.
