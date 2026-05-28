#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/build_envoy.py
if ! command -v envoy >/dev/null 2>&1; then
    echo "Envoy wurde nicht gefunden. Nur YAML wurde generiert: generated/envoy.yaml"
    exit 0
fi
envoy --mode validate -c generated/envoy.yaml
