from PySide6.QtWidgets import QWidget

from app.ui.ui_home_page import Ui_HomePage


class HomePage(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_HomePage()
        self.ui.setupUi(self)
