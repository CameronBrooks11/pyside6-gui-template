"""Run the app as `python -m <package>` does, without a display, and drive what needs no user.

This takes over at app.exec().

Run through `just check`, from the repository root, which sets
QT_QPA_PLATFORM=offscreen and turns Python warnings into errors so a deprecated
Qt call fails here. Qt's own warnings, an exception in a slot, a page that does
not switch, a drag that does not move the window, an image path with no file or
resource behind it and a generated module that is out of date fail it too.
"""

import importlib
import re
import runpy
import shutil
import subprocess
import sys
from pathlib import Path

from PySide6.QtCore import (
    QEvent,
    QFile,
    QPoint,
    QPointF,
    Qt,
    QTimer,
    QtMsgType,
    qInstallMessageHandler,
)
from PySide6.QtGui import QColor, QFontDatabase, QFontInfo, QIcon, QMouseEvent
from PySide6.QtTest import QTest
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFrame,
    QMessageBox,
    QPushButton,
    QSizeGrip,
    QWidget,
)

# The name of the application package under src/. Change it here when you
# rename the package.
PACKAGE = "app"
SRC = f"src/{PACKAGE}"

ui_function = importlib.import_module(f"{PACKAGE}.ui_function")

UI_FILES = (f"{SRC}/ui/ui_main.ui", f"{SRC}/ui/ui_dialog.ui", f"{SRC}/ui/ui_error.ui")

# Every file that can name an image: the Designer sources, what is generated
# from them, and the Python that sets one at run time.
ICON_SOURCES = (
    f"{SRC}/main.py",
    f"{SRC}/ui_function.py",
    *UI_FILES,
    f"{SRC}/ui/ui_main.py",
    f"{SRC}/ui/ui_dialog.py",
    f"{SRC}/ui/ui_error.py",
    f"{SRC}/resources/style.qss",
)

RESOURCES = f"{SRC}/resources/resources.qrc"

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
if f"{PACKAGE}.main" in sys.modules:
    problems.append(f"importing {PACKAGE}.ui_function imported {PACKAGE}.main")

# The check reads the sources under src/, so the package it runs has to be that
# one and not a copy installed somewhere else.
if Path(ui_function.__file__).resolve().parent != Path(SRC).resolve():
    problems.append(f"the {PACKAGE} package imported is {ui_function.__file__}, not {SRC}")

# What app.exec() returns, to see that the app passes it on as its exit status.
STATUS = 7
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


# Tool, options, source, generated module: the same commands as `just uic`.
# rcc writes format version 1 because later versions record each file's
# modification time, which differs from one checkout to the next, and writes
# the files uncompressed so the result does not depend on the host's zlib.
GENERATED = (
    (
        "pyside6-rcc",
        ["--format-version", "1", "--no-compress"],
        RESOURCES,
        f"{SRC}/ui/resources_rc.py",
    ),
    *(("pyside6-uic", ["--from-imports"], ui, ui[:-3] + ".py") for ui in UI_FILES),
)

# What Qt's tools print about the host under a non-UTF-8 locale such as C.
LOCALE_NOTE = re.compile(
    r"Detected locale|Qt depends on a UTF-8 locale|If this causes problems|for more information|\s*$"
)

# The header line of a generated module that names the Qt version.
VERSION_LINE = re.compile(r"^#+ Created by: .*version")


def check_generated():
    """The generated modules must be what their sources produce now."""

    def body(text):
        return [line for line in text.splitlines() if not VERSION_LINE.match(line)]

    for tool, options, source, generated in GENERATED:
        program = shutil.which(tool, path=str(Path(sys.executable).parent)) or shutil.which(tool)
        if program is None:
            fail(f"{tool} was not found, so {generated} could not be checked against {source}")
            continue
        fresh = subprocess.run(
            [program, *options, source], capture_output=True, text=True, encoding="utf-8"
        )
        print(fresh.stderr, end="", file=sys.stderr)
        said = [line for line in fresh.stderr.splitlines() if not LOCALE_NOTE.match(line)]
        if fresh.returncode != 0:
            fail(f"{tool} failed on {source} with status {fresh.returncode}")
        elif said:
            fail(f"{tool} on {source}: {said[0]}")
        elif body(fresh.stdout) != body(Path(generated).read_text(encoding="utf-8")):
            fail(f"{generated} is out of date with {source}: run `just uic`")

    # What Qt Designer follows from a form to the icons: it has to lead to
    # the resource file.
    for ui in UI_FILES:
        text = Path(ui).read_text(encoding="utf-8")
        named = set(re.findall(r'(?:<include location|\bresource)="([^"]+)"', text))
        for location in named:
            expect(
                (Path(ui).parent / location).resolve() == Path(RESOURCES).resolve(),
                f"{ui} names the resource file {location}, which is not {RESOURCES}",
            )


def colour_at(widget, x=2, y=2):
    """The colour a widget paints at a point, as (r, g, b)."""
    return widget.grab().toImage().pixelColor(x, y).getRgb()[:3]


STYLE = f"{SRC}/resources/style.qss"


def qss_colour(selector, prop="background"):
    """The rgb() that style.qss gives `prop` in the rule listing `selector`.

    The check reads its expected colours from the stylesheet, so recolouring
    the template does not fail it; what it tests is that the rule reaches
    the widget.
    """
    text = re.sub(r"/\*.*?\*/", "", Path(STYLE).read_text(encoding="utf-8"), flags=re.S)
    colour = None
    for selectors, body in re.findall(r"([^{}]+)\{([^{}]*)\}", text):
        if selector not in [s.strip() for s in selectors.split(",")]:
            continue
        found = re.search(rf"(?:^|;)\s*{prop}(?:-color)?\s*:\s*([^;]+)", body)
        if not found:
            continue
        value = found.group(1).strip()
        numbers = re.fullmatch(r"rgba?\(([^)]*)\)", value)
        if numbers:
            parsed = QColor(*(int(n) for n in re.findall(r"\d+", numbers.group(1))[:3]))
        else:
            parsed = QColor(value)  # a name or #rrggbb
        if parsed.isValid():
            colour = parsed.getRgb()[:3]  # a later rule for the selector wins, as in Qt
    if colour is None:
        fail(f"{STYLE} has no rule that gives {selector} a {prop} this check can read")
    return colour


def check_style(window):
    """style.qss has to reach the windows, and `selected` has to show."""
    ui = window.ui
    ui.bn_home.click()
    on, off = qss_colour('QFrame[selected="true"]'), qss_colour('QFrame[selected="false"]')
    for widget, selector, what in (
        (ui.frame_top_east, "#frame_top_east", "the title bar"),
        (ui.page_home, "QStackedWidget > QWidget", "the page"),
        (ui.frame_toodle, "#frame_toodle", "the toggle"),
        (ui.frame_home, 'QFrame[selected="true"]', "the frame of the selected menu button"),
        (ui.frame_bug, 'QFrame[selected="false"]', "the frame of an unselected menu button"),
        (window.diag.d.frame_top, "QDialog #frame_top", "the bar of the dialog box"),
        (window.error.e.frame_top, "QDialog #frame_top", "the bar of the error box"),
    ):
        got, colour = colour_at(widget), qss_colour(selector)
        if colour is not None:
            expect(got == colour, f"{what} is painted {got}, not the {colour} of {selector}")
    expect(on != off, "selected and unselected menu frames have the same colour")

    text = qss_colour("QLabel", "color")
    image = ui.lab_appname.grab().toImage()
    if text is not None:
        expect(
            any(
                image.pixelColor(x, y).getRgb()[:3] == text
                for x in range(image.width())
                for y in range(image.height())
            ),
            f"no pixel of the application name has the QLabel colour {text}",
        )

    # The selection has to move, on screen as well as in the property.
    ui.bn_bug.click()
    expect(
        (colour_at(ui.frame_bug), colour_at(ui.frame_home)) == (on, off),
        "selecting another menu button did not repaint the two frames",
    )
    ui.toodle.click()
    expect(
        selected(ui.frame_home) and not selected(ui.frame_bug),
        "the toggle did not move the selection to Home",
    )
    wait_until(lambda: ui.frame_bottom_west.width() == 160)
    ui.toodle.click()
    wait_until(lambda: ui.frame_bottom_west.width() == 80)

    # Each kind of button is told apart by its `variant`. A button you add to
    # one of these four frames has to carry the variant of the frame.
    expect(
        ui.bn_android_contact_delete.property("variant") == "danger",
        "the Delete button does not have the danger variant",
    )
    for container, variant in (
        (ui.frame_bottom_west, "menu"),
        (ui.frame_android_menu, "menu"),
        (ui.frame_top_east, "window"),
        (window.diag.d.frame_top, "window"),
    ):
        for button in container.findChildren(QPushButton):
            expect(
                button.property("variant") == variant,
                f"{button.objectName()} has variant {button.property('variant')!r}, not {variant!r}",
            )

    # The stylesheet stops at the content of the app's own windows. A dialog
    # of Qt's opened from any of the three is drawn by the plain style, as
    # one with no parent is, and no sheet sits on the application.
    expect(QApplication.instance().styleSheet() == "", "a stylesheet is set on the QApplication")
    plain = QMessageBox().style().metaObject().className()
    for parent in (window, window.diag, window.error):
        box = QMessageBox(QMessageBox.Icon.NoIcon, "Title", "Some text", parent=parent)
        box.ensurePolished()
        drawn_by = box.style().metaObject().className()
        expect(
            drawn_by == plain,
            f"a QMessageBox opened from {type(parent).__name__} is drawn by {drawn_by}: "
            "style.qss reaches it",
        )
        box.deleteLater()


def check_icons():
    for source in ICON_SOURCES:
        text = Path(source).read_text(encoding="utf-8")
        for match in IMAGE_PATH.finditer(text):
            path = next(group for group in match.groups() if group)
            if path.startswith(":"):  # a Qt resource, compiled into resources_rc.py
                expect(QFile.exists(path), f"{source} names {path}, which is not a resource")
            else:
                expect(Path(path).is_file(), f"{source} names {path}, which is not a file")
    listed = re.findall(r"<file>([^<]+)</file>", Path(RESOURCES).read_text(encoding="utf-8"))
    expect(listed, f"{RESOURCES} lists no files")
    for name in listed:
        expect(
            (Path(RESOURCES).parent / name).is_file(),
            f"{RESOURCES} lists {name}, which is not a file",
        )
        expect(
            QFile.exists(":/" + name),
            f"{name} is not in resources_rc.py: run `just uic`",
        )


def selected(frame):
    """Whether a menu frame is marked as the one whose page is showing."""
    return frame.property("selected") is True


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
        marked = [f.objectName() for f in ui.frame_bottom_west.findChildren(QFrame) if selected(f)]
        expect(marked == [frame], f"{button} left {marked} selected, not only {frame}")


def check_highlight(ui):
    ui.bn_home.click()
    ui.bn_home.click()
    expect(
        selected(ui.frame_home),
        "clicking the current menu button removed its highlight",
    )

    def part_way():
        return 80 < ui.frame_bottom_west.width() < 160

    window = ui.toodle.window()
    ui.toodle.click()
    expect(selected(ui.frame_home), "the toggle did not highlight Home")
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
        selected(ui.frame_bug),
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
        and selected(ui.frame_android),
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
        shows(ui.bn_max, ":/icons/restore.png"),
        "the maximise button does not show the restore icon while maximised",
    )
    window.showNormal()
    QApplication.processEvents()
    expect(
        ui.bn_max.toolTip() == "Maximize" and ui.frame_drag.isVisible(),
        "the maximise button did not follow a restore it did not make",
    )
    expect(
        shows(ui.bn_max, ":/icons/maximize.png"),
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
        second.ui.lab_tab.text() == "Home" and selected(second.ui.frame_home),
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
        marked = [f.objectName() for f in ui.frame_android_menu.findChildren(QFrame) if selected(f)]
        expect(marked == [frame], f"{button} left {marked} selected, not only {frame}")

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
    expect(window.isVisible(), "the app did not show the main window")
    expect(
        ui.lab_appname.text() == window.windowTitle() != "",
        "the title bar does not show the application name",
    )

    check_generated()
    check_icons()
    check_style(window)
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
    return STATUS


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

# The verdict is given here, not through the app's exit status: the app may
# not pass it on, and may not reach app.exec() at all.
status = None
try:
    runpy.run_module(PACKAGE, run_name="__main__", alter_sys=True)
except SystemExit as exit_:
    status = exit_.code
except Exception:
    on_exception(*sys.exc_info())
if not drove:
    fail("the windows were not driven to the end")
elif status != STATUS:
    fail(f"app.exec() returned {STATUS} and the app exited with {status!r}")
for problem in problems:
    print("FAIL:", problem, file=sys.stderr)
if not problems:
    print("smoke ok")
sys.exit(1 if problems else 0)
