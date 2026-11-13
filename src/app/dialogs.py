"""The dialog box and the error box.

Both are frameless like the main window, built from their own .ui files, and
filled in per call: the main window keeps one of each and reuses it.
"""

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QDialog

from .frameless import drag_by, make_frameless
from .theme import load_style, set_font_fallbacks
from .ui.ui_dialog import Ui_Dialog
from .ui.ui_error import Ui_Error


class DialogBox(QDialog):
    """A question with a heading, a message, an icon and two buttons."""

    def __init__(self, parent=None):
        super().__init__(parent)
        set_font_fallbacks()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.frame_2.setStyleSheet(load_style())
        make_frameless(self)

        # With no system title bar, the box has its own minimise and close
        # buttons. Closing counts as the left-hand answer.
        self.ui.bn_min.clicked.connect(self.showMinimized)
        self.ui.bn_close.clicked.connect(self.close)
        self.ui.bn_east.clicked.connect(self.accept)
        self.ui.bn_west.clicked.connect(self.reject)
        drag_by(self, self.ui.frame_top)

    def set_content(self, heading, message, icon, no_text, yes_text):
        self.ui.lab_heading.setText(heading)
        self.ui.lab_message.setText(message)
        self.ui.bn_west.setText(no_text)
        self.ui.bn_east.setText(yes_text)
        self.ui.lab_icon.setPixmap(QPixmap(icon))

    def ask(self, heading, message, icon, no_text, yes_text):
        """Show the box and block until it is answered. Return True when the
        right-hand button, labelled `yes_text`, was pressed."""
        self.set_content(heading, message, icon, no_text, yes_text)
        return self.exec() == QDialog.DialogCode.Accepted


class ErrorBox(QDialog):
    """A notice with a heading, an icon and one button."""

    def __init__(self, parent=None):
        super().__init__(parent)
        set_font_fallbacks()
        self.ui = Ui_Error()
        self.ui.setupUi(self)
        self.ui.frame.setStyleSheet(load_style())
        make_frameless(self)

        self.ui.bn_ok.clicked.connect(self.close)
        drag_by(self, self.ui.frame_top)

    def set_content(self, heading, icon, button_text):
        self.ui.lab_heading.setText(heading)
        self.ui.bn_ok.setText(button_text)
        self.ui.lab_icon.setPixmap(QPixmap(icon))

    def show_error(self, heading, icon, button_text):
        """Show the box and block until it is closed."""
        self.set_content(heading, icon, button_text)
        self.exec()
