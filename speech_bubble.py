"""Speech Bubble Widget for Da Goose Companion.
Animated speech bubble with typewriter effect, auto-dismiss, and proper
duration calculation so AI responses get enough time to be read.
"""

import math
from typing import Optional
from PyQt6.QtCore import QPointF, QRectF, Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QBrush, QColor, QFont, QPainter, QPainterPath, QPen
from PyQt6.QtWidgets import QWidget


def _calc_read_duration(text: str, ai_response: bool = False) -> float:
    """
    Returns how many seconds to display the bubble.
    AI responses get extra time since they're longer and more interesting.
    Rule of thumb: average reading speed ~200 words/min = 3.3 words/sec.
    We halve that for safety (1.65 words/sec), then add 2.5s buffer.
    """
    words = len(text.split())
    base = words / 1.65 + 2.5
    if ai_response:
        # Minimum 8 seconds, max 22 seconds for AI text
        return max(8.0, min(22.0, base))
    else:
        # Regular quips: minimum 4s, max 14s
        return max(4.0, min(14.0, base))


class SpeechBubble(QWidget):
    text_typing_finished = pyqtSignal()
    bubble_dismissed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self._full_text = ""
        self._displayed_text = ""
        self._char_index = 0
        self._is_visible = False
        self._opacity = 0.0
        self._is_ai_response = False

        self._type_timer = QTimer(self)
        self._type_timer.timeout.connect(self._on_type_tick)

        self._dismiss_timer = QTimer(self)
        self._dismiss_timer.setSingleShot(True)
        self._dismiss_timer.timeout.connect(self.hide_bubble)

        self._fade_timer = QTimer(self)
        self._fade_timer.timeout.connect(self._on_fade_tick)
        self._fade_target = 0.0
        self._duration_sec = 5.0

        self._font = QFont("Segoe UI", 10, QFont.Weight.Medium)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def say(self, text: str, duration_sec: Optional[float] = None,
            speed_ms: int = 26, ai_response: bool = False):
        """
        Display text with typewriter effect.
        Pass ai_response=True for Gemini replies to get generous read time.
        """
        self._type_timer.stop()
        self._dismiss_timer.stop()

        self._full_text = text.strip()
        self._displayed_text = ""
        self._char_index = 0
        self._is_ai_response = ai_response

        if duration_sec is None:
            self._duration_sec = _calc_read_duration(self._full_text, ai_response)
        else:
            self._duration_sec = duration_sec

        self._is_visible = True
        self._fade_target = 1.0
        self._fade_timer.start(16)
        self._type_timer.start(speed_ms)
        self.update()

    def hide_bubble(self):
        self._type_timer.stop()
        self._dismiss_timer.stop()
        self._fade_target = 0.0
        self._fade_timer.start(16)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self._char_index < len(self._full_text):
                # Instant reveal
                self._char_index = len(self._full_text)
                self._displayed_text = self._full_text
                self._type_timer.stop()
                self.text_typing_finished.emit()
                self._dismiss_timer.start(int(self._duration_sec * 1000))
                self.update()
            else:
                self.hide_bubble()
            event.accept()
        else:
            super().mousePressEvent(event)

    def _on_type_tick(self):
        if self._char_index < len(self._full_text):
            self._char_index += 1
            self._displayed_text = self._full_text[:self._char_index]
            self.update()
        else:
            self._type_timer.stop()
            self.text_typing_finished.emit()
            self._dismiss_timer.start(int(self._duration_sec * 1000))

    def _on_fade_tick(self):
        if self._fade_target > self._opacity:
            self._opacity = min(1.0, self._opacity + 0.1)
        elif self._fade_target < self._opacity:
            self._opacity = max(0.0, self._opacity - 0.1)
            if self._opacity <= 0.0:
                self._fade_timer.stop()
                self._is_visible = False
                self.bubble_dismissed.emit()

        if abs(self._opacity - self._fade_target) < 0.01:
            self._opacity = self._fade_target
            self._fade_timer.stop()

        self.update()

    def paintEvent(self, event):
        if not self._is_visible or self._opacity <= 0.0:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setOpacity(self._opacity)

        w, h = float(self.width()), float(self.height())
        tail_h = 12.0
        box = QRectF(6.0, 4.0, w - 12.0, h - 8.0 - tail_h)

        # Drop shadow
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(0, 0, 0, 40)))
        painter.drawRoundedRect(QRectF(box.x() + 1, box.y() + 2, box.width(), box.height()), 14.0, 14.0)

        # Bubble body
        bubble = QPainterPath()
        bubble.addRoundedRect(box, 13.0, 13.0)

        # Tail pointing to goose head
        tx = w * 0.60
        tail = QPainterPath()
        tail.moveTo(tx - 10.0, box.bottom())
        tail.lineTo(tx, box.bottom() + tail_h)
        tail.lineTo(tx + 6.0, box.bottom())
        tail.closeSubpath()

        full = bubble.united(tail)

        painter.setPen(QPen(QColor(255, 255, 255, 65), 1.3))
        painter.setBrush(QBrush(QColor(28, 30, 40, 238)))
        painter.drawPath(full)

        # Text
        painter.setFont(self._font)
        painter.setPen(QColor(245, 248, 255))
        pad = 10.0
        painter.drawText(
            QRectF(box.x() + pad, box.y() + pad - 2.0,
                   box.width() - pad * 2, box.height() - pad * 2 + 4.0),
            int(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter | Qt.TextFlag.TextWordWrap),
            self._displayed_text
        )
