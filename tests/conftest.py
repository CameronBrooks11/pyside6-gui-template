import pytest
from PySide6.QtCore import QCoreApplication, QSettings
from PySide6.QtWidgets import QApplication, QMessageBox

from app.main_window import MainWindow


@pytest.fixture(autouse=True)
def isolated_settings(qapp, tmp_path):
    """Keep QSettings in a directory of the test's own, and undo any theme."""
    QCoreApplication.setOrganizationName("tests")
    QCoreApplication.setApplicationName("app")
    QSettings.setDefaultFormat(QSettings.Format.IniFormat)
    QSettings.setPath(QSettings.Format.IniFormat, QSettings.Scope.UserScope, str(tmp_path))
    yield
    QApplication.setPalette(QApplication.style().standardPalette())


@pytest.fixture
def window(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()
    return window


@pytest.fixture
def answer(monkeypatch):
    """Answer the next QMessageBox.question without showing it; records the calls."""
    asked = []

    def set_answer(button: QMessageBox.StandardButton):
        def question(parent, title, text, *args, **kwargs):
            asked.append(text)
            return button

        monkeypatch.setattr(QMessageBox, "question", question)
        return asked

    return set_answer
