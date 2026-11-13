"""Run main.py as a script, without a display, and drive what needs no user.

main.py and ui_function.py import each other, which only resolves when main.py
is the entry script, so this runs it that way and takes over at app.exec().

Run through `just check`, which sets QT_QPA_PLATFORM=offscreen and turns
warnings into errors so a deprecated Qt call fails here.
"""

import runpy
import sys

from PySide6.QtCore import QEvent, QPointF, Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QApplication


def drag(press_target, move_target):
    for kind, target in (
        (QEvent.Type.MouseButtonPress, press_target.mousePressEvent),
        (QEvent.Type.MouseMove, move_target.mouseMoveEvent),
    ):
        target(
            QMouseEvent(
                kind,
                QPointF(5, 5),
                QPointF(105, 105),
                Qt.MouseButton.LeftButton,
                Qt.MouseButton.LeftButton,
                Qt.KeyboardModifier.NoModifier,
            )
        )


def drive(*_):
    ui = sys.modules["ui_function"].UIFunction
    (window,) = [
        w for w in QApplication.topLevelWidgets() if type(w).__name__ == "MainWindow"
    ]

    for page in ("bn_home", "bn_bug", "bn_android", "bn_cloud"):
        ui.buttonPressed(window, page)
    ui.toodleMenu(window, 160, True)
    ui.maximize_restore(window)
    ui.maximize_restore(window)

    drag(window, window.ui.frame_appname)
    drag(window.diag, window.diag.d.frame_top)
    drag(window.error, window.error.e.frame_top)

    QApplication.processEvents()
    print("smoke ok")
    return 0


QApplication.exec = drive
runpy.run_path("main.py", run_name="__main__")
