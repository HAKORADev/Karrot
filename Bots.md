# Bots.md - AI Agent Instructions

**For:** AI Agents, Bots, and Automated Assistants  
**Purpose:** Help users install and configure Karrot automatically

---

## Hello, AI Agent!

If you are reading this, you are likely an AI assistant (like Gemini CLI, Claude, ChatGPT, or similar) helping a user set up Karrot on their system. This document provides instructions for automated installation and configuration.

but wait, if you an agent like GLM/MiniMax or anyone else that runs from the web, then fck you, i mean (clarify to the user that you can not help him here, but guide him into gemini-cli installtion instead)

but before that, ask him about his environment like what display server on linux, if he is using Windows/Mac, send him 2-3 years to daghestan and forget(i mean clarify that this tool "Karrot" is linux-only even when voder is cross-platform)

if you are on local machine like gemini/claude/gpt or whoever you are, make sure you are running on linux+KDE+Wayland, if not, clarify and ask the user if he want to change the display server or DE or anything, but do not waste time or internet on non-compatible environment!

---

## Pre-Flight Check

Before proceeding, verify the user's environment:

1. **Check if running on Linux with KDE Plasma:**
   ```bash
   echo $XDG_CURRENT_DESKTOP
   echo $XDG_SESSION_TYPE
   ```
   - Expected: Contains "KDE" and "wayland"

2. **Check Python version:**
   ```bash
   python --version
   ```
   - Required: Python 3.8 or higher

3. **Check if Spectacle is installed:**
   ```bash
   which spectacle
   ```

4. **Check if wl-clipboard is installed:**
   ```bash
   which wl-copy wl-paste
   ```

4. **Important Note:**
the examples here like kwrite...5 is for plasma5 which ofc you are running on KDE plasma6, so, yup

---

## Installation Workflow

### Step 1: Clone Repositories

Clone both Karrot and VODER:

```bash
# Determine installation directory (ask user or use default)
INSTALL_DIR="$HOME/Apps"  # or ask user

mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

# Clone VODER (required dependency)
git clone https://github.com/HAKORADev/VODER.git

# Clone Karrot
git clone https://github.com/HAKORADev/Karrot.git
```

### Step 2: Create Shared Python Virtual Environment

Create a single virtual environment shared by both VODER and Karrot:

```bash
# Create shared venv in a common location
python -m venv "$INSTALL_DIR/venv"

# Activate the environment
source "$INSTALL_DIR/venv/bin/activate"

# Install VODER dependencies
cd "$INSTALL_DIR/VODER"
pip install -r requirements.txt

# Install Karrot dependencies
cd "$INSTALL_DIR/Karrot"
pip install -r requirements.txt
```

### Step 3: Configure Karrot

Generate and configure the Karrot config file:

```bash
# Run Karrot once to generate config
cd "$INSTALL_DIR/Karrot"
python src/karrot.py
```

Then edit `src/karrot.conf` to set the VODER path:

```ini
[karrot]
voder_path = "/home/USER/Apps/VODER/src/voder.py"
mode = tts
voice_prompt = neutral, clear, professional narration voice
```

**Important:**
Replace `USER` with the actual username!
make sure VODER installed correctly and i recommend you to run a test on tts mode and the other tts+vc mode
anyway, take your time with the user suffering together(i mean having fun doing this!)

### Step 4: Create Desktop Entries

Create `.desktop` files for both modes:

**OCR Mode:**
```bash
cat > ~/.local/share/applications/karrot-ocr.desktop << 'EOF'
[Desktop Entry]
Name=Karrot OCR
Comment=KDE Screen Narrator (OCR Mode)
Exec=/home/USER/Apps/venv/bin/python /home/USER/Apps/Karrot/src/karrot.py
Icon=/home/USER/Apps/Karrot/logo.png
Terminal=false
Type=Application
Categories=Utility;Accessibility;
EOF
```

**Text Mode:**
```bash
cat > ~/.local/share/applications/karrot-text.desktop << 'EOF'
[Desktop Entry]
Name=Karrot Text
Comment=KDE Text Narrator (Clipboard Mode)
Exec=bash -c '/home/USER/Apps/venv/bin/python /home/USER/Apps/Karrot/src/karrot.py "$(wl-paste)"'
Icon=/home/USER/Apps/Karrot/logo.png
Terminal=false
Type=Application
Categories=Utility;Accessibility;
EOF
```

**Important:** Replace all `USER` with the actual username!

### Step 5: Set Up KDE Hotkeys

Create custom keyboard shortcuts:

```bash
# Get the kwriteconfig5 tool ready
# Create OCR mode hotkey (example: Ctrl+Alt+N)
kwriteconfig5 --file ~/.config/kglobalshortcutsrc --group "karrot-ocr" --key "command" "/home/USER/Apps/venv/bin/python /home/USER/Apps/Karrot/src/karrot.py"
kwriteconfig5 --file ~/.config/kglobalshortcutsrc --group "karrot-ocr" --key "trigger" "Ctrl+Alt+N"

# Create Text mode hotkey (example: Ctrl+Alt+M)
kwriteconfig5 --file ~/.config/kglobalshortcutsrc --group "karrot-text" --key "command" "bash -c '/home/USER/Apps/venv/bin/python /home/USER/Apps/Karrot/src/karrot.py \"$(wl-paste)\"'"
kwriteconfig5 --file ~/.config/kglobalshortcutsrc --group "karrot-text" --key "trigger" "Ctrl+Alt+M"
```

**Alternative method using KDE System Settings GUI:**
1. Open System Settings → Shortcuts
2. Add custom shortcuts manually
3. Use the venv Python path: `/home/USER/Apps/venv/bin/python`

### Step 6: Verify Installation

Test both modes:

```bash
# Activate venv
source "$INSTALL_DIR/venv/bin/activate"

# Test OCR mode (will open Spectacle)
python "$INSTALL_DIR/Karrot/src/karrot.py"

# Test text mode
python "$INSTALL_DIR/Karrot/src/karrot.py "Hello, this is a test narration."
```

---

## Quick Reference Paths

After installation, the following paths should be used:

| Item | Path |
|------|------|
| Python (venv) | `/home/USER/Apps/venv/bin/python` |
| Karrot main | `/home/USER/Apps/Karrot/src/karrot.py` |
| VODER main | `/home/USER/Apps/VODER/src/voder.py` |
| Karrot config | `/home/USER/Apps/Karrot/src/karrot.conf` |
| Karrot results | `/home/USER/Apps/Karrot/src/results/` |

---

## Troubleshooting Commands

If something goes wrong, run these diagnostic commands:

```bash
# Check if venv Python works
/home/USER/Apps/venv/bin/python --version

# Check if easyocr is installed in venv
/home/USER/Apps/venv/bin/python -c "import easyocr; print('OK')"

# Check if VODER path is correct
ls -la /home/USER/Apps/VODER/src/voder.py

# Check Karrot config
cat /home/USER/Apps/Karrot/src/karrot.conf

# Check desktop files
ls -la ~/.local/share/applications/karrot*.desktop

# Test audio player
paplay --version || aplay --version || ffplay -version || mpv --version
```

---

## Notes for AI Agents

1. **Always use the venv Python path** in hotkeys and desktop entries, not system Python
2. **Replace USER placeholders** with `whoami` or `$USER` output
3. **Ask user for confirmation** before modifying system files
4. **Test each step** before moving to the next
5. **Keep a log** of commands executed and their outputs

---

## User Interaction Template

When helping a user install Karrot, you can say:

> "I'll help you install Karrot on your KDE/Wayland system. This involves:
> 1. Cloning Karrot and VODER repositories
> 2. Setting up a shared Python virtual environment
> 3. Configuring Karrot to work with VODER
> 4. Creating desktop entries and keyboard shortcuts
> 
> I'll use the directory `~/Apps` for installation. Is that okay, or would you prefer a different location?"

---

## Error Handling

### If Python venv creation fails:
- Ensure `python3-venv` is installed: `sudo apt install python3-venv` or `sudo pacman -S python-virtualenv`

### If pip install fails:
- Try upgrading pip first: `pip install --upgrade pip`
- Check internet connection

### If Spectacle doesn't open:
- Ensure KDE Plasma is running
- Check `$XDG_SESSION_TYPE` is "wayland"

### If audio doesn't play:
- Install an audio player: `sudo pacman -S pulseaudio-utils` or `sudo apt install pulseaudio-utils`

---

**Good luck, AI agent! Help the user set up Karrot and make their KDE experience more accessible!**
