# Voice Typer — Hardware Settings Guide

Find your hardware below and copy the matching settings into the top of `voice_typer.py`.

---

## How to apply settings

Open `voice_typer.py` and edit this section at the top:

```python
MODEL_SIZE  = "..."   # change this
LANGUAGE    = None
SAMPLE_RATE = 16000
```

And this function:

```python
def detect_device():
    try:
        import torch
        if torch.cuda.is_available():
            return "cuda", "..."   # change compute_type here
    except ImportError:
        pass
    return "cpu", "int8"
```

And this line inside `transcribe_and_paste()`:

```python
beam_size=...,   # change this
```

---

## CPU Only (no GPU)

**Applies to:** Any machine without a dedicated GPU, or laptops with integrated graphics only.

```python
MODEL_SIZE   = "small"
compute_type = "int8"
beam_size    = 1
```

| Metric | Value |
|---|---|
| Speed (1 min audio) | 2-5 minutes |
| Accuracy | Good |
| RAM used | ~2GB |
| Best for | Occasional use, short clips only |

> Tip: Use `small` not `medium` — CPU is too slow for medium.

---

## GTX 1060 / GTX 1660 / GTX 1660 Ti / GTX 1660 Super (6GB VRAM)

**Applies to:** GTX 10xx and 16xx series — no Tensor Cores, no native float16 acceleration.

```python
MODEL_SIZE   = "medium"
compute_type = "int8"
beam_size    = 1
```

| Metric | Value |
|---|---|
| Speed (1 min audio) | 5-10 seconds |
| Accuracy | Very good |
| VRAM used | ~2GB |
| Best for | Daily use, clips up to 5 minutes |

> Note: Do NOT use float16 on GTX cards — it runs slower than int8 because GTX has no Tensor Cores.

---

## RTX 2060 / RTX 2070 / RTX 2080 (6-8GB VRAM)

**Applies to:** RTX 20xx series — has Tensor Cores, float16 works well.

```python
MODEL_SIZE   = "large-v3"
compute_type = "float16"
beam_size    = 3
```

| Metric | Value |
|---|---|
| Speed (1 min audio) | 5-8 seconds |
| Accuracy | Excellent |
| VRAM used | ~4GB |
| Best for | Daily use, clips up to 15 minutes |

---

## RTX 3050 / RTX 3060 (6-8GB VRAM)

**Applies to:** RTX 30xx entry/mid range.

```python
MODEL_SIZE   = "large-v3"
compute_type = "float16"
beam_size    = 3
```

| Metric | Value |
|---|---|
| Speed (1 min audio) | 4-6 seconds |
| Accuracy | Excellent |
| VRAM used | ~4GB |
| Best for | Daily use, clips up to 20 minutes |

---

## RTX 3070 / RTX 3080 / RTX 3090 (8-24GB VRAM)

**Applies to:** RTX 30xx high-end.

```python
MODEL_SIZE   = "large-v3"
compute_type = "float16"
beam_size    = 5
```

| Metric | Value |
|---|---|
| Speed (1 min audio) | 2-4 seconds |
| Accuracy | Excellent |
| VRAM used | ~5GB |
| Best for | Heavy use, long recordings |

---

## RTX 4060 / RTX 4070 (8-12GB VRAM)

**Applies to:** RTX 40xx mid range — Ada Lovelace arch, very efficient.

```python
MODEL_SIZE   = "large-v3"
compute_type = "float16"
beam_size    = 5
```

| Metric | Value |
|---|---|
| Speed (1 min audio) | 1-3 seconds |
| Accuracy | Excellent |
| VRAM used | ~5GB |
| Best for | Heavy use, near real-time |

---

## RTX 4080 / RTX 4090 (16-24GB VRAM)

**Applies to:** RTX 40xx high-end.

```python
MODEL_SIZE   = "large-v3"
compute_type = "float16"
beam_size    = 5
```

| Metric | Value |
|---|---|
| Speed (1 min audio) | < 1 second |
| Accuracy | Excellent |
| VRAM used | ~5GB |
| Best for | Any use case |

---

## Apple Silicon (M1 / M2 / M3)

**Applies to:** MacBook and Mac Mini with Apple chips.

```python
MODEL_SIZE   = "large-v3"
compute_type = "int8"
beam_size    = 3
```

Also change `detect_device()` to:

```python
def detect_device():
    try:
        import torch
        if torch.backends.mps.is_available():
            return "mps", "int8"
    except ImportError:
        pass
    return "cpu", "int8"
```

| Metric | Value |
|---|---|
| Speed (1 min audio) | 5-10 seconds |
| Accuracy | Excellent |
| RAM used | ~5GB unified memory |
| Best for | Daily use |

---

## Quick Comparison Table

| Hardware | MODEL_SIZE | compute_type | beam_size | Speed (1 min) |
|---|---|---|---|---|
| CPU only | small | int8 | 1 | 2-5 min |
| GTX 1060/1660 | medium | int8 | 1 | 5-10 sec |
| RTX 2060/2070/2080 | large-v3 | float16 | 3 | 5-8 sec |
| RTX 3050/3060 | large-v3 | float16 | 3 | 4-6 sec |
| RTX 3070/3080/3090 | large-v3 | float16 | 5 | 2-4 sec |
| RTX 4060/4070 | large-v3 | float16 | 5 | 1-3 sec |
| RTX 4080/4090 | large-v3 | float16 | 5 | < 1 sec |
| Apple M1/M2/M3 | large-v3 | int8 | 3 | 5-10 sec |

---

## Model sizes explained

| Model | Size on disk | Accuracy | Best for |
|---|---|---|---|
| tiny | 75MB | Basic | Testing only |
| base | 145MB | Okay | CPU, very old machines |
| small | 465MB | Good | CPU, low VRAM |
| medium | 1.5GB | Very good | GTX cards, 4-6GB VRAM |
| large-v3 | 3GB | Excellent | RTX cards, 6GB+ VRAM |

---

## VRAM not enough?

If you get a CUDA out-of-memory error, go one step down:

```
large-v3 → medium → small
float16  → int8
beam_size 5 → beam_size 1
```
