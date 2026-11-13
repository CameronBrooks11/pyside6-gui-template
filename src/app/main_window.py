"""The main window: its header, its menu and the pages behind it.

The layout comes from ui/ui_main.ui, edited in Qt Designer, and the look from
resources/style.qss. This module says what the window does. What the widgets
on the example pages do is in pages.py.
"""

from PySide6.QtCore import QEasingCurve, QPropertyAnimation
from PySide6.QtWidgets import QFrame, QMainWindow

from .dialogs import DialogBox, ErrorBox
from .pages import ExamplePages
from .theme import load_style, set_font_fallbacks
from .ui.ui_main import Ui_MainWindow

# Shown in the header of the window and given to the operating system as the
# window title.
APP_NAME = "App Name"

# The menu: for each menu button, the frame around it, its page, its About
# page and the name shown in the bottom label. Add a line here for a new menu
# button.
MENU = {
    "bn_home": ("frame_home", "page_home", "page_about_home", "Home"),
    "bn_bug": ("frame_bug", "page_bug", "page_about_bug", "Bug"),
    "bn_android": ("frame_android", "page_android", "page_about_android", "Android"),
    "bn_cloud": ("frame_cloud", "page_cloud", "page_about_cloud", "Cloud"),
}

# The Android page has a menu of its own: for each of its buttons, the frame
# around it, its page and the name shown in the bottom label.
ANDROID_MENU = {
    "bn_android_contact": ("frame_android_contact", "page_android_contact", "Contact"),
    "bn_android_game": ("frame_android_game", "page_android_game", "GamePad"),
    "bn_android_clean": ("frame_android_clean", "page_android_clean", "Clean"),
    "bn_android_world": ("frame_android_world", "page_android_world", "World"),
}

MENU_WIDTH = 80  # the width of the menu bar
MENU_WIDTH_ABOUT = 160  # its width while the About pages are shown


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        set_font_fallbacks()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.centralwidget.setStyleSheet(load_style())

        self.setWindowTitle(APP_NAME)
        self.ui.lab_appname.setText(APP_NAME)

        self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
        self.ui.lab_tab.setText("Home")
        self.select(self.ui.frame_bottom_west, self.ui.frame_home)

        self.ui.toodle.clicked.connect(self.toggle_menu)
        for button in MENU:
            getattr(self.ui, button).clicked.connect(
                lambda _checked=False, button=button: self.show_page(button)
            )
        for button in ANDROID_MENU:
            getattr(self.ui, button).clicked.connect(
                lambda _checked=False, button=button: self.show_android_page(button)
            )

        # One of each box, filled in and shown whenever it is needed.
        self.dialog = DialogBox()
        self.error_box = ErrorBox()

        self.pages = ExamplePages(self)

    # ---- The menu and the pages ----

    def about_shown(self):
        """True while the menu is widened, that is, while one of the About
        pages is the current page."""
        current = self.ui.stackedWidget.currentWidget()
        return any(current is getattr(self.ui, about) for _, _, about, _ in MENU.values())

    def toggle_menu(self):
        """Widen the menu and show the About page of Home, or narrow it again
        and go back to Home."""
        if self.about_shown():
            width = MENU_WIDTH
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
            self.ui.lab_tab.setText("Home")
        else:
            width = MENU_WIDTH_ABOUT
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_about_home)
            self.ui.lab_tab.setText("About > Home")
        self.select(self.ui.frame_bottom_west, self.ui.frame_home)

        self.animation = QPropertyAnimation(self.ui.frame_bottom_west, b"minimumWidth")
        self.animation.setDuration(300)
        self.animation.setStartValue(self.ui.frame_bottom_west.width())
        self.animation.setEndValue(width)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuart)
        self.animation.start()

    def show_page(self, button):
        """Show the page of a menu button, or its About page while the menu
        is widened, and highlight the button."""
        frame, page, about_page, title = MENU[button]
        about = self.about_shown()
        target = getattr(self.ui, about_page if about else page)

        self.select(self.ui.frame_bottom_west, getattr(self.ui, frame))

        # The button of the page already showing changes nothing else, so a
        # sub-page of Android stays where it is.
        if self.ui.stackedWidget.currentWidget() is target:
            return

        self.ui.stackedWidget.setCurrentWidget(target)
        self.ui.lab_tab.setText("About > " + title if about else title)

        if button == "bn_android" and not about:
            self.show_android_page("bn_android_contact")

    def show_android_page(self, button):
        """Show one of the pages inside the Android page."""
        frame, page, title = ANDROID_MENU[button]
        self.ui.stackedWidget_android.setCurrentWidget(getattr(self.ui, page))
        self.ui.lab_tab.setText("Android > " + title)
        self.select(self.ui.frame_android_menu, getattr(self.ui, frame))

    def select(self, container, frame):
        """Mark `frame` as the selected one among the frames inside
        `container`, and the rest as not selected.

        The look of each is in style.qss, under QFrame[selected=...]. A widget
        has to be polished again for a changed property to show.
        """
        for each in container.findChildren(QFrame):
            if each.property("selected") is not (each is frame):
                each.setProperty("selected", each is frame)
                each.style().unpolish(each)
                each.style().polish(each)
