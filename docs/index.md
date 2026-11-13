# pyside6-gui-template

A flat, frameless desktop GUI to start a Python application from: PySide6
(Qt 6), laid out in Qt Designer, for Windows, Linux and macOS.

![Home page of the template](images/home.png)

It is a PySide6 port of
[Minimalistic-Flat-Modern-GUI-Template](https://github.com/anjalp/Minimalistic-Flat-Modern-GUI-Template)
by Anjal.P, which targets PySide2. The design, the layouts and the guide these
pages are converted from are theirs. The port, this site and the template
tooling are by
[Cameron Brooks](https://github.com/CameronBrooks11).
See [Credits](credits.md).

## What is in it

- Flat, two-tone design with one accent colour.
- Frameless window with its own title bar: drag, minimise, maximise, restore
  and close.
- Side menu with four example pages (Home, Bug, Android, Cloud) on a stacked
  widget, and a toggle that widens the menu and swaps each page for its About
  page.
- Styled widgets: push buttons, progress bar, radio buttons, check boxes, line
  and text edits, horizontal and vertical sliders, vertical scroll bars, combo
  box.
- A dialog box with a heading, a message, an icon and two buttons you set per
  call.
- An error box with a heading, an icon and one button you set per call.

## Where to go next

| Page                                  | What it covers                                                  |
| ------------------------------------- | --------------------------------------------------------------- |
| [Getting started](getting-started.md) | Install, run, check, and what each file is for                  |
| [Gallery](gallery.md)                 | Every page, the dialog box and the error box                    |
| [Layout](layout.md)                   | Colours, fonts, and the object name of every frame and widget   |
| [Customising](customising.md)         | Adding a menu button and page, adding widgets, calling the boxes |
| [Widgets and stylesheets](widgets.md) | The calls and the Qt stylesheet for each widget type            |
| [Design approach](design-approach.md) | How the original author went from sketch to Qt Designer         |

## Tour

The home page, with the parts of the window named:

![Home page, annotated](images/home-annotated.png)

The toggle at the top left widens the menu and shows the About page of Home.
While the menu is wide, each menu button shows the About page of its page
instead of the page. Pressing the toggle again narrows the menu and goes back
to Home:

![About panel toggled open](images/about-annotated.png)

A page can hold its own stacked widget. The Android page has four sub-pages
behind a second row of buttons:

![A page within a page](images/android-annotated.png)

The dialog box and the error box:

![Dialog box and error box](images/dialog-error-annotated.png)

The styled widgets:

![Toggle, window and push buttons](images/widgets-buttons.png)

![Menu buttons, slider, progress bar, scroll bar and text field](images/widgets-controls.png)

![Text edit with scroll bar, combo box, radio button and check box](images/widgets-text-combo.png)
