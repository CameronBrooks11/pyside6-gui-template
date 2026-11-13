"""The light and dark themes, and remembering which one was chosen."""

from PySide6.QtCore import QSettings
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QApplication, QPushButton

SYSTEM = "System"
LIGHT = "Light"
DARK = "Dark"
THEMES = (SYSTEM, LIGHT, DARK)

_ACCENT = QColor(0, 143, 150)


def _palette(
    window: QColor, base: QColor, alternate: QColor, button: QColor, text: QColor, disabled: QColor
) -> QPalette:
    # This constructor derives the shades used for frames and bevels.
    palette = QPalette(button, window)
    role = QPalette.ColorRole
    colours = {
        role.WindowText: text,
        role.Text: text,
        role.ButtonText: text,
        role.ToolTipText: text,
        role.Base: base,
        role.ToolTipBase: base,
        role.AlternateBase: alternate,
        role.PlaceholderText: disabled,
        role.Highlight: _ACCENT,
        role.HighlightedText: QColor("white"),
        role.Link: _ACCENT,
    }
    for colour_role, colour in colours.items():
        palette.setColor(colour_role, colour)
    for colour_role in (role.WindowText, role.Text, role.ButtonText):
        palette.setColor(QPalette.ColorGroup.Disabled, colour_role, disabled)
    return palette


def light_palette() -> QPalette:
    return _palette(
        window=QColor(246, 247, 248),
        base=QColor(255, 255, 255),
        alternate=QColor(238, 240, 242),
        button=QColor(240, 241, 243),
        text=QColor(28, 30, 33),
        disabled=QColor(150, 154, 160),
    )


def dark_palette() -> QPalette:
    return _palette(
        window=QColor(43, 45, 48),
        base=QColor(30, 31, 34),
        alternate=QColor(52, 55, 59),
        button=QColor(58, 61, 66),
        text=QColor(230, 232, 235),
        disabled=QColor(120, 124, 130),
    )


def make_primary(button: QPushButton) -> None:
    """Paint the button for a page's main action in the accent colour."""
    palette = button.palette()
    for group in (QPalette.ColorGroup.Active, QPalette.ColorGroup.Inactive):
        palette.setColor(group, QPalette.ColorRole.Button, _ACCENT)
        palette.setColor(group, QPalette.ColorRole.ButtonText, QColor("white"))
    button.setPalette(palette)


def apply_theme(name: str) -> None:
    """Repaint the whole application in the named theme."""
    if name == DARK:
        QApplication.setPalette(dark_palette())
    elif name == LIGHT:
        QApplication.setPalette(light_palette())
    else:
        QApplication.setPalette(QApplication.style().standardPalette())


def saved_theme() -> str:
    name = QSettings().value("theme", SYSTEM)
    return name if name in THEMES else SYSTEM


def save_theme(name: str) -> None:
    QSettings().setValue("theme", name)
