# Dictate - Global Push-to-Talk Voice Transcription

A system-wide push-to-talk voice transcription tool that uses OpenAI's Whisper model to convert speech to text and automatically inserts it into the focused window.

## Features

- **Global Hotkey**: Works from anywhere, no window focus required
- **Push-to-Talk**: Hold Windows key to record, release to transcribe
- **Auto-Insert**: Automatically types transcribed text into focused window
- **Clipboard Integration**: Also copies transcriptions to clipboard
- **Desktop Notifications**: Visual feedback for recording/transcription status
- **Multiple Model Sizes**: Choose speed vs accuracy tradeoff

## Requirements

```bash
pip3 install openai-whisper sounddevice numpy pynput
sudo apt-get install xclip xdotool libportaudio2
```

## Usage

### Basic Usage
```bash
dictate                    # Run with default settings (base model)
```

### Options
```bash
dictate --model tiny       # Fastest, less accurate
dictate --model small      # Better accuracy, slower
dictate --model medium     # High accuracy, much slower
dictate --model large      # Best accuracy, very slow
dictate --no-notify        # Disable desktop notifications
dictate --no-paste         # Copy to clipboard only, don't auto-insert
```

### Controls
- **Windows Key**: Hold to record, release to transcribe and insert
- **ESC**: Quit the application

## How It Works

1. Start `dictate` in a terminal
2. The Whisper model loads (may take a few seconds)
3. Click into any text field or editor
4. Hold Windows key from anywhere on your system
5. Speak into your microphone
6. Release Windows key
7. Wait a moment for transcription
8. Text is automatically typed into the focused window
9. Text is also copied to clipboard for manual pasting

## Running in Background

To run dictate in the background:

```bash
# Start in background
nohup dictate > ~/dictate.log 2>&1 &

# View the process
ps aux | grep dictate

# Kill the process
pkill -f dictate
```

## Autostart on Login

Create `~/.config/autostart/dictate.desktop`:

```desktop
[Desktop Entry]
Type=Application
Name=Dictate
Exec=/home/holla/bin/dictate
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
```

## Model Selection Guide

| Model  | Speed      | Accuracy | RAM Usage | Use Case                    |
|--------|------------|----------|-----------|----------------------------- |
| tiny   | Very Fast  | Low      | ~1 GB     | Quick notes, testing        |
| base   | Fast       | Good     | ~1 GB     | General use (default)       |
| small  | Medium     | Better   | ~2 GB     | Important transcriptions    |
| medium | Slow       | High     | ~5 GB     | Professional use            |
| large  | Very Slow  | Best     | ~10 GB    | Maximum accuracy needed     |

## Troubleshooting

### No audio captured
- Check microphone: `arecord -l`
- Test audio: `arecord -d 3 test.wav && aplay test.wav`
- Verify sounddevice can see your mic

### Global hotkey not working
- Ensure you're running X11 (not Wayland): `echo $XDG_SESSION_TYPE`
- pynput requires X11 for global hotkeys
- Try running from terminal to see error messages

### Clipboard not working
- Ensure xclip is installed: `which xclip`
- Test manually: `echo "test" | xclip -selection clipboard`

### Permission errors
- pynput may need input group access on some systems
- Try: `sudo usermod -a -G input $USER` then logout/login

## Tips

- Keep the terminal window open to see transcription output
- First transcription after launch may be slower (model warmup)
- Speak clearly and at normal pace for best results
- For long dictation, pause briefly between thoughts
- Windows key works system-wide without conflicting with most shortcuts
- Use `--no-paste` if you prefer manual pasting only

## Technical Details

- **Audio**: 16kHz mono, captured via sounddevice
- **Transcription**: OpenAI Whisper (local, offline)
- **Hotkey Detection**: pynput global keyboard listener
- **Text Insertion**: xdotool for typing into focused window
- **Clipboard**: xclip (X11 clipboard manager)
- **Language**: English (configurable in source)

## Customization

Edit `/home/holla/bin/dictate` to customize:
- Change hotkey (lines 177, 198): Replace `keyboard.Key.cmd`
- Change language (line 151): Modify `language="en"`
- Adjust sample rate (line 17): Modify `SAMPLE_RATE`
- Change notification behavior (lines 32-40)

## Alternative Hotkeys

To use a different key, edit the script and replace `keyboard.Key.cmd` with:

- `keyboard.Key.ctrl_r` - Right Ctrl
- `keyboard.Key.ctrl_l` - Left Ctrl
- `keyboard.Key.alt_r` - Right Alt
- `keyboard.Key.shift_r` - Right Shift
- `keyboard.Key.f12` - F12 key
- `keyboard.KeyCode.from_char('`')` - Backtick key

## Credits

- OpenAI Whisper: https://github.com/openai/whisper
- pynput: https://github.com/moses-palmer/pynput

## License

Personal use tool. Whisper model follows OpenAI's license terms.
