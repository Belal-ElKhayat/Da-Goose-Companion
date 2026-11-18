"""Vector Goose Painter for Da Goose Companion.
Renders beautiful, crisp geese and ducks sitting on an upright swivel office chair,
or getting off the chair to run across the taskbar in Untitled Goose chaos mode!
Features:
- 11+ distinct skins (Classic, Smoking, Coder, Duck, Cooker/Chef, Detective, Ninja, King, Cyberpunk, Wizard, Coffee)
- 22+ procedural idle animations (Spaghetti snap, phone scroll, boba, juggle, ramen, guitar, bubblegum, polaroid, etc.)
- Off-chair sprinting & rampage mode (empty swivel chair left behind)
- Untitled Goose Theft items (shiny bell, golden key, red mug, scissors, cursor pointer)
- Baby gosling parade
- Super Saiyan rage aura & laser eyes
- Honk bomb landmine
- Goose DJ headphones & turntable deck
"""

import math
import random
import time
from typing import Dict, List, Optional, Tuple
from PyQt6.QtCore import QPointF, QRectF, Qt
from PyQt6.QtGui import (
    QBrush,
    QColor,
    QFont,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPen,
    QRadialGradient,
)

from sound_effects import SoundFX

SKINS: Dict[str, Dict] = {
    "classic": {
        "name": "🪿 Classic White Goose",
        "shape": "goose",
        "body": "#FFFFFF",
        "belly": "#F7F9FA",
        "neck": "#FFFFFF",
        "head": "#FFFFFF",
        "beak": "#FFA04D",
        "beak_inside": "#E07525",
        "blush": "#FFAAA6",
        "outline": "#40454D",
        "eye": "#1E2229",
        "eye_highlight": "#FFFFFF",
        "wing": "#EDF1F5",
        "leg": "#FFA04D",
        "foot": "#E87C20",
        "accessory": "none",
        "chair_seat": "#263238",
        "chair_cushion": "#37474F",
        "shadow": "#00000030",
    },
    "smoking": {
        "name": "🚬 Smoking Gray Goose",
        "shape": "goose",
        "body": "#5C6470",
        "belly": "#838D9B",
        "neck": "#6B7482",
        "head": "#525A66",
        "beak": "#E67328",
        "beak_inside": "#A84C10",
        "blush": "#D47F7B",
        "outline": "#23272E",
        "eye": "#15181C",
        "eye_highlight": "#FFFFFF",
        "wing": "#484E59",
        "leg": "#E67328",
        "foot": "#BA5514",
        "accessory": "smoking",
        "chair_seat": "#1E2124",
        "chair_cushion": "#2F3338",
        "shadow": "#00000035",
    },
    "coder": {
        "name": "💻 Coder Goose",
        "shape": "goose",
        "body": "#282A36",
        "belly": "#44475A",
        "neck": "#282A36",
        "head": "#21222C",
        "beak": "#FFB86C",
        "beak_inside": "#BD93F9",
        "blush": "#FF79C6",
        "outline": "#191A21",
        "eye": "#50FA7B",
        "eye_highlight": "#8BE9FD",
        "wing": "#383A59",
        "leg": "#FFB86C",
        "foot": "#E09040",
        "accessory": "laptop",
        "glasses_color": "#8BE9FD",
        "chair_seat": "#21222C",
        "chair_cushion": "#44475A",
        "shadow": "#00000035",
    },
    "cooker": {
        "name": "👨‍🍳 Chef / Cooker Goose",
        "shape": "goose",
        "body": "#FFFFFF",
        "belly": "#FFF9E6",
        "neck": "#FFFFFF",
        "head": "#FFFFFF",
        "beak": "#FFA04D",
        "beak_inside": "#E07525",
        "blush": "#FFAAA6",
        "outline": "#374151",
        "eye": "#1E2229",
        "eye_highlight": "#FFFFFF",
        "wing": "#F3F4F6",
        "leg": "#FFA04D",
        "foot": "#E87C20",
        "accessory": "cooker",
        "chair_seat": "#7F1D1D",
        "chair_cushion": "#B91C1C",
        "shadow": "#00000030",
    },
    "detective": {
        "name": "🕵️ Detective Goose",
        "shape": "goose",
        "body": "#E6D5B8",
        "belly": "#FAF0E6",
        "neck": "#E6D5B8",
        "head": "#D4C2A5",
        "beak": "#E08538",
        "beak_inside": "#A85018",
        "blush": "#D4A373",
        "outline": "#3D2B1F",
        "eye": "#2B1E16",
        "eye_highlight": "#FFFFFF",
        "wing": "#C4B296",
        "leg": "#E08538",
        "foot": "#BA6320",
        "accessory": "detective",
        "chair_seat": "#2C1B11",
        "chair_cushion": "#4A3525",
        "shadow": "#00000035",
    },
    "ninja": {
        "name": "🥷 Ninja Goose",
        "shape": "goose",
        "body": "#1F2421",
        "belly": "#2F3632",
        "neck": "#1F2421",
        "head": "#141715",
        "beak": "#E67328",
        "beak_inside": "#993D12",
        "blush": "#D64045",
        "outline": "#0A0C0B",
        "eye": "#E71D36",
        "eye_highlight": "#FFFFFF",
        "wing": "#2B332E",
        "leg": "#E67328",
        "foot": "#BA5514",
        "accessory": "ninja",
        "chair_seat": "#0F1110",
        "chair_cushion": "#232825",
        "shadow": "#00000045",
    },
    "king": {
        "name": "👑 Royal King Goose",
        "shape": "goose",
        "body": "#FFFFFF",
        "belly": "#FFF8E7",
        "neck": "#FFFFFF",
        "head": "#FFFFFF",
        "beak": "#FFA04D",
        "beak_inside": "#E07525",
        "blush": "#FFAAA6",
        "outline": "#332211",
        "eye": "#1E2229",
        "eye_highlight": "#FFFFFF",
        "wing": "#F7F5F0",
        "leg": "#FFA04D",
        "foot": "#E87C20",
        "accessory": "king",
        "chair_seat": "#4A0E17",
        "chair_cushion": "#800E13",
        "shadow": "#00000030",
    },
    "duck": {
        "name": "🐤 Classic Rubber Duck",
        "shape": "duck",
        "body": "#FFD23F",
        "belly": "#FFE66D",
        "neck": "#FFD23F",
        "head": "#FFCE2B",
        "beak": "#FF6B35",
        "beak_inside": "#C84B15",
        "blush": "#FF8DA1",
        "outline": "#4A3E1B",
        "eye": "#1E1E1E",
        "eye_highlight": "#FFFFFF",
        "wing": "#EEC02B",
        "leg": "#FF6B35",
        "foot": "#D94E1A",
        "accessory": "none",
        "chair_seat": "#22252A",
        "chair_cushion": "#374151",
        "shadow": "#2A2A2A33",
    },
    "cyberpunk": {
        "name": "⚡ Cyberpunk 2077",
        "shape": "goose",
        "body": "#FF007F",
        "belly": "#00F0FF",
        "neck": "#D6006B",
        "head": "#CC005F",
        "beak": "#FFE600",
        "beak_inside": "#99004C",
        "blush": "#BD00FF",
        "outline": "#2B0038",
        "eye": "#00F0FF",
        "eye_highlight": "#FFFFFF",
        "wing": "#D6006B",
        "leg": "#FFE600",
        "foot": "#CCA800",
        "accessory": "visor",
        "chair_seat": "#1A0022",
        "chair_cushion": "#FF007F",
        "shadow": "#BD00FF44",
    },
    "wizard": {
        "name": "🧙 Wizard Goose",
        "shape": "goose",
        "body": "#5E548E",
        "belly": "#9F86C0",
        "neck": "#4A3F70",
        "head": "#3C096C",
        "beak": "#FFA04D",
        "beak_inside": "#C26820",
        "blush": "#E2B6CF",
        "outline": "#231942",
        "eye": "#E0B1CB",
        "eye_highlight": "#FFFFFF",
        "wing": "#4A3F70",
        "leg": "#FFA04D",
        "foot": "#C26820",
        "accessory": "hat",
        "hat_color": "#3C096C",
        "chair_seat": "#3C096C",
        "chair_cushion": "#5A189A",
        "shadow": "#23194244",
    },
    "coffee": {
        "name": "☕ Coffee Addict",
        "shape": "goose",
        "body": "#D4A373",
        "belly": "#FAEDCD",
        "neck": "#CCD5AE",
        "head": "#A98467",
        "beak": "#BC6C25",
        "beak_inside": "#8B4513",
        "blush": "#DDA15E",
        "outline": "#43281C",
        "eye": "#283618",
        "eye_highlight": "#FFFFFF",
        "wing": "#CCD5AE",
        "leg": "#BC6C25",
        "foot": "#8B4513",
        "accessory": "coffee",
        "chair_seat": "#332211",
        "chair_cushion": "#553311",
        "shadow": "#43281C44",
    },
}

ALL_IDLE_ACTIONS = [
    "spaghetti",
    "phone_scroll",
    "boba",
    "juggle",
    "yawn_stretch",
    "ramen",
    "rubiks_cube",
    "coin_flip",
    "guitar",
    "bubblegum",
    "polaroid",
    "magnifying_glass",
    "pushups",
    "fidget_spinner",
    "deal_with_it",
    "hula_hoop",
    "watch_check",
    "binoculars",
    "pizza",
    "laser_chase",
    "magic_rabbit",
    "sneeze",
]


class ZzzParticle:
    def __init__(self, x: float, y: float, size: int = 11):
        self.x = x; self.y = y; self.orig_y = y
        self.size = size; self.alpha = 230
        self.drift = random.uniform(0, math.pi * 2)

    def update(self, dt: float) -> bool:
        self.y -= 13.0 * dt
        self.drift += 3.0 * dt
        self.x += math.sin(self.drift) * 0.5
        self.alpha = max(0, int(230 * (1.0 - (self.orig_y - self.y) / 45.0)))
        return self.alpha > 0 and (self.orig_y - self.y) < 45.0


class SmokeParticle:
    def __init__(self, x: float, y: float):
        self.x = x; self.y = y; self.orig_y = y
        self.radius = random.uniform(2.5, 4.5)
        self.alpha = random.randint(160, 210)
        self.drift_phase = random.uniform(0, math.pi * 2)
        self.speed_y = random.uniform(14.0, 20.0)

    def update(self, dt: float) -> bool:
        self.y -= self.speed_y * dt
        self.drift_phase += 2.5 * dt
        self.x += math.sin(self.drift_phase) * 0.6
        self.radius += 8.0 * dt
        dist = self.orig_y - self.y
        self.alpha = max(0, int(180 * (1.0 - dist / 55.0)))
        return self.alpha > 0 and dist < 55.0


class CrumbParticle:
    def __init__(self, x: float, y: float, ty: float):
        self.x = x; self.y = y; self.target_y = ty; self.speed = 4.5

    def update(self) -> bool:
        if self.y < self.target_y:
            self.y += self.speed
            return True
        return False


class BabyGosling:
    def __init__(self, start_x: float):
        self.x = start_x
        self.y = 0.0
        self.vx = random.uniform(-35.0, 35.0)
        self.walk_phase = random.uniform(0, math.pi * 2)
        self.peep_timer = random.uniform(2.0, 5.0)
        self.flip_angle = 0.0
        self.is_flipping = False
        self.state_timer = random.uniform(1.0, 3.0)
        self.behavior = "scurry"  # scurry, peck, tumble, zoom

    def update(self, dt: float):
        self.walk_phase += dt * (18.0 if abs(self.vx) > 10 else 4.0)
        self.state_timer -= dt
        if self.state_timer <= 0:
            self.state_timer = random.uniform(1.2, 3.5)
            self.behavior = random.choice(["scurry", "scurry", "peck", "tumble", "zoom"])
            if self.behavior == "zoom":
                self.vx = random.choice([-50.0, 50.0])
            elif self.behavior == "peck":
                self.vx = 0.0
            elif self.behavior == "tumble":
                self.is_flipping = True
            else:
                self.vx = random.uniform(-30.0, 30.0)

        # Move
        self.x += self.vx * dt

        # Bounce across taskbar
        if self.x < -125.0:
            self.x = -125.0
            self.vx = abs(self.vx)
        elif self.x > 125.0:
            self.x = 125.0
            self.vx = -abs(self.vx)

        # Flip tumble animation
        if self.is_flipping:
            self.flip_angle += dt * 650.0
            if self.flip_angle >= 360.0:
                self.flip_angle = 0.0
                self.is_flipping = False

        self.peep_timer -= dt
        if self.peep_timer <= 0:
            self.peep_timer = random.uniform(2.5, 6.0)
            SoundFX.play_peep()


class GoosePainter:
    """Master Vector Renderer for Goose, Chair, 22+ Idle Animations, and Chaos Modes."""

    def __init__(self, skin_key: str = "classic"):
        self.skin_key = skin_key if skin_key in SKINS else "classic"
        self.expression = "idle"

        # Chair Swivel (upright vertical axis rotation)
        self.chair_angle = 0.0
        self.chair_spin_velocity = 0.0
        self.is_spinning = False

        # Off-Chair State (when running / rampaging / stealing)
        self.is_off_chair = False
        self.goose_off_x = 0.0
        self.goose_off_y = 0.0
        self.run_cycle = 0.0
        self.sprint_dir = 1.0  # 1 facing right, -1 facing left

        # Chaos Mode States
        self.stolen_item: Optional[str] = None  # bell, key, mug, scissors, pointer
        self.is_super_rage = False
        self.rage_click_combo = 0
        self.rage_timer = 0.0
        self.goslings_active = False
        self.goslings: List[BabyGosling] = [BabyGosling(ox) for ox in [-45, -70, -95, -120]]
        self.honk_bomb_active = False
        self.honk_bomb_timer = 0.0
        self.is_dj_mode = False
        self.dj_beat_phase = 0.0

        # Animation states
        self.breathing_time = 0.0
        self.blink_progress = 0.0
        self.is_blinking = False
        self.next_blink_time = time.time() + random.uniform(2.5, 5.0)

        # Mouth / Beak
        self.mouth_phase = 0.0
        self.mouth_open_ratio = 0.0
        self.tilt_angle = 0.0

        # 22+ Idle Action State Machine
        self.current_idle_action: Optional[str] = None
        self.idle_action_timer = 0.0
        self.idle_action_duration = 0.0
        self.next_idle_action_time = time.time() + random.uniform(10.0, 16.0)
        self.on_idle_action_started = None  # Callback to trigger witty dialogue!
        self.spaghetti_broken = False
        self.bubblegum_radius = 0.0
        self.bubblegum_popped = False

        # Smoking Goose State
        self.idle_seconds = 0.0
        self.is_smoking = False
        self.lighter_progress = 0.0
        self.lighter_sound_played = False
        self.smoke_particles: List[SmokeParticle] = []
        self.last_smoke_spawn = 0.0

        # Sleeping & Crumbs
        self.zzz_particles: List[ZzzParticle] = []
        self.last_zzz = 0.0
        self.active_crumbs: List[CrumbParticle] = []
        self.eating_timer = 0.0

    @property
    def skin(self) -> Dict:
        return SKINS.get(self.skin_key, SKINS["classic"])

    @property
    def theme(self) -> Dict:
        return self.skin

    def set_theme(self, key: str):
        if key in SKINS:
            self.skin_key = key
            self.is_smoking = False
            self.lighter_progress = 0.0
            self.smoke_particles.clear()

    def set_expression(self, expr: str):
        if expr != self.expression:
            self.expression = expr
            if expr != "sleeping":
                self.zzz_particles.clear()
            if expr != "idle":
                self.current_idle_action = None

    def spin_chair(self, force: float = 35.0):
        self.chair_spin_velocity = force
        self.is_spinning = True

    def trigger_steal_item(self, item_name: Optional[str] = None):
        items = ["bell", "key", "mug", "scissors", "pointer"]
        self.stolen_item = item_name or random.choice(items)
        self.is_off_chair = True
        self.goose_off_x = 0.0
        self.sprint_dir = 1.0
        if self.stolen_item == "bell":
            SoundFX.play_bell()
        else:
            SoundFX.play_random_whaack()

    def toggle_super_rage(self, enable: bool):
        self.is_super_rage = enable
        if enable:
            self.rage_timer = 7.0
            self.spin_chair(90.0)
            SoundFX.play_laser_blast()

    def feed_crumb(self, x: float, y: float, ty: float):
        self.active_crumbs.append(CrumbParticle(x, y, ty))

    def notify_user_interaction(self):
        self.idle_seconds = 0.0
        # Push next idle action into the future so poking/clicking NEVER gets interrupted!
        self.next_idle_action_time = time.time() + random.uniform(14.0, 22.0)
        if self.current_idle_action:
            self.current_idle_action = None
        if self.is_smoking:
            self.is_smoking = False
            self.lighter_progress = 0.0
            self.lighter_sound_played = False

    def update_animation(self, dt: float = 0.028):
        now = time.time()
        self.idle_seconds += dt
        self.breathing_time += dt

        # 1. Swivel Chair Physics
        if self.is_spinning:
            self.chair_angle += self.chair_spin_velocity
            self.chair_spin_velocity *= 0.94
            if abs(self.chair_spin_velocity) < 0.3:
                self.is_spinning = False
                self.chair_spin_velocity = 0.0
        else:
            ambient_swivel = math.sin(self.breathing_time * 1.5) * 14.0
            drag_swivel = self.tilt_angle * 1.2
            target_angle = ambient_swivel + drag_swivel
            self.chair_angle += (target_angle - self.chair_angle) * 0.12

        # 2. Super Rage Mode Countdown
        if self.is_super_rage:
            self.rage_timer -= dt
            if self.rage_timer <= 0:
                self.is_super_rage = False
                self.rage_click_combo = 0

        # 3. Off-Chair Running animation
        if self.is_off_chair:
            self.run_cycle += dt * 18.0

        # 4. Autonomous Baby Goslings
        if self.goslings_active:
            for g in self.goslings:
                g.update(dt)

        # 5. Skin-Specific Realistic Animations (Hands, Beak, Typing, Sipping)
        if self.skin_key == "coder" and not self.is_off_chair:
            # Mechanical keyboard clatter
            if int(self.breathing_time * 12) % 4 == 0 and random.random() < 0.20:
                SoundFX.play_keyboard_clack()
        elif self.skin_key == "coffee" and not self.is_off_chair:
            # Coffee periodic realistic sip cycle every ~7s
            sip_cycle = self.breathing_time % 7.0
            if 3.2 < sip_cycle < 3.5 and not hasattr(self, "_coffee_sipped"):
                self._coffee_sipped = True
                SoundFX.play_sip()
            elif sip_cycle < 1.0 and hasattr(self, "_coffee_sipped"):
                delattr(self, "_coffee_sipped")

        # 6. 22+ Idle Animations Engine (Only for non-coder, non-coffee, non-smoking skins to keep realism!)
        if not self.is_off_chair and self.expression == "idle" and not self.is_super_rage:
            if self.skin_key not in ("coder", "smoking", "coffee"):
                if self.current_idle_action is None and now >= self.next_idle_action_time:
                    self.current_idle_action = random.choice(ALL_IDLE_ACTIONS)
                    self.idle_action_timer = 0.0
                    self.idle_action_duration = random.uniform(4.5, 7.5)
                    self.spaghetti_broken = False
                    self.bubblegum_radius = 0.0
                    self.bubblegum_popped = False
                    if self.on_idle_action_started:
                        self.on_idle_action_started(self.current_idle_action)

            if self.current_idle_action:
                self.idle_action_timer += dt
                # Sound / trigger points for specific actions
                if self.current_idle_action == "spaghetti" and not self.spaghetti_broken and self.idle_action_timer > 2.0:
                    self.spaghetti_broken = True
                    SoundFX.play_snap()

                if self.current_idle_action == "bubblegum":
                    if not self.bubblegum_popped and self.idle_action_timer > 2.5:
                        self.bubblegum_popped = True
                        SoundFX.play_pop()

                if self.current_idle_action == "coin_flip" and int(self.idle_action_timer * 10) == 12:
                    SoundFX.play_bell()

                if self.idle_action_timer >= self.idle_action_duration:
                    self.current_idle_action = None
                    self.next_idle_action_time = now + random.uniform(12.0, 20.0)

        # 6. Smoking Goose
        if self.skin_key == "smoking" and self.expression != "sleeping" and not self.is_off_chair:
            if self.idle_seconds >= 10.0:
                self.is_smoking = True
                if self.lighter_progress < 1.0:
                    self.lighter_progress = min(1.0, self.lighter_progress + dt * 1.8)
                    if not self.lighter_sound_played and self.lighter_progress > 0.4:
                        self.lighter_sound_played = True
                        SoundFX.play_lighter()

                if self.lighter_progress >= 0.7 and now - self.last_smoke_spawn > 0.22:
                    self.last_smoke_spawn = now
                    self.smoke_particles.append(SmokeParticle(x=52.0, y=-95.0))
            else:
                self.is_smoking = False
                self.lighter_progress = max(0.0, self.lighter_progress - dt * 2.5)

            self.smoke_particles = [s for s in self.smoke_particles if s.update(dt)]
        else:
            self.smoke_particles.clear()

        # 7. Sleeping & Crumbs
        if self.expression == "sleeping":
            if now - self.last_zzz > 0.9:
                self.last_zzz = now
                self.zzz_particles.append(ZzzParticle(65.0, 30.0, random.choice([9, 12, 15])))
            self.zzz_particles = [p for p in self.zzz_particles if p.update(dt)]
        else:
            self.zzz_particles.clear()

        if self.active_crumbs:
            for c in list(self.active_crumbs):
                if not c.update():
                    self.active_crumbs.remove(c)
                    self.eating_timer = 0.65
                    self.set_expression("eating")

        if self.eating_timer > 0:
            self.eating_timer -= dt
            self.mouth_open_ratio = (math.sin(self.eating_timer * 22.0) + 1.0) / 2.0
            if self.eating_timer <= 0:
                self.mouth_open_ratio = 0.0
                if self.expression == "eating":
                    self.set_expression("idle")

    # ------------------------------------------------------------------
    # MAIN PAINT ENTRY POINT
    # ------------------------------------------------------------------
    def paint(self, painter: QPainter, base_rect: QRectF, draw_chair: bool = True):
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)

        sk = self.skin
        outline = QPen(QColor(sk["outline"]), 2.0)
        outline.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        outline.setCapStyle(Qt.PenCapStyle.RoundCap)

        cx = base_rect.x() + base_rect.width() / 2.0
        cy = base_rect.y() + base_rect.height() - 4.0
        painter.translate(cx, cy)

        bob_y = math.sin(self.breathing_time * 2.6) * 2.0
        if self.expression == "sleeping":
            bob_y = math.sin(self.breathing_time * 1.4) * 1.2

        # 1. DRAW FIXED CHAIR (Always at center floor)
        if draw_chair:
            self._draw_chair_base(painter)

        theta_rad = math.radians(self.chair_angle)
        cos_theta = math.cos(theta_rad)
        sin_theta = math.sin(theta_rad)
        h_scale = abs(cos_theta) * 0.35 + 0.65
        facing_dir = 1.0 if cos_theta >= 0 else -1.0

        if draw_chair and facing_dir > 0:
            self._draw_backrest(painter, sk, sin_theta, h_scale)

        if draw_chair:
            painter.save()
            painter.translate(sin_theta * 6.0, 0.0)
            painter.scale(h_scale * (1.0 if cos_theta >= 0 else -1.0), 1.0)
            self._draw_seat_cushion(painter, sk)
            painter.restore()

        # 2. DRAW GOOSE (On Chair OR Running Off Chair)
        painter.save()
        if self.is_off_chair:
            # Running off chair at (goose_off_x, goose_off_y)
            painter.translate(self.goose_off_x, self.goose_off_y)
            painter.scale(self.sprint_dir, 1.0)
            self._draw_running_goose(painter, sk, outline)
        else:
            # Seated on chair with swivel rotation
            painter.translate(sin_theta * 6.0, 0.0)
            painter.scale(h_scale * (1.0 if cos_theta >= 0 else -1.0), 1.0)
            painter.translate(0.0, -22.0 + bob_y)

            if sk["shape"] == "duck":
                self._draw_rubber_duck(painter, sk, outline)
            else:
                self._draw_goose_character(painter, sk, outline)

        painter.restore()

        if draw_chair and facing_dir < 0:
            self._draw_backrest(painter, sk, sin_theta, h_scale)

        # 3. DRAW BABY GOSLINGS PARADE
        if self.goslings_active:
            self._draw_goslings_parade(painter)

        # 4. DRAW HONK BOMB
        if self.honk_bomb_active:
            self._draw_honk_bomb(painter)

        # 5. DRAW WORLD PARTICLES (Smoke, Zzz, Crumbs)
        painter.restore()
        self._draw_particles(painter, base_rect)

    # ------------------------------------------------------------------
    # CHAIR
    # ------------------------------------------------------------------
    def _draw_chair_base(self, painter: QPainter):
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(0, 0, 0, 40)))
        painter.drawEllipse(QRectF(-48.0, -4.0, 96.0, 10.0))

        g = QLinearGradient(-6.0, 0, 6.0, 0)
        g.setColorAt(0.0, QColor("#2D3036"))
        g.setColorAt(0.5, QColor("#7B828E"))
        g.setColorAt(1.0, QColor("#1F2126"))
        painter.setPen(QPen(QColor("#18191D"), 1.2))
        painter.setBrush(QBrush(g))
        painter.drawRoundedRect(QRectF(-6.0, -28.0, 12.0, 26.0), 2.5, 2.5)

        lp = QPen(QColor("#24272D"), 3.6)
        lp.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(lp)
        for deg in [18, 90, 162, 234, 306]:
            r = math.radians(deg)
            painter.drawLine(QPointF(0, -6.0), QPointF(math.cos(r) * 35, math.sin(r) * 10 - 4))

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor("#121417")))
        for deg in [18, 90, 162, 234, 306]:
            r = math.radians(deg)
            painter.drawEllipse(QRectF(math.cos(r) * 35 - 3.0, math.sin(r) * 10 - 7.5, 6.0, 5.0))

    def _draw_seat_cushion(self, painter: QPainter, sk: Dict):
        seat_c = QColor(sk.get("chair_seat", "#22252A"))
        cushion_c = QColor(sk.get("chair_cushion", "#374151"))
        bp = QPen(QColor("#111317"), 1.6)

        painter.setPen(bp)
        painter.setBrush(QBrush(seat_c))
        painter.drawRoundedRect(QRectF(-36.0, -25.0, 72.0, 16.0), 7.0, 7.0)

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(cushion_c))
        painter.drawRoundedRect(QRectF(-32.0, -25.0, 64.0, 10.0), 5.0, 5.0)

        ap = QPen(QColor("#14161A"), 2.6)
        ap.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(ap)
        for s in [-1, 1]:
            x0 = s * 34.0
            painter.drawLine(QPointF(x0, -22.0), QPointF(x0 + s * 3.0, -38.0))
            painter.drawLine(QPointF(x0 + s * 3.0, -38.0), QPointF(x0 - s * 10.0, -38.0))

    def _draw_backrest(self, painter: QPainter, sk: Dict, sin_theta: float, h_scale: float):
        sc = QColor(sk.get("chair_seat", "#22252A"))
        cc = QColor(sk.get("chair_cushion", "#374151"))
        bp = QPen(QColor("#111317"), 1.6)
        bx = -sin_theta * 12.0
        bw = 54.0 * h_scale

        painter.save()
        painter.setPen(QPen(QColor("#111317"), 3.6))
        painter.drawLine(QPointF(bx, -24.0), QPointF(bx, -8.0))
        painter.setPen(bp)
        painter.setBrush(QBrush(sc))
        painter.drawRoundedRect(QRectF(bx - bw / 2.0, -74.0, bw, 52.0), 8.0, 8.0)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(cc))
        painter.drawRoundedRect(QRectF(bx - (bw - 10.0) / 2.0, -68.0, bw - 10.0, 40.0), 6.0, 6.0)
        painter.restore()

    # ------------------------------------------------------------------
    # GOOSE BODY (Seated & Running)
    # ------------------------------------------------------------------
    def _draw_goose_character(self, painter: QPainter, sk: Dict, outline: QPen):
        # Super Saiyan Aura if Rage mode
        if self.is_super_rage:
            self._draw_rage_aura(painter)

        # Hanging legs on seat
        leg_c = QColor(sk["leg"])
        foot_c = QColor(sk["foot"])
        painter.setPen(outline)
        painter.setBrush(QBrush(leg_c))

        for side in [-1, 1]:
            lx = side * 10.0
            painter.drawRoundedRect(QRectF(lx - 2.5, -4.0, 5.0, 16.0), 2.0, 2.0)
            painter.setBrush(QBrush(foot_c))
            fp = QPainterPath()
            fp.moveTo(lx, 12.0)
            fp.quadTo(lx + side * 16.0, 10.0, lx + side * 20.0, 18.0)
            fp.quadTo(lx + side * 10.0, 22.0, lx, 20.0)
            fp.quadTo(lx - side * 3.0, 20.0, lx, 12.0)
            fp.closeSubpath()
            painter.drawPath(fp)
            painter.setBrush(QBrush(leg_c))

        self._draw_goose_upper_body(painter, sk, outline)

    def _draw_running_goose(self, painter: QPainter, sk: Dict, outline: QPen):
        """Active sprint pose with cycling feet and flapping wings."""
        if self.is_super_rage:
            self._draw_rage_aura(painter)

        leg_c = QColor(sk["leg"])
        foot_c = QColor(sk["foot"])

        # Running feet cycling
        leg_stride_1 = math.sin(self.run_cycle) * 16.0
        leg_stride_2 = -math.sin(self.run_cycle) * 16.0

        painter.setPen(outline)
        painter.setBrush(QBrush(leg_c))

        # Leg 1
        painter.drawLine(QPointF(-8.0, -8.0), QPointF(-8.0 + leg_stride_1, 10.0))
        painter.setBrush(QBrush(foot_c))
        painter.drawEllipse(QRectF(-8.0 + leg_stride_1 - 4.0, 8.0, 10.0, 6.0))

        # Leg 2
        painter.setBrush(QBrush(leg_c))
        painter.drawLine(QPointF(8.0, -8.0), QPointF(8.0 + leg_stride_2, 10.0))
        painter.setBrush(QBrush(foot_c))
        painter.drawEllipse(QRectF(8.0 + leg_stride_2 - 4.0, 8.0, 10.0, 6.0))

        # Tilt body forward in sprint
        painter.save()
        painter.rotate(14.0)
        self._draw_goose_upper_body(painter, sk, outline, is_running=True)
        painter.restore()

    def _draw_goose_upper_body(self, painter: QPainter, sk: Dict, outline: QPen, is_running: bool = False):
        # Body
        painter.setPen(outline)
        painter.setBrush(QBrush(QColor(sk["body"])))
        painter.drawEllipse(QRectF(-34.0, -50.0, 68.0, 52.0))

        # Belly highlight
        b = QPainterPath()
        b.moveTo(8.0, -40.0)
        b.cubicTo(34.0, -34.0, 34.0, -8.0, 14.0, -2.0)
        b.quadTo(0.0, -16.0, 8.0, -40.0)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(sk["belly"])))
        painter.drawPath(b)

        # Tail
        t = QPainterPath()
        t.moveTo(-28.0, -20.0)
        t.quadTo(-48.0, -38.0, -40.0, -44.0)
        t.quadTo(-34.0, -38.0, -24.0, -28.0)
        t.closeSubpath()
        painter.setPen(outline)
        painter.setBrush(QBrush(QColor(sk["body"])))
        painter.drawPath(t)

        # Wing
        if is_running:
            # Flapping wings in sprint
            flap_y = math.sin(self.run_cycle * 1.5) * 14.0
            w = QPainterPath()
            w.moveTo(-16.0, -32.0)
            w.quadTo(-38.0, -50.0 + flap_y, -26.0, -24.0)
            w.closeSubpath()
            painter.drawPath(w)
        else:
            w = QPainterPath()
            w.moveTo(-18.0, -30.0)
            w.cubicTo(-20.0, -12.0, 12.0, -10.0, 8.0, -26.0)
            w.quadTo(-4.0, -36.0, -18.0, -30.0)
            painter.drawPath(w)

        # Neck
        n = QPainterPath()
        n.moveTo(8.0, -44.0)
        n.cubicTo(20.0, -58.0, 22.0, -74.0, 16.0, -86.0)
        n.cubicTo(12.0, -86.0, 7.0, -74.0, 4.0, -44.0)
        n.closeSubpath()
        painter.setPen(outline)
        painter.setBrush(QBrush(QColor(sk["neck"])))
        painter.drawPath(n)

        # Head
        hcx, hcy, hr = 16.0, -97.0, 20.0
        painter.setPen(outline)
        painter.setBrush(QBrush(QColor(sk["head"])))
        painter.drawEllipse(QRectF(hcx - hr, hcy - hr, hr * 2, hr * 2))

        # Crown tuft
        tu = QPainterPath()
        tu.moveTo(hcx - 3.0, hcy - hr + 2.0)
        tu.quadTo(hcx - 4.0, hcy - hr - 8.0, hcx + 2.0, hcy - hr - 5.0)
        tu.quadTo(hcx + 5.0, hcy - hr - 11.0, hcx + 7.0, hcy - hr)
        painter.drawPath(tu)

        # Beak
        self._draw_goose_beak(painter, sk, outline)

        # Face & Eyes (Laser eyes if rage!)
        self._draw_face(painter, sk, outline, ex=24.0, ey=-101.0)

        # Accessories (Skins & Items)
        self._draw_accessories(painter, sk)

        # 22+ Idle Animations Drawer (if active)
        if self.current_idle_action and not is_running:
            self._draw_idle_action(painter, sk)

        # Stolen Item held in beak (Untitled Goose Theft!)
        if self.stolen_item:
            self._draw_stolen_item(painter, self.stolen_item)

    def _draw_goose_beak(self, painter: QPainter, sk: Dict, outline: QPen):
        bk = QColor(sk["beak"])
        bki = QColor(sk["beak_inside"])
        bx, by = 32.0, -95.0
        open_r = self.mouth_open_ratio if self.expression in ("talking", "eating") else 0.0

        if open_r > 0.05:
            gap = open_r * 8.0
            cav = QPainterPath()
            cav.moveTo(bx, by - 2.0)
            cav.lineTo(bx + 20.0, by + 1.0)
            cav.lineTo(bx, by + gap + 1.0)
            cav.closeSubpath()
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(bki))
            painter.drawPath(cav)

            upper = QPainterPath()
            upper.moveTo(bx, by - 5.0)
            upper.lineTo(bx + 24.0, by - 3.0)
            upper.quadTo(bx + 26.0, by + 1.0, bx + 22.0, by + 2.0)
            upper.lineTo(bx, by - 1.0)
            upper.closeSubpath()
            painter.setPen(outline)
            painter.setBrush(QBrush(bk))
            painter.drawPath(upper)

            lower = QPainterPath()
            lower.moveTo(bx + 2.0, by + 2.0)
            lower.lineTo(bx + 22.0, by + 2.0 + gap)
            lower.quadTo(bx + 14.0, by + 7.0 + gap, bx + 2.0, by + 4.0 + gap)
            lower.closeSubpath()
            painter.drawPath(lower)
        elif self.expression == "judging":
            flat = QPainterPath()
            flat.moveTo(bx, by - 4.0)
            flat.lineTo(bx + 24.0, by - 2.0)
            flat.quadTo(bx + 26.0, by + 1.0, bx + 22.0, by + 3.0)
            flat.lineTo(bx, by + 3.0)
            flat.closeSubpath()
            painter.setPen(outline)
            painter.setBrush(QBrush(bk))
            painter.drawPath(flat)
        else:
            bill = QPainterPath()
            bill.moveTo(bx, by - 5.0)
            bill.cubicTo(bx + 18.0, by - 7.0, bx + 26.0, by - 2.0, bx + 26.0, by + 2.0)
            bill.cubicTo(bx + 24.0, by + 6.0, bx + 14.0, by + 5.0, bx, by + 4.0)
            bill.closeSubpath()
            painter.setPen(outline)
            painter.setBrush(QBrush(bk))
            painter.drawPath(bill)

            painter.setPen(QPen(QColor(sk["outline"]), 1.4))
            painter.drawLine(QPointF(bx + 6.0, by - 1.0), QPointF(bx + 11.0, by - 1.0))

    def _draw_rubber_duck(self, painter: QPainter, sk: Dict, outline: QPen):
        painter.setPen(outline)
        painter.setBrush(QBrush(QColor(sk["leg"])))
        for side in [-1, 1]:
            lx = side * 8.0
            painter.drawRoundedRect(QRectF(lx - 2.0, -4.0, 4.0, 12.0), 1.5, 1.5)
            painter.setBrush(QBrush(QColor(sk["foot"])))
            fp = QPainterPath()
            fp.moveTo(lx, 8.0)
            fp.quadTo(lx + side * 10.0, 6.0, lx + side * 14.0, 13.0)
            fp.quadTo(lx + side * 6.0, 16.0, lx, 14.0)
            fp.quadTo(lx - side * 2.0, 14.0, lx, 8.0)
            fp.closeSubpath()
            painter.drawPath(fp)
            painter.setBrush(QBrush(QColor(sk["leg"])))

        painter.setPen(outline)
        painter.setBrush(QBrush(QColor(sk["body"])))
        painter.drawEllipse(QRectF(-32.0, -44.0, 64.0, 46.0))

        b = QPainterPath()
        b.moveTo(6.0, -34.0)
        b.cubicTo(30.0, -28.0, 30.0, -6.0, 10.0, -2.0)
        b.quadTo(0.0, -14.0, 6.0, -34.0)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(sk["belly"])))
        painter.drawPath(b)

        t = QPainterPath()
        t.moveTo(-25.0, -18.0)
        t.quadTo(-42.0, -34.0, -36.0, -40.0)
        t.quadTo(-30.0, -34.0, -22.0, -24.0)
        t.closeSubpath()
        painter.setPen(outline)
        painter.setBrush(QBrush(QColor(sk["body"])))
        painter.drawPath(t)

        w = QPainterPath()
        w.moveTo(-14.0, -26.0)
        w.cubicTo(-16.0, -10.0, 10.0, -8.0, 7.0, -22.0)
        w.quadTo(-3.0, -32.0, -14.0, -26.0)
        painter.drawPath(w)

        hcx, hcy, hr = 16.0, -58.0, 21.0
        painter.setPen(outline)
        painter.setBrush(QBrush(QColor(sk["head"])))
        painter.drawEllipse(QRectF(hcx - hr, hcy - hr, hr * 2, hr * 2))

        bk = QColor(sk["beak"])
        bx, by = 32.0, -56.0
        bill = QPainterPath()
        bill.moveTo(bx, by - 5.0)
        bill.cubicTo(bx + 12.0, by - 6.0, bx + 20.0, by - 2.0, bx + 20.0, by + 2.0)
        bill.cubicTo(bx + 18.0, by + 5.0, bx + 10.0, by + 5.0, bx, by + 4.0)
        bill.closeSubpath()
        painter.setBrush(QBrush(bk))
        painter.drawPath(bill)

        self._draw_face(painter, sk, outline, ex=24.0, ey=-63.0)

    def _draw_face(self, painter: QPainter, sk: Dict, outline: QPen, ex: float, ey: float):
        er = 5.0
        # FULL-SCREEN PIERCING LASER BEAM (Super Saiyan Rage!)
        if self.is_super_rage:
            beam_pulse = math.sin(self.breathing_time * 35.0) * 4.0
            # 1. Blazing red & gold energy eye orbs
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(QColor(255, 255, 220)))
            painter.drawEllipse(QRectF(ex - 7.0, ey - 7.0, 14.0, 14.0))
            painter.setBrush(QBrush(QColor(255, 30, 60, 230)))
            painter.drawEllipse(QRectF(ex - 10.0, ey - 10.0, 20.0, 20.0))

            # 2. Outer massive laser glow beam across entire screen width
            outer_pen = QPen(QColor(255, 30, 60, 130), 26.0 + beam_pulse)
            outer_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            painter.setPen(outer_pen)
            painter.drawLine(QPointF(ex, ey), QPointF(ex + 480.0, ey))

            # 3. Inner vibrant crimson-orange beam
            mid_pen = QPen(QColor(255, 120, 30, 220), 13.0 + beam_pulse * 0.5)
            painter.setPen(mid_pen)
            painter.drawLine(QPointF(ex, ey), QPointF(ex + 480.0, ey))

            # 4. White-hot core energy beam
            core_pen = QPen(QColor(255, 255, 255, 250), 5.0)
            painter.setPen(core_pen)
            painter.drawLine(QPointF(ex, ey), QPointF(ex + 480.0, ey))

            # 5. Electric energy arcs & lightning crackles radiating from beam
            painter.setPen(QPen(QColor(255, 235, 120, 220), 1.6))
            for i in range(5):
                lx = ex + 35.0 + i * 85.0
                ly = ey + math.sin(self.breathing_time * 45.0 + i * 1.8) * 16.0
                painter.drawLine(QPointF(lx, ey), QPointF(lx + 18.0, ly))
                painter.drawLine(QPointF(lx + 18.0, ly), QPointF(lx + 36.0, ey))
            return

        blush = QColor(sk["blush"])
        blush.setAlpha(165)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(blush))
        painter.drawEllipse(QRectF(ex - 1.0, ey + 7.0, 11.0, 6.0))

        if self.expression == "sleeping":
            pen = QPen(QColor(sk["outline"]), 2.4)
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            arc = QPainterPath()
            arc.moveTo(ex - er - 1.0, ey)
            arc.quadTo(ex, ey - 4.5, ex + er + 1.0, ey)
            painter.drawPath(arc)
        elif self.expression == "judging":
            sq = QPainterPath()
            sq.moveTo(ex - er - 2.0, ey - 2.0)
            sq.lineTo(ex + er + 2.0, ey + 1.5)
            sq.quadTo(ex, ey + 4.5, ex - er - 2.0, ey - 2.0)
            painter.setPen(outline)
            painter.setBrush(QBrush(QColor(sk["eye"])))
            painter.drawPath(sq)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(QColor(sk["eye_highlight"])))
            painter.drawEllipse(QRectF(ex + 1.0, ey, 2.2, 2.2))
        else:
            eh = er * 2.0 * (1.0 - self.blink_progress * 0.95)
            ew = er * 2.0 * (1.0 + self.blink_progress * 0.2)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(QColor(sk["eye"])))
            painter.drawEllipse(QRectF(ex - ew / 2.0, ey - eh / 2.0, ew, eh))
            if self.blink_progress < 0.6:
                painter.setBrush(QBrush(QColor(sk["eye_highlight"])))
                painter.drawEllipse(QRectF(ex + 0.5, ey - eh / 2.0 + 1.5, 2.2, 2.2 * (1.0 - self.blink_progress)))

    def _draw_rage_aura(self, painter: QPainter):
        """Flames and energy sparks radiating around goose in Super Saiyan mode."""
        painter.save()
        for i in range(8):
            ang = (i / 8.0) * math.pi * 2.0 + self.breathing_time * 8.0
            dist = 42.0 + math.sin(ang * 3.0) * 8.0
            px = math.cos(ang) * dist
            py = math.sin(ang) * dist - 50.0
            flame_r = random.uniform(5.0, 12.0)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(QColor(255, random.randint(140, 220), 0, 160)))
            painter.drawEllipse(QRectF(px - flame_r, py - flame_r, flame_r * 2, flame_r * 2))
        painter.restore()

    # ------------------------------------------------------------------
    # 22+ PROCEDURAL IDLE ANIMATIONS
    # ------------------------------------------------------------------
    def _draw_idle_action(self, painter: QPainter, sk: Dict):
        act = self.current_idle_action
        t = self.idle_action_timer

        # 1. SPAGHETTI SNAP (User explicitly requested!)
        if act == "spaghetti":
            self._anim_spaghetti(painter, t)

        # 2. PHONE DOOMSCROLL (User explicitly requested!)
        elif act == "phone_scroll":
            self._anim_phone_scroll(painter, t)

        # 3. BOBA MILK TEA
        elif act == "boba":
            self._anim_boba(painter, t)

        # 4. JUGGLING BALLS
        elif act == "juggle":
            self._anim_juggle(painter, t)

        # 5. YAWN & WING STRETCH
        elif act == "yawn_stretch":
            self._anim_yawn(painter, t)

        # 6. RAMEN NOODLES
        elif act == "ramen":
            self._anim_ramen(painter, t)

        # 7. RUBIK'S CUBE
        elif act == "rubiks_cube":
            self._anim_rubiks_cube(painter, t)

        # 8. COIN FLIP
        elif act == "coin_flip":
            self._anim_coin_flip(painter, t)

        # 9. ACOUSTIC GUITAR
        elif act == "guitar":
            self._anim_guitar(painter, t)

        # 10. BUBBLEGUM POP
        elif act == "bubblegum":
            self._anim_bubblegum(painter, t)

        # 11. POLAROID FLASH
        elif act == "polaroid":
            self._anim_polaroid(painter, t)

        # 12. MAGNIFYING GLASS
        elif act == "magnifying_glass":
            self._anim_magnifying_glass(painter, t)

        # 13. PUSHUPS
        elif act == "pushups":
            self._anim_pushups(painter, t)

        # 14. FIDGET SPINNER
        elif act == "fidget_spinner":
            self._anim_fidget_spinner(painter, t)

        # 15. DEAL WITH IT SUNGLASSES
        elif act == "deal_with_it":
            self._anim_deal_with_it(painter, t)

        # 16. HULA HOOP
        elif act == "hula_hoop":
            self._anim_hula_hoop(painter, t)

        # 17. WRISTWATCH CHECK
        elif act == "watch_check":
            self._anim_watch_check(painter, t)

        # 18. BINOCULARS
        elif act == "binoculars":
            self._anim_binoculars(painter, t)

        # 19. PIZZA SLICE
        elif act == "pizza":
            self._anim_pizza(painter, t)

        # 20. LASER CHASE
        elif act == "laser_chase":
            self._anim_laser_chase(painter, t)

        # 21. MAGIC TOP HAT RABBIT
        elif act == "magic_rabbit":
            self._anim_magic_rabbit(painter, t)

        # 22. ACHOO SNEEZE
        elif act == "sneeze":
            self._anim_sneeze(painter, t)

    def _anim_spaghetti(self, painter: QPainter, t: float):
        """Brings out a long uncooked spaghetti strand, bends it, and *SNAPS* it!"""
        sp_pen = QPen(QColor("#F4D03F"), 2.2)
        painter.setPen(sp_pen)

        if not self.spaghetti_broken:
            # Bending spaghetti curve
            bend = min(12.0, t * 6.0)
            p = QPainterPath()
            p.moveTo(14.0, -40.0)
            p.quadTo(30.0, -40.0 - bend, 46.0, -40.0)
            painter.drawPath(p)
        else:
            # Broken into two pieces flying apart!
            dt = t - 2.0
            painter.drawLine(QPointF(14.0 - dt * 6.0, -40.0 - dt * 4.0), QPointF(28.0 - dt * 10.0, -44.0 + dt * 8.0))
            painter.drawLine(QPointF(32.0 + dt * 10.0, -44.0 + dt * 8.0), QPointF(46.0 + dt * 6.0, -40.0 - dt * 4.0))

            # Snap sparkles
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(QColor("#FFEA00")))
            painter.drawEllipse(QRectF(29.0, -42.0, 4.0, 4.0))

    def _anim_phone_scroll(self, painter: QPainter, t: float):
        """Goose holds a tiny smartphone and doomscrolls with its wing tip!"""
        # Phone body
        painter.setPen(QPen(QColor("#111827"), 1.2))
        painter.setBrush(QBrush(QColor("#1F2937")))
        painter.drawRoundedRect(QRectF(30.0, -50.0, 16.0, 26.0), 2.5, 2.5)

        # Glowing screen with content lines
        painter.setBrush(QBrush(QColor("#38BDF8")))
        painter.drawRect(QRectF(32.0, -47.0, 12.0, 20.0))

        # Blue screen reflection glow on goose face
        glow = QRadialGradient(24.0, -95.0, 25.0)
        glow.setColorAt(0.0, QColor(56, 189, 248, 80))
        glow.setColorAt(1.0, QColor(56, 189, 248, 0))
        painter.setBrush(QBrush(glow))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QRectF(10.0, -110.0, 30.0, 30.0))

        # Swiping wing tip
        swipe_y = math.sin(t * 8.0) * 4.0
        painter.setPen(QPen(QColor("#FFA04D"), 2.0))
        painter.drawLine(QPointF(24.0, -38.0), QPointF(36.0, -38.0 + swipe_y))

    def _anim_boba(self, painter: QPainter, t: float):
        # Boba cup
        cup = QPainterPath()
        cup.moveTo(34.0, -50.0); cup.lineTo(46.0, -50.0)
        cup.lineTo(43.0, -26.0); cup.lineTo(37.0, -26.0); cup.closeSubpath()
        painter.setPen(QPen(QColor("#4B5563"), 1.2))
        painter.setBrush(QBrush(QColor(217, 119, 6, 180)))  # Milk tea
        painter.drawPath(cup)

        # Tapioca pearls at bottom
        painter.setBrush(QBrush(QColor("#111827")))
        for ox in [39.0, 42.0, 40.5]:
            painter.drawEllipse(QRectF(ox - 1.5, -29.0, 3.0, 3.0))

        # Purple wide straw into beak
        painter.setPen(QPen(QColor("#8B5CF6"), 2.2))
        painter.drawLine(QPointF(40.0, -28.0), QPointF(32.0, -92.0))

    def _anim_juggle(self, painter: QPainter, t: float):
        colors = ["#EF4444", "#10B981", "#3B82F6"]
        for i, col in enumerate(colors):
            phase = (t * 2.0 + i * (math.pi * 2.0 / 3.0)) % (math.pi * 2.0)
            jx = 32.0 + math.cos(phase) * 22.0
            jy = -65.0 - abs(math.sin(phase)) * 32.0
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(QColor(col)))
            painter.drawEllipse(QRectF(jx - 3.5, jy - 3.5, 7.0, 7.0))

    def _anim_yawn(self, painter: QPainter, t: float):
        # Wings wide stretch
        stretch = math.sin(min(math.pi, t * 1.5)) * 20.0
        painter.setPen(QPen(QColor("#40454D"), 2.0))
        painter.setBrush(QBrush(QColor("#FFFFFF")))
        # Left wing outstretched
        painter.drawLine(QPointF(-16.0, -32.0), QPointF(-44.0 - stretch * 0.5, -50.0))
        # Right wing outstretched
        painter.drawLine(QPointF(16.0, -32.0), QPointF(44.0 + stretch * 0.5, -50.0))

    def _anim_ramen(self, painter: QPainter, t: float):
        # Bowl
        bowl = QPainterPath()
        bowl.moveTo(30.0, -42.0); bowl.quadTo(44.0, -22.0, 58.0, -42.0); bowl.closeSubpath()
        painter.setPen(QPen(QColor("#B91C1C"), 1.4))
        painter.setBrush(QBrush(QColor("#DC2626")))
        painter.drawPath(bowl)
        # Chopsticks lifting noodles
        painter.setPen(QPen(QColor("#FDE047"), 1.8))
        painter.drawLine(QPointF(44.0, -38.0), QPointF(36.0, -88.0))
        painter.setPen(QPen(QColor("#92400E"), 1.5))
        painter.drawLine(QPointF(38.0, -84.0), QPointF(52.0, -78.0))

    def _anim_rubiks_cube(self, painter: QPainter, t: float):
        cx, cy = 36.0, -40.0
        painter.setPen(QPen(QColor("#000000"), 1.0))
        face_colors = ["#EF4444", "#3B82F6", "#10B981", "#F59E0B"]
        for row in range(2):
            for col in range(2):
                colr = face_colors[(row * 2 + col + int(t * 3.0)) % 4]
                painter.setBrush(QBrush(QColor(colr)))
                painter.drawRect(QRectF(cx + col * 7.0, cy + row * 7.0, 6.0, 6.0))

    def _anim_coin_flip(self, painter: QPainter, t: float):
        spin_phase = (t * 6.0) % (math.pi * 2.0)
        cy = -65.0 - abs(math.sin(t * 2.5)) * 36.0
        coin_w = abs(math.cos(spin_phase)) * 9.0 + 1.0
        painter.setPen(QPen(QColor("#B45309"), 1.0))
        painter.setBrush(QBrush(QColor("#FBBF24")))
        painter.drawEllipse(QRectF(38.0 - coin_w / 2.0, cy - 4.5, coin_w, 9.0))

    def _anim_guitar(self, painter: QPainter, t: float):
        # Mini ukulele body
        painter.setPen(QPen(QColor("#78350F"), 1.2))
        painter.setBrush(QBrush(QColor("#D97706")))
        painter.drawEllipse(QRectF(28.0, -45.0, 18.0, 22.0))
        # Neck
        painter.setBrush(QBrush(QColor("#92400E")))
        painter.drawRect(QRectF(35.0, -66.0, 4.0, 22.0))
        # Musical note floating
        painter.setPen(QPen(QColor("#8B5CF6"), 1.5))
        painter.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        painter.drawText(QPointF(48.0, -60.0 - (t * 6.0) % 20.0), "♫")

    def _anim_bubblegum(self, painter: QPainter, t: float):
        if not self.bubblegum_popped:
            r = min(14.0, t * 5.0)
            painter.setPen(QPen(QColor("#F472B6"), 1.2))
            painter.setBrush(QBrush(QColor(244, 114, 182, 210)))
            painter.drawEllipse(QRectF(35.0 - r, -95.0 - r, r * 2, r * 2))
        else:
            # Splattered pink gum on beak!
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(QColor("#EC4899")))
            painter.drawEllipse(QRectF(33.0, -97.0, 8.0, 6.0))

    def _anim_polaroid(self, painter: QPainter, t: float):
        # Camera
        painter.setPen(QPen(QColor("#374151"), 1.2))
        painter.setBrush(QBrush(QColor("#F3F4F6")))
        painter.drawRoundedRect(QRectF(30.0, -50.0, 20.0, 16.0), 2.0, 2.0)
        # Lens
        painter.setBrush(QBrush(QColor("#111827")))
        painter.drawEllipse(QRectF(37.0, -45.0, 6.0, 6.0))
        # Flash
        if 1.0 < t < 1.3:
            painter.setBrush(QBrush(QColor(255, 255, 255, 220)))
            painter.drawEllipse(QRectF(15.0, -80.0, 50.0, 50.0))

    def _anim_magnifying_glass(self, painter: QPainter, t: float):
        mx = 28.0 + math.sin(t * 3.0) * 8.0
        my = -20.0
        painter.setPen(QPen(QColor("#1E293B"), 2.2))
        painter.setBrush(QBrush(QColor(186, 230, 253, 90)))
        painter.drawEllipse(QRectF(mx - 8.0, my - 8.0, 16.0, 16.0))
        painter.drawLine(QPointF(mx + 6.0, my + 6.0), QPointF(mx + 14.0, my + 14.0))

    def _anim_pushups(self, painter: QPainter, t: float):
        # Fast wing pushups
        push_y = abs(math.sin(t * 10.0)) * 6.0
        painter.setPen(QPen(QColor("#FFA04D"), 2.0))
        painter.drawLine(QPointF(-16.0, -6.0 + push_y), QPointF(-24.0, 6.0))
        painter.drawLine(QPointF(16.0, -6.0 + push_y), QPointF(24.0, 6.0))
        # Sweat droplet
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor("#38BDF8")))
        painter.drawEllipse(QRectF(32.0, -90.0, 3.5, 4.5))

    def _anim_fidget_spinner(self, painter: QPainter, t: float):
        fx, fy = 42.0, -96.0
        spin_ang = t * 25.0
        painter.save()
        painter.translate(fx, fy)
        painter.rotate(math.degrees(spin_ang))
        painter.setPen(Qt.PenStyle.NoPen)
        for ang in [0, 120, 240]:
            rad = math.radians(ang)
            px = math.cos(rad) * 9.0
            py = math.sin(rad) * 9.0
            painter.setBrush(QBrush(QColor("#06B6D4")))
            painter.drawEllipse(QRectF(px - 3.5, py - 3.5, 7.0, 7.0))
        painter.setBrush(QBrush(QColor("#0891B2")))
        painter.drawEllipse(QRectF(-2.5, -2.5, 5.0, 5.0))
        painter.restore()

    def _anim_deal_with_it(self, painter: QPainter, t: float):
        # 8-bit black shades sliding down from sky
        drop = min(36.0, t * 18.0)
        sy = -135.0 + drop
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor("#000000")))
        painter.drawRect(QRectF(14.0, sy, 22.0, 6.0))
        painter.drawRect(QRectF(18.0, sy + 6.0, 5.0, 3.0))
        painter.drawRect(QRectF(28.0, sy + 6.0, 5.0, 3.0))
        # White pixel shine
        painter.setBrush(QBrush(QColor("#FFFFFF")))
        painter.drawRect(QRectF(16.0, sy + 1.0, 2.0, 2.0))
        painter.drawRect(QRectF(26.0, sy + 1.0, 2.0, 2.0))

    def _anim_hula_hoop(self, painter: QPainter, t: float):
        hx = math.sin(t * 8.0) * 12.0
        painter.setPen(QPen(QColor("#F43F5E"), 2.2))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(QRectF(-24.0 + hx, -38.0, 48.0, 12.0))

    def _anim_watch_check(self, painter: QPainter, t: float):
        # Mini golden wristwatch
        painter.setPen(QPen(QColor("#F59E0B"), 1.5))
        painter.setBrush(QBrush(QColor("#FDE68A")))
        painter.drawEllipse(QRectF(12.0, -32.0, 6.0, 6.0))
        # Tapping foot
        tap = abs(math.sin(t * 6.0)) * 4.0
        painter.drawLine(QPointF(10.0, 10.0 - tap), QPointF(16.0, 12.0 - tap))

    def _anim_binoculars(self, painter: QPainter, t: float):
        bx = 28.0 + math.sin(t * 2.0) * 6.0
        painter.setPen(QPen(QColor("#1F2937"), 1.2))
        painter.setBrush(QBrush(QColor("#4B5563")))
        painter.drawRoundedRect(QRectF(bx, -102.0, 7.0, 12.0), 1.5, 1.5)
        painter.drawRoundedRect(QRectF(bx + 8.0, -102.0, 7.0, 12.0), 1.5, 1.5)
        painter.drawLine(QPointF(bx + 6.0, -96.0), QPointF(bx + 9.0, -96.0))

    def _anim_pizza(self, painter: QPainter, t: float):
        # Pizza slice
        p = QPainterPath()
        p.moveTo(34.0, -90.0); p.lineTo(52.0, -78.0); p.lineTo(46.0, -64.0); p.closeSubpath()
        painter.setPen(QPen(QColor("#D97706"), 1.2))
        painter.setBrush(QBrush(QColor("#FBBF24")))
        painter.drawPath(p)
        # Pepperoni dots
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor("#DC2626")))
        painter.drawEllipse(QRectF(42.0, -78.0, 3.5, 3.5))

    def _anim_laser_chase(self, painter: QPainter, t: float):
        # Red laser dot darting around taskbar
        lx = math.sin(t * 5.0) * 35.0
        ly = -8.0 + math.cos(t * 4.0) * 6.0
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor("#EF4444")))
        painter.drawEllipse(QRectF(lx - 3.0, ly - 3.0, 6.0, 6.0))
        glow = QRadialGradient(lx, ly, 8.0)
        glow.setColorAt(0.0, QColor(239, 68, 68, 140))
        glow.setColorAt(1.0, QColor(239, 68, 68, 0))
        painter.setBrush(QBrush(glow))
        painter.drawEllipse(QRectF(lx - 8.0, ly - 8.0, 16.0, 16.0))

    def _anim_magic_rabbit(self, painter: QPainter, t: float):
        # Top hat
        painter.setPen(QPen(QColor("#111827"), 1.2))
        painter.setBrush(QBrush(QColor("#1F2937")))
        painter.drawRoundedRect(QRectF(30.0, -42.0, 20.0, 16.0), 1.0, 1.0)
        painter.drawLine(QPointF(26.0, -42.0), QPointF(54.0, -42.0))
        # White bunny emerging
        hop = min(12.0, t * 4.0)
        painter.setBrush(QBrush(QColor("#FFFFFF")))
        painter.drawEllipse(QRectF(36.0, -42.0 - hop, 8.0, 8.0))
        # Bunny ears
        painter.drawEllipse(QRectF(37.0, -48.0 - hop, 2.5, 7.0))
        painter.drawEllipse(QRectF(41.0, -48.0 - hop, 2.5, 7.0))

    def _anim_sneeze(self, painter: QPainter, t: float):
        if t < 1.5:
            # Inhale shudder
            shiver = math.sin(t * 30.0) * 2.0
            painter.setPen(QPen(QColor("#38BDF8"), 1.0))
            painter.drawText(QPointF(34.0, -104.0), "Ah...")
        else:
            # ACHOO!
            painter.setPen(QPen(QColor("#0284C7"), 2.0))
            painter.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
            painter.drawText(QPointF(36.0, -96.0), "ACHOO!!")

    # ------------------------------------------------------------------
    # STOLEN ITEMS (Untitled Goose Mode)
    # ------------------------------------------------------------------
    def _draw_stolen_item(self, painter: QPainter, item: str):
        ix, iy = 42.0, -94.0

        if item == "bell":
            # Shiny golden brass bell ringing
            painter.setPen(QPen(QColor("#B45309"), 1.2))
            painter.setBrush(QBrush(QColor("#FBBF24")))
            bell = QPainterPath()
            bell.moveTo(ix, iy); bell.quadTo(ix + 6.0, iy + 10.0, ix + 12.0, iy + 10.0)
            bell.lineTo(ix - 12.0, iy + 10.0); bell.quadTo(ix - 6.0, iy + 10.0, ix, iy)
            painter.drawPath(bell)
            # Clapper
            painter.setBrush(QBrush(QColor("#78350F")))
            painter.drawEllipse(QRectF(ix - 2.0, iy + 10.0, 4.0, 4.0))

        elif item == "key":
            painter.setPen(QPen(QColor("#B45309"), 1.5))
            painter.setBrush(QBrush(QColor("#FDE047")))
            painter.drawEllipse(QRectF(ix - 4.0, iy - 4.0, 8.0, 8.0))
            painter.drawLine(QPointF(ix + 4.0, iy), QPointF(ix + 18.0, iy))
            painter.drawLine(QPointF(ix + 14.0, iy), QPointF(ix + 14.0, iy + 4.0))

        elif item == "mug":
            painter.setPen(QPen(QColor("#7F1D1D"), 1.2))
            painter.setBrush(QBrush(QColor("#DC2626")))
            painter.drawRoundedRect(QRectF(ix, iy - 2.0, 12.0, 14.0), 2.0, 2.0)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawArc(QRectF(ix + 10.0, iy + 1.0, 6.0, 8.0), -90 * 16, 180 * 16)

        elif item == "scissors":
            painter.setPen(QPen(QColor("#4B5563"), 1.8))
            painter.drawLine(QPointF(ix, iy), QPointF(ix + 14.0, iy - 4.0))
            painter.drawLine(QPointF(ix, iy), QPointF(ix + 14.0, iy + 4.0))
            painter.setBrush(QBrush(QColor("#EF4444")))
            painter.drawEllipse(QRectF(ix - 5.0, iy - 5.0, 6.0, 6.0))

        elif item == "pointer":
            # Stolen Windows cursor arrow!
            p = QPainterPath()
            p.moveTo(ix, iy)
            p.lineTo(ix + 12.0, iy + 8.0)
            p.lineTo(ix + 6.0, iy + 8.0)
            p.lineTo(ix + 9.0, iy + 15.0)
            p.lineTo(ix + 6.0, iy + 16.0)
            p.lineTo(ix + 3.0, iy + 9.0)
            p.lineTo(ix, iy + 12.0)
            p.closeSubpath()
            painter.setPen(QPen(QColor("#000000"), 1.5))
            painter.setBrush(QBrush(QColor("#FFFFFF")))
            painter.drawPath(p)

    # ------------------------------------------------------------------
    # ACCESSORIES: CHEF, DETECTIVE, NINJA, KING, SMOKING, CODER, ETC.
    # ------------------------------------------------------------------
    def _draw_accessories(self, painter: QPainter, sk: Dict):
        acc = sk.get("accessory", "none")

        # Chef Cooker Toque Hat & Wooden Spoon
        if acc == "cooker":
            # Puffy white chef toque hat
            toque = QPainterPath()
            toque.moveTo(6.0, -114.0)
            toque.quadTo(4.0, -132.0, 14.0, -136.0)
            toque.quadTo(20.0, -144.0, 28.0, -136.0)
            toque.quadTo(36.0, -130.0, 32.0, -114.0)
            toque.closeSubpath()
            painter.setPen(QPen(QColor("#4B5563"), 1.5))
            painter.setBrush(QBrush(QColor("#FFFFFF")))
            painter.drawPath(toque)
            # Red neckerchief
            painter.setBrush(QBrush(QColor("#DC2626")))
            painter.drawRect(QRectF(10.0, -84.0, 12.0, 4.0))
            # Wooden spoon in wing
            painter.setPen(QPen(QColor("#92400E"), 1.8))
            painter.drawLine(QPointF(14.0, -28.0), QPointF(32.0, -38.0))
            painter.setBrush(QBrush(QColor("#B45309")))
            painter.drawEllipse(QRectF(30.0, -42.0, 7.0, 8.0))

        # Detective Deerstalker Hat & Magnifying Glass
        elif acc == "detective":
            painter.setPen(QPen(QColor("#3D2B1F"), 1.5))
            painter.setBrush(QBrush(QColor("#78350F")))
            # Hat dome
            painter.drawChord(QRectF(6.0, -122.0, 28.0, 20.0), 0, 180 * 16)
            # Front & back brims
            painter.drawLine(QPointF(2.0, -112.0), QPointF(12.0, -112.0))
            painter.drawLine(QPointF(28.0, -112.0), QPointF(38.0, -112.0))

        # Ninja Cowl & Red Headband
        elif acc == "ninja":
            # Red headband with fluttering trailing ties
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(QColor("#E71D36")))
            painter.drawRect(QRectF(6.0, -106.0, 26.0, 4.0))
            # Trailing ties
            tail = QPainterPath()
            tail.moveTo(6.0, -106.0)
            tail.quadTo(-6.0, -102.0, -14.0, -96.0)
            tail.lineTo(-12.0, -92.0)
            tail.quadTo(-4.0, -100.0, 6.0, -102.0)
            tail.closeSubpath()
            painter.drawPath(tail)

        # Royal King Crown & Velvet Cape
        elif acc == "king":
            # Golden crown with rubies
            crown = QPainterPath()
            crown.moveTo(6.0, -114.0)
            crown.lineTo(8.0, -126.0)
            crown.lineTo(16.0, -118.0)
            crown.lineTo(22.0, -128.0)
            crown.lineTo(28.0, -118.0)
            crown.lineTo(34.0, -126.0)
            crown.lineTo(36.0, -114.0)
            crown.closeSubpath()
            painter.setPen(QPen(QColor("#B45309"), 1.5))
            painter.setBrush(QBrush(QColor("#FBBF24")))
            painter.drawPath(crown)
            # Rubies
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(QColor("#DC2626")))
            painter.drawEllipse(QRectF(20.5, -122.0, 3.5, 3.5))

        # Smoking Goose
        elif acc == "smoking" and (self.is_smoking or self.lighter_progress > 0.05):
            self._draw_smoking_props(painter)

        # Coder Laptop
        elif acc == "laptop":
            if self.expression == "judging":
                self._draw_glasses(painter, sk, 24.0, -100.0)
            self._draw_laptop(painter, sk)

        # Wizard Hat
        elif acc == "hat":
            self._draw_wizard_hat(painter, sk)

        # Cyber Visor
        elif acc == "visor":
            self._draw_visor(painter)

        # Coffee Cup
        elif acc == "coffee":
            self._draw_coffee_cup(painter, sk)

        # Glasses for judging
        if self.expression == "judging" and acc not in ("laptop",):
            self._draw_glasses(painter, sk, 24.0, -100.0)

        # DJ Turntable Deck & Headphones
        if self.is_dj_mode:
            self._draw_dj_mode(painter, sk)

    def _draw_smoking_props(self, painter: QPainter):
        """Realistic classic white filtered cigarette held firmly in the beak with real flame & smoke."""
        cig_x, cig_y = 38.0, -95.0
        cig_len = 22.0

        painter.save()
        painter.translate(cig_x, cig_y)
        painter.rotate(-8.0)

        # 1. Tan/Amber Filter (6mm) clamped in beak
        painter.setPen(QPen(QColor("#78350F"), 0.8))
        painter.setBrush(QBrush(QColor("#D97706")))
        painter.drawRoundedRect(QRectF(0.0, -1.8, 6.0, 3.6), 1.0, 1.0)

        # 2. White paper cylinder (14mm)
        painter.setPen(QPen(QColor("#CBD5E1"), 0.8))
        painter.setBrush(QBrush(QColor("#FFFFFF")))
        painter.drawRect(QRectF(6.0, -1.8, 14.0, 3.6))

        # 3. Glowing burning ember cherry at the tip
        ember_glow = abs(math.sin(self.breathing_time * 4.0)) * 60
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(255, int(60 + ember_glow), 0)))
        painter.drawEllipse(QRectF(cig_len - 2.5, -2.0, 4.5, 4.0))

        # 4. Fine gray ash tip
        painter.setBrush(QBrush(QColor("#71717A")))
        painter.drawRoundedRect(QRectF(cig_len + 1.0, -1.5, 2.5, 3.0), 0.8, 0.8)
        painter.restore()

        # Zippo lighter flicking flame beneath the cigarette tip
        lp = self.lighter_progress
        if lp > 0.1:
            lx = 42.0
            ly = -75.0 - lp * 16.0
            painter.save()
            painter.setPen(QPen(QColor("#1A1C20"), 1.2))
            painter.setBrush(QBrush(QColor("#94A3B8")))  # Shiny chrome lighter
            painter.drawRoundedRect(QRectF(lx, ly, 11.0, 16.0), 2.0, 2.0)

            # Flip-open lid
            lid = QPainterPath()
            lid.moveTo(lx, ly)
            lid.lineTo(lx - 6.0, ly - 7.0)
            lid.lineTo(lx + 4.0, ly - 9.0)
            lid.lineTo(lx + 10.0, ly)
            lid.closeSubpath()
            painter.setBrush(QBrush(QColor("#64748B")))
            painter.drawPath(lid)

            # Chimney & spark wheel
            painter.setBrush(QBrush(QColor("#CBD5E1")))
            painter.drawRect(QRectF(lx + 2.0, ly - 5.0, 7.0, 5.0))

            # Realistic yellow-orange flame with blue inner core
            if self.idle_seconds < 13.5:
                flame_h = 11.0 + math.sin(self.breathing_time * 28.0) * 3.5
                flame = QPainterPath()
                flame.moveTo(lx + 3.0, ly - 5.0)
                flame.quadTo(lx + 5.5 + math.sin(self.breathing_time * 22.0) * 2.0, ly - 5.0 - flame_h, lx + 8.0, ly - 5.0)
                flame.closeSubpath()
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(QBrush(QColor(255, 180, 0, 230)))
                painter.drawPath(flame)
                core = QPainterPath()
                core.moveTo(lx + 4.0, ly - 5.0)
                core.quadTo(lx + 5.5, ly - 9.0, lx + 7.0, ly - 5.0)
                core.closeSubpath()
                painter.setBrush(QBrush(QColor(59, 130, 246, 210)))
                painter.drawPath(core)
            painter.restore()

    def _draw_laptop(self, painter: QPainter, sk: Dict):
        """Active Coder Laptop with scrolling green phosphor matrix code and typing wings!"""
        bx, by = 18.0, -8.0
        kw = 38.0
        kh = 8.0
        painter.setPen(QPen(QColor("#191A21"), 1.3))
        painter.setBrush(QBrush(QColor("#44475A")))
        painter.drawRoundedRect(QRectF(bx, by - 4.0, kw, kh), 2.0, 2.0)

        # Keyboard base
        painter.setPen(QPen(QColor("#282A36"), 0.8))
        painter.setBrush(QBrush(QColor("#21222C")))
        painter.drawRect(QRectF(bx + 2.0, by - 3.5, kw - 4.0, kh - 2.0))

        # Animated wings actively tapping keys!
        wing_c = QColor(sk.get("wing", "#FFFFFF"))
        painter.setPen(QPen(QColor(sk["outline"]), 1.4))
        painter.setBrush(QBrush(wing_c))
        type_l = math.sin(self.breathing_time * 26.0) * 3.5
        type_r = -math.sin(self.breathing_time * 26.0) * 3.5
        painter.drawEllipse(QRectF(bx + 8.0, by - 4.0 + type_l, 6.0, 4.0))
        painter.drawEllipse(QRectF(bx + 24.0, by - 4.0 + type_r, 6.0, 4.0))

        sh, sw, sx = 24.0, 34.0, 4.0
        screen = QPainterPath()
        screen.moveTo(bx + 2.0, by - 4.0)
        screen.lineTo(bx + 2.0 + sx, by - 4.0 - sh)
        screen.lineTo(bx + 2.0 + sx + sw, by - 4.0 - sh)
        screen.lineTo(bx + 2.0 + sw, by - 4.0)
        screen.closeSubpath()
        painter.setBrush(QBrush(QColor("#21222C")))
        painter.drawPath(screen)

        inner = QRectF(bx + 5.0, by - 1.5 - sh, sw - 4.0, sh - 4.0)
        painter.setBrush(QBrush(QColor("#0D1117")))
        painter.drawRoundedRect(inner, 1.5, 1.5)

        # Scrolling terminal green phosphor code
        scroll_off = (self.breathing_time * 8.0) % 5.0
        painter.setPen(QPen(QColor("#50FA7B"), 1.2))
        for i in range(4):
            ly = inner.top() + 3.0 + i * 4.2 - scroll_off
            if inner.top() + 1.0 <= ly <= inner.bottom() - 1.5:
                lw = 0.55 + 0.40 * math.sin(i * 2.5 + self.breathing_time * 2.0)
                painter.drawLine(QPointF(inner.left() + 2, ly), QPointF(inner.left() + 2 + (inner.width() - 4) * lw, ly))

    def _draw_glasses(self, painter: QPainter, sk: Dict, cx: float, cy: float):
        gp = QPen(QColor(sk.get("glasses_color", "#8BE9FD")), 2.2)
        gp.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
        painter.setPen(gp)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        lw, lh = 17.0, 13.0
        painter.drawRoundedRect(QRectF(cx - lw / 2.0, cy - lh / 2.0, lw, lh), 3.0, 3.0)
        painter.drawLine(QPointF(cx + lw / 2.0, cy - 1.0), QPointF(cx + lw / 2.0 + 7.0, cy - 1.0))
        painter.drawLine(QPointF(cx - lw / 2.0, cy - 1.0), QPointF(cx - lw / 2.0 - 10.0, cy - 3.0))

    def _draw_visor(self, painter: QPainter):
        vp = QPainterPath()
        vp.moveTo(10.0, -106.0); vp.lineTo(36.0, -104.0)
        vp.lineTo(33.0, -96.0); vp.lineTo(8.0, -98.0)
        vp.closeSubpath()
        painter.setPen(QPen(QColor("#00F0FF"), 1.8))
        painter.setBrush(QBrush(QColor(0, 240, 255, 130)))
        painter.drawPath(vp)

    def _draw_wizard_hat(self, painter: QPainter, sk: Dict):
        hc = QColor(sk.get("hat_color", "#3C096C"))
        painter.setPen(QPen(QColor(sk["outline"]), 1.8))
        painter.setBrush(QBrush(hc))
        painter.drawEllipse(QRectF(2.0, -122.0, 32.0, 8.0))
        cone = QPainterPath()
        cone.moveTo(6.0, -120.0)
        cone.quadTo(18.0, -150.0, 28.0, -156.0)
        cone.lineTo(26.0, -120.0)
        cone.closeSubpath()
        painter.drawPath(cone)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor("#FFD700")))
        painter.drawEllipse(QRectF(14.0, -123.0, 5.0, 5.0))

    def _draw_coffee_cup(self, painter: QPainter, sk: Dict):
        """Realistic coffee drinking: periodically lifts right to the BEAK and sips!"""
        sip_cycle = self.breathing_time % 7.0
        is_sipping = (2.6 <= sip_cycle <= 4.5)

        painter.save()
        if is_sipping:
            painter.translate(38.0, -94.0)
            painter.rotate(-32.0)
        else:
            painter.translate(34.0, -22.0)

        cp = QPainterPath()
        cp.moveTo(0.0, 0.0); cp.lineTo(12.0, 0.0)
        cp.lineTo(10.0, 14.0); cp.lineTo(2.0, 14.0)
        cp.closeSubpath()

        painter.setPen(QPen(QColor(sk["outline"]), 1.2))
        painter.setBrush(QBrush(QColor("#FDF0D5")))
        painter.drawPath(cp)

        painter.setBrush(QBrush(QColor("#92400E")))
        painter.drawRect(QRectF(1.0, 4.0, 10.0, 6.0))

        painter.setBrush(QBrush(QColor("#FFFFFF")))
        painter.drawRoundedRect(QRectF(-1.0, -3.0, 14.0, 3.5), 1.0, 1.0)

        if is_sipping:
            steam_y = math.sin(self.breathing_time * 10.0) * 3.0
            painter.setPen(QPen(QColor(255, 255, 255, 160), 1.2))
            painter.drawLine(QPointF(6.0, -4.0), QPointF(5.0, -10.0 + steam_y))
            painter.drawLine(QPointF(9.0, -4.0), QPointF(11.0, -11.0 - steam_y))
        painter.restore()

    def _draw_dj_mode(self, painter: QPainter, sk: Dict):
        """Full DJ mode with chunky glowing neon headphones, turntable deck, and spinning vinyl!"""
        # 1. Glowing RGB DJ Headphones on goose head
        hcx, hcy = 16.0, -97.0
        painter.save()
        hp_pen = QPen(QColor("#111827"), 4.0)
        hp_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(hp_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        arc = QPainterPath()
        arc.moveTo(hcx - 17.0, hcy - 8.0)
        arc.quadTo(hcx, hcy - 28.0, hcx + 17.0, hcy - 8.0)
        painter.drawPath(arc)

        painter.setPen(QPen(QColor("#00F0FF"), 1.8))
        painter.drawPath(arc)

        for s in [-1, 1]:
            ex = hcx + s * 18.0
            ey = hcy - 6.0
            painter.setPen(QPen(QColor("#1F2937"), 1.5))
            painter.setBrush(QBrush(QColor("#111827")))
            painter.drawRoundedRect(QRectF(ex - 4.0, ey - 9.0, 8.0, 18.0), 3.0, 3.0)
            ring_col = QColor("#00F0FF" if s < 0 else "#F43F5E")
            painter.setPen(QPen(ring_col, 2.0))
            painter.drawRoundedRect(QRectF(ex - 2.5, ey - 7.0, 5.0, 14.0), 2.0, 2.0)
        painter.restore()

        # 2. Slanted DJ Turntable Mixing Deck
        dx, dy = 6.0, -38.0
        dw, dh = 72.0, 24.0
        painter.save()
        painter.setPen(QPen(QColor("#090A0F"), 1.8))
        painter.setBrush(QBrush(QColor("#1E2028")))
        painter.drawRoundedRect(QRectF(dx, dy, dw, dh), 4.0, 4.0)

        painter.setBrush(QBrush(QColor("#12141A")))
        painter.drawRoundedRect(QRectF(dx + 2.0, dy + 2.0, dw - 4.0, dh - 4.0), 3.0, 3.0)

        spin1 = (self.breathing_time * 360.0) % 360.0
        spin2 = (-self.breathing_time * 420.0) % 360.0

        for vx, spin, col in [(dx + 16.0, spin1, "#00F0FF"), (dx + 56.0, spin2, "#F43F5E")]:
            vy = dy + 12.0
            painter.setPen(QPen(QColor("#050508"), 1.0))
            painter.setBrush(QBrush(QColor("#0B0C10")))
            painter.drawEllipse(QRectF(vx - 11.0, vy - 9.0, 22.0, 18.0))

            painter.setPen(QPen(QColor(60, 65, 80, 140), 0.8))
            painter.drawEllipse(QRectF(vx - 7.5, vy - 6.0, 15.0, 12.0))

            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(QColor(col)))
            painter.drawEllipse(QRectF(vx - 3.5, vy - 3.0, 7.0, 6.0))

            painter.setBrush(QBrush(QColor("#FFFFFF")))
            painter.drawEllipse(QRectF(vx - 1.0, vy - 1.0, 2.0, 2.0))

            painter.setPen(QPen(QColor("#E2E8F0"), 1.2))
            painter.drawLine(QPointF(vx + 9.0, vy - 8.0), QPointF(vx + 3.0, vy - 2.0))

        cx = dx + 36.0
        painter.setPen(QPen(QColor("#374151"), 1.0))
        painter.drawLine(QPointF(cx - 5.0, dy + 18.0), QPointF(cx + 5.0, dy + 18.0))
        fader_x = cx + math.sin(self.breathing_time * 8.0) * 3.5
        painter.setBrush(QBrush(QColor("#FFD23F")))
        painter.drawRect(QRectF(fader_x - 1.5, dy + 16.5, 3.0, 3.0))

        # 3. Equalizer LED Bars Jumping to the beat
        for b in range(5):
            bx = cx - 4.5 + b * 2.2
            b_height = abs(math.sin(self.breathing_time * 18.0 + b * 1.5)) * 9.0 + 2.0
            b_col = "#10B981" if b_height < 5.0 else ("#FBBF24" if b_height < 8.0 else "#EF4444")
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(QColor(b_col)))
            painter.drawRect(QRectF(bx, dy - 2.0 - b_height, 1.8, b_height))

        painter.restore()

    def _draw_goslings_parade(self, painter: QPainter):
        """Autonomous chaotic baby goslings scurrying and tumbling across the taskbar!"""
        for g in self.goslings:
            gx = g.x
            gy = -4.0 + math.sin(g.walk_phase) * 2.5
            painter.save()
            painter.translate(gx, gy)
            if g.is_flipping:
                painter.rotate(g.flip_angle)
            elif g.vx < 0:
                painter.scale(-1.0, 1.0)

            # Plump yellow chick body
            painter.setPen(QPen(QColor("#78350F"), 1.0))
            painter.setBrush(QBrush(QColor("#FDE047")))
            painter.drawEllipse(QRectF(-7.0, -10.0, 14.0, 10.0))

            # Head
            painter.drawEllipse(QRectF(3.0, -15.0, 8.0, 8.0))

            # Beady black eye
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(QColor("#111827")))
            painter.drawEllipse(QRectF(7.0, -13.0, 2.0, 2.0))

            # Orange beak
            painter.setBrush(QBrush(QColor("#F97316")))
            painter.drawRect(QRectF(9.5, -12.0, 4.0, 2.5))

            # Tiny running feet
            painter.setPen(QPen(QColor("#EA580C"), 1.2))
            painter.drawLine(QPointF(-2.0, 0.0), QPointF(-2.0 + math.sin(g.walk_phase) * 4.0, 4.0))
            painter.drawLine(QPointF(2.0, 0.0), QPointF(2.0 - math.sin(g.walk_phase) * 4.0, 4.0))

            # Little flappy wing
            painter.setBrush(QBrush(QColor("#FEF08A")))
            painter.drawEllipse(QRectF(-4.0, -9.0 + math.sin(g.walk_phase * 2.0) * 1.5, 6.0, 4.0))
            painter.restore()

    def _draw_honk_bomb(self, painter: QPainter):
        """Ticking comical bomb with glowing spark fuse on taskbar."""
        bx = 55.0
        by = -12.0
        # Bomb ball
        painter.setPen(QPen(QColor("#000000"), 1.5))
        painter.setBrush(QBrush(QColor("#1F2937")))
        painter.drawEllipse(QRectF(bx - 10.0, by - 10.0, 20.0, 20.0))
        # Fuse
        painter.setPen(QPen(QColor("#D97706"), 1.5))
        painter.drawLine(QPointF(bx, by - 10.0), QPointF(bx + 6.0, by - 18.0))
        # Spark
        spark_r = abs(math.sin(self.breathing_time * 15.0)) * 4.0 + 2.0
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor("#EF4444")))
        painter.drawEllipse(QRectF(bx + 6.0 - spark_r, by - 18.0 - spark_r, spark_r * 2, spark_r * 2))

    # ------------------------------------------------------------------
    # PARTICLES
    # ------------------------------------------------------------------
    def _draw_particles(self, painter: QPainter, base_rect: QRectF):
        if self.active_crumbs:
            painter.save()
            painter.setPen(QPen(QColor("#8A5A2B"), 1.2))
            painter.setBrush(QBrush(QColor("#DDA15E")))
            for c in self.active_crumbs:
                painter.drawEllipse(QRectF(c.x - 3.0, c.y - 3.0, 6.0, 6.0))
            painter.restore()

        if self.smoke_particles:
            painter.save()
            cx = base_rect.x() + base_rect.width() / 2.0
            cy = base_rect.y() + base_rect.height() - 4.0
            painter.setPen(Qt.PenStyle.NoPen)
            for s in self.smoke_particles:
                smoke_color = QColor(220, 225, 235, s.alpha)
                painter.setBrush(QBrush(smoke_color))
                painter.drawEllipse(QRectF(cx + s.x - s.radius, cy + s.y - s.radius, s.radius * 2, s.radius * 2))
            painter.restore()

        if self.expression == "sleeping" and self.zzz_particles:
            painter.save()
            for p in self.zzz_particles:
                painter.setPen(QPen(QColor(140, 180, 255, p.alpha), 1.8))
                painter.setFont(QFont("Segoe UI", p.size, QFont.Weight.Bold))
                rx = base_rect.x() + base_rect.width() / 2.0 + p.x - 30.0
                ry = base_rect.y() + base_rect.height() - 30.0 + p.y - 60.0
                painter.drawText(QPointF(rx, ry), "Z")
            painter.restore()
