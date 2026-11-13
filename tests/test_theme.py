from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QApplication, QPushButton

from app import theme
from app.pages.form import FormPage
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


def test_the_sidebar_follows_a_change_of_theme(window, qtbot):
    def sidebar_lightness() -> int:
        navigation = window.ui.navigation
        return navigation.grab().toImage().pixelColor(navigation.width() - 5, 3).lightness()

    theme.apply_theme(theme.LIGHT)
    qtbot.waitUntil(lambda: sidebar_lightness() > 200)
    theme.apply_theme(theme.DARK)
    qtbot.waitUntil(lambda: sidebar_lightness() < 80)


def test_a_primary_button_is_the_accent_colour_in_both_themes(qtbot):
    button = QPushButton("Save")
    qtbot.addWidget(button)
    theme.make_primary(button)
    for name in (theme.LIGHT, theme.DARK):
        theme.apply_theme(name)
        assert button.palette().color(QPalette.ColorRole.Button) == QColor(0, 128, 134).darker(125)
        assert button.palette().color(QPalette.ColorRole.ButtonText) == QColor("white")


def test_the_form_error_is_a_lighter_red_on_the_dark_theme(qtbot):
    page = FormPage()
    qtbot.addWidget(page)

    def error_lightness() -> int:
        return page.ui.error_label.palette().color(QPalette.ColorRole.WindowText).lightness()

    theme.apply_theme(theme.LIGHT)
    qtbot.waitUntil(lambda: error_lightness() < 140)
    theme.apply_theme(theme.DARK)
    qtbot.waitUntil(lambda: error_lightness() > 160)
