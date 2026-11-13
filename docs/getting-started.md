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

Without just, run `uv sync` and then `uv run python -m app`, or `uv run app`.
Without uv, `pip install -e .` in an environment of your own and run
`python -m app`. The icons are compiled into the package, so it runs from any
directory.

## Check it

```sh
just check
```

builds every window on Qt's offscreen platform and clicks through the pages,
the menu toggle, the window buttons and the example widgets. It fails on a
Python or Qt warning (a deprecated Qt call included), an exception in a slot,
a page that does not switch, an icon path with no file or resource behind it,
and a generated module that is out of date with its `.ui` or `.qrc` source. It
does not show what the GUI looks like.

When you add a page or a button, add it to `smoke.py` so the check covers it.

## The files

The application is the `app` package in `src/app/`. Rename it to your own.
The other pages name its files without the directory.

| File                                        | Purpose                                                           |
| ------------------------------------------- | ----------------------------------------------------------------- |
| `src/app/__main__.py`                       | Entry point for `python -m app`                                   |
| `src/app/main.py`                           | The main window, the dialog box, the error box, and `main()`      |
| `src/app/ui_function.py`                    | Behaviour: menu, page switching, window controls, widget handlers |
| `src/app/about.py`                          | Text shown in the About panel of each page                        |
| `src/app/ui/*.ui`                           | Qt Designer sources                                               |
| `src/app/ui/ui_*.py`                        | Generated from the `.ui` files; do not edit by hand               |
| `src/app/resources/`                        | The icons and `resources.qrc`, the Qt resource file that lists them |
| `src/app/ui/resources_rc.py`                | The icons compiled from `resources.qrc`; do not edit by hand        |
| `css.txt`                                   | Reference copy of the stylesheets set in the `.ui` files; not loaded |
| `smoke.py`                                  | The check behind `just check`                                     |

`main.py` holds the three window classes: `MainWindow`, `dialogUi` and
`errorUi`. It connects the menu buttons and registers what the user enters.
`ui_function.py` is where the application acts on that: `UIFunction` holds the
window behaviour (menu toggle, page switching, maximise and restore) and
`APFunction` holds the example application logic behind the buttons on each
page. Put the code for your own application there.

## The edit loop

1. Open a `.ui` file in Qt Designer (`uv run pyside6-designer src/app/ui/ui_main.ui`) and
   change the layout. Sizes, icons, labels, stylesheets and object names are
   all set there, so the Python side only has to say what a widget does.
2. Run `just uic` to regenerate the `ui_*.py` modules and `resources_rc.py`.
3. Wire the widgets up in `main.py` and `ui_function.py`.
   `UIFunction.stackPage` in `ui_function.py` wires up the example pages and
   is the place to copy from.
4. Set the application name in `MainWindow.__init__` in `main.py`.

[Customising](customising.md) walks through the common changes, and
[Layout](layout.md) gives the object name of every widget you will need to
refer to.
