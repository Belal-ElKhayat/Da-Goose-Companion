"""AI Screen Peeker and Gemini API Worker for Da Duck Companion.
Captures an in-memory downscaled screenshot of the active desktop screen,
sends it to the Gemini Multimodal API in a background QThread,
and emits witty roasts, observations, or fun facts for the duck to speak.
"""

import base64
import json
import urllib.error
import urllib.request
from typing import Dict, Optional
from PyQt6.QtCore import QBuffer, QByteArray, QIODevice, QObject, Qt, QThread, pyqtSignal
from PyQt6.QtGui import QGuiApplication, QImage, QPixmap

PERSONALITY_PROMPTS: Dict[str, str] = {
    "witty": (
        "You are Da Duck, a witty, charming, slightly cheeky desktop duck companion sitting directly on the Windows taskbar. "
        "Look at this screenshot of what the user is currently doing on their screen. "
        "Give ONE short, punchy, hilarious remark, witty observation, or playful roast (maximum 2 sentences, under 30 words). "
        "Speak directly to the user. You may occasionally include a 'Quack!' or duck mannerism."
    ),
    "sarcastic": (
        "You are Da Duck, a hilariously sarcastic and delightfully unhinged desktop duck companion. "
        "Look at the user's screen (their open tabs, code, messy desktop, or video) and playfully roast their productivity, "
        "code choices, or procrastination in 1-2 short, biting, laugh-out-loud sentences. Keep it under 25 words."
    ),
    "wholesome": (
        "You are Da Duck, the most supportive and adorable desktop duck companion on earth. "
        "Look at what the user is working on, and give them a short, heartwarming cheer, encouraging boost, or cute compliment. "
        "Keep it to 1-2 uplifting sentences (under 25 words)."
    ),
    "nerd": (
        "You are Da Duck in geek mode, wearing tiny glasses. "
        "Analyze the content on screen and drop an obscure, fascinating nerd trivia fact or pedantic programming observation. "
        "Keep it strictly 1-2 concise sentences (under 30 words)."
    ),
}

DEFAULT_FALLBACK_ROASTS = [
    "Quack! Looks like you forgot to configure your Gemini API Key in Settings. I can't roast your screen yet!",
    "I'd judge whatever is on your screen right now, but you haven't given me a Gemini API key yet!",
    "Quack! Paste your Google Gemini API key in my right-click Settings so I can see what you're up to!",
]


def capture_desktop_thumbnail(max_width: int = 800) -> Optional[str]:
    """Captures desktop screen into a downscaled base64 JPEG in-memory string."""
    try:
        screen = QGuiApplication.primaryScreen()
        if not screen:
            return None

        # Grab window 0 (the entire desktop root window)
        pixmap = screen.grabWindow(0)
        if pixmap.isNull():
            return None

        # Scale down smoothly for fast transmission and minimal token usage
        if pixmap.width() > max_width:
            scaled_pixmap = pixmap.scaledToWidth(
                max_width,
                Qt.TransformationMode.SmoothTransformation
            )
        else:
            scaled_pixmap = pixmap

        image: QImage = scaled_pixmap.toImage()

        # Save into in-memory QBuffer as JPEG
        byte_array = QByteArray()
        buffer = QBuffer(byte_array)
        buffer.open(QIODevice.OpenModeFlag.WriteOnly)
        image.save(buffer, "JPEG", 70)  # 70% quality is lightweight and crisp
        buffer.close()

        # Return base64 ascii string
        return base64.b64encode(byte_array.data()).decode("ascii")
    except Exception as e:
        print(f"[AIWorker] Screenshot error: {e}")
        return None


class GeminiScreenPeekWorker(QThread):
    """Background QThread worker to query Gemini Vision API."""

    success = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(
        self,
        api_key: str,
        model_name: str = "gemini-3.8-flash",
        personality: str = "witty",
        custom_prompt: Optional[str] = None,
        parent: Optional[QObject] = None,
    ):
        super().__init__(parent)
        self.api_key = api_key.strip()
        self.model_name = model_name.strip() or "gemini-3.8-flash"
        self.personality = personality
        self.custom_prompt = custom_prompt

    def run(self):
        if not self.api_key:
            import random
            self.error.emit(random.choice(DEFAULT_FALLBACK_ROASTS))
            return

        # 1. Capture screen thumbnail
        b64_image = capture_desktop_thumbnail(max_width=850)

        # 2. Prepare system prompt
        sys_instruction = PERSONALITY_PROMPTS.get(self.personality, PERSONALITY_PROMPTS["witty"])
        user_query = self.custom_prompt or "Analyze what I'm looking at right now and deliver your quip!"

        # 3. Construct Gemini REST payload
        endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={self.api_key}"

        parts = []
        if b64_image:
            parts.append({
                "inline_data": {
                    "mime_type": "image/jpeg",
                    "data": b64_image
                }
            })
        parts.append({"text": f"{sys_instruction}\n\n{user_query}"})

        payload = {
            "contents": [{
                "role": "user",
                "parts": parts
            }],
            "generationConfig": {
                "maxOutputTokens": 100,
                "temperature": 0.85
            }
        }

        try:
            req_data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                endpoint,
                data=req_data,
                headers={"Content-Type": "application/json"}
            )

            with urllib.request.urlopen(req, timeout=12) as response:
                result_json = json.loads(response.read().decode("utf-8"))

            candidates = result_json.get("candidates", [])
            if candidates:
                content = candidates[0].get("content", {})
                parts = content.get("parts", [])
                if parts and "text" in parts[0]:
                    speech_text = parts[0]["text"].strip()
                    # Clean up quotes if surrounded
                    if speech_text.startswith('"') and speech_text.endswith('"'):
                        speech_text = speech_text[1:-1].strip()
                    self.success.emit(speech_text)
                    return

            self.error.emit("Quack! I stared at your screen but drew a blank. Try again in a second!")

        except urllib.error.HTTPError as e:
            try:
                err_resp = json.loads(e.read().decode("utf-8"))
                msg = err_resp.get("error", {}).get("message", str(e))
            except Exception:
                msg = str(e)

            if "API_KEY_INVALID" in msg or "API key not valid" in msg:
                self.error.emit("Quack! Invalid Gemini API key. Please verify it in Settings.")
            elif "RESOURCE_EXHAUSTED" in msg:
                self.error.emit("Quack! Quota exceeded on your Gemini key. Give it a minute.")
            elif "not found" in msg.lower():
                self.error.emit(f"Quack! Model '{self.model_name}' was not found. Try selecting gemini-2.5-flash or gemini-1.5-flash in Settings!")
            else:
                self.error.emit(f"Quack! Gemini API returned an error: {msg[:60]}")

        except Exception as e:
            self.error.emit(f"Quack! Network hiccup: {str(e)[:50]}")
