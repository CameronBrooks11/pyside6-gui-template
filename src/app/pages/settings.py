"""Settings: the theme, applied at once and remembered between runs."""

from PySide6.QtWidgets import QWidget

from app.theme import THEMES, apply_theme, save_theme, saved_theme
from app.ui.ui_settings_page import Ui_SettingsPage


class SettingsPage(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_SettingsPage()
        self.ui.setupUi(self)
        self.ui.theme_combo.addItems(THEMES)
        self.ui.theme_combo.setCurrentText(saved_theme())
        self.ui.theme_combo.currentTextChanged.connect(self._set_theme)

    def _set_theme(self, name: str) -> None:
        apply_theme(name)
        save_theme(name)
