# Changelog

All notable changes to Karrot will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.6.5] - 2026-03-19

### Added

- **Text Input Mode** - Direct text narration without OCR
  - Accept text from command line arguments
  - Perfect for long articles and documents
  - Use with `python karrot.py "$(wl-paste)"` to narrate clipboard content
- **Dual Hotkey Support** - Two modes for different use cases:
  - `Ctrl+Alt+N` → OCR Mode (screenshot + text extraction)
  - `Ctrl+Alt+M` → Text Mode (clipboard narration)
- **Long Text Support** - Narrate entire articles without multiple screenshots
- **Escape Sequence Handling** - Proper `\n` conversion in text input

### Changed

- **Refactored Architecture** - Modular design for both input modes
  - New `process_text()` function for shared text processing
  - New `run_karrot_ocr()` for screenshot/OCR mode
  - New `run_karrot_text()` for direct text input mode
  - Refactored `main()` to detect mode from command line arguments
- **Improved Workflow** - Skip unnecessary steps in text mode
  - No Spectacle launch in text mode
  - No OCR processing for direct text input

### Use Cases

| Scenario | Mode | Hotkey |
|----------|------|--------|
| Text in image/video | OCR | Ctrl+Alt+N |
| Selectable text (short) | Text | Copy → Ctrl+Alt+M |
| Selectable text (long article) | Text | Copy → Ctrl+Alt+M |
| PDF with selectable text | Text | Copy → Ctrl+Alt+M |
| PDF as image | OCR | Ctrl+Alt+N |

---

## [0.6.0] - 2026-03-19

### Added

- **Initial Release** of Karrot - KDE Desktop Environment Narrator
- **OCR Text Extraction** using EasyOCR for screen text recognition
- **Dual Audio Modes:**
  - TTS (Text-to-Speech) mode with customizable voice prompts
  - VC (Voice Cloning) mode for voice replication from reference audio
- **VODER Integration** - Seamless integration with VODER for AI-powered narration
- **Region Selection** via KDE Spectacle for precise screen area capture
- **Clipboard Support** - Automatic text copying using wl-copy (Wayland)
- **Configuration System** with auto-generated `karrot.conf` file
- **Output Organization:**
  - OCR results saved to `src/results/ocr/`
  - Narrator audio saved to `src/results/narrator/`
- **Desktop Notifications** via `notify-send` for status updates
- **Multi-Player Audio Support:**
  - PulseAudio (paplay)
  - ALSA (aplay)
  - FFplay
  - MPV
- **Character System** - Uses "Karrot" character prefix for consistent voice identity
- **Fallback Mechanisms:**
  - Fallback to TTS mode if VC mode fails
  - Default voice prompt if none specified
  - Error handling for missing dependencies

### Dependencies

- **EasyOCR** - OCR engine for text extraction
- **VODER** - Required for TTS/VC functionality
- **Spectacle** - KDE screenshot tool for region selection
- **wl-clipboard** - Wayland clipboard utilities

### Technical Features

- Automatic memory cleanup after OCR processing (garbage collection)
- Timestamped output files for easy organization
- Config validation with helpful error messages
- Quote handling in config file paths
- Temporary file management (auto-cleanup)

---
