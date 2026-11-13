"""Entry point: `python -m app`, and the `app` command."""

import sys

from PySide6.QtWidgets import QApplication

from .frameless import keep_on_screen
from .main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    keep_on_screen(window)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
