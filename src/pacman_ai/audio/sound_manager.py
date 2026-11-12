"""Audio management for win / lose sounds.

If the WAV files are present they are loaded via ``pygame.mixer.Sound``.
If NumPy is available a synthetic tone is generated as a fallback.
The module exposes ``play_win_sound`` and ``play_lose_sound`` functions that
are safe to call even when audio initialization failed.
"""

from __future__ import annotations

import os
from typing import Optional

import pygame

try:
    import numpy as np
    HAS_NUMPY = True
except Exception:
    HAS_NUMPY = False

WIN_SOUND: Optional[pygame.mixer.Sound] = None
LOSE_SOUND: Optional[pygame.mixer.Sound] = None


def _load_sounds() -> None:
    global WIN_SOUND, LOSE_SOUND
    try:
        if os.path.exists("win.wav"):
            WIN_SOUND = pygame.mixer.Sound("win.wav")
        if os.path.exists("lose.wav"):
            LOSE_SOUND = pygame.mixer.Sound("lose.wav")
        if WIN_SOUND or LOSE_SOUND:
            return
    except Exception:
        WIN_SOUND = LOSE_SOUND = None
    if HAS_NUMPY:
        try:
            def _make_tone(freq: float = 440, duration: float = 0.4, volume: float = 0.5):
                samplerate = 44100
                t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
                wave = (np.sin(2 * np.pi * freq * t) * (2 ** 15 - 1) * volume).astype(np.int16)
                stereo = np.column_stack([wave, wave])
                return pygame.sndarray.make_sound(stereo.copy())

            WIN_SOUND = _make_tone(660, 0.35, 0.5)
            LOSE_SOUND = _make_tone(220, 0.45, 0.6)
        except Exception:
            WIN_SOUND = LOSE_SOUND = None

# Load at module import – pygame must already be initialized by the caller.
_load_sounds()


def play_win_sound() -> None:
    if WIN_SOUND:
        WIN_SOUND.play()


def play_lose_sound() -> None:
    if LOSE_SOUND:
        LOSE_SOUND.play()
