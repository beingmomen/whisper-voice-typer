#!/bin/bash
set -e

echo "======================================"
echo "   Voice Typer - Installation (Ubuntu)"
echo "======================================"

# ── 1. System dependencies ─────────────────────────────────────────────────
echo ""
echo "[1/5] Installing system dependencies..."
sudo apt update -qq
sudo apt install -y python3 python3-pip python3-venv ffmpeg portaudio19-dev xdotool xclip libnotify-bin

# ── 2. Python virtual environment ──────────────────────────────────────────
echo ""
echo "[2/5] Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# ── 3. Python packages ─────────────────────────────────────────────────────
echo ""
echo "[3/5] Installing Python packages..."
pip install --upgrade pip -q
pip install faster-whisper sounddevice numpy pyperclip pynput pystray pillow -q

# ── 4. PyTorch with CUDA (for GPU support) ─────────────────────────────────
echo ""
echo "[4/5] Installing PyTorch with CUDA support (~2GB)..."
pip install torch --index-url https://download.pytorch.org/whl/cu121 -q

# ── 5. Download model (~1.5GB, one time only) ────────────────────────────────
echo ""
echo "[5/5] Downloading Whisper medium model (~1.5GB)..."
echo "      This will only happen once."
echo "      Tip: Edit voice_typer.py and change MODEL_SIZE to 'large-v3' for better accuracy."
python3 - <<'PYEOF'
from faster_whisper import WhisperModel
print("Downloading model...")
WhisperModel("medium", device="cpu")
print("Model downloaded successfully.")
PYEOF

echo ""
echo "======================================"
echo " Installation complete!"
echo " Run the app with:  ./run.sh"
echo "======================================"
