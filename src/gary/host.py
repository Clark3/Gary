"""Host discovery and safe capability probes for Gary."""

from __future__ import annotations

import json
import os
import platform
import shutil
import subprocess
from pathlib import Path
from typing import Any


def read_os_release() -> dict[str, str]:
    data: dict[str, str] = {}
    path = Path("/etc/os-release")
    if not path.exists():
        return data
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if "=" not in line or not line or line.startswith("#"):
            continue
        key, value = line.split("=", 1)
        data[key] = value.strip().strip('"')
    return data


def command_exists(name: str) -> bool:
    return shutil.which(name) is not None


def run_probe(args: list[str], timeout: float = 4.0) -> dict[str, Any]:
    try:
        completed = subprocess.run(args, check=False, capture_output=True, text=True, timeout=timeout, env={"PATH": os.environ.get("PATH", "")})
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"ok": False, "error": str(exc)}
    return {"ok": completed.returncode == 0, "returncode": completed.returncode, "stdout": completed.stdout.strip()[:2000], "stderr": completed.stderr.strip()[:2000]}


def detect_init() -> str | None:
    init = Path("/sbin/init")
    if init.exists():
        try:
            return str(init.resolve())
        except OSError:
            return str(init)
    return None


def detect_desktop() -> str | None:
    for key in ("XDG_CURRENT_DESKTOP", "XDG_SESSION_DESKTOP", "DESKTOP_SESSION"):
        value = os.environ.get(key)
        if value:
            return value
    return None


def detect_network_manager() -> list[str]:
    found: list[str] = []
    if command_exists("nmcli"):
        found.append("NetworkManager")
    if Path("/run/systemd/system").exists() and command_exists("networkctl"):
        found.append("systemd-networkd")
    if command_exists("connmanctl"):
        found.append("connman")
    if Path("/run/iwd").exists():
        found.append("iwd")
    return found


def detect_package_manager() -> list[str]:
    return [m for m in ("apt-get", "dnf", "pacman", "zypper", "apk") if command_exists(m)]


def detect_secure_boot() -> str:
    if not Path("/sys/firmware/efi").exists():
        return "not-uefi-or-unavailable"
    if command_exists("mokutil"):
        probe = run_probe(["mokutil", "--sb-state"])
        combined = f'{probe.get("stdout", "")} {probe.get("stderr", "")}'.lower()
        if "secureboot enabled" in combined:
            return "enabled"
        if "secureboot disabled" in combined:
            return "disabled"
    return "uefi-unknown"


def memory_total_kib() -> int | None:
    try:
        for line in Path("/proc/meminfo").read_text(encoding="ascii", errors="ignore").splitlines():
            if line.startswith("MemTotal:"):
                return int(line.split()[1])
    except (OSError, ValueError):
        return None
    return None


def cpu_model() -> str | None:
    try:
        for line in Path("/proc/cpuinfo").read_text(encoding="utf-8", errors="replace").splitlines():
            if line.lower().startswith("model name") and ":" in line:
                return line.split(":", 1)[1].strip()
    except OSError:
        return None
    return platform.processor() or None


def capability_summary() -> dict[str, Any]:
    binaries = {name: shutil.which(name) for name in ("python3", "git", "podman", "llama-server", "systemctl", "nmcli")}
    return {
        "python3": binaries["python3"] is not None,
        "git": binaries["git"] is not None,
        "podman": binaries["podman"] is not None,
        "llama_server": binaries["llama-server"] is not None,
        "systemd": command_exists("systemctl"),
        "network_manager": command_exists("nmcli"),
        "git_path": binaries["git"],
        "podman_path": binaries["podman"],
        "llama_server_path": binaries["llama-server"],
    }


def discover_host() -> dict[str, Any]:
    os_release = read_os_release()
    return {
        "distribution": os_release.get("PRETTY_NAME") or os_release.get("NAME"),
        "distribution_id": os_release.get("ID"),
        "version": os_release.get("VERSION_ID"),
        "architecture": platform.machine(),
        "kernel": platform.release(),
        "cpu_model": cpu_model(),
        "memory_total_kib": memory_total_kib(),
        "init": detect_init(),
        "desktop": detect_desktop(),
        "package_managers": detect_package_manager(),
        "network_managers": detect_network_manager(),
        "boot_mode": "uefi" if Path("/sys/firmware/efi").exists() else "legacy-or-unknown",
        "secure_boot": detect_secure_boot(),
        "capabilities": capability_summary(),
    }


def json_dumps(data: Any) -> str:
    return json.dumps(data, indent=2, sort_keys=True)
