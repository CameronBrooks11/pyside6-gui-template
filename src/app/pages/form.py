"""A form: input, validation, and a confirmation before discarding."""

import re

from PySide6.QtCore import Signal
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QMessageBox, QWidget

from app.contacts import Contact
from app.ui.ui_form_page import Ui_FormPage

_EMAIL = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")


class FormPage(QWidget):
    submitted = Signal(Contact)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_FormPage()
        self.ui.setupUi(self)

        palette = self.ui.error_label.palette()
        palette.setColor(QPalette.ColorRole.WindowText, QColor(220, 60, 60))
        self.ui.error_label.setPalette(palette)

        self.ui.save_button.clicked.connect(self.save)
        self.ui.clear_button.clicked.connect(self.clear)
        self.ui.name_edit.returnPressed.connect(self.save)
        self.ui.email_edit.returnPressed.connect(self.save)

    def save(self) -> None:
        name = self.ui.name_edit.text().strip()
        email = self.ui.email_edit.text().strip()
        if not name:
            self._reject("Enter a name.", self.ui.name_edit)
            return
        if not _EMAIL.fullmatch(email):
            self._reject("Enter an email address, like name@example.com.", self.ui.email_edit)
            return
        contact = Contact(
            name, email, self.ui.role_combo.currentText(), self.ui.notes_edit.toPlainText().strip()
        )
        self._reset()
        self.submitted.emit(contact)

    def clear(self) -> None:
        if self._is_empty():
            self._reset()
            return
        answer = QMessageBox.question(self, "Clear the form", "Discard what you have typed?")
        if answer == QMessageBox.StandardButton.Yes:
            self._reset()

    def _reject(self, message: str, field: QWidget) -> None:
        self.ui.error_label.setText(message)
        field.setFocus()

    def _is_empty(self) -> bool:
        return not (
            self.ui.name_edit.text()
            or self.ui.email_edit.text()
            or self.ui.notes_edit.toPlainText()
        )

    def _reset(self) -> None:
        self.ui.name_edit.clear()
        self.ui.email_edit.clear()
        self.ui.notes_edit.clear()
        self.ui.role_combo.setCurrentIndex(0)
        self.ui.error_label.clear()
        self.ui.name_edit.setFocus()
