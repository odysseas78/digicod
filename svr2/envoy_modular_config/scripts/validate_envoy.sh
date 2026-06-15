#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

PY_CMD=()

try_python() {
    if "$@" -c "import yaml" >/dev/null 2>&1; then
        PY_CMD=("$@")
        return 0
    fi
    return 1
}

if [[ -n "${PYTHON:-}" ]]; then
    try_python "$PYTHON" || true
fi

if [[ ${#PY_CMD[@]} -eq 0 ]] && command -v python >/dev/null 2>&1; then
    try_python python || true
fi

if [[ ${#PY_CMD[@]} -eq 0 ]] && command -v python.exe >/dev/null 2>&1; then
    try_python python.exe || true
fi

if [[ ${#PY_CMD[@]} -eq 0 ]] && command -v py >/dev/null 2>&1; then
    try_python py -3 || true
fi

if [[ ${#PY_CMD[@]} -eq 0 ]] && command -v py.exe >/dev/null 2>&1; then
    try_python py.exe -3 || true
fi

if [[ ${#PY_CMD[@]} -eq 0 ]] && command -v python3 >/dev/null 2>&1; then
    try_python python3 || true
fi

if [[ ${#PY_CMD[@]} -eq 0 ]] && command -v python3.exe >/dev/null 2>&1; then
    try_python python3.exe || true
fi

if [[ ${#PY_CMD[@]} -eq 0 ]]; then
    echo "Kein Python-Interpreter mit PyYAML gefunden."
    echo "Unter Windows bitte versuchen:"
    echo "  python scripts/build_envoy.py"
    echo "  py -3 scripts/build_envoy.py"
    exit 1
fi

echo "Benutze Python: ${PY_CMD[*]}"
"${PY_CMD[@]}" scripts/build_envoy.py

if ! command -v envoy >/dev/null 2>&1; then
    echo "Envoy wurde nicht gefunden. Nur YAML wurde generiert: generated/envoy.yaml"
    exit 0
fi
envoy --mode validate -c generated/envoy.yaml
