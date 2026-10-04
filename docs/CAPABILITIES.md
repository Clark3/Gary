# Capability Model

Gary should reason in capabilities first and commands second.

| Capability | Examples |
|---|---|
| packages | install/query/update/remove |
| services | status/start/stop/enable |
| networking | interfaces/routes/DNS |
| storage | disks/mounts/filesystems |
| boot | UEFI/bootloader state |
| firewall | query/rules |
| logs | journal/kernel/service logs |
| firmware | device/firmware inventory |
| power | sleep/hibernate/thermal |
| containers | rootless Podman |
| models | discover/load/unload |
| research | web/repository lookup |

Adapters declare detection rules, concrete commands, known exceptions, and tests.
