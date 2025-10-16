# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**dictate** is a system-wide push-to-talk voice transcription tool that uses OpenAI's Whisper model to convert speech to text. It runs as a background service with global hotkey support and automatically inserts transcribed text into the focused window.

## Architecture

### Core Components

- **Audio Capture**: Uses `sounddevice` to capture 16kHz mono audio in real-time via callback (`audio_callback`)
- **Transcription Pipeline**: Thread-based architecture with `transcribe_audio()` running in daemon thread, processing queued audio chunks
- **Global Hotkey**: `pynput` keyboard listener detects Home key press/release system-wide (X11 only)
- **Text Insertion**: Multi-fallback strategy:
  1. `xdotool type` with window focus capture (primary)
  2. `pynput` keyboard controller (fallback)
- **Window Tracking**: Captures focused window ID at recording start (`target_window_id`) to ensure text goes to correct window

### State Management

All global state is thread-safe:
- `is_recording`: Protected by `recording_lock` (threading.Lock)
- `audio_queue`: Thread-safe queue for audio chunks
- `stop_flag`: Threading event for clean shutdown

### Key Implementation Details

1. **Home Key Detection**: Uses multiple detection methods (VK code 0x1008ff18, string matching, keyboard.Key.home) for reliability across different X11 configurations
2. **Recording Flow**: Press Home → capture window ID → start recording → release Home → transcribe → auto-paste to captured window
3. **Logging**: Dual-handler setup - DEBUG to `~/dictate.log`, INFO to console

## Development

### Dependencies

Install Python packages:
```bash
pip3 install -r requirements.txt
```

System dependencies (Ubuntu/Debian):
```bash
sudo apt-get install xclip xdotool libportaudio2
```

### Running

Basic:
```bash
./dictate
```

With options:
```bash
./dictate --model tiny        # Faster, less accurate
./dictate --no-notify         # No desktop notifications
./dictate --no-paste          # Clipboard only, no auto-paste
```

### Testing

Manual testing workflow:
1. Run `./dictate` in terminal
2. Click into any text field
3. Hold Home key, speak, release
4. Verify text appears and check `~/dictate.log` for debug info

### Platform Requirements

- **X11 required**: pynput global hotkeys don't work on Wayland
- Check session type: `echo $XDG_SESSION_TYPE` should output `x11`

## Configuration Constants

Located at top of `dictate` script:
- `SAMPLE_RATE = 16000`: Audio sample rate
- `BUFFER_SIZE = 1024`: Audio buffer size
- `DEFAULT_HOTKEY = '<home>'`: Hotkey (currently hardcoded to Home key)
- `LOG_FILE`: Log file location (`~/dictate.log`)

## Key Gotchas

1. **First transcription slowness**: Whisper model warmup - normal behavior
2. **Text insertion timing**: Multiple `time.sleep()` delays ensure clipboard/window focus stability
3. **Key repeat handling**: `on_press` ignores repeats when already recording to avoid multiple starts
4. **Language**: Hardcoded to English in transcription call (`language="en"`)
