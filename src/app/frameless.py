"""What a window needs once it gives up the system's title bar."""

from PySide6.QtCore import Qt


def make_frameless(window):
    """Drop the system title bar and border, and let the corners show through,
    so the window is only what its own frames draw."""
    window.setWindowFlags(Qt.WindowType.FramelessWindowHint)
    window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)


def drag_by(window, handle, before_move=None):
    """Move `window` when `handle`, the frame acting as its title bar, is
    dragged with the left button.

    `before_move`, if given, is called before each move: the main window uses
    it to leave the maximised state.
    """
    window.drag_position = window.pos()

    def press(event):
        window.drag_position = event.globalPosition().toPoint()

    def move(event):
        if before_move:
            before_move()
        if event.buttons() == Qt.MouseButton.LeftButton:
            here = event.globalPosition().toPoint()
            window.move(window.pos() + here - window.drag_position)
            window.drag_position = here
            event.accept()

    handle.mousePressEvent = press
    handle.mouseMoveEvent = move
