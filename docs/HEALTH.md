# Installation and Health Model

## Installation level

- **0 — Backbone present**
- **1 — Host prepared**
- **2 — Runtime working**
- **3 — Model working**
- **4 — Tools/research verified**
- **5 — Fully operational**

## Health

- **HEALTHY:** all required checks pass.
- **DEGRADED:** Gary core works but a non-critical component is impaired.
- **BROKEN:** a required capability is unavailable or inconsistent.
- **NOT CONFIGURED:** a later-phase capability has not been built yet.

The CLI exposes human-readable and machine-readable status. Transient machine-readable state belongs under the host's XDG state directory and is not part of portable Git history.
