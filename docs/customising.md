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

7. Add the button to the `pages` tuple in `smoke.py` so `just check` clicks it.

## Add a sub-page to the Android page

The Android page has its own stacked widget and button row. Add a frame and a
button to `frame_android_menu` and a page to `stackedWidget_android` the same
way, connect the button in `UIFunction.stackPage`, and add a branch to
`UIFunction.androidStackPages`.

## Add a widget

Copy the widget you want in Qt Designer, paste it where it should go, and set
its size, alignment, stylesheet and object name in the Property Editor. Run
`just uic`, then connect it. `UIFunction.stackPage` in `ui_function.py` is
where the existing page widgets are connected:

```python
self.ui.bn_cloud_clear.clicked.connect(lambda: APFunction.cloudClear(self))
```

`APFunction` in the same file holds what the example buttons do. Replace its
methods with your own application's.

[Widgets and stylesheets](widgets.md) lists the calls and the stylesheet for
each widget type.

## Call the dialog box

`MainWindow.dialogexec` sets the heading, the message, the icon and the text
of the two buttons, then shows the box and blocks until it is closed:

```python
self.dialogexec(
    "Warning",
    "The contact information will be deleted. Do you want to continue?",
    "icons/1x/errorAsset 55.png",
    "Cancel",
    "Yes",
)
```

Both buttons close the box. To act on the choice, connect `bn_west` and
`bn_east` in `dialogUi.__init__` in `main.py`.

## Call the error box

`MainWindow.errorexec` takes the heading, the icon and the button text:

```python
self.errorexec("Incorrect Credentials", "icons/1x/errorAsset 55.png", "Retry")
```

## Change a dialog's design

Open `ui_dialog.ui` or `ui_error.ui` in Qt Designer, run `just uic`, and put
the code for it in `dialogUi` or `errorUi` in `main.py`.
