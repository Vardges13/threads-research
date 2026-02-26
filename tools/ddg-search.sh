#!/bin/bash
# DuckDuckGo search wrapper
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/ddg-venv/bin/activate"
python3 "$SCRIPT_DIR/ddg-search.py" "$@"
