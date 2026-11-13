# pyside6-gui-template

A flat, frameless desktop GUI to start a Python application from: PySide6
(Qt 6), laid out in Qt Designer, for Windows, Linux and macOS.

<p align="center">
  <img src="images/homepage.png" alt="Home page of the template">
</p>

It is a PySide6 port of
[Minimalistic-Flat-Modern-GUI-Template](https://github.com/anjalp/Minimalistic-Flat-Modern-GUI-Template)
by Anjal.P, which targets PySide2. The design, the layouts and the
documentation are theirs.

## What is in it

- Frameless window with its own title bar: drag, minimise, maximise, restore
  and close.
- Side menu with four example pages (Home, Bug, Android, Cloud) on a stacked
  widget, and a toggle that widens the menu into an About panel.
- Styled widgets: push buttons, progress bar, radio buttons, check boxes, line
  and text edits, sliders, scroll bars, combo box, text browser.
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

`just check` builds every window on Qt's offscreen platform and fails on any
warning, a deprecated Qt call included. It does not show what the GUI looks
like.

## Layout

| File                                             | Purpose                                                            |
| ------------------------------------------------ | ------------------------------------------------------------------ |
| `main.py`                                        | Entry point: the main window, the dialog box and the error box     |
| `ui_function.py`                                 | Behaviour: menu, page switching, window controls, widget handlers  |
| `about.py`                                       | Text shown in the About panel of each page                         |
| `ui_main.ui`, `ui_dialog.ui`, `ui_error.ui`      | Qt Designer sources                                                |
| `ui_main.py`, `ui_dialog.py`, `ui_error.py`      | Generated from the `.ui` files; do not edit by hand                |
| `icons/`                                         | Icons the application loads at run time                            |
| `css.txt`                                        | The Qt stylesheets used on the widgets                             |
| `Documentation.pdf`                              | Upstream's guide to the layout, widget names and stylesheets       |
| `images/`                                        | Screenshots and layout diagrams                                    |
| `smoke.py`                                       | The check behind `just check`                                      |

`main.py` and `ui_function.py` import each other. That resolves only when
`main.py` is the entry script, so run it rather than importing it.

## Making it yours

1. Open a `.ui` file in Qt Designer (`uv run pyside6-designer`) and change the
   layout.
2. Run `just uic` to regenerate the matching `ui_*.py`.
3. Wire the widgets up in `main.py` and `ui_function.py`. `main.py` carries
   commented examples for each page.
4. Set the application name in `MainWindow.__init__` in `main.py`.

`Documentation.pdf` was written for the PySide2 original. Its layout diagrams,
widget names and stylesheets apply here unchanged; where it says PySide2 or
`pyside2-uic`, read PySide6 and `pyside6-uic`.

<p align="center">
  <img src="images/layoutAsset%2097.png" alt="Layout of the main window">
</p>

## More screenshots

<p align="center">
  <img src="images/homeDetailed.png" alt="Home page, annotated">
  <img src="images/about%20pageAsset%2096.png" alt="About panel toggled open">
  <img src="images/android.png" alt="A page within a page">
  <img src="images/dialogerro.png" alt="Dialog box and error box">
  <img src="images/buttons.png" alt="Widgets">
</p>

## License

MIT, copyright 2020 Anjal.P. See [LICENSE](LICENSE).
