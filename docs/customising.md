# Customising

Layout changes happen in Qt Designer, followed by `just uic`. Behaviour goes in
`main.py` and `ui_function.py`. [Layout](layout.md) has the object names used
below.

## Set the application name

In `MainWindow.__init__` in `main.py`:

```python
applicationName = "App Name"
```

The name goes to the operating system as the window title and to `lab_appname`
in the custom title bar.

## Add a menu button and its page

A menu button needs two pages in `stackedWidget`: the page itself and its
About page, which is shown instead while the menu is widened.

1. Open `ui_main.ui` in Qt Designer and find `frame_bottom_west`, which holds
   the existing menu buttons. Add a frame inside it, give it a horizontal
   layout, and name it, for example `frame_settings`.
2. Copy one of the existing menu buttons into the new frame. Change its icon
   and its object name, for example `bn_settings`, in the Property Editor.
   The copy keeps the dynamic property `variant` = `menu`, which is what
   gives it the menu button style.
3. Right-click `stackedWidget`, choose Insert Page, and add two pages. Name
   them, for example `page_settings` and `page_about_settings`, and put your
   widgets on the first.
4. Run `just uic`.
5. In `MainWindow.__init__` in `main.py`, under the existing menu button
   connections, connect the new button:

    ```python
    self.ui.bn_settings.clicked.connect(
        lambda: UIFunction.buttonPressed(self, "bn_settings")
    )
    ```

6. In `ui_function.py`, add a line to `MENU` naming the frame around the
   button, the page, the About page and the name to show in the bottom label:

    ```python
    MENU = {
        ...
        'bn_settings': ('frame_settings', 'page_settings', 'page_about_settings', 'Settings'),
    }
    ```

    `UIFunction.buttonPressed` reads the table: it shows the page, or the About
    page while the menu is widened, sets the label, and gives the button's
    frame the lighter background that marks it as selected.

7. Add a `(button, page, label)` entry to the `pages` tuple in `smoke.py`, for
   example `("bn_settings", "page_settings", "Settings")`, so `just check`
   clicks it. The check finds the About page by putting `about_` after `page_`,
   and the frame by swapping `bn_` for `frame_`, so keep to those names.

## Add a sub-page to the Android page

The Android page has its own stacked widget and button row. Add a frame and a
button to `frame_android_menu` and a page to `stackedWidget_android` the same
way, connect the button in `UIFunction.stackPage`, and add a branch to
`UIFunction.androidStackPages`.

## Add a widget

Copy the widget you want in Qt Designer, paste it where it should go, and set
its size, alignment and object name in the Property Editor. Run
`just uic`, then connect it. `UIFunction.stackPage` in `ui_function.py` is
where the existing page widgets are connected:

```python
self.ui.bn_cloud_clear.clicked.connect(lambda: APFunction.cloudClear(self))
```

`APFunction` in the same file holds what the example buttons do. Replace its
methods with your own application's.

A slot runs on the GUI thread, and the window does not repaint or respond
until it returns. For work that takes time, do it in steps from a `QTimer`, as
`APFunction.addNumbers` does for the progress bar, or move it to a worker
thread.

[Widgets and stylesheets](widgets.md) lists the calls and the stylesheet for
each widget type.

## Change the look

Every colour and widget style is in `src/app/resources/style.qss`, a Qt
stylesheet that `main.py` sets on the application. The `.ui` files carry no
styles, so a form looks plain in Qt Designer and takes its look when the
application runs.

- To recolour, change the `rgb(...)` values; the comment at the top of the
  file says what each colour is used for.
- A plain `QPushButton` is an action button. A button that is something else
  says so with a dynamic property named `variant`, which you add in Qt
  Designer with the plus sign in the Property Editor (a String property):
  `menu` for the side and sub-menu buttons, `window` for minimise, maximise
  and close, `danger` for a button that turns red on hover.
- The frame around a menu button is marked with a `selected` property by
  `UIFunction.select` in `ui_function.py`; the two `QFrame[selected=...]`
  rules give the selected and unselected colours.
- A widget inside a page that needs a colour of its own gets a rule by its
  object name, for example `#frame_settings { background: ... }`.

Run `just uic` after editing the file: the stylesheet is compiled into the
resources, and `just check` fails if the compiled copy is out of date.

## Add an icon

The icons are Qt resources: `resources.qrc` lists them, `just uic` compiles
them into `resources_rc.py`, and the application refers to them by a path that
starts with `:/`, which works from any directory.

1. Put the image in `src/app/resources/icons/`.
2. Add a line for it to `src/app/resources/resources.qrc`:

    ```xml
    <file>icons/settings.png</file>
    ```

3. Run `just uic`.
4. Use it as `:/icons/settings.png`: in Qt Designer through the resource
   browser, in Python as `QIcon(":/icons/settings.png")`, in a stylesheet as
   `url(:/icons/settings.png)`.

`just check` fails if a listed file is missing, if `resources_rc.py` is out of
date with the list, or if the code names a resource that is not there.

## Call the dialog box

`MainWindow.dialogexec` sets the heading, the message, the icon and the text
of the two buttons, then shows the box and blocks until it is closed. It
returns `True` when the second, right-hand button was pressed, and `False` for
the first button or the close button:

```python
if self.dialogexec(
    "Warning",
    "The contact information will be deleted. Do you want to continue?",
    ":/icons/warning.png",
    "Cancel",
    "Yes",
):
    ...  # the user chose Yes
```

`APFunction.deleteContact` in `ui_function.py` is the working example.

## Call the error box

`MainWindow.errorexec` takes the heading, the icon and the button text:

```python
self.errorexec("Incorrect Credentials", ":/icons/warning.png", "Retry")
```

## Change a dialog's design

Open `ui_dialog.ui` or `ui_error.ui` in Qt Designer, run `just uic`, and put
the code for it in `dialogUi` or `errorUi` in `main.py`.
