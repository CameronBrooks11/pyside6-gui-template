"""Run main.py as a script, without a display, and drive what needs no user.

main.py runs as the entry script, as `just run` runs it, and this takes over at
app.exec().

Run through `just check`, which sets QT_QPA_PLATFORM=offscreen and turns Python
warnings into errors so a deprecated Qt call fails here. Qt's own warnings, an
exception in a slot, a page that does not switch, a drag that does not move the
window and an icon path with no file behind it fail it too.
"""

import re
import runpy
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
from PySide6.QtGui import QFontDatabase, QFontInfo, QIcon, QMouseEvent
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication, QDialog, QSizeGrip, QWidget

import ui_function

# Every file that can name an image: the Designer sources, what is generated
# from them, and the Python that sets one at run time.
ICON_SOURCES = (
    "main.py",
    "ui_main.ui",
    "ui_dialog.ui",
    "ui_error.ui",
    "ui_main.py",
    "ui_dialog.py",
    "ui_error.py",
    "ui_function.py",
)

# An image path as the sources write one: a quoted string, a stylesheet url()
# or the text of an element in a .ui file. Prose in a comment is not matched.
IMAGE_PATH = re.compile(
    r"""["']([^"'\n]+\.png)["']|url\(([^()"'\n]+\.png)\)|>([^<>\n]+\.png)<""",
    re.IGNORECASE,
)

problems = []
dialogs_shown = []

# ui_function has to import without main: when it needed main, the two modules
# imported each other and only one import order worked.
if "main" in sys.modules:
    problems.append("importing ui_function imported main")
drove = []


def fail(what):
    if what not in problems:
        problems.append(what)


def on_qt_message(kind, _context, message):
    print(message, file=sys.stderr)
    # Qt says this about the host, under LC_ALL=C for one, not about the app.
    if message.startswith("Detected locale"):
        return
    if kind != QtMsgType.QtDebugMsg and kind != QtMsgType.QtInfoMsg:
        fail(f"Qt message: {message}")


def on_exception(kind, value, traceback):
    sys.__excepthook__(kind, value, traceback)
    fail(f"uncaught exception: {kind.__name__}: {value}")


def expect(condition, what):
    if not condition:
        fail(what)


def wait_until(condition, timeout_ms=2000):
    for _ in range(timeout_ms // 10):
        if condition():
            return True
        QTest.qWait(10)
    return condition()


def really_exec(dialog, show, button):
    """Run `show` with the real QDialog.exec and click `button` to end it.

    A button that does not close the dialog would leave exec() blocking for
    good, so a timer closes it and records the failure instead.
    """

    def give_up():
        if dialog.isVisible():
            fail(f"{button.objectName()} did not close its dialog")
            dialog.done(QDialog.DialogCode.Rejected)

    guard = QTimer()
    guard.setSingleShot(True)
    guard.timeout.connect(give_up)
    guard.start(2000)
    QTimer.singleShot(0, button.click)
    QDialog.exec = real_exec
    try:
        return show()
    finally:
        guard.stop()
        QDialog.exec = fake_exec


def drag(press_target, move_target, held=Qt.MouseButton.LeftButton):
    for kind, target, global_pos in (
        (QEvent.Type.MouseButtonPress, press_target.mousePressEvent, QPointF(105, 105)),
        (QEvent.Type.MouseMove, move_target.mouseMoveEvent, QPointF(140, 140)),
    ):
        target(
            QMouseEvent(
                kind,
                QPointF(5, 5),
                global_pos,
                held,
                held,
                Qt.KeyboardModifier.NoModifier,
            )
        )


def check_drag(name, window, handle):
    before = window.pos()
    drag(window, handle)  # pressed at (105, 105) and moved to (140, 140)
    moved = window.pos() - before
    expect(
        moved == QPoint(35, 35),
        f"dragging the {name} by (35, 35) moved it by {moved.toTuple()}",
    )
    before = window.pos()
    drag(window, handle, held=Qt.MouseButton.NoButton)
    expect(window.pos() == before, f"the {name} moved with no mouse button held")


def check_fonts(window):
    """Where Segoe UI is missing, its three families must fall back to one typeface."""
    if "Segoe UI" in QFontDatabase.families():
        return
    resolved = {
        QFontInfo(w.font()).family()
        for top in (window, window.diag, window.error)
        for w in top.findChildren(QWidget)
        if w.font().family().startswith("Segoe UI")
    }
    expect(len(resolved) == 1, f"the Segoe UI families fall back to {sorted(resolved)}")


def check_icons():
    for source in ICON_SOURCES:
        text = Path(source).read_text(encoding="utf-8")
        for match in IMAGE_PATH.finditer(text):
            path = next(group for group in match.groups() if group)
            if path.startswith(":"):  # a Qt resource, not a file
                continue
            expect(Path(path).is_file(), f"{source} names {path}, which is not a file")


HIGHLIGHT = "rgb(91,90,90)"


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
        frame = button.replace("bn_", "frame_")
        expect(
            HIGHLIGHT in getattr(ui, frame).styleSheet(),
            f"{button} did not highlight {frame}",
        )


def check_highlight(ui):
    ui.bn_home.click()
    ui.bn_home.click()
    expect(
        HIGHLIGHT in ui.frame_home.styleSheet(),
        "clicking the current menu button removed its highlight",
    )

    def part_way():
        return 80 < ui.frame_bottom_west.width() < 160

    window = ui.toodle.window()
    ui.toodle.click()
    expect(HIGHLIGHT in ui.frame_home.styleSheet(), "the toggle did not highlight Home")
    expect(
        (window.animation.startValue(), window.animation.endValue()) == (80, 160),
        "the menu does not animate open from its narrow width to its wide one",
    )
    wait_until(part_way, 1000)
    ui.bn_bug.click()  # with the menu part of the way open, if the wait caught it
    expect(
        ui.stackedWidget.currentWidget() is ui.page_about_bug,
        "a menu button clicked part-way through the animation did not show its About page",
    )
    expect(
        HIGHLIGHT in ui.frame_bug.styleSheet(),
        "a menu button clicked part-way through the animation lost its highlight",
    )
    wait_until(lambda: ui.frame_bottom_west.width() == 160)
    ui.toodle.click()
    expect(
        (window.animation.startValue(), window.animation.endValue()) == (160, 80),
        "the menu does not animate closed from its wide width to its narrow one",
    )
    wait_until(lambda: ui.frame_bottom_west.width() == 80)
    expect(ui.frame_bottom_west.width() == 80, "the menu did not narrow again")

    ui.bn_android.click()
    ui.bn_android_game.click()
    ui.bn_android.click()
    expect(
        ui.stackedWidget_android.currentWidget() is ui.page_android_game
        and ui.lab_tab.text() == "Android > GamePad"
        and HIGHLIGHT in ui.frame_android.styleSheet(),
        "clicking Android again lost the sub-page that was showing",
    )
    ui.bn_home.click()


def shows(button, icon_path):
    return button.icon().pixmap(16, 16).toImage() == QIcon(icon_path).pixmap(16, 16).toImage()


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
    expect(ui.frame_drag.isVisible(), "the resize grip did not come back after restore")

    # The window manager can change the state behind the button's back.
    window.showMaximized()
    QApplication.processEvents()
    expect(
        ui.bn_max.toolTip() == "Restore" and not ui.frame_drag.isVisible(),
        "the maximise button did not follow a maximise it did not make",
    )
    expect(
        shows(ui.bn_max, "icons/1x/restore.png"),
        "the maximise button does not show the restore icon while maximised",
    )
    window.showNormal()
    QApplication.processEvents()
    expect(
        ui.bn_max.toolTip() == "Maximize" and ui.frame_drag.isVisible(),
        "the maximise button did not follow a restore it did not make",
    )
    expect(
        shows(ui.bn_max, "icons/1x/max.png"),
        "the maximise button does not show the maximise icon when restored",
    )

    QTest.mouseDClick(ui.frame_appname, Qt.MouseButton.LeftButton)
    wait_until(window.isMaximized)  # the double click maximises after 250 ms
    expect(window.isMaximized(), "double-clicking the title bar did not maximise")
    drag(window, ui.frame_appname)
    QApplication.processEvents()
    expect(
        not window.isMaximized() and ui.bn_max.toolTip() == "Maximize",
        "dragging a maximised window did not restore it",
    )

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
        image = grip.grab().toImage()
        colours = {
            image.pixel(x, y) for x in range(image.width()) for y in range(image.height())
        }
        expect(len(colours) > 1, "the resize grip is drawn as a blank square")
        size = window.size()
        QTest.mousePress(grip, Qt.MouseButton.LeftButton, pos=QPoint(5, 5))
        QTest.mouseMove(grip, QPoint(5, 45))
        QTest.mouseRelease(grip, Qt.MouseButton.LeftButton, pos=QPoint(5, 45))
        expect(window.size() != size, "dragging the resize grip did not resize")

    second = type(window)()
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
    expect(not ui.bn_bug_start.isEnabled(), "Start can be clicked again mid-run")
    wait_until(lambda: ui.progressBar_bug.value() == 100)
    expect(ui.progressBar_bug.value() == 100, "Start did not fill the progress bar")
    expect(ui.bn_bug_start.isEnabled(), "Start stayed disabled after the run")
    expect(
        not ui.bn_bug_start.window().bugTimer.isActive(),
        "the progress timer kept running after 100%",
    )
    # A second call while the first still runs must take over cleanly.
    ui_function.APFunction.addNumbers(ui.bn_bug_start.window(), "100000")
    ui_function.APFunction.addNumbers(ui.bn_bug_start.window(), "100000")
    expect(
        len(ui.bn_bug_start.window().findChildren(QTimer)) == 1,
        "starting the progress bar twice left more than one timer",
    )
    wait_until(lambda: ui.progressBar_bug.value() == 100)
    expect(ui.bn_bug_start.isEnabled(), "Start stayed disabled after a second run")

    window = ui.bn_cloud_connect.window()
    cloud_fields = (ui.line_cloud_id, ui.line_cloud_adress, ui.line_cloud_proxy)
    shown = len(dialogs_shown)
    ui.bn_cloud_connect.click()
    expect(
        len(dialogs_shown) == shown + 1
        and dialogs_shown[-1] is window.error
        and window.error.e.lab_heading.text() == "Incorrect Credentials",
        "Connect did not raise the error box saying Incorrect Credentials",
    )
    for field in cloud_fields:
        field.setText("x")
    ui.bn_cloud_clear.click()
    expect(
        all(field.text() == "" for field in cloud_fields),
        "Clear did not empty all three fields after a failed Connect",
    )
    ui.line_cloud_id.setText("asd")
    ui.line_cloud_adress.setText("1234")
    ui.bn_cloud_connect.click()
    expect(
        len(dialogs_shown) == shown + 1
        and ui.line_cloud_proxy.text() == "Connection established",
        "Connect with the right credentials did not report a connection",
    )

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
        frame = button.replace("bn_", "frame_")
        expect(
            HIGHLIGHT in getattr(ui, frame).styleSheet(),
            f"{button} did not highlight {frame}",
        )

    contact_fields = (
        ui.line_android_name,
        ui.line_android_adress,
        ui.line_android_org,
        ui.line_android_email,
        ui.line_android_ph,
    )
    ui.bn_android_contact_edit.click()
    expect(
        all(field.isEnabled() for field in contact_fields),
        "Edit did not enable every contact field",
    )
    ui.bn_android_contact_save.click()
    expect(
        not any(field.isEnabled() for field in contact_fields),
        "Save did not disable every contact field",
    )

    shown = len(dialogs_shown)
    ui.bn_android_contact_delete.click()
    expect(
        len(dialogs_shown) == shown + 1
        and dialogs_shown[-1] is window.diag
        and window.diag.d.lab_heading.text() == "Warning",
        "Delete did not raise the dialog box headed Warning",
    )

    for box in (ui.checkBox, ui.checkBox_2):
        name = box.objectName()
        shown = len(dialogs_shown)
        box.setChecked(True)
        expect(
            len(dialogs_shown) == shown + 1 and dialogs_shown[-1] is window.error,
            f"{name} did not raise the error box",
        )
        box.setChecked(False)
        expect(len(dialogs_shown) == shown + 1, f"unchecking {name} raised the error box")

    ui.horizontalSlider_2.setValue(ui.horizontalSlider_2.value() + 1)


def check_dialog_result(window):
    for button, expected in (("bn_east", True), ("bn_west", False), ("bn_close", False)):
        result = really_exec(
            window.diag,
            lambda: window.dialogexec("Heading", "Message", "", "No", "Yes"),
            getattr(window.diag.d, button),
        )
        expect(result is expected, f"dialogexec returned {result!r} after {button}")
    expect(
        (window.diag.d.bn_west.text(), window.diag.d.bn_east.text()) == ("No", "Yes"),
        "dialogexec put the button texts on the wrong buttons",
    )
    really_exec(window.error, lambda: window.errorexec("Heading", "", "Ok"), window.error.e.bn_ok)

    ui = window.ui
    fields = (
        ui.line_android_name,
        ui.line_android_adress,
        ui.line_android_org,
        ui.line_android_email,
        ui.line_android_ph,
    )
    for field in fields:
        field.setText("someone")
    answers.append(False)
    ui.bn_android_contact_delete.click()
    expect(
        all(field.text() == "someone" for field in fields),
        "Cancel deleted the contact anyway",
    )
    answers.append(True)
    ui.bn_android_contact_delete.click()
    expect(
        all(field.text() == "" for field in fields),
        "Yes did not empty every field of the contact",
    )


def drive(*_):
    (window,) = [
        w for w in QApplication.topLevelWidgets() if type(w).__name__ == "MainWindow"
    ]
    ui = window.ui
    expect(window.isVisible(), "main.py did not show the main window")
    expect(
        ui.lab_appname.text() == window.windowTitle() != "",
        "the title bar does not show the application name",
    )

    check_icons()
    check_fonts(window)

    pages = (
        ("bn_bug", "page_bug", "Bug"),
        ("bn_android", "page_android", "Android"),
        ("bn_cloud", "page_cloud", "Cloud"),
        ("bn_home", "page_home", "Home"),
    )
    check_menu(ui, pages, "")

    ui.toodle.click()
    wait_until(lambda: ui.frame_bottom_west.width() == 160)  # it animates open
    expect(ui.frame_bottom_west.width() == 160, "the toggle did not widen the menu")
    expect(
        ui.stackedWidget.currentWidget() is ui.page_about_home,
        "the toggle did not show the About page of Home",
    )
    about = tuple((b, p.replace("page_", "page_about_"), t) for b, p, t in pages)
    check_menu(ui, about, "About > ")
    ui.toodle.click()
    wait_until(lambda: ui.frame_bottom_west.width() == 80)
    expect(ui.frame_bottom_west.width() == 80, "the toggle did not narrow the menu")
    expect(
        ui.stackedWidget.currentWidget() is ui.page_home,
        "the toggle did not go back to the Home page",
    )

    check_highlight(ui)
    check_page_widgets(ui)
    check_dialog_result(window)
    check_window_state(window)

    check_drag("main window", window, ui.frame_appname)
    check_drag("dialog box", window.diag, window.diag.d.frame_top)
    check_drag("error box", window.error, window.error.e.frame_top)

    ui.bn_close.click()
    expect(not window.isVisible(), "the close button did not close the window")

    QApplication.processEvents()
    drove.append(True)
    return 0


def fake_exec(dialog):
    dialogs_shown.append(dialog)
    accepted = answers.pop() if answers else False
    return QDialog.DialogCode.Accepted if accepted else QDialog.DialogCode.Rejected


answers = []
real_exec = QDialog.exec
QDialog.exec = fake_exec

qInstallMessageHandler(on_qt_message)
sys.excepthook = on_exception
QApplication.exec = drive

# The verdict is given here, not through main.py's exit status: main.py may
# not pass it on, and may not reach app.exec() at all.
try:
    runpy.run_path("main.py", run_name="__main__")
except SystemExit:
    pass
except Exception:
    on_exception(*sys.exc_info())
if not drove:
    fail("the windows were not driven to the end")
for problem in problems:
    print("FAIL:", problem, file=sys.stderr)
if not problems:
    print("smoke ok")
sys.exit(1 if problems else 0)
