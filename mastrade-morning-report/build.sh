#!/usr/bin/env bash
# Build the report tool on Linux/macOS.
#
# NOTE: PyInstaller does NOT cross-compile. Running this on Linux produces a
# Linux ELF binary, not a Windows .exe. To get an .exe you need to build on
# Windows (build.ps1) or use the GitHub Actions workflow in
# .github/workflows/build-windows-exe.yml.

set -euo pipefail
cd "$(dirname "$0")"

if [ ! -d .venv ]; then
    echo "==> creating .venv"
    python3 -m venv .venv
fi

echo "==> installing dependencies"
./.venv/bin/python -m pip install --upgrade pip -q
./.venv/bin/python -m pip install -r requirements.txt -q

echo "==> building"
./.venv/bin/pyinstaller mastrade_morning_report.spec --clean --noconfirm

echo "==> smoke test"
./dist/mastrade_morning_report --help > /dev/null

echo "==> OK: $(ls -lh dist/mastrade_morning_report | awk '{print $9, $5}')"
