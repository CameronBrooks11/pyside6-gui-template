"""Run main.py as a script, without a display, and drive what needs no user.

main.py and ui_function.py import each other, which only resolves when main.py
is the entry script, so this runs it that way and takes over at app.exec().

Run through `just check`, which sets QT_QPA_PLATFORM=offscreen and turns Python
warnings into errors so a deprecated Qt call fails here. Qt's own warnings, an
exception in a slot, a page that does not switch, a drag that does not move the
window and an icon path with no file behind it fail it too.
"""

import re
import runpy
import sys
from pathlib import Path

from PySide6.QtCore import QEvent, QPointF, Qt, QtMsgType, qInstallMessageHandler
from PySide6.QtGui import QMouseEvent
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication, QDialog

ICON_SOURCES = ("ui_main.py", "ui_dialog.py", "ui_error.py", "ui_function.py")

problems = []
dialogs_shown = []


def on_qt_message(kind, _context, message):
    print(message, file=sys.stderr)
    if kind != QtMsgType.QtDebugMsg and kind != QtMsgType.QtInfoMsg:
        problems.append(f"Qt message: {message}")


def on_exception(kind, value, traceback):
    sys.__excepthook__(kind, value, traceback)
    problems.append(f"exception in a slot: {kind.__name__}: {value}")


def expect(condition, what):
    if not condition:
        problems.append(what)


def drag(press_target, move_target):
    for kind, target, global_pos in (
        (QEvent.Type.MouseButtonPress, press_target.mousePressEvent, QPointF(105, 105)),
        (QEvent.Type.MouseMove, move_target.mouseMoveEvent, QPointF(140, 140)),
    ):
        target(
            QMouseEvent(
                kind,
                QPointF(5, 5),
                global_pos,
                Qt.MouseButton.LeftButton,
                Qt.MouseButton.LeftButton,
                Qt.KeyboardModifier.NoModifier,
            )
        )


def check_drag(name, window, handle):
    before = window.pos()
    drag(window, handle)
    expect(window.pos() != before, f"dragging the {name} did not move it")


def check_icons():
    for source in ICON_SOURCES:
        for path in set(re.findall(r"icons/[^\"']+\.png", Path(source).read_text())):
            expect(Path(path).is_file(), f"{source} names {path}, which is not a file")


def check_menu(ui, pages, tab_prefix):
    for button, page, tab in pages:
        getattr(ui, button).click()
        expect(
            ui.stackedWidget.currentWidget() is getattr(ui, page),
            f"{button} did not show {page}",
        )
        expect(
            ui.lab_tab.text().startswith(tab_prefix + tab),
            f"{button} left the tab label at {ui.lab_tab.text()!r}",
        )


def check_page_widgets(ui):
    ui.bn_bug.click()
    ui.comboBox_bug.setCurrentIndex(
        min(
            range(ui.comboBox_bug.count()),
            key=lambda i: int(ui.comboBox_bug.itemText(i)),
        )
    )
    ui.progressBar_bug.setValue(0)
    ui.bn_bug_start.click()
    expect(ui.progressBar_bug.value() == 100, "Start did not fill the progress bar")

    ui.line_cloud_id.setText("x")
    ui.bn_cloud_clear.click()
    expect(ui.line_cloud_id.text() == "", "Clear did not empty the client id")
    shown = len(dialogs_shown)
    ui.bn_cloud_connect.click()
    expect(len(dialogs_shown) == shown + 1, "Connect did not raise the error box")

    ui.bn_android.click()
    for button, page in (
        ("bn_android_game", "page_android_game"),
        ("bn_android_clean", "page_android_clean"),
        ("bn_android_world", "page_android_world"),
        ("bn_android_contact", "page_android_contact"),
    ):
        getattr(ui, button).click()
        expect(
            ui.stackedWidget_android.currentWidget() is getattr(ui, page),
            f"{button} did not show {page}",
        )

    ui.bn_android_contact_edit.click()
    expect(ui.line_android_name.isEnabled(), "Edit did not enable the name field")
    ui.bn_android_contact_save.click()
    expect(not ui.line_android_name.isEnabled(), "Save did not disable the name field")

    shown = len(dialogs_shown)
    ui.bn_android_contact_delete.click()
    expect(len(dialogs_shown) == shown + 1, "Delete did not raise the dialog box")

    shown = len(dialogs_shown)
    ui.checkBox.setChecked(True)
    expect(len(dialogs_shown) == shown + 1, "the check box did not raise the error box")


def drive(*_):
    (window,) = [
        w for w in QApplication.topLevelWidgets() if type(w).__name__ == "MainWindow"
    ]
    ui = window.ui

    check_icons()

    pages = (
        ("bn_bug", "page_bug", "Bug"),
        ("bn_android", "page_android", "Android"),
        ("bn_cloud", "page_cloud", "Cloud"),
        ("bn_home", "page_home", "Home"),
    )
    check_menu(ui, pages, "")

    ui.toodle.click()
    QTest.qWait(400)  # the menu animates open over 300 ms
    expect(ui.frame_bottom_west.width() == 160, "the toggle did not widen the menu")
    about = tuple((b, p.replace("page_", "page_about_"), t) for b, p, t in pages)
    check_menu(ui, about, "About > ")
    ui.toodle.click()
    QTest.qWait(400)
    expect(ui.frame_bottom_west.width() == 80, "the toggle did not narrow the menu")

    check_page_widgets(ui)

    ui.bn_max.click()
    expect(window.isMaximized(), "the maximise button did not maximise")
    ui.bn_max.click()
    expect(not window.isMaximized(), "the maximise button did not restore")

    check_drag("main window", window, ui.frame_appname)
    check_drag("dialog box", window.diag, window.diag.d.frame_top)
    check_drag("error box", window.error, window.error.e.frame_top)

    QApplication.processEvents()
    for problem in problems:
        print("FAIL:", problem, file=sys.stderr)
    if not problems:
        print("smoke ok")
    return 1 if problems else 0


qInstallMessageHandler(on_qt_message)
sys.excepthook = on_exception
QDialog.exec = lambda self: dialogs_shown.append(self)
QApplication.exec = drive
runpy.run_path("main.py", run_name="__main__")
