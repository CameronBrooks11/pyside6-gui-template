# pyside6-gui-template

A desktop application to start your own from: PySide6 (Qt 6), laid out in
Qt Designer, for Windows, Linux and macOS.

It is an ordinary Qt main window with a menu bar, a status bar, a sidebar and
a stack of pages, and each example page shows one thing most applications
need:

- **Form**: input, validation with an inline message, and a confirmation
  before discarding what was typed.
- **Table**: a `QAbstractTableModel` in a `QTableView`, with sorting, a
  filter, and deleting the selected rows.
- **Task**: long work on a `QThread` with a progress bar and a cancel button,
  so the window stays responsive.
- **Settings**: a light and a dark theme, applied at once and remembered
  between runs.

Documentation: <https://cameronbrooks11.github.io/pyside6-gui-template/>, built
from [`docs/`](docs/index.md).

## Quick start

With [uv](https://docs.astral.sh/uv/) and [just](https://just.systems/):

```sh
just setup   # install the app, PySide6 and the dev tools into .venv
just run     # launch the GUI
```

Without just, run `uv sync` and then `uv run python -m app`, or `uv run app`.
Without uv, `pip install -e .` in an environment of your own and run
`python -m app`.

`just check` runs the formatter, the linter and the type checker without
changing anything; `just fmt` applies the formatting. `just test` runs the
tests in `tests/` with pytest and pytest-qt on Qt's offscreen platform, so it
needs no display. A Python or Qt warning raised while a test runs fails it,
as a failed assertion does. The tests do not show what the GUI looks like.

## Layout

The application is the `app` package in `src/app/`. Rename it to your own.

| File                     | Purpose                                                        |
| ------------------------ | -------------------------------------------------------------- |
| `src/app/__init__.py`    | The application and organisation names                         |
| `src/app/__main__.py`    | Entry point for `python -m app` and the `app` command          |
| `src/app/main_window.py` | The main window: sidebar, pages, menu, saved window size       |
| `src/app/pages/`         | One module per page; replace with your own                     |
| `src/app/contacts.py`    | The example data and its table model                           |
| `src/app/worker.py`      | The example long task, which runs on a second thread           |
| `src/app/theme.py`       | The light and dark palettes, and the saved choice              |
| `src/app/ui/*.ui`        | Qt Designer forms, one per window or page                      |
| `src/app/ui/ui_*.py`     | Generated from the `.ui` files; do not edit by hand            |
| `tests/`                 | The tests behind `just test`                                   |
| `docs/`, `mkdocs.yml`    | The documentation site                                         |

## Making it yours

1. Set `APP_NAME` and `ORGANISATION` in `src/app/__init__.py`. Qt uses the
   two to decide where the saved theme and window size are kept.
2. To change a page, open its form in Qt Designer
   (`uv run pyside6-designer src/app/ui/form_page.ui`), run `just uic` to
   regenerate the `ui_*.py` modules, and wire the widgets up in the page's
   module in `src/app/pages/`. `just test` fails when a generated module is
   out of date with its form, as long as the installed PySide6 is the version
   that generated it; the lock file keeps the two the same.
3. To add a page, make a form and a module for it the same way and give it a
   line in `MainWindow.__init__`, which lists the pages in sidebar order.
4. Change the colours in `src/app/theme.py`. The application uses Qt's Fusion
   style, which draws every widget from the palette, so there is no
   stylesheet.
5. Set `name`, `description` and `version` in `pyproject.toml`, then run
   `uv lock`: the lock file records the project's name and version, and CI
   installs with `uv sync --locked`, which refuses a lock that is out of date.
6. Rename the `app` package: the `src/app/` directory, the imports of `app` in
   `src/` and `tests/`, the `[project.scripts]` line and `module-name` in
   `pyproject.toml`, and the paths in the `run` and `uic` recipes of the
   justfile.
7. Keep the notices in `LICENSE`, which the MIT terms require of copies, and
   add your own copyright line.
8. Replace this README and `docs/` with your own, and set `site_name`,
   `site_description`, `site_url`, `repo_url` and `repo_name` in `mkdocs.yml`.
   If you do not want a docs site, delete `docs/`, `mkdocs.yml` and
   `.github/workflows/docs.yml`, the `docs` and `docs-build` recipes in the
   justfile, the Docs step in `.github/workflows/check.yml` and the `docs`
   group in `pyproject.toml`, then run `uv lock`.
9. `.github/workflows/check.yml` runs `just check`, `just test` and
   `just docs-build` on every pull request into `main`. It and `docs.yml` ask
   for Python 3.10, the oldest version `requires-python` allows: change both
   if you raise that floor.

## License

MIT. See [LICENSE](LICENSE).

## Credits

This began as a PySide6 port of
[Minimalistic-Flat-Modern-GUI-Template](https://github.com/anjalp/Minimalistic-Flat-Modern-GUI-Template)
by [Anjal.P](https://github.com/anjalp), and has since been rewritten. The
current application, tests, documentation site and tooling are by
[Cameron Brooks](https://github.com/CameronBrooks11).
