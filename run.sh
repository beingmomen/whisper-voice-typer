#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [ ! -d "venv" ]; then
    echo "ERROR: Virtual environment not found."
    echo "Please run install.sh first."
    exit 1
fi

source venv/bin/activate
exec python3 voice_typer.py
