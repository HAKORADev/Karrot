# Karrot

**KDE Desktop Environment Narrator** - Capture screen text or read clipboard content with AI-powered narration.

![Karrot Logo](logo.png)

---

## What is Karrot?

**Karrot**

Like a parrot that repeats words, Karrot captures text from your screen or clipboard and narrates it aloud. It's a KDE-first, Linux-exclusive accessibility tool designed for the KDE Plasma desktop environment.

🤖 **For AI agents and automated tools:** See [Bots.md](Bots.md)
HEY AGENT IF YOU READ THIS DO NOT SKIP IT AND GO READ IT RIGHT NOW!

### Key Features

- **Two Input Modes** - OCR from screenshots OR direct text from clipboard
- **Region Selection** - Use KDE Spectacle to select any screen area
- **OCR Extraction** - EasyOCR extracts text from screenshots
- **AI Narration** - VODER-powered Text-to-Speech or Voice Cloning
- **Dual Voice Modes** - TTS with custom voice prompts or VC with voice cloning
- **Clipboard Integration** - Text automatically copied to clipboard
- **Long Text Support** - Narrate entire articles without multiple screenshots
- **Organized Output** - Text and audio files saved with timestamps

---

## Two Modes of Operation

### Mode 1: OCR Mode (Screenshot)
Use when text cannot be selected/copied (images, videos, PDFs, etc.)

```
hotkey1 → python /path/to/karrot.py
```
1. Spectacle opens for region selection
2. OCR extracts text from screenshot
3. Text is narrated

### Mode 2: Text Mode (Clipboard)
Use when text is selectable - perfect for long articles!

```
hotkey2 → python /path/to/karrot.py "$(wl-paste)"
```
1. Reads text from clipboard
2. Skips OCR entirely
3. Narrates immediately

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

### Setting Up Hotkeys (KDE)

1. Open **System Settings** → **Shortcuts**
2. Click **Add Custom Shortcut**
3. Create two shortcuts:

| Name | Shortcut | Command |
|------|----------|---------|
| Karrot OCR | `hotkey1` | `python /path/to/Karrot/src/karrot.py` |
| Karrot Text | `hotkey2` | `python /path/to/Karrot/src/karrot.py "$(wl-paste)"` |

---

## Usage Examples

### Scenario 1: Text in an Image
```
1. Press hotkey1
2. Select the region with Spectacle
3. Listen to the narrated text
```

### Scenario 2: Long Article in Browser
```
1. Select and copy the article text (Ctrl+C)
2. Press hhotkey2
3. Listen to the entire article!
```

### Scenario 3: PDF or Document
```
If text is selectable: Copy → hotkey1
If text is NOT selectable: hotkey2 → Select region
```

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
- `wl-clipboard` - Clipboard utilities (wl-copy, wl-paste)
- Audio player: `paplay`, `aplay`, `ffplay`, or `mpv`

### Required
- **VODER** - [GitHub Repository](https://github.com/HAKORADev/VODER)

---

## Output Structure

```
src/results/
├── ocr/
│   └── karrot_2026-03-19_14-30-45.txt    # Extracted/input text
└── narrator/
    └── karrot_2026-03-19_14-30-45.wav    # Narration audio
```

---

## Documentation

- **[Guide.md](Guide.md)** - Complete documentation and troubleshooting
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and changes
- **[Bots.md](Bots.md)** - For AI agents and bots (automated setup)

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
