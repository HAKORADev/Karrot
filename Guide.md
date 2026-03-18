# Karrot Documentation Guide

**Version:** 0.6.0  
**Last Updated:** March 19, 2026

---

## Table of Contents

1. [Introduction](#introduction)
2. [What is Karrot?](#what-is-karrot)
3. [Requirements](#requirements)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Usage](#usage)
7. [How It Works](#how-it-works)
8. [Output Files](#output-files)
9. [Troubleshooting](#troubleshooting)
10. [Dependencies Deep Dive](#dependencies-deep-dive)

---

## Introduction

Karrot is a KDE Desktop Environment narrator tool that captures text from your screen and narrates it aloud using AI-powered text-to-speech. The name "Karrot" combines "K" (for KDE) with "arrot" (from parrot, which repeats words) - perfectly describing what this tool does.

**Key Philosophy:**
- **KDE-First:** Designed specifically for the KDE Plasma desktop environment
- **Linux-Exclusive:** Built for Linux systems with Wayland support
- **Accessibility-Focused:** Helps users who prefer auditory content consumption
- **Privacy-Conscious:** All processing happens locally on your machine

---

## What is Karrot?

Karrot is a screen narrator that performs the following workflow:

1. **Region Selection:** Uses KDE's Spectacle tool to let you select a screen region
2. **Text Extraction:** Uses EasyOCR to extract text from the captured image
3. **Clipboard Copy:** Automatically copies extracted text to your clipboard
4. **Audio Generation:** Calls VODER to generate narration using TTS or Voice Cloning
5. **Playback:** Plays the generated audio using your system's audio player

**Use Cases:**
- Reading articles while resting your eyes
- Accessibility for users with visual impairments
- Multitasking - listen to content while doing other work
- Language learning - hear text pronounced clearly
- Content creation - generate voiceovers from screen text

---

## Requirements

### System Requirements

| Requirement | Description |
|-------------|-------------|
| **Operating System** | Linux with KDE Plasma desktop |
| **Display Server** | Wayland (wl-clipboard required) |
| **Python** | Python 3.8 or higher |
| **RAM** | 4GB minimum (8GB recommended for OCR) |
| **Storage** | ~2GB for models and dependencies |

### Software Dependencies

1. **VODER** - Must be installed first
   - Repository: https://github.com/HAKORADev/VODER
   - Follow VODER's installation guide completely

2. **Spectacle** - KDE screenshot tool
   - Usually pre-installed on KDE Plasma
   - Install: `sudo pacman -S spectacle` (Arch) or `sudo apt install spectacle` (Debian/Ubuntu)

3. **wl-clipboard** - Wayland clipboard utilities
   - Install: `sudo pacman -S wl-clipboard` (Arch) or `sudo apt install wl-clipboard` (Debian/Ubuntu)

4. **Audio Player** - At least one of:
   - paplay (PulseAudio) - typically pre-installed
   - aplay (ALSA) - typically pre-installed
   - ffplay (FFmpeg) - `sudo pacman -S ffmpeg`
   - mpv - `sudo pacman -S mpv`

---

## Installation

### Step 1: Install VODER

Karrot depends on VODER for audio generation. Install it first:

```bash
# Clone VODER
git clone https://github.com/HAKORADev/VODER.git
cd VODER

# Install VODER dependencies
pip install -r requirements.txt

# Test VODER installation
python src/voder.py --help
```

### Step 2: Install System Dependencies

**Arch Linux:**
```bash
sudo pacman -S spectacle wl-clipboard
```

**Debian/Ubuntu:**
```bash
sudo apt install spectacle wl-clipboard
```

### Step 3: Install Karrot

```bash
# Clone Karrot
git clone https://github.com/HAKORADev/Karrot.git
cd Karrot

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### Step 4: Configure Karrot

Run Karrot once to generate the default config:

```bash
python src/karrot.py
```

This will create `src/karrot.conf`. Edit this file to set your VODER path.

---

## Configuration

Karrot uses a configuration file located at `src/karrot.conf`. On first run, a default config is auto-generated.

### Configuration File Structure

```ini
[karrot]
# Path to VODER's voder.py file (REQUIRED)
voder_path = "/home/user/VODER/src/voder.py"

# Mode selection: tts or vc
mode = tts

# Voice prompt for TTS mode
voice_prompt = neutral, clear, professional narration voice

# Voice reference audio path for VC mode
voice_path = "/home/user/voice_reference.wav"
```

### Configuration Options

| Option | Required | Description |
|--------|----------|-------------|
| `voder_path` | **Yes** | Full path to VODER's voder.py file |
| `mode` | No | `tts` (Text-to-Speech) or `vc` (Voice Cloning) |
| `voice_prompt` | No | Voice description for TTS mode |
| `voice_path` | No | Path to reference audio for VC mode |

### Mode Details

#### TTS Mode (Text-to-Speech)
- Uses AI to generate speech from text
- Voice is defined by `voice_prompt` description
- Examples:
  - `neutral, clear, professional narration voice`
  - `deep male voice, calm and authoritative`
  - `young female voice, cheerful and energetic`

#### VC Mode (Voice Cloning)
- Clones a voice from a reference audio file
- Requires `voice_path` to point to a valid WAV/MP3 file
- If `voice_path` is invalid, falls back to TTS mode
- Best results with 10-30 seconds of clear speech

---

## Usage

### Basic Usage

1. **Run Karrot:**
   ```bash
   python src/karrot.py
   ```

2. **Select Region:**
   - Spectacle will open in region selection mode
   - Click and drag to select the area containing text
   - Press Enter or double-click to confirm

3. **Wait for Processing:**
   - OCR extracts text from the image
   - Text is copied to clipboard
   - VODER generates narration audio
   - Audio plays automatically

4. **Check Results:**
   - OCR text saved to: `src/results/ocr/karrot_TIMESTAMP.txt`
   - Audio saved to: `src/results/narrator/karrot_TIMESTAMP.wav`

### Creating a Desktop Entry (Optional)

Create a `.desktop` file for easy access:

```bash
nano ~/.local/share/applications/karrot.desktop
```

Content:
```ini
[Desktop Entry]
Name=Karrot
Comment=KDE Screen Narrator
Exec=python /path/to/Karrot/src/karrot.py
Icon=/path/to/Karrot/logo.png
Terminal=false
Type=Application
Categories=Utility;Accessibility;
```

### Setting a Keyboard Shortcut (KDE)

1. Open **System Settings** → **Shortcuts**
2. Click **Add Application** → Select Karrot
3. Set your preferred shortcut (e.g., `Meta+K`)

---

## How It Works

### Workflow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        KARROT WORKFLOW                       │
└─────────────────────────────────────────────────────────────┘

[Start] → [Spectacle Region Select] → [Image Saved to /tmp]
                                              │
                                              ▼
         [EasyOCR Text Extraction] ← ───────────
                  │
                  ▼
         [Text to Clipboard (wl-copy)]
                  │
                  ▼
         [Save OCR to results/ocr/]
                  │
                  ▼
         ┌────────────────┐
         │  Mode Selection│
         └────────┬───────┘
                  │
         ┌────────┴────────┐
         ▼                 ▼
    [TTS Mode]        [VC Mode]
         │                 │
         ▼                 ▼
    [voice_prompt]    [voice_path]
         │                 │
         └────────┬────────┘
                  ▼
         [Call VODER for Audio]
                  │
                  ▼
         [Save to results/narrator/]
                  │
                  ▼
         [Play Audio (paplay/aplay/etc)]
                  │
                  ▼
              [Complete]
```

### Technical Details

1. **Spectacle Integration:**
   - Called with `-r` (region mode), `-b` (background), `-n` (no notifications), `-o` (output path)
   - Creates temporary image at `/tmp/karrot_snippet.png`

2. **OCR Processing:**
   - Uses EasyOCR with English language model
   - GPU acceleration disabled by default (set `gpu=True` in code to enable)
   - Model loaded and unloaded per session to save memory

3. **VODER Integration:**
   - Text prefixed with character name: `Karrot: {text}`
   - Voice prompt also prefixed: `Karrot: {voice_prompt}`
   - Output parsed to find generated audio path

4. **Audio Playback:**
   - Tries multiple players in order: paplay, aplay, ffplay, mpv
   - First successful player is used

---

## Output Files

Karrot creates two types of output files, organized in the `src/results/` directory:

### OCR Results (`src/results/ocr/`)

- **Format:** Plain text files (`.txt`)
- **Naming:** `karrot_YYYY-MM-DD_HH-MM-SS.txt`
- **Content:** Extracted text from the screenshot
- **Example:** `karrot_2026-03-19_14-30-45.txt`

### Narrator Audio (`src/results/narrator/`)

- **Format:** WAV audio files
- **Naming:** `karrot_YYYY-MM-DD_HH-MM-SS.wav`
- **Content:** Generated narration audio
- **Example:** `karrot_2026-03-19_14-30-45.wav`

### File Management

Files accumulate over time. To clean up:

```bash
# Remove old OCR files (older than 30 days)
find src/results/ocr -name "*.txt" -mtime +30 -delete

# Remove old audio files (older than 30 days)
find src/results/narrator -name "*.wav" -mtime +30 -delete
```

---

## Troubleshooting

### Common Issues

#### "voder_path not configured!"

**Problem:** The config file is missing the VODER path.  
**Solution:** Edit `src/karrot.conf` and set the correct path to voder.py.

```ini
voder_path = "/home/youruser/VODER/src/voder.py"
```

#### "voder_path does not exist"

**Problem:** The specified path doesn't exist.  
**Solution:** Verify the path and ensure VODER is installed.

```bash
ls /path/to/VODER/src/voder.py
```

#### "voder_path must point to voder.py"

**Problem:** Path doesn't end with `voder.py`.  
**Solution:** Point to the actual voder.py file, not the directory.

#### "No text detected"

**Problem:** OCR couldn't extract text from the selection.  
**Solutions:**
- Ensure the selected region contains clear, readable text
- Try selecting a larger area
- Check if the text is in a supported language (English by default)

#### "No audio player found"

**Problem:** None of the supported audio players are installed.  
**Solution:** Install one of: paplay, aplay, ffplay, or mpv.

```bash
# Option 1: PulseAudio (usually pre-installed)
sudo pacman -S pulseaudio-utils

# Option 2: FFmpeg
sudo pacman -S ffmpeg

# Option 3: MPV
sudo pacman -S mpv
```

#### "VODER TTS failed"

**Problem:** VODER encountered an error during audio generation.  
**Solutions:**
- Check VODER is installed correctly
- Run VODER directly to test: `python /path/to/voder.py tts script "test" voice "neutral"`
- Check the VODER documentation for troubleshooting

#### Spectacle doesn't open

**Problem:** Spectacle fails to launch.  
**Solutions:**
- Ensure Spectacle is installed: `spectacle --version`
- Try running Spectacle manually: `spectacle -r`
- Check KDE/Qt environment variables

### Debug Mode

For more verbose output, run Karrot directly in a terminal:

```bash
python src/karrot.py
```

All debug messages will be printed to the console.

---

## Dependencies Deep Dive

### EasyOCR

EasyOCR is a Python module for extracting text from images. It supports 80+ languages and uses deep learning models.

- **Repository:** https://github.com/JaidedAI/EasyOCR
- **Models:** Downloaded automatically on first use (~500MB for English)
- **GPU Support:** Available (set `gpu=True` in code)

### VODER

VODER is HAKORA's TTS/VC tool that Karrot uses for audio generation.

- **Repository:** https://github.com/HAKORADev/VODER
- **Modes:** TTS (Text-to-Speech) and TTS+VC (Voice Cloning)
- **Character System:** Supports character prefixes for consistent voices

### Spectacle

Spectacle is KDE's default screenshot application with powerful region selection features.

- **Documentation:** https://docs.kde.org/stable5/en/spectacle/spectacle/
- **Used Flags:**
  - `-r`: Region mode (interactive selection)
  - `-b`: Background mode (no main window)
  - `-n`: No notifications
  - `-o`: Output file path

### wl-clipboard

Wayland clipboard utilities for copying text to the system clipboard.

- **Repository:** https://github.com/bugaevc/wl-clipboard
- **Used:** `wl-copy` command to copy OCR text to clipboard

---

## License

Karrot is open-source software. See the repository for license details.

## Contributing

Contributions are welcome! Please submit pull requests or open issues on GitHub.

## Support

For issues and questions:
- GitHub Issues: https://github.com/HAKORADev/Karrot/issues
- VODER Issues: https://github.com/HAKORADev/VODER/issues
