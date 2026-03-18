#v0.6.5
import easyocr
import subprocess
import os
import re
import shutil
import gc
import sys
import configparser
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(SCRIPT_DIR, "results")
OCR_DIR = os.path.join(RESULTS_DIR, "ocr")
NARRATOR_DIR = os.path.join(RESULTS_DIR, "narrator")
TEMP_IMAGE = "/tmp/karrot_snippet.png"
CONFIG_FILE = os.path.join(SCRIPT_DIR, "karrot.conf")

KARROT_CHARACTER = "Karrot"

FALLBACK_MODE = "tts"
FALLBACK_VOICE_PROMPT = "neutral, clear, professional narration voice"

def create_default_config():
    config_content = """[karrot]
# Karrot Configuration File
# This file is auto-generated on first run.
# Edit the values below to customize Karrot's behavior.

# Path to VODER's voder.py file (REQUIRED)
# This must point to the actual voder.py file from the VODER repository.
# If this path is wrong, Karrot will crash.
# Use quotes around the path, especially if it contains spaces.
voder_path = "/home/user/VODER/src/voder.py"

# Mode selection: tts or vc
# tts = Text-to-Speech using voice_prompt (default)
# vc = Voice Cloning using a reference audio file (voice_path)
# If invalid, falls back to tts mode.
mode = tts

# Voice prompt for TTS mode
# Describe the voice you want Karrot to use for narration.
# Examples: "deep male voice, calm and authoritative" or "young female voice, cheerful and energetic"
# If empty or corrupted, falls back to default prompt.
voice_prompt = neutral, clear, professional narration voice

# Voice reference audio path for VC mode
# Path to a WAV/MP3 file containing a voice to clone.
# Only used when mode = vc
# If file doesn't exist or is invalid, falls back to tts mode with default voice_prompt.
# Use quotes around the path, especially if it contains spaces.
voice_path = "/home/user/voice_reference.wav"
"""
    with open(CONFIG_FILE, 'w') as f:
        f.write(config_content)
    print(f"Created default config at: {CONFIG_FILE}")

def strip_quotes(path):
    if path and len(path) >= 2:
        if (path.startswith('"') and path.endswith('"')) or \
           (path.startswith("'") and path.endswith("'")):
            return path[1:-1]
    return path

def load_config():
    config = {
        'voder_path': None,
        'mode': FALLBACK_MODE,
        'voice_prompt': FALLBACK_VOICE_PROMPT,
        'voice_path': None,
        'using_fallback_mode': False,
        'using_fallback_voice_prompt': False,
        'using_fallback_voice_path': False
    }

    if not os.path.exists(CONFIG_FILE):
        create_default_config()
        return config

    parser = configparser.ConfigParser()
    parser.read(CONFIG_FILE)

    section = 'karrot'
    if not parser.has_section(section):
        print(f"Warning: No [karrot] section in config, using defaults")
        return config

    voder_path = parser.get(section, 'voder_path', fallback='').strip()
    voder_path = strip_quotes(voder_path)
    if voder_path:
        config['voder_path'] = voder_path

    mode = parser.get(section, 'mode', fallback='').strip().lower()
    if mode in ('tts', 'vc'):
        config['mode'] = mode
    else:
        config['mode'] = FALLBACK_MODE
        config['using_fallback_mode'] = True

    voice_prompt = parser.get(section, 'voice_prompt', fallback='').strip()
    if voice_prompt and len(voice_prompt) > 0:
        config['voice_prompt'] = voice_prompt
    else:
        config['voice_prompt'] = FALLBACK_VOICE_PROMPT
        config['using_fallback_voice_prompt'] = True

    voice_path = parser.get(section, 'voice_path', fallback='').strip()
    voice_path = strip_quotes(voice_path)
    if voice_path and os.path.exists(voice_path):
        config['voice_path'] = voice_path
    else:
        config['voice_path'] = None
        config['using_fallback_voice_path'] = True
        if config['mode'] == 'vc':
            config['mode'] = FALLBACK_MODE
            config['using_fallback_mode'] = True

    return config

def ensure_directories():
    os.makedirs(OCR_DIR, exist_ok=True)
    os.makedirs(NARRATOR_DIR, exist_ok=True)

def run_ocr(image_path):
    print("Loading OCR model...")
    reader = easyocr.Reader(['en'], gpu=False)

    print("Extracting text...")
    results = reader.readtext(image_path, detail=0)
    text = "\n".join(results)

    print("Releasing OCR memory...")
    del reader
    gc.collect()

    return text if text.strip() else "[No text detected]"

def call_voder_tts(voder_path, text, voice_prompt):
    voder_dir = os.path.dirname(voder_path)

    script_with_char = f"{KARROT_CHARACTER}: {text}"
    voice_with_char = f"{KARROT_CHARACTER}: {voice_prompt}"

    cmd = [
        "python", voder_path, "tts",
        "script", script_with_char,
        "voice", voice_with_char
    ]

    print(f"Calling VODER TTS...")
    print(f"  Working dir: {voder_dir}")
    print(f"  Text length: {len(text)} chars")
    print(f"  Lines: {text.count(chr(10)) + 1}")
    if len(voice_prompt) > 50:
        print(f"  Voice: {voice_prompt[:50]}...")
    else:
        print(f"  Voice: {voice_prompt}")
    print("  (This may take a while on first run or slow systems...)")

    result = subprocess.run(
        cmd,
        cwd=voder_dir,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"VODER TTS failed with code {result.returncode}!")
        if len(result.stdout) > 500:
            print(f"  stdout: ...{result.stdout[-500:]}")
        else:
            print(f"  stdout: {result.stdout}")
        if len(result.stderr) > 500:
            print(f"  stderr: ...{result.stderr[-500:]}")
        else:
            print(f"  stderr: {result.stderr}")
        return None

    match = re.search(r'Output saved to:\s*(.+\.wav)', result.stdout)
    if match:
        output_path = match.group(1).strip()
        print(f"VODER output: {output_path}")
        return output_path

    print(f"Could not parse output path from VODER output:")
    if len(result.stdout) > 500:
        print(f"  ...{result.stdout[-500:]}")
    else:
        print(result.stdout)
    return None

def call_voder_vc(voder_path, text, voice_path):
    voder_dir = os.path.dirname(voder_path)

    script_with_char = f"{KARROT_CHARACTER}: {text}"
    target_with_char = f"{KARROT_CHARACTER}: {voice_path}"

    cmd = [
        "python", voder_path, "tts+vc",
        "script", script_with_char,
        "target", target_with_char
    ]

    print(f"Calling VODER TTS+VC...")
    print(f"  Working dir: {voder_dir}")
    print(f"  Text length: {len(text)} chars")
    print(f"  Lines: {text.count(chr(10)) + 1}")
    print(f"  Voice reference: {voice_path}")
    print("  (This may take a while on first run or slow systems...)")

    result = subprocess.run(
        cmd,
        cwd=voder_dir,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"VODER TTS+VC failed with code {result.returncode}!")
        if len(result.stdout) > 500:
            print(f"  stdout: ...{result.stdout[-500:]}")
        else:
            print(f"  stdout: {result.stdout}")
        if len(result.stderr) > 500:
            print(f"  stderr: ...{result.stderr[-500:]}")
        else:
            print(f"  stderr: {result.stderr}")
        return None

    match = re.search(r'Output saved to:\s*(.+\.wav)', result.stdout)
    if match:
        output_path = match.group(1).strip()
        print(f"VODER output: {output_path}")
        return output_path

    print(f"Could not parse output path from VODER output:")
    if len(result.stdout) > 500:
        print(f"  ...{result.stdout[-500:]}")
    else:
        print(result.stdout)
    return None

def play_audio(audio_path):
    if not os.path.exists(audio_path):
        print(f"Audio file not found: {audio_path}")
        return False

    players = [
        (["paplay", audio_path], "PulseAudio (paplay)"),
        (["aplay", audio_path], "ALSA (aplay)"),
        (["ffplay", "-nodisp", "-autoexit", audio_path], "FFplay"),
        (["mpv", "--no-video", audio_path], "MPV"),
    ]

    for cmd, name in players:
        try:
            result = subprocess.run(cmd, capture_output=True)
            if result.returncode == 0:
                print(f"Played audio using {name}")
                return True
        except FileNotFoundError:
            continue
        except Exception as e:
            print(f"{name} error: {e}")
            continue

    print("No audio player found! Install paplay, aplay, ffplay, or mpv.")
    return False

def process_text(text, config):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    ocr_file_path = os.path.join(OCR_DIR, f"karrot_{timestamp}.txt")
    with open(ocr_file_path, "w") as f:
        f.write(text)
    print(f"Text saved to: {ocr_file_path}")

    subprocess.run(["wl-copy"], input=text.encode())
    print("Text copied to clipboard.")

    if not text.strip() or text == "[No text detected]":
        subprocess.run(["notify-send", "Karrot Complete", "No text to narrate."])
        print("No text to narrate.")
        return

    print(f"\n[3/4] Narrating with VODER ({config['mode']} mode)...")
    subprocess.run(["notify-send", "Karrot", f"Generating narration ({config['mode']} mode)..."])

    voder_output = None

    if config['mode'] == 'vc' and config['voice_path']:
        voder_output = call_voder_vc(
            config['voder_path'],
            text,
            config['voice_path']
        )
    else:
        voder_output = call_voder_tts(
            config['voder_path'],
            text,
            config['voice_prompt']
        )

    if voder_output is None:
        print("Failed to generate narration!")
        subprocess.run(["notify-send", "Karrot Error", "Failed to generate narration!"])
        return

    narrator_file_path = os.path.join(NARRATOR_DIR, f"karrot_{timestamp}.wav")

    if os.path.exists(voder_output):
        shutil.move(voder_output, narrator_file_path)
        print(f"Audio moved to: {narrator_file_path}")
    else:
        print(f"VODER output not found at: {voder_output}")
        subprocess.run(["notify-send", "Karrot Error", "Audio generation failed!"])
        return

    print("\n[4/4] Playing narration...")
    subprocess.run(["notify-send", "Karrot", "Playing narration..."])
    play_audio(narrator_file_path)

    subprocess.run([
        "notify-send",
        "Karrot Complete",
        f"Text: {ocr_file_path}\nAudio: {narrator_file_path}"
    ])

    print(f"\n{'='*50}")
    print("✓ KARROT COMPLETE!")
    print(f"{'='*50}")
    print(f"  Text:   {ocr_file_path}")
    print(f"  Audio:  {narrator_file_path}")

def run_karrot_ocr(config):
    print("\n[1/4] Selection mode active...")
    subprocess.run(["spectacle", "-r", "-b", "-n", "-o", TEMP_IMAGE])

    if not os.path.exists(TEMP_IMAGE):
        print("Operation cancelled by user.")
        return

    print("\n[2/4] Processing with OCR...")
    text = run_ocr(TEMP_IMAGE)

    os.remove(TEMP_IMAGE)
    print("Temp image removed.")

    process_text(text, config)

def run_karrot_text(text_input, config):
    print("\n[1/4] Text input mode...")
    print("\n[2/4] Processing text...")

    text = text_input.replace('\\n', '\n')

    print(f"Received {len(text)} chars, {text.count(chr(10)) + 1} lines")

    process_text(text, config)

def main():
    ensure_directories()

    config = load_config()

    if config['voder_path'] is None:
        print("ERROR: voder_path not set in config!")
        print(f"Please edit: {CONFIG_FILE}")
        subprocess.run(["notify-send", "Karrot Error", "voder_path not configured!"])
        return

    if not os.path.exists(config['voder_path']):
        print(f"ERROR: voder_path does not exist: {config['voder_path']}")
        print(f"Please edit: {CONFIG_FILE}")
        subprocess.run(["notify-send", "Karrot Error", "voder_path is invalid!"])
        return

    if not config['voder_path'].endswith('voder.py'):
        print(f"ERROR: voder_path must point to voder.py file, got: {config['voder_path']}")
        subprocess.run(["notify-send", "Karrot Error", "voder_path must be voder.py!"])
        return

    print(f"Config loaded:")
    print(f"  voder_path: {config['voder_path']}")
    print(f"  mode: {config['mode']}")
    if len(config['voice_prompt']) > 50:
        print(f"  voice_prompt: {config['voice_prompt'][:50]}...")
    else:
        print(f"  voice_prompt: {config['voice_prompt']}")
    print(f"  voice_path: {config['voice_path']}")

    if config['using_fallback_mode']:
        print("  [Using fallback mode]")
    if config['using_fallback_voice_prompt']:
        print("  [Using fallback voice_prompt]")
    if config['using_fallback_voice_path']:
        print("  [Using fallback - voice_path invalid, switched to tts]")

    if len(sys.argv) > 1:
        text_input = " ".join(sys.argv[1:])
        run_karrot_text(text_input, config)
    else:
        run_karrot_ocr(config)

if __name__ == "__main__":
    main()
