#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

if [ ! -f config.yml ]; then
  cp config.example.yml config.yml
fi

echo "Installation fertig. Start: ./run.sh"
