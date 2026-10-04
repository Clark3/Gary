# Bootstrap Design

`bootstrap.sh` is Gary's rebuild authority for lightweight host setup. It must be idempotent, conservative, and explicit about privilege.

It detects architecture, distribution, package manager, init/service manager, desktop, network manager, UEFI/Secure Boot, existing runtimes, executable locations, and capabilities.

Prefer distro repositories for baseline dependencies and upstream release metadata for specialized runtimes. Do not rely solely on latest filenames or version strings. If upstream changes its layout, fail safely with an actionable Engineer report.

The install exposes a stable `gary` command while allowing underlying paths to change.
