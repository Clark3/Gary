# Gary Roadmap

## Phase 0 — Foundation ✅

- [x] Define Gary as the holistic identity.
- [x] Define Admin and Engineer roles.
- [x] Define portable-backbone vs host-runtime separation.
- [x] Define approval, rehearsal, verification, and logging principles.
- [x] Define model independence and lifecycle.
- [x] Define host records and incident history.
- [x] Define health/completion concepts.
- [x] Define capability-driven distro adapters.
- [x] Establish GitHub repository and contribution scaffolding.

## Phase 1 — Bootstrap and health 🚧

- [x] Implement initial `bootstrap.sh`.
- [x] Detect OS family/version, architecture, init, desktop, package manager, network manager, UEFI/Secure Boot.
- [x] Discover executable paths for baseline tools.
- [x] Create stable `gary` wrapper.
- [x] Implement installation-level and health reporting.
- [x] Implement machine-readable health output.
- [ ] Install/verify llama.cpp capabilities.
- [ ] Install/verify Open Interpreter capabilities.
- [ ] Add richer self-healing / migration checks.

## Phase 2 — Start/stop lifecycle

- [x] Define lifecycle contract.
- [ ] Implement model-server startup only when needed.
- [ ] Implement harness startup only when needed.
- [ ] Save/restore session state.
- [ ] Verify clean shutdown and no orphaned heavy processes.
- [ ] Finish Cinnamon launcher integration.

## Phase 3 — Model manager

- [ ] Scan configured GGUF directories.
- [ ] Maintain model registry and metadata.
- [ ] Load/unload/switch models through the current llama.cpp server API.
- [ ] Select models from available RAM and task requirements.
- [ ] Preserve Gary identity and session state across model switches.
- [ ] Keep model files host-local.
- [ ] Add optional free remote-provider interface.

## Phase 4 — Admin tools and Podman repair lab

- [ ] Build read-only diagnostic command set.
- [ ] Build narrowly scoped remediation tools.
- [ ] Implement rootless Podman rehearsal environments.
- [ ] Mark host-specific operations that cannot be faithfully rehearsed.
- [ ] Add evidence ledger automation.
- [ ] Enforce explicit approval gates.

## Phase 5 — Persistent knowledge

- [ ] Finalize memory, host inventory, incident, and recipe schemas.
- [ ] Add safe Git-backed synchronization.
- [ ] Add memory compaction/summarization.
- [ ] Prevent accidental secret persistence with automated checks.

## Phase 6 — Engineer / self-maintenance

- [ ] Build the ephemeral Engineer model profile.
- [ ] Research upstream runtime/API changes.
- [ ] Rehearse proposed changes in Podman where meaningful.
- [ ] Produce maintenance reports.
- [ ] Apply approved project changes.
- [ ] Validate a clean rebuild end-to-end.
- [ ] Remove temporary Engineer runtime/model after maintenance.

## Phase 7 — Portability validation

- [ ] Debian/Ubuntu/Mint
- [ ] Fedora
- [ ] Arch
- [ ] openSUSE
- [ ] Alpine or documented unsupported features
- [ ] Clean-machine bootstrap tests
- [ ] Portable-backbone migration tests

## Operating cadence

- Normal use: on-demand only.
- Engineer maintenance: approximately every 2 months initially.
- Security/critical upstream breakage: act sooner.
