# Changelog

All notable changes to Karrot will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## v0.6.0 - 2026-03-19

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
