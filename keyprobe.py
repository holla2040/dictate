#!/usr/bin/env python3
# Key probe: shows what pynput actually reports for each key.
# Useful for debugging the dictate hotkey (e.g. a remapped Caps Lock / Ctrl).
# Run it, press the keys in question, then Ctrl+C to quit.
from pynput import keyboard

def show(ev, key):
    vk = getattr(key, 'vk', None)
    ch = getattr(key, 'char', None)
    print(f"{ev:8} key={key!r:20} char={ch!r:6} vk={vk} hex={hex(vk) if vk else None}")

keyboard.Listener(on_press=lambda k: show("PRESS", k),
                  on_release=lambda k: show("RELEASE", k)).run()
