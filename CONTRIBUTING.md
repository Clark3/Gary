# Contributing to Gary

Thanks for helping improve Gary.

Before opening a change, read `PROJECT_SPEC.md`, `docs/SECURITY.md`, and `agent/OPERATING_RULES.md`.

Prefer small, reviewable changes. Keep host-specific behavior inside adapters or explicit host records. Do not add secrets, model weights, container images, caches, or transient state. Do not weaken the privilege/approval boundary for convenience. Add or update tests when behavior changes and update documentation when architecture or user-visible behavior changes.

Pull requests should describe the problem, proposed change, tests, security/privilege implications, and rollback considerations.
