# Getting started

## What you need

- Python 3.10 or newer.
- [uv](https://docs.astral.sh/uv/) and [just](https://just.systems/), or a
  Python environment you manage yourself.

Qt Designer ships with PySide6 as `pyside6-designer`; there is nothing separate
to install.

## Run it

With uv and just:

```sh
just setup   # install the app, PySide6 and the dev tools into .venv
just run     # launch the GUI
```

Without just, run `uv sync` and then `uv run python -m app`, or `uv run app`.
Without uv, `pip install -e .` in an environment of your own and run
`python -m app`.

## Check it

```sh
just check   # formatter, linter, type checker; changes nothing
just test    # the tests, run without a display
```

`just fmt` applies the formatting. `just test` runs the tests in `tests/` with
pytest and [pytest-qt](https://pytest-qt.readthedocs.io/) on Qt's offscreen
platform. They click the buttons and read the widgets of the real pages. A
Python or Qt warning raised while a test runs fails it, as a failed assertion
does, and one test fails when a generated `ui_*.py` module is out of date with
its form. Where the installed PySide6 is not the version that generated the
modules, that test skips, or fails in CI. The tests do not show what the GUI
looks like.

A pull request into `main` runs `just check`, `just test` and
`just docs-build` in GitHub Actions.

## The files

The application is the `app` package in `src/app/`.

| File                     | Purpose                                                  |
| ------------------------ | -------------------------------------------------------- |
| `src/app/__init__.py`    | The application and organisation names                   |
| `src/app/__main__.py`    | Entry point for `python -m app` and the `app` command    |
| `src/app/main_window.py` | The main window: sidebar, pages, menu, saved window size |
| `src/app/pages/`         | One module per page                                      |
| `src/app/contacts.py`    | The example data and its table model                     |
| `src/app/worker.py`      | The example long task, which runs on a second thread     |
| `src/app/theme.py`       | The light and dark palettes, and the saved choice        |
| `src/app/ui/*.ui`        | Qt Designer forms, one per window or page                |
| `src/app/ui/ui_*.py`     | Generated from the `.ui` files; do not edit by hand      |
| `tests/`                 | The tests behind `just test`                             |
| `docs/`, `mkdocs.yml`    | This site                                                |

## How a page is put together

Every page is the same three pieces:

1. A form, `ui/<name>_page.ui`, drawn in Qt Designer. It holds the layout, the
   labels and the object name of each widget, and no colours.
2. A generated module, `ui/ui_<name>_page.py`, which `just uic` writes from
   the form.
3. A class in `pages/<name>.py` that builds the form and says what the widgets
   do:

```python
class SettingsPage(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_SettingsPage()
        self.ui.setupUi(self)
        self.ui.theme_combo.addItems(THEMES)
        self.ui.theme_combo.setCurrentText(saved_theme())
        self.ui.theme_combo.currentTextChanged.connect(self._set_theme)
```

The widgets are reached through `self.ui`, by the object names given in
Designer. `MainWindow.__init__` creates each page and adds it to the sidebar.
