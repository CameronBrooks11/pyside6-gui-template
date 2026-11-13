# Getting started

## What you need

- Python 3.10 or newer.
- Some familiarity with Qt for Python (PySide or PyQt) and with Qt Designer.
  [Resources](credits.md#resources) lists places to start if you have neither.
- [uv](https://docs.astral.sh/uv/) and [just](https://just.systems/), or a
  Python environment you manage yourself.

Qt Designer ships with PySide6 as `pyside6-designer`; there is nothing separate
to install.

## Run it

With uv and just:

```sh
just setup   # install PySide6 into .venv
just run     # launch the GUI
```

Without them, install `pyside6` 6.7 or newer and run `python main.py` from the
repository root. The icons load by relative path, so the working directory has
to be the root.

## Check it

```sh
just check
```

builds every window on Qt's offscreen platform and clicks through the pages,
the menu toggle, the window buttons and the example widgets. It fails on a
Python or Qt warning (a deprecated Qt call included), an exception in a slot,
a page that does not switch, and an icon path with no file behind it. It does
not show what the GUI looks like.

When you add a page or a button, add it to `smoke.py` so the check covers it.

## The files

| File                                        | Purpose                                                           |
| ------------------------------------------- | ----------------------------------------------------------------- |
| `main.py`                                   | Entry point: the main window, the dialog box and the error box    |
| `ui_function.py`                            | Behaviour: menu, page switching, window controls, widget handlers |
| `about.py`                                  | Text shown in the About panel of each page                        |
| `ui_main.ui`, `ui_dialog.ui`, `ui_error.ui` | Qt Designer sources                                               |
| `ui_main.py`, `ui_dialog.py`, `ui_error.py` | Generated from the `.ui` files; do not edit by hand               |
| `icons/`                                    | Icons the application loads at run time                           |
| `css.txt`                                   | The Qt stylesheets used on the widgets                            |
| `smoke.py`                                  | The check behind `just check`                                     |

`main.py` holds the three window classes: `MainWindow`, `dialogUi` and
`errorUi`. It connects the menu buttons and registers what the user enters.
`ui_function.py` is where the application acts on that: `UIFunction` holds the
window behaviour (menu toggle, page switching, maximise and restore) and
`APFunction` holds the example application logic behind the buttons on each
page. Put the code for your own application there.

## The edit loop

1. Open a `.ui` file in Qt Designer (`uv run pyside6-designer ui_main.ui`) and
   change the layout. Sizes, icons, labels, stylesheets and object names are
   all set there, so the Python side only has to say what a widget does.
2. Run `just uic` to regenerate the matching `ui_*.py`.
3. Wire the widgets up in `main.py` and `ui_function.py`.
   `UIFunction.stackPage` in `ui_function.py` has a working example for each
   page.
4. Set the application name in `MainWindow.__init__` in `main.py`.

[Customising](customising.md) walks through the common changes, and
[Layout](layout.md) gives the object name of every widget you will need to
refer to.
