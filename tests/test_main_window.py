from PySide6.QtCore import QSize
from PySide6.QtWidgets import QApplication, QMessageBox

from app import APP_NAME, __main__
from app.main_window import MainWindow


def test_every_sidebar_row_shows_its_own_page(window):
    navigation, pages = window.ui.navigation, window.ui.pages
    assert navigation.count() == pages.count() == 5
    assert pages.currentIndex() == 0
    for row in range(navigation.count()):
        navigation.setCurrentRow(row)
        assert pages.currentIndex() == row
    assert pages.widget(2) is window.table_page


def test_every_sidebar_row_has_an_icon(window):
    navigation = window.ui.navigation
    for row in range(navigation.count()):
        assert not navigation.item(row).icon().isNull(), navigation.item(row).text()


def test_about_names_the_application(window, monkeypatch):
    shown = []
    monkeypatch.setattr(QMessageBox, "about", lambda parent, title, text: shown.append(text))
    window.ui.action_about.trigger()
    assert len(shown) == 1 and APP_NAME in shown[0]


def test_quit_closes_the_window(window):
    window.ui.action_quit.trigger()
    assert not window.isVisible()


def test_window_size_is_restored(window, qtbot):
    window.resize(640, 480)
    window.close()
    reopened = MainWindow()
    qtbot.addWidget(reopened)
    assert reopened.size() == QSize(640, 480)


def test_main_shows_a_window_and_returns_the_exit_status(monkeypatch, qapp):
    visible = []

    def exec_(*_):
        visible.extend(w for w in QApplication.topLevelWidgets() if w.isVisible())
        return 3

    monkeypatch.setattr(QApplication, "exec", exec_)
    assert __main__.main() == 3
    assert [type(w) for w in visible] == [MainWindow]
    for widget in visible:
        widget.close()
