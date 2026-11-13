"""Write the screenshots the documentation uses into docs/images/.

Run it with `just screenshots`. It drives the real application on Qt's
offscreen platform, so it needs no display, and it keeps its settings in a
temporary directory, so it does not touch yours.
"""

import sys
import tempfile
from pathlib import Path

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QApplication

from app import theme
from app.main_window import MainWindow

IMAGES = Path(__file__).parent / "images"
HOME, FORM, TABLE, TASK, SETTINGS = range(5)


def grab(window: MainWindow, page: int, name: str) -> None:
    window.ui.navigation.setCurrentRow(page)
    QApplication.processEvents()
    if not window.grab().save(str(IMAGES / name)):
        sys.exit(f"could not write {name}")


def main() -> None:
    app = QApplication(sys.argv)
    QApplication.setStyle("Fusion")
    IMAGES.mkdir(exist_ok=True)

    with tempfile.TemporaryDirectory() as settings_dir:
        QSettings.setDefaultFormat(QSettings.Format.IniFormat)
        QSettings.setPath(QSettings.Format.IniFormat, QSettings.Scope.UserScope, settings_dir)

        theme.apply_theme(theme.LIGHT)
        window = MainWindow()
        window.resize(820, 540)
        window.show()
        grab(window, HOME, "home.png")

        form = window.form_page.ui
        form.name_edit.setText("Margaret Hamilton")
        form.email_edit.setText("margaret@example")
        form.notes_edit.setPlainText("Led the Apollo flight software team")
        window.form_page.save()
        grab(window, FORM, "form.png")

        window.table_page.ui.filter_edit.setText("engineer")
        window.table_page.ui.table_view.selectRow(0)
        grab(window, TABLE, "table.png")

        task = window.task_page
        task.start()
        while task.ui.progress_bar.value() < 60:
            app.processEvents()
        grab(window, TASK, "task.png")
        task.stop()

        window.settings_page.ui.theme_combo.setCurrentText(theme.DARK)
        grab(window, SETTINGS, "settings-dark.png")
        grab(window, TABLE, "table-dark.png")
        window.close()


if __name__ == "__main__":
    main()
