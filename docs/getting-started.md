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
just check   # formatter, linter, type checker; changes nothing
just test    # the app itself, driven without a display
```

`just fmt` applies the formatting. `just test` builds every window on Qt's offscreen platform and clicks through the pages,
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
| `src/app/__main__.py`                       | Entry point for `python -m app` and the `app` command             |
| `src/app/main_window.py`                    | The main window: title bar, menu, switching pages                 |
| `src/app/pages.py`                          | What the widgets on the example pages do; replace with your own   |
| `src/app/dialogs.py`                        | The dialog box and the error box                                  |
| `src/app/frameless.py`                      | Dragging and the frameless window flags the three windows share   |
| `src/app/theme.py`                          | Loading `style.qss`, and the font fallbacks                       |
| `src/app/about.py`                          | Text shown in the About panel of each page                        |
| `src/app/ui/*.ui`                           | Qt Designer sources                                               |
| `src/app/ui/ui_*.py`                        | Generated from the `.ui` files; do not edit by hand               |
| `src/app/resources/style.qss`               | The one stylesheet: every colour and widget style                   |
| `src/app/resources/`                        | The icons and `resources.qrc`, the Qt resource file that lists them |
| `src/app/ui/resources_rc.py`                | The resources compiled from `resources.qrc`; do not edit by hand    |
| `smoke.py`                                  | The test behind `just test`                                      |

`MainWindow` in `main_window.py` is the window: its title bar buttons, the
menu toggle, switching pages, maximise and restore. `ExamplePages` in
`pages.py` is the example application logic behind the buttons on each page.
Put the code for your own application there.

## The edit loop

1. Open a `.ui` file in Qt Designer (`uv run pyside6-designer src/app/ui/ui_main.ui`) and
   change the layout. Sizes, icons, labels and object names are set there, so
   the Python side only has to say what a widget does. The forms look plain
   in Designer: the colours and widget styles come from
   `src/app/resources/style.qss` when the application runs.
2. Change colours and widget styles in `style.qss`; see
   [Change the look](customising.md#change-the-look).
3. Run `just uic` to regenerate the `ui_*.py` modules and `resources_rc.py`.
4. Wire the widgets up in `pages.py`. `ExamplePages.__init__` connects the
   widgets of the example pages and is the place to copy from.
5. Set the application name, `APP_NAME`, in `main_window.py`.

[Customising](customising.md) walks through the common changes, and
[Layout](layout.md) gives the object name of every widget you will need to
refer to.
