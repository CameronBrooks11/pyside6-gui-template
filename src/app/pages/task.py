"""A long task on a second thread, with a progress bar and a cancel button."""

from PySide6.QtCore import QThread
from PySide6.QtWidgets import QWidget

from app.theme import make_primary
from app.ui.ui_task_page import Ui_TaskPage
from app.worker import Worker


class TaskPage(QWidget):
    step_seconds = 0.03

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_TaskPage()
        self.ui.setupUi(self)
        self._thread: QThread | None = None
        self._worker: Worker | None = None
        make_primary(self.ui.start_button)
        self.ui.start_button.clicked.connect(self.start)
        self.ui.cancel_button.clicked.connect(self.cancel)

    def is_running(self) -> bool:
        return self._thread is not None

    def start(self) -> None:
        if self.is_running():
            return
        steps = self.ui.steps_spin.value()
        self.ui.progress_bar.setRange(0, steps)
        self.ui.progress_bar.setValue(0)

        # The worker has no parent, so it can move to the thread. Its signals
        # arrive here on the GUI thread, where touching widgets is allowed.
        thread = QThread(self)
        worker = Worker(steps, self.step_seconds)
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        worker.progress.connect(self._on_progress)
        worker.finished.connect(self._on_finished)
        self._thread, self._worker = thread, worker
        thread.start()
        self._show_running(True, "Running…")

    def cancel(self) -> None:
        """Ask the task to stop; the page updates when the worker reports back."""
        if self._worker is not None:
            self._worker.cancel()
            self.ui.cancel_button.setEnabled(False)

    def stop(self) -> None:
        """Cancel and wait for the thread to end.

        Call this before the page is destroyed: Qt aborts the process when a
        QThread is deleted while it is running. MainWindow.closeEvent does.
        """
        if self._worker is not None:
            self._worker.cancel()
            self._end("Cancelled")

    def _is_current(self) -> bool:
        # A report from a task that stop() has already ended is out of date.
        return self._worker is not None and self.sender() is self._worker

    def _on_progress(self, step: int) -> None:
        if self._is_current():
            self.ui.progress_bar.setValue(step)
            self.ui.status_label.setText(f"Running… {step} of {self.ui.progress_bar.maximum()}")

    def _on_finished(self, completed: bool) -> None:
        if self._is_current():
            self._end("Finished" if completed else "Cancelled")

    def _end(self, status: str) -> None:
        thread = self._thread
        if thread is not None:
            thread.quit()
            thread.wait()
            thread.deleteLater()
        self._thread = self._worker = None
        self._show_running(False, status)

    def _show_running(self, running: bool, status: str) -> None:
        self.ui.start_button.setEnabled(not running)
        self.ui.steps_spin.setEnabled(not running)
        self.ui.cancel_button.setEnabled(running)
        self.ui.status_label.setText(status)
