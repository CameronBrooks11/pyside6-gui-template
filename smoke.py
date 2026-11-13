"""Build the windows without a display and drive what needs no user.

Run through `just check`, which sets QT_QPA_PLATFORM=offscreen and turns Python
warnings into errors so a deprecated Qt call fails here. Qt's own warnings, an
exception in a slot, a page that does not switch, a drag that does not move the
window and an icon path with no file behind it fail it too.
"""

import re
import sys
from pathlib import Path

from PySide6.QtCore import (
    QEvent,
    QPoint,
    QPointF,
    Qt,
    QTimer,
    QtMsgType,
    qInstallMessageHandler,
)
from PySide6.QtGui import QMouseEvent
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication, QDialog, QSizeGrip

import main

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


HIGHLIGHT = "rgb(91,90,90)"


def check_highlight(ui):
    ui.bn_home.click()
    ui.bn_home.click()
    expect(
        HIGHLIGHT in ui.frame_home.styleSheet(),
        "clicking the current menu button removed its highlight",
    )

    ui.toodle.click()
    ui.bn_bug.click()  # while the menu is still animating open
    expect(
        ui.stackedWidget.currentWidget() is ui.page_about_bug,
        "a menu button clicked during the toggle animation did nothing",
    )
    expect(
        HIGHLIGHT in ui.frame_bug.styleSheet(),
        "a menu button clicked during the toggle animation lost its highlight",
    )
    QTest.qWait(400)
    ui.toodle.click()
    QTest.qWait(400)
    expect(ui.frame_bottom_west.width() == 80, "the menu did not narrow again")


def check_window_state(window):
    ui = window.ui
    size = window.size()
    ui.bn_max.click()
    expect(window.isMaximized(), "the maximise button did not maximise")
    expect(not ui.frame_drag.isVisible(), "the resize grip shows while maximised")
    ui.bn_max.click()
    QApplication.processEvents()
    expect(not window.isMaximized(), "the maximise button did not restore")
    expect(
        window.size() == size,
        f"restore gave {window.size().toTuple()}, not the {size.toTuple()} it had",
    )

    QTest.mouseDClick(ui.frame_appname, Qt.MouseButton.LeftButton)
    QTest.qWait(300)  # the double click maximises after 250 ms
    expect(window.isMaximized(), "double-clicking the title bar did not maximise")
    ui.bn_max.click()
    QApplication.processEvents()

    ui.bn_min.click()
    expect(window.isMinimized(), "the minimise button did not minimise")
    window.showNormal()
    QApplication.processEvents()

    window.showMaximized()  # as the window manager would, behind the button's back
    ui.bn_max.click()
    QApplication.processEvents()
    expect(not window.isMaximized(), "the button maximised an already maximised window")

    grip = ui.frame_drag.findChild(QSizeGrip)
    expect(grip is not None, "there is no resize grip on the frameless window")
    if grip is not None:
        size = window.size()
        QTest.mousePress(grip, Qt.MouseButton.LeftButton, pos=QPoint(5, 5))
        QTest.mouseMove(grip, QPoint(5, 45))
        QTest.mouseRelease(grip, Qt.MouseButton.LeftButton, pos=QPoint(5, 45))
        expect(window.size() != size, "dragging the resize grip did not resize")

    second = main.MainWindow()
    expect(
        second.ui.lab_tab.text() == "Home" and HIGHLIGHT in second.ui.frame_home.styleSheet(),
        "a second main window did not start on the Home page",
    )
    second.deleteLater()


def check_page_widgets(ui):
    ui.bn_bug.click()
    ui.comboBox_bug.setCurrentIndex(
        min(
            range(ui.comboBox_bug.count()),
            key=lambda i: int(ui.comboBox_bug.itemText(i)),
        )
    )
    ui.bn_bug_start.click()
    expect(
        ui.progressBar_bug.value() < 100,
        "Start ran to 100% inside the click, blocking the GUI while it did",
    )
    for _ in range(200):  # up to 2 s
        if ui.progressBar_bug.value() == 100:
            break
        QTest.qWait(10)
    expect(ui.progressBar_bug.value() == 100, "Start did not fill the progress bar")
    expect(ui.bn_bug_start.isEnabled(), "Start stayed disabled after the run")

    shown = len(dialogs_shown)
    ui.bn_cloud_connect.click()
    expect(len(dialogs_shown) == shown + 1, "Connect did not raise the error box")
    ui.line_cloud_id.setText("x")
    ui.bn_cloud_clear.click()
    expect(ui.line_cloud_id.text() == "", "Clear did nothing after a failed Connect")

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
    ui.checkBox.setChecked(False)
    expect(len(dialogs_shown) == shown + 1, "unchecking the box raised the error box again")


def check_dialog_result(window):
    for button, expected in (("bn_east", True), ("bn_west", False), ("bn_close", False)):
        QTimer.singleShot(0, getattr(window.diag.d, button).click)
        QDialog.exec = real_exec
        try:
            result = window.dialogexec("Heading", "Message", "", "No", "Yes")
        finally:
            QDialog.exec = fake_exec
        expect(result is expected, f"dialogexec returned {result!r} after {button}")

    ui = window.ui
    ui.line_android_name.setText("someone")
    answers.append(False)
    ui.bn_android_contact_delete.click()
    expect(ui.line_android_name.text() == "someone", "Cancel deleted the contact anyway")
    answers.append(True)
    ui.bn_android_contact_delete.click()
    expect(ui.line_android_name.text() == "", "Yes did not delete the contact")


def drive(window):
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

    check_highlight(ui)
    check_page_widgets(ui)
    check_dialog_result(window)
    check_window_state(window)

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
def fake_exec(dialog):
    dialogs_shown.append(dialog)
    accepted = answers.pop() if answers else False
    return QDialog.DialogCode.Accepted if accepted else QDialog.DialogCode.Rejected


answers = []
real_exec = QDialog.exec
QDialog.exec = fake_exec

app = QApplication(sys.argv)
window = main.MainWindow()
window.show()
sys.exit(drive(window))
