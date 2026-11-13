"""The main window: a sidebar that switches between pages."""

from pathlib import Path

from PySide6.QtCore import QByteArray, QEvent, QSettings
from PySide6.QtGui import QCloseEvent, QIcon
from PySide6.QtWidgets import QListWidgetItem, QMainWindow, QMessageBox, QWidget

from app import APP_NAME
from app.contacts import EXAMPLES, Contact, ContactsModel
from app.pages.form import FormPage
from app.pages.home import HomePage
from app.pages.settings import SettingsPage
from app.pages.table import TablePage
from app.pages.task import TaskPage
from app.ui.ui_main_window import Ui_MainWindow

ICONS = Path(__file__).parent / "icons"

# The sidebar. palette() takes the theme's colours, so this needs none of its own.
NAVIGATION_STYLE = """
QListWidget { background: palette(base); border: none; outline: 0; padding: 8px 0; }
QListWidget::item { padding: 9px 12px; border-left: 3px solid transparent; }
QListWidget::item:hover { background: palette(alternate-base); }
QListWidget::item:selected {
    background: palette(alternate-base);
    border-left: 3px solid palette(highlight);
    color: palette(text);
}
"""

ABOUT = f"<p><b>{APP_NAME}</b></p><p>A PySide6 desktop application to start your own from.</p>"


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(APP_NAME)

        self.contacts = ContactsModel(EXAMPLES, self)
        self.form_page = FormPage()
        self.table_page = TablePage(self.contacts)
        self.task_page = TaskPage()
        self.settings_page = SettingsPage()

        # To add a page: make its widget and give it a line here.
        self.ui.navigation.setStyleSheet(NAVIGATION_STYLE)
        self._add_page("Home", "home.svg", HomePage())
        self._add_page("Form", "form.svg", self.form_page)
        self._add_page("Table", "table.svg", self.table_page)
        self._add_page("Task", "task.svg", self.task_page)
        self._add_page("Settings", "settings.svg", self.settings_page)
        self.ui.navigation.currentRowChanged.connect(self.ui.pages.setCurrentIndex)
        self.ui.navigation.setCurrentRow(0)

        self.form_page.submitted.connect(self._add_contact)
        self.ui.action_quit.triggered.connect(self.close)
        self.ui.action_about.triggered.connect(self.show_about)

        geometry = QSettings().value("geometry")
        if isinstance(geometry, QByteArray):
            self.restoreGeometry(geometry)

    def show_about(self) -> None:
        QMessageBox.about(self, f"About {APP_NAME}", ABOUT)

    def changeEvent(self, event: QEvent) -> None:
        # A stylesheet reads palette() once, so set it again when the theme changes.
        if event.type() == QEvent.Type.PaletteChange:
            self.ui.navigation.setStyleSheet(NAVIGATION_STYLE)
        super().changeEvent(event)

    def closeEvent(self, event: QCloseEvent) -> None:
        self.task_page.stop()
        QSettings().setValue("geometry", self.saveGeometry())
        super().closeEvent(event)

    def _add_page(self, title: str, icon: str, page: QWidget) -> None:
        QListWidgetItem(QIcon(str(ICONS / icon)), title, self.ui.navigation)
        self.ui.pages.addWidget(page)

    def _add_contact(self, contact: Contact) -> None:
        self.contacts.add(contact)
        self.ui.status_bar.showMessage(f"Saved {contact.name}", 5000)
