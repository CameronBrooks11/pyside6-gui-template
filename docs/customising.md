# Customising

## Name it

Set `APP_NAME` and `ORGANISATION` in `src/app/__init__.py`. The first is the
window title; Qt uses the two together to decide where `QSettings` keeps the
saved theme and window size.

Set `name`, `description` and `version` in `pyproject.toml`, then run
`uv lock`: the lock file records the project's name and version, and CI
installs with `uv sync --locked`, which refuses a lock that is out of date.

To rename the `app` package, change the `src/app/` directory, the imports
that start `from app`, the `[project.scripts]` line and `module-name` in
`pyproject.toml`, and the paths in the `run` and `uic` recipes of the justfile.

## Change a page

1. Open its form in Qt Designer:
   `uv run pyside6-designer src/app/ui/form_page.ui`.
2. Give each widget you add an object name you will recognise in code, such as
   `phone_edit`.
3. Run `just uic` to regenerate the `ui_*.py` modules.
4. Use the widget in the page's module as `self.ui.phone_edit`.

`just test` fails if you forget step 3.

## Add a page

1. In Qt Designer, make a new form from the Widget template, lay it out, and
   save it as `src/app/ui/reports_page.ui`. Set the object name of the form
   itself to `ReportsPage`: the generated class is named after it.
2. Run `just uic`.
3. Write `src/app/pages/reports.py`:

    ```python
    from PySide6.QtWidgets import QWidget

    from app.ui.ui_reports_page import Ui_ReportsPage


    class ReportsPage(QWidget):
        def __init__(self, parent: QWidget | None = None) -> None:
            super().__init__(parent)
            self.ui = Ui_ReportsPage()
            self.ui.setupUi(self)
    ```

4. Give it a line in `MainWindow.__init__` in `main_window.py`, where the
   order of the lines is the order of the sidebar:

    ```python
    self._add_page("Reports", icon.SP_FileDialogContentsView, ReportsPage())
    ```

The icon is one of
[Qt's standard icons](https://doc.qt.io/qt-6/qstyle.html#StandardPixmap-enum).
To use an image of your own, pass a `QIcon` made from a file to
`QListWidgetItem` in `_add_page` instead.

To remove a page, delete its line there, its module, its form and the
generated module, and the tests that use it.

## Change the colours

The application uses Qt's Fusion style, which draws every widget from the
palette, so there is no stylesheet. `light_palette()` and `dark_palette()` in
`theme.py` each give the window, field, button and text colours, and `_ACCENT`
is the colour of selections and links in both.

To add a theme, write a function that returns its palette, add its name to
`THEMES`, and handle the name in `apply_theme`. The Settings page lists
whatever `THEMES` holds.

## Ask or tell the user something

Use Qt's own boxes. They follow the theme and behave as the system expects.

```python
answer = QMessageBox.question(self, "Clear the form", "Discard what you have typed?")
if answer == QMessageBox.StandardButton.Yes:
    ...
```

`QMessageBox.information`, `warning` and `critical` take the same arguments.
For something that needs no answer, such as "Saved", use the status bar:
`self.ui.status_bar.showMessage("Saved", 5000)` in `MainWindow`.

## Run your own long task

Anything that takes more than a moment should not run on the GUI thread, or
the window freezes until it ends. `worker.py` and `pages/task.py` show the
pattern:

- The work is a method of a `QObject` with no parent, here `Worker.run`.
- The page creates a `QThread`, moves the worker to it, and connects the
  thread's `started` signal to `run`.
- The worker never touches a widget. It emits signals, here `progress` and
  `finished`, and the page's slots update the widgets on the GUI thread.
- Cancelling sets a flag that `run` checks between steps.
- The page waits for the thread to end before letting go of it, and the main
  window's `closeEvent` calls the page's `stop()` so the application never
  exits with the thread still running.

Replace the body of `Worker.run` with your work, emitting `progress` as it
goes and checking the flag wherever it can safely stop.

## Remember a setting

```python
QSettings().setValue("theme", name)
name = QSettings().value("theme", "System")
```

`QSettings()` with no arguments uses the application and organisation names,
which `main()` sets. A value read back may be a string whatever type was
saved, so check it before use, as `saved_theme()` does.

## Test what you add

The tests in `tests/` are short and each is named for one behaviour. pytest-qt
provides `qtbot`, and `conftest.py` adds a `window` fixture, an `answer`
fixture that answers a question box without showing it, and a fixture that
keeps `QSettings` in a temporary directory.

```python
def test_clear_asks_first_and_keeps_the_text_on_no(page, answer):
    asked = answer(QMessageBox.StandardButton.No)
    fill(page)
    page.ui.clear_button.click()
    assert len(asked) == 1
    assert page.ui.name_edit.text() == "Linus"
```

## Replace the documentation

Replace the README and `docs/` with your own, and set `site_name`,
`site_description`, `site_url`, `repo_url` and `repo_name` in `mkdocs.yml`.
`just docs` serves the site locally, and `just screenshots` regenerates the
images from the application by running `docs/screenshots.py`.

If you do not want a docs site, delete `docs/`, `mkdocs.yml` and
`.github/workflows/docs.yml`, the `docs`, `docs-build` and `screenshots`
recipes in the justfile, the Docs step in `.github/workflows/check.yml` and
the `docs` group in `pyproject.toml`, then run `uv lock`.

Both workflows ask for Python 3.10, the oldest version `requires-python`
allows: change both if you raise that floor.
