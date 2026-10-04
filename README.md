# Gary

> Your local Linux system administrator, engineer, and boss.
>
> **For the love of it, not the money.**

Gary is a portable, local-first Linux system-administration agent. The portable Git repository is Gary's durable backbone: identity, policy, knowledge, host records, incident history, bootstrap logic, tests, and maintenance instructions. Heavy runtime components and model weights stay on the host and are started only when needed.

## What Gary is

**Gary** is the whole system and identity. Roles are operating modes:

- **Admin** — day-to-day host administration: inspect, diagnose, research, rehearse, repair, verify, and record.
- **Engineer** — maintains Gary itself: repository, bootstrap, runtimes, adapters, tests, documentation, portability, and scheduled maintenance.

Changing the underlying LLM does **not** change Gary's identity, permissions, memory, or operating rules.

## Current status

Gary `0.2.0-mvp` implements the portable backbone plus a working host/status/self-test CLI. The LLM runtime, model manager, Podman rehearsal lab, and full Admin tool execution layer are deliberately being built in later phases rather than being hidden behind a fragile bootstrap.

## Design principles

1. Measure the current host; never guess.
2. Keep policy and identity outside the model.
3. Read first; rehearse meaningful changes in Podman when possible.
4. Require explicit approval for privileged, boot, storage, firmware, firewall, repository, and destructive operations.
5. Keep heavy runtimes and model files host-local and on-demand.
6. Prefer capability checks over brittle version or path assumptions.
7. Record important evidence and outcomes so the next Gary instance can pick up where the previous one left off.

## Quick start

```bash
./bootstrap.sh
./bin/gary status
./bin/gary self-test
./bin/gary admin host
./bin/gary engineer check
```

`bootstrap.sh` is intentionally conservative. It installs only the lightweight host prerequisites when explicitly requested with `--install`; it does not download model weights or silently grant Gary root access.

## Repository layout

```text
gary/
├── agent/              Gary identity and operating rules
├── adapters/           Distro-family capability adapters
├── bin/                Stable user-facing entry point
├── bootstrap.sh        Idempotent host bootstrap
├── docs/               Architecture, security, health, models, GitHub
├── engineer/           Engineer role and maintenance playbook
├── hosts/              Sanitized host records
├── incidents/          Historical incidents and evidence
├── manifests/          Runtime contracts
├── policies/           Approval and privileged-action policy
├── src/gary/           Lightweight Python core
├── tests/              Fast local tests
└── .github/            CI, contribution and automation configuration
```

## Security boundary

Gary is not an unrestricted shell and never receives unrestricted root authority. Secrets, API tokens, private keys, credentials, recovery keys, model weights, caches, and transient host state are intentionally excluded from the portable repository.

See [docs/SECURITY.md](docs/SECURITY.md), [policies/PRIVILEGED_ACTIONS.md](policies/PRIVILEGED_ACTIONS.md), and [SECURITY.md](SECURITY.md).

## Roadmap

See [ROADMAP.md](ROADMAP.md). The near-term target is a dependable start/stop lifecycle, local GGUF model discovery through llama.cpp, and a rootless Podman rehearsal lab.
