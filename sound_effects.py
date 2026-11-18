"""Procedural Sound Generator & Audio Player for Da Goose Companion.
Generates 12+ distinct comical 'WHAACK!' honks, bell rings, lighter flicks,
explosion booms, and crumb crunches in memory using Python's wave + struct modules.
Zero external audio files required!
"""

import io
import math
import random
import struct
import threading
import wave
from typing import Dict, List, Optional

try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False


class SoundFX:
    """Generates and plays dynamic sound effects."""

    _cached_wavs: Dict[str, bytes] = {}

    @classmethod
    def _create_wav(cls, samples: list, sample_rate: int = 22050) -> bytes:
        """Converts raw float samples (-1.0 to 1.0) into in-memory WAV byte string."""
        buf = io.BytesIO()
        with wave.open(buf, "wb") as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            int_samples = [int(max(-1.0, min(1.0, s)) * 32760) for s in samples]
            data = struct.pack(f"<{len(int_samples)}h", *int_samples)
            wav_file.writeframes(data)
        return buf.getvalue()

    # -------------------------------------------------------------------------
    # 12+ DIVERSE PROCEDURAL "WHAACK!" HONK SYNTHESIZERS
    # -------------------------------------------------------------------------
    @classmethod
    def get_whaack_loud(cls) -> bytes:
        """Classic loud comical WHAACK! Sharp attack, nasal screech, brass decay."""
        if "whaack_loud" in cls._cached_wavs:
            return cls._cached_wavs["whaack_loud"]

        sample_rate = 22050
        duration = 0.24
        num_samples = int(sample_rate * duration)
        samples = []

        for i in range(num_samples):
            t = i / sample_rate
            prog = t / duration

            # 'Whaack' vowel formant sweep: starts at 400Hz ('Wh'), shoots up to 740Hz ('AA'), drops to 620Hz ('CK')
            if prog < 0.20:
                freq = 380.0 + (prog / 0.20) * 360.0
            elif prog < 0.70:
                freq = 740.0 - ((prog - 0.20) / 0.50) * 80.0
            else:
                freq = 660.0 - ((prog - 0.70) / 0.30) * 90.0

            phase = 2.0 * math.pi * freq * t

            # Comical nasal timbre: strong 1st, 2nd, 3rd harmonics + sharp edge
            val = (
                0.48 * math.sin(phase) +
                0.32 * math.sin(2.0 * phase) +
                0.16 * math.sin(3.0 * phase) +
                0.08 * math.sin(4.0 * phase)
            )

            # Fast punchy attack
            env = (prog / 0.08) if prog < 0.08 else math.exp(-4.2 * (prog - 0.08))
            samples.append(val * env * 0.98)

        wav = cls._create_wav(samples, sample_rate)
        cls._cached_wavs["whaack_loud"] = wav
        return wav

    @classmethod
    def get_whaack_deep(cls) -> bytes:
        """Deep, grumpy, authoritative WHAACK!"""
        if "whaack_deep" in cls._cached_wavs:
            return cls._cached_wavs["whaack_deep"]

        sample_rate = 22050
        duration = 0.28
        num_samples = int(sample_rate * duration)
        samples = []

        for i in range(num_samples):
            t = i / sample_rate
            prog = t / duration
            freq = 280.0 + math.sin(prog * math.pi * 0.9) * 180.0
            phase = 2.0 * math.pi * freq * t
            val = 0.55 * math.sin(phase) + 0.35 * math.sin(2.0 * phase) + 0.15 * math.sin(3.0 * phase)
            env = (prog / 0.07) if prog < 0.07 else math.exp(-3.5 * (prog - 0.07))
            samples.append(val * env * 0.96)

        wav = cls._create_wav(samples, sample_rate)
        cls._cached_wavs["whaack_deep"] = wav
        return wav

    @classmethod
    def get_whaack_high(cls) -> bytes:
        """High-pitched, startled squeaky WHAACK!"""
        if "whaack_high" in cls._cached_wavs:
            return cls._cached_wavs["whaack_high"]

        sample_rate = 22050
        duration = 0.18
        num_samples = int(sample_rate * duration)
        samples = []

        for i in range(num_samples):
            t = i / sample_rate
            prog = t / duration
            freq = 600.0 + (prog ** 0.5) * 420.0
            phase = 2.0 * math.pi * freq * t
            val = 0.60 * math.sin(phase) + 0.30 * math.sin(2.0 * phase) + 0.10 * math.sin(4.0 * phase)
            env = math.exp(-6.0 * prog) if prog > 0.05 else (prog / 0.05)
            samples.append(val * env * 0.95)

        wav = cls._create_wav(samples, sample_rate)
        cls._cached_wavs["whaack_high"] = wav
        return wav

    @classmethod
    def get_whaack_angry_double(cls) -> bytes:
        """Rapid double fire: WHAACK-WHAACK!"""
        if "whaack_double" in cls._cached_wavs:
            return cls._cached_wavs["whaack_double"]

        sample_rate = 22050
        duration = 0.36
        num_samples = int(sample_rate * duration)
        samples = []

        for i in range(num_samples):
            t = i / sample_rate
            if t < 0.15:
                p = t / 0.15
                f = 500.0 + p * 220.0
                env = math.sin(math.pi * p)
            elif 0.19 <= t <= 0.34:
                p = (t - 0.19) / 0.15
                f = 540.0 + p * 240.0
                env = math.sin(math.pi * p) * 1.05
            else:
                f = 0.0
                env = 0.0

            phase = 2.0 * math.pi * f * t
            val = 0.50 * math.sin(phase) + 0.35 * math.sin(2.0 * phase) + 0.15 * math.sin(3.0 * phase) if f > 0 else 0
            samples.append(val * env * 0.95)

        wav = cls._create_wav(samples, sample_rate)
        cls._cached_wavs["whaack_double"] = wav
        return wav

    @classmethod
    def get_whaack_staccato(cls) -> bytes:
        """Ultra-fast, punchy WHACK!"""
        if "whaack_staccato" in cls._cached_wavs:
            return cls._cached_wavs["whaack_staccato"]

        sample_rate = 22050
        duration = 0.12
        num_samples = int(sample_rate * duration)
        samples = []

        for i in range(num_samples):
            t = i / sample_rate
            prog = t / duration
            freq = 620.0 - prog * 100.0
            phase = 2.0 * math.pi * freq * t
            val = 0.70 * math.sin(phase) + 0.30 * math.sin(2.0 * phase)
            env = math.exp(-12.0 * prog)
            samples.append(val * env * 0.95)

        wav = cls._create_wav(samples, sample_rate)
        cls._cached_wavs["whaack_staccato"] = wav
        return wav

    @classmethod
    def get_whaack_warble(cls) -> bytes:
        """Trembling, vibrating WHA-A-A-CK!"""
        if "whaack_warble" in cls._cached_wavs:
            return cls._cached_wavs["whaack_warble"]

        sample_rate = 22050
        duration = 0.28
        num_samples = int(sample_rate * duration)
        samples = []

        for i in range(num_samples):
            t = i / sample_rate
            prog = t / duration
            vibrato = math.sin(2.0 * math.pi * 28.0 * t) * 60.0
            freq = 550.0 + vibrato
            phase = 2.0 * math.pi * freq * t
            val = 0.50 * math.sin(phase) + 0.35 * math.sin(2.0 * phase) + 0.15 * math.sin(3.0 * phase)
            env = (prog / 0.08) if prog < 0.08 else math.exp(-4.0 * (prog - 0.08))
            samples.append(val * env * 0.95)

        wav = cls._create_wav(samples, sample_rate)
        cls._cached_wavs["whaack_warble"] = wav
        return wav

    @classmethod
    def get_whaack_scandalized(cls) -> bytes:
        """Ascending indignant WHAACK?! Like someone insulted its ancestors."""
        if "whaack_scandalized" in cls._cached_wavs:
            return cls._cached_wavs["whaack_scandalized"]

        sample_rate = 22050
        duration = 0.26
        num_samples = int(sample_rate * duration)
        samples = []

        for i in range(num_samples):
            t = i / sample_rate
            prog = t / duration
            freq = 380.0 + (prog ** 1.5) * 480.0
            phase = 2.0 * math.pi * freq * t
            val = 0.52 * math.sin(phase) + 0.33 * math.sin(2.0 * phase) + 0.15 * math.sin(3.0 * phase)
            env = math.sin(math.pi * (prog ** 0.8))
            samples.append(val * env * 0.95)

        wav = cls._create_wav(samples, sample_rate)
        cls._cached_wavs["whaack_scandalized"] = wav
        return wav

    @classmethod
    def get_whaack_furious(cls) -> bytes:
        """Raspy, aggressive, slightly distorted WHAACK!"""
        if "whaack_furious" in cls._cached_wavs:
            return cls._cached_wavs["whaack_furious"]

        sample_rate = 22050
        duration = 0.25
        num_samples = int(sample_rate * duration)
        samples = []

        for i in range(num_samples):
            t = i / sample_rate
            prog = t / duration
            freq = 660.0 - prog * 180.0
            phase = 2.0 * math.pi * freq * t
            # Overdriven square-ish clipping for furry distortion
            raw = math.sin(phase) * 1.5 + math.sin(2.5 * phase) * 0.6
            val = max(-1.0, min(1.0, raw))
            env = (prog / 0.05) if prog < 0.05 else math.exp(-4.5 * (prog - 0.05))
            samples.append(val * env * 0.92)

        wav = cls._create_wav(samples, sample_rate)
        cls._cached_wavs["whaack_furious"] = wav
        return wav

    @classmethod
    def get_whaack_trumpet(cls) -> bytes:
        """Majestic brass trumpet honk bugle!"""
        if "whaack_trumpet" in cls._cached_wavs:
            return cls._cached_wavs["whaack_trumpet"]

        sample_rate = 22050
        duration = 0.32
        num_samples = int(sample_rate * duration)
        samples = []

        for i in range(num_samples):
            t = i / sample_rate
            prog = t / duration
            freq = 520.0 + math.sin(prog * math.pi) * 80.0
            phase = 2.0 * math.pi * freq * t
            val = (
                0.40 * math.sin(phase) +
                0.30 * math.sin(2.0 * phase) +
                0.20 * math.sin(3.0 * phase) +
                0.10 * math.sin(5.0 * phase)
            )
            env = (prog / 0.12) if prog < 0.12 else math.exp(-3.0 * (prog - 0.12))
            samples.append(val * env * 0.95)

        wav = cls._create_wav(samples, sample_rate)
        cls._cached_wavs["whaack_trumpet"] = wav
        return wav

    @classmethod
    def get_whaack_squeak(cls) -> bytes:
        """Tiny hilarious clown squeak honk."""
        if "whaack_squeak" in cls._cached_wavs:
            return cls._cached_wavs["whaack_squeak"]

        sample_rate = 22050
        duration = 0.10
        num_samples = int(sample_rate * duration)
        samples = []

        for i in range(num_samples):
            t = i / sample_rate
            prog = t / duration
            freq = 950.0 + prog * 300.0
            phase = 2.0 * math.pi * freq * t
            val = math.sin(phase) * 0.9
            env = math.sin(math.pi * prog)
            samples.append(val * env * 0.9)

        wav = cls._create_wav(samples, sample_rate)
        cls._cached_wavs["whaack_squeak"] = wav
        return wav

    @classmethod
    def get_whaack_bass_boom(cls) -> bytes:
        """Sub-bass heavy mega honk."""
        if "whaack_bass" in cls._cached_wavs:
            return cls._cached_wavs["whaack_bass"]

        sample_rate = 22050
        duration = 0.35
        num_samples = int(sample_rate * duration)
        samples = []

        for i in range(num_samples):
            t = i / sample_rate
            prog = t / duration
            freq = 190.0 + math.exp(-prog * 5.0) * 220.0
            phase = 2.0 * math.pi * freq * t
            val = 0.70 * math.sin(phase) + 0.30 * math.sin(2.0 * phase)
            env = math.exp(-3.2 * prog)
            samples.append(val * env * 0.98)

        wav = cls._create_wav(samples, sample_rate)
        cls._cached_wavs["whaack_bass"] = wav
        return wav

    @classmethod
    def get_peep_gosling(cls) -> bytes:
        """Tiny cute baby gosling peep!"""
        sample_rate = 22050
        duration = 0.08
        num_samples = int(sample_rate * duration)
        samples = []
        for i in range(num_samples):
            t = i / sample_rate
            prog = t / duration
            freq = 1400.0 + math.sin(prog * math.pi) * 300.0
            val = math.sin(2.0 * math.pi * freq * t) * math.sin(math.pi * prog)
            samples.append(val * 0.85)
        return cls._create_wav(samples, sample_rate)

    @classmethod
    def get_bell_ding(cls) -> bytes:
        """Chime / bell ding when stealing items or ringing bell."""
        if "bell_ding" in cls._cached_wavs:
            return cls._cached_wavs["bell_ding"]

        sample_rate = 22050
        duration = 0.45
        num_samples = int(sample_rate * duration)
        samples = []

        for i in range(num_samples):
            t = i / sample_rate
            prog = t / duration
            # Bell harmonics (fundamental 1600Hz + non-harmonic bells)
            val = (
                0.50 * math.sin(2.0 * math.pi * 1580.0 * t) +
                0.30 * math.sin(2.0 * math.pi * 3160.0 * t) +
                0.20 * math.sin(2.0 * math.pi * 4740.0 * t)
            )
            env = math.exp(-7.0 * prog)
            samples.append(val * env * 0.9)

        wav = cls._create_wav(samples, sample_rate)
        cls._cached_wavs["bell_ding"] = wav
        return wav

    @classmethod
    def get_explosion_boom(cls) -> bytes:
        """Honk bomb explosion boom!"""
        if "explosion" in cls._cached_wavs:
            return cls._cached_wavs["explosion"]

        sample_rate = 22050
        duration = 0.55
        num_samples = int(sample_rate * duration)
        samples = []

        for i in range(num_samples):
            t = i / sample_rate
            prog = t / duration
            # Low rumble pitch drop + noise
            freq = 120.0 * math.exp(-prog * 4.0)
            noise = (random.random() * 2.0 - 1.0) * math.exp(-prog * 6.0) * 0.5
            val = math.sin(2.0 * math.pi * freq * t) * 0.6 + noise
            env = math.exp(-3.5 * prog)
            samples.append(val * env * 0.98)

        wav = cls._create_wav(samples, sample_rate)
        cls._cached_wavs["explosion"] = wav
        return wav

    @classmethod
    def get_chomp_wav(cls) -> bytes:
        """Crunch / munch sound."""
        if "chomp" in cls._cached_wavs:
            return cls._cached_wavs["chomp"]
        sample_rate = 22050
        duration = 0.14
        num_samples = int(sample_rate * duration)
        samples = []
        for i in range(num_samples):
            t = i / sample_rate
            prog = t / duration
            freq = 340.0 + math.sin(prog * math.pi * 3.5) * 160.0
            val = 0.65 * math.sin(2.0 * math.pi * freq * t) + 0.25 * math.sin(4.0 * math.pi * freq * t)
            env = math.exp(-10.0 * prog)
            samples.append(val * env * 0.9)
        wav = cls._create_wav(samples, sample_rate)
        cls._cached_wavs["chomp"] = wav
        return wav

    @classmethod
    def get_lighter_wav(cls) -> bytes:
        """Zippo lighter click and hiss."""
        if "lighter" in cls._cached_wavs:
            return cls._cached_wavs["lighter"]
        sample_rate = 22050
        duration = 0.18
        num_samples = int(sample_rate * duration)
        samples = []
        for i in range(num_samples):
            t = i / sample_rate
            prog = t / duration
            if prog < 0.2:
                val = math.sin(2.0 * math.pi * 2800.0 * t) * math.exp(-prog * 40.0)
            else:
                hiss = (random.random() * 2.0 - 1.0) * 0.35
                val = hiss * math.sin(math.pi * ((prog - 0.2) / 0.8))
            samples.append(val * 0.85)
        wav = cls._create_wav(samples, sample_rate)
        cls._cached_wavs["lighter"] = wav
        return wav

    # -------------------------------------------------------------------------
    # AUDIO PLAYER ENGINE
    # -------------------------------------------------------------------------
    @classmethod
    def play_wav_bytes_async(cls, wav_data: bytes) -> None:
        """Plays sound in background thread without cutting off buffer."""
        if not HAS_WINSOUND or not wav_data:
            return

        def _worker():
            try:
                winsound.PlaySound(wav_data, winsound.SND_MEMORY)
            except Exception:
                try:
                    winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
                except Exception:
                    pass

        threading.Thread(target=_worker, daemon=True).start()

    @classmethod
    def play_random_whaack(cls) -> str:
        """Picks and plays randomly from the 10+ distinct WHAACK! variations!"""
        generators = [
            ("LOUD WHAACK!", cls.get_whaack_loud),
            ("DEEP WHAACK!", cls.get_whaack_deep),
            ("SQUEAKY WHAACK!", cls.get_whaack_high),
            ("DOUBLE WHAACK!", cls.get_whaack_angry_double),
            ("PUNCHY WHACK!", cls.get_whaack_staccato),
            ("WARBLING WHA-A-CK!", cls.get_whaack_warble),
            ("SCANDALIZED WHAACK?!", cls.get_whaack_scandalized),
            ("FURIOUS WHAACK!", cls.get_whaack_furious),
            ("TRUMPET HONK!", cls.get_whaack_trumpet),
            ("CLOWN SQUEAK!", cls.get_whaack_squeak),
            ("BASS BOOM WHAACK!", cls.get_whaack_bass_boom),
        ]
        name, gen = random.choice(generators)
        cls.play_wav_bytes_async(gen())
        return name

    @classmethod
    def play_quack(cls) -> None:
        cls.play_random_whaack()

    @classmethod
    def play_chomp(cls) -> None:
        cls.play_wav_bytes_async(cls.get_chomp_wav())

    @classmethod
    def play_lighter(cls) -> None:
        cls.play_wav_bytes_async(cls.get_lighter_wav())

    @classmethod
    def play_bell(cls) -> None:
        cls.play_wav_bytes_async(cls.get_bell_ding())

    @classmethod
    def play_explosion(cls) -> None:
        cls.play_wav_bytes_async(cls.get_explosion_boom())

    @classmethod
    def play_peep(cls) -> None:
        cls.play_wav_bytes_async(cls.get_peep_gosling())

    @classmethod
    def get_snap_wav(cls) -> bytes:
        """Crisp dry snap sound (for breaking spaghetti!)."""
        if "snap" in cls._cached_wavs:
            return cls._cached_wavs["snap"]
        sample_rate = 22050
        duration = 0.08
        num_samples = int(sample_rate * duration)
        samples = []
        for i in range(num_samples):
            t = i / sample_rate
            prog = t / duration
            noise = (random.random() * 2.0 - 1.0) * math.exp(-prog * 45.0)
            tone = math.sin(2.0 * math.pi * 3200.0 * t) * math.exp(-prog * 35.0)
            samples.append((noise * 0.6 + tone * 0.4) * 0.95)
        wav = cls._create_wav(samples, sample_rate)
        cls._cached_wavs["snap"] = wav
        return wav

    @classmethod
    def get_pop_wav(cls) -> bytes:
        """Bubblegum pop sound!"""
        if "pop" in cls._cached_wavs:
            return cls._cached_wavs["pop"]
        sample_rate = 22050
        duration = 0.10
        num_samples = int(sample_rate * duration)
        samples = []
        for i in range(num_samples):
            t = i / sample_rate
            prog = t / duration
            freq = 400.0 + (1.0 - prog) * 600.0
            val = math.sin(2.0 * math.pi * freq * t) * math.exp(-prog * 18.0)
            samples.append(val * 0.92)
        wav = cls._create_wav(samples, sample_rate)
        cls._cached_wavs["pop"] = wav
        return wav

    @classmethod
    def play_snap(cls) -> None:
        cls.play_wav_bytes_async(cls.get_snap_wav())

    @classmethod
    def play_pop(cls) -> None:
        cls.play_wav_bytes_async(cls.get_pop_wav())

    @classmethod
    def play_scold(cls) -> None:
        cls.play_wav_bytes_async(cls.get_whaack_angry_double())

    # -------------------------------------------------------------------------
    # NEW PROCEDURAL AUDIO FOR SPECIAL SKINS & CHAOS MODES
    # -------------------------------------------------------------------------
    @classmethod
    def get_dj_beat_wav(cls) -> bytes:
        """Electronic 4-on-the-floor DJ dance beat: 808 kick, snare clap, hi-hats."""
        if "dj_beat" in cls._cached_wavs:
            return cls._cached_wavs["dj_beat"]
        sample_rate = 22050
        duration = 1.60  # 4 beats @ 150 BPM
        num_samples = int(sample_rate * duration)
        samples = [0.0] * num_samples

        # 4 beats (0.0s, 0.4s, 0.8s, 1.2s)
        for beat_idx, beat_t in enumerate([0.0, 0.4, 0.8, 1.2]):
            # 808 Kick on beat 1 and 3 (0.0s and 0.8s), plus syncopated kick at 1.0s
            if beat_idx in (0, 2):
                start_i = int(beat_t * sample_rate)
                kick_len = int(sample_rate * 0.28)
                for i in range(min(kick_len, num_samples - start_i)):
                    t = i / sample_rate
                    freq = 160.0 * math.exp(-t * 22.0) + 48.0
                    val = math.sin(2.0 * math.pi * freq * t) * math.exp(-t * 12.0)
                    samples[start_i + i] += val * 0.75

            # Snare Clap on beat 2 and 4 (0.4s and 1.2s)
            if beat_idx in (1, 3):
                start_i = int(beat_t * sample_rate)
                snare_len = int(sample_rate * 0.22)
                for i in range(min(snare_len, num_samples - start_i)):
                    t = i / sample_rate
                    noise = (random.random() * 2.0 - 1.0) * math.exp(-t * 18.0)
                    body = math.sin(2.0 * math.pi * 210.0 * t) * math.exp(-t * 22.0)
                    samples[start_i + i] += (noise * 0.65 + body * 0.35) * 0.70

        # Hi-hat ticks on every 8th note (every 0.2s)
        for hat_idx in range(8):
            start_i = int(hat_idx * 0.20 * sample_rate)
            hat_len = int(sample_rate * 0.05)
            for i in range(min(hat_len, num_samples - start_i)):
                t = i / sample_rate
                noise = (random.random() * 2.0 - 1.0) * math.exp(-t * 85.0)
                samples[start_i + i] += noise * 0.28

        wav = cls._create_wav(samples, sample_rate)
        cls._cached_wavs["dj_beat"] = wav
        return wav

    @classmethod
    def get_keyboard_clack_wav(cls) -> bytes:
        """Crisp mechanical keyboard keypress clack."""
        sample_rate = 22050
        duration = 0.05
        num_samples = int(sample_rate * duration)
        samples = []
        for i in range(num_samples):
            t = i / sample_rate
            noise = (random.random() * 2.0 - 1.0) * math.exp(-t * 90.0)
            tone = math.sin(2.0 * math.pi * (1400.0 + random.uniform(-100, 100)) * t) * math.exp(-t * 70.0)
            samples.append((noise * 0.6 + tone * 0.4) * 0.85)
        return cls._create_wav(samples, sample_rate)

    @classmethod
    def get_sip_wav(cls) -> bytes:
        """Liquid slurp/gulp sound for drinking coffee & boba."""
        sample_rate = 22050
        duration = 0.20
        num_samples = int(sample_rate * duration)
        samples = []
        for i in range(num_samples):
            t = i / sample_rate
            prog = t / duration
            freq = 550.0 - prog * 200.0 + math.sin(t * 80.0) * 80.0
            bubble = math.sin(2.0 * math.pi * freq * t)
            env = math.sin(prog * math.pi) * 0.85
            samples.append(bubble * env)
        return cls._create_wav(samples, sample_rate)

    @classmethod
    def get_laser_blast_wav(cls) -> bytes:
        """Sci-fi Super Saiyan beam blast charge."""
        if "laser_blast" in cls._cached_wavs:
            return cls._cached_wavs["laser_blast"]
        sample_rate = 22050
        duration = 0.45
        num_samples = int(sample_rate * duration)
        samples = []
        for i in range(num_samples):
            t = i / sample_rate
            prog = t / duration
            freq = 2400.0 * math.exp(-prog * 6.5) + 90.0
            tone = math.sin(2.0 * math.pi * freq * t)
            # Add distortion harmonics
            tone += 0.4 * math.sin(4.0 * math.pi * freq * t)
            buzz = (random.random() * 2.0 - 1.0) * 0.25 * (1.0 - prog)
            env = math.exp(-prog * 3.8)
            samples.append((tone + buzz) * env * 0.95)
        wav = cls._create_wav(samples, sample_rate)
        cls._cached_wavs["laser_blast"] = wav
        return wav

    @classmethod
    def get_megaphone_wav(cls) -> bytes:
        """Loud overdriven megaphone honk with reverb echo."""
        sample_rate = 22050
        duration = 0.38
        num_samples = int(sample_rate * duration)
        samples = []
        for i in range(num_samples):
            t = i / sample_rate
            prog = t / duration
            freq = 680.0 + math.sin(t * 35.0) * 120.0
            tone = math.sin(2.0 * math.pi * freq * t)
            # Hard clipping distortion (megaphone cone saturation)
            val = max(-0.85, min(0.85, tone * 2.4))
            env = math.exp(-prog * 4.5)
            samples.append(val * env * 0.95)
        return cls._create_wav(samples, sample_rate)

    @classmethod
    def play_dj_beat(cls) -> None:
        cls.play_wav_bytes_async(cls.get_dj_beat_wav())

    @classmethod
    def play_keyboard_clack(cls) -> None:
        cls.play_wav_bytes_async(cls.get_keyboard_clack_wav())

    @classmethod
    def play_sip(cls) -> None:
        cls.play_wav_bytes_async(cls.get_sip_wav())

    @classmethod
    def play_laser_blast(cls) -> None:
        cls.play_wav_bytes_async(cls.get_laser_blast_wav())

    @classmethod
    def play_megaphone(cls) -> None:
        cls.play_wav_bytes_async(cls.get_megaphone_wav())
