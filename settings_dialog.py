"""Settings Dialog for Da Goose Companion."""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QCheckBox, QComboBox, QDialog, QFormLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QPushButton, QSlider,
    QSpinBox, QTabWidget, QTextEdit, QVBoxLayout, QWidget,
)
from config_manager import ConfigManager
from goose_painter import SKINS

STYLE = """
QDialog { background:#1A1C23; color:#E2E8F0; font-family:'Segoe UI',system-ui,sans-serif; font-size:13px; }
QTabWidget::pane { border:1px solid #2D3748; border-radius:8px; background:#21252F; top:-1px; }
QTabBar::tab { background:#1A1C23; color:#A0AEC0; padding:8px 18px; border:1px solid #2D3748;
               border-bottom:none; border-top-left-radius:6px; border-top-right-radius:6px; margin-right:4px; }
QTabBar::tab:selected { background:#21252F; color:#FFD23F; font-weight:bold; border-bottom:2px solid #FFD23F; }
QGroupBox { border:1px solid #323B4E; border-radius:8px; margin-top:14px; padding:14px; font-weight:600; color:#E2E8F0; }
QGroupBox::title { subcontrol-origin:margin; left:12px; padding:0 6px; color:#FFD23F; }
QLabel { color:#CBD5E0; }
QLineEdit, QSpinBox, QComboBox, QTextEdit {
    background:#16181F; border:1px solid #374151; border-radius:6px;
    padding:6px 10px; color:#F9FAFB; selection-background-color:#FFD23F; selection-color:#111827; }
QLineEdit:focus, QSpinBox:focus, QComboBox:focus, QTextEdit:focus { border:1px solid #FFD23F; }
QPushButton { background:#2D3748; border:1px solid #4A5568; border-radius:6px;
              color:#F7FAFC; padding:7px 16px; font-weight:600; }
QPushButton:hover { background:#3C4758; border-color:#718096; }
QPushButton#primaryBtn { background:#FFD23F; color:#1A202C; border:none; }
QPushButton#primaryBtn:hover { background:#FFE066; }
QCheckBox { color:#E2E8F0; spacing:8px; }
QCheckBox::indicator { width:18px; height:18px; border-radius:4px; border:1px solid #4A5568; background:#16181F; }
QCheckBox::indicator:checked { background:#FFD23F; border-color:#FFD23F; }
"""


class SettingsDialog(QDialog):
    settings_applied = pyqtSignal()

    def __init__(self, config_manager: ConfigManager, parent=None):
        super().__init__(parent)
        self.cfg = config_manager
        self.setWindowTitle("Da Goose Companion — Settings")
        self.setFixedSize(530, 580)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        self.setStyleSheet(STYLE)
        self._build_ui()
        self._load()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(14)

        title = QLabel("🪿 Da Goose Companion Preferences")
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title.setStyleSheet("color:#FFD23F; margin-bottom:2px;")
        root.addWidget(title)

        tabs = QTabWidget()

        # ---- AI TAB ----
        ai_w = QWidget()
        ai_l = QVBoxLayout(ai_w)
        ai_l.setContentsMargins(14, 14, 14, 14)

        ai_box = QGroupBox("Google Gemini API")
        ai_form = QFormLayout(ai_box)
        ai_form.setSpacing(10)

        key_row = QHBoxLayout()
        self.api_key = QLineEdit()
        self.api_key.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key.setPlaceholderText("Paste your Gemini API key (aistudio.google.com)…")
        key_row.addWidget(self.api_key)
        self.eye_btn = QPushButton("👁️")
        self.eye_btn.setFixedWidth(38)
        self.eye_btn.clicked.connect(self._toggle_key)
        key_row.addWidget(self.eye_btn)
        ai_form.addRow("API Key:", key_row)

        self.model_combo = QComboBox()
        self.model_combo.addItems([
            "gemini-3.8-flash",
            "gemini-3.5-flash-lite",
            "gemini-2.5-flash",
            "gemini-1.5-flash",
            "gemini-1.5-pro",
        ])
        ai_form.addRow("AI Model:", self.model_combo)

        self.personality_combo = QComboBox()
        self.personality_combo.addItem("Witty & Cheeky (Default)", "witty")
        self.personality_combo.addItem("Unapologetically Sarcastic", "sarcastic")
        self.personality_combo.addItem("Cute & Wholesome", "wholesome")
        self.personality_combo.addItem("Pedantic Nerd", "nerd")
        ai_form.addRow("Personality:", self.personality_combo)

        self.peek_combo = QComboBox()
        self.peek_combo.addItem("Disabled (Manual Only)", 0)
        self.peek_combo.addItem("Every 5 min", 5)
        self.peek_combo.addItem("Every 10 min", 10)
        self.peek_combo.addItem("Every 20 min", 20)
        self.peek_combo.addItem("Every 30 min", 30)
        ai_form.addRow("Auto Peek:", self.peek_combo)

        ai_l.addWidget(ai_box)
        hint = QLabel("💡 Get a free API key at aistudio.google.com")
        hint.setStyleSheet("color:#718096; font-size:11px;")
        ai_l.addWidget(hint)
        ai_l.addStretch()
        tabs.addTab(ai_w, "🤖 AI Screen Peeker")

        # ---- DOOMSCROLL TAB ----
        ds_w = QWidget()
        ds_l = QVBoxLayout(ds_w)
        ds_l.setContentsMargins(14, 14, 14, 14)

        ds_box = QGroupBox("Distraction Guard")
        ds_form = QFormLayout(ds_box)
        ds_form.setSpacing(10)
        self.doom_cb = QCheckBox("Enable Anti-Doomscroll Monitor")
        ds_form.addRow(self.doom_cb)
        self.doom_spin = QSpinBox()
        self.doom_spin.setRange(1, 120)
        self.doom_spin.setSuffix(" minutes")
        ds_form.addRow("Scold After:", self.doom_spin)
        ds_l.addWidget(ds_box)

        kw_box = QGroupBox("Monitored Window Keywords")
        kw_l = QVBoxLayout(kw_box)
        self.kw_text = QTextEdit()
        self.kw_text.setPlaceholderText("youtube, reddit, twitter, tiktok…")
        self.kw_text.setMaximumHeight(85)
        kw_l.addWidget(self.kw_text)
        kw_l.addWidget(QLabel("Comma-separated."))
        ds_l.addWidget(kw_box)
        ds_l.addStretch()
        tabs.addTab(ds_w, "🛡️ Doomscroll Guard")

        # ---- APPEARANCE TAB ----
        ap_w = QWidget()
        ap_l = QVBoxLayout(ap_w)
        ap_l.setContentsMargins(14, 14, 14, 14)

        look_box = QGroupBox("Goose Visuals")
        look_form = QFormLayout(look_box)
        look_form.setSpacing(10)

        self.skin_combo = QComboBox()
        for key, val in SKINS.items():
            self.skin_combo.addItem(val["name"], key)
        look_form.addRow("Goose Skin:", self.skin_combo)

        self.chair_cb = QCheckBox("Show Rotating Swivel Chair")
        look_form.addRow(self.chair_cb)

        sl_row = QHBoxLayout()
        self.scale_sl = QSlider(Qt.Orientation.Horizontal)
        self.scale_sl.setRange(8, 14)
        self.scale_sl.setValue(10)
        self.scale_lbl = QLabel("100%")
        self.scale_sl.valueChanged.connect(lambda v: self.scale_lbl.setText(f"{v * 10}%"))
        sl_row.addWidget(self.scale_sl)
        sl_row.addWidget(self.scale_lbl)
        look_form.addRow("Size:", sl_row)

        self.sound_cb = QCheckBox("Enable Sound Effects")
        look_form.addRow(self.sound_cb)
        self.top_cb = QCheckBox("Always on Top")
        look_form.addRow(self.top_cb)

        ap_l.addWidget(look_box)
        ap_l.addStretch()
        tabs.addTab(ap_w, "🎨 Appearance")

        root.addWidget(tabs)

        # Buttons
        btns = QHBoxLayout()
        btns.addStretch()
        cancel = QPushButton("Cancel")
        cancel.clicked.connect(self.reject)
        btns.addWidget(cancel)
        save = QPushButton("Save & Apply")
        save.setObjectName("primaryBtn")
        save.clicked.connect(self._save)
        btns.addWidget(save)
        root.addLayout(btns)

    def _toggle_key(self):
        if self.api_key.echoMode() == QLineEdit.EchoMode.Password:
            self.api_key.setEchoMode(QLineEdit.EchoMode.Normal)
            self.eye_btn.setText("🔒")
        else:
            self.api_key.setEchoMode(QLineEdit.EchoMode.Password)
            self.eye_btn.setText("👁️")

    def _load(self):
        c = self.cfg
        self.api_key.setText(c.get("gemini_api_key", ""))
        m = c.get("gemini_model", "gemini-3.8-flash")
        idx = self.model_combo.findText(m)
        self.model_combo.setCurrentIndex(idx if idx >= 0 else 0)

        p = c.get("ai_personality", "witty")
        self.personality_combo.setCurrentIndex(max(0, self.personality_combo.findData(p)))

        pk = c.get("ai_auto_peek_interval", 0)
        self.peek_combo.setCurrentIndex(max(0, self.peek_combo.findData(pk)))

        self.doom_cb.setChecked(c.get("doomscroll_enabled", True))
        self.doom_spin.setValue(c.get("doomscroll_threshold_minutes", 10))
        self.kw_text.setPlainText(", ".join(c.get("doomscroll_keywords", [])))

        skin = c.get("goose_skin", "classic")
        si = self.skin_combo.findData(skin)
        self.skin_combo.setCurrentIndex(si if si >= 0 else 0)

        self.chair_cb.setChecked(c.get("chair_enabled", True))
        scale = int(c.get("duck_scale", 1.0) * 10)
        self.scale_sl.setValue(scale)
        self.scale_lbl.setText(f"{scale * 10}%")
        self.sound_cb.setChecked(c.get("sound_enabled", True))
        self.top_cb.setChecked(c.get("always_on_top", True))

    def _save(self):
        raw = self.kw_text.toPlainText().replace("\n", ",")
        kw = [k.strip() for k in raw.split(",") if k.strip()]
        self.cfg.update({
            "gemini_api_key": self.api_key.text().strip(),
            "gemini_model": self.model_combo.currentText().strip(),
            "ai_personality": self.personality_combo.currentData(),
            "ai_auto_peek_interval": self.peek_combo.currentData(),
            "doomscroll_enabled": self.doom_cb.isChecked(),
            "doomscroll_threshold_minutes": self.doom_spin.value(),
            "doomscroll_keywords": kw,
            "goose_skin": self.skin_combo.currentData(),
            "chair_enabled": self.chair_cb.isChecked(),
            "duck_scale": round(self.scale_sl.value() / 10.0, 1),
            "sound_enabled": self.sound_cb.isChecked(),
            "always_on_top": self.top_cb.isChecked(),
        })
        self.accept()
        self.settings_applied.emit()
