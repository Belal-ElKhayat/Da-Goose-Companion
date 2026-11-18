"""Anti-Doomscroll Active Window Monitor for Da Duck Companion.
Monitors foreground window titles on Windows using the Win32 API (ctypes)
to detect social media / distraction platforms and scold the user after a set threshold.
"""

import ctypes
import os
import random
import sys
import time
from typing import List, Optional
from PyQt6.QtCore import QObject, QThread, pyqtSignal

# Pre-packaged witty scolding quips by platform
SCOLD_QUIPS = {
    "youtube": [
        "Quack! 🦆 You've been watching YouTube for {mins} minutes. Are you *really* researching tutorials?",
        "Look at you, lost in the algorithmic void of YouTube. What happened to that deadline?",
        "Another video essay about a show you don't even watch? Back to work, human!",
    ],
    "reddit": [
        "Quack! {mins} minutes on Reddit arguing with strangers? Your code misses you.",
        "Browsing r/all won't write your documentation. Close the tab!",
        "Downvoting won't upgrade your productivity stats. Get moving!",
    ],
    "twitter": [
        "Doomscrolling Twitter/X again? Your blood pressure must be through the roof.",
        "Quack! {mins} minutes of hot takes and doomposting. Close the bird app!",
        "There are no solutions on the feed, only rage-bait. Focus!",
    ],
    "x.com": [
        "Doomscrolling X again? Your blood pressure must be through the roof.",
        "Quack! {mins} minutes of hot takes and doomposting. Close the bird app!",
    ],
    "tiktok": [
        "Your attention span is evaporating by the microsecond. Close TikTok!",
        "Quack! {mins} minutes of vertical videos. Stand up and touch some grass!",
    ],
    "default": [
        "Ahem! You've been distracted on '{site}' for {mins} minutes straight. Didn't you have work?",
        "I'm judging you. Hard. Step away from '{site}' and finish your task!",
        "Quack! Distraction alert! {mins} minutes wasted. Shall I quack loudly until you close it?",
    ],
}


class WindowPoller:
    """Safely retrieves the title of the active foreground window using Win32 API."""

    def __init__(self):
        self.is_windows = sys.platform == "win32"
        if self.is_windows:
            self.user32 = ctypes.windll.user32
            self.kernel32 = ctypes.windll.kernel32

    def get_active_window_title(self) -> str:
        """Returns the active window title, or empty string on failure."""
        if not self.is_windows:
            return ""

        try:
            hwnd = self.user32.GetForegroundWindow()
            if not hwnd:
                return ""

            length = self.user32.GetWindowTextLengthW(hwnd)
            if length == 0:
                return ""

            buff = ctypes.create_unicode_buffer(length + 1)
            self.user32.GetWindowTextW(hwnd, buff, length + 1)
            return buff.value
        except Exception:
            return ""


class WindowMonitorWorker(QThread):
    """Background worker thread polling active window titles."""

    doomscroll_alert = pyqtSignal(str, int, str)  # (site_name, minutes_elapsed, quip)
    doomscroll_cleared = pyqtSignal()
    active_window_changed = pyqtSignal(str)

    def __init__(
        self,
        keywords: List[str],
        threshold_minutes: int = 10,
        check_interval_sec: float = 2.0,
        parent: Optional[QObject] = None,
    ):
        super().__init__(parent)
        self.poller = WindowPoller()
        self.keywords = [k.lower().strip() for k in keywords]
        self.threshold_seconds = threshold_minutes * 60
        self.check_interval_sec = check_interval_sec

        self._running = True
        self._enabled = True
        self._active_site: Optional[str] = None
        self._doom_seconds = 0.0
        self._last_alert_time = 0.0
        self._alert_cooldown = 120.0  # Alert every 2 minutes once threshold breached
        self._in_alert_state = False

    def update_settings(self, keywords: List[str], threshold_minutes: int, enabled: bool):
        """Update monitor settings dynamically."""
        self.keywords = [k.lower().strip() for k in keywords]
        self.threshold_seconds = max(60, threshold_minutes * 60)
        self._enabled = enabled
        if not enabled and self._in_alert_state:
            self._in_alert_state = False
            self.doomscroll_cleared.emit()

    def reset_timer(self):
        """Manually reset the doomscroll counter."""
        self._doom_seconds = 0.0
        if self._in_alert_state:
            self._in_alert_state = False
            self.doomscroll_cleared.emit()

    def stop(self):
        self._running = False
        self.wait(1000)

    def run(self):
        last_title = ""

        while self._running:
            try:
                time.sleep(self.check_interval_sec)

                if not self._enabled:
                    time.sleep(1.0)
                    continue

                title = self.poller.get_active_window_title()
                if title != last_title:
                    last_title = title
                    self.active_window_changed.emit(title)

                title_lower = title.lower()

                # Check if current window matches any doomscroll keyword
                matched_keyword: Optional[str] = None
                for kw in self.keywords:
                    if kw in title_lower:
                        matched_keyword = kw
                        break

                now = time.time()

                if matched_keyword:
                    self._active_site = matched_keyword
                    self._doom_seconds += self.check_interval_sec

                    # Check threshold breach
                    if self._doom_seconds >= self.threshold_seconds:
                        if not self._in_alert_state or (now - self._last_alert_time >= self._alert_cooldown):
                            self._in_alert_state = True
                            self._last_alert_time = now
                            mins = int(self._doom_seconds // 60)
                            quip = self._pick_quip(matched_keyword, mins)
                            self.doomscroll_alert.emit(matched_keyword.capitalize(), mins, quip)
                else:
                    # User is on a non-distracting window
                    if self._doom_seconds > 0:
                        # Gradual cool down
                        self._doom_seconds = max(0.0, self._doom_seconds - (self.check_interval_sec * 0.5))

                    if self._in_alert_state and self._doom_seconds < (self.threshold_seconds * 0.7):
                        self._in_alert_state = False
                        self.doomscroll_cleared.emit()

            except Exception as e:
                # Polling should never crash the companion thread
                time.sleep(2.0)

    def _pick_quip(self, site: str, mins: int) -> str:
        quips = SCOLD_QUIPS.get(site, SCOLD_QUIPS["default"])
        template = random.choice(quips)
        return template.format(site=site.capitalize(), mins=mins)
