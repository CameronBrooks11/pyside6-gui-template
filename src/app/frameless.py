"""What a window needs once it gives up the system's title bar.

A frameless window still has to be moved and resized by the window manager,
not by the application: only then does dragging it to a screen edge snap or
tile it, and only then does the window manager keep its title bar within
reach. So the title bar and the edges here ask the window manager to start a
move or a resize, and move the window themselves only where the platform
cannot do that.
"""

from PySide6.QtCore import QEvent, QObject, QPoint, QRect, Qt
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QFrame, QWidget

# Set this to False to give every window the system's own title bar and
# border in place of the custom ones.
FRAMELESS = True

EDGE = 4  # how far in from each side of the window a resize can start
CORNER = 12  # how far along each side a corner reaches


def make_frameless(window):
    """Drop the system title bar and border, and let the corners show through,
    so the window is only what its own frames draw. Return False, and leave
    the window alone, when FRAMELESS is off."""
    if FRAMELESS:
        window.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    return FRAMELESS


def drag_by(window, handle, before_move=None):
    """Move `window` when `handle`, the frame acting as its title bar, is
    dragged with the left button.

    The window manager does the move where it can. Otherwise the window
    follows the mouse itself, and `before_move`, if given, is called before
    each move: the main window uses it to leave the maximised state, which a
    window manager does on its own.
    """
    window.drag_position = window.pos()
    # "armed": a press has come and no move has been started for it yet.
    # "handed_over": the window manager is doing the move for this press.
    state = {"armed": False, "handed_over": False}

    def press(event):
        window.drag_position = event.globalPosition().toPoint()
        state["armed"] = True
        state["handed_over"] = False

    def move(event):
        if state["handed_over"]:
            return
        left = event.buttons() == Qt.MouseButton.LeftButton
        if left and state["armed"]:
            # Ask once per press. The window manager takes the pointer, so
            # the release never arrives here, and a second request would
            # reach it after the release and start a move that nothing ends:
            # the window would follow the pointer until the next click.
            state["armed"] = False
            native = window.windowHandle()
            if native is not None and native.startSystemMove():
                state["handed_over"] = True
                event.accept()
                return
        if before_move:
            before_move()
        if left:
            here = event.globalPosition().toPoint()
            window.move(window.pos() + here - window.drag_position)
            window.drag_position = here
            event.accept()

    handle.mousePressEvent = press
    handle.mouseMoveEvent = move


class _Follow(QObject):
    """Calls `place` whenever one of the watched widgets is resized, shown or
    changes its window state."""

    def __init__(self, owner, watched, place):
        super().__init__(owner)
        self.place = place
        for widget in watched:
            widget.installEventFilter(self)
        place()

    def eventFilter(self, _watched, event):
        if event.type() in (
            QEvent.Type.Resize,
            QEvent.Type.Show,
            QEvent.Type.WindowStateChange,
        ):
            self.place()
        return False


def add_outline(window, content):
    """Draw a line around `content`, the frame that fills `window`, so the
    window has a visible edge on any background. A frameless window gets no
    border or shadow from the system. The line's look is in style.qss, under
    #window_outline."""
    outline = QFrame(content)
    outline.setObjectName("window_outline")
    outline.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

    def place():
        outline.setGeometry(content.rect())
        outline.raise_()

    _Follow(window, (window, content), place)
    return outline


class _ResizeEdge(QWidget):
    """An invisible strip along one side or corner of a window that asks the
    window manager to resize the window from there."""

    def __init__(self, window, edges, cursor):
        super().__init__(window)
        self.setObjectName("resize_edge")
        self.edges = edges
        self.setCursor(cursor)

    def mousePressEvent(self, event):
        native = self.window().windowHandle()
        if event.button() == Qt.MouseButton.LeftButton and native is not None:
            native.startSystemResize(self.edges)


def add_resize_edges(window):
    """Let `window` be resized from every side and corner, as a window with a
    system border can be. The strips are hidden while it is maximised."""
    left, right = Qt.Edge.LeftEdge, Qt.Edge.RightEdge
    top, bottom = Qt.Edge.TopEdge, Qt.Edge.BottomEdge
    horizontal, vertical = Qt.CursorShape.SizeHorCursor, Qt.CursorShape.SizeVerCursor
    falling, rising = Qt.CursorShape.SizeFDiagCursor, Qt.CursorShape.SizeBDiagCursor

    # For each strip: its edges, its cursor, and its rectangle in a window of
    # width w and height h. The corners come last so they sit on top.
    strips = [
        (left, horizontal, lambda w, h: QRect(0, 0, EDGE, h)),
        (right, horizontal, lambda w, h: QRect(w - EDGE, 0, EDGE, h)),
        (top, vertical, lambda w, h: QRect(0, 0, w, EDGE)),
        (bottom, vertical, lambda w, h: QRect(0, h - EDGE, w, EDGE)),
        (top | left, falling, lambda w, h: QRect(0, 0, CORNER, CORNER)),
        (bottom | right, falling, lambda w, h: QRect(w - CORNER, h - CORNER, CORNER, CORNER)),
        (top | right, rising, lambda w, h: QRect(w - CORNER, 0, CORNER, CORNER)),
        (bottom | left, rising, lambda w, h: QRect(0, h - CORNER, CORNER, CORNER)),
    ]
    edges = [(_ResizeEdge(window, which, cursor), rect) for which, cursor, rect in strips]

    def place():
        for edge, rect in edges:
            edge.setGeometry(rect(window.width(), window.height()))
            edge.setVisible(not window.isMaximized())
            edge.raise_()

    _Follow(window, (window,), place)


def keep_on_screen(window):
    """Move `window` to the middle of the main screen if its close button,
    near its top right corner, is on no screen."""
    button = window.frameGeometry().topRight() + QPoint(-20, 20)
    screens = QGuiApplication.screens()
    if not any(screen.availableGeometry().contains(button) for screen in screens):
        area = QGuiApplication.primaryScreen().availableGeometry()
        window.move(area.center() - window.rect().center())
