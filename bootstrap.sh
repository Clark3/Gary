#!/usr/bin/env bash
set -euo pipefail
PROJECT_ROOT="$(cd -- "$(dirname -- "$0")" && pwd)"
INSTALL=0
while [ "$#" -gt 0 ]; do
  case "$1" in
    --install) INSTALL=1 ;;
    --skip-desktop) ;;
    -h|--help) echo 'Usage: ./bootstrap.sh [--install] [--skip-desktop]'; exit 0 ;;
    *) echo "Unknown option: $1" >&2; exit 2 ;;
  esac
  shift
done
have() { command -v "$1" >/dev/null 2>&1; }
OS_ID=unknown; OS_VERSION=unknown
if [ -r /etc/os-release ]; then
  # shellcheck source=/etc/os-release
  . /etc/os-release; OS_ID="${ID:-unknown}"; OS_VERSION="${VERSION_ID:-unknown}"; fi
PKG=""
if have apt-get; then PKG=apt-get; elif have dnf; then PKG=dnf; elif have pacman; then PKG=pacman; elif have zypper; then PKG=zypper; elif have apk; then PKG=apk; fi
printf 'Gary bootstrap\nHost: %s %s (%s)\nPackage manager: %s\n' "$OS_ID" "$OS_VERSION" "$(uname -m)" "${PKG:-none detected}"
missing=(); for cmd in python3 git; do if ! have "$cmd"; then missing+=("$cmd"); fi; done
if [ "$INSTALL" -eq 1 ] && [ "${#missing[@]}" -gt 0 ]; then
  case "$PKG" in
    apt-get) sudo apt-get update && sudo apt-get install -y "${missing[@]}" ;;
    dnf) sudo dnf install -y "${missing[@]}" ;;
    pacman) sudo pacman -Sy --needed --noconfirm "${missing[@]}" ;;
    zypper) sudo zypper --non-interactive install "${missing[@]}" ;;
    apk) sudo apk add "${missing[@]}" ;;
    *) echo "No supported package manager; install ${missing[*]} manually." >&2; exit 1 ;;
  esac
fi
if [ "${#missing[@]}" -gt 0 ] && [ "$INSTALL" -eq 0 ]; then echo "Missing baseline prerequisites: ${missing[*]}"; echo "Run './bootstrap.sh --install'."; exit 1; fi
mkdir -p "${XDG_STATE_HOME:-$HOME/.local/state}/gary" "${XDG_BIN_HOME:-$HOME/.local/bin}"
WRAPPER="${XDG_BIN_HOME:-$HOME/.local/bin}/gary"
cat > "$WRAPPER" <<EOF
#!/usr/bin/env bash
exec "$PROJECT_ROOT/bin/gary" "\$@"
EOF
chmod 0755 "$WRAPPER"
APPLICATIONS_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/applications"
mkdir -p "$APPLICATIONS_DIR"
cat > "$APPLICATIONS_DIR/gary.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=Gary
Comment=Local Linux system administrator
Exec=$PROJECT_ROOT/start.sh
Icon=utilities-terminal
Terminal=true
Categories=System;Utility;
EOF
printf 'Bootstrap complete. Gary command: %s\n' "$WRAPPER"
