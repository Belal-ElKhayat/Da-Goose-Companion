"""Main Companion Window — Da Goose Companion.
Features:
- Windows System Tray Integration (Hidden Icons Area ^) with QSystemTrayIcon
- Doomscroll Escalation & Boss Chase Mini-Game (Angry WHAACK every 20s, gets off chair, run to click-close)
- 5 Chaos Modes: Untitled Goose Theft, Super Saiyan Rage, Gosling Parade, Honk Bomb, Goose DJ
- 11+ Customizable Skins and 22+ Procedural Idle Animations
"""

import math
import random
import time
from typing import Optional
from PyQt6.QtCore import QPoint, QRect, QRectF, QSize, Qt, QTimer
from PyQt6.QtGui import (
    QAction,
    QBrush,
    QColor,
    QCursor,
    QGuiApplication,
    QIcon,
    QImage,
    QMouseEvent,
    QPainter,
    QPen,
    QPixmap,
)
from PyQt6.QtWidgets import QMenu, QMessageBox, QSystemTrayIcon, QWidget

from ai_worker import GeminiScreenPeekWorker
from config_manager import ConfigManager
from goose_painter import SKINS, GoosePainter
from settings_dialog import SettingsDialog
from sound_effects import SoundFX
from speech_bubble import SpeechBubble
from window_monitor import WindowMonitorWorker

IDLE_QUIPS = [
    "Honk! Just keeping your taskbar warm and aerodynamic.",
    "Did you know? Geese fly in V-formation to reduce air resistance. Very efficient.",
    "Hydrate, un-hunch your shoulders, and touch grass—in that order.",
    "I'm watching your code. No pressure. Honk.",
    "If you feed me a breadcrumb, I'll keep quiet about your browser history.",
    "Every great programmer has an equally great desk companion.",
    "*quietly judges your open tabs*",
    "Peace was never an option... but high productivity is! 🪿",
    "Honk! I may look peaceful on this chair, but my honk reaches 120 decibels.",
    "Your monitor has great resolution. Makes my feathers look sharp.",
]

SKIN_QUIPS = {
    "classic": IDLE_QUIPS,
    "smoking": [
        "*takes a slow drag* Another day, another unhandled exception.",
        "They told me geese shouldn't smoke. I honked at them.",
        "*sighs in gray plumage* Coding is stressful today.",
        "Watching you debug is hard work. *puffs smoke*",
        "*exhales a perfect smoke ring* Keep going, human.",
        "I've seen legacy codebases that would turn any bird's feathers gray.",
        "*flicks lighter* Got a flame? Debugging is cold out here on the taskbar.",
        "Back in my pond, we didn't have async/await. We had patience.",
    ],
    "coder": [
        "git commit -m 'Fixed everything. Probably.' 💻",
        "Rubber goose debugging: explain the algorithm to me step by step.",
        "Stack Overflow is my true co-author. Honk.",
        "Compiling... It worked on my machine, I swear!",
        "Refactoring in production. What could go wrong? *honk*",
        "Tabs vs spaces? Real geese use single-feather indentation.",
        "My mini vector laptop has 64GB of virtual RAM. Peak specs.",
        "404: Motivation not found. Retrying in 5 seconds.",
        "I don't always test my code, but when I do, I do it in production.",
    ],
    "rubber_duck": [
        "Squeak! The legendary Rubber Duck is ready for debugging!",
        "*squeeeeeak* Walk me through your loops, I'm all ears.",
        "Float mode activated! Zero critical bugs detected so far.",
        "Bright yellow, squishy, and ready to listen. Squeak!",
        "Who needs complicated AI when you have a classic bath duck on your taskbar?",
        "Squeak squeak! That variable name is suspiciously ambiguous.",
    ],
    "cooker": [
        "WHAACK! This code is RAW! Where's the lamb sauce?! 🍳",
        "Chef Goose says: season your functions with pinch of salt and comments!",
        "Simmering the backend API... exquisite flavor profile.",
        "Don't rush the build! Good code needs time to bake in the oven.",
        "Order up! One hot, freshly-served unit test pass!",
        "A 5-star Michelin commit right there. Delicious!",
    ],
    "detective": [
        "The magnifying glass reveals a suspicious null pointer at line 42. 🕵️",
        "Elementary, my friend: the culprit is always an off-by-one error.",
        "The case of the vanishing semicolons is almost solved...",
        "Trench coat on, fedora tilted. Justice for unhandled exceptions!",
        "I have deduced that you haven't stretched in the last hour.",
        "A footprint on the taskbar... could it be a rogue daemon process?",
    ],
    "ninja": [
        "Shhh... A stealth goose strikes in silence. *silent whaack* 🥷",
        "Vanishing into the shadows of your taskbar!",
        "My shurikens are vector-sharp and compile in zero milliseconds.",
        "A true master coder leaves no footprints in the git blame history.",
        "Shadow clone jutsu: 10 geese debugging simultaneously!",
        "Silent as a feather, deadly as a segfault.",
    ],
    "royal": [
        "By royal decree of the Goose King, this pull request shall be merged! 👑",
        "Bow before the golden crown! All breadcrumbs belong to the throne.",
        "My kingdom for clean indentation and zero memory leaks!",
        "Royal plumage inspection: everything is magnificent.",
        "You may continue typing in our royal presence, mortal.",
        "We knight you: Sir Debugger of the Broken Taskbar!",
    ],
    "cyberpunk": [
        "Neural link synchronized. Visor HUD reading 100% wattage. ⚡",
        "Wake up samurai, we have legacy monolithic code to burn.",
        "Neon cyan glow on the taskbar. Chrome aesthetic to the max.",
        "Overclocking the Goose CPU to 5.2 GHz! *pulse*",
        "Cyber-wings deployed. Infiltrating the mainframe... Honk.",
        "High tech, low plumage. Let's breach the firewall.",
    ],
    "wizard": [
        "Hocus pocus, abracadabra, cast away the syntax errors! 🧙✨",
        "By the power of my starry hat, I grant you clean compilation!",
        "A wizard is never late with a release. He commits precisely when he means to.",
        "You shall not pass... without passing all the unit tests!",
        "Ancient goose alchemy: turning caffeine directly into working code.",
        "I sense great magic in this repository... or a massive memory leak.",
    ],
    "coffee": [
        "*CHUG* Espresso shot #4 kicking in! My wings are vibrating! ☕",
        "More coffee! The taskbar runs on dark roast!",
        "Decaf? We don't speak of such dark arts here. Double espresso please!",
        "My heart rate is synchronized with your typing speed!",
        "Coffee level: 100%. Productivity level: OVER 9000!",
        "Sleep is just an arbitrary interrupt. Drink more brew!",
    ],
}

IDLE_ACTION_QUIPS = {
    "spaghetti": [
        "*CRACK!* Italian chefs are weeping. Perfectly snapped spaghetti! 🍝",
        "Snap! Breaking raw spaghetti is my favorite culinary crime.",
    ],
    "phone_scroll": [
        "Just checking GooseBook... 99+ notifications from the pond. 📱",
        "*scrolling* Hmm, duck memes are subpar today. Honk.",
    ],
    "boba": [
        "*slurp* Tapioca pearls are top-tier goose fuel. 🧋",
        "Mmm, brown sugar boba! Don't look at my vector calories.",
    ],
    "juggle": [
        "Look ma, no hands! Just vector wings juggling apples! 🍎",
        "Catch, toss, catch! Clumsiness is not in my codebase.",
    ],
    "yawn_stretch": [
        "*yaaawn* Coding is exhausting when you don't have opposable thumbs.",
        "*big stretch* Ahhh, wing cramps are the worst.",
    ],
    "ramen": [
        "*slurp* Authentic taskbar ramen! Extra noodles, no bugs. 🍜",
        "Careful! Don't spill the warm broth on the taskbar registry!",
    ],
    "rubiks_cube": [
        "Solving Rubik's cube in O(1)... and done. Next puzzle, please. 🎲",
        "Red, green, white... simple math for a big-brained goose.",
    ],
    "coin_flip": [
        "*flick* Heads: write unit tests. Tails: push straight to main! 🪙",
        "*ting* The coin of destiny has landed on heads!",
    ],
    "guitar": [
        "Anyway, here's 'Wonderwall' in WHAACK-major! 🎸🎶",
        "*strum strum* A little acoustic solo for your debugging session.",
    ],
    "bubblegum": [
        "*chew chew* Watch me blow the biggest vector bubble! 🎈",
        "*POP* ...right all over my feathers. Worth it.",
    ],
    "polaroid": [
        "*CLICK! FLASH!* Smile! Adding this to my Desk Hall of Fame! 📸",
        "Captured your focused coder face in crisp 4K vector!",
    ],
    "magnifying_glass": [
        "Elementary! The bug is located between the chair and keyboard. 🔍",
        "Investigating the suspicious lack of comments in your code...",
    ],
    "pushups": [
        "1... 2... 3! Gotta keep the wings swole for the next sprint! 💪",
        "Pushup time! No pain, no plumage gain!",
    ],
    "fidget_spinner": [
        "*whirrrrr* My dopamine receptors are thoroughly satisfied.",
        "Spin to win! Peak taskbar operational efficiency.",
    ],
    "deal_with_it": [
        "*puts on shades* Deal with it. Zero merge conflicts today. 😎",
        "🕶️ Too cool for unresolved compile errors.",
    ],
    "hula_hoop": [
        "Look at that centrifugal goose motion! Pure physics! ⭕",
        "Hula-hooping on an office chair: an official Olympic discipline.",
    ],
    "watch_check": [
        "Tick-tock. Is it lunch time or commit time yet? ⌚",
        "*taps watch* Exactly goose past four. Stay focused!",
    ],
    "binoculars": [
        "Scouting ahead... I see green passing test suites in your future! 🔭",
        "Scanning the horizon for incoming pull requests...",
    ],
    "pizza": [
        "*munch* Pizza slice on the clock. Best perk of being a desk pet! 🍕",
        "Pepperoni power! NOM NOM NOM.",
    ],
    "laser_chase": [
        "MUST... CATCH... THE RED DOT! WHAACK! 🔴",
        "That laser dot is taunting me! Get back here!",
    ],
    "magic_rabbit": [
        "Ta-da! Out of an empty top hat comes a floppy bunny! 🎩🐰",
        "A little stage magic to brighten your busy taskbar.",
    ],
    "sneeze": [
        "*ACHOOO!* WHAACK! Excuse me, floating dust particle.",
        "*sniff* Feather allergy? But I AM feathers!",
    ],
}

POKE_QUIPS = [
    "WHAACK! Hey, watch the feathers!",
    "Honk! That tickles!",
    "Poke me again and I'll steal your mouse cursor!",
    "Whaack! I'm on duty, no poking the goose!",
    "Boop! Beak sensor recalibrated.",
    "Did you need something or just admiring my plumage? *whaack*",
    "Honk! I'm a professional companion, not a stress ball!",
    "WHAACK! Keep your hands on the keyboard, human!",
    "Careful! My swivel chair is finely balanced!",
]

DRAG_QUIPS = [
    "Wheeeeeee! Taskbar sightseeing tour!",
    "Hold on to your feathers!",
    "Relocating to prime monitor real estate!",
    "WHAACK! Mind the velocity!",
    "Turbulence! Fasten your seatbelts!",
]

BOUNCE_QUIPS = [
    "BOING! Elastic goose physics!",
    "Oof! Hit the monitor border!",
    "WHAACK! Ricochet champion!",
    "Nice toss! 10/10 for trajectory.",
]

SKIN_SWITCH_GREETINGS = {
    "classic": "Clean white feathers and orange beak. Classic perfection! 🪿",
    "smoking": "*lights up* Ah... Back in business. What's the code damage today? 🚬",
    "coder": "Glasses on, vector laptop ready. Let's write some code! 💻",
    "rubber_duck": "Squeeeeak! Classic yellow bath duck on duty! 🦆",
    "cooker": "Chef Goose reporting to the kitchen! Bon appétit! 🍳",
    "detective": "The game is afoot! Let's solve these bugs! 🕵️",
    "ninja": "Stealth mode engaged. You won't even hear me honk. 🥷",
    "royal": "The King has arrived! Sound the royal trumpets! 👑",
    "cyberpunk": "Cyber-visor online. Neon city awaits! ⚡",
    "wizard": "Starry robes equipped! Let the spellcraft begin! 🧙",
    "coffee": "CAFFEINE INJECTED! Let's GOOOOO! ☕",
}

EAT_QUIPS = [
    "NOM NOM NOM! 10/10 vector crumb.",
    "Honk! Delicious pixelated carbs!",
    "Energy restored. Plumage approved.",
    "Munch munch... exquisite breadcrumb, human.",
    "Crunch crunch! You are officially my favorite human.",
    "Breadcrumb absorbed! +50 Goose Stamina!",
]


def create_tray_icon() -> QIcon:
    """Generates an in-memory 64x64 cute goose icon for the Windows system tray."""
    img = QImage(64, 64, QImage.Format.Format_ARGB32_Premultiplied)
    img.fill(QColor(0, 0, 0, 0))
    p = QPainter(img)
    p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    # Background circle
    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(QBrush(QColor("#FFA04D")))
    p.drawEllipse(QRectF(2, 2, 60, 60))
    # Goose head silhouette
    p.setBrush(QBrush(QColor("#FFFFFF")))
    p.drawEllipse(QRectF(16, 12, 32, 32))
    # Orange beak
    p.setBrush(QBrush(QColor("#E67328")))
    p.drawRoundedRect(QRectF(38, 22, 18, 10), 3.0, 3.0)
    # Beady eye
    p.setBrush(QBrush(QColor("#111827")))
    p.drawEllipse(QRectF(32, 20, 5, 5))
    p.end()
    return QIcon(QPixmap.fromImage(img))


class GooseWindow(QWidget):
    """The floating goose companion window anchored to the Windows taskbar."""

    def __init__(self, config_manager: ConfigManager):
        super().__init__()
        self.cfg = config_manager
        self._ai_worker: Optional[GeminiScreenPeekWorker] = None

        # Frameless, tool window, translucent background
        flags = Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool
        if self.cfg.get("always_on_top", True):
            flags |= Qt.WindowType.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating, True)

        self.resize(320, 270)

        # Master Vector Painter Engine
        self.painter_engine = GoosePainter(skin_key=self.cfg.get("goose_skin", "classic"))
        self.painter_engine.on_idle_action_started = self._on_idle_action_speech

        # Speech bubble
        self.speech_bubble = SpeechBubble(self)
        self.speech_bubble.setGeometry(10, 10, 300, 130)
        self.speech_bubble.text_typing_finished.connect(self._on_speech_finished)
        self.speech_bubble.bubble_dismissed.connect(self._on_bubble_dismissed)

        # Drag & Physics
        self._is_dragging = False
        self._drag_start = QPoint()
        self._drag_distance = 0.0
        self._last_mouse_x = 0
        self._vel_x = 0.0
        self._target_x = 0.0
        self._friction = 0.90
        self._bounce = 0.55

        # Rapid Click Rage Combo
        self._click_timestamps = []

        # Doomscroll Escalation & Rampage Chase State
        self._doomscroll_active = False
        self._doomscroll_start_time = 0.0
        self._doomscroll_last_warning_time = 0.0
        self._doomscroll_target_site = ""
        self._rampage_active = False
        self._rampage_speed = 7.0
        self._rampage_direction = 1.0

        # Inactivity & Sleep
        self._last_interaction = time.time()
        self._manually_sleeping = False
        self._sleep_threshold = 180.0

        # Animation & Physics Timers
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self._anim_tick)
        self.anim_timer.start(28)

        self.phys_timer = QTimer(self)
        self.phys_timer.timeout.connect(self._physics_tick)
        self.phys_timer.start(20)

        # Idle chatter timer - frequent spontaneous banter every 22-45s
        self.chatter_timer = QTimer(self)
        self.chatter_timer.timeout.connect(self._idle_chatter)
        self.chatter_timer.start(random.randint(22_000, 45_000))

        # AI timer
        self.ai_timer = QTimer(self)
        self.ai_timer.timeout.connect(self.trigger_ai_peek)
        self._update_ai_timer()

        # Anti-Doomscroll Monitor Worker
        self._init_monitor()

        # System Tray Icon (Hidden icons notification area ^)
        self._init_tray_icon()

        # Screen anchoring
        screen = QGuiApplication.primaryScreen()
        if screen:
            screen.availableGeometryChanged.connect(lambda _: self._anchor())

        self._anchor()
        QTimer.singleShot(1000, self._greet)

    # ------------------------------------------------------------------
    # SYSTEM TRAY INTEGRATION (Hidden Icons Tray ^)
    # ------------------------------------------------------------------
    def _init_tray_icon(self):
        """Initializes the Windows system tray icon in the hidden icons area."""
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(create_tray_icon())
        self.tray_icon.setToolTip("Da Goose Companion 🪿")

        # Tray Context Menu
        tray_menu = QMenu()
        tray_menu.setStyleSheet("""
            QMenu { background:#1E2028; color:#F3F4F6; border:1px solid #374151;
                    border-radius:8px; padding:6px; font-family:'Segoe UI',sans-serif; font-size:13px; }
            QMenu::item { padding:7px 22px 7px 12px; border-radius:4px; }
            QMenu::item:selected { background:#374151; color:#FFD23F; }
        """)

        toggle_act = tray_menu.addAction("👁️ Toggle / Show Da Goose")
        toggle_act.triggered.connect(self._toggle_show)

        peek_act = tray_menu.addAction("🪿 Ask Da Goose (AI Peek)")
        peek_act.triggered.connect(self.trigger_ai_peek)

        spin_act = tray_menu.addAction("🔄 Spin Swivel Chair!")
        spin_act.triggered.connect(self._spin)

        # Chaos Submenu
        chaos_menu = tray_menu.addMenu("⚡ Chaos Modes")
        chaos_menu.addAction("🔔 Steal Something!").triggered.connect(self._steal_item)
        chaos_menu.addAction("🐣 Call Baby Goslings").triggered.connect(self._toggle_goslings)
        chaos_menu.addAction("💣 Drop Honk Bomb").triggered.connect(self._drop_honk_bomb)
        chaos_menu.addAction("🔥 Super Saiyan Rage!").triggered.connect(self._trigger_super_rage)

        # Skins Submenu
        skin_menu = tray_menu.addMenu("🎨 Goose Skins")
        for key, val in SKINS.items():
            skin_menu.addAction(val["name"]).triggered.connect(lambda _, k=key: self._change_skin(k))

        tray_menu.addSeparator()
        settings_act = tray_menu.addAction("⚙️ Preferences...")
        settings_act.triggered.connect(self._settings)

        exit_act = tray_menu.addAction("❌ Exit Da Goose")
        exit_act.triggered.connect(self._exit)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self._on_tray_activated)
        self.tray_icon.show()

    def _toggle_show(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()
            self._anchor()

    def _on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self._toggle_show()

    # ------------------------------------------------------------------
    # STARTUP & ANCHORING
    # ------------------------------------------------------------------
    def _greet(self):
        skin_name = self.painter_engine.skin.get("name", "Da Goose")
        if self.cfg.get("sound_enabled", True):
            SoundFX.play_quack()
        self.say(f"WHAACK! {skin_name} is on duty on your taskbar!", duration_sec=5.0)

    def _anchor(self, preserve_x: Optional[int] = None):
        screen = QGuiApplication.primaryScreen()
        if not screen:
            return
        avail = screen.availableGeometry()
        ty = avail.bottom() - self.height() + 5

        if preserve_x is not None:
            tx = preserve_x
        else:
            saved = self.cfg.get("last_x_position")
            tx = int(saved) if saved is not None else avail.right() - self.width() - 90

        tx = max(avail.left(), min(avail.right() - self.width(), tx))
        self.move(tx, ty)
        self._target_x = float(tx)

    # ------------------------------------------------------------------
    # ANIMATION & PHYSICS TICKS
    # ------------------------------------------------------------------
    def _anim_tick(self):
        now = time.time()

        # Inactivity Sleep check
        if not self._manually_sleeping and self.painter_engine.expression not in ("talking", "judging"):
            if now - self._last_interaction > self._sleep_threshold:
                if self.painter_engine.expression != "sleeping":
                    self.painter_engine.set_expression("sleeping")

        # Smooth tilt angle decay back to 0
        if not self._is_dragging and abs(self.painter_engine.tilt_angle) > 0.1:
            self.painter_engine.tilt_angle *= 0.88

        # --------------------------------------------------------------
        # DOOMSCROLL ESCALATION & RAMPAGE CHASE SYSTEM
        # --------------------------------------------------------------
        if self._doomscroll_active:
            elapsed = now - self._doomscroll_start_time

            # Phase 1: Angry "WHAACK! WACK!" every 20 seconds for the first 60 seconds
            if elapsed < 60.0:
                if now - self._doomscroll_last_warning_time >= 20.0:
                    self._doomscroll_last_warning_time = now
                    remaining_secs = int(60.0 - elapsed)
                    if self.cfg.get("sound_enabled"):
                        SoundFX.play_scold()
                    self.painter_engine.spin_chair(30.0)
                    self.say(
                        f"WHAACK WACK! Doomscrolling {self._doomscroll_target_site}! "
                        f"{remaining_secs}s before I get off the chair and close it! 🪿",
                        duration_sec=7.0
                    )
            # Phase 2: RAMPAGE! Goose hops off the chair and runs across screen to close window!
            else:
                if not self._rampage_active:
                    self._rampage_active = True
                    self.painter_engine.is_off_chair = True
                    if self.cfg.get("sound_enabled"):
                        SoundFX.play_scold()
                    self.say("THAT'S IT! GETTING OFF THE CHAIR! CLICK ME TO STOP ME! 🪿💨", duration_sec=8.0)
                    self.tray_icon.showMessage(
                        "GOOSE RAMPAGE! 🪿",
                        "Da Goose hopped off the chair to click close on your doomscroll window! Catch it!",
                        QSystemTrayIcon.MessageIcon.Warning,
                        4000
                    )

                # Move goose across taskbar
                self.painter_engine.goose_off_x += self._rampage_speed * self._rampage_direction
                # Boundary turn
                if self.painter_engine.goose_off_x > 90.0:
                    self._rampage_direction = -1.0
                    self.painter_engine.sprint_dir = -1.0
                    SoundFX.play_random_whaack()
                elif self.painter_engine.goose_off_x < -90.0:
                    self._rampage_direction = 1.0
                    self.painter_engine.sprint_dir = 1.0
                    SoundFX.play_random_whaack()

        self.painter_engine.update_animation(dt=0.028)
        self.update()

    def _physics_tick(self):
        if self._is_dragging or abs(self._vel_x) < 0.2:
            return
        screen = QGuiApplication.primaryScreen()
        if not screen:
            return
        avail = screen.availableGeometry()
        min_x, max_x = avail.left(), avail.right() - self.width()

        self._target_x += self._vel_x
        self._vel_x *= self._friction

        if self._target_x <= min_x:
            self._target_x = min_x
            self._vel_x = -self._vel_x * self._bounce
            self.painter_engine.tilt_angle = -12.0
            self.painter_engine.spin_chair(-20.0)
            if self.cfg.get("sound_enabled") and abs(self._vel_x) > 2.0:
                SoundFX.play_random_whaack()
            if abs(self._vel_x) > 3.0 and not self.speech_bubble._is_visible:
                self.say(random.choice(BOUNCE_QUIPS), duration_sec=3.0)
        elif self._target_x >= max_x:
            self._target_x = max_x
            self._vel_x = -self._vel_x * self._bounce
            self.painter_engine.tilt_angle = 12.0
            self.painter_engine.spin_chair(20.0)
            if self.cfg.get("sound_enabled") and abs(self._vel_x) > 2.0:
                SoundFX.play_random_whaack()
            if abs(self._vel_x) > 3.0 and not self.speech_bubble._is_visible:
                self.say(random.choice(BOUNCE_QUIPS), duration_sec=3.0)

        self.move(int(self._target_x), self.y())
        self.cfg.set("last_x_position", int(self._target_x), auto_save=False)

    # ------------------------------------------------------------------
    # MOUSE EVENTS & TACKLE MECHANIC
    # ------------------------------------------------------------------
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            now = time.time()
            self._touch()

            # TACKLE MINI-GAME: If goose is rampaging off chair, clicking tackles it!
            if self._rampage_active:
                self._tackle_goose()
                event.accept()
                return

            # Untitled Goose Theft: click goose to take back stolen item!
            if self.painter_engine.stolen_item is not None:
                item = self.painter_engine.stolen_item
                self.painter_engine.stolen_item = None
                SoundFX.play_random_whaack()
                self.say(f"Fine! Take your {item} back! 🪿", duration_sec=4.0)
                event.accept()
                return

            # Honk Bomb detonation on click!
            if self.painter_engine.honk_bomb_active:
                self._detonate_honk_bomb()
                event.accept()
                return

            # RAPID CLICK RAGE COMBO
            self._click_timestamps = [t for t in self._click_timestamps if now - t < 2.0]
            self._click_timestamps.append(now)
            combo = len(self._click_timestamps)

            if combo >= 8:
                self._trigger_super_rage()
            elif combo >= 2:
                SoundFX.play_random_whaack()
                self.painter_engine.spin_chair(25.0 * combo * 0.4)

            # Wake up if sleeping
            if self.painter_engine.expression == "sleeping":
                self._wake()

            # Normal Dragging
            self._is_dragging = True
            self._drag_start = event.globalPosition().toPoint() - self.pos()
            self._drag_distance = 0.0
            self._last_mouse_x = event.globalPosition().x()
            self._vel_x = 0.0
            event.accept()

        elif event.button() == Qt.MouseButton.RightButton:
            self._context_menu(event.globalPosition().toPoint())
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self._is_dragging:
            gx = event.globalPosition().x()
            dx = gx - self._last_mouse_x
            self._drag_distance += abs(dx)
            self._vel_x = dx * 0.8
            self._last_mouse_x = gx
            self.painter_engine.tilt_angle = max(-18.0, min(18.0, dx * 1.6))
            nx = int(gx - self._drag_start.x())
            screen = QGuiApplication.primaryScreen()
            if screen:
                a = screen.availableGeometry()
                nx = max(a.left(), min(a.right() - self.width(), nx))
            self.move(nx, self.y())
            self._target_x = float(nx)
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton and self._is_dragging:
            self._is_dragging = False
            self.cfg.set("last_x_position", self.x(), auto_save=True)

            # If user clicked without dragging -> Poke / Pet reaction!
            if self._drag_distance < 6.0 and not self._rampage_active:
                if self.painter_engine.expression != "sleeping":
                    self.painter_engine.spin_chair(random.choice([-15.0, 15.0]))
                    if self.cfg.get("sound_enabled"):
                        SoundFX.play_random_whaack()
                    self.say(random.choice(POKE_QUIPS), duration_sec=3.5)
            elif self._drag_distance > 120.0 and random.random() < 0.40:
                if not self.speech_bubble._is_visible:
                    self.say(random.choice(DRAG_QUIPS), duration_sec=3.0)

            event.accept()

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self._spin()
            self._feed()
            event.accept()

    def _touch(self):
        self._last_interaction = time.time()
        self.painter_engine.notify_user_interaction()

    def _tackle_goose(self):
        """User tackled the rampaging goose!"""
        self._rampage_active = False
        self._doomscroll_active = False
        self.painter_engine.is_off_chair = False
        self.painter_engine.goose_off_x = 0.0
        SoundFX.play_peep()
        SoundFX.play_random_whaack()
        self.say("OOF! You tackled me! FINE! But close that doomscroll tab! 🪿", duration_sec=6.0)

    # ------------------------------------------------------------------
    # CHAOS MODES
    # ------------------------------------------------------------------
    def _steal_item(self):
        """Untitled Goose Theft: Goose runs off with a shiny object!"""
        self._touch()
        items = ["bell", "key", "mug", "scissors", "pointer"]
        item = random.choice(items)
        self.painter_engine.trigger_steal_item(item)
        SoundFX.play_random_whaack()
        self.say(f"WHAACK! I stole your {item}! Click me if you want it back! 🪿💨", duration_sec=6.0)

    def _trigger_super_rage(self):
        """Super Saiyan Turbo Goose Rage!"""
        self._touch()
        self.painter_engine.toggle_super_rage(True)
        SoundFX.play_scold()
        self.say("🔥 MAXIMUM GOOSE POWER! 10X COMBO ACTIVATED!! 🔥", duration_sec=5.0)

    def _toggle_goslings(self):
        """Toggles baby goslings marching parade."""
        self._touch()
        self.painter_engine.goslings_active = not self.painter_engine.goslings_active
        if self.painter_engine.goslings_active:
            SoundFX.play_peep()
            self.say("🐣 The baby goslings have arrived! Peep peep!", duration_sec=4.0)
        else:
            self.say("The goslings waddled home for a nap.", duration_sec=3.5)

    def _drop_honk_bomb(self):
        """Lays a comical honk landmine bomb."""
        self._touch()
        self.painter_engine.honk_bomb_active = True
        SoundFX.play_random_whaack()
        self.say("💣 *TICK-TOCK* Dropped a Honk Mine! Don't step on it!", duration_sec=4.5)

    def _detonate_honk_bomb(self):
        """Detonates the honk bomb with a massive bass explosion!"""
        self.painter_engine.honk_bomb_active = False
        SoundFX.play_explosion()
        self.painter_engine.spin_chair(80.0)
        self.say("💥 BOOOOM! WHAACK! That was loud!", duration_sec=4.5)

    def _toggle_dj_beat(self):
        """Toggles Goose DJ beat mode."""
        self._touch()
        self.painter_engine.is_dj_mode = not self.painter_engine.is_dj_mode
        if self.painter_engine.is_dj_mode:
            SoundFX.play_random_whaack()
            self.say("🎧 DJ GOOSE IN THE HOUSE! Drop the beat! 🪿🎶", duration_sec=5.0)
        else:
            self.say("DJ Goose signed off the decks.", duration_sec=3.0)

    # ------------------------------------------------------------------
    # SPEECH & EXPRESSIONS
    # ------------------------------------------------------------------
    def say(self, text: str, duration_sec: Optional[float] = None, ai_response: bool = False):
        self._touch()
        self.painter_engine.set_expression("talking")
        self.speech_bubble.say(text, duration_sec=duration_sec, ai_response=ai_response)

    def _on_speech_finished(self):
        if self.painter_engine.expression == "talking":
            self.painter_engine.set_expression(
                "judging" if self._doomscroll_active else "idle"
            )

    def _on_bubble_dismissed(self):
        if self.painter_engine.expression == "talking":
            self.painter_engine.set_expression("idle")

    def _on_idle_action_speech(self, action: str):
        """Delivers contextual in-character dialogue matching the 22+ idle actions."""
        if self._doomscroll_active or self._rampage_active or self.painter_engine.expression == "sleeping":
            return
        quips = IDLE_ACTION_QUIPS.get(action)
        if quips and not self.speech_bubble._is_visible:
            self.say(random.choice(quips), duration_sec=5.0)

    def _idle_chatter(self):
        """Spontaneous chatter picked dynamically from the equipped skin's dialogue pool."""
        if self.painter_engine.expression in ("idle",) and not self.speech_bubble._is_visible:
            skin_key = self.painter_engine.skin_key
            pool = SKIN_QUIPS.get(skin_key, SKIN_QUIPS.get("classic", IDLE_QUIPS))
            self.say(random.choice(pool), duration_sec=6.0)
        # Re-arm chatter timer for frequent lively company (22 to 45 seconds)
        self.chatter_timer.start(random.randint(22_000, 45_000))

    # ------------------------------------------------------------------
    # INTERACTIONS: SPIN, FEED, NAP
    # ------------------------------------------------------------------
    def _spin(self):
        self._touch()
        self.painter_engine.spin_chair(42.0)
        if self.cfg.get("sound_enabled"):
            SoundFX.play_random_whaack()

    def _feed(self):
        self._touch()
        if self.painter_engine.expression == "sleeping":
            self._wake()
        cx = float(self.width() / 2.0 + 36.0)
        self.painter_engine.feed_crumb(cx, 65.0, float(self.height() - 40.0))
        if self.cfg.get("sound_enabled"):
            QTimer.singleShot(260, SoundFX.play_chomp)
        QTimer.singleShot(420, lambda: self.say(random.choice(EAT_QUIPS), duration_sec=4.5))

    def _nap(self):
        self._manually_sleeping = True
        self.painter_engine.set_expression("sleeping")
        self.speech_bubble.hide_bubble()

    def _wake(self):
        self._manually_sleeping = False
        self._touch()
        self.painter_engine.set_expression("idle")
        if self.cfg.get("sound_enabled"):
            SoundFX.play_random_whaack()

    # ------------------------------------------------------------------
    # AI SCREEN PEEKER (Gemini 3.8 Flash)
    # ------------------------------------------------------------------
    def trigger_ai_peek(self):
        self._touch()
        if self._ai_worker is not None and self._ai_worker.isRunning():
            return
        api_key = self.cfg.get("gemini_api_key", "").strip()
        if not api_key:
            self.say("WHAACK! Add your Gemini API key in Settings so I can roast your screen!", duration_sec=6.0)
            return

        self.speech_bubble.say("Peeking at your screen... 👀", duration_sec=3.0)
        self.painter_engine.set_expression("talking")

        self._ai_worker = GeminiScreenPeekWorker(
            api_key=api_key,
            model_name=self.cfg.get("gemini_model", "gemini-3.8-flash"),
            personality=self.cfg.get("ai_personality", "witty"),
            parent=None,
        )
        self._ai_worker.success.connect(self._on_ai_ok)
        self._ai_worker.error.connect(self._on_ai_err)
        self._ai_worker.start()

    def _on_ai_ok(self, text: str):
        if self.cfg.get("sound_enabled"):
            SoundFX.play_random_whaack()
        self.say(text, ai_response=True)
        # Also notify in Windows tray
        self.tray_icon.showMessage("Da Goose Observed 👀", text[:100] + ("..." if len(text) > 100 else ""), QSystemTrayIcon.MessageIcon.Information, 4000)

    def _on_ai_err(self, msg: str):
        self.say(msg, duration_sec=7.0)

    def _update_ai_timer(self):
        mins = self.cfg.get("ai_auto_peek_interval", 0)
        self.ai_timer.stop()
        if mins > 0:
            self.ai_timer.start(mins * 60 * 1000)

    # ------------------------------------------------------------------
    # ANTI-DOOMSCROLL MONITOR
    # ------------------------------------------------------------------
    def _init_monitor(self):
        kw = self.cfg.get("doomscroll_keywords", [])
        th = self.cfg.get("doomscroll_threshold_minutes", 10)
        en = self.cfg.get("doomscroll_enabled", True)
        self.monitor = WindowMonitorWorker(keywords=kw, threshold_minutes=th,
                                           check_interval_sec=2.0, parent=None)
        self.monitor.update_settings(kw, th, en)
        self.monitor.doomscroll_alert.connect(self._on_scold)
        self.monitor.doomscroll_cleared.connect(self._on_scold_clear)
        self.monitor.start()

    def _on_scold(self, site: str, mins: int, quip: str):
        if not self._doomscroll_active:
            self._doomscroll_active = True
            self._doomscroll_start_time = time.time()
            self._doomscroll_last_warning_time = time.time()
            self._doomscroll_target_site = site

        self.painter_engine.set_expression("judging")
        if self.cfg.get("sound_enabled"):
            SoundFX.play_scold()
        self.say(quip, duration_sec=9.0)

    def _on_scold_clear(self):
        self._doomscroll_active = False
        self._rampage_active = False
        self.painter_engine.is_off_chair = False
        self.painter_engine.goose_off_x = 0.0
        if self.painter_engine.expression == "judging":
            self.painter_engine.set_expression("idle")
            self.say("Good job closing that tab! You're safe... for now. 🪿", duration_sec=4.5)

    # ------------------------------------------------------------------
    # CONTEXT MENU
    # ------------------------------------------------------------------
    MENU_STYLE = """
        QMenu { background:#1E2028; color:#F3F4F6; border:1px solid #374151;
                border-radius:8px; padding:6px; font-family:'Segoe UI',sans-serif; font-size:13px; }
        QMenu::item { padding:7px 22px 7px 12px; border-radius:4px; }
        QMenu::item:selected { background:#374151; color:#FFD23F; }
        QMenu::separator { height:1px; background:#2D3748; margin:4px 6px; }
    """

    def _context_menu(self, pos: QPoint):
        menu = QMenu(self)
        menu.setStyleSheet(self.MENU_STYLE)

        menu.addAction("👁️ Ask Da Goose (AI Peek)").triggered.connect(self.trigger_ai_peek)
        menu.addAction("🔄 Spin Swivel Chair!").triggered.connect(self._spin)
        menu.addAction("🍞 Feed Breadcrumb").triggered.connect(self._feed)

        # CHAOS MODES SUBMENU
        chaos_menu = menu.addMenu("⚡ Chaos Modes")
        chaos_menu.setStyleSheet(self.MENU_STYLE)
        chaos_menu.addAction("🔔 Steal Something!").triggered.connect(self._steal_item)
        chaos_menu.addAction("🐣 Call Baby Goslings").triggered.connect(self._toggle_goslings)
        chaos_menu.addAction("💣 Drop Honk Mine").triggered.connect(self._drop_honk_bomb)
        chaos_menu.addAction("🔥 Super Saiyan Rage!").triggered.connect(self._trigger_super_rage)
        chaos_menu.addAction("🎧 Goose DJ Beat").triggered.connect(self._toggle_dj_beat)

        # 11+ SKINS SUBMENU
        sk_menu = menu.addMenu("🎨 Goose Skins")
        sk_menu.setStyleSheet(self.MENU_STYLE)
        cur = self.painter_engine.skin_key
        for key, val in SKINS.items():
            check = "✓ " if key == cur else "   "
            sk_menu.addAction(f"{check}{val['name']}").triggered.connect(
                lambda _, k=key: self._change_skin(k))

        menu.addSeparator()

        if self.painter_engine.expression == "sleeping":
            menu.addAction("☀️ Wake Up!").triggered.connect(self._wake)
        else:
            menu.addAction("💤 Take a Nap").triggered.connect(self._nap)

        # Doomscroll toggle
        ds_menu = menu.addMenu("🛡️ Doomscroll Guard")
        ds_menu.setStyleSheet(self.MENU_STYLE)
        is_on = self.cfg.get("doomscroll_enabled", True)
        ds_menu.addAction(f"{'Disable' if is_on else 'Enable'} Guard").triggered.connect(self._toggle_doom)
        ds_menu.addAction("Reset Timer").triggered.connect(self.monitor.reset_timer)

        menu.addSeparator()
        menu.addAction("⚙️ Preferences...").triggered.connect(self._settings)
        menu.addAction("❌ Exit Da Goose").triggered.connect(self._exit)

        menu.exec(pos)

    def _change_skin(self, key: str):
        self.painter_engine.set_theme(key)
        self.cfg.set("goose_skin", key)
        if self.cfg.get("sound_enabled"):
            SoundFX.play_random_whaack()
        greeting = SKIN_SWITCH_GREETINGS.get(key, f"WHAACK! Switched to {key} skin! 🪿")
        self.say(greeting, duration_sec=4.5)

    def _toggle_doom(self):
        new = not self.cfg.get("doomscroll_enabled", True)
        self.cfg.set("doomscroll_enabled", new)
        self.monitor.update_settings(
            self.cfg.get("doomscroll_keywords", []),
            self.cfg.get("doomscroll_threshold_minutes", 10),
            new
        )
        self.say(f"Doomscroll guard {'enabled 👀' if new else 'disabled.'}", duration_sec=3.5)

    def _settings(self):
        dlg = SettingsDialog(self.cfg, self)
        dlg.settings_applied.connect(self._apply_settings)
        dlg.exec()

    def _apply_settings(self):
        new_skin = self.cfg.get("goose_skin", "classic")
        old_skin = self.painter_engine.skin_key
        self.painter_engine.set_theme(new_skin)
        if new_skin != old_skin:
            greeting = SKIN_SWITCH_GREETINGS.get(new_skin, f"WHAACK! Switched to {new_skin}! 🪿")
            self.say(greeting, duration_sec=4.5)
        self.monitor.update_settings(
            self.cfg.get("doomscroll_keywords", []),
            self.cfg.get("doomscroll_threshold_minutes", 10),
            self.cfg.get("doomscroll_enabled", True)
        )
        self._update_ai_timer()
        topmost = self.cfg.get("always_on_top", True)
        cur_top = bool(self.windowFlags() & Qt.WindowType.WindowStaysOnTopHint)
        if cur_top != topmost:
            self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, topmost)
            self.show()

    def _exit(self):
        if hasattr(self, "tray_icon") and self.tray_icon:
            self.tray_icon.hide()
        if hasattr(self, "monitor") and self.monitor:
            self.monitor.stop()
        if self._ai_worker and self._ai_worker.isRunning():
            self._ai_worker.wait(500)
        self.close()
        QGuiApplication.quit()

    # ------------------------------------------------------------------
    # PAINT
    # ------------------------------------------------------------------
    def paintEvent(self, event):
        painter = QPainter(self)
        goose_rect = QRectF(
            (self.width() - 150.0) / 2.0,
            self.height() - 145.0,
            150.0,
            145.0
        )
        draw_chair = self.cfg.get("chair_enabled", True)
        self.painter_engine.paint(painter, goose_rect, draw_chair=draw_chair)
