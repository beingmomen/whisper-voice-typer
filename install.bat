@echo off
setlocal EnableDelayedExpansion
title Voice Typer - Installation (Windows)

echo ======================================
echo    Voice Typer - Installation (Windows)
echo ======================================

echo [1/4] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found.
    echo Download from https://python.org and check "Add Python to PATH".
    pause
    exit /b 1
)
echo       Python found.

echo [2/4] Creating virtual environment and installing packages...
python -m venv venv
call venv\Scripts\activate.bat
python -m pip install --upgrade pip -q
pip install faster-whisper sounddevice numpy pyperclip pynput pystray pillow plyer -q

echo [3/4] Installing PyTorch with CUDA support (~2GB)...
pip install torch --index-url https://download.pytorch.org/whl/cu121 -q

echo [4/4] Downloading Whisper medium model (~1.5GB)...
python -c "from faster_whisper import WhisperModel; print('Downloading...'); WhisperModel('medium', device='cpu'); print('Done.')"

echo ======================================
echo  Installation complete!
echo  Run the app with:  run.bat
echo ======================================
pause
