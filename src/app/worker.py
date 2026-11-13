"""Long work that runs on a second thread and reports back with signals."""

import threading
import time

from PySide6.QtCore import QObject, Signal, Slot


class Worker(QObject):
    progress = Signal(int)  # steps done so far
    finished = Signal(bool)  # True when it ran to the end, False when cancelled

    def __init__(self, steps: int, step_seconds: float) -> None:
        super().__init__()
        self._steps = steps
        self._step_seconds = step_seconds
        self._cancelled = threading.Event()

    @Slot()
    def run(self) -> None:
        for step in range(1, self._steps + 1):
            if self._cancelled.is_set():
                self.finished.emit(False)
                return
            time.sleep(self._step_seconds)  # stands in for one piece of real work
            self.progress.emit(step)
        self.finished.emit(True)

    def cancel(self) -> None:
        """Ask run() to stop at the next step. Safe to call from any thread."""
        self._cancelled.set()
