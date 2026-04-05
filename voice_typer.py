import sounddevice as sd
import numpy as np
import pyperclip
import sys
import time
import subprocess
import threading
import platform
from pynput import keyboard
from faster_whisper import WhisperModel
from PIL import Image, ImageDraw
import pystray

# ══════════════════════════════════════════════════════════════
#  Settings - edit as you like
HOTKEY      = {keyboard.Key.ctrl_l, keyboard.KeyCode.from_char('m')}  # Ctrl+M
MODEL_SIZE  = "medium"    # large-v3 = best | medium = faster
LANGUAGE    = None          # None = auto | "ar" = Arabic | "en" = English
SAMPLE_RATE = 16000
# ══════════════════════════════════════════════════════════════

OS = platform.system()  # "Linux" or "Windows"

# ── Tray icon ──────────────────────────────────────────────────────────────
def make_icon(color):
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([4, 4, 60, 60], fill=color)
    return img

ICON_IDLE       = make_icon((100, 100, 100))
ICON_RECORDING  = make_icon((220, 50,  50))
ICON_PROCESSING = make_icon((230, 180, 0))
ICON_DONE       = make_icon((50,  200, 80))

tray = pystray.Icon(
    "VoiceTyper",
    ICON_IDLE,
    "Voice Typer - Ready",
    menu=pystray.Menu(
        pystray.MenuItem("Quit", lambda: (stream.stop(), tray.stop()))
    )
)

def set_tray(icon_img, tooltip):
    tray.icon  = icon_img
    tray.title = tooltip

# ── Notification ───────────────────────────────────────────────────────────
def notify(title, body, urgency="normal"):
    if OS == "Linux":
        subprocess.Popen(
            ["notify-send", "-u", urgency, "-t", "3000", title, body],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
    elif OS == "Windows":
        try:
            from plyer import notification
            notification.notify(title=title, message=body, timeout=3)
        except Exception:
            pass

# ── Paste text ─────────────────────────────────────────────────────────────
def paste_text():
    if OS == "Linux":
        subprocess.run(["xdotool", "key", "--clearmodifiers", "ctrl+v"], check=False)
    elif OS == "Windows":
        import ctypes
        ctypes.windll.user32.keybd_event(0x11, 0, 0, 0)
        ctypes.windll.user32.keybd_event(0x56, 0, 0, 0)
        ctypes.windll.user32.keybd_event(0x56, 0, 0x0002, 0)
        ctypes.windll.user32.keybd_event(0x11, 0, 0x0002, 0)

# ── Device detection ───────────────────────────────────────────────────────
def detect_device():
    try:
        import torch
        if torch.cuda.is_available():
            return "cuda", "int8"
            # return "cuda", "float16"
    except ImportError:
        pass
    return "cpu", "int8"

device, compute_type = detect_device()

print(f"Loading model on {device.upper()}...")
model = WhisperModel(MODEL_SIZE, device=device, compute_type=compute_type)
print("Ready! Press [Ctrl+M] to start recording, press again to stop.")
print("Press Esc to quit.\n")

notify("Voice Typer", "Ready! Press Ctrl+M to start.", "low")
set_tray(ICON_IDLE, "Voice Typer - Ready")

# ── State ──────────────────────────────────────────────────────────────────
recording    = False
audio_chunks = []
pressed_keys = set()

stream = sd.InputStream(
    samplerate=SAMPLE_RATE, channels=1, dtype="float32",
    callback=lambda indata, f, t, s: audio_chunks.append(indata.copy()) if recording else None
)
stream.start()

# ── Transcribe & paste ─────────────────────────────────────────────────────
def transcribe_and_paste():
    if not audio_chunks:
        notify("Voice Typer", "No audio recorded.", "normal")
        set_tray(ICON_IDLE, "Voice Typer - Ready")
        return

    set_tray(ICON_PROCESSING, "Voice Typer - Transcribing...")
    notify("Voice Typer", "Transcribing...", "low")
    print("Transcribing...", end=" ", flush=True)

    audio = np.concatenate(audio_chunks, axis=0).flatten()
    segments, _ = model.transcribe(
        audio,
        language=LANGUAGE,
        beam_size=1,
        # beam_size=5,
        vad_filter=True,
        vad_parameters={"min_silence_duration_ms": 300},
    )

    text = " ".join(seg.text for seg in segments).strip()

    if text:
        print(f"Done: {text}")
        pyperclip.copy(text)
        paste_text()
        set_tray(ICON_DONE, "Voice Typer - Done")
        notify("Voice Typer", f"{text[:80]}{'...' if len(text) > 80 else ''}", "low")
        threading.Timer(2.0, lambda: set_tray(ICON_IDLE, "Voice Typer - Ready")).start()
    else:
        notify("Voice Typer", "No speech detected.", "normal")
        set_tray(ICON_IDLE, "Voice Typer - Ready")
        print("No speech detected.")

# ── Key listener ───────────────────────────────────────────────────────────
def normalize(key):
    if key in (keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
        return keyboard.Key.ctrl_l
    return key

def on_press(key):
    global recording, audio_chunks
    pressed_keys.add(normalize(key))

    if pressed_keys >= HOTKEY:
        pressed_keys.clear()
        if not recording:
            recording = True
            audio_chunks = []
            set_tray(ICON_RECORDING, "Voice Typer - Recording...")
            notify("Voice Typer", "Recording... (press Ctrl+M to stop)", "low")
            print("Recording...", end="\r", flush=True)
        else:
            recording = False
            print(" " * 50, end="\r")
            threading.Thread(target=transcribe_and_paste, daemon=True).start()

def on_release(key):
    pressed_keys.discard(normalize(key))

# ── Run ────────────────────────────────────────────────────────────────────
def start_listener():
    try:
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
    except Exception as e:
        print(f"Keyboard listener error: {e}")

threading.Thread(target=start_listener, daemon=True).start()

tray.run()
