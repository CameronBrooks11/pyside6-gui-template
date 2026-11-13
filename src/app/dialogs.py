"""The dialog box and the error box.

Both are built from their own .ui files and filled in per call: the main
window keeps one of each and reuses it.
"""

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QDialog

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

        # Closing the box counts as the left-hand answer.
        self.ui.bn_east.clicked.connect(self.accept)
        self.ui.bn_west.clicked.connect(self.reject)

    def set_content(self, heading, message, icon, no_text, yes_text):
        self.setWindowTitle(heading)
        self.ui.lab_heading.setText(heading)
        self.ui.lab_message.setText(message)
        self.ui.bn_west.setText(no_text)
        self.ui.bn_east.setText(yes_text)
        self.ui.lab_icon.setPixmap(QPixmap(icon))

    def ask(self, heading, message, icon, no_text, yes_text):
        """Show the box and block until it is answered. Return True when the
        right-hand button, labelled `yes_text`, was pressed."""
        self.set_content(heading, message, icon, no_text, yes_text)
        # The keyboard starts on the left-hand answer, so that a stray Space
        # does not confirm.
        self.ui.bn_west.setFocus()
        return self.exec() == QDialog.DialogCode.Accepted


class ErrorBox(QDialog):
    """A notice with a heading, an icon and one button."""

    def __init__(self, parent=None):
        super().__init__(parent)
        set_font_fallbacks()
        self.ui = Ui_Error()
        self.ui.setupUi(self)
        self.ui.frame.setStyleSheet(load_style())

        self.ui.bn_ok.clicked.connect(self.close)

    def set_content(self, heading, icon, button_text):
        self.setWindowTitle(heading)
        self.ui.lab_heading.setText(heading)
        self.ui.bn_ok.setText(button_text)
        self.ui.lab_icon.setPixmap(QPixmap(icon))

    def show_error(self, heading, icon, button_text):
        """Show the box and block until it is closed."""
        self.set_content(heading, icon, button_text)
        self.exec()
