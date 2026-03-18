# Karrot

**KDE Desktop Environment Narrator** - Capture screen text and listen to it with AI-powered narration.

![Karrot Logo](logo.png)

---

## What is Karrot?

**Karrot**

Like a parrot that repeats words, Karrot captures text from your screen and narrates it aloud. It's a KDE-first, Linux-exclusive accessibility tool designed for the KDE Plasma desktop environment.

### Key Features

- **Region Selection** - Use KDE Spectacle to select any screen area
- **OCR Extraction** - EasyOCR extracts text from screenshots
- **AI Narration** - VODER-powered Text-to-Speech or Voice Cloning
- **Dual Modes** - TTS with custom voice prompts or VC with voice cloning
- **Clipboard Integration** - Text automatically copied to clipboard
- **Organized Output** - OCR text and audio files saved with timestamps

---

## Quick Start

### Prerequisites

1. **VODER** - Install first: [VODER Repository](https://github.com/HAKORADev/VODER)
2. **Spectacle** - KDE screenshot tool (usually pre-installed)
3. **wl-clipboard** - Wayland clipboard utilities

### Installation

```bash
# Clone Karrot
git clone https://github.com/HAKORADev/Karrot.git
cd Karrot

# Install dependencies
pip install -r requirements.txt

# Run to generate config
python src/karrot.py
```

### Configuration

Edit `src/karrot.conf` to set your VODER path:

```ini
[karrot]
voder_path = "/home/user/VODER/src/voder.py"
mode = tts
voice_prompt = neutral, clear, professional narration voice
```

### Usage

1. Run: `python src/karrot.py`
2. Select a screen region with Spectacle
3. Wait for OCR and narration
4. Listen to the generated audio!

---

## System Requirements

| Requirement | Details |
|-------------|---------|
| **OS** | Linux with KDE Plasma |
| **Display** | Wayland |
| **Python** | 3.8+ |
| **RAM** | 4GB minimum (8GB recommended) |
| **Storage** | ~2GB for models |

---

## Dependencies

### Python Packages
- `easyocr` - OCR engine

### System Tools
- `spectacle` - KDE screenshot (region selection)
- `wl-clipboard` - Clipboard utilities (wl-copy)
- Audio player: `paplay`, `aplay`, `ffplay`, or `mpv`

### Required
- **VODER** - [GitHub Repository](https://github.com/HAKORADev/VODER)

---

## Output Structure

```
src/results/
├── ocr/
│   └── karrot_2026-03-19_14-30-45.txt    # Extracted text
└── narrator/
    └── karrot_2026-03-19_14-30-45.wav    # Narration audio
```

---

## Documentation

- **[Guide.md](Guide.md)** - Complete documentation and troubleshooting
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and changes

---

## License

Open-source software. See repository for details.

---

## Links

- **VODER:** https://github.com/HAKORADev/VODER
- **Issues:** https://github.com/HAKORADev/Karrot/issues

---

<p align="center">
  <b>Made with 🥕 by HAKORA</b>
</p>
