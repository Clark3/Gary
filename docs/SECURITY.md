# Security and Safety Model

## Core rule

The LLM does not receive unrestricted root authority.

Gary uses four operating levels: **Observe**, **Rehearse**, **Apply**, and **Approve**. Rootless/disposable Podman is preferred for meaningful host-independent rehearsal. High-impact operations require explicit human approval.

## Never auto-run

- raw block-device writes
- partition deletion or formatting
- filesystem destruction
- bootloader replacement without explicit approval
- BIOS/UEFI flashing without explicit approval
- unrestricted `sudo` shells
- recursive destructive deletion outside the Gary workspace
- secret extraction or export

Never place API keys, access tokens, SSH keys, private keys, passwords, browser credentials, recovery keys, or similar secrets in this repository.
