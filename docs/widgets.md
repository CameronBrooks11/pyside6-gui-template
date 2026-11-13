# Widgets and stylesheets

Every widget in the template is created, sized and given its icon and text in
Qt Designer. None of that appears in the Python. The Python side only says what
happens when the widget is used, and the look of every widget comes from one
stylesheet, `src/app/resources/style.qss`.

For each widget type this page gives the calls you are likely to need and
says which rules in `style.qss` style it.
[Change the look](customising.md#change-the-look) explains how the stylesheet
is organised. In the snippets, `self.ui` is the `Ui_MainWindow` instance held by
`MainWindow`, and the names come from:

```python
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QFont, QIcon
from PySide6.QtWidgets import (
    QCheckBox, QComboBox, QLineEdit, QProgressBar,
    QPushButton, QRadioButton, QScrollBar, QSlider,
)
```

The states the stylesheet produces:

![Toggle, window and push buttons](images/widgets-buttons.png)

![Menu buttons, slider, progress bar, scroll bar and text field](images/widgets-controls.png)

![Text edit with scroll bar, combo box, radio button and check box](images/widgets-text-combo.png)

## Push button

Push buttons are used in three places: the close, minimise and maximise
buttons; the menu buttons; and ordinary action buttons such as Save, Delete
and Connect.

```python
button = QPushButton(self.ui.frame_bug_main)  # create inside a frame
button.setObjectName("bn_name")
button.setMinimumSize(QSize(20, 20))
button.setMaximumSize(QSize(55, 55))
button.setEnabled(False)  # True to enable
button.setText("Start")
button.setIcon(QIcon(":/icons/home.png"))
button.setIconSize(QSize(22, 22))
button.setFlat(True)
button.setToolTip("Name")

font = QFont()
font.setFamily("Segoe UI")
font.setPointSize(12)
button.setFont(font)

button.clicked.connect(lambda: print("clicked"))
```

In `style.qss` the `QPushButton` rules style an action button (Start, Clear,
Connect, Edit, Share, Save), with `:hover`, `:pressed` and `:disabled` states.
The other kinds are told apart by a `variant` property set in Qt Designer:

| `variant` | Buttons                                | Rules                              |
| --------- | -------------------------------------- | ---------------------------------- |
| `menu`    | The side menu and the Android sub-menu | `QPushButton[variant="menu"]`      |
| `window`  | Minimise, maximise and close           | `QPushButton[variant="window"]`    |
| `danger`  | Delete, which turns red on hover       | `QPushButton[variant="danger"]`    |

The menu toggle is styled by its object name, `#toodle`. To set a variant
from Python:

```python
button.setProperty("variant", "danger")
button.style().unpolish(button)  # a widget already shown keeps its old look
button.style().polish(button)    # until it is polished again
```

Reference: [QPushButton](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QPushButton.html).

## Progress bar

```python
bar = self.ui.progressBar_bug
bar.setRange(0, 100)  # or setMinimum() and setMaximum()
bar.setValue(22)  # call this from your own code as the work advances
bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
bar.setTextVisible(True)  # show the percentage
bar.setOrientation(Qt.Orientation.Horizontal)
bar.setInvertedAppearance(False)
```

Styled by the `QProgressBar` and `QProgressBar::chunk` rules in `style.qss`.

Reference: [QProgressBar](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QProgressBar.html).

## Combo box

```python
combo = self.ui.comboBox_bug
combo.addItem("10000")  # append an item
combo.setItemText(0, "100")  # replace the text of the item at an index
combo.currentIndex()  # index of the item shown
combo.currentText()  # its text
combo.setMaximumSize(QSize(16777215, 25))  # 16777215 is Qt's "no limit"
```

Styled by the `QComboBox` rules in `style.qss`, with
`QComboBox QAbstractItemView` for the list it drops down. The arrow is the
resource `:/icons/dropdown.png`.

See [Add an icon](customising.md#add-an-icon) for how resources work.

Reference: [QComboBox](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QComboBox.html).

## Radio button

```python
radio = self.ui.radioButton
radio.setAutoExclusive(True)  # one of the group at a time
radio.isChecked()
radio.toggled.connect(lambda checked: print(checked))
```

Styled by the `QRadioButton` and `QRadioButton::indicator` rules in
`style.qss`.

Reference: [QRadioButton](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QRadioButton.html).

## Check box

```python
box = self.ui.checkBox
box.setTristate(False)  # True adds a third, partially checked state
box.isChecked()
box.toggled.connect(lambda checked: print(checked))  # True when it becomes checked
```

Styled by the `QCheckBox` and `QCheckBox::indicator` rules in `style.qss`.

Reference: [QCheckBox](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QCheckBox.html).

## Slider

```python
slider = self.ui.verticalSlider
slider.setTracking(True)  # emit valueChanged while dragging
slider.setOrientation(Qt.Orientation.Vertical)
slider.setInvertedAppearance(False)
slider.setInvertedControls(False)
slider.setValue(5)
slider.value()  # the value at the moment of the call
slider.valueChanged.connect(lambda value: print(value))
```

Styled by the `QSlider::groove`, `::handle`, `::add-page` and `::sub-page`
rules in `style.qss`, one set for each orientation.

Reference: [QSlider](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QSlider.html).

## Scroll bar

A scroll bar placed in Qt Designer can replace the built-in one of a text edit
or any other scroll area:

```python
self.ui.textEdit_gamepad.setVerticalScrollBar(self.ui.vsb_gamepad)
```

`ExamplePages.__init__` already makes this call for `textEdit_gamepad` and
`text_about_home`. Make it once per scroll bar: the text edit takes ownership
of the bar and deletes the one it had before, so handing it the same bar a
second time crashes.

Styled by the `QScrollBar:vertical` rules in `style.qss`.

Reference: [QScrollBar](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QScrollBar.html).

## Line edit

```python
line = self.ui.line_cloud_id
line.setText("test")
line.text()  # what the user entered, as a str
line.setEnabled(True)
line.setEchoMode(QLineEdit.EchoMode.Password)  # mask the input
line.setMinimumSize(QSize(400, 25))
line.setMaximumSize(QSize(500, 25))
```

Styled by the `QLineEdit` and `QLineEdit:disabled` rules in `style.qss`.

Reference: [QLineEdit](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QLineEdit.html).

## Label and group box

`QLabel` and `QGroupBox` have one rule each in `style.qss`; `QTextEdit` has
one for its text and background colours.
