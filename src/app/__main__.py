"""Entry point for `python -m app` and the `app` command."""

import sys

from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QApplication

from app import APP_NAME, ORGANISATION
from app.main_window import MainWindow
from app.theme import apply_theme, saved_theme


def main() -> int:
    app = QApplication.instance() or QApplication(sys.argv)
    QCoreApplication.setOrganizationName(ORGANISATION)
    QCoreApplication.setApplicationName(APP_NAME)
    # Fusion draws every widget from the palette, so the themes look the same
    # on Windows, Linux and macOS.
    QApplication.setStyle("Fusion")
    apply_theme(saved_theme())
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
