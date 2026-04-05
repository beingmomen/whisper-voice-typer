# Whisper Voice Typer

A lightweight, privacy-first voice-to-text application powered by [OpenAI Whisper](https://github.com/openai/whisper).

**Press hotkey → speak → text appears in your document automatically.**

No API key. No internet after setup. All transcription happens locally on your machine.

---

## How It Works

1. Press **Ctrl+M** to start recording
2. Speak naturally
3. Press **Ctrl+M** again to stop → text is transcribed and automatically pasted into the active window

A system tray icon shows the current state:
- **Grey** = Ready
- **Red** = Recording
- **Yellow** = Transcribing
- **Green** = Done (returns to grey after 2 seconds)

---

## Features

✅ **Works offline** — Whisper model runs locally, no cloud needed  
✅ **Fast** — Transcribe in real-time (2-30 seconds per minute of audio)  
✅ **Lightweight** — ~1.5 GB disk for the model, ~400 MB RAM at runtime  
✅ **Accurate** — Supports 99 languages via Whisper  
✅ **Simple** — Single hotkey, global listening (works in any application)  
✅ **Cross-platform** — Ubuntu, Windows, macOS (Apple Silicon)  

---

## Requirements

| Platform | Requirements |
|----------|---|
| **Ubuntu / Debian** | Python 3.10+, `ffmpeg`, `xdotool`, `xclip` |
| **Windows** | Python 3.10+ (from [python.org](https://python.org)) |
| **macOS (Apple Silicon)** | Python 3.10+, Xcode Command Line Tools |

**Disk space:** ~5–10 GB (PyTorch + Whisper model, downloaded once during setup)

---

## Installation

### 🐧 Ubuntu / Debian

```bash
chmod +x install.sh run.sh
./install.sh        # first time only — downloads ~5 GB
./run.sh            # every time
```

**What it does:**
- Installs system dependencies (`ffmpeg`, `xdotool`, `xclip`, etc.)
- Creates a Python virtual environment
- Installs Python packages (`faster-whisper`, `sounddevice`, etc.)
- Downloads PyTorch with CUDA support (~2 GB)
- Downloads the Whisper `medium` model (~1.5 GB) for fast inference

**Troubleshooting:**
- If you get a `sudo` password prompt, type your password and press Enter
- If `install.sh` fails, check that you have ~10 GB free disk space
- If you're on an older GPU or CPU-only, see [HARDWARE_GUIDE.md](HARDWARE_GUIDE.md)

---

### 🪟 Windows

1. **Download Python 3.10+** from [python.org](https://python.org)
   - During installation, **check "Add Python to PATH"**
   - Verify: Open Command Prompt and type `python --version`

2. **Double-click `install.bat`** in the project folder (first time only)
   - A command window will open and run the installer
   - This downloads ~5 GB; may take 10–15 minutes on slower internet
   - Wait for "Installation complete!" message

3. **Double-click `run.bat`** every time you want to start the app
   - A command window will appear briefly, then the tray icon shows up
   - Close the command window when done, or it will stay open

**Troubleshooting:**
- If `install.bat` fails, ensure Python is in PATH: `python --version` in CMD should work
- If "Installation complete!" doesn't appear, scroll up in the window to see the error
- If the model download fails midway, delete the `venv/` folder and try again

---

### 🍎 macOS (Apple Silicon M1/M2/M3/M4)

```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python

# Follow Ubuntu instructions
chmod +x install.sh run.sh
./install.sh
./run.sh
```

**Grant accessibility permissions:**
When you first run the app, you'll get a prompt asking for accessibility permissions.
- Go to **System Settings → Privacy & Security → Accessibility**
- Add "Terminal" or your terminal app to the list
- Restart the app

**Performance note:** Whisper uses Apple's Metal Performance Shaders (MPS) for GPU acceleration. See [HARDWARE_GUIDE.md](HARDWARE_GUIDE.md) for optimal `MODEL_SIZE` and `compute_type` settings.

---

## Usage

### Controls

| Action | How |
|--------|-----|
| **Start recording** | Press **Ctrl+M** |
| **Stop & transcribe** | Press **Ctrl+M** again |
| **Quit the app** | Right-click tray icon → **Quit** |

### Tray Icon States

| Color | Meaning |
|-------|---------|
| 🔵 Grey | Idle, ready to record |
| 🔴 Red | Recording audio |
| 🟡 Yellow | Transcribing (processing audio) |
| 🟢 Green | Done! (resets after 2 seconds) |

---

## Configuration

All settings are in the top of `voice_typer.py`:

```python
HOTKEY      = {keyboard.Key.ctrl_l, keyboard.KeyCode.from_char('m')}  # Ctrl+M
MODEL_SIZE  = "medium"    # See model table below
LANGUAGE    = None        # None = auto-detect, "ar" = Arabic, "en" = English, etc.
SAMPLE_RATE = 16000
```

### Change the Hotkey

To use **Ctrl+Shift+Space** instead:

```python
HOTKEY = {keyboard.Key.ctrl_l, keyboard.Key.shift, keyboard.KeyCode.from_char(' ')}
```

To use **Alt+M**:

```python
HOTKEY = {keyboard.Key.alt_l, keyboard.KeyCode.from_char('m')}
```

### Choose a Model

Models affect **speed**, **accuracy**, and **VRAM usage**:

| Model | Size | Speed | Accuracy | Best for |
|-------|------|-------|----------|----------|
| `tiny` | 75 MB | ⚡⚡⚡ Ultra-fast | ⭐ Low | Weak hardware, low-accuracy tolerance |
| `base` | 145 MB | ⚡⚡ Very fast | ⭐⭐ OK | Budget CPUs |
| `small` | 465 MB | ⚡ Fast | ⭐⭐⭐ Good | Standard CPUs, older GPUs |
| `medium` | 1.5 GB | 🟢 Balanced | ⭐⭐⭐⭐ Very good | **Default** — recommended for most users |
| `large-v3` | 3 GB | 🐢 Slower | ⭐⭐⭐⭐⭐ Best | High-end GPU, maximum accuracy needed |

**Example:** To use `large-v3` (best accuracy):

```python
MODEL_SIZE = "large-v3"
```

Then run `install.sh` again, or manually download:

```bash
source venv/bin/activate
python -c "from faster_whisper import WhisperModel; WhisperModel('large-v3', device='cpu')"
```

### Set Language

By default, Whisper auto-detects the language. To force a specific language:

```python
LANGUAGE = "ar"   # Arabic
LANGUAGE = "en"   # English
LANGUAGE = "fr"   # French
LANGUAGE = "es"   # Spanish
LANGUAGE = "de"   # German
```

---

## Hardware Recommendations

Choose your `MODEL_SIZE` based on your hardware:

| Hardware | Recommended | Notes |
|----------|---|---|
| **CPU only** | `small` or `tiny` | Takes 2–5 minutes per minute of audio |
| **Intel GTX/RTX** | `medium` or `small` | Uses CUDA; fast with int8 quantization |
| **NVIDIA RTX 2060+** | `large-v3` | Excellent speed; see [HARDWARE_GUIDE.md](HARDWARE_GUIDE.md) for settings |
| **NVIDIA RTX 3070+** | `large-v3` | Best speed; can use float16 |
| **Apple Silicon M1–M4** | `medium` | Uses Metal performance; see guide for MPS config |

**See [HARDWARE_GUIDE.md](HARDWARE_GUIDE.md) for detailed per-GPU tuning and VRAM troubleshooting.**

---

## Troubleshooting

### ❌ No audio / "No speech detected"

**Symptom:** App records but says "No speech detected."

**Solutions:**
- Check that your microphone is set as the **default input device**
  - Ubuntu: System Settings → Sound → Input Device
  - Windows: Settings → Sound → Input
- Try speaking louder and closer to the mic
- Switch to a smaller model (`small` or `base`) for faster feedback and debugging
- Check that no other app is blocking the audio device

---

### ❌ Out of Memory (VRAM)

**Symptom:** `RuntimeError: CUDA out of memory` or `torch.cuda.OutOfMemoryError`

**Solutions:**
1. Switch to a smaller model: `tiny` → `base` → `small`
2. Change compute type to `int8`:
   ```python
   # In detect_device() function, change:
   return device, "int8"
   ```
3. Close other apps to free up VRAM
4. See [HARDWARE_GUIDE.md](HARDWARE_GUIDE.md) for detailed VRAM troubleshooting per GPU

---

### ❌ Text not pasting (Linux)

**Symptom:** Audio transcribes but doesn't paste into the document.

**Solutions:**
- Ensure `xdotool` and `xclip` are installed:
  ```bash
  sudo apt install xdotool xclip
  ```
- Some applications don't accept simulated keyboard input; try a different app (e.g., text editor instead of browser)
- On Wayland, you may need to use X11 instead:
  - Log out and select "Ubuntu on Xorg" at the login screen
  - Then restart the app

---

### ❌ App won't start (Windows)

**Symptom:** Double-click `run.bat` and nothing happens.

**Solutions:**
1. Make sure `install.bat` completed successfully
2. Verify Python is installed: Open Command Prompt and type `python --version`
3. Try running from Command Prompt to see error messages:
   ```
   cd path\to\voice-typer
   run.bat
   ```
4. If it says "venv not found," run `install.bat` again

---

### ❌ Whisper model won't download

**Symptom:** Installation fails during model download step.

**Solutions:**
- Check your internet connection
- Try again; if it fails midway, delete the `venv/` folder and restart `install.sh`
- If stuck, manually download a smaller model:
  ```bash
  source venv/bin/activate
  python -c "from faster_whisper import WhisperModel; WhisperModel('tiny', device='cpu')"
  ```

---

### ❌ Wayland: pynput not working

**Symptom:** App runs but Ctrl+M doesn't work; you see X11 errors.

**Solutions:**
- Voice Typer requires X11. On Wayland, either:
  - Log out and select "**Ubuntu on Xorg**" at the login screen
  - OR set environment variable:
    ```bash
    QT_QPA_PLATFORM=xcb ./run.sh
    ```

---

## Advanced: Using Different Models

### Download a specific model manually

```bash
source venv/bin/activate
python -c "from faster_whisper import WhisperModel; WhisperModel('large-v3')"
```

### Run without the pre-downloaded model

The app will download `medium` on first use if it's not already cached.

### Use custom compute types

In `voice_typer.py`, modify the `detect_device()` function:

```python
def detect_device():
    return "cuda", "float16"  # Use float16 for precision (uses more VRAM)
```

See [HARDWARE_GUIDE.md](HARDWARE_GUIDE.md) for detailed configs per GPU.

---

## Building from Source

The app is a single Python file — no compilation needed.

```bash
# After install.sh / install.bat, simply edit voice_typer.py
# Changes take effect next time you run ./run.sh or run.bat
```

---

## Contributing

Found a bug? Have a feature idea? Issues and pull requests are welcome.

**Before contributing:**
- Test on both Ubuntu and Windows if possible
- Keep it simple — this is meant to be a lightweight, single-file utility
- See [CLAUDE.md](CLAUDE.md) for architecture notes

---

## License

[GNU General Public License v3](LICENSE) — See [LICENSE](LICENSE) for details.

**In short:** You can use, modify, and share this software freely, as long as you distribute any modified versions under the same GPL-3.0 license.

---

## Architecture

See [CLAUDE.md](CLAUDE.md) for:
- Threading model
- How to modify the code
- Configuration options
- Platform-specific details

---

## FAQ

**Q: Does this send my audio to the internet?**  
A: No. Everything runs locally. Whisper is an offline model.

**Q: Can I change the language?**  
A: Yes — set `LANGUAGE` in `voice_typer.py` to any of the 99 languages Whisper supports.

**Q: What if I don't have a GPU?**  
A: It works on CPU too, just slower (2–5 minutes per minute of audio). Use a smaller model like `tiny` or `base`.

**Q: Can I use this in other languages?**  
A: Yes — Whisper supports 99 languages, and pynput works globally.

**Q: Is this only for English?**  
A: No — see the `LANGUAGE` setting above.

---

**Happy transcribing! 🎤✨**