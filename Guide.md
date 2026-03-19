# Karrot Documentation Guide

**Version:** 0.6.5  
**Last Updated:** March 19, 2026

---

## Table of Contents

1. [Introduction](#introduction)
2. [What is Karrot?](#what-is-karrot)
3. [Two Modes of Operation](#two-modes-of-operation)
4. [Requirements](#requirements)
5. [Installation](#installation)
6. ["Silly Way" Setup (Using AI Assistant)](#silly-way-setup-using-ai-assistant)
7. [Configuration](#configuration)
8. [Usage](#usage)
9. [How It Works](#how-it-works)
10. [Output Files](#output-files)
11. [Troubleshooting](#troubleshooting)
12. [Dependencies Deep Dive](#dependencies-deep-dive)

---

## Introduction

Karrot is a KDE Desktop Environment narrator tool that captures text from your screen or clipboard and narrates it aloud using AI-powered text-to-speech. The name "Karrot" combines "K" (for KDE) with "arrot" (from parrot, which repeats words ofc) - perfectly describing what this tool does.

**Key Philosophy:**
- **KDE-First:** Designed specifically for the KDE Plasma desktop environment
- **Linux-Exclusive:** Built for Linux systems with Wayland support
- **Accessibility-Focused:** Helps users who prefer auditory content consumption
- **Privacy-Conscious:** All processing happens locally on your machine

---

## What is Karrot?

Karrot is a screen and text narrator that supports two input modes:

### OCR Mode (Screenshot)
1. **Region Selection:** Uses KDE's Spectacle tool to let you select a screen region
2. **Text Extraction:** Uses EasyOCR to extract text from the captured image
3. **Clipboard Copy:** Automatically copies extracted text to your clipboard
4. **Audio Generation:** Calls VODER to generate narration using TTS or Voice Cloning
5. **Playback:** Plays the generated audio using your system's audio player

### Text Mode (Clipboard)
1. **Text Input:** Reads text directly from command line/clipboard
2. **Clipboard Copy:** Text is preserved in clipboard
3. **Audio Generation:** Calls VODER to generate narration
4. **Playback:** Plays the generated audio

**Use Cases:**
- Reading articles while resting your eyes
- Accessibility for users with visual impairments
- Multitasking - listen to content while doing other work
- Language learning - hear text pronounced clearly
- Content creation - generate voiceovers from screen text
- **Long articles** - Narrate entire documents without multiple screenshots
- **E-books and PDFs** - Copy text and listen immediately

---

## Two Modes of Operation

Karrot v0.6.5 introduces two distinct modes for maximum flexibility:

### Mode 1: OCR Mode (Screenshot)

**When to use:** Text cannot be selected or copied
- Text embedded in images
- Text in videos
- Scanned documents
- Non-selectable PDFs
- UI elements without copy functionality

**Hotkey1:**

**Command:**
```bash
python /path/to/Karrot/src/karrot.py
```

**Workflow:**
1. Press hotkey
2. Spectacle opens for region selection
3. Select area containing text
4. OCR extracts text
5. Audio plays automatically

### Mode 2: Text Mode (Clipboard)

**When to use:** Text is selectable and can be copied
- Web articles
- Documents with selectable text
- Email content
- Chat messages
- Code files
- Any long text content

**Hotkey2:**

**Command:**
```bash
python /path/to/Karrot/src/karrot.py "$(wl-paste)"
```

**Workflow:**
1. Select and copy text (Ctrl+C)
2. Press hotkey
3. Text is read from clipboard
4. Audio plays immediately (no OCR delay!)

### Comparison Table

| Feature | OCR Mode | Text Mode |
|---------|----------|-----------|
| Input | Screenshot | Clipboard text |
| Requires | Spectacle + OCR | wl-paste |
| Speed | Slower (OCR processing) | Faster (direct text) |
| Use case | Non-selectable text | Selectable text |
| Long text | Multiple captures needed | Single narration |
| Accuracy | Depends on image quality | 100% (already text) |

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

## "Silly Way" Setup (Using AI Assistant)

Don't want to read all this documentation? Let an AI assistant do it for you!

### Using Gemini CLI

1. **Install Node.js** (if not already installed):
   ```bash
   # Arch Linux
   sudo pacman -S nodejs npm
   
   # Debian/Ubuntu
   sudo apt install nodejs npm
   ```

2. **Install Gemini CLI**:
   ```bash
   npm install -g @google/gemini-cli
   ```

3. **Run Gemini**:
   ```bash
   gemini
   ```

4. **Login via Web**:
   - Select "Sign in with Google (OAuth login using your Google Account)"
   - Complete the login in your browser

5. **Ask Gemini to install Karrot**:
   ```
   Read the Guide.md in the current Karrot repo and help me install 
   and set up Karrot on my KDE/Wayland system. Also clone VODER and 
   set up a shared Python environment for both tools.
   ```

The AI will guide you through the entire process automatically!

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

### Setting Up Hotkeys (KDE)

Karrot works best with keyboard shortcuts. Set up two hotkeys for both modes:

1. Open **System Settings** → **Shortcuts**
2. Click **Edit** → **New** → **Global Shortcut** → **Command/URL**
3. Create two shortcuts:

#### OCR Mode Shortcut
- **Name:** Karrot OCR
- **Trigger:** `e.g Ctrl+Alt+N`
- **Action:** `python /path/to/Karrot/src/karrot.py`

#### Text Mode Shortcut
- **Name:** Karrot Text
- **Trigger:** `e.g Ctrl+Alt+M`
- **Action:** `python /path/to/Karrot/src/karrot.py "$(wl-paste)"`

> **Note:** Replace `/path/to/Karrot` with your actual installation path.

### Using OCR Mode

1. Press `Ctrl+Alt+N` (or run `python src/karrot.py`)
2. Spectacle opens in region selection mode
3. Click and drag to select the area containing text
4. Press Enter or double-click to confirm
5. Wait for processing:
   - OCR extracts text from the image
   - Text is copied to clipboard
   - VODER generates narration audio
   - Audio plays automatically

### Using Text Mode

1. Select text in any application
2. Copy to clipboard (`Ctrl+C`)
3. Press `Ctrl+Alt+M`
4. Wait for narration:
   - Text is read from clipboard
   - VODER generates narration
   - Audio plays automatically

### Example Scenarios

#### Scenario 1: Text in a YouTube Video
```
1. Pause video at the frame with text
2. Press Ctrl+Alt+N (OCR mode)
3. Select the text area
4. Listen to the extracted text
```

#### Scenario 2: Long Web Article
```
1. Select all text (Ctrl+A)
2. Copy (Ctrl+C)
3. Press Ctrl+Alt+M (Text mode)
4. Listen to the entire article!
```

#### Scenario 3: PDF Document
```
If text is selectable:
  - Copy text → Ctrl+Alt+M

If text is NOT selectable (scanned PDF):
  - Ctrl+Alt+N → Select region
```

### Creating a Desktop Entry (Optional)

Create a `.desktop` file for easy access from the application menu:

```bash
nano ~/.local/share/applications/karrot.desktop
```

Content:
```ini
[Desktop Entry]
Name=Karrot OCR
Comment=KDE Screen Narrator (OCR Mode)
Exec=python /path/to/Karrot/src/karrot.py
Icon=/path/to/Karrot/logo.png
Terminal=false
Type=Application
Categories=Utility;Accessibility;
```

For Text mode, create a second entry:
```ini
[Desktop Entry]
Name=Karrot Text
Comment=KDE Text Narrator (Clipboard Mode)
Exec=bash -c 'python /path/to/Karrot/src/karrot.py "$(wl-paste)"'
Icon=/path/to/Karrot/logo.png
Terminal=false
Type=Application
Categories=Utility;Accessibility;
```

---

## How It Works

### Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        KARROT WORKFLOW (v0.6.5)                              │
└─────────────────────────────────────────────────────────────────────────────┘

                              [Start]
                                 │
                 ┌───────────────┴───────────────┐
                 │      Check sys.argv           │
                 └───────────────┬───────────────┘
                                 │
          ┌──────────────────────┴──────────────────────┐
          │                                             │
   [No Arguments]                              [Arguments Provided]
          │                                             │
          ▼                                             ▼
   ┌──────────────┐                           ┌──────────────────┐
   │   OCR MODE   │                           │    TEXT MODE     │
   │  (Ctrl+Alt+N)│                           │   (Ctrl+Alt+M)   │
   └──────┬───────┘                           └────────┬─────────┘
          │                                            │
          ▼                                            ▼
[Spectacle Region Select]                    [Read from Clipboard]
          │                                            │
          ▼                                            │
   [Save Image]                                       │
          │                                            │
          ▼                                            │
  [EasyOCR Extraction]                                 │
          │                                            │
          └─────────────────┬──────────────────────────┘
                            │
                            ▼
                [Process Text & Save to results/ocr/]
                            │
                            ▼
                  [Copy to Clipboard (wl-copy)]
                            │
                            ▼
                   ┌────────────────┐
                   │  Voice Mode    │
                   └────────┬───────┘
                            │
                 ┌──────────┴──────────┐
                 ▼                     ▼
            [TTS Mode]           [VC Mode]
                 │                     │
                 ▼                     ▼
           [voice_prompt]        [voice_path]
                 │                     │
                 └──────────┬──────────┘
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

#### Mode Detection
- Karrot checks `sys.argv` at startup
- If no arguments: OCR mode (screenshot + OCR)
- If arguments provided: Text mode (direct text input)
- Text mode uses `$(wl-paste)` to read clipboard content

#### OCR Mode Specifics
1. **Spectacle Integration:**
   - Called with `-r` (region mode), `-b` (background), `-n` (no notifications), `-o` (output path)
   - Creates temporary image at `/tmp/karrot_snippet.png`
   - Image deleted after processing

2. **OCR Processing:**
   - Uses EasyOCR with English language model
   - GPU acceleration disabled by default (set `gpu=True` in code to enable)
   - Model loaded and unloaded per session to save memory

#### Text Mode Specifics
1. **Input Handling:**
   - Accepts text from command line arguments
   - Handles escape sequences (`\\n` → `\n`)
   - No temporary files created

2. **Speed Advantage:**
   - No OCR model loading
   - No image capture
   - Direct text processing

#### Shared Processing (Both Modes)
1. **VODER Integration:**
   - Text prefixed with character name: `Karrot: {text}`
   - Voice prompt also prefixed: `Karrot: {voice_prompt}`
   - Output parsed to find generated audio path

2. **Audio Playback:**
   - Tries multiple players in order: paplay, aplay, ffplay, mpv
   - First successful player is used

---

## Output Files

Karrot creates two types of output files, organized in the `src/results/` directory:

### Text Files (`src/results/ocr/`)

- **Format:** Plain text files (`.txt`)
- **Naming:** `karrot_YYYY-MM-DD_HH-MM-SS.txt`
- **Content:** 
  - OCR Mode: Extracted text from screenshot
  - Text Mode: Clipboard text that was narrated
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

#### Text mode not working (Ctrl+Alt+M)

**Problem:** Text mode hotkey doesn't work or shows empty text.  
**Solutions:**
- Ensure text is copied to clipboard before pressing the hotkey
- Check wl-clipboard is installed: `wl-paste --help`
- Test manually: `python src/karrot.py "test text"`
- Verify the hotkey command includes `$(wl-paste)` with proper quotes

#### Clipboard is empty in text mode

**Problem:** Karrot reports no text when using text mode.  
**Solutions:**
- Copy text first (Ctrl+C in the source application)
- Test clipboard content: `wl-paste`
- Some applications don't use the standard Wayland clipboard
- Try using OCR mode instead for non-standard applications

#### Hotkey doesn't trigger Karrot

**Problem:** Keyboard shortcut is set but nothing happens.  
**Solutions:**
- Check for conflicting shortcuts in KDE settings
- Verify the command path is correct (use absolute path)
- Test the command manually in a terminal
- Ensure Python is in your PATH

#### Long text causes VODER to fail

**Problem:** Very long texts cause issues.  
**Solutions:**
- VODER has text length limits
- Split long articles into smaller sections
- For extremely long content, consider using a dedicated TTS tool

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

Wayland clipboard utilities for clipboard operations.

- **Repository:** https://github.com/bugaevc/wl-clipboard
- **Used in Karrot:**
  - `wl-copy`: Copies OCR text to clipboard (both modes)
  - `wl-paste`: Reads clipboard content for Text mode

---

## License

Karrot is open-source software. See the repository for license details.

## Contributing

Contributions are welcome! Please submit pull requests or open issues on GitHub.

## Support

For issues and questions:
- GitHub Issues: https://github.com/HAKORADev/Karrot/issues
- VODER Issues: https://github.com/HAKORADev/VODER/issues
