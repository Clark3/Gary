# Architecture

The portable repository is the durable source of truth for Gary identity, policy, adapters, memory, host records, incidents, recipes, manifests, bootstrap logic, tests, and documentation.

Host-local runtime includes llama.cpp, the selected harness, Podman, system utilities, research tooling, model files, and transient state.

Lifecycle: detect → preflight → choose model → start only required runtime → load state; then observe → research → rehearse → explain → approve → apply → verify → record; finally save state → unload model → stop runtime → clean temporary containers → verify shutdown.

Gary reasons in capabilities such as packages, services, networking, storage, boot, firewall, logs, firmware, power, containers, models, and research. Adapters map those capabilities to concrete distro-specific commands.
