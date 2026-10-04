"""Command-line entry point for the lightweight Gary core."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

from gary import __version__
from gary.host import discover_host, json_dumps
from gary.state import write_runtime_state


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def health_from_host(host: dict[str, Any]) -> tuple[int, str, list[dict[str, Any]]]:
    caps = host["capabilities"]
    checks = [
        {"name": "portable_backbone", "ok": repo_root().joinpath("PROJECT_SPEC.md").exists()},
        {"name": "python3", "ok": caps["python3"]},
        {"name": "git", "ok": caps["git"]},
    ]
    health = "HEALTHY" if all(c["ok"] for c in checks) else "DEGRADED"
    level = 1 if all(c["ok"] for c in checks) else 0
    if caps["llama_server"]:
        level = max(level, 2)
    return level, health, checks


def runtime_info() -> dict[str, Any]:
    root = repo_root()
    git = None
    if (root / ".git").exists():
        try:
            out = subprocess.run(["git", "-C", str(root), "status", "--porcelain=v1", "--branch"], check=False, capture_output=True, text=True, timeout=5)
            git = {"ok": out.returncode == 0, "status": out.stdout.strip()[:3000]}
        except (OSError, subprocess.TimeoutExpired) as exc:
            git = {"ok": False, "error": str(exc)}
    return {"repository": str(root), "git": git}


def build_status() -> dict[str, Any]:
    host = discover_host()
    level, health, checks = health_from_host(host)
    return {"gary": {"version": __version__, "project_root": str(repo_root())}, "installation_level": level, "health": health, "checks": checks, "host": host, "runtime": runtime_info()}


def print_status(data: dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json_dumps(data)); return
    print(f"Gary {data['gary']['version']}")
    print(f"Health: {data['health']}")
    print(f"Installation level: {data['installation_level']}/5")
    print(f"Host: {data['host'].get('distribution') or 'unknown'} | {data['host']['architecture']} | kernel {data['host']['kernel']}")
    print(f"CPU: {data['host'].get('cpu_model') or 'unknown'}")
    mem = data['host'].get('memory_total_kib')
    if mem: print(f"RAM: {mem / 1024 / 1024:.1f} GiB")
    print(f"Desktop: {data['host'].get('desktop') or 'unknown'}")
    print(f"Boot: {data['host']['boot_mode']} | Secure Boot: {data['host']['secure_boot']}")
    print("Capabilities:")
    for key in ("python3", "git", "podman", "llama_server", "systemd", "network_manager"):
        print(f"  {'OK' if data['host']['capabilities'][key] else 'MISSING'} {key}")


def cmd_self_test(as_json: bool) -> int:
    data = build_status()
    caps = data["host"]["capabilities"]
    results = data["checks"] + [
        {"name": "podman", "ok": caps["podman"], "severity": "optional"},
        {"name": "llama_server", "ok": caps["llama_server"], "severity": "future-required"},
    ]
    for result in results: result.setdefault("severity", "required")
    data["self_test"] = results
    if any(not r["ok"] for r in results if r["severity"] == "required"): data["health"] = "BROKEN"
    elif any(not r["ok"] for r in results if r["severity"] != "required"): data["health"] = "DEGRADED"
    try: data["state_file"] = str(write_runtime_state({"installation_level": data["installation_level"], "health": data["health"], "self_test": results}))
    except OSError as exc: data["state_write_error"] = str(exc); return 1
    if as_json: print(json_dumps(data))
    else:
        print_status(data, False); print("Self-test:")
        for r in results: print(f"  [{'PASS' if r['ok'] else ('WARN' if r['severity'] != 'required' else 'FAIL')}] {r['name']}")
        print(f"State: {data['state_file']}")
    return 0 if data["health"] != "BROKEN" else 1


def cmd_engineer(as_json: bool) -> int:
    data = build_status(); root = repo_root()
    docs = ["PROJECT_SPEC.md", "ROADMAP.md", "docs/SECURITY.md", "docs/BOOTSTRAP.md", "docs/HEALTH.md", "docs/MODELS.md", "engineer/SYSTEM.md", "engineer/MAINTENANCE.md"]
    missing = [p for p in docs if not (root / p).exists()]
    data["engineer"] = {"documentation_complete": not missing, "missing_documents": missing, "git_repository_present": (root / ".git").exists(), "bootstrap_present": (root / "bootstrap.sh").exists(), "tests_present": (root / "tests").is_dir(), "ci_present": (root / ".github" / "workflows" / "ci.yml").exists()}
    ok = not missing and all(data["engineer"][k] for k in ("git_repository_present", "bootstrap_present", "tests_present", "ci_present"))
    data["engineer"]["check"] = "PASS" if ok else "FAIL"
    if as_json: print(json_dumps(data))
    else:
        print("Gary — Engineer check")
        for k in ("documentation_complete", "git_repository_present", "bootstrap_present", "tests_present", "ci_present"): print(f"{k}: {'OK' if data['engineer'][k] else 'MISSING'}")
        print(f"Result: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="gary")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--version", action="version", version=__version__)
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("status"); sub.add_parser("self-test"); sub.add_parser("version")
    admin = sub.add_parser("admin"); admin.add_argument("action", nargs="?", default="host", choices=["host"])
    eng = sub.add_parser("engineer"); eng.add_argument("action", nargs="?", default="check", choices=["check"])
    args = parser.parse_args(argv); as_json = args.json
    if args.command in (None, "status"):
        data = build_status()
        try: write_runtime_state({"installation_level": data["installation_level"], "health": data["health"]})
        except OSError: pass
        print_status(data, as_json); return 0
    if args.command == "self-test": return cmd_self_test(as_json)
    if args.command == "version": print(__version__); return 0
    if args.command == "admin":
        data = discover_host()
        print(json.dumps(data, indent=2, sort_keys=True) if as_json else f"Gary — Admin host view\nDistribution: {data.get('distribution') or 'unknown'}\nKernel: {data['kernel']}\nArchitecture: {data['architecture']}\nCPU: {data.get('cpu_model') or 'unknown'}")
        return 0
    if args.command == "engineer": return cmd_engineer(as_json)
    return 2


if __name__ == "__main__": raise SystemExit(main())
