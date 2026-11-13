from PySide6.QtGui import QPalette
from PySide6.QtWidgets import QApplication

from app import theme
from app.pages.settings import SettingsPage


def window_lightness() -> int:
    return QApplication.palette().color(QPalette.ColorRole.Window).lightness()


def text_lightness() -> int:
    return QApplication.palette().color(QPalette.ColorRole.WindowText).lightness()


def test_dark_is_light_text_on_a_dark_window():
    theme.apply_theme(theme.DARK)
    assert window_lightness() < 80 and text_lightness() > 200


def test_light_is_dark_text_on_a_light_window():
    theme.apply_theme(theme.DARK)
    theme.apply_theme(theme.LIGHT)
    assert window_lightness() > 200 and text_lightness() < 80


def test_system_restores_the_palette_of_the_style():
    theme.apply_theme(theme.DARK)
    theme.apply_theme(theme.SYSTEM)
    assert QApplication.palette() == QApplication.style().standardPalette()


def test_the_saved_theme_defaults_to_system_and_ignores_an_unknown_name():
    assert theme.saved_theme() == theme.SYSTEM
    theme.save_theme("Sepia")
    assert theme.saved_theme() == theme.SYSTEM


def test_choosing_a_theme_applies_and_remembers_it(qtbot):
    page = SettingsPage()
    qtbot.addWidget(page)
    assert page.ui.theme_combo.currentText() == theme.SYSTEM

    page.ui.theme_combo.setCurrentText(theme.DARK)
    assert window_lightness() < 80
    assert theme.saved_theme() == theme.DARK

    reopened = SettingsPage()
    qtbot.addWidget(reopened)
    assert reopened.ui.theme_combo.currentText() == theme.DARK
