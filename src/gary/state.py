"""Host-local Gary state helpers."""

from __future__ import annotations

import json
import os
import platform
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def state_dir() -> Path:
    base = os.environ.get("XDG_STATE_HOME")
    return (Path(base) if base else Path.home() / ".local" / "state") / "gary"


def write_runtime_state(payload: dict[str, Any]) -> Path:
    directory = state_dir()
    directory.mkdir(parents=True, exist_ok=True)
    record = {"updated_at": datetime.now(timezone.utc).isoformat(), "hostname": platform.node(), **payload}
    target = directory / "runtime.json"
    temporary = directory / "runtime.json.tmp"
    temporary.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(temporary, target)
    return target
