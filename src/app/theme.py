"""The fonts and the stylesheet the three windows share."""

from PySide6.QtCore import QFile, QIODevice, QTextStream
from PySide6.QtGui import QFont, QFontDatabase, QFontInfo

from .ui import resources_rc  # noqa: F401  registers the icons and :/style.qss

# The .ui files ask for Segoe UI, which ships with Windows. Where it is
# missing, the first of these that is installed stands in for all three of
# its families, and the system's own font if none is, so a window does not end
# up mixing two typefaces. A substitute has to be the name of an installed
# family: a generic name such as "Sans Serif" is ignored.
FONT_FALLBACKS = ["Noto Sans", "Helvetica Neue", "Arial"]
SEGOE_FAMILIES = ("Segoe UI", "Segoe UI Light", "Segoe UI Semilight")


def set_font_fallbacks():
    """Register the fallbacks. Call it before building a window's widgets:
    a widget keeps the font it resolved when it was built."""
    # QFontInfo gives the family the system font resolves to; the font itself
    # may only say "Sans Serif".
    system = QFontInfo(QFontDatabase.systemFont(QFontDatabase.SystemFont.GeneralFont)).family()
    for family in SEGOE_FAMILIES:
        QFont.insertSubstitutions(family, FONT_FALLBACKS + [system])


def load_style():
    """Return resources/style.qss, which `just uic` compiles into the resources.

    Each window sets it on the frame that holds its content, not on itself and
    not on the application, so that it does not reach Qt's own dialogs: a
    QMessageBox or QFileDialog given one of the three windows as its parent
    keeps its normal look. Given a widget inside a window as its parent, it
    would take the sheet.
    """
    sheet = QFile(":/style.qss")
    if not sheet.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
        raise RuntimeError("style.qss is not in the compiled resources: run `just uic`")
    return QTextStream(sheet).readAll()  # reads UTF-8
