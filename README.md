# pyside6-gui-template

A flat, frameless desktop GUI to start a Python application from: PySide6
(Qt 6), laid out in Qt Designer, for Windows, Linux and macOS.

<p align="center">
  <img src="docs/images/home.png" alt="Home page of the template">
</p>

It is a PySide6 port of
[Minimalistic-Flat-Modern-GUI-Template](https://github.com/anjalp/Minimalistic-Flat-Modern-GUI-Template)
by Anjal.P, which targets PySide2. The design, the layouts and the guide the
documentation is converted from are theirs.

Documentation: <https://cameronbrooks11.github.io/pyside6-gui-template/>, built
from [`docs/`](docs/index.md).

## What is in it

- Frameless window with its own title bar: drag, minimise, maximise, restore
  and close.
- Side menu with four example pages (Home, Bug, Android, Cloud) on a stacked
  widget, and a toggle that widens the menu and swaps each page for its About
  page.
- Styled widgets: push buttons, progress bar, radio buttons, check boxes, line
  and text edits, sliders, vertical scroll bars, combo box.
- A dialog box and an error box, each called with one function that sets the
  heading, message, icon and button text.

## Quick start

With [uv](https://docs.astral.sh/uv/) and [just](https://just.systems/):

```sh
just setup   # install PySide6 into .venv
just run     # launch the GUI
```

Without them, install `pyside6` 6.7 or newer and run `python main.py` from the
repository root. The icons load by relative path, so the working directory has
to be the root.

`just check` builds every window on Qt's offscreen platform and clicks through
the pages, the menu toggle, the window buttons and the example widgets. It
fails on a Python or Qt warning (a deprecated Qt call included), an exception
in a slot, a page that does not switch, and an icon path with no file behind
it. It does not show what the GUI looks like.

## Layout

| File                                             | Purpose                                                            |
| ------------------------------------------------ | ------------------------------------------------------------------ |
| `main.py`                                        | Entry point: the main window, the dialog box and the error box     |
| `ui_function.py`                                 | Behaviour: menu, page switching, window controls, widget handlers  |
| `about.py`                                       | Text shown in the About panel of each page                         |
| `ui_main.ui`, `ui_dialog.ui`, `ui_error.ui`      | Qt Designer sources                                                |
| `ui_main.py`, `ui_dialog.py`, `ui_error.py`      | Generated from the `.ui` files; do not edit by hand                |
| `icons/`                                         | Icons the application loads at run time                            |
| `css.txt`                                        | Reference copy of the stylesheets set in the `.ui` files; not loaded |
| `docs/`, `mkdocs.yml`                            | The documentation site: layout, widget names, stylesheets          |
| `smoke.py`                                       | The check behind `just check`                                      |

## Making it yours

1. Open a `.ui` file in Qt Designer (`uv run pyside6-designer`) and change the
   layout.
2. Run `just uic` to regenerate the matching `ui_*.py`.
3. Wire the widgets up in `main.py` and `ui_function.py`.
   `UIFunction.stackPage` in `ui_function.py` wires up the example pages and
   is the place to copy from.
4. Set the application name in `MainWindow.__init__` in `main.py`.
5. Set `name`, `description` and `version` in `pyproject.toml`.
6. Keep `LICENSE` with its Anjal.P notice, which the MIT terms require of
   copies, and add your own copyright line to it.
7. Replace this README and `docs/` with your own, and set `site_name`,
   `site_description`, `site_url`, `repo_url` and `repo_name` in `mkdocs.yml`.
   If you do not want a docs site, delete `docs/`, `mkdocs.yml` and
   `.github/workflows/docs.yml`, the `docs` and `docs-build` recipes in the
   justfile and the `docs` group in `pyproject.toml`. The comments at the top
   of `main.py`, `ui_function.py` and `css.txt` and one in
   `MainWindow.__init__` point into `docs/`.

The documentation covers each of these steps:
[the object name of every widget](docs/layout.md),
[adding a menu button, a page or a widget](docs/customising.md), and
[the calls and stylesheet for each widget type](docs/widgets.md).
`just docs` serves it locally.

<p align="center">
  <img src="docs/images/layout/main-window-annotated.png" alt="Main window with object names">
</p>

## License

MIT, copyright 2020 Anjal.P. See [LICENSE](LICENSE).
