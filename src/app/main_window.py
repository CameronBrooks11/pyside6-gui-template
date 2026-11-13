"""The main window: a sidebar that switches between pages."""

from PySide6.QtCore import QByteArray, QSettings
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QListWidgetItem, QMainWindow, QMessageBox, QStyle, QWidget

from app import APP_NAME
from app.contacts import EXAMPLES, Contact, ContactsModel
from app.pages.form import FormPage
from app.pages.home import HomePage
from app.pages.settings import SettingsPage
from app.pages.table import TablePage
from app.pages.task import TaskPage
from app.ui.ui_main_window import Ui_MainWindow

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
        icon = QStyle.StandardPixmap
        self._add_page("Home", icon.SP_DirHomeIcon, HomePage())
        self._add_page("Form", icon.SP_FileIcon, self.form_page)
        self._add_page("Table", icon.SP_FileDialogDetailedView, self.table_page)
        self._add_page("Task", icon.SP_BrowserReload, self.task_page)
        self._add_page("Settings", icon.SP_ComputerIcon, self.settings_page)
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

    def closeEvent(self, event: QCloseEvent) -> None:
        self.task_page.stop()
        QSettings().setValue("geometry", self.saveGeometry())
        super().closeEvent(event)

    def _add_page(self, title: str, icon: QStyle.StandardPixmap, page: QWidget) -> None:
        QListWidgetItem(self.style().standardIcon(icon), title, self.ui.navigation)
        self.ui.pages.addWidget(page)

    def _add_contact(self, contact: Contact) -> None:
        self.contacts.add(contact)
        self.ui.status_bar.showMessage(f"Saved {contact.name}", 5000)
