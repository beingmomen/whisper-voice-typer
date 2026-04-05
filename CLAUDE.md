# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Application

```bash
# First-time setup (downloads ~5-10GB: PyTorch + Whisper model)
./install.sh

# Run the application
./run.sh

# Or manually after setup
source venv/bin/activate
python voice_typer.py
```

No test suite exists — this is a desktop utility verified by running it.

## Architecture

**Single-file application:** All logic lives in [voice_typer.py](voice_typer.py) (~180 lines).

### Threading model
- **Main thread:** Blocks on `tray.run()` to keep the app alive
- **Daemon thread:** `pynput` keyboard listener watching for hotkey
- **Daemon threads:** Transcription task + tray icon updates (via `threading.Timer`)

### Core flow
1. On startup: detect GPU/CPU → load Whisper model → start audio stream → start keyboard listener → block on tray
2. Hotkey press (Ctrl+M): set `recording=True`, start accumulating `audio_chunks`
3. Hotkey release: set `recording=False` → spawn `transcribe_and_paste()` thread
4. `transcribe_and_paste()`: concatenate chunks → run Whisper → copy to clipboard → `xdotool key ctrl+v` (Linux) or Win32 paste (Windows)

### Tray icon state machine
Grey (idle) → Red (recording) → Yellow (transcribing) → Green (done, 2s) → Grey

### Configuration (top of voice_typer.py, lines 14–20)
```python
HOTKEY      = {keyboard.Key.ctrl_l, keyboard.KeyCode.from_char('m')}
MODEL_SIZE  = "medium"   # large-v3, medium, small, base, tiny
LANGUAGE    = None       # None = auto-detect, "ar", "en", etc.
SAMPLE_RATE = 16000
```

### Device detection (lines 75–83)
Returns `(device, compute_type)` — CUDA → MPS → CPU, all using `int8`. Model loads once at startup.

### Platform differences
- **Linux:** paste via `xdotool key ctrl+v`, notifications via `notify-send`
- **Windows:** paste via Win32 `keybd_event`, notifications via `plyer`

## Key dependencies
- `faster-whisper` — optimized CTranslate2-based Whisper inference
- `sounddevice` — continuous float32 16kHz mono audio stream
- `pynput` — global keyboard listener (requires accessibility permissions on macOS)
- `pystray` — system tray icon
- `xdotool` + `xclip` — Linux clipboard/paste automation

See [HARDWARE_GUIDE.md](HARDWARE_GUIDE.md) for model size vs. VRAM/speed tradeoffs per GPU.
